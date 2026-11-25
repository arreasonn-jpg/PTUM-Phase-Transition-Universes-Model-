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


def ptum_scalar_heat_kernel_a2_decomposition(
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
    """Expand the same two-field a_2 coefficient into local operator pieces.

    This algebraic decomposition is useful for specifying an EFT
    counterterm basis. It does not select which operators are retained or
    assign finite renormalization conditions.
    """
    phi = _finite_real_scalar("Phi", Phi)
    waterfall = _finite_real_scalar("psi", psi)
    xi_phi_value = _finite_real_scalar("xi_phi", xi_phi)
    xi_psi_value = _finite_real_scalar("xi_psi", xi_psi)
    ricci = _finite_real_scalar("ricci_scalar_gev2", ricci_scalar_gev2)
    riemann_sq = _finite_real_scalar("riemann_squared_gev4", riemann_squared_gev4)
    ricci_tensor_sq = _finite_real_scalar(
        "ricci_tensor_squared_gev4", ricci_tensor_squared_gev4
    )

    x = params.lambda_phi * (phi / M_PL) ** 2
    u_phi = (
        2.0 * params.V0 * params.lambda_phi / M_PL**2
        * np.exp(-x) * (1.0 - 2.0 * x)
    )
    m2_psi = float(meff_sq_psi(phi, params))
    c_psi = params.alpha * params.m_psi**2 / params.E_th**2
    delta_xi_phi = xi_phi_value - 1.0 / 6.0
    delta_xi_psi = xi_psi_value - 1.0 / 6.0
    lam = params.lambda_psi

    components = {
        "phi_self_potential_GeV4": 0.5 * u_phi**2,
        "waterfall_mass_potential_GeV4": 0.5 * m2_psi**2,
        "mixed_quadratic_psi2_GeV4": (
            u_phi * c_psi
            + 3.0 * lam * m2_psi
            + 4.0 * c_psi**2 * phi**2
        ) * waterfall**2,
        "quartic_psi4_GeV4": 0.5 * (c_psi**2 + 9.0 * lam**2) * waterfall**4,
        "linear_curvature_GeV4": ricci * (
            delta_xi_phi * u_phi + delta_xi_psi * m2_psi
        ),
        "curvature_psi2_GeV4": ricci * waterfall**2 * (
            delta_xi_phi * c_psi + 3.0 * delta_xi_psi * lam
        ),
        "curvature_squared_GeV4": 0.5 * ricci**2 * (
            delta_xi_phi**2 + delta_xi_psi**2
        ),
        "geometry_GeV4": (2.0 / 180.0) * (riemann_sq - ricci_tensor_sq),
    }
    total = float(sum(components.values()))
    matrix_result = ptum_scalar_heat_kernel_a2(
        phi,
        waterfall,
        params,
        xi_phi=xi_phi_value,
        xi_psi=xi_psi_value,
        ricci_scalar_gev2=ricci,
        riemann_squared_gev4=riemann_sq,
        ricci_tensor_squared_gev4=ricci_tensor_sq,
    )
    residual = total - float(matrix_result["a2_bulk_GeV4"])
    scale = max(1.0, sum(abs(value) for value in components.values()))
    if abs(residual) > 5.0e-13 * scale:
        raise ArithmeticError("expanded a_2 decomposition disagrees with matrix trace")

    return {
        "components_GeV4": components,
        "a2_bulk_GeV4": total,
        "matrix_identity_residual_GeV4": residual,
        "operator_basis": [
            "1",
            "Phi^2",
            "Phi^4",
            "V_eff''(Phi)^2",
            "R",
            "R*Phi^2",
            "R*V_eff''(Phi)",
            "R^2",
            "Riemann^2",
            "RicciTensor^2",
            "psi^2",
            "psi^2*V_eff''(Phi)",
            "psi^2*m_eff^2(Phi)",
            "Phi^2*psi^2",
            "psi^4",
            "R*psi^2",
        ],
        "assumptions": matrix_result["assumptions"],
    }


def scalar_one_loop_pole_coefficients(a2_bulk_gev4: float) -> dict[str, object]:
    """Return scalar-sector Euclidean one-loop simple-pole coefficients.

    Convention: Gamma_E^(1) = +1/2 Tr ln(D_E), dimensional
    regularization d = 4 - epsilon with epsilon = 4-d. For the local
    bulk heat-kernel coefficient defined above,

        Gamma_E,div^(1) / integral(sqrt(g_E)) =
            - a2_bulk / (16 pi^2 epsilon),

    so the cancelling Euclidean local counterterm density has the
    opposite coefficient. This returns the coefficients multiplying
    1/epsilon; it does not insert a renormalization scale, choose an
    MS-bar finite constant, or define finite renormalization conditions.
    Boundary/initial-surface and real-time CTP terms are outside this
    bulk Euclidean result.
    """
    a2 = _finite_real_scalar("a2_bulk_gev4", a2_bulk_gev4)
    pole_coefficient = a2 / (16.0 * np.pi**2)
    gamma_divergence = -pole_coefficient
    counterterm = pole_coefficient
    return {
        "a2_bulk_GeV4": a2,
        "dimensional_regularization": "d=4-epsilon, epsilon=4-d",
        "one_loop_effective_action_convention": "Gamma_E^(1)=+1/2 Tr ln(D_E)",
        "pole_factor": "1/epsilon",
        "gamma1_divergent_density_coefficient_GeV4": gamma_divergence,
        "euclidean_counterterm_density_coefficient_GeV4": counterterm,
        "pole_cancellation_residual_GeV4": gamma_divergence + counterterm,
        "assumptions": {
            "scalar_bulk_heat_kernel_only": True,
            "covariant_total_derivatives_omitted": True,
            "boundary_and_initial_surface_terms_included": False,
            "renormalization_scale_inserted": False,
            "msbar_finite_constant_inserted": False,
            "finite_renormalization_conditions_fixed": False,
            "finite_effective_action_computed": False,
            "renormalized_stress_tensor_computed": False,
            "real_time_CTP_finite_part_computed": False,
            "SM_gauge_fermion_and_graviton_loops_included": False,
            "physical_prediction": False,
        },
    }


def ptum_scalar_one_loop_pole_field_gradients(
    Phi: float,
    psi: float,
    params: PTUMParameters,
    *,
    xi_phi: float,
    xi_psi: float,
    ricci_scalar_gev2: float,
) -> dict[str, object]:
    """Return field derivatives of the scalar bulk a2 and its simple pole.

    Curvature invariants are held fixed while differentiating with respect
    to the two background fields. Since the geometric a2 term is
    field-independent, d a2/dvarphi = tr[A dH/dvarphi], where
    A = H + (Xi - I/6) R_E. This is the derivative of the local Euclidean
    bulk pole only, not a finite or renormalized real-time force.
    """
    phi = _finite_real_scalar("Phi", Phi)
    waterfall = _finite_real_scalar("psi", psi)
    xi_phi_value = _finite_real_scalar("xi_phi", xi_phi)
    xi_psi_value = _finite_real_scalar("xi_psi", xi_psi)
    ricci = _finite_real_scalar("ricci_scalar_gev2", ricci_scalar_gev2)
    alpha = _finite_real_scalar("alpha", params.alpha)

    hessian = ptum_scalar_hessian(phi, waterfall, params)
    c_psi = alpha * params.m_psi**2 / params.E_th**2
    x = params.lambda_phi * (phi / M_PL)**2
    v_eff_third = (
        4.0 * params.V0 * params.lambda_phi**2 * phi / M_PL**4
        * np.exp(-x) * (2.0 * x - 3.0)
    )

    hessian_phi = np.array(
        [
            [v_eff_third, 2.0 * c_psi * waterfall],
            [2.0 * c_psi * waterfall, 2.0 * c_psi * phi],
        ],
        dtype=float,
    )
    hessian_psi = np.array(
        [
            [2.0 * c_psi * waterfall, 2.0 * c_psi * phi],
            [2.0 * c_psi * phi, 6.0 * params.lambda_psi * waterfall],
        ],
        dtype=float,
    )
    shifted_hessian = hessian + np.diag(
        np.array([xi_phi_value, xi_psi_value], dtype=float) - 1.0 / 6.0
    ) * ricci
    da2_dphi = float(np.trace(shifted_hessian @ hessian_phi))
    da2_dpsi = float(np.trace(shifted_hessian @ hessian_psi))
    derivatives = np.array([da2_dphi, da2_dpsi], dtype=float)
    if not np.all(np.isfinite(derivatives)):
        raise ValueError("scalar heat-kernel field gradient is non-finite")

    loop_factor = 1.0 / (16.0 * np.pi**2)
    gamma_gradient = -loop_factor * derivatives
    counterterm_gradient = loop_factor * derivatives
    return {
        "field_basis": ["Phi", "psi"],
        "a2_field_gradient_GeV3": {
            "Phi": da2_dphi,
            "psi": da2_dpsi,
        },
        "gamma1_divergent_density_field_gradient_coefficient_GeV3": {
            "Phi": float(gamma_gradient[0]),
            "psi": float(gamma_gradient[1]),
        },
        "euclidean_counterterm_density_field_gradient_coefficient_GeV3": {
            "Phi": float(counterterm_gradient[0]),
            "psi": float(counterterm_gradient[1]),
        },
        "pole_factor": "1/epsilon",
        "hessian_field_derivatives_GeV": {
            "Phi": hessian_phi.tolist(),
            "psi": hessian_psi.tolist(),
        },
        "assumptions": {
            "curvature_invariants_held_fixed_in_field_derivative": True,
            "scalar_bulk_heat_kernel_only": True,
            "boundary_and_initial_surface_terms_included": False,
            "finite_effective_action_computed": False,
            "renormalized_real_time_force_computed": False,
            "renormalized_stress_tensor_computed": False,
            "physical_prediction": False,
        },
    }



def ptum_scalar_one_loop_pole_metric_variation(
    Phi: float,
    psi: float,
    params: PTUMParameters,
    *,
    xi_phi: float,
    xi_psi: float,
    metric_euclidean: np.ndarray,
    ricci_tensor_euclidean_gev2: np.ndarray,
    ricci_scalar_euclidean_gev2: float,
    riemann_tensor_euclidean_gev2: np.ndarray,
    box_ricci_tensor_euclidean_gev4: np.ndarray,
    hessian_ricci_scalar_euclidean_gev4: np.ndarray,
    hessian_F_euclidean_gev4: np.ndarray,
) -> dict[str, object]:
    """Vary the local two-scalar bulk a2 pole with respect to g_E^{mu nu}.

    Tensor slots of riemann_tensor_euclidean_gev2 are ordered
    R_{mu alpha nu beta}.  The Euclidean metric is positive definite and
    uses the analytic continuation of the manuscript's MTW Riemann
    convention.  The supplied covariant derivative data are
    Box(R_{mu nu}), nabla_mu nabla_nu R, and nabla_mu nabla_nu F,
    respectively.  Their contractions are checked before use.

    In exactly four dimensions, modulo the Euler density and boundary
    terms, the local coefficient is
        a2 = U + F R + A R^2 + B R_{mu nu} R^{mu nu},
    where U=tr(H^2)/2, F=tr[(Xi-I/6)H],
    A=tr[(Xi-I/6)^2]/2-N/180, and B=N/60.
    The returned tensor is (1/sqrt(g_E)) delta int sqrt(g_E) a2 /
    delta g_E^{mu nu}.  It is a metric Euler derivative of the divergent
    local coefficient, not a renormalized stress tensor or a finite
    in-in source.  The four-dimensional Euler term has zero bulk
    variation; its boundary and dimensional-continuation finite pieces
    are not represented.
    """
    phi = _finite_real_scalar("Phi", Phi)
    waterfall = _finite_real_scalar("psi", psi)
    xi_phi_value = _finite_real_scalar("xi_phi", xi_phi)
    xi_psi_value = _finite_real_scalar("xi_psi", xi_psi)

    def tensor(name: str, value: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
        raw = np.asarray(value)
        if raw.dtype.kind == "b":
            raise ValueError(f"{name} must contain finite real tensor components")
        try:
            array = np.asarray(value, dtype=float)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{name} must contain finite real tensor components"
            ) from exc
        if array.shape != shape or not np.all(np.isfinite(array)):
            raise ValueError(
                f"{name} must have shape {shape} and finite real components"
            )
        return array

    metric = tensor("metric_euclidean", metric_euclidean, (4, 4))
    metric_scale = max(1.0, float(np.max(np.abs(metric))))
    if not np.allclose(
        metric, metric.T, rtol=0.0, atol=1.0e-12 * metric_scale
    ):
        raise ValueError("metric_euclidean must be symmetric")
    try:
        np.linalg.cholesky(metric)
        inverse_metric = np.linalg.inv(metric)
    except np.linalg.LinAlgError as exc:
        raise ValueError("metric_euclidean must be positive definite") from exc

    ricci = tensor(
        "ricci_tensor_euclidean_gev2", ricci_tensor_euclidean_gev2, (4, 4)
    )
    ricci_scale = max(1.0, float(np.max(np.abs(ricci))))
    if not np.allclose(ricci, ricci.T, rtol=0.0, atol=1.0e-10 * ricci_scale):
        raise ValueError("ricci_tensor_euclidean_gev2 must be symmetric")
    scalar_ricci = _finite_real_scalar(
        "ricci_scalar_euclidean_gev2", ricci_scalar_euclidean_gev2
    )
    riemann = tensor(
        "riemann_tensor_euclidean_gev2",
        riemann_tensor_euclidean_gev2,
        (4, 4, 4, 4),
    )
    riemann_scale = max(1.0, float(np.max(np.abs(riemann))))
    riemann_atol = 1.0e-9 * riemann_scale
    if not np.allclose(
        riemann, -riemann.swapaxes(0, 1), rtol=0.0, atol=riemann_atol
    ):
        raise ValueError("Riemann tensor must be antisymmetric in its first pair")
    if not np.allclose(
        riemann, -riemann.swapaxes(2, 3), rtol=0.0, atol=riemann_atol
    ):
        raise ValueError("Riemann tensor must be antisymmetric in its second pair")
    if not np.allclose(
        riemann, riemann.transpose(2, 3, 0, 1),
        rtol=0.0, atol=riemann_atol,
    ):
        raise ValueError("Riemann tensor must have pair-exchange symmetry")
    riemann_bianchi = (
        riemann
        + riemann.transpose(0, 2, 3, 1)
        + riemann.transpose(0, 3, 1, 2)
    )
    if not np.allclose(
        riemann_bianchi, 0.0, rtol=0.0, atol=3.0 * riemann_atol
    ):
        raise ValueError("Riemann tensor must satisfy the first Bianchi identity")

    ricci_from_riemann = np.einsum(
        "mn,manb->ab", inverse_metric, riemann
    )
    curvature_scale = max(
        1.0,
        float(np.max(np.abs(ricci))),
        float(np.max(np.abs(ricci_from_riemann))),
    )
    if not np.allclose(
        ricci_from_riemann, ricci,
        rtol=1.0e-9, atol=1.0e-10 * curvature_scale,
    ):
        raise ValueError("Ricci tensor is inconsistent with the Riemann contraction")
    scalar_from_ricci = float(np.einsum("mn,mn", inverse_metric, ricci))
    if not np.isclose(
        scalar_from_ricci, scalar_ricci,
        rtol=1.0e-9, atol=1.0e-10 * max(1.0, abs(scalar_ricci)),
    ):
        raise ValueError("Ricci scalar is inconsistent with the Ricci tensor")

    box_ricci = tensor(
        "box_ricci_tensor_euclidean_gev4",
        box_ricci_tensor_euclidean_gev4,
        (4, 4),
    )
    if not np.allclose(
        box_ricci, box_ricci.T, rtol=0.0,
        atol=1.0e-10 * max(1.0, float(np.max(np.abs(box_ricci)))),
    ):
        raise ValueError("Box(Ricci tensor) must be symmetric")
    hessian_ricci = tensor(
        "hessian_ricci_scalar_euclidean_gev4",
        hessian_ricci_scalar_euclidean_gev4,
        (4, 4),
    )
    hessian_F = tensor(
        "hessian_F_euclidean_gev4", hessian_F_euclidean_gev4, (4, 4)
    )
    for name, hessian in (
        ("Hessian(R)", hessian_ricci),
        ("Hessian(F)", hessian_F),
    ):
        if not np.allclose(
            hessian, hessian.T, rtol=0.0,
            atol=1.0e-10 * max(1.0, float(np.max(np.abs(hessian)))),
        ):
            raise ValueError(f"{name} must be symmetric")

    box_R = float(np.einsum("mn,mn", inverse_metric, hessian_ricci))
    box_R_from_ricci = float(np.einsum("mn,mn", inverse_metric, box_ricci))
    if not np.isclose(
        box_R_from_ricci, box_R,
        rtol=1.0e-9, atol=1.0e-10 * max(1.0, abs(box_R)),
    ):
        raise ValueError("Box(R) must equal the metric trace of Box(Ricci tensor)")
    box_F = float(np.einsum("mn,mn", inverse_metric, hessian_F))

    hessian = ptum_scalar_hessian(phi, waterfall, params)
    delta_xi = np.diag(
        [xi_phi_value - 1.0 / 6.0, xi_psi_value - 1.0 / 6.0]
    )
    field_count = int(hessian.shape[0])
    if field_count != 2:
        raise ArithmeticError("PTUM scalar pole variation expects two real scalar fields")
    U = 0.5 * float(np.trace(hessian @ hessian))
    F = float(np.trace(delta_xi @ hessian))
    A = 0.5 * float(np.trace(delta_xi @ delta_xi)) - field_count / 180.0
    B = field_count / 60.0

    ricci_up = inverse_metric @ ricci @ inverse_metric
    ricci_squared = float(np.einsum("mn,mn", ricci, ricci_up))
    riemann_squared = float(np.einsum(
        "mr,as,nl,bk,manb,rslk",
        inverse_metric, inverse_metric, inverse_metric, inverse_metric,
        riemann, riemann,
    ))
    geometry = (field_count / 180.0) * (
        riemann_squared - ricci_squared
    )
    a2_bulk = (
        0.5 * float(np.trace(
            (hessian + delta_xi * scalar_ricci)
            @ (hessian + delta_xi * scalar_ricci)
        ))
        + geometry
    )

    einstein = ricci - 0.5 * metric * scalar_ricci
    H1 = (
        2.0 * scalar_ricci * ricci
        - 0.5 * metric * scalar_ricci**2
        - 2.0 * hessian_ricci
        + 2.0 * metric * box_R
    )
    H2 = (
        2.0 * np.einsum("manb,ab->mn", riemann, ricci_up)
        - 0.5 * metric * ricci_squared
        - hessian_ricci
        + 0.5 * metric * box_R
        + box_ricci
    )
    metric_components = {
        "volume_potential_term_GeV4": -0.5 * metric * U,
        "field_curvature_term_GeV4": (
            F * einstein + metric * box_F - hessian_F
        ),
        "ricci_scalar_squared_term_GeV4": A * H1,
        "ricci_tensor_squared_term_GeV4": B * H2,
    }
    metric_euler = sum(metric_components.values())
    if not np.all(np.isfinite(metric_euler)) or not np.isfinite(a2_bulk):
        raise ValueError("scalar pole metric variation is non-finite")

    loop_factor = 1.0 / (16.0 * np.pi**2)
    return {
        "field_basis": ["Phi", "psi"],
        "a2_bulk_GeV4": float(a2_bulk),
        "a2_operator_coefficients": {
            "U_GeV4": U,
            "F_GeV2": F,
            "A_dimensionless": A,
            "B_dimensionless": B,
            "ricci_squared_GeV4": ricci_squared,
            "riemann_squared_GeV4": riemann_squared,
        },
        "metric_variation_components_GeV4": {
            name: value.tolist() for name, value in metric_components.items()
        },
        "curvature_variation_tensors_GeV4": {
            "H1_R_squared": H1.tolist(),
            "H2_Ricci_squared": H2.tolist(),
        },
        "metric_euler_derivative_a2_GeV4": metric_euler.tolist(),
        "metric_euler_derivative_trace_GeV4": float(
            np.einsum("mn,mn", inverse_metric, metric_euler)
        ),
        "gamma1_divergent_metric_euler_derivative_coefficient_GeV4": (
            -loop_factor * metric_euler
        ).tolist(),
        "euclidean_counterterm_metric_euler_derivative_coefficient_GeV4": (
            loop_factor * metric_euler
        ).tolist(),
        "pole_factor": "1/epsilon",
        "variation_variable": "inverse Euclidean metric g_E^{mu nu}",
        "assumptions": {
            "operator": "D_E=-nabla_E^2 I+Hessian(V)+Xi R_E",
            "euclidean_metric_positive_definite": True,
            "riemann_slots": "R_{mu alpha nu beta}",
            "riemann_convention": "analytic continuation of the manuscript MTW convention",
            "curvature_and_covariant_derivative_tensors_are_caller_supplied": True,
            "four_dimensional_euler_density_dropped_from_bulk_variation": True,
            "boundary_and_initial_surface_terms_included": False,
            "dimensional_continuation_finite_terms_included": False,
            "result_is_metric_euler_derivative_not_stress_tensor": True,
            "finite_renormalization_conditions_fixed": False,
            "renormalized_stress_tensor_computed": False,
            "real_time_CTP_finite_part_computed": False,
            "SM_gauge_fermion_and_graviton_loops_included": False,
            "physical_prediction": False,
        },
    }
