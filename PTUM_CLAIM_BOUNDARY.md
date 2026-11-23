# PTUM Claim Boundary, updated 2026-11-24

## Verified scope of the current public code

The current `main` branch implements and tests a **homogeneous, classical, two-field truncation** for the coupled fuel field `Phi` and activation/proxy field `psi`. The implementation uses the Planck-normalized fuel potential, the field-dependent activation mass, the Friedmann equation sourced by the unshifted Hilbert energy, and an exact split of the activation energy into excitation energy plus its moving minimum.

For the current convention,
`m_eff^2(Phi) = m_psi^2 [1 - alpha Phi^2/E_th^2]`.
Thus the tachyonic region is `|Phi| > Phi_c`, not `|Phi| < Phi_c`. The merged numerical study explicitly finds that a downhill fuel trajectory exits this tachyonic region. This is a model-level trigger-direction problem: the current homogeneous trajectory does not demonstrate a post-inflationary transition *into* the tachyonic phase.

## Latest reproducible numerical checkpoint

Canonical source commit: `1136c4e589be44f6dbe201c59d0d6decb1ae0141` (2026-11-23).

GitHub Actions workflow `PTUM Phi-Psi Validation`, run `45257091704`, completed successfully. It compiled the simulation module, ran the 11 mathematical regression tests, and reran the complete declared 18-point coupled Phi-Psi scan.

The merged PR #30 records:
- 18/18 integrations succeeded;
- 2 zero-seed trajectories remained on the exact invariant `psi = 0` solution;
- the other 16 trajectories were classified as quadratic after leaving the tachyonic phase;
- 0/18 trajectories satisfied the joint quartic-fluid classifier;
- maximum relative total-continuity residual: `6.26e-17`;
- maximum relative moving-minimum split-continuity residual: `2.53e-14`;
- maximum relative dense state-derivative residual: `2.67e-4`.

These results validate the stated finite homogeneous benchmark and its numerical identities. They do **not** demonstrate a quartic-dominated radiation-like phase.

## What may be claimed

- The implemented homogeneous Phi-Psi equations are dimensionally consistent with the declared potential and effective mass.
- The interaction is included once in the total Hilbert/Friedmann source.
- The total energy continuity identity and the exact moving-minimum sector split pass the stated numerical regression and scan gates.
- The declared 18-point homogeneous scan completed without integration failures.
- The quartic-fluid classification is conditional and was not reached by any trajectory in that scan.

## What must not be claimed as demonstrated

- That the current downhill background dynamically triggers entry into the tachyonic phase.
- That the current benchmark realizes a sustained quartic-fluid phase or a microscopic radiation-like proxy fluid.
- That the homogeneous calculation establishes inhomogeneous quantum-seeded waterfall dynamics, backreaction, rescattering, fragmentation, defect evolution, thermalization, reheating temperature, or a relic abundance.
- That the current repository independently reproduces a full CLASS/Cobaya Bayesian pipeline, production MCMC chains, or lattice results.
- That PTUM is UV complete, solves the cosmological-constant problem, or is observationally preferred to LambdaCDM.

## Required next scientific gates

1. Resolve the trigger-direction issue from the covariant action and intended cosmological history. Do not flip the mass sign merely to obtain a desired outcome.
2. Derive and implement the post-inflationary background and threshold crossing with physically justified initial conditions.
3. Re-run solver, tolerance, output-grid, and parameter-space convergence on that corrected physical trajectory.
4. Build a spatially inhomogeneous quantum-seeded simulation with controlled UV/IR treatment, backreaction, energy accounting, volume and lattice-spacing convergence.
5. Derive the proxy-fluid, reheating, and dark-matter abundance from those dynamics, or retain them explicitly as phenomenological conditional sectors.
6. Publish the complete observational pipeline, exact software versions, configurations, chains, and checksums before claiming end-to-end Bayesian reproducibility.

**Disposition:** the coupled homogeneous numerical work package is validated for its declared scope. The physical trigger and downstream microscopic cosmology remain open. PTUM is not 10/10 and the absence of a quartic trajectory is a result, not a software failure.
