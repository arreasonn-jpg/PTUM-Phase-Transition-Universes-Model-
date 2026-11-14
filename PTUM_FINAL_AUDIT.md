# PTUM Final Audit, Evidence-Corrected Snapshot

**Review date:** 2026-11-13  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-

## Package status

```text
Current manuscript source: present
Historical main.pdf: present, but predates current scientific corrections
Cover letter and highlights: present
Figure PDFs: present in figures/
Journal class files: present
Latest LaTeX build: PASS (workflow 43568345144)
Latest Python regression: 81 passed (workflow 43568345144)
100-trajectory scan at tau_max=120: PASS (workflow 43567382554)
10-trajectory follow-up at tau_max=240: PASS (workflow 43568345159)
```

## CLASS/Cobaya code availability

```text
Historical repository URL: https://github.com/ErdemEsa/ptum-cosmology.git
Historical URL API result: HTTP 404 during 2026-11-13 review
Canonical repository CLASS patch as individual tracked source: not located
PTUM.zip archive contents: not inspected
CLASS v3.2.0 patch public availability: UNVERIFIED
Clean-tree patch apply check: UNVERIFIED
Cobaya production configs: pending / not verified
Full MCMC chains: pending or external archive, not verified
```

The earlier v1.2 package audit marked the CLASS patch public and its
apply-check as PASS based on a historical user-reported status. That
claim could not be independently verified against the current
canonical repository snapshot and is superseded by this evidence-based
audit. A repository URL returning 404 does not establish whether the
legacy repository is private, renamed, or deleted.

## Scientific and software status

The current correction branch specifies the minimally coupled
classical tree-level PTUM+SM action, revises the scalar and transfer
conventions, includes the exact inflation endpoint and trajectory
matching, and provides homogeneous simulation and linear resonance
diagnostics. These are not a complete nonlinear waterfall, reheating,
relic-abundance, or observational reproduction pipeline.

The latest observed branch has 81 passing regression tests and a successful LaTeX build. The 100-trajectory scan at 120 mu^-1 and the targeted ten-trajectory follow-up at 240 mu^-1 both completed and passed aggregation. See
`PTUM_10_OF_10_ACCEPTANCE.md`,
`PTUM_CLAIM_BOUNDARY.md`, and
`PTUM_REPRODUCIBILITY_NOTES.md` for the detailed evidence gates.

## Audit disposition

The former label
`PTUM_LIBRARY_FINAL_v1.2_CODE_AVAILABLE_CORRECTED_COMPLETE: PASS`
is withdrawn. The package must not be described as fully code-available,
fully reproducible, or 10/10 until the CLASS patch, production configs,
chains, current manuscript build, scan artifact, and outstanding
scientific calculations are independently verified.

## 2026-11-13 follow-up: lattice-claim audit

A source-level consistency review found that the manuscript still
contained detailed LATTICEEASY results and reproduction instructions
while the current public repository did not expose the solver or the
underlying run artifacts. The former $256^3/512^3$, energy-conservation,
Floquet, relic-density, defect, and entropy claims have been removed
from the verified-results narrative. The replacement subsection
states the evidence gap and specifies the minimum source, initial
conditions, discretization, renormalization, diagnostics, raw outputs,
and convergence material required before those claims can be restored.

The introduction was also narrowed from saying that PTUM implements
proxy-fluid perturbations to saying that it specifies a phenomenological
linear proxy-fluid closure. The closure is not a microscopic result.

Two new manuscript-boundary regression tests have been added. Their
status, the 100-trajectory scan, and the current LaTeX build must be
checked in the latest GitHub Actions run before any pass is recorded.


## 2026-11-14 evidence correction

The full homogeneous scan now has a validated 100-row artifact at \(\tau_{\max}=120\). The ten selected low-scale high-seed cases were extended to \(\tau_{\max}=240\). No sustained late-time quartic classification was obtained; five transient quartic-like episodes were observed. These results strengthen the evidence boundary around the proxy-fluid closure but do not close the nonlinear waterfall, backreaction, defect, reheating, or observational reproducibility gaps.
