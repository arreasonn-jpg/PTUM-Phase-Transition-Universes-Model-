"""Exact free conformal-scalar benchmarks for curved-FRW renormalization.

This module contains analytic controls only. It does not evolve the PTUM
waterfall field, include interactions or backreaction, or implement a
general adiabatic subtraction prescription.
"""
from __future__ import annotations

import numpy as np


def _finite_real_scalar(name: str, value: float) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a finite real scalar")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real scalar") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be a finite real scalar")
    return result


def conformal_massless_vacuum_mode(
    k_comoving: float,
    conformal_time: float,
) -> dict[str, complex | float]:
    """Return the exact positive-frequency mode for a massless xi=1/6 scalar.

    For a spatially flat FLRW metric, v_k=a*varphi_k obeys
    v_k''+k^2 v_k=0. The returned mode is exp(-i*k*eta)/sqrt(2*k),
    normalized so v_k*v_k'^* - v_k'*v_k^* = i.
    """
    k = _finite_real_scalar("k_comoving", k_comoving)
    eta = _finite_real_scalar("conformal_time", conformal_time)
    if k <= 0.0:
        raise ValueError("k_comoving must be positive")
    amplitude = 1.0 / np.sqrt(2.0 * k)
    mode = complex(amplitude * np.exp(-1j * k * eta))
    derivative = complex(-1j * k * mode)
    second_derivative = complex(-(k**2) * mode)
    wronskian = mode * np.conjugate(derivative) - derivative * np.conjugate(mode)
    residual = second_derivative + k**2 * mode
    return {
        "k_comoving": k,
        "conformal_time": eta,
        "mode": mode,
        "mode_derivative": derivative,
        "mode_second_derivative": second_derivative,
        "wronskian": complex(wronskian),
        "mode_equation_residual": complex(residual),
        "occupation_number": 0.0,
        "positive_frequency": True,
    }


def conformal_scalar_radiation_flrw_anomaly_stress(
    hubble_gev: float,
) -> dict[str, object]:
    """Return the conformal-vacuum stress benchmark in radiation FLRW.

    Assumptions:
      * spatially flat radiation background: dot(H)=-2 H^2 and R=0;
      * one free, massless, conformally coupled real scalar;
      * heat-kernel trace anomaly T = (Riemann^2-Ricci^2)/(2880*pi^2);
      * no additional state-dependent a^(-4) radiation term.

    Conservation and the trace identity then fix rho and p. This is an
    analytic free-field benchmark, not a stress tensor for the interacting
    PTUM waterfall or a general FLRW subtraction algorithm.
    """
    h = _finite_real_scalar("hubble_gev", hubble_gev)
    if h < 0.0:
        raise ValueError("hubble_gev must be non-negative")

    h2 = h**2
    h4 = h2**2
    ricci_scalar = 0.0
    riemann_squared = 24.0 * h4
    ricci_tensor_squared = 12.0 * h4
    euler_density = -24.0 * h4
    a2_bulk = (riemann_squared - ricci_tensor_squared) / 180.0
    trace_anomaly = a2_bulk / (16.0 * np.pi**2)

    # Solving dot(rho)+3H(rho+p)=0 and -rho+3p=T with
    # dot(H)=-2H^2 gives rho=T/4 when the a^-4 state term is set to zero.
    rho = trace_anomaly / 4.0
    pressure = (trace_anomaly + rho) / 3.0
    rho_dot = -8.0 * h * rho
    continuity_residual = rho_dot + 3.0 * h * (rho + pressure)
    trace_residual = -rho + 3.0 * pressure - trace_anomaly

    values = np.asarray(
        [
            ricci_scalar,
            riemann_squared,
            ricci_tensor_squared,
            euler_density,
            a2_bulk,
            trace_anomaly,
            rho,
            pressure,
            rho_dot,
            continuity_residual,
            trace_residual,
        ],
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("conformal-scalar anomaly benchmark is non-finite")

    return {
        "background": {
            "geometry": "spatially_flat_radiation_FLRW",
            "H_GeV": h,
            "dot_H_GeV2": -2.0 * h2,
            "Ricci_scalar_GeV2": ricci_scalar,
        },
        "curvature_invariants_GeV4": {
            "Riemann_squared": riemann_squared,
            "Ricci_tensor_squared": ricci_tensor_squared,
            "Euler_density": euler_density,
        },
        "heat_kernel_a2_bulk_GeV4": a2_bulk,
        "trace_anomaly_GeV4": trace_anomaly,
        "rho_renormalized_GeV4": rho,
        "pressure_renormalized_GeV4": pressure,
        "rho_time_derivative_GeV5": rho_dot,
        "continuity_residual_GeV5": continuity_residual,
        "trace_identity_residual_GeV4": trace_residual,
        "state_dependent_radiation_constant": 0.0,
        "renormalization": {
            "field": "one_free_real_massless_scalar",
            "curvature_coupling": "xi=1/6",
            "prescription": "four-dimensional_heat-kernel_trace_anomaly",
            "box_R_term": 0.0,
            "finite_R_squared_ambiguity_on_this_background": 0.0,
            "additional_a_minus_4_state_component": False,
            "interactions_included": False,
            "ptum_waterfall_backreaction_included": False,
            "general_FLRW_subtraction_implemented": False,
            "physical_PTUM_prediction": False,
        },
    }
