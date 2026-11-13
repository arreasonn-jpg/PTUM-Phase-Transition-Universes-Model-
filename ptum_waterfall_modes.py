"""Linear quantum waterfall-mode evolution on a supplied FRW background.

This module evolves linear psi fluctuations around a prescribed homogeneous
background. It does not include nonlinear backreaction, rescattering or a
renormalized stress-energy integral, and therefore does not predict a relic
abundance.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


def integrate_waterfall_mode(
    t,
    a,
    H,
    Phi,
    k_comoving: float,
    m_psi: float,
    Phi_c: float,
    *,
    lambda_psi: float = 0.0,
    psi_background=None,
    H_dot=None,
    adiabaticity_max: float = 0.1,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
) -> dict:
    """Evolve one canonical mode v_k=a^(3/2) delta_psi_k.

    Inputs use mutually consistent units: t in inverse-mass units, H,
    k_comoving and m_psi in mass units, and Phi/Phi_c in the same field units.
    The initial state is the leading adiabatic vacuum and is rejected unless
    its WKB adiabaticity parameter is below adiabaticity_max.
    """
    t = np.asarray(t, dtype=float)
    a = np.asarray(a, dtype=float)
    H = np.asarray(H, dtype=float)
    Phi = np.asarray(Phi, dtype=float)
    if t.ndim != 1 or len(t) < 5:
        raise ValueError("t must be a one-dimensional array with at least five samples")
    if any(x.shape != t.shape for x in (a, H, Phi)):
        raise ValueError("a, H and Phi must have the same shape as t")
    if not all(np.all(np.isfinite(x)) for x in (t, a, H, Phi)):
        raise ValueError("background arrays must be finite")
    if np.any(np.diff(t) <= 0.0) or np.any(a <= 0.0):
        raise ValueError("t must increase strictly and a must remain positive")
    if k_comoving < 0.0 or m_psi <= 0.0 or Phi_c <= 0.0 or lambda_psi < 0.0:
        raise ValueError("k_comoving, m_psi, Phi_c or lambda_psi is outside its domain")
    if adiabaticity_max <= 0.0 or rtol <= 0.0 or atol <= 0.0:
        raise ValueError("adiabaticity_max, rtol and atol must be positive")

    if H_dot is None:
        H_dot = np.gradient(H, t, edge_order=2)
    else:
        H_dot = np.asarray(H_dot, dtype=float)
        if H_dot.shape != t.shape or not np.all(np.isfinite(H_dot)):
            raise ValueError("H_dot must be finite and match the background grid")

    if psi_background is None:
        psi_background = np.zeros_like(t)
    else:
        psi_background = np.asarray(psi_background, dtype=float)
        if psi_background.shape != t.shape or not np.all(np.isfinite(psi_background)):
            raise ValueError("psi_background must be finite and match the background grid")

    m_eff_sq = m_psi**2 * ((Phi / Phi_c)**2 - 1.0)
    physical_k_sq = (k_comoving / a)**2
    omega_sq = (
        physical_k_sq + m_eff_sq + 3.0 * lambda_psi * psi_background**2
        - 1.5 * H_dot - 2.25 * H**2
    )
    omega_sq_dot = np.gradient(omega_sq, t, edge_order=2)
    if omega_sq[0] <= 0.0:
        raise ValueError("Initial canonical frequency squared must be positive")
    omega0 = float(np.sqrt(omega_sq[0]))
    initial_adiabaticity = float(abs(omega_sq_dot[0]) / (2.0 * omega0**3))
    if initial_adiabaticity > adiabaticity_max:
        raise ValueError(
            f"Initial state is not adiabatic: epsilon_WKB={initial_adiabaticity:.3e}"
        )

    v0 = 1.0 / np.sqrt(2.0 * omega0)
    vdot0 = (-1j * omega0 - omega_sq_dot[0] / (4.0 * omega0**2)) * v0

    def rhs(time, state):
        omega2 = float(np.interp(time, t, omega_sq))
        return np.array([state[1], -omega2 * state[0]], dtype=complex)

    sol = solve_ivp(
        rhs, (float(t[0]), float(t[-1])), np.array([v0, vdot0], dtype=complex),
        method="DOP853", t_eval=t, rtol=rtol, atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"Waterfall mode integration failed: {sol.message}")

    v, v_dot = sol.y
    wronskian = v * np.conjugate(v_dot) - np.conjugate(v) * v_dot
    wronskian_error = float(np.max(np.abs(wronskian - 1j)))
    amplification = float(abs(v[-1])**2 / abs(v[0])**2)
    tachyonic_fraction = float(
        np.sum(np.diff(t) * (0.5 * (omega_sq[:-1] + omega_sq[1:]) < 0.0))
        / (t[-1] - t[0])
    )

    if omega_sq[-1] > 0.0:
        omega_final = float(np.sqrt(omega_sq[-1]))
        final_adiabaticity = float(
            abs(omega_sq_dot[-1]) / (2.0 * omega_final**3)
        )
        if final_adiabaticity <= adiabaticity_max:
            n_final = float(
                (abs(v_dot[-1])**2 + omega_sq[-1] * abs(v[-1])**2)
                / (2.0 * omega_final) - 0.5
            )
            if n_final < -1.0e-7:
                raise RuntimeError("Final adiabatic particle number is significantly negative")
            n_final = max(n_final, 0.0)
        else:
            n_final = None
    else:
        final_adiabaticity = float("inf")
        n_final = None

    return {
        "t": t,
        "omega_sq": omega_sq,
        "mode": v,
        "mode_dot": v_dot,
        "initial_adiabaticity": initial_adiabaticity,
        "final_adiabaticity": final_adiabaticity,
        "wronskian_error": wronskian_error,
        "amplification": amplification,
        "tachyonic_time_fraction": tachyonic_fraction,
        "final_particle_number": n_final,
        "particle_number_is_adiabatic": n_final is not None,
    }
