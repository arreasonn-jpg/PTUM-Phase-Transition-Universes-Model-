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
