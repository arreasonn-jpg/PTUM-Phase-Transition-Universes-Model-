#!/usr/bin/env python3
"""Paired full-grid output-sampling and solver-tolerance convergence study.

All five numerical profiles are run in one process with one immutable set of
scenario parameters and initial conditions. Solver-tolerance convergence is
assessed from successive refinements, not only against the coarsest solver
tolerance. The study remains a homogeneous post-threshold sensitivity
calculation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from ptum_inflation_background import state_at_field_value
from ptum_task1_scan import build_initial_condition_grid, build_scan_scenarios
from ptum_task1_simulation import M_PL, run_parameter_scan

T_MAX = 20.0
EXPECTED_ROWS = 100
MAX_RHS_EVALUATIONS = 1_000_000
SOLVER_METHOD = "DOP853"
OUTPUT_GRID_REFERENCE = 4001
OUTPUT_GRID_REFINED = 256001
TOLERANCE_REFERENCE = (1.0e-9, 1.0e-12)
TOLERANCE_LEVELS = (
    TOLERANCE_REFERENCE,
    (1.0e-10, 1.0e-13),
    (1.0e-11, 1.0e-14),
    (1.0e-12, 1.0e-15),
)
STUDY_SPECS = (
    {
        "name": "reference_4001",
        "comparison_role": "reference",
        "n_output_points": OUTPUT_GRID_REFERENCE,
        "rtol": TOLERANCE_REFERENCE[0],
        "atol": TOLERANCE_REFERENCE[1],
    },
    {
        "name": "grid_256001",
        "comparison_role": "output_grid",
        "n_output_points": OUTPUT_GRID_REFINED,
        "rtol": TOLERANCE_REFERENCE[0],
        "atol": TOLERANCE_REFERENCE[1],
    },
    {
        "name": "tolerance_1e-10_1e-13",
        "comparison_role": "solver_tolerance",
        "n_output_points": OUTPUT_GRID_REFINED,
        "rtol": TOLERANCE_LEVELS[1][0],
        "atol": TOLERANCE_LEVELS[1][1],
    },
    {
        "name": "tolerance_1e-11_1e-14",
        "comparison_role": "solver_tolerance",
        "n_output_points": OUTPUT_GRID_REFINED,
        "rtol": TOLERANCE_LEVELS[2][0],
        "atol": TOLERANCE_LEVELS[2][1],
    },
    {
        "name": "tolerance_1e-12_1e-15",
        "comparison_role": "solver_tolerance",
        "n_output_points": OUTPUT_GRID_REFINED,
        "rtol": TOLERANCE_LEVELS[3][0],
        "atol": TOLERANCE_LEVELS[3][1],
    },
)
FINAL_FIELDS = ("Phi", "Phi_dot", "psi", "psi_dot", "H", "rho_total")
CLASSIFICATION_METRICS = (
    "Q_final",
    "w_final",
    "virial_final",
    "quadratic_virial_final",
    "H_over_omega_max",
)
CLASSIFICATION_FLAGS = (
    "regime",
    "quartic_achieved",
    "n_late_half_cycles",
    "n_oscillations",
    "adiabaticity_valid",
)
DIAGNOSTIC_FIELDS = (
    "max_abs_relative_frw_continuity_residual",
    "max_abs_finite_difference_frw_residual_over_Hrho",
)
LIMITS = {
    "max_final_state_relative_difference": 1.0e-6,
    "max_classification_normalized_absolute_difference": 1.0e-5,
    "max_chain_rule_residual_absolute_difference": 1.0e-8,
    "max_finite_difference_residual_absolute_difference_for_tolerance": 1.0e-3,
}


def _finite_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _max_finite(values: Any) -> float | None:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    return float(np.max(np.abs(finite))) if finite.size else None


def _relative_difference(a: float, b: float, scale: float) -> float:
    denominator = max(
        abs(a),
        abs(b),
        abs(scale) * 1.0e-14,
        np.finfo(float).tiny,
    )
    return abs(a - b) / denominator


def build_row_key(scenario: str, ic_params: dict[str, Any], params: Any) -> str:
    """Build a stable dimensionless key from the exact shared input values."""
    seed = float(ic_params["psi_init"]) / params.psi_0
    velocity = float(ic_params["psi_dot_init"]) / (params.mu * params.psi_0)
    offset = float(ic_params["phi_offset"]) / params.Phi_c
    return (
        f"{scenario}|seed={seed:.12g}|velocity={velocity:.12g}|"
        f"offset={offset:.12g}"
    )


def _record_result(row: dict[str, Any], scenario: str, params: Any) -> dict[str, Any]:
    ic = row.get("ic_params", {})
    record: dict[str, Any] = {
        "scenario": scenario,
        "row_key": build_row_key(scenario, ic, params),
        "ic_params": _json_safe(ic),
        "success": bool(row.get("success", False)),
        "solver_stats": _json_safe(row.get("solver_stats", {})),
    }
    if not record["success"]:
        record["error"] = row.get("error", "unspecified integration failure")
        return record

    classification = row.get("classification", {})
    record["final_state"] = {
        field: _finite_float(row[field][-1]) for field in FINAL_FIELDS
    }
    record["classification"] = {
        field: (
            _finite_float(classification.get(field))
            if field in CLASSIFICATION_METRICS
            else _json_safe(classification.get(field))
        )
        for field in (*CLASSIFICATION_METRICS, *CLASSIFICATION_FLAGS)
    }
    record["diagnostics"] = {
        "max_abs_relative_frw_continuity_residual":
            _max_finite(row["continuity_residual_relative"]),
        "max_abs_finite_difference_frw_residual_over_Hrho":
            _max_finite(
                row["continuity_residual_finite_difference_background_relative"]
            ),
    }
    return record


def compare_records(reference: dict[str, Any], candidate: dict[str, Any],
                    params: Any, comparison_role: str) -> dict[str, Any]:
    """Compare one identical-input trajectory across grid/tolerance settings."""
    result: dict[str, Any] = {
        "row_key": reference.get("row_key"),
        "comparison_role": comparison_role,
        "comparison_available": False,
        "comparison_pass": False,
    }
    if not reference.get("success") or not candidate.get("success"):
        result["reference_success"] = bool(reference.get("success"))
        result["candidate_success"] = bool(candidate.get("success"))
        result["reference_error"] = reference.get("error")
        result["candidate_error"] = candidate.get("error")
        return result

    scales = {
        "Phi": params.Phi_c,
        "Phi_dot": params.mu * params.Phi_c,
        "psi": params.psi_0,
        "psi_dot": params.mu * params.psi_0,
        "H": max(params.H_threshold_exact_end, params.mu * 1.0e-12),
        "rho_total": max(params.V0, 1.0),
    }
    state_differences = {}
    state_complete = True
    for field in FINAL_FIELDS:
        left = _finite_float(reference["final_state"].get(field))
        right = _finite_float(candidate["final_state"].get(field))
        if left is None or right is None:
            state_complete = False
            state_differences[field] = None
        else:
            state_differences[field] = _relative_difference(
                left, right, scales[field]
            )

    class_relative_differences = {}
    class_normalized_differences = {}
    class_availability_match = True
    for field in CLASSIFICATION_METRICS:
        left = _finite_float(reference["classification"].get(field))
        right = _finite_float(candidate["classification"].get(field))
        if (left is None) != (right is None):
            class_availability_match = False
            class_relative_differences[field] = None
            class_normalized_differences[field] = None
        elif left is None:
            class_relative_differences[field] = None
            class_normalized_differences[field] = None
        else:
            class_relative_differences[field] = _relative_difference(
                left, right, 1.0
            )
            # These observables are dimensionless. Normalize by their natural
            # unit scale so a value near zero (especially w) is not assigned
            # an arbitrarily large relative error by division by |value|.
            class_normalized_differences[field] = (
                abs(left - right) / max(1.0, abs(left), abs(right))
            )

    flag_matches = {
        field: (
            reference["classification"].get(field)
            == candidate["classification"].get(field)
        )
        for field in CLASSIFICATION_FLAGS
    }
    diagnostic_differences = {}
    diagnostic_availability_match = True
    for field in DIAGNOSTIC_FIELDS:
        left = _finite_float(reference["diagnostics"].get(field))
        right = _finite_float(candidate["diagnostics"].get(field))
        if left is None or right is None:
            diagnostic_availability_match = False
            diagnostic_differences[field] = None
        else:
            diagnostic_differences[field] = abs(left - right)

    max_state = max(
        (value for value in state_differences.values() if value is not None),
        default=None,
    )
    max_class_relative = max(
        (value for value in class_relative_differences.values()
         if value is not None),
        default=None,
    )
    max_class_normalized = max(
        (value for value in class_normalized_differences.values()
         if value is not None),
        default=None,
    )
    chain_difference = diagnostic_differences[
        "max_abs_relative_frw_continuity_residual"
    ]
    finite_difference_residual_difference = diagnostic_differences[
        "max_abs_finite_difference_frw_residual_over_Hrho"
    ]

    state_pass = (
        state_complete
        and max_state is not None
        and max_state <= LIMITS["max_final_state_relative_difference"]
    )
    classification_pass = (
        class_availability_match
        and (
            max_class_normalized is None
            or max_class_normalized
            <= LIMITS["max_classification_normalized_absolute_difference"]
        )
    )
    flags_pass = all(flag_matches.values())
    chain_rule_pass = (
        chain_difference is not None
        and chain_difference
        <= LIMITS["max_chain_rule_residual_absolute_difference"]
    )
    finite_difference_pass = (
        comparison_role == "output_grid"
        or (
            finite_difference_residual_difference is not None
            and finite_difference_residual_difference
            <= LIMITS[
                "max_finite_difference_residual_absolute_difference_for_tolerance"
            ]
        )
    )

    result.update({
        "comparison_available": True,
        "state_relative_differences": state_differences,
        "classification_relative_differences": class_relative_differences,
        "classification_normalized_absolute_differences":
            class_normalized_differences,
        "classification_flag_matches": flag_matches,
        "classification_metric_availability_match": class_availability_match,
        "diagnostic_absolute_differences": diagnostic_differences,
        "max_final_state_relative_difference": max_state,
        # Retained as a diagnostic only; it is ill-conditioned for dimensionless
        # observables close to zero and is not used as the acceptance metric.
        "max_classification_relative_difference": max_class_relative,
        "max_classification_normalized_absolute_difference":
            max_class_normalized,
        "classification_metrics_compared": sum(
            value is not None for value in class_normalized_differences.values()
        ),
        "max_chain_rule_residual_absolute_difference": chain_difference,
        "max_finite_difference_residual_absolute_difference":
            finite_difference_residual_difference,
        "state_pass": bool(state_pass),
        "classification_pass": bool(classification_pass),
        "flags_pass": bool(flags_pass),
        "chain_rule_pass": bool(chain_rule_pass),
        "finite_difference_residual_pass": bool(finite_difference_pass),
        "comparison_pass": bool(
            state_pass
            and classification_pass
            and flags_pass
            and chain_rule_pass
            and finite_difference_pass
            and diagnostic_availability_match
        ),
    })
    return result


def summarize_solver_tolerance_convergence(
    comparisons: list[dict[str, Any]],
    expected_rows: int = EXPECTED_ROWS,
) -> dict[str, Any]:
    """Assess successive tolerance refinement and require a converged final pair."""
    tolerance_specs = [
        item["name"] for item in STUDY_SPECS
        if item["comparison_role"] == "solver_tolerance"
    ]
    state_fields = list(FINAL_FIELDS)
    classification_fields = list(CLASSIFICATION_METRICS)
    steps = []

    for candidate_spec in tolerance_specs:
        items = [
            item for item in comparisons
            if item.get("comparison_role") == "solver_tolerance"
            and item.get("candidate_spec") == candidate_spec
        ]
        state_envelope = {
            field: max(
                (
                    row.get("state_relative_differences", {}).get(field)
                    for row in items
                    if row.get("state_relative_differences", {}).get(field)
                    is not None
                ),
                default=None,
            )
            for field in state_fields
        }
        classification_envelope = {
            field: max(
                (
                    row.get(
                        "classification_normalized_absolute_differences", {}
                    ).get(field)
                    for row in items
                    if row.get(
                        "classification_normalized_absolute_differences", {}
                    ).get(field) is not None
                ),
                default=None,
            )
            for field in classification_fields
        }
        steps.append({
            "candidate_spec": candidate_spec,
            "comparison_count": len(items),
            "strictly_passing_comparisons": sum(
                bool(row.get("comparison_pass")) for row in items
            ),
            "max_state_relative_difference_by_field": state_envelope,
            "all_state_metrics_available": bool(items) and all(
                all(
                    row.get("state_relative_differences", {}).get(field)
                    is not None
                    for field in state_fields
                )
                for row in items
            ),
            "max_classification_normalized_absolute_difference_by_field":
                classification_envelope,
            "classification_metrics_available_by_field": {
                field: sum(
                    row.get(
                        "classification_normalized_absolute_differences", {}
                    ).get(field) is not None
                    for row in items
                )
                for field in classification_fields
            },
            "max_chain_rule_residual_absolute_difference": max(
                (
                    row.get(
                        "max_chain_rule_residual_absolute_difference"
                    )
                    for row in items
                    if row.get(
                        "max_chain_rule_residual_absolute_difference"
                    ) is not None
                ),
                default=None,
            ),
            "max_finite_difference_residual_absolute_difference": max(
                (
                    row.get(
                        "max_finite_difference_residual_absolute_difference"
                    )
                    for row in items
                    if row.get(
                        "max_finite_difference_residual_absolute_difference"
                    ) is not None
                ),
                default=None,
            ),
            "all_flags_match": bool(items) and all(
                row.get("flags_pass", False) for row in items
            ),
            "all_metric_availability_matches": bool(items) and all(
                row.get("classification_metric_availability_match", False)
                for row in items
            ),
            "all_chain_rule_checks_pass": bool(items) and all(
                row.get("chain_rule_pass", False) for row in items
            ),
            "all_finite_difference_checks_pass": bool(items) and all(
                row.get("finite_difference_residual_pass", False)
                for row in items
            ),
        })

    def monotonic_envelopes(
        field_name: str,
        fields: list[str],
        *,
        allow_consistently_unavailable: bool = False,
    ) -> dict[str, bool]:
        result = {}
        for field in fields:
            values = [step[field_name].get(field) for step in steps]
            if (
                allow_consistently_unavailable
                and len(values) == len(tolerance_specs)
                and all(value is None for value in values)
            ):
                result[field] = True
                continue
            result[field] = (
                len(values) == len(tolerance_specs)
                and all(value is not None for value in values)
                and all(
                    values[index + 1] <= values[index]
                    for index in range(len(values) - 1)
                )
            )
        return result

    state_monotonic = monotonic_envelopes(
        "max_state_relative_difference_by_field", state_fields
    )
    classification_monotonic = monotonic_envelopes(
        "max_classification_normalized_absolute_difference_by_field",
        classification_fields,
        allow_consistently_unavailable=True,
    )
    consistently_unavailable_classification_fields = [
        field for field in classification_fields
        if all(
            step["max_classification_normalized_absolute_difference_by_field"]
            .get(field) is None
            for step in steps
        )
    ]
    final_step = steps[-1] if steps else {}
    final_items = [
        item for item in comparisons
        if item.get("comparison_role") == "solver_tolerance"
        and item.get("candidate_spec") == (
            tolerance_specs[-1] if tolerance_specs else None
        )
    ]
    final_refinement_pass = (
        len(final_items) == expected_rows
        and all(item.get("comparison_pass", False) for item in final_items)
    )
    complete_steps = (
        len(steps) == len(tolerance_specs)
        and all(step["comparison_count"] == expected_rows for step in steps)
    )
    all_diagnostics_pass = all(
        step["all_state_metrics_available"]
        and step["all_chain_rule_checks_pass"]
        and step["all_finite_difference_checks_pass"]
        and step["all_metric_availability_matches"]
        and step["all_flags_match"]
        for step in steps
    )
    monotonic_state_pass = bool(state_monotonic) and all(
        state_monotonic.values()
    )
    monotonic_classification_pass = (
        bool(classification_monotonic)
        and all(classification_monotonic.values())
    )
    passed = bool(
        complete_steps
        and monotonic_state_pass
        and monotonic_classification_pass
        and all_diagnostics_pass
        and final_refinement_pass
    )
    return {
        "step_count": len(steps),
        "steps": steps,
        "state_error_envelope_monotonic_by_field": state_monotonic,
        "classification_error_envelope_monotonic_by_field":
            classification_monotonic,
        "consistently_unavailable_classification_fields":
            consistently_unavailable_classification_fields,
        "monotonic_state_error_envelope": monotonic_state_pass,
        "monotonic_classification_error_envelope":
            monotonic_classification_pass,
        "final_refinement_comparison_count": len(final_items),
        "final_refinement_passing_comparisons": sum(
            bool(item.get("comparison_pass")) for item in final_items
        ),
        "final_refinement_pass": final_refinement_pass,
        "complete_steps": complete_steps,
        "all_diagnostics_pass": all_diagnostics_pass,
        "pass": passed,
        "interpretation": (
            "The first tolerance refinements are retained as convergence "
            "history and may lie outside the final pairwise error limits. "
            "Acceptance requires monotonic reduction of every state and "
            "dimensionless diagnostic error envelope, unchanged classification "
            "flags and metric availability, passing conservation diagnostics, "
            "and all rows passing the finest adjacent tolerance comparison."
        ),
        "final_step": final_step,
    }

def _build_cases() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    scenario_params = dict(build_scan_scenarios())
    for scenario, params in scenario_params.items():
        psi_values, velocity_values, offsets = build_initial_condition_grid(
            params, profile="full"
        )
        phi_dot_by_offset = {}
        for offset in offsets:
            x_target = (params.Phi_c - offset) / M_PL
            background_state = state_at_field_value(
                params.lambda_phi, x_target, V0=params.V0
            )
            phi_dot_by_offset[offset] = float(background_state["Phi_dot"])
        for psi_init in psi_values:
            for psi_dot_init in velocity_values:
                for offset in offsets:
                    ic = {
                        "psi_init": float(psi_init),
                        "psi_dot_init": float(psi_dot_init),
                        "phi_offset": float(offset),
                    }
                    cases.append({
                        "scenario": scenario,
                        "params": params,
                        "ic_params": ic,
                        "phi_dot_init": phi_dot_by_offset[offset],
                        "row_key": build_row_key(scenario, ic, params),
                    })
    return cases, scenario_params


def _payload(records_by_spec: dict[str, list[dict[str, Any]]],
             comparisons: list[dict[str, Any]],
             failures: list[dict[str, Any]],
             completed_specs: list[str],
             expected_keys: set[str]) -> dict[str, Any]:
    flat_records = [
        record
        for spec in STUDY_SPECS
        for record in records_by_spec.get(spec["name"], [])
    ]
    expected_spec_names = [spec["name"] for spec in STUDY_SPECS]
    coverage = {}
    for spec_name in expected_spec_names:
        rows = records_by_spec.get(spec_name, [])
        keys = [row.get("row_key") for row in rows]
        coverage[spec_name] = {
            "row_count": len(rows),
            "unique_row_keys": len(set(keys)),
            "missing_row_keys": sorted(expected_keys - set(keys)),
            "unexpected_row_keys": sorted(set(keys) - expected_keys),
            "complete": (
                len(rows) == EXPECTED_ROWS
                and len(set(keys)) == EXPECTED_ROWS
                and set(keys) == expected_keys
            ),
        }
    all_successful = (
        len(flat_records) == len(STUDY_SPECS) * EXPECTED_ROWS
        and all(row.get("success") for row in flat_records)
    )
    all_coverage_complete = all(item["complete"] for item in coverage.values())

    by_role = {}
    for role in ("output_grid", "solver_tolerance"):
        items = [item for item in comparisons
                 if item.get("comparison_role") == role]
        by_role[role] = {
            "comparison_count": len(items),
            "passing_comparisons": sum(
                bool(item.get("comparison_pass")) for item in items
            ),
            "max_final_state_relative_difference": max(
                (item["max_final_state_relative_difference"]
                 for item in items
                 if item.get("max_final_state_relative_difference") is not None),
                default=None,
            ),
            "max_classification_relative_difference_diagnostic": max(
                (item["max_classification_relative_difference"]
                 for item in items
                 if item.get("max_classification_relative_difference") is not None),
                default=None,
            ),
            "max_classification_normalized_absolute_difference": max(
                (
                    item["max_classification_normalized_absolute_difference"]
                    for item in items
                    if item.get(
                        "max_classification_normalized_absolute_difference"
                    ) is not None
                ),
                default=None,
            ),
            "max_chain_rule_residual_absolute_difference": max(
                (item["max_chain_rule_residual_absolute_difference"]
                 for item in items
                 if item.get("max_chain_rule_residual_absolute_difference") is not None),
                default=None,
            ),
            "max_finite_difference_residual_absolute_difference": max(
                (item["max_finite_difference_residual_absolute_difference"]
                 for item in items
                 if item.get("max_finite_difference_residual_absolute_difference") is not None),
                default=None,
            ),
        }

    output_grid_items = [
        item for item in comparisons
        if item.get("comparison_role") == "output_grid"
    ]
    output_grid_pass = (
        len(output_grid_items) == EXPECTED_ROWS
        and all(
            item.get("comparison_available") and item.get("comparison_pass")
            for item in output_grid_items
        )
    )
    tolerance_convergence = summarize_solver_tolerance_convergence(
        comparisons, expected_rows=EXPECTED_ROWS
    )
    all_comparisons_present = (
        len(comparisons) == (len(STUDY_SPECS) - 1) * EXPECTED_ROWS
        and all(item.get("comparison_available") for item in comparisons)
    )
    full_study_pass = (
        all_successful
        and all_coverage_complete
        and not failures
        and len(completed_specs) == len(STUDY_SPECS)
        and all_comparisons_present
        and output_grid_pass
        and tolerance_convergence["pass"]
    )
    return {
        "schema_version": 2,
        "purpose": "paired full 100-row homogeneous DOP853 output-grid and solver-tolerance convergence study",
        "solver_method": SOLVER_METHOD,
        "t_max_over_mu_inverse": T_MAX,
        "max_rhs_evaluations_per_trajectory": MAX_RHS_EVALUATIONS,
        "expected_rows_per_spec": EXPECTED_ROWS,
        "study_specs": list(STUDY_SPECS),
        "limits": dict(LIMITS),
        "completed_specs": list(completed_specs),
        "coverage": coverage,
        "run_count": len(flat_records),
        "successful_runs": sum(bool(row.get("success")) for row in flat_records),
        "failed_runs": sum(not bool(row.get("success")) for row in flat_records),
        "comparison_count": len(comparisons),
        "comparisons_by_role": by_role,
        "output_grid_comparison_pass": output_grid_pass,
        "solver_tolerance_convergence": tolerance_convergence,
        "all_comparisons_present": all_comparisons_present,
        "comparisons": comparisons,
        "failures": failures,
        "full_study_pass": bool(full_study_pass),
        "rows": flat_records,
        "interpretation": (
            "All output-grid and tolerance variants reuse the same scenario "
            "parameter objects and exact initial-condition values within this "
            "process. Solver-tolerance acceptance is based on a monotonically "
            "decreasing successive-refinement error envelope and a passing "
            "finest adjacent pair, not on requiring every intermediate solver "
            "profile to be within the final error threshold of the coarsest "
            "profile. This is a homogeneous post-threshold sensitivity scan, "
            "not a coupled threshold-crossing, quantum-seeded inhomogeneous "
            "waterfall, backreaction, rescattering, or relic calculation."
        ),
    }

def write_json_atomic(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(_json_safe(payload), indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def run_study(output: Path, checkpoint: Path) -> dict[str, Any]:
    cases, scenario_params = _build_cases()
    expected_keys = {case["row_key"] for case in cases}
    if len(cases) != EXPECTED_ROWS or len(expected_keys) != EXPECTED_ROWS:
        raise RuntimeError(
            f"Expected {EXPECTED_ROWS} unique initial conditions; "
            f"received {len(cases)} cases and {len(expected_keys)} keys"
        )

    records_by_spec: dict[str, list[dict[str, Any]]] = {}
    comparisons: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    completed_specs: list[str] = []

    for spec in STUDY_SPECS:
        spec_name = spec["name"]
        spec_records: list[dict[str, Any]] = []
        records_by_spec[spec_name] = spec_records
        print(
            f"[paired-convergence] starting {spec_name}: "
            f"{EXPECTED_ROWS} trajectories, n_points={spec['n_output_points']}, "
            f"rtol={spec['rtol']:g}, atol={spec['atol']:g}",
            flush=True,
        )
        for index, case in enumerate(cases, start=1):
            params = case["params"]
            ic = case["ic_params"]
            try:
                rows = run_parameter_scan(
                    params,
                    psi_init_range=[ic["psi_init"]],
                    psi_dot_init_range=[ic["psi_dot_init"]],
                    phi_offset_range=[ic["phi_offset"]],
                    t_max=T_MAX,
                    n_points=spec["n_output_points"],
                    phi_dot_init_by_offset={
                        ic["phi_offset"]: case["phi_dot_init"]
                    },
                    max_rhs_evaluations=MAX_RHS_EVALUATIONS,
                    rtol=spec["rtol"],
                    atol=spec["atol"],
                    solver_method=SOLVER_METHOD,
                    progress_label=f"{spec_name} {case['row_key']}",
                )
                if len(rows) != 1:
                    raise RuntimeError(
                        f"Expected one trajectory result, received {len(rows)}"
                    )
                record = _record_result(rows[0], case["scenario"], params)
            except Exception as exc:
                record = {
                    "scenario": case["scenario"],
                    "row_key": case["row_key"],
                    "ic_params": _json_safe(ic),
                    "success": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            record["study_spec"] = spec_name
            spec_records.append(record)
            if not record.get("success"):
                failures.append({
                    "study_spec": spec_name,
                    "row_key": case["row_key"],
                    "error": record.get("error", "unspecified failure"),
                    "solver_stats": record.get("solver_stats"),
                })
            partial = _payload(
                records_by_spec, comparisons, failures, completed_specs,
                expected_keys,
            )
            write_json_atomic(partial, output)
            write_json_atomic(partial, checkpoint)
            if index % 10 == 0 or index == EXPECTED_ROWS:
                print(
                    f"[paired-convergence] {spec_name}: "
                    f"{index}/{EXPECTED_ROWS} rows recorded",
                    flush=True,
                )

        keys = [record.get("row_key") for record in spec_records]
        if (
            len(spec_records) != EXPECTED_ROWS
            or len(set(keys)) != EXPECTED_ROWS
            or set(keys) != expected_keys
        ):
            failures.append({
                "study_spec": spec_name,
                "error": "row coverage is incomplete or contains duplicate/unexpected keys",
                "row_count": len(spec_records),
                "unique_row_keys": len(set(keys)),
                "missing_row_keys": sorted(expected_keys - set(keys)),
                "unexpected_row_keys": sorted(set(keys) - expected_keys),
            })

        completed_specs.append(spec_name)
        if spec_name == "grid_256001":
            reference_name = "reference_4001"
            role = "output_grid"
        elif spec["comparison_role"] == "solver_tolerance":
            spec_index = next(
                index for index, item in enumerate(STUDY_SPECS)
                if item["name"] == spec_name
            )
            reference_name = STUDY_SPECS[spec_index - 1]["name"]
            role = "solver_tolerance"
        else:
            reference_name = None
            role = None

        if reference_name is not None:
            reference_map = {
                row["row_key"]: row
                for row in records_by_spec.get(reference_name, [])
            }
            candidate_map = {row["row_key"]: row for row in spec_records}
            for row_key in sorted(expected_keys):
                reference = reference_map.get(row_key)
                candidate = candidate_map.get(row_key)
                if reference is None or candidate is None:
                    comparisons.append({
                        "row_key": row_key,
                        "comparison_role": role,
                        "comparison_available": False,
                        "comparison_pass": False,
                        "error": "missing reference or candidate row",
                    })
                    continue
                comparison = compare_records(
                    reference,
                    candidate,
                    scenario_params[reference["scenario"]],
                    role,
                )
                comparison["reference_spec"] = reference_name
                comparison["candidate_spec"] = spec_name
                comparisons.append(comparison)

        partial = _payload(
            records_by_spec, comparisons, failures, completed_specs,
            expected_keys,
        )
        write_json_atomic(partial, output)
        write_json_atomic(partial, checkpoint)
        print(
            f"[paired-convergence] completed {spec_name}: "
            f"{sum(bool(row.get('success')) for row in spec_records)}/"
            f"{len(spec_records)} successful",
            flush=True,
        )

    payload = _payload(
        records_by_spec, comparisons, failures, completed_specs, expected_keys
    )
    write_json_atomic(payload, output)
    write_json_atomic(payload, checkpoint)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="ptum_full_grid_convergence_study.json",
        help="Strict-JSON result path",
    )
    parser.add_argument(
        "--checkpoint",
        default="ptum_full_grid_convergence_study_checkpoint.json",
        help="Strict-JSON incremental checkpoint path",
    )
    args = parser.parse_args()
    payload = run_study(Path(args.output), Path(args.checkpoint))
    print(
        f"Paired convergence: {payload['successful_runs']}/"
        f"{payload['run_count']} integrations; "
        f"{payload['comparison_count']} comparisons; "
        f"pass={payload['full_study_pass']}",
        flush=True,
    )
    if not payload["full_study_pass"]:
        raise RuntimeError(
            "Paired full-grid convergence failed or is incomplete; "
            "strict-JSON diagnostics were preserved"
        )


if __name__ == "__main__":
    main()
