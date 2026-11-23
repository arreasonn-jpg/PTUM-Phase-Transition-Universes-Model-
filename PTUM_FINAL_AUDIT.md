# PTUM Final Audit, evidence-based snapshot

**Review date:** 2026-11-24  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-  
**Reviewed main commit:** `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

## Repository and access

The canonical repository exists, is public, and the connected GitHub identity has admin, maintain, push, and pull permissions. The default branch is `main`.

## Current tracked implementation

- `main.tex` and the historical tracked `main.pdf`;
- figure PDFs and journal class files;
- `ptum_task1_simulation.py`, the coupled homogeneous Phi-Psi solver;
- `tests/test_ptum_task1_simulation.py`, containing 11 mathematical regression tests;
- `.github/workflows/ptum-phi-psi-validation.yml`, which compiles the solver, runs the tests, reruns the 18-point scan, and uploads its JSON artifact;
- claim-boundary, audit, inventory, and task notes.

The current workflow does not include a LaTeX build, CLASS/Cobaya pipeline, or lattice simulation. The presence of a tracked historical PDF is not evidence that it was freshly built from the reviewed commit.

## Latest verified CI and numerical result

Workflow run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) on commit `1136c4e589be44f6dbe201c59d0d6decb1ae0141` completed successfully:
- Python module compilation: PASS;
- mathematical regression tests: PASS (11 tests);
- declared 18-point coupled Phi-Psi scan: PASS (18/18 integrations);
- scan artifact upload: PASS.

The merged PR #30 reports 2 exact zero-seed invariant trajectories and 16 quadratic outcomes after tachyonic-to-dormant exit. No trajectory passes the joint quartic-fluid classifier. Maximum relative residuals are 6.26e-17 (total continuity), 2.53e-14 (moving-minimum split continuity), and 2.67e-4 (dense state-derivative audit).

The workflow's green result validates only the declared code/test/scan gates. It does not establish a physical trigger into the tachyonic phase or a quartic-fluid realization.

## Critical sign and trigger boundary

The current convention is `m_eff^2 = m_psi^2(1 - alpha Phi^2/E_th^2)`, so the tachyonic region is `|Phi| > Phi_c`. The merged scan notes that a downhill fuel trajectory exits that region. The current homogeneous background therefore does not demonstrate the claimed post-inflationary trigger into tachyonic activation. This must be resolved from the action and cosmological history, not by changing a sign to force the desired result.

## Not verified / not delivered by this repository checkpoint

- Independent LaTeX rebuild of the latest manuscript source;
- complete CLASS patch and production Cobaya configuration/chain package;
- reproducible inhomogeneous lattice code, initial conditions, raw configurations, and convergence artifacts;
- quantum-seeded nonlinear waterfall with backreaction and rescattering;
- self-consistent reheating and entropy history;
- derived dark-matter relic abundance;
- microscopic derivation of the proxy-fluid closure;
- UV completion or solution to the cosmological-constant problem.

Older audit text that called the package “code-available corrected complete” or marked a legacy CLASS patch as publicly verified is superseded. The current main tree does not contain that CLASS patch as an individually reviewable tracked file.

## Disposition

**Software/numerical checkpoint:** PASS for the explicitly bounded homogeneous 18-point study.  
**Physical mechanism:** NOT ESTABLISHED.  
**Full scientific reproducibility:** NOT COMPLETE.  
**10/10 acceptance:** NOT MET.

This audit deliberately separates successful numerical bookkeeping from the still-unresolved physical mechanism.
