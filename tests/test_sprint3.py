"""
SPRINT 3 test suite -- the three items SPRINT 2 left open, plus the
Mathieu/Floquet analysis.

Parts
-----
A. Mathieu / Floquet: ``mu_max(q)``, instability onset, and the manuscript's
   two mutually contradictory claims.
B. Reheating: the ``beta^3`` power of the Yukawa width, the absence of a
   ``psi -> phi phi`` vertex, and the two ``T_rh`` routes.
C. The fermionic half of the Yukawa transfer, from the Dirac equation.
D. Entropy bookkeeping.
E. The trace anomaly and the status of ``sum_i Q_i = 0`` at the quantum level.

Every number asserted here is computed, never copied from ``main.tex``.
"""

from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
import warnings

from src import ptum_fermion as F
from src import ptum_reheating as R
from src import ptum_anomaly as A

warnings.filterwarnings("ignore", category=RuntimeWarning)


# ===========================================================================
# A. MATHIEU / FLOQUET
# ===========================================================================
@pytest.fixture(scope="module")
def mathieu():
    import src.ptum_mathieu as M
    return M


def test_monodromy_converges_with_the_step_count(mathieu):
    """The Floquet exponent must be step-size independent."""
    vals = [mathieu.floquet_mu(1.0, 1.0, n) for n in (100, 200, 400, 800)]
    assert max(vals) - min(vals) < 1e-6


def test_two_independent_integrators_agree(mathieu):
    """RK4 monodromy vs. ``solve_ivp`` with tight tolerances."""
    for a, q in ((1.0, 1.0), (1.0, 10.0), (2.0, 1.0)):
        mu1 = mathieu.floquet_mu(a, q, 400)
        mu2 = mathieu.floquet_from_transfer_matrix(a, q)
        assert abs(mu1 - mu2) < 1e-5 * max(1.0, abs(mu1))


def test_mu_is_zero_outside_instability_bands(mathieu):
    """A far-from-resonance point must give no growth."""
    assert mathieu.floquet_mu(10.0, 0.01, 400) == 0.0


def test_mu_max_scales_as_sqrt_q_not_linearly(mathieu):
    """SPRINT 3 finding: ``mu_max ~ 0.545 sqrt(q)``.

    The manuscript claims ``mu_max ~ q omega_res/2`` (linear).  Fitting the
    numerically computed ``mu_max`` over two decades gives a power ``0.5``,
    decisively rejecting the linear claim.
    """
    qs = np.array([10.0, 30.0, 100.0, 300.0, 1000.0])
    mus = np.array([mathieu.mu_max_scan([q], n_a=300, n_steps=200)[q] for q in qs])
    p, _ = np.polyfit(np.log(qs), np.log(mus), 1)
    assert 0.45 < p < 0.56, f"power law exponent {p} is not ~0.5"
    # the constant 0.2 claim is also excluded for large q
    ratios = mus / qs
    assert ratios[-1] < 0.05


def test_mu_max_coefficient(mathieu):
    """``mu_max / sqrt(q) -> 0.545``."""
    vals = [mathieu.mu_max_scan([q], n_a=300, n_steps=200)[q] / np.sqrt(q)
            for q in (100.0, 500.0, 2000.0)]
    assert all(0.4 < v < 0.65 for v in vals), vals


def test_ptum_locus_instability_onset(mathieu):
    """The PTUM ``k=0`` mode sits at ``a = 2q``; the band opens at ``q ~ 0.33``."""
    q_crit = mathieu.find_q_critical_on_ptum_locus()
    assert q_crit is not None
    assert 0.25 < q_crit < 0.40, q_crit
    # just below: stable.  just above: unstable.
    assert mathieu.floquet_mu(2 * 0.25, 0.25, 400) == 0.0
    assert mathieu.floquet_mu(2 * 0.45, 0.45, 400) > 0.0


def test_benchmark_is_outside_the_resonance_region(mathieu):
    """At ``g_DM ~ 1e-3`` the benchmark has ``q ~ 1e-5``: no growth at all.

    This is a *falsification* of the manuscript's parametric-resonance claim
    at its own benchmark values, not a numerical subtlety.
    """
    for g in (1e-6, 1e-4, 1e-3, 1e-1):
        r = mathieu.ptum_is_in_the_narrow_regime(g, 1e13, 1e13)
        assert r["unstable"] is False, g
        assert r["q"] < mathieu.find_q_critical_on_ptum_locus()


def test_required_coupling_for_resonance(mathieu):
    """Resonance needs ``g_DM >~ 5`` at ``A_res = omega_res``."""
    g_need = mathieu.required_g_for_resonance(1e13, 1e13)
    assert 1.0 < g_need < 20.0
    r = mathieu.ptum_is_in_the_narrow_regime(g_need * 1.5, 1e13, 1e13)
    assert r["unstable"] is True


def test_manuscript_q_normalisation_differs_by_four(mathieu):
    """``main.tex`` defines ``q = g A^2/omega^2``; the standard normalisation is a quarter."""
    g, Ares, w = 1.0, 1e13, 1e13
    a_std, q_std = mathieu.ptum_to_mathieu(g, Ares, w)
    a_ms, q_ms = mathieu.manuscript_to_mathieu(g, Ares, w)
    assert q_ms == pytest.approx(4 * q_std)
    assert a_ms == pytest.approx(4 * a_std)


def test_efold_conversion(mathieu):
    """``N`` periods advance ``z`` by ``N pi``, so ``e-folds = mu pi N``."""
    assert mathieu.efolds_over_periods(0.1, 10) == pytest.approx(0.1 * np.pi * 10)
    assert mathieu.required_N_for(np.pi, 0.1) == pytest.approx(10.0)


# ===========================================================================
# B. REHEATING
# ===========================================================================
def test_yukawa_width_power_of_beta():
    """A real scalar needs a p-wave pair: ``beta^3``, not ``beta``."""
    m_psi, y = sp.symbols("m_psi y", positive=True)
    m_f = sp.Symbol("m_f", positive=True)
    right = R.decay_width_yukawa(m_psi, y, m_f, p_wave_power=1)
    wrong = R.decay_width_yukawa(m_psi, y, m_f, p_wave_power=0)
    beta = R.beta_factor(m_psi, m_f)
    assert sp.simplify(right - y**2 * m_psi * beta**3 / (8 * sp.pi)) == 0
    assert sp.simplify(right - wrong) != 0
    assert R.which_beta_power_applies()["power_of_beta"] == 3


def test_manuscript_beta_power_is_consistent():
    """``main.tex`` writes ``(1-4m_f^2/m_psi^2)^{3/2} = beta^3`` -- correct."""
    assert R.which_beta_power_applies()["verdict"] == "consistent"


def test_no_single_particle_decay_from_the_quartic():
    """``<phi phi| L |psi> = 0`` because ``psi`` appears quadratically."""
    d = R.quartic_vertex_vanishes_at_psi_zero()
    assert d["decay_amplitude_at_psi0"] == 0


def test_annihilation_requires_a_density():
    """``Gamma_eff = n <sigma v>`` -- the Lagrangian alone cannot supply ``n``."""
    msg = R.effective_rate_needs_number_density()
    assert "FENOMENOLOJIK" in msg
    assert "n_psi" in msg


def test_two_T_rh_routes_disagree_at_the_benchmark():
    """The decay route and the instantaneous route differ by orders of magnitude."""
    b = R.order_of_magnitude_report()
    ratio = float(b["ratio"])
    assert ratio < 1e-2, ratio          # ~7e-4 at the benchmark point


def test_T_rh_scalings():
    """Dimensional consistency of both routes."""
    G, gs = sp.symbols("Gamma g_star", positive=True)
    V0q = sp.Symbol("V0q", positive=True)
    t1 = R.T_rh_from_decay(G, gs)
    t2 = R.T_rh_from_instantaneous(V0q, gs)
    # T1 ~ sqrt(Gamma M_Pl), T2 ~ V0^{1/4}
    assert sp.simplify(t1.subs(G, 1).subs(gs, 100) / sp.sqrt(R.M_Pl_red)) != 0
    assert sp.simplify(t2.subs(V0q, 1).subs(gs, 100) - (30 / sp.pi**2 / 100)**sp.Rational(1, 4)) == 0


def test_condensate_caveat_is_stated():
    """A perturbative width applied to a condensate needs three conditions."""
    msg = R.needs_condensate_averaging()
    assert "oscillations per Hubble time" in msg
    assert "backreaction" in msg


# ===========================================================================
# C. FERMIONIC HALF OF THE YUKAWA TRANSFER
# ===========================================================================
def test_gamma_matrices_satisfy_the_clifford_algebra():
    for key, res in F.check_clifford().items():
        assert res == sp.zeros(4, 4), key


def test_gamma_hermiticity_matches_the_metric_signature():
    h = F.check_hermiticity()
    assert h["g0_anti_hermitian"] is True
    assert all(h[f"g{i}_hermitian"] for i in (1, 2, 3))


def test_onshell_derivatives_solve_the_dirac_equation():
    """``i gamma^0 d_0 f - (m_f + y psi) f = 0`` with the substituted ``d_0 f``."""
    res = F.dirac_residual()
    assert sp.simplify(res) == sp.zeros(4, 1)


def test_fbar_f_is_conserved():
    """The scalar bilinear is fermion-number neutral, hence conserved."""
    assert F.bilinear_is_conserved() == 0


def test_vector_current_is_conserved():
    """``d_mu (fbar gamma^mu f) = 0``: no fermion-number source.

    Note that ``fbar gamma^0 f = n_f`` (the number density) is **not** zero --
    earlier drafts of this test wrongly assumed it was.  What vanishes is its
    time derivative.
    """
    lhs, n_f = F.vector_current_divergence()
    assert lhs == 0
    assert sp.simplify(n_f - F.fbarf()) == 0


def test_fermion_energy_density_is_the_shifted_mass_bilinear():
    """``T_f^{00} = (m_f + y psi) fbar f``: the condensate shifts the mass."""
    T00 = F.fermion_energy_density()
    fbarf = F.fbarf()
    M = F.effective_mass()
    assert sp.simplify(T00 - M * fbarf) == 0


def test_fermionic_half_closes_the_yukawa_transfer():
    """The result SPRINT 2 could not prove: ``d_0 T_f^{00} = -Q_psi``.

    A zero residual in :func:`F.fermion_closure_residual` means
    ``Q_f = +y psidot fbar f = -Q_psi``, i.e. ``Q_psi + Q_f = 0`` with the
    same ``Q_psi`` derived from the scalar side.
    """
    assert F.fermion_closure_residual() == 0


def test_Q_f_equals_minus_Q_psi():
    """Cross-module check against SPRINT 2's ``Q_psi``."""
    from src import ptum_transfer as T
    Q_f = F.Q_f_closed()
    # SPROINT 2: Q_psi = -y (fbar f) psidot  with lam_psi = 0
    Q_psi = -F.y_psi * F.fbarf() * sp.diff(F.psi_b, F.t)
    assert sp.simplify(Q_f - (-Q_psi)) == 0


def test_fermion_transfer_dimension():
    assert F.dim_transfer() == 5


def test_fermion_limits():
    d = F.fermion_limit_checks()
    assert d["yukawa_off"] == 0
    assert d["static_scalar"] == 0


# ===========================================================================
# D. ENTROPY
# ===========================================================================
def test_entropy_scaling_exponents():
    """``s ∝ g_* T^3`` so the logarithmic derivatives are ``1`` and ``3``."""
    e = R.entropy_scaling_exponents()
    assert sp.simplify(e["S_vs_gstar"] - 1) == 0
    assert sp.simplify(e["S_vs_T"] - 3) == 0


def test_radiation_density_normalisation():
    gs, T = sp.symbols("g_star T", positive=True)
    assert sp.simplify(R.radiation_density(T, gs) - sp.pi**2 * gs * T**4 / 30) == 0


def test_entropy_is_labelled_conditional():
    d = R.entropy_is_a_prediction_or_a_check()
    assert d["status"] == "CONDITIONAL"
    assert "instantaneous" in d["reason"]


# ===========================================================================
# E. TRACE ANOMALY
# ===========================================================================
def test_anomaly_is_a_trace_statement_only():
    """Diffeomorphism invariance is exact; only ``T^mu_mu`` is anomalous."""
    d = A.anomaly_is_trace_only()
    assert "exact" in d["nabla_mu_T_total"]
    assert "anomalous" in d["T^mu_mu"]
    assert "survives" in d["consequence"]


def test_beta_function_coefficients():
    lam = sp.Symbol("lambda", positive=True)
    assert sp.simplify(A.beta_function("quartic_scalar", lam)
                       - 3 * lam**2 / (16 * sp.pi**2)) == 0
    y = sp.Symbol("y", positive=True)
    assert sp.simplify(A.beta_function("yukawa_real_scalar", y)
                       - 5 * y**3 / (16 * sp.pi**2)) == 0


def test_running_correction_is_small():
    """At ``lam = 0.1`` and one decade, the running is ``O(1%)``."""
    val = float(A.benchmark_running())
    assert val < 0.05


def test_scheme_dependence_of_individual_transfers():
    """A field rescaling changes ``Q_i`` but not ``Q_Phi + Q_psi``."""
    scaling, at_zero = A.field_rescaling_effect(None, None)
    assert at_zero == 1
    assert sp.simplify(scaling.subs(sp.Symbol("epsilon", real=True), 0) - 1) == 0


def test_open_questions_are_recorded():
    assert len(A.OPEN_QUESTIONS) >= 3
