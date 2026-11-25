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


The first current-source trigger attempt was workflow 43703837000.
Its Python regression and smoke jobs passed, but the
full-waterfall-scan job was skipped. The temporary title marker was
restored before GitHub evaluated the synchronize event, so this attempt
did not launch the Radau scan. No scan result is inferred from it.
The next synchronize event is being queued while the marker remains
present; the title will be restored only after the full-scan job is
confirmed queued or in progress.


## 2026-11-15 current-source DOP853 result (workflow 43753469944)

The stale DOP853 execution branch was superseded by isolated PR #7,
created from current PR #2 source commit
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`. The workflow ran the
full profile with DOP853, `rtol=1e-9`, `atol=1e-12`,
4001 output samples over `20 mu^-1`, and the unchanged
1,000,000-RHS per-trajectory guard.

The workflow's full-scan job completed 100/100 integrations:
- High-scale threshold-matched: 50/50 success; 48 non_quartic,
  two insufficient_oscillation_data.
- Low-scale underdamped control: 50/50 success; 43 non_quartic,
  seven insufficient_oscillation_data.
- No row passed the joint quartic classifier.
- The two initial-condition rows that exhausted the Radau and BDF
  budgets completed under DOP853 with 7,718 and 1,334 RHS evaluations.
  Both DOP853 rows are non_quartic; no successful Radau/BDF values
  exist for those two rows.

The DOP853 ZIP digest is
`sha256:3e758909f191c863b358424be0d7d86a253224fe066e3ceaa279368719e39c8b`.
The extracted strict-JSON result digest is
`sha256:e848ff87c8fa3741d65f5fd2909d56db4af567a903d4dc05845cb081d175372c`.
The JSON contains exactly 100 rows and rejects non-standard NaN/Infinity
constants.

The Radau, BDF and DOP853 artifacts have the same ordered 100-row
initial-condition grid. All 98 rows successful under all three methods
have identical regime labels. DOP853 versus Radau maximum relative
differences on those 98 rows are 3.16e-9 in Phi, 1.18e-7 in Phi_dot,
4.77e-7 in psi, 9.12e-6 in psi_dot, 2.86e-10 in H, and
5.72e-10 in total density. Q, averaged w and virial diagnostics
agree within 5.95e-8, 1.81e-8 and 1.77e-7. These comparisons do
not include the two DOP853-only rows and do not replace tolerance
or output-grid convergence.

Workflow 43753469944 also passed all 103 Python tests, the four-row
two-scale smoke scan and the LaTeX build. The execution-only PR #7
was closed without merging after artifact inspection. The earlier
stale DOP853 PR #6 was also closed without merging. No changes were
made to main.

Interpretation remains limited to this homogeneous post-threshold
grid. No quartic proxy-fluid realization, coupled threshold crossing,
quantum-seeded inhomogeneous waterfall, nonlinear backreaction,
rescattering, relic abundance or observational reproduction is
established.


## Targeted DOP853 convergence follow-up (workflow 43754922200)

A separate convergence-only workflow ran 36/36 integrations over four
representative trajectories: both DOP853-only rows and two high-Q
controls. The tolerance ladder was 1e-9/1e-12, 1e-10/1e-13 and
1e-11/1e-14. Output grids ranged from 4,001 to 256,001 points.

All four cases passed the script's provisional targeted stability
limits. Across tolerances, the maximum final-state relative difference
was 4.75e-7 and the maximum classification-diagnostic relative
difference was 3.48e-7. Across the final output-grid doubling
128,001 -> 256,001, all four regime labels, quartic flags and
late-half-cycle counts were unchanged. Maximum absolute changes were
7.57e-4 in Q_final, 2.57e-4 in w_final, 2.25e-4 in virial_final,
and 6.05e-4 in the maximum finite-difference continuity diagnostic.

The targeted convergence artifact ZIP digest is
`sha256:d4f80abf0e2705d3d019e67855592efaf7242ee96a90f970798119748a6bfe51`;
the extracted strict-JSON digest is
`sha256:f99e7da8644c399e3bb5ff6d6b08cbffe272ab75c99faad311689fa283a71899`.
The workflow passed 107 Python tests and the LaTeX build. Final LaTeX
pass has 73 Underfull hbox warnings, with no Overfull hboxes or
unresolved references/citations.

This is not a full 100-row convergence proof. Gate 4 remains PARTIAL.


## 2026-11-25 fresh exact-endpoint 100-row scan queued

A new full scan is being triggered from the current authorized PR #2
branch because older 100-row artifacts predate later equation,
threshold and diagnostic changes. The current source derives
\(\Phi_c\) from
\(\texttt{compute\_observables}(0.02,n_{\rm target}=60,n_*=55)\)
through the exact Hubble-flow endpoint, then sets
\(\Phi_c=x_{\rm end,H}M_{\rm Pl}\) in both scan scenarios.

The current scan contract is:
- two energy scales: \(V_0=10^{64}\) and \(10^{56}\ {\rm GeV}^4\);
- 50 initial conditions per scale, the full \(5\times5\times2\)
  seed/velocity/threshold-offset grid, 100 unique row keys total;
- homogeneous post-threshold trajectories over \(20\,\mu^{-1}\),
  4,001 output points, DOP853, \(rtol=10^{-9}\),
  \(atol=10^{-12}\), and a 1,000,000-RHS fail-closed guard;
- a paired full-grid study on the same 100 initial conditions:
  4,001 versus 256,001 output points and successive tolerance pairs
  \((10^{-9},10^{-12})\), \((10^{-10},10^{-13})\),
  \((10^{-11},10^{-14})\), and \((10^{-12},10^{-15})\);
- a separate 36-run targeted convergence probe on representative
  trajectories.

The source explicitly sets quantum_vacuum_seeded=false. This remains
a homogeneous post-threshold classical sensitivity scan, not the
threshold crossing, a quantum vacuum ensemble, or an inhomogeneous
backreacting waterfall. No result is accepted until the full JSON
artifacts, row keys, failed integrations, all comparison tables and
strict convergence flags have been inspected. A failed or incomplete
row is not a physical classification.

The new run is triggered by the [FULL-SCAN] commit marker below.
At the time of this entry, the new artifacts do not yet exist.


## 2026-11-25 fresh exact-endpoint 100-row baseline scan

Workflow [45592679131](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45592679131), exact source head 4590fc37825399f668098bdf3177b261e60e071f, completed the baseline full scan:
- 100/100 integrations succeeded, zero failed rows; 50 rows in each scenario and 100 unique initial-condition keys.
- All rows use the exact threshold Phi_c/M_Pl = 0.9862280831209045, 4,001 output points over 20 mu^-1, DOP853, rtol=1e-9, atol=1e-12, and quantum_vacuum_seeded=false.
- Classification counts: high-scale threshold-matched, 48 non-quartic and 2 insufficient-oscillation rows, 0 quartic; low-scale underdamped control, 41 non-quartic, 4 insufficient-oscillation and 5 quartic rows. Overall: 89 non-quartic, 6 insufficient-oscillation, 5 quartic.
- Every quartic row lies in the low-scale control at the largest tested classical field seed (psi_init=5 psi_0) and the smaller offset (0.01 Phi_c). Their w_final spans 0.37218--0.37363, Q_final 10.651--11.071, virial ratio 0.90607--0.90962, and H/omega about 6.87e-5--7.01e-5. They are not quantum-vacuum-seeded attractor evidence.
- The strict JSON artifact was parsed with non-finite JSON constants rejected. ZIP SHA-256: 82d1771f15417d172152233fcd1c41fcec776df936b6b56dfc59f958dcc2556d; extracted result JSON SHA-256: 625873f9d761e6df694170c33efa02dc543464f87542d75f76ff747c856764e3.
- The maximum chain-rule FRW continuity residual was 1.33249e-10; the maximum sampled finite-difference residual ratio was 0.03723375. These are diagnostics of the homogeneous ODE/output-grid calculation, not a full inhomogeneous stress-tensor conservation result.
- Exact-head short checks passed: 211 Python cases, 4/4 two-scale smoke trajectories, targeted convergence job, 11-grid bare-WKB UV audit, and LaTeX build. The PDF is 48 pages; its final pass has zero Overfull boxes and zero unresolved references/citations, but 80 Underfull hbox warnings remain.
- The paired 100-row 4,001/256,001-point and four-level tolerance study was still running at the time of this record. No paired-convergence pass is inferred here.

Gate 4's fresh baseline sensitivity scan is verified, but the paired convergence job is still pending. Gate 5 remains NOT MET; the bare WKB UV audit still has no subtraction/counterterms or continuum limit. Gate 10 remains PARTIAL because the paired study and warning-free manuscript are outstanding.
