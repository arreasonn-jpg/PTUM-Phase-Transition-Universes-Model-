# PTUM Theoretical Inventory, evidence-corrected update

**Updated:** 2026-11-24  
**Canonical code checkpoint:** `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

> This document supersedes the earlier inventory below, whose tachyonic-region direction, benchmark conclusions, and lattice/reheating statements predate the current coupled Phi-Psi implementation. Historical numerical tables in earlier revisions are not evidence for the current branch.

## 1. Current mathematical core

The current homogeneous implementation uses
`V_eff(Phi) = V0 [1 - exp(-lambda_phi (Phi/M_Pl)^2)]`,
`m_eff^2(Phi) = m_psi^2 [1 - alpha Phi^2/E_th^2]`,
and
`V(Phi,psi) = V_eff(Phi) + (1/2)m_eff^2(Phi)psi^2 + (1/4)lambda_psi psi^4`.

The tachyonic region for this convention is `|Phi| > Phi_c`. The field equations are the Euler-Lagrange equations for this declared potential in the homogeneous FRW truncation. The interaction contribution is assigned once to the activation-sector Hilbert energy.

The excitation split is exact:
`V_act(Phi,psi) = U(Phi,psi) + V_min(Phi)`.
The `V_min'(Phi) Phi_dot` contribution is included in the sector transfer. The total Friedmann source remains the unshifted Hilbert source.

## 2. What is verified

The main-branch GitHub Actions run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) on 2026-11-23 passed:
- simulation-module compilation;
- all 11 mathematical regression tests;
- all 18 integrations in the declared homogeneous parameter grid;
- scan artifact upload.

The merged numerical report records maximum relative residuals:
- total continuity: 6.26e-17;
- moving-minimum split continuity: 2.53e-14;
- dense state derivative: 2.67e-4.

The 18 outcomes are 2 exact zero-seed invariant trajectories and 16 quadratic outcomes after tachyonic-to-dormant exit. No trajectory satisfies the joint quartic-fluid classifier.

These are finite-grid numerical validations of the implemented homogeneous equations and diagnostics. They do not prove the full PTUM cosmology.

## 3. Critical unresolved physical questions

### A. Trigger direction

The current convention is tachyonic for `|Phi| > Phi_c`. The reported downhill fuel trajectory exits that region. The current calculation therefore does not show the intended post-inflationary entry into tachyonic activation. The resolution must come from the action, field orientation, and cosmological history. A sign change made solely to obtain tachyonic growth would be unjustified.

### B. Quartic-fluid realization

No trajectory in the validated 18-point scan reaches the joint sustained quartic-fluid criteria. The effective closure `w = 1/3, c_s^2 = 1/3, sigma = 0` remains conditional/phenomenological, not a microscopic outcome of this calculation.

### C. Inhomogeneous waterfall

The current code is homogeneous. It does not evolve spatial modes as a coupled nonlinear lattice, include quantum-seeded inhomogeneous initial conditions, backreaction, rescattering, fragmentation, or defect formation.

### D. Dark matter and reheating

No self-consistent coupled resonance-Boltzmann relic calculation or kinetic reheating/thermalization/entropy history is included in the current workflow. Any abundance or reheating number not reproduced by such a calculation must remain a target or estimate.

### E. Observational reproducibility

The current main tree does not include a complete individually reviewable CLASS/Cobaya production package with configurations, likelihood versions, full chains, and checksums. The latest CI workflow tests the homogeneous solver and scan, not the observational pipeline.

## 4. Work required before a 10/10 scientific claim

1. Resolve the trigger-direction issue from the action and derive a physically consistent background history.
2. Repeat the homogeneous scan with solver/tolerance/output-grid convergence on that history.
3. Implement and validate the inhomogeneous quantum-seeded nonlinear waterfall.
4. Establish or withdraw the microscopic proxy-fluid, dark-matter, and reheating claims.
5. Publish and independently reproduce the complete observational pipeline.
6. Build the current LaTeX source in CI and archive the log and PDF.
7. Maintain explicit claim boundaries and reproduce every quantitative statement from clean checkout.

## 5. Disposition

The homogeneous Phi-Psi implementation and its declared 18-point numerical gate are validated. The central physical trigger and downstream microscopic cosmology are not established. The correct status is **validated bounded numerical subsystem; broader PTUM theory still under research; not 10/10**.
