#!/usr/bin/env python3
"""Quantify the finite-cutoff stress carried by bare adiabatic-WKB samples.

This module deliberately does not subtract the zero-point energy or claim a
renormalized quantum state. It evaluates the Gaussian ensemble expectation of
the same finite-lattice stress tensor used by the classical waterfall solver.
The result is a diagnostic of UV-cutoff dependence and of the test-field
Friedmann mismatch, not a physical prediction.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np

from ptum_lattice_waterfall import sample_adiabatic_vacuum_initial_conditions
from ptum_task1_simulation import M_PL, PTUMParameters, veff_phi


def compute_bare_wkb_stress_expectation(
    params: PTUMParameters,
    sample: dict[str, object],
) -> dict[str, float | int | bool | str]:
    """Return the equal-time Gaussian expectation of the bare lattice stress.

    With s=psi/psi_0, v=ds/dtau, eta=m_eff^2/mu^2 and the stated Fourier
    convention, P_k=lambda_psi/(2 Omega_k) and R_k=lambda_psi Omega_k/2
    are the field and residual-velocity powers. The WKB velocity shift is
    nu_k=-(Omega'_k/Omega_k+3h)/2. The Gaussian Wick estimate
    <s^4>=3 <s^2>^2 is included because the nonlinear lattice Hamiltonian
    contains s^4/4. No subtraction or counterterm is applied.
    """
    if not isinstance(sample, dict):
        raise ValueError("sample must be the dictionary returned by the WKB sampler")
    metadata = sample.get("metadata")
    diagnostics = sample.get("diagnostics")
    if not isinstance(metadata, dict) or not isinstance(diagnostics, dict):
        raise ValueError("sample is missing WKB metadata or diagnostics")
    if metadata.get("kind") != "bare_first_order_adiabatic_wkb_gaussian_classical_sample":
        raise ValueError("unsupported WKB sample kind")
    if metadata.get("vacuum_renormalized") is not False or (
        metadata.get("vacuum_subtraction_applied") is not False
    ) or metadata.get("zero_point_energy_retained") is not True:
        raise ValueError("the audit accepts only explicitly bare, unsubtracted WKB samples")

    shape = tuple(int(value) for value in metadata.get("grid_shape", ()))
    if len(shape) != 3 or len(set(shape)) != 1 or shape[0] < 4:
        raise ValueError("WKB metadata has an invalid cubic grid shape")
    omega = np.asarray(diagnostics.get("mode_frequency_over_mu"), dtype=float)
    k_squared = np.asarray(diagnostics.get("lattice_k_squared_over_mu2"), dtype=float)
    if omega.shape != shape or k_squared.shape != shape:
        raise ValueError("mode arrays do not match the WKB grid")
    if (not np.all(np.isfinite(omega)) or np.any(omega <= 0.0)
            or not np.all(np.isfinite(k_squared)) or np.any(k_squared < 0.0)):
        raise ValueError("mode frequencies and lattice momenta must be finite and physical")

    box = float(metadata.get("box_size_over_mu", np.nan))
    eta = float(metadata.get("m_eff_squared_over_mu2", np.nan))
    velocity_shift = float(diagnostics.get("velocity_shift", np.nan))
    mu = float(params.mu)
    psi0 = float(params.psi_0)
    lam = float(params.lambda_psi)
    if (not np.isfinite(box) or box <= 0.0 or not np.isfinite(eta) or eta <= 0.0
            or not np.isfinite(velocity_shift) or mu <= 0.0 or psi0 <= 0.0
            or lam <= 0.0):
        raise ValueError("WKB background and PTUM scales must be finite and positive")

    volume = box**3
    field_power = lam / (2.0 * omega)
    residual_velocity_power = lam * omega / 2.0
    field_variance = float(np.sum(field_power) / volume)
    velocity_variance = float(np.sum(
        residual_velocity_power + velocity_shift**2 * field_power
    ) / volume)
    gradient_variance = float(np.sum(k_squared * field_power) / volume)

    rho_quadratic_norm = 0.5 * (
        velocity_variance + gradient_variance + eta * field_variance
    )
    rho_quartic_wick_norm = 0.75 * field_variance**2
    pressure_quadratic_norm = (
        0.5 * velocity_variance
        - gradient_variance / 6.0
        - 0.5 * eta * field_variance
    )
    pressure_quartic_wick_norm = -rho_quartic_wick_norm
    rho_psi_norm = rho_quadratic_norm + rho_quartic_wick_norm
    pressure_psi_norm = pressure_quadratic_norm + pressure_quartic_wick_norm

    rho_scale = mu**2 * psi0**2
    rho_psi = rho_scale * rho_psi_norm
    pressure_psi = rho_scale * pressure_psi_norm
    phi = float(metadata.get("Phi_initial_GeV", np.nan))
    phi_dot = float(metadata.get("Phi_dot_initial_GeV2", np.nan))
    rho_phi = 0.5 * phi_dot**2 + float(veff_phi(phi, params))
    rho_total_bare = rho_phi + rho_psi
    if (not np.isfinite(rho_total_bare) or rho_total_bare <= 0.0
            or not np.isfinite(rho_psi) or rho_psi < 0.0):
        raise FloatingPointError("bare WKB stress produced a non-positive or non-finite energy")

    h_background = float(metadata.get("H_background_over_mu", np.nan))
    h_prime_background = float(metadata.get("H_prime_over_mu2", np.nan))
    if not np.isfinite(h_background) or h_background <= 0.0:
        raise ValueError("the sampler background Hubble rate must be positive")
    h_bare = float(np.sqrt(rho_total_bare / (3.0 * M_PL**2)) / mu)
    h_prime_bare = float(
        -(phi_dot**2 + rho_scale * (velocity_variance + gradient_variance / 3.0))
        / (2.0 * M_PL**2 * mu**2)
    )
    tiny = np.finfo(float).tiny
    dx = box / shape[0]
    k_cutoff = float(np.sqrt(np.max(k_squared)))

    return {
        "grid_size": int(shape[0]),
        "mode_count": int(np.prod(shape)),
        "box_size_over_mu": box,
        "dx_over_mu_inverse": dx,
        "lattice_k_cutoff_over_mu": k_cutoff,
        "mean_s_squared": field_variance,
        "mean_s_prime_squared": velocity_variance,
        "mean_lattice_gradient_squared": gradient_variance,
        "rho_psi_quadratic_over_rho_scale": rho_quadratic_norm,
        "rho_psi_quartic_wick_over_rho_scale": rho_quartic_wick_norm,
        "rho_psi_bare_over_rho_scale": rho_psi_norm,
        "pressure_psi_bare_over_rho_scale": pressure_psi_norm,
        "rho_psi_bare_GeV4": rho_psi,
        "pressure_psi_bare_GeV4": pressure_psi,
        "rho_phi_GeV4": rho_phi,
        "rho_total_bare_GeV4": rho_total_bare,
        "rho_psi_to_rho_phi": rho_psi / rho_phi,
        "H_background_over_mu": h_background,
        "H_bare_total_over_mu": h_bare,
        "H_relative_mismatch": (h_bare - h_background) / h_background,
        "H_prime_background_over_mu2": h_prime_background,
        "H_prime_bare_total_over_mu2": h_prime_bare,
        "H_prime_relative_mismatch": (
            (h_prime_bare - h_prime_background)
            / max(abs(h_prime_background), tiny)
        ),
        "zero_point_energy_retained": True,
        "vacuum_subtraction_applied": False,
        "counterterms_applied": False,
        "vacuum_renormalized": False,
        "continuum_limit_claimed": False,
    }


def build_bare_wkb_cutoff_audit(
    params: PTUMParameters,
    *,
    grid_sizes: Iterable[int] = (4, 6, 8, 10),
    box_size_over_mu: float = 8.0,
    Phi_initial: float | None = None,
    Phi_dot_initial: float | None = None,
    seed: int = 20261121,
    adiabaticity_tolerance: float = 0.1,
) -> dict[str, object]:
    """Build a fixed-box cutoff sequence; every row is a bare diagnostic."""
    sizes = list(grid_sizes)
    if len(sizes) < 2:
        raise ValueError("at least two grid sizes are required for a cutoff audit")
    if any(isinstance(n, (bool, np.bool_)) or int(n) != n or n < 4 for n in sizes):
        raise ValueError("grid sizes must be integers >= 4")
    sizes = [int(n) for n in sizes]
    if sizes != sorted(set(sizes)):
        raise ValueError("grid sizes must be unique and strictly increasing")
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)):
        raise ValueError("seed must be an integer")
    box = float(box_size_over_mu)
    if not np.isfinite(box) or box <= 0.0:
        raise ValueError("box_size_over_mu must be finite and positive")

    phi = 1.2 * params.Phi_c if Phi_initial is None else float(Phi_initial)
    phi_dot = (
        -1.0e-4 * params.mu * params.Phi_c
        if Phi_dot_initial is None else float(Phi_dot_initial)
    )
    rows: list[dict[str, float | int | bool | str]] = []
    for n in sizes:
        sample = sample_adiabatic_vacuum_initial_conditions(
            params,
            grid_size=n,
            box_size_over_mu=box,
            Phi_initial=phi,
            Phi_dot_initial=phi_dot,
            seed=int(seed),
            adiabaticity_tolerance=adiabaticity_tolerance,
        )
        rows.append(compute_bare_wkb_stress_expectation(params, sample))

    cutoffs = [float(row["lattice_k_cutoff_over_mu"]) for row in rows]
    energies = [float(row["rho_psi_bare_GeV4"]) for row in rows]
    cutoff_monotonic = all(b > a for a, b in zip(cutoffs, cutoffs[1:]))
    energy_monotonic = all(b > a for a, b in zip(energies, energies[1:]))
    log_slope = float(
        np.log(energies[-1] / energies[0]) / np.log(cutoffs[-1] / cutoffs[0])
    )
    return {
        "schema": "ptum.bare_wkb_lattice_cutoff_audit",
        "schema_version": 1,
        "method": "finite_volume_gaussian_mode_sum_with_gaussian_wick_quartic",
        "inputs": {
            "V0_GeV4": float(params.V0),
            "Phi_initial_GeV": phi,
            "Phi_dot_initial_GeV2": phi_dot,
            "box_size_over_mu": box,
            "grid_sizes": sizes,
            "seed": int(seed),
            "adiabaticity_tolerance": float(adiabaticity_tolerance),
            "metric_signature": "(-+++)",
            "scale_factor_initial": 1.0,
        },
        "rows": rows,
        "cutoff_increases_monotonically": cutoff_monotonic,
        "bare_psi_energy_increases_monotonically": energy_monotonic,
        "observed_log_slope_rho_vs_lattice_cutoff": log_slope,
        "renormalization": {
            "zero_point_energy_retained": True,
            "vacuum_subtraction_applied": False,
            "counterterms_applied": False,
            "continuum_limit_claimed": False,
            "physical_quantum_prediction": False,
        },
        "interpretation": (
            "The fixed-box bare Gaussian stress grows with the lattice UV cutoff. "
            "This quantifies the need for a renormalization prescription; it does "
            "not provide one and does not define a physical continuum limit."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit the bare WKB lattice stress as the fixed-box UV cutoff is raised."
    )
    parser.add_argument("--grid-sizes", nargs="+", type=int, default=[4, 6, 8, 10])
    parser.add_argument("--box-size-over-mu", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=20261121)
    parser.add_argument("--output", type=Path, default=Path("ptum_lattice_uv_cutoff_audit.json"))
    args = parser.parse_args(argv)

    params = PTUMParameters(V0=1.0e56)
    report = build_bare_wkb_cutoff_audit(
        params,
        grid_sizes=args.grid_sizes,
        box_size_over_mu=args.box_size_over_mu,
        seed=args.seed,
    )
    if not report["cutoff_increases_monotonically"]:
        raise RuntimeError("the declared lattice cutoff did not increase with grid size")
    if not report["bare_psi_energy_increases_monotonically"]:
        raise RuntimeError("the bare WKB stress did not expose monotonic UV growth")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        "BARE WKB CUTOFF AUDIT COMPLETED: "
        f"{len(report['rows'])} grids; "
        f"rho ratio={report['rows'][-1]['rho_psi_bare_GeV4'] / report['rows'][0]['rho_psi_bare_GeV4']:.8g}; "
        f"log slope={report['observed_log_slope_rho_vs_lattice_cutoff']:.8g}; "
        "renormalized=False"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
