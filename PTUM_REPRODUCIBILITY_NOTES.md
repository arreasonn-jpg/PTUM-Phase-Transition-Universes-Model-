# PTUM Reproducibility Notes

## Public repository

```text
https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-
```

## Current public code status

```text
Manuscript archive: public
Final figure artifacts: public
Claim-boundary notes: public
CLASS v3.2.0 PTUM patch: public
Patch apply check: PASS, against a clean CLASS v3.2.0 tree
Cobaya production YAML files: pending
Full MCMC chains: pending or external archive
```

The repository includes a clean path-limited PTUM patch for `CLASS v3.2.0`. The patch implements the proxy-fluid dark-radiation sector used in the manuscript by introducing `Delta_N_fluid`, the corresponding background contribution, and the linear perturbation variables for the perfect-fluid component.

## Verification status in the current repository review (2026-11-13)

The legacy URL above, `https://github.com/ErdemEsa/ptum-cosmology.git`,
returned HTTP 404 through the GitHub repository API during this review.
This does not establish whether the repository is private, renamed, or
otherwise inaccessible; it means its contents and public accessibility
could not be verified from the present connection.

The current PTUM repository root contains a binary `PTUM.zip`, but the
tracked file list does not expose the CLASS patch as an individually
reviewable source file. The archive contents were not inspected in this
review. Therefore the claim that the CLASS v3.2.0 patch is publicly
available and apply-check verified is currently **UNVERIFIED** from the
canonical repository snapshot. To restore a reproducibility claim, add
the exact patch file and its target CLASS version, checksum, apply
command, and clean-tree test log to this repository, or provide a
verifiable accessible archive/repository location.

## Remaining public reproducibility items

```text
1. Add production Cobaya YAML files.
2. Add full MCMC chain summaries or external archive links.
3. Optionally add CI/build logs for patched CLASS.
```

## Claim boundary

The CLASS implementation side is now publicly inspectable through the patch. The full Bayesian pipeline should not yet be described as completely end-to-end public until the production Cobaya configuration files and MCMC chains are released.


## Current scientific correction branches

- Scientific consistency and simulation corrections: PR #2
  https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/pull/2
- Dependent residual-potential, radiation-budget, EFT and linear-mode audit:
  branch `ptum/claims-and-eft-dimensional-audit-v2-2026-11-13`
  (PR creation pending).

The latest completed scientific-base test step passed 43 tests and the
LaTeX build passed. The 100-trajectory scan was cancelled before
completion once and is being rerun with a 45-minute timeout and
per-ten-trajectory progress logging. The dependent audit branch contains
54 tests (43 base plus 11 new regressions); its combined CI run has not
yet completed. Do not claim full CI-green status until the scan artifact,
all 54 tests, and the LaTeX build have been inspected.
