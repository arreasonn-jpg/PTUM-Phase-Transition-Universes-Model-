"""Analytic real-scalar Z2 domain-wall diagnostics for the PTUM waterfall.

This module is a local, frozen-background field-theory estimate. It does not
simulate defect formation, a cosmological wall network, or the time-dependent
waterfall. All quantities use natural units (hbar=c=1).
"""
from __future__ import annotations

import numpy as np


def _validate_positive(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _validate_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


def domain_wall_vev(mu_eff: float, lambda_psi: float) -> float:
    """Return v=mu_eff/sqrt(lambda_psi) for V=lambda(psi^2-v^2)^2/4."""
    mu_eff = _validate_positive("mu_eff", mu_eff)
    lambda_psi = _validate_positive("lambda_psi", lambda_psi)
    return mu_eff / np.sqrt(lambda_psi)


def domain_wall_profile(z, mu_eff: float, lambda_psi: float):
    """Planar static kink psi(z)=v tanh(mu_eff*z/sqrt(2))."""
    v = domain_wall_vev(mu_eff, lambda_psi)
    z_arr = np.asarray(z, dtype=float)
    if not np.all(np.isfinite(z_arr)):
        raise ValueError("z must be finite")
    return v * np.tanh(mu_eff * z_arr / np.sqrt(2.0))


def domain_wall_profile_derivative(z, mu_eff: float, lambda_psi: float):
    """Exact d psi/dz for the planar kink."""
    v = domain_wall_vev(mu_eff, lambda_psi)
    z_arr = np.asarray(z, dtype=float)
    if not np.all(np.isfinite(z_arr)):
        raise ValueError("z must be finite")
    u = mu_eff * z_arr / np.sqrt(2.0)
    return v * mu_eff / np.sqrt(2.0) / np.cosh(u) ** 2


def domain_wall_energy_density(z, mu_eff: float, lambda_psi: float):
    """Static kink energy density above the degenerate vacuum."""
    derivative = domain_wall_profile_derivative(z, mu_eff, lambda_psi)
    return np.asarray(derivative) ** 2


def domain_wall_tension(mu_eff: float, lambda_psi: float) -> float:
    """Exact flat-space kink tension sigma=2 sqrt(2) mu_eff^3/(3 lambda)."""
    mu_eff = _validate_positive("mu_eff", mu_eff)
    lambda_psi = _validate_positive("lambda_psi", lambda_psi)
    return 2.0 * np.sqrt(2.0) * mu_eff**3 / (3.0 * lambda_psi)


def bias_from_operator_vev(
    operator_vev: float,
    cutoff: float,
    wilson_coefficient: float = 1.0,
) -> float:
    """Magnitude of epsilon=|C <O_SM>|/Lambda for U_bias=-epsilon*psi.

    The operator has canonical dimension four, so epsilon has dimension
    three. This function only maps a supplied renormalized expectation value
    to a linear source; it does not predict that expectation value.
    """
    operator_vev = abs(float(operator_vev))
    cutoff = _validate_positive("cutoff", cutoff)
    wilson_coefficient = abs(float(wilson_coefficient))
    if not np.isfinite(operator_vev) or not np.isfinite(wilson_coefficient):
        raise ValueError("operator_vev and wilson_coefficient must be finite")
    return wilson_coefficient * operator_vev / cutoff


def _tilted_minima(mu_eff: float, lambda_psi: float, epsilon_bias: float):
    """Solve the exact stationary cubic for the tilted double-well potential."""
    mu_eff = _validate_positive("mu_eff", mu_eff)
    lambda_psi = _validate_positive("lambda_psi", lambda_psi)
    epsilon_bias = _validate_nonnegative("epsilon_bias", epsilon_bias)
    v = mu_eff / np.sqrt(lambda_psi)
    epsilon_critical = (
        2.0 * mu_eff**3 / (3.0 * np.sqrt(3.0 * lambda_psi))
    )
    b = epsilon_bias * np.sqrt(lambda_psi) / mu_eff**3
    b_critical = 2.0 / (3.0 * np.sqrt(3.0))
    if b >= b_critical:
        return {
            "metastable_vacuum_exists": False,
            "true_minimum": None,
            "false_minimum": None,
            "vacuum_bias": None,
            "epsilon_critical": epsilon_critical,
            "bias_ratio_to_spinodal": b / b_critical,
        }

    # Parameterize the three real stationary points with
    # delta = (1/3) asin(3 sqrt(3) b / 2). This is better conditioned
    # than a generic cubic root finder when b is far below machine
    # precision relative to the O(1) locations of the two minima.
    argument = np.clip(1.5 * np.sqrt(3.0) * b, 0.0, 1.0)
    delta = np.arcsin(argument) / 3.0
    y_true = 2.0 / np.sqrt(3.0) * np.cos(np.pi / 6.0 - delta)
    y_false = -2.0 / np.sqrt(3.0) * np.cos(np.pi / 6.0 + delta)

    # Hellmann-Feynman: d(f_false - f_true)/db = y_true - y_false.
    # Integrating this identity gives a cancellation-free closed form.
    # Directly subtracting the two O(mu_eff^4/lambda_psi) potential
    # values loses the entire bias when b is cosmologically tiny.
    delta_f = (
        np.sin(2.0 * delta) + 0.5 * np.sin(4.0 * delta)
    ) / np.sqrt(3.0)
    vacuum_bias = delta_f * mu_eff**4 / lambda_psi

    return {
        "metastable_vacuum_exists": True,
        "true_minimum": y_true * v,
        "false_minimum": y_false * v,
        "vacuum_bias": vacuum_bias,
        "epsilon_critical": epsilon_critical,
        "bias_ratio_to_spinodal": b / b_critical,
    }


def domain_wall_bias_diagnostics(
    mu_eff: float,
    lambda_psi: float,
    epsilon_bias: float,
    *,
    hubble_bbn: float,
    reduced_planck_mass: float,
    network_area_factor: float = 1.0,
    small_bias_fraction: float = 0.1,
) -> dict[str, float | bool | None]:
    """Return necessary annihilation-before-domination/BBN estimates.

    The static wall tension is exact at zero bias. For a tilted potential it
    is used in H_ann ~= DeltaV/sigma only when epsilon is below the declared
    small-bias fraction of the spinodal source. The wall-domination estimate
    uses rho_wall ~= A*sigma*H and hence H_dom ~= A*sigma/(3 M_Pl^2).
    Both cosmological estimates are order-of-magnitude network criteria,
    not a substitute for a defect-network simulation.
    """
    mu_eff = _validate_positive("mu_eff", mu_eff)
    lambda_psi = _validate_positive("lambda_psi", lambda_psi)
    epsilon_bias = _validate_nonnegative("epsilon_bias", epsilon_bias)
    hubble_bbn = _validate_positive("hubble_bbn", hubble_bbn)
    reduced_planck_mass = _validate_positive(
        "reduced_planck_mass", reduced_planck_mass
    )
    network_area_factor = _validate_positive(
        "network_area_factor", network_area_factor
    )
    small_bias_fraction = float(small_bias_fraction)
    if (not np.isfinite(small_bias_fraction)
            or not 0.0 < small_bias_fraction < 1.0):
        raise ValueError("small_bias_fraction must lie strictly between 0 and 1")

    v = domain_wall_vev(mu_eff, lambda_psi)
    sigma = domain_wall_tension(mu_eff, lambda_psi)
    tilted = _tilted_minima(mu_eff, lambda_psi, epsilon_bias)
    h_dom = network_area_factor * sigma / (3.0 * reduced_planck_mass**2)
    required_delta_v = sigma * max(hubble_bbn, h_dom)
    required_epsilon_linear = required_delta_v / (2.0 * v)
    epsilon_critical = float(tilted["epsilon_critical"])
    small_bias_valid = (
        bool(tilted["metastable_vacuum_exists"])
        and epsilon_bias <= small_bias_fraction * epsilon_critical
    )

    if small_bias_valid:
        delta_v = float(tilted["vacuum_bias"])
        h_ann = delta_v / sigma
        before_bbn = bool(h_ann > hubble_bbn)
        before_domination = bool(h_ann > h_dom)
    else:
        delta_v = tilted["vacuum_bias"]
        h_ann = None
        before_bbn = None
        before_domination = None

    return {
        "vev": v,
        "wall_core_length": np.sqrt(2.0) / mu_eff,
        "wall_tension": sigma,
        "epsilon_bias": epsilon_bias,
        "epsilon_critical": epsilon_critical,
        "bias_ratio_to_spinodal": float(tilted["bias_ratio_to_spinodal"]),
        "metastable_vacuum_exists": bool(tilted["metastable_vacuum_exists"]),
        "vacuum_bias": delta_v,
        "small_bias_tension_approx_valid": small_bias_valid,
        "hubble_annihilation_estimate": h_ann,
        "hubble_domination_estimate": h_dom,
        "annihilation_before_bbn": before_bbn,
        "annihilation_before_wall_domination": before_domination,
        "required_vacuum_bias_for_bbn_and_domination": required_delta_v,
        "required_linear_source_for_bbn_and_domination": required_epsilon_linear,
        "network_area_factor": network_area_factor,
        "small_bias_fraction": small_bias_fraction,
        "cosmological_estimates_are_order_of_magnitude": True,
    }
