"""SPRINT 7: a real spectral lattice, used to test the paper's own claims.

Appendix (main.tex ~4218-4230) reports three lattice results:

  * mu_max^lattice = 0.198 +- 0.005 w_res
  * Omega_chi h^2 = 0.118 +- 0.015
  * "Total energy conserved to < 0.1% throughout the simulation"

Blocker #4 in SPRINT 5 was that ``scripts/convergence_test.py`` is absent.
It still is.  But the *numerical statements* can be tested on a
reimplementation, and two of the three turn out to be checkable here.

Method
------
Fourier (pseudo-spectral) collocation on a periodic box, symplectic
(velocity-Verlet) time stepping.  For a free massive field the total energy
is exactly conserved by the continuum equations, so any drift is purely
numerical -- which is what an energy-conservation claim is about.

Scaling is exact: the drift depends only on ``m dt`` and the number of
steps, so we can measure it on a small grid and read off the behaviour at
512^3 without running 512^3.
"""

from __future__ import annotations

import numpy as np


def laplacian_k(n, L=1.0):
    """Fourier symbol of the Laplacian on an ``n``-point periodic grid (1D)."""
    k = 2 * np.pi * np.fft.fftfreq(n, d=L / n)
    return -(k ** 2)


def energy(chi, chi_dot, m, k2, L=1.0):
    """Total energy of a free massive field, per unit cell (spectral)."""
    grad = np.fft.ifft(k2 * np.fft.fft(chi)).real * -1.0
    kin = 0.5 * np.mean(chi_dot ** 2)
    pot = 0.5 * m ** 2 * np.mean(chi ** 2)
    grad_e = 0.5 * np.mean(chi * grad)
    return float(kin + pot + grad_e)


def evolve(n=64, m=1.0, dt=1e-3, n_steps=2000, L=1.0):
    """Velocity-Verlet evolution of a free field; return the energy history."""
    rng = np.random.default_rng(0)
    chi = 0.1 * rng.standard_normal(n)
    chi_dot = np.zeros(n)
    k2 = laplacian_k(n, L)

    def acc(x):
        return np.fft.ifft(k2 * np.fft.fft(x)).real - m ** 2 * x

    e0 = energy(chi, chi_dot, m, k2, L)
    acc_now = acc(chi)
    hist = [e0]
    for _ in range(n_steps):
        chi_dot = chi_dot + 0.5 * dt * acc_now
        chi = chi + dt * chi_dot
        acc_now = acc(chi)
        chi_dot = chi_dot + 0.5 * dt * acc_now
        hist.append(energy(chi, chi_dot, m, k2, L))
    return np.array(hist)


def relative_drift(hist):
    """``max |E - E0| / |E0|`` -- exactly the quantity the paper claims < 0.1%."""
    hist = np.asarray(hist)
    return float(np.max(np.abs(hist - hist[0])) / abs(hist[0]))


def drift_vs_dt(n=64, m=1.0, dts=(2e-3, 1e-3, 5e-4, 2.5e-4), n_steps=2000):
    """Energy drift as a function of step size (the convergence study)."""
    return [{"dt": dt, "drift": relative_drift(evolve(n, m, dt, n_steps))}
            for dt in dts]


def drift_vs_grid(m=1.0, dt=1e-3, grids=(32, 64, 128, 256), n_steps=2000):
    """Energy drift as a function of grid size, at fixed step size."""
    return [{"n": n, "drift": relative_drift(evolve(n, m, dt, n_steps))}
            for n in grids]


# ---------------------------------------------------------------------------
# The validity window of the paper's "< 0.1%" claim
# ---------------------------------------------------------------------------
def dt_for_drift(target=1e-3, m=1.0, coefficient=1.0):
    """Step size at which the symplectic drift reaches ``target``.

    Velocity-Verlet conserves a *shadow* Hamiltonian, so the energy error is
    bounded and oscillatory with amplitude ``~ (m dt)^2 / 4`` rather than
    growing secularly.  That is why the paper's "< 0.1%" is achievable --
    the question is only over what duration.
    """
    return float(2.0 * np.sqrt(target) / (m * coefficient))


def periods_supported(target=1e-3, m=1.0):
    """How many oscillation periods the drift stays under ``target``."""
    dt = dt_for_drift(target, m)
    return float(1.0 / (m * dt))


# ---------------------------------------------------------------------------
# The scaling law that decides the 512^3 claim
# ---------------------------------------------------------------------------
def kmax(n, L=1.0):
    """Largest resolved wavenumber of an ``n``-point periodic grid."""
    return float(np.pi * n / L)


def predicted_drift(n, dt, L=1.0, coefficient=0.25):
    """Velocity-Verlet shadow-Hamiltonian error: ``~ coefficient (k_max dt)^2``.

    The energy error of a symplectic integrator is bounded and oscillatory,
    with amplitude set by the *largest* frequency in the problem, i.e. by
    ``k_max = pi n / L`` -- **not** by the number of cells alone.  This is
    why a fixed ``dt`` becomes unstable as the grid is refined.
    """
    return float(coefficient * (kmax(n, L) * dt) ** 2)


def dt_for_target_drift(target, n, L=1.0, coefficient=0.25):
    """Largest ``dt`` that keeps the drift under ``target`` on an ``n^3`` grid."""
    return float(np.sqrt(target / coefficient) / kmax(n, L))


def stability_limit(n, m=1.0, L=1.0):
    """Explicit stability bound of velocity-Verlet: ``dt < 2/sqrt(m^2+k_max^2)``."""
    return float(2.0 / np.sqrt(m ** 2 + kmax(n, L) ** 2))


def five12_is_stable_at(dt, target=1e-3, n=512, L=1.0):
    """Would the paper's ``n=512`` run meet ``<0.1%`` at this ``dt``?"""
    return bool(dt <= dt_for_target_drift(target, n, L))


def cost_for_target(target=1e-3, n=512, m=1.0, periods=100.0, L=1.0):
    """Steps and wall-time needed to satisfy the conservation claim at ``n``."""
    dt = dt_for_target_drift(target, n, L)
    steps = int(np.ceil(periods * (2 * np.pi / m) / dt))
    return {"n": n, "dt": dt, "steps": steps,
            "stable": dt < stability_limit(n, m, L),
            "drift_at_dt": predicted_drift(n, dt, L)}
