# PTUM waterfall scan baseline: 2026-11-14

## Reproducibility record

- Workflow run: [#43535578775](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/43535578775)
- Code commit: `01ca4bf0a9458d811bd3ec492d5b206666ad91df`
- Integrator: DOP853 in dimensionless variables
- Dimensionless time: `tau = mu * t`
- Baseline horizon: `tau_max = 20`
- Output samples per trajectory: `4001`
- Trajectories: `100/100` successful; aggregation passed

## Baseline classification

| Scenario | Successful | Non-quartic | Insufficient late-time data |
|---|---:|---:|---:|
| High-scale threshold-matched | 50 | 48 | 2 |
| Low-scale underdamped control | 50 | 43 | 7 |
| Total | 100 | 91 | 9 |

No trajectory was certified as quartic in this baseline scan. The classifier was intentionally not relaxed: it requires the quartic energy/virial/EOS conditions and at least three complete late-time half-cycles with a valid adiabaticity diagnostic.

The low-scale grid contains promising quartic-like candidates. For example, trajectory 98 reported `Q_final ~= 11.12`, `w_final ~= 0.363`, and `virial_final ~= 0.890`, but only two complete late-time half-cycles were available, so the classifier withheld a quartic label.

## Numerical consistency

- Maximum relative FRW continuity residual, high-scale scenario: `1.77e-10`
- Maximum relative FRW continuity residual, low-scale scenario: `5.46e-15`
- The previous overflow case, trajectory 72, now completes successfully with finite output.
- Previously cancelled trajectories 20 and 70 also complete successfully.

## Follow-up

The workflow has been configured to rerun the full 100-point grid with `tau_max = 60` and `12001` output samples. This longer horizon is intended to test whether quartic-like candidates accumulate enough late-time cycles to pass the existing classifier. No extended-horizon result is claimed until that run and aggregation complete.

The homogeneous scan is a classical two-field truncation. It is not a quantum-vacuum-seeded inhomogeneous lattice calculation and does not establish a relic-abundance prediction.


## Workflow correction

The extended scan command is kept as plain shell arguments. YAML comments are placed outside the folded shell command so they cannot swallow the time-horizon or output-path arguments.
