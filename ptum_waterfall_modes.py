#!/usr/bin/env python3
"""Linear tachyonic waterfall modes on the exact single-field FRW background.

The homogeneous psi=0 trajectory is an exact classical invariant solution.
This module initializes linear psi_k fluctuations in an adiabatic vacuum
before threshold crossing and evolves them through m_eff^2(Phi)<0. It does
not include nonlinear backreaction, rescattering or fragmentation.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp

from ptum_floquet import integrate_expanding_mode, integrate_expanding_spectrum
from ptum_inflation_background import state_at_field_value
from ptum_task1_simulation import (
    M_PL,
    PTUMParameters,
    dveff_dphi,
    meff_sq_psi,
    veff_phi,
)


def build_waterfall_background(
    params: PTUMParameters,
    *,
    start_fraction: float = 0.05,
    t_end_mu: float = 20.0,
    n_points: int = 4001,
    rtol: float = 2.0e-9,
    atol: float = 1.0e-11,
) -> dict[str, object]:
    """Build a psi=0 FRW background spanning the threshold and waterfall.

    Time is measured in tau=mu*t, Hubble rates in H/mu, and masses squared
    in mu^2. The initial fuel-field position is (1+start_fraction)*Phi_c,
    with Phi_dot taken from the integrated single-field inflationary
    trajectory. The psi=0 homogeneous solution is kept exact; its linear
    perturbations are evolved separately.
    """
    scalars = np.asarray([start_fraction, t_end_mu, rtol, atol], dtype=float)
    if not np.all(np.isfinite(scalars)) or start_fraction <= 0.0:
        raise ValueError("start_fraction, t_end_mu and tolerances must be finite")
    if t_end_mu <= 0.0 or n_points < 32 or rtol <= 0.0 or atol <= 0.0:
        raise ValueError("require t_end_mu>0, n_points>=32 and positive tolerances")
    mu = float(params.mu)
    if not np.isfinite(mu) or mu <= 0.0:
        raise ValueError("the waterfall reference scale mu must be positive")

    x_c = params.Phi_c / M_PL
    x_initial = x_c * (1.0 + start_fraction)
    state = state_at_field_value(
        params.lambda_phi, x_initial, V0=params.V0
    )
    y_initial = np.asarray([
        x_initial,
        state["Phi_dot"] / (M_PL * mu),
        0.0,
    ], dtype=float)

    def rhs(tau: float, y: np.ndarray) -> np.ndarray:
        x, x_prime, _log_a = y
        phi = x * M_PL
        phi_dot = x_prime * M_PL * mu
        rho = 0.5 * phi_dot**2 + veff_phi(phi, params)
        if not np.isfinite(rho) or rho <= 0.0:
            raise ValueError("single-field background reached non-positive density")
        h_over_mu = np.sqrt(rho / (3.0 * M_PL**2)) / mu
        x_second = (
            -3.0 * h_over_mu * x_prime
            - dveff_dphi(phi, params) / (M_PL * mu**2)
        )
        return np.asarray([x_prime, x_second, h_over_mu], dtype=float)

    tau = np.linspace(0.0, t_end_mu, n_points)
    solution = solve_ivp(
        rhs,
        (0.0, t_end_mu),
        y_initial,
        t_eval=tau,
        method="DOP853",
        rtol=rtol,
        atol=atol,
    )
    if not solution.success or len(solution.t) != n_points:
        raise RuntimeError(f"waterfall background integration failed: {solution.message}")

    x = solution.y[0]
    x_prime = solution.y[1]
    log_a = solution.y[2]
    phi = x * M_PL
    phi_dot = x_prime * M_PL * mu
    scale_factor = np.exp(log_a)
    rho = 0.5 * phi_dot**2 + np.asarray([veff_phi(value, params) for value in phi])
    hubble_over_mu = np.sqrt(rho / (3.0 * M_PL**2)) / mu
    effective_mass_sq = np.asarray([
        meff_sq_psi(value, params) / mu**2 for value in phi
    ])

    threshold_offset = phi - params.Phi_c
    crossings = []
    for i in range(len(tau) - 1):
        if threshold_offset[i] >= 0.0 and threshold_offset[i + 1] < 0.0:
            fraction = threshold_offset[i] / (
                threshold_offset[i] - threshold_offset[i + 1]
            )
            crossings.append(float(tau[i] + fraction * (tau[i + 1] - tau[i])))

    if not crossings:
        raise RuntimeError(
            "fuel field did not cross Phi_c during the requested background interval"
        )
    if effective_mass_sq[0] <= 0.0:
        raise RuntimeError("initial waterfall mass is not in the stable phase")

    return {
        "tau": tau,
        "scale_factor": scale_factor,
        "hubble_over_mu": hubble_over_mu,
        "Phi_over_Mpl": x,
        "Phi_dot_over_Mpl_mu": x_prime,
        "effective_mass_sq_over_mu2": effective_mass_sq,
        "threshold_crossing_tau": crossings[0],
        "all_threshold_crossings_tau": crossings,
        "mu_GeV": mu,
        "initial_state": state,
        "psi_homogeneous_exact_zero": True,
        "adiabatic_vacuum_initialized": False,
        "backreaction_included": False,
    }


def integrate_waterfall_mode(
    background: dict[str, object],
    *,
    k_over_mu: float,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
    max_initial_adiabaticity: float = 0.1,
    wronskian_tolerance: float = 1.0e-7,
) -> dict[str, object]:
    """Evolve one linear psi_k mode, allowing a tachyonic mass interval."""
    tau = np.asarray(background["tau"], dtype=float)
    scale_factor = np.asarray(background["scale_factor"], dtype=float)
    hubble = np.asarray(background["hubble_over_mu"], dtype=float)
    mass_sq = np.asarray(background["effective_mass_sq_over_mu2"], dtype=float)
    result = integrate_expanding_mode(
        tau,
        scale_factor,
        hubble,
        np.zeros_like(tau),
        k_comoving=float(k_over_mu),
        m_chi=0.0,
        g_dm=0.0,
        rtol=rtol,
        atol=atol,
        max_initial_adiabaticity=max_initial_adiabaticity,
        effective_mass_sq=mass_sq,
        wronskian_tolerance=wronskian_tolerance,
    )
    result["psi_k"] = result["chi"]
    result["psi_k_dot"] = result["chi_dot"]
    result["k_over_mu"] = float(k_over_mu)
    result["tachyonic_mass_interval"] = bool(np.any(mass_sq < 0.0))
    result["initial_adiabatic_vacuum"] = True
    return result


def integrate_waterfall_spectrum(
    background: dict[str, object],
    k_over_mu_values: Iterable[float],
    *,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
    max_initial_adiabaticity: float = 0.1,
    wronskian_tolerance: float = 1.0e-7,
) -> dict[str, object]:
    """Integrate a finite dimensionless momentum band of linear waterfall modes."""
    tau = np.asarray(background["tau"], dtype=float)
    scale_factor = np.asarray(background["scale_factor"], dtype=float)
    hubble = np.asarray(background["hubble_over_mu"], dtype=float)
    mass_sq = np.asarray(background["effective_mass_sq_over_mu2"], dtype=float)
    result = integrate_expanding_spectrum(
        k_over_mu_values,
        tau,
        scale_factor,
        hubble,
        np.zeros_like(tau),
        m_chi=0.0,
        g_dm=0.0,
        rtol=rtol,
        atol=atol,
        max_initial_adiabaticity=max_initial_adiabaticity,
        effective_mass_sq=mass_sq,
        wronskian_tolerance=wronskian_tolerance,
    )
    result["k_over_mu"] = result["k_comoving"]
    result["tachyonic_mass_interval"] = bool(np.any(mass_sq < 0.0))
    result["finite_band_only"] = True
    result["momentum_unit"] = "mu"
    result["number_density_unit"] = "mu^3"
    return result
