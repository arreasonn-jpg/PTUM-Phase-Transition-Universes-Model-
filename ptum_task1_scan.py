#!/usr/bin/env python3
"""Run high-resolution PTUM waterfall scans at two energy scales.

These homogeneous post-threshold scans probe initial-condition sensitivity.
They are not a quantum-seeded inhomogeneous calculation or a relic-density
prediction.
"""
from __future__ import annotations

import argparse
from collections import Counter

from ptum_inflation_background import compute_observables, state_at_field_value
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
    inflation = compute_observables(0.02, n_target=60.0, n_star=55.0)
    phi_c_exact = inflation["x_end_hubble_flow"] * M_PL
    common = dict(
        lambda_phi=0.02,
        Phi_c=phi_c_exact,
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
        # Initialize Phi_dot from the same single-field FRW trajectory
        # that defines the exact epsilon_H=1 endpoint. Each post-threshold
        # offset is reached by integrating beyond that endpoint, rather than
        # assigning a potential-slow-roll velocity at the displaced field.
        phi_dot_init_by_offset = {}
        for offset in phi_offset_range:
            x_target = (params.Phi_c - offset) / M_PL
            state = state_at_field_value(
                params.lambda_phi, x_target, V0=params.V0
            )
            phi_dot_init_by_offset[offset] = state["Phi_dot"]

        print(
            f"[scan] starting {scenario_name}: {len(psi_init_range) * len(psi_dot_init_range) * len(phi_offset_range)} trajectories",
            flush=True,
        )
        rows = run_parameter_scan(
            params,
            psi_init_range,
            psi_dot_init_range,
            phi_offset_range,
            t_max=t_max,
            n_points=n_points,
            phi_dot_init_by_offset=phi_dot_init_by_offset,
            progress_interval=10,
            progress_label=scenario_name,
        )
        print(f"[scan] finished {scenario_name}", flush=True)
        for row in rows:
            row["scan_metadata"] = {
                "scenario": scenario_name,
                "V0_GeV4": params.V0,
                "Phi_c_over_Mpl": params.Phi_c / M_PL,
                "exact_endpoint_damping_ratio": params.damping_ratio,
                "potential_only_endpoint_damping_ratio": params.damping_ratio_potential,
                "plateau_damping_ratio": params.damping_ratio_plateau,
                "t_max_over_mu_inverse": t_max,
                "n_output_points": n_points,
                "psi_seed_scales": list(SEED_SCALES),
                "psi_velocity_scales": list(VELOCITY_SCALES),
                "phi_offset_scales": list(PHI_OFFSETS),
                "fuel_velocity_source": "integrated_single_field_FRW_trajectory",
                "quantum_vacuum_seeded": False,
                "zero_seed_rows_are_exact_classical_invariant_controls": True,
            }
        all_results.extend(rows)
    return all_results


def validate_scan_results(results):
    """Fail closed unless the complete two-scenario scan integrates successfully."""
    expected = 2 * len(SEED_SCALES) * len(VELOCITY_SCALES) * len(PHI_OFFSETS)
    if len(results) != expected:
        raise RuntimeError(
            f"Incomplete scan: expected {expected} trajectories, received {len(results)}"
        )
    failures = [
        (row.get("scan_metadata", {}).get("scenario", "unknown"),
         row.get("ic_params", {}), row.get("error", "unspecified failure"))
        for row in results if not row.get("success", False)
    ]
    if failures:
        preview = failures[:5]
        raise RuntimeError(
            f"{len(failures)} of {expected} scan integrations failed; "
            f"first failures: {preview}"
        )
    return expected


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
    # Persist the complete diagnostic summary before enforcing the CI gate,
    # so a failed run still leaves an inspectable artifact.
    save_results(results, args.output)
    validate_scan_results(results)

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
