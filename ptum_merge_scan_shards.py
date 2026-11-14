#!/usr/bin/env python3
"""Validate and merge independently checkpointed PTUM scan-shard summaries."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def load_rows(input_dir: Path) -> list[dict]:
    rows: list[dict] = []
    files = sorted(input_dir.glob("task1_parameter_scan_shard_*.json"))
    if not files:
        raise RuntimeError(f"No shard summaries found in {input_dir}")
    for path in files:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, list):
            raise RuntimeError(f"{path} must contain a JSON list")
        rows.extend(payload)
    return rows


def validate_and_merge(rows: list[dict], expected_count: int) -> list[dict]:
    if expected_count < 1:
        raise ValueError("expected_count must be positive")
    indices = []
    for row in rows:
        metadata = row.get("scan_metadata", {})
        index = metadata.get("global_trajectory_index")
        if not isinstance(index, int):
            raise RuntimeError("A shard row is missing integer global_trajectory_index")
        indices.append(index)
        if row.get("success") is not True:
            raise RuntimeError(
                f"Trajectory {index} is missing or unsuccessful: {row.get('error', 'no error detail')}"
            )
    if len(rows) != expected_count:
        raise RuntimeError(
            f"Incomplete merged scan: expected {expected_count} rows, received {len(rows)}"
        )
    if len(set(indices)) != expected_count:
        raise RuntimeError("Duplicate global trajectory indices detected")
    expected = set(range(expected_count))
    actual = set(indices)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise RuntimeError(f"Trajectory index coverage mismatch; missing={missing}, extra={extra}")
    return sorted(rows, key=lambda row: row["scan_metadata"]["global_trajectory_index"])


def atomic_write(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=100)
    args = parser.parse_args()
    rows = validate_and_merge(load_rows(args.input_dir), args.expected_count)
    atomic_write(rows, args.output)
    print(f"Validated and merged {len(rows)}/{args.expected_count} successful trajectories.")


if __name__ == "__main__":
    main()
