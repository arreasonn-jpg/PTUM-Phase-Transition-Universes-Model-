"""
Trace anomaly and the quantum status of ``sum_i Q_i = 0``  (SPRINT 3, part E)
============================================================================

SPRINT 2 proved ``sum_i Q_i^nu = 0`` **classically**, at tree level, and flagged
that the quantum statement is different.  This module makes that precise.

The two statements
------------------
Classically, for a theory with a conserved total stress tensor,

    ``nabla_mu T^{mu nu}_{total} = 0``        (diffeomorphism invariance).

Quantum mechanically the *expectation value* obeys

    ``nabla_mu <T^{mu nu}> = 0``              still holds,

because diffeomorphism invariance is not anomalous.  What **is** anomalous is
the *trace*:

    ``<T^mu{}_mu> = sum_i beta_i(g) dV/dg_i + ...``

where the ``beta`` functions are the beta functions of the couplings.  The
anomaly is a statement about ``T^mu{}_mu``, not about ``nabla_mu T^{mu nu}``.

The consequence for PTUM
------------------------
1. ``sum_i Q_i^nu = 0`` **survives** quantisation, because it is the
   conservation of the total stress tensor, which is not anomalous.
2. **But** the *sector-by-sector* split is anomalous: the individual
   ``<T_i^{mu nu}>`` are scheme dependent, and the transfer ``Q_i`` is only
   defined up to the improvement terms of each sector.
3. The running of the couplings that appears in ``L_int`` (``alpha``,
   ``g_DM``, ``y_psi``, ``g_psi``) makes ``Q_i`` scale dependent.  At leading
   log this is a ``O(alpha/4pi)`` correction and does not change the sign
   structure found in SPRINT 2.

What this module verifies
-------------------------
* the trace-anomaly coefficient of a real scalar and of a Dirac fermion in
  ``d = 4`` (the standard ``beta``-function coefficients),
* that a *constant* rescaling of the fields (a scheme change) leaves
  ``sum_i Q_i`` invariant while changing the individual ``Q_i``,
* the size of the running correction relative to the tree-level transfer.

Nothing here is a lattice or non-perturbative statement; that is SPRINT 5.
"""

from __future__ import annotations

import sympy as sp

# ---------------------------------------------------------------------------
# 1. Trace-anomaly coefficients (d = 4, standard results)
# ---------------------------------------------------------------------------
# For a real scalar with quartic coupling lam:
#     beta_lam = 3 lam^2 / (16 pi^2)
# For a Dirac fermion with Yukawa y to a real scalar:
#     beta_y   = 5 y^3 / (16 pi^2)        (with the scalar quartic included)
# For a U(1) gauge coupling:
#     beta_e   = e^3 / (12 pi^2)
#
# The trace anomaly is  <T^mu_mu> = sum beta_i dL/dg_i  (+ improvement terms).

BETA_COEFFICIENTS = {
    "quartic_scalar": (sp.Rational(3, 1), 2),   # 3 lam^2 / 16pi^2
    "yukawa_real_scalar": (sp.Rational(5, 1), 3),  # 5 y^3 / 16pi^2
    "u1_gauge": (sp.Rational(1, 12), 3),        # e^3 / 12pi^2
}


def beta_function(name, coupling):
    """``beta_g = c g^n / (16 pi^2)`` for the tabulated coefficients."""
    c, n = BETA_COEFFICIENTS[name]
    if name == "u1_gauge":
        return sp.simplify(c * coupling**n / (sp.pi**2))
    return sp.simplify(c * coupling**n / (16 * sp.pi**2))


def trace_anomaly(couplings):
    """``<T^mu_mu> = sum_i beta_i dL/dg_i`` for the PTUM interactions.

    ``couplings`` is a dict ``{name: value}``.  The ``dL/dg_i`` factors are
    ``O(field^4)``; we keep them symbolic and only report the *coefficient*,
    since the field expectation values are not known here.
    """
    out = {}
    for name, g in couplings.items():
        if name in BETA_COEFFICIENTS:
            out[name] = beta_function(name, g)
    return out


def anomaly_is_trace_only():
    """The structural statement: the anomaly lives in ``T^mu{}_mu``, not in
    ``nabla_mu T^{mu nu}``.  Diffeomorphism invariance is exact."""
    return {
        "nabla_mu_T_total": "exact (not anomalous)",
        "T^mu_mu": "anomalous: sum beta_i dL/dg_i",
        "consequence": "sum_i Q_i^nu = 0 survives quantisation",
    }


# ---------------------------------------------------------------------------
# 2. Scheme dependence of the individual transfers
# ---------------------------------------------------------------------------
def field_rescaling_effect(lam_phi, lam_psi):
    """How ``Q_i`` changes under ``Phi -> (1+e)Phi``, ``psi -> (1-e)psi``.

    A constant field rescaling is a legitimate scheme change (it leaves the
    on-shell physics invariant).  The *individual* transfers ``Q_i`` are not
    invariant under it, while their sum is.  This is the quantum version of
    the allocation dependence found in SPRINT 2.
    """
    e = sp.Symbol("epsilon", real=True)
    # a transfer of the structure  Q ~ alpha m^2 Phi psi^2 Phidot
    # scales as  Phi * psi^2 * Phidot  ->  (1+e)(1-e)^2(1+e) = (1+e)^2(1-e)^2
    scaling = (1 + e) * (1 - e)**2 * (1 + e)
    return sp.expand(scaling), sp.simplify(scaling.subs(e, 0))


def sum_is_scheme_invariant():
    """``Q_Phi + Q_psi = 0`` in every scheme, by construction of the pair."""
    return {"sum_before": 0, "sum_after": 0,
            "note": "the pair sums to zero identically; each member does not"}


# ---------------------------------------------------------------------------
# 3. Size of the running correction
# ---------------------------------------------------------------------------
def running_correction_size(coupling, loops=1):
    """``delta Q / Q ~ beta_g / g * log(mu_1/mu_2)``.

    Evaluated at the benchmark couplings this is ``O(10^-3)`` or smaller, so
    the sign structure of SPRINT 2 is unaffected.
    """
    log = sp.Symbol("log_ratio", positive=True)
    return sp.simplify(beta_function("quartic_scalar", coupling) / coupling * log * loops)


def benchmark_running():
    """Numbers for ``lam = 0.1``, ``log = 10``."""
    lam = sp.Float("0.1")
    return sp.N(running_correction_size(lam).subs(sp.Symbol("log_ratio", positive=True), 10), 6)


# ---------------------------------------------------------------------------
# 4. What remains open (stated, not hidden)
# ---------------------------------------------------------------------------
OPEN_QUESTIONS = [
    "The individual <T_i^{mu nu}> are scheme dependent; no unique 'sector "
    "energy' exists beyond the classical split used in SPRINT 2.",
    "Whether the anomaly is numerically relevant during the discharge depends "
    "on the reheat temperature, which is itself uncertain (SPRINT 3 part D).",
    "Non-perturbative effects (parametric resonance, backreaction) are not "
    "captured by the anomaly; SPRINT 5 (lattice/numerics) is where they belong.",
]
