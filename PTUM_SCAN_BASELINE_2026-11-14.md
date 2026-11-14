# PTUM waterfall scan baseline: 2026-11-14

## Latest reproducibility record

- Full-grid workflow: [#43567382554](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/43567382554)
- Full-grid code commit: `366257f78be5a5794e4231cb8c50b1c375785c68`
- Latest regression + manuscript workflow: [#43568345144](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/43568345144)
- Latest targeted follow-up: [#43568345159](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/43568345159)
- Current reviewed branch head at this update: `0e214d81707c464fb4bdbfc55be45c1d8113f727`
- Integrator: DOP853 in dimensionless variables
- Dimensionless time: `tau = mu * t`
- Full-grid horizon: `tau_max = 120`
- Full-grid output samples per trajectory: `24001`
- Full-grid result: **100/100 trajectories successful; aggregation passed**
- Regression suite: **81 passed**
- LaTeX manuscript build: **passed**

## Full-grid late-time classification

| Scenario | Successful | Non-quartic | Insufficient oscillation data | Transient quartic-like episodes |
|---|---:|---:|---:|---:|
| High-scale threshold-matched | 50 | 48 | 2 | 0 |
| Low-scale underdamped control | 50 | 48 | 2 | 5 |
| Total | 100 | 96 | 4 | 5 |

No trajectory was certified as a sustained late-time quartic regime. The four `insufficient_oscillation_data` rows are the exact classical invariant controls with `psi_init = psi_dot_init = 0`; the homogeneous solution remains exactly `psi = psi_dot = 0`. They are not failed integrations and are not quantum-vacuum seeds.

The transient diagnostic is separate from the late-time classifier. It requires, in the same complete half-cycle, quartic energy dominance, (w) close to (1/3), virial balance, and (H/\omega < 0.1), with at least three consecutive qualifying half-cycles.

## Long-horizon follow-up of the five transient candidates

The ten low-scale trajectories with seed index 4 (trajectory indices 90--99) were rerun to `tau_max = 240` with `48001` output samples each. The follow-up aggregate passed: **10/10 successful**.

- Sustained late-time quartic classifications: **0/10**
- Transient quartic-like episodes: **5/10**, at indices 90, 92, 94, 96 and 98
- The paired larger-offset cases 91, 93, 95, 97 and 99 showed no qualifying transient episode.
- Episode end times are approximately 34.26, 37.44, 37.41, 35.73 and 39.77 in units of (\mu^{-1}).
- At (\tau=240), the five episode-bearing trajectories remain non-quartic: (w_{\rm final}\simeq0.389\)--0.400, (Q_{\rm final}\simeq2.167\)--2.231, and virial ratios (\simeq0.526\)--0.539.

Thus the transient episode is real within the stated linear/homogeneous diagnostics, but it does not evolve into a sustained late-time quartic regime over the tested horizon. It is not evidence of an attractor.

## Numerical consistency and turning-point correction

- Full-grid maximum relative FRW continuity residual: (4.16\times10^{-10})
- Full-grid median relative FRW continuity residual: (1.26\times10^{-11})
- Targeted follow-up maximum relative FRW continuity residual: (6.27\times10^{-15})
- Trajectory 72, which previously overflowed, completes with finite output under dimensionless integration.
- The oscillation diagnostics now share a robust turning-point detector. It interpolates sign reversals, excludes tangential zero touches and unbracketed final zeros, and treats an exactly zero initial velocity as the prescribed initial turning point.
- The regression suite tests the turning-point edge cases and the exact homogeneous invariant branch.

## Evidence boundary

The 100-row scan is a homogeneous post-threshold sensitivity study. It is not a coupled quantum-seeded nonlinear waterfall calculation and does not include backreaction, rescattering, fragmentation, defect evolution, or a self-consistent reheating history.

The separate `ptum_waterfall_modes.py` module evolves linear modes with an adiabatic vacuum on a prescribed single-field FRW background and checks the Wronskian. It does not close the nonlinear or backreaction gaps.

