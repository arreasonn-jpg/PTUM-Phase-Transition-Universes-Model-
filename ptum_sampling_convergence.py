#!/usr/bin/env python3
"""Isolate output-sampling convergence from ODE solver-tolerance convergence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from ptum_task1_scan_worker import run_one_trajectory


SAMPLE_COUNTS = (24001, 48001, 96001, 192001)
FIELDS = ("Phi", "Phi_dot", "psi", "psi_dot", "H", "Q", "virial_ratio")


def finite_residual_summary(values: np.ndarray) -> dict:
    values = np.asarray(values, dtype=float)
    finite = np.abs(values[np.isfinite(values)])
    if finite.size == 0:
        raise ValueError("finite-difference continuity residual has no finite samples")
    return {
        "finite_sample_count": int(finite.size),
        "max_abs_relative_residual": float(np.max(finite)),
        "p95_abs_relative_residual": float(np.percentile(finite, 95)),
        "rms_relative_residual": float(np.sqrt(np.mean(finite**2))),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indices", type=int, nargs="+", default=[94, 98])
    parser.add_argument("--t-max", type=float, default=480.0)
    parser.add_argument("--output", default="ptum_sampling_convergence_report.json")
    args = parser.parse_args()

    report = {
        "experiment": "output_sampling_density_convergence",
        "purpose": "Separate t_eval sampling effects from ODE tolerance and max-step effects.",
        "horizon_mu_inverse": args.t_max,
        "sample_counts": list(SAMPLE_COUNTS),
        "solver_settings": {"method": "DOP853", "rtol": 1e-9, "atol": 1e-12, "max_step": 0.05},
        "trajectories": [],
    }

    for index in args.indices:
        runs = {}
        for count in SAMPLE_COUNTS:
            print(f"[sampling] trajectory={index} output_points={count}", flush=True)
            row = run_one_trajectory(
                index, t_max=args.t_max, n_points=count,
                rtol=1e-9, atol=1e-12, max_step=0.05,
            )
            if not row.get("success", False):
                raise RuntimeError(f"trajectory {index} failed at {count} points: {row.get('error')}")
            runs[count] = row

        base_count = SAMPLE_COUNTS[0]
        base = runs[base_count]
        base_t = np.asarray(base["t"], dtype=float)
        comparisons = {}
        for count in SAMPLE_COUNTS:
            row = runs[count]
            t = np.asarray(row["t"], dtype=float)
            if count != base_count:
                intervals = count - 1
                base_intervals = base_count - 1
                if intervals % base_intervals != 0:
                    raise ValueError(
                        f"trajectory {index}: {count}-point grid cannot be compared "
                        f"on the {base_count}-point base grid"
                    )
                stride = intervals // base_intervals
                # run_one_trajectory returns physical t, while t_max is
                # specified in dimensionless mu*t units. Compare against the
                # actual base grid instead of assuming t_max is physical time.
                if not np.allclose(t[::stride], base_t, rtol=1e-12, atol=1e-14):
                    raise ValueError(
                        f"trajectory {index}: {count}-point grid does not nest "
                        "on the actual base time grid"
                    )
            residual = row.get("continuity_residual_finite_difference_relative")
            if residual is None:
                raise KeyError("missing continuity_residual_finite_difference_relative")
            comparisons[str(count)] = {
                "finite_difference_residual": finite_residual_summary(residual),
                "classification": row.get("classification", {}),
                "max_relative_difference_vs_coarsest_on_common_grid": {
                    field: float(
                        np.max(np.abs(np.asarray(row[field])[:: (count - 1) // (base_count - 1)]
                                       - np.asarray(base[field])))
                        / max(float(np.max(np.abs(np.asarray(base[field])))), np.finfo(float).tiny)
                    )
                    for field in FIELDS
                },
            }
        report["trajectories"].append({
            "trajectory_index": index,
            "comparisons": comparisons,
        })

    Path(args.output).write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    print(f"[sampling] wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
