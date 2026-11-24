"""Local one-loop UV coefficient for the coupled PTUM scalar sector.

This module derives the bulk heat-kernel a_2 coefficient for the Gaussian
(two-real-scalar) fluctuation operator built from the common tree-level
PTUM potential. It is a UV-pole oracle, not a renormalization prescription.

The curvature invariants passed to scalar_heat_kernel_a2 must use the same
Euclidean Laplace-type convention as
    D_E = -nabla_E^2 I + Hessian(V) + Xi R_E.
Covariant total derivatives and boundary/initial-surface terms are omitted.
No finite counterterms, CTP state-dependent terms, stress tensor, or
real-time backreaction are computed.
"""
from __future__ import annotations

import numpy as np

from ptum_task1_simulation import M_PL, PTUMParameters, meff_sq_psi


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


def ptum_scalar_hessian(
    Phi: float,
    psi: float,
    params: PTUMParameters,
) -> np.ndarray:
    """Return d^2 V(Phi,psi)/d(Phi,psi)^2 in the canonical field basis.

    V = V_eff(Phi) + m_eff^2(Phi) psi^2/2 + lambda_psi psi^4/4,
    m_eff^2 = c_psi Phi^2 - m_psi^2,
    c_psi = alpha m_psi^2 / E_th^2.
    The matrix has units GeV^2. Negative eigenvalues in the tachyonic
    region are allowed; no static logarithm is evaluated.
    """
    phi = _finite_real_scalar("Phi", Phi)
    waterfall = _finite_real_scalar("psi", psi)
    required = {
        "V0": params.V0,
        "lambda_phi": params.lambda_phi,
        "Phi_c": params.Phi_c,
        "m_psi": params.m_psi,
        "E_th": params.E_th,
        "lambda_psi": params.lambda_psi,
    }
    for name, value in required.items():
        _finite_real_scalar(name, value)
    if params.V0 <= 0.0 or params.lambda_phi < 0.0:
        raise ValueError("V0 must be positive and lambda_phi non-negative")
    if params.Phi_c <= 0.0 or params.m_psi <= 0.0 or params.E_th <= 0.0:
        raise ValueError("Phi_c, m_psi and E_th must be positive")
    if params.lambda_psi < 0.0:
        raise ValueError("lambda_psi must be non-negative")

    x = params.lambda_phi * (phi / M_PL) ** 2
    c_psi = params.alpha * params.m_psi**2 / params.E_th**2
    d2v_phi = (
        2.0 * params.V0 * params.lambda_phi / M_PL**2
        * np.exp(-x) * (1.0 - 2.0 * x)
        + c_psi * waterfall**2
    )
    mixed = 2.0 * c_psi * phi * waterfall
    d2v_psi = (
        float(meff_sq_psi(phi, params))
        + 3.0 * params.lambda_psi * waterfall**2
    )
    hessian = np.array([[d2v_phi, mixed], [mixed, d2v_psi]], dtype=float)
    if not np.all(np.isfinite(hessian)):
        raise ValueError("PTUM scalar Hessian overflowed or became non-finite")
    return hessian


def scalar_heat_kernel_a2(
    hessian_gev2: np.ndarray,
    xi: float | tuple[float, ...] | list[float] | np.ndarray,
    *,
    ricci_scalar_gev2: float,
    riemann_squared_gev4: float,
    ricci_tensor_squared_gev4: float,
) -> dict[str, object]:
    """Return the bulk a_2 coefficient for N coupled real scalar fields.

    For D_E = -nabla_E^2 I + H + Xi R_E, with trivial field-space
    connection, modulo covariant total derivatives:
      a_2 = 1/2 tr[(H + (Xi - I/6) R_E)^2]
            + N/180 (Riemann^2 - RicciTensor^2).

    Inputs H and R have units GeV^2; curvature squares have units GeV^4.
    Only a_2 is returned. No pole prefactor or counterterm sign is chosen.
    """
    hessian = np.asarray(hessian_gev2, dtype=float)
    if hessian.ndim != 2 or hessian.shape[0] == 0 or hessian.shape[0] != hessian.shape[1]:
        raise ValueError("hessian_gev2 must be a non-empty square matrix")
    if not np.all(np.isfinite(hessian)):
        raise ValueError("hessian_gev2 must contain only finite real values")
    scale = max(1.0, float(np.max(np.abs(hessian))))
    if not np.allclose(hessian, hessian.T, rtol=0.0, atol=1.0e-12 * scale):
        raise ValueError("hessian_gev2 must be symmetric")

    xi_values = np.asarray(xi, dtype=float)
    if xi_values.ndim == 0:
        xi_values = np.full(hessian.shape[0], float(xi_values), dtype=float)
    if xi_values.shape != (hessian.shape[0],) or not np.all(np.isfinite(xi_values)):
        raise ValueError("xi must be a finite scalar or one value per scalar field")

    ricci = _finite_real_scalar("ricci_scalar_gev2", ricci_scalar_gev2)
    riemann_sq = _finite_real_scalar("riemann_squared_gev4", riemann_squared_gev4)
    ricci_tensor_sq = _finite_real_scalar(
        "ricci_tensor_squared_gev4", ricci_tensor_squared_gev4
    )
    shifted = hessian + np.diag((xi_values - 1.0 / 6.0) * ricci)
    mass_curvature = 0.5 * float(np.trace(shifted @ shifted))
    n_fields = int(hessian.shape[0])
    geometry = (n_fields / 180.0) * (riemann_sq - ricci_tensor_sq)
    total = mass_curvature + geometry
    if not np.all(np.isfinite([mass_curvature, geometry, total])):
        raise ValueError("heat-kernel coefficient is non-finite")

    return {
        "a2_mass_curvature_GeV4": mass_curvature,
        "a2_geometry_GeV4": geometry,
        "a2_bulk_GeV4": total,
        "shifted_hessian_GeV2": shifted.tolist(),
        "field_count": n_fields,
        "assumptions": {
            "operator": "D_E=-nabla_E^2 I + Hessian(V) + Xi R_E",
            "curvature_inputs_use_euclidean_laplace_type_convention": True,
            "canonical_scalar_field_space_connection_is_trivial": True,
            "covariant_total_derivatives_omitted": True,
            "boundary_and_initial_surface_terms_included": False,
            "dimensional_regularization_pole_prefactor_applied": False,
            "finite_renormalization_conditions_fixed": False,
            "renormalized_stress_tensor_computed": False,
            "real_time_CTP_finite_part_computed": False,
            "SM_gauge_and_fermion_loops_included": False,
            "graviton_loops_included": False,
            "physical_prediction": False,
        },
    }


def ptum_scalar_heat_kernel_a2(
    Phi: float,
    psi: float,
    params: PTUMParameters,
    *,
    xi_phi: float,
    xi_psi: float,
    ricci_scalar_gev2: float,
    riemann_squared_gev4: float,
    ricci_tensor_squared_gev4: float,
) -> dict[str, object]:
    """Evaluate the coupled (Phi,psi) scalar-sector a_2 coefficient.

    xi_phi and xi_psi are explicit renormalized curvature-coupling inputs.
    Their finite values and renormalization scale are not selected here.
    """
    hessian = ptum_scalar_hessian(Phi, psi, params)
    result = scalar_heat_kernel_a2(
        hessian,
        (xi_phi, xi_psi),
        ricci_scalar_gev2=ricci_scalar_gev2,
        riemann_squared_gev4=riemann_squared_gev4,
        ricci_tensor_squared_gev4=ricci_tensor_squared_gev4,
    )
    result["field_basis"] = ["Phi", "psi"]
    result["background"] = {
        "Phi_GeV": float(Phi),
        "psi_GeV": float(psi),
        "xi_phi": float(xi_phi),
        "xi_psi": float(xi_psi),
    }
    return result
