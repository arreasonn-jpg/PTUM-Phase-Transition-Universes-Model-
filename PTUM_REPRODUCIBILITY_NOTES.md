# PTUM Reproducibility Notes

## Public repository

```text
https://github.com/ErdemEsa/ptum-cosmology.git
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

## Remaining public reproducibility items

```text
1. Add production Cobaya YAML files.
2. Add full MCMC chain summaries or external archive links.
3. Optionally add CI/build logs for patched CLASS.
```

## Claim boundary

The CLASS implementation side is now publicly inspectable through the patch. The full Bayesian pipeline should not yet be described as completely end-to-end public until the production Cobaya configuration files and MCMC chains are released.
