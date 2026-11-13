"""
SPRINT 5 test suite -- numerical reproducibility and artefact detection.

These tests audit the *pipeline*, not the physics: can the reported numbers be
regenerated, and are the diagnostics physically meaningful?

Scope note
----------
Tests that would need the CLASS/Cobaya/lattice outputs are marked
``pytest.mark.skip`` with a reason, because those artifacts are not in the
repository.  They are recorded as ``NOT RUN`` in the report rather than
silently passing.
"""

from __future__ import annotations

import json
import os

import numpy as np
import pytest

from src import ptum_reproducibility as R

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = os.path.join(REPO, "task1_parameter_scan_results.json")


# ===========================================================================
# 1. Scale separation of the published ODE
# ===========================================================================
def test_the_background_ode_is_badly_scaled():
    """``|y| ~ 1e19`` while ``1/|dy/dt| ~ 1e-39``: a 57-decade mismatch.

    This is the root cause of the non-terminating runs, not a solver bug.
    """
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    rhs = lambda t, y: S.background_equations(t, y, p)
    ss = R.scale_separation(rhs, [1e19, 0.0, 1e13, 0.0])
    assert ss["ratio"] > 1e50
    assert R.is_badly_scaled(ss["ratio"]) is True


def test_scale_separation_recovers_a_well_scaled_problem():
    """Sanity check of the diagnostic itself: a benign ODE must not flag."""
    rhs = lambda t, y: np.array([y[1], -y[0]])     # harmonic oscillator
    ss = R.scale_separation(rhs, [1.0, 0.0])
    assert R.is_badly_scaled(ss["ratio"]) is False


# ===========================================================================
# 2. The energy-density shift
# ===========================================================================
def test_rho_psi_omits_the_constant_offset():
    """``rho_psi(0) = 0`` while the true energy at that point is ``U(0) > 0``."""
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    rho0 = S.rho_psi(p.Phi_c, 0.0, 0.0, p)
    U0 = S.shifted_potential_psi(0.0, p)
    assert rho0 == 0.0
    assert U0 > 0
    assert R.shift_is_missing(rho0, U0) is True


def test_the_two_potentials_are_not_the_same_function():
    """``rho_code - U`` is **not** a constant ``V_min``: it varies with ``psi``.

    This corrects an earlier version of this sprint's own claim (see the report,
    self-criticism section).  ``U`` is built from ``lam*psi_0^2``; ``rho_psi``
    is built from ``m_eff^2(Phi)``, which vanishes at ``Phi = Phi_c``.
    """
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    psi0 = p.psi_0
    diffs = []
    for frac in (0.0, 0.1, 0.5, 1.0, 2.0):
        psi = frac * psi0
        rho = S.rho_psi(p.Phi_c, psi, 0.0, p)
        U = S.shifted_potential_psi(psi, p)
        diffs.append(float(R.rho_minus_U(rho, U)))
    assert len(set(np.round(diffs, 3))) > 1        # not constant
    assert diffs[0] == pytest.approx(-p.psi_0**2 * p.lambda_psi
                                     * p.psi_0**2 / 4, rel=1e-9)


def test_the_effective_mass_vanishes_at_the_benchmark():
    """``m_eff^2(Phi_c) = 0`` exactly -- why the mass term silently drops out."""
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    assert S.meff_sq_psi(p.Phi_c, p) == pytest.approx(0.0, abs=1e-6 * p.m_psi**2)


def test_rho_at_psi0_is_pure_quartic():
    """At ``psi_0`` the mass term is absent, so ``rho = lam psi_0^4/4``."""
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    psi0 = p.psi_0
    rho0 = S.rho_psi(p.Phi_c, psi0, 0.0, p)
    quartic = 0.25 * p.lambda_psi * psi0**4
    assert R.mass_term_is_absent(rho0, quartic) is True


def test_w_at_the_frozen_point_is_wrong_in_the_code():
    """``psi = psidot = 0``: the code returns the ``0/0`` guard; physics says -1."""
    import ptum_task1_simulation as S
    p = S.PTUMParameters()
    w_code = S.w_psi(p.Phi_c, 0.0, 0.0, p)
    w_true = R.w_from_shifted(0.0, S.shifted_potential_psi(0.0, p))
    assert w_code == 0.0
    assert w_true == pytest.approx(-1.0)


# ===========================================================================
# 3. The scan artefact
# ===========================================================================
def test_most_scan_values_are_outside_the_physical_bound():
    """16 of 18 reported ``w`` values violate ``-1 <= w <= +1``."""
    s = R.scan_summary(SCAN)
    assert s["n_points"] == 18
    assert s["w"]["n_out_of_bounds"] == 16
    assert s["w"]["verdict"] == "artefact"
    assert s["w"]["min"] < -20.0
    assert s["w"]["max"] > 6.0


def test_no_scanned_point_reaches_the_quartic_regime():
    """``quartic_achieved = False`` in all 18 points (this part is consistent)."""
    s = R.scan_summary(SCAN)
    assert s["quartic_achieved_any"] is False


def test_validator_accepts_a_physical_set():
    """The validator must not flag genuine physics."""
    v = R.validate_w_values([-1.0, -0.5, 0.0, 1 / 3, 1.0])
    assert v["n_out_of_bounds"] == 0
    assert v["verdict"] == "consistent"


def test_validator_flags_both_directions():
    v = R.validate_w_values([-1.5, 0.2, 2.0])
    assert v["n_below_minus_1"] == 1
    assert v["n_above_plus_1"] == 1


# ===========================================================================
# 4. Artifact inventory
# ===========================================================================
def test_every_referenced_script_is_missing():
    """``main.tex`` invokes four scripts under ``scripts/``; the directory is absent."""
    inv = R.script_inventory(REPO)
    assert inv["n_missing"] == len(R.REFERENCED_SCRIPTS)
    assert not os.path.isdir(os.path.join(REPO, "scripts"))


def test_numerical_artifacts_are_declared_not_public():
    inv = R.artifact_inventory()
    assert "CLASS" in " ".join(inv)
    for name in inv:
        assert R.claim_is_supported(name) is False
    assert R.claim_is_supported("something never declared") is False


def test_convergence_claims_are_not_reproducible_here():
    st = R.convergence_status()
    assert st["grid_512"]["reproducible"] is False
    assert st["floquet_0p198"]["reproducible"] is False


# ===========================================================================
# 5. Reproducibility harness (self-test of the machinery)
# ===========================================================================
def test_time_limit_harness():
    import time

    def slow():
        time.sleep(5)

    def fast():
        return 1

    assert R.can_run(fast, timeout=2.0) is True
    assert R.can_run(slow, timeout=0.5) is False


def test_reproducibility_table_shape():
    rows = [1, 2, 3]
    t = R.reproducibility_table(lambda ic: ic, rows, timeout=2.0)
    assert t["n_total"] == 3
    assert t["n_complete"] == 3


# ===========================================================================
# 6. Blocked items -- recorded, never silently passed
# ===========================================================================
@pytest.mark.skip(reason="BLOCKED: modified CLASS code is not public; "
                         "the CLASS/Cobaya results cannot be rerun here")
def test_class_rerun():        # pragma: no cover
    pass


@pytest.mark.skip(reason="BLOCKED: MCMC chains are not public; the reported "
                         "R-1 and ESS values cannot be verified")
def test_mcmc_convergence():   # pragma: no cover
    pass


@pytest.mark.skip(reason="BLOCKED: lattice outputs and scripts/run_lattice.py "
                         "are absent; the 0.198 Floquet value cannot be checked")
def test_lattice_floquet():    # pragma: no cover
    pass


@pytest.mark.skip(reason="BLOCKED: scripts/convergence_test.py is absent; the "
                         "512^3 convergence study cannot be reproduced")
def test_lattice_convergence():  # pragma: no cover
    pass


# ===========================================================================
# 7. What IS reproducible
# ===========================================================================
def test_the_decoupled_reference_matches_sprint4():
    """The one part of the pipeline that does reproduce: SPRINT 4's field runs.

    This ties the reproducibility audit back to a verified result rather than
    leaving it purely negative.
    """
    from src import ptum_background as B
    mu, lam = 1.0, 0.1
    H = 25.0 * 2 * mu / 3.0
    r = B.evolve(psi_i=1e-3 * B.psi0(mu, lam), psidot_i=0.0,
                 mu=mu, lam=lam, H=H, t_max=6.0 / H)
    assert r["w_avg"] == pytest.approx(-1.0, abs=1e-6)


# ===========================================================================
# 8. "Verified with the public script" -- checkable against the script itself
# ===========================================================================
def test_the_script_cannot_produce_spectral_observables():
    """``ptum_task1_simulation.py`` is a background-only integrator."""
    assert R.script_can("homogeneous background") is True
    assert R.script_can("spectral index n_s") is False
    assert R.script_can("tensor-to-scalar ratio r") is False
    assert R.script_can("200-mode Mukhanov-Sasaki") is False


def test_k_modes_is_never_actually_used():
    """``k_modes`` is declared in ``InitialConditions`` and then dropped.

    This is a *source-level* check, so it verifies the claim directly rather
    than trusting a summary table.
    """
    import re
    path = os.path.join(REPO, "ptum_task1_simulation.py")
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    uses = re.findall(r"k_modes", src)
    assert len(uses) == 1, "k_modes appears more than once -- re-check the claim"


def test_script_attestations_are_unsupported():
    for claim in R.SCRIPT_ATTESTATIONS:
        supported, reason = R.attestation_is_supported(claim)
        assert supported is False
        assert reason


def test_no_spectral_code_exists_in_the_script():
    """No power spectrum / transfer function anywhere in the pipeline."""
    path = os.path.join(REPO, "ptum_task1_simulation.py")
    with open(path, encoding="utf-8") as fh:
        src = fh.read().lower()
    for token in ("power_spectrum", "mukhanov", "transfer_function"):
        assert token not in src
