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

The canonical repository for this review is
`https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-`.
The older `https://github.com/ErdemEsa/ptum-cosmology.git` reference
returned HTTP 404 through the GitHub repository API. This does not
establish whether the legacy repository is private, renamed, or
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


## Current correction branches

- Scientific consistency and simulation corrections: PR #2
  https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/pull/2
- Dependent claims, EFT, residual-potential and linear-mode corrections: PR #3
  https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/pull/3

The latest completed test step on the PR #2 branch passed 35 tests and
the LaTeX build passed; the 100-trajectory scan was still running at
the last check. PR #3 currently contains 46 tests, but its full CI run
is pending because it is based on the PR #2 branch. Do not describe
either branch as fully CI-green until the 100-trajectory artifact and
the PR #3 suite are completed and inspected.
