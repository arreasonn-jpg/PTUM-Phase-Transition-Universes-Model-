#!/usr/bin/env python3
"""Reproducible 18-point homogeneous Phi-psi benchmark scan."""
import argparse
import json
from pathlib import Path

import numpy as np

from ptum_task1_simulation import (
    PTUMParameters,
    run_parameter_scan,
    save_results,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="ptum_phi_psi_18_point_results.json")
    parser.add_argument("--t-max-mu", type=float, default=3500.0)
    parser.add_argument("--n-points", type=int, default=8000)
    args = parser.parse_args()

    params = PTUMParameters(
        V0=1e56,
        lambda_phi=0.02,
        m_psi=1e13,
        lambda_psi=0.1,
        E_th=1e16,
    )
    psi_init = [0.0, 0.01 * params.psi_0, 0.1 * params.psi_0]
    psi_dot_init = [0.0, 0.1 * params.mu * params.psi_0,
                    params.mu * params.psi_0]
    phi_offset = [0.01 * params.Phi_c, 0.1 * params.Phi_c]

    results = run_parameter_scan(
        params, psi_init, psi_dot_init, phi_offset,
        t_max=args.t_max_mu, n_points=args.n_points,
    )
    if len(results) != 18:
        raise RuntimeError(f"Expected 18 trajectories, received {len(results)}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_results(results, str(output))

    summary = []
    for index, result in enumerate(results):
        if not result["success"]:
            summary.append({
                "index": index,
                "success": False,
                "error": result.get("error", "unknown"),
                "ic_params": result["ic_params"],
            })
            continue
        c = result["classification"]
        summary.append({
            "index": index,
            "success": True,
            "regime": c["regime"],
            "quartic_achieved": c["quartic_achieved"],
            "n_full_cycles": c["n_full_cycles"],
            "w_final": c["w_final"],
            "Q_final": c["Q_final"],
            "virial_final": c["virial_final"],
            "omega_over_H_final": c["omega_over_H_final"],
            "tachyonic_duration": result["tachyonic_duration"],
            "tachyonic_fraction": result["tachyonic_fraction"],
            "threshold_crossings": result["threshold_crossings"],
            "max_relative_continuity_residual":
                result["max_relative_continuity_residual"],
            "max_abs_psi": result["max_abs_psi"],
            "max_abs_Phi_over_Phi_c": result["max_abs_Phi_over_Phi_c"],
            "seedless_invariant": result["seedless_invariant"],
            "ic_params": result["ic_params"],
        })

    summary_path = output.with_name(output.stem + "_summary.json")
    def json_safe(value):
        if isinstance(value, (np.floating, float)):
            number = float(value)
            return number if np.isfinite(number) else None
        if isinstance(value, np.generic):
            return json_safe(value.item())
        if isinstance(value, dict):
            return {str(key): json_safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [json_safe(item) for item in value]
        return value

    summary_path.write_text(
        json.dumps(json_safe(summary), indent=2, allow_nan=False), encoding="utf-8"
    )
    successful = sum(bool(item["success"]) for item in summary)
    quartic = sum(
        bool(item.get("quartic_achieved", False))
        for item in summary if item["success"]
    )
    print(json.dumps({
        "trajectories": len(summary),
        "successful_integrations": successful,
        "failed_integrations": len(summary) - successful,
        "quartic_achieved": quartic,
        "results": str(output),
        "summary": str(summary_path),
    }, indent=2))


if __name__ == "__main__":
    main()
