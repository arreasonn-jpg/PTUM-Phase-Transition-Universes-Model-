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

Energy densities (interaction potential assigned once, to ψ):
  ρ_Φ = ½Φ̇² + V_eff(Φ)
  ρ_ψ = ½ψ̇² + ½m_eff²(Φ)ψ² + ¼λ_ψψ⁴
  ρ_total = ρ_Φ + ρ_ψ

Pressures:
  p_Φ = ½Φ̇² - V_eff(Φ)
  p_ψ = ½ψ̇² - ½m_eff²(Φ)ψ² - ¼λ_ψψ⁴

Diagnostics:
  Q = λ_ψ⟨ψ⁴⟩ / ⟨|m_eff²(Φ)|ψ²⟩, evaluated per half-cycle
  R_vir = ⟨K⟩ / (2⟨V_4⟩), which tends to 1 for quartic oscillations
  C_FRW = dρ_total/dt + 3H(ρ_total+p_total)
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


def shifted_potential_psi(psi: float, params: PTUMParameters) -> float:
    """U(ψ) = ¼λ_ψ(ψ² - ψ₀²)² - energy measured from minimum"""
    psi_0 = params.psi_0
    return 0.25 * params.lambda_psi * (psi**2 - psi_0**2)**2


def w_psi(Phi: float, psi: float, psi_dot: float, params: PTUMParameters) -> float:
    """Equation of state parameter w_ψ = p_ψ/ρ_ψ"""
    p = pressure_psi(Phi, psi, psi_dot, params)
    rho = rho_psi(Phi, psi, psi_dot, params)
    return p / rho if rho != 0 else 0.0


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
    p_phi_arr = np.array([pressure_phi(Phi[i], Phi_dot[i], params) for i in range(len(t))])
    p_psi_arr = np.array([pressure_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    rho_total_arr = rho_phi_arr + rho_psi_arr
    p_total_arr = p_phi_arr + p_psi_arr
    # Evaluate d(rho)/dt by the chain rule using the same RHS that evolves
    # the fields. This avoids differencing a nearly constant, ~1e50 GeV^4
    # vacuum density and dividing round-off noise by an almost-zero scale.
    # It is an equation-consistency diagnostic, not an independent solver test.
    coupling = params.alpha * params.m_psi**2 / params.E_th**2
    m_eff_sq_arr = np.array([meff_sq_psi(x, params) for x in Phi])
    dV_dPhi_arr = np.array([dveff_dphi(x, params) for x in Phi])
    Phi_ddot_arr = -3.0 * H * Phi_dot - dV_dPhi_arr + coupling * Phi * psi**2
    psi_ddot_arr = -3.0 * H * psi_dot - m_eff_sq_arr * psi - params.lambda_psi * psi**3
    dm_eff_sq_dPhi_arr = -2.0 * coupling * Phi
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
    w_psi_arr = np.array([w_psi(Phi[i], psi[i], psi_dot[i], params) for i in range(len(t))])
    
    # Quartic diagnostics are evaluated over complete half-cycles.
    # NaN denotes that no valid oscillation interval was available.
    U_psi = 0.25 * params.lambda_psi * psi**4
    virial_ratio = compute_quartic_virial_ratio(t, psi, psi_dot, params)
    Q_arr = compute_quartic_dominance(t, psi, psi_dot, params, Phi)
    
    # Time-averaged w_psi over oscillation periods
    w_avg, t_avg = compute_time_averaged_w(t, w_psi_arr, psi_dot)
    
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
        'continuity_residual': continuity_residual,
        'continuity_residual_relative': continuity_residual_relative,
        'continuity_residual_finite_difference': continuity_residual_finite_difference,
        'continuity_residual_finite_difference_relative': continuity_residual_finite_difference_relative,
        'w_psi': w_psi_arr,
        'w_psi_avg': w_avg,
        't_avg': t_avg,
        'U_psi': U_psi,
        'virial_ratio': virial_ratio,
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


def compute_time_averaged_w(t: np.ndarray, w: np.ndarray, 
                            psi_dot: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute time-averaged w_ψ over oscillation periods."""
    zero_crossings = np.where(np.diff(np.sign(psi_dot)))[0]
    
    if len(zero_crossings) < 2:
        return np.array([]), np.array([])
    
    w_avg = []
    t_avg = []
    
    for i in range(len(zero_crossings) - 1):
        start = zero_crossings[i]
        end = zero_crossings[i + 1]
        if end - start < 2:
            continue
        w_avg.append(np.mean(w[start:end]))
        t_avg.append(0.5 * (t[start] + t[end]))
    
    return np.array(w_avg), np.array(t_avg)


def create_initial_conditions(params: PTUMParameters,
                              psi_init: float = 0.0,
                              psi_dot_init: float = 0.0,
                              phi_offset: float = 0.0) -> InitialConditions:
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
    Phi_dot = -np.sqrt(2 * epsilon_V) * H * M_PL
    
    return InitialConditions(
        Phi=Phi,
        Phi_dot=Phi_dot,
        psi=psi_init,
        psi_dot=psi_dot_init
    )


def create_initial_conditions_underdamped(params: PTUMParameters,
                                           psi_init: float = 0.0,
                                           psi_dot_init: float = 0.0,
                                           phi_ratio: float = 1.01) -> InitialConditions:
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
                       n_points: int = 500) -> List[Dict]:
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
                ic = create_initial_conditions(params, psi_init, psi_dot_init, phi_offset)
                
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
    """
    Classify simulation outcome based on diagnostics.
    
    Returns classification dict with:
    - regime: 'quartic', 'quadratic', 'tachyonic', 'barrier_crossing', 'failed'
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
    
    # Use last few oscillation averages
    n_tail = max(10, len(w_avg) * 10)
    q_tail = Q[-n_tail:] if len(Q) else np.array([])
    v_tail = virial[-n_tail:] if len(virial) else np.array([])
    q_valid = q_tail[np.isfinite(q_tail)]
    v_valid = v_tail[np.isfinite(v_tail)]
    w_final = float(np.mean(w_avg[-3:])) if len(w_avg) >= 3 else (
        float(w_avg[-1]) if len(w_avg) else float("nan"))
    Q_final = float(np.mean(q_valid)) if len(q_valid) else float("nan")
    virial_final = float(np.mean(v_valid)) if len(v_valid) else float("nan")

    # Do not classify a regime when the required diagnostics are unavailable.
    diagnostics_valid = np.isfinite([w_final, Q_final, virial_final]).all()
    quartic_achieved = (diagnostics_valid and Q_final > 5 and
                        abs(w_final - 1/3) < 0.05 and
                        abs(virial_final - 1) < 0.2)
    
    if not diagnostics_valid:
        regime = 'insufficient_oscillation_data'
    elif quartic_achieved:
        regime = 'quartic'
    elif abs(w_final) < 0.1 and Q_final < 1:
        regime = 'quadratic'
    elif w_final > 0.5:
        regime = 'barrier_crossing'
    else:
        regime = 'transitional'
    
    return {
        'regime': regime,
        'quartic_achieved': quartic_achieved,
        'w_final': float(w_final),
        'Q_final': float(Q_final),
        'virial_final': float(virial_final),
        'n_oscillations': len(w_avg)
    }


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
                'max_abs_relative_frw_continuity_residual': float(np.nanmax(
                    np.abs(r['continuity_residual_relative'])
                ))
            })
        else:
            summary.append({
                'success': False,
                'error': r.get('error', 'Unknown'),
                'ic_params': r['ic_params']
            })
    
    with open(filepath, 'w') as f:
        json.dump(summary, f, indent=2)


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