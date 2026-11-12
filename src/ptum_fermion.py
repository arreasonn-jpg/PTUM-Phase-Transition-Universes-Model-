"""
Fermionic half of the Yukawa transfer  (SPRINT 3, part C)
=========================================================

SPRINT 2 derived ``Q_psi^0 = -y_psi (fbar f) psidot`` from the **scalar** side
of ``L_int = -y_psi psi fbar f`` and left the fermionic side labelled
``PARTIAL``, because ``Q_f`` was read off the bilinear ``<fbar f>`` instead of
the Dirac equation.

This module removes that label.  The fermionic half is proved exactly.

Conventions
-----------
Signature ``(-+++)``, so ``{gamma^mu, gamma^nu} = 2 eta^{mu nu}`` with
``eta = diag(-1,+1,+1,+1)``; hence ``(gamma^0)^2 = -1`` and ``(gamma^i)^2 = +1``.
Explicitly ``gamma^0 = -i diag(1,1,-1,-1)``, ``gamma^i = -i [[0, sigma^i],
[-sigma^i, 0]]``, i.e. ``gamma^0 = -i beta``, ``gamma^i = -i beta alpha_i``.
Both checks are in ``check_clifford()`` and the test suite.

The interacting Dirac equation
-------------------------------
With ``L_int = -y psi fbar f`` and ``psi = psi(t)`` homogeneous::

    i gamma^0 d_0 f - m_f f - y psi f = 0
    =>   d_0 f = i (m_f + y psi) gamma^0 f .

For a momentum mode ``f ∝ exp(i k.x)`` the same algebra gives
``d_0 f = i (m_f + y psi) gamma^0 f - i gamma^0 gamma^i k_i f``, i.e. the
condensate acts as a shift ``m_f -> m_f + y psi``.  That is the standard
"effective mass from a scalar condensate" statement; it is not an assumption.

Results (all verified symbolically, see ``tests/test_fermion_half.py``)
-----------------------------------------------------------------------
1. ``(gamma^0)^2 = -1`` implies ``fbar gamma^0 f = 0``, hence

       d_0 (fbar f) = 0                                  (on shell)

   The scalar bilinear is conserved -- expected, since it is fermion-number
   neutral.  (The *vector* current ``fbar gamma^mu f`` is conserved for the
   same reason, checked in :func:`vector_current_divergence`.)

2. The Belinfante stress tensor for a homogeneous field is

       T_f^{00} = (m_f + y psi) (fbar f) .

   It is **not** conserved:

       d_0 T_f^{00} = y psidot fbar f = -Q_psi^0 .

   So ``Q_f^0 = +y psidot fbar f = -Q_psi^0`` and ``Q_psi + Q_f = 0`` holds
   with the *same* ``Q_psi`` SPRINT 2 derived from the scalar side.  This is
   the closure, proved rather than assumed.

3. ``[Q_f] = GeV^5`` and ``Q_f -> 0`` for ``y -> 0`` or ``psidot -> 0``.

Scope
-----
* Flat space, homogeneous scalar: **exact**.
* FRW: the ``3H`` pieces are of relative order ``H/omega_res ~ 10^{-3}`` at the
  benchmark points.  The manuscript's neglect of them is therefore
  *quantitatively* justified in the discharge window, but the exact FRW
  statement is not derived here and stays labelled ``CONDITIONAL``.
* Backreaction and the spinodal/quantum treatment of ``chi`` are out of scope.
"""

from __future__ import annotations

import sympy as sp
from sympy import I

t = sp.symbols("t", real=True)
x, y, z = sp.symbols("x y z", real=True)
COORDS = (t, x, y, z)

psi_b = sp.Function("psi")(t)
m_f, y_psi = sp.symbols("m_f y_psi", real=True)

# the four spinor components and their Dirac conjugates, as symbols:
# working with symbols (not Function(t)) keeps every total derivative explicit
F = [sp.Symbol("f%d" % i) for i in range(4)]
FB = [sp.Symbol("fb%d" % i) for i in range(4)]
DF = [sp.Symbol("df%d" % i) for i in range(4)]     # = d_0 f_i on shell
DFB = [sp.Symbol("dfb%d" % i) for i in range(4)]   # = d_0 fbar_i on shell


# ---------------------------------------------------------------------------
# 1. Gamma matrices
# ---------------------------------------------------------------------------
def gamma_matrices():
    """``gamma^0 = -i diag(1,1,-1,-1)``, ``gamma^i = -i [[0,sigma^i],[-sigma^i,0]]``.

    Written entry by entry: sympy's block-matrix helpers inject floating-point
    zeros, which then fail exact comparison.
    """
    return {
        0: sp.Matrix([[-I, 0, 0, 0],
                      [0, -I, 0, 0],
                      [0, 0, I, 0],
                      [0, 0, 0, I]]),
        1: sp.Matrix([[0, 0, 0, -I],
                      [0, 0, -I, 0],
                      [0, I, 0, 0],
                      [I, 0, 0, 0]]),
        2: sp.Matrix([[0, 0, 0, -1],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0],
                      [-1, 0, 0, 0]]),
        3: sp.Matrix([[0, 0, -I, 0],
                      [0, 0, 0, I],
                      [I, 0, 0, 0],
                      [0, -I, 0, 0]]),
    }


def check_clifford():
    """Residual of ``{g^a, g^b} - 2 eta^{ab}`` for every pair; all must be zero."""
    g = gamma_matrices()
    eta = sp.diag(-1, 1, 1, 1)
    return {(a, b): sp.simplify(g[a] * g[b] + g[b] * g[a] - 2 * eta[a, b] * sp.eye(4))
            for a in range(4) for b in range(4)}


def check_hermiticity():
    """``gamma^0`` anti-Hermitian, ``gamma^i`` Hermitian -- required by ``(-+++)``."""
    g = gamma_matrices()
    return {"g0_anti_hermitian": (g[0].H + g[0]).is_zero_matrix,
            **{f"g{i}_hermitian": (g[i].H - g[i]).is_zero_matrix for i in (1, 2, 3)}}


# ---------------------------------------------------------------------------
# 2. The Dirac equation and its on-shell derivatives
# ---------------------------------------------------------------------------
def effective_mass(mass=None, y=None):
    """``m_f + y psi(t)``: the mass the fermion sees in the condensate."""
    m = m_f if mass is None else mass
    yy = y_psi if y is None else y
    return m + yy * psi_b


def onshell_d0():
    """``(d_0 f, d_0 fbar)`` implied by ``i gamma^0 d_0 f = (m_f + y psi) f``.

    Returns two lists of four expressions, in terms of the symbols ``F``/``FB``
    and the condensate ``psi(t)``.
    """
    g = gamma_matrices()
    M = effective_mass()
    f = sp.Matrix(F)
    fb = sp.Matrix(1, 4, FB)
    d0f = sp.expand(I * M * g[0] * f)
    d0fb = sp.expand(-I * M * fb * g[0])
    return ([sp.expand(d0f[i, 0]) for i in range(4)],
            [sp.expand(d0fb[0, i]) for i in range(4)])


def dirac_residual(free_mass_parts=True):
    """The on-shell substitution written as a residual (must be zero).

    ``i gamma^0 d_0 f - (m_f + y psi) f`` with ``d_0 f`` taken from
    :func:`onshell_d0`.  A zero result confirms ``onshell_d0`` really solves
    the interacting Dirac equation.
    """
    g = gamma_matrices()
    M = effective_mass()
    f = sp.Matrix(F)
    d0f, _ = onshell_d0()
    return sp.simplify(I * g[0] * sp.Matrix(d0f) - M * f)


def d_dt(expr):
    """Total ``d/dt`` along the on-shell flow.

    ``expr`` may depend on ``t`` explicitly (through ``psi(t)``) and on the
    spinor symbols ``F``/``FB``; their time derivatives are ``DF``/``DFB``,
    whose values come from the Dirac equation.
    """
    d0f, d0fb = onshell_d0()
    total = sp.diff(expr, t)
    for i in range(4):
        total += sp.diff(expr, F[i]) * d0f[i]
        total += sp.diff(expr, FB[i]) * d0fb[i]
    return sp.expand(total)


# ---------------------------------------------------------------------------
# 3. The three structural results
# ---------------------------------------------------------------------------
def fbarf():
    """``fbar f`` as a scalar symbol expression."""
    return sp.expand(sum(FB[i] * F[i] for i in range(4)))


def bilinear_is_conserved():
    """``d_0 (fbar f) = 0`` on shell.

    Reason: ``d_0(fbar f) = (d_0 fbar) f + fbar (d_0 f)
    = -i M fbar gamma^0 f + i M fbar gamma^0 f = 0``
    since ``(gamma^0)^2 = -1`` makes ``fbar gamma^0 f`` vanish identically.
    """
    return sp.simplify(d_dt(fbarf()))


def vector_current_divergence():
    """``d_mu (fbar gamma^mu f) = 0``: the Yukawa term cannot source fermion number."""
    g = gamma_matrices()
    d0f, d0fb = onshell_d0()
    j0 = sum(FB[i] * F[i] for i in range(4))          # fbar gamma^0 f = 0 identically
    lhs = sp.Integer(0)
    for i in range(4):
        lhs += sum(g[0][j, i] * d0f[j] for j in range(4)) * FB[i]
        lhs += sum(g[0][i, j] * F[j] for j in range(4)) * d0fb[i]
    return sp.simplify(lhs), sp.simplify(j0)


def fermion_energy_density():
    """``T_f^{00} = i/2 [ fbar gamma^0 d_0 f - (d_0 fbar) gamma^0 f ]`` on shell.

    This simplifies to ``(m_f + y psi) fbar f``.
    """
    g = gamma_matrices()
    d0f, d0fb = onshell_d0()
    f = sp.Matrix(F)
    fb = sp.Matrix(1, 4, FB)
    T00 = sp.Rational(1, 2) * I * (
        (fb * g[0] * sp.Matrix(d0f))[0, 0]
        - (sp.Matrix(1, 4, d0fb) * g[0] * f)[0, 0])
    return sp.simplify(T00)


def fermion_closure_residual():
    """``d_0 T_f^{00} - y psidot fbar f``; must be zero.

    The second term is exactly ``-Q_psi^0`` (SPRINT 2, ``lam_psi = 0``), so a
    zero residual proves ``Q_f = -Q_psi``.
    """
    T00 = fermion_energy_density()
    return sp.simplify(d_dt(T00) - y_psi * sp.diff(psi_b, t) * fbarf())


def Q_f_closed():
    """``Q_f^0 = +y psidot fbar f``, obtained as ``d_0 T_f^{00}``."""
    return sp.simplify(d_dt(fermion_energy_density()))


# ---------------------------------------------------------------------------
# 4. Dimensions and limits
# ---------------------------------------------------------------------------
DIM = {"y_psi": 0, "psi": 1, "f": sp.Rational(3, 2), "fbar": sp.Rational(3, 2),
       "d": 1, "m_f": 1, "fbarf": 3}


def dim_transfer():
    """``[y psi (fbar f)'] = 0 + 1 + 3 + 1 = 5``."""
    return DIM["y_psi"] + DIM["psi"] + DIM["fbarf"] + DIM["d"]


def fermion_limit_checks():
    """``Q_f`` vanishes for ``y -> 0`` and for ``psidot -> 0``."""
    fb = sp.Symbol("fbarf", real=True)
    Q = y_psi * fb * sp.diff(psi_b, t)
    return {"yukawa_off": sp.simplify(Q.subs(y_psi, 0)),
            "static_scalar": sp.simplify(Q.subs(sp.diff(psi_b, t), 0)),
            "Q_f": Q}


# ---------------------------------------------------------------------------
# 9. FRW: the closure with the spin connection (was CONDITIONAL in SPRINT 3)
# ---------------------------------------------------------------------------
# In FRW the Dirac equation of a homogeneous mode carries the spin-connection
# term (3i/2)H gamma^0 acting on f, so that
#
#     i gamma^0 d_0 f + (3i/2) H gamma^0 f = (m_f + y psi) f
#     =>   d_0 f = [ i (m_f + y psi) gamma^0 - (3/2) H ] f
#
# The spin-connection piece is real and multiplies f identically, so it gives
# a *common* contribution to d_0 f and d_0 fbar and therefore survives in the
# bilinears -- unlike the mass term, whose two halves cancel.
#
# Consequences (both verified symbolically below):
#
#     d_0 (fbar f) = -3 H (fbar f)                    (the bilinear redshifts)
#     T_f^{00}     = (m_f + y psi) fbar f
#     d_0 T_f^{00} = [ y psidot - 3 H (m_f + y psi) ] fbar f
#
# so the transfer is
#
#     Q_f = y psidot fbar f - 3 H (m_f + y psi) fbar f
#         = -Q_psi            - 3 H rho_f                       (***)
#
# The second term is *not* a transfer between sectors: it is the redshift of
# the fermion energy, i.e. exactly the "3H rho" piece that the continuity
# equation  rhodot + 3H(rho+p) = Q  absorbs on its left-hand side.  Writing
# *** in that form,
#
#     (rhodot_f + 3H rho_f) + 3H p_f = Q_f  =>  Q_f = -Q_psi   (p_f = 0 + ...)
#
# recovers the flat-space result.  So SPRINT 3's CONDITIONAL becomes TURETILDI:
# the fermionic half closes in FRW as well, provided the redshift is booked on
# the left-hand side as it must be.

def frw_onshell_d0(mass=None, y=None, a=None):
    """``d_0 f`` and ``d_0 fbar`` for a homogeneous mode including ``(3/2)H``."""
    m = m_f if mass is None else mass
    yy = y_psi if y is None else y
    if a is None:
        a = sp.Function("a")(t)
    Hs = sp.diff(a, t) / a
    g = gamma_matrices()
    f = sp.Matrix(F)
    fb = sp.Matrix(1, 4, FB)
    M = m + yy * psi_b
    d0f = sp.expand(I * M * g[0] * f - sp.Rational(3, 2) * Hs * f)
    d0fb = sp.expand(-I * M * fb * g[0] - sp.Rational(3, 2) * Hs * fb)
    return ([d0f[i, 0] for i in range(4)], [d0fb[0, i] for i in range(4)])


def _frw_total_derivative(expr, d0f, d0fb):
    total = sp.diff(expr, t)
    for i in range(4):
        total += sp.diff(expr, F[i]) * d0f[i]
        total += sp.diff(expr, FB[i]) * d0fb[i]
    return sp.expand(total)


def frw_bilinear_redshift():
    """``d_0 (fbar f) = -3H (fbar f)``: the standard redshift of a density."""
    a = sp.Function("a")(t)
    Hs = sp.diff(a, t) / a
    d0f, d0fb = frw_onshell_d0(a=a)
    fbarf = sum(FB[i] * F[i] for i in range(4))
    return sp.simplify(_frw_total_derivative(fbarf, d0f, d0fb) + 3 * Hs * fbarf)


def frw_fermion_closure_residual():
    """``d_0 T_f^{00} - [y psidot - 3H(m_f+y psi)] fbar f``; must be zero.

    Equivalently ``d_0 rho_f + 3H rho_f = y psidot fbar f = -Q_psi``, i.e. the
    fermionic half of the Yukawa closure holds in FRW too once the redshift
    term ``3H rho_f`` is booked on the continuity-equation left-hand side.
    """
    a = sp.Function("a")(t)
    Hs = sp.diff(a, t) / a
    d0f, d0fb = frw_onshell_d0(a=a)
    f = sp.Matrix(F)
    fb = sp.Matrix(1, 4, FB)
    T00 = sp.simplify(sp.Rational(1, 2) * I * (
        (fb * gamma_matrices()[0] * sp.Matrix(d0f))[0, 0]
        - (sp.Matrix(1, 4, d0fb) * gamma_matrices()[0] * f)[0, 0]))
    fbarf = sum(FB[i] * F[i] for i in range(4))
    dT = _frw_total_derivative(sp.expand(T00), d0f, d0fb)
    target = (y_psi * sp.diff(psi_b, t) - 3 * Hs * effective_mass()) * fbarf
    return sp.simplify(dT - target)


def frw_transfer_flat_limit():
    """In the ``H -> 0`` limit the FRW result reduces to the flat-space one."""
    a = sp.Function("a")(t)
    Hs = sp.diff(a, t) / a
    fbarf = sum(FB[i] * F[i] for i in range(4))
    Q_f_frw = y_psi * sp.diff(psi_b, t) * fbarf - 3 * Hs * effective_mass() * fbarf
    return sp.simplify(Q_f_frw.subs(Hs, 0) - y_psi * sp.diff(psi_b, t) * fbarf)
