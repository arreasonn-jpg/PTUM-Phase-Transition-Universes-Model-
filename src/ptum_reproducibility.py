"""
Reproducibility and numerical-artefact audit  (SPRINT 5)
========================================================

SPRINT 5 asks a narrow question: *can the numbers reported in the manuscript
be regenerated from the artifacts in the repository, and are the diagnostics
physically meaningful?*  It is not a physics sprint; it is an audit of the
numerical pipeline.

What this module checks
-----------------------
1. **Scale separation.**  The background ODE is integrated in units where the
   field is ``~10^19 GeV`` and ``|dy/dt| ~ 10^38``; the solver is therefore
   asked to span ~40 decades of time in a single call.  This is a *diagnosis*,
   not a crash: it explains why some initial conditions never terminate.

2. **Energy-density bookkeeping.**  ``rho_psi`` and ``shifted_potential_psi``
   in the public script do **not** describe the same potential.  ``U`` uses the
   symmetry-breaking mass scale ``lam*psi_0^2 = |mu^2|``; ``rho_psi`` uses
   ``m_eff^2(Phi)`` instead.  At the benchmark point ``Phi = Phi_c`` one has
   ``m_eff^2 = 0`` *exactly*, so ``rho_psi`` collapses to the pure quartic
   ``lam psi^4/4`` with no mass term at all, while ``U`` still carries
   ``-(1/2) lam psi_0^2 psi^2 + const``.  The difference is therefore
   **psi-dependent, not a constant offset**, and it vanishes nowhere.  At
   ``psi = 0`` this gives ``rho_psi = 0`` against ``U(0) > 0``, and ``w`` is
   then read off the ``0/0`` guard rather than the physics.

3. **The ``w`` bound.**  ``w = (K-U)/(K+U)`` with ``K,U >= 0`` lies in
   ``[-1,+1]``.  Any scan value outside that range is an artefact.

4. **Reproducibility.**  Which of the 18 scanned initial-condition points can
   actually be re-run to completion?

5. **Artifact inventory.**  ``main.tex`` refers to ``scripts/run_lattice.py``,
   ``scripts/convergence_test.py``, ``scripts/reproduce_figures.py`` and
   ``scripts/compare_class_camb.py``.  Do these files exist?

Nothing here changes ``main.tex``.
"""

from __future__ import annotations

import json
import os
import signal
from contextlib import contextmanager

import numpy as np


# ---------------------------------------------------------------------------
# 1. Scale separation
# ---------------------------------------------------------------------------
def scale_separation(rhs, y0, t=0.0):
    """Ratio of the field scale to the characteristic time scale of ``dy/dt``.

    A value much larger than ``1`` means the integrator must take steps far
    smaller than the timescale over which anything physical happens, which is
    the textbook signature of a badly scaled ODE.
    """
    d = np.asarray(rhs(t, np.asarray(y0, dtype=float)), dtype=float)
    field_scale = float(np.max(np.abs(y0)))
    time_scale = float(1.0 / np.max(np.abs(d))) if np.max(np.abs(d)) > 0 else np.inf
    return {"field_scale": field_scale,
            "time_scale": time_scale,
            "ratio": field_scale / time_scale if time_scale else np.inf}


def is_badly_scaled(ratio, threshold=1e10):
    return bool(ratio > threshold)


# ---------------------------------------------------------------------------
# 2. Energy density versus the shifted potential
# ---------------------------------------------------------------------------
def rho_minus_U(rho, U):
    """``rho_code - U``.

    If the two functions described the same potential this would be constant
    and equal to ``V_min``.  It is not: see :func:`shift_is_missing`.  Returning
    the raw difference lets a caller demonstrate that.
    """
    rho = np.asarray(rho, dtype=float)
    U = np.asarray(U, dtype=float)
    return rho - U


def mass_term_is_absent(rho_at_psi0, quartic_at_psi0, tol=1e-9):
    """``True`` when ``rho(psi_0)`` equals the pure quartic ``lam psi_0^4/4``.

    At ``Phi = Phi_c`` the effective mass vanishes identically, so a correct
    ``rho`` containing ``(1/2) m_eff^2 psi^2`` is indistinguishable from one
    that simply has no mass term.  This helper documents that degeneracy.
    """
    if abs(quartic_at_psi0) == 0:
        return False
    return bool(abs(rho_at_psi0 - quartic_at_psi0) <= tol * abs(quartic_at_psi0))


def shift_is_missing(rho_at_zero, U_at_zero, tol=1e-12):
    """``True`` when ``rho(0)`` does not include the ``U(0)`` offset."""
    return bool(abs(rho_at_zero) < tol * max(abs(U_at_zero), 1.0))


def w_from_shifted(K, U):
    """The physically correct ``w`` using the shifted potential."""
    K = np.asarray(K, dtype=float)
    U = np.asarray(U, dtype=float)
    den = K + U
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den > 0, (K - U) / den, np.nan)


# ---------------------------------------------------------------------------
# 3. Validating a scan against the physical bound
# ---------------------------------------------------------------------------
def validate_w_values(values, tol=1e-9):
    """Classify each ``w`` value as physical, or as an artefact and how."""
    values = [float(v) for v in values]
    below = [v for v in values if v < -1.0 - tol]
    above = [v for v in values if v > 1.0 + tol]
    return {"n": len(values),
            "n_below_minus_1": len(below),
            "n_above_plus_1": len(above),
            "n_out_of_bounds": len(below) + len(above),
            "fraction_out_of_bounds": (len(below) + len(above)) / len(values) if values else 0.0,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "verdict": ("artefact" if (below or above) else "consistent")}


def load_scan(path="task1_parameter_scan_results.json"):
    """Load the shipped parameter scan and extract the ``w_final`` values."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data


def scan_summary(path="task1_parameter_scan_results.json"):
    data = load_scan(path)
    ws = [e["classification"]["w_final"] for e in data]
    quartic = [e["classification"]["quartic_achieved"] for e in data]
    regimes = {}
    for e in data:
        r = e["classification"]["regime"]
        regimes[r] = regimes.get(r, 0) + 1
    return {"n_points": len(data),
            "w": validate_w_values(ws),
            "quartic_achieved_any": any(quartic),
            "regimes": regimes}


# ---------------------------------------------------------------------------
# 4. Reproducibility harness
# ---------------------------------------------------------------------------
@contextmanager
def time_limit(seconds):
    """Raise ``TimeoutError`` after ``seconds`` (POSIX only)."""
    def handler(signum, frame):
        raise TimeoutError
    # NB: signal.alarm() only accepts whole seconds, so a sub-second budget is
    # rounded up to 1 s rather than silently disabling the alarm.
    delay = max(1, int(np.ceil(seconds)))
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(delay)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def can_run(fn, timeout=5.0):
    """``True`` when ``fn()`` completes within ``timeout`` seconds."""
    try:
        with time_limit(timeout):
            fn()
        return True
    except TimeoutError:
        return False
    except Exception:
        return False


def reproducibility_table(run_one, ic_list, timeout=5.0):
    """For each initial condition, record whether the run completes."""
    rows = []
    for ic in ic_list:
        ok = can_run(lambda ic=ic: run_one(ic), timeout)
        rows.append({"ic": ic, "completes": ok})
    n_ok = sum(r["completes"] for r in rows)
    return {"rows": rows, "n_complete": n_ok, "n_total": len(rows),
            "fraction": n_ok / len(rows) if rows else 0.0}


# ---------------------------------------------------------------------------
# 5. Artifact inventory
# ---------------------------------------------------------------------------
REFERENCED_SCRIPTS = (
    "scripts/run_lattice.py",
    "scripts/convergence_test.py",
    "scripts/reproduce_figures.py",
    "scripts/compare_class_camb.py",
)


def script_inventory(root=".", referenced=REFERENCED_SCRIPTS):
    """Which referenced scripts exist on disk?"""
    present = {p: os.path.exists(os.path.join(root, p)) for p in referenced}
    return {"referenced": list(referenced),
            "present": present,
            "n_missing": sum(1 for v in present.values() if not v)}


# Each status begins with ``present`` or ``absent`` so that support can be
# decided mechanically instead of by substring luck.
REFERENCED_ARTIFACTS = {
    "CLASS modified code": "absent (author-reported as not public)",
    "Cobaya chains": "absent (author-reported as not public)",
    "lattice output": "absent (author-reported as not public)",
    "Docker image 'ptum-cosmology'": "absent (no Dockerfile in the repo)",
}


def artifact_inventory():
    """The set of claimed-but-absent numerical artifacts."""
    return dict(REFERENCED_ARTIFACTS)


def claim_is_supported(artifact):
    """``False`` for every artifact whose status says it is not in the repo."""
    status = REFERENCED_ARTIFACTS.get(artifact)
    if status is None:
        return False
    return status.startswith("present")


# ---------------------------------------------------------------------------
# 6. Convergence artefacts (the manuscript's own lattice claims)
# ---------------------------------------------------------------------------
CONVERGENCE_CLAIMS = {
    "grid_256": "stated reference run",
    "grid_512": "convergence_test.py -- missing",
    "energy_conservation_0p1_percent": "no output file in the repo",
    "floquet_0p198": "no output file in the repo",
    "omega_chi_h2_0p118": "no output file in the repo",
}


# ---------------------------------------------------------------------------
# 5b. What the public script can and cannot compute
# ---------------------------------------------------------------------------
# ``ptum_task1_simulation.py`` solves the homogeneous background ODE only.
# It contains no perturbation solver, no power spectrum, and no transfer
# function, so it cannot produce ``n_s``, ``r`` or any 200-mode result.
SCRIPT_CAPABILITY = {
    "homogeneous background": True,
    "spectral index n_s": False,
    "tensor-to-scalar ratio r": False,
    "200-mode Mukhanov-Sasaki": False,
    "matter power spectrum": False,
}

# Attestations in the manuscript of the form "verified with the public script".
SCRIPT_ATTESTATIONS = {
    "Delta n_s ~ 5e-4": "requires n_s -- script has no perturbation solver",
    "|Delta r|/r ~ 1.5%": "requires r -- script has no perturbation solver",
    "200-mode MS agreement": "requires k-modes -- k_modes is declared but never used",
}


def script_can(quantity):
    """Can the shipped script compute ``quantity``?"""
    return SCRIPT_CAPABILITY.get(quantity, False)


def attestation_is_supported(claim):
    """Every 'verified with the public script' attestation in the manuscript.

    Returns ``(supported, reason)``.  All are unsupported: the script is a
    background-only integrator.
    """
    reason = SCRIPT_ATTESTATIONS.get(claim, "claim not registered")
    return SCRIPT_CAPABILITY["spectral index n_s"] and \
        SCRIPT_CAPABILITY["tensor-to-scalar ratio r"], reason


def convergence_status():
    """Every stated convergence check, and whether it can be reproduced here."""
    return {k: {"claim": v, "reproducible": False} for k, v in CONVERGENCE_CLAIMS.items()}
