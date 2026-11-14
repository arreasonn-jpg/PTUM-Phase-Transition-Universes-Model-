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


EXPECTED_INDICES = tuple(range(100))
EXPECTED_SCENARIOS = {
    "high_scale_threshold_matched",
    "low_scale_underdamped_control",
}
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
    """Load, validate and order the extended 0..99 trajectory summaries."""
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
        for key in (
            "max_abs_psi_over_trajectory",
            "final_Phi",
            "max_abs_chain_rule_background_relative_frw_continuity_residual",
            "max_abs_finite_difference_background_relative_frw_continuity_residual",
        ):
            if not _finite_number(row.get(key)):
                raise RuntimeError(f"trajectory {index}: {key} must be finite")
        # The dynamic-term chain-rule normalization can become ill-conditioned
        # when both terms approach zero. The background-normalized chain-rule
        # residual is the acceptance diagnostic; the independent finite-
        # difference residual is retained as a separate numerical cross-check.
        residual = float(
            row["max_abs_chain_rule_background_relative_frw_continuity_residual"]
        )
        if residual < 0 or residual > max_continuity_residual:
            raise RuntimeError(
                f"trajectory {index}: background-normalized chain-rule "
                f"continuity residual {residual:.3e} exceeds limit "
                f"{max_continuity_residual:.3e}"
            )
        exact_control = classification.get("exact_classical_invariant_control") is True
        if exact_control:
            if regime != "insufficient_oscillation_data":
                raise RuntimeError(
                    f"trajectory {index}: exact invariant control must have "
                    "insufficient_oscillation_data regime"
                )
            if classification.get("transient_quartic_episode_detected") is not False:
                raise RuntimeError(
                    f"trajectory {index}: exact invariant control cannot have a transient episode"
                )
        else:
            if regime == "insufficient_oscillation_data":
                raise RuntimeError(
                    f"trajectory {index}: insufficient oscillation data without an exact control"
                )
            for key in ("w_final", "Q_final", "virial_final"):
                if not _finite_number(classification.get(key)):
                    raise RuntimeError(
                        f"trajectory {index}: classification.{key} must be finite"
                    )
        if not isinstance(classification.get("transient_quartic_episode_detected"), bool):
            raise RuntimeError(f"trajectory {index}: missing transient episode diagnostic")
        if metadata.get("scenario") not in EXPECTED_SCENARIOS:
            raise RuntimeError(f"trajectory {index}: unexpected scenario {metadata.get('scenario')!r}")
        by_index[index] = row

    if set(by_index) != set(expected):
        missing = sorted(set(expected) - set(by_index))
        unexpected = sorted(set(by_index) - set(expected))
        raise RuntimeError(f"follow-up index mismatch; missing={missing}, unexpected={unexpected}")

    rows = [by_index[index] for index in expected]
    if set(expected) == set(EXPECTED_INDICES):
        scenario_counts = Counter(row["scan_metadata"]["scenario"] for row in rows)
        required_counts = Counter({
            "high_scale_threshold_matched": 50,
            "low_scale_underdamped_control": 50,
        })
        if scenario_counts != required_counts:
            raise RuntimeError(
                f"unexpected full-scan scenario distribution: {dict(scenario_counts)}"
            )
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
    chain_rule_relative = [
        float(row["max_abs_chain_rule_relative_frw_continuity_residual"])
        for row in rows
        if _finite_number(row.get("max_abs_chain_rule_relative_frw_continuity_residual"))
    ]
    chain_rule_background_relative = [
        float(row["max_abs_chain_rule_background_relative_frw_continuity_residual"])
        for row in rows
    ]
    finite_difference_absolute = [
        float(row["max_abs_finite_difference_frw_continuity_residual"])
        for row in rows
        if _finite_number(row.get("max_abs_finite_difference_frw_continuity_residual"))
    ]
    finite_difference_relative = [
        float(row["max_abs_finite_difference_relative_frw_continuity_residual"])
        for row in rows
        if _finite_number(row.get("max_abs_finite_difference_relative_frw_continuity_residual"))
    ]
    finite_difference_background_relative = [
        float(row["max_abs_finite_difference_background_relative_frw_continuity_residual"])
        for row in rows
    ]
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
            "latest_transient_episode_end_mu_inverse": max(
                (float(c.get("transient_quartic_last_episode_end_mu_inverse"))
                 for c in classifications
                 if _finite_number(c.get("transient_quartic_last_episode_end_mu_inverse"))),
                default=None
            ),
            "max_abs_chain_rule_relative_frw_continuity_residual": (
                max(chain_rule_relative) if chain_rule_relative else None
            ),
            "max_abs_chain_rule_background_relative_frw_continuity_residual": max(
                chain_rule_background_relative
            ),
            "max_abs_finite_difference_frw_continuity_residual": (
                max(finite_difference_absolute) if finite_difference_absolute else None
            ),
            "max_abs_finite_difference_relative_frw_continuity_residual": (
                max(finite_difference_relative) if finite_difference_relative else None
            ),
            "max_abs_finite_difference_background_relative_frw_continuity_residual": max(
                finite_difference_background_relative
            ),
            "median_abs_finite_difference_background_relative_frw_continuity_residual": (
                statistics.median(finite_difference_background_relative)
            ),
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
        f"- Validated trajectories: **{summary['validated_trajectories']} / {len(report['scan_definition']['expected_trajectory_indices'])}**",
        f"- Horizon: **{report['scan_definition']['horizon_mu_inverse']} mu^-1**",
        f"- Output points per trajectory: **{report['scan_definition']['output_points']}**",
        f"- Late-time quartic classifications: **{summary['late_time_quartic_count']}**",
        f"- Transient quartic-like episodes: **{summary['transient_quartic_episode_count']}**",
        f"- Transient episode indices: **{summary['transient_episode_indices']}**",
        f"- Maximum accepted chain-rule background-relative FRW residual: **{summary['max_abs_chain_rule_background_relative_frw_continuity_residual']:.3e}**",
        f"- Maximum chain-rule dynamic-relative FRW residual: **{summary['max_abs_chain_rule_relative_frw_continuity_residual']:.3e}**",
        f"- Maximum independent finite-difference background-relative FRW residual (diagnostic): **{summary['max_abs_finite_difference_background_relative_frw_continuity_residual']:.3e}**",
        "",
        "| Index | Offset (GeV) | Initial psi_dot (GeV^2) | Late regime | w_final | Q_final | Virial | H/omega max | Transient half-cycles | Duration (mu^-1) | Episode intervals (mu^-1) |",
        "|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in report["trajectories"]:
        c = row["classification"]
        ic = row["ic_params"]
        h_over_omega = c.get("H_over_omega_max")
        h_text = "n/a" if h_over_omega is None else f"{h_over_omega:.4g}"
        episode_text = "; ".join(
            f"{episode['start_mu_inverse']:.2f}-{episode['end_mu_inverse']:.2f}"
            for episode in c.get("transient_quartic_episodes", [])
        ) or "none"
        w_text = "n/a" if not _finite_number(c.get("w_final")) else f"{c['w_final']:.4f}"
        q_text = "n/a" if not _finite_number(c.get("Q_final")) else f"{c['Q_final']:.4f}"
        virial_text = "n/a" if not _finite_number(c.get("virial_final")) else f"{c['virial_final']:.4f}"
        lines.append(
            f"| {row['scan_metadata']['trajectory_index']} | {ic['phi_offset']:.4e} | "
            f"{ic['psi_dot_init']:.4e} | {c['regime']} | {w_text} | "
            f"{q_text} | {virial_text} | {h_text} | "
            f"{c.get('transient_quartic_max_consecutive_half_cycles', 0)} | "
            f"{c.get('transient_quartic_max_episode_duration_mu_inverse', 0.0):.3f} | "
            f"{episode_text} |"
        )
    lines += ["", report["interpretation"], ""]
    Path(output).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="extended-scan-results")
    parser.add_argument("--output-json", default="ptum_transient_followup_results.json")
    parser.add_argument("--output-markdown", default="ptum_transient_followup_report.md")
    parser.add_argument(
        "--max-continuity-residual", type=float, default=1.0e-8,
        help="maximum accepted chain-rule residual normalized to the total background",
    )
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
