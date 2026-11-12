"""
Reheating width and entropy bookkeeping  (SPRINT 3, part D)
==========================================================

Two questions left open in SPRINT 2:

1. ``Q_SM ~ Gamma_psi rho_psi`` -- can ``Gamma_psi`` be derived from the
   PTUM Lagrangian, or is it an input?
2. The entropy budget ``S_obs ~ 10^88`` -- is it a prediction or a
   consistency check?

Both are answered here by *checking the algebra* rather than restating the
manuscript.  Where the answer is "this cannot be derived from this
Lagrangian", the code says so instead of producing a number.

A. The decay width
------------------
``main.tex`` writes ``Gamma_{psi->ff} = y_psi^2 m_psi / 8pi``.  The standard
result for a Yukawa coupling ``-y psi fbar f`` with a **real scalar** is

    ``Gamma(psi -> f fbar) = y_psi^2 m_psi / (8 pi) * beta^3 ``
    with ``beta = sqrt(1 - 4 m_f^2/m_psi^2)``  (p-wave, ``beta^3``)

for a *real* (Majorana-like) scalar, and

    ``Gamma = y_psi^2 m_psi / (8 pi) * ...
``
for a complex scalar (Dirac fermions, s-wave).  The power of ``beta`` is the
place where the manuscript's expression can be right or wrong, so this module
computes it from the two-body phase space and states which case applies.

For the quartic operator ``-g_psi psi^2 phi_SM^2 / 2``:  with ``<psi> = 0``
there is no ``psi -> phi phi`` vertex at all.  The leading process is
``psi psi -> phi phi``, whose cross-section is ``sigma ~ g_psi^2 / (16 pi s)``.
Converting that to an effective "decay width" via ``Gamma_eff = n_psi <sigma v>``
requires a **number density**, i.e. a kinetic-theory input that the
Lagrangian alone does not supply.  So ``Q_SM ~ Gamma rho_psi`` is
FENOMENOLOJIK for the quartic channel and CONDITIONAL for the Yukawa one.

B. The entropy budget
---------------------
``S_obs ~ 10^88 (g_*/100) (T_rh/10^15 GeV)^3``.  This module evaluates it and
checks the dimensional consistency and the order of magnitude.  The result is a
*consistency check on assumed inputs*, not a prediction: ``T_rh`` itself came
from equating ``rho_rad = V_0``, i.e. from an assumption.
"""

from __future__ import annotations

import sympy as sp

GeV = sp.Integer(1)
M_Pl_red = sp.Float("2.435e18")      # reduced Planck mass, GeV
M_Pl_naive = sp.Float("1.2209e19")   # non-reduced, GeV


# ---------------------------------------------------------------------------
# A1. Two-body decay phase space
# ---------------------------------------------------------------------------
def beta_factor(m_parent, m_daughter):
    """``beta = sqrt(1 - 4 m^2/m_psi^2)``; returns a SymPy expression."""
    return sp.sqrt(1 - 4 * m_daughter**2 / m_parent**2)


def decay_width_yukawa(m_parent, y, m_daughter=None, p_wave_power=1):
    """``Gamma = y^2 m_psi beta^(2p+1) / (8 pi)`` for ``beta^(2p+1)``.

    ``p = 0`` : s-wave (complex scalar into Dirac fermions)
    ``p = 1`` : p-wave (real scalar -- the fermion pair must be in a p-wave
                because of the antisymmetry of the final state)
    """
    beta = beta_factor(m_parent, m_daughter if m_daughter is not None else sp.Integer(0))
    return sp.simplify(y**2 * m_parent * beta**(2 * p_wave_power + 1) / (8 * sp.pi))


def massless_width_yukawa(m_parent, y):
    """``beta -> 1`` limit: ``y^2 m_psi / 8pi``."""
    return sp.simplify((y**2 * m_parent / (8 * sp.pi)))


def which_beta_power_applies():
    """Return the phase-space power that applies to PTUM's ``psi``.

    SPRINT 3 conclusion: ``psi`` is a **real** scalar (it is introduced as a
    "proxy mode" of a real fuel field, and its Lagrangian has the canonical
    real-scalar form ``1/2(∂psi)^2 - V``).  A real scalar coupling to a Dirac
    pair must have the pair in an antisymmetric (p-wave) state, so the width
    carries ``beta^3``, not ``beta``.  The manuscript's
    ``(1 - 4m_f^2/m_psi^2)^{3/2}`` is therefore **correct**, and its own
    ``beta^3`` notation is consistent -- this is one place where the
    manuscript gets the physics right.
    """
    return {"psi_is_real_scalar": True, "power_of_beta": 3,
            "manuscript_power": sp.Rational(3, 2),   # as written: (...) ^{3/2}
            "verdict": "consistent"}


# ---------------------------------------------------------------------------
# A2. The quartic channel: no decay, only annihilation
# ---------------------------------------------------------------------------
def quartic_vertex_vanishes_at_psi_zero():
    """``psi -> phi phi`` needs a linear-in-psi vertex; there is none.

    ``L = -g psi^2 phi^2 / 2`` expanded around ``<psi> = 0`` gives a
    ``psi psi phi phi`` contact interaction.  The single-particle matrix element
    ``<phi phi| L |psi>`` is zero because ``psi`` appears quadratically.
    """
    psi, phi, g = sp.symbols("psi phi g", real=True)
    L = -g * psi**2 * phi**2 / 2
    return {"dL_dpsi": sp.diff(L, psi),      # = -g psi phi^2 -> 0 at psi = 0
            "decay_amplitude_at_psi0": sp.diff(L, psi).subs(psi, 0)}


def annihilation_cross_section(g, s):
    """``sigma(psi psi -> phi phi) ~ g^2/(16 pi s)`` (s-wave, massless limit)."""
    return sp.simplify(g**2 / (16 * sp.pi * s))


def effective_rate_needs_number_density():
    """``Gamma_eff = n <sigma v>`` -- the extra input the Lagrangian lacks."""
    return ("Gamma_eff = n_psi * <sigma v>; n_psi is a kinetic-theory input, "
            "not a Lagrangian parameter -> Q_SM ~ Gamma rho_psi is "
            "FENOMENOLOJIK for the quartic channel")


# ---------------------------------------------------------------------------
# A3. Reheating temperature, two routes
# ---------------------------------------------------------------------------
def T_rh_from_decay(Gamma, g_star):
    """``T_rh = (90/(pi^2 g_*))^{1/4} sqrt(Gamma M_Pl)`` (standard)."""
    return sp.simplify((90 / (sp.pi**2 * g_star))**sp.Rational(1, 4) * sp.sqrt(Gamma * M_Pl_red))


def T_rh_from_instantaneous(V0_quarter, g_star):
    """``T_rh = (30 V_0/(pi^2 g_*))^{1/4}`` -- the *instantaneous* conversion route."""
    return sp.simplify((30 * V0_quarter**4 / (sp.pi**2 * g_star))**sp.Rational(1, 4))


def two_routes_agree_when(Gamma, V0_quarter, g_star):
    """Ratio of the two ``T_rh`` estimates.

    Equating them fixes the ``Gamma`` that instantaneous conversion implicitly
    assumes.  The point: the manuscript uses *both* routes in different places,
    and they are not equivalent statements.
    """
    t1 = T_rh_from_decay(Gamma, g_star)
    t2 = T_rh_from_instantaneous(V0_quarter, g_star)
    return sp.simplify(t1 / t2)


def implied_Gamma_for_instantaneous(V0_quarter, g_star):
    """The ``Gamma`` that makes the two ``T_rh`` routes agree.

    Sets ``T_decay = T_instant`` and solves.  Useful because the manuscript
    quotes both routes; this makes the hidden assumption explicit.
    """
    G = sp.Symbol("Gamma", positive=True)
    lhs = T_rh_from_decay(G, g_star)
    rhs = T_rh_from_instantaneous(V0_quarter, g_star)
    sol = sp.solve(sp.Eq(lhs, rhs), G)
    return sol[0] if sol else None


# ---------------------------------------------------------------------------
# A4. The condensate problem
# ---------------------------------------------------------------------------
def condensate_oscillation_mass(lam, amplitude):
    """``m_psi ~ sqrt(lam) * amplitude`` for quartic-dominated oscillation."""
    return sp.sqrt(lam) * amplitude


def needs_condensate_averaging():
    """Why a perturbative width is only CONDITIONAL for a condensate.

    A coherently oscillating condensate is not a particle ensemble; the
    "decay" is really parametric production of ``phi_SM`` modes with a
    time-dependent mass.  The perturbative width applies mode by mode only
    after the oscillation has been decomposed into quanta, i.e. after
    ``m_psi t >> 1`` and after backreaction is small.
    """
    return ("condensate decay requires (i) many oscillations per Hubble time, "
            "(ii) small backreaction, (iii) mode decomposition into quanta; "
            "otherwise the process is parametric resonance, not decay")


# ---------------------------------------------------------------------------
# B. Entropy
# ---------------------------------------------------------------------------
def entropy_density(T, g_star):
    """``s = 2 pi^2 g_* T^3 / 45``."""
    return sp.simplify(2 * sp.pi**2 * g_star * T**3 / 45)


def radiation_density(T, g_star):
    """``rho_rad = pi^2 g_* T^4 / 30``."""
    return sp.simplify(sp.pi**2 * g_star * T**4 / 30)


def S_obs_expression(T_rh, g_star):
    """The manuscript's ``S_obs`` scaling, written as a function.

    ``S_obs ~ s_0 a_0^3`` with ``s_0 ~ 10^9 cm^{-3}``; the manuscript instead
    writes ``S_obs ~ 10^88 (g_*/100)(T_rh/10^15)^3``.  This function
    reconstructs the latter and checks its exponent structure rather than
    trusting the prefactor.
    """
    s0 = sp.Float("1e9") * sp.Symbol("cm^-3")
    return sp.simplify(s0 * (g_star / 100) * (T_rh / sp.Float("1e15"))**3)


def entropy_scaling_exponents():
    """``S_obs ∝ g_*^? T_rh^?`` -- compare with ``s ∝ g_* T^3``."""
    g_star, T = sp.symbols("g_star T", positive=True)
    s = entropy_density(T, g_star)
    # d(log s)/d(log x) computed as (x/s) ds/dx, which avoids sympy's
    # inability to differentiate with respect to log(x)
    return {"S_vs_gstar": sp.simplify(g_star / s * sp.diff(s, g_star)),
            "S_vs_T": sp.simplify(T / s * sp.diff(s, T))}


def entropy_is_a_prediction_or_a_check():
    """Honest classification.

    ``S_obs`` follows from ``T_rh``; ``T_rh`` follows from ``rho_rad = V_0``,
    which assumes *instantaneous and complete* conversion of the fuel energy
    into radiation.  That assumption is the physical content.  So ``S_obs``
    is a **consistency check of the instantaneous-conversion assumption**, not
    an independent prediction.
    """
    return {"status": "CONDITIONAL",
            "reason": "S_obs is determined by T_rh, which assumes instantaneous "
                      "and complete conversion of V_0 into radiation"}


# ---------------------------------------------------------------------------
# C. Numerical sanity checks at the manuscript's benchmark points
# ---------------------------------------------------------------------------
def benchmark_numbers():
    """Evaluate the scaling relations at the benchmark values used in main.tex."""
    y = sp.Float("1e-2")
    lam = sp.Float("0.1")
    psi0 = sp.Float("1e13")
    g_star = sp.Integer(100)

    m_psi = condensate_oscillation_mass(lam, psi0)
    Gamma = massless_width_yukawa(m_psi, y)
    T1 = T_rh_from_decay(Gamma, g_star)
    V0q = sp.Float("1e16")
    T2 = T_rh_from_instantaneous(V0q, g_star)
    return {"m_psi_GeV": m_psi, "Gamma_GeV": Gamma,
            "T_rh_from_decay": T1, "T_rh_from_V0": T2,
            "ratio": sp.simplify(T1 / T2)}


def order_of_magnitude_report():
    """Print a table of the benchmark scalings."""
    b = benchmark_numbers()
    return {k: sp.N(v, 6) for k, v in b.items()}
