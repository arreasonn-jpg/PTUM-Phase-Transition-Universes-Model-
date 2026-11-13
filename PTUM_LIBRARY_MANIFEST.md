# PTUM Library Package Manifest

**Review snapshot:** 2026-11-13  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-

## Tracked manuscript/library assets

The repository contains the manuscript source `main.tex`, a historical
`main.pdf`, figure PDFs under `figures/`, the journal class files,
cover-letter/highlights material, and the supplementary-note source/PDF.
The tracked `main.pdf` predates the current scientific corrections and
must not be treated as the current compiled manuscript. A fresh PDF must
come from a successful CI LaTeX artifact.

Generated LaTeX auxiliary files, temporary compile logs, and stale
homogeneous-scan JSON outputs are not source artifacts and are excluded
from the scientific correction branch. The CI workflow publishes fresh
build and scan outputs as workflow artifacts when those jobs complete.

## Scientific source modules

The current correction branch also contains:
- `ptum_task1_simulation.py`: homogeneous two-field background model;
- `ptum_inflation_background.py`: exact single-field inflation endpoint and post-end trajectory matching;
- `ptum_task1_scan.py`: 100-trajectory homogeneous post-threshold sensitivity scan;
- `ptum_floquet.py`: frozen Mathieu monodromy, linear expanding-background mode evolution, and finite-band momentum integration;
- `ptum_covariant_action.py`: algebraic gauge-representation and operator-dimension registry;
- `tests/test_ptum_consistency.py`: 51 regression tests on the current branch;
- `PTUM_10_OF_10_ACCEPTANCE.md`: evidence gates and current scientific status.

These modules do not collectively constitute a self-consistent nonlinear
waterfall/reheating/relic-abundance simulation. See
`PTUM_CLAIM_BOUNDARY.md` and `PTUM_REPRODUCIBILITY_NOTES.md`.

## CLASS/Cobaya code-availability status

Historical package metadata referenced
`https://github.com/ErdemEsa/ptum-cosmology.git`. That URL returned
HTTP 404 through the 2026-11-13 repository API review. The current
canonical repository inventory does not expose the CLASS v3.2.0 patch
as an individually reviewable tracked source file. A `PTUM.zip`
archive name is not proof of its contents; the archive was not inspected
in this review.

Therefore public availability and clean-tree apply verification of the
CLASS patch are **UNVERIFIED**. The exact patch, target CLASS commit,
checksum, apply command, build log, production Cobaya configurations,
and full chains are still required for an independent reproduction.

## Reproducibility boundary

The Python environment is pinned in `requirements-ci.txt`, and the
scientific workflow is defined in
`.github/workflows/ptum-scientific-tests.yml`. The current branch has
51 regression tests, but the latest full CI run is pending at this
snapshot. The 100-trajectory scan and current LaTeX build are not yet
claimed as passing.

Passing CI is necessary but insufficient for 10/10. The remaining
physics gates include coupled quantum-seeded inhomogeneous waterfall
dynamics, backreaction/rescattering, converged expanding-background
mode production, a microscopic proxy-fluid realization, reheating and
entropy history, and independent CLASS/Cobaya reproduction.
