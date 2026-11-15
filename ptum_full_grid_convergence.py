#!/usr/bin/env python3
"""Run a chunked 100-row DOP853 scan at a refined output grid.

The scan uses the same homogeneous post-threshold initial-condition grid,
solver tolerances and RHS guard as the 4,001-point baseline. Results are
stored as compact strict JSON so baseline and refined-grid artifacts can
be compared row by row without retaining all trajectory arrays in memory.
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

EXPECTED_ROWS = 100
T_MAX = 20.0
N_POINTS = 256001
RTOL = 1.0e-9
ATOL = 1.0e-12
MAX_RHS_EVALUATIONS = 1_000_000
SOLVER_METHOD = "DOP853"
FINAL_FIELDS = ("Phi", "Phi_dot", "psi", "psi_dot", "H", "rho_total")


def json_safe(value: Any) -> Any:
    """Recursively convert NumPy values and non-finite floats to strict JSON."""
    if isinstance(value, np.ndarray):
        return json_safe(value.tolist())
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_json_atomic(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(json_safe(payload), indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def finite_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def max_abs_finite(values: Any) -> float | None:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    return float(np.max(np.abs(finite))) if finite.size else None


def summarize_row(row: dict[str, Any], scenario: str,
                  params: Any) -> dict[str, Any]:
    ic = row.get("ic_params", {})
    psi_scale = finite_float(ic.get("psi_init"))
    velocity_scale = finite_float(ic.get("psi_dot_init"))
    offset = finite_float(ic.get("phi_offset"))
    seed_scale = psi_scale / params.psi_0 if psi_scale is not None else None
    velocity_scale = (
        velocity_scale / (params.mu * params.psi_0)
        if velocity_scale is not None else None
    )
    offset_scale = offset / params.Phi_c if offset is not None else None
    row_key = (
        f"{scenario}|seed={seed_scale:.12g}|velocity={velocity_scale:.12g}|"
        f"offset={offset_scale:.12g}"
        if None not in (seed_scale, velocity_scale, offset_scale)
        else None
    )

    result: dict[str, Any] = {
        "scenario": scenario,
        "row_key": row_key,
        "ic_params": ic,
        "initial_condition_scales": {
            "psi_seed_scale": seed_scale,
            "psi_velocity_scale": velocity_scale,
            "phi_offset_scale": offset_scale,
        },
        "success": bool(row.get("success", False)),
        "solver_method": SOLVER_METHOD,
    }
    if not result["success"]:
        result["error"] = row.get("error", "unspecified integration failure")
        result["solver_stats"] = row.get("solver_stats")
        return result

    classification = row.get("classification", {})
    result["solver_stats"] = row.get("solver_stats")
    result["final_state"] = {
        field: finite_float(row[field][-1])
        for field in FINAL_FIELDS
    }
    result["classification"] = {
        field: classification.get(field)
        for field in (
            "regime",
            "quartic_achieved",
            "Q_final",
            "w_final",
            "virial_final",
            "n_late_half_cycles",
            "n_oscillations",
            "adiabaticity_valid",
            "cycle_quadrature_relative_error_max",
        )
    }
    result["diagnostics"] = {
        "max_abs_relative_frw_continuity_residual":
            max_abs_finite(row["continuity_residual_relative"]),
        "max_abs_finite_difference_frw_residual_over_Hrho":
            max_abs_finite(
                row["continuity_residual_finite_difference_background_relative"]
            ),
    }
    return result


def run_refined_grid_scan(checkpoint_path: Path | None = None) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    scenario_metadata = []

    for scenario_name, params in build_scan_scenarios():
        psi_values, velocity_values, offset_values = build_initial_condition_grid(
            params, profile="full"
        )
        phi_dot_by_offset = {}
        for offset in offset_values:
            x_target = (params.Phi_c - offset) / M_PL
            state = state_at_field_value(
                params.lambda_phi, x_target, V0=params.V0
            )
            phi_dot_by_offset[offset] = float(state["Phi_dot"])

        scenario_metadata.append({
            "scenario": scenario_name,
            "V0_GeV4": params.V0,
            "Phi_c_over_Mpl": params.Phi_c / M_PL,
            "lambda_phi": params.lambda_phi,
            "m_psi_GeV": params.m_psi,
            "lambda_psi": params.lambda_psi,
            "E_th_GeV": params.E_th,
            "psi_seed_scales": [value / params.psi_0 for value in psi_values],
            "psi_velocity_scales": [
                value / (params.mu * params.psi_0) for value in velocity_values
            ],
            "phi_offset_scales": [
                value / params.Phi_c for value in offset_values
            ],
        })

        # Five seeds per batch keeps the trajectory arrays bounded in memory.
        for offset_index, offset in enumerate(offset_values):
            for velocity_index, velocity in enumerate(velocity_values):
                batch_label = (
                    f"{scenario_name}-offset{offset_index}-velocity{velocity_index}"
                )
                batch = run_parameter_scan(
                    params,
                    psi_values,
                    [velocity],
                    [offset],
                    t_max=T_MAX,
                    n_points=N_POINTS,
                    phi_dot_init_by_offset={offset: phi_dot_by_offset[offset]},
                    progress_interval=5,
                    progress_label=batch_label,
                    max_rhs_evaluations=MAX_RHS_EVALUATIONS,
                    rtol=RTOL,
                    atol=ATOL,
                    solver_method=SOLVER_METHOD,
                )
                for row in batch:
                    summary = summarize_row(row, scenario_name, params)
                    rows.append(summary)
                    if not summary["success"]:
                        failures.append({
                            "scenario": scenario_name,
                            "row_key": summary["row_key"],
                            "error": summary.get("error"),
                            "solver_stats": summary.get("solver_stats"),
                        })
                print(
                    f"[full-grid] {scenario_name}: "
                    f"{len([r for r in rows if r['scenario'] == scenario_name])}/50 "
                    "rows summarized",
                    flush=True,
                )
                del batch
                if checkpoint_path is not None:
                    checkpoint_payload = {
                        "schema_version": 1,
                        "checkpoint_complete": False,
                        "n_output_points": N_POINTS,
                        "expected_rows": EXPECTED_ROWS,
                        "row_count": len(rows),
                        "unique_row_keys": len({
                            item["row_key"] for item in rows
                        }),
                        "successful_rows": sum(bool(item["success"]) for item in rows),
                        "failed_rows": len(failures),
                        "scenario_metadata": scenario_metadata,
                        "rows": rows,
                        "failures": failures,
                    }
                    write_json_atomic(checkpoint_payload, checkpoint_path)

    row_keys = [row["row_key"] for row in rows]
    unique_row_keys = len(set(row_keys))
    return {
        "schema_version": 1,
        "purpose": "full 100-row homogeneous DOP853 output-grid refinement",
        "scan_profile": "full",
        "solver_method": SOLVER_METHOD,
        "rtol": RTOL,
        "atol": ATOL,
        "t_max_over_mu_inverse": T_MAX,
        "n_output_points": N_POINTS,
        "max_rhs_evaluations_per_trajectory": MAX_RHS_EVALUATIONS,
        "fuel_velocity_source": "integrated_single_field_FRW_trajectory",
        "quantum_vacuum_seeded": False,
        "scenario_metadata": scenario_metadata,
        "expected_rows": EXPECTED_ROWS,
        "row_count": len(rows),
        "unique_row_keys": unique_row_keys,
        "successful_rows": sum(bool(row["success"]) for row in rows),
        "failed_rows": len(failures),
        "rows": rows,
        "failures": failures,
        "interpretation": (
            "Refined output-grid artifact for row-by-row comparison with the "
            "4,001-point DOP853 baseline. This is not a coupled threshold-crossing "
            "or quantum-seeded inhomogeneous waterfall calculation."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="ptum_full_grid_convergence_256001.json",
        help="Strict-JSON output path",
    )
    parser.add_argument(
        "--checkpoint",
        default="ptum_full_grid_convergence_256001_checkpoint.json",
        help="Atomically save a strict-JSON checkpoint after each five-row batch",
    )
    args = parser.parse_args()

    output = Path(args.output)
    checkpoint = Path(args.checkpoint)
    payload = run_refined_grid_scan(checkpoint_path=checkpoint)
    payload["checkpoint_complete"] = True
    write_json_atomic(payload, output)
    write_json_atomic(payload, checkpoint)

    print(
        f"Refined full grid: {payload['successful_rows']}/{payload['row_count']} "
        f"successful, {payload['unique_row_keys']} unique rows; output={output}",
        flush=True,
    )
    if (
        payload["row_count"] != EXPECTED_ROWS
        or payload["unique_row_keys"] != EXPECTED_ROWS
        or payload["failed_rows"]
    ):
        raise RuntimeError(
            "Refined full-grid scan failed closed; inspect the saved JSON artifact"
        )


if __name__ == "__main__":
    main()
