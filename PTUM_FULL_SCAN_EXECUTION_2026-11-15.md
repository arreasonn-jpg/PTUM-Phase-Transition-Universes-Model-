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


## 2026-11-15 completed DOP853 attempt and current Radau rerun

The completed DOP853 attempt is workflow 43701420639 on source
af9724092c94d8469fcf23a87f29438b2cf8c58a. The actual job log and
artifact metadata show DOP853 with a 100000-RHS budget. The artifact
contains 100 strict-JSON rows: 97 successful and three failed
(two budget exhaustions at 100001 calls and one non-finite total
density). No successful row satisfies quartic_achieved. The
high-scale successful classifications are 47 non_quartic and two
insufficient_oscillation_data; the low-scale successful
classifications are 41 non_quartic and seven
insufficient_oscillation_data. The artifact SHA-256 is
4f98f4320ff5cfccb2917607270a8be86ee20eb9ed21b1e71ec8441660ce5722.

This attempt is not current-source validation. A 21-commit comparison
from af9724092c94d8469fcf23a87f29438b2cf8c58a to
ca053f58e3713b274e22f0d69bd5ca89863dab26 confirms that both the scan
runner and simulation implementation changed, together with the
workflow. The old results are retained only as a diagnostic record.

A new full scan is queued from the current PR branch by a
synchronize event carrying the temporary [FULL-SCAN] title marker.
Workflow 43703837000 is expected to use the current workflow command:
Radau, rtol=1e-9, atol=1e-12 and a 1000000-RHS per-trajectory
engineering guard. The title marker has been removed after the
synchronize event was queued. The new artifact and job logs must be
inspected before accepting any result. A complete scan requires all
100 integrations to succeed; a failed row is not classified as a
physical regime.
