#!/usr/bin/env python3
"""Compare IVP solvers on one exact deterministic PTUM scan trajectory.

This is a diagnostic only: it never changes physical parameters or equations.
# Full validation gate: [run-full-scan] executes the complete 100-row Radau scan.
"""
# Diagnostic baseline: preserve scan initial conditions and physical parameters.
import argparse
import warnings
import numpy as np
from scipy.integrate import solve_ivp
from ptum_inflation_background import state_at_field_value
from ptum_task1_simulation import (
    M_PL, DEFAULT_RTOL, DEFAULT_DIMENSIONLESS_ATOL, default_state_atol,
    background_equations, rho_phi, rho_psi, rho_total,
)
from ptum_task1_scan import build_scan_scenarios, SEED_SCALES, VELOCITY_SCALES, PHI_OFFSETS, DEFAULT_T_MAX, DEFAULT_N_POINTS


def get_spec(index):
    rows = []
    for scenario, params in build_scan_scenarios():
        seeds = [x * params.psi_0 for x in SEED_SCALES]
        velocities = [x * params.mu * params.psi_0 for x in VELOCITY_SCALES]
        offsets = [x * params.Phi_c for x in PHI_OFFSETS]
        phi_dots = {
            off: state_at_field_value(params.lambda_phi, (params.Phi_c-off)/M_PL, V0=params.V0)["Phi_dot"]
            for off in offsets
        }
        for psi in seeds:
            for psi_dot in velocities:
                for off in offsets:
                    rows.append((scenario, params, psi, psi_dot, off, phi_dots[off]))
    if not 0 <= index < len(rows):
        raise ValueError(f"index must be in [0, {len(rows)-1}]")
    return rows[index]


def energy(y, p):
    phi, phi_dot, psi, psi_dot = map(float, y)
    with np.errstate(over="ignore", invalid="ignore"):
        return {
            "rho_phi": float(rho_phi(phi, phi_dot, psi, p)),
            "rho_psi": float(rho_psi(phi, psi, psi_dot, p)),
            "rho_total": float(rho_total(phi, phi_dot, psi, psi_dot, p)),
        }


def run(method, spec, tmax, npoints):
    scenario, p, psi, psi_dot, offset, phi_dot = spec
    y0 = np.array([p.Phi_c-offset, phi_dot, psi, psi_dot], dtype=float)
    span = (0.0, tmax / p.mu)
    evaluation = np.linspace(*span, npoints)
    failed_rhs = {}

    def rhs(t, y, params):
        try:
            return background_equations(t, y, params)
        except Exception as exc:
            failed_rhs.update({
                "t": float(t), "state": [float(v) for v in y],
                "energy": energy(y, params),
                "exception": f"{type(exc).__name__}: {exc}",
            })
            raise

    state_atol = default_state_atol(p)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", RuntimeWarning)
        try:
            sol = solve_ivp(rhs, span, y0, args=(p,), t_eval=evaluation,
                            method=method, rtol=DEFAULT_RTOL, atol=state_atol)
            report = {
                "success": bool(sol.success), "message": str(sol.message),
                "rtol": DEFAULT_RTOL,
                "dimensionless_atol": DEFAULT_DIMENSIONLESS_ATOL,
                "atol_state_vector": state_atol.tolist(),
                "nfev": int(sol.nfev), "njev": int(getattr(sol, "njev", 0) or 0),
                "nlu": int(getattr(sol, "nlu", 0) or 0),
                "accepted_samples": int(len(sol.t)),
                "last_sampled_time": float(sol.t[-1]) if len(sol.t) else None,
                "min_sampled_rho_total": min(
                    (energy(sol.y[:, i], p)["rho_total"] for i in range(sol.y.shape[1])
                     if np.isfinite(energy(sol.y[:, i], p)["rho_total"])),
                    default=None,
                ),
                "final_state": [float(value) for value in sol.y[:, -1]],
            }
        except Exception as exc:
            report = {"success": False, "message": f"{type(exc).__name__}: {exc}"}
        report["rhs_failure"] = failed_rhs or None
        report["runtime_warnings"] = [str(x.message) for x in captured]
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, default=72)
    parser.add_argument("--methods", nargs="+", default=["DOP853", "Radau", "BDF"])
    parser.add_argument("--t-max", type=float, default=DEFAULT_T_MAX)
    parser.add_argument("--n-points", type=int, default=DEFAULT_N_POINTS)
    args = parser.parse_args()
    spec = get_spec(args.index)
    scenario, p, psi, psi_dot, offset, phi_dot = spec
    y0 = np.array([p.Phi_c-offset, phi_dot, psi, psi_dot])
    print("EXACT_SCAN_ROW", {
        "index_zero_based": args.index, "scenario": scenario, "V0": p.V0,
        "psi_init": psi, "psi_dot_init": psi_dot, "phi_offset": offset,
        "Phi_dot_init": phi_dot, "initial_energy": energy(y0, p),
        "t_max_over_mu_inverse": args.t_max, "n_points": args.n_points,
        "rtol": DEFAULT_RTOL,
        "dimensionless_atol": DEFAULT_DIMENSIONLESS_ATOL,
        "atol_state_vector": default_state_atol(p).tolist(),
    }, flush=True)
    reports = {}
    for method in args.methods:
        reports[method] = run(method, spec, args.t_max, args.n_points)
        print("SOLVER", method, reports[method], flush=True)
    if "Radau" in reports and "BDF" in reports:
        left = reports["Radau"].get("final_state")
        right = reports["BDF"].get("final_state")
        if left is not None and right is not None:
            left = np.asarray(left, dtype=float)
            right = np.asarray(right, dtype=float)
            scale = np.maximum(np.maximum(np.abs(left), np.abs(right)), 1.0)
            print("RADAU_BDF_FINAL_STATE_RELATIVE_DIFFERENCE",
                  (np.abs(left - right) / scale).tolist(), flush=True)


if __name__ == "__main__":
    main()
