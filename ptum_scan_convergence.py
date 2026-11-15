#!/usr/bin/env python3
"""Run targeted DOP853 tolerance and output-grid convergence diagnostics.

The probe covers the two rows that exhausted the Radau/BDF work guards and
two representative high-Q rows from the completed 100-point scan. It is a
homogeneous post-threshold numerical convergence study, not a new physical
waterfall or relic-abundance calculation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from ptum_inflation_background import state_at_field_value
from ptum_task1_scan import build_scan_scenarios
from ptum_task1_simulation import M_PL, run_parameter_scan

T_MAX = 20.0
OUTPUT_GRIDS = (4001, 8001, 16001)
TOLERANCE_LEVELS = (
    (1.0e-9, 1.0e-12),
    (1.0e-10, 1.0e-13),
    (1.0e-11, 1.0e-14),
)
MAX_RHS_EVALUATIONS = 1_000_000

# The first two reproduce the two DOP853-success / Radau-BDF-budget rows.
# The latter two probe the strongest quartic indicators in the DOP853 scan.
CASES = (
    {
        "name": "high_scale_implicit_budget_row",
        "scenario": "high_scale_threshold_matched",
        "psi_seed_scale": 1.0,
        "psi_velocity_scale": 0.0,
        "phi_offset_scale": 0.01,
    },
    {
        "name": "low_scale_implicit_budget_row",
        "scenario": "low_scale_underdamped_control",
        "psi_seed_scale": 1.0,
        "psi_velocity_scale": 0.0,
        "phi_offset_scale": 0.01,
    },
    {
        "name": "high_scale_largest_Q_row",
        "scenario": "high_scale_threshold_matched",
        "psi_seed_scale": 0.0,
        "psi_velocity_scale": 0.1,
        "phi_offset_scale": 0.1,
    },
    {
        "name": "low_scale_largest_Q_row",
        "scenario": "low_scale_underdamped_control",
        "psi_seed_scale": 5.0,
        "psi_velocity_scale": 5.0,
        "phi_offset_scale": 0.01,
    },
)

FINAL_FIELDS = (
    "Phi",
    "Phi_dot",
    "psi",
    "psi_dot",
    "H",
    "rho_total",
)
CLASSIFICATION_FIELDS = ("Q_final", "w_final", "virial_final")


def _finite_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def relative_difference(a: float | None, b: float | None,
                        characteristic_scale: float = 1.0) -> float | None:
    """Return a scale-aware symmetric relative difference, or None."""
    if a is None or b is None:
        return None
    denominator = max(
        abs(float(a)),
        abs(float(b)),
        abs(float(characteristic_scale)) * 1.0e-14,
        np.finfo(float).tiny,
    )
    return abs(float(a) - float(b)) / denominator


def _max_finite(values: Any) -> float | None:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    return float(np.max(np.abs(finite))) if finite.size else None


def _record_result(case: dict[str, Any], rtol: float, atol: float,
                   n_points: int, row: dict[str, Any]) -> dict[str, Any]:
    record: dict[str, Any] = {
        "case": case["name"],
        "scenario": case["scenario"],
        "rtol": rtol,
        "atol": atol,
        "n_output_points": n_points,
        "solver_method": "DOP853",
        "success": bool(row.get("success", False)),
        "ic_params": row.get("ic_params"),
    }
    if not record["success"]:
        record["error"] = row.get("error", "unspecified integration failure")
        record["solver_stats"] = row.get("solver_stats")
        return record

    record["solver_stats"] = row["solver_stats"]
    record["final_state"] = {
        field: _finite_float(row[field][-1])
        for field in FINAL_FIELDS
    }
    classification = row.get("classification", {})
    record["classification"] = {
        key: classification.get(key)
        for key in (
            "regime",
            "quartic_achieved",
            "Q_final",
            "w_final",
            "virial_final",
            "n_late_half_cycles",
            "n_oscillations",
            "adiabaticity_valid",
        )
    }
    record["diagnostics"] = {
        "max_abs_relative_frw_continuity_residual":
            _max_finite(row["continuity_residual_relative"]),
        "max_abs_finite_difference_frw_residual_over_Hrho":
            _max_finite(row["continuity_residual_finite_difference_background_relative"]),
    }
    return record


def _compare_records(reference: dict[str, Any],
                     candidate: dict[str, Any],
                     params: Any,
                     comparison: str) -> dict[str, Any]:
    state_scales = {
        "Phi": params.Phi_c,
        "Phi_dot": params.mu * params.Phi_c,
        "psi": params.psi_0,
        "psi_dot": params.mu * params.psi_0,
        "H": max(params.H_threshold_exact_end, params.mu * 1.0e-12),
        "rho_total": max(params.V0, 1.0),
    }
    ref_state = reference["final_state"]
    cand_state = candidate["final_state"]
    state_differences = {
        field: relative_difference(
            ref_state[field], cand_state[field], state_scales[field]
        )
        for field in FINAL_FIELDS
    }

    ref_class = reference["classification"]
    cand_class = candidate["classification"]
    class_differences = {
        field: relative_difference(
            _finite_float(ref_class.get(field)),
            _finite_float(cand_class.get(field)),
            1.0,
        )
        for field in CLASSIFICATION_FIELDS
    }
    return {
        "comparison": comparison,
        "reference": {
            "rtol": reference["rtol"],
            "atol": reference["atol"],
            "n_output_points": reference["n_output_points"],
        },
        "candidate": {
            "rtol": candidate["rtol"],
            "atol": candidate["atol"],
            "n_output_points": candidate["n_output_points"],
        },
        "regime_match": ref_class.get("regime") == cand_class.get("regime"),
        "quartic_flag_match":
            ref_class.get("quartic_achieved") == cand_class.get("quartic_achieved"),
        "late_half_cycle_count_match":
            ref_class.get("n_late_half_cycles") == cand_class.get("n_late_half_cycles"),
        "final_state_relative_differences": state_differences,
        "classification_relative_differences": class_differences,
        "diagnostic_absolute_differences": {
            key: (
                None
                if reference["diagnostics"].get(key) is None
                or candidate["diagnostics"].get(key) is None
                else abs(
                    reference["diagnostics"][key]
                    - candidate["diagnostics"][key]
                )
            )
            for key in reference["diagnostics"]
        },
    }


def run_convergence_probe() -> dict[str, Any]:
    scenario_params = dict(build_scan_scenarios())
    records: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for case in CASES:
        params = scenario_params[case["scenario"]]
        phi_offset = case["phi_offset_scale"] * params.Phi_c
        psi_init = case["psi_seed_scale"] * params.psi_0
        psi_dot_init = (
            case["psi_velocity_scale"] * params.mu * params.psi_0
        )
        x_target = (params.Phi_c - phi_offset) / M_PL
        fuel_state = state_at_field_value(
            params.lambda_phi, x_target, V0=params.V0
        )
        phi_dot_init = float(fuel_state["Phi_dot"])

        # Tolerance ladder at the finest output grid.
        run_specs = [
            (rtol, atol, OUTPUT_GRIDS[-1])
            for rtol, atol in TOLERANCE_LEVELS
        ]
        # Output-grid ladder at the reference tolerance. The finest-grid
        # reference is already present in the tolerance ladder.
        run_specs.extend([
            (TOLERANCE_LEVELS[0][0], TOLERANCE_LEVELS[0][1], n_points)
            for n_points in OUTPUT_GRIDS[:-1]
        ])

        case_records: dict[tuple[float, float, int], dict[str, Any]] = {}
        for rtol, atol, n_points in run_specs:
            print(
                f"[convergence] {case['name']}: rtol={rtol:g}, "
                f"atol={atol:g}, n_points={n_points}",
                flush=True,
            )
            rows = run_parameter_scan(
                params,
                psi_init_range=[psi_init],
                psi_dot_init_range=[psi_dot_init],
                phi_offset_range=[phi_offset],
                t_max=T_MAX,
                n_points=n_points,
                phi_dot_init_by_offset={phi_offset: phi_dot_init},
                max_rhs_evaluations=MAX_RHS_EVALUATIONS,
                rtol=rtol,
                atol=atol,
                solver_method="DOP853",
            )
            row = rows[0]
            record = _record_result(case, rtol, atol, n_points, row)
            record["fuel_velocity_source"] = "integrated_single_field_FRW_trajectory"
            records.append(record)
            case_records[(rtol, atol, n_points)] = record
            if not record["success"]:
                failures.append({
                    "case": case["name"],
                    "rtol": rtol,
                    "atol": atol,
                    "n_output_points": n_points,
                    "error": record.get("error"),
                })

        reference_tolerance = TOLERANCE_LEVELS[0]
        finest_grid = OUTPUT_GRIDS[-1]
        tolerance_reference = case_records[
            (reference_tolerance[0], reference_tolerance[1], finest_grid)
        ]
        for rtol, atol in TOLERANCE_LEVELS[1:]:
            candidate = case_records[(rtol, atol, finest_grid)]
            comparisons.append(_compare_records(
                tolerance_reference, candidate, params, "tolerance"
            ))

        grid_reference = case_records[
            (reference_tolerance[0], reference_tolerance[1], finest_grid)
        ]
        for n_points in OUTPUT_GRIDS[:-1]:
            candidate = case_records[
                (reference_tolerance[0], reference_tolerance[1], n_points)
            ]
            comparisons.append(_compare_records(
                grid_reference, candidate, params, "output_grid"
            ))

    return {
        "schema_version": 1,
        "purpose": "targeted homogeneous DOP853 tolerance and output-grid convergence diagnostic",
        "solver": "DOP853",
        "t_max_over_mu_inverse": T_MAX,
        "rhs_evaluation_limit_per_run": MAX_RHS_EVALUATIONS,
        "tolerance_levels": [
            {"rtol": rtol, "atol": atol}
            for rtol, atol in TOLERANCE_LEVELS
        ],
        "output_grids": list(OUTPUT_GRIDS),
        "cases": list(CASES),
        "run_count": len(records),
        "successful_runs": sum(bool(row["success"]) for row in records),
        "failed_runs": len(failures),
        "runs": records,
        "comparisons": comparisons,
        "failures": failures,
        "interpretation": (
            "Diagnostic only. No convergence threshold is declared by this "
            "script; inspect final-state and classification stability before "
            "promoting Gate 4. This does not simulate an inhomogeneous waterfall."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="ptum_scan_convergence_results.json",
        help="Strict-JSON output path",
    )
    args = parser.parse_args()

    payload = run_convergence_probe()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(output)

    print(
        f"Convergence runs: {payload['successful_runs']}/{payload['run_count']} "
        f"successful; output: {output}",
        flush=True,
    )
    if payload["failed_runs"]:
        raise RuntimeError(
            f"{payload['failed_runs']} convergence integrations failed; "
            "strict-JSON diagnostics were preserved"
        )


if __name__ == "__main__":
    main()
