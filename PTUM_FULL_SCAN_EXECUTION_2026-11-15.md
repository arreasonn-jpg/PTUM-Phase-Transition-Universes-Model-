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


## 2026-11-15 isolated Radau rerun

The preceding full-scan workflow `43701420639` ran on source
`af9724092c94d8469fcf23a87f29438b2cf8c58a` with DOP853 and a
100000-RHS budget, despite the later intended Radau profile. Its
artifact contained 100 rows: 97 successful integrations and three
failed integrations (two work-budget exhaustions and one non-finite
total-density failure). The artifact digest was
`sha256:4f98f4320ff5cfccb2917607270a8be86ee20eb9ed21b1e71ec8441660ce5722`.
It is retained as a diagnostic failure record, not a converged scan.
Among its 97 successful rows, no row met the joint quartic classifier:
the high-scale scenario had 47 non-quartic and 2 insufficient-data
rows; the low-scale scenario had 41 non-quartic and 7 insufficient-data
rows. This old run does not validate the current Radau profile.

A new isolated execution branch,
`ptum/full-scan-2026-11-15-r3`, is based on PR #2 source
`ca053f58e3713b274e22f0d69bd5ca89863dab26`. The branch-only manifest
commit does not alter the scan implementation. Its push triggers the
workflow's current Radau command:
`--max-rhs-evaluations 1000000 --rtol 1e-9 --atol 1e-12 --solver-method Radau`.
The run must still complete all 100 integrations without failures and
produce a strict-JSON artifact before it can be considered a complete
homogeneous scan. It remains a post-threshold classical sensitivity
scan, not an inhomogeneous quantum-seeded waterfall or a relic
calculation.
