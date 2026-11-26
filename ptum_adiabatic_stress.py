"""Fourth-order adiabatic stress-tensor subtraction controls for a real scalar.

Metric signature is (-+++). Conformal-time derivatives are denoted by primes.
The canonical mode v_k=a*psi_k obeys
    v_k'' + [k^2+a^2 M^2+(6 xi-1)a''/a] v_k = 0.

This module derives local fourth-order WKB counterterms for the homogeneous
energy density and isotropic pressure on a caller-supplied spatially flat
FLRW background. It also integrates bare-minus-counterterm quantities over
a finite comoving momentum band.

This is not a complete renormalization prescription: no finite matching
conditions or momentum-tail extrapolations are selected, no coupled Phi
equation is solved, and no renormalized CTP or nonlinear-lattice evolution
is claimed.
"""
from __future__ import annotations

import math
import numpy as np


def _finite_scalar(name: str, value: float) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a finite real scalar")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real scalar") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be a finite real scalar")
    return result


def _momentum_grid(k_comoving: np.ndarray) -> np.ndarray:
    raw = np.asarray(k_comoving)
    if raw.dtype.kind == "b":
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
    return k


def _derivative_jet(name: str, values) -> np.ndarray:
    """Validate f and its first four conformal-time derivatives."""
    try:
        raw = list(values)
    except TypeError as exc:
        raise ValueError(f"{name} must contain five conformal-time derivatives") from exc
    if len(raw) != 5:
        raise ValueError(f"{name} must contain five conformal-time derivatives")
    return np.asarray(
        [_finite_scalar(f"{name}[{index}]", value) for index, value in enumerate(raw)],
        dtype=float,
    )


def _jet_multiply(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Multiply truncated Taylor jets; coefficient n is f^(n)/n!."""
    size = min(left.size, right.size)
    result = np.zeros(size, dtype=float)
    for order in range(size):
        result[order] = sum(
            left[index] * right[order - index]
            for index in range(order + 1)
        )
    return result


def _jet_inverse(values: np.ndarray) -> np.ndarray:
    if values.ndim != 1 or values.size == 0 or values[0] == 0.0:
        raise ValueError("Taylor-series inverse requires a nonzero leading coefficient")
    result = np.zeros_like(values, dtype=float)
    result[0] = 1.0 / values[0]
    for order in range(1, values.size):
        result[order] = -sum(
            values[index] * result[order - index]
            for index in range(1, order + 1)
        ) / values[0]
    return result


def _jet_sqrt(values: np.ndarray) -> np.ndarray:
    if values.ndim != 1 or values.size == 0 or values[0] <= 0.0:
        raise ValueError("Taylor-series square root requires a positive leading coefficient")
    result = np.zeros_like(values, dtype=float)
    result[0] = math.sqrt(values[0])
    for order in range(1, values.size):
        result[order] = (
            values[order]
            - sum(result[index] * result[order - index]
                  for index in range(1, order))
        ) / (2.0 * result[0])
    return result


def _one_mode_counterterms(
    k: float,
    a: np.ndarray,
    mass: np.ndarray,
    xi: float,
) -> dict[str, float]:
    """Return one-mode WKB stress and variance coefficients through order four."""
    factorials = np.asarray([math.factorial(index) for index in range(5)], dtype=float)
    a_series = a / factorials
    mass_series = mass / factorials
    q_series = _jet_multiply(
        _jet_multiply(a_series, a_series),
        mass_series,
    )
    q_series[0] += k * k
    if q_series[0] <= 0.0 or not np.isfinite(q_series[0]):
        raise ValueError("zeroth-order WKB frequency squared must be positive")

    omega_series = _jet_sqrt(q_series)
    omega = float(omega_series[0])
    omega_prime = float(omega_series[1])
    omega_second = float(2.0 * omega_series[2])
    h_conformal = a[1] / a[0]
    sigma0 = (6.0 * xi - 1.0) * a[2] / a[0]
    full_frequency_squared = q_series[0] + sigma0
    if not np.isfinite(full_frequency_squared) or full_frequency_squared <= 0.0:
        raise ValueError(
            "full zeroth-plus-curvature frequency squared must be positive "
            "on the supplied adiabatic band"
        )

    # sigma=(6 xi-1) a''/a, through its second Taylor coefficient.
    a_second_series = np.asarray([a[2], a[3], a[4] / 2.0], dtype=float)
    inverse_a_series = _jet_inverse(a_series[:3])
    sigma_series = (6.0 * xi - 1.0) * _jet_multiply(
        a_second_series, inverse_a_series
    )

    # The omega-prime and omega-second jets retain the derivatives needed by W2''.
    omega_prime_series = np.asarray(
        [omega_series[1], 2.0 * omega_series[2], 3.0 * omega_series[3]],
        dtype=float,
    )
    omega_second_series = np.asarray(
        [2.0 * omega_series[2], 6.0 * omega_series[3],
         12.0 * omega_series[4]],
        dtype=float,
    )
    inverse_omega = _jet_inverse(omega_series[:3])
    inverse_omega2 = _jet_multiply(inverse_omega, inverse_omega)
    inverse_omega3 = _jet_multiply(inverse_omega2, inverse_omega)

    # W=omega+W2+W4, with W2 retained as a two-derivative Taylor jet.
    w2_series = (
        0.5 * _jet_multiply(sigma_series, inverse_omega)
        - 0.25 * _jet_multiply(omega_second_series, inverse_omega2)
        + 0.375 * _jet_multiply(
            _jet_multiply(omega_prime_series, omega_prime_series),
            inverse_omega3,
        )
    )
    w2 = float(w2_series[0])
    w2_prime = float(w2_series[1])
    w2_second = float(2.0 * w2_series[2])

    # Fourth-order solution of W^2=omega^2+sigma-W''/(2W)+3W'^2/(4W^2).
    w4 = (
        -0.5 * (w2_second / omega - omega_second * w2 / omega**2)
        + 1.5 * (omega_prime / omega) * (
            w2_prime / omega - omega_prime * w2 / omega**2
        )
        - w2**2
    ) / (2.0 * omega)

    # S=|v|^2=S0+S2+S4. Derivatives of S4 first enter at order six.
    s0_series = 0.5 * inverse_omega
    s2_series = -0.5 * _jet_multiply(w2_series, inverse_omega2)
    s0 = float(s0_series[0])
    s0_prime = float(s0_series[1])
    s0_second = float(2.0 * s0_series[2])
    s2 = float(s2_series[0])
    s2_prime = float(s2_series[1])
    s2_second = float(2.0 * s2_series[2])
    s4 = w2**2 / (2.0 * omega**3) - w4 / (2.0 * omega**2)

    # A=H_conf+W'/(2W)=A0+A2+O(ad^5).
    a0 = h_conformal + omega_prime / (2.0 * omega)
    a2 = w2_prime / (2.0 * omega) - omega_prime * w2 / (2.0 * omega**2)
    b_gradient = k * k / 3.0 + a[0] ** 2 * mass[0]

    # Hilbert tensor: canonical part plus xi*(G_munu+g_munu Box-nabla_m nabla_nu)|psi|^2.
    rho = (
        omega / 2.0
        + w2**2 / (4.0 * omega)
        + a0**2 / (4.0 * omega)
        + a0 * a2 / (2.0 * omega)
        - a0**2 * w2 / (4.0 * omega**2)
        + 3.0 * xi * (
            h_conformal * (s0_prime + s2_prime)
            - h_conformal**2 * (s0 + s2)
        )
    ) / a[0] ** 4

    pressure = (
        omega
        - b_gradient / omega
        + w2
        + b_gradient * w2 / omega**2
        + w4 * (1.0 + b_gradient / omega**2)
        - b_gradient * w2**2 / omega**3
        + a0**2 / omega
        + 2.0 * a0 * a2 / omega
        - a0**2 * w2 / omega**2
    ) / 4.0
    pressure += xi * (
        -(s0_second + s2_second)
        + 3.0 * h_conformal * (s0_prime + s2_prime)
        - 3.0 * h_conformal**2 * (s0 + s2)
    )
    pressure /= a[0] ** 4

    variance_order2 = (s0 + s2) / a[0] ** 2
    variance_order4 = (s0 + s2 + s4) / a[0] ** 2
    values = np.asarray(
        [rho, pressure, variance_order2, variance_order4, w2, w2_prime,
         w2_second, w4, omega],
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise FloatingPointError("fourth-order adiabatic coefficients are non-finite")

    return {
        "rho_mode_counterterm": float(rho),
        "pressure_mode_counterterm": float(pressure),
        "field_variance_mode_counterterm_order0_to2": float(variance_order2),
        "field_variance_mode_counterterm_order0_to4": float(variance_order4),
        "omega0": float(omega),
        "WKB_frequency_order2": float(w2),
        "WKB_frequency_order2_prime": float(w2_prime),
        "WKB_frequency_order2_second": float(w2_second),
        "WKB_frequency_order4": float(w4),
        "WKB_frequency_order2_over_omega": float(w2 / omega),
        "WKB_frequency_order4_over_omega": float(w4 / omega),
    }


def fourth_order_adiabatic_stress_coefficients(
    k_comoving: np.ndarray,
    *,
    scale_factor_derivatives,
    effective_mass_squared_derivatives,
    curvature_coupling: float = 0.0,
) -> dict[str, object]:
    """Return mode-by-mode fourth-order adiabatic stress counterterms.

    The two derivative inputs contain f and its first four conformal-time
    derivatives. The WKB frequency is W=omega+W2+W4, with omega^2=k^2+a^2*M^2
    and W2=(6*xi-1)*a''/(2*a*omega)-omega''/(4*omega^2)
    +3*omega'^2/(8*omega^3). W4 follows by expanding the nonlinear WKB
    equation consistently through fourth adiabatic order.

    The variance counterterm is returned at orders zero-to-two and
    zero-to-four. The stress tensor uses the fourth-order expansion.
    """
    k = _momentum_grid(k_comoving)
    a = _derivative_jet("scale_factor_derivatives", scale_factor_derivatives)
    mass = _derivative_jet(
        "effective_mass_squared_derivatives",
        effective_mass_squared_derivatives,
    )
    xi = _finite_scalar("curvature_coupling", curvature_coupling)
    if a[0] <= 0.0:
        raise ValueError("scale factor must be positive")

    rows = [_one_mode_counterterms(float(momentum), a, mass, xi) for momentum in k]
    keys = tuple(rows[0])
    result = {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in keys
    }
    result.update({
        "k_comoving": k,
        "adiabatic_order_stress_tensor": 4,
        "adiabatic_order_field_variance_uv": 2,
        "metric_signature": "(-+++)",
        "mode_equation": "v''+[k^2+a^2*M^2+(6*xi-1)*a''/a]v=0",
        "assumptions": {
            "homogeneous_spatially_flat_flrw": True,
            "external_scale_factor_and_mass_jets": True,
            "positive_zeroth_order_frequency_on_band": True,
            "positive_full_mode_frequency_on_band": True,
            "finite_renormalization_conditions_selected": False,
            "infrared_or_ultraviolet_tail_extrapolated": False,
            "renormalized_PTUM_stress_tensor_claimed": False,
            "physical_PTUM_prediction": False,
        },
    })
    return result


def adiabatically_subtracted_stress_tensor_finite_band(
    k_comoving: np.ndarray,
    canonical_modes: np.ndarray,
    canonical_mode_derivatives: np.ndarray,
    *,
    scale_factor_derivatives,
    effective_mass_squared_derivatives,
    curvature_coupling: float = 0.0,
    wronskian_tolerance: float = 1.0e-7,
) -> dict[str, object]:
    """Integrate bare-minus-fourth-order-counterterm stress over a finite k band.

    The supplied canonical modes must satisfy v*v'^* - v'*v^*=i.
    Both order-two and order-four variance subtractions are reported so
    the external-mass energy-transfer convention is explicit.
    """
    k = _momentum_grid(k_comoving)
    try:
        modes = np.asarray(canonical_modes, dtype=complex)
        derivatives = np.asarray(canonical_mode_derivatives, dtype=complex)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("canonical mode arrays must be finite numeric arrays") from exc
    if modes.shape != k.shape or derivatives.shape != k.shape:
        raise ValueError("canonical mode arrays must match the momentum grid")
    if not np.all(np.isfinite(modes)) or not np.all(np.isfinite(derivatives)):
        raise ValueError("canonical modes and derivatives must be finite")

    tolerance = _finite_scalar("wronskian_tolerance", wronskian_tolerance)
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

    a = _derivative_jet("scale_factor_derivatives", scale_factor_derivatives)
    mass = _derivative_jet(
        "effective_mass_squared_derivatives",
        effective_mass_squared_derivatives,
    )
    xi = _finite_scalar("curvature_coupling", curvature_coupling)
    if a[0] <= 0.0:
        raise ValueError("scale factor must be positive")
    coefficients = fourth_order_adiabatic_stress_coefficients(
        k,
        scale_factor_derivatives=a,
        effective_mass_squared_derivatives=mass,
        curvature_coupling=xi,
    )

    a0 = a[0]
    h_conformal = a[1] / a0
    omega_full_squared = (
        k**2 + a0**2 * mass[0] + (6.0 * xi - 1.0) * a[2] / a0
    )
    if np.any(omega_full_squared <= 0.0) or not np.all(np.isfinite(omega_full_squared)):
        raise ValueError("full mode frequency squared must be positive on the supplied band")

    mode_variance = np.abs(modes) ** 2
    mode_variance_prime = 2.0 * np.real(np.conjugate(modes) * derivatives)
    mode_variance_second = (
        2.0 * np.abs(derivatives) ** 2
        - 2.0 * omega_full_squared * mode_variance
    )
    shifted_derivative = derivatives - h_conformal * modes
    canonical_frequency_squared = k**2 + a0**2 * mass[0]
    pressure_gradient_mass = k**2 / 3.0 + a0**2 * mass[0]

    rho_bare_mode = (
        0.5 * (
            np.abs(shifted_derivative) ** 2
            + canonical_frequency_squared * mode_variance
        )
        + 3.0 * xi * (
            h_conformal * mode_variance_prime
            - h_conformal**2 * mode_variance
        )
    ) / a0**4
    pressure_bare_mode = (
        0.5 * (
            np.abs(shifted_derivative) ** 2
            - pressure_gradient_mass * mode_variance
        )
        + xi * (
            -mode_variance_second
            + 3.0 * h_conformal * mode_variance_prime
            - 3.0 * h_conformal**2 * mode_variance
        )
    ) / a0**4
    variance_bare_mode = mode_variance / a0**2

    measure = k**2 / (2.0 * np.pi**2)
    rho_ct_mode = np.asarray(coefficients["rho_mode_counterterm"], dtype=float)
    pressure_ct_mode = np.asarray(coefficients["pressure_mode_counterterm"], dtype=float)
    variance_ct2_mode = np.asarray(
        coefficients["field_variance_mode_counterterm_order0_to2"], dtype=float
    )
    variance_ct4_mode = np.asarray(
        coefficients["field_variance_mode_counterterm_order0_to4"], dtype=float
    )

    def integrate(values):
        return float(np.trapezoid(measure * values, k))

    rho_bare = integrate(rho_bare_mode)
    pressure_bare = integrate(pressure_bare_mode)
    rho_counterterm = integrate(rho_ct_mode)
    pressure_counterterm = integrate(pressure_ct_mode)
    variance_bare = integrate(variance_bare_mode)
    variance_counterterm_order2 = integrate(variance_ct2_mode)
    variance_counterterm_order4 = integrate(variance_ct4_mode)
    rho_subtracted = rho_bare - rho_counterterm
    pressure_subtracted = pressure_bare - pressure_counterterm
    variance_subtracted_order2 = variance_bare - variance_counterterm_order2
    variance_subtracted_order4 = variance_bare - variance_counterterm_order4
    hubble = a[1] / a0**2
    mass_squared_dot = mass[1] / a0

    values = np.asarray([
        rho_bare, pressure_bare, rho_counterterm, pressure_counterterm,
        variance_bare, variance_counterterm_order2, variance_counterterm_order4,
        rho_subtracted, pressure_subtracted,
        variance_subtracted_order2, variance_subtracted_order4,
    ])
    if not np.all(np.isfinite(values)):
        raise FloatingPointError("finite-band stress-tensor integral is non-finite")

    return {
        "rho_bare_finite_band_GeV4": rho_bare,
        "rho_adiabatic_counterterm_finite_band_GeV4": rho_counterterm,
        "rho_subtracted_finite_band_GeV4": rho_subtracted,
        "pressure_bare_finite_band_GeV4": pressure_bare,
        "pressure_adiabatic_counterterm_finite_band_GeV4": pressure_counterterm,
        "pressure_subtracted_finite_band_GeV4": pressure_subtracted,
        "variance_bare_finite_band_GeV2": variance_bare,
        "variance_adiabatic_counterterm_order0_to2_finite_band_GeV2": (
            variance_counterterm_order2
        ),
        "variance_adiabatic_counterterm_order0_to4_finite_band_GeV2": (
            variance_counterterm_order4
        ),
        "variance_subtracted_order0_to2_finite_band_GeV2": variance_subtracted_order2,
        "variance_subtracted_order0_to4_finite_band_GeV2": variance_subtracted_order4,
        "external_mass_energy_transfer_source_order0_to2_GeV5": (
            0.5 * mass_squared_dot * variance_subtracted_order2
        ),
        "external_mass_energy_transfer_source_order0_to4_GeV5": (
            0.5 * mass_squared_dot * variance_subtracted_order4
        ),
        "hubble_GeV": hubble,
        "mass_squared_dot_GeV3": mass_squared_dot,
        "k_min_GeV": float(k[0]),
        "k_max_GeV": float(k[-1]),
        "number_of_modes": int(k.size),
        "mode_wronskian_max_normalized_error": max_wronskian_error,
        "finite_band_only": True,
        "infrared_tail_extrapolated": False,
        "ultraviolet_tail_extrapolated": False,
        "finite_renormalization_conditions_selected": False,
        "renormalized_stress_tensor_claimed": False,
        "renormalized_force_on_Phi_computed": False,
        "self_consistent_friedmann_backreaction": False,
        "nonlinear_lattice_counterterm_implemented": False,
        "physical_PTUM_prediction": False,
        "adiabatic_stress_tensor_order": 4,
        "field_variance_uv_subtraction_order": 2,
        "metric_signature": "(-+++)",
        "prescription": "fourth_order_adiabatic_stress_subtraction_finite_band",
    }
