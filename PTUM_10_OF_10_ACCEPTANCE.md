# PTUM 10/10 Scientific Acceptance Matrix

This file defines the evidence required before PTUM can be called scientifically and computationally ready. A passing CI workflow is necessary but not sufficient. A phenomenological ansatz is not counted as a microscopic derivation, and an author-reported result is not counted as independently reproduced.

## Acceptance gates

| Gate | Required evidence for 10/10 | Current status |
|---|---|---|
| 1. Complete action and conventions | One explicit covariant action; fixed metric/sign conventions; all fields, dimensions, gauge representations, potentials, couplings, real/complex field choices and symmetry-breaking structure specified | **MET (classical tree-level EFT)**. The minimally coupled Einstein + PTUM + chiral-SM action, field representations, canonical dimensions, Higgs and Yukawa potentials, dimension-five PTUM operators, and the explicit \(\psi\)/\(\Phi_{\rm res}\) symmetry scope are now specified. Quantum/UV completion remains outside this gate and open separately |
| 2. Inflation-to-waterfall connection | Exact inflation endpoint; threshold crossing in the same coupled background; stability of all modes before crossing; quantum seed prescription | **PARTIAL**. Exact epsilon_H endpoint is computed; post-threshold scan velocities are now taken from the integrated single-field FRW trajectory at each offset, but the coupled crossing and quantum seeds are not evolved |
| 3. Hilbert tensors and conservation | Every sector tensor derived from the same action; all Q_i^nu derived; sum of currents cancels; numerical conservation converges independently with solver tolerance and timestep | **PARTIAL**. The classical tree-level gauge, Higgs, chiral-fermion and PTUM Hilbert tensors and all interaction currents are now written from one action; the current solver does not evolve SM fields, and full-sector numerical conservation/timestep-tolerance convergence is not yet demonstrated |
| 4. Background numerical solution | Stable expanding-FRW integration; positivity/domain checks; independent energy and continuity diagnostics with robust background-energy normalization; timestep and solver-tolerance convergence | **PARTIAL**. Chain-rule and finite-difference diagnostics exist; convergence campaign remains open |
| 5. Waterfall/tachyonic dynamics | Inhomogeneous mode evolution, correct vacuum initial conditions, lattice or validated mode treatment, backreaction, rescattering and a defect-topology analysis (including the Z2 domain-wall risk of a real waterfall scalar) | **NOT MET**. Current scan is homogeneous and post-threshold |
| 6. Resonance and relic abundance | Expanding-background mode equations; converged monodromy/Floquet growth; momentum integration; backreaction; thermalization and entropy dilution; independently reproduced relic abundance | **NOT MET**. A linear mode integrator now evolves supplied expanding-FRW histories with an adiabatic-vacuum check and Wronskian monitor, and a finite-band trapezoidal momentum integral is implemented. The background is not generated self-consistently, the momentum tails and grid are not converged, and no backreaction or entropy dilution is available |
| 7. Proxy-fluid realization | Demonstrate a stable parameter region with the required averaged equation of state, sound speed and anisotropic stress from the dynamics; show convergence and perturbative stability | **NOT MET**. The closure remains phenomenological; no microscopic realization is established |
| 8. Reheating and entropy | Full energy partition from the coupled trajectory; decay/thermalization rates; BBN-compatible thermal history; comoving entropy calculation | **PARTIAL**. Conditional potential-dominated T_rh estimate only; branching and thermalization are not computed |
| 9. Observational reproducibility | Public exact CLASS patch; pinned version/commit; complete configs, likelihoods, data, chains and commands; independent rerun reproduces posteriors and model comparison | **NOT MET**. Reported numbers are author-reported; patch availability and chains remain unverified |
| 10. Software and manuscript reproducibility | Pinned environment; deterministic seeds; strict data schemas; full CI; clean LaTeX build; no unresolved references or contradictory claims; artifact hashes | **PARTIAL**. Regression suite, pinned CI and strict JSON exist; scan now fails closed on missing/failed trajectories and preserves failure artifacts, but the latest tests, 100-point scan and LaTeX build remain pending |

## Current implementation evidence

- Canonical scalar kinetic and stress-tensor conventions use metric signature (-+++).
- The waterfall mass is now
  `m_eff^2(Phi) = m_psi^2 (alpha Phi^2/E_th^2 - 1)`,
  stable above Phi_c and tachyonic below it.
- The exact epsilon_H = 1 endpoint for lambda_phi = 0.02 is approximately 0.98622808 M_Pl. The older epsilon_V = 1 proxy endpoint, approximately 1.387175 M_Pl, is not the exact end.
- The threshold-matched scan derives Phi_c from the exact Hubble-flow endpoint.
- The revised scan uses 50 initial conditions per energy scale, two scales, 4001 output points per trajectory and a 20 mu^-1 time span. It is a homogeneous post-threshold sensitivity scan, not an inhomogeneous waterfall calculation.
- The quartic energy-dominance indicator is Q/2 = <V4>/<|V2|>; the necessary energy-dominance boundary is Q > 2. Independent equation-of-state and virial checks are also required.
- The simulation now has a positive excitation-energy split about the instantaneous real-psi minimum. It preserves total rho and p, and the cycle-averaged w_psi uses this excitation energy; the raw Hilbert split remains separately available. This diagnostic is limited to the pre-reheating two-field truncation.
- The signed sector source depends on the declared stress-tensor split. Under the current split, Q_psi^0 is negative for dot(Phi) < 0; this is not described as positive energy injection into psi.
- The exact epsilon_H=1 single-field endpoint has V_end/V0 about 0.01926493, K_end/V0 about 0.00963246 and rho_end/V0 about 0.02889739. The idealized instantaneous-thermalization temperature is about 1.72e15 GeV at V0^(1/4)=1e16 GeV and g*=100; this is an upper-limit benchmark, not the coupled energy partition or a reheating prediction.

## Non-negotiable scientific rules

1. Never weaken a failed test merely to obtain green CI. Any tolerance must be justified by a numerical error estimate or convergence study.
2. Never infer a physical phase from one scalar diagnostic. Require independent energy, virial, equation-of-state and stability evidence.
3. Never call the homogeneous post-threshold scan a simulation of the threshold crossing.
4. Never infer quantum vacuum seeding from an exactly zero classical initial condition.
9. Never call a real-scalar Z2 waterfall defect-free: check whether its two tachyonic minima generate domain walls; cosmic strings require a separately specified field manifold and topology.
5. Never call a frozen-background Floquet exponent a relic abundance.
6. Never describe a phenomenological proxy-fluid closure as microscopically realized without a calculation of its production and perturbations.
7. Never call author-reported MCMC output independently reproduced without public inputs and chains.
8. Keep all scientific changes on reviewable branches and PRs. Do not merge or modify main without explicit user instruction.

## 10/10 decision rule

PTUM is 10/10 only when all ten gates are **MET**, every numerical claim is reproducible from a clean checkout, the latest full CI and manuscript build pass, and no critical physics or claim-boundary issue remains open. Until then, report the gate statuses above rather than assigning an inflated percentage.


## Latest engineering correction

The high-resolution scan now derives each post-threshold fuel velocity from the integrated single-field FRW trajectory rather than the potential slow-roll formula at an arbitrary displaced field value. The scan validates all 100 expected rows and fails if any integration fails; the JSON summary is written before this gate so failures remain inspectable. The zero-seed cases are marked as exact classical invariant controls, not quantum-vacuum seeds. The coupled threshold crossing, quantum-seeded inhomogeneous evolution and backreaction remain unmet.


## 2026-11-13 classical action completion update

Gate 1 is now **MET for the explicitly stated minimally coupled classical
tree-level EFT**. The manuscript specifies the \(SU(3)_c\times SU(2)_L\times
U(1)_Y\) representations, three chiral generations, complex Higgs doublet,
four real PTUM gauge singlets, all displayed potentials and interaction
operators, canonical dimensions, and the actual symmetry breaking induced by
the odd \(\psi\mathcal O_{\rm SM}/\Lambda\) operator. The tree-level SM
Hilbert tensor is expressed as gauge + Higgs + symmetric on-shell
chiral-fermion (Belinfante) pieces. The ordinary SM Yukawa equations of
motion are included in the on-shell fermion tensor, so the ordinary
Yukawa potential is not added a second time as a separate metric term.
The distinct PTUM operator is outside the SM reference action and is
assigned exactly once through the explicit $-g^{\\mu\\nu}U_Y$ term.

ptum_covariant_action.py and regression tests check the hypercharge
contractions, non-Abelian singlet contractions, and canonical dimensions.
This is an algebraic consistency layer, not an SM field solver. Gate 3 remains
**PARTIAL** because no numerical evolution or independent conservation
convergence has yet been performed with the SM/Higgs/fermion fields active.
The quantum/renormalized effective action, loop-induced curvature operators,
thermal bias of the real-\(\psi\) vacua, and reheating rates remain open.



## 2026-11-13 follow-up: LaTeX and Hilbert bookkeeping

The latest observed 43-test regression step passed, but the LaTeX job
failed because `mathrsfs` was not loaded for `\\mathscr D_\\mu`.
The package is now loaded and a source regression guards its presence.
A further tensor audit removed a duplicate explicit ordinary-SM-Yukawa
term from the displayed on-shell fermion Hilbert tensor; the separate
PTUM interaction $U_Y$ remains assigned once to the SM sector.
The current branch has 45 tests, but these newest changes have not yet
been verified by a fresh CI run. Gate 3 remains PARTIAL until the
independent variational and full-sector conservation checks are complete.



## 2026-11-13 expanding-mode implementation update

The frozen-background Mathieu solver is now complemented by a
linear `integrate_expanding_mode` routine. It integrates the
(chi_k) equation on supplied (a(t)), (H(t)), and
(Phi_{\\rm res}(t)) histories, imposes a first-order adiabatic
vacuum only when the initial WKB condition is satisfied, and reports
the final instantaneous occupation estimate and Wronskian error.
Regression tests cover a de Sitter vacuum-preservation control and
fail-closed rejection of a non-adiabatic initial state.

Gate 6 remains **NOT MET**: the histories are external inputs rather
than a self-consistent PTUM background, and there is no backreaction,
rescattering, momentum-integrated relic abundance or entropy history.
The threshold-matched benchmark remains overdamped. The branch now
contains 47 Python regression tests, but the newest tests and LaTeX
fix have not yet been observed in a fresh CI run.



## 2026-11-13 finite-band spectrum update

The expanding-mode module now evolves each mode on a supplied
(a(t),H(t),Phi_{\\rm res}(t)) history, checks H=dot(a)/a consistency,
and computes a finite-band trapezoidal estimate of n_chi,com over a
strictly increasing k-grid. The finite-band output is explicitly not
extrapolated beyond its input range. Regression tests cover the
vacuum-preservation control and momentum-grid validation.

Gate 6 remains **NOT MET**. Momentum-range and resolution convergence,
a self-consistent PTUM background, backreaction, rescattering,
nonlinear mode coupling, and entropy dilution are still missing.
The latest branch contains 51 tests, but no fresh CI run has yet
verified the newest mode and manuscript changes.



## 2026-11-13 tachyonic interval regression

The expanding mode solver no longer requires (Omega_k^2(t)>0)
throughout the entire supplied history. It requires a real positive
initial frequency for the adiabatic vacuum, permits intermediate
(Omega_k^2<0) intervals, and assigns an instantaneous particle
number only if the final frequency is positive. The initial WKB
derivative is obtained from the derivative of (Omega_k^2), avoiding
a square root of negative intermediate values. A regression test
checks tachyonic growth and Wronskian preservation.

Gate 6 remains **NOT MET** because this solver still uses externally
supplied histories and no self-consistent PTUM production/relic
calculation has been performed. The current branch contains 51 tests;
the latest full CI run is still pending.

## 2026-11-13 claim-boundary correction: nonlinear lattice evidence

The manuscript's former LATTICEEASY subsection described specific
$256^3/512^3$ runs, sub-percent energy conservation, a lattice Floquet
exponent, a dark-matter relic density, defect statistics, and entropy
outputs. The current canonical repository does not expose the solver,
complete run inputs, raw configurations, or machine-readable outputs
needed to reproduce those numbers. The manuscript subsection has
therefore been replaced by an explicit status statement and a
reproduction checklist. Those historical numerical values are
withdrawn from the verified-results record; they are not accepted
evidence for Gates 5, 6, or 8.

Two regression tests were added to ensure that the manuscript keeps
this boundary explicit and describes the proxy-fluid as a
phenomenological closure. The new tests are awaiting the next CI run.


## 2026-11-14 final particle-basis validity gate

The expanding-background mode solver now distinguishes three independent
conditions before reporting an instantaneous occupation number:
(i) the final canonical frequency squared is positive;
(ii) the final first-order WKB measure
$|\\dot\\Omega_k/\\Omega_k^2|$ is no larger than the declared
threshold (default 0.1); and (iii) the canonical Wronskian remains within
the numerical tolerance. A positive final frequency by itself is not
enough to define an adiabatic particle basis. If any condition fails,
the mode occupation is NaN and a finite-band number density is withheld.
The same validity flag is propagated through the waterfall spectrum and
its fixed-band resolution helper.

Two numerical regression tests cover a positive-frequency but rapidly
varying final mass history, verifying that the mode occupation and
spectrum density are withheld. A manuscript source test guards the
claim boundary. The default threshold is a conservative numerical
criterion, not a physical constant; convergence under changing this
threshold remains required before a production result.

### Verification checkpoint

- Workflow run 43501562655, on the previous PR head
  859353fcefcf7ced7efb434d98b31a1ffac97e8d, completed successfully:
  **72 Python tests passed**, the four-trajectory two-scale smoke scan
  passed, and the 41-page LaTeX manuscript compiled and was uploaded.
  The final LaTeX log has zero reported Overfull \\hbox warnings.
- The smoke-scan artifact contains exactly four trajectories, not the
  full 100. The zero-seed rows remain exact classical invariant controls.
  The two nonzero-seed rows were classified as non-quartic or
  insufficient-oscillation-data; neither establishes the proxy-fluid
  regime. These four rows are a CI smoke check only.
- The final-WKB code, documentation and three new regression tests
  bring the branch to 75 tests. They are newer than run 43501562655
  and therefore remain **pending fresh CI verification**.
- The complete 100-trajectory high-resolution scan has not yet produced
  an inspected, validated artifact on the current PR head. No full-scan
  regime conclusion is claimed.

Gate 6 remains **NOT MET**. The mode calculation is still linear on a
prescribed single-field background, has a finite momentum band, and
contains no mode backreaction, rescattering, nonlinear fragmentation,
or entropy dilution. Gates 5 and 7 remain **NOT MET**; the real-scalar
$Z_2$ defect problem and microscopic proxy-fluid perturbation closure
are unresolved. PTUM is not 10/10.


## 2026-11-14 fresh CI verification (supersedes earlier pending checkpoint)

The manuscript wording regression introduced with the final-WKB particle-basis guard was initially stale: workflow 43580694626 reported 74 passed and one failed because the test expected the older phrase "occupation number is withheld", while the manuscript correctly states that both the occupation number and associated finite-band number density are withheld. The regression assertion was aligned to the actual manuscript wording in commit 82ab0f26014de58634386efd1d90b635f6ec9e45.

Fresh PR workflow 43580982470 on that head completed successfully:
- Python regression suite: **75 passed**.
- Two-scale CI smoke scan: four of four integrations succeeded (two per scenario).
- Both scenarios returned one `insufficient_oscillation_data` and one `non_quartic` classification. No quartic proxy-fluid realization was demonstrated.
- LaTeX manuscript build and PDF artifact upload: passed.
- The LaTeX log contains no reported Overfull \\hbox warnings, but it still contains Underfull \\hbox warnings and two float-placement warnings (`h` changed to `ht`). Gate 10 therefore remains PARTIAL rather than clean.

This is a four-trajectory smoke scan only. The 100-trajectory full scan, its strict-JSON artifact, solver-tolerance/time-grid convergence, and classification-stability checks remain outstanding. The full scan must run on an isolated `ptum/full-scan-*` branch so it cannot supersede or cancel the PR workflow.

Gate 10 remains **PARTIAL**. Gates 2--9 retain the statuses in the matrix above; no acceptance gate is promoted by a passing software-only smoke run. PTUM remains **NOT 10/10**.


## 2026-11-14 latest-head verification and full-scan isolation

The documentation-only follow-up commits are on PR head
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`. Workflow
`43582227619` completed successfully on this exact head:
- **75 passed** in the Python regression suite;
- four of four smoke integrations succeeded, with zero integration
  failures;
- each scenario still produced one `insufficient_oscillation_data`
  and one `non_quartic` classification;
- the LaTeX PDF build and artifact upload succeeded.

The LaTeX log still contains numerous Underfull \\hbox warnings and
two distinct `h`-to-`ht` float-placement warnings. No Overfull
\\hbox warning or LaTeX error was reported. This is a successful
build, not a warning-free manuscript. Gate 10 remains PARTIAL.

An isolated full-scan execution branch,
`ptum/full-scan-2026-11-14-r2`, was created from this PR head and
received execution-manifest commit
`c101aaed58e44c9f0159ebb806a84d670cd892e2`. It is configured to
run the 100-trajectory full profile without modifying the PR branch
or `main`. At this checkpoint, no completed run or validated 100-row
artifact has been confirmed; the scan result is not yet evidence.

No physical gate is promoted by the 75-test CI result. The coupled
quantum-seeded inhomogeneous waterfall, nonlinear backreaction,
rescattering, converged spectrum/relic calculation, proxy-fluid
microphysics, thermal history, and independent CLASS/Cobaya
reproduction remain unmet or partial as listed in the matrix.


## 2026-11-14 analytic real-psi defect-topology progress

The real waterfall scalar has a genuine pair of degenerate minima in the
unbiased broken phase. The manuscript now derives the planar kink and its
flat-space tension,
`psi_wall=v tanh(mu_eff z/sqrt(2))` and
`sigma_wall=2 sqrt(2) mu_eff^3/(3 lambda_psi)`, at fixed
post-threshold background. It also derives the spinodal source for a
linear tilt `-epsilon_bias psi`, the small-bias vacuum splitting
`DeltaV ~= 2 epsilon_bias v`, and necessary order-of-magnitude
conditions for annihilation before wall domination and BBN.

The new `ptum_defects.py` implements the exact tilted-quartic stationary
minima, the spinodal threshold, the kink tension, and conditional
annihilation/domination estimates. Seven regression tests cover the
static kink equation, numerical tension integral, small-bias splitting,
spinodal disappearance of the false vacuum, zero-bias persistence, the
necessary bias bound, and the dimension-five operator-to-source mapping.

This is analytic defect-topology progress only. The renormalized
`<O_SM>`, Wilson coefficients, thermal history and actual bias are not
specified, and no expanding inhomogeneous network, formation probability,
wall evolution, backreaction or rescattering has been computed. Gate 5
therefore remains **NOT MET**. The new tests and manuscript change are
pending the next CI result.


## 2026-11-14 tilted-domain-wall diagnostic API regression

Workflow `43584145515` on PR head
`5d5247163e52effb8c4edeff26b9cc99a16f0ff4` ran 83 tests and reported
82 passed, 1 failed. The failure was a real public-API omission:
`_tilted_minima` computed the dimensionful true and false stationary
minima, but `domain_wall_bias_diagnostics` did not return those two
values. The moderate-bias regression therefore raised `KeyError:
'true_minimum'`. No physics tolerance was involved.

The diagnostic now exposes `true_minimum` and `false_minimum` as
dimensionful field values, and returns `None` for both when the
metastable minimum disappears at/above the spinodal. The regression
now checks the stationary cubic
`y^3-y-b=0`, positive curvature `3y^2-1>0` at both minima, the
direct potential difference, and the spinodal absence of both minima.
The correction is on the authorized PR branch; a fresh full CI run is
required before marking Gate 10's software status improved.

This does not change Gate 5: the analytic tilted-potential minima and
flat-space kink do not determine the renormalized SM condensate, the
actual bias, the expanding defect-network evolution, or its formation
probability. Gate 5 remains **NOT MET**.

## 2026-11-14 fresh verification after tilted-minimum API fix

Workflow `43585095937` completed successfully on the current PR
head `3f78946668bd43d59953ead562abf158105ec595`:
- **83/83 Python regression tests passed**.
- The two-scale CI smoke scan completed all four integrations with
  zero integration failures.
- Each scenario still contained one
  `insufficient_oscillation_data` and one `non_quartic` result;
  no quartic proxy-fluid phase was demonstrated.
- The 42-page manuscript PDF compiled and was uploaded.
- The final LaTeX pass reported no Overfull `\\hbox` warnings and
  no unresolved-reference warning, but retained numerous Underfull
  `\\hbox` warnings and two `h`-to-`ht` float-placement warnings.
  This is a successful build, not a warning-free build.

The regression failure in workflow `43584145515` (82 passed, one
`KeyError`) is resolved by returning the exact stationary minima
from `domain_wall_bias_diagnostics` and testing their stationarity,
positive curvature and spinodal disappearance. Gate 10 remains
**PARTIAL** because manuscript warnings remain and the full reproducible
100-trajectory scan has not yet been inspected.

The isolated full scan run `43582371029` on
`ptum/full-scan-2026-11-14-r2` remains in progress at the time of this
checkpoint. It was launched from the earlier PR head
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`, before the latest
domain-wall diagnostic API correction. No full-scan artifact is
available yet. Its output may be used only after verifying that the
scan-relevant source and configuration are identical to the current
PR head; otherwise the scan must be rerun from the current source.


## 2026-11-14 conditional finite-temperature fermion bias estimator

The real-`psi` defect analysis now includes a finite-temperature,
zero-temperature-subtracted ideal Dirac-gas contribution to the
dimension-five operator bias. For a broken-phase mass eigenstate with
fixed mass and diagonal real mass-basis coupling
`y_psi_f=Re[(C_f)_ii] v_H/(sqrt(2) Lambda)`, with `v_H` the
fixed broken-phase Higgs expectation value, the code evaluates the Fermi-Dirac
integral for `Delta_T <bar(f)f>` and returns the signed source in
the convention `V_bias=-epsilon_bias psi`. The relativistic limit
is `Delta_T <bar(f)f> -> N_c m_f T^2/6`. The manuscript records the
same integral and its sign convention.

The implementation is explicitly conditional: equilibrium free
Dirac gas, fixed broken-phase masses and Higgs expectation value,
zero chemical potential, and no gauge/QCD corrections, thermal
masses, electroweak crossover, non-equilibrium production or
renormalized vacuum condensate. No Wilson coefficients, cutoff,
thermal history or actual PTUM bias are assigned. The result is a
parameterized one-loop estimate, not a wall-lifetime prediction.

Six regressions cover the relativistic limit, dimensional scaling,
zero-mass/zero-temperature limits, signed-coupling cancellation,
input validation and manuscript claim boundaries. The branch now
contains 89 Python tests by source count; the new tests and LaTeX
equations await fresh CI. Gate 5 remains **NOT MET** because the
actual bias and expanding inhomogeneous defect network are not
calculated.


## 2026-11-14 thermal-bias LaTeX layout correction

Workflow `43586022884` completed successfully on
`9902041fa8c2dfaf52eab213cfbbd82612e67b58`: 89 Python tests passed,
all four smoke integrations succeeded, and the 42-page manuscript
compiled. The final log audit nevertheless found an Overfull
`\\hbox` at the long inline broken-phase coupling expression in
the new thermal-bias paragraph. The coupling has been moved to a
display equation in commit `d9455781f0a643f6c1b2badc199bf2fb6fedcab7`.
The fresh LaTeX build on that latest source is pending; Gate 10 stays
PARTIAL until the new log is checked. The previous build also retained
numerous Underfull `\\hbox` warnings and two float-placement warnings.
