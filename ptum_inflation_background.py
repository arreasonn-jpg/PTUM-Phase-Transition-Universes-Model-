#!/usr/bin/env python3
"""Reproducible single-field PTUM inflationary background scan.

The field variable x = Phi/M_Pl and the normalized velocity
X = dot(Phi)/(sqrt(6) H M_Pl) are dimensionless.  This module solves
the scalar-dominated flat-FRW background and reports first-order
Hubble-flow estimates (not a Mukhanov-Sasaki mode integration).
"""
from __future__ import annotations

import argparse
import json
from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def _one_minus_exp_minus(q: float) -> float:
    return float(-np.expm1(-q))


def potential_fraction(x: float, lambda_phi: float) -> float:
    """V/V0 for V = V0 [1 - exp(-lambda_phi x^2)]."""
    if lambda_phi <= 0.0:
        raise ValueError("lambda_phi must be positive")
    return _one_minus_exp_minus(lambda_phi * x * x)


def logarithmic_slope(x: float, lambda_phi: float) -> float:
    """s(x) = -M_Pl V_,Phi/V, dimensionless."""
    q = lambda_phi * x * x
    den = _one_minus_exp_minus(q)
    if den <= 0.0:
        raise ValueError("The potential slope is undefined at x=0")
    return -2.0 * lambda_phi * x * np.exp(-q) / den


def epsilon_potential(x: float, lambda_phi: float) -> float:
    q = lambda_phi * x * x
    den = _one_minus_exp_minus(q)
    if den <= 0.0:
        return float("inf")
    return 2.0 * lambda_phi**2 * x**2 * np.exp(-2.0 * q) / den**2


def eta_potential(x: float, lambda_phi: float) -> float:
    q = lambda_phi * x * x
    den = _one_minus_exp_minus(q)
    if den <= 0.0:
        return float("inf")
    return 2.0 * lambda_phi * np.exp(-q) * (1.0 - 2.0 * q) / den


def background_rhs(_N: float, state: np.ndarray, lambda_phi: float) -> np.ndarray:
    """Autonomous scalar-dominated background equations for (x, X)."""
    x, X = state
    s = logarithmic_slope(float(x), lambda_phi)
    return np.array([
        np.sqrt(6.0) * X,
        (1.0 - X**2) * (np.sqrt(1.5) * s - 3.0 * X),
    ])


def integrate_background(
    x_initial: float,
    lambda_phi: float,
    *,
    n_max: float = 150.0,
    rtol: float = 2.0e-9,
    atol: float = 1.0e-11,
    max_step: float = 0.08,
    dense_output: bool = False,
):
    """Integrate from the slow-roll attractor until epsilon_H = 1."""
    if x_initial <= 0.0 or lambda_phi <= 0.0:
        raise ValueError("x_initial and lambda_phi must be positive")
    X_initial = logarithmic_slope(x_initial, lambda_phi) / np.sqrt(6.0)

    def inflation_end(_N: float, state: np.ndarray, _lambda: float) -> float:
        return 3.0 * state[1] ** 2 - 1.0

    inflation_end.terminal = True
    inflation_end.direction = 1.0

    return solve_ivp(
        background_rhs,
        (0.0, n_max),
        np.array([x_initial, X_initial]),
        args=(lambda_phi,),
        events=inflation_end,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=dense_output,
    )


def find_initial_field(
    lambda_phi: float,
    *,
    n_target: float = 60.0,
    n_max: float = 150.0,
) -> tuple[float, float]:
    """Find x_initial giving n_target e-folds before epsilon_H reaches one."""
    if lambda_phi <= 0.0 or n_target <= 0.0:
        raise ValueError("lambda_phi and n_target must be positive")

    x_end_sr = brentq(
        lambda x: epsilon_potential(x, lambda_phi) - 1.0,
        1.0e-8,
        100.0 / np.sqrt(lambda_phi),
    )
    lower = x_end_sr * 1.001

    def n_end(x_initial: float) -> float:
        sol = integrate_background(x_initial, lambda_phi, n_max=n_max)
        if len(sol.t_events[0]):
            return float(sol.t_events[0][0])
        if sol.success:
            # No end event before n_max means the end lies beyond this
            # integration window; use a bracket sentinel above n_target.
            return n_max + 1.0
        raise RuntimeError(f"Background integration failed: {sol.message}")

    if n_end(lower) >= n_target:
        raise RuntimeError("Could not establish a lower bracket for x_initial")

    upper = max(2.0 * lower, lower + 0.1)
    for _ in range(60):
        if n_end(upper) > n_target:
            break
        upper *= 1.1
    else:
        raise RuntimeError("Could not bracket the requested inflation duration")

    x_initial = brentq(
        lambda x: n_end(x) - n_target,
        lower,
        upper,
        xtol=1.0e-10,
    )
    return float(x_initial), float(x_end_sr)


def compute_observables(
    lambda_phi: float,
    *,
    n_target: float = 60.0,
    n_star: float = 55.0,
) -> dict[str, float]:
    """Compute background and first-order Hubble-flow observables."""
    if n_star <= 0.0 or n_star >= n_target:
        raise ValueError("Require 0 < n_star < n_target")

    x_initial, x_end_sr = find_initial_field(
        lambda_phi, n_target=n_target
    )
    sol = integrate_background(
        x_initial, lambda_phi, dense_output=True
    )
    if not sol.success or not len(sol.t_events[0]):
        raise RuntimeError("Inflation-end event was not reached")

    n_end = float(sol.t_events[0][0])
    x_end_hubble_flow = float(sol.y[0, -1])
    epsilon_v_end = epsilon_potential(x_end_hubble_flow, lambda_phi)
    # Compare the potential slow-roll end estimate with the exact epsilon_H=1
    # event. This also quantifies when an older Phi_c=x_end_SR match crosses.
    n_old_threshold = brentq(
        lambda N: float(sol.sol(N)[0]) - x_end_sr,
        0.0,
        n_end,
    )
    old_threshold_lead_efolds = n_end - n_old_threshold
    x_star, X_star = sol.sol(n_end - n_star)
    dX_dN = background_rhs(
        n_end - n_star, np.array([x_star, X_star]), lambda_phi
    )[1]

    epsilon_1 = 3.0 * X_star**2
    epsilon_2 = 6.0 * X_star * dX_dN / epsilon_1
    n_s = 1.0 - 2.0 * epsilon_1 - epsilon_2
    r = 16.0 * epsilon_1

    epsilon_v = epsilon_potential(float(x_star), lambda_phi)
    eta_v = eta_potential(float(x_star), lambda_phi)
    n_s_sr = 1.0 - 6.0 * epsilon_v + 2.0 * eta_v
    r_sr = 16.0 * epsilon_v

    return {
        "lambda_phi": float(lambda_phi),
        "x_initial": x_initial,
        "x_end_slow_roll": x_end_sr,
        "x_end_hubble_flow": x_end_hubble_flow,
        "epsilon_V_at_hubble_end": float(epsilon_v_end),
        "old_potential_end_threshold_lead_efolds": float(old_threshold_lead_efolds),
        "n_end": n_end,
        "x_star": float(x_star),
        "epsilon_1_star": float(epsilon_1),
        "epsilon_2_star": float(epsilon_2),
        "n_s_hubble_flow_1st_order": float(n_s),
        "r_hubble_flow_1st_order": float(r),
        "epsilon_V_star": float(epsilon_v),
        "eta_V_star": float(eta_v),
        "n_s_slow_roll": float(n_s_sr),
        "r_slow_roll": float(r_sr),
        "n_star": float(n_star),
    }


def run_scan(
    lambdas: Iterable[float] = (0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0),
    *,
    n_target: float = 60.0,
    n_star: float = 55.0,
) -> list[dict[str, float]]:
    return [
        compute_observables(lam, n_target=n_target, n_star=n_star)
        for lam in lambdas
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-target", type=float, default=60.0)
    parser.add_argument("--n-star", type=float, default=55.0)
    parser.add_argument("--output", default="ptum_inflation_scan.json")
    args = parser.parse_args()

    results = run_scan(n_target=args.n_target, n_star=args.n_star)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    for row in results:
        print(
            f"lambda={row['lambda_phi']:g}  "
            f"x_i={row['x_initial']:.6f}  "
            f"x_end_H={row['x_end_hubble_flow']:.6f}  "
            f"N_end={row['n_end']:.6f}  "
            f"n_s={row['n_s_hubble_flow_1st_order']:.8f}  "
            f"r={row['r_hubble_flow_1st_order']:.8g}"
        )
    print(f"Saved {len(results)} rows to {args.output}")


if __name__ == "__main__":
    main()
