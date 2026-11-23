# PTUM Task 1: Current Coupled Phi-Psi Numerical Findings

**Updated:** 2026-11-24  
**Canonical source commit:** `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

> This document supersedes the earlier Task 1 tables, which were produced by a previous model convention and solver implementation. Do not combine the historical results below with the current branch results.

## Current equations and threshold direction

The current solver uses
`m_eff^2(Phi) = m_psi^2 [1 - alpha Phi^2/E_th^2]`.
Therefore the activation field is tachyonic for `|Phi| > Phi_c` and non-tachyonic for `|Phi| < Phi_c`.

The current coupled homogeneous equations follow from the declared potential:
`V(Phi,psi) = V_eff(Phi) + (1/2)m_eff^2(Phi)psi^2 + (1/4)lambda_psi psi^4`.
The total Friedmann source uses the unshifted Hilbert energy. The excitation diagnostic subtracts the exact instantaneous minimum and assigns the complementary minimum term to the fuel-sector split.

## Latest validation

GitHub Actions run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) passed on the canonical main commit:
- 11/11 mathematical regression tests;
- 18/18 coupled homogeneous integrations;
- total continuity, moving-minimum split, and dense state-derivative acceptance thresholds;
- scan artifact upload.

The merged PR #30 records:
- 2 zero-seed trajectories remain on the exact invariant `psi = 0` solution;
- 16 trajectories leave the tachyonic region and are classified as quadratic;
- 0 trajectories pass the joint quartic-fluid classifier.

Maximum relative residuals:
| Diagnostic | Maximum |
|---|---:|
| Total continuity | 6.26e-17 |
| Moving-minimum split continuity | 2.53e-14 |
| Dense state derivative | 2.67e-4 |

## Physical interpretation

The finite homogeneous scan does not produce a sustained quartic-dominated radiation-like phase. More importantly, the current mass-sign convention makes the tachyonic region `|Phi| > Phi_c`, while the reported downhill fuel trajectory exits that region. Thus this scan does not demonstrate a post-inflationary trigger into the tachyonic phase.

This is not fixed by calling a quadratic trajectory quartic or by changing the sign of the mass term without deriving that change from the action. The trigger-direction question remains a physical model problem.

## Scope

The result is limited to the declared homogeneous two-field truncation and finite 18-point grid. It does not establish inhomogeneous quantum-seeded waterfall dynamics, backreaction, rescattering, fragmentation, defect evolution, microscopic proxy-fluid behavior, reheating, or dark-matter relic abundance.
