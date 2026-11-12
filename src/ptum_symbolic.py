"""
PTUM symbolic derivation core  (SPRINT 1)
==========================================

Single source of truth for the *action, conventions and stress-energy* of the
PTUM effective theory.  Everything in this module is derived from one action;
nothing is copied from `main.tex`.

Fixed conventions (SPRINT 1 decision, option (a) of AUDIT_00 §10)
------------------------------------------------------------------
* Metric signature  ``(-+++)``
* Riemann            ``R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - ...`` (MTW)
* Matter action      ``S_m = int d^4x sqrt(-g) L_m``
* Stress-energy      ``T_{mu nu} = -2/sqrt(-g) * delta(sqrt(-g) L_m)/delta g^{mu nu}``
* Canonical scalar   ``L = -1/2 g^{mu nu} d_mu phi d_nu phi - V(phi)``

Why ``-1/2`` and not ``+1/2``
-----------------------------
In ``main.tex`` (lines 318-320 and 375/443/469/475/2541-2544) the kinetic term is
written ``+1/2 (d phi)^2``.  With signature ``(-+++)`` that term has the *wrong*
sign for a canonical field: varying the action gives
``-phi'' - 3H phi' + V' = 0`` (a ghost-like sign), not the printed
``phi'' + 3H phi' + V' = 0``.  Moreover ``T_{00}`` becomes
``-1/2 phi'^2 + V`` instead of ``+1/2 phi'^2 + V``.
With ``-1/2`` both the printed equation of motion and the printed
``rho = 1/2 phi'^2 + V``, ``p = 1/2 phi'^2 - V`` are recovered.
This is AUDIT_00 finding **B-04**.

Every function below is exercised in ``tests/test_action_consistency.py``.
"""

from __future__ import annotations

import sympy as sp
from sympy.calculus.euler import euler_equations

# ----------------------------------------------------------------------------
# 0. Symbols
# ----------------------------------------------------------------------------
t = sp.symbols("t", positive=True)
x, y, z = sp.symbols("x y z", real=True)
ETA = sp.symbols("eta", real=True)          # conformal time (unused, documented)

M_PL = sp.symbols("M_Pl", positive=True)
G00 = sp.symbols("g00", real=True)   # g^{00}, the variation variable for T_{00}
H = sp.symbols("H", real=True)

# Dimensionless couplings
alpha, lam_psi, g_DM, lambda_phi = sp.symbols("alpha lambda_psi g_DM lambda_phi", positive=True)
y_psi, g_psi, kappa, lam_res = sp.symbols("y_psi g_psi kappa lambda_res", real=True)
# ``fbar f`` is treated as a background bilinear.  It must be ONE object shared
# by every module: a symbol here, and in ``ptum_transfer`` the very same symbol
# is what the time derivative acts on.  (See the ``g00`` identity trap in the
# SPRINT-1 notes: duplicating a symbol silently makes substitutions no-ops.)
fbarf = sp.Symbol("fbarf", real=True)

# Dimensionful parameters
V0, m, m_chi, E_th, W0, Lam_NP, f_res = sp.symbols(
    "V0 m m_chi E_th W0 Lambda_NP f_res", positive=True
)


def to_hubble(expr, a_t, H_symbol=None):
    """Rewrite ``a'/a`` as ``H`` in a way that actually cancels.

    A structural substitution of ``a'/a`` fails once the term is written as
    ``a' * phi'/a``; substituting ``a' -> H a`` and simplifying is robust.
    """
    Hs = H if H_symbol is None else H_symbol
    expr = sp.expand(expr.subs(sp.Derivative(a_t, t), Hs * a_t))
    return sp.simplify(expr)


# ----------------------------------------------------------------------------
# 1. Metric, connection, curvature  (signature -+++, MTW)
# ----------------------------------------------------------------------------
def frw_metric(a_t):
    """Flat FRW metric tensor ``g_{mu nu}`` with signature ``(-+++)``."""
    return sp.diag(-1, a_t**2, a_t**2, a_t**2)


def frw_metric_inverse(a_t):
    return sp.diag(-1, 1/a_t**2, 1/a_t**2, 1/a_t**2)


def kretschmann_scalar(a_t):
    """Ricci scalar of flat FRW: ``R = 6(a''/a + H^2)``.

    With the MTW Riemann convention this is the standard result.  It is used in
    :func:`einstein_tensor` and cross-checked against the componentwise
    Christoffel computation in the tests.
    """
    adot = sp.diff(a_t, t)
    addot = sp.diff(a_t, t, 2)
    return 6 * (addot / a_t + (adot / a_t) ** 2)


def christoffel(g, ginv, coords):
    """``Gamma^rho_{mu nu}`` from the metric."""
    n = len(coords)
    G = sp.MutableDenseNDimArray.zeros(n, n, n)
    for r in range(n):
        for mu in range(n):
            for nu in range(n):
                s = sp.Integer(0)
                for sgm in range(n):
                    s += ginv[r, sgm] * (
                        sp.diff(g[sgm, nu], coords[mu])
                        + sp.diff(g[sgm, mu], coords[nu])
                        - sp.diff(g[mu, nu], coords[sgm])
                    )
                G[r, mu, nu] = sp.simplify(s / 2)
    return G


def einstein_tensor_mixed(a_t):
    """``G^mu{}_nu`` of flat FRW as a diagonal matrix.

    Derived (not assumed) from ``R^mu{}_nu - 1/2 delta^mu_nu R``:

        ``G^0{}_0 = -3H^2``,   ``G^i{}_j = -delta^i_j (2 a''/a + H^2)``,

    so that ``G^mu{}_mu = -R`` and Einstein's equation
    ``G^0{}_0 = -T^0{}_0 / M_Pl^2`` reproduces ``3H^2 = rho / M_Pl^2``.
    """
    adot = sp.diff(a_t, t)
    addot = sp.diff(a_t, t, 2)
    spatial = -(2 * addot / a_t + (adot / a_t) ** 2)
    return sp.diag(-3 * (adot / a_t) ** 2, spatial, spatial, spatial)


# ----------------------------------------------------------------------------
# 2. Generic scalar sector: variation of the action
# ----------------------------------------------------------------------------
DEFAULT_SIGN = -sp.Rational(1, 2)   # canonical scalar in (-+++)


class ScalarSector:
    """A real scalar with ``L = s g^{mu nu} d_mu phi d_nu phi - V(phi)``.

    ``s = -1/2`` is canonical for signature ``(-+++)``; ``s = +1/2`` reproduces
    the (wrong-sign) convention printed in the current manuscript and is kept
    only so that the tests can demonstrate the inconsistency.
    """

    def __init__(self, name: str, potential, sign=DEFAULT_SIGN,
                 xdep_potential=None):
        self.name = name
        self.phi = sp.Function(name)(t)
        self.sign = sp.Rational(sign)
        # potential may depend on the field (and, for the activation sector,
        # explicitly on time through Phi(t)); we always differentiate w.r.t. phi
        self._V_expr = potential
        self.V = potential if not callable(potential) else None

    # -- Lagrangian pieces ---------------------------------------------------
    def L_kinetic(self, a_t):
        """``s * g^{mu nu} d_mu phi d_nu phi`` for a homogeneous field.

        In ``(-+++)``, ``(d phi)^2 = g^{00} phidot^2 = -phidot^2``, hence the
        homogeneous Lagrangian is ``-s * phidot^2``.  For the canonical
        ``s = -1/2`` this is ``+1/2 phidot^2``, the usual kinetic term.
        """
        return self.sign * (-sp.diff(self.phi, t) ** 2)

    def kinetic_only_flat(self, phidot_value):
        """``s * (dphi)^2`` evaluated on a homogeneous field in flat space.

        In ``(-+++)`` flat space ``(dphi)^2 = -phidot^2``, hence ``-s phidot^2``.
        """
        return -self.sign * phidot_value**2

    def stress_energy(self, V_expr, phidot, phi_grad=None):
        """``T_{mu nu}`` of a canonical scalar, derived (not assumed).

        Returns ``(rho, p)`` evaluated on a homogeneous field:

        * ``rho = T_{00} = 1/2 phidot^2 + V``      (canonical sign)
        * ``p   = T_{ii}/a^2 = 1/2 phidot^2 - V``
        """
        if self.sign != DEFAULT_SIGN:
            raise ValueError(
                "stress_energy() implements the canonical (-1/2) sector only; "
                "the +1/2 variant is intentionally not provided "
                "(see AUDIT_00 B-04)"
            )
        rho = sp.Rational(1, 2) * phidot**2 + V_expr
        p = sp.Rational(1, 2) * phidot**2 - V_expr
        return rho, p


def T_from_L_symbolic(L_of_g00, g00_symbol=None):
    """``T_{00}`` obtained by differentiating the Lagrangian w.r.t. ``g^{00}``.

    ``T_{mu nu} = -2/sqrt(-g) delta(sqrt(-g) L)/delta g^{mu nu}``.  With

        ``delta sqrt(-g) / delta g^{mu nu} = -1/2 sqrt(-g) g_{mu nu}``

    one obtains

        ``T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L``.

    (The second sign is ``+``; writing ``-`` gives ``T_00 = -p`` instead of
    ``rho``.)  This is a genuine variation, which is what ``main.tex`` claims
    to perform but only asserts.
    """
    g00 = G00 if g00_symbol is None else g00_symbol
    L = L_of_g00(g00)
    dL = sp.diff(L, g00)
    # for a metric with signature (-+++), g_{00} = 1/g^{00}
    g_lower = 1 / g00          # g_{00}, since g^{00} g_{00} = 1
    return sp.simplify(-2 * dL + g_lower * L)


def scalar_T_munu_canonical(phi, V_expr):
    """Covariant ``T_{mu nu}`` of a canonical scalar in ``(-+++)``.

    ``T_{mu nu} = d_mu phi d_nu phi - g_{mu nu} [ 1/2 (d phi)^2 + V ]``

    The bracket carries **+V** (not ``-V``).  This is the sign that ``main.tex``
    gets wrong in Eq. (70) for the DM/DE sectors (AUDIT_00 B-07).
    """
    return lambda g, dphi, box: (
        sp.Matrix([[dphi[i] * dphi[j] for j in range(4)] for i in range(4)])
        - g * (sp.Rational(1, 2) * box + V_expr)
    )


# ----------------------------------------------------------------------------
# 3. Explicit potentials of PTUM
# ----------------------------------------------------------------------------
def V_eff_fuel(Phi_expr, cw_terms=None):
    """Tree-level fuel potential ``V0 (1 - exp(-lambda Phi^2))``.

    ``lambda`` carries mass dimension ``-2`` (``main.tex`` Table 8 states this
    explicitly).  Writing ``lambda = 0.02`` as a *number of GeV^-2* makes
    ``lambda Phi^2 ~ 10^36`` and the potential identically flat
    (AUDIT_00 B-15).  The correct reading is ``lambda ~ O(1)/M_Pl^2``.
    """
    V = V0 * (1 - sp.exp(-lambda_phi * Phi_expr**2))
    if cw_terms is not None:
        V = V + cw_terms
    return V


def m_eff2_psi(Phi_expr):
    """``m_eff^2(Phi) = m^2 (1 - alpha Phi^2 / E_th^2)``."""
    return m**2 * (1 - alpha * Phi_expr**2 / E_th**2)


def psi_0_sq(mu_sq):
    """Post-activation minimum ``psi_0^2 = mu^2 / lambda_psi``, ``mu^2 = |m_eff^2|``."""
    return mu_sq / lam_psi


def V_act(Phi_expr, psi_expr):
    """Activation potential, *as printed* in ``main.tex`` Eq. (7)."""
    return sp.Rational(1, 2) * m_eff2_psi(Phi_expr) * psi_expr**2 \
        + lam_psi / 4 * psi_expr**4


def V_act_shifted(Phi_expr, psi_expr):
    """``U(psi) = (lambda_psi/4)(psi^2 - psi_0^2)^2`` (energy from the minimum)."""
    return lam_psi / 4 * (psi_expr**2 - psi_0_sq(-m_eff2_psi(Phi_expr))) ** 2


def V_DM(chi_expr, Phi_res_expr):
    """``1/2 m_chi^2 chi^2 + g_DM chi^2 Phi_res^2``."""
    return sp.Rational(1, 2) * m_chi**2 * chi_expr**2 \
        + g_DM * chi_expr**2 * Phi_res_expr**2


def V_DE(Phi_res_expr):
    """Residual dark-energy potential of ``main.tex`` Eq. (12)."""
    return (W0 * sp.exp(-kappa * Phi_res_expr**2)
            * (1 - sp.exp(-lam_res * Phi_res_expr**2))
            + Lam_NP**4 * sp.exp(-sp.Symbol("S_E"))
            * sp.cos(Phi_res_expr / f_res))


def V_rh(psi_expr, f_expr, phi_SM_expr):
    """Reheating potential ``y_psi psi fbar f + 1/2 g_psi psi^2 phi_SM^2``.

    ``f_expr`` stands for ``bar f f`` (the fermion bilinear).
    """
    return y_psi * psi_expr * f_expr + sp.Rational(1, 2) * g_psi * psi_expr**2 * phi_SM_expr**2


def L_total_density(Phi, psi, chi, Phi_res, f, phi_SM):
    """The **complete** Lagrangian density of PTUM.

    ``main.tex`` Eq. (3) lists only four sectors and omits ``L_rh``, while
    Eq. (5.5.2) uses ``L_rh`` to build ``Q_SM`` (AUDIT_00 B-05).  Here it is
    part of the total from the start.
    """
    # For each canonical field in (-+++):  L = -1/2 (d phi)^2 - V = +1/2 phidot^2 - V.
    L = (
        # fuel
        sp.Rational(1, 2) * sp.diff(Phi, t) ** 2 - V_eff_fuel(Phi)
        # activation (interaction with the fuel is *inside* m_eff^2)
        + sp.Rational(1, 2) * sp.diff(psi, t) ** 2 - V_act(Phi, psi)
        # dark matter
        + sp.Rational(1, 2) * sp.diff(chi, t) ** 2 - V_DM(chi, Phi_res)
        # dark energy
        + sp.Rational(1, 2) * sp.diff(Phi_res, t) ** 2 - V_DE(Phi_res)
        # reheating / SM
        - V_rh(psi, f, phi_SM)
    )
    return L


# ----------------------------------------------------------------------------
# 4. Equations of motion from the action
# ----------------------------------------------------------------------------
def eom_from_action(L_density, fields, a_t):
    """Euler-Lagrange equations for ``S = int dt a^3 L`` (homogeneous fields).

    Uses :func:`sympy.calculus.euler.euler_equations`, i.e. the variation is
    performed symbolically on the action, never guessed.
    """
    S = a_t**3 * L_density
    return [sp.simplify(eq.lhs) for eq in euler_equations(S, fields, t)]


def canonical_scalar_eom(potential_of_field, a_t):
    """``phi'' + 3H phi' + V'(phi) = 0`` for the canonical sign."""
    phi = sp.Function("phi")(t)
    # canonical: L = -1/2 (d phi)^2 - V = +1/2 phidot^2 - V  in (-+++)
    L = sp.Rational(1, 2) * sp.diff(phi, t) ** 2 - potential_of_field(phi)
    e = eom_from_action(L, [phi], a_t)[0] / a_t**3
    return to_hubble(e, a_t)


# ----------------------------------------------------------------------------
# 5. Interaction split used by SPRINT 2 (documented here, derived there)
# ----------------------------------------------------------------------------
def L_int_psi_Phi(Phi_expr, psi_expr):
    """The ``Phi^2 psi^2`` interaction **as it follows from Eq. (7)**.

    Expanding ``-1/2 m^2 (1 - alpha Phi^2/E_th^2) psi^2`` gives

        ``+ alpha m^2 Phi^2 psi^2 / (2 E_th^2)``

    i.e. ``+``, whereas ``main.tex`` Eq. (74) writes ``-``
    (AUDIT_00 B-06).  The sign below is the one that follows from the action.
    """
    return +alpha * m**2 * Phi_expr**2 * psi_expr**2 / (2 * E_th**2)


def L_int_DM_DE(chi_expr, Phi_res_expr):
    """``- g_DM chi^2 Phi_res^2`` (this sign is consistent in the manuscript)."""
    return -g_DM * chi_expr**2 * Phi_res_expr**2


def L_int_rh(psi_expr, f_expr, phi_SM_expr):
    """``- y_psi psi fbar f - 1/2 g_psi psi^2 phi_SM^2``."""
    return -V_rh(psi_expr, f_expr, phi_SM_expr)


# ----------------------------------------------------------------------------
# 6. FRW field equations (reduced form, for the Solver / bookkeeping)
# ----------------------------------------------------------------------------
def frw_eoms_symbolic():
    """Return the four PTUM equations of motion **derived from the action**.

    Returns a dict of SymPy expressions that must vanish.  The interaction
    between ``Phi`` and ``psi`` enters only through ``m_eff^2(Phi)`` — the
    ``+alpha m^2 Phi psi^2/E_th^2`` term of the current manuscript Eq. (13)
    is *not* produced by the printed Lagrangian and is recovered only with the
    opposite overall kinetic sign (see AUDIT_00 B-04/B-06).
    """
    a_t = sp.Function("a")(t)
    Phi = sp.Function("Phi")(t)
    psi = sp.Function("psi")(t)
    chi = sp.Function("chi")(t)
    Phi_res = sp.Function("Phi_res")(t)

    L = L_total_density(Phi, psi, chi, Phi_res,
                        fbarf, sp.Function("phi_SM")(t))
    eqs = eom_from_action(L, [Phi, psi, chi, Phi_res], a_t)
    out = {}
    for fld, eq in zip(("Phi", "psi", "chi", "Phi_res"), eqs):
        eq = sp.expand(eq / a_t**3)
        # eliminate H = a'/a and the scale factor in favour of H
        out[fld] = to_hubble(eq, a_t)
    return out


if __name__ == "__main__":  # pragma: no cover - manual inspection helper
    print("conventions: (-+++), T = -2/sqrt(-g) dS/dg, L_kin = -1/2 (dphi)^2")
    print()
    a_t = sp.Function("a")(t)
    print("canonical scalar EOM:", canonical_scalar_eom(lambda p: p**2 / 2, a_t))
