# PTUM current-source DOP853 full-scan execution manifest

- Execution branch: `ptum/full-scan-2026-11-15-dop853-current`
- Exact source base: `bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`
- Source branch: `ptum/scientific-consistency-fixes-2026-11-13`
- This branch is created directly from the current PR #2 head. It is not based on the stale DOP853 execution branch.
- Solver: DOP853
- Tolerances: `rtol=1e-9`, `atol=1e-12`
- Time/output grid: 20 `mu^-1`, 4001 output points per trajectory
- Grid: 100 homogeneous post-threshold trajectories, two energy scales
- Work guard: unchanged `1,000,000` RHS evaluations per trajectory
- Command: `python ptum_task1_scan.py --profile full --output task1_parameter_scan_results.json --checkpoint task1_parameter_scan_checkpoint.json --max-rhs-evaluations 1000000 --rtol 1e-9 --atol 1e-12 --solver-method DOP853`

## Purpose

This is a same-source third-solver diagnostic against the archived Radau and BDF runs. The prior DOP853 execution branch was based on an earlier source commit and cannot serve as a valid comparison to the current PR #2 source. This run deliberately changes neither tolerances nor the RHS guard.

## Interpretation rules

- A trajectory that exhausts the RHS budget or encounters a numerical failure remains failed and unclassified.
- A complete scan requires all 100 integrations to succeed.
- Compare only common successful rows across solvers; report solver agreement separately from time-grid and tolerance convergence.
- The scan is homogeneous and post-threshold. It is not a coupled threshold-crossing calculation, quantum-vacuum-seeded inhomogeneous waterfall, nonlinear backreaction/rescattering calculation, or relic-abundance prediction.
- No scientific acceptance gate is promoted by this execution alone.
