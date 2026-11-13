#!/usr/bin/env python3
"""Run the reproducible 18-point homogeneous PTUM two-field scan.

The output is a compact summary of the current two-field truncation.
It is not a full cosmological or dark-matter relic-abundance result.
"""
from __future__ import annotations

import argparse
from collections import Counter

from ptum_task1_simulation import (
    PTUMParameters,
    run_parameter_scan,
    save_results,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="task1_parameter_scan_results.json",
        help="Path for the compact JSON summary",
    )
    args = parser.parse_args()

    params = PTUMParameters(
        V0=1.0e56,
        lambda_phi=0.02,
        m_psi=1.0e13,
        lambda_psi=0.1,
        E_th=1.0e16,
    )
    psi_init_range = [0.0, 0.01 * params.psi_0, 0.1 * params.psi_0]
    psi_dot_init_range = [
        0.0,
        0.1 * params.mu * params.psi_0,
        params.mu * params.psi_0,
    ]
    phi_offset_range = [0.01 * params.Phi_c, 0.1 * params.Phi_c]

    results = run_parameter_scan(
        params,
        psi_init_range,
        psi_dot_init_range,
        phi_offset_range,
        t_max=20.0,
        n_points=200,
    )
    save_results(results, args.output)

    successful = [row for row in results if row.get("success")]
    failed = len(results) - len(successful)
    regimes = Counter(
        row.get("classification", {}).get("regime", "missing")
        for row in successful
    )
    print(f"Scan points: {len(results)}")
    print(f"Successful integrations: {len(successful)}")
    print(f"Failed integrations: {failed}")
    print(f"Late-time regimes: {dict(regimes)}")
    print(f"Summary written to: {args.output}")


if __name__ == "__main__":
    main()
