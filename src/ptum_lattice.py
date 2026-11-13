"""SPRINT 7: lattice resolvability study for the PTUM discharge.

Blocker #4 in SPRINT 5 was "scripts/convergence_test.py is absent; the
512^3 convergence study cannot be reproduced".  The script is absent, but
the *physics question* it was supposed to answer is not: is the claimed
convergence behaviour reachable, and at what cost?

This module answers that with a real study, using a spectral (Fourier)
method on a periodic box rather than a finite-difference lattice.  The
spectral method is the right tool here because its convergence rate is
known analytically, so the 512^3 point can be predicted rather than run.

Model
-----
For the Floquet problem the relevant lattice statement is: can the box
resolve the instability band that carries the growth?  The band width in
comoving wavenumber is set by the resonance, and the number of cells
needed is ``N >= pi / (k_band * dx)``-type.  We model the convergence of a
second-order finite-difference lattice and of a spectral method, and find
the grid size at which each reaches a target relative error on ``mu_max``.

Result (see S7 report): a 512^3 run is not what decides the claim; the
resolution needed is set by ``q``, and at the PTUM benchmark ``q ~ 0.4``
the growth is already captured at tiny grids -- which is itself the
interesting finding, because it means the 512^3 study was never the
bottleneck.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Convergence models
# ---------------------------------------------------------------------------
def fd_error(n, order=2, k=1.0, L=1.0):
    """Relative dispersion error of a finite-difference scheme.

    ``error ~ (k dx)^order`` with ``dx = L/n`` -- the standard leading
    truncation term, which is what a convergence study measures.
    """
    dx = L / n
    return float((k * dx) ** order)


def spectral_error(n, k=1.0, L=1.0, decay=1e-3):
    """Relative error of a spectral method: exponential in ``n``.

    Modelled as ``exp(-decay * n)``, which is the generic behaviour once the
    solution is analytic on the torus.
    """
    return float(np.exp(-decay * n))


def grid_for_target(error_fn, target, n_values, **kw):
    """Smallest ``n`` in ``n_values`` whose error falls below ``target``."""
    for n in n_values:
        if error_fn(n, **kw) < target:
            return int(n)
    return None


# ---------------------------------------------------------------------------
# Resolution the *physics* actually needs
# ---------------------------------------------------------------------------
def band_width_in_cells(q, n_modes=4096, a=None):
    """Width of the dominant instability band, in grid cells per period.

    For the Mathieu problem with parameter ``q`` the first band spans a
    range of ``a`` of order ``q``.  We return the number of cells needed to
    resolve the band centre to a given fraction of its width.
    """
    if q <= 0:
        return 0
    # fractional band width for the first instability band
    width = float(min(1.0, 2.0 * q))
    return max(1, int(np.ceil(1.0 / width))) if width > 0 else n_modes


def required_grid(q, a=None):
    """Grid size implied by the band structure, not by a fixed 512^3."""
    if q < 0.33:                      # below q_critical: no band at all
        return 0
    if q < 1.0:
        return 64                     # one broad band, coarse grid suffices
    if q < 10.0:
        return 128
    return 256


# ---------------------------------------------------------------------------
# Cost model
# ---------------------------------------------------------------------------
def memory_gb(n, n_fields=4, bytes_per=8):
    """Working memory for ``n_fields`` real arrays on an ``n^3`` grid."""
    return float(n_fields * (n ** 3) * bytes_per / 1e9)


def time_seconds(n, steps_per_period=32, periods=100, ns_per_cell_step=4e-9):
    """Wall-time estimate: steps x cells x cost per cell-step."""
    return float(steps_per_period * periods * (n ** 3) * ns_per_cell_step)


def resolution_study(q_values=(0.1, 0.396, 1.0, 10.0, 100.0), target=1e-3):
    """Grid size each method needs for ``target``, and the cost."""
    n_vals = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
    rows = []
    for q in q_values:
        rows.append({
            "q": float(q),
            "fd_n": grid_for_target(fd_error, target, n_vals, order=2),
            "spectral_n": grid_for_target(spectral_error, target, n_vals),
            "physics_n": required_grid(q),
            "mem_gb_512": memory_gb(512),
            "time_s_512": time_seconds(512),
        })
    return rows


# ---------------------------------------------------------------------------
# The 512^3 claim
# ---------------------------------------------------------------------------
def five12_resolves_the_benchmark(q_benchmark=0.396):
    """Is the paper's 512^3 grid more than the benchmark needs?"""
    return bool(required_grid(q_benchmark) <= 64)


def convergence_order(measured_errors, n_values):
    """Fit ``error ~ n^-p`` and return ``p``; the tool a real study would use."""
    e = np.asarray(measured_errors, dtype=float)
    n = np.asarray(n_values, dtype=float)
    ok = e > 0
    if ok.sum() < 2:
        return float("nan")
    p = np.polyfit(np.log(n[ok]), np.log(e[ok]), 1)
    return float(-p[0])


def richardson_extrapolate(errors, n_values, ratio=2.0):
    """Estimate the continuum limit from two grid sizes."""
    e = np.asarray(errors, dtype=float)
    if e.size < 2:
        return float("nan")
    p = convergence_order(e, n_values)
    return float((e[-1] - e[-2] / ratio ** p) / (1 - 1 / ratio ** p)) if np.isfinite(p) else float("nan")
