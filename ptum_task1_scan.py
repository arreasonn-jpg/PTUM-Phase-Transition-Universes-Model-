#!/usr/bin/env python3
"""Run high-resolution PTUM waterfall scans at two energy scales.

These homogeneous post-threshold scans probe initial-condition sensitivity.
They are not a quantum-seeded inhomogeneous calculation or a relic-density
prediction.
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

SEED_SCALES = (0.0, 0.1, 1.0, 2.0, 5.0)
VELOCITY_SCALES = (0.0, 0.1, 1.0, 2.0, 5.0)
PHI_OFFSETS = (0.01, 0.1)
DEFAULT_T_MAX = 20.0
DEFAULT_N_POINTS = 4001


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


def build_initial_condition_grid(params: PTUMParameters):
    """Build a 5x5x2 grid in field seed, velocity seed and threshold offset."""
    psi_init_range = [scale * params.psi_0 for scale in SEED_SCALES]
    psi_dot_init_range = [
        scale * params.mu * params.psi_0 for scale in VELOCITY_SCALES
    ]
    phi_offset_range = [scale * params.Phi_c for scale in PHI_OFFSETS]
    return psi_init_range, psi_dot_init_range, phi_offset_range


def run_scan_suite(*, t_max: float = DEFAULT_T_MAX,
                   n_points: int = DEFAULT_N_POINTS):
    """Run 50 initial-condition combinations in each of the two scenarios."""
    all_results = []
    for scenario_name, params in build_scan_scenarios():
        psi_init_range, psi_dot_init_range, phi_offset_range = (
            build_initial_condition_grid(params)
        )
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
                "t_max_over_mu_inverse": t_max,
                "n_output_points": n_points,
                "psi_seed_scales": list(SEED_SCALES),
                "psi_velocity_scales": list(VELOCITY_SCALES),
                "phi_offset_scales": list(PHI_OFFSETS),
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
    parser.add_argument("--t-max", type=float, default=DEFAULT_T_MAX)
    parser.add_argument("--n-points", type=int, default=DEFAULT_N_POINTS)
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
