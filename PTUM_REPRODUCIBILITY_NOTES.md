# PTUM Reproducibility Notes

**Updated:** 2026-11-24  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-  
**Verified commit:** `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

## Reproduce the verified homogeneous calculation

The current repository provides:
- `ptum_task1_simulation.py`;
- `tests/test_ptum_task1_simulation.py`;
- `requirements` installed by the workflow (NumPy, SciPy, pytest);
- `.github/workflows/ptum-phi-psi-validation.yml`.

From a clean checkout with Python 3.11:

```bash
python -m pip install --upgrade pip numpy scipy pytest
python -m py_compile ptum_task1_simulation.py
pytest -q tests/test_ptum_task1_simulation.py
```

The workflow additionally runs the 18-point grid using:
- `psi_init = [0, 0.01 psi_0, 0.1 psi_0]`;
- `psi_dot_init = [0, 0.1 mu psi_0, mu psi_0]`;
- `phi_offset = [0.01 Phi_c, 0.1 Phi_c]`;
- `t_max = 4000`, `n_points = 40000`.

It requires 18/18 successful integrations and bounds the maximum relative residuals by 1e-5 (total continuity), 1e-4 (moving-minimum split continuity), and 1e-3 (dense state-derivative audit).

Workflow run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) passed all these gates. Its scan artifact is `ptum-phi-psi-18point-scan` (artifact SHA-256: `f13eb7a6c957d3ed08a93d330c0e4b81ef28d9b0b1e5cdbacd707e6e72bc1d6e`).

## What this reproduction establishes

It establishes numerical consistency of the declared homogeneous two-field truncation over the finite scan. The exact total Hilbert/Friedmann source is kept separate from the minimum-subtracted excitation diagnostic, and the moving-minimum contribution is included in the sector transfer bookkeeping.

The scan found 18/18 integrations successful, 2 exact zero-seed invariant solutions, 16 quadratic outcomes after leaving the tachyonic region, and no quartic-fluid outcome.

The current mass convention makes the tachyonic region `|Phi| > Phi_c`. The scan does not demonstrate a downhill post-inflationary entry into this region. That trigger-direction issue is a physical-model question, not a solver convergence issue.

## Not reproduced by this package

The following are outside the current workflow and must not be represented as independently reproduced:
- fresh LaTeX build of the latest manuscript;
- CLASS/Cobaya production pipeline, YAML files, likelihood versions, and full MCMC chains;
- inhomogeneous quantum-seeded lattice dynamics, backreaction, rescattering, fragmentation, and defect evolution;
- self-consistent reheating/thermalization/entropy history;
- dark-matter relic abundance;
- microscopic derivation of the proxy-fluid closure;
- UV completion or cosmological-constant solution.

The repository's tracked historical `main.pdf` is not, by itself, a fresh build artifact for the reviewed commit. The current CI workflow does not compile LaTeX.

## Reproducibility boundary

A passing finite homogeneous scan is necessary evidence for the implemented equations, but it is not a proof of the full cosmological scenario. Any expanded claim requires source, configuration, environment, seeds, raw output, checksums, and convergence evidence appropriate to that claim.
