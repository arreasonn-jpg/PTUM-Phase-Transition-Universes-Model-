#!/usr/bin/env python3
"""Run solver-tolerance and maximum-step convergence checks for PTUM trajectories."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from ptum_task1_scan_worker import run_one_trajectory


CASES = {
    "reference": {"rtol": 1.0e-9, "atol": 1.0e-12, "max_step": 0.05},
    "tight_tolerance": {"rtol": 1.0e-11, "atol": 1.0e-14, "max_step": 0.05},
    "half_max_step": {"rtol": 1.0e-9, "atol": 1.0e-12, "max_step": 0.025},
    "tight_and_half_step": {"rtol": 1.0e-11, "atol": 1.0e-14, "max_step": 0.025},
}
FIELDS = ("Phi", "Phi_dot", "psi", "psi_dot", "H", "w_psi", "Q", "virial_ratio")


def relative_max_difference(reference: np.ndarray, candidate: np.ndarray) -> float:
    a = np.asarray(reference, dtype=float)
    b = np.asarray(candidate, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"trajectory array shape mismatch: {a.shape} != {b.shape}")
    finite = np.isfinite(a) & np.isfinite(b)
    if not np.any(finite):
        return 0.0 if np.array_equal(np.isnan(a), np.isnan(b)) else float("inf")
    scale = max(float(np.max(np.abs(a[finite]))), np.finfo(float).tiny)
    return float(np.max(np.abs(a[finite] - b[finite])) / scale)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indices", type=int, nargs="+", default=[90, 94, 98])
    parser.add_argument("--t-max", type=float, default=480.0)
    parser.add_argument("--n-points", type=int, default=96001)
    parser.add_argument("--output", default="ptum_solver_convergence_report.json")
    args = parser.parse_args()

    report = {
        "experiment": "solver_tolerance_and_max_step_convergence",
        "horizon_mu_inverse": args.t_max,
        "output_points": args.n_points,
        "trajectory_indices": args.indices,
        "comparison_normalization": "max_abs_difference / max_abs_reference_field",
        "cases": CASES,
        "trajectories": [],
    }
    for index in args.indices:
        runs = {}
        for label, settings in CASES.items():
            print(f"[convergence] trajectory={index} case={label} settings={settings}", flush=True)
            row = run_one_trajectory(
                index, t_max=args.t_max, n_points=args.n_points, **settings
            )
            if not row.get("success", False):
                raise RuntimeError(f"trajectory {index} failed in {label}: {row.get('error')}")
            runs[label] = row

        reference = runs["reference"]
        entry = {
            "trajectory_index": index,
            "reference_classification": reference.get("classification", {}),
            "comparisons": {},
        }
        reference_t = np.asarray(reference["t"], dtype=float)
        for label, candidate in runs.items():
            candidate_t = np.asarray(candidate["t"], dtype=float)
            if not np.array_equal(reference_t, candidate_t):
                raise ValueError(
                    f"trajectory {index} {label}: output time grids differ; "
                    "interpolate explicitly before comparing"
                )
            entry["comparisons"][label] = {
                "solver_settings": candidate.get("solver_settings"),
                "classification": candidate.get("classification", {}),
                "max_relative_field_differences": {
                    field: relative_max_difference(reference[field], candidate[field])
                    for field in FIELDS
                },
                "max_abs_relative_frw_chain_rule_residual": float(
                    np.nanmax(np.abs(candidate["continuity_residual_background_relative"]))
                ),
            }
        report["trajectories"].append(entry)

    Path(args.output).write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    print(f"[convergence] wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
