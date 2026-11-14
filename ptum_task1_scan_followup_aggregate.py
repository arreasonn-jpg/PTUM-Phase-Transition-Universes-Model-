#!/usr/bin/env python3
"""Validate and summarize the targeted long-horizon PTUM transient follow-up."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable


EXPECTED_INDICES = tuple(range(90, 100))
EXPECTED_SCENARIO = "low_scale_underdamped_control"
ALLOWED_REGIMES = {
    "quartic", "quadratic_candidate", "non_quartic",
    "insufficient_oscillation_data", "failed",
}


def _finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def load_followup_rows(
    input_dir: str | Path,
    expected_indices: Iterable[int] = EXPECTED_INDICES,
    max_continuity_residual: float = 1.0e-8,
) -> list[dict]:
    """Load, validate and order the extended 90..99 trajectory summaries."""
    expected = tuple(expected_indices)
    if not expected or len(set(expected)) != len(expected):
        raise ValueError("expected_indices must be a non-empty sequence of unique indices")
    if not _finite_number(max_continuity_residual) or max_continuity_residual <= 0:
        raise ValueError("max_continuity_residual must be finite and positive")

    files = sorted(Path(input_dir).glob("extended_trajectory_*_result.json"))
    by_index: dict[int, dict] = {}
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list) or len(payload) != 1:
            raise RuntimeError(f"{path}: expected a one-row JSON list")
        row = payload[0]
        metadata = row.get("scan_metadata", {})
        index = metadata.get("trajectory_index")
        if isinstance(index, bool) or not isinstance(index, int):
            raise RuntimeError(f"{path}: missing integer trajectory_index")
        if index in by_index:
            raise RuntimeError(f"duplicate trajectory index {index}")
        if path.stem != f"extended_trajectory_{index}_result":
            raise RuntimeError(f"{path}: filename/index mismatch for trajectory {index}")
        if row.get("success") is False or "error" in row:
            raise RuntimeError(f"trajectory {index} failed: {row.get('error', 'unknown error')}")
        classification = row.get("classification")
        if not isinstance(classification, dict):
            raise RuntimeError(f"trajectory {index}: missing classification")
        regime = classification.get("regime")
        if regime not in ALLOWED_REGIMES or regime == "failed":
            raise RuntimeError(f"trajectory {index}: invalid regime {regime!r}")
        if not isinstance(classification.get("quartic_achieved"), bool):
            raise RuntimeError(f"trajectory {index}: missing quartic_achieved boolean")
        for key in ("max_abs_psi_over_trajectory", "final_Phi",
                    "max_abs_relative_frw_continuity_residual"):
            if not _finite_number(row.get(key)):
                raise RuntimeError(f"trajectory {index}: {key} must be finite")
        residual = float(row["max_abs_relative_frw_continuity_residual"])
        if residual < 0 or residual > max_continuity_residual:
            raise RuntimeError(
                f"trajectory {index}: continuity residual {residual:.3e} "
                f"exceeds limit {max_continuity_residual:.3e}"
            )
        for key in ("w_final", "Q_final", "virial_final"):
            if not _finite_number(classification.get(key)):
                raise RuntimeError(f"trajectory {index}: classification.{key} must be finite")
        if not isinstance(classification.get("transient_quartic_episode_detected"), bool):
            raise RuntimeError(f"trajectory {index}: missing transient episode diagnostic")
        if metadata.get("scenario") != EXPECTED_SCENARIO:
            raise RuntimeError(f"trajectory {index}: unexpected scenario {metadata.get('scenario')!r}")
        by_index[index] = row

    if set(by_index) != set(expected):
        missing = sorted(set(expected) - set(by_index))
        unexpected = sorted(set(by_index) - set(expected))
        raise RuntimeError(f"follow-up index mismatch; missing={missing}, unexpected={unexpected}")

    rows = [by_index[index] for index in expected]
    horizons = {row["scan_metadata"].get("t_max_over_mu_inverse") for row in rows}
    resolutions = {row["scan_metadata"].get("n_output_points") for row in rows}
    if len(horizons) != 1 or not all(_finite_number(x) for x in horizons):
        raise RuntimeError(f"inconsistent or invalid follow-up horizons: {horizons}")
    if len(resolutions) != 1 or not all(isinstance(x, int) and x > 1 for x in resolutions):
        raise RuntimeError(f"inconsistent or invalid output resolutions: {resolutions}")
    if next(iter(horizons)) < 120.0:
        raise RuntimeError("follow-up horizon is shorter than the required 120 mu^-1")
    if next(iter(resolutions)) < 24001:
        raise RuntimeError("follow-up output resolution is below 24001 points")
    return rows


def build_followup_report(rows: list[dict]) -> dict:
    regimes = Counter(row["classification"]["regime"] for row in rows)
    scenarios = Counter(row["scan_metadata"]["scenario"] for row in rows)
    residuals = [float(row["max_abs_relative_frw_continuity_residual"]) for row in rows]
    transient_rows = [
        row for row in rows
        if row["classification"]["transient_quartic_episode_detected"]
    ]
    classifications = [row["classification"] for row in rows]
    return {
        "scan_definition": {
            "expected_trajectory_indices": [row["scan_metadata"]["trajectory_index"] for row in rows],
            "scenario_counts": dict(scenarios),
            "horizon_mu_inverse": rows[0]["scan_metadata"]["t_max_over_mu_inverse"],
            "output_points": rows[0]["scan_metadata"]["n_output_points"],
            "quantum_vacuum_seeded": False,
        },
        "summary": {
            "validated_trajectories": len(rows),
            "late_time_regime_counts": dict(regimes),
            "late_time_quartic_count": sum(c["regime"] == "quartic" for c in classifications),
            "transient_quartic_episode_count": len(transient_rows),
            "transient_episode_indices": [
                row["scan_metadata"]["trajectory_index"] for row in transient_rows
            ],
            "max_transient_candidate_half_cycles": max(
                (int(c.get("transient_quartic_max_consecutive_half_cycles", 0))
                 for c in classifications), default=0
            ),
            "max_transient_episode_duration_mu_inverse": max(
                (float(c.get("transient_quartic_max_episode_duration_mu_inverse", 0.0))
                 for c in classifications), default=0.0
            ),
            "max_abs_relative_frw_continuity_residual": max(residuals),
            "median_abs_relative_frw_continuity_residual": statistics.median(residuals),
        },
        "trajectories": rows,
        "interpretation": (
            "A transient quartic-like episode is not evidence of a late-time quartic regime "
            "or an attractor. The late-time classification is reported independently."
        ),
    }


def write_markdown_report(report: dict, output: str | Path) -> None:
    summary = report["summary"]
    lines = [
        "# PTUM long-horizon transient-quartic follow-up",
        "",
        f"- Validated trajectories: **{summary['validated_trajectories']} / 10**",
        f"- Horizon: **{report['scan_definition']['horizon_mu_inverse']} mu^-1**",
        f"- Output points per trajectory: **{report['scan_definition']['output_points']}**",
        f"- Late-time quartic classifications: **{summary['late_time_quartic_count']}**",
        f"- Transient quartic-like episodes: **{summary['transient_quartic_episode_count']}**",
        f"- Transient episode indices: **{summary['transient_episode_indices']}**",
        f"- Maximum relative FRW continuity residual: **{summary['max_abs_relative_frw_continuity_residual']:.3e}**",
        "",
        "| Index | Offset (GeV) | Initial psi_dot (GeV^2) | Late regime | w_final | Q_final | Virial | H/omega max | Transient half-cycles | Duration (mu^-1) |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["trajectories"]:
        c = row["classification"]
        ic = row["ic_params"]
        h_over_omega = c.get("H_over_omega_max")
        h_text = "n/a" if h_over_omega is None else f"{h_over_omega:.4g}"
        lines.append(
            f"| {row['scan_metadata']['trajectory_index']} | {ic['phi_offset']:.4e} | "
            f"{ic['psi_dot_init']:.4e} | {c['regime']} | {c['w_final']:.4f} | "
            f"{c['Q_final']:.4f} | {c['virial_final']:.4f} | {h_text} | "
            f"{c.get('transient_quartic_max_consecutive_half_cycles', 0)} | "
            f"{c.get('transient_quartic_max_episode_duration_mu_inverse', 0.0):.3f} |"
        )
    lines += ["", report["interpretation"], ""]
    Path(output).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="extended-scan-results")
    parser.add_argument("--output-json", default="ptum_transient_followup_results.json")
    parser.add_argument("--output-markdown", default="ptum_transient_followup_report.md")
    parser.add_argument("--max-continuity-residual", type=float, default=1.0e-8)
    args = parser.parse_args()
    rows = load_followup_rows(
        args.input_dir, max_continuity_residual=args.max_continuity_residual
    )
    report = build_followup_report(rows)
    Path(args.output_json).write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    write_markdown_report(report, args.output_markdown)
    print(json.dumps(report["summary"], indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
