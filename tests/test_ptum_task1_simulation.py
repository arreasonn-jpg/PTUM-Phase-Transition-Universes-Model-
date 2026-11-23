import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ptum_task1_simulation as sim


def test_effective_mass_changes_sign_at_critical_field():
    p = sim.PTUMParameters()
    assert sim.meff_sq_psi(0.99 * p.Phi_c, p) > 0.0
    assert sim.meff_sq_psi(1.01 * p.Phi_c, p) < 0.0


def test_total_phi_psi_energy_exchange_cancels_exactly():
    p = sim.PTUMParameters(V0=1e56, m_psi=1e13, lambda_psi=0.1)
    phi = 0.5 * p.Phi_c
    phi_dot = 1.0e27
    psi = 1.0e12
    psi_dot = 1.0e24
    ydot = sim.background_equations(0.0, np.array([phi, phi_dot, psi, psi_dot]), p)
    _, phi_ddot, _, psi_ddot = ydot
    h = sim.hubble_rate(phi, phi_dot, psi, psi_dot, p)
    m2 = sim.meff_sq_psi(phi, p)
    dm2_dphi = -2.0 * p.alpha * p.m_psi**2 * phi / p.E_th**2
    rho_dot = (
        phi_dot * phi_ddot + psi_dot * psi_ddot
        + sim.dveff_dphi(phi, p) * phi_dot
        + 0.5 * dm2_dphi * phi_dot * psi**2
        + m2 * psi * psi_dot + p.lambda_psi * psi**3 * psi_dot
    )
    expected = -3.0 * h * (phi_dot**2 + psi_dot**2)
    assert np.isclose(rho_dot, expected, rtol=2e-12, atol=1e-8 * abs(expected))


def test_threshold_diagnostics_resolve_crossing_direction_and_duration():
    p = sim.PTUMParameters()
    t = np.array([0.0, 5.0, 10.0])
    phi = p.Phi_c * np.array([0.9, 1.1, 0.9])
    duration, fraction, crossings = sim._tachyonic_trajectory_diagnostics(t, phi, p)
    assert np.isclose(duration, 5.0)
    assert np.isclose(fraction, 0.5)
    assert [x["direction"] for x in crossings] == [
        "dormant_to_tachyonic", "tachyonic_to_dormant"
    ]
    assert np.allclose([x["time"] for x in crossings], [2.5, 7.5])


def test_fuel_velocity_can_be_supplied_without_slow_roll_guess():
    p = sim.PTUMParameters()
    chosen_velocity = 1.23e27
    ic = sim.create_initial_conditions(
        p, psi_init=0.01 * p.psi_0, phi_offset=-0.01 * p.Phi_c,
        phi_dot_init=chosen_velocity
    )
    assert np.isclose(ic.Phi, 0.99 * p.Phi_c)
    assert ic.Phi_dot == chosen_velocity


def test_exact_zero_proxy_solution_is_classified_separately():
    p = sim.PTUMParameters(V0=1e56)
    ic = sim.InitialConditions(
        Phi=0.5 * p.Phi_c, Phi_dot=0.0, psi=0.0, psi_dot=0.0
    )
    result = sim.run_simulation(
        p, ic, (0.0, 0.2 / p.m_psi),
        np.linspace(0.0, 0.2 / p.m_psi, 64)
    )
    assert result["success"]
    assert result["seedless_invariant"]
    assert np.max(np.abs(result["psi"])) == 0.0
    assert sim.classify_outcome(result, p)["regime"] == "unseeded_invariant"


def test_full_cycle_integral_diagnostics_recover_quartic_virial_limit():
    p = sim.PTUMParameters(m_psi=0.0, lambda_psi=1.0)
    t_eval = np.linspace(0.0, 70.0, 70001)
    sol = solve_ivp(
        lambda t, y: (y[1], -y[0]**3),
        (t_eval[0], t_eval[-1]), (1.0, 0.0),
        t_eval=t_eval, rtol=1e-11, atol=1e-13, method="DOP853"
    )
    assert sol.success
    psi, psi_dot = sol.y
    rho = 0.5 * psi_dot**2 + 0.25 * psi**4
    pressure = 0.5 * psi_dot**2 - 0.25 * psi**4
    zeros = np.zeros_like(t_eval)
    h = np.full_like(t_eval, 1e-3)
    cycles = sim.compute_full_cycle_diagnostics(
        t_eval, zeros, psi, psi_dot, rho, pressure, h, p
    )
    assert len(cycles) >= 5
    for cycle in cycles[-3:]:
        assert abs(cycle["w"] - 1.0 / 3.0) < 2e-3
        assert abs(cycle["virial"] - 1.0) < 2e-3
        assert cycle["Q4"] == float("inf")
        assert cycle["omega_over_H"] > 10.0
    classification = sim.classify_outcome({
        "success": True, "seedless_invariant": False,
        "t": t_eval, "Phi": zeros, "psi": psi, "psi_dot": psi_dot,
        "rho_psi": rho, "p_psi": pressure, "H": h
    }, p)
    assert classification["quartic_achieved"]
