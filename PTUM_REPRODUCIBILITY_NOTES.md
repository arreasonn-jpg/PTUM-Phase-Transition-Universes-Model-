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


## Full high-resolution scan execution snapshot (2026-11-14)

The full-scan execution branch ptum/full-scan-2026-11-14 was created
from PR head f50e962b38deb991daedfce425c9a278c84d9f80. It differs from
that head only by this execution record. The workflow is configured to
run the full 5x5x2 initial-condition grid at each of the two energy
scales (100 trajectories total), with 4001 output samples per
trajectory over 20 mu^-1 and per-trajectory atomic checkpoints.

The purpose of this isolated branch is to obtain the complete scan
artifact without changing the draft PR branch or main. The full result
is not accepted until the workflow completes, the final JSON and any
checkpoint are downloaded and validated for exactly 100 unique rows,
all integrations succeed, and the data are inspected. A partial
checkpoint is evidence of progress only, not a completed scan.
