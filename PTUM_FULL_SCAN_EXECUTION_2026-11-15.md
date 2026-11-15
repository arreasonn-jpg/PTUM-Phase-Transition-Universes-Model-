# PTUM full homogeneous scan execution manifest

- Source branch: `ptum/scientific-consistency-fixes-2026-11-13`
- Source commit before this manifest: `a0cb59a47f1b4c8ad461b4804c19bc164615f9e8`; the current Radau rerun includes subsequent solver-method and final-state audit commits.
- Scan command:
  `python ptum_task1_scan.py --profile full --output task1_parameter_scan_results.json --checkpoint task1_parameter_scan_checkpoint.json --max-rhs-evaluations 1000000 --rtol 1e-9 --atol 1e-12 --solver-method Radau`
- Scenarios: two energy scales, 50 trajectories each (100 total)
- Grid per scenario: 5 seed scales x 5 velocity scales x 2 post-threshold offsets
- Output grid: 4001 samples over 20 mu^-1 per trajectory
- Integrator: Radau (implicit solver cross-check)
- Solver tolerances: rtol=1e-9, atol=1e-12
- Work guard: 1000000 RHS evaluations per trajectory for this diagnostic rerun

The previous 100-row run at a 100000-call budget completed 97 rows and
recorded three failed rows: two exhausted the work budget and one
encountered non-finite total density. The higher cap is a diagnostic rerun, and Radau is used as an independent
implicit solver cross-check against the earlier DOP853 run. It does not
turn budget exhaustion into success or relax solver tolerances. The
non-finite-state failure is now annotated with field values and RHS
work count. All failed rows remain excluded from physical classification.

This is a homogeneous post-threshold sensitivity scan, not a coupled
threshold-crossing calculation, quantum-vacuum-seeded inhomogeneous
waterfall, nonlinear lattice simulation, or relic-abundance calculation.
No physical acceptance gate is promoted by the scan alone.

The solver method, RHS evaluation count and failure-state fields are preserved in each row so the DOP853/Radau comparison can be audited.
