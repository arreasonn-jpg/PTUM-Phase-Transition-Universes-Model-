#!/usr/bin/env python3
"""
PTUM Task 1: Tachyonic-to-Quartic Transition Numerical Simulation

This module is a homogeneous two-field truncation of the PTUM
discharge sector. It evolves only the fuel field Phi and proxy field psi.
The Friedmann source is rho_Phi + rho_psi; dark matter chi, residual
dark energy Phi_res, Standard Model radiation, fermions, and their
backreaction are NOT integrated here. It therefore tests the local
two-field tachyonic-to-quartic dynamics, not the complete cosmological
history or the post-discharge relic abundance.

Equations (from the revised hybrid-waterfall action in main.tex):
  Phi_ddot + 3H Phi_dot + dV_eff/dPhi
      + (alpha m_psi^2/E_th^2) Phi psi^2 = 0
  psi_ddot + 3H psi_dot
      + m_psi^2(alpha Phi^2/E_th^2 - 1)psi
      + lambda_psi psi^3 = 0
  H^2 = (rho_Phi + rho_psi)/(3 M_Pl^2)

The waterfall mass is positive for |Phi| > Phi_c and tachyonic for
|Phi| < Phi_c. The interaction potential is
U_int = +alpha*m_psi^2*Phi^2*psi^2/(2 E_th^2), assigned once to rho_psi.

Energy densities (interaction potential assigned once, to psi):
  rho_Phi = 1/2 Phi_dot^2 + V_eff(Phi)
  rho_psi = 1/2 psi_dot^2 + 1/2 m_eff^2(Phi) psi^2
            + 1/4 lambda_psi psi^4

Diagnostics:
  Q = lambda_psi <psi^4> / <|m_eff^2(Phi)| psi^2>, per half-cycle
  R_vir = <K> / (2<V_4>), tending to 1 for quartic oscillations
  C_FRW = d rho_total/dt + 3H(rho_total+p_total)
"""

import numpy as np
from scipy.integrate import solve_ivp, quad_vec
from scipy.optimize import brentq
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Callable
import json
import os
import math

# Physical constants (natural units: c = ħ = k_B = 1)
M_PL = 2.435e18  # GeV (reduced Planck mass)
GEV_TO_S = 6.582e-25  # 1 GeV^-1 = 6.582e-25 s


class RHSWorkBudgetExceeded(RuntimeError):
    """Deterministic guard against pathological adaptive-solver work."""

    def __init__(self, limit: int, evaluations: int):
        self.limit = int(limit)
        self.evaluations = int(evaluations)
        super().__init__(
            f"RHS evaluation budget exceeded: limit={self.limit}, "
            f"attempted_evaluations={self.evaluations}"
        )


class RHSIntegrationError(RuntimeError):
    """Numerical RHS failure annotated with the work spent before failure."""

    def __init__(self, message: str, evaluations: int):
        self.rhs_evaluations = int(evaluations)
        super().__init__(
            f"{message} (after {self.rhs_evaluations} RHS evaluations)"
        )


DEFAULT_MAX_RHS_EVALUATIONS = 100_000


@dataclass
class PTUMParameters:
    """PTUM model parameters for the discharge simulation."""
    # Inflation/discharge parameters
    V0: float = 1e56          # GeV^4, plateau height ~ (10^14 GeV)^4
    lambda_phi: float = 0.02  # Dimensionless plateau-shape parameter
    Phi_c: float = 0.9862280831209068 * M_PL # GeV, independent critical field; match to Phi_end

    # Activation sector parameters
    m_psi: float = 1e13       # GeV, bare mass of ψ
    lambda_psi: float = 0.1   # Quartic coupling
    E_th: float = 1e16        # GeV, threshold scale

    @property
    def alpha(self) -> float:
        """Threshold coupling fixed by m_eff^2(Phi_c)=0: alpha=(E_th/Phi_c)^2."""
        return (self.E_th / self.Phi_c)**2
    
    @property
    def mu_sq(self) -> float:
        """Tachyonic scale |m_eff²| just below the threshold at 0.99 Phi_c."""
        Phi = 0.99 * self.Phi_c
        m_eff_sq = self.m_psi**2 * (self.alpha * Phi**2 / self.E_th**2 - 1)
        return m_eff_sq  # negative
    
    @property
    def mu(self) -> float:
        """μ = sqrt(|m_eff²|)"""
        return np.sqrt(abs(self.mu_sq))
    
    @property
    def psi_0(self) -> float:
        """ψ₀ = sqrt(μ²/λ_ψ) - oscillation amplitude scale"""
        return np.sqrt(abs(self.mu_sq) / self.lambda_psi)
    
    @property
    def H_star(self) -> float:
        """Hubble scale during inflation H_* ~ sqrt(V0/3)/M_Pl"""
        return np.sqrt(self.V0 / 3) / M_PL
    
    @property
    def H_threshold_potential(self) -> float:
        """Potential-dominated Hubble estimate evaluated at Phi=Phi_c."""
        x = self.lambda_phi * (self.Phi_c / M_PL)**2
        V_c = self.V0 * (-np.expm1(-x))
        return np.sqrt(V_c / (3.0 * M_PL**2))

    @property
    def H_threshold_exact_end(self) -> float:
        """H at epsilon_H=1 when Phi_c is matched to the exact inflation endpoint.

        At epsilon_H=1 for a canonical scalar, X^2=1/3 and rho=3V/2.
        """
        return np.sqrt(1.5) * self.H_threshold_potential

    @property
    def damping_ratio_potential(self) -> float:
        """Potential-only estimate 3 H_V(Phi_c)/(2 mu)."""
        return 3.0 * self.H_threshold_potential / (2.0 * self.mu)

    @property
    def damping_ratio_plateau(self) -> float:
        """3 H_star/(2 mu), a plateau-scale estimate, not the local trigger value."""
        return 3.0 * self.H_star / (2.0 * self.mu)

    @property
    def damping_ratio(self) -> float:
        """Exact-endpoint 3 H_c/(2 mu), assuming Phi_c is epsilon_H=1."""
        return 3.0 * self.H_threshold_exact_end / (2.0 * self.mu)


@dataclass
class InitialConditions:
    """Initial conditions for the post-threshold homogeneous evolution."""
    Phi: float           # Φ(t_c) = Φ_c (at threshold)
    Phi_dot: float       # Φ̇(t_c) from slow-roll
    psi: float           # ψ(t_c) - homogeneous mode
    psi_dot: float       # ψ̇(t_c)
    # Quantum fluctuation seeds for ensemble runs
    psi_k: Optional[np.ndarray] = None  # Fourier modes
    k_modes: Optional[np.ndarray] = None


def waterfall_transfer_rate(
    Phi: np.ndarray | float,
    psi: np.ndarray | float,
    Phi_dot: np.ndarray | float,
    params: PTUMParameters,
) -> tuple[np.ndarray | float, np.ndarray | float]:
    """Return homogeneous Q_psi^0 and Q_Phi^0 for the declared sector split.

    The interaction potential U_int=+alpha*m_psi^2*Phi^2*psi^2/(2 E_th^2)
    is assigned to T_psi. With (-+++), Q_psi^0=+U_int,Phi*Phi_dot
    and Q_Phi^0=-Q_psi^0. For Phi>0 and Phi_dot<0, Q_psi^0 is negative.
    """
    coefficient = params.alpha * params.m_psi**2 / params.E_th**2
    q_psi = coefficient * np.asarray(Phi) * np.asarray(psi)**2 * np.asarray(Phi_dot)
    q_phi = -q_psi
    if np.ndim(q_psi) == 0:
        return float(q_psi), float(q_phi)
    return q_psi, q_phi


def veff_phi(Phi: float, params: PTUMParameters) -> float:
    """Tree-level fuel potential with dimensionless exponent.

    lambda_phi is dimensionless; M_PL/sqrt(lambda_phi) is the
    characteristic plateau field scale. The discharge threshold Phi_c
    is an independent parameter fixed through alpha=(E_th/Phi_c)**2.
    """
    x = params.lambda_phi * (Phi / M_PL)**2
    return params.V0 * (-np.expm1(-x))


def dveff_dphi(Phi: float, params: PTUMParameters) -> float:
    """Analytic derivative of the dimensionally consistent fuel potential."""
    x = params.lambda_phi * (Phi / M_PL)**2
    return (2.0 * params.V0 * params.lambda_phi * Phi / M_PL**2
            * np.exp(-x))


def meff_sq_psi(Phi: float, params: PTUMParameters) -> float:
    """Waterfall mass: positive above Phi_c and tachyonic below it."""
    return params.m_psi**2 * (params.alpha * Phi**2 / params.E_th**2 - 1)


def rho_phi(Phi: float, Phi_dot: float, psi: float, params: PTUMParameters) -> float:
    """Fuel-sector density; the interaction potential is assigned only to ψ."""
    return 0.5 * Phi_dot**2 + veff_phi(Phi, params)


def pressure_phi(Phi: float, Phi_dot: float, params: PTUMParameters) -> float:
    """Pressure of the canonical fuel field Φ."""
    return 0.5 * Phi_dot**2 - veff_phi(Phi, params)


def rho_total(Phi: float, Phi_dot: float, psi: float, psi_dot: float,
              params: PTUMParameters, rho_other: float = 0.0) -> float:
    """Total homogeneous density; the Φ-ψ interaction is counted exactly once."""
    return rho_phi(Phi, Phi_dot, psi, params) + rho_psi(Phi, psi, psi_dot, params) + rho_other


def rho_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Energy density of proxy field ψ"""
    m_eff_sq = meff_sq_psi(Phi, params)
    return 0.5 * psi_dot**2 + 0.5 * m_eff_sq * psi**2 + 0.25 * params.lambda_psi * psi**4


def pressure_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Pressure of proxy field ψ"""
    m_eff_sq = meff_sq_psi(Phi, params)
    return 0.5 * psi_dot**2 - 0.5 * m_eff_sq * psi**2 - 0.25 * params.lambda_psi * psi**4


def psi_minimum_squared(Phi: np.ndarray | float, params: PTUMParameters):
    """Instantaneous |psi_min(Phi)|^2, zero in the unbroken phase."""
    m_eff_sq = meff_sq_psi(Phi, params)
    return np.maximum(-np.asarray(m_eff_sq), 0.0) / params.lambda_psi


def psi_minimum_potential(Phi: np.ndarray | float, params: PTUMParameters):
    """Potential value at the instantaneous global minimum of V_psi."""
    m_eff_sq = np.asarray(meff_sq_psi(Phi, params))
    return -(np.maximum(-m_eff_sq, 0.0) ** 2) / (4.0 * params.lambda_psi)


def psi_excitation_potential(
    Phi: np.ndarray | float,
    psi: np.ndarray | float,
    params: PTUMParameters,
):
    """V_psi(Phi,psi)-V_psi(Phi,psi_min(Phi)); non-negative by construction."""
    m_eff_sq = np.asarray(meff_sq_psi(Phi, params))
    psi_arr = np.asarray(psi)
    psi_min_sq = psi_minimum_squared(Phi, params)
    raw_potential = 0.5 * m_eff_sq * psi_arr**2 + 0.25 * params.lambda_psi * psi_arr**4
    shifted_double_well = 0.25 * params.lambda_psi * (psi_arr**2 - psi_min_sq)**2
    return np.where(m_eff_sq < 0.0, shifted_double_well, raw_potential)


def psi_excitation_energy(
    Phi: np.ndarray | float,
    psi: np.ndarray | float,
    psi_dot: np.ndarray | float,
    params: PTUMParameters,
):
    return 0.5 * np.asarray(psi_dot)**2 + psi_excitation_potential(Phi, psi, params)


def psi_excitation_pressure(
    Phi: np.ndarray | float,
    psi: np.ndarray | float,
    psi_dot: np.ndarray | float,
    params: PTUMParameters,
):
    return 0.5 * np.asarray(psi_dot)**2 - psi_excitation_potential(Phi, psi, params)


def waterfall_excitation_transfer_rate(
    Phi: np.ndarray | float,
    psi: np.ndarray | float,
    Phi_dot: np.ndarray | float,
    params: PTUMParameters,
):
    """Q_psi^0 after moving V_min(Phi) from the psi sector to the Phi sector."""
    Phi_arr = np.asarray(Phi)
    psi_arr = np.asarray(psi)
    Phi_dot_arr = np.asarray(Phi_dot)
    m_eff_sq = np.asarray(meff_sq_psi(Phi_arr, params))
    coupling = params.alpha * params.m_psi**2 / params.E_th**2
    q_raw, _ = waterfall_transfer_rate(Phi_arr, psi_arr, Phi_dot_arr, params)
    dVmin_dPhi = np.where(
        m_eff_sq < 0.0,
        -m_eff_sq * coupling * Phi_arr / params.lambda_psi,
        0.0,
    )
    q_exc = np.asarray(q_raw) - dVmin_dPhi * Phi_dot_arr
    q_phi = -q_exc
    if np.ndim(q_exc) == 0:
        return float(q_exc), float(q_phi)
    return q_exc, q_phi


def w_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Raw unshifted w_psi; NaN when the sector density is numerically zero."""
    p = pressure_psi(Phi, psi, psi_dot, params)
    rho = rho_psi(Phi, psi, psi_dot, params)
    if not np.isfinite(rho) or abs(rho) <= np.finfo(float).tiny:
        return float("nan")
    return p / rho


def hubble_rate(Phi: float, Phi_dot: float, psi: float, psi_dot: float, 
                params: PTUMParameters, rho_other: float = 0.0) -> float:
    """Hubble rate H = sqrt(ρ_total/3M_Pl²)"""
    rho_phi_value = rho_phi(Phi, Phi_dot, psi, params)
    rho_psi_value = rho_psi(Phi, psi, psi_dot, params)
    rho_tot = rho_phi_value + rho_psi_value + rho_other
    if not np.isfinite(rho_tot) or rho_tot <= 0.0:
        raise ValueError(
            "Non-positive or non-finite total density: "
            f"rho_total={rho_tot}, rho_phi={rho_phi_value}, "
            f"rho_psi={rho_psi_value}, Phi={Phi}, Phi_dot={Phi_dot}, "
            f"psi={psi}, psi_dot={psi_dot}"
        )
    return np.sqrt(rho_tot / (3 * M_PL**2))


def background_equations(t: float, y: np.ndarray, params: PTUMParameters) -> np.ndarray:
    """
    Coupled background equations for (Φ, Φ̇, ψ, ψ̇).
    
    State vector y = [Phi, Phi_dot, psi, psi_dot]
    Returns dydt = [Phi_dot, Phi_ddot, psi_dot, psi_ddot]
    """
    Phi, Phi_dot, psi, psi_dot = y
    
    # Hubble rate
    H = hubble_rate(Phi, Phi_dot, psi, psi_dot, params)
    
    # Waterfall coupling U_int=+alpha*m_psi^2*Phi^2*psi^2/(2 E_th^2):
    # Phi_ddot + 3H Phi_dot + V_eff,Phi + alpha*m_psi^2*Phi*psi^2/E_th^2 = 0.
    Phi_ddot = -3 * H * Phi_dot - dveff_dphi(Phi, params) - \
               (params.alpha * params.m_psi**2 / params.E_th**2) * Phi * psi**2
    
    # ψ equation: ψ̈ + 3Hψ̇ + m_eff²(Φ)ψ + λ_ψψ³ = 0
    m_eff_sq = meff_sq_psi(Phi, params)
    psi_ddot = -3 * H * psi_dot - m_eff_sq * psi - params.lambda_psi * psi**3
    
    return np.array([Phi_dot, Phi_ddot, psi_dot, psi_ddot])


def dimensionless_state_scales(params: PTUMParameters) -> np.ndarray:
    """Characteristic scales for the state (Phi, Phi_dot, psi, psi_dot).

    The entries have dimensions GeV, GeV^2, GeV, GeV^2 respectively.
    They use the exact threshold field, the local tachyonic time scale
    mu defined by PTUMParameters, and the broken-phase amplitude psi_0.
    """
    mu = float(params.mu)
    scales = np.asarray([
        params.Phi_c,
        mu * params.Phi_c,
        params.psi_0,
        mu * params.psi_0,
    ], dtype=float)
    if (scales.shape != (4,) or not np.all(np.isfinite(scales))
            or np.any(scales <= 0.0) or not np.isfinite(mu) or mu <= 0.0):
        raise ValueError("dimensionless state scales must be finite and positive")
    return scales


def dimensionless_state_scale_metadata(params: PTUMParameters) -> Dict[str, float]:
    """JSON-safe record of the physical scales used to nondimensionalize the ODE."""
    scales = dimensionless_state_scales(params)
    return {
        "mu_GeV": float(params.mu),
        "Phi_GeV": float(scales[0]),
        "Phi_dot_GeV2": float(scales[1]),
        "psi_GeV": float(scales[2]),
        "psi_dot_GeV2": float(scales[3]),
    }


def _dimensionless_rhs_with_scales(
    tau: float,
    y_scaled: np.ndarray,
    params: PTUMParameters,
    mu: float,
    scales: np.ndarray,
) -> np.ndarray:
    """Transform the physical RHS to tau=mu*t and order-one state variables."""
    y_physical = np.asarray(y_scaled, dtype=float) * scales
    rhs_physical = background_equations(float(tau) / mu, y_physical, params)
    return rhs_physical / (mu * scales)


def dimensionless_background_equations(
    tau: float, y_scaled: np.ndarray, params: PTUMParameters
) -> np.ndarray:
    """Dimensionless equivalent of background_equations for regression checks.

    The independent variable is tau=mu*t and the state is
    (Phi/Phi_c, Phi_dot/(mu*Phi_c), psi/psi_0, psi_dot/(mu*psi_0)).
    """
    mu = float(params.mu)
    scales = dimensionless_state_scales(params)
    return _dimensionless_rhs_with_scales(tau, y_scaled, params, mu, scales)


def run_simulation(params: PTUMParameters, 
                   ic: InitialConditions,
                   t_span: Tuple[float, float],
                   t_eval: Optional[np.ndarray] = None,
                   rtol: float = 1e-9,
                   atol: float = 1e-12,
                   max_rhs_evaluations: Optional[int] = DEFAULT_MAX_RHS_EVALUATIONS,
                   solver_method: str = "DOP853") -> Dict:
    """
    Run a single background simulation with a deterministic RHS-work guard.

    The integrator evolves tau=mu*t and the order-one state
    (Phi/Phi_c, Phi_dot/(mu*Phi_c), psi/psi_0, psi_dot/(mu*psi_0)).
    Thus rtol and atol are dimensionless and apply consistently to all
    components. Returned fields and time are converted back to physical units.

    The evaluation budget is an engineering fail-closed limit, not a physical
    cutoff or a substitute for convergence. A trajectory that exhausts it is
    reported as failed and must not be classified as a physical regime.
    """
    if (max_rhs_evaluations is not None
            and (isinstance(max_rhs_evaluations, bool)
                 or int(max_rhs_evaluations) != max_rhs_evaluations
                 or max_rhs_evaluations < 1)):
        raise ValueError("max_rhs_evaluations must be a positive integer or None")
    if not np.isfinite(rtol) or rtol <= 0.0:
        raise ValueError("rtol must be finite and positive")
    if not np.isfinite(atol) or atol <= 0.0:
        raise ValueError("atol must be finite and positive")
    if solver_method not in {"DOP853", "Radau", "BDF", "LSODA"}:
        raise ValueError("solver_method must be one of DOP853, Radau, BDF, LSODA")

    mu = float(params.mu)
    state_scales = dimensionless_state_scales(params)
    state_scale_metadata = dimensionless_state_scale_metadata(params)
    y0_physical = np.array([ic.Phi, ic.Phi_dot, ic.psi, ic.psi_dot], dtype=float)
    y0_scaled = y0_physical / state_scales
    tau_span = (float(t_span[0]) * mu, float(t_span[1]) * mu)
    tau_eval = None if t_eval is None else np.asarray(t_eval, dtype=float) * mu
    rhs_evaluations = 0

    def counted_dimensionless_equations(tau, y_scaled, model_params):
        nonlocal rhs_evaluations
        rhs_evaluations += 1
        if (max_rhs_evaluations is not None
                and rhs_evaluations > max_rhs_evaluations):
            raise RHSWorkBudgetExceeded(max_rhs_evaluations, rhs_evaluations)
        return _dimensionless_rhs_with_scales(
            tau, y_scaled, model_params, mu, state_scales
        )

    try:
        sol = solve_ivp(
            counted_dimensionless_equations,
            tau_span,
            y0_scaled,
            args=(params,),
            t_eval=tau_eval,
            rtol=rtol,
            atol=atol,
            method=solver_method,
            dense_output=True
        )
    except RHSWorkBudgetExceeded:
        raise
    except Exception as exc:
        raise RHSIntegrationError(str(exc), rhs_evaluations) from exc

    if not sol.success:
        raise RHSIntegrationError(
            f"Integration failed: {sol.message}", rhs_evaluations
        )
    
    # Return physical fields and physical time after integrating the
    # dimensionless system. Solver atol is now dimensionless and comparable
    # across all four state variables.
    t = sol.t / mu
    y_physical = sol.y * state_scales[:, np.newaxis]
    Phi = y_physical[0]
    Phi_dot = y_physical[1]
    psi = y_physical[2]
    psi_dot = y_physical[3]
    
    # Compute diagnostics
    H = np.array([hubble_rate(Phi[i], Phi_dot[i], psi[i], psi_dot[i], params) 
                  for i in range(len(t))])
    
    rho_phi_arr = np.array([rho_phi(Phi[i], Phi_dot[i], psi[i], params) for i in range(len(t))])
    rho_psi_arr = np.array([rho_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    p_phi_arr = np.array([pressure_phi(Phi[i], Phi_dot[i], params) for i in range(len(t))])
    p_psi_arr = np.array([pressure_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    rho_total_arr = rho_phi_arr + rho_psi_arr
    p_total_arr = p_phi_arr + p_psi_arr

    # Diagnostic split around the instantaneous broken-phase minimum:
    # move V_min(Phi) from the psi excitation sector into the Phi sector.
    V_psi_min_arr = np.asarray(psi_minimum_potential(Phi, params), dtype=float)
    rho_psi_exc_arr = 0.5 * psi_dot**2 + psi_excitation_potential(Phi, psi, params)
    p_psi_exc_arr = 0.5 * psi_dot**2 - psi_excitation_potential(Phi, psi, params)
    rho_phi_split_arr = rho_phi_arr + V_psi_min_arr
    p_phi_split_arr = p_phi_arr - V_psi_min_arr
    w_psi_exc_arr = np.divide(
        p_psi_exc_arr,
        rho_psi_exc_arr,
        out=np.full_like(rho_psi_exc_arr, np.nan, dtype=float),
        where=np.abs(rho_psi_exc_arr) > np.finfo(float).tiny,
    )
    Q_psi_exc0_arr, Q_Phi_split0_arr = waterfall_excitation_transfer_rate(
        Phi, psi, Phi_dot, params
    )

    # Evaluate d(rho)/dt by the chain rule using the same RHS that evolves
    # the fields. This avoids differencing a nearly constant, ~1e50 GeV^4
    # vacuum density and dividing round-off noise by an almost-zero scale.
    # It is an equation-consistency diagnostic, not an independent solver test.
    coupling = params.alpha * params.m_psi**2 / params.E_th**2
    m_eff_sq_arr = np.array([meff_sq_psi(x, params) for x in Phi])
    dV_dPhi_arr = np.array([dveff_dphi(x, params) for x in Phi])
    Phi_ddot_arr = -3.0 * H * Phi_dot - dV_dPhi_arr - coupling * Phi * psi**2
    psi_ddot_arr = -3.0 * H * psi_dot - m_eff_sq_arr * psi - params.lambda_psi * psi**3
    dm_eff_sq_dPhi_arr = 2.0 * coupling * Phi
    rho_dot_chain_rule = (
        Phi_dot * (Phi_ddot_arr + dV_dPhi_arr)
        + psi_dot * psi_ddot_arr
        + m_eff_sq_arr * psi * psi_dot
        + 0.5 * dm_eff_sq_dPhi_arr * Phi_dot * psi**2
        + params.lambda_psi * psi**3 * psi_dot
    )
    # For canonical homogeneous scalars rho + p = Phi_dot^2 + psi_dot^2;
    # evaluate this directly to avoid subtracting two vacuum-sized arrays.
    expansion_term = 3.0 * H * (Phi_dot**2 + psi_dot**2)
    continuity_residual = rho_dot_chain_rule + expansion_term
    continuity_scale = np.abs(rho_dot_chain_rule) + np.abs(expansion_term)
    continuity_residual_relative = np.divide(
        continuity_residual,
        continuity_scale,
        out=np.zeros_like(continuity_residual),
        where=continuity_scale > 0.0
    )
    # A second normalization referenced to the total background energy
    # remains well-conditioned when rho_dot and 3H(rho+p) both approach
    # zero in a vacuum-dominated, nearly static solution.
    background_energy_scale = np.maximum(
        np.abs(H) * np.abs(rho_total_arr),
        np.finfo(float).tiny,
    )
    continuity_residual_background_relative = (
        continuity_residual / background_energy_scale
    )

    Q_psi0_arr, Q_Phi0_arr = waterfall_transfer_rate(
        Phi, psi, Phi_dot, params
    )

    # Keep the sampled finite-difference estimate as a separate convergence
    # diagnostic. It is expected to be noisy when rho is vacuum dominated.
    rho_dot_finite_difference = np.gradient(rho_total_arr, t)
    continuity_residual_finite_difference = rho_dot_finite_difference + expansion_term
    continuity_scale_finite_difference = (
        np.abs(rho_dot_finite_difference) + np.abs(expansion_term)
    )
    continuity_residual_finite_difference_relative = np.divide(
        continuity_residual_finite_difference,
        continuity_scale_finite_difference,
        out=np.full_like(continuity_residual_finite_difference, np.nan),
        where=continuity_scale_finite_difference > 0.0
    )
    continuity_residual_finite_difference_background_relative = (
        continuity_residual_finite_difference / background_energy_scale
    )
    w_psi_arr = np.array([w_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    
    # Retain the sampled estimators as independent diagnostics, but use
    # adaptive quadrature on the solver's dense interpolant for the reported
    # complete-cycle averages. This removes output-grid endpoint bias.
    U_psi = 0.25 * params.lambda_psi * psi**4
    virial_ratio_sampled = compute_quartic_virial_ratio(
        t, psi, psi_dot, params
    )
    Q_sampled = compute_quartic_dominance(t, psi, psi_dot, params, Phi)
    w_avg_sampled, t_avg_sampled = compute_time_averaged_w(
        t, p_psi_exc_arr, rho_psi_exc_arr, psi_dot
    )
    quadratic_virial_ratio = compute_quadratic_virial_ratio(
        t, psi, psi_dot, Phi, params
    )
    dense_cycle = compute_dense_cycle_diagnostics(
        sol.sol, t * mu, mu, state_scales, params, len(t)
    )
    Q_arr = dense_cycle["Q"]
    virial_ratio = dense_cycle["virial_ratio"]
    w_avg = dense_cycle["w_avg"]
    t_avg = dense_cycle["t_avg"]
    w_avg_raw, t_avg_raw = compute_time_averaged_w(
        t, p_psi_arr, rho_psi_arr, psi_dot
    )
    
    return {
        'success': True,
        'solver_stats': {
            'method': solver_method,
            'rhs_evaluations': int(rhs_evaluations),
            'nfev': int(sol.nfev),
            'njev': int(sol.njev),
            'nlu': int(sol.nlu),
            'rtol': float(rtol),
            'atol': float(atol),
            'rhs_evaluation_limit': (
                None if max_rhs_evaluations is None
                else int(max_rhs_evaluations)
            ),
            'budget_exhausted': False,
            'time_variable': 'tau=mu*t',
            'state_variables_dimensionless': True,
            'state_scales': state_scale_metadata,
        },
        't': t,
        'Phi': Phi,
        'Phi_dot': Phi_dot,
        'psi': psi,
        'psi_dot': psi_dot,
        'H': H,
        'rho_phi': rho_phi_arr,
        'rho_psi': rho_psi_arr,
        'rho_total': rho_total_arr,
        'p_phi': p_phi_arr,
        'p_psi': p_psi_arr,
        'p_total': p_total_arr,
        'V_psi_min': V_psi_min_arr,
        'rho_phi_split': rho_phi_split_arr,
        'p_phi_split': p_phi_split_arr,
        'rho_psi_exc': rho_psi_exc_arr,
        'p_psi_exc': p_psi_exc_arr,
        'Q_psi_exc0': Q_psi_exc0_arr,
        'Q_Phi_split0': Q_Phi_split0_arr,
        'continuity_residual': continuity_residual,
        'continuity_residual_relative': continuity_residual_relative,
        'continuity_residual_background_relative': continuity_residual_background_relative,
        'Q_psi0': Q_psi0_arr,
        'Q_Phi0': Q_Phi0_arr,
        'continuity_residual_finite_difference': continuity_residual_finite_difference,
        'continuity_residual_finite_difference_relative': continuity_residual_finite_difference_relative,
        'continuity_residual_finite_difference_background_relative': continuity_residual_finite_difference_background_relative,
        'w_psi': w_psi_arr,
        'w_psi_exc': w_psi_exc_arr,
        'w_psi_avg': w_avg,
        'w_psi_avg_raw': w_avg_raw,
        'Q_sampled': Q_sampled,
        'virial_ratio_sampled': virial_ratio_sampled,
        'w_psi_avg_sampled': w_avg_sampled,
        't_avg_sampled': t_avg_sampled,
        'cycle_quadrature_relative_error_max': dense_cycle["max_relative_quadrature_error"],
        'cycle_quadrature_normalized_absolute_error_max': dense_cycle[
            "max_normalized_absolute_quadrature_error"
        ],
        'cycle_turning_times': dense_cycle["turning_times"],
        'Q_cycle': dense_cycle["Q_cycle"],
        'virial_ratio_cycle': dense_cycle["virial_ratio_cycle"],
        'H_avg_cycle': dense_cycle["H_avg_cycle"],
        't_avg': t_avg,
        't_avg_raw': t_avg_raw,
        'U_psi': U_psi,
        'virial_ratio': virial_ratio,
        'quadratic_virial_ratio': quadratic_virial_ratio,
        'Q': Q_arr,
        'params': params,
        'ic': ic
    }


def compute_quartic_dominance(t: np.ndarray, psi: np.ndarray,
                              psi_dot: np.ndarray, params: PTUMParameters,
                              Phi: Optional[np.ndarray] = None) -> np.ndarray:
    """Return half-cycle Q = λ<ψ⁴>/<|m_eff²(Φ)| ψ²>; NaN means not measurable."""
    Q = np.full_like(t, np.nan, dtype=float)
    if Phi is None:
        raise ValueError("Phi history is required for a time-local quartic diagnostic")
    if len(Phi) != len(t):
        raise ValueError("Phi and t must have the same length")

    # Turning points delimit half-oscillations; signbit handles exact zeros robustly.
    turning_points = np.where(np.diff(np.signbit(psi_dot)))[0]
    if len(turning_points) < 2:
        return Q

    for i in range(len(turning_points) - 1):
        start, end = turning_points[i], turning_points[i + 1] + 1
        if end - start < 3:
            continue
        psi_seg = psi[start:end]
        mass_sq_seg = np.abs(meff_sq_psi(Phi[start:end], params))
        numerator = params.lambda_psi * np.mean(psi_seg**4)
        denominator = np.mean(mass_sq_seg * psi_seg**2)
        if denominator > 0.0 and np.isfinite(denominator):
            Q[start:end] = numerator / denominator
    return Q


def compute_quartic_virial_ratio(t: np.ndarray, psi: np.ndarray,
                                psi_dot: np.ndarray,
                                params: PTUMParameters) -> np.ndarray:
    """Half-cycle <K>/(2<V4>) for a quartic oscillator; NaN if undefined."""
    ratio = np.full_like(t, np.nan, dtype=float)
    turning_points = np.where(np.diff(np.signbit(psi_dot)))[0]
    for i in range(len(turning_points) - 1):
        start, end = turning_points[i], turning_points[i + 1] + 1
        if end - start < 3:
            continue
        kinetic_avg = 0.5 * np.mean(psi_dot[start:end]**2)
        twice_potential_avg = 0.5 * params.lambda_psi * np.mean(psi[start:end]**4)
        if twice_potential_avg > 0.0:
            ratio[start:end] = kinetic_avg / twice_potential_avg
    return ratio


def compute_quadratic_virial_ratio(t: np.ndarray, psi: np.ndarray,
                                      psi_dot: np.ndarray, Phi: np.ndarray,
                                      params: PTUMParameters) -> np.ndarray:
    """Half-cycle <K>/<V2> for a positive, slowly varying quadratic mode."""
    if len(Phi) != len(t):
        raise ValueError("Phi and t must have the same length")
    ratio = np.full_like(t, np.nan, dtype=float)
    m_eff_sq = np.array([meff_sq_psi(value, params) for value in Phi])
    turning_points = np.where(np.diff(np.signbit(psi_dot)))[0]
    for i in range(len(turning_points) - 1):
        start, end = turning_points[i], turning_points[i + 1] + 1
        if end - start < 3 or np.any(m_eff_sq[start:end] <= 0.0):
            continue
        kinetic_avg = 0.5 * np.mean(psi_dot[start:end]**2)
        quadratic_potential_avg = 0.5 * np.mean(
            m_eff_sq[start:end] * psi[start:end]**2
        )
        if quadratic_potential_avg > 0.0:
            ratio[start:end] = kinetic_avg / quadratic_potential_avg
    return ratio


def compute_dense_cycle_diagnostics(
    dense_solution: Callable[[float], np.ndarray],
    tau_samples: np.ndarray,
    mu: float,
    state_scales: np.ndarray,
    params: PTUMParameters,
    n_output: int,
) -> Dict[str, np.ndarray | float | list]:
    """Compute half-cycle ratios by adaptive quadrature of the ODE dense output.

    Turning points are roots of psi_dot in the continuous DOP853 interpolant.
    The integrated quantities are lambda*psi^4, |m_eff^2|*psi^2,
    kinetic energy, 2*V4, excitation pressure, excitation density, and H.
    The returned ratios and cycle-mean H therefore do not depend on
    rectangular output-grid means. The accepted solver mesh brackets roots;
    tau_samples only clips the requested interval and maps diagnostics onto
    the legacy time-series representation.
    """
    tau_samples = np.asarray(tau_samples, dtype=float)
    scales = np.asarray(state_scales, dtype=float)
    if (tau_samples.ndim != 1 or len(tau_samples) < 3
            or np.any(np.diff(tau_samples) <= 0.0)
            or scales.shape != (4,) or not np.all(np.isfinite(scales))
            or mu <= 0.0 or n_output != len(tau_samples)):
        raise ValueError("invalid dense-cycle diagnostic inputs")

    def physical_state(tau):
        return np.asarray(dense_solution(float(tau)), dtype=float) * scales

    # Prefer the adaptive solver's accepted dense-output mesh for root
    # bracketing. It is independent of the user-selected t_eval/output grid.
    # Midpoints provide an additional guard against multiple crossings inside
    # one accepted step. Analytic test callables without an OdeSolution mesh
    # fall back to tau_samples.
    solver_mesh = getattr(dense_solution, "ts", None)
    if solver_mesh is None:
        bracket_times = tau_samples
    else:
        solver_mesh = np.asarray(solver_mesh, dtype=float)
        if (solver_mesh.ndim != 1 or len(solver_mesh) < 2
                or not np.all(np.isfinite(solver_mesh))
                or np.any(np.diff(solver_mesh) <= 0.0)):
            raise ValueError("dense solver mesh must be finite and increasing")
        # A single midpoint can miss an even number of turning points
        # inside one accepted step. Subdivide each dense-output interval so
        # root bracketing samples the interpolant at a bounded spacing.
        # This is a detection safeguard, not a formal root-count proof.
        subdivisions = 16
        fractions = np.linspace(0.0, 1.0, subdivisions + 1)
        bracket_times = np.unique(np.concatenate([
            start + fractions * (end - start)
            for start, end in zip(solver_mesh[:-1], solver_mesh[1:])
        ]))
        bracket_times = bracket_times[
            (bracket_times >= tau_samples[0])
            & (bracket_times <= tau_samples[-1])
        ]
        if len(bracket_times) < 3:
            raise ValueError("dense solver mesh does not cover output interval")

    def locate_turning_points(subdivisions):
        if solver_mesh is None:
            base_mesh = tau_samples
        else:
            base_mesh = solver_mesh[
                (solver_mesh >= tau_samples[0])
                & (solver_mesh <= tau_samples[-1])
            ]
            # Include requested interval endpoints when the solver mesh
            # extends beyond the diagnostic window.
            base_mesh = np.unique(np.concatenate((
                [tau_samples[0]], base_mesh, [tau_samples[-1]]
            )))
        fractions = np.linspace(0.0, 1.0, subdivisions + 1)
        sample_times = np.unique(np.concatenate([
            start + fractions * (end - start)
            for start, end in zip(base_mesh[:-1], base_mesh[1:])
        ]))
        sampled_psi_dot = np.asarray([
            physical_state(tau)[3] for tau in sample_times
        ])
        roots = []

        # A turning point requires an isolated zero/sign reversal of psi_dot.
        # Ignore zero plateaus and non-finite gaps rather than invent cycles.
        finite_nonzero = np.flatnonzero(
            np.isfinite(sampled_psi_dot) & (sampled_psi_dot != 0.0)
        )
        if (len(finite_nonzero) and finite_nonzero[0] == 1
                and sampled_psi_dot[0] == 0.0):
            roots.append(float(sample_times[0]))

        for left_index, right_index in zip(
            finite_nonzero[:-1], finite_nonzero[1:]
        ):
            if right_index - left_index > 2:
                continue
            left_value = sampled_psi_dot[left_index]
            right_value = sampled_psi_dot[right_index]
            if np.signbit(left_value) == np.signbit(right_value):
                continue
            root = float(brentq(
                lambda tau: physical_state(tau)[3],
                sample_times[left_index], sample_times[right_index],
                xtol=4.0 * np.finfo(float).eps,
                rtol=8.0 * np.finfo(float).eps,
            ))
            if not roots or root - roots[-1] > (
                32.0 * np.finfo(float).eps * max(1.0, abs(root))
            ):
                roots.append(root)

        if (len(finite_nonzero)
                and finite_nonzero[-1] == len(sample_times) - 2
                and sampled_psi_dot[-1] == 0.0):
            endpoint = float(sample_times[-1])
            if not roots or endpoint - roots[-1] > (
                32.0 * np.finfo(float).eps * max(1.0, abs(endpoint))
            ):
                roots.append(endpoint)
        return np.asarray(roots, dtype=float)

    # Increase the bracketing density until two successive refinements agree
    # in both root count and root locations. This is a numerical stability
    # check, not a proof that an arbitrary interpolant has no unresolved roots.
    roots = locate_turning_points(16)
    root_refinement_converged = False
    root_bracketing_subdivisions = 16
    for subdivisions in (32, 64, 128):
        roots_refined = locate_turning_points(subdivisions)
        same_count = len(roots_refined) == len(roots)
        same_locations = (
            same_count and np.allclose(
                roots_refined, roots, rtol=1.0e-10, atol=1.0e-12
            )
        )
        if same_locations:
            root_refinement_converged = True
            roots = roots_refined
            root_bracketing_subdivisions = subdivisions
            break
        roots = roots_refined
        root_bracketing_subdivisions = subdivisions
    if not root_refinement_converged:
        raise ValueError(
            "dense turning-point roots did not converge under "
            "bracketing refinement through 128 subdivisions"
        )

    q_values = np.full(n_output, np.nan, dtype=float)
    virial_values = np.full(n_output, np.nan, dtype=float)
    w_values = []
    t_values = []
    q_cycle_values = []
    virial_cycle_values = []
    h_cycle_values = []
    relative_errors = []
    normalized_absolute_errors = []

    psi_scale = float(params.psi_0)
    quartic_scale = max(
        params.lambda_psi * psi_scale**4, np.finfo(float).tiny
    )
    quadratic_scale = max(
        params.m_psi**2 * psi_scale**2, np.finfo(float).tiny
    )
    kinetic_scale = max(
        (mu * psi_scale)**2, np.finfo(float).tiny
    )
    energy_scale = max(
        quartic_scale, quadratic_scale, kinetic_scale,
        np.finfo(float).tiny,
    )
    # Normalize each component before vector quadrature. Without this,
    # quad_vec's max norm would compare quantities with identical units but
    # wildly different characteristic magnitudes, masking small components.
    hubble_scale = max(float(params.H_star), np.finfo(float).tiny)
    integral_scales = np.asarray([
        quartic_scale, quadratic_scale, energy_scale,
        quartic_scale, energy_scale, energy_scale, hubble_scale,
    ])

    def integrand(tau):
        state = physical_state(tau)
        phi_value, _, psi_value, psi_dot_value = state
        mass_sq = float(meff_sq_psi(phi_value, params))
        excitation_potential = float(
            psi_excitation_potential(phi_value, psi_value, params)
        )
        quartic_potential = 0.25 * params.lambda_psi * psi_value**4
        kinetic = 0.5 * psi_dot_value**2
        excitation_density = kinetic + excitation_potential
        excitation_pressure = kinetic - excitation_potential
        physical_integrand = np.asarray([
            params.lambda_psi * psi_value**4,
            abs(mass_sq) * psi_value**2,
            kinetic,
            2.0 * quartic_potential,
            excitation_pressure,
            excitation_density,
            hubble_rate(phi_value, state[1], psi_value, psi_dot_value, params),
        ], dtype=float)
        return physical_integrand / integral_scales

    for start, end in zip(roots[:-1], roots[1:]):
        if end <= start:
            continue
        normalized_integral, error = quad_vec(
            integrand, start, end, epsabs=0.0, epsrel=1.0e-9,
            norm="max", limit=200,
        )
        normalized_integral = np.asarray(normalized_integral, dtype=float)
        integral = normalized_integral * integral_scales
        # The first four normalized integrals are strictly non-negative
        # cycle moments. Bound each relative error separately rather than
        # dividing by the largest component (which could hide a weak moment).
        positive_moments = np.abs(normalized_integral[:4])
        relative_errors.append(float(
            error / max(float(np.min(positive_moments)), np.finfo(float).tiny)
        ))
        normalized_absolute_errors.append(float(error))
        lo = max(0, int(np.searchsorted(tau_samples, start, side="left")))
        hi = min(n_output, int(np.searchsorted(tau_samples, end, side="right")))
        q_cycle = (
            float(integral[0] / integral[1])
            if integral[1] > 0.0 and np.isfinite(integral[1])
            else float("nan")
        )
        virial_cycle = (
            float(integral[2] / integral[3])
            if integral[3] > 0.0 and np.isfinite(integral[3])
            else float("nan")
        )
        w_cycle = (
            float(integral[4] / integral[5])
            if integral[5] > np.finfo(float).tiny
            and np.all(np.isfinite(integral[4:6]))
            else float("nan")
        )
        # The quadrature variable is tau=mu*t, so divide the H integral
        # by the tau interval to obtain the physical-time mean of H.
        h_cycle = float(integral[6] / (end - start))
        if np.isfinite(q_cycle):
            q_values[lo:hi] = q_cycle
        if np.isfinite(virial_cycle):
            virial_values[lo:hi] = virial_cycle
        q_cycle_values.append(q_cycle)
        virial_cycle_values.append(virial_cycle)
        w_values.append(w_cycle)
        h_cycle_values.append(h_cycle)
        t_values.append(float(0.5 * (start + end) / mu))

    return {
        "Q": q_values,
        "virial_ratio": virial_values,
        "w_avg": np.asarray(w_values, dtype=float),
        "t_avg": np.asarray(t_values, dtype=float),
        "Q_cycle": np.asarray(q_cycle_values, dtype=float),
        "virial_ratio_cycle": np.asarray(virial_cycle_values, dtype=float),
        "H_avg_cycle": np.asarray(h_cycle_values, dtype=float),
        "turning_times": [float(value / mu) for value in roots],
        "max_relative_quadrature_error": (
            max(relative_errors) if relative_errors else float("nan")
        ),
        "max_normalized_absolute_quadrature_error": (
            max(normalized_absolute_errors)
            if normalized_absolute_errors else float("nan")
        ),
    }


def compute_time_averaged_w(t: np.ndarray, pressure: np.ndarray,
                            density: np.ndarray,
                            psi_dot: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute cycle-averaged w as <p>/<rho>, not as <p/rho>.

    Turning points of psi delimit half-oscillation intervals. The ratio of
    separately averaged pressure and density is the physically relevant
    coarse-grained equation of state; averaging the instantaneous ratio can
    overweight epochs where rho is small.
    """
    turning_points = np.where(np.diff(np.signbit(psi_dot)))[0]

    if len(turning_points) < 2:
        return np.array([]), np.array([])

    w_avg = []
    t_avg = []

    for i in range(len(turning_points) - 1):
        start = turning_points[i]
        end = turning_points[i + 1] + 1
        if end - start < 2:
            continue
        rho_mean = float(np.mean(density[start:end]))
        p_mean = float(np.mean(pressure[start:end]))
        scale = max(float(np.max(np.abs(density[start:end]))),
                    float(np.max(np.abs(pressure[start:end]))),
                    np.finfo(float).tiny)
        if not np.isfinite(rho_mean) or abs(rho_mean) <= 1.0e-14 * scale:
            w_avg.append(np.nan)
        else:
            w_avg.append(p_mean / rho_mean)
        t_avg.append(0.5 * (t[start] + t[end - 1]))

    return np.asarray(w_avg), np.asarray(t_avg)


def create_initial_conditions(params: PTUMParameters,
                              psi_init: float = 0.0,
                              psi_dot_init: float = 0.0,
                              phi_offset: float = 0.0,
                              Phi_dot_override: Optional[float] = None) -> InitialConditions:
    """
    Create post-threshold initial conditions for the homogeneous evolution.
    
    Args:
        params: PTUM parameters
        psi_init: Initial ψ(t_c) [default 0 = top of barrier]
        psi_dot_init: Initial ψ̇(t_c) [default 0]
        phi_offset: Positive offset places Φ below Φ_c, on the tachyonic side.
    
    Returns:
        InitialConditions object
    """
    Phi_c = params.Phi_c
    # Positive offset means the field has rolled below the threshold.
    Phi = Phi_c - phi_offset
    
    if Phi_dot_override is None:
        # Fallback for exploratory runs only. Production threshold scans
        # should supply the velocity from the integrated inflationary
        # background via ptum_inflation_background.state_at_field_value.
        V = veff_phi(Phi, params)
        V_prime = dveff_dphi(Phi, params)
        epsilon_V = 0.5 * (M_PL * V_prime / V)**2 if V > 0 else 0.01
        H = np.sqrt(V / (3.0 * M_PL**2)) if V > 0 else params.H_star
        Phi_dot = -np.sqrt(2.0 * epsilon_V) * H * M_PL
    else:
        Phi_dot = float(Phi_dot_override)
        if not np.isfinite(Phi_dot):
            raise ValueError("Phi_dot_override must be finite")
    
    return InitialConditions(
        Phi=Phi,
        Phi_dot=Phi_dot,
        psi=psi_init,
        psi_dot=psi_dot_init
    )


def create_initial_conditions_underdamped(params: PTUMParameters,
                                           psi_init: float = 0.0,
                                           psi_dot_init: float = 0.0,
                                           phi_ratio: float = 0.99) -> InitialConditions:
    """
    Create initial conditions on the tachyonic side (Phi < Phi_c).
    
    Args:
        params: PTUM parameters
        psi_init: Initial ψ [default 0 = top of barrier]
        psi_dot_init: Initial ψ̇ [default 0]
        phi_ratio: Φ/Φ_c ratio [default 0.99 = just below threshold]
    
    Returns:
        InitialConditions object
    """
    Phi = phi_ratio * params.Phi_c
    
    # Slow-roll Φ̇
    V = veff_phi(Phi, params)
    V_prime = dveff_dphi(Phi, params)
    epsilon_V = 0.5 * (M_PL * V_prime / V)**2 if V > 0 else 0.01
    H = np.sqrt(V / (3.0 * M_PL**2)) if V > 0 else params.H_star
    Phi_dot = -np.sqrt(2 * epsilon_V) * H * M_PL
    
    return InitialConditions(
        Phi=Phi,
        Phi_dot=Phi_dot,
        psi=psi_init,
        psi_dot=psi_dot_init
    )


def run_parameter_scan(params: PTUMParameters,
                       psi_init_range: List[float],
                       psi_dot_init_range: List[float],
                       phi_offset_range: List[float],
                       t_max: float = 50.0,
                       n_points: int = 500,
                       phi_dot_init_by_offset: Optional[Dict[float, float]] = None,
                       progress_interval: int = 0,
                       progress_label: str = "scan",
                       result_callback: Optional[Callable[[Dict], None]] = None,
                       max_rhs_evaluations: Optional[int] = DEFAULT_MAX_RHS_EVALUATIONS,
                       rtol: float = 1e-9,
                       atol: float = 1e-12,
                       solver_method: str = "DOP853"
                       ) -> List[Dict]:
    """
    Run parameter scan over initial conditions.
    
    Returns list of simulation results with success/failure classification.
    """
    results = []
    total_runs = (
        len(psi_init_range) * len(psi_dot_init_range) * len(phi_offset_range)
    )
    completed_runs = 0
    if progress_interval < 0:
        raise ValueError("progress_interval must be non-negative")

    def record_progress():
        nonlocal completed_runs
        completed_runs += 1
        if progress_interval and (
            completed_runs % progress_interval == 0 or completed_runs == total_runs
        ):
            print(
                f"[{progress_label}] completed {completed_runs}/{total_runs} trajectories",
                flush=True,
            )

    # Time array (in units of 1/μ)
    mu = np.sqrt(abs(params.mu_sq))
    t_span = (0, t_max / mu)
    t_eval = np.linspace(0, t_max / mu, n_points)
    
    for psi_init in psi_init_range:
        for psi_dot_init in psi_dot_init_range:
            for phi_offset in phi_offset_range:
                phi_dot_override = (
                    phi_dot_init_by_offset[phi_offset]
                    if phi_dot_init_by_offset is not None
                    else None
                )
                ic = create_initial_conditions(
                    params, psi_init, psi_dot_init, phi_offset,
                    Phi_dot_override=phi_dot_override
                )
                
                print(
                    f"[{progress_label}] starting trajectory "
                    f"{completed_runs + 1}/{total_runs}: "
                    f"psi={psi_init}, psi_dot={psi_dot_init}, "
                    f"phi_offset={phi_offset}",
                    flush=True,
                )
                try:
                    result = run_simulation(
                        params, ic, t_span, t_eval,
                        rtol=rtol, atol=atol,
                        max_rhs_evaluations=max_rhs_evaluations,
                        solver_method=solver_method,
                    )
                    
                    # Classify outcome
                    classification = classify_outcome(result, params)
                    result['classification'] = classification
                    result['ic_params'] = {
                        'psi_init': psi_init,
                        'psi_dot_init': psi_dot_init,
                        'phi_offset': phi_offset
                    }
                    results.append(result)
                    if result_callback is not None:
                        result_callback(result)
                    record_progress()
                    
                except Exception as e:
                    failed_result = {
                        'success': False,
                        'error': str(e),
                        'ic_params': {
                            'psi_init': psi_init,
                            'psi_dot_init': psi_dot_init,
                            'phi_offset': phi_offset
                        }
                    }
                    if isinstance(e, RHSWorkBudgetExceeded):
                        failed_result['solver_stats'] = {
                            'method': solver_method,
                            'rhs_evaluations': e.evaluations,
                            'rhs_evaluation_limit': e.limit,
                            'rtol': float(rtol),
                            'atol': float(atol),
                            'budget_exhausted': True,
                            'time_variable': 'tau=mu*t',
                            'state_variables_dimensionless': True,
                            'state_scales': dimensionless_state_scale_metadata(params),
                        }
                    elif isinstance(e, RHSIntegrationError):
                        failed_result['solver_stats'] = {
                            'method': solver_method,
                            'rhs_evaluations': e.rhs_evaluations,
                            'rhs_evaluation_limit': max_rhs_evaluations,
                            'rtol': float(rtol),
                            'atol': float(atol),
                            'budget_exhausted': False,
                            'integration_error': True,
                            'time_variable': 'tau=mu*t',
                            'state_variables_dimensionless': True,
                            'state_scales': dimensionless_state_scale_metadata(params),
                        }
                    results.append(failed_result)
                    if result_callback is not None:
                        result_callback(failed_result)
                    record_progress()
    
    return results


def _late_time_adiabaticity_diagnostic(result: Dict,
                                       tail_fraction: float = 0.2,
                                       min_half_cycles: int = 3) -> Dict:
    """Estimate H/omega from complete late-time half-cycles.

    Turning points are zero crossings of psi_dot. For adjacent extrema,
    omega_half = pi / Delta_t. The reported ratio is interval-mean H divided
    by this frequency. At least three complete half-cycles must lie in the
    final 20% of the trajectory. H/omega < 0.1 is a conservative numerical
    classifier choice, not a theorem or universal physical boundary.
    """
    t = np.asarray(result.get('t', []), dtype=float)
    H = np.asarray(result.get('H', []), dtype=float)
    psi_dot = np.asarray(result.get('psi_dot', []), dtype=float)
    unavailable = {
        'H_over_omega_max': float('nan'),
        'H_over_omega_values': [],
        'n_late_half_cycles': 0,
        'adiabaticity_valid': False,
    }
    if (t.ndim != 1 or len(t) < 2 or not np.all(np.isfinite(t))
            or np.any(np.diff(t) <= 0.0)):
        return unavailable
    if not (0.0 < tail_fraction < 1.0) or min_half_cycles < 1:
        raise ValueError("tail_fraction must be in (0, 1) and min_half_cycles >= 1")

    # Define the tail by elapsed physical time, not by an index fraction.
    # This remains invariant when callers choose a nonuniform t_eval grid.
    tail_start = float(t[0] + (1.0 - tail_fraction) * (t[-1] - t[0]))

    # Prefer the same dense-output half-cycle records used by the Q, virial,
    # and w estimators. H was integrated over each interval, so H/omega is
    # evaluated on identical physical cycle boundaries without re-detecting
    # extrema on the user-selected output grid.
    dense_turning = np.asarray(result.get('cycle_turning_times', []), dtype=float)
    dense_hubble = np.asarray(result.get('H_avg_cycle', []), dtype=float)
    if (dense_turning.ndim == 1 and dense_hubble.ndim == 1
            and len(dense_turning) == len(dense_hubble) + 1
            and len(dense_hubble) > 0
            and np.all(np.isfinite(dense_turning))
            and np.all(np.diff(dense_turning) > 0.0)
            and np.all(np.isfinite(dense_hubble))):
        dense_ratios = []
        for index, (start, end) in enumerate(zip(
            dense_turning[:-1], dense_turning[1:]
        )):
            midpoint = 0.5 * (start + end)
            if midpoint < tail_start or end > t[-1] or end <= start:
                continue
            omega_half = np.pi / (end - start)
            ratio = float(dense_hubble[index]) / omega_half
            if np.isfinite(ratio):
                dense_ratios.append(ratio)
        if len(dense_ratios) < min_half_cycles:
            return {
                'H_over_omega_max': float('nan'),
                'H_over_omega_values': dense_ratios,
                'n_late_half_cycles': len(dense_ratios),
                'adiabaticity_valid': False,
            }
        last_ratios = dense_ratios[-min_half_cycles:]
        maximum = float(max(last_ratios))
        return {
            'H_over_omega_max': maximum,
            'H_over_omega_values': last_ratios,
            'n_late_half_cycles': len(dense_ratios),
            'adiabaticity_valid': maximum < 0.1,
        }

    if (H.shape != t.shape or psi_dot.shape != t.shape or len(t) < 8):
        return unavailable

    turning_times = []
    # A zero is a turning point only when the derivative changes sign
    # across it. This excludes tangential touches and unbracketed endpoints.
    nonzero_indices = np.flatnonzero(np.isfinite(psi_dot) & (psi_dot != 0.0))
    for left_index, right_index in zip(nonzero_indices[:-1], nonzero_indices[1:]):
        if not np.all(np.isfinite(psi_dot[left_index:right_index + 1])):
            continue
        left, right = psi_dot[left_index], psi_dot[right_index]
        if np.signbit(left) == np.signbit(right):
            continue
        if right_index == left_index + 1:
            crossing = (t[left_index] - left *
                        (t[right_index] - t[left_index]) / (right - left))
        else:
            # A sampled zero plateau is bracketed by opposite signs.
            crossing = float(np.mean(t[left_index + 1:right_index]))
        if (not turning_times or
                crossing - turning_times[-1] > 1.0e-12 * max(1.0, abs(crossing))):
            turning_times.append(float(crossing))

    ratios = []
    for start, end in zip(turning_times[:-1], turning_times[1:]):
        if start < tail_start or end > t[-1] or end <= start:
            continue
        lo = max(0, int(np.searchsorted(t, start, side='left')) - 1)
        hi = min(len(t) - 1, int(np.searchsorted(t, end, side='right')))
        h_segment = H[lo:hi + 1]
        if (len(h_segment) < 2 or not np.all(np.isfinite(h_segment))
                or np.any(h_segment < 0.0)):
            continue
        half_period = end - start
        omega = np.pi / half_period
        ratio = float(np.mean(h_segment)) / omega
        if np.isfinite(ratio):
            ratios.append(float(ratio))

    if len(ratios) < min_half_cycles:
        return {
            'H_over_omega_max': float('nan'),
            'H_over_omega_values': ratios,
            'n_late_half_cycles': len(ratios),
            'adiabaticity_valid': False,
        }
    last_ratios = ratios[-min_half_cycles:]
    maximum = float(max(last_ratios))
    return {
        'H_over_omega_max': maximum,
        'H_over_omega_values': last_ratios,
        'n_late_half_cycles': len(ratios),
        'adiabaticity_valid': maximum < 0.1,
    }


def classify_outcome(result: Dict, params: PTUMParameters) -> Dict:
    """
    Classify simulation outcome based on diagnostics.
    
    Returns classification dict with:
    - regime: 'quartic', 'quadratic_candidate', 'non_quartic', 'insufficient_oscillation_data', 'failed'
    - quartic_achieved: bool
    - w_final: final time-averaged w
    - Q_final: final quartic dominance
    - virial_final: final virial ratio
    """
    if not result['success']:
        return {'regime': 'failed', 'quartic_achieved': False}
    
    w_avg = np.asarray(result['w_psi_avg'], dtype=float)
    cycle_times = np.asarray(result.get('t_avg', []), dtype=float)
    q_cycles = np.asarray(result.get('Q_cycle', []), dtype=float)
    virial_cycles = np.asarray(result.get('virial_ratio_cycle', []), dtype=float)
    quadratic_virial = np.asarray(result.get('quadratic_virial_ratio', []), dtype=float)
    adiabaticity = _late_time_adiabaticity_diagnostic(result)

    # Apply one physical late-time window to all dense half-cycle estimators.
    # A cycle belongs to the tail only if its midpoint lies in the final 20%.
    time = np.asarray(result.get('t', []), dtype=float)
    tail_start = (
        float(time[0] + 0.8 * (time[-1] - time[0]))
        if len(time) >= 2 and np.all(np.isfinite(time))
        and np.all(np.diff(time) > 0.0) else float('inf')
    )
    if (cycle_times.ndim == 1 and q_cycles.shape == cycle_times.shape
            and virial_cycles.shape == cycle_times.shape):
        tail_mask = cycle_times >= tail_start
        q_valid = q_cycles[tail_mask & np.isfinite(q_cycles)]
        v_valid = virial_cycles[tail_mask & np.isfinite(virial_cycles)]
        w_tail = w_avg[tail_mask & np.isfinite(w_avg)] if w_avg.shape == cycle_times.shape else np.array([])
    else:
        # Compatibility path for older serialized results lacking cycle arrays.
        q_values = np.asarray(result.get('Q', []), dtype=float)
        v_values = np.asarray(result.get('virial_ratio', []), dtype=float)
        if time.ndim == 1 and len(time) == len(q_values) == len(v_values):
            sample_tail = time >= tail_start
            q_valid = q_values[sample_tail & np.isfinite(q_values)]
            v_valid = v_values[sample_tail & np.isfinite(v_values)]
        else:
            q_valid = q_values[int(0.8 * len(q_values)):]
            v_valid = v_values[int(0.8 * len(v_values)):]
            q_valid = q_valid[np.isfinite(q_valid)]
            v_valid = v_valid[np.isfinite(v_valid)]
        w_tail = w_avg[-3:][np.isfinite(w_avg[-3:])]
    if time.ndim == 1 and len(time) == len(quadratic_virial):
        qv_tail = quadratic_virial[(time >= tail_start)]
    else:
        qv_tail = quadratic_virial[int(0.8 * len(quadratic_virial)):]
    qv_valid = qv_tail[np.isfinite(qv_tail)]
    w_final = float(np.mean(w_tail)) if len(w_tail) else float("nan")
    Q_final = float(np.mean(q_valid)) if len(q_valid) else float("nan")
    virial_final = float(np.mean(v_valid)) if len(v_valid) else float("nan")
    quadratic_virial_final = float(np.mean(qv_valid)) if len(qv_valid) else float("nan")

    # Do not classify a regime when the required diagnostics are unavailable.
    diagnostics_valid = np.isfinite([w_final, Q_final, virial_final]).all()
    # Q = lambda <psi^4>/<|m_eff^2| psi^2> is twice the
    # quartic-to-tachyonic-quadratic potential-energy ratio:
    # <V4>/<|V2|> = Q/2. Thus Q>2 is the energy-dominance boundary.
    quartic_to_tachyonic_potential_ratio = 0.5 * Q_final
    quartic_candidate_shape = (
        diagnostics_valid and
        quartic_to_tachyonic_potential_ratio > 1.0 and
        abs(w_final - 1/3) < 0.05 and
        abs(virial_final - 1) < 0.2
    )
    quadratic_candidate_shape = (
        diagnostics_valid and abs(w_final) < 0.1 and Q_final < 1 and
        np.isfinite(quadratic_virial_final) and
        abs(quadratic_virial_final - 1.0) < 0.2
    )
    adiabaticity_measured = np.isfinite(adiabaticity['H_over_omega_max'])
    quartic_achieved = (
        quartic_candidate_shape and adiabaticity['adiabaticity_valid']
    )

    if not diagnostics_valid:
        regime = 'insufficient_oscillation_data'
    elif quartic_candidate_shape or quadratic_candidate_shape:
        if not adiabaticity_measured:
            regime = 'insufficient_oscillation_data'
        elif not adiabaticity['adiabaticity_valid']:
            regime = 'non_quartic'
        elif quartic_candidate_shape:
            regime = 'quartic'
        else:
            # Matter-like equation of state, quadratic virial balance, and
            # adiabatic oscillations are required; this is not attractor proof.
            regime = 'quadratic_candidate'
    else:
        # w alone does not establish barrier crossing. In particular, a
        # tachyonic/negative contribution can produce w > 1 without any
        # direct measurement of a field-space barrier crossing.
        regime = 'non_quartic'
    
    return {
        'regime': regime,
        'quartic_achieved': quartic_achieved,
        'w_final': float(w_final),
        'Q_final': float(Q_final),
        'quartic_to_tachyonic_potential_ratio': float(quartic_to_tachyonic_potential_ratio),
        'virial_final': float(virial_final),
        'quadratic_virial_final': float(quadratic_virial_final),
        'H_over_omega_max': float(adiabaticity['H_over_omega_max']),
        'H_over_omega_values': adiabaticity['H_over_omega_values'],
        'n_late_half_cycles': int(adiabaticity['n_late_half_cycles']),
        'adiabaticity_valid': bool(adiabaticity['adiabaticity_valid']),
        'n_oscillations': len(w_avg),
        'cycle_quadrature_relative_error_max': result.get(
            'cycle_quadrature_relative_error_max', float('nan')
        ),
        'cycle_quadrature_normalized_absolute_error_max': result.get(
            'cycle_quadrature_normalized_absolute_error_max', float('nan')
        ),
    }


def _json_safe(value):
    """Convert NumPy values and non-finite floats to strict JSON values."""
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def save_results(results: List[Dict], filepath: str):
    """Save a strict-JSON summary, excluding large time-series arrays."""
    # Create summary without full time series
    summary = []
    for r in results:
        if r['success']:
            # Convert numpy types to Python native types
            classification = r['classification']
            class_dict = {}
            for k, v in classification.items():
                if isinstance(v, (np.bool_, np.integer, np.floating)):
                    class_dict[k] = v.item()
                else:
                    class_dict[k] = v
            
            summary.append({
                'success': True,
                'classification': class_dict,
                'solver_stats': _json_safe(r.get('solver_stats', {})),
                'scan_metadata': _json_safe(r.get('scan_metadata', {})),
                'ic_params': r['ic_params'],
                'max_abs_psi_over_trajectory': float(np.max(np.abs(r['psi']))),
                'final_Phi': float(r['Phi'][-1]),
                'final_Phi_dot': float(r['Phi_dot'][-1]),
                'final_psi': float(r['psi'][-1]),
                'final_psi_dot': float(r['psi_dot'][-1]),
                'final_H': float(r['H'][-1]),
                'final_rho_total': float(r['rho_total'][-1]),
                'final_w_psi_exc': _json_safe(r['w_psi_exc'][-1]),
                'final_Q': _json_safe(r['Q'][-1]),
                'final_virial_ratio': _json_safe(r['virial_ratio'][-1]),
                'max_abs_relative_frw_continuity_residual': float(np.nanmax(
                    np.abs(r['continuity_residual_relative'])
                )),
                'max_abs_finite_difference_frw_residual_over_Hrho': float(np.nanmax(
                    np.abs(r['continuity_residual_finite_difference_background_relative'])
                ))
            })
        else:
            summary.append({
                'success': False,
                'error': r.get('error', 'Unknown'),
                'solver_stats': _json_safe(r.get('solver_stats', {})),
                'scan_metadata': _json_safe(r.get('scan_metadata', {})),
                'ic_params': r['ic_params']
            })
    
    # Atomic replacement preserves the last complete checkpoint on interruption.
    temporary_path = f"{filepath}.tmp"
    with open(temporary_path, 'w', encoding='utf-8') as f:
        json.dump(_json_safe(summary), f, indent=2, allow_nan=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporary_path, filepath)


# ============================================================
# Main execution for testing
# ============================================================

def run_baseline_tests():
    """Run baseline simulation tests with paper parameters."""
    print("=" * 60)
    print("PTUM Task 1: Tachyonic-to-Quartic Transition Simulation")
    print("=" * 60)
    
    # Low-scale control benchmark - underdamped regime (V0=1e56)
    params = PTUMParameters(
        V0=1e56,
        lambda_phi=0.02,
        m_psi=1e13,
        lambda_psi=0.1,
        E_th=1e16
    )
    
    print(f"\nParameters:")
    print(f"  V0 = {params.V0:.1e} GeV^4")
    print(f"  lambda_phi = {params.lambda_phi}")
    print(f"  m_psi = {params.m_psi:.1e} GeV")
    print(f"  lambda_psi = {params.lambda_psi}")
    print(f"  E_th = {params.E_th:.1e} GeV")
    print(f"  Phi_c = {params.Phi_c:.2e} GeV")
    print(f"  alpha = {params.alpha:.2e}")
    print(f"  mu = {params.mu:.2e} GeV")
    print(f"  psi_0 = {params.psi_0:.2e} GeV")
    print(f"  H_* = {params.H_star:.2e} GeV")
    print(f"  H_c (potential dominated) = {params.H_threshold_potential:.2e} GeV")
    print(f"  3H_c/(2mu) = {params.damping_ratio:.3f}")
    print(f"  3H_*/(2mu) = {params.damping_ratio_plateau:.3f}")
    
    # Time span: ~100 oscillations
    mu = params.mu
    t_span = (0, 200 / mu)
    t_eval = np.linspace(t_span[0], t_span[1], 20000)
    
    # Test 1: Waterfall field seeded just below the critical threshold
    print("\n" + "=" * 60)
    print("Test 1: Waterfall seed (psi=0.01*psi_0, psi_dot=0, Phi=0.99 Phi_c)")
    print("=" * 60)
    
    ic1 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=0.0, phi_ratio=0.99)
    result1 = run_simulation(params, ic1, t_span, t_eval)
    classification1 = classify_outcome(result1, params)
    
    print(f"  Regime: {classification1['regime']}")
    print(f"  Quartic achieved: {classification1['quartic_achieved']}")
    print(f"  Final <w> = {classification1['w_final']:.4f}")
    print(f"  Final Q = {classification1['Q_final']:.4f}")
    print(f"  Final virial = {classification1['virial_final']:.4f}")
    print(f"  Oscillations: {classification1['n_oscillations']}")
    print(f"  Max |psi| = {np.max(np.abs(result1['psi'])):.2e} GeV")
    print(f"  psi_0 = {params.psi_0:.2e} GeV")
    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result1['psi']))/params.psi_0:.2f}")
    
    # Test 2: Non-zero initial velocity
    print("\n" + "=" * 60)
    print("Test 2: Non-zero initial velocity (psi_dot = 0.1 mu psi_0)")
    print("=" * 60)
    
    psi_dot_init = 0.1 * mu * params.psi_0
    ic2 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=psi_dot_init, phi_ratio=0.99)
    result2 = run_simulation(params, ic2, t_span, t_eval)
    classification2 = classify_outcome(result2, params)
    
    print(f"  Regime: {classification2['regime']}")
    print(f"  Quartic achieved: {classification2['quartic_achieved']}")
    print(f"  Final <w> = {classification2['w_final']:.4f}")
    print(f"  Final Q = {classification2['Q_final']:.4f}")
    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result2['psi']))/params.psi_0:.2f}")
    
    # Test 3: Larger Phi offset (Phi = 1.1 Phi_c)
    print("\n" + "=" * 60)
    print("Test 3: Larger Phi offset (Phi = 1.1 Phi_c)")
    print("=" * 60)
    
    ic3 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=0.0, phi_ratio=1.1)
    result3 = run_simulation(params, ic3, t_span, t_eval)
    classification3 = classify_outcome(result3, params)
    
    print(f"  Regime: {classification3['regime']}")
    print(f"  Quartic achieved: {classification3['quartic_achieved']}")
    print(f"  Final <w> = {classification3['w_final']:.4f}")
    print(f"  Final Q = {classification3['Q_final']:.4f}")
    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result3['psi']))/params.psi_0:.2f}")
    
    # Test 4: Combined - larger Phi offset + initial velocity
    print("\n" + "=" * 60)
    print("Test 4: Larger Phi offset + initial velocity")
    print("=" * 60)
    
    ic4 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=psi_dot_init, phi_ratio=1.1)
    result4 = run_simulation(params, ic4, t_span, t_eval)
    classification4 = classify_outcome(result4, params)
    
    print(f"  Regime: {classification4['regime']}")
    print(f"  Quartic achieved: {classification4['quartic_achieved']}")
    print(f"  Final <w> = {classification4['w_final']:.4f}")
    print(f"  Final Q = {classification4['Q_final']:.4f}")
    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result4['psi']))/params.psi_0:.2f}")
    
    print("\n" + "=" * 60)
    print("Baseline tests complete. Ready for parameter scan.")
    print("=" * 60)
    
    print(f"  Regime: {classification4['regime']}")
    print(f"  Quartic achieved: {classification4['quartic_achieved']}")
    print(f"  Final <w> = {classification4['w_final']:.4f}")
    print(f"  Final Q = {classification4['Q_final']:.4f}")
    print(f"  Max |psi|/psi_0 = {np.max(np.abs(result4['psi']))/params.psi_0:.2f}")
    
    print("\n" + "=" * 60)
    print("Baseline tests complete. Ready for parameter scan.")
    print("=" * 60)


if __name__ == "__main__":
    run_baseline_tests()
    # Run parameter scan
    print("\n" + "=" * 60)
    print("Running parameter scan...")
    print("=" * 60)
    
    params = PTUMParameters(
        V0=1e56,
        lambda_phi=0.02,
        m_psi=1e13,
        lambda_psi=0.1,
        E_th=1e16
    )
    
    # Define parameter ranges for scan (smaller for quick test)
    psi_init_range = [0.0, 0.01*params.psi_0, 0.1*params.psi_0]
    psi_dot_init_range = [0.0, 0.1*params.mu*params.psi_0, params.mu*params.psi_0]
    phi_offset_range = [0.01*params.Phi_c, 0.1*params.Phi_c]
    
    results = run_parameter_scan(params, psi_init_range, psi_dot_init_range, phi_offset_range, t_max=20.0, n_points=200)
    
    # Save results
    save_results(results, "task1_parameter_scan_results.json")
    print(f"\nSaved {len(results)} results to task1_parameter_scan_results.json")