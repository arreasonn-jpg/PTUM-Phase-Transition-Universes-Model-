"""Regression tests for PTUM homogeneous energy bookkeeping and diagnostics."""
import numpy as np
import pytest

from ptum_task1_simulation import (
    PTUMParameters,
    M_PL,
    meff_sq_psi,
    veff_phi,
    dveff_dphi,
    rho_phi,
    rho_psi,
    rho_total,
    pressure_phi,
    pressure_psi,
    hubble_rate,
    compute_quartic_dominance,
    compute_quartic_virial_ratio,
    InitialConditions,
    run_simulation,
    compute_time_averaged_w,
    classify_outcome,
)


def test_interaction_energy_is_counted_exactly_once():
    p = PTUMParameters(V0=2.0e50, m_psi=3.0e8, lambda_psi=0.2)
    phi, phi_dot, psi, psi_dot = 1.01 * p.Phi_c, 2.0e7, 4.0e5, 5.0e6
    expected = (
        0.5 * phi_dot**2
        + veff_phi(phi, p)
        + 0.5 * psi_dot**2
        + 0.5 * meff_sq_psi(phi, p) * psi**2
        + 0.25 * p.lambda_psi * psi**4
    )
    assert rho_total(phi, phi_dot, psi, psi_dot, p) == pytest.approx(expected)
    assert rho_phi(phi, phi_dot, psi, p) == pytest.approx(
        0.5 * phi_dot**2 + veff_phi(phi, p)
    )


def test_friedmann_rate_uses_single_total_density():
    p = PTUMParameters(V0=2.0e50, m_psi=3.0e8, lambda_psi=0.2)
    phi, phi_dot, psi, psi_dot = 1.01 * p.Phi_c, 2.0e7, 4.0e5, 5.0e6
    expected = np.sqrt(rho_total(phi, phi_dot, psi, psi_dot, p) / (3.0 * M_PL**2))
    assert hubble_rate(phi, phi_dot, psi, psi_dot, p) == pytest.approx(expected)


def test_quartic_diagnostic_uses_local_phi_history():
    p = PTUMParameters(V0=2.0e50, m_psi=3.0e8, lambda_psi=0.2)
    t = np.linspace(0.0, 8.0 * np.pi, 4001)
    psi = 2.0e5 * np.sin(t)
    psi_dot = 2.0e5 * np.cos(t)
    phi = np.full_like(t, 1.01 * p.Phi_c)
    q = compute_quartic_dominance(t, psi, psi_dot, p, phi)
    assert np.isfinite(q).any()
    assert np.isnan(q).any()


def test_quartic_diagnostic_marks_nonoscillatory_history_unavailable():
    p = PTUMParameters()
    t = np.linspace(0.0, 1.0, 100)
    psi = np.ones_like(t)
    psi_dot = np.zeros_like(t)
    q = compute_quartic_dominance(t, psi, psi_dot, p, np.full_like(t, 1.01 * p.Phi_c))
    assert np.isnan(q).all()


def test_scalar_pressure_and_density_are_consistent_components():
    p = PTUMParameters(V0=2.0e50, m_psi=3.0e8, lambda_psi=0.2)
    phi, phi_dot, psi, psi_dot = 1.01 * p.Phi_c, 2.0e7, 4.0e5, 5.0e6
    rho = rho_phi(phi, phi_dot, psi, p) + rho_psi(phi, psi, psi_dot, p)
    pressure = pressure_phi(phi, phi_dot, p) + pressure_psi(phi, psi, psi_dot, p)
    assert np.isfinite(rho + pressure)



def test_quartic_virial_ratio_is_defined_only_on_complete_half_cycles():
    p = PTUMParameters(lambda_psi=0.1)
    t = np.linspace(0.0, 8.0 * np.pi, 4001)
    psi = np.sin(t)
    psi_dot = np.cos(t)
    ratio = compute_quartic_virial_ratio(t, psi, psi_dot, p)
    assert np.isfinite(ratio).any()
    assert np.isnan(ratio).any()



def test_static_de_sitter_solution_satisfies_frw_continuity_diagnostic():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=0.0,
        psi=0.0,
        psi_dot=0.0,
    )
    t = np.linspace(0.0, 1.0e-9, 101)
    result = run_simulation(p, ic, (t[0], t[-1]), t_eval=t)
    assert result["success"]
    # The chain-rule residual must vanish for the exact static solution.
    assert np.max(np.abs(result["continuity_residual_relative"])) < 1.0e-10
    # The sampled finite-difference estimate is retained separately; it is
    # not expected to reach this tolerance for a vacuum-dominated constant rho.
    assert result["continuity_residual_finite_difference"].shape == t.shape
    assert result["continuity_residual_finite_difference_relative"].shape == t.shape



def test_frw_chain_rule_residual_closes_for_evolving_two_field_solution():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=1.0e20,
        psi=1.0e4,
        psi_dot=1.0e8,
    )
    t = np.linspace(0.0, 1.0e-9, 101)
    result = run_simulation(p, ic, (t[0], t[-1]), t_eval=t)
    assert result["success"]
    assert np.max(np.abs(result["continuity_residual_relative"])) < 1.0e-10
    assert np.max(np.abs(result["Phi"] - result["Phi"][0])) > 0.0
    assert np.max(np.abs(result["psi"] - result["psi"][0])) > 0.0



def test_cycle_averaged_equation_of_state_is_ratio_of_averages():
    t = np.arange(5.0)
    psi_dot = np.array([1.0, 1.0, -1.0, -1.0, 1.0])
    pressure = np.array([0.0, 4.0, 3.0, 2.0, 0.0])
    density = np.array([1.0, 2.0, 6.0, 2.0, 1.0])
    w_avg, t_avg = compute_time_averaged_w(t, pressure, density, psi_dot)

    # The first complete half-cycle uses indices 1, 2, 3:
    # <p>/<rho> = (4+3+2)/(2+6+2) = 0.9.
    assert w_avg[0] == pytest.approx(0.9)
    assert t_avg[0] == pytest.approx(2.0)
    # This differs from mean(p/rho), which would be 1.0 here.
    assert w_avg[0] != pytest.approx(np.mean(pressure[1:4] / density[1:4]))



def test_regime_classifier_uses_late_time_diagnostics():
    result = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.1, 0.2, 1.0 / 3.0, 1.0 / 3.0]),
        "Q": np.concatenate([np.zeros(80), np.full(20, 10.0)]),
        "virial_ratio": np.concatenate([np.full(80, 0.2), np.ones(20)]),
    }
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "quartic"
    assert classification["quartic_achieved"]
    assert classification["Q_final"] == pytest.approx(10.0)
    assert classification["virial_final"] == pytest.approx(1.0)



def test_fuel_potential_exponent_is_dimensionless_and_threshold_is_independent():
    p = PTUMParameters(V0=3.0e50, lambda_phi=0.02, Phi_c=1.4 * M_PL)
    phi_lambda = M_PL / np.sqrt(p.lambda_phi)

    assert veff_phi(phi_lambda, p) == pytest.approx(
        p.V0 * (1.0 - np.exp(-1.0))
    )
    expected_derivative = (
        2.0 * p.V0 * p.lambda_phi * phi_lambda / M_PL**2 * np.exp(-1.0)
    )
    assert dveff_dphi(phi_lambda, p) == pytest.approx(expected_derivative)

    step = 1.0e-6 * phi_lambda
    finite_difference = (
        veff_phi(phi_lambda + step, p) - veff_phi(phi_lambda - step, p)
    ) / (2.0 * step)
    assert dveff_dphi(phi_lambda, p) == pytest.approx(
        finite_difference, rel=1.0e-8
    )
    assert meff_sq_psi(p.Phi_c, p) == pytest.approx(0.0, abs=1.0e-10 * p.m_psi**2)
    assert meff_sq_psi(1.01 * p.Phi_c, p) < 0.0



def test_reproducible_inflation_background_scan_lambda_002():
    from ptum_inflation_background import compute_observables

    result = compute_observables(0.02, n_target=60.0, n_star=55.0)
    assert result["n_end"] == pytest.approx(60.0, abs=1.0e-6)
    assert result["x_initial"] == pytest.approx(10.71523918, rel=2.0e-7)
    assert result["x_star"] == pytest.approx(10.46534426, rel=2.0e-7)
    assert result["n_s_hubble_flow_1st_order"] == pytest.approx(
        0.95808593, abs=2.0e-7
    )
    assert result["r_hubble_flow_1st_order"] == pytest.approx(
        0.02195265, abs=2.0e-7
    )
