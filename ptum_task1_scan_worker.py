#!/usr/bin/env python3
"""Execute exactly one deterministic PTUM waterfall scan trajectory."""
from __future__ import annotations

import argparse
from pathlib import Path

from ptum_inflation_background import state_at_field_value
from ptum_task1_scan import (
    DEFAULT_N_POINTS,
    DEFAULT_T_MAX,
    build_initial_condition_grid,
    build_scan_scenarios,
    expected_scan_count,
    scan_profile_scales,
)
from ptum_task1_simulation import M_PL, run_parameter_scan, save_results


def trajectory_coordinates(index: int) -> tuple[int, int, int, int]:
    """Map a stable 0..99 index to scenario, seed, velocity and offset indices."""
    total = expected_scan_count("full")
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < total:
        raise ValueError(f"trajectory index must be an integer in [0, {total - 1}]")
    per_scenario = total // 2
    local = index % per_scenario
    return index // per_scenario, local // 10, (local % 10) // 2, local % 2


def run_one_trajectory(index: int, *, t_max: float = DEFAULT_T_MAX,
                       n_points: int = DEFAULT_N_POINTS) -> dict:
    scenario_index, seed_index, velocity_index, offset_index = trajectory_coordinates(index)
    scenario_name, params = build_scan_scenarios()[scenario_index]
    seeds, velocities, offsets = scan_profile_scales("full")
    psi_values, velocity_values, phi_values = build_initial_condition_grid(params, "full")
    offset = phi_values[offset_index]
    state = state_at_field_value(
        params.lambda_phi, (params.Phi_c - offset) / M_PL, V0=params.V0
    )
    metadata = {
        "trajectory_index": index,
        "scenario": scenario_name,
        "V0_GeV4": params.V0,
        "Phi_c_over_Mpl": params.Phi_c / M_PL,
        "exact_endpoint_damping_ratio": params.damping_ratio,
        "potential_only_endpoint_damping_ratio": params.damping_ratio_potential,
        "plateau_damping_ratio": params.damping_ratio_plateau,
        "t_max_over_mu_inverse": t_max,
        "n_output_points": n_points,
        "scan_profile": "full",
        "psi_seed_scales": list(seeds),
        "psi_velocity_scales": list(velocities),
        "phi_offset_scales": list(offsets),
        "phi_velocity_source": "integrated_single_field_FRW_trajectory",
        "quantum_vacuum_seeded": False,
        "zero_seed_rows_are_exact_classical_invariant_controls": True,
    }
    print(
        f"[worker] trajectory={index}/99 scenario={scenario_name} "
        f"seed={seed_index} velocity={velocity_index} offset={offset_index}",
        flush=True,
    )
    rows = run_parameter_scan(
        params,
        [psi_values[seed_index]],
        [velocity_values[velocity_index]],
        [offset],
        t_max=t_max,
        n_points=n_points,
        phi_dot_init_by_offset={offset: state["Phi_dot"]},
        progress_interval=1,
        progress_label=f"trajectory-{index:03d}",
    )
    row = rows[0]
    row["scan_metadata"] = metadata
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory-index", type=int, required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--t-max", type=float, default=DEFAULT_T_MAX)
    parser.add_argument("--n-points", type=int, default=DEFAULT_N_POINTS)
    args = parser.parse_args()
    row = run_one_trajectory(
        args.trajectory_index, t_max=args.t_max, n_points=args.n_points
    )
    output = args.output or f"trajectory_{args.trajectory_index:03d}_result.json"
    save_results([row], output)
    print(f"[worker] saved {Path(output)} success={row.get('success', False)}", flush=True)
    if not row.get("success", False):
        raise RuntimeError(
            f"Trajectory {args.trajectory_index} failed: {row.get('error', 'unknown error')}"
        )


if __name__ == "__main__":
    main()
