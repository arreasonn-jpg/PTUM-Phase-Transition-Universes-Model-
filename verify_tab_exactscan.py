#!/usr/bin/env python3
"""
Independent verification of tab:exactscan from main.tex Section 3.3.

This is a standalone verification script, NOT a replacement for
ptum_inflation_background.py. It independently re-derives the eight-row
scan from first principles and compares against the paper table.

The canonical background solver used by ptum_task1_scan.py and
ptum_waterfall_modes.py remains ptum_inflation_background.py.

This file exists for the reproducibility record: it demonstrates that
the paper table can be reproduced from the stated equations without
relying on the production module.

Run directly:
    python verify_tab_exactscan.py
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

M_PL = 2.435e18


def V(u, lam):      return 1.0 - np.exp(-lam * u**2)
def dV(u, lam):     return 2.0 * lam * u * np.exp(-lam * u**2)
def d2V(u, lam):    return 2.0 * lam * np.exp(-lam * u**2) * (1.0 - 2.0 * lam * u**2)
def s(u, lam):      return -dV(u, lam) / V(u, lam)
def eps_V(u, lam):  return 0.5 * s(u, lam)**2
def eta_V(u, lam):  return d2V(u, lam) / V(u, lam)


def rhs(N, y, lam):
    u, X = y
    return [np.sqrt(6.0) * X,
            (1.0 - X**2) * (np.sqrt(1.5) * s(u, lam) - 3.0 * X)]


def end_ev(N, y, lam): return 3.0 * y[1]**2 - 1.0
end_ev.terminal = True
end_ev.direction = 1


def integrate(u_i, lam, max_N=300.0):
    X_i = s(u_i, lam) / np.sqrt(6.0)
    return solve_ivp(rhs, [0, max_N], [u_i, X_i], args=(lam,),
                     events=end_ev, method="DOP853",
                     rtol=1e-10, atol=1e-12, dense_output=True)


def res_of_u(u, lam, N_target):
    X0 = s(u, lam) / np.sqrt(6.0)
    if 3.0 * X0**2 >= 1.0:
        return -N_target
    sol = integrate(u, lam)
    if len(sol.t_events[0]) == 0:
        return 1e6
    return sol.t_events[0][0] - N_target


def find_u_i(lam, N_target=60.0):
    import numpy as np
    # Log-space grid + bracket search (same approach as Colab verification)
    grid = np.logspace(np.log10(0.3), np.log10(30.0), 40)
    vals = [res_of_u(u, lam, N_target) for u in grid]
    for i in range(len(grid) - 1):
        if vals[i] * vals[i+1] < 0:
            return brentq(res_of_u, grid[i], grid[i+1],
                          args=(lam, N_target), xtol=1e-8)
    raise RuntimeError(f"No root for lambda={lam}")


def observables(sol, lam, N_val):
    u, X = sol.sol(N_val)
    eps1 = 3.0 * X**2
    h = 1e-4
    Xp = sol.sol(N_val + h)[1]
    Xm = sol.sol(N_val - h)[1]
    eps2 = 2.0 * (np.log(abs(Xp)) - np.log(abs(Xm))) / (2.0 * h)
    return dict(
        u_star=u, eps1=eps1, eps2=eps2,
        n_s_HF=1.0 - 2.0 * eps1 - eps2,
        n_s_SR=1.0 - 6.0 * eps_V(u, lam) + 2.0 * eta_V(u, lam),
        r_HF=16.0 * eps1,
    )


def run_one(lam, N_total=60.0, N_from_end=55.0):
    u_i = find_u_i(lam, N_total)
    sol = integrate(u_i, lam)
    N_end = sol.t_events[0][0]
    obs = observables(sol, lam, N_end - N_from_end)
    return dict(lam=lam, u_i=u_i, N_end=N_end, **obs)


if __name__ == "__main__":
    ref = {
        0.020: dict(u_i=10.715, n_s_HF=0.95809, n_s_SR=0.95759, r_HF=0.021953),
        0.050: dict(u_i=8.326,  n_s_HF=0.95646, n_s_SR=0.95589, r_HF=0.006986),
        0.100: dict(u_i=6.615,  n_s_HF=0.95644, n_s_SR=0.95586, r_HF=0.002757),
        0.200: dict(u_i=5.133,  n_s_HF=0.95700, n_s_SR=0.95642, r_HF=0.001092),
        0.500: dict(u_i=3.582,  n_s_HF=0.95794, n_s_SR=0.95738, r_HF=0.0003331),
        1.000: dict(u_i=2.693,  n_s_HF=0.95859, n_s_SR=0.95804, r_HF=0.0001401),
        2.000: dict(u_i=2.009,  n_s_HF=0.95913, n_s_SR=0.95859, r_HF=0.00006034),
        5.000: dict(u_i=1.352,  n_s_HF=0.95969, n_s_SR=0.95917, r_HF=0.00002040),
    }

    print(f"{'lam':>6} | {'u_i':>8} {'ref':>8} | "
          f"{'n_s_HF':>8} {'ref':>8} | {'r_HF':>10} {'ref':>10} | OK")
    print("-" * 90)

    n_ok = 0
    for lam, r in ref.items():
        row = run_one(lam)
        ok = (abs(row['u_i'] - r['u_i']) < 1e-3
              and abs(row['n_s_HF'] - r['n_s_HF']) < 1e-4
              and abs(row['r_HF'] - r['r_HF']) / r['r_HF'] < 1e-3)
        n_ok += int(ok)
        print(f"{lam:>6.3f} | {row['u_i']:>8.3f} {r['u_i']:>8.3f} | "
              f"{row['n_s_HF']:>8.5f} {r['n_s_HF']:>8.5f} | "
              f"{row['r_HF']:>10.6f} {r['r_HF']:>10.6f} | "
              f"{'OK' if ok else 'FAIL'}")

    print(f"\n{n_ok}/{len(ref)} verified")
