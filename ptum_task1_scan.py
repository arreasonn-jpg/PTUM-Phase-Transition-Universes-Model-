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


def scan_profile_scales(profile: str = "full"):
    """Return the declared initial-condition grid for a named scan profile."""
    if profile == "full":
        return SEED_SCALES, VELOCITY_SCALES, PHI_OFFSETS
    if profile == "ci":
        # Two field seeds (exact invariant control + nonzero seed), one
        # velocity seed and one post-threshold offset per energy scale.
        return (0.0, 1.0), (0.0,), (0.1,)
    raise ValueError("profile must be 'ci' or 'full'")


def expected_scan_count(profile: str = "full") -> int:
    """Number of trajectories in both energy-scale scenarios."""
    seeds, velocities, offsets = scan_profile_scales(profile)
    return 2 * len(seeds) * len(velocities) * len(offsets)


def build_initial_condition_grid(params: PTUMParameters, profile: str = "full"):
    """Build either the full 5x5x2 grid or the four-trajectory CI smoke grid."""
    seed_scales, velocity_scales, phi_offsets = scan_profile_scales(profile)
    psi_init_range = [scale * params.psi_0 for scale in seed_scales]
    psi_dot_init_range = [
        scale * params.mu * params.psi_0 for scale in velocity_scales
    ]
    phi_offset_range = [scale * params.Phi_c for scale in phi_offsets]
    return psi_init_range, psi_dot_init_range, phi_offset_range


def run_scan_suite(*, t_max: float = DEFAULT_T_MAX,
                   n_points: int = DEFAULT_N_POINTS,
                   profile: str = "full"):
    """Run the selected scan profile at both high and low energy scales."""
    seed_scales, velocity_scales, phi_offsets = scan_profile_scales(profile)
    all_results = []
    for scenario_name, params in build_scan_scenarios():
        psi_init_range, psi_dot_init_range, phi_offset_range = (
            build_initial_condition_grid(params, profile=profile)
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
                "scan_profile": profile,
                "psi_seed_scales": list(seed_scales),
                "psi_velocity_scales": list(velocity_scales),
                "phi_offset_scales": list(phi_offsets),
                "fuel_velocity_source": "integrated_single_field_FRW_trajectory",
                "quantum_vacuum_seeded": False,
                "zero_seed_rows_are_exact_classical_invariant_controls": True,
            }
        all_results.extend(rows)
    return all_results


def validate_scan_results(results, expected_count: int | None = None):
    """Fail closed unless every trajectory in the selected profile succeeds."""
    expected = expected_scan_count() if expected_count is None else expected_count
    if expected < 1:
        raise ValueError("expected_count must be positive")
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
    parser.add_argument(
        "--profile", choices=("ci", "full"), default="full",
        help="Use four fast CI smoke trajectories or the full 100-trajectory scan",
    )
    args = parser.parse_args()

    results = run_scan_suite(
        t_max=args.t_max, n_points=args.n_points, profile=args.profile
    )
    # Persist the complete diagnostic summary before enforcing the CI gate,
    # so a failed run still leaves an inspectable artifact.
    save_results(results, args.output)
    validate_scan_results(results, expected_count=expected_scan_count(args.profile))

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

    print(f"Scan profile: {args.profile}")
    print(f"Total scan points: {len(results)}")
    print(f"Summary written to: {args.output}")


if __name__ == "__main__":
    main()
