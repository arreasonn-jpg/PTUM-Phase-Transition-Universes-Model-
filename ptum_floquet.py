#!/usr/bin/env python3
"""Frozen-background Floquet diagnostics for the PTUM chi mode.

This module computes the monodromy matrix of the corrected Mathieu
reduction. It is a local/adiabatic diagnostic only: it does not include
backreaction, rescattering, expansion across many oscillations, or a
relic-density calculation.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


def mathieu_parameters(
    *,
    g_dm: float,
    phi_res_amplitude: float,
    omega_res: float,
    k_comoving: float,
    m_chi: float,
    scale_factor: float = 1.0,
    hubble: float = 0.0,
    hubble_dot: float = 0.0,
) -> tuple[float, float]:
    """Return (A_k, q) for X'' + [A_k - 2 q cos(2z)] X = 0.

    The rescaling X=a^(3/2) chi contributes
    -3 Hdot/2 - 9 H^2/4 to the frozen effective frequency squared.
    """
    if omega_res <= 0.0 or scale_factor <= 0.0:
        raise ValueError("omega_res and scale_factor must be positive")
    if phi_res_amplitude < 0.0 or m_chi < 0.0 or k_comoving < 0.0:
        raise ValueError("amplitudes, masses and wavenumbers must be non-negative")

    k_physical_sq = (k_comoving / scale_factor) ** 2
    static_frequency_sq = (
        k_physical_sq
        + m_chi**2
        + g_dm * phi_res_amplitude**2
        - 1.5 * hubble_dot
        - 2.25 * hubble**2
    )
    A_k = static_frequency_sq / omega_res**2
    q = -g_dm * phi_res_amplitude**2 / (2.0 * omega_res**2)
    return float(A_k), float(q)


def monodromy_matrix(
    A_k: float,
    q: float,
    *,
    rtol: float = 1.0e-10,
    atol: float = 1.0e-12,
) -> np.ndarray:
    """Integrate two independent solutions over one Mathieu period pi."""
    def rhs(z: float, state: np.ndarray) -> np.ndarray:
        X, X_prime = state
        return np.array([
            X_prime,
            -(A_k - 2.0 * q * np.cos(2.0 * z)) * X,
        ])

    columns = []
    for initial_state in (
        np.array([1.0, 0.0]),
        np.array([0.0, 1.0]),
    ):
        sol = solve_ivp(
            rhs,
            (0.0, np.pi),
            initial_state,
            method="DOP853",
            rtol=rtol,
            atol=atol,
        )
        if not sol.success:
            raise RuntimeError(f"Monodromy integration failed: {sol.message}")
        columns.append(sol.y[:, -1])

    return np.column_stack(columns)


def floquet_diagnostic(A_k: float, q: float) -> dict[str, float | bool]:
    """Return the real growth exponent per z and monodromy invariants."""
    matrix = monodromy_matrix(A_k, q)
    discriminant = float(np.trace(matrix))
    determinant = float(np.linalg.det(matrix))
    half_trace = abs(discriminant) / 2.0
    unstable = half_trace > 1.0 + 1.0e-9
    mu_z = (
        float(np.arccosh(half_trace) / np.pi)
        if unstable else 0.0
    )
    return {
        "A_k": float(A_k),
        "q": float(q),
        "trace_monodromy": discriminant,
        "det_monodromy": determinant,
        "unstable": bool(unstable),
        "mu_z": mu_z,
    }


def scan_momentum(
    k_values: Iterable[float],
    *,
    g_dm: float,
    phi_res_amplitude: float,
    omega_res: float,
    m_chi: float,
    scale_factor: float = 1.0,
    hubble: float = 0.0,
    hubble_dot: float = 0.0,
) -> list[dict[str, float | bool]]:
    """Compute frozen-background Floquet diagnostics over k values."""
    results = []
    for k in k_values:
        A_k, q = mathieu_parameters(
            g_dm=g_dm,
            phi_res_amplitude=phi_res_amplitude,
            omega_res=omega_res,
            k_comoving=float(k),
            m_chi=m_chi,
            scale_factor=scale_factor,
            hubble=hubble,
            hubble_dot=hubble_dot,
        )
        row = floquet_diagnostic(A_k, q)
        row["k_comoving"] = float(k)
        row["mu_time"] = float(omega_res * row["mu_z"])
        results.append(row)
    return results



def integrate_expanding_mode(
    t: Iterable[float],
    scale_factor: Iterable[float],
    hubble: Iterable[float],
    phi_res: Iterable[float],
    *,
    k_comoving: float,
    m_chi: float,
    g_dm: float,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
    max_initial_adiabaticity: float = 0.1,
    background_consistency_tolerance: float = 5.0e-2,
) -> dict[str, object]:
    """Evolve one chi_k mode on a supplied expanding-FRW background.

    The physical mode equation is integrated for chi_k:
        chi_ddot + 3 H chi_dot
        + [k^2/a^2 + m_chi^2 + 2 g_dm phi_res(t)^2] chi = 0.

    Initial conditions are imposed on X_k=a^(3/2) chi_k using a
    first-order adiabatic/WKB vacuum. The canonical frequency is
        Omega_k^2 = k^2/a^2 + m_chi^2 + 2 g_dm phi_res^2
                    - 3 Hdot/2 - 9 H^2/4.

    The initial state is rejected if Omega_k^2<=0 or if the WKB
    adiabaticity parameter |Omegadot/Omega^2| exceeds the supplied
    threshold. The final instantaneous occupation number is reported
    only when the final canonical frequency is real and positive.

    This is a linear mode calculation on a prescribed background. It
    does not include mode backreaction, rescattering, nonlinear
    fragmentation, or a self-consistent Friedmann evolution.
    """
    t_arr = np.asarray(tuple(t), dtype=float)
    a_arr = np.asarray(tuple(scale_factor), dtype=float)
    h_arr = np.asarray(tuple(hubble), dtype=float)
    phi_arr = np.asarray(tuple(phi_res), dtype=float)

    arrays = (t_arr, a_arr, h_arr, phi_arr)
    if any(arr.ndim != 1 for arr in arrays):
        raise ValueError("background histories must be one-dimensional")
    if len(t_arr) < 3 or any(len(arr) != len(t_arr) for arr in arrays[1:]):
        raise ValueError("background histories must have equal length >= 3")
    if not all(np.all(np.isfinite(arr)) for arr in arrays):
        raise ValueError("background histories must be finite")
    if np.any(np.diff(t_arr) <= 0.0):
        raise ValueError("time samples must be strictly increasing")
    if np.any(a_arr <= 0.0):
        raise ValueError("scale factor must remain positive")
    scalar_parameters = np.asarray(
        [k_comoving, m_chi, g_dm, rtol, atol, max_initial_adiabaticity,
         background_consistency_tolerance],
        dtype=float,
    )
    if not np.all(np.isfinite(scalar_parameters)):
        raise ValueError("mode parameters and solver tolerances must be finite")
    if k_comoving < 0.0 or m_chi < 0.0:
        raise ValueError("wavenumber and mass must be non-negative")
    if (rtol <= 0.0 or atol <= 0.0 or max_initial_adiabaticity <= 0.0
            or background_consistency_tolerance <= 0.0):
        raise ValueError("solver tolerances and consistency thresholds must be positive")

    a_spline = CubicSpline(t_arr, a_arr, extrapolate=False)
    h_spline = CubicSpline(t_arr, h_arr, extrapolate=False)
    phi_spline = CubicSpline(t_arr, phi_arr, extrapolate=False)
    hubble_from_scale_factor = a_spline.derivative()(t_arr) / a_arr
    hubble_consistency_scale = np.maximum(
        np.maximum(np.abs(hubble_from_scale_factor), np.abs(h_arr)),
        np.finfo(float).tiny,
    )
    hubble_consistency_relative = np.abs(
        hubble_from_scale_factor - h_arr
    ) / hubble_consistency_scale
    max_hubble_consistency_error = float(np.max(hubble_consistency_relative))
    if max_hubble_consistency_error > background_consistency_tolerance:
        raise ValueError(
            "inconsistent background histories: max |a_dot/a-H|/max(|a_dot/a|,|H|)="
            f"{max_hubble_consistency_error:.6g} exceeds "
            f"{background_consistency_tolerance:.6g}"
        )
    h_dot_arr = h_spline.derivative()(t_arr)
    omega_chi_sq = (
        (k_comoving / a_arr) ** 2
        + m_chi**2
        + 2.0 * g_dm * phi_arr**2
    )
    omega_canonical_sq = (
        omega_chi_sq - 1.5 * h_dot_arr - 2.25 * h_arr**2
    )
    if omega_canonical_sq[0] <= 0.0:
        raise ValueError("initial canonical mode frequency is not real and positive")

    omega_arr = np.sqrt(omega_canonical_sq)
    omega_spline = CubicSpline(t_arr, omega_arr, extrapolate=False)
    omega_dot_arr = omega_spline.derivative()(t_arr)
    initial_adiabaticity = float(
        abs(omega_dot_arr[0]) / max(omega_arr[0] ** 2, np.finfo(float).tiny)
    )
    if initial_adiabaticity > max_initial_adiabaticity:
        raise ValueError(
            "initial state is not sufficiently adiabatic: "
            f"|Omega_dot/Omega^2|={initial_adiabaticity:.6g} exceeds "
            f"{max_initial_adiabaticity:.6g}"
        )

    omega0 = omega_arr[0]
    X0 = 1.0 / np.sqrt(2.0 * omega0)
    X_dot0 = (
        -1j * omega0 - 0.5 * omega_dot_arr[0] / omega0
    ) * X0
    chi0 = X0 / a_arr[0] ** 1.5
    chi_dot0 = (
        X_dot0 - 1.5 * h_arr[0] * X0
    ) / a_arr[0] ** 1.5

    def background_at(time: float) -> tuple[float, float, float]:
        return (
            float(a_spline(time)),
            float(h_spline(time)),
            float(phi_spline(time)),
        )

    def rhs(time: float, state: np.ndarray) -> np.ndarray:
        chi, chi_dot = state
        a_now, h_now, phi_now = background_at(time)
        frequency_sq = (
            (k_comoving / a_now) ** 2
            + m_chi**2
            + 2.0 * g_dm * phi_now**2
        )
        return np.array([
            chi_dot,
            -3.0 * h_now * chi_dot - frequency_sq * chi,
        ], dtype=complex)

    solution = solve_ivp(
        rhs,
        (float(t_arr[0]), float(t_arr[-1])),
        np.array([chi0, chi_dot0], dtype=complex),
        t_eval=t_arr,
        method="DOP853",
        rtol=rtol,
        atol=atol,
    )
    if not solution.success:
        raise RuntimeError(f"Expanding mode integration failed: {solution.message}")

    chi = solution.y[0]
    chi_dot = solution.y[1]
    X = a_arr**1.5 * chi
    X_dot = a_arr**1.5 * (chi_dot + 1.5 * h_arr * chi)
    wronskian = X * np.conjugate(X_dot) - np.conjugate(X) * X_dot
    wronskian_relative_error = float(
        abs(wronskian[-1] - 1j) / max(abs(wronskian[0]), np.finfo(float).tiny)
    )

    final_omega_sq = float(omega_canonical_sq[-1])
    if final_omega_sq > 0.0:
        final_omega = float(np.sqrt(final_omega_sq))
        occupation = float(
            (abs(X_dot[-1]) ** 2 + final_omega_sq * abs(X[-1]) ** 2)
            / (2.0 * final_omega)
            - 0.5
        )
        occupation = max(occupation, 0.0) if occupation > -1.0e-10 else occupation
        final_frequency_valid = True
    else:
        final_omega = float("nan")
        occupation = float("nan")
        final_frequency_valid = False

    return {
        "t": t_arr,
        "chi": chi,
        "chi_dot": chi_dot,
        "canonical_mode": X,
        "canonical_mode_dot": X_dot,
        "canonical_frequency_sq": omega_canonical_sq,
        "initial_adiabaticity": initial_adiabaticity,
        "background_hubble_consistency_max_relative": max_hubble_consistency_error,
        "wronskian_relative_error": wronskian_relative_error,
        "final_frequency_valid": final_frequency_valid,
        "final_omega": final_omega,
        "particle_number": occupation,
        "integration_success": bool(solution.success),
    }


def integrate_expanding_spectrum(
    k_values: Iterable[float],
    t: Iterable[float],
    scale_factor: Iterable[float],
    hubble: Iterable[float],
    phi_res: Iterable[float],
    *,
    m_chi: float,
    g_dm: float,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
    max_initial_adiabaticity: float = 0.1,
) -> dict[str, object]:
    """Integrate a finite k-grid and estimate the produced comoving number.

    The supplied k-grid must be strictly increasing and contain at least
    two points. The integral is the finite-band trapezoidal estimate
        n_com = (1 / 2 pi^2) integral dk k^2 n_k.
    The physical number density is n_com/a_final^3.

    This routine does not extrapolate the uncomputed infrared or ultraviolet
    tails. A result is only a finite-grid estimate; momentum-range and
    resolution convergence must be demonstrated before interpreting it as
    a relic abundance.
    """
    k_arr = np.asarray(tuple(k_values), dtype=float)
    if k_arr.ndim != 1 or len(k_arr) < 2:
        raise ValueError("k_values must be one-dimensional with at least two points")
    if not np.all(np.isfinite(k_arr)) or np.any(k_arr < 0.0):
        raise ValueError("k_values must be finite and non-negative")
    if np.any(np.diff(k_arr) <= 0.0):
        raise ValueError("k_values must be strictly increasing")

    t_arr = np.asarray(tuple(t), dtype=float)
    a_arr = np.asarray(tuple(scale_factor), dtype=float)
    h_arr = np.asarray(tuple(hubble), dtype=float)
    phi_arr = np.asarray(tuple(phi_res), dtype=float)
    mode_results = [
        integrate_expanding_mode(
            t_arr,
            a_arr,
            h_arr,
            phi_arr,
            k_comoving=float(k),
            m_chi=m_chi,
            g_dm=g_dm,
            rtol=rtol,
            atol=atol,
            max_initial_adiabaticity=max_initial_adiabaticity,
        )
        for k in k_arr
    ]
    occupations = np.asarray(
        [mode["particle_number"] for mode in mode_results], dtype=float
    )
    all_final_frequencies_valid = all(
        bool(mode["final_frequency_valid"]) for mode in mode_results
    )
    if all_final_frequencies_valid and np.all(np.isfinite(occupations)):
        n_comoving = float(
            np.trapezoid(k_arr**2 * occupations, x=k_arr) / (2.0 * np.pi**2)
        )
        n_physical = float(n_comoving / float(a_arr[-1])**3)
    else:
        n_comoving = float("nan")
        n_physical = float("nan")

    return {
        "k_comoving": k_arr,
        "occupation_numbers": occupations,
        "mode_results": mode_results,
        "n_comoving_finite_band": n_comoving,
        "n_physical_finite_band": n_physical,
        "all_final_frequencies_valid": all_final_frequencies_valid,
        "finite_band_only": True,
        "momentum_range": (float(k_arr[0]), float(k_arr[-1])),
    }
