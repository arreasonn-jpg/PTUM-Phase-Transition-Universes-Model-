"""Second-order adiabatic subtraction controls for scalar-field variance.

For the canonical conformal-time mode v_k=a*varphi_k,

    v_k'' + [k^2 + a^2 M^2 + (6 xi - 1) a''/a] v_k = 0.

The field-variance UV counterterm in four spacetime dimensions is required
through adiabatic order two. This module computes that local subtraction and
a finite-band integral for caller-supplied, canonically normalized modes.

It deliberately does not subtract the stress tensor, choose finite
renormalization conditions, extrapolate momentum tails, or claim a
renormalized PTUM waterfall.
"""
from __future__ import annotations

import numpy as np


def _finite_real_scalar(name: str, value: float) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a finite real scalar")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real scalar") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be a finite real scalar")
    return result


def second_order_adiabatic_mode_variance(
    k_comoving: np.ndarray,
    *,
    scale_factor: float,
    scale_factor_prime: float,
    scale_factor_second: float,
    effective_mass_squared: float,
    effective_mass_squared_prime: float = 0.0,
    effective_mass_squared_second: float = 0.0,
    curvature_coupling: float = 0.0,
) -> dict[str, np.ndarray | float | int | str]:
    """Return the zeroth- and second-order WKB counterterms for |v_k|^2.

    Primes denote conformal-time derivatives. The zeroth-order frequency is

        omega_k^2 = k^2 + a^2 M^2,

    while sigma=(6 xi - 1) a''/a is assigned adiabatic order two. Derivatives
    of the supplied effective mass squared are included in omega' and omega''.
    Expanding the WKB equation gives

        W_2 = sigma/(2 omega) - omega''/(4 omega^2)
              + 3 omega'^2/(8 omega^3),

        |v_k|^2_ad^(0-2) = 1/(2 omega) - W_2/(2 omega^2).

    The routine is fail-closed when the zeroth-order frequency is not real
    and positive on the supplied momentum grid. Tachyonic IR modes must not
    be silently assigned an adiabatic particle basis.
    """
    raw_k = np.asarray(k_comoving)
    if raw_k.dtype.kind == "b":
        raise ValueError("k_comoving must contain positive finite real momenta")
    try:
        k = np.asarray(k_comoving, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("k_comoving must contain positive finite real momenta") from exc
    if k.ndim != 1 or k.size < 2:
        raise ValueError("k_comoving must be a one-dimensional grid with at least two modes")
    if not np.all(np.isfinite(k)) or np.any(k <= 0.0):
        raise ValueError("k_comoving must contain positive finite real momenta")
    if np.any(np.diff(k) <= 0.0):
        raise ValueError("k_comoving must be strictly increasing")

    a = _finite_real_scalar("scale_factor", scale_factor)
    ap = _finite_real_scalar("scale_factor_prime", scale_factor_prime)
    app = _finite_real_scalar("scale_factor_second", scale_factor_second)
    mass2 = _finite_real_scalar("effective_mass_squared", effective_mass_squared)
    mass2p = _finite_real_scalar(
        "effective_mass_squared_prime", effective_mass_squared_prime
    )
    mass2pp = _finite_real_scalar(
        "effective_mass_squared_second", effective_mass_squared_second
    )
    xi = _finite_real_scalar("curvature_coupling", curvature_coupling)
    if a <= 0.0:
        raise ValueError("scale_factor must be positive")

    omega_squared = k**2 + a**2 * mass2
    if not np.all(np.isfinite(omega_squared)) or np.any(omega_squared <= 0.0):
        raise ValueError(
            "zeroth-order frequency squared must be finite and positive "
            "for every supplied momentum"
        )

    omega_squared_prime = (
        2.0 * a * ap * mass2 + a**2 * mass2p
    )
    omega_squared_second = (
        2.0 * (ap**2 + a * app) * mass2
        + 4.0 * a * ap * mass2p
        + a**2 * mass2pp
    )
    omega = np.sqrt(omega_squared)
    omega_prime = omega_squared_prime / (2.0 * omega)
    omega_second = (
        omega_squared_second / (2.0 * omega)
        - omega_squared_prime**2 / (4.0 * omega**3)
    )
    sigma = (6.0 * xi - 1.0) * app / a
    W2 = (
        sigma / (2.0 * omega)
        - omega_second / (4.0 * omega**2)
        + 3.0 * omega_prime**2 / (8.0 * omega**3)
    )
    variance_order0 = 1.0 / (2.0 * omega)
    variance_order2_correction = -W2 / (2.0 * omega**2)
    variance_order0_to_2 = variance_order0 + variance_order2_correction

    arrays = (
        omega, omega_prime, omega_second, W2,
        variance_order0, variance_order2_correction, variance_order0_to_2,
    )
    if not all(np.all(np.isfinite(value)) for value in arrays):
        raise FloatingPointError("adiabatic subtraction coefficients are non-finite")

    return {
        "k_comoving": k,
        "omega0": omega,
        "omega0_prime": omega_prime,
        "omega0_second": omega_second,
        "WKB_frequency_order2": W2,
        "mode_variance_order0": variance_order0,
        "mode_variance_order2_correction": variance_order2_correction,
        "mode_variance_adiabatic_order0_to_2": variance_order0_to_2,
        "adiabatic_order": 2,
        "mode_equation": (
            "v''+[k^2+a^2*M^2+(6*xi-1)*a''/a]v=0"
        ),
        "assumptions": {
            "conformal_time_derivatives_supplied": True,
            "effective_mass_derivatives_included": True,
            "zeroth_order_frequency_positive_on_grid": True,
            "field_variance_subtraction_order": 2,
            "stress_tensor_subtraction_implemented": False,
            "finite_renormalization_conditions_selected": False,
            "physical_PTUM_prediction": False,
        },
    }


def adiabatically_subtracted_field_variance_finite_band(
    k_comoving: np.ndarray,
    canonical_modes: np.ndarray,
    canonical_mode_derivatives: np.ndarray,
    *,
    scale_factor: float,
    scale_factor_prime: float,
    scale_factor_second: float,
    effective_mass_squared: float,
    effective_mass_squared_prime: float = 0.0,
    effective_mass_squared_second: float = 0.0,
    curvature_coupling: float = 0.0,
    wronskian_tolerance: float = 1.0e-7,
) -> dict[str, object]:
    """Integrate the order-two adiabatically subtracted <varphi^2> on a finite band.

    The caller supplies canonical modes with
    v_k v_k'^* - v_k' v_k^* = i. The returned integral is

        integral[k_min,k_max] dk k^2/(2 pi^2 a^2)
            (|v_k|^2 - |v_k|^2_ad^(0-2)).

    This is a finite-band field-variance diagnostic only. It is not a
    renormalized stress tensor, a renormalized force on Phi, or a complete
    renormalized expectation value because the omitted IR/UV tails and
    finite local renormalization conditions are not supplied.
    """
    raw_k = np.asarray(k_comoving)
    if raw_k.dtype.kind == "b":
        raise ValueError("k_comoving must contain positive finite real momenta")
    try:
        k = np.asarray(k_comoving, dtype=float)
        modes = np.asarray(canonical_modes, dtype=complex)
        derivatives = np.asarray(canonical_mode_derivatives, dtype=complex)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("momentum and mode arrays must be finite numeric arrays") from exc
    if k.ndim != 1 or k.size < 2:
        raise ValueError("k_comoving must be a one-dimensional grid with at least two modes")
    if modes.shape != k.shape or derivatives.shape != k.shape:
        raise ValueError("mode arrays must match the momentum grid")
    if (not np.all(np.isfinite(k)) or np.any(k <= 0.0)
            or np.any(np.diff(k) <= 0.0)):
        raise ValueError("k_comoving must be positive, finite and strictly increasing")
    if not np.all(np.isfinite(modes)) or not np.all(np.isfinite(derivatives)):
        raise ValueError("canonical modes and derivatives must be finite")

    tolerance = _finite_real_scalar("wronskian_tolerance", wronskian_tolerance)
    if tolerance <= 0.0:
        raise ValueError("wronskian_tolerance must be positive")
    wronskian = modes * np.conjugate(derivatives) - derivatives * np.conjugate(modes)
    wronskian_error = np.abs(wronskian - 1.0j) / np.maximum(1.0, np.abs(wronskian))
    max_wronskian_error = float(np.max(wronskian_error))
    if not np.isfinite(max_wronskian_error) or max_wronskian_error > tolerance:
        raise ValueError(
            "canonical modes violate the required Wronskian normalization: "
            f"{max_wronskian_error:.6g} exceeds {tolerance:.6g}"
        )

    subtraction = second_order_adiabatic_mode_variance(
        k,
        scale_factor=scale_factor,
        scale_factor_prime=scale_factor_prime,
        scale_factor_second=scale_factor_second,
        effective_mass_squared=effective_mass_squared,
        effective_mass_squared_prime=effective_mass_squared_prime,
        effective_mass_squared_second=effective_mass_squared_second,
        curvature_coupling=curvature_coupling,
    )
    a = _finite_real_scalar("scale_factor", scale_factor)
    bare_mode_variance = np.abs(modes) ** 2
    adiabatic_mode_variance = np.asarray(
        subtraction["mode_variance_adiabatic_order0_to_2"], dtype=float
    )
    measure = k**2 / (2.0 * np.pi**2 * a**2)
    bare_integrand = measure * bare_mode_variance
    counterterm_integrand = measure * adiabatic_mode_variance
    subtracted_integrand = bare_integrand - counterterm_integrand

    bare_integral = float(np.trapezoid(bare_integrand, k))
    counterterm_integral = float(np.trapezoid(counterterm_integrand, k))
    subtracted_integral = float(np.trapezoid(subtracted_integrand, k))
    values = np.asarray(
        [bare_integral, counterterm_integral, subtracted_integral],
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise FloatingPointError("finite-band adiabatic variance integral is non-finite")

    return {
        "variance_bare_finite_band": bare_integral,
        "variance_adiabatic_counterterm_finite_band": counterterm_integral,
        "variance_subtracted_finite_band": subtracted_integral,
        "variance_units": "the square of the momentum unit",
        "k_min": float(k[0]),
        "k_max": float(k[-1]),
        "number_of_modes": int(k.size),
        "mode_wronskian_max_normalized_error": max_wronskian_error,
        "mode_variance_bare": bare_mode_variance.tolist(),
        "mode_variance_counterterm_order0_to2": adiabatic_mode_variance.tolist(),
        "mode_variance_subtracted": (
            (bare_mode_variance - adiabatic_mode_variance).tolist()
        ),
        "finite_band_only": True,
        "infrared_tail_extrapolated": False,
        "ultraviolet_tail_extrapolated": False,
        "fully_renormalized_expectation_claimed": False,
        "renormalized_stress_tensor_computed": False,
        "renormalized_force_on_Phi_computed": False,
        "physical_PTUM_prediction": False,
        "prescription": "second_order_adiabatic_subtraction_of_field_variance",
    }
