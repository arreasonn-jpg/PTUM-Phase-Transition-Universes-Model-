#!/usr/bin/env python3
"""Finite-band momentum convergence oracle for a free squeezed Minkowski scalar.

This is a deliberately controlled R1 test, not a PTUM waterfall prediction.
A pure Gaussian state with beta_k = i beta_0 exp(-k/k_*) has an analytic
particle contribution to the Minkowski stress. Fourth-order adiabatic
subtraction removes the exact vacuum terms, leaving independently integrable
rho_k = omega_k |beta_k|^2 and p_k = k^2 |beta_k|^2/(3 omega_k).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

from ptum_adiabatic_stress import adiabatically_subtracted_stress_tensor_finite_band


MASS_SQUARED_GEV2 = 1.7
BETA_AMPLITUDE = 0.25
K_STAR_GEV = 0.8
REFERENCE_RELATIVE_TOLERANCE = 2.0e-7
WRONSKIAN_TOLERANCE = 1.0e-12


def _squeezed_minkowski_modes(k_comoving: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Canonical Minkowski modes with a purely imaginary Bogoliubov beta_k."""
    k = np.asarray(k_comoving, dtype=float)
    if k.ndim != 1 or k.size < 2 or np.any(k <= 0.0) or np.any(np.diff(k) <= 0.0):
        raise ValueError("k_comoving must be positive, finite and strictly increasing")
    if not np.all(np.isfinite(k)):
        raise ValueError("k_comoving must be finite")
    omega = np.sqrt(k**2 + MASS_SQUARED_GEV2)
    beta_imaginary = BETA_AMPLITUDE * np.exp(-k / K_STAR_GEV)
    alpha = np.sqrt(1.0 + beta_imaginary**2)
    normalization = np.sqrt(2.0 * omega)
    modes = (alpha + 1.0j * beta_imaginary) / normalization
    derivatives = (
        -1.0j * omega * (alpha - 1.0j * beta_imaginary) / normalization
    )
    return modes, derivatives


def _adaptive_reference() -> dict[str, dict[str, float]]:
    """Integrate the exact squeezed-state particle spectra on [0,infinity)."""
    def common(k: float) -> tuple[float, float, float]:
        omega = float(np.sqrt(k**2 + MASS_SQUARED_GEV2))
        beta_squared = BETA_AMPLITUDE**2 * np.exp(-2.0 * k / K_STAR_GEV)
        measure = k**2 / (2.0 * np.pi**2)
        return (
            measure * omega * beta_squared,
            measure * (k**2 / (3.0 * omega)) * beta_squared,
            measure * beta_squared / omega,
        )

    names = ("rho_GeV4", "pressure_GeV4", "variance_GeV2")
    reference = {}
    for index, name in enumerate(names):
        value, error = quad(
            lambda momentum: common(momentum)[index],
            0.0,
            np.inf,
            epsabs=1.0e-13,
            epsrel=1.0e-13,
            limit=200,
        )
        reference[name] = {"value": float(value), "quad_error_estimate": float(error)}
    return reference


def _evaluate_band(k: np.ndarray) -> dict[str, object]:
    modes, derivatives = _squeezed_minkowski_modes(k)
    result = adiabatically_subtracted_stress_tensor_finite_band(
        k,
        modes,
        derivatives,
        scale_factor_derivatives=(1.0, 0.0, 0.0, 0.0, 0.0),
        effective_mass_squared_derivatives=(
            MASS_SQUARED_GEV2, 0.0, 0.0, 0.0, 0.0
        ),
        curvature_coupling=0.0,
        wronskian_tolerance=WRONSKIAN_TOLERANCE,
    )
    return {
        "k_min": float(k[0]),
        "k_max": float(k[-1]),
        "n_modes": int(k.size),
        "rho_GeV4": float(result["rho_subtracted_finite_band_GeV4"]),
        "pressure_GeV4": float(result["pressure_subtracted_finite_band_GeV4"]),
        "variance_GeV2": float(
            result["variance_subtracted_order0_to2_finite_band_GeV2"]
        ),
        "max_wronskian_error": float(result["mode_wronskian_max_normalized_error"]),
        "finite_band_only": bool(result["finite_band_only"]),
        "renormalized_stress_tensor_claimed": bool(
            result["renormalized_stress_tensor_claimed"]
        ),
    }


def _family_report(
    grids: list[np.ndarray],
    reference: dict[str, dict[str, float]],
) -> dict[str, object]:
    rows = []
    for grid in grids:
        row = _evaluate_band(grid)
        row["relative_error"] = {
            name: abs(row[name] - reference[name]["value"])
            / max(abs(reference[name]["value"]), np.finfo(float).tiny)
            for name in ("rho_GeV4", "pressure_GeV4", "variance_GeV2")
        }
        rows.append(row)
    finest = rows[-1]
    finest_errors = finest["relative_error"]
    passed = (
        all(
            value <= REFERENCE_RELATIVE_TOLERANCE
            for value in finest_errors.values()
        )
        and finest["max_wronskian_error"] <= WRONSKIAN_TOLERANCE
        and all(row["finite_band_only"] for row in rows)
        and not any(row["renormalized_stress_tensor_claimed"] for row in rows)
    )
    return {
        "rows": rows,
        "finest_relative_errors": finest_errors,
        "finest_wronskian_error": finest["max_wronskian_error"],
        "passed": bool(passed),
    }


def run_minkowski_squeezed_band_audit() -> dict[str, object]:
    """Run resolution, UV-extension and IR-extension comparisons."""
    reference = _adaptive_reference()
    resolution_grids = [
        np.linspace(1.0e-3, 10.0, n)
        for n in (501, 1001, 2001, 4001)
    ]
    uv_grids = [
        np.linspace(1.0e-3, upper, int(round((upper - 1.0e-3) / 1.0e-2)) + 1)
        for upper in (4.0, 6.0, 8.0, 10.0, 12.0)
    ]
    ir_grids = [
        np.linspace(lower, 10.0, int(round((10.0 - lower) / 1.0e-2)) + 1)
        for lower in (0.1, 0.05, 0.02, 0.01, 1.0e-3)
    ]

    families = {
        "fixed_band_grid_refinement": _family_report(resolution_grids, reference),
        "ultraviolet_cutoff_extension": _family_report(uv_grids, reference),
        "infrared_cutoff_extension": _family_report(ir_grids, reference),
    }
    return {
        "model": {
            "field": "one free real scalar",
            "background": "Minkowski",
            "metric_signature": "(-+++)",
            "units": "GeV; the numerical mass and momentum scales are an arbitrary free-field control, not PTUM parameters",
            "mass_squared_GeV2": MASS_SQUARED_GEV2,
            "curvature_coupling": 0.0,
            "state": "pure Gaussian squeezed state",
            "bogoliubov_beta": "i*0.25*exp(-k/0.8)",
            "vacuum_wronskian": "v_k*v_k_prime_conjugate-v_k_prime*v_k_conjugate=i",
        },
        "subtraction": {
            "stress_tensor_adiabatic_order": 4,
            "variance_adiabatic_order": 2,
            "vacuum_piece_removed": True,
            "particle_spectrum_preserved": True,
            "reference_method": "independent adaptive quadrature on [0,infinity)",
        },
        "reference": reference,
        "tolerances": {
            "finest_relative_error": REFERENCE_RELATIVE_TOLERANCE,
            "wronskian_normalized_error": WRONSKIAN_TOLERANCE,
        },
        "families": families,
        "passed": all(family["passed"] for family in families.values()),
        "scope": {
            "finite_band_integrals_only": True,
            "free_field_control_only": True,
            "infrared_and_ultraviolet_extensions_compared": True,
            "interactions_included": False,
            "PTUM_time_dependent_waterfall_included": False,
            "self_consistent_background": False,
            "backreaction_included": False,
            "physical_PTUM_prediction": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit finite-band adiabatic stress integration in a free Minkowski control."
    )
    parser.add_argument(
        "--output",
        default="ptum_adiabatic_band_audit.json",
        help="strict-JSON output path",
    )
    args = parser.parse_args()
    report = run_minkowski_squeezed_band_audit()
    output = Path(args.output)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Finite-band adiabatic momentum audit: {'PASS' if report['passed'] else 'FAIL'}")
    print(f"Output: {output}")
    for name, family in report["families"].items():
        print(f"{name}: {family['finest_relative_errors']}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
