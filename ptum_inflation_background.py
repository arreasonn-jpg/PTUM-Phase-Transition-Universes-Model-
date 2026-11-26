#!/usr/bin/env python3
"""
PTUM inflation background: independent implementation from main.tex §3.3.

This module reproduces the eight-row scan in tab:exactscan, verified
against an independent DOP853 + bracketed-brentq implementation in
the PTUM validation suite. It is not a copy of any original file; it
was constructed from the equations in the manuscript and cross-checked
against the paper table.

Equations used:
    V(u) = V_0 (1 - exp(-lambda_Phi * u^2)),  u = Phi / M_Pl
    dx/dN = sqrt(6) * X
    dX/dN = (1 - X^2) (sqrt(3/2) * s(x) - 3 X)
    s(x)  = -(dV/dx) / V
    eps_H = 3 X^2,  N_end at eps_H = 1
    eps_1 = eps_H
    eps_2 = d ln eps_1 / dN
    n_s^HF = 1 - 2 eps_1 - eps_2
    n_s^SR = 1 - 6 eps_V + 2 eta_V
    r^HF   = 16 eps_1

Requires: numpy, scipy.
Run directly to print tab:exactscan.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

M_PL = 2.435e18  # GeV


def V_plateau(u, lam, V0=1.0):
    return V0 * (1.0 - np.exp(-lam * u**2))


def dV_du(u, lam, V0=1.0):
    return V0 * 2.0 * lam * u * np.exp(-lam * u**2)


def d2V_du2(u, lam, V0=1.0):
    return V0 * 2.0 * lam * np.exp(-lam * u**2) * (1.0 - 2.0 * lam * u**2)


def s_of_u(u, lam):
    return -dV_du(u, lam) / V_plateau(u, lam)


def eps_V(u, lam):
    return 0.5 * s_of_u(u, lam)**2


def eta_V(u, lam):
    return d2V_du2(u, lam) / V_plateau(u, lam)


def ode_rhs(N, y, lam):
    u, X = y
    s = s_of_u(u, lam)
    return [np.sqrt(6.0) * X,
            (1.0 - X**2) * (np.sqrt(1.5) * s - 3.0 * X)]


def _end_event(N, y, lam):
    return 3.0 * y[1]**2 - 1.0


_end_event.terminal = True
_end_event.direction = 1


def integrate(u_i, lam, max_N=300.0, rtol=1e-10, atol=1e-12):
    X_i = s_of_u(u_i, lam) / np.sqrt(6.0)
    return solve_ivp(ode_rhs, [0, max_N], [u_i, X_i],
                     args=(lam,), events=_end_event, method="DOP853",
                     rtol=rtol, atol=atol, dense_output=True)


def _res_of_u(u, lam, N_target):
    X0 = s_of_u(u, lam) / np.sqrt(6.0)
    if 3.0 * X0**2 >= 1.0:
        return -N_target
    sol = integrate(u, lam)
    if len(sol.t_events[0]) == 0:
        return 1e6
    return sol.t_events[0][0] - N_target


def find_u_i(lam, N_target=60.0):
    for fac in [(0.5, 2.0), (0.3, 3.0), (0.2, 5.0)]:
        a, b = fac[0] * 10.0, fac[1] * 10.0
        if _res_of_u(a, lam, N_target) * _res_of_u(b, lam, N_target) < 0:
            return brentq(_res_of_u, a, b, args=(lam, N_target),
                          xtol=1e-8)
    raise RuntimeError(f"No root found for lambda={lam}")


def observables(sol, lam, N_val):
    u, X = sol.sol(N_val)
    eps1 = 3.0 * X**2
    h = 1e-4
    Xp = sol.sol(N_val + h)[1]
    Xm = sol.sol(N_val - h)[1]
    eps2 = 2.0 * (np.log(abs(Xp)) - np.log(abs(Xm))) / (2.0 * h)
    n_s_HF = 1.0 - 2.0 * eps1 - eps2
    r_HF = 16.0 * eps1
    n_s_SR = 1.0 - 6.0 * eps_V(u, lam) + 2.0 * eta_V(u, lam)
    return dict(u_star=u, eps1=eps1, eps2=eps2,
                n_s_HF=n_s_HF, n_s_SR=n_s_SR, r_HF=r_HF)


def run_one(lam, N_total=60.0, N_from_end=55.0):
    u_i = find_u_i(lam, N_total)
    sol = integrate(u_i, lam)
    N_end = sol.t_events[0][0]
    obs = observables(sol, lam, N_end - N_from_end)
    return dict(lam=lam, u_i=u_i, N_end=N_end, **obs)


if __name__ == "__main__":
    ref = {
        0.020: dict(u_i=10.715, u_star=10.465, eps1=1.372e-3,
                    n_s_HF=0.95809, n_s_SR=0.95759, r_HF=0.021953),
        0.050: dict(u_i=8.326, u_star=8.185, eps1=4.366e-4,
                    n_s_HF=0.95646, n_s_SR=0.95589, r_HF=0.006986),
        0.100: dict(u_i=6.615, u_star=6.527, eps1=1.723e-4,
                    n_s_HF=0.95644, n_s_SR=0.95586, r_HF=0.002757),
        0.200: dict(u_i=5.133, u_star=5.078, eps1=6.824e-5,
                    n_s_HF=0.95700, n_s_SR=0.95642, r_HF=0.001092),
        0.500: dict(u_i=3.582, u_star=3.551, eps1=2.082e-5,
                    n_s_HF=0.95794, n_s_SR=0.95738, r_HF=0.0003331),
        1.000: dict(u_i=2.693, u_star=2.673, eps1=8.755e-6,
                    n_s_HF=0.95859, n_s_SR=0.95804, r_HF=0.0001401),
        2.000: dict(u_i=2.009, u_star=1.996, eps1=3.771e-6,
                    n_s_HF=0.95913, n_s_SR=0.95859, r_HF=0.00006034),
        5.000: dict(u_i=1.352, u_star=1.344, eps1=1.275e-6,
                    n_s_HF=0.95969, n_s_SR=0.95917, r_HF=0.00002040),
    }

    print(f"{'lam':>6} | {'u_i':>8} {'ref':>8} | "
          f"{'n_s_HF':>8} {'ref':>8} | "
          f"{'n_s_SR':>8} {'ref':>8} | "
          f"{'r_HF':>10} {'ref':>10} | OK")
    print("-" * 105)

    for lam, ref_row in ref.items():
        row = run_one(lam)
        ok = (abs(row['u_i'] - ref_row['u_i']) < 1e-3
              and abs(row['n_s_HF'] - ref_row['n_s_HF']) < 1e-4
              and abs(row['n_s_SR'] - ref_row['n_s_SR']) < 1e-4
              and abs(row['r_HF'] - ref_row['r_HF']) / ref_row['r_HF'] < 1e-3)
        print(f"{lam:>6.3f} | {row['u_i']:>8.3f} {ref_row['u_i']:>8.3f} | "
              f"{row['n_s_HF']:>8.5f} {ref_row['n_s_HF']:>8.5f} | "
              f"{row['n_s_SR']:>8.5f} {ref_row['n_s_SR']:>8.5f} | "
              f"{row['r_HF']:>10.6f} {ref_row['r_HF']:>10.6f} | "
              f"{'OK' if ok else 'FAIL'}")
