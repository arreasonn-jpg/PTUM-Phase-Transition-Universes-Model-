"""Regression tests for PTUM homogeneous energy bookkeeping and diagnostics."""
import json

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from ptum_full_grid_convergence import (
    EXPECTED_ROWS as FULL_GRID_EXPECTED_ROWS,
    N_POINTS as FULL_GRID_N_POINTS,
    RTOL as FULL_GRID_RTOL,
    ATOL as FULL_GRID_ATOL,
    MAX_RHS_EVALUATIONS as FULL_GRID_MAX_RHS,
    json_safe as full_grid_json_safe,
)
from ptum_scan_convergence import (
    CASES as CONVERGENCE_CASES,
    OUTPUT_GRIDS,
    TOLERANCE_LEVELS,
    TARGETED_GRID_LIMITS,
    TARGETED_TOLERANCE_LIMITS,
    _compare_records,
    _finite_float,
    relative_difference,
)

from ptum_task1_simulation import (
    DEFAULT_MAX_RHS_EVALUATIONS,
    RHSWorkBudgetExceeded,
    RHSIntegrationError,
    PTUMParameters,
    background_equations,
    dimensionless_state_scales,
    dimensionless_state_scale_metadata,
    dimensionless_background_equations,
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
    compute_quadratic_virial_ratio,
    waterfall_transfer_rate,
    w_psi,
    psi_minimum_potential,
    psi_minimum_squared,
    psi_excitation_potential,
    psi_excitation_energy,
    psi_excitation_pressure,
    waterfall_excitation_transfer_rate,
    InitialConditions,
    create_initial_conditions,
    run_simulation,
    compute_time_averaged_w,
    compute_dense_cycle_diagnostics,
    classify_outcome,
    run_parameter_scan,
    save_results,
)


def _add_fast_adiabatic_oscillation_history(result, hubble=0.01, t_end=100.0):
    t = np.linspace(0.0, t_end, 10001)
    result.update({
        "t": t,
        "H": np.full_like(t, hubble),
        "psi": np.cos(t),
        "psi_dot": -np.sin(t),
    })
    return result


def _minimal_successful_scan_row(*, classification=None, scan_metadata=None):
    """Return a complete two-sample success record for strict-JSON tests."""
    return {
        "success": True,
        "classification": classification or {
            "regime": "insufficient_oscillation_data",
            "quartic_achieved": False,
            "w_final": float("nan"),
            "Q_final": float("nan"),
            "virial_final": float("nan"),
            "n_oscillations": 0,
        },
        "ic_params": {"psi_init": 0.0, "psi_dot_init": 0.0, "phi_offset": 0.0},
        "scan_metadata": scan_metadata or {},
        "psi": np.array([0.0, 0.0]),
        "psi_dot": np.array([0.0, 0.0]),
        "Phi": np.array([1.0, 1.0]),
        "Phi_dot": np.array([0.0, 0.0]),
        "H": np.array([1.0, 1.0]),
        "rho_total": np.array([1.0, 1.0]),
        "w_psi_exc": np.array([np.nan, np.nan]),
        "Q": np.array([np.nan, np.nan]),
        "virial_ratio": np.array([np.nan, np.nan]),
        "continuity_residual_relative": np.array([0.0, 0.0]),
        "continuity_residual_finite_difference_background_relative": np.array([0.0, 0.0]),
    }


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



def test_vacuum_dominated_near_static_background_satisfies_frw_continuity_diagnostic():
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
    assert np.allclose(
        result["rho_phi_split"] + result["rho_psi_exc"],
        result["rho_total"], rtol=1.0e-12, atol=1.0e-30
    )
    assert np.allclose(
        result["p_phi_split"] + result["p_psi_exc"],
        result["p_total"], rtol=1.0e-12, atol=1.0e-30
    )
    assert np.allclose(result["Q_psi_exc0"] + result["Q_Phi_split0"], 0.0)
    # The chain-rule residual must vanish for the near-static background.
    assert np.max(np.abs(result["continuity_residual_relative"])) < 1.0e-10
    assert np.max(np.abs(result["continuity_residual_background_relative"])) < 1.0e-10
    assert np.max(np.abs(result["continuity_residual_finite_difference_background_relative"])) < 1.0e-6
    # The sampled finite-difference estimate is retained separately; its
    # local normalization is ill-conditioned when rho is vacuum dominated.
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
    assert np.max(np.abs(result["continuity_residual_background_relative"])) < 1.0e-10
    assert np.max(np.abs(result["continuity_residual_finite_difference_background_relative"])) < 1.0e-6
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
    _add_fast_adiabatic_oscillation_history(result)
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "quartic"
    assert classification["quartic_achieved"]
    assert classification["Q_final"] == pytest.approx(10.0)
    assert classification["virial_final"] == pytest.approx(1.0)
    assert classification["H_over_omega_max"] < 0.1
    assert classification["n_late_half_cycles"] >= 3



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
    assert meff_sq_psi(1.01 * p.Phi_c, p) > 0.0



def test_reproducible_inflation_background_scan():
    from ptum_inflation_background import run_scan

    results = run_scan(n_target=60.0, n_star=55.0)
    assert len(results) == 8
    assert all(row["n_end"] == pytest.approx(60.0, abs=1.0e-6)
               for row in results)

    reference = results[0]
    assert reference["lambda_phi"] == pytest.approx(0.02)
    assert reference["x_initial"] == pytest.approx(10.71523918, rel=2.0e-7)
    assert reference["x_star"] == pytest.approx(10.46534426, rel=2.0e-7)
    assert reference["n_s_hubble_flow_1st_order"] == pytest.approx(
        0.95808593, abs=2.0e-7
    )
    assert reference["r_hubble_flow_1st_order"] == pytest.approx(
        0.02195265, abs=2.0e-7
    )



def test_mathieu_floquet_solver_has_unit_wronskian_and_stable_q_zero():
    from ptum_floquet import floquet_diagnostic

    result = floquet_diagnostic(A_k=0.7, q=0.0)
    assert not result["unstable"]
    assert result["mu_z"] == pytest.approx(0.0)
    assert result["det_monodromy"] == pytest.approx(1.0, abs=1.0e-8)


def test_mathieu_primary_resonance_matches_narrow_band_limit():
    from ptum_floquet import floquet_diagnostic

    q = 0.01
    result = floquet_diagnostic(A_k=1.0, q=q)
    assert result["unstable"]
    # For |q| << 1, the primary-band exponent at A=1 is mu_z ~ |q|/2.
    assert result["mu_z"] == pytest.approx(abs(q) / 2.0, rel=2.0e-3)
    assert result["det_monodromy"] == pytest.approx(1.0, abs=1.0e-8)



def test_damping_ratio_uses_local_threshold_hubble_scale():
    p = PTUMParameters(
        V0=1.0e64,
        lambda_phi=0.02,
        Phi_c=1.4 * M_PL,
        m_psi=1.0e13,
        E_th=1.0e16,
    )
    expected_hc_potential = np.sqrt(veff_phi(p.Phi_c, p) / (3.0 * M_PL**2))
    expected_hc_exact_end = np.sqrt(1.5) * expected_hc_potential
    assert p.H_threshold_potential == pytest.approx(expected_hc_potential)
    assert p.H_threshold_exact_end == pytest.approx(expected_hc_exact_end)
    assert p.damping_ratio_potential == pytest.approx(
        3.0 * expected_hc_potential / (2.0 * p.mu)
    )
    assert p.damping_ratio == pytest.approx(
        3.0 * expected_hc_exact_end / (2.0 * p.mu)
    )
    assert p.damping_ratio > p.damping_ratio_potential
    assert p.damping_ratio < p.damping_ratio_plateau



def test_two_field_parameter_scan_returns_explicit_classification():
    from ptum_task1_simulation import run_parameter_scan

    p = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    results = run_parameter_scan(
        p,
        psi_init_range=[0.01 * p.psi_0],
        psi_dot_init_range=[0.1 * p.mu * p.psi_0],
        phi_offset_range=[0.01 * p.Phi_c],
        t_max=1.0,
        n_points=40,
    )
    assert len(results) == 1
    assert results[0]["success"]
    assert "regime" in results[0]["classification"]
    assert "quartic_achieved" in results[0]["classification"]



def test_high_w_does_not_claim_barrier_crossing_without_a_barrier_diagnostic():
    result = {
        "success": True,
        "w_psi_avg": np.array([0.8, 0.9, 1.0]),
        "Q": np.full(100, 2.0),
        "virial_ratio": np.full(100, 0.4),
    }
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "non_quartic"
    assert "barrier_crossed" not in classification



def test_parameter_scan_calls_result_callback_for_each_completed_trajectory():
    from ptum_task1_simulation import run_parameter_scan

    p = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    observed = []
    results = run_parameter_scan(
        p,
        psi_init_range=[0.01 * p.psi_0],
        psi_dot_init_range=[0.1 * p.mu * p.psi_0],
        phi_offset_range=[0.01 * p.Phi_c],
        t_max=1.0,
        n_points=40,
        result_callback=observed.append,
    )
    assert len(results) == 1
    assert observed == results
    assert observed[0]["success"]


def test_scan_summary_is_strict_json_and_nonfinite_values_become_null(tmp_path):
    from ptum_task1_simulation import save_results

    result = _minimal_successful_scan_row(
        scan_metadata={"scenario": "unit_test", "n_output_points": 101}
    )
    output = tmp_path / "scan.json"
    save_results([result], str(output))
    raw = output.read_text(encoding="utf-8")
    parsed = json.loads(
        raw,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    assert parsed[0]["classification"]["w_final"] is None
    assert parsed[0]["classification"]["Q_final"] is None
    assert "NaN" not in raw
    assert "max_abs_psi_over_trajectory" in parsed[0]
    assert parsed[0]["scan_metadata"]["scenario"] == "unit_test"
    assert parsed[0]["scan_metadata"]["n_output_points"] == 101




def test_scan_summary_replaces_checkpoint_atomically(tmp_path):
    from ptum_task1_simulation import save_results

    result = _minimal_successful_scan_row(
        classification={"regime": "insufficient_oscillation_data"}
    )
    output = tmp_path / "checkpoint.json"
    save_results([result], str(output))
    assert output.exists()
    assert not (tmp_path / "checkpoint.json.tmp").exists()
    assert json.loads(output.read_text(encoding="utf-8"))[0]["ic_params"]["psi_init"] == 0.0


def test_task1_scan_includes_threshold_matched_high_scale_and_low_scale_control():
    from ptum_task1_scan import (
        DEFAULT_N_POINTS,
        build_initial_condition_grid,
        build_scan_scenarios,
    )

    scenarios = dict(build_scan_scenarios())
    assert set(scenarios) == {
        "high_scale_threshold_matched",
        "low_scale_underdamped_control",
    }
    high = scenarios["high_scale_threshold_matched"]
    low = scenarios["low_scale_underdamped_control"]
    assert high.Phi_c / M_PL == pytest.approx(0.9862280831209068, rel=1.0e-8)
    assert high.V0 == pytest.approx(1.0e64)
    assert low.V0 == pytest.approx(1.0e56)
    assert high.damping_ratio > 1.0
    assert low.damping_ratio < 1.0
    assert high.damping_ratio == pytest.approx(4.2858253624, rel=1.0e-8)
    assert high.damping_ratio_potential == pytest.approx(3.4993617549, rel=1.0e-8)
    assert high.damping_ratio == pytest.approx(
        np.sqrt(1.5) * high.damping_ratio_potential
    )
    assert DEFAULT_N_POINTS >= 4001
    psi, psi_dot, offsets = build_initial_condition_grid(high)
    assert len(psi) * len(psi_dot) * len(offsets) == 50
    assert max(psi) == pytest.approx(5.0 * high.psi_0)
    assert max(psi_dot) == pytest.approx(5.0 * high.mu * high.psi_0)



def test_quartic_threshold_matches_potential_energy_dominance():
    base = {
        "success": True,
        "w_psi_avg": np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]),
        "virial_ratio": np.ones(100),
    }
    quartic = dict(base, Q=np.full(100, 2.1))
    non_quartic = dict(base, Q=np.full(100, 1.9))

    _add_fast_adiabatic_oscillation_history(quartic)
    _add_fast_adiabatic_oscillation_history(non_quartic)
    q_class = classify_outcome(quartic, PTUMParameters())
    non_q_class = classify_outcome(non_quartic, PTUMParameters())

    assert q_class["quartic_achieved"]
    assert q_class["quartic_to_tachyonic_potential_ratio"] == pytest.approx(1.05)
    assert not non_q_class["quartic_achieved"]
    assert non_q_class["quartic_to_tachyonic_potential_ratio"] == pytest.approx(0.95)





def test_quartic_classification_rejects_hubble_damped_oscillations():
    result = {
        "success": True,
        "w_psi_avg": np.full(5, 1.0 / 3.0),
        "Q": np.full(100, 2.1),
        "virial_ratio": np.ones(100),
    }
    _add_fast_adiabatic_oscillation_history(result, hubble=0.2)
    classification = classify_outcome(result, PTUMParameters())
    assert not classification["quartic_achieved"]
    assert classification["H_over_omega_max"] >= 0.1
    assert not classification["adiabaticity_valid"]


def test_quartic_classification_requires_three_late_half_cycles():
    result = {
        "success": True,
        "w_psi_avg": np.full(5, 1.0 / 3.0),
        "Q": np.full(100, 2.1),
        "virial_ratio": np.ones(100),
    }
    _add_fast_adiabatic_oscillation_history(result, hubble=0.001, t_end=10.0)
    classification = classify_outcome(result, PTUMParameters())
    assert not classification["quartic_achieved"]
    assert classification["n_late_half_cycles"] < 3
    assert not classification["adiabaticity_valid"]


def test_quartic_classification_rejects_missing_hubble_and_time_history():
    result = {
        "success": True,
        "w_psi_avg": np.full(5, 1.0 / 3.0),
        "Q": np.full(100, 2.1),
        "virial_ratio": np.ones(100),
    }
    classification = classify_outcome(result, PTUMParameters())
    assert not classification["quartic_achieved"]
    assert np.isnan(classification["H_over_omega_max"])
    assert classification["n_late_half_cycles"] == 0
    assert classification["regime"] == "insufficient_oscillation_data"


def test_threshold_matched_inflation_starts_dormant_and_becomes_tachyonic():
    # The revised waterfall mass is positive during slow roll above Phi_c
    # and negative after the field crosses below the critical value.
    p = PTUMParameters(
        lambda_phi=0.02,
        Phi_c=0.9862280831209068 * M_PL,
        m_psi=1.0e13,
        E_th=1.0e16,
    )
    phi_star = 10.7152391828 * M_PL
    phi_end = 0.9862280831 * M_PL
    assert meff_sq_psi(phi_star, p) > 0.0
    assert meff_sq_psi(phi_end, p) == pytest.approx(
        0.0, abs=1.0e-10 * p.m_psi**2
    )
    assert meff_sq_psi(0.99 * phi_end, p) < 0.0



def test_quadratic_virial_ratio_is_unity_for_harmonic_oscillator():
    p = PTUMParameters()
    phi = 1.1 * p.Phi_c
    mass = np.sqrt(meff_sq_psi(phi, p))
    t = np.linspace(0.0, 20.0 * np.pi / mass, 4001)
    amplitude = 1.0e10
    psi = amplitude * np.cos(mass * t)
    psi_dot = -mass * amplitude * np.sin(mass * t)
    Phi = np.full_like(t, phi)

    ratio = compute_quadratic_virial_ratio(t, psi, psi_dot, Phi, p)
    valid = ratio[np.isfinite(ratio)]
    assert len(valid) > 0
    # Turning points are represented by the nearest output-grid sample;
    # with 100 samples per half-cycle the expected endpoint bias is about 1%.
    assert np.mean(valid) == pytest.approx(1.0, rel=1.2e-2)


def test_quadratic_virial_ratio_is_unavailable_for_tachyonic_mass():
    p = PTUMParameters()
    phi = 0.9 * p.Phi_c
    t = np.linspace(0.0, 10.0, 1001)
    psi = np.cos(t)
    psi_dot = -np.sin(t)
    Phi = np.full_like(t, phi)

    ratio = compute_quadratic_virial_ratio(t, psi, psi_dot, Phi, p)
    assert np.all(np.isnan(ratio))




def test_late_time_adiabaticity_ignores_tangential_zero_without_sign_change():
    from ptum_task1_simulation import _late_time_adiabaticity_diagnostic

    t = np.linspace(0.0, 100.0, 10001)
    psi_dot = -np.sin(t)
    psi_dot[np.argmin(np.abs(t - 85.0))] = 0.0
    result = {
        "t": t,
        "H": np.full_like(t, 0.01),
        "psi_dot": psi_dot,
    }
    diagnostic = _late_time_adiabaticity_diagnostic(result)
    assert diagnostic["n_late_half_cycles"] == 5
    assert diagnostic["adiabaticity_valid"]

def test_quadratic_candidate_requires_its_own_virial_balance():
    base = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.02, -0.02]),
        "Q": np.full(100, 0.1),
        "virial_ratio": np.full(100, 1.0e6),
    }
    no_balance = dict(base, quadratic_virial_ratio=np.full(100, 4.0))
    with_balance = dict(base, quadratic_virial_ratio=np.full(100, 1.0))
    _add_fast_adiabatic_oscillation_history(with_balance)

    assert classify_outcome(no_balance, PTUMParameters())["regime"] == "non_quartic"
    assert classify_outcome(with_balance, PTUMParameters())["regime"] == "quadratic_candidate"


def test_quadratic_candidate_rejects_hubble_damped_oscillations():
    result = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.02, -0.02]),
        "Q": np.full(100, 0.1),
        "virial_ratio": np.full(100, 1.0e6),
        "quadratic_virial_ratio": np.ones(100),
    }
    _add_fast_adiabatic_oscillation_history(result, hubble=0.2)
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "non_quartic"
    assert not classification["adiabaticity_valid"]
    assert classification["H_over_omega_max"] >= 0.1


def test_quadratic_candidate_requires_oscillation_history():
    result = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.02, -0.02]),
        "Q": np.full(100, 0.1),
        "virial_ratio": np.full(100, 1.0e6),
        "quadratic_virial_ratio": np.ones(100),
    }
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "insufficient_oscillation_data"
    assert not classification["adiabaticity_valid"]



def test_positive_phi_offset_initializes_below_threshold_on_waterfall_side():
    p = PTUMParameters(Phi_c=0.9862280831209068 * M_PL)
    ic = create_initial_conditions(p, psi_init=0.01 * p.psi_0, phi_offset=0.01 * p.Phi_c)
    assert ic.Phi < p.Phi_c
    assert meff_sq_psi(ic.Phi, p) < 0.0



def test_threshold_matching_uses_exact_hubble_flow_end_not_epsilon_v_estimate():
    from ptum_inflation_background import compute_observables

    result = compute_observables(0.02, n_target=60.0, n_star=55.0)
    assert result["x_end_slow_roll"] == pytest.approx(1.3871750383, rel=1.0e-8)
    assert result["x_end_hubble_flow"] == pytest.approx(0.9862280831, rel=1.0e-8)
    assert result["epsilon_V_at_hubble_end"] > 2.0
    assert result["X_end"] ** 2 == pytest.approx(1.0 / 3.0, rel=1.0e-8)
    assert result["V_end_over_V0"] == pytest.approx(0.0192649296, rel=1.0e-8)
    assert result["kinetic_end_over_V0"] == pytest.approx(0.0096324648, rel=1.0e-8)
    assert result["rho_end_over_V0"] == pytest.approx(0.0288973944, rel=1.0e-8)
    assert result["old_potential_end_threshold_lead_efolds"] == pytest.approx(
        0.31852, rel=1.0e-3
    )



def test_waterfall_sector_transfer_rates_cancel_with_revised_sign():
    p = PTUMParameters()
    q_psi, q_phi = waterfall_transfer_rate(
        Phi=0.9 * p.Phi_c,
        psi=0.2 * p.psi_0,
        Phi_dot=-1.0e20,
        params=p,
    )
    assert q_psi < 0.0
    assert q_phi > 0.0
    assert q_psi + q_phi == pytest.approx(0.0, abs=1.0e-30)



def test_instantaneous_minimum_excitation_split_preserves_total_stress():
    p = PTUMParameters()
    Phi = 0.9 * p.Phi_c
    psi = 0.2 * p.psi_0
    Phi_dot = -1.0e20
    psi_dot = 2.0e18

    v_min = psi_minimum_potential(Phi, p)
    rho_phi_raw = rho_phi(Phi, Phi_dot, psi, p)
    rho_psi_raw = rho_psi(Phi, psi, psi_dot, p)
    p_phi_raw = pressure_phi(Phi, Phi_dot, p)
    p_psi_raw = pressure_psi(Phi, psi, psi_dot, p)

    rho_phi_split = rho_phi_raw + v_min
    rho_psi_exc = psi_excitation_energy(Phi, psi, psi_dot, p)
    p_phi_split = p_phi_raw - v_min
    p_psi_exc = psi_excitation_pressure(Phi, psi, psi_dot, p)

    assert rho_psi_exc >= 0.0
    assert rho_phi_split + rho_psi_exc == pytest.approx(
        rho_phi_raw + rho_psi_raw
    )
    assert p_phi_split + p_psi_exc == pytest.approx(
        p_phi_raw + p_psi_raw
    )


def test_excitation_potential_vanishes_at_instantaneous_broken_minimum():
    p = PTUMParameters()
    Phi = 0.9 * p.Phi_c
    psi_min_sq = psi_minimum_squared(Phi, p)
    assert psi_min_sq > 0.0
    psi_min = np.sqrt(psi_min_sq)
    v_exc = psi_excitation_potential(Phi, psi_min, p)
    v_min = psi_minimum_potential(Phi, p)
    # sqrt followed by squaring incurs round-off at the 1e-16 relative
    # field level; the residual energy must nevertheless be negligible
    # compared with the double-well barrier.
    assert v_exc <= 1.0e-28 * abs(v_min)


def test_shifted_excitation_transfer_vanishes_at_moving_minimum():
    p = PTUMParameters()
    Phi = 0.9 * p.Phi_c
    psi_min = np.sqrt(psi_minimum_squared(Phi, p))
    q_psi_exc, q_phi_split = waterfall_excitation_transfer_rate(
        Phi, psi_min, -1.0e20, p
    )
    q_psi_raw, _ = waterfall_transfer_rate(Phi, psi_min, -1.0e20, p)
    assert abs(q_psi_exc) <= 1.0e-12 * abs(q_psi_raw)
    assert q_phi_split == pytest.approx(-q_psi_exc, rel=1.0e-14, abs=0.0)


def test_unbroken_phase_excitation_potential_matches_raw_potential():
    p = PTUMParameters()
    Phi = 1.1 * p.Phi_c
    psi = 0.3 * p.psi_0
    m_eff_sq = meff_sq_psi(Phi, p)
    raw = 0.5 * m_eff_sq * psi**2 + 0.25 * p.lambda_psi * psi**4
    assert psi_minimum_potential(Phi, p) == pytest.approx(0.0)
    assert psi_excitation_potential(Phi, psi, p) == pytest.approx(raw)



def test_raw_psi_equation_of_state_is_nan_when_sector_density_is_zero():
    p = PTUMParameters()
    assert np.isnan(w_psi(1.1 * p.Phi_c, 0.0, 0.0, p))




def test_scan_profiles_keep_ci_smoke_separate_from_full_high_resolution_scan():
    from ptum_task1_scan import (
        build_initial_condition_grid,
        build_scan_scenarios,
        expected_scan_count,
        validate_scan_results,
    )

    assert expected_scan_count("ci") == 4
    assert expected_scan_count("full") == 100
    params = build_scan_scenarios()[0][1]
    ci_grid = build_initial_condition_grid(params, profile="ci")
    assert tuple(map(len, ci_grid)) == (2, 1, 1)
    assert len(build_initial_condition_grid(params, profile="full")[0]) == 5

    ci_rows = [
        {"success": True, "scan_metadata": {"scenario": "ci"}}
        for _ in range(4)
    ]
    assert validate_scan_results(ci_rows, expected_count=4) == 4

def test_high_resolution_scan_validation_fails_closed():
    from ptum_task1_scan import validate_scan_results

    valid_rows = [
        {"success": True, "scan_metadata": {"scenario": "test"}}
        for _ in range(100)
    ]
    assert validate_scan_results(valid_rows) == 100

    with pytest.raises(RuntimeError, match="Incomplete scan"):
        validate_scan_results(valid_rows[:-1])

    failed_rows = [dict(row) for row in valid_rows]
    failed_rows[17] = {
        "success": False,
        "scan_metadata": {"scenario": "test"},
        "ic_params": {"psi_init": 0.0},
        "error": "synthetic integration failure",
    }
    with pytest.raises(RuntimeError, match="integrations failed"):
        validate_scan_results(failed_rows)



def test_post_inflation_threshold_state_uses_exact_background_velocity():
    from ptum_inflation_background import (
        compute_observables,
        state_at_field_value,
    )

    benchmark = compute_observables(0.02, n_target=60.0, n_star=55.0)
    x_end = benchmark["x_end_hubble_flow"]
    endpoint = state_at_field_value(
        0.02, x_end, V0=1.0e64
    )
    assert endpoint["x"] == pytest.approx(x_end, rel=1.0e-9)
    assert endpoint["epsilon_H"] == pytest.approx(1.0, abs=2.0e-7)
    assert endpoint["X"] == pytest.approx(-1.0 / np.sqrt(3.0), abs=2.0e-7)
    assert endpoint["Phi_dot"] < 0.0

    post_threshold = state_at_field_value(
        0.02, 0.9 * x_end, V0=1.0e64
    )
    assert post_threshold["N"] > endpoint["N"]
    assert post_threshold["x"] == pytest.approx(0.9 * x_end, rel=1.0e-9)
    assert post_threshold["Phi_dot"] < 0.0
    assert post_threshold["epsilon_H"] > 1.0


def test_scan_initial_conditions_accept_integrated_fuel_velocity():
    p = PTUMParameters()
    expected_phi_dot = -2.5e30
    ic = create_initial_conditions(
        p,
        psi_init=0.1 * p.psi_0,
        phi_offset=0.01 * p.Phi_c,
        Phi_dot_override=expected_phi_dot,
    )
    assert ic.Phi_dot == expected_phi_dot


# Gauge-representation, operator-dimension and manuscript/action regressions.
def test_ptum_sm_yukawa_operators_are_hypercharge_neutral():
    from ptum_covariant_action import yukawa_hypercharge_residuals

    assert set(yukawa_hypercharge_residuals()) == {"down", "up", "charged_lepton"}
    assert all(value == 0 for value in yukawa_hypercharge_residuals().values())


def test_ptum_sm_yukawa_operators_form_nonabelian_singlets():
    from ptum_covariant_action import yukawa_nonabelian_singlet_checks

    checks = yukawa_nonabelian_singlet_checks()
    assert set(checks) == {"down", "up", "charged_lepton"}
    assert all(all(groups.values()) for groups in checks.values())


def test_manuscript_displays_chiral_sm_gauge_anomaly_cancellation():
    from pathlib import Path

    source = " ".join(
        Path("main.tex").read_text(encoding="utf-8").split()
    )
    assert r"\mathcal A_{SU(3)^3}" in source
    assert r"\mathcal A_{SU(3)^2U(1)_Y}" in source
    assert r"\mathcal A_{SU(2)^2U(1)_Y}" in source
    assert r"\mathcal A_{U(1)_Y^3}" in source
    assert r"\mathcal A_{\mathrm{grav}^2U(1)_Y}" in source
    assert r"\label{eq:sm_gauge_anomaly_cancellation}" in source
    assert r"&=6\left(\frac16\right)^3+3\left(-\frac23\right)^3" in source
    assert r"&\quad+3\left(\frac13\right)^3" in source
    assert "twelve across the three generations" in source
    assert "do not supply a PTUM UV completion" in source


def test_ptum_action_operator_mass_dimensions_are_four():
    from fractions import Fraction
    from ptum_covariant_action import operator_mass_dimensions

    dimensions = operator_mass_dimensions()
    assert dimensions
    assert all(value == Fraction(4, 1) for value in dimensions.values())


def test_ptum_scalar_fields_are_real_standard_model_gauge_singlets():
    from ptum_covariant_action import PTUM_SCALAR_REPRESENTATIONS

    assert set(PTUM_SCALAR_REPRESENTATIONS) == {"Phi", "psi", "chi", "Phi_res"}
    for rep in PTUM_SCALAR_REPRESENTATIONS.values():
        assert rep["su3"] == "1"
        assert rep["su2"] == "1"
        assert rep["hypercharge"] == 0
        assert rep["reality"] == "real"


def test_ptum_covariant_action_registry_passes_all_algebraic_checks():
    from ptum_covariant_action import validate_action_registry

    assert validate_action_registry()


def test_ptum_standard_model_gauge_anomalies_cancel_exactly():
    from fractions import Fraction
    from ptum_covariant_action import (
        gauge_anomaly_audit,
        validate_gauge_anomaly_cancellation,
    )

    audit = gauge_anomaly_audit()
    anomalies = audit["perturbative_anomalies_per_generation"]
    assert anomalies == {
        "su3_cubic": 0,
        "su3_squared_u1": Fraction(0, 1),
        "su2_squared_u1": Fraction(0, 1),
        "u1_cubic": Fraction(0, 1),
        "mixed_gravitational_u1": Fraction(0, 1),
    }
    assert audit["weak_doublets_per_generation"] == 4
    assert audit["weak_doublets_total"] == 12
    assert audit["witten_su2_anomaly_absent"]
    assert not audit["right_handed_neutrino_included"]
    assert validate_gauge_anomaly_cancellation()


def test_manuscript_uses_one_waterfall_mass_parameter():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert "m^2" not in source
    assert r"m_\psi^2" in source
    assert r"m_{\rm eff}^2(\Phi)" in source


def test_manuscript_contains_explicit_curved_sm_action_and_hilbert_tensor():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    normalized_source = " ".join(source.split())
    for required in (
        r"\label{sec:sm_covariant_action}",
        r"\label{eq:sm_curved_action}",
        r"\label{eq:sm_hilbert_tensor}",
        r"T_{\rm gauge}^{\mu\nu}",
        r"T_H^{\mu\nu}",
        r"T_{f,\mathrm{kin}}^{\mu\nu}",
        r"T_{f,0}^{\mu\nu}",
        r"\mathcal K_f",
        r"T_{{\rm SM},0}^{\mu\nu}",
        r"-\frac{i}{4}",
    ):
        assert required in source


def test_manuscript_does_not_overstate_psi_z2_or_phi_res_shift_symmetry():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert "explicitly broken when any" in source
    assert "No exact or technically protected shift symmetry" in source



def test_manuscript_loads_mathrsfs_for_covariant_spinor_derivative():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert r"\usepackage{mathrsfs}" in source
    assert r"\mathscr D_\mu" in source


def test_off_shell_sm_hilbert_tensor_reduces_with_full_ptum_fermion_eom():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    start = source.index(r"T_{f,\mathrm{kin}}^{\mu\nu}={}&")
    end = source.index(r"\label{eq:sm_hilbert_tensor}", start)
    tensor_definition = source[start:end]
    assert r"\mathcal K_f" in tensor_definition
    assert r"g^{\mu\nu}\left(\mathcal K_f-U_{{\rm SM},Y}\right)" in tensor_definition
    assert r"T_{\rm gauge}^{\mu\nu}+T_H^{\mu\nu}+T_{f,0}^{\mu\nu}" in tensor_definition
    assert r"U_{{\rm SM},Y}+U_Y" in source
    normalized_source = " ".join(source.split())
    assert "full PTUM+SM fermion equations of motion" in normalized_source
    assert r"T_{{\rm SM},0}^{\mu\nu}-g^{\mu\nu}U_Y" in source
    assert r"T_{\rm gauge}^{\mu\nu}+T_H^{\mu\nu}" in source
    assert r"T_{f,\mathrm{kin}}^{\mu\nu}" in source
    assert "must be retained before applying" in source



def test_expanding_mode_solver_accepts_tachyonic_effective_mass_history():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 10.0, 1001)
    mass_sq = 1.0 - 2.0 * np.exp(-((t - 5.0) / 1.2) ** 2)
    result = integrate_expanding_mode(
        t=t,
        scale_factor=np.ones_like(t),
        hubble=np.zeros_like(t),
        phi_res=np.zeros_like(t),
        k_comoving=0.0,
        m_chi=0.0,
        g_dm=0.0,
        effective_mass_sq=mass_sq,
    )
    assert np.min(result["effective_mass_sq"]) < 0.0
    assert np.min(result["canonical_frequency_sq"]) < 0.0
    assert result["final_frequency_valid"]
    assert np.isfinite(result["particle_number"])
    assert result["wronskian_valid"]
    assert result["particle_number_valid"]
    assert result["wronskian_relative_error"] < 1.0e-7


def test_expanding_mode_solver_rejects_tachyonic_initial_effective_mass():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 2.0, 101)
    with pytest.raises(ValueError, match="initial canonical mode frequency"):
        integrate_expanding_mode(
            t=t,
            scale_factor=np.ones_like(t),
            hubble=np.zeros_like(t),
            phi_res=np.zeros_like(t),
            k_comoving=0.0,
            m_chi=0.0,
            g_dm=0.0,
            effective_mass_sq=-np.ones_like(t),
        )


def test_waterfall_background_crosses_threshold_from_stable_phase():
    from ptum_waterfall_modes import build_waterfall_background

    params = PTUMParameters(V0=1.0e64)
    background = build_waterfall_background(
        params, start_fraction=0.05, t_end_mu=10.0, n_points=1001
    )
    mass_sq = background["effective_mass_sq_over_mu2"]
    assert mass_sq[0] > 0.0
    assert np.min(mass_sq) < 0.0
    assert 0.0 < background["threshold_crossing_tau"] < 10.0
    assert np.all(np.diff(background["scale_factor"]) > 0.0)
    assert background["psi_homogeneous_exact_zero"]
    assert not background["backreaction_included"]


def test_waterfall_mode_uses_adiabatic_vacuum_and_preserves_wronskian():
    from ptum_waterfall_modes import build_waterfall_background, integrate_waterfall_mode

    background = build_waterfall_background(
        PTUMParameters(V0=1.0e64),
        start_fraction=0.05,
        t_end_mu=1.0,
        n_points=1001,
    )
    mode = integrate_waterfall_mode(
        background, k_over_mu=60.0, max_initial_adiabaticity=0.1
    )
    assert mode["integration_success"]
    assert mode["initial_adiabatic_vacuum"]
    assert mode["tachyonic_mass_interval"]
    assert mode["wronskian_valid"]
    assert mode["particle_number_valid"]
    assert mode["wronskian_relative_error"] < 1.0e-7





def test_forecast_methodology_discloses_missing_reproducibility_artifacts():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    normalized_source = " ".join(source.split())
    required = (
        "not independently reproduced from the present repository",
        r"modified \texttt{CLASS} implementation",
        "Fisher code",
        "bandpower covariance outputs",
        "foreground and delensing-residual model",
        "indicative forecasts rather than independently validated detection significances",
        "derivative step-size tests",
    )
    for phrase in required:
        assert phrase in normalized_source


def test_manuscript_documents_linear_waterfall_mode_hierarchy():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    normalized_source = " ".join(source.split())
    for required in (
        r"\label{sec:linear_waterfall_modes}",
        r"\label{eq:waterfall_mode_eom}",
        r"\label{eq:waterfall_canonical_frequency}",
        r"\label{eq:waterfall_wkb_initial}",
        r"\label{eq:waterfall_wronskian}",
        r"\label{eq:waterfall_finite_band_number}",
        "the occupation number and the associated finite-band number density are withheld",
        "does not include mode backreaction",
    ):
        assert required in normalized_source


def test_waterfall_finite_band_spectrum_reports_units_and_wronskian_status():
    from ptum_waterfall_modes import (
        build_waterfall_background,
        integrate_waterfall_spectrum,
    )

    background = build_waterfall_background(
        PTUMParameters(V0=1.0e64),
        start_fraction=0.05,
        t_end_mu=1.0,
        n_points=1001,
    )
    spectrum = integrate_waterfall_spectrum(
        background, [60.0, 80.0, 100.0]
    )
    assert spectrum["finite_band_only"]
    assert spectrum["all_wronskians_valid"]
    assert spectrum["number_density_unit"] == "mu^3"
    assert spectrum["momentum_unit"] == "mu"
    assert np.isfinite(spectrum["n_comoving_finite_band"])



def test_waterfall_band_resolution_helper_never_claims_uv_ir_convergence():
    from ptum_waterfall_modes import (
        build_waterfall_background,
        converge_waterfall_band_resolution,
    )

    background = build_waterfall_background(
        PTUMParameters(V0=1.0e64),
        start_fraction=0.05,
        t_end_mu=1.0,
        n_points=1001,
    )
    result = converge_waterfall_band_resolution(
        background,
        k_min_over_mu=60.0,
        k_max_over_mu=100.0,
        resolutions=(4, 8),
        relative_tolerance=0.5,
    )
    assert result["resolution_counts"] == [4, 8]
    assert result["finite_band_only"]
    assert result["all_wronskians_valid"]
    assert result["uv_ir_tail_converged"] is False
    assert len(result["n_comoving_finite_band_estimates"]) == 2
    assert result["band_resolution_converged"] == (
        result["relative_changes"][-1] <= result["relative_tolerance"]
    )



def test_waterfall_band_resolution_rejects_non_integer_grid_counts():
    from ptum_waterfall_modes import converge_waterfall_band_resolution

    with pytest.raises(ValueError, match="integers"):
        converge_waterfall_band_resolution(
            {},
            k_min_over_mu=60.0,
            k_max_over_mu=100.0,
            resolutions=(4, 8.5),
        )


def test_deep_tachyonic_growth_with_wronskian_drift_withholds_particle_number():
    from ptum_waterfall_modes import build_waterfall_background, integrate_waterfall_mode

    background = build_waterfall_background(
        PTUMParameters(V0=1.0e64),
        start_fraction=0.05,
        t_end_mu=10.0,
        n_points=2001,
    )
    mode = integrate_waterfall_mode(
        background, k_over_mu=60.0, wronskian_tolerance=1.0e-7
    )
    assert mode["integration_success"]
    assert mode["tachyonic_mass_interval"]
    assert not mode["wronskian_valid"]
    assert not mode["particle_number_valid"]
    assert np.isnan(mode["particle_number"])


def test_expanding_mode_solver_preserves_adiabatic_vacuum_in_de_sitter():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 10.0, 501)
    H0 = 0.1
    result = integrate_expanding_mode(
        t=t,
        scale_factor=np.exp(H0 * t),
        hubble=np.full_like(t, H0),
        phi_res=np.zeros_like(t),
        k_comoving=0.0,
        m_chi=1.0,
        g_dm=0.0,
    )
    assert result["integration_success"]
    assert result["final_frequency_valid"]
    assert result["initial_adiabaticity"] < 1.0e-10
    assert result["background_hubble_consistency_max_relative"] < 1.0e-8
    assert result["particle_number"] == pytest.approx(0.0, abs=2.0e-8)
    assert result["wronskian_relative_error"] < 2.0e-8


def test_expanding_mode_solver_rejects_non_adiabatic_initial_vacuum():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 1.0, 101)
    phi_res = np.zeros_like(t)
    phi_res[0] = 0.0
    phi_res[1:] = np.linspace(0.0, 1.0e4, len(t) - 1)
    with pytest.raises(ValueError, match="not sufficiently adiabatic"):
        integrate_expanding_mode(
            t=t,
            scale_factor=np.ones_like(t),
            hubble=np.zeros_like(t),
            phi_res=phi_res,
            k_comoving=0.0,
            m_chi=1.0,
            g_dm=1.0,
            max_initial_adiabaticity=1.0e-12,
        )



def test_expanding_spectrum_integrates_finite_band_vacuum_control():
    from ptum_floquet import integrate_expanding_spectrum

    t = np.linspace(0.0, 5.0, 251)
    H0 = 0.05
    result = integrate_expanding_spectrum(
        k_values=np.array([0.0, 1.0e-5]),
        t=t,
        scale_factor=np.exp(H0 * t),
        hubble=np.full_like(t, H0),
        phi_res=np.zeros_like(t),
        m_chi=1.0,
        g_dm=0.0,
    )
    assert result["all_final_frequencies_valid"]
    assert result["finite_band_only"]
    assert result["n_comoving_finite_band"] == pytest.approx(0.0, abs=2.0e-7)
    assert result["n_physical_finite_band"] == pytest.approx(0.0, abs=2.0e-7)
    assert len(result["occupation_numbers"]) == 2


def test_expanding_spectrum_rejects_unsorted_momentum_grid():
    from ptum_floquet import integrate_expanding_spectrum

    t = np.linspace(0.0, 1.0, 11)
    with pytest.raises(ValueError, match="strictly increasing"):
        integrate_expanding_spectrum(
            k_values=[0.0, 2.0, 1.0],
            t=t,
            scale_factor=np.ones_like(t),
            hubble=np.zeros_like(t),
            phi_res=np.zeros_like(t),
            m_chi=1.0,
            g_dm=0.0,
        )



def test_expanding_mode_solver_rejects_inconsistent_scale_factor_and_hubble():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 2.0, 101)
    with pytest.raises(ValueError, match="inconsistent background histories"):
        integrate_expanding_mode(
            t=t,
            scale_factor=np.exp(0.1 * t),
            hubble=np.zeros_like(t),
            phi_res=np.zeros_like(t),
            k_comoving=0.0,
            m_chi=1.0,
            g_dm=0.0,
        )



def test_expanding_mode_solver_allows_intermediate_tachyonic_canonical_frequency():
    from scipy.integrate import cumulative_trapezoid
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 3.0, 1201)
    H = np.sin(np.pi * t / 3.0) ** 4
    log_a = np.concatenate(([0.0], cumulative_trapezoid(H, t)))
    a = np.exp(log_a)
    result = integrate_expanding_mode(
        t=t,
        scale_factor=a,
        hubble=H,
        phi_res=np.zeros_like(t),
        k_comoving=0.0,
        m_chi=1.0,
        g_dm=0.0,
    )
    assert result["integration_success"]
    assert np.min(result["canonical_frequency_sq"]) < 0.0
    assert result["final_frequency_valid"]
    assert np.isfinite(result["particle_number"])
    assert result["wronskian_relative_error"] < 1.0e-7


def test_manuscript_withdraws_unverified_lattice_outputs_and_reproduction_claims():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    start = source.index(r"\subsection{Nonlinear lattice validation: current status}")
    end = source.index("%============================================================\n% REFERENCES", start)
    section = source[start:end]
    normalized_section = " ".join(section.split()).lower()
    assert "versioned periodic cubic finite-difference prototype" in normalized_section
    assert "not a quantum-seeded waterfall calculation" in normalized_section
    assert "does not generate adiabatic-vacuum initial conditions" in normalized_section
    assert "does not expose an individually reviewable ptum lattice solver" not in normalized_section
    assert r"does \emph{not} claim".lower() in normalized_section
    assert "sub-percent time-integrated energy-conservation" in normalized_section
    assert "raw field configurations, outputs, and checksums" in normalized_section
    for unsupported_claim in (
        "The following lattice outputs are included",
        "convergence tested up to",
        r"0.198 \pm 0.005",
        r"0.118 \pm 0.015",
        r"S_{\rm obs} \sim 10^{88}",
        "docker run -v",
    ):
        assert unsupported_claim.lower() not in normalized_section


def test_manuscript_describes_proxy_fluid_as_a_phenomenological_closure():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert "specifies a phenomenological linear proxy-fluid perturbation closure" in source



def test_expanding_mode_withholds_particle_number_for_nonadiabatic_final_basis():
    from ptum_floquet import integrate_expanding_mode

    t = np.linspace(0.0, 1.0, 501)
    mass_sq = 1.0 + 10.0 * t**2
    result = integrate_expanding_mode(
        t=t,
        scale_factor=np.ones_like(t),
        hubble=np.zeros_like(t),
        phi_res=np.zeros_like(t),
        k_comoving=0.0,
        m_chi=0.0,
        g_dm=0.0,
        effective_mass_sq=mass_sq,
        max_initial_adiabaticity=0.1,
        max_final_adiabaticity=0.1,
    )
    assert result["integration_success"]
    assert result["final_frequency_valid"]
    assert result["wronskian_valid"]
    assert result["final_adiabaticity"] > 0.1
    assert not result["final_adiabaticity_valid"]
    assert not result["particle_number_valid"]
    assert np.isnan(result["particle_number"])


def test_expanding_spectrum_withholds_finite_band_density_if_final_basis_is_nonadiabatic():
    from ptum_floquet import integrate_expanding_spectrum

    t = np.linspace(0.0, 1.0, 501)
    mass_sq = 1.0 + 10.0 * t**2
    result = integrate_expanding_spectrum(
        k_values=[0.0, 0.1],
        t=t,
        scale_factor=np.ones_like(t),
        hubble=np.zeros_like(t),
        phi_res=np.zeros_like(t),
        m_chi=0.0,
        g_dm=0.0,
        effective_mass_sq=mass_sq,
        max_initial_adiabaticity=0.1,
        max_final_adiabaticity=0.1,
    )
    assert result["all_final_frequencies_valid"]
    assert result["all_wronskians_valid"]
    assert not result["all_particle_numbers_valid"]
    assert np.isnan(result["n_comoving_finite_band"])
    assert np.isnan(result["n_physical_finite_band"])



def test_manuscript_requires_final_wkb_adiabaticity_for_particle_number():
    from pathlib import Path

    source = " ".join(Path("main.tex").read_text(encoding="utf-8").split())
    assert "final first-order WKB" in source
    assert r"\(|\dot\Omega_{k,f}/\Omega_{k,f}^2|\)" in source
    assert "occupation number and the associated finite-band number density are withheld" in source



def test_radiation_hubble_rate_uses_reduced_planck_friedmann_equation():
    from ptum_defects import radiation_hubble_rate

    value = radiation_hubble_rate(
        temperature=5.0e-3,
        g_star=10.75,
        reduced_planck_mass=2.435e18,
    )
    assert value == pytest.approx(1.1147407908489041e-23, rel=2.0e-15)
    with pytest.raises(ValueError):
        radiation_hubble_rate(temperature=0.0, g_star=10.75,
                              reduced_planck_mass=2.435e18)
    with pytest.raises(ValueError):
        radiation_hubble_rate(temperature=5.0e-3, g_star=-1.0,
                              reduced_planck_mass=2.435e18)


def test_ptum_real_psi_benchmark_has_catastrophic_unbiased_wall_scaling():
    from ptum_defects import (
        domain_wall_bias_diagnostics,
        radiation_hubble_rate,
    )

    mu_eff = 1.0e13
    lambda_psi = 0.1
    reduced_planck_mass = 2.435e18
    hubble_bbn = radiation_hubble_rate(
        temperature=5.0e-3,
        g_star=10.75,
        reduced_planck_mass=reduced_planck_mass,
    )
    unbiased = domain_wall_bias_diagnostics(
        mu_eff, lambda_psi, 0.0,
        hubble_bbn=hubble_bbn,
        reduced_planck_mass=reduced_planck_mass,
        network_area_factor=1.0,
    )
    assert unbiased["wall_tension"] == pytest.approx(9.428090415820633e39)
    assert unbiased["hubble_domination_estimate"] == pytest.approx(
        530.0350054642124, rel=2.0e-14
    )
    assert unbiased["hubble_domination_estimate"] / hubble_bbn > 4.0e25
    assert not unbiased["annihilation_before_bbn"]
    assert not unbiased["annihilation_before_wall_domination"]

    required_source = unbiased["required_linear_source_for_bbn_and_domination"]
    required_ratio = required_source / unbiased["epsilon_critical"]
    assert required_source == pytest.approx(7.9012953511496755e28, rel=2.0e-14)
    assert required_ratio == pytest.approx(6.49157654600307e-11, rel=2.0e-14)

    safely_biased = domain_wall_bias_diagnostics(
        mu_eff, lambda_psi, 2.0 * required_source,
        hubble_bbn=hubble_bbn,
        reduced_planck_mass=reduced_planck_mass,
        network_area_factor=1.0,
    )
    assert safely_biased["small_bias_tension_approx_valid"]
    assert safely_biased["annihilation_before_bbn"]
    assert safely_biased["annihilation_before_wall_domination"]


def test_domain_wall_bbn_risk_reports_critical_network_area_factor():
    from ptum_defects import (
        domain_wall_bias_diagnostics,
        radiation_hubble_rate,
    )

    mu_eff = 1.0e13
    lambda_psi = 0.1
    reduced_planck_mass = 2.435e18
    hubble_bbn = radiation_hubble_rate(
        temperature=5.0e-3,
        g_star=10.75,
        reduced_planck_mass=reduced_planck_mass,
    )
    benchmark = domain_wall_bias_diagnostics(
        mu_eff, lambda_psi, 0.0,
        hubble_bbn=hubble_bbn,
        reduced_planck_mass=reduced_planck_mass,
        network_area_factor=1.0,
    )
    critical_area = benchmark[
        "critical_network_area_factor_for_domination_before_bbn"
    ]
    assert critical_area == pytest.approx(2.1031456023788425e-26, rel=2.0e-14)
    assert benchmark["wall_domination_before_bbn"]
    assert benchmark["wall_domination_hubble_ratio_to_bbn"] == pytest.approx(
        1.0 / critical_area, rel=2.0e-14
    )

    below = domain_wall_bias_diagnostics(
        mu_eff, lambda_psi, 0.0,
        hubble_bbn=hubble_bbn,
        reduced_planck_mass=reduced_planck_mass,
        network_area_factor=0.5 * critical_area,
    )
    above = domain_wall_bias_diagnostics(
        mu_eff, lambda_psi, 0.0,
        hubble_bbn=hubble_bbn,
        reduced_planck_mass=reduced_planck_mass,
        network_area_factor=2.0 * critical_area,
    )
    assert not below["wall_domination_before_bbn"]
    assert below["wall_domination_hubble_ratio_to_bbn"] == pytest.approx(0.5)
    assert above["wall_domination_before_bbn"]
    assert above["wall_domination_hubble_ratio_to_bbn"] == pytest.approx(2.0)
    assert below["required_vacuum_bias_for_bbn_and_domination"] == pytest.approx(
        below["wall_tension"] * hubble_bbn
    )
    assert above["required_vacuum_bias_for_bbn_and_domination"] == pytest.approx(
        above["wall_tension"] * 2.0 * hubble_bbn
    )


def test_real_psi_domain_wall_kink_solves_static_field_equation():
    from ptum_defects import domain_wall_profile

    mu = 3.0
    lam = 0.2
    v = mu / np.sqrt(lam)
    z = np.linspace(-1.5 / mu, 1.5 / mu, 101)
    h = 1.0e-4 / mu
    psi = domain_wall_profile(z, mu, lam)
    psi_plus = domain_wall_profile(z + h, mu, lam)
    psi_minus = domain_wall_profile(z - h, mu, lam)
    second_derivative = (psi_plus - 2.0 * psi + psi_minus) / h**2
    residual = second_derivative - lam * psi * (psi**2 - v**2)
    scale = mu**2 * v
    assert np.max(np.abs(residual)) / scale < 2.0e-7


def test_real_psi_domain_wall_tension_matches_profile_energy_integral():
    from ptum_defects import domain_wall_energy_density, domain_wall_tension

    mu = 2.5
    lam = 0.15
    z = np.linspace(-20.0 / mu, 20.0 / mu, 40001)
    numerical = np.trapezoid(domain_wall_energy_density(z, mu, lam), z)
    analytic = domain_wall_tension(mu, lam)
    assert numerical == pytest.approx(analytic, rel=2.0e-8)


def test_small_explicit_bias_splits_the_two_vacua_by_two_epsilon_v():
    from ptum_defects import domain_wall_bias_diagnostics

    mu = 1.0e4
    lam = 0.1
    epsilon_critical = 2.0 * mu**3 / (3.0 * np.sqrt(3.0 * lam))
    epsilon = 1.0e-6 * epsilon_critical
    result = domain_wall_bias_diagnostics(
        mu, lam, epsilon, hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    expected = 2.0 * epsilon * mu / np.sqrt(lam)
    assert result["metastable_vacuum_exists"]
    assert result["small_bias_tension_approx_valid"]
    assert result["vacuum_bias"] == pytest.approx(expected, rel=2.0e-6)


def test_tilted_quartic_bias_matches_stationary_potential_at_moderate_bias():
    from ptum_defects import domain_wall_bias_diagnostics

    mu = 1.0e4
    lam = 0.1
    epsilon_critical = 2.0 * mu**3 / (3.0 * np.sqrt(3.0 * lam))
    epsilon = 0.35 * epsilon_critical
    result = domain_wall_bias_diagnostics(
        mu, lam, epsilon, hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    v = mu / np.sqrt(lam)
    y_true = result["true_minimum"] / v
    y_false = result["false_minimum"] / v
    b = epsilon * np.sqrt(lam) / mu**3

    # Both returned field values must be stationary local minima of
    # f(y)=y^4/4-y^2/2-b*y, not merely roots with the expected signs.
    assert y_true**3 - y_true - b == pytest.approx(0.0, abs=2.0e-14)
    assert y_false**3 - y_false - b == pytest.approx(0.0, abs=2.0e-14)
    assert 3.0 * y_true**2 - 1.0 > 0.0
    assert 3.0 * y_false**2 - 1.0 > 0.0

    def dimensionless_potential(y):
        return 0.25 * y**4 - 0.5 * y**2 - b * y

    direct = (dimensionless_potential(y_false)
              - dimensionless_potential(y_true)) * mu**4 / lam
    assert result["vacuum_bias"] == pytest.approx(direct, rel=2.0e-13)
    assert result["true_minimum"] > 0.0
    assert result["false_minimum"] < 0.0


def test_signed_domain_wall_bias_swaps_true_and_false_vacua():
    from ptum_defects import (
        domain_wall_bias_diagnostics,
        thermal_fermion_bias,
    )

    mu = 1.0e4
    lam = 0.1
    epsilon_critical = 2.0 * mu**3 / (3.0 * np.sqrt(3.0 * lam))
    epsilon = 0.2 * epsilon_critical
    kwargs = dict(
        mu_eff=mu,
        lambda_psi=lam,
        hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    positive = domain_wall_bias_diagnostics(epsilon_bias=epsilon, **kwargs)
    negative = domain_wall_bias_diagnostics(epsilon_bias=-epsilon, **kwargs)

    assert positive["true_minimum"] > 0.0
    assert positive["false_minimum"] < 0.0
    assert negative["true_minimum"] < 0.0
    assert negative["false_minimum"] > 0.0
    assert negative["true_minimum"] == pytest.approx(
        -positive["true_minimum"], rel=2.0e-14
    )
    assert negative["false_minimum"] == pytest.approx(
        -positive["false_minimum"], rel=2.0e-14
    )
    assert negative["vacuum_bias"] == pytest.approx(
        positive["vacuum_bias"], rel=2.0e-14
    )
    assert negative["epsilon_bias"] == pytest.approx(-epsilon)
    assert negative["epsilon_bias_magnitude"] == pytest.approx(epsilon)
    assert negative["bias_favors_positive_psi"] is False

    thermal = thermal_fermion_bias([(0.5, 0.2, 1)], temperature=1.0)
    thermal_result = domain_wall_bias_diagnostics(
        mu, lam, thermal["epsilon_bias"],
        hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    assert thermal["epsilon_bias"] < 0.0
    assert thermal_result["true_minimum"] < 0.0
    assert thermal_result["vacuum_bias"] > 0.0


def test_domain_wall_bias_spinodal_removes_false_vacuum():
    from ptum_defects import domain_wall_bias_diagnostics

    mu = 1.0e4
    lam = 0.1
    epsilon_critical = 2.0 * mu**3 / (3.0 * np.sqrt(3.0 * lam))
    result = domain_wall_bias_diagnostics(
        mu, lam, 1.01 * epsilon_critical, hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    assert not result["metastable_vacuum_exists"]
    assert result["true_minimum"] is None
    assert result["false_minimum"] is None
    assert not result["small_bias_tension_approx_valid"]
    assert result["hubble_annihilation_estimate"] is None
    assert result["annihilation_before_bbn"] is None


def test_zero_domain_wall_bias_cannot_annihilate_scaling_network():
    from ptum_defects import domain_wall_bias_diagnostics

    result = domain_wall_bias_diagnostics(
        1.0e4, 0.1, 0.0, hubble_bbn=1.0e-20,
        reduced_planck_mass=2.435e18,
    )
    assert result["vacuum_bias"] == pytest.approx(0.0, abs=1.0e-20)
    assert result["hubble_annihilation_estimate"] == pytest.approx(0.0)
    assert not result["annihilation_before_bbn"]
    assert not result["annihilation_before_wall_domination"]


def test_domain_wall_bias_required_source_can_annihilate_before_bbn():
    from ptum_defects import domain_wall_bias_diagnostics

    kwargs = dict(
        mu_eff=1.0e4, lambda_psi=0.1,
        hubble_bbn=1.0e-20, reduced_planck_mass=2.435e18,
    )
    threshold = domain_wall_bias_diagnostics(epsilon_bias=0.0, **kwargs)
    epsilon = 2.0 * threshold["required_linear_source_for_bbn_and_domination"]
    result = domain_wall_bias_diagnostics(epsilon_bias=epsilon, **kwargs)
    expected_linear_bias = 2.0 * epsilon * result["vev"]
    assert result["small_bias_tension_approx_valid"]
    # Here epsilon/epsilon_crit is about 1e-24. Direct subtraction of
    # the two O(mu^4/lambda) minima rounds their splitting to exactly zero.
    assert result["vacuum_bias"] == pytest.approx(expected_linear_bias, rel=2.0e-14)
    assert result["hubble_annihilation_estimate"] == pytest.approx(
        expected_linear_bias / result["wall_tension"], rel=2.0e-14
    )
    assert result["annihilation_before_bbn"]
    assert result["annihilation_before_wall_domination"]


def test_dimension_five_operator_vev_maps_to_dimension_three_bias_source():
    from ptum_defects import bias_from_operator_vev

    epsilon = bias_from_operator_vev(
        operator_vev=2.0e12, cutoff=1.0e16, wilson_coefficient=0.5
    )
    assert epsilon == pytest.approx(1.0e-4)
    with pytest.raises(ValueError):
        bias_from_operator_vev(operator_vev=1.0, cutoff=0.0)


def test_thermal_dirac_condensate_has_correct_relativistic_limit():
    from ptum_defects import thermal_dirac_scalar_condensate

    mass = 1.0e-4
    temperature = 1.0
    nc = 3
    value = thermal_dirac_scalar_condensate(mass, temperature, nc)
    expected = nc * mass * temperature**2 / 6.0
    assert value == pytest.approx(expected, rel=2.0e-6)


def test_thermal_dirac_condensate_scales_as_mass_times_temperature_squared():
    from ptum_defects import thermal_dirac_scalar_condensate

    base = thermal_dirac_scalar_condensate(0.7, 1.4, 3)
    scaled = thermal_dirac_scalar_condensate(1.4, 2.8, 3)
    assert scaled == pytest.approx(8.0 * base, rel=2.0e-11)


def test_thermal_dirac_condensate_vanishes_for_zero_mass_or_temperature():
    from ptum_defects import thermal_dirac_scalar_condensate

    assert thermal_dirac_scalar_condensate(0.0, 1.0, 3) == 0.0
    assert thermal_dirac_scalar_condensate(1.0, 0.0, 3) == 0.0


def test_thermal_fermion_bias_uses_signed_real_couplings_and_cancels():
    from ptum_defects import thermal_fermion_bias

    positive = thermal_fermion_bias([(0.5, 0.2, 1)], temperature=1.0)
    negative = thermal_fermion_bias([(0.5, -0.2, 1)], temperature=1.0)
    cancelled = thermal_fermion_bias(
        [(0.5, 0.2, 1), (0.5, -0.2, 1)], temperature=1.0
    )
    assert positive["epsilon_bias"] < 0.0
    assert negative["epsilon_bias"] > 0.0
    assert cancelled["epsilon_bias"] == pytest.approx(0.0, abs=1.0e-14)
    assert positive["uses_zero_temperature_subtracted_condensate"]
    assert positive["ideal_equilibrium_dirac_gas_only"]


def test_thermal_fermion_bias_rejects_invalid_degeneracy_and_temperature():
    from ptum_defects import thermal_fermion_bias

    with pytest.raises(ValueError):
        thermal_fermion_bias([(0.5, 0.2, 1.5)], temperature=1.0)
    with pytest.raises(ValueError):
        thermal_fermion_bias([(0.5, 0.2, 1)], temperature=-1.0)


def test_manuscript_thermal_domain_wall_bias_keeps_ideal_gas_scope_explicit():
    from pathlib import Path

    manuscript = Path("main.tex").read_text(encoding="utf-8")
    normalized_manuscript = " ".join(manuscript.split())
    assert "eq:ptum_thermal_fermion_condensate" in normalized_manuscript
    assert "eq:ptum_thermal_bias" in normalized_manuscript
    assert "Re}[(C_f)_{ii}]" in normalized_manuscript
    assert "ideal-gas contribution only" in normalized_manuscript
    assert "electroweak crossover" in normalized_manuscript
    assert "not a prediction of the PTUM bias or" in normalized_manuscript
    assert "For a conditional benchmark" in normalized_manuscript
    assert "6.49\\times10^{-11}" in normalized_manuscript
    assert "eq:ptum_domain_wall_area_critical" in normalized_manuscript
    assert "2.10\\times10^{-26}" in normalized_manuscript
    assert "does not evolve wall formation or annihilation" in normalized_manuscript



def test_simulation_reports_deterministic_solver_work_statistics():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=1.0e20,
        psi=1.0e4,
        psi_dot=1.0e8,
    )
    t = np.linspace(0.0, 1.0e-9, 51)
    result = run_simulation(
        p, ic, (t[0], t[-1]), t_eval=t,
        max_rhs_evaluations=DEFAULT_MAX_RHS_EVALUATIONS,
    )
    stats = result["solver_stats"]
    assert stats["method"] == "DOP853"
    assert stats["rhs_evaluations"] == stats["nfev"]
    assert 0 < stats["rhs_evaluations"] <= DEFAULT_MAX_RHS_EVALUATIONS
    assert not stats["budget_exhausted"]
    assert stats["time_variable"] == "tau=mu*t"
    assert stats["state_variables_dimensionless"] is True
    assert stats["state_scales"] == dimensionless_state_scale_metadata(p)


def test_simulation_rhs_work_budget_raises_with_exact_attempt_count():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=1.0e20,
        psi=1.0e4,
        psi_dot=1.0e8,
    )
    t = np.linspace(0.0, 1.0e-9, 11)
    with pytest.raises(RHSWorkBudgetExceeded) as error:
        run_simulation(
            p, ic, (t[0], t[-1]), t_eval=t,
            max_rhs_evaluations=1,
        )
    assert error.value.limit == 1
    assert error.value.evaluations == 2


def test_scan_records_budget_exhaustion_and_preserves_it_in_strict_json(tmp_path):
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    rows = run_parameter_scan(
        p,
        psi_init_range=[0.0],
        psi_dot_init_range=[0.0],
        phi_offset_range=[0.01 * p.Phi_c],
        t_max=0.01,
        n_points=5,
        max_rhs_evaluations=1,
    )
    assert len(rows) == 1
    assert not rows[0]["success"]
    assert rows[0]["solver_stats"] == {
        "method": "DOP853",
        "rhs_evaluations": 2,
        "rhs_evaluation_limit": 1,
        "rtol": 1.0e-9,
        "atol": 1.0e-12,
        "budget_exhausted": True,
        "time_variable": "tau=mu*t",
        "state_variables_dimensionless": True,
        "state_scales": dimensionless_state_scale_metadata(p),
    }

    output = tmp_path / "partial_scan.json"
    save_results(rows, str(output))
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert len(payload) == 1
    assert payload[0]["success"] is False
    assert payload[0]["solver_stats"]["budget_exhausted"] is True
    assert payload[0]["solver_stats"]["rhs_evaluations"] == 2



def test_manuscript_thermal_condensate_and_table_floats_have_safe_layout():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert r"\qquad\times" in source
    assert r"\begin{table}[h]" not in source
    assert r"\begin{table}[htbp]" in source



def test_nonfinite_background_state_is_annotated_with_rhs_work_and_fields():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=0.0,
        psi=1.0e100,
        psi_dot=0.0,
    )
    # The deliberately extreme field value overflows the quartic energy
    # term before the solver rejects the non-finite Friedmann source. Treat
    # that warning as part of the tested failure path, not as an unexamined
    # warning in the suite summary.
    with pytest.warns(RuntimeWarning, match="overflow encountered in scalar power"):
        with pytest.raises(RHSIntegrationError) as error:
            run_simulation(
                p, ic, (0.0, 1.0e-9),
                t_eval=np.linspace(0.0, 1.0e-9, 3),
                max_rhs_evaluations=100,
            )
    assert error.value.rhs_evaluations == 1
    assert "rho_psi=inf" in str(error.value)
    assert "psi=1e+100" in str(error.value)


def test_simulation_rejects_nonpositive_or_nonfinite_solver_tolerances():
    p = PTUMParameters()
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=0.0,
        psi=0.0,
        psi_dot=0.0,
    )
    with pytest.raises(ValueError, match="rtol"):
        run_simulation(p, ic, (0.0, 1.0e-9), rtol=0.0)
    with pytest.raises(ValueError, match="atol"):
        run_simulation(p, ic, (0.0, 1.0e-9), atol=float("nan"))



def test_radau_and_dop853_agree_on_a_smooth_evolving_two_field_case():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=1.0e20,
        psi=1.0e4,
        psi_dot=1.0e8,
    )
    t = np.linspace(0.0, 1.0e-9, 101)
    explicit = run_simulation(
        p, ic, (t[0], t[-1]), t_eval=t,
        rtol=1.0e-8, atol=1.0e-10,
        solver_method="DOP853",
    )
    implicit = run_simulation(
        p, ic, (t[0], t[-1]), t_eval=t,
        rtol=1.0e-8, atol=1.0e-10,
        solver_method="Radau",
    )
    assert explicit["solver_stats"]["method"] == "DOP853"
    assert implicit["solver_stats"]["method"] == "Radau"
    scales = {
        "Phi": M_PL,
        "Phi_dot": 1.0e20,
        "psi": 1.0e4,
        "psi_dot": 1.0e8,
    }
    for key, scale in scales.items():
        relative_max = np.max(
            np.abs(explicit[key] - implicit[key])
        ) / scale
        assert relative_max < 5.0e-6


def test_simulation_rejects_unknown_solver_method():
    p = PTUMParameters()
    ic = InitialConditions(
        Phi=0.9 * p.Phi_c,
        Phi_dot=0.0,
        psi=0.0,
        psi_dot=0.0,
    )
    with pytest.raises(ValueError, match="solver_method"):
        run_simulation(
            p, ic, (0.0, 1.0e-9), solver_method="ExplicitEuler"
        )



def test_successful_scan_json_preserves_final_state_for_solver_comparison(tmp_path):
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    rows = run_parameter_scan(
        p,
        psi_init_range=[0.0],
        psi_dot_init_range=[0.0],
        phi_offset_range=[0.01 * p.Phi_c],
        t_max=0.01,
        n_points=11,
        max_rhs_evaluations=DEFAULT_MAX_RHS_EVALUATIONS,
        solver_method="Radau",
    )
    assert rows[0]["success"]
    output = tmp_path / "successful_scan.json"
    save_results(rows, str(output))
    row = json.loads(output.read_text(encoding="utf-8"))[0]
    for key in (
        "final_Phi", "final_Phi_dot", "final_psi", "final_psi_dot",
        "final_H", "final_rho_total", "final_w_psi_exc", "final_Q",
        "final_virial_ratio",
        "max_abs_finite_difference_frw_residual_over_Hrho",
    ):
        assert key in row
    assert row["solver_stats"]["method"] == "Radau"



def test_main_tex_environments_are_balanced_and_nested():
    import re
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    stack = []
    errors = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        # Ignore unescaped comments so commented-out environments do not count.
        line = re.sub(r"(?<!\\)%.*$", "", line)
        for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", line):
            action, environment = match.groups()
            if action == "begin":
                stack.append((environment, line_number))
                continue
            if not stack or stack[-1][0] != environment:
                errors.append((line_number, environment, stack[-1] if stack else None))
            else:
                stack.pop()

    assert not errors, f"Mismatched LaTeX environments: {errors}"
    assert not stack, f"Unclosed LaTeX environments: {stack}"


def test_mukhanov_sasaki_spectrum_claim_remains_author_reported():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    subsection = source.split(
        r"\subsection{Mukhanov--Sasaki mode-by-mode integration}", 1
    )[1].split(r"\section{Late-time dark sector viability}", 1)[0]
    normalized = " ".join(subsection.split())
    assert "AUTHOR-REPORTED" in normalized
    assert "not independently reproduced" in normalized
    assert "does not integrate" in normalized
    assert r"\begin{itemize}" not in subsection
    assert "we performed a full mode-by-mode integration" not in subsection



def test_manuscript_reports_current_radau_scan_failures_and_claim_boundary():
    from pathlib import Path

    source = " ".join(Path("main.tex").read_text(encoding="utf-8").split())
    assert "Radau and BDF full scans each completed 98/100 trajectories" in source
    assert "two rows exhausted" in source
    assert "No trajectory passes the joint quartic classifier" in source
    assert "only two late half-cycles occur" in source
    assert "all three solvers give identical regime labels" in source
    assert "completed all 100/100 trajectories" in source
    assert "all three solvers give identical regime labels" in source
    assert "No trajectory passes the joint quartic classifier" in source
    assert r"current-source DOP853 execution PR \#7 completed the 100-row scan" in source
    assert "neither a quantum-seeded inhomogeneous waterfall" in source



def test_dimensionless_background_rhs_is_equivalent_to_physical_rhs():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    state_physical = np.array([
        0.9 * p.Phi_c,
        -1.0e20,
        0.2 * p.psi_0,
        0.1 * p.mu * p.psi_0,
    ])
    scales = dimensionless_state_scales(p)
    assert scales.shape == (4,)
    assert np.all(np.isfinite(scales))
    assert np.all(scales > 0.0)
    tau = 0.37
    rhs_physical = background_equations(tau / p.mu, state_physical, p)
    rhs_dimensionless = dimensionless_background_equations(
        tau, state_physical / scales, p
    )
    expected = rhs_physical / (p.mu * scales)
    np.testing.assert_allclose(
        rhs_dimensionless, expected, rtol=1.0e-13, atol=1.0e-13
    )


def test_dimensionless_state_scale_metadata_has_correct_component_order():
    p = PTUMParameters(V0=1.0e50, m_psi=1.0e5, lambda_psi=0.1)
    metadata = dimensionless_state_scale_metadata(p)
    assert set(metadata) == {
        "mu_GeV", "Phi_GeV", "Phi_dot_GeV2", "psi_GeV", "psi_dot_GeV2"
    }
    scales = dimensionless_state_scales(p)
    assert metadata["mu_GeV"] == p.mu
    assert metadata["Phi_GeV"] == scales[0]
    assert metadata["Phi_dot_GeV2"] == scales[1]
    assert metadata["psi_GeV"] == scales[2]
    assert metadata["psi_dot_GeV2"] == scales[3]



def test_targeted_convergence_probe_covers_two_budget_rows_and_two_high_Q_controls():
    assert len(CONVERGENCE_CASES) == 4
    assert {case["name"] for case in CONVERGENCE_CASES} == {
        "high_scale_implicit_budget_row",
        "low_scale_implicit_budget_row",
        "high_scale_largest_Q_row",
        "low_scale_largest_Q_row",
    }
    assert OUTPUT_GRIDS == (4001, 8001, 16001, 32001, 64001, 128001, 256001)
    assert TOLERANCE_LEVELS == (
        (1.0e-9, 1.0e-12),
        (1.0e-10, 1.0e-13),
        (1.0e-11, 1.0e-14),
    )


def test_convergence_relative_difference_is_scale_aware_and_handles_missing_values():
    assert relative_difference(1.0, 1.0 + 1.0e-8, 1.0) == pytest.approx(1.0e-8)
    assert relative_difference(0.0, 1.0e-16, 1.0) == pytest.approx(1.0e-2)
    assert relative_difference(None, 1.0, 1.0) is None
    assert _finite_float(float("nan")) is None
    assert _finite_float(float("inf")) is None


def test_convergence_comparison_fails_closed_when_a_run_is_unsuccessful():
    failed = {"success": False, "error": "budget exhausted"}
    successful = {"success": True}
    comparison = _compare_records(failed, successful, None, "tolerance")
    assert comparison["comparison_available"] is False
    assert comparison["reference_success"] is False
    assert comparison["candidate_success"] is True



def test_targeted_convergence_acceptance_limits_are_explicit_and_provisional():
    assert TARGETED_TOLERANCE_LIMITS == {
        "max_final_state_relative_difference": 1.0e-6,
        "max_classification_relative_difference": 1.0e-5,
    }
    assert TARGETED_GRID_LIMITS == {
        "Q_final_absolute_difference": 1.0e-3,
        "w_final_absolute_difference": 1.0e-3,
        "virial_final_absolute_difference": 1.0e-3,
        "finite_difference_continuity_residual_absolute_difference": 1.0e-3,
    }



def test_full_grid_convergence_profile_matches_declared_100_row_dop853_grid():
    assert FULL_GRID_EXPECTED_ROWS == 100
    assert FULL_GRID_N_POINTS == 256001
    assert FULL_GRID_RTOL == 1.0e-9
    assert FULL_GRID_ATOL == 1.0e-12
    assert FULL_GRID_MAX_RHS == 1_000_000



def test_full_grid_json_sanitizer_replaces_nonfinite_values_with_null():
    sanitized = full_grid_json_safe({
        "nan": float("nan"),
        "positive_inf": float("inf"),
        "negative_inf": float("-inf"),
        "nested": [1.0, float("nan")],
    })
    assert sanitized == {
        "nan": None,
        "positive_inf": None,
        "negative_inf": None,
        "nested": [1.0, None],
    }



def test_dense_cycle_integrals_are_invariant_to_output_sampling_density():
    from ptum_task1_simulation import PTUMParameters

    params = PTUMParameters(lambda_psi=0.1)
    mu = params.mu
    amplitude = 0.2 * params.psi_0
    phi_value = 0.99 * params.Phi_c

    # Analytic harmonic trajectory used as a continuous dense-output oracle.
    # Keep tau=mu*t and the physical-time derivative dimensionally consistent
    # with the model mass scale, then vary only the requested output grid.
    def dense_state(tau):
        return np.asarray([
            phi_value,
            0.0,
            amplitude * np.cos(tau),
            -mu * amplitude * np.sin(tau),
        ])

    # Mimic OdeSolution.ts: the adaptive solver mesh is held fixed while
    # t_eval/output sampling changes by a factor of forty.
    dense_state.ts = np.linspace(0.0, 4.0 * np.pi, 4001)
    scales = np.ones(4)
    coarse_tau = np.linspace(0.0, 4.0 * np.pi, 101)
    fine_tau = np.linspace(0.0, 4.0 * np.pi, 4001)
    coarse = compute_dense_cycle_diagnostics(
        dense_state, coarse_tau, mu, scales, params, len(coarse_tau)
    )
    fine = compute_dense_cycle_diagnostics(
        dense_state, fine_tau, mu, scales, params, len(fine_tau)
    )

    expected_q = (
        3.0 * params.lambda_psi * amplitude**2
        / (4.0 * abs(meff_sq_psi(phi_value, params)))
    )
    expected_virial = (
        4.0 * mu**2 / (3.0 * params.lambda_psi * amplitude**2)
    )
    np.testing.assert_allclose(
        coarse["Q"][np.isfinite(coarse["Q"])],
        expected_q, rtol=2.0e-8, atol=0.0,
    )
    np.testing.assert_allclose(
        fine["Q"][np.isfinite(fine["Q"])],
        expected_q, rtol=2.0e-8, atol=0.0,
    )
    np.testing.assert_allclose(
        coarse["virial_ratio"][np.isfinite(coarse["virial_ratio"])],
        expected_virial, rtol=2.0e-8, atol=0.0,
    )
    np.testing.assert_allclose(
        fine["virial_ratio"][np.isfinite(fine["virial_ratio"])],
        expected_virial, rtol=2.0e-8, atol=0.0,
    )
    assert len(coarse["w_avg"]) == len(fine["w_avg"]) == 4
    assert len(coarse["Q_cycle"]) == len(coarse["virial_ratio_cycle"]) == 4
    assert len(coarse["H_avg_cycle"]) == 4
    assert np.all(np.isfinite(coarse["H_avg_cycle"]))
    assert np.all(coarse["H_avg_cycle"] > 0.0)
    np.testing.assert_allclose(
        coarse["turning_times"],
        np.arange(5, dtype=float) * np.pi / mu,
        rtol=0.0, atol=2.0e-10,
    )
    assert coarse["turning_times"] == pytest.approx(
        fine["turning_times"], abs=2.0e-10
    )
    assert coarse["max_relative_quadrature_error"] < 1.0e-8
    assert fine["max_relative_quadrature_error"] < 1.0e-8



def test_dense_cycle_integrals_preserve_physical_units_when_mu_is_not_one():
    from ptum_task1_simulation import PTUMParameters

    mu = 2.5
    # Choose m_psi so the model's tachyonic scale is exactly the non-unit
    # frequency used by the synthetic dense solution.
    params = PTUMParameters(
        lambda_psi=0.1,
        m_psi=mu / np.sqrt(1.0 - 0.99**2),
    )
    assert params.mu == pytest.approx(mu, rel=1.0e-12)
    amplitude = 0.2 * params.psi_0
    phi_value = 0.99 * params.Phi_c

    # The dense ODE solution is parameterized by tau=mu*t, while psi_dot
    # remains a physical-time derivative. This catches accidental mixing
    # of tau derivatives with physical velocities in cycle energies.
    def dense_state(tau):
        return np.asarray([
            phi_value,
            0.0,
            amplitude * np.cos(tau),
            -mu * amplitude * np.sin(tau),
        ])

    dense_state.ts = np.linspace(0.0, 4.0 * np.pi, 4001)
    tau = np.linspace(0.0, 4.0 * np.pi, 101)
    result = compute_dense_cycle_diagnostics(
        dense_state, tau, mu, np.ones(4), params, len(tau)
    )

    expected_q = (
        3.0 * params.lambda_psi * amplitude**2
        / (4.0 * abs(meff_sq_psi(phi_value, params)))
    )
    expected_virial = (
        4.0 * mu**2 / (3.0 * params.lambda_psi * amplitude**2)
    )
    np.testing.assert_allclose(
        result["Q_cycle"], expected_q, rtol=2.0e-8, atol=0.0
    )
    np.testing.assert_allclose(
        result["virial_ratio_cycle"], expected_virial,
        rtol=2.0e-8, atol=0.0,
    )
    np.testing.assert_allclose(
        result["turning_times"],
        np.arange(5, dtype=float) * np.pi / mu,
        rtol=0.0, atol=2.0e-10,
    )
    assert result["root_refinement_converged"]
    assert result["max_relative_quadrature_error"] < 1.0e-8

def test_dense_cycle_root_bracketing_resolves_multiple_turns_per_solver_step():
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 101)
    scales = np.ones(4)

    # Ten simple roots of psi_dot lie inside one deliberately coarse
    # accepted-step interval. Endpoint and midpoint-only bracketing misses
    # most of them, while dense interval subdivision resolves each root.
    frequency = 10.0 * np.pi

    def rapidly_oscillating_state(time):
        return np.asarray([
            0.99 * params.Phi_c,
            0.0,
            np.sin(frequency * time) / frequency,
            np.cos(frequency * time),
        ])

    rapidly_oscillating_state.ts = np.asarray([0.0, 1.0])
    result = compute_dense_cycle_diagnostics(
        rapidly_oscillating_state,
        tau,
        1.0,
        scales,
        params,
        len(tau),
    )
    expected_roots = (np.arange(10, dtype=float) + 0.5) / 10.0
    assert result["turning_times"] == pytest.approx(
        expected_roots, abs=2.0e-10
    )



def test_dense_cycle_root_bracketing_refines_until_root_count_stabilizes():
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 101)
    scales = np.ones(4)
    frequency = 40.0 * np.pi

    def high_frequency_state(time):
        return np.asarray([
            0.99 * params.Phi_c,
            0.0,
            np.sin(frequency * time) / frequency,
            np.cos(frequency * time),
        ])

    # One coarse accepted interval hides many roots at low subdivision
    # counts. The diagnostic must refine until root count and locations agree.
    high_frequency_state.ts = np.asarray([0.0, 1.0])
    result = compute_dense_cycle_diagnostics(
        high_frequency_state, tau, 1.0, scales, params, len(tau)
    )
    expected_roots = (np.arange(40, dtype=float) + 0.5) / 40.0
    assert result["turning_times"] == pytest.approx(
        expected_roots, abs=2.0e-10
    )
    assert result["root_refinement_converged"] is True
    assert result["root_bracketing_subdivisions"] in (32, 64, 128)


def test_dense_cycle_integrals_are_invariant_to_adaptive_solver_mesh_partition():
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 101)
    scales = np.ones(4)
    frequency = 10.0 * np.pi
    phi_value = 0.99 * params.Phi_c
    amplitude = 0.2 * params.psi_0

    def make_dense_state(mesh):
        def dense_state(time):
            return np.asarray([
                phi_value,
                0.0,
                amplitude * np.sin(frequency * time),
                amplitude * frequency * np.cos(frequency * time),
            ])
        dense_state.ts = np.asarray(mesh, dtype=float)
        return dense_state

    coarse_mesh_state = make_dense_state([0.0, 1.0])
    irregular_mesh_state = make_dense_state(
        [0.0, 0.07, 0.19, 0.31, 0.58, 0.73, 0.91, 1.0]
    )
    coarse = compute_dense_cycle_diagnostics(
        coarse_mesh_state, tau, 1.0, scales, params, len(tau)
    )
    irregular = compute_dense_cycle_diagnostics(
        irregular_mesh_state, tau, 1.0, scales, params, len(tau)
    )

    assert coarse["root_refinement_converged"]
    assert irregular["root_refinement_converged"]
    np.testing.assert_allclose(
        coarse["turning_times"], irregular["turning_times"],
        rtol=0.0, atol=2.0e-10,
    )
    np.testing.assert_allclose(
        coarse["Q_cycle"], irregular["Q_cycle"],
        rtol=2.0e-9, atol=0.0,
    )
    np.testing.assert_allclose(
        coarse["virial_ratio_cycle"], irregular["virial_ratio_cycle"],
        rtol=2.0e-9, atol=0.0,
    )
    np.testing.assert_allclose(
        coarse["w_avg"], irregular["w_avg"],
        rtol=2.0e-9, atol=2.0e-12,
    )
    np.testing.assert_allclose(
        coarse["H_avg_cycle"], irregular["H_avg_cycle"],
        rtol=2.0e-9, atol=0.0,
    )



def test_dense_cycle_diagnostics_are_stable_across_real_dop853_step_sizes():
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 501)
    scales = np.ones(4)
    omega = 10.0 * np.pi
    initial = np.asarray([
        0.99 * params.Phi_c,
        0.0,
        0.2 * params.psi_0,
        0.0,
    ])

    def rhs(_time, state):
        return np.asarray([
            state[1],
            0.0,
            state[3],
            -(omega**2) * state[2],
        ])

    solutions = [
        solve_ivp(
            rhs, (0.0, 1.0), initial, method="DOP853",
            rtol=rtol, atol=atol, max_step=max_step,
            dense_output=True,
        )
        for rtol, atol, max_step in (
            (1.0e-8, 1.0e-11, 0.08),
            (1.0e-11, 1.0e-14, 0.025),
        )
    ]
    assert all(solution.success for solution in solutions)
    assert all(solution.sol is not None for solution in solutions)

    diagnostics = [
        compute_dense_cycle_diagnostics(
            solution.sol, tau, 1.0, scales, params, len(tau)
        )
        for solution in solutions
    ]
    coarse, fine = diagnostics
    assert coarse["root_refinement_converged"]
    assert fine["root_refinement_converged"]
    np.testing.assert_allclose(
        coarse["turning_times"], fine["turning_times"],
        rtol=0.0, atol=2.0e-6,
    )
    np.testing.assert_allclose(
        coarse["Q_cycle"], fine["Q_cycle"],
        rtol=2.0e-5, atol=2.0e-10,
    )
    np.testing.assert_allclose(
        coarse["virial_ratio_cycle"], fine["virial_ratio_cycle"],
        rtol=2.0e-5, atol=2.0e-10,
    )
    np.testing.assert_allclose(
        coarse["w_avg"], fine["w_avg"],
        rtol=2.0e-5, atol=2.0e-10,
    )
    np.testing.assert_allclose(
        coarse["H_avg_cycle"], fine["H_avg_cycle"],
        rtol=2.0e-5, atol=2.0e-10,
    )



@pytest.mark.parametrize("bad_time", [np.nan, np.inf, -np.inf])
def test_dense_cycle_diagnostics_reject_nonfinite_output_times(bad_time):
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 11)
    tau[5] = bad_time
    with pytest.raises(ValueError, match="invalid dense-cycle diagnostic inputs"):
        compute_dense_cycle_diagnostics(
            lambda _time: np.zeros(4), tau, 1.0, np.ones(4), params, len(tau)
        )


@pytest.mark.parametrize(
    "bad_state",
    [
        np.zeros(3),
        np.asarray([0.0, 0.0, 0.0, np.nan]),
        np.asarray([0.0, 0.0, 0.0, np.inf]),
    ],
)
def test_dense_cycle_diagnostics_reject_malformed_or_nonfinite_dense_states(
    bad_state,
):
    params = PTUMParameters()
    tau = np.linspace(0.0, 1.0, 11)
    with pytest.raises(
        ValueError, match="dense solution must return four finite state components"
    ):
        compute_dense_cycle_diagnostics(
            lambda _time: bad_state, tau, 1.0, np.ones(4), params, len(tau)
        )



def test_dense_cycle_diagnostics_are_independent_of_output_sampling_density():
    params = PTUMParameters()
    scales = np.ones(4)
    omega = 10.0 * np.pi
    initial = np.asarray([
        0.99 * params.Phi_c,
        0.0,
        0.2 * params.psi_0,
        0.0,
    ])

    def rhs(_time, state):
        return np.asarray([
            state[1],
            0.0,
            state[3],
            -(omega**2) * state[2],
        ])

    solution = solve_ivp(
        rhs, (0.0, 1.0), initial, method="DOP853",
        rtol=1.0e-11, atol=1.0e-14, max_step=0.025,
        dense_output=True,
    )
    assert solution.success
    assert solution.sol is not None

    outputs = [
        np.linspace(0.0, 1.0, count)
        for count in (31, 501, 4001)
    ]
    diagnostics = [
        compute_dense_cycle_diagnostics(
            solution.sol, output_times, 1.0, scales, params, len(output_times)
        )
        for output_times in outputs
    ]
    reference = diagnostics[0]
    for result in diagnostics[1:]:
        np.testing.assert_array_equal(
            result["turning_times"], reference["turning_times"]
        )
        np.testing.assert_array_equal(result["Q_cycle"], reference["Q_cycle"])
        np.testing.assert_array_equal(
            result["virial_ratio_cycle"], reference["virial_ratio_cycle"]
        )
        np.testing.assert_array_equal(result["w_avg"], reference["w_avg"])
        np.testing.assert_array_equal(
            result["H_avg_cycle"], reference["H_avg_cycle"]
        )


def test_dense_cycle_diagnostics_reject_stationary_zero_solution():
    params = PTUMParameters()
    tau = np.linspace(0.0, 20.0, 1001)
    scales = np.ones(4)

    def stationary_state(_tau):
        return np.zeros(4, dtype=float)

    result = compute_dense_cycle_diagnostics(
        stationary_state, tau, 1.0, scales, params, len(tau)
    )
    assert result["turning_times"] == []
    assert len(result["w_avg"]) == 0
    assert len(result["t_avg"]) == 0
    assert not np.any(np.isfinite(result["Q"]))
    assert not np.any(np.isfinite(result["virial_ratio"]))


def test_dense_cycle_diagnostics_do_not_count_monotonic_motion_as_cycles():
    params = PTUMParameters()
    tau = np.linspace(0.0, 20.0, 1001)
    scales = np.ones(4)

    def monotonic_state(time):
        return np.asarray([0.99 * params.Phi_c, 0.0, time, 1.0])

    result = compute_dense_cycle_diagnostics(
        monotonic_state, tau, 1.0, scales, params, len(tau)
    )
    assert result["turning_times"] == []
    assert len(result["w_avg"]) == 0
    assert len(result["t_avg"]) == 0



def test_late_time_adiabaticity_uses_dense_cycle_boundaries_and_hubble_means():
    from ptum_task1_simulation import _late_time_adiabaticity_diagnostic

    # Deliberately nonuniform output times: the final 20% in physical
    # elapsed time starts at t=8. The first late cycle straddles t=8 but
    # has its midpoint at t=8, matching the classifier's midpoint rule.
    # Dense-cycle diagnostics must not depend on sampled H or psi_dot arrays.
    result = {
        "t": np.asarray([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 9.0, 9.5, 10.0]),
        "H": np.asarray([0.5]),
        "psi_dot": np.asarray([0.0]),
        "cycle_turning_times": [1.0, 2.0, 3.0, 4.0, 7.5, 8.5, 9.0, 9.5, 10.0],
        "H_avg_cycle": [0.5, 0.5, 0.5, 0.5, 0.01, 0.01, 0.01, 0.01],
    }
    diagnostic = _late_time_adiabaticity_diagnostic(result)
    expected = 0.01 / (np.pi / 0.5)
    assert diagnostic["n_late_half_cycles"] == 4
    assert diagnostic["H_over_omega_max"] == pytest.approx(expected)
    assert diagnostic["adiabaticity_valid"]



def test_classifier_uses_elapsed_physical_time_for_dense_cycle_tail():
    from ptum_task1_simulation import classify_outcome

    times = np.asarray([
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 9.0, 9.5, 10.0,
    ])
    cycle_midpoints = np.asarray([1.5, 2.5, 3.5, 6.0, 8.25, 8.75, 9.25, 9.75])
    result = {
        "success": True,
        "t": times,
        "w_psi_avg": np.full(8, 1.0 / 3.0),
        "t_avg": cycle_midpoints,
        # The early-time cycles look quartic, but the final 20% in elapsed
        # physical time is deliberately non-quartic.
        "Q_cycle": np.asarray([4.0, 4.0, 4.0, 4.0, 0.2, 0.2, 0.2, 0.2]),
        "virial_ratio_cycle": np.ones(8),
        "quadratic_virial_ratio": np.ones(len(times)),
        "cycle_turning_times": [1.0, 2.0, 3.0, 4.0, 8.0, 8.5, 9.0, 9.5, 10.0],
        "H_avg_cycle": np.full(8, 0.01),
    }
    classification = classify_outcome(result, PTUMParameters())
    assert classification["Q_final"] == pytest.approx(0.2)
    assert classification["regime"] == "non_quartic"
    assert not classification["quartic_achieved"]


def test_full_reheating_scalar_and_higgs_eom_sources_are_explicit_in_manuscript():
    from pathlib import Path

    source = " ".join(Path("main.tex").read_text(encoding="utf-8").split())
    assert "eq:psi_full_reheating_eom" in source
    assert "eq:higgs_full_reheating_eom" in source
    assert r"\begin{aligned} D_\mu D^\mu H" in source
    assert r"=J_H." in source
    assert r"J_H \equiv{}&" in source
    assert r"\frac{\partial U_{{\rm SM},Y}}{\partial H^\dagger}" in source
    assert r"\frac{\partial U_Y}{\partial H^\dagger}" in source
    assert "g_{\\psi H}\\psi H^\\dagger H" in source
    assert "mathcal O_{\\rm SM}" in source
    assert "do not imply that the present homogeneous code evolves the Higgs or fermion fields" in source


def test_pr2_full_scan_opt_in_runs_targeted_convergence_job():
    from pathlib import Path

    workflow = Path(".github/workflows/ptum-scientific-tests.yml").read_text(
        encoding="utf-8"
    )
    convergence_job = workflow.split("  scan-convergence:", 1)[1].split(
        "  latex-build:", 1
    )[0]
    normalized = " ".join(convergence_job.split())
    assert (
        "github.event.pull_request.head.ref == "
        "'ptum/scientific-consistency-fixes-2026-11-13'"
    ) in normalized
    assert "contains(github.event.pull_request.title, '[FULL-SCAN]')" in normalized
    assert "ptum/convergence-" in normalized



def test_pr2_full_scan_opt_in_runs_full_grid_convergence_job():
    from pathlib import Path

    workflow = Path(".github/workflows/ptum-scientific-tests.yml").read_text(
        encoding="utf-8"
    )
    full_grid_job = workflow.split(
        "  scan-full-grid-convergence:", 1
    )[1].split("  latex-build:", 1)[0]
    normalized = " ".join(full_grid_job.split())
    assert (
        "github.event.pull_request.head.ref == "
        "'ptum/scientific-consistency-fixes-2026-11-13'"
    ) in normalized
    assert "contains(github.event.pull_request.title, '[FULL-SCAN]')" in normalized
    assert "python ptum_full_grid_convergence_study.py" in normalized
    assert "256,001" in normalized
    assert "--output ptum_full_grid_convergence_study.json" in normalized
    assert "--checkpoint ptum_full_grid_convergence_study_checkpoint.json" in normalized


def test_paired_convergence_profiles_reuse_one_complete_initial_condition_grid():
    from ptum_full_grid_convergence_study import (
        EXPECTED_ROWS,
        OUTPUT_GRID_REFERENCE,
        OUTPUT_GRID_REFINED,
        STUDY_SPECS,
        TOLERANCE_LEVELS,
        _build_cases,
    )

    cases, scenario_params = _build_cases()
    assert len(cases) == EXPECTED_ROWS == 100
    assert len({case["row_key"] for case in cases}) == EXPECTED_ROWS
    assert len(scenario_params) == 2
    assert all(
        case["params"] is scenario_params[case["scenario"]]
        for case in cases
    )
    assert [spec["n_output_points"] for spec in STUDY_SPECS] == [
        OUTPUT_GRID_REFERENCE,
        OUTPUT_GRID_REFINED,
        OUTPUT_GRID_REFINED,
        OUTPUT_GRID_REFINED,
        OUTPUT_GRID_REFINED,
    ]
    assert len(STUDY_SPECS) == 5
    assert [(spec["rtol"], spec["atol"]) for spec in STUDY_SPECS] == [
        TOLERANCE_LEVELS[0],
        TOLERANCE_LEVELS[0],
        TOLERANCE_LEVELS[1],
        TOLERANCE_LEVELS[2],
        TOLERANCE_LEVELS[3],
    ]


def test_classifier_falls_back_to_sampled_diagnostics_when_dense_cycle_arrays_are_empty():
    result = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.1, 0.2, 1.0 / 3.0, 1.0 / 3.0]),
        "Q": np.concatenate([np.zeros(80), np.full(20, 10.0)]),
        "virial_ratio": np.concatenate([np.full(80, 0.2), np.ones(20)]),
        "t_avg": np.array([]),
        "Q_cycle": np.array([]),
        "virial_ratio_cycle": np.array([]),
    }
    _add_fast_adiabatic_oscillation_history(result)
    classification = classify_outcome(result, PTUMParameters())
    assert classification["regime"] == "quartic"
    assert classification["quartic_achieved"]
    assert classification["Q_final"] == pytest.approx(10.0)


def test_dense_cycle_root_detector_keeps_roundoff_zero_final_endpoint():
    params = PTUMParameters()
    amplitude = 0.2 * params.psi_0

    def dense_state(tau):
        return np.asarray([
            0.99 * params.Phi_c,
            0.0,
            amplitude * np.cos(tau),
            -amplitude * np.sin(tau),
        ])

    dense_state.ts = np.linspace(0.0, 4.0 * np.pi, 401)
    tau = np.linspace(0.0, 4.0 * np.pi, 31)
    result = compute_dense_cycle_diagnostics(
        dense_state, tau, 1.0, np.ones(4), params, len(tau)
    )
    np.testing.assert_allclose(
        result["turning_times"],
        np.arange(5, dtype=float) * np.pi,
        rtol=0.0,
        atol=2.0e-10,
    )
    assert len(result["Q_cycle"]) == 4


def test_paired_full_grid_study_uses_five_complete_profiles():
    from ptum_full_grid_convergence_study import STUDY_SPECS

    assert [item["name"] for item in STUDY_SPECS] == [
        "reference_4001",
        "grid_256001",
        "tolerance_1e-10_1e-13",
        "tolerance_1e-11_1e-14",
        "tolerance_1e-12_1e-15",
    ]
    assert [item["comparison_role"] for item in STUDY_SPECS] == [
        "reference",
        "output_grid",
        "solver_tolerance",
        "solver_tolerance",
        "solver_tolerance",
    ]
    assert [(item["rtol"], item["atol"]) for item in STUDY_SPECS] == [
        (1.0e-9, 1.0e-12),
        (1.0e-9, 1.0e-12),
        (1.0e-10, 1.0e-13),
        (1.0e-11, 1.0e-14),
        (1.0e-12, 1.0e-15),
    ]
    assert STUDY_SPECS[0]["n_output_points"] == 4001
    assert all(item["n_output_points"] == 256001 for item in STUDY_SPECS[1:])


def test_paired_full_grid_row_key_uses_dimensionless_initial_conditions():
    from ptum_full_grid_convergence_study import build_row_key

    params = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    key = build_row_key(
        "low_scale_underdamped_control",
        {
            "psi_init": 2.0 * params.psi_0,
            "psi_dot_init": 0.5 * params.mu * params.psi_0,
            "phi_offset": 0.01 * params.Phi_c,
        },
        params,
    )
    assert key == (
        "low_scale_underdamped_control|seed=2|velocity=0.5|offset=0.01"
    )


def test_paired_full_grid_comparator_accepts_identical_complete_records():
    from ptum_full_grid_convergence_study import compare_records

    params = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    record = {
        "success": True,
        "row_key": "synthetic|seed=1|velocity=0|offset=0.01",
        "final_state": {
            "Phi": params.Phi_c,
            "Phi_dot": params.mu * params.Phi_c,
            "psi": params.psi_0,
            "psi_dot": params.mu * params.psi_0,
            "H": params.H_threshold_exact_end,
            "rho_total": params.V0,
        },
        "classification": {
            "Q_final": 2.2,
            "w_final": 1.0 / 3.0,
            "virial_final": 1.0,
            "quadratic_virial_final": 0.0,
            "H_over_omega_max": 0.01,
            "regime": "quartic",
            "quartic_achieved": True,
            "n_late_half_cycles": 5,
            "n_oscillations": 5,
            "adiabaticity_valid": True,
        },
        "diagnostics": {
            "max_abs_relative_frw_continuity_residual": 1.0e-10,
            "max_abs_finite_difference_frw_residual_over_Hrho": 1.0e-3,
        },
    }
    comparison = compare_records(record, record, params, "solver_tolerance")
    assert comparison["comparison_available"]
    assert comparison["comparison_pass"]


def test_paired_full_grid_comparator_rejects_state_or_regime_instability():
    from copy import deepcopy
    from ptum_full_grid_convergence_study import compare_records

    params = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    reference = {
        "success": True,
        "row_key": "synthetic|seed=1|velocity=0|offset=0.01",
        "final_state": {
            "Phi": params.Phi_c,
            "Phi_dot": params.mu * params.Phi_c,
            "psi": params.psi_0,
            "psi_dot": params.mu * params.psi_0,
            "H": params.H_threshold_exact_end,
            "rho_total": params.V0,
        },
        "classification": {
            "Q_final": 2.2,
            "w_final": 1.0 / 3.0,
            "virial_final": 1.0,
            "quadratic_virial_final": 0.0,
            "H_over_omega_max": 0.01,
            "regime": "quartic",
            "quartic_achieved": True,
            "n_late_half_cycles": 5,
            "n_oscillations": 5,
            "adiabaticity_valid": True,
        },
        "diagnostics": {
            "max_abs_relative_frw_continuity_residual": 1.0e-10,
            "max_abs_finite_difference_frw_residual_over_Hrho": 1.0e-3,
        },
    }
    unstable_state = deepcopy(reference)
    unstable_state["final_state"]["Phi"] *= 1.0 + 2.0e-6
    assert not compare_records(
        reference, unstable_state, params, "solver_tolerance"
    )["comparison_pass"]

    unstable_regime = deepcopy(reference)
    unstable_regime["classification"]["regime"] = "non_quartic"
    unstable_regime["classification"]["quartic_achieved"] = False
    assert not compare_records(
        reference, unstable_regime, params, "solver_tolerance"
    )["comparison_pass"]


def test_paired_comparator_normalizes_near_zero_dimensionless_w_absolutely():
    from copy import deepcopy
    from ptum_full_grid_convergence_study import compare_records

    params = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    reference = {
        "success": True,
        "row_key": "synthetic|seed=1|velocity=0|offset=0.01",
        "final_state": {
            "Phi": params.Phi_c,
            "Phi_dot": params.mu * params.Phi_c,
            "psi": params.psi_0,
            "psi_dot": params.mu * params.psi_0,
            "H": params.H_threshold_exact_end,
            "rho_total": params.V0,
        },
        "classification": {
            "Q_final": 1.0,
            "w_final": -2.5329e-6,
            "virial_final": 1.0,
            "quadratic_virial_final": None,
            "H_over_omega_max": 0.01,
            "regime": "non_quartic",
            "quartic_achieved": False,
            "n_late_half_cycles": 5,
            "n_oscillations": 5,
            "adiabaticity_valid": True,
        },
        "diagnostics": {
            "max_abs_relative_frw_continuity_residual": 1.0e-10,
            "max_abs_finite_difference_frw_residual_over_Hrho": 1.0e-3,
        },
    }
    candidate = deepcopy(reference)
    candidate["classification"]["w_final"] += 1.0e-10

    comparison = compare_records(
        reference, candidate, params, "solver_tolerance"
    )
    assert (
        comparison["classification_relative_differences"]["w_final"]
        > 1.0e-5
    )
    assert (
        comparison["classification_normalized_absolute_differences"]["w_final"]
        == pytest.approx(1.0e-10)
    )
    assert comparison["classification_pass"]
    assert comparison["comparison_pass"]


def test_output_grid_comparison_requires_finite_difference_residual_reduction():
    from copy import deepcopy
    from ptum_full_grid_convergence_study import compare_records

    params = PTUMParameters(V0=1.0e56, m_psi=1.0e13, lambda_psi=0.1)
    reference = {
        "success": True,
        "row_key": "synthetic|seed=1|velocity=0|offset=0.01",
        "final_state": {
            "Phi": params.Phi_c,
            "Phi_dot": params.mu * params.Phi_c,
            "psi": params.psi_0,
            "psi_dot": params.mu * params.psi_0,
            "H": params.H_threshold_exact_end,
            "rho_total": params.V0,
        },
        "classification": {
            "Q_final": 2.2,
            "w_final": 1.0 / 3.0,
            "virial_final": 1.0,
            "quadratic_virial_final": None,
            "H_over_omega_max": 0.01,
            "regime": "non_quartic",
            "quartic_achieved": False,
            "n_late_half_cycles": 5,
            "n_oscillations": 5,
            "adiabaticity_valid": True,
        },
        "diagnostics": {
            "max_abs_relative_frw_continuity_residual": 1.0e-10,
            "max_abs_finite_difference_frw_residual_over_Hrho": 1.0e-2,
        },
    }
    refined = deepcopy(reference)
    refined["diagnostics"][
        "max_abs_finite_difference_frw_residual_over_Hrho"
    ] = 1.0e-2 / 64.0
    comparison = compare_records(reference, refined, params, "output_grid")
    assert comparison["comparison_pass"]
    assert comparison["finite_difference_residual_grid_reduction_factor"] == pytest.approx(64.0)
    assert comparison["finite_difference_residual_grid_observed_order"] == pytest.approx(1.0)

    no_improvement = deepcopy(reference)
    no_improvement["diagnostics"][
        "max_abs_finite_difference_frw_residual_over_Hrho"
    ] = 1.01e-2
    assert not compare_records(
        reference, no_improvement, params, "output_grid"
    )["comparison_pass"]


def test_output_grid_fd_summary_requires_all_rows_and_near_first_order_scaling():
    from ptum_full_grid_convergence_study import (
        summarize_output_grid_finite_difference_convergence,
    )

    comparisons = [
        {
            "comparison_role": "output_grid",
            "comparison_available": True,
            "reference_finite_difference_residual_over_Hrho": 1.0,
            "candidate_finite_difference_residual_over_Hrho": 1.0 / 64.0,
        },
        {
            "comparison_role": "output_grid",
            "comparison_available": True,
            "reference_finite_difference_residual_over_Hrho": 1.0,
            "candidate_finite_difference_residual_over_Hrho": 1.0 / 32.0,
        },
    ]
    summary = summarize_output_grid_finite_difference_convergence(
        comparisons, expected_rows=2
    )
    assert summary["pass"]
    assert summary["median_observed_order"] == pytest.approx(11.0 / 12.0)

    failed = [dict(item) for item in comparisons]
    failed[1]["candidate_finite_difference_residual_over_Hrho"] = 1.1
    assert not summarize_output_grid_finite_difference_convergence(
        failed, expected_rows=2
    )["pass"]
    assert not summarize_output_grid_finite_difference_convergence(
        comparisons[:1], expected_rows=2
    )["pass"]


def test_paired_tolerance_summary_requires_monotonic_envelopes_and_final_pair():
    from copy import deepcopy
    from ptum_full_grid_convergence_study import (
        FINAL_FIELDS,
        CLASSIFICATION_METRICS,
        STUDY_SPECS,
        summarize_solver_tolerance_convergence,
    )

    tolerance_specs = [
        item["name"] for item in STUDY_SPECS
        if item["comparison_role"] == "solver_tolerance"
    ]
    comparisons = []
    for step_index, candidate_spec in enumerate(tolerance_specs):
        state_error = 1.0e-3 * (0.1 ** step_index)
        classification_error = 1.0e-5 * (0.1 ** step_index)
        for row_index in range(2):
            comparisons.append({
                "comparison_role": "solver_tolerance",
                "candidate_spec": candidate_spec,
                "row_key": f"row-{row_index}",
                "comparison_pass": step_index == len(tolerance_specs) - 1,
                "state_relative_differences": {
                    field: state_error for field in FINAL_FIELDS
                },
                "classification_normalized_absolute_differences": {
                    field: classification_error
                    for field in CLASSIFICATION_METRICS
                },
                "flags_pass": True,
                "classification_metric_availability_match": True,
                "chain_rule_pass": True,
                "finite_difference_residual_pass": True,
                "max_chain_rule_residual_absolute_difference": 1.0e-10,
                "max_finite_difference_residual_absolute_difference": 1.0e-6,
            })

    summary = summarize_solver_tolerance_convergence(
        comparisons, expected_rows=2
    )
    assert summary["pass"]
    assert summary["final_refinement_passing_comparisons"] == 2
    assert summary["monotonic_state_error_envelope"]
    assert summary["monotonic_classification_error_envelope"]

    unavailable_metric = deepcopy(comparisons)
    for row in unavailable_metric:
        row["classification_normalized_absolute_differences"][
            "quadratic_virial_final"
        ] = None
    unavailable_summary = summarize_solver_tolerance_convergence(
        unavailable_metric, expected_rows=2
    )
    assert unavailable_summary["pass"]
    assert "quadratic_virial_final" in (
        unavailable_summary["consistently_unavailable_classification_fields"]
    )

    incomplete_state = deepcopy(comparisons)
    first_spec = tolerance_specs[0]
    first_row = next(
        row for row in incomplete_state
        if row["candidate_spec"] == first_spec
    )
    first_row["state_relative_differences"]["psi"] = None
    assert not summarize_solver_tolerance_convergence(
        incomplete_state, expected_rows=2
    )["pass"]

    nonmonotonic = deepcopy(comparisons)
    last_spec = tolerance_specs[-1]
    last_row = next(
        row for row in nonmonotonic
        if row["candidate_spec"] == last_spec
    )
    last_row["state_relative_differences"]["psi_dot"] = 2.0e-3
    assert not summarize_solver_tolerance_convergence(
        nonmonotonic, expected_rows=2
    )["pass"]

    final_pair_failure = deepcopy(comparisons)
    final_row = next(
        row for row in final_pair_failure
        if row["candidate_spec"] == last_spec
    )
    final_row["comparison_pass"] = False
    assert not summarize_solver_tolerance_convergence(
        final_pair_failure, expected_rows=2
    )["pass"]


def test_pr2_full_scan_opt_in_runs_paired_full_grid_convergence_job():
    from pathlib import Path

    workflow = Path(".github/workflows/ptum-scientific-tests.yml").read_text(
        encoding="utf-8"
    )
    push_branches = workflow.split("  push:", 1)[1].split(
        "  pull_request:", 1
    )[0]
    assert "ptum/scientific-consistency-fixes-2026-11-13" in push_branches
    assert "contains(github.event.head_commit.message, '[FULL-SCAN]')" in workflow
    assert "ptum_full_grid_convergence_study.py" in workflow

    for job_name in ("full-waterfall-scan:", "scan-convergence:",
                     "scan-full-grid-convergence:"):
        job = workflow.split(f"  {job_name}", 1)[1]
        if job_name != "scan-full-grid-convergence:":
            job = job.split(f"  {('scan-convergence:' if job_name == 'full-waterfall-scan:' else 'scan-full-grid-convergence:')}", 1)[0]
        else:
            job = job.split("  latex-build:", 1)[0]
        assert "github.event_name == 'workflow_dispatch'" in job
        assert "github.event_name == 'push'" in job
        assert "github.event.head_commit.message" in job

    assert "ptum-full-grid-convergence-study" in workflow


def test_action_derived_sector_currents_match_variations_and_cancel():
    from ptum_sector_currents import action_derived_sector_currents

    Phi, psi = 0.73, -0.41
    chi, Phi_res = 0.62, -0.88
    alpha, m_psi, E_th = 1.3, 2.2, 4.7
    g_psiH, g_DM, Lambda, O_SM = 0.37, 0.21, 3.4, -0.29
    grad_phi = np.array([0.2, -0.1, 0.07, 0.3])
    grad_psi = np.array([-0.11, 0.09, 0.04, -0.2])
    grad_phi_res = np.array([0.08, 0.12, -0.17, 0.03])
    higgs_real = np.array([0.4, -0.2, 0.6, 0.3])
    higgs_covariant_grad = np.array(
        [
            [0.03, -0.02, 0.04, 0.01],
            [0.05, 0.01, -0.03, 0.02],
            [-0.04, 0.06, 0.02, -0.01],
            [0.02, -0.03, 0.05, 0.07],
        ]
    )
    grad_higgs_norm = np.sum(
        higgs_real[:, None] * higgs_covariant_grad, axis=0
    )

    currents = action_derived_sector_currents(
        Phi=Phi,
        psi=psi,
        grad_Phi=grad_phi,
        grad_psi=grad_psi,
        grad_HdaggerH=grad_higgs_norm,
        chi=chi,
        Phi_res=Phi_res,
        grad_Phi_res=grad_phi_res,
        O_SM=O_SM,
        alpha=alpha,
        m_psi=m_psi,
        E_th=E_th,
        g_psiH=g_psiH,
        g_DM=g_DM,
        Lambda=Lambda,
    )

    eps = 1.0e-6
    coeff = alpha * m_psi**2 / E_th**2
    U_phi_psi = lambda value: 0.5 * coeff * value**2 * psi**2
    dU_dPhi_fd = (
        U_phi_psi(Phi + eps) - U_phi_psi(Phi - eps)
    ) / (2.0 * eps)
    np.testing.assert_allclose(
        currents["Phi"], dU_dPhi_fd * grad_phi, rtol=2.0e-9, atol=1.0e-13
    )

    def U_psi_H(h):
        return 0.5 * g_psiH * psi**2 * (0.5 * np.dot(h, h))

    q_higgs_fd = np.empty(4)
    for nu in range(4):
        plus = higgs_real + eps * higgs_covariant_grad[:, nu]
        minus = higgs_real - eps * higgs_covariant_grad[:, nu]
        q_higgs_fd[nu] = (U_psi_H(plus) - U_psi_H(minus)) / (2.0 * eps)
    q_yukawa = (O_SM / Lambda) * grad_psi
    np.testing.assert_allclose(
        currents["SM"] + q_yukawa,
        q_higgs_fd,
        rtol=2.0e-9,
        atol=1.0e-13,
    )

    U_chi_res = lambda value: g_DM * chi**2 * value**2
    dU_dPhi_res_fd = (
        U_chi_res(Phi_res + eps) - U_chi_res(Phi_res - eps)
    ) / (2.0 * eps)
    np.testing.assert_allclose(
        currents["DE"],
        dU_dPhi_res_fd * grad_phi_res,
        rtol=2.0e-9,
        atol=1.0e-13,
    )

    q_phi = dU_dPhi_fd * grad_phi
    q_higgs = q_higgs_fd
    q_yukawa_fd = (O_SM / Lambda) * grad_psi
    np.testing.assert_allclose(
        currents["psi"],
        -q_phi - q_higgs + q_yukawa_fd,
        rtol=2.0e-9,
        atol=1.0e-13,
    )
    np.testing.assert_allclose(
        sum(currents.values()),
        np.zeros(4),
        rtol=0.0,
        atol=2.0e-15,
    )


def test_action_derived_homogeneous_current_matches_minus_plus_metric_sign():
    from ptum_sector_currents import action_derived_sector_currents

    params = PTUMParameters()
    Phi = 0.9 * params.Phi_c
    psi = 0.2 * params.psi_0
    Phi_dot = -1.0e20
    currents = action_derived_sector_currents(
        Phi=Phi,
        psi=psi,
        grad_Phi=np.array([-Phi_dot, 0.0, 0.0, 0.0]),
        grad_psi=np.zeros(4),
        grad_HdaggerH=np.zeros(4),
        chi=0.0,
        Phi_res=0.0,
        grad_Phi_res=np.zeros(4),
        O_SM=0.0,
        alpha=params.alpha,
        m_psi=params.m_psi,
        E_th=params.E_th,
        g_psiH=0.0,
        g_DM=0.0,
        Lambda=1.0,
    )
    q_psi_code, _ = waterfall_transfer_rate(
        Phi=Phi, psi=psi, Phi_dot=Phi_dot, params=params
    )
    assert currents["psi"][0] == pytest.approx(q_psi_code, rel=2.0e-15)
    assert currents["psi"][0] < 0.0
    np.testing.assert_allclose(
        sum(currents.values()), np.zeros(4), rtol=0.0, atol=0.0
    )


def test_action_derived_sector_currents_reject_malformed_gradients_and_scales():
    from ptum_sector_currents import action_derived_sector_currents

    arguments = dict(
        Phi=1.0,
        psi=0.2,
        grad_Phi=np.zeros(4),
        grad_psi=np.zeros(4),
        grad_HdaggerH=np.zeros(4),
        chi=0.3,
        Phi_res=0.4,
        grad_Phi_res=np.zeros(4),
        O_SM=0.1,
        alpha=1.0,
        m_psi=2.0,
        E_th=3.0,
        g_psiH=0.1,
        g_DM=0.2,
        Lambda=4.0,
    )
    with pytest.raises(ValueError, match="contravariant four-vector"):
        action_derived_sector_currents(**{**arguments, "grad_Phi": np.zeros(3)})
    with pytest.raises(ValueError, match="strictly positive"):
        action_derived_sector_currents(**{**arguments, "Lambda": 0.0})


def test_dirac_and_real_scalar_reheating_examples_are_explicitly_toy_models():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    normalized = " ".join(source.split())
    assert r"\mathcal{L}_{Y}^{\rm toy}=-y_\psi\psi\bar f f" in normalized
    assert "generic vector-like Dirac toy" in normalized
    assert "not the gauge-invariant electroweak operator" in normalized
    assert r"\psi\mathcal O_{\rm SM}/\Lambda" in normalized
    assert r"\bar Q_L C_d H d_R" in normalized
    assert r"\bar Q_L C_u\widetilde H u_R" in normalized
    assert r"\bar L_L C_e H e_R" in normalized
    assert r"U_{\rm toy}=\tfrac12g_{\rm toy}\psi^2\varphi_{\rm toy}^2" in normalized
    assert "not identified with the Standard Model Higgs doublet" in normalized
    assert r"\eqref{eq:sm_hilbert_tensor}" in normalized
    assert "do not replace the still-missing explicit SM action" not in normalized

def test_periodic_lattice_operators_satisfy_discrete_integration_by_parts():
    from ptum_lattice_waterfall import periodic_laplacian_and_gradient_energy

    rng = np.random.default_rng(20261119)
    field = rng.normal(size=(8, 8, 8))
    laplacian, gradient_norm_squared = periodic_laplacian_and_gradient_energy(
        field, dx=0.37
    )
    np.testing.assert_allclose(
        np.mean(field * laplacian),
        -np.mean(gradient_norm_squared),
        rtol=2.0e-14,
        atol=2.0e-14,
    )


def test_lattice_homogeneous_limit_matches_existing_two_field_ode():
    from ptum_lattice_waterfall import run_lattice_waterfall

    params = PTUMParameters(V0=1.0e56)
    mu = params.mu
    psi0 = params.psi_0
    phi = 0.99 * params.Phi_c
    phi_dot = -0.005 * mu * params.Phi_c
    psi = 0.03 * psi0
    psi_dot = 0.001 * mu * psi0
    tau = np.linspace(0.0, 0.03, 31)

    lattice = run_lattice_waterfall(
        params,
        Phi_initial=phi,
        Phi_dot_initial=phi_dot,
        psi_initial=np.full((4, 4, 4), psi),
        psi_dot_initial=np.full((4, 4, 4), psi_dot),
        box_size_over_mu=4.0,
        tau_span=(float(tau[0]), float(tau[-1])),
        n_output_points=len(tau),
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    ode = run_simulation(
        params,
        InitialConditions(
            Phi=phi,
            Phi_dot=phi_dot,
            psi=psi,
            psi_dot=psi_dot,
        ),
        (float(tau[0] / mu), float(tau[-1] / mu)),
        t_eval=tau / mu,
        rtol=1.0e-10,
        atol=1.0e-12,
        max_rhs_evaluations=None,
    )

    assert ode["success"]
    np.testing.assert_allclose(lattice["Phi"], ode["Phi"], rtol=5.0e-8)
    np.testing.assert_allclose(lattice["Phi_dot"], ode["Phi_dot"], rtol=5.0e-8)
    np.testing.assert_allclose(
        lattice["psi"][:, 0, 0, 0], ode["psi"], rtol=5.0e-8
    )
    np.testing.assert_allclose(
        lattice["psi_dot"][:, 0, 0, 0], ode["psi_dot"], rtol=5.0e-8
    )
    np.testing.assert_allclose(lattice["H"], ode["H"], rtol=5.0e-8)
    assert np.allclose(lattice["wall_area_density_over_mu"], 0.0)
    assert lattice["max_abs_rhs_energy_balance_residual_relative"] < 1.0e-12


def test_inhomogeneous_lattice_reports_classical_backreaction_and_wall_geometry():
    from ptum_lattice_waterfall import run_lattice_waterfall

    params = PTUMParameters(V0=1.0e56)
    n = 8
    coordinate = np.arange(n, dtype=float)
    profile = np.cos(2.0 * np.pi * coordinate / n + 0.23)
    psi_initial = (
        0.03 * params.psi_0
        * profile[:, None, None]
        * np.ones((1, n, n))
    )
    result = run_lattice_waterfall(
        params,
        Phi_initial=0.99 * params.Phi_c,
        Phi_dot_initial=-0.005 * params.mu * params.Phi_c,
        psi_initial=psi_initial,
        psi_dot_initial=np.zeros_like(psi_initial),
        box_size_over_mu=8.0,
        tau_span=(0.0, 0.02),
        n_output_points=21,
        rtol=1.0e-9,
        atol=1.0e-11,
    )

    assert result["success"]
    assert result["backreaction_included"]
    assert result["nonlinear_mode_coupling_included"]
    assert result["classical_rescattering_included"]
    assert not result["quantum_vacuum_seeded"]
    assert not result["vacuum_renormalized"]
    assert not result["continuum_limit_demonstrated"]
    assert result["initial_seed_interpretation"] == "caller_supplied_classical_field"
    assert np.all(np.isfinite(result["rho_total"]))
    assert np.all(np.isfinite(result["psi_gradient_energy_density"]))
    assert np.max(result["psi_gradient_energy_density"]) > 0.0
    assert np.max(result["psi_variance"]) > 0.0
    assert np.max(result["wall_area_density_over_mu"]) > 0.0
    assert np.all(np.diff(result["scale_factor"]) > 0.0)
    assert np.all(np.isfinite(result["continuity_residual_relative"]))
    assert result["max_abs_rhs_energy_balance_residual_relative"] < 1.0e-12

def test_lattice_wall_area_counts_zero_crossings_once_with_periodic_boundaries():
    from ptum_lattice_waterfall import _wall_area_density_over_mu

    profile = np.array([-1.0, 0.0, 1.0, 1.0])
    field = np.broadcast_to(profile[:, None, None], (4, 4, 4)).copy()
    # Two planar sign changes per periodic length L=4*dx.
    assert _wall_area_density_over_mu(field, dx=1.0, scale_factor=1.0) == pytest.approx(0.5)

def test_manuscript_distinguishes_classical_lattice_prototype_from_quantum_waterfall():
    from pathlib import Path

    source = " ".join(Path("main.tex").read_text(encoding="utf-8").split())
    required = (
        r"\texttt{ptum\_lattice\_waterfall.py}",
        r"\label{eq:ptum_lattice_psi}",
        r"\label{eq:ptum_lattice_phi}",
        r"\label{eq:ptum_lattice_friedmann}",
        r"\label{eq:ptum_lattice_pressure}",
        r"\partial_\Phi m_{\rm eff}^2",
        "caller-supplied classical initial fields",
        "bare first-order adiabatic-WKB Gaussian samples",
        "symmetrized free-mode two-point covariance",
        "zero-point energy is retained",
        "not a renormalized quantum-seeded waterfall",
        "vacuum counterterms or continuum renormalization",
        "not a nonlinear lattice simulation of the full four-field system",
        "internal identity of the implemented discrete equations",
        "the authors' original lattice/perturbation implementation is not public",
    )
    for phrase in required:
        assert phrase in source
    assert "does not expose an individually reviewable PTUM lattice solver" not in source
    assert "lattice code not yet public" not in source



def test_adiabatic_vacuum_sampler_is_reproducible_and_uses_lattice_dispersion():
    from ptum_lattice_waterfall import sample_adiabatic_vacuum_initial_conditions

    params = PTUMParameters(V0=1.0e56)
    n = 4
    box = 8.0
    phi = 1.2 * params.Phi_c
    phi_dot = -1.0e-4 * params.mu * params.Phi_c
    first = sample_adiabatic_vacuum_initial_conditions(
        params,
        grid_size=n,
        box_size_over_mu=box,
        Phi_initial=phi,
        Phi_dot_initial=phi_dot,
        seed=20261120,
    )
    repeated = sample_adiabatic_vacuum_initial_conditions(
        params,
        grid_size=n,
        box_size_over_mu=box,
        Phi_initial=phi,
        Phi_dot_initial=phi_dot,
        seed=20261120,
    )

    np.testing.assert_array_equal(first["psi_initial"], repeated["psi_initial"])
    np.testing.assert_array_equal(first["psi_dot_initial"], repeated["psi_dot_initial"])
    assert first["metadata"]["all_modes_stable"]
    assert first["metadata"]["all_modes_adiabatic"]
    assert first["metadata"]["maximum_adiabaticity_parameter"] <= 0.1
    assert first["metadata"]["vacuum_renormalized"] is False
    assert first["metadata"]["zero_point_energy_retained"] is True
    assert first["metadata"]["full_quantum_evolution"] is False

    dx = box / n
    expected_k2 = 4.0 * np.sin(np.pi / n) ** 2 / dx**2
    assert first["diagnostics"]["lattice_k_squared_over_mu2"][1, 0, 0] == pytest.approx(
        expected_k2, rel=1.0e-14
    )
    eta = first["metadata"]["m_eff_squared_over_mu2"]
    h = first["metadata"]["H_background_over_mu"]
    h_prime = first["metadata"]["H_prime_over_mu2"]
    expected_omega_squared = expected_k2 + eta - 1.5 * h_prime - 2.25 * h**2
    omega = first["diagnostics"]["mode_frequency_over_mu"][1, 0, 0]
    assert omega**2 == pytest.approx(expected_omega_squared, rel=1.0e-13)


def test_adiabatic_vacuum_sampler_rejects_tachyonic_and_nonadiabatic_states():
    from ptum_lattice_waterfall import sample_adiabatic_vacuum_initial_conditions

    params = PTUMParameters(V0=1.0e56)
    common = {
        "grid_size": 4,
        "box_size_over_mu": 8.0,
        "Phi_dot_initial": -1.0e-4 * params.mu * params.Phi_c,
        "seed": 7,
    }
    with pytest.raises(ValueError, match="tachyonic threshold"):
        sample_adiabatic_vacuum_initial_conditions(
            params, Phi_initial=0.99 * params.Phi_c, **common
        )
    with pytest.raises(ValueError, match="not adiabatic"):
        sample_adiabatic_vacuum_initial_conditions(
            params,
            Phi_initial=1.2 * params.Phi_c,
            adiabaticity_tolerance=1.0e-12,
            **common,
        )


def test_adiabatic_vacuum_sampler_reproduces_symmetrized_free_mode_covariance():
    from ptum_lattice_waterfall import sample_adiabatic_vacuum_initial_conditions

    params = PTUMParameters(V0=1.0e56)
    n = 4
    box = 8.0
    volume = box**3
    mode = (1, 0, 0)
    phi = 1.2 * params.Phi_c
    phi_dot = -1.0e-4 * params.mu * params.Phi_c
    reference = sample_adiabatic_vacuum_initial_conditions(
        params,
        grid_size=n,
        box_size_over_mu=box,
        Phi_initial=phi,
        Phi_dot_initial=phi_dot,
        seed=0,
    )
    omega = reference["diagnostics"]["mode_frequency_over_mu"][mode]
    omega_prime = reference["diagnostics"]["mode_frequency_derivative"][mode]
    velocity_shift = reference["diagnostics"]["velocity_shift"]
    expected_field_power = params.lambda_psi / (2.0 * omega)
    expected_residual_velocity_power = params.lambda_psi * omega / 2.0

    field_powers = []
    residual_velocity_powers = []
    cross_powers = []
    for realization in range(256):
        sample = sample_adiabatic_vacuum_initial_conditions(
            params,
            grid_size=n,
            box_size_over_mu=box,
            Phi_initial=phi,
            Phi_dot_initial=phi_dot,
            seed=realization,
        )
        dimensionless_field = sample["psi_initial"] / params.psi_0
        dimensionless_velocity = sample["psi_dot_initial"] / (
            params.mu * params.psi_0
        )
        field_fourier = np.fft.fftn(dimensionless_field) * np.sqrt(volume) / n**3
        residual_fourier = (
            np.fft.fftn(dimensionless_velocity - velocity_shift * dimensionless_field)
            * np.sqrt(volume) / n**3
        )
        q_mode = field_fourier[mode]
        r_mode = residual_fourier[mode]
        field_powers.append(abs(q_mode) ** 2)
        residual_velocity_powers.append(abs(r_mode) ** 2)
        cross_powers.append((q_mode * np.conjugate(r_mode)).real)

    assert np.mean(field_powers) == pytest.approx(expected_field_power, rel=0.2)
    assert np.mean(residual_velocity_powers) == pytest.approx(
        expected_residual_velocity_power, rel=0.2
    )
    assert abs(np.mean(cross_powers)) < (
        0.15 * np.sqrt(expected_field_power * expected_residual_velocity_power)
    )
    assert np.isfinite(omega_prime)


def test_lattice_tracks_bare_adiabatic_sample_without_claiming_quantum_evolution():
    from ptum_lattice_waterfall import (
        run_lattice_waterfall,
        sample_adiabatic_vacuum_initial_conditions,
    )

    params = PTUMParameters(V0=1.0e56)
    sample = sample_adiabatic_vacuum_initial_conditions(
        params,
        grid_size=4,
        box_size_over_mu=4.0,
        Phi_initial=1.2 * params.Phi_c,
        Phi_dot_initial=-1.0e-4 * params.mu * params.Phi_c,
        seed=41,
    )
    result = run_lattice_waterfall(
        params,
        Phi_initial=1.2 * params.Phi_c,
        Phi_dot_initial=-1.0e-4 * params.mu * params.Phi_c,
        psi_initial=sample["psi_initial"],
        psi_dot_initial=sample["psi_dot_initial"],
        box_size_over_mu=4.0,
        tau_span=(0.0, 1.0e-3),
        n_output_points=3,
        rtol=1.0e-8,
        atol=1.0e-10,
        initial_state_metadata=sample["metadata"],
    )
    assert result["bare_adiabatic_vacuum_sampled"]
    assert result["bare_zero_point_energy_present"]
    assert result["initial_seed_interpretation"] == (
        "bare_first_order_adiabatic_wkb_gaussian_classical_statistical_sample"
    )
    assert result["quantum_vacuum_seeded"] is False
    assert result["vacuum_renormalized"] is False
    assert result["initial_state_metadata"]["seed"] == 41

    altered_field = sample["psi_initial"].copy()
    altered_field[0, 0, 0] += 1.0
    with pytest.raises(ValueError, match="field hash does not match"):
        run_lattice_waterfall(
            params,
            Phi_initial=1.2 * params.Phi_c,
            Phi_dot_initial=-1.0e-4 * params.mu * params.Phi_c,
            psi_initial=altered_field,
            psi_dot_initial=sample["psi_dot_initial"],
            box_size_over_mu=4.0,
            tau_span=(0.0, 1.0e-3),
            n_output_points=3,
            initial_state_metadata=sample["metadata"],
        )
