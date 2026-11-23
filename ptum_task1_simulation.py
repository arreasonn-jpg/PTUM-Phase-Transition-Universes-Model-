#!/usr/bin/env python3
"""
PTUM Task 1: Tachyonic-to-Quartic Transition Numerical Simulation

This module implements the coupled background evolution equations for the
PTUM discharge dynamics to determine whether and under what conditions
the proxy field ψ transitions to a quartic-dominated oscillatory regime
with radiation-like equation of state (w = 1/3).

Equations (from main.tex Sec 3.5.6, Eqs 3.18-3.21):
  Φ̈ + 3HΦ̇ + ∂V_eff/∂Φ - (αm²/E_th²)Φψ² = 0
  ψ̈ + 3Hψ̇ + m²(1 - αΦ²/E_th²)ψ + λ_ψψ³ = 0
  H² = (1/3M_Pl²)(ρ_Φ + ρ_ψ + ρ_χ + ρ_res + ρ_rad)

Energy densities (interaction allocated exactly once to the ψ sector):
  ρ_Φ = ½Φ̇² + V_eff(Φ)
  ρ_ψ = ½ψ̇² + ½m_eff²(Φ)ψ² + ¼λ_ψψ⁴

Shifted potential for ψ (energy measured from minimum):
  U(ψ) = ¼λ_ψ(ψ² - ψ₀²)²,  ψ₀² = μ²/λ_ψ,  μ² = |m_eff²|

Diagnostics:
  w_ψ = p_ψ/ρ_ψ from the unshifted field-dependent potential
  Q = ⟨V₄⟩/⟨|V₂|⟩, evaluated with m_eff²(Φ) on each half-cycle
  Virial ratio = ⟨ψ̇²⟩/(4⟨V₄⟩), which tends to 1 in a quartic regime
  Total energy is tested with ρ̇ + 3H(ρ+p)=0, not by assuming ρ is constant
"""

import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
import json
import os

# Physical constants (natural units: c = ħ = k_B = 1)
M_PL = 2.435e18  # GeV (reduced Planck mass)
GEV_TO_S = 6.582e-25  # 1 GeV^-1 = 6.582e-25 s


@dataclass
class PTUMParameters:
    """PTUM model parameters for the discharge simulation."""
    # Inflation/discharge parameters
    V0: float = 1e56          # GeV^4, plateau height ~ (10^14 GeV)^4 (for underdamped)
    lambda_phi: float = 0.02  # Fuel potential parameter
    
    # Activation sector parameters
    m_psi: float = 1e13       # GeV, bare mass of ψ
    lambda_psi: float = 0.1   # Quartic coupling
    E_th: float = 1e16        # GeV, threshold scale
    
    # Derived: alpha from Phi_c = M_Pl/sqrt(lambda_phi) ~ 1.7e19 GeV
    @property
    def Phi_c(self) -> float:
        """Critical threshold Φ_c = M_Pl / sqrt(lambda_phi)"""
        return M_PL / np.sqrt(self.lambda_phi)
    
    @property
    def alpha(self) -> float:
        """Threshold coupling α = (E_th/Φ_c)²"""
        return (self.E_th / self.Phi_c)**2
    
    @property
    def mu_sq(self) -> float:
        """μ² = |m_eff²| at Φ = 1.01 Φ_c (just past threshold)"""
        Phi = 1.01 * self.Phi_c
        m_eff_sq = self.m_psi**2 * (1 - self.alpha * Phi**2 / self.E_th**2)
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
    def damping_ratio(self) -> float:
        """3H/(2μ) - determines underdamped (<1) vs overdamped (>1)"""
        return 3 * self.H_star / (2 * self.mu)


@dataclass
class InitialConditions:
    """Initial conditions at threshold crossing t = t_c."""
    Phi: float           # Φ(t_c) = Φ_c (at threshold)
    Phi_dot: float       # Φ̇(t_c) from slow-roll
    psi: float           # ψ(t_c) - homogeneous mode
    psi_dot: float       # ψ̇(t_c)
    # Quantum fluctuation seeds for ensemble runs
    psi_k: Optional[np.ndarray] = None  # Fourier modes
    k_modes: Optional[np.ndarray] = None


def veff_phi(Phi: float, params: PTUMParameters) -> float:
    """Effective potential for fuel field: V_eff(Φ) = V0(1 - exp(-λΦ²))"""
    return params.V0 * (1 - np.exp(-params.lambda_phi * Phi**2))


def dveff_dphi(Phi: float, params: PTUMParameters) -> float:
    """Derivative of V_eff wrt Φ"""
    return params.V0 * 2 * params.lambda_phi * Phi * np.exp(-params.lambda_phi * Phi**2)


def meff_sq_psi(Phi: float, params: PTUMParameters) -> float:
    """Effective mass squared for ψ: m²(1 - αΦ²/E_th²)"""
    return params.m_psi**2 * (1 - params.alpha * Phi**2 / params.E_th**2)


def rho_phi(Phi: float, Phi_dot: float, psi: float, params: PTUMParameters) -> float:
    """Fuel-sector energy density; the Φ-dependent ψ interaction is allocated to ψ."""
    return 0.5 * Phi_dot**2 + veff_phi(Phi, params)


def rho_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Energy density of proxy field ψ"""
    m_eff_sq = meff_sq_psi(Phi, params)
    return 0.5 * psi_dot**2 + 0.5 * m_eff_sq * psi**2 + 0.25 * params.lambda_psi * psi**4


def pressure_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Pressure of proxy field ψ"""
    m_eff_sq = meff_sq_psi(Phi, params)
    return 0.5 * psi_dot**2 - 0.5 * m_eff_sq * psi**2 - 0.25 * params.lambda_psi * psi**4


def minimum_value_psi(Phi: float, params: PTUMParameters) -> float:
    """Instantaneous minimum of the activation potential, zero in the dormant phase."""
    mu_sq = max(-meff_sq_psi(Phi, params), 0.0)
    return -mu_sq**2 / (4.0 * params.lambda_psi)


def dminimum_value_psi_dphi(Phi: float, params: PTUMParameters) -> float:
    """Derivative of the moving minimum with respect to the fuel field."""
    m2 = meff_sq_psi(Phi, params)
    if m2 >= 0.0:
        return 0.0
    dm2 = -2.0 * params.alpha * params.m_psi**2 * Phi / params.E_th**2
    return -(m2 * dm2) / (2.0 * params.lambda_psi)


def shifted_potential_psi(Phi: float, psi: float, params: PTUMParameters) -> float:
    """Instantaneous excitation potential above the moving minimum."""
    m_eff_sq = meff_sq_psi(Phi, params)
    mu_sq = max(-m_eff_sq, 0.0)
    psi0_sq = mu_sq / params.lambda_psi
    return 0.25 * params.lambda_psi * (psi**2 - psi0_sq)**2


def w_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Instantaneous p/rho; undefined when sector energy is numerically zero."""
    p = pressure_psi(Phi, psi, psi_dot, params)
    rho = rho_psi(Phi, psi, psi_dot, params)
    scale = max(abs(p), abs(rho), np.finfo(float).tiny)
    return p / rho if abs(rho) > 32.0 * np.finfo(float).eps * scale else float('nan')


def hubble_rate(Phi: float, Phi_dot: float, psi: float, psi_dot: float, 
                params: PTUMParameters, rho_other: float = 0.0) -> float:
    """Hubble rate H = sqrt(ρ_total/3M_Pl²)"""
    # The interaction term ½ m_eff²(Φ) ψ² is included only in rho_psi.
    rho_tot = rho_phi(Phi, Phi_dot, psi, params) + rho_psi(Phi, psi, psi_dot, params) + rho_other
    if not np.isfinite(rho_tot):
        raise FloatingPointError("Non-finite total energy density in Friedmann equation")
    if rho_tot <= 0.0:
        raise ValueError(
            f"Non-positive total energy density ({rho_tot:.6e} GeV^4); "
            "the background is outside the physical Friedmann branch"
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
    
    # Φ equation: Φ̈ + 3HΦ̇ + ∂V_eff/∂Φ - (αm²/E_th²)Φψ² = 0
    Phi_ddot = -3 * H * Phi_dot - dveff_dphi(Phi, params) + \
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
    y0 = np.array([ic.Phi, ic.Phi_dot, ic.psi, ic.psi_dot])
    
    sol = solve_ivp(
        background_equations,
        t_span,
        y0,
        args=(params,),
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
        method='DOP853',  # High-order Runge-Kutta
        dense_output=True
    )
    
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    
    # Extract solution
    t = sol.t
    Phi = sol.y[0]
    Phi_dot = sol.y[1]
    psi = sol.y[2]
    psi_dot = sol.y[3]
    
    # Compute diagnostics
    H = np.array([hubble_rate(Phi[i], Phi_dot[i], psi[i], psi_dot[i], params) 
                  for i in range(len(t))])
    
    rho_phi_arr = np.array([rho_phi(Phi[i], Phi_dot[i], psi[i], params) for i in range(len(t))])
    rho_psi_arr = np.array([rho_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    p_psi_arr = np.array([pressure_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    w_psi_arr = np.array([w_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    
    # Split the exact activation energy into excitation energy plus the
    # moving minimum. The complementary V_min term is assigned to Phi so
    # that the sum remains exactly the unshifted Hilbert/Friedmann source.
    U_psi = np.array([shifted_potential_psi(Phi[i], psi[i], params) for i in range(len(t))])
    Vmin_psi = np.array([minimum_value_psi(x, params) for x in Phi])
    rho_psi_exc_arr = 0.5 * psi_dot**2 + U_psi
    p_psi_exc_arr = 0.5 * psi_dot**2 - U_psi
    w_psi_exc_arr = np.divide(
        p_psi_exc_arr, rho_psi_exc_arr,
        out=np.full_like(rho_psi_exc_arr, np.nan),
        where=np.abs(rho_psi_exc_arr) > 32*np.finfo(float).eps*np.maximum(
            np.maximum(np.abs(p_psi_exc_arr), np.abs(rho_psi_exc_arr)),
            np.finfo(float).tiny
        )
    )

    # Quartic dominance is measured as <V4>/<|V2|>, with the instantaneous
    # field-dependent mass, rather than a fixed mass sampled at 1.01 Phi_c.
    Q_arr = compute_quartic_dominance(t, Phi, psi, psi_dot, params)
    virial_ratio = compute_quartic_virial_ratio(t, psi, psi_dot, params)
    
    # Cycle-averaged equation of state is <p>/<rho>, not <p/rho>.
    # The latter is biased near turning points and when rho varies strongly.
    w_avg, t_avg = compute_time_averaged_w(t, rho_psi_exc_arr, p_psi_exc_arr, psi_dot)
    
    # Dense-output continuity diagnostic, independent of the requested output grid.
    p_phi_arr = 0.5 * Phi_dot**2 - np.array([veff_phi(x, params) for x in Phi])
    rho_total_arr = rho_phi_arr + rho_psi_arr
    p_total_arr = p_phi_arr + p_psi_arr
    n_diag = max(len(t), 4000)
    t_diag = np.linspace(float(t[0]), float(t[-1]), n_diag)
    y_diag = sol.sol(t_diag)
    phi_d, phi_dot_d, psi_d, psi_dot_d = y_diag
    rho_diag = np.array([rho_phi(phi_d[i], phi_dot_d[i], psi_d[i], params)
                         + rho_psi(phi_d[i], psi_d[i], psi_dot_d[i], params)
                         for i in range(n_diag)])
    p_diag = np.array([0.5 * phi_dot_d[i]**2 - veff_phi(phi_d[i], params)
                       + pressure_psi(phi_d[i], psi_d[i], psi_dot_d[i], params)
                       for i in range(n_diag)])
    h_diag = np.array([hubble_rate(phi_d[i], phi_dot_d[i], psi_d[i], psi_dot_d[i], params)
                       for i in range(n_diag)])
    rho_dot_diag = np.gradient(rho_diag, t_diag, edge_order=2)
    continuity = rho_dot_diag + 3.0 * h_diag * (rho_diag + p_diag)
    continuity_scale = np.maximum.reduce([
        np.abs(rho_dot_diag), np.abs(3.0 * h_diag * (rho_diag + p_diag)),
        np.abs(h_diag * rho_diag), np.full_like(t_diag, np.finfo(float).tiny)
    ])
    max_relative_continuity_residual = float(np.max(np.abs(continuity) / continuity_scale))

    # Check the exact bookkeeping split: V_act = U + V_min. The moving
    # minimum contributes V_min'(Phi)*Phi_dot to the Phi-side transfer.
    m2_diag = np.array([meff_sq_psi(x, params) for x in phi_d])
    vmin_diag = np.array([minimum_value_psi(x, params) for x in phi_d])
    u_diag = np.array([shifted_potential_psi(phi_d[i], psi_d[i], params)
                       for i in range(n_diag)])
    rho_phi_split = 0.5*phi_dot_d**2 + np.array([veff_phi(x, params) for x in phi_d]) + vmin_diag
    p_phi_split = 0.5*phi_dot_d**2 - np.array([veff_phi(x, params) for x in phi_d]) - vmin_diag
    rho_psi_exc_diag = 0.5*psi_dot_d**2 + u_diag
    p_psi_exc_diag = 0.5*psi_dot_d**2 - u_diag
    vmin_prime_diag = np.array([dminimum_value_psi_dphi(x, params) for x in phi_d])
    transfer_phi_split = (
        params.alpha*params.m_psi**2/params.E_th**2
        * phi_d*psi_d**2*phi_dot_d + vmin_prime_diag*phi_dot_d
    )
    rho_phi_dot = np.gradient(rho_phi_split, t_diag, edge_order=2)
    rho_psi_exc_dot = np.gradient(rho_psi_exc_diag, t_diag, edge_order=2)
    residual_phi_split = rho_phi_dot + 3*h_diag*(rho_phi_split+p_phi_split) - transfer_phi_split
    residual_psi_split = rho_psi_exc_dot + 3*h_diag*(rho_psi_exc_diag+p_psi_exc_diag) + transfer_phi_split
    split_scale = np.maximum.reduce([
        np.abs(rho_phi_dot), np.abs(rho_psi_exc_dot),
        np.abs(transfer_phi_split), np.abs(3*h_diag*(rho_phi_split+p_phi_split)),
        np.abs(3*h_diag*(rho_psi_exc_diag+p_psi_exc_diag)),
        np.full_like(t_diag, np.finfo(float).tiny)
    ])
    max_relative_split_continuity_residual = float(np.max(
        np.maximum(np.abs(residual_phi_split), np.abs(residual_psi_split))/split_scale
    ))

    meff_sq_arr = np.array([meff_sq_psi(x, params) for x in Phi])
    tachyonic_duration, tachyonic_fraction, threshold_crossings = \
        _tachyonic_trajectory_diagnostics(t_diag, phi_d, params)
    seedless_invariant = (ic.psi == 0.0 and ic.psi_dot == 0.0)

    return {
        'success': True,
        'max_relative_continuity_residual': max_relative_continuity_residual,
        'max_relative_split_continuity_residual': max_relative_split_continuity_residual,
        'meff_sq': meff_sq_arr,
        'min_meff_sq': float(np.min(meff_sq_arr)),
        'tachyonic_duration': tachyonic_duration,
        'tachyonic_fraction': tachyonic_fraction,
        'threshold_crossings': threshold_crossings,
        'initially_tachyonic': bool(meff_sq_arr[0] < 0.0),
        'finally_tachyonic': bool(meff_sq_arr[-1] < 0.0),
        'seedless_invariant': seedless_invariant,
        'max_abs_psi': float(np.max(np.abs(psi))),
        'max_abs_Phi_over_Phi_c': float(np.max(np.abs(Phi)) / params.Phi_c),
        'rho_total': rho_total_arr,
        'p_total': p_total_arr,
        't': t,
        'Phi': Phi,
        'Phi_dot': Phi_dot,
        'psi': psi,
        'psi_dot': psi_dot,
        'H': H,
        'rho_phi': rho_phi_arr,
        'rho_psi': rho_psi_arr,
        'p_psi': p_psi_arr,
        'w_psi': w_psi_arr,
        'rho_psi_exc': rho_psi_exc_arr,
        'p_psi_exc': p_psi_exc_arr,
        'w_psi_exc': w_psi_exc_arr,
        'Vmin_psi': Vmin_psi,
        'w_psi_avg': w_avg,
        't_avg': t_avg,
        'U_psi': U_psi,
        'virial_ratio': virial_ratio,
        'Q': Q_arr,
        'params': params,
        'ic': ic
    }


def _turning_point_intervals(psi_dot: np.ndarray) -> np.ndarray:
    """Indices bracketing successive ψ̇ sign changes (half-cycle boundaries)."""
    values = np.asarray(psi_dot, dtype=float)
    sign = np.sign(values)
    exact_zeros = np.flatnonzero(sign == 0.0)
    crossings = np.flatnonzero(sign[:-1] * sign[1:] < 0.0)
    # Include exact sampled zeros, but collapse adjacent zero runs to one midpoint.
    zero_groups = []
    if exact_zeros.size:
        groups = np.split(exact_zeros, np.where(np.diff(exact_zeros) > 1)[0] + 1)
        zero_groups = [int(group[len(group) // 2]) for group in groups if len(group)]
    return np.unique(np.concatenate([crossings, np.asarray(zero_groups, dtype=int)])).astype(int)


def _tachyonic_trajectory_diagnostics(t: np.ndarray, Phi: np.ndarray,
                                      params: PTUMParameters) -> Tuple[float, float, List[Dict]]:
    """Integrate time spent beyond threshold and interpolate crossing directions."""
    signed = np.abs(np.asarray(Phi, dtype=float)) - params.Phi_c
    duration, crossings = 0.0, []
    for i in range(len(t) - 1):
        dt = float(t[i + 1] - t[i])
        left, right = float(signed[i]), float(signed[i + 1])
        if left > 0.0 and right > 0.0:
            duration += dt
        elif (left > 0.0) != (right > 0.0):
            frac = abs(left) / (abs(left) + abs(right))
            tc = float(t[i] + frac * dt)
            if left > 0.0:
                duration += frac * dt
                direction = 'tachyonic_to_dormant'
            else:
                duration += (1.0 - frac) * dt
                direction = 'dormant_to_tachyonic'
            crossings.append({'time': tc, 'direction': direction})
    span = float(t[-1] - t[0]) if len(t) > 1 else 0.0
    return duration, duration / span if span > 0.0 else 0.0, crossings


def _time_average(t_seg: np.ndarray, values: np.ndarray) -> float:
    """Trapezoidal time average, valid for uniform or adaptive solver grids."""
    duration = float(t_seg[-1] - t_seg[0])
    if duration <= 0.0:
        return float('nan')
    return float(np.trapezoid(values, t_seg) / duration)


def compute_quartic_dominance(t: np.ndarray, Phi: np.ndarray, psi: np.ndarray,
                              psi_dot: np.ndarray, params: PTUMParameters) -> np.ndarray:
    """Compute <V4>/<|V2|> on each half-cycle using the instantaneous m_eff(Φ)."""
    Q = np.full_like(t, np.nan, dtype=float)
    turning_points = _turning_point_intervals(psi_dot)
    for start, end in zip(turning_points[:-1], turning_points[1:]):
        if end - start < 2:
            continue
        phi_seg, psi_seg = Phi[start:end], psi[start:end]
        mass_sq = np.abs(np.array([meff_sq_psi(x, params) for x in phi_seg]))
        v4_avg = _time_average(t[start:end], 0.25 * params.lambda_psi * psi_seg**4)
        v2_avg = _time_average(t[start:end], 0.5 * mass_sq * psi_seg**2)
        Q[start:end] = v4_avg / v2_avg if v2_avg > 0 else np.inf
    return Q


def compute_quartic_virial_ratio(t: np.ndarray, psi: np.ndarray, psi_dot: np.ndarray,
                                 params: PTUMParameters) -> np.ndarray:
    """Return <ψ̇²>/(4<V4>) per half-cycle; this tends to one for a quartic oscillator."""
    ratio = np.full_like(t, np.nan, dtype=float)
    turning_points = _turning_point_intervals(psi_dot)
    for start, end in zip(turning_points[:-1], turning_points[1:]):
        if end - start < 2:
            continue
        v4_avg = _time_average(t[start:end], 0.25 * params.lambda_psi * psi[start:end]**4)
        kinetic_numerator = _time_average(t[start:end], psi_dot[start:end]**2)
        ratio[start:end] = kinetic_numerator / (4.0 * v4_avg) if v4_avg > 0 else np.nan
    return ratio


def compute_full_cycle_diagnostics(t: np.ndarray, Phi: np.ndarray, psi: np.ndarray,
                                   psi_dot: np.ndarray, rho: np.ndarray, p: np.ndarray,
                                   H: np.ndarray, params: PTUMParameters) -> List[Dict]:
    """Compute w, Q4, virial and omega/H as integral ratios per complete period."""
    turning = _turning_point_intervals(psi_dot)
    cycles = []
    for i in range(0, len(turning) - 2, 2):
        start, end = int(turning[i]), int(turning[i + 2])
        if end - start < 3:
            continue
        sl = slice(start, end + 1)
        ts = t[sl]
        period = float(ts[-1] - ts[0])
        if period <= 0.0:
            continue
        m2 = np.abs(np.array([meff_sq_psi(x, params) for x in Phi[sl]]))
        v2 = float(np.trapezoid(0.5 * m2 * psi[sl]**2, ts))
        v4 = float(np.trapezoid(0.25 * params.lambda_psi * psi[sl]**4, ts))
        kinetic = float(np.trapezoid(psi_dot[sl]**2, ts))
        rint, pint = float(np.trapezoid(rho[sl], ts)), float(np.trapezoid(p[sl], ts))
        rabs = float(np.trapezoid(np.abs(rho[sl]), ts))
        if not np.isfinite(rint) or abs(rint) <= 32*np.finfo(float).eps*rabs:
            continue
        havg = float(np.trapezoid(H[sl], ts) / period)
        cycles.append({'t_mid': 0.5*(ts[0]+ts[-1]), 'period': period,
                       'w': pint/rint, 'Q4': v4/v2 if v2 > 0 else float('inf'),
                       'virial': kinetic/(4*v4) if v4 > 0 else float('nan'),
                       'omega_over_H': (2*np.pi/period)/havg if havg > 0 else float('inf')})
    return cycles


def compute_time_averaged_w(t: np.ndarray, rho: np.ndarray, p: np.ndarray,
                            psi_dot: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute cycle-averaged equation of state as integral(p dt)/integral(rho dt)."""
    turning_points = _turning_point_intervals(psi_dot)
    if len(turning_points) < 3:
        return np.array([]), np.array([])

    w_avg, t_avg = [], []
    # A full oscillation runs from one turning point to the next same-side
    # turning point, i.e. across two consecutive half-cycles.
    for i in range(0, len(turning_points) - 2, 2):
        start, end = int(turning_points[i]), int(turning_points[i + 2])
        if end - start < 3:
            continue
        rho_int = float(np.trapezoid(rho[start:end + 1], t[start:end + 1]))
        p_int = float(np.trapezoid(p[start:end + 1], t[start:end + 1]))
        scale = float(np.trapezoid(np.abs(rho[start:end + 1]), t[start:end + 1]))
        if not np.isfinite(rho_int) or abs(rho_int) <= np.finfo(float).eps * scale:
            continue
        w_avg.append(p_int / rho_int)
        t_avg.append(0.5 * (t[start] + t[end]))
    return np.asarray(w_avg, dtype=float), np.asarray(t_avg, dtype=float)


def create_initial_conditions(params: PTUMParameters,
                              psi_init: float = 0.0,
                              psi_dot_init: float = 0.0,
                              phi_offset: float = 0.0,
                              phi_dot_init: Optional[float] = None) -> InitialConditions:
    """
    Create initial conditions at threshold crossing.
    
    Args:
        params: PTUM parameters
        psi_init: Initial ψ(t_c) [default 0 = top of barrier]
        psi_dot_init: Initial ψ̇(t_c) [default 0]
        phi_offset: Offset from Φ_c (positive = already past threshold)
    
    Returns:
        InitialConditions object
    """
    Phi_c = params.Phi_c
    Phi = Phi_c + phi_offset
    
    # Slow-roll Φ̇ at threshold: Φ̇ ≈ -√(2ε_V) H M_Pl
    # ε_V = ½(V'/V)²
    V = veff_phi(Phi, params)
    V_prime = dveff_dphi(Phi, params)
    epsilon_V = 0.5 * (V_prime / V)**2 if V > 0 else 0.01
    H = params.H_star
    slow_roll_phi_dot = -np.sqrt(2 * epsilon_V) * H * M_PL
    Phi_dot = slow_roll_phi_dot if phi_dot_init is None else float(phi_dot_init)
    
    return InitialConditions(
        Phi=Phi,
        Phi_dot=Phi_dot,
        psi=psi_init,
        psi_dot=psi_dot_init
    )


def create_initial_conditions_underdamped(params: PTUMParameters,
                                           psi_init: float = 0.0,
                                           psi_dot_init: float = 0.0,
                                           phi_ratio: float = 1.01,
                                           phi_dot_init: Optional[float] = None) -> InitialConditions:
    """
    Create initial conditions for underdamped regime (Phi > Phi_c).
    
    Args:
        params: PTUM parameters
        psi_init: Initial ψ [default 0 = top of barrier]
        psi_dot_init: Initial ψ̇ [default 0]
        phi_ratio: Φ/Φ_c ratio [default 1.01 = just past threshold]
    
    Returns:
        InitialConditions object
    """
    Phi = phi_ratio * params.Phi_c
    
    # Slow-roll Φ̇
    V = veff_phi(Phi, params)
    V_prime = dveff_dphi(Phi, params)
    epsilon_V = 0.5 * (V_prime / V)**2 if V > 0 else 0.01
    H = params.H_star
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
                       phi_dot_init: Optional[float] = None) -> List[Dict]:
    """
    Run parameter scan over initial conditions.
    
    Returns list of simulation results with success/failure classification.
    """
    results = []
    
    # Time array (in units of 1/μ)
    mu = np.sqrt(abs(params.mu_sq))
    t_span = (0, t_max / mu)
    t_eval = np.linspace(0, t_max / mu, n_points)
    
    for psi_init in psi_init_range:
        for psi_dot_init in psi_dot_init_range:
            for phi_offset in phi_offset_range:
                ic = create_initial_conditions(params, psi_init, psi_dot_init, phi_offset,
                                               phi_dot_init=phi_dot_init)
                
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
                    
                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'ic_params': {
                            'psi_init': psi_init,
                            'psi_dot_init': psi_dot_init,
                            'phi_offset': phi_offset
                        }
                    })
    
    return results


def classify_outcome(result: Dict, params: PTUMParameters) -> Dict:
    """Classify the trajectory using full-period integral diagnostics."""
    if not result['success']:
        return {'regime': 'failed', 'quartic_achieved': False}
    if result.get('seedless_invariant', False):
        return {'regime': 'unseeded_invariant', 'quartic_achieved': False,
                'w_final': 0.0, 'Q_final': 0.0, 'virial_final': float('nan'),
                'omega_over_H_final': float('nan'), 'n_oscillations': 0,
                'n_full_cycles': 0}
    cycles = compute_full_cycle_diagnostics(
        result['t'], result['Phi'], result['psi'], result['psi_dot'],
        result['rho_psi_exc'], result['p_psi_exc'], result['H'], params)
    last = cycles[-3:]
    if last:
        wv = np.asarray([c['w'] for c in last])
        qv = np.asarray([c['Q4'] for c in last])
        vv = np.asarray([c['virial'] for c in last])
        ov = np.asarray([c['omega_over_H'] for c in last])
        wf, qf, vf, of = map(float, (np.mean(wv), np.mean(qv), np.mean(vv), np.mean(ov)))
    else:
        wv = qv = vv = ov = np.asarray([], dtype=float)
        wf, qf, vf, of = 0.0, 0.0, float('nan'), float('nan')
    quartic = (len(last) == 3 and np.all(np.abs(wv-1/3) < 0.05)
               and np.all(qv > 5.0) and np.all(np.abs(vv-1.0) < 0.2)
               and np.all(ov > 10.0))
    if quartic:
        regime = 'quartic'
    elif len(cycles) and abs(wf) < 0.1 and qf < 1.0:
        regime = 'quadratic'
    elif len(cycles) and wf > 0.5:
        regime = 'barrier_crossing'
    else:
        regime = 'transitional'
    return {'regime': regime, 'quartic_achieved': bool(quartic),
            'w_final': wf, 'Q_final': qf, 'virial_final': vf,
            'omega_over_H_final': of, 'n_oscillations': len(cycles),
            'n_full_cycles': len(cycles), 'cycle_diagnostics': cycles}


def save_results(results: List[Dict], filepath: str):
    """Save simulation results to JSON (excluding large arrays)."""
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
                'ic_params': r['ic_params'],
                'final_psi_amplitude': float(np.max(np.abs(r['psi']))),
                'final_Phi': float(r['Phi'][-1]),
                'max_relative_continuity_residual': float(r['max_relative_continuity_residual']),
                'max_relative_split_continuity_residual': float(r['max_relative_split_continuity_residual']),
                'min_meff_sq': float(r['min_meff_sq']),
                'tachyonic_duration': float(r['tachyonic_duration']),
                'tachyonic_fraction': float(r['tachyonic_fraction']),
                'threshold_crossings': r['threshold_crossings'],
                'initially_tachyonic': bool(r['initially_tachyonic']),
                'finally_tachyonic': bool(r['finally_tachyonic']),
                'seedless_invariant': bool(r['seedless_invariant']),
                'max_abs_psi': float(r['max_abs_psi']),
                'max_abs_Phi_over_Phi_c': float(r['max_abs_Phi_over_Phi_c'])
            })
        else:
            summary.append({
                'success': False,
                'error': r.get('error', 'Unknown'),
                'ic_params': r['ic_params']
            })
    
    def json_safe(value):
        if isinstance(value, np.ndarray):
            return [json_safe(x) for x in value.tolist()]
        if isinstance(value, np.generic):
            return json_safe(value.item())
        if isinstance(value, float) and not np.isfinite(value):
            return None
        if isinstance(value, dict):
            return {str(k): json_safe(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [json_safe(v) for v in value]
        return value

    summary = json_safe(summary)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, allow_nan=False)


# ============================================================
# Main execution for testing
# ============================================================

def run_baseline_tests():
    """Run baseline simulation tests with paper parameters."""
    print("=" * 60)
    print("PTUM Task 1: Tachyonic-to-Quartic Transition Simulation")
    print("=" * 60)
    
    # Paper benchmark parameters - UNDAMPED regime (V0=1e56)
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
    print(f"  3H/(2mu) = {params.damping_ratio:.3f}")
    
    # Time span: ~100 oscillations
    mu = params.mu
    t_span = (0, 200 / mu)
    t_eval = np.linspace(t_span[0], t_span[1], 20000)
    
    # Test 1: Baseline - field at top of barrier with small quantum kick, Phi = 1.01 Phi_c
    print("\n" + "=" * 60)
    print("Test 1: Baseline (psi=0.01*psi_0, psi_dot=0, Phi=1.01 Phi_c)")
    print("=" * 60)
    
    ic1 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=0.0, phi_ratio=1.01)
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
    ic2 = create_initial_conditions_underdamped(params, psi_init=0.01*params.psi_0, psi_dot_init=psi_dot_init, phi_ratio=1.01)
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