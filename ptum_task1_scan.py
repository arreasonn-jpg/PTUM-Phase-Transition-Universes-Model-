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


def shard_indices(total: int, shard_count: int, shard_index: int) -> list[int]:
    """Return deterministic, disjoint trajectory indices for one shard."""
    if total < 1:
        raise ValueError("total must be positive")
    if shard_count < 1:
        raise ValueError("shard_count must be positive")
    if not 0 <= shard_index < shard_count:
        raise ValueError("shard_index must satisfy 0 <= index < shard_count")
    return list(range(shard_index, total, shard_count))


def expected_shard_count(profile: str, shard_count: int, shard_index: int) -> int:
    return len(shard_indices(expected_scan_count(profile), shard_count, shard_index))


def run_scan_suite(*, t_max: float = DEFAULT_T_MAX,
                   n_points: int = DEFAULT_N_POINTS,
                   profile: str = "full",
                   checkpoint_path: str | None = None,
                   shard_index: int = 0,
                   shard_count: int = 1):
    """Run a deterministic shard of the global scan, checkpointing each trajectory."""
    seed_scales, velocity_scales, phi_offsets = scan_profile_scales(profile)
    total = expected_scan_count(profile)
    selected_indices = set(shard_indices(total, shard_count, shard_index))
    all_results = []
    checkpoint_results = []

    # Build the same stable global ordering regardless of shard count.
    specs = []
    for scenario_name, params in build_scan_scenarios():
        psi_init_range, psi_dot_init_range, phi_offset_range = (
            build_initial_condition_grid(params, profile=profile)
        )
        phi_dot_init_by_offset = {}
        for offset in phi_offset_range:
            x_target = (params.Phi_c - offset) / M_PL
            state = state_at_field_value(params.lambda_phi, x_target, V0=params.V0)
            phi_dot_init_by_offset[offset] = state["Phi_dot"]
        for psi_init in psi_init_range:
            for psi_dot_init in psi_dot_init_range:
                for phi_offset in phi_offset_range:
                    specs.append({
                        "scenario": scenario_name,
                        "params": params,
                        "psi_init": psi_init,
                        "psi_dot_init": psi_dot_init,
                        "phi_offset": phi_offset,
                        "phi_dot_init": phi_dot_init_by_offset[phi_offset],
                    })

    if len(specs) != total:
        raise RuntimeError(f"Internal scan-grid mismatch: expected {total}, built {len(specs)}")

    for global_index, spec in enumerate(specs):
        if global_index not in selected_indices:
            continue
        scenario_name = spec["scenario"]
        params = spec["params"]
        ic_params = {
            "psi_init": spec["psi_init"],
            "psi_dot_init": spec["psi_dot_init"],
            "phi_offset": spec["phi_offset"],
        }
        metadata = {
            "scenario": scenario_name,
            "global_trajectory_index": global_index,
            "shard_index": shard_index,
            "shard_count": shard_count,
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

        def record_checkpoint(row, meta=metadata):
            row["scan_metadata"] = dict(meta)
            checkpoint_results.append(row)
            if checkpoint_path is not None:
                save_results(checkpoint_results, checkpoint_path)
            print(
                f"[scan] completed shard {shard_index + 1}/{shard_count}, "
                f"global trajectory {meta['global_trajectory_index'] + 1}/{total} "
                f"({meta['scenario']}): success={row.get('success')}",
                flush=True,
            )

        rows = run_parameter_scan(
            params,
            [spec["psi_init"]],
            [spec["psi_dot_init"]],
            [spec["phi_offset"]],
            t_max=t_max,
            n_points=n_points,
            phi_dot_init_by_offset={spec["phi_offset"]: spec["phi_dot_init"]},
            progress_interval=0,
            progress_label=f"{scenario_name}-trajectory-{global_index}",
            result_callback=record_checkpoint,
        )
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
    parser.add_argument(
        "--checkpoint", default=None,
        help="Atomically save a compact partial summary after each completed trajectory",
    )
    parser.add_argument("--shard-index", type=int, default=0, help="Zero-based scan shard index")
    parser.add_argument("--shard-count", type=int, default=1, help="Total number of deterministic scan shards")
    parser.add_argument("--t-max", type=float, default=DEFAULT_T_MAX)
    parser.add_argument("--n-points", type=int, default=DEFAULT_N_POINTS)
    parser.add_argument(
        "--profile", choices=("ci", "full"), default="full",
        help="Use four fast CI smoke trajectories or the full 100-trajectory scan",
    )
    args = parser.parse_args()

    results = run_scan_suite(
        t_max=args.t_max, n_points=args.n_points, profile=args.profile,
        checkpoint_path=args.checkpoint,
        shard_index=args.shard_index, shard_count=args.shard_count,
    )
    # Persist the complete diagnostic summary before enforcing the CI gate,
    # so a failed run still leaves an inspectable artifact.
    save_results(results, args.output)
    expected_here = expected_shard_count(args.profile, args.shard_count, args.shard_index)
    validate_scan_results(results, expected_count=expected_here)

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
    print(f"Shard: {args.shard_index + 1}/{args.shard_count}")
    print(f"Shard scan points: {len(results)}")
    print(f"Summary written to: {args.output}")


if __name__ == "__main__":
    main()
