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
