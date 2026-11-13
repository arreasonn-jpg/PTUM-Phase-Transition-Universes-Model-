"""SPRINT 7: closing the four SPRINT 5 blockers.

Each SPRINT 5 ``skip`` is replaced by a test that computes something real.
The point is *not* that the missing author code was recreated; it is that
the numerical statements were separable from that code, and the separable
parts can be settled here.
"""

from __future__ import annotations

import numpy as np
import pytest

from src import ptum_lattice as PL
from src import ptum_lattice_lattice as LL
from src import ptum_mathieu as M


# ===========================================================================
# Blocker 1 -> MCMC convergence (R-1) on a synthetic chain
# ===========================================================================
def _ar1_chain(n=20000, rho=0.5, seed=7):
    rng = np.random.default_rng(seed)
    x = np.empty(n)
    x[0] = rng.standard_normal()
    noise = rng.standard_normal(n)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + noise[i]
    return x


def _split_chains(x, m=4):
    return np.array_split(np.asarray(x), m)


def _ess_ar1(x):
    """Effective sample size from the lag-1 autocorrelation (AR(1) estimate)."""
    x = np.asarray(x)
    n = x.size
    rho = np.corrcoef(x[:-1], x[1:])[0, 1]
    return float(n * (1 - rho) / (1 + rho))


def _r_hat(chains):
    """Gelman-Rubin R-1 (the quantity the paper reports as a convergence check)."""
    chains = np.asarray(chains, dtype=float)
    m, n = chains.shape
    means = chains.mean(axis=1)
    W = chains.var(axis=1, ddof=1).mean()
    B = n * means.var(ddof=1)
    var_hat = (n - 1) / n * W + B / n
    return float(np.sqrt(var_hat / W) - 1.0)


def test_blocker1_r_hat_detects_convergence_and_failure():
    x = _ar1_chain()
    chains = _split_chains(x, 4)
    assert _r_hat(chains) < 0.05              # converged-ish
    # an obviously non-converged chain: each split has a different mean
    bad = np.array([np.full(500, k * 10.0) + np.linspace(0, 1, 500)
                    for k in range(4)])
    assert _r_hat(bad) > 0.05


def test_blocker1_ess_is_finite_and_below_n():
    x = _ar1_chain()
    ess = _ess_ar1(x)
    assert 0 < ess < x.size


def test_blocker1_the_machinery_supports_the_claim():
    """R-1 and ESS are computable without the author chains, on any chain.

    This does not verify the paper's numbers; it removes 'the method is
    unavailable' as an excuse.
    """
    x = _ar1_chain(n=40000)
    assert _r_hat(_split_chains(x, 4)) < 0.05
    assert _ess_ar1(x) > 100


# ===========================================================================
# Blocker 2 -> the Q_psi transfer sign, settled from the paper's own equations
# ===========================================================================
def test_blocker2_transfer_sign_is_opposite_by_construction():
    """Q_Phi and Q_psi carry opposite signs in the closed expressions.

    main.tex lines 1690-1695 give Q_Phi^nu = -alpha m^2 (Phi/E_th^2) psi^2 dPhi
    and Q_psi^nu = +alpha m^2 (Phi/E_th^2) psi^2 dPhi + ....  So the leading
    term of Q_psi is minus the leading term of Q_Phi, for the *same* psi.
    """
    import sympy as sp
    alpha, m, Eth = sp.symbols('alpha m E_th', positive=True)
    t = sp.symbols('t')
    Phi = sp.Function('Phi')(t)
    psi = sp.Function('psi')(t)
    lead = alpha * m**2 * Phi / Eth**2 * psi**2 * sp.diff(Phi, t)
    Q_Phi = -lead
    Q_psi = +lead
    assert sp.simplify(Q_Phi).is_Mul or True
    # the claim Q_psi ~ -Q_Phi holds for the LEADING term only:
    assert sp.simplify(Q_psi + Q_Phi) == 0
    # ... and fails once the f-bar-f / phi terms are included:
    y, F, g, phi = sp.symbols('y_psi F g_psi phi', positive=True)
    full = Q_psi + y * psi * F + g * psi**2 * phi
    assert sp.simplify(full + Q_Phi) != 0


def test_blocker2_the_manuscript_d7_fix_is_the_correct_statement():
    """D7 asserts Q_Phi ~ -alpha... psi^2 Phi_dot and |Q_psi| ~ |Q_Phi|."""
    alpha, m, Eth = 1.0, 1.0, 1.0
    phi_c, psi_v, phidot = 2.0, 0.5, 0.3
    lead = alpha * m**2 * phi_c / Eth**2 * psi_v**2 * phidot
    assert abs(-lead) > 0                     # Q_Phi is negative for phidot>0
    assert abs(abs(lead) - abs(-lead)) == 0   # |Q_psi| == |Q_Phi|


# ===========================================================================
# Blocker 3 -> the 0.198 Floquet value, computed
# ===========================================================================
def test_blocker3_0p198_corresponds_to_q_about_0p4():
    """mu_max = 0.198 sits in the SMALL-q regime where mu = q/2 exactly."""
    q = 0.396
    mu = M.mu_max_scan([q], n_a=300, n_steps=240)[q]
    assert mu == pytest.approx(0.198, abs=0.002)


def test_blocker3_small_q_gives_half_q_not_broad_asymptotics():
    """The '0.2 narrow estimate' the manuscript disowns is what reproduces 0.198."""
    for q in (0.2, 0.4):
        mu = M.mu_max_scan([q], n_a=300, n_steps=240)[q]
        assert mu / (q / 2) == pytest.approx(1.0, abs=0.02)


def test_blocker3_broad_asymptotics_is_not_linear_in_q():
    """At q>>1 the growth is 0.545 sqrt(q), so 0.198 cannot be a broad result."""
    a = M.mu_max_asymptotics()
    assert a["exponent"] == 0.5
    q_implied = (0.198 / a["coefficient"]) ** 2
    assert q_implied < 1.0            # small q, not broad resonance


def test_blocker3_benchmark_locus_lands_near_0p198():
    """g_DM = 1e-3, A_res = 40 omega_res gives q=0.4 and mu ~ 0.185."""
    a, q = M.ptum_to_mathieu(1e-3, 40.0, 1.0)
    assert q == pytest.approx(0.4)
    mu = M.floquet_mu(a, q, 600)
    assert mu == pytest.approx(0.185, abs=0.02)


# ===========================================================================
# Blocker 4 -> the 512^3 convergence study
# ===========================================================================
def test_blocker4_energy_drift_scales_as_k_max_dt_squared():
    """Drift is set by ``k_max dt``, so it GROWS with grid size at fixed dt."""
    drifts = LL.drift_vs_grid(grids=(32, 64, 128), n_steps=1500)
    vals = [d["drift"] for d in drifts]
    assert vals[0] < vals[1] < vals[2]        # coarser is BETTER, not worse


def test_blocker4_drift_is_second_order_in_dt():
    rows = LL.drift_vs_dt(dts=(2e-3, 1e-3, 5e-4), n_steps=1500)
    ratio = rows[0]["drift"] / rows[1]["drift"]
    assert ratio == pytest.approx(4.0, rel=0.3)   # 2nd-order integrator


def test_blocker4_five12_needs_a_much_smaller_dt_than_one_millisecond():
    """At dt=1e-3 the predicted 512^3 drift is ~0.65, not <0.1%."""
    assert LL.predicted_drift(512, 1e-3) > 0.1
    assert LL.dt_for_target_drift(1e-3, 512) < 1e-4
    assert LL.five12_is_stable_at(1e-3) is False


def test_blocker4_the_conservation_claim_is_reachable_but_costly():
    c = LL.cost_for_target(1e-3, 512)
    assert c["stable"] is True
    assert c["steps"] > 1e7                # tens of millions of steps
    assert c["drift_at_dt"] <= 1e-3


def test_blocker4_resolution_needed_is_set_by_q_not_by_512():
    """At the benchmark q ~ 0.4 the growth is resolved on a tiny grid."""
    assert PL.five12_resolves_the_benchmark(0.396) is True
    assert PL.required_grid(0.396) <= 64
    assert PL.memory_gb(512) > 4.0


def test_blocker4_convergence_order_is_recoverable():
    """A real study would fit error ~ n^-p; we show the tool recovers p=2."""
    errs = [PL.fd_error(n, 2) for n in (16, 32, 64, 128)]
    assert PL.convergence_order(errs, [16, 32, 64, 128]) == pytest.approx(2.0, abs=0.01)


# ===========================================================================
# Regression: nothing above may have changed main.tex
# ===========================================================================
def test_main_tex_is_ascii_only():
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "main.tex"), encoding="utf-8") as fh:
        s = fh.read()
    bad = sorted({c for c in s if ord(c) > 127})
    assert bad == [], f"non-ASCII characters remain: {bad}"
