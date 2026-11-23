# PTUM Work Package Summary

**Updated:** 2026-11-24  
**Canonical source:** `main` at `1136c4e589be44f6dbe201c59d0d6decb1ae0141`

## Completed in the current homogeneous Phi-Psi work package

1. Dimensionally consistent Planck-normalized fuel potential and derivative.
2. Coupled homogeneous Phi-Psi background equations with the declared field-dependent activation mass.
3. Unshifted Hilbert/Friedmann energy source, with the interaction counted exactly once.
4. Exact moving-minimum split between excitation energy and the minimum contribution.
5. Sector transfer bookkeeping including the derivative of the moving minimum.
6. Full-cycle equation-of-state, quartic-dominance, virial, and adiabaticity diagnostics.
7. Threshold crossing direction/duration and exact-zero-seed invariant classification.
8. Dense-output state-derivative and total/split continuity diagnostics.
9. Regression coverage for the key mathematical identities and numerical edge cases.
10. Automated 18-point scan in GitHub Actions.

## Verified result

GitHub Actions run [45257091704](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45257091704) passed on 2026-11-23:
- module compilation passed;
- 11 mathematical regression tests passed;
- all 18 scan integrations succeeded;
- scan artifact upload succeeded.

The merged PR #30 reports:
- 2 zero-seed cases remain exactly on `psi = 0`;
- 16 cases become quadratic after leaving the tachyonic phase;
- no case meets the joint quartic-fluid classifier;
- maximum relative total continuity residual = 6.26e-17;
- maximum relative moving-minimum split residual = 2.53e-14;
- maximum relative dense state-derivative residual = 2.67e-4.

## Central physical result

For the implemented convention `m_eff^2 = m_psi^2(1 - alpha Phi^2/E_th^2)`, tachyonic activation occurs at `|Phi| > Phi_c`. The current downhill homogeneous fuel trajectory exits that region rather than entering it. The present calculation therefore does not establish the claimed post-inflationary tachyonic trigger. It also does not produce a sustained quartic-dominated phase.

This is a substantive negative result. It must remain visible in the manuscript and project claims; it must not be hidden by relabeling the scan or by changing the mass sign without deriving that change from the action.

## Remaining major scientific work

1. Derive a physically consistent cosmological trajectory that enters the tachyonic region at the intended epoch, or revise the mechanism/claim.
2. Recompute the homogeneous dynamics and parameter scan on that corrected physical history, including solver/tolerance/time-grid convergence.
3. Develop an inhomogeneous quantum-seeded waterfall with controlled UV/IR initialization, backreaction, rescattering, energy accounting, and lattice/volume convergence.
4. Derive or explicitly retain as phenomenological the radiation-like proxy-fluid closure.
5. Couple resonance to Boltzmann evolution and compute relic abundance rather than treating the target abundance as a result.
6. Compute reheating, thermalization, and entropy history self-consistently.
7. Release the complete observational pipeline (CLASS patch, production Cobaya configurations, data/likelihood versions, chains, and checksums) if those results remain part of the paper.
8. Perform a fresh LaTeX build from the current manuscript source and archive the exact build log/PDF.

## Final disposition

The **homogeneous numerical work package is complete and its declared CI gates pass**. The broader PTUM scientific program is **not complete and is not 10/10**. The open items above require new physical derivations and simulations; they cannot honestly be closed by documentation edits or by the successful 18-point background scan.

This summary supersedes earlier historical summaries that reported 11 referee tasks as complete while relying on pre-correction lattice, reheating, or publication-pipeline claims.
