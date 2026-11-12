"""
Background evolution of the proxy field ``psi``  (SPRINT 4, part A)
===================================================================

Reproduces the equation of state of ``psi`` from the actual field dynamics,
rather than from the oscillation-averaged ansatz, and checks the manuscript's
own ``w_psi = 0`` vs ``w_psi = 1/3`` statements.

The model
---------
``main.tex`` Eq. (``eq:psi_eom_full``)::

    psi'' + 3H psi' - mu^2 psi + lam_psi psi^3 = 0

with ``mu^2 = |m_eff^2| > 0`` and the double-well ``U = lam/4 (psi^2 - psi0^2)^2``.

The equation of state, measured from the minimum (Eq. ``eq:w_psi_energy``)::

    rho = psi'^2/2 + U ,   p = psi'^2/2 - U ,   w = p/rho

Key structural fact -- this is the whole of SPRINT 4 part A
-----------------------------------------------------------
``w`` is bounded by the potential:

    U >= 0  =>  w = (K - U)/(K + U) >= -1 ,    and  <= +1 since K >= 0

So ``w < -1`` is **impossible** for a canonical scalar with a non-negative
potential.  Any numerical quadruple-precision run that reports ``w < -1`` is
reporting a *numerical* artefact (or is using a signed potential / a modified
gravity), never a property of this Lagrangian.

Two distinct ``1/3`` statements that the literature conflates
--------------------------------------------------------------
* **Instantaneous** ``w``: for a quartic oscillator ``psi^4``, ``w`` oscillates
  between ``-1`` and ``+1`` and is ``1/3`` only at the turning points of the
  virial cycle, never identically.
* **Oscillation-averaged** ``<w>``: for ``U ~ lam psi^4/4`` the virial theorem
  gives ``<K> = 2<U>``, hence ``<w> = 1/3``.  This holds only in the
  quartic-dominated regime ``|psi| >> psi0``.

For a *quadratic* oscillator (small oscillations about the minimum),
``<K> = <U>`` and ``<w> = 0``.  In between, ``<w>`` interpolates.

``main.tex`` is careful about this distinction in section 4.4; SPRINT 4 checks
that the *numerics* agree with it and that no other part of the paper
contradicts it.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# 1. The bounds on w -- pure algebra, no dynamics
# ---------------------------------------------------------------------------
def w_bounds():
    """``-1 <= w <= 1`` for ``K >= 0`` and ``U >= 0``.

    Returns the two bounds and the reason.
    """
    return {"w_min": -1.0, "w_max": 1.0,
            "reason": "w = (K-U)/(K+U) with K,U >= 0",
            "implies": "w < -1 is impossible for a canonical scalar with U >= 0"}


def w_from_energy(K, U):
    """``w = (K - U)/(K + U)``; handles the ``K = U = 0`` case as ``nan``."""
    K = np.asarray(K, dtype=float)
    U = np.asarray(U, dtype=float)
    den = K + U
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den > 0, (K - U) / den, np.nan)


# ---------------------------------------------------------------------------
# 2. The double-well potential and its scales
# ---------------------------------------------------------------------------
def potential(psi, mu, lam):
    """``U = lam/4 (psi^2 - psi0^2)^2`` with ``psi0^2 = mu^2/lam``."""
    psi0sq = mu**2 / lam
    return lam / 4.0 * (psi**2 - psi0sq) ** 2


def psi0(mu, lam):
    return np.sqrt(mu**2 / lam)


def oscillation_mass(mu):
    """``m_osc^2 = U''(+-psi0) = 2 mu^2`` (manuscript Eq. ``minimum_expansion``)."""
    return np.sqrt(2.0) * mu


def omega_over_H(mu, lam, psi_amp, H):
    """Effective oscillation frequency over the Hubble rate.

    Quartic regime: ``omega ~ sqrt(lam) psi_amp``.
    Quadratic regime: ``omega ~ sqrt(2) mu``.
    """
    omega_quartic = np.sqrt(lam) * psi_amp
    omega_quad = np.sqrt(2.0) * mu
    return {"quartic": omega_quartic / H, "quadratic": omega_quad / H}


# ---------------------------------------------------------------------------
# 3. Background integrator
# ---------------------------------------------------------------------------
def evolve(psi_i, psidot_i, mu, lam, H, t_max, n_eval=4000, rtol=1e-10):
    """Integrate ``psi'' + 3H psi' - mu^2 psi + lam psi^3 = 0``.

    ``H`` is held fixed (de Sitter-like) -- the manuscript's own "overdamped,
    no oscillation" regime is precisely the one where this is a good
    approximation over the timescales of interest.
    """

    def rhs(t, y):
        psi, psidot = y
        return [psidot, -3.0 * H * psidot + mu**2 * psi - lam * psi**3]

    t_eval = np.linspace(0.0, t_max, n_eval)
    sol = solve_ivp(rhs, (0.0, t_max), [psi_i, psidot_i], t_eval=t_eval,
                    rtol=rtol, atol=1e-30, method="DOP853")
    psi = sol.y[0]
    psidot = sol.y[1]
    K = 0.5 * psidot**2
    U = potential(psi, mu, lam)
    return {"t": sol.t, "psi": psi, "psidot": psidot,
            "K": K, "U": U, "rho": K + U, "p": K - U,
            "w": w_from_energy(K, U),
            "w_avg": (K - U).sum() / (K + U).sum()}


def damping_ratio(mu, H):
    """``3H/(2 mu)`` -- the manuscript's overdamping diagnostic."""
    return 3.0 * H / (2.0 * mu)


def crosses_barrier(psi_i, psidot_i, mu, lam):
    """Energy compared with the barrier height ``U(0) = mu^4/(4 lam)``."""
    E = 0.5 * psidot_i**2 + potential(psi_i, mu, lam)
    barrier = mu**4 / (4.0 * lam)
    # NOTE: E == barrier means the field sits *on* the maximum with zero
    # velocity, which does NOT cross.  Only strictly more energy does.
    return {"E": E, "barrier": barrier, "crosses": bool(E > barrier),
            "ratio": E / barrier,
            "on_the_barrier": abs(E - barrier) < 1e-12 * max(barrier, 1.0)}


# ---------------------------------------------------------------------------
# 4. The averaged equation of state, analytically
# ---------------------------------------------------------------------------
def averaged_w_power_law(n):
    """``<w> = (n-2)/(n+2)`` for ``U ~ psi^n`` (virial theorem).

    ``n = 2`` -> 0 (matter-like), ``n = 4`` -> 1/3 (radiation-like).
    """
    return (n - 2) / (n + 2)


def averaged_w_quartic():
    return averaged_w_power_law(4)


def averaged_w_quadratic():
    return averaged_w_power_law(2)


def effective_power(psi_amp, mu, lam):
    """Which power law the orbit actually follows.

    The orbit samples ``|psi|`` up to ``psi_amp``.  If ``psi_amp >> psi0`` the
    quartic term dominates and ``n -> 4``; if ``psi_amp << psi0`` the quadratic
    term dominates and ``n -> 2``.  In between, the averaged ``<w>`` is between
    ``0`` and ``1/3``.
    """
    ratio = psi_amp / psi0(mu, lam)
    return {"psi_amp_over_psi0": ratio,
            "regime": ("quartic" if ratio > 3 else
                       "quadratic" if ratio < 1 / 3 else "intermediate"),
            "w_quartic_limit": averaged_w_quartic(),
            "w_quadratic_limit": averaged_w_quadratic()}
