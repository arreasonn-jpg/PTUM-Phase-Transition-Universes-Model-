"""
SPRINT 2 test suite -- energy-momentum transfer vectors ``Q_i^nu``.

Mandatory checks from the audit brief (section 3):

* every ``Q_i^nu`` is ``GeV^5``;
* ``sum_i Q_i^nu = 0``;
* ``Q_i^nu = 0`` when the interaction is switched off;
* in a two-sector example one sector's loss equals the other's gain;
* the FRW time-component sign convention is explicit.

Everything is derived in ``src/ptum_transfer.py`` from

    ``Q_i^0 = phidot_i dL_int/dphi_i - lam_i dL_int/dt``,

which follows from ``nabla_mu T_i^{mu 0}`` with the full equations of motion
substituted.  ``sum_i Q_i^0 = 0`` is then an identity, not an assumption.

Run::

    python -m pytest tests/test_transfer_vectors.py -v
"""

from __future__ import annotations

import sympy as sp

from src import ptum_transfer as T
from src.ptum_transfer import (
    alpha, g_DM, g_psi, m, y_psi, E_th,
    Phi_b, psi_b, chi_b, res_b, phiSM_b, fbarf, t,
)

R = sp.Rational


# ===========================================================================
# 1. Dimensions -- every Q^nu must be GeV^5
# ===========================================================================
def test_dimension_table():
    d = {name: T.term_dimension(name) for name in T.TERM_DIMENSIONS}
    assert d["Q_psi(alpha)"] == 5
    assert d["Q_dm"] == 5
    assert d["Q_quartic"] == 5
    assert d["Q_psi(yukawa,derived)"] == 5
    assert d["Q_psi(yukawa,as printed)"] == 4
    # the printed Yukawa term is the only dimensionally wrong one
    assert [k for k, v in d.items() if v != 5] == ["Q_psi(yukawa,as printed)"]


def test_yukawa_dimension_arithmetic():
    assert T.DIM["y_psi"] + T.DIM["psi"] + T.DIM["d"] + T.DIM["fbar f"] == 5
    assert T.DIM["y_psi"] + T.DIM["psi"] + T.DIM["fbar f"] == 4


# ===========================================================================
# 2. FRW divergence identity and the sign convention
# ===========================================================================
def test_frw_divergence_identity():
    """``nabla_mu T^{mu 0} - phidot*EOM = 0`` for a canonical scalar."""
    phi = sp.Function("phi")(t)
    V = sp.Function("V")(phi)
    assert T.divergence_minus_phidot_EOM(phi, V) == 0


def test_sign_convention_is_explicit():
    rates = T.background_rates()
    assert "Q_i>0 means inflow" in rates["convention"]
    assert "rho_i' + 3H(rho_i+p_i) = Q_i" in rates["convention"]


# ===========================================================================
# 3. The derivation: formula (**) against a direct divergence
# ===========================================================================
def test_formula_matches_direct_divergence_psi_Phi():
    """``Phi`` appears only in this one interaction, so its closure must be exact."""
    for lam in (0, R(1, 4), R(1, 2), R(3, 4), 1):
        assert T.zero(T.closure_residual("Phi", "psi", T.L_int_psi_Phi(), lam)), lam


def test_psi_sector_residual_is_exactly_the_other_two_interactions():
    """``psi`` sits in three interactions.

    Closing the psi sector with *only* ``psi_Phi`` must leave precisely the
    Yukawa and quartic transfers behind -- which is a strong independent check
    that the three contributions add up correctly and nothing is missing.
    """
    for lam in (0, R(1, 2), 1):
        residual = T.closure_residual("psi", "Phi", T.L_int_psi_Phi(), lam)
        expected = T.Q_yukawa(0)["psi"] + T.Q_quartic(0)["psi"]
        assert T.zero(residual - expected), lam


def test_formula_matches_direct_divergence_DM_DE():
    for lam in (0, R(1, 2), 1):
        assert T.zero(T.closure_residual("chi", "Phi_res", T.L_int_DM_DE(), lam)), lam
        assert T.zero(T.closure_residual("Phi_res", "chi", T.L_int_DM_DE(), 1 - R(lam))), lam


# ===========================================================================
# 4. Global closure for arbitrary allocations
# ===========================================================================
def test_sum_Q_vanishes_identically():
    for kw in ({},
               dict(lam_psiPhi=R(1, 2), lam_DMDE=R(1, 2)),
               dict(lam_psiPhi=R(1, 3), lam_DMDE=R(2, 5), lam_yuk=R(1, 4)),
               dict(lam_psiPhi=1, lam_DMDE=0, lam_yuk=R(3, 7), lam_quart=R(2, 9))):
        assert T.total_Q(**kw) == 0, kw


def test_sum_Q_is_not_a_term_by_term_sign_flip():
    """The closure is structural: each ``Q_i`` is derived separately.

    ``psi`` is *not* simply ``-Phi``: ``Q_Phi = phidot dL/dPhi - lam dL/dt``
    and ``Q_psi = psidot dL/dpsi - (1-lam) dL/dt`` are different objects that
    happen to sum to zero.
    """
    L = T.L_int_psi_Phi()
    q = T.Q_psi_Phi(0)
    dLdt = sp.diff(L, t)
    # Q_Phi = Phidot dL/dPhi - 0 * dL/dt
    assert T.zero(q["Phi"] - sp.diff(L, Phi_b) * sp.diff(Phi_b, t))
    # Q_psi = psidot dL/dpsi - 1 * dL/dt        (and dL/dpsi != 0)
    assert T.zero(q["psi"] - (sp.diff(L, psi_b) * sp.diff(psi_b, t) - dLdt))
    assert not T.zero(sp.diff(L, psi_b))
    assert T.zero(q["Phi"] + q["psi"])


def test_allocation_dependence():
    """Individual Q's depend on the split; the pair sum does not."""
    a, b = T.Q_psi_Phi(0), T.Q_psi_Phi(R(1, 2))
    assert not T.zero(a["Phi"] - b["Phi"])
    assert T.zero((a["Phi"] + a["psi"]) - (b["Phi"] + b["psi"]))


# ===========================================================================
# 5. A) Phi-psi
# ===========================================================================
def test_psi_Phi_closed_forms():
    """``L_int = +alpha m^2 Phi^2 psi^2/2E_th^2`` with ``lam_Phi = 0``."""
    q = T.Q_psi_Phi(0)
    expected_phi = +alpha * m**2 * Phi_b * psi_b**2 * sp.diff(Phi_b, t) / E_th**2
    expected_psi = -alpha * m**2 * Phi_b * psi_b**2 * sp.diff(Phi_b, t) / E_th**2
    assert T.zero(q["Phi"] - expected_phi)
    assert T.zero(q["psi"] - expected_psi)


def test_psi_Phi_is_opposite_to_the_manuscript():
    """main.tex Eq. (77) prints the negative of the derived ``Q_Phi``."""
    assert T.zero(T.Q_psi_Phi(0)["Phi"] + T.manuscript_Q("Q_Phi"))


def test_psi_Phi_switching_off():
    for lam in (0, R(1, 2)):
        q = T.Q_psi_Phi(lam)
        assert T.zero(q["Phi"].subs(alpha, 0))
        assert T.zero(q["psi"].subs(alpha, 0))


# ===========================================================================
# 6. B) DM-DE
# ===========================================================================
def test_DM_DE_closed_forms():
    q = T.Q_DM_DE(1)
    expected = 2 * g_DM * chi_b**2 * res_b * sp.diff(res_b, t)
    assert T.zero(q["chi"] - expected)
    assert T.zero(q["Phi_res"] + expected)


def test_DM_DE_is_opposite_to_the_manuscript():
    q = T.Q_DM_DE(1)
    assert T.zero(q["chi"] + T.manuscript_Q("Q_DM"))
    assert T.zero(q["Phi_res"] + T.manuscript_Q("Q_DE"))


def test_DM_DE_two_sector_energy_conservation():
    q = T.Q_DM_DE(1)
    assert T.zero(q["chi"] + q["Phi_res"])


def test_DM_DE_switching_off():
    q = T.Q_DM_DE(1)
    assert T.zero(q["chi"].subs(g_DM, 0))
    assert T.zero(q["Phi_res"].subs(g_DM, 0))


# ===========================================================================
# 7. C) Yukawa
# ===========================================================================
def test_yukawa_closed_forms():
    """``L_int = -y psi fbar f`` with ``lam_psi = 0``.

    ``Q_psi = -y (fbar f) psidot``,  ``Q_f = +y psidot (fbar f)``.
    """
    q = T.Q_yukawa(0)
    assert T.zero(q["psi"] + y_psi * fbarf * sp.diff(psi_b, t))
    assert T.zero(q["f"] - y_psi * fbarf * sp.diff(psi_b, t))


def test_yukawa_has_dimension_five():
    q = T.Q_yukawa(0)
    assert T.term_dimension("Q_psi(yukawa,derived)") == 5
    # the printed version is lower-dimensional AND has different structure
    assert not T.zero(q["psi"] - T.manuscript_Q("Q_psi_Yukawa"))


def test_yukawa_sum_closes():
    for lam in (0, R(1, 2), 1):
        q = T.Q_yukawa(lam)
        assert T.zero(q["psi"] + q["f"])


def test_yukawa_switching_off():
    q = T.Q_yukawa(R(1, 2))
    assert T.zero(q["psi"].subs(y_psi, 0))
    assert T.zero(q["f"].subs(y_psi, 0))


def test_yukawa_partial_label():
    assert "PARTIAL" in T.Q_yukawa()["note"]


# ===========================================================================
# 8. D) Quartic reheating
# ===========================================================================
def test_quartic_closed_forms():
    """``L_int = -g psi^2 phi^2/2`` with ``lam_psi = 0``.

    ``Q_psi = -g psi phi^2 psidot``,  ``Q_SM = +g psi phi^2 psidot``.
    """
    q = T.Q_quartic(0)
    expected = -g_psi * psi_b * phiSM_b**2 * sp.diff(psi_b, t)
    assert T.zero(q["psi"] - expected)
    assert T.zero(q["SM"] + expected)


def test_quartic_manuscript_has_different_structure():
    """main.tex has ``Q_SM = -g psi^2 phi dphi``: a different operator entirely."""
    q = T.Q_quartic(0)
    assert not T.zero(q["SM"] - T.manuscript_Q("Q_SM_Quartic"))


def test_quartic_sum_closes():
    for lam in (0, R(1, 2), 1):
        q = T.Q_quartic(lam)
        assert T.zero(q["psi"] + q["SM"])


def test_quartic_switching_off():
    q = T.Q_quartic(R(1, 2))
    assert T.zero(q["psi"].subs(g_psi, 0))
    assert T.zero(q["SM"].subs(g_psi, 0))


def test_quartic_is_annihilation_not_decay():
    assert "annihilation" in T.Q_quartic()["note"]


# ===========================================================================
# 9. Aggregate
# ===========================================================================
def test_all_couplings_off_means_all_Q_zero():
    q = T.all_Q()
    subs = {alpha: 0, g_DM: 0, y_psi: 0, g_psi: 0}
    for name, val in q.items():
        assert T.zero(val.subs(subs)), name


def test_all_Q_covers_every_sector():
    assert set(T.all_Q()) == {"Phi", "psi", "chi", "Phi_res", "SM", "f"}


# ===========================================================================
# 10. The central sign finding
# ===========================================================================
def test_every_printed_Q_has_the_opposite_overall_sign():
    """SPRINT 2 finding: Eqs. (1684)-(1686) carry one global sign error.

    All four potential-derived ``Q_i`` are exactly the negative of the derived
    ones; the four Yukawa/quartic entries differ in structure as well.
    """
    table = T.sign_table()
    for nm in ("Q_Phi", "Q_psi_PhiTerm", "Q_DM", "Q_DE"):
        assert table[nm] == "opposite", nm
    for nm in ("Q_psi_Yukawa", "Q_SM_Yukawa", "Q_psi_Quartic", "Q_SM_Quartic"):
        assert table[nm] == "different structure", nm


def test_line_1712_of_the_manuscript_agrees_with_the_derivation():
    """main.tex line 1712 writes ``Q_DM ~ -Q_DE ~ +2g chi^2 Phi_res Phidot_res``.

    That is *our* ``Q_DM``, i.e. the text is internally inconsistent with its
    own Eq. (1684) which has the opposite sign.
    """
    q = T.Q_DM_DE(1)
    line1712 = 2 * g_DM * chi_b**2 * res_b * sp.diff(res_b, t)
    assert T.zero(q["chi"] - line1712)
    assert T.zero(T.manuscript_Q("Q_DM") + line1712)


# ===========================================================================
# 11. Cross-check of the global convention against the manuscript's own text
# ===========================================================================
def test_manuscript_states_nabla_T_equals_Q_but_uses_the_opposite_sign():
    """The manuscript declares ``nabla_mu T_i^{mu nu} = Q_i^nu`` and ``Q_i>0`` = inflow.

    Under that stated convention the printed ``Q_Phi`` has the wrong sign: during
    discharge ``Phidot < 0`` and the fuel must *lose* energy, so ``Q_Phi`` must be
    negative.  The printed expression gives ``+alpha m^2 Phi psi^2|Phidot|/E_th^2
    > 0``, i.e. the fuel would gain energy while driving the transition.
    """
    # a representative point on the discharge trajectory
    vals = {Phi_b: sp.Integer(2), psi_b: sp.Integer(1), E_th: sp.Integer(1),
            sp.Symbol("alpha"): sp.Rational(1, 10), m: sp.Integer(1),
            sp.Derivative(Phi_b, t): sp.Integer(-1)}
    printed = T.manuscript_Q("Q_Phi").subs(vals)
    derived = T.Q_psi_Phi(0)["Phi"].subs(vals)
    assert printed.is_positive is True      # fuel would gain energy -- unphysical
    assert derived.is_negative is True      # fuel loses energy -- correct
    # and the energy lands in psi
    assert T.Q_psi_Phi(0)["psi"].subs(vals).is_positive is True


def test_manuscript_line_1712_contradicts_its_own_equation_1684():
    """Line 1712: ``Q_DM ~ -Q_DE ~ +2g chi^2 Phi_res Phidot_res``.

    That is the derived sign.  Eq. (1684) two lines above prints the negative.
    The manuscript is therefore internally inconsistent, which is exactly why a
    single global sign flip (not eight local edits) is the right repair.
    """
    q = T.Q_DM_DE(1)
    line1712 = 2 * g_DM * chi_b**2 * res_b * sp.diff(res_b, t)
    assert T.zero(q["chi"] - line1712)
    assert T.zero(T.manuscript_Q("Q_DM") + line1712)
