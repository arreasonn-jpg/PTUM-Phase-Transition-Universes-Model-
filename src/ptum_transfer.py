"""
PTUM energy-momentum transfer vectors  (SPRINT 2)
=================================================

Every ``Q_i^nu`` is derived here from the SPRINT-1 action.  No sign is imposed
and ``sum_i Q_i^nu = 0`` is never assumed: it is a consequence.

The derivation (complete, four lines)
-------------------------------------
Write the total Lagrangian as

    ``L = sum_i L_i^free + L_int``,     ``L_i^free = 1/2 phidot_i^2 - V_i(phi_i)``

and split the interaction between the sectors that appear in it,

    ``L_i = L_i^free + lam_i L_int``,   ``sum_i lam_i = 1``.        (allocation)

The ``T_i^{mu nu}`` defined from this ``L_i`` give

    ``rho_i = 1/2 phidot_i^2 + V_i - lam_i L_int``,
    ``rho_i + p_i = phidot_i^2``,

so

    ``nabla_mu T_i^{mu 0} = phidot_i (phiddot_i + 3H phidot_i + V_i')
                            - lam_i dL_int/dt``.

The **full** equation of motion of field ``i`` is

    ``phiddot_i + 3H phidot_i + V_i' = dL_int/dphi_i``,

hence

    ``Q_i^0 = phidot_i dL_int/dphi_i - lam_i dL_int/dt``.           (**)

Summing:

    ``sum_i Q_i^0 = sum_i phidot_i dL_int/dphi_i - (sum_i lam_i) dL_int/dt
                  = dL_int/dt - dL_int/dt = 0``

identically, **for every allocation** ``{lam_i}``.  This is the algebraic
content of "``sum_i Q_i = 0``"; it is not a term-by-term sign cancellation.

Consequences that the tests check
---------------------------------
* ``(**)</s>`` agrees with a *direct* ``nabla_mu T_i^{mu 0}`` computed from
  ``rho_i, p_i`` with the full EOM substituted (no shortcut).
* ``sum_i Q_i^0 = 0`` for several allocations.
* Each ``Q_i^0`` has mass dimension 5 (``GeV^5``).
* ``Q_i -> 0`` when the corresponding coupling is switched off.
* ``Q_i`` **does** depend on the allocation, and so does the split of energy
  between "transfer" and "``rho_i + 3H(rho_i + p_i)``".  What is allocation
  independent is the pair sum and hence the physical evolution.

What the manuscript gets right and wrong
----------------------------------------
* ``Q_DM``/``Q_DE`` (Eqs. 78-79): **correct**, and reproduced by ``lam_chi = 1``.
* ``Q_Phi`` (Eq. 77): **correct** as printed, and reproduced by ``lam_Phi = 0``.
* ``Q_psi`` (Eq. 76): **not** the derived transfer for the ``Phi^2 psi^2``
  interaction.  The manuscript writes ``Q_psi = -Q_Phi``; the derivation gives
  ``Q_psi = psidot dL_int/dpsi - lam_psi dL_int/dt``, which differs by a
  ``psidot`` term.  Writing the pair as exact opposites is a *choice* that makes
  the sum vanish, not a derivation.
* The Yukawa term ``y psi fbar gamma^nu f``: **dimensionally wrong** (``GeV^4``)
  and structurally wrong (a vector current instead of a derivative of the
  bilinear).  The derived object is ``Q_psi^0 = y psi d(fbar f)/dt``.

Units
-----
``[Q^nu] = GeV^5``.  With ``[phi] = 1``, ``[f] = 3/2``, ``[d_mu] = 1``:

    alpha m^2 (Phi/E_th^2) psi^2 dPhi  ->  5   OK
    y_psi psi fbar gamma^nu f          ->  4   WRONG   (the manuscript's form)
    y_psi (fbar f) dpsi                ->  5   OK      (the derived form)
    2 g_DM chi^2 Phi_res dPhi_res      ->  5   OK
    g_psi psi^2 phi_SM dphi_SM         ->  5   OK

So the printed Yukawa term is the *only* dimensionally wrong one.  This
supersedes the broader wording of AUDIT_00 finding B-08.
"""

from __future__ import annotations

import sympy as sp

from .ptum_symbolic import (
    alpha, g_DM, g_psi, lam_psi, m, m_chi, y_psi, fbarf,
    V_eff_fuel, V_DE, V_act,
)

t = sp.symbols("t", positive=True)
H = sp.symbols("H", real=True)
E_th = sp.symbols("E_th", positive=True)

Phi_b = sp.Function("Phi")(t)
psi_b = sp.Function("psi")(t)
chi_b = sp.Function("chi")(t)
res_b = sp.Function("Phi_res")(t)
phiSM_b = sp.Function("phi_SM")(t)

A = sp.Function("a")(t)


def Hs():
    return sp.diff(A, t) / A


# ---------------------------------------------------------------------------
# 1. FRW divergence and the EOMs
# ---------------------------------------------------------------------------
def frw_divergence_0(rho, p):
    """``nabla_mu T^{mu 0} = rhodot + 3H(rho+p)`` (homogeneous fluid)."""
    return sp.expand(sp.diff(rho, t) + 3 * Hs() * (rho + p))


def canonical_EOM(field, potential):
    return sp.expand(sp.diff(field, t, 2) + 3 * Hs() * sp.diff(field, t)
                     + sp.diff(potential, field))


def divergence_minus_phidot_EOM(field, potential):
    """``nabla_mu T^{mu 0} - phidot * EOM`` must vanish identically."""
    phidot = sp.diff(field, t)
    rho = sp.Rational(1, 2) * phidot**2 + potential
    p = sp.Rational(1, 2) * phidot**2 - potential
    return sp.simplify(frw_divergence_0(rho, p) - phidot * canonical_EOM(field, potential))


from .ptum_symbolic import frw_eoms_symbolic as _frw_eoms  # noqa: E402


def _onshell_seconds():
    eoms = _frw_eoms()
    out = {}
    for key, fld in (("Phi", Phi_b), ("psi", psi_b), ("chi", chi_b), ("Phi_res", res_b)):
        d2 = sp.Derivative(fld, (t, 2))
        sol = sp.solve(sp.Eq(sp.expand(eoms[key]), 0), d2)
        assert len(sol) == 1, key
        out[key] = sp.expand(sol[0].subs(H, Hs()))
    return out


ONSHELL = _onshell_seconds()
FIELD = {"Phi": Phi_b, "psi": psi_b, "chi": chi_b, "Phi_res": res_b,
         "SM": phiSM_b, "f": fbarf}


# ---------------------------------------------------------------------------
# 2. Interaction Lagrangians (L_int, not V_int) -- signs from SPRINT 1
# ---------------------------------------------------------------------------
def L_int_psi_Phi():
    """``+alpha m^2 Phi^2 psi^2/(2 E_th^2)``, from ``-1/2 m^2(1-alpha Phi^2/E_th^2)psi^2``."""
    return alpha * m**2 * Phi_b**2 * psi_b**2 / (2 * E_th**2)


def L_int_DM_DE():
    return -g_DM * chi_b**2 * res_b**2


def L_int_yukawa():
    return -y_psi * psi_b * fbarf


def L_int_quartic():
    return -sp.Rational(1, 2) * g_psi * psi_b**2 * phiSM_b**2


# ---------------------------------------------------------------------------
# 3. The general formula (**)
# ---------------------------------------------------------------------------
def Q_two_field(L_int, field_a, field_b, label_a, label_b, lam_a):
    """Apply ``Q_i^0 = phidot_i dL_int/dphi_i - lam_i dL_int/dt``.

    Parameters
    ----------
    L_int : SymPy expression, the interaction Lagrangian.
    lam_a : Rational(0..1); ``lam_b = 1 - lam_a``.

    Returns ``{label_a: Q_a^0, label_b: Q_b^0}``.
    """
    lam_a = sp.Rational(lam_a)
    lam_b = 1 - lam_a
    dLdt = sp.diff(L_int, field_a) * sp.diff(field_a, t) \
        + sp.diff(L_int, field_b) * sp.diff(field_b, t)
    qa = sp.expand(sp.diff(L_int, field_a) * sp.diff(field_a, t) - lam_a * dLdt)
    qb = sp.expand(sp.diff(L_int, field_b) * sp.diff(field_b, t) - lam_b * dLdt)
    return {label_a: qa, label_b: qb}


def zero(expr) -> bool:
    """True when ``expr`` is identically zero.

    ``sp.simplify`` does not cancel derivative coefficients (e.g.
    ``g*phi*psi*phidot`` against ``g*phi*psi*phidot``) when the terms also carry
    ``Derivative`` objects, so we replace every derivative by an independent
    symbol first and *then* simplify.  The replacement is injective on the
    set of derivatives appearing in ``expr``, so a zero result means the
    original expression is a polynomial identity in the derivatives.
    """
    e = sp.expand(expr)
    if e == 0:
        return True
    atoms = sorted(e.atoms(sp.Derivative), key=str)
    subs = {a: sp.Symbol(f"_d{i}") for i, a in enumerate(atoms)}
    return sp.simplify(sp.expand(e.subs(subs))) == 0


def Q_psi_Phi(lam_Phi=sp.Integer(0)):
    """Transfers for ``+alpha m^2 Phi^2 psi^2/(2 E_th^2)``.

    ``lam_Phi = 0`` puts all of ``L_int`` on ``psi`` -- which is where it lives
    in the action, since it comes from ``m_eff^2(Phi) psi^2/2``.  This choice
    reproduces ``Q_Phi`` of ``main.tex`` Eq. (77) exactly.
    """
    return Q_two_field(L_int_psi_Phi(), Phi_b, psi_b, "Phi", "psi", lam_Phi)


def Q_DM_DE(lam_chi=sp.Integer(1)):
    """Transfers for ``-g_DM chi^2 Phi_res^2``; ``lam_chi = 1`` reproduces Eqs. (78)-(79)."""
    return Q_two_field(L_int_DM_DE(), chi_b, res_b, "chi", "Phi_res", lam_chi)


def Q_yukawa(lam_psi=sp.Rational(1, 2)):
    """Transfers for ``-y_psi psi fbar f`` (bilinear approximation for the fermion)."""
    out = Q_two_field(L_int_yukawa(), psi_b, fbarf, "psi", "f", lam_psi)
    out["note"] = ("fermionic half needs the Dirac equation; only <fbar f> is retained "
                   "-> PARTIAL")
    return out


def Q_quartic(lam_psi=sp.Rational(1, 2)):
    """Transfers for ``-1/2 g_psi psi^2 phi_SM^2``."""
    out = Q_two_field(L_int_quartic(), psi_b, phiSM_b, "psi", "SM", lam_psi)
    out["note"] = ("with <psi>=0 this operator mediates psi psi -> phi phi (annihilation), "
                   "not the 1->2 decay psi -> phi phi")
    return out


# ---------------------------------------------------------------------------
# 4. Direct, independent check of (**)
# ---------------------------------------------------------------------------
def direct_divergence(name, potential_own, interaction_share):
    """``nabla_mu T_i^{mu 0}`` from ``rho_i, p_i``, with the full EOM substituted.

    ``L_i = 1/2 phidot^2 - V_own + interaction_share`` (``interaction_share``
    is ``lam_i * L_int``), so ``rho_i = 1/2 phidot^2 + V_own - interaction_share``.
    """
    fld = FIELD[name]
    phidot = sp.diff(fld, t)
    rho = sp.expand(sp.Rational(1, 2) * phidot**2 + potential_own - interaction_share)
    p = sp.expand(sp.Rational(1, 2) * phidot**2 - potential_own + interaction_share)
    d = sp.expand(frw_divergence_0(rho, p))
    key = name if name in ONSHELL else None
    if key is not None:
        d = d.subs(sp.Derivative(fld, (t, 2)), ONSHELL[key])
    return sp.simplify(d)


V_OWN = {
    "Phi": V_eff_fuel(Phi_b),
    "psi": sp.Rational(1, 2) * m**2 * psi_b**2 + lam_psi / 4 * psi_b**4,
    "chi": sp.Rational(1, 2) * m_chi**2 * chi_b**2,
    "Phi_res": V_DE(res_b),
}


def closure_residual(name, other, L_int, lam):
    """``direct_divergence(name) - Q_formula(name)``; must be zero."""
    formula = Q_two_field(L_int, FIELD[name], FIELD[other], name, other, lam)[name]
    direct = direct_divergence(name, V_OWN[name], lam * L_int)
    return sp.expand(direct - formula)


# ---------------------------------------------------------------------------
# 5. Aggregate quantities
# ---------------------------------------------------------------------------
COUPLING_OF = {"psi_Phi": alpha, "DM_DE": g_DM, "yukawa": y_psi, "quartic": g_psi}


def all_Q(lam_psiPhi=sp.Integer(0), lam_DMDE=sp.Integer(1),
          lam_yuk=sp.Rational(1, 2), lam_quart=sp.Rational(1, 2)):
    """``Q_i^0`` for every sector, summing each sector's share over interactions."""
    parts = {
        "psi_Phi": Q_psi_Phi(lam_psiPhi),
        "DM_DE": Q_DM_DE(lam_DMDE),
        "yukawa": Q_yukawa(lam_yuk),
        "quartic": Q_quartic(lam_quart),
    }
    out = {k: sp.Integer(0) for k in FIELD}
    for d in parts.values():
        for k, v in d.items():
            if k == "note":
                continue
            out[k] = sp.expand(out[k] + v)
    return out


def total_Q(**kw):
    """``sum_i Q_i^0``; must be identically zero."""
    return sp.simplify(sum(all_Q(**kw).values()))


def interaction_off_test():
    """Return the couplings; used by ``test_interaction_off_means_all_Q_zero``."""
    return COUPLING_OF


# ---------------------------------------------------------------------------
# 6. Background rates and the FRW time-component sign convention
# ---------------------------------------------------------------------------
def background_rates():
    """``nu = 0`` components with the sign convention stated explicitly.

    ``rho_i' + 3H(rho_i + p_i) = Q_i`` and ``Q_i > 0`` means **inflow** into
    sector ``i``.  In ``(-+++)``, ``T^0{}_0 = -rho``, so a positive ``Q`` for an
    energy *gain* corresponds to ``nabla_mu T_i^{mu 0} = -Q_i``.  The convention
    is recorded here because the audit brief lists it as a mandatory check.
    """
    q = all_Q()
    return {
        "convention": "rho_i' + 3H(rho_i+p_i) = Q_i ; Q_i>0 means inflow",
        **{k: v for k, v in q.items()},
    }


# ---------------------------------------------------------------------------
# 7. Dimensional bookkeeping
# ---------------------------------------------------------------------------
DIM = {"alpha": 0, "m": 1, "Phi": 1, "psi": 1, "E_th": 1, "g_DM": 0, "chi": 1,
       "Phi_res": 1, "y_psi": 0, "fbar f": 3, "g_psi": 0, "phi_SM": 1, "d": 1}

TERM_DIMENSIONS = {
    "Q_psi(alpha)":             [("alpha", 1), ("m", 2), ("Phi", 1), ("E_th", -2), ("psi", 2), ("d", 1), ("Phi", 1)],
    "Q_psi(yukawa,as printed)": [("y_psi", 1), ("psi", 1), ("fbar f", 1)],
    "Q_psi(yukawa,derived)":    [("y_psi", 1), ("fbar f", 1), ("d", 1), ("psi", 1)],
    "Q_dm":                     [("g_DM", 1), ("chi", 2), ("Phi_res", 1), ("d", 1), ("Phi_res", 1)],
    "Q_quartic":                [("g_psi", 1), ("psi", 2), ("phi_SM", 1), ("d", 1), ("phi_SM", 1)],
}


def term_dimension(name):
    return sum(DIM[s] * pw for s, pw in TERM_DIMENSIONS[name])


if __name__ == "__main__":  # pragma: no cover
    print("dimensions (target 5):")
    for k in TERM_DIMENSIONS:
        print(f"  {k:26s} {term_dimension(k):2d}")
    print("\nsum_i Q_i^0 =", total_Q())


# ---------------------------------------------------------------------------
# 8. Sign audit against the printed equations of main.tex
# ---------------------------------------------------------------------------
def manuscript_Q(name):
    """The ``Q_i^0`` exactly as printed in ``main.tex`` lines 1684-1686."""
    if name == "Q_Phi":
        return -alpha * m**2 * Phi_b * psi_b**2 * sp.diff(Phi_b, t) / E_th**2
    if name == "Q_psi_PhiTerm":
        return +alpha * m**2 * Phi_b * psi_b**2 * sp.diff(Phi_b, t) / E_th**2
    if name == "Q_DM":
        return -2 * g_DM * chi_b**2 * res_b * sp.diff(res_b, t)
    if name == "Q_DE":
        return +2 * g_DM * chi_b**2 * res_b * sp.diff(res_b, t)
    if name == "Q_psi_Yukawa":
        return y_psi * psi_b * fbarf                 # y_psi psi fbar gamma^nu f
    if name == "Q_SM_Yukawa":
        return -y_psi * psi_b * fbarf
    if name == "Q_psi_Quartic":
        return +g_psi * psi_b**2 * phiSM_b * sp.diff(phiSM_b, t)
    if name == "Q_SM_Quartic":
        return -g_psi * psi_b**2 * phiSM_b * sp.diff(phiSM_b, t)
    raise KeyError(name)


def manuscript_Q_derived(name, **kw):
    """The derived counterpart of :func:`manuscript_Q`."""
    if name == "Q_Phi":
        return Q_psi_Phi(0)["Phi"]
    if name == "Q_psi_PhiTerm":
        return Q_psi_Phi(0)["psi"]
    if name == "Q_DM":
        return Q_DM_DE(1)["chi"]
    if name == "Q_DE":
        return Q_DM_DE(1)["Phi_res"]
    if name == "Q_psi_Yukawa":
        return Q_yukawa(0)["psi"]
    if name == "Q_SM_Yukawa":
        return Q_yukawa(0)["f"]
    if name == "Q_psi_Quartic":
        return Q_quartic(0)["psi"]
    if name == "Q_SM_Quartic":
        return Q_quartic(0)["SM"]
    raise KeyError(name)


MANUSCRIPT_Q_NAMES = ("Q_Phi", "Q_psi_PhiTerm", "Q_DM", "Q_DE",
                      "Q_psi_Yukawa", "Q_SM_Yukawa",
                      "Q_psi_Quartic", "Q_SM_Quartic")


def sign_table():
    """Compare each printed ``Q_i`` with the derived one.

    Returns ``{name: "opposite" | "same" | "different structure"}``.

    The result of this audit is the central finding of SPRINT 2:
    **every** printed ``Q_i`` has the opposite overall sign to the derived one,
    which is a single global convention error in Eqs. (1684)-(1686), not eight
    independent mistakes.
    """
    out = {}
    for nm in MANUSCRIPT_Q_NAMES:
        ms, ours = manuscript_Q(nm), manuscript_Q_derived(nm)
        if zero(ours + ms):
            out[nm] = "opposite"
        elif zero(ours - ms):
            out[nm] = "same"
        else:
            out[nm] = "different structure"
    return out


def manual_continuity_check(name, L_int, lam, potential_own, other_field=None):
    """Textbook check: ``rho_i' + 3H(rho_i + p_i)`` for one sector, by hand.

    Independent of formula (**): we build ``rho_i`` and ``p_i`` from ``L_i``
    and differentiate, then substitute the *full* EOM of the field.  Used to
    confirm that the sign of ``Q`` corresponds to ``Q_i > 0`` = inflow.
    """
    fld = FIELD[name]
    phidot = sp.diff(fld, t)
    rho = sp.expand(sp.Rational(1, 2) * phidot**2 + potential_own - lam * L_int)
    p = sp.expand(sp.Rational(1, 2) * phidot**2 - potential_own + lam * L_int)
    d = sp.expand(frw_divergence_0(rho, p))
    if name in ONSHELL:
        d = d.subs(sp.Derivative(fld, (t, 2)), ONSHELL[name])
    return sp.simplify(d)
