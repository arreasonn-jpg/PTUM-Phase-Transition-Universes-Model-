# PTUM 10/10 Acceptance Gates

**Updated:** 2026-11-24  
**Canonical code checkpoint:** `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

A 10/10 score is reserved for independently reproducible scientific and numerical maturity. Passing software tests alone cannot satisfy physical or observational gates.

| Gate | Requirement | Current status |
|---|---|---|
| 1. Covariant model definition | One unambiguous action, conventions, field dimensions, signs, and sector definitions | PARTIAL: homogeneous two-field potential and equations are implemented; full cosmological trigger history remains unresolved |
| 2. Trigger mechanism | Derive and demonstrate entry into the tachyonic region at the intended epoch | NOT MET: current convention is tachyonic for `|Phi| > Phi_c`; downhill background exits rather than enters |
| 3. Homogeneous numerical verification | Regression identities, successful scan, solver/tolerance/output-grid convergence | PARTIAL: 11 tests and 18/18 integrations pass; no full convergence study on a physically corrected trigger history |
| 4. Quartic-fluid realization | Demonstrate sustained quartic dominance with consistent cycle, virial, and adiabatic criteria | NOT MET: 0/18 current trajectories pass the joint classifier |
| 5. Inhomogeneous waterfall | Quantum-seeded spatial evolution with UV/IR prescription, backreaction, rescattering, and lattice/volume convergence | NOT MET |
| 6. Dark-matter abundance | Couple production/resonance to Boltzmann evolution and reproduce relic abundance | NOT MET: no current end-to-end calculation |
| 7. Reheating and entropy | Compute decay, thermalization, branching, and entropy history self-consistently | NOT MET |
| 8. Observational pipeline | Reproducible CLASS/Cobaya source, production configs, likelihood/data versions, chains, and checksums | NOT MET in the current tracked main tree |
| 9. Independent reproducibility | Clean-checkout commands, pinned environment, raw artifacts, hashes, and independent rerun | PARTIAL: bounded homogeneous CI/scan is reproducible; downstream scientific packages are absent |
| 10. Manuscript/build integrity | Current manuscript claims match evidence; fresh LaTeX build and archived log/PDF in CI | PARTIAL: claim/audit docs updated; current workflow does not build LaTeX |

## Verified homogeneous checkpoint

GitHub Actions run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) passed on the canonical code commit:
- module compilation;
- 11 mathematical regression tests;
- 18/18 homogeneous integrations;
- scan artifact upload.

The merged numerical report records 2 exact zero-seed invariant trajectories, 16 quadratic outcomes after tachyonic exit, and no quartic-fluid outcome. Maximum relative residuals were 6.26e-17 (total continuity), 2.53e-14 (moving-minimum split continuity), and 2.67e-4 (dense state derivative).

## Acceptance rule

PTUM may be labelled 10/10 only when all ten gates are MET on a single identified source snapshot, the full evidence package is available from a clean checkout, and independent reruns reproduce the quantitative claims. A gate cannot be promoted by a documentation edit, a green unit-test suite, a finite homogeneous scan, or a phenomenological closure.

**Current verdict: NOT 10/10.** The homogeneous numerical work package is validated within its declared scope. The trigger mechanism and downstream physical/observational calculations remain open research tasks.
