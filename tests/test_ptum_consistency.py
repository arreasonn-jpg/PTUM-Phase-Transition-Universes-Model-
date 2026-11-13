"""Regression tests for PTUM homogeneous energy bookkeeping and diagnostics."""
import numpy as np
import pytest

from ptum_task1_simulation import (
    PTUMParameters,
    M_PL,
    meff_sq_psi,
    veff_phi,
    rho_phi,
    rho_psi,
    rho_total,
    pressure_phi,
    pressure_psi,
    hubble_rate,
    compute_quartic_dominance,
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
    assert np.isnan(q).any() is False


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
