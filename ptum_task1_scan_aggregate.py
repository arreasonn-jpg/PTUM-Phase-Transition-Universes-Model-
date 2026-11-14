#!/usr/bin/env python3
"""Validate and combine independently uploaded PTUM trajectory summaries."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="scan-results")
    parser.add_argument("--expected", type=int, default=100)
    parser.add_argument("--output", default="task1_parameter_scan_results.json")
    args = parser.parse_args()

    files = sorted(Path(args.input_dir).glob("trajectory_*_result.json"))
    rows = []
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list) or len(payload) != 1:
            raise RuntimeError(f"{path}: expected a one-row JSON list")
        rows.append(payload[0])

    indices = [row.get("scan_metadata", {}).get("trajectory_index") for row in rows]
    if len(rows) != args.expected:
        raise RuntimeError(
            f"Incomplete scan: expected {args.expected} uploaded trajectories, found {len(rows)}"
        )
    if sorted(indices) != list(range(args.expected)):
        raise RuntimeError("Missing, duplicate, or invalid trajectory indices")
    failures = [row for row in rows if row.get("success") is False or "error" in row]
    if failures:
        preview = [
            (r.get("scan_metadata", {}).get("trajectory_index"), r.get("error"))
            for r in failures[:10]
        ]
        raise RuntimeError(f"{len(failures)} trajectory failures: {preview}")

    rows.sort(key=lambda row: row["scan_metadata"]["trajectory_index"])
    Path(args.output).write_text(
        json.dumps(rows, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    regimes = Counter(
        row.get("classification", {}).get("regime", "missing") for row in rows
    )
    scenarios = Counter(
        row.get("scan_metadata", {}).get("scenario", "missing") for row in rows
    )
    print(f"Validated trajectories: {len(rows)}/{args.expected}")
    print(f"Scenarios: {dict(scenarios)}")
    print(f"Late-time regimes: {dict(regimes)}")
    print(f"Combined summary: {args.output}")


if __name__ == "__main__":
    main()
