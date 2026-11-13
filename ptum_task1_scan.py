#!/usr/bin/env python3
"""Run matched high-scale and low-scale PTUM two-field diagnostic scans.

The high-scale scenario uses the threshold-matched inflationary benchmark.
The low-scale scenario is an underdamped control. Neither scan is a full
inhomogeneous cosmological evolution or a dark-matter relic calculation.
"""
from __future__ import annotations

import argparse
from collections import Counter

from ptum_task1_simulation import (
    M_PL,
    PTUMParameters,
    run_parameter_scan,
    save_results,
)


def build_scan_scenarios():
    """Return the threshold-matched high-scale benchmark and low-scale control."""
    common = dict(
        lambda_phi=0.02,
        Phi_c=1.387 * M_PL,
        m_psi=1.0e13,
        lambda_psi=0.1,
        E_th=1.0e16,
    )
    return [
        (
            "high_scale_threshold_matched",
            PTUMParameters(V0=1.0e64, **common),
        ),
        (
            "low_scale_underdamped_control",
            PTUMParameters(V0=1.0e56, **common),
        ),
    ]


def run_scan_suite(*, t_max: float = 20.0, n_points: int = 200):
    """Run the same 18 initial-condition combinations in both scenarios."""
    all_results = []
    for scenario_name, params in build_scan_scenarios():
        psi_init_range = [0.0, 0.01 * params.psi_0, 0.1 * params.psi_0]
        psi_dot_init_range = [
            0.0,
            0.1 * params.mu * params.psi_0,
            params.mu * params.psi_0,
        ]
        phi_offset_range = [0.01 * params.Phi_c, 0.1 * params.Phi_c]

        rows = run_parameter_scan(
            params,
            psi_init_range,
            psi_dot_init_range,
            phi_offset_range,
            t_max=t_max,
            n_points=n_points,
        )
        for row in rows:
            row["scan_metadata"] = {
                "scenario": scenario_name,
                "V0_GeV4": params.V0,
                "Phi_c_over_Mpl": params.Phi_c / M_PL,
                "local_damping_ratio": params.damping_ratio,
                "plateau_damping_ratio": params.damping_ratio_plateau,
            }
        all_results.extend(rows)
    return all_results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="task1_parameter_scan_results.json",
        help="Path for the compact strict-JSON summary",
    )
    parser.add_argument("--t-max", type=float, default=20.0)
    parser.add_argument("--n-points", type=int, default=200)
    args = parser.parse_args()

    results = run_scan_suite(t_max=args.t_max, n_points=args.n_points)
    save_results(results, args.output)

    for scenario_name, _params in build_scan_scenarios():
        scenario_rows = [
            row for row in results
            if row.get("scan_metadata", {}).get("scenario") == scenario_name
        ]
        successful = [row for row in scenario_rows if row.get("success")]
        regimes = Counter(
            row.get("classification", {}).get("regime", "missing")
            for row in successful
        )
        print(f"Scenario: {scenario_name}")
        print(f"  Scan points: {len(scenario_rows)}")
        print(f"  Successful integrations: {len(successful)}")
        print(f"  Failed integrations: {len(scenario_rows) - len(successful)}")
        print(f"  Late-time regimes: {dict(regimes)}")

    print(f"Total scan points: {len(results)}")
    print(f"Summary written to: {args.output}")


if __name__ == "__main__":
    main()
