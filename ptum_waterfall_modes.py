"""Linear quantum waterfall-mode evolution on a supplied FRW background.

The canonical mode is represented by its Ermakov-Pinney amplitude and phase.
This preserves the vacuum Wronskian even when one solution grows tachyonically.
The calculation is linear on a prescribed background: it excludes mode
backreaction, rescattering and a renormalized stress-energy integral.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


def integrate_waterfall_mode(
    t, a, H, Phi, k_comoving: float, m_psi: float, Phi_c: float, *,
    lambda_psi: float = 0.0, psi_background=None, H_dot=None,
    adiabaticity_max: float = 0.1, rtol: float = 1.0e-9, atol: float = 1.0e-12,
) -> dict:
    """Evolve one canonical mode v_k=a^(3/2) delta_psi_k.

    All inputs use mutually consistent units. The initial state is the
    leading adiabatic vacuum and is rejected unless its WKB parameter is
    below adiabaticity_max. The amplitude R and phase theta obey the
    Ermakov-Pinney representation:
      Rddot + Omega^2 R = 1/(4 R^3),  thetadot = -1/(2 R^2).
    This representation preserves the canonical Wronskian by construction.
    """
    t = np.asarray(t, dtype=float)
    a = np.asarray(a, dtype=float)
    H = np.asarray(H, dtype=float)
    Phi = np.asarray(Phi, dtype=float)
    if t.ndim != 1 or len(t) < 5:
        raise ValueError("t must be one-dimensional with at least five samples")
    if any(x.shape != t.shape for x in (a, H, Phi)):
        raise ValueError("a, H and Phi must match the t grid")
    if not all(np.all(np.isfinite(x)) for x in (t, a, H, Phi)):
        raise ValueError("background arrays must be finite")
    if np.any(np.diff(t) <= 0.0) or np.any(a <= 0.0):
        raise ValueError("t must increase strictly and a must remain positive")
    if k_comoving < 0.0 or m_psi <= 0.0 or Phi_c <= 0.0 or lambda_psi < 0.0:
        raise ValueError("mode parameters are outside their physical domain")
    if adiabaticity_max <= 0.0 or rtol <= 0.0 or atol <= 0.0:
        raise ValueError("adiabaticity_max, rtol and atol must be positive")

    if H_dot is None:
        H_dot = np.gradient(H, t, edge_order=2)
    else:
        H_dot = np.asarray(H_dot, dtype=float)
        if H_dot.shape != t.shape or not np.all(np.isfinite(H_dot)):
            raise ValueError("H_dot must be finite and match the t grid")
    if psi_background is None:
        psi_background = np.zeros_like(t)
    else:
        psi_background = np.asarray(psi_background, dtype=float)
        if psi_background.shape != t.shape or not np.all(np.isfinite(psi_background)):
            raise ValueError("psi_background must be finite and match the t grid")

    m_eff_sq = m_psi**2 * ((Phi / Phi_c)**2 - 1.0)
    omega_sq = (
        (k_comoving / a)**2 + m_eff_sq + 3.0 * lambda_psi * psi_background**2
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

    s0 = float(-0.5 * np.log(2.0 * omega0))
    sdot0 = float(-omega_sq_dot[0] / (4.0 * omega0**2))

    def rhs(time, state):
        s, s_dot, _theta = state
        omega2 = float(np.interp(time, t, omega_sq))
        exp_m2s = np.exp(-2.0 * s)
        exp_m4s = exp_m2s * exp_m2s
        return np.array([
            s_dot,
            -s_dot**2 - omega2 + 0.25 * exp_m4s,
            -0.5 * exp_m2s,
        ])

    sol = solve_ivp(
        rhs, (float(t[0]), float(t[-1])), np.array([s0, sdot0, 0.0]),
        method="DOP853", t_eval=t, rtol=rtol, atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"Waterfall mode integration failed: {sol.message}")
    s, s_dot, theta = sol.y
    if not np.all(np.isfinite(sol.y)):
        raise RuntimeError("Waterfall mode amplitude/phase became non-finite")

    theta_dot = -0.5 * np.exp(-2.0 * s)
    log_amplification = float(2.0 * (s[-1] - s[0]))
    amplification = float(np.exp(log_amplification)) if log_amplification < 700.0 else float("inf")
    if np.max(s) < 350.0:
        amplitude = np.exp(s)
        mode = amplitude * np.exp(1j * theta)
        mode_dot = (s_dot + 1j * theta_dot) * mode
    else:
        mode = None
        mode_dot = None

    # W = v vdot* - v* vdot = i, evaluated from the amplitude-phase form.
    wronskian_norm = np.ones_like(s)
    finite = s < 300.0
    wronskian_norm[finite] = 2.0 * np.exp(2.0 * s[finite]) * (-theta_dot[finite])
    wronskian_error = float(np.max(np.abs(wronskian_norm - 1.0)))
    tachyonic_fraction = float(
        np.sum(np.diff(t) * (0.5 * (omega_sq[:-1] + omega_sq[1:]) < 0.0))
        / (t[-1] - t[0])
    )

    if omega_sq[-1] > 0.0:
        omega_final = float(np.sqrt(omega_sq[-1]))
        final_adiabaticity = float(abs(omega_sq_dot[-1]) / (2.0 * omega_final**3))
        if final_adiabaticity <= adiabaticity_max and s[-1] < 300.0:
            R = float(np.exp(s[-1]))
            R_dot = float(s_dot[-1] * R)
            n_final = float(
                (R_dot**2 + 1.0 / (4.0 * R**2) + omega_sq[-1] * R**2)
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
        "t": t, "omega_sq": omega_sq, "log_amplitude": s, "phase": theta,
        "mode": mode, "mode_dot": mode_dot,
        "initial_adiabaticity": initial_adiabaticity,
        "final_adiabaticity": final_adiabaticity,
        "wronskian_error": wronskian_error,
        "log_amplification": log_amplification, "amplification": amplification,
        "tachyonic_time_fraction": tachyonic_fraction,
        "final_particle_number": n_final,
        "particle_number_is_adiabatic": n_final is not None,
    }



def integrate_waterfall_spectrum(
    t, a, H, Phi, k_comoving_values, m_psi: float, Phi_c: float, **kwargs
) -> dict:
    """Integrate a discrete set of independent linear Fourier modes.

    This returns mode-by-mode diagnostics only. It deliberately does not
    integrate a renormalized energy density over momentum or include
    backreaction.
    """
    k_values = np.asarray(k_comoving_values, dtype=float)
    if k_values.ndim != 1 or len(k_values) == 0:
        raise ValueError("k_comoving_values must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(k_values)) or np.any(k_values < 0.0):
        raise ValueError("all comoving wavenumbers must be finite and non-negative")
    if np.any(np.diff(k_values) <= 0.0):
        raise ValueError("comoving wavenumbers must be strictly increasing")

    modes = [
        integrate_waterfall_mode(
            t, a, H, Phi, float(k), m_psi, Phi_c, **kwargs
        )
        for k in k_values
    ]
    return {
        "k_comoving": k_values,
        "modes": modes,
        "log_amplification": np.array(
            [mode["log_amplification"] for mode in modes], dtype=float
        ),
        "tachyonic_time_fraction": np.array(
            [mode["tachyonic_time_fraction"] for mode in modes], dtype=float
        ),
        "final_particle_number": [
            mode["final_particle_number"] for mode in modes
        ],
        "particle_number_is_adiabatic": np.array(
            [mode["particle_number_is_adiabatic"] for mode in modes], dtype=bool
        ),
    }
