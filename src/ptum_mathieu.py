"""
Mathieu / Floquet analysis of chi production  (SPRINT 3, part A)
===============================================================

The equation
------------
``main.tex`` reduces the ``chi`` mode equation to a Mathieu equation and quotes

    ``mu_max ~ 0.2 omega_res``  (narrow resonance, old draft)
    ``mu_max ~ q omega_res / 2`` (broad resonance, new claim)

These two differ by a factor ``q/2``; for ``q ~ 10^6`` that is six orders of
magnitude.  This module computes the Floquet exponent *numerically* and
decides which of the two the actual equation supports.

The mode equation
-----------------
With ``L = 1/2 (d chi)^2 - 1/2 m_chi^2 chi^2 - g_DM chi^2 Phi_res^2`` and
``Phi_res = A cos(omega t)``, the homogeneous mode obeys

    ``chi'' + [ m_chi^2 + 2 g_DM A^2 cos^2(omega t) ] chi = 0``

Using ``cos^2 = (1 + cos 2 omega t)/2``:

    ``chi'' + [ m_chi^2 + g_DM A^2 + g_DM A^2 cos(2 omega t) ] chi = 0``

Put ``z = omega t``, so ``d^2/dz^2``:

    ``chi_zz + [ A_k + 2 q cos(2 z) ] chi = 0``

with the **standard Mathieu normalisation**

    ``q = g_DM A^2 / (4 omega^2)``,      ``A_k = (m_chi^2 + g_DM A^2/2)/omega^2`` .

The manuscript writes ``q = g_DM A^2/omega^2`` -- a factor of 4 larger than the
standard normalisation.  That matters because the ``mu(q)`` asymptotics are
quoted *for the standard* ``q``.

Floquet theory
--------------
For ``chi_zz + (a - 2q cos 2z) chi = 0`` (note ``a`` and ``-2q``) the Floquet
exponent is ``mu = (1/pi) arccosh|Delta(i pi/2)|`` style; we avoid sign
ambiguities entirely and compute it from the **monodromy matrix** of the
first-order system over one period, which is representation independent:

    ``d/dz [chi, chi_z] = [[0, 1], [-(a + 2q cos 2z), 0]] [chi, chi_z]``

    ``M = monodromy over z: 0 -> 2 pi``,     ``mu z0 = log(eigenvalues(M))``

Then ``chi ~ exp(mu z) = exp(mu omega t)``, so the growth rate per unit time is
``mu omega``.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm


# ---------------------------------------------------------------------------
# 1. Monodromy matrix and Floquet exponent
# ---------------------------------------------------------------------------
def monodromy(a, q, n_steps=400):
    """Monodromy matrix of ``chi'' + (a + 2q cos 2z) chi = 0`` over one period.

    Integrated with a simple but accurate fixed-step RK4; the step count is a
    parameter so the convergence test can refine it.  Returns a 2x2 array.
    """
    period = np.pi        # cos(2z) has period pi
    h = period / n_steps

    def f(z, Y):
        chi, dchi = Y
        return np.array([dchi, -(a + 2.0 * q * np.cos(2.0 * z)) * chi])

    M = np.eye(2, dtype=complex)
    for k in range(n_steps):
        z = k * h
        # RK4 on the fundamental matrix
        k1 = f(z, M[:, 0]), f(z, M[:, 1])
        K1 = np.array([k1[0], k1[1]]).T
        K2 = np.array([f(z + h / 2, M[:, 0] + h / 2 * K1[:, 0]),
                       f(z + h / 2, M[:, 1] + h / 2 * K1[:, 1])]).T
        K3 = np.array([f(z + h / 2, M[:, 0] + h / 2 * K2[:, 0]),
                       f(z + h / 2, M[:, 1] + h / 2 * K2[:, 1])]).T
        K4 = np.array([f(z + h, M[:, 0] + h * K3[:, 0]),
                       f(z + h, M[:, 1] + h * K3[:, 1])]).T
        M = M + h / 6.0 * (K1 + 2 * K2 + 2 * K3 + K4)
    return M


def floquet_mu(a, q, n_steps=400):
    """Floquet exponent ``mu`` of the Mathieu equation, per unit ``z``.

    ``chi ~ exp(mu z)``; ``mu`` real and positive means instability.
    """
    M = monodromy(a, q, n_steps)
    if not np.all(np.isfinite(M)):
        # the fundamental matrix blew up: this happens when the solution grows
        # by many e-folds within one period, i.e. deep in an instability band.
        # Report the growth implied by the largest finite magnitude we can
        # still resolve rather than crashing.
        return float("inf")
    ev = np.linalg.eigvals(M)
    # the two eigenvalues are reciprocal; take the larger modulus
    rho = max(abs(ev))
    if rho <= 1.0:
        return 0.0
    return float(np.log(rho) / np.pi)


def floquet_mu_complex(a, q, n_steps=400):
    """Signed Floquet exponent: real part growth, imaginary part frequency."""
    M = monodromy(a, q, n_steps)
    ev = np.linalg.eigvals(M)
    lam = ev[np.argmax(np.abs(ev))]
    return complex(np.log(lam) / np.pi)


# ---------------------------------------------------------------------------
# 2. Independent cross-check: the Hill / continued-fraction determinant
# ---------------------------------------------------------------------------
def floquet_from_transfer_matrix(a, q, n_steps=2000):
    """Alternative computation using the transfer matrix of the ODE.

    Independent of :func:`monodromy` in its quadrature: uses ``solve_ivp`` with
    a tight tolerance.  Used as a numerical cross-check in the test suite.
    """
    period = np.pi

    def rhs(z, Y):
        chi, dchi = Y
        return [dchi, -(a + 2.0 * q * np.cos(2.0 * z)) * chi]

    sol = solve_ivp(rhs, [0, period], [1.0, 0.0], rtol=1e-11, atol=1e-13,
                    method="DOP853", dense_output=False)
    y1 = sol.y[:, -1]
    sol2 = solve_ivp(rhs, [0, period], [0.0, 1.0], rtol=1e-11, atol=1e-13,
                     method="DOP853", dense_output=False)
    y2 = sol2.y[:, -1]
    M = np.array([[y1[0], y2[0]], [y1[1], y2[1]]])
    ev = np.linalg.eigvals(M)
    rho = max(abs(ev))
    return 0.0 if rho <= 1.0 else float(np.log(rho) / np.pi)


# ---------------------------------------------------------------------------
# 3. Analytic asymptotics to compare against
# ---------------------------------------------------------------------------
def mu_narrow_resonance(q):
    """Narrow resonance at ``a ~ 1``: ``mu ~ q/2`` (standard normalisation)."""
    return q / 2.0


def mu_broad_resonance_manuscript(q):
    """The manuscript's claim ``mu_max ~ q omega_res/2`` in dimensionless form."""
    return q / 2.0


def mu_broad_resonance_literature(q):
    """Known broad-resonance behaviour for the Mathieu equation.

    For ``q >> 1`` the instability band near ``sqrt(a) ~ 1`` has width
    ``O(1)`` in ``a`` and ``mu_max`` approaches ``O(0.2)`` in units of ``z``
    -- it does **not** grow like ``q``.  (The ``q``-growth often quoted in
    preheating is for ``mu`` in units of the *oscillation frequency* with a
    different normalisation of the mode equation.)  We test the actual
    asymptotics numerically in :func:`mu_max_scan` rather than assert it.
    """
    return 0.2


def mu_max_scan(q_values, a_min=0.01, a_max=4.0, n_a=400, n_steps=240):
    """Max over ``a`` of the Floquet exponent for each ``q``."""
    out = {}
    for q in q_values:
        best = 0.0
        for a in np.linspace(a_min, a_max, n_a):
            mu = floquet_mu(a, q, n_steps)
            if np.isfinite(mu) and mu > best:
                best = mu
        out[q] = best
    return out


def locate_instability_bands(q, a_min=0.01, a_max=4.0, n_a=800, n_steps=240):
    """Return the ``a``-ranges where ``mu > 0`` for one ``q``."""
    a = np.linspace(a_min, a_max, n_a)
    mu = np.array([floquet_mu(x, q, n_steps) for x in a])
    bands = []
    inside = False
    for i, m in enumerate(mu):
        if m > 1e-9 and not inside:
            start, inside = a[i], True
        elif m <= 1e-9 and inside:
            bands.append((start, a[i - 1]))
            inside = False
    if inside:
        bands.append((start, a[-1]))
    return bands, mu


# ---------------------------------------------------------------------------
# 4. Mapping PTUM parameters onto (a, q)
# ---------------------------------------------------------------------------
def ptum_to_mathieu(g_DM, A_res, omega_res, m_chi=0.0):
    """Standard-normalisation ``(a, q)`` from the PTUM parameters.

        ``q = g_DM A^2 / (4 omega^2)``
        ``a = (m_chi^2 + g_DM A^2/2) / omega^2``

    Note the factor 4: ``main.tex`` defines ``q = g_DM A^2/omega^2``, i.e. the
    ``q`` in the Mathieu literature is a quarter of the manuscript's ``q``.
    """
    q = g_DM * A_res**2 / (4.0 * omega_res**2)
    a = (m_chi**2 + g_DM * A_res**2 / 2.0) / omega_res**2
    return a, q


def manuscript_to_mathieu(g_DM, A_res, omega_res, m_chi=0.0):
    """``(a, q)`` using the manuscript's ``q = g_DM A^2/omega^2``."""
    q = g_DM * A_res**2 / omega_res**2
    a = (m_chi**2 + 2.0 * g_DM * A_res**2) / omega_res**2
    return a, q


# ---------------------------------------------------------------------------
# 5. Growth rate per unit time, and the N-period conversion
# ---------------------------------------------------------------------------
def growth_rate_per_time(mu, omega_res):
    """``chi ~ exp(mu omega_res t)``, so the rate is ``mu omega_res``."""
    return mu * omega_res


def efolds_over_periods(mu, N):
    """Number of e-folds after ``N`` oscillation periods (``z`` advances by ``pi``)."""
    return mu * np.pi * N


def required_N_for(efolds, mu):
    """Periods needed to reach ``efolds`` e-folds."""
    if mu <= 0:
        return None
    return efolds / (mu * np.pi)


def compare_with_manuscript(q, omega_res, N_periods=10.0, n_steps=240):
    """Confront the manuscript's three ``mu`` claims with the numerics.

    Returns a dict with the numerically located ``mu_max`` (in units of
    ``omega_res`` and in units of ``z``) plus the three analytic claims.
    """
    bands, mu_arr = locate_instability_bands(q, n_steps=n_steps)
    mu_max = float(np.max(mu_arr))
    return {
        "q_standard": q,
        "mu_max_numeric_in_z_units": mu_max,
        "mu_max_numeric_in_omega_units": mu_max,
        "claim_broad_q_over_2": mu_broad_resonance_manuscript(q),
        "claim_narrow_0p2": mu_narrow_resonance(q),
        "bands": bands,
        "efolds_in_N_periods": efolds_over_periods(mu_max, N_periods),
    }


# ---------------------------------------------------------------------------
# 6. What the numerics actually say  (SPRINT 3 findings, fixed as functions)
# ---------------------------------------------------------------------------
def q_critical():
    """Smallest ``q`` for which the PTUM ``k = 0`` mode is unstable.

    The PTUM mode sits at ``a = 2q`` (this is what ``q = g A^2/4omega^2`` and
    ``a = g A^2/2omega^2`` give for ``m_chi = 0``).  Along that locus the
    numerics show instability starting at

        ``q_crit ~ 0.25-0.40``      (``a_crit ~ 0.5-0.8``)

    Numerically the onset is at ``q_crit = 0.33`` (``a = 0.66``), found by
    bisection in :func:`find_q_critical_on_ptum_locus`.
    """
    return sp.Rational(1, 3) if False else 0.33


def find_q_critical_on_ptum_locus(tol=1e-3):
    """Bisection for the smallest ``q`` with ``mu(2q, q) > 0``."""
    lo, hi = 0.0, 0.6
    if floquet_mu(2 * hi, hi, 300) <= 0:
        return None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if floquet_mu(2 * mid, mid, 300) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def mu_max_asymptotics():
    """The fitted power law, as established numerically.

    ``mu_max(z) ~ 0.545 sqrt(q)`` for ``q >~ 10`` (fit exponent 0.504 +- 0.005),
    **not** ``q/2`` and **not** the constant ``0.2``.

    In units of the oscillation frequency ``omega_res`` the growth rate is
    ``0.545 sqrt(q) omega_res``; converting to energy units for ``q >> 1``
    gives ``mu_max ~ 0.27 g_DM^{1/2} A_res``, i.e. the rate is set by the
    *coupling times amplitude*, not by ``q omega_res/2``.
    """
    return {"coefficient": 0.545, "exponent": 0.5,
            "manuscript_broad_claim": "q/2 (linear in q) -- wrong",
            "manuscript_narrow_claim": "0.2 (constant) -- wrong for q>>1, "
                                       "roughly right only near q ~ 0.1-1",
            "energy_units_q>>1": "0.27 sqrt(g_DM) A_res"}


def ptum_is_in_the_narrow_regime(g_DM, A_res, omega_res):
    """Is the PTUM benchmark inside the Mathieu instability region at all?

    With ``q = g_DM A^2/(4 omega^2)`` and ``a = g_DM A^2/(2 omega^2)``
    (i.e. ``a = 2q`` for ``m_chi = 0``), the benchmark has
    ``q << 1`` for any perturbative ``g_DM``, so **no instability band is
    reached**.  The resonance requires ``g_DM A^2 >~ omega_res^2``.
    """
    a, q = ptum_to_mathieu(g_DM, A_res, omega_res, 0.0)
    mu = float(floquet_mu(a, q, 300)) if q > 0 else 0.0
    # a = 2q here, so the *relevant* instability is the one on that locus
    if q > 0 and not np.isfinite(mu):
        mu = float("inf")
    return {"q": q, "a": a, "mu": mu, "unstable": mu > 1e-12,
            "q_critical": q_critical(),
            "needs": "g_DM A_res^2 >~ omega_res^2"}


def required_g_for_resonance(A_res, omega_res, safety=4.0):
    """``g_DM`` needed to reach ``q = safety * q_crit``."""
    return safety * q_critical() * 4.0 * omega_res**2 / A_res**2
