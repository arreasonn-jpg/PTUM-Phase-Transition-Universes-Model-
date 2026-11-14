from ptum_task1_scan import expected_scan_count, expected_shard_count, shard_indices


def test_full_scan_shards_are_disjoint_and_cover_all_trajectories():
    total = expected_scan_count("full")
    shards = [shard_indices(total, 20, index) for index in range(20)]
    flattened = [item for shard in shards for item in shard]
    assert len(flattened) == total == 100
    assert len(set(flattened)) == total
    assert sorted(flattened) == list(range(total))
    assert all(len(shard) == 5 for shard in shards)


def test_ci_scan_shards_cover_four_trajectories():
    total = expected_scan_count("ci")
    shards = [shard_indices(total, 2, index) for index in range(2)]
    flattened = [item for shard in shards for item in shard]
    assert total == 4
    assert sorted(flattened) == list(range(total))
    assert sum(expected_shard_count("ci", 2, i) for i in range(2)) == total


def test_shard_indices_reject_invalid_arguments():
    import pytest
    with pytest.raises(ValueError):
        shard_indices(100, 0, 0)
    with pytest.raises(ValueError):
        shard_indices(100, 10, 10)


def test_successful_scan_summary_preserves_success_flag(tmp_path):
    import json
    import numpy as np
    from ptum_task1_simulation import save_results

    output = tmp_path / "scan.json"
    row = {
        "success": True,
        "classification": {"regime": "quartic", "quartic_achieved": True},
        "scan_metadata": {"global_trajectory_index": 7},
        "ic_params": {"psi_init": 1.0, "psi_dot_init": 0.0, "phi_offset": 0.1},
        "psi": np.array([0.0, 1.0]),
        "Phi": np.array([2.0, 1.9]),
        "continuity_residual_relative": np.array([0.0, 1e-8]),
    }

    save_results([row], str(output))

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload[0]["success"] is True
    assert payload[0]["scan_metadata"]["global_trajectory_index"] == 7
    assert not (tmp_path / "scan.json.tmp").exists()


def test_merger_accepts_serialized_successful_rows():
    from ptum_merge_scan_shards import validate_and_merge

    rows = [
        {
            "success": True,
            "scan_metadata": {"global_trajectory_index": index},
            "ic_params": {},
        }
        for index in [2, 0, 1]
    ]
    merged = validate_and_merge(rows, expected_count=3)
    assert [row["scan_metadata"]["global_trajectory_index"] for row in merged] == [0, 1, 2]


def test_stiff_scan_trajectory_73_is_solver_stable():
    import numpy as np
    from ptum_diagnose_trajectory import get_spec
    from ptum_task1_simulation import create_initial_conditions, run_simulation

    scenario, params, psi_init, psi_dot_init, phi_offset, phi_dot = get_spec(72)
    assert scenario == "low_scale_underdamped_control"
    initial = create_initial_conditions(
        params, psi_init, psi_dot_init, phi_offset,
        Phi_dot_override=phi_dot,
    )
    mu = np.sqrt(abs(params.mu_sq))
    t_span = (0.0, 20.0 / mu)
    t_eval = np.linspace(*t_span, 4001)

    radau = run_simulation(params, initial, t_span, t_eval, solver_method="Radau")
    bdf = run_simulation(params, initial, t_span, t_eval, solver_method="BDF")

    for result in (radau, bdf):
        assert result["success"] is True
        assert np.all(np.isfinite(result["rho_total"]))
        assert np.all(result["rho_total"] > 0.0)
        assert np.all(np.isfinite(result["continuity_residual_relative"]))

    for key in ("Phi", "Phi_dot", "psi", "psi_dot", "rho_total"):
        left = np.asarray(radau[key], dtype=float)
        right = np.asarray(bdf[key], dtype=float)
        scale = max(float(np.max(np.abs(left))), float(np.max(np.abs(right))), 1.0)
        relative_max_difference = float(np.max(np.abs(left - right)) / scale)
        assert relative_max_difference < 5.0e-5, (key, relative_max_difference)
