"""Regression tests for PTUM homogeneous energy bookkeeping and diagnostics."""
import json

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


def test_scan_summary_is_strict_json_and_nonfinite_values_become_null(tmp_path):
    from ptum_task1_simulation import save_results

    result = {
        "success": True,
        "classification": {
            "regime": "insufficient_oscillation_data",
            "quartic_achieved": False,
            "w_final": float("nan"),
            "Q_final": float("nan"),
            "virial_final": float("nan"),
            "n_oscillations": 0,
        },
        "ic_params": {"psi_init": 0.0, "psi_dot_init": 0.0, "phi_offset": 0.0},
        "scan_metadata": {"scenario": "unit_test", "n_output_points": 101},
        "psi": np.array([0.0, 0.0]),
        "Phi": np.array([1.0, 1.0]),
        "continuity_residual_relative": np.array([0.0, 0.0]),
    }
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

    q_class = classify_outcome(quartic, PTUMParameters())
    non_q_class = classify_outcome(non_quartic, PTUMParameters())

    assert q_class["quartic_achieved"]
    assert q_class["quartic_to_tachyonic_potential_ratio"] == pytest.approx(1.05)
    assert not non_q_class["quartic_achieved"]
    assert non_q_class["quartic_to_tachyonic_potential_ratio"] == pytest.approx(0.95)



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



def test_quadratic_candidate_requires_its_own_virial_balance():
    base = {
        "success": True,
        "w_psi_avg": np.array([0.0, 0.02, -0.02]),
        "Q": np.full(100, 0.1),
        "virial_ratio": np.full(100, 1.0e6),
    }
    no_balance = dict(base, quadratic_virial_ratio=np.full(100, 4.0))
    with_balance = dict(base, quadratic_virial_ratio=np.full(100, 1.0))

    assert classify_outcome(no_balance, PTUMParameters())["regime"] == "non_quartic"
    assert classify_outcome(with_balance, PTUMParameters())["regime"] == "quadratic_candidate"



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


def test_manuscript_uses_one_waterfall_mass_parameter():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    assert "m^2" not in source
    assert r"m_\psi^2" in source
    assert r"m_{\rm eff}^2(\Phi)" in source


def test_manuscript_contains_explicit_curved_sm_action_and_hilbert_tensor():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    for required in (
        r"\label{sec:sm_covariant_action}",
        r"\label{eq:sm_curved_action}",
        r"\label{eq:sm_hilbert_tensor}",
        r"T_{\rm gauge}^{\mu\nu}",
        r"T_H^{\mu\nu}",
        r"T_f^{\mu\nu}",
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


def test_on_shell_sm_hilbert_tensor_does_not_double_count_ordinary_yukawa():
    from pathlib import Path

    source = Path("main.tex").read_text(encoding="utf-8")
    start = source.index(r"T_{{\rm SM},0}^{\mu\nu}={}&")
    end = source.index(r"\label{eq:sm_hilbert_tensor}", start)
    tensor_definition = source[start:end]
    assert r"T_{\rm gauge}^{\mu\nu}+T_H^{\mu\nu}+T_f^{\mu\nu}." in tensor_definition
    assert r"-g^{\mu\nu}U_{{\rm SM},Y}" not in tensor_definition
    assert "must not be added again" in source
    assert r"T_{{\rm SM},0}^{\mu\nu}-g^{\mu\nu}U_Y" in source
