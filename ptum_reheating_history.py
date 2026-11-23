#!/usr/bin/env python3
"""Conditional continuous perturbative reheating in a two-fluid FRW model.

This module integrates a homogeneous condensate treated as a constant-w fluid
with a constant perturbative width Gamma, plus instantly thermalized radiation.
It is a controlled phenomenological benchmark, not a PTUM-derived decay history:
the Wilson coefficients, time-dependent quasiparticle spectrum, w(t), Gamma(T),
thermal thresholds, and energy partition must be supplied by a separate model.

Natural units are used. Densities are GeV^4, H and Gamma are GeV, and T is GeV.
"""
from __future__ import annotations

import json
from math import isfinite, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp

from ptum_reheating import (
    DEFAULT_BBN_TEMPERATURE_GEV,
    REDUCED_PLANCK_MASS_GEV,
    reheating_temperature_from_width,
)


def _real(name: str, value: object) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite real number")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be a finite real number")
    return result


def _positive(name: str, value: object) -> float:
    result = _real(name, value)
    if result <= 0.0:
        raise ValueError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: object) -> float:
    result = _real(name, value)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return result


def _positive_integer(name: str, value: object, minimum: int = 1) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer >= {minimum}")
    try:
        result = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be an integer >= {minimum}") from exc
    if result != value or result < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return result


def integrate_perturbative_reheating_history(
    initial_condensate_density: float,
    decay_width: float,
    *,
    initial_radiation_density: float = 0.0,
    condensate_equation_of_state: float = 0.0,
    g_star: float = 100.0,
    reduced_planck_mass: float = REDUCED_PLANCK_MASS_GEV,
    minimum_bbn_temperature: float = DEFAULT_BBN_TEMPERATURE_GEV,
    max_efolds: float = 30.0,
    n_output_points: int = 2049,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-12,
    completion_fraction: float = 1.0e-12,
) -> dict[str, object]:
    r"""Integrate the constant-w, constant-width condensate/radiation system.

    With N=ln(a/a_i), the equations are
        d rho_c/dN = -3(1+w_c) rho_c - (Gamma/H) rho_c,
        d rho_r/dN = -4 rho_r + (Gamma/H) rho_c,
        H^2 = (rho_c+rho_r)/(3 Mbar_Pl^2).
    All decay products are assumed to thermalize immediately into a bath with
    constant g_star. The numerical state is normalized to the initial total
    density. Three cumulative integrals independently audit condensate work,
    radiation work, and energy transferred from the condensate.

    The reported temperature at H=Gamma is the continuous-decay bath
    temperature, not the sudden-decay estimate. At that event,
    T_cont/T_sudden = Omega_r^(1/4) for constant g_star.
    """
    rho_c0 = _positive("initial_condensate_density", initial_condensate_density)
    gamma_width = _nonnegative("decay_width", decay_width)
    rho_r0 = _nonnegative("initial_radiation_density", initial_radiation_density)
    w_c = _real("condensate_equation_of_state", condensate_equation_of_state)
    if not (-1.0 / 3.0 <= w_c <= 1.0):
        raise ValueError("condensate_equation_of_state must lie in [-1/3, 1]")
    degrees = _positive("g_star", g_star)
    planck = _positive("reduced_planck_mass", reduced_planck_mass)
    bbn_temperature = _positive("minimum_bbn_temperature", minimum_bbn_temperature)
    n_max = _positive("max_efolds", max_efolds)
    if n_max > 100.0:
        raise ValueError("max_efolds must not exceed 100")
    n_points = _positive_integer("n_output_points", n_output_points, minimum=3)
    rel_tol = _positive("rtol", rtol)
    abs_tol = _positive("atol", atol)
    if rel_tol < 1.0e-12:
        raise ValueError("rtol must be >= 1e-12 to avoid solver tolerance clipping")
    completion = _positive("completion_fraction", completion_fraction)
    if completion >= 1.0:
        raise ValueError("completion_fraction must be below one")

    rho_total0 = rho_c0 + rho_r0
    if not isfinite(rho_total0) or rho_total0 <= 0.0:
        raise ValueError("initial total density must be finite and positive")
    h_initial = sqrt(rho_total0 / (3.0 * planck**2))
    gamma_over_h_initial = gamma_width / h_initial
    if not isfinite(gamma_over_h_initial):
        raise ValueError("decay_width/H_initial must be finite")

    f_c0 = rho_c0 / rho_total0
    f_r0 = rho_r0 / rho_total0

    def rhs(_efolds: float, state: np.ndarray) -> tuple[float, ...]:
        rho_c_bar, rho_r_bar, work_c, work_r, transfer = state
        total_bar = max(float(rho_c_bar + rho_r_bar), np.finfo(float).tiny)
        source = gamma_over_h_initial * float(rho_c_bar) / sqrt(total_bar)
        return (
            -3.0 * (1.0 + w_c) * rho_c_bar - source,
            -4.0 * rho_r_bar + source,
            3.0 * (1.0 + w_c) * rho_c_bar,
            4.0 * rho_r_bar,
            source,
        )

    def radiation_domination_event(_efolds: float, state: np.ndarray) -> float:
        return float(state[1] - state[0])

    radiation_domination_event.direction = 1
    radiation_domination_event.terminal = False

    def h_equals_gamma_event(_efolds: float, state: np.ndarray) -> float:
        total_bar = max(float(state[0] + state[1]), 0.0)
        return sqrt(total_bar) - gamma_over_h_initial

    h_equals_gamma_event.direction = -1
    h_equals_gamma_event.terminal = False

    def condensate_completion_event(_efolds: float, state: np.ndarray) -> float:
        total_bar = max(float(state[0] + state[1]), np.finfo(float).tiny)
        return float(state[0] - completion * total_bar)

    condensate_completion_event.direction = -1
    condensate_completion_event.terminal = True

    events = [radiation_domination_event, h_equals_gamma_event]
    completion_event_added = f_c0 > completion
    if completion_event_added:
        events.append(condensate_completion_event)

    initial_state = np.array([f_c0, f_r0, 0.0, 0.0, 0.0], dtype=float)
    solution = solve_ivp(
        rhs,
        (0.0, n_max),
        initial_state,
        method="BDF",
        dense_output=True,
        events=events,
        rtol=rel_tol,
        atol=abs_tol,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"continuous reheating integration failed: {solution.message}")
    n_final = float(solution.t[-1])
    if not isfinite(n_final) or n_final <= 0.0:
        raise RuntimeError("continuous reheating integration returned an invalid interval")

    efolds = np.linspace(0.0, n_final, n_points)
    sampled = np.asarray(solution.sol(efolds), dtype=float)
    if sampled.shape != (5, n_points) or not np.all(np.isfinite(sampled)):
        raise RuntimeError("continuous reheating solution contains non-finite state values")

    rho_c_bar_raw, rho_r_bar_raw, work_c, work_r, transfer = sampled
    negative_tolerance = max(1.0e-10, 100.0 * abs_tol)
    if min(float(np.min(rho_c_bar_raw)), float(np.min(rho_r_bar_raw))) < -negative_tolerance:
        raise RuntimeError("continuous reheating solution left the non-negative density domain")

    rho_c_bar = np.maximum(rho_c_bar_raw, 0.0)
    rho_r_bar = np.maximum(rho_r_bar_raw, 0.0)
    total_bar = rho_c_bar + rho_r_bar
    if np.any(total_bar <= 0.0):
        raise RuntimeError("continuous reheating solution reached zero total density")

    condensate_budget = rho_c_bar_raw - f_c0 + work_c + transfer
    radiation_budget = rho_r_bar_raw - f_r0 - transfer + work_r
    total_budget = rho_c_bar_raw + rho_r_bar_raw - 1.0 + work_c + work_r
    condensate_budget_max = float(np.max(np.abs(condensate_budget)))
    radiation_budget_max = float(np.max(np.abs(radiation_budget)))
    total_budget_max = float(np.max(np.abs(total_budget)))
    budget_max = max(condensate_budget_max, radiation_budget_max, total_budget_max)

    h_history = h_initial * np.sqrt(total_bar)
    temperature_scale = (30.0 * rho_total0 / (pi**2 * degrees)) ** 0.25
    temperature = temperature_scale * np.power(rho_r_bar, 0.25)
    entropy_density = (2.0 * pi**2 / 45.0) * degrees * temperature**3
    comoving_entropy = np.exp(3.0 * efolds) * entropy_density
    if not (
        np.all(np.isfinite(h_history))
        and np.all(np.isfinite(temperature))
        and np.all(np.isfinite(comoving_entropy))
    ):
        raise RuntimeError("derived reheating temperature/entropy is non-finite")

    entropy_scale = max(float(np.max(comoving_entropy)), 1.0e-300)
    minimum_entropy_step = (
        float(np.min(np.diff(comoving_entropy)) / entropy_scale)
        if n_points > 1 else 0.0
    )
    entropy_monotonic_tolerance = 1.0e-5
    entropy_monotonic = minimum_entropy_step >= -entropy_monotonic_tolerance
    late_index = int(0.9 * (n_points - 1))
    late_entropy_change = (
        float((comoving_entropy[-1] - comoving_entropy[late_index]) / max(comoving_entropy[-1], 1.0e-300))
        if comoving_entropy[-1] > 0.0 else None
    )

    def event_record(event_n: float, state: np.ndarray) -> dict[str, float]:
        ec = max(float(state[0]), 0.0)
        er = max(float(state[1]), 0.0)
        et = ec + er
        if et <= 0.0:
            raise RuntimeError("event state has non-positive total density")
        t_event = temperature_scale * er**0.25
        return {
            "N": float(event_n),
            "a_over_ai": float(np.exp(event_n)),
            "rho_condensate_GeV4": float(rho_total0 * ec),
            "rho_radiation_GeV4": float(rho_total0 * er),
            "H_GeV": float(h_initial * sqrt(et)),
            "temperature_GeV": float(t_event),
            "radiation_fraction": float(er / et),
        }

    radiation_event: dict[str, float] | None = None
    if f_r0 >= f_c0:
        radiation_event = event_record(0.0, initial_state)
    elif len(solution.t_events) > 0 and len(solution.t_events[0]) > 0:
        radiation_event = event_record(
            float(solution.t_events[0][0]), solution.y_events[0][0]
        )

    h_gamma_event: dict[str, float] | None = None
    if gamma_width > 0.0 and abs(gamma_over_h_initial - 1.0) <= 1.0e-12:
        h_gamma_event = event_record(0.0, initial_state)
    elif 0.0 < gamma_over_h_initial < 1.0:
        if len(solution.t_events) > 1 and len(solution.t_events[1]) > 0:
            h_gamma_event = event_record(
                float(solution.t_events[1][0]), solution.y_events[1][0]
            )

    completion_reached = f_c0 <= completion
    if completion_event_added and len(solution.t_events) > 2 and len(solution.t_events[2]) > 0:
        completion_reached = True

    sudden_temperature = (
        reheating_temperature_from_width(gamma_width, degrees, reduced_planck_mass=planck)
        if gamma_width > 0.0 else None
    )
    continuous_to_sudden_ratio = None
    sudden_ratio_identity_residual = None
    if h_gamma_event is not None and sudden_temperature is not None and sudden_temperature > 0.0:
        continuous_to_sudden_ratio = h_gamma_event["temperature_GeV"] / sudden_temperature
        expected_ratio = h_gamma_event["radiation_fraction"] ** 0.25
        sudden_ratio_identity_residual = continuous_to_sudden_ratio - expected_ratio

    bbn_proxy = None
    if h_gamma_event is not None:
        bbn_proxy = h_gamma_event["temperature_GeV"] >= bbn_temperature

    radiation_fraction_history = rho_r_bar / total_bar
    entropy_ratio_to_initial = (
        float(comoving_entropy[-1] / comoving_entropy[0])
        if comoving_entropy[0] > 0.0 else None
    )
    report: dict[str, object] = {
        "schema": "ptum.continuous_perturbative_reheating_history",
        "schema_version": 1,
        "model_scope": "conditional_constant_w_constant_width_two_fluid_FRW",
        "initial_conditions": {
            "rho_condensate_GeV4": rho_c0,
            "rho_radiation_GeV4": rho_r0,
            "rho_total_GeV4": rho_total0,
            "condensate_initial_fraction": f_c0,
            "radiation_initial_fraction": f_r0,
            "H_initial_GeV": h_initial,
            "decay_width_GeV": gamma_width,
            "Gamma_over_H_initial": gamma_over_h_initial,
            "condensate_equation_of_state": w_c,
            "g_star_constant": degrees,
            "reduced_planck_mass_GeV": planck,
        },
        "integration": {
            "success": True,
            "solver": "BDF",
            "rtol": rel_tol,
            "atol": abs_tol,
            "max_efolds_requested": n_max,
            "N_final": n_final,
            "n_output_points": n_points,
            "completion_fraction_numerical": completion,
            "condensate_decay_completion_reached": completion_reached,
            "terminated_on_completion_event": bool(solution.status == 1),
            "termination_message": str(solution.message),
        },
        "energy_budget": {
            "initial_total_density_normalized": 1.0,
            "cumulative_condensate_expansion_work_fraction": float(work_c[-1]),
            "cumulative_radiation_expansion_work_fraction": float(work_r[-1]),
            "cumulative_condensate_to_radiation_transfer_fraction": float(transfer[-1]),
            "condensate_budget_max_abs_residual": condensate_budget_max,
            "radiation_budget_max_abs_residual": radiation_budget_max,
            "total_budget_max_abs_residual": total_budget_max,
            "max_abs_residual_normalized_to_initial_total": budget_max,
        },
        "events": {
            "radiation_domination": radiation_event,
            "H_equals_Gamma": h_gamma_event,
            "initial_H_below_Gamma": bool(gamma_width > h_initial),
        },
        "reheating_diagnostics": {
            "sudden_decay_temperature_GeV": sudden_temperature,
            "continuous_temperature_at_H_equals_Gamma_GeV": (
                h_gamma_event["temperature_GeV"] if h_gamma_event is not None else None
            ),
            "continuous_to_sudden_temperature_ratio_at_H_equals_Gamma": continuous_to_sudden_ratio,
            "T_ratio_identity_residual_vs_Omega_r_quarter_power": sudden_ratio_identity_residual,
            "temperature_at_radiation_domination_GeV": (
                radiation_event["temperature_GeV"] if radiation_event is not None else None
            ),
            "maximum_temperature_sampled_GeV": float(np.max(temperature)),
            "N_at_maximum_temperature_sampled": float(efolds[int(np.argmax(temperature))]),
            "final_temperature_GeV": float(temperature[-1]),
            "final_radiation_fraction": float(radiation_fraction_history[-1]),
            "bbn_proxy_at_H_equals_Gamma_passes": bbn_proxy,
            "bbn_proxy_temperature_GeV": bbn_temperature,
            "bbn_proxy_is_full_thermal_history": False,
        },
        "entropy": {
            "initial_comoving_entropy_GeV3": float(comoving_entropy[0]),
            "final_comoving_entropy_GeV3": float(comoving_entropy[-1]),
            "final_to_initial_comoving_entropy_ratio": entropy_ratio_to_initial,
            "comoving_entropy_non_decreasing_within_tolerance": bool(entropy_monotonic),
            "minimum_sampled_entropy_step_over_final_entropy": minimum_entropy_step,
            "relative_entropy_change_over_last_tenth_of_integration": late_entropy_change,
            "numerical_monotonicity_tolerance": entropy_monotonic_tolerance,
            "g_star_entropy_assumed_equal_to_energy_g_star": True,
        },
        "assumptions": {
            "constant_condensate_equation_of_state": True,
            "constant_perturbative_decay_width": True,
            "instantaneous_thermalization_of_decay_products": True,
            "constant_radiation_degrees_of_freedom": True,
            "radiation_equation_of_state": "1/3",
            "inverse_decays_and_scattering": False,
            "thermal_masses_pauli_blocking_bose_enhancement": False,
            "temperature_dependent_EW_QCD_thresholds": False,
            "Higgs_portal_pair_production": False,
            "nonperturbative_preheating_and_rescattering": False,
            "PTUM_scalar_energy_partition_derived_from_action": False,
            "physical_PTUM_benchmark_prediction": False,
        },
        "history": {
            "N": efolds.tolist(),
            "a_over_ai": np.exp(efolds).tolist(),
            "rho_condensate_GeV4": (rho_total0 * rho_c_bar).tolist(),
            "rho_radiation_GeV4": (rho_total0 * rho_r_bar).tolist(),
            "H_GeV": h_history.tolist(),
            "temperature_GeV": temperature.tolist(),
            "radiation_fraction": radiation_fraction_history.tolist(),
            "comoving_entropy_GeV3": comoving_entropy.tolist(),
            "cumulative_transfer_fraction": transfer.tolist(),
            "total_energy_budget_residual": total_budget.tolist(),
        },
    }
    json.dumps(report, allow_nan=False)
    return report


__all__ = ["integrate_perturbative_reheating_history"]
