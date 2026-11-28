# PTUM Reproducibility Notes

**Review snapshot:** 2026-11-13  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-

## 1. Public repository and historical reference

The active repository reviewed for this branch is:

```text
https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-
```

Earlier package metadata referenced:

```text
https://github.com/ErdemEsa/ptum-cosmology.git
```

The legacy URL returned HTTP 404 through the GitHub repository API during the 2026-11-13 review. This does not prove whether the repository is private, renamed, or deleted; its contents could not be verified from the current connection.

## 2. Evidence-based code availability

| Item | Current status | Evidence boundary |
|---|---|---|
| Manuscript source | Present | `main.tex` is tracked |
| Historical manuscript PDF | Present | `main.pdf` predates current branch corrections; not a current build |
| Figure artifacts | Present | Tracked under `figures/` |
| Scalar homogeneous simulation | Present | `ptum_task1_simulation.py` |
| Inflation background integrator | Present | `ptum_inflation_background.py` |
| High-resolution homogeneous scan runner | Present | `ptum_task1_scan.py`; expects 100 trajectories |
| Frozen Mathieu/Floquet solver | Present | `ptum_floquet.py` |
| Linear expanding-background mode solver | Present | `integrate_expanding_mode` in `ptum_floquet.py`; supplied backgrounds only |
| Finite-band momentum integration | Present | `integrate_expanding_spectrum`; no IR/UV extrapolation or convergence claim |
| Covariant action registry | Present | `ptum_covariant_action.py`; algebraic representation/dimension checks only |
| Python regression tests | Present | `tests/test_ptum_consistency.py`; 51 tests on current correction branch |
| CLASS v3.2.0 patch source | **UNVERIFIED / not individually exposed** | The tracked root inventory does not expose a reviewable patch file |
| PTUM.zip archive contents | **NOT INSPECTED** | Archive existence does not establish contents or patch validity |
| CLASS patch clean-tree apply check | **UNVERIFIED** | No accessible patch, checksum, target tree, or apply log was available |
| Production Cobaya YAML files | Pending / not verified | Not available as a complete public reproducibility package |
| Full MCMC chains | Pending or external archive | No independently reproducible chain package verified |

## 3. Current CI status

The workflow is `.github/workflows/ptum-scientific-tests.yml`; its Python dependencies are pinned in `requirements-ci.txt`.

Workflow run 43400134268 completed the then-current 43-test Python regression step successfully. Its LaTeX job failed because `main.tex` used `\mathscr D_\mu` without loading `mathrsfs`. The package has since been added, and regression tests now guard the package declaration and the SM Hilbert-tensor bookkeeping.

The current correction branch contains 51 tests and has triggered workflow run 43405427845. At the time of this snapshot, that run is pending. The newest 51-test suite, 100-trajectory scan, and LaTeX build are therefore **not yet verified as passing**. The earlier scan attempt was cancelled when a newer commit superseded its run, and no complete scan artifact was validated.

## 4. Requirements to make the CLASS/Cobaya claim reproducible

To claim that the CLASS v3.2.0 patch is publicly available and independently applicable, the repository must expose:

1. The exact patch file as a tracked, individually reviewable source file.
2. The exact upstream CLASS version and commit SHA.
3. A cryptographic checksum for the patch.
4. The clean-tree apply command.
5. A reproducible log showing the patch applies without conflicts.
6. A build/test command and successful output.
7. The exact production Cobaya YAML files, likelihood versions, dataset versions, parameter priors, and sampler settings.
8. Full chains or an accessible archival record with checksums and enough metadata to reproduce posterior summaries and model comparison.

Until these are available and independently rerun, the earlier statement that the CLASS v3.2.0 patch is public and apply-check verified must remain **UNVERIFIED**.

## 5. Reproduction commands

From a clean checkout of the correction branch:

```bash
python -m pip install -r requirements-ci.txt
python -m pytest -q tests/test_ptum_consistency.py
python ptum_task1_scan.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The 100-trajectory scan is a homogeneous post-threshold sensitivity study, not an inhomogeneous quantum-seeded waterfall simulation. Its output must be inspected and subjected to timestep, solver-tolerance, and output-grid convergence before any physical regime conclusion is accepted.

The expanding-background mode solver requires supplied histories (a(t),H(t),\Phi_{\rm res}(t)). It does not generate a self-consistent PTUM background, include backreaction/rescattering, or by itself yield a relic abundance.

## 6. Reproducibility boundary

A passing Python test suite is necessary but not sufficient. The project is not 10/10 until the latest CI and LaTeX build pass, the complete 100-trajectory scan is validated, all relevant numerical convergence studies are supplied, the CLASS/Cobaya pipeline is independently reproducible, and the microscopic waterfall, resonance, reheating, and proxy-fluid claims are supported by the required calculations.

## 2026-11-13 follow-up: nonlinear lattice status

The manuscript's former nonlinear-lattice subsection has been replaced.
The current canonical repository does not expose an individually
reviewable PTUM lattice solver, full run configuration, raw field
configurations, or diagnostic artifacts sufficient to reproduce the
previously described numerical outputs. Consequently, the historical
grid-size, energy-conservation, Floquet, relic-density, defect, and
entropy values are not treated as verified results. A future release
must provide the solver/version, action and discretization, physical
initial-state prescription and UV treatment, fixed seeds, energy
bookkeeping, raw outputs, checksums, and volume/grid/timestep/ensemble
convergence.

The current numerical evidence remains limited to the homogeneous
two-field background and linear modes on prescribed external
background histories. The proxy-fluid closure remains phenomenological.
Two regression tests now guard the manuscript's claim boundary; their
latest CI result is pending.


## 2026-11-15 current-source three-solver scan comparison

The full homogeneous post-threshold scan was run with Radau
(workflow 43703987436), BDF (workflow 43705977596) and DOP853
(workflow 43753469944). The current-source DOP853 execution branch
was created from PR #2 source commit
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`. The subsequent PR #2
changes through the audit update modify manuscript, tests and
documentation only; the scan and simulation implementation are
unchanged.

All three artifacts contain the same ordered 100-row initial-condition
grid. Radau and BDF each complete 98/100 integrations and hit the
1,000,000-RHS engineering guard on the same two rows. DOP853 completes
100/100 at the same `rtol=1e-9`, `atol=1e-12`, output grid and
RHS guard. The two DOP853-only rows are non_quartic, but they have
no successful Radau/BDF counterpart and therefore lack independent
cross-method validation.

Across the 98 rows successful under all three methods, all regime
labels are identical. DOP853/Radau maximum relative differences:
`final_Phi` 3.1589e-9, `final_Phi_dot` 1.1799e-7,
`final_psi` 4.7689e-7, `final_psi_dot` 9.1140e-6,
`final_H` 2.8607e-10, `final_rho_total` 5.7215e-10,
`w_final` 1.8036e-8, `Q_final` 5.9411e-8, and
`virial_final` 1.7698e-7. These are pairwise solver differences
on the common successful subset. They are not a substitute for
tighter-tolerance runs or output-grid convergence.

DOP853 regime counts are:
- High-scale threshold-matched: 48 non_quartic, 2
  insufficient_oscillation_data, zero quartic_achieved.
- Low-scale underdamped control: 43 non_quartic, 7
  insufficient_oscillation_data, zero quartic_achieved.

The full scan is now complete under DOP853 for the declared finite
homogeneous grid. It does not establish an inhomogeneous quantum-
seeded waterfall, backreaction, rescattering, a microscopic
proxy-fluid realization, relic abundance, or observational validity.


## Targeted DOP853 convergence artifact (workflow 43754922200)

The convergence-only workflow tested four representative trajectories
with 36 integrations: three tolerance pairs (1e-9/1e-12,
1e-10/1e-13, 1e-11/1e-14) and seven output grids
(4,001, 8,001, 16,001, 32,001, 64,001, 128,001, 256,001).
All 36 integrations succeeded and the script's targeted stability
flag is true for all four cases.

Across tolerance changes, maximum final-state relative difference
was 4.75e-7 and maximum relative difference in Q/w/virial diagnostics
was 3.48e-7. Across 128,001 -> 256,001 output samples, all regime
labels, quartic flags and late-half-cycle counts were unchanged.
Maximum absolute differences were 7.57e-4 in Q_final, 2.57e-4 in
w_final, 2.25e-4 in virial_final and 6.05e-4 in the maximum
finite-difference continuity diagnostic. The thresholds used are
provisional and apply only to these four selected trajectories:
1e-6 final-state relative, 1e-5 classification relative and 1e-3
absolute for the listed output-grid diagnostics.

Artifact ZIP SHA-256:
`d4f80abf0e2705d3d019e67855592efaf7242ee96a90f970798119748a6bfe51`.
Extracted JSON SHA-256:
`f99e7da8644c399e3bb5ff6d6b08cbffe272ab75c99faad311689fa283a71899`.

This targeted study does not establish convergence of the complete
100-row scan. It does not simulate an inhomogeneous quantum-seeded
waterfall or establish a relic abundance.


## 2026-11-27 exact-head repository and CI audit

**Source:** canonical branch head d2f15928ba6af8b75b0dc9d823d0a291acbf22f3.  
**Tracked tree:** 86 entries, recursive tree response not truncated.

The tracked tree contains PTUM.zip (6,248,335 bytes), the manuscript,
figures, Python modules, one CI workflow, and regression tests. Outside
that archive, the tree contains no individually reviewable CLASS patch
or diff, no production Cobaya YAML configuration, no MCMC chain files,
and no raw likelihood/data bundle. The archive exists, but its contents
remain unverified; its presence is not evidence that it contains a
valid patch or complete pipeline. No claim about the archive's internal
contents is made here.

Workflow 45971792497 ran on the exact source head above and completed
successfully:
- 227 Python tests passed.
- The four-trajectory, two-scale smoke scan completed 4/4 with zero
  integration failures. Its strict JSON contains no NaN/Infinity.
  Exact endpoint matching gives Phi_c/M_Pl=0.9862280831209068, and
  every row declares quantum_vacuum_seeded=false. The largest sampled
  chain-rule continuity residual is 3.3603e-12.
- The 11-grid bare-lattice UV audit passed as a diagnostic. It still
  records zero-point energy, with vacuum_subtraction_applied=false,
  counterterms_applied=false and continuum_limit_claimed=false.
- The manuscript built to a 49-page PDF. On the final LaTeX pass there
  were 79 Underfull hboxes, zero Overfull hboxes and no unresolved
  citations/references. Initial-pass forward-reference warnings were
  resolved on the second pass.

The full 100-row scan, full-grid convergence and scan-convergence jobs
were skipped by workflow conditions. Their earlier artifacts are not
revalidated by workflow 45971792497. This addendum supersedes the
historical 51-test/pending-CI snapshot above.

**Gate 9 remains NOT MET.** The exact CLASS upstream commit, patch
source/checksum, clean-tree apply/build log, production Cobaya YAMLs,
likelihood/data versions and independently rerunnable chains are still
not available as a verified package. No observational result is
reclassified as independently reproduced.


## 2026-11-27 exact-head software/build recheck

The branch head ce5c7fe40ab89ac2efa3a378df7344fea678d8ed was
verified by workflow [45973043125](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45973043125):
228 Python regression cases passed; the two-scale smoke scan completed
4/4 with zero failed integrations; the 11-grid bare-WKB UV audit passed;
and the 49-page manuscript PDF built. The final LaTeX pass retained
81 Underfull hboxes, zero Overfull hboxes, and zero unresolved
references/citations. The full 100-row scan and paired convergence jobs
were skipped on this test/documentation-only head. The bare-WKB audit
still retains zero-point energy, applies no vacuum subtraction or
counterterms, and makes no continuum-limit claim. The tracked PTUM.zip
archive remains uninspected; CLASS/Cobaya inputs and chains remain
unverified.
