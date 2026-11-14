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
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Callable
import json
import os
import math

# Physical constants (natural units: c = ħ = k_B = 1)
M_PL = 2.435e18  # GeV (reduced Planck mass)
GEV_TO_S = 6.582e-25  # 1 GeV^-1 = 6.582e-25 s


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
    rho_tot = rho_total(Phi, Phi_dot, psi, psi_dot, params, rho_other)
    if not np.isfinite(rho_tot) or rho_tot <= 0.0:
        raise ValueError(f"Non-positive or non-finite total density: {rho_tot}")
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


def run_simulation(params: PTUMParameters, 
                   ic: InitialConditions,
                   t_span: Tuple[float, float],
                   t_eval: Optional[np.ndarray] = None,
                   rtol: float = 1e-9,
                   atol: float = 1e-12) -> Dict:
    """
    Run a single background simulation.
    
    Returns dictionary with time series and diagnostics.
    """
    # Integrate in dimensionless variables.  The physical state contains
    # components separated by 17+ orders of magnitude (GeV fields and
    # GeV^2 velocities); integrating that raw vector makes the adaptive
    # error norm poorly balanced and can turn a stable trajectory into a
    # numerically unresolved one.
    #
    #   tau = mu t, x = Phi/M_Pl, u = Phi_dot/(mu M_Pl)
    #   z = psi/psi_0, v = psi_dot/(mu psi_0), psi_0 = mu/sqrt(lambda_psi)
    #
    # This is an exact change of variables, not a change to the model.
    mu = float(params.mu)
    psi_scale = float(params.psi_0)
    if (not np.isfinite(mu) or mu <= 0.0 or
            not np.isfinite(psi_scale) or psi_scale <= 0.0):
        raise ValueError("Dimensionless integration requires finite positive mu and psi_0")
    psi_ratio = psi_scale / M_PL
    coupling = params.alpha * params.m_psi**2 / params.E_th**2

    def dimensionless_background_equations(tau: float, state: np.ndarray,
                                           model: PTUMParameters) -> np.ndarray:
        x, u, z, v = state
        Phi = M_PL * x
        m_eff_ratio = meff_sq_psi(Phi, model) / mu**2
        rho_bar = (
            0.5 * u**2
            + veff_phi(Phi, model) / (mu**2 * M_PL**2)
            + 0.5 * psi_ratio**2 * (v**2 + m_eff_ratio * z**2 + 0.5 * z**4)
        )
        if not np.isfinite(rho_bar) or rho_bar <= 0.0:
            raise ValueError(
                f"Non-positive or non-finite dimensionless total density: {rho_bar}"
            )
        h = np.sqrt(rho_bar / 3.0)
        dV_bar_dx = dveff_dphi(Phi, model) / (mu**2 * M_PL)
        interaction_bar = coupling * x / model.lambda_psi
        u_dot = -3.0 * h * u - dV_bar_dx - interaction_bar * z**2
        v_dot = -3.0 * h * v - m_eff_ratio * z - z**3
        return np.array([u, u_dot, v, v_dot], dtype=float)

    y0 = np.array([
        ic.Phi / M_PL,
        ic.Phi_dot / (mu * M_PL),
        ic.psi / psi_scale,
        ic.psi_dot / (mu * psi_scale),
    ], dtype=float)
    tau_span = (mu * t_span[0], mu * t_span[1])
    tau_eval = None if t_eval is None else np.asarray(t_eval, dtype=float) * mu

    sol = solve_ivp(
        dimensionless_background_equations,
        tau_span,
        y0,
        args=(params,),
        t_eval=tau_eval,
        rtol=rtol,
        atol=atol,
        method='DOP853',
        dense_output=False,
        max_step=0.05,
    )

    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    # Restore the physical variables for all downstream diagnostics and
    # serialized results.  The public result schema remains unchanged.
    t = sol.t / mu
    Phi = M_PL * sol.y[0]
    Phi_dot = mu * M_PL * sol.y[1]
    psi = psi_scale * sol.y[2]
    psi_dot = mu * psi_scale * sol.y[3]
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
    
    # Quartic diagnostics are evaluated over complete half-cycles.
    # NaN denotes that no valid oscillation interval was available.
    U_psi = 0.25 * params.lambda_psi * psi**4
    virial_ratio = compute_quartic_virial_ratio(t, psi, psi_dot, params)
    quadratic_virial_ratio = compute_quadratic_virial_ratio(
        t, psi, psi_dot, Phi, params
    )
    Q_arr = compute_quartic_dominance(t, psi, psi_dot, params, Phi)
    
    # Average the excitation-sector equation of state, not the raw
    # potential density whose moving minimum can be negative.
    w_avg, t_avg = compute_time_averaged_w(
        t, p_psi_exc_arr, rho_psi_exc_arr, psi_dot
    )
    w_avg_raw, t_avg_raw = compute_time_averaged_w(
        t, p_psi_arr, rho_psi_arr, psi_dot
    )
    
    return {
        'success': True,
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
        't_avg': t_avg,
        't_avg_raw': t_avg_raw,
        'U_psi': U_psi,
        'virial_ratio': virial_ratio,
        'quadratic_virial_ratio': quadratic_virial_ratio,
        'Q': Q_arr,
        'params': params,
        'ic': ic
    }


def _turning_point_indices(psi_dot: np.ndarray) -> np.ndarray:
    """Return sampled boundaries for genuine velocity sign reversals.

    An exactly zero initial velocity is retained as the prescribed initial
    turning point. Interior zeros count only when bracketed by opposite
    nonzero signs; tangential touches and an unbracketed final zero are ignored.
    """
    derivative = np.asarray(psi_dot, dtype=float)
    if derivative.ndim != 1 or len(derivative) < 2:
        return np.array([], dtype=int)

    boundaries = []
    if np.isfinite(derivative[0]) and derivative[0] == 0.0:
        first_nonzero = np.flatnonzero(
            np.isfinite(derivative) & (derivative != 0.0)
        )
        if len(first_nonzero):
            boundaries.append(0)

    nonzero_indices = np.flatnonzero(
        np.isfinite(derivative) & (derivative != 0.0)
    )
    for left, right in zip(nonzero_indices[:-1], nonzero_indices[1:]):
        if np.signbit(derivative[left]) == np.signbit(derivative[right]):
            continue
        if right > left + 1:
            interior = derivative[left + 1:right]
            if not np.all(np.isfinite(interior)) or not np.all(interior == 0.0):
                continue
            boundary = (left + right) // 2
        else:
            boundary = left
        if not boundaries or boundary > boundaries[-1]:
            boundaries.append(int(boundary))
    return np.asarray(boundaries, dtype=int)


def _turning_point_times(t: np.ndarray, psi_dot: np.ndarray) -> list[float]:
    """Return interpolated times of genuine velocity reversals."""
    times = np.asarray(t, dtype=float)
    derivative = np.asarray(psi_dot, dtype=float)
    if (times.ndim != 1 or derivative.shape != times.shape or len(times) < 2
            or not np.all(np.isfinite(times)) or np.any(np.diff(times) <= 0.0)):
        return []

    turning_times = []
    if np.isfinite(derivative[0]) and derivative[0] == 0.0:
        if np.any(np.isfinite(derivative[1:]) & (derivative[1:] != 0.0)):
            turning_times.append(float(times[0]))

    nonzero_indices = np.flatnonzero(
        np.isfinite(derivative) & (derivative != 0.0)
    )
    for left, right in zip(nonzero_indices[:-1], nonzero_indices[1:]):
        if np.signbit(derivative[left]) == np.signbit(derivative[right]):
            continue
        if right > left + 1:
            interior = derivative[left + 1:right]
            if not np.all(np.isfinite(interior)) or not np.all(interior == 0.0):
                continue
            crossing = float(np.mean(times[left + 1:right]))
        else:
            fraction = -derivative[left] / (derivative[right] - derivative[left])
            crossing = float(times[left] + fraction * (times[right] - times[left]))
        if (not turning_times or
                crossing - turning_times[-1] > 1.0e-12 * max(1.0, abs(crossing))):
            turning_times.append(crossing)
    return turning_times


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
    turning_points = _turning_point_indices(psi_dot)
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
    turning_points = _turning_point_indices(psi_dot)
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
    turning_points = _turning_point_indices(psi_dot)
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


def compute_time_averaged_w(t: np.ndarray, pressure: np.ndarray,
                            density: np.ndarray,
                            psi_dot: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute cycle-averaged w as <p>/<rho>, not as <p/rho>.

    Turning points of psi delimit half-oscillation intervals. The ratio of
    separately averaged pressure and density is the physically relevant
    coarse-grained equation of state; averaging the instantaneous ratio can
    overweight epochs where rho is small.
    """
    turning_points = _turning_point_indices(psi_dot)

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
                       result_callback: Optional[Callable[[Dict], None]] = None
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
                
                try:
                    result = run_simulation(params, ic, t_span, t_eval)
                    
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
    if (t.ndim != 1 or H.shape != t.shape or psi_dot.shape != t.shape
            or len(t) < 8 or not np.all(np.isfinite(t))
            or np.any(np.diff(t) <= 0.0)):
        return unavailable
    if not (0.0 < tail_fraction < 1.0) or min_half_cycles < 1:
        raise ValueError("tail_fraction must be in (0, 1) and min_half_cycles >= 1")

    tail_start = t[int(np.floor((1.0 - tail_fraction) * (len(t) - 1)))]
    turning_times = _turning_point_times(t, psi_dot)

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


def _transient_quartic_episode_diagnostic(
    result: Dict,
    min_consecutive_half_cycles: int = 3,
) -> Dict:
    """Identify transient quartic-like episodes without calling them attractors.

    A half-cycle is a candidate only when the same conservative conditions
    used by the late-time classifier hold simultaneously: Q>2,
    |w-1/3|<0.05, |R_vir-1|<0.2, and H/omega<0.1.  A transient episode
    requires at least three consecutive candidate half-cycles.
    """
    empty = {
        "transient_quartic_candidate_half_cycles": 0,
        "transient_quartic_max_consecutive_half_cycles": 0,
        "transient_quartic_episode_count": 0,
        "transient_quartic_episode_detected": False,
        "transient_quartic_episodes": [],
        "transient_quartic_last_episode_end_mu_inverse": None,
        "transient_quartic_max_episode_duration_mu_inverse": 0.0,
    }
    if min_consecutive_half_cycles < 1:
        raise ValueError("min_consecutive_half_cycles must be positive")

    t = np.asarray(result.get("t", []), dtype=float)
    H = np.asarray(result.get("H", []), dtype=float)
    psi_dot = np.asarray(result.get("psi_dot", []), dtype=float)
    Q = np.asarray(result.get("Q", []), dtype=float)
    virial = np.asarray(result.get("virial_ratio", []), dtype=float)
    w_avg = np.asarray(result.get("w_psi_avg", []), dtype=float)
    t_avg = np.asarray(result.get("t_avg", []), dtype=float)
    if (t.ndim != 1 or len(t) < 8 or H.shape != t.shape
            or psi_dot.shape != t.shape or Q.shape != t.shape
            or virial.shape != t.shape or not np.all(np.isfinite(t))
            or np.any(np.diff(t) <= 0.0)):
        return empty

    turning_times = _turning_point_times(t, psi_dot)
    if len(turning_times) < 2 or len(w_avg) == 0:
        return empty

    candidate_intervals = []
    for i, (start_time, end_time) in enumerate(zip(turning_times[:-1], turning_times[1:])):
        left = max(0, int(np.searchsorted(t, start_time, side="left")) - 1)
        right = min(len(t) - 1, int(np.searchsorted(t, end_time, side="right")))
        if right - left < 2 or end_time <= start_time:
            candidate_intervals.append((False, float(start_time), float(end_time)))
            continue
        segment = slice(left, right + 1)
        q_values = Q[segment]
        virial_values = virial[segment]
        h_values = H[segment]
        q_values = q_values[np.isfinite(q_values)]
        virial_values = virial_values[np.isfinite(virial_values)]
        h_values = h_values[np.isfinite(h_values)]
        midpoint = 0.5 * (start_time + end_time)
        if len(t_avg) == len(w_avg) and len(t_avg):
            w_index = int(np.argmin(np.abs(t_avg - midpoint)))
            w_value = float(w_avg[w_index])
        elif i < len(w_avg):
            w_value = float(w_avg[i])
        else:
            w_value = float("nan")
        q_value = float(np.mean(q_values)) if len(q_values) else float("nan")
        virial_value = (
            float(np.mean(virial_values)) if len(virial_values) else float("nan")
        )
        half_period = float(end_time - start_time)
        omega = np.pi / half_period
        h_over_omega = (
            float(np.mean(h_values)) / omega if len(h_values) else float("nan")
        )
        candidate = (
            np.isfinite([q_value, virial_value, w_value, h_over_omega]).all()
            and q_value > 2.0
            and abs(w_value - 1.0 / 3.0) < 0.05
            and abs(virial_value - 1.0) < 0.2
            and h_over_omega < 0.1
        )
        candidate_intervals.append((bool(candidate), float(start_time), float(end_time)))

    runs = []
    current = []
    for interval in candidate_intervals:
        if interval[0]:
            current.append(interval)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)

    max_run = max((len(run) for run in runs), default=0)
    episode_runs = [run for run in runs if len(run) >= min_consecutive_half_cycles]
    params = result.get("params")
    mu = float(getattr(params, "mu", 1.0))
    if not np.isfinite(mu) or mu <= 0.0:
        mu = 1.0
    episode_details = []
    for run in episode_runs:
        start_mu = float(run[0][1] * mu)
        end_mu = float(run[-1][2] * mu)
        duration_mu = float(sum(end - start for _, start, end in run) * mu)
        episode_details.append({
            "start_mu_inverse": start_mu,
            "end_mu_inverse": end_mu,
            "half_cycles": int(len(run)),
            "duration_mu_inverse": duration_mu,
        })
    max_duration = max(
        (episode["duration_mu_inverse"] for episode in episode_details),
        default=0.0,
    )
    return {
        "transient_quartic_candidate_half_cycles": int(
            sum(candidate for candidate, _, _ in candidate_intervals)
        ),
        "transient_quartic_max_consecutive_half_cycles": int(max_run),
        "transient_quartic_episode_count": int(len(episode_details)),
        "transient_quartic_episode_detected": bool(episode_details),
        "transient_quartic_episodes": episode_details,
        "transient_quartic_last_episode_end_mu_inverse": (
            episode_details[-1]["end_mu_inverse"] if episode_details else None
        ),
        "transient_quartic_max_episode_duration_mu_inverse": float(max_duration),
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
    
    w_avg = result['w_psi_avg']
    Q = result['Q']
    virial = result['virial_ratio']
    quadratic_virial = result.get('quadratic_virial_ratio', np.array([]))
    adiabaticity = _late_time_adiabaticity_diagnostic(result)

    # Classify the late-time regime, not the whole trajectory.
    # Q and virial are sampled diagnostics; use the final 20% of the run.
    tail_start_q = int(0.8 * len(Q))
    tail_start_v = int(0.8 * len(virial))
    q_tail = Q[tail_start_q:] if len(Q) else np.array([])
    v_tail = virial[tail_start_v:] if len(virial) else np.array([])
    qv_tail = quadratic_virial[tail_start_v:] if len(quadratic_virial) else np.array([])
    q_valid = q_tail[np.isfinite(q_tail)]
    v_valid = v_tail[np.isfinite(v_tail)]
    qv_valid = qv_tail[np.isfinite(qv_tail)]
    w_final = float(np.mean(w_avg[-3:])) if len(w_avg) >= 3 else (
        float(w_avg[-1]) if len(w_avg) else float("nan"))
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
        **_transient_quartic_episode_diagnostic(result),
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
                'classification': class_dict,
                'scan_metadata': _json_safe(r.get('scan_metadata', {})),
                'ic_params': r['ic_params'],
                'max_abs_psi_over_trajectory': float(np.max(np.abs(r['psi']))),
                'final_Phi': float(r['Phi'][-1]),
                'max_abs_relative_frw_continuity_residual': float(np.nanmax(
                    np.abs(r['continuity_residual_relative'])
                ))
            })
        else:
            summary.append({
                'success': False,
                'error': r.get('error', 'Unknown'),
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