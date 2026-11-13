# PTUM GitHub Audit - 2026-11-13

## Scope and method

This audit was performed against the public `main` branch of
`arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-` on 2026-11-13.
It is a source-level analytical audit. No numerical result is represented as
independently reproduced unless a test artifact is explicitly supplied.

This file is intentionally an audit, not a patch to the scientific equations.
Changing signs or source terms without rebuilding the complete action,
stress tensors, and equations would risk making the manuscript internally
consistent in appearance while physically wrong.

## Executive result

The current manuscript is **not ready to be treated as a fully internally
verified derivation**. Several concrete contradictions are visible in
`main.tex`, and the auxiliary simulation script has energy-accounting and
diagnostic problems. The most consequential issues are:

1. Metric/sign convention and scalar stress-energy definition are inconsistent.
2. The activation interaction sign in the microscopic-transfer section
   contradicts the activation Lagrangian.
3. The claimed Yukawa contribution to the transfer four-vector has the
   wrong mass dimension.
4. The Mathieu reduction omits the constant effective-mass contribution and
   has a factor-of-two/sign-convention problem in q.
5. The Python simulation double-counts the interaction potential in the
   total energy used by the Friedmann equation.
6. The reported "energy conservation" diagnostic incorrectly tests constant
   energy density in an expanding universe.
7. The public reproducibility notes point to a different repository and
   conflict with the manuscript's own code-availability statements.

## Findings

### F-01 - Scalar convention mismatch (critical)

In `main.tex`, the metric signature is `(-+++)`. The manuscript defines
`T_{mu nu} = -2/sqrt(-g) delta(S_m)/delta(g^{mu nu})`, while stating that
`L = +1/2 g^{mu nu} d_mu phi d_nu phi - V` is canonical and gives
`rho = +1/2 phidot^2 + V`.

With signature `(-+++)`, this combination is not the standard canonical
scalar convention. For the usual positive-energy canonical scalar and the
stated metric signature, use
`L = -1/2 g^{mu nu} d_mu phi d_nu phi - V`
with the corresponding standard stress-energy definition. Alternatively,
one may change the metric/stress-tensor convention consistently, but the
paper must choose one convention and use it everywhere.

**Required work:** derive the stress tensor by metric variation from the
chosen action; verify T_00, pressure, flat-space Klein-Gordon equation,
homogeneous FRW equation, and Einstein/Friedmann equations. Apply to
Phi, psi, chi, and Phi_res. Audit all appendices and lattice equations.

### F-02 - Activation interaction sign contradiction (critical)

The activation Lagrangian in Eq. (activation) contains
`-m^2 psi^2/2 (1 - alpha Phi^2/E_th^2)`.
Its expansion contains the mixed term
`+ alpha m^2 Phi^2 psi^2/(2 E_th^2)`.

However, the microscopic-transfer section writes
`L_int^(psi Phi) = - alpha m^2 Phi^2 psi^2/(2 E_th^2)`.
These are opposite signs. The equations of motion shown elsewhere must
therefore not be accepted as a verified derivation until the full action is
varied with a single sign convention.

**Required work:** define the full action once; derive all four scalar EOMs;
derive each sector stress tensor from a declared split of the interaction
potential; state the convention for assigning interaction energy; prove
the sum of all sector divergences vanishes on shell.

### F-03 - Yukawa transfer vector has wrong mass dimension (critical)

The manuscript gives `L_rh = -y_psi psi fbar f` and includes a term
`y_psi psi fbar gamma^nu f` in `Q_psi^nu`.

In four spacetime dimensions, `[psi]=1`, `[f]=3/2`,
`[fbar gamma^nu f]=3`, and dimensionless `[y_psi]=0`. The displayed
term therefore has mass dimension 4. But
`[Q^nu] = [nabla_mu T^{mu nu}] = 5` in natural units. It cannot be the
claimed transfer four-vector as written.

**Required work:** derive the Yukawa exchange from the complete fermion and
scalar equations of motion and the Hilbert stress tensors. Do not guess a
replacement expression. Check dimensions and signs before assigning the
opposite contribution to the SM sector.

### F-04 - Mathieu parameters need re-derivation (critical)

The manuscript uses
`L_int = -g_DM chi^2 Phi_res^2`, hence
`m_chi,eff^2 = m_chi^2 + 2 g_DM Phi_res^2`.
For
`Phi_res = A_res cos(omega_res t)`, this becomes
`m_chi,eff^2 = m_chi^2 + g_DM A_res^2 [1 + cos(2 omega_res t)]`.

With `z = omega_res t` and neglecting expansion only for this first
reduction, the mode equation has the form
`X_k'' + [A_k + B_k cos(2z)] X_k = 0`, where
`A_k = (k^2/a^2 + m_chi^2 + g_DM A_res^2)/omega_res^2`
and
`B_k = g_DM A_res^2/omega_res^2`.
Matching the standard convention
`X'' + [A_k - 2 q cos(2z)]X=0` gives
`q = -g_DM A_res^2/(2 omega_res^2)` (the sign can be shifted by a
phase redefinition, but the magnitude and factor 1/2 cannot be omitted).

The current manuscript instead defines
`q = g_DM A_res^2/omega_res^2` and omits the constant
`g_DM A_res^2` from `A_k`. It also states `A_k approximately 1`
and then infers `omega_chi approximately omega_res/2`; with the
stated definition of A_k this inference does not follow.

**Required work:** derive the expanding-FRW mode equation, use the
appropriate rescaled variable (including H and dot-H terms), calculate
Floquet exponents from the monodromy matrix, map instability bands, and
check narrow/broad resonance, backreaction, and relic abundance. Do not
retain the quoted `mu_max approximately q omega/2` unless verified in the
actual convention and regime.

### F-05 - Simulation energy double-counting (critical)

In `ptum_task1_simulation.py`:

- `rho_phi()` adds `+ 0.5 m_eff_sq psi**2`.
- `rho_psi()` also adds `+ 0.5 m_eff_sq psi**2`.
- `hubble_rate()` sums `rho_phi + rho_psi`.

The same mixed mass-potential term is therefore counted twice in the
Friedmann source. Derive the total energy density from the full action and
count each interaction term exactly once. A sector split may allocate the
interaction energy to one sector or divide it by a declared convention, but
the total must be unique.

Also, the script's `max(rho_tot, 0)` can hide negative-energy or invalid
states. Replace silent clipping with explicit physical-domain checks and
failure diagnostics.

### F-06 - Simulation conservation diagnostic is not valid in FRW (high)

The script stores
`max(abs(rho_total(t) - rho_total(0)))` under the name
`energy_conservation`. In an expanding universe, energy density is not
generally constant. The appropriate total continuity residual is
`dot(rho_total) + 3 H (rho_total + p_total)`
for a closed homogeneous system, with source terms included consistently
when sectors exchange energy. Also monitor the Friedmann constraint
residual and numerical convergence under tighter tolerances and finer
time sampling.

### F-07 - Quartic-dominance diagnostic uses a fixed reference mass (high)

`compute_quartic_dominance()` uses `abs(params.mu_sq)`, evaluated at
one fixed reference value `Phi=1.01 Phi_c`, even though the effective
mass changes with the evolving `Phi(t)`. The diagnostic can therefore
misclassify the quartic regime. It also returns an all-zero Q array when
there are insufficient turning points, which is ambiguous between
"no oscillation" and "not quartic".

**Required work:** define a time-local or physically motivated effective
quadratic contribution, use oscillation-window averages with robust
turning-point detection, and distinguish `NO_OSCILLATION`,
`INSUFFICIENT_CYCLES`, `QUADRATIC`, `TRANSITIONAL`, and
`QUARTIC_CONFIRMED`. Report the virial and equation-of-state criteria
with uncertainties and convergence checks.

### F-08 - Proxy-fluid closure remains phenomenological (high)

The manuscript correctly states that the quoted benchmark is overdamped
and does not reach the quartic oscillatory regime. Preserve this caveat.
The conditions `w=1/3`, `c_s^2=1/3`, and `sigma=0` must remain
labelled as a phenomenological perfect-fluid closure unless the microscopic
field dynamics and perturbations demonstrate the closure. Distinguish
`c_a^2 = dot(p)/dot(rho)` from rest-frame `c_s^2`. In a perfect-fluid
closure, higher multipoles/anisotropic stress are set to zero by closure,
not merely claimed to be irrelevant.

### F-09 - Repository/reproducibility claims conflict (high)

The current repository's `PTUM_REPRODUCIBILITY_NOTES.md` and
`PTUM_CLAIM_BOUNDARY.md` point to
`https://github.com/ErdemEsa/ptum-cosmology.git`, while this project is
`https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-.git`.
The manuscript also contains conflicting statements about whether the
modified CLASS patch is public. It describes a lattice release path and
scripts, while another section says the lattice code/raw outputs are not
public. These statements need a single verified inventory.

**Required work:** establish which repository is canonical; inspect any
archive/zip; enumerate actual CLASS patch, Cobaya YAMLs, chains, lattice
code, raw outputs, seeds, configs, scripts, environment lockfiles, and
CI logs. Update availability statements only after each artifact is
confirmed accessible and runnable.

### F-10 - Claims that need independent reproduction (high)

The following must not be described as independently verified merely
because values appear in the manuscript or notes:

- Bayesian posterior bound on Delta N_fluid and reported model comparison.
- CLASS perturbation implementation and gauge/conservation tests.
- Lattice Floquet exponent, relic abundance, entropy, and defect claims.
- Dark-energy parameter-space scan fractions.
- Any "convergence tested" statement without scripts, inputs, and outputs.

Use explicit labels: `REPRODUCED`, `AUTHOR_REPORTED`,
`PARTIALLY_REPRODUCED`, `NOT_REPRODUCED`, `BLOCKED`.

## Repository hygiene

The visible repository inventory includes LaTeX build artifacts and
Windows Zone.Identifier files. Add/verify a `.gitignore` for transient
LaTeX files, Python caches, local environments, generated intermediate
outputs, and OS metadata. Do not delete existing artifacts until their
purpose and release status are checked.

## Safe implementation sequence

1. Freeze a baseline commit and record SHA, Python/package versions, and
   manuscript checksum.
2. Build a full action/convention notebook or symbolic derivation.
3. Correct scalar sign conventions and regenerate EOM/stress tensors.
4. Derive the complete sector transfer vectors from the corrected action.
5. Re-derive Mathieu/Floquet analysis and update all downstream relic claims.
6. Correct simulation energy accounting and diagnostics.
7. Separate microscopic predictions from phenomenological CLASS proxy-fluid
   constraints.
8. Audit repository inventory and reconcile all code-availability claims.
9. Run LaTeX build, unit tests, dimensional checks, convergence tests, and
   regression tests.
10. Publish changes on a review branch and merge only after every scientific
    check is documented.

## Status of this audit branch

This branch adds this audit report only. It does not modify the manuscript,
simulation source, numerical data, or scientific claims. No result is
fabricated or silently promoted to a verified result.
