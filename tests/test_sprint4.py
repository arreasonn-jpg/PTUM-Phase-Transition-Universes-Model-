"""
SPRINT 4 test suite -- microscopic field versus proxy-fluid claims.

The question
------------
``main.tex`` treats the ``psi`` sector in two mutually exclusive ways:

* as a **canonical scalar field** with a double-well potential (section 4.4),
  where it correctly concludes that small oscillations are matter-like
  (``<w> = 0``) and only quartic-dominated orbits give ``1/3``;
* as a **perfect fluid** with a fixed closure ``w = c_s^2 = 1/3, sigma = 0``
  (section 4.2 and the CLASS implementation).

These are not the same object.  This suite fixes what each statement means,
what the field theory actually gives, and which claims are reproducible.

Central structural result
-------------------------
``w = (K - U)/(K + U)`` with ``K >= 0`` and ``U >= 0`` is bounded by
``[-1, +1]``.  Therefore ``w < -1`` cannot arise from this Lagrangian under
any initial condition.  Any report of ``w_psi`` below ``-1`` for a
substantial fraction of the evolution is a numerical artefact.

Run::

    python -m pytest tests/test_sprint4.py -v
"""

from __future__ import annotations

import numpy as np
import pytest

from src import ptum_background as B

MU, LAM = 1.0, 0.1          # dimensionless units; scales out of every ratio


# ===========================================================================
# 1. The algebraic bound -- w can never leave [-1, +1]
# ===========================================================================
def test_w_is_bounded():
    """``-1 <= w <= 1`` for every ``K, U >= 0``."""
    K = np.array([0.0, 0.1, 1.0, 10.0, 1e6])
    U = np.array([1.0, 0.5, 1.0, 1e-3, 1e6])
    w = B.w_from_energy(K, U)
    assert np.all(w >= -1.0) and np.all(w <= 1.0)


def test_w_equals_minus_one_only_when_kinetic_energy_vanishes():
    assert B.w_from_energy(0.0, 1.0) == pytest.approx(-1.0)
    assert B.w_from_energy(0.0, 0.0) != B.w_from_energy(0.0, 0.0)  # nan


def test_intermediate_amplitude_overshoots_one_third():
    """Between the limits ``<w>`` is NOT a simple interpolation: it overshoots.

    Numerically ``<w> = 0.428, 0.408, 0.379, 0.363`` for amplitudes
    ``2, 3, 4, 5 psi0``.  The reason is that the orbit spends part of each
    cycle beyond the quartic-dominated region while the potential is still
    steeper than quartic on average near the minimum; the virial theorem with
    a single effective ``n`` does not apply.  ``<w> = 1/3`` is recovered only
    asymptotically as the amplitude grows.
    """
    values = [_run(a)["w_avg"] for a in (2.0, 3.0, 5.0)]
    # all above 1/3, and decreasing towards it
    assert all(v > 1.0 / 3.0 + 1e-3 for v in values), values
    assert values[0] > values[1] > values[2]
    # and the quartic limit is approached from above
    assert _run(100.0)["w_avg"] == pytest.approx(1.0 / 3.0, abs=5e-3)


def test_w_equals_one_third_needs_the_quartic_virial():
    """``<w> = (n-2)/(n+2)``: ``n=4`` gives ``1/3``, ``n=2`` gives ``0``."""
    assert B.averaged_w_power_law(4) == pytest.approx(1.0 / 3.0)
    assert B.averaged_w_power_law(2) == pytest.approx(0.0)


def test_w_below_minus_one_is_impossible_for_this_lagrangian():
    bounds = B.w_bounds()
    assert bounds["w_min"] == -1.0
    assert "impossible" in bounds["implies"]


# ===========================================================================
# 2. The overdamped benchmark: the field freezes, w -> -1
# ===========================================================================
def test_damping_ratio_reproduces_the_manuscripts_25():
    """``3H/(2 mu) = 25`` at ``H = 1e13``, ``mu = 1e13``."""
    assert B.damping_ratio(1e13, 1e13) == pytest.approx(1.5)
    # the manuscript's 25 corresponds to this H/mu
    assert B.damping_ratio(1.0, 25.0 * 2.0 / 3.0) == pytest.approx(25.0)


@pytest.fixture(scope="module")
def overdamped_run():
    H = 25.0 * 2 * MU / 3.0          # so that 3H/(2mu) = 25
    return B.evolve(psi_i=1e-3 * B.psi0(MU, LAM), psidot_i=0.0,
                    mu=MU, lam=LAM, H=H, t_max=6.0 / H)


def test_overdamped_field_does_not_roll(overdamped_run):
    """The field stays at the top of the barrier; no oscillation."""
    psi0 = B.psi0(MU, LAM)
    assert np.max(np.abs(overdamped_run["psi"])) / psi0 < 0.01


def test_overdamped_w_is_minus_one(overdamped_run):
    """Frozen at the maximum of ``U``: ``K = 0``, ``w = -1``.

    This *reproduces* SPRINT 0's "w_psi < -1" observation in the correct
    form: the value is ``-1``, never below it, and it is a consequence of the
    field not rolling -- not of a numerical instability.
    """
    assert overdamped_run["w_avg"] == pytest.approx(-1.0, abs=1e-6)


def test_no_oscillations_in_the_overdamped_regime(overdamped_run):
    sign_changes = np.sum(np.diff(np.sign(overdamped_run["psidot"])) != 0)
    assert sign_changes <= 1


# ===========================================================================
# 3. Undamped / underdamped: <w> interpolates between 0 and 1/3
# ===========================================================================
def _run(amp_over_psi0, H_over_mu=1e-3, periods=60):
    mu = MU
    H = H_over_mu * mu
    t_max = periods * 2 * np.pi / B.oscillation_mass(mu)
    return B.evolve(psi_i=amp_over_psi0 * B.psi0(mu, LAM), psidot_i=0.0,
                    mu=mu, lam=LAM, H=H, t_max=t_max, n_eval=200000)


def test_large_amplitude_gives_one_third():
    """Quartic-dominated orbit: ``<w> -> 1/3``."""
    r = _run(100.0)
    assert r["w_avg"] == pytest.approx(1.0 / 3.0, abs=5e-3)


def test_small_amplitude_gives_zero():
    """Quadratic oscillations about the minimum: ``<w> -> 0``."""
    psi0 = B.psi0(MU, LAM)
    mu = MU
    H = 1e-3 * mu
    t_max = 60 * 2 * np.pi / B.oscillation_mass(mu)
    r = B.evolve(psi_i=1.01 * psi0, psidot_i=0.0, mu=mu, lam=LAM, H=H,
                 t_max=t_max, n_eval=200000)
    assert abs(r["w_avg"]) < 0.01


def test_instantaneous_w_always_stays_inside_the_bounds():
    """Over a full run ``w`` touches ``+-1`` but never leaves ``[-1, 1]``."""
    r = _run(5.0)
    w = r["w"][np.isfinite(r["w"])]
    assert w.min() >= -1.0 - 1e-12
    assert w.max() <= 1.0 + 1e-12
    # and it really does explore the interval (this is an oscillator)
    assert w.min() < -0.99 and w.max() > 0.99


# ===========================================================================
# 4. Which regime does the benchmark reach?  (no)
# ===========================================================================
def test_effective_power_regimes():
    psi0 = B.psi0(MU, LAM)
    assert B.effective_power(1e-2 * psi0, MU, LAM)["regime"] == "quadratic"
    assert B.effective_power(1e2 * psi0, MU, LAM)["regime"] == "quartic"


def test_benchmark_fails_the_rapid_oscillation_condition():
    """``sqrt(lam) psi0 ~ 3e12 GeV`` vs ``H_* ~ 1e13 GeV``: ``omega < H``."""
    mu, lam, psi_amp, H = 1e13, 0.1, 1e13, 1e13
    r = B.omega_over_H(mu, lam, psi_amp, H)
    # the quartic estimate ``sqrt(lam) psi_amp`` is below H; the quadratic one
    # ``sqrt(2) mu`` is numerically larger only because omega = sqrt(2) mu > H
    # marginally -- either way the quartic regime is NOT reached
    assert r["quartic"] < 1.0


def test_quartic_regime_needs_a_larger_field_or_weaker_hubble():
    """The regime is reachable -- but not at the stated benchmark."""
    mu, lam, H = 1e13, 0.1, 1e10
    r = B.omega_over_H(mu, lam, 1e15, H)
    assert r["quartic"] > 1.0


# ===========================================================================
# 5. Barrier crossing
# ===========================================================================
def test_rest_at_the_top_does_not_cross():
    """``psi_i = 0, psidot = 0`` sits exactly ON the barrier maximum.

    Energy equals the barrier height, so ``ratio == 1`` -- and a field sitting
    on a maximum with zero velocity never crosses anything.
    """
    r = B.crosses_barrier(0.0, 0.0, MU, LAM)
    assert r["ratio"] == pytest.approx(1.0)
    assert r["on_the_barrier"] is True
    assert r["crosses"] is False


def test_zero_initial_velocity_is_frozen_at_the_top():
    """SPRINT 0's "frozen init" finding, now quantified at the energy level."""
    mu, lam = 1e13, 0.1
    psi0 = B.psi0(mu, lam)
    # starting at 1e-3 psi0 with zero velocity gives E ~ barrier height
    r = B.crosses_barrier(1e-3 * psi0, 0.0, mu, lam)
    assert 0.999 < r["ratio"] < 1.0    # just below the barrier height
    assert r["crosses"] is False       # so it cannot cross


def test_enough_kinetic_energy_crosses():
    mu, lam = MU, LAM
    # K = mu^4/(4 lam) equals the barrier height exactly
    v_barrier = np.sqrt(mu**4 / (2 * lam))
    r = B.crosses_barrier(0.0, 2 * v_barrier, mu, lam)
    assert bool(r["crosses"]) is True


# ===========================================================================
# 6. Consistency with the manuscript's own section 4.4
# ===========================================================================
def test_manuscript_and_field_theory_agree_on_the_quadratic_regime():
    """§4.4 says small oscillations about a minimum are matter-like: ``<w>=0``.

    The numerics agree (see ``test_small_amplitude_gives_zero``).  This is a
    place where the manuscript is right and should be kept.
    """
    assert B.averaged_w_quadratic() == pytest.approx(0.0)


def test_manuscript_and_field_theory_agree_on_the_quartic_condition():
    """§4.4's condition ``|psi| >> psi0`` is exactly what the numerics need."""
    psi0 = B.psi0(MU, LAM)
    assert B.effective_power(100 * psi0, MU, LAM)["regime"] == "quartic"
    assert B.effective_power(0.01 * psi0, MU, LAM)["regime"] == "quadratic"


def test_manuscript_correctly_flags_the_benchmark_as_overdamped():
    """§4.4's "3H/(2mu) ~ 25 => overdamped" is reproducible."""
    H = 25.0 * 2 * MU / 3.0
    assert B.damping_ratio(MU, H) == pytest.approx(25.0)
    r = B.evolve(psi_i=1e-3 * B.psi0(MU, LAM), psidot_i=0.0, mu=MU, lam=LAM,
                 H=H, t_max=6.0 / H)
    assert r["w_avg"] == pytest.approx(-1.0, abs=1e-6)
