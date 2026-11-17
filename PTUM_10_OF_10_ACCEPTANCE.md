# PTUM 10/10 Scientific Acceptance Matrix

This file defines the evidence required before PTUM can be called scientifically and computationally ready. A passing CI workflow is necessary but not sufficient. A phenomenological ansatz is not counted as a microscopic derivation, and an author-reported result is not counted as independently reproduced.

## Acceptance gates

| Gate | Required evidence for 10/10 | Current status |
|---|---|---|
| 1. Complete action and conventions | One explicit covariant action; fixed metric/sign conventions; all fields, dimensions, gauge representations, potentials, couplings, real/complex field choices and symmetry-breaking structure specified | **MET (classical tree-level EFT)**. The minimally coupled Einstein + PTUM + chiral-SM action, field representations, canonical dimensions, Higgs and Yukawa potentials, dimension-five PTUM operators, and the explicit \(\psi\)/\(\Phi_{\rm res}\) symmetry scope are now specified. Quantum/UV completion remains outside this gate and open separately |
| 2. Inflation-to-waterfall connection | Exact inflation endpoint; threshold crossing in the same coupled background; stability of all modes before crossing; quantum seed prescription | **PARTIAL**. Exact epsilon_H endpoint is computed; post-threshold scan velocities are now taken from the integrated single-field FRW trajectory at each offset, but the coupled crossing and quantum seeds are not evolved |
| 3. Hilbert tensors and conservation | Every sector tensor derived from the same action; all Q_i^nu derived; sum of currents cancels; numerical conservation converges independently with solver tolerance and timestep | **PARTIAL**. The classical tree-level gauge, Higgs, chiral-fermion and PTUM Hilbert tensors and all interaction currents are now written from one action; the current solver does not evolve SM fields, and full-sector numerical conservation/timestep-tolerance convergence is not yet demonstrated |
| 4. Background numerical solution | Stable expanding-FRW integration; positivity/domain checks; independent energy and continuity diagnostics with robust background-energy normalization; timestep and solver-tolerance convergence | **PARTIAL**. The separate 100-row 4,001- and 256,001-point scans and the 36/36 four-case tolerance probe completed. The separate jobs recomputed the exact endpoint independently, producing a tiny relative difference in Phi_c (2.3e-15); their normalized row join is therefore not a strictly identical-input grid test. A paired 400-run study now reuses identical parameters and initial conditions across both grids and three tolerances; coupled inhomogeneous dynamics remain open |
| 5. Waterfall/tachyonic dynamics | Inhomogeneous mode evolution, correct vacuum initial conditions, lattice or validated mode treatment, backreaction, rescattering and a defect-topology analysis (including the Z2 domain-wall risk of a real waterfall scalar) | **NOT MET**. Current scan is homogeneous and post-threshold |
| 6. Resonance and relic abundance | Expanding-background mode equations; converged monodromy/Floquet growth; momentum integration; backreaction; thermalization and entropy dilution; independently reproduced relic abundance | **NOT MET**. A linear mode integrator now evolves supplied expanding-FRW histories with an adiabatic-vacuum check and Wronskian monitor, and a finite-band trapezoidal momentum integral is implemented. The background is not generated self-consistently, the momentum tails and grid are not converged, and no backreaction or entropy dilution is available |
| 7. Proxy-fluid realization | Demonstrate a stable parameter region with the required averaged equation of state, sound speed and anisotropic stress from the dynamics; show convergence and perturbative stability | **NOT MET**. The closure remains phenomenological; no microscopic realization is established |
| 8. Reheating and entropy | Full energy partition from the coupled trajectory; decay/thermalization rates; BBN-compatible thermal history; comoving entropy calculation | **PARTIAL**. Conditional potential-dominated T_rh estimate only; branching and thermalization are not computed |
| 9. Observational reproducibility | Public exact CLASS patch; pinned version/commit; complete configs, likelihoods, data, chains and commands; independent rerun reproduces posteriors and model comparison | **NOT MET**. Reported numbers are author-reported; patch availability and chains remain unverified |
| 10. Software and manuscript reproducibility | Pinned environment; deterministic seeds; strict data schemas; full CI; clean LaTeX build; no unresolved references or contradictory claims; artifact hashes | **PARTIAL**. Workflow 43843783240 on head 32f33013 reported 131 Python tests passed, the 4/4 smoke scan, both 100-row scans and the 36/36 targeted convergence probe passed, and the 42-page PDF built. The final LaTeX log still reports 73 Underfull and one Overfull hbox warning. A paired full-grid convergence job has been added and awaits fresh CI |

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



## 2026-11-15 bounded scan execution and fresh CI checkpoint

The previous isolated full-scan attempt, workflow `43582371029` on
source head `d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`, completed only
20 of 100 trajectories before the hosted runner received a shutdown
signal. The full-scan step was cancelled and no scan JSON/checkpoint
artifact was uploaded. This is an execution failure, not a physical
result; no regime conclusion is drawn from those 20 rows. The old
attempt predates the deterministic solver-work guard below.

The homogeneous integrator and scan runner now:
- count RHS evaluations for every DOP853 trajectory;
- stop a trajectory after a configurable default budget of 100000 RHS
  evaluations, recording the exact attempted count and limit;
- classify a budget-exhausted trajectory as failed, never as a physical
  regime;
- preserve solver method, tolerances, evaluation count and budget status
  in the strict-JSON checkpoint and final summary; and
- print the initial conditions before each trajectory so a stalled row
  is identifiable from the workflow log.

The 100000-call limit is an engineering fail-closed guard, not a physical
cutoff and not a relaxation of `rtol=1e-9` or `atol=1e-12`. Any row
that reaches it remains a failed integration and prevents a passing full
scan. This change is intended to turn an indefinitely long adaptive solve
into an inspectable failure while allowing the remaining grid points to
be attempted.

Workflow `43701174233` completed on PR source head
`5379ec8a2e85e875c9819121b0409ea454cf99e9`:
- **93 Python regression tests passed**;
- all four two-scale smoke integrations succeeded;
- each scenario still returned one `insufficient_oscillation_data`
  and one `non_quartic` result, so the smoke scan does not establish
  quartic proxy-fluid behavior;
- the 42-page manuscript PDF compiled and uploaded;
- the final log audit found no Overfull `\\hbox` warnings and no
  float-placement warnings after splitting the thermal-condensate
  equation and changing two table placements to `[htbp]`;
- Underfull `\\hbox` warnings remain and require a typography review.
  Citation warnings occur during the initial LaTeX pass and are resolved
  by subsequent `latexmk` passes; no unresolved-reference warning is
  present in the final pass.

The fresh full scan has been explicitly armed on PR #2 by a temporary
title marker and is running as workflow `43701420639` on source head
`af9724092c94d8469fcf23a87f29438b2cf8c58a`. The title marker has been
removed after the workflow was queued. At this checkpoint the full-scan
job is in progress; no 100-row artifact or result is yet accepted.

Gate 4 remains **PARTIAL** until timestep and solver-tolerance convergence
are measured. Gate 10 remains **PARTIAL** because Underfull warnings
remain and the bounded full scan is not yet inspected. Gates 5, 6, 7 and
9 remain **NOT MET**. No physical acceptance gate is promoted by the
93-test result or four-row smoke scan. PTUM is **NOT 10/10**.


## 2026-11-15 full-scan artifact audit and current-head verification

Workflow 43701420639 produced a complete 100-row JSON artifact on
source head af9724092c94d8469fcf23a87f29438b2cf8c58a. The job log
shows that this run actually used DOP853 with a 100000-RHS evaluation
budget, not the later intended Radau/1000000 profile. The artifact
digest is sha256:4f98f4320ff5cfccb2917607270a8be86ee20eb9ed21b1e71ec8441660ce5722.
The file parses as strict JSON and contains 100 rows with no NaN or
Infinity tokens:
- High-scale threshold-matched: 49/50 integrations succeeded; 47
  were classified non_quartic, 2 insufficient_oscillation_data, and
  1 failed at the RHS budget.
- Low-scale underdamped control: 48/50 integrations succeeded; 41
  were classified non_quartic, 7 insufficient_oscillation_data, and
  2 failed (one RHS budget exhaustion and one non-finite total density).
- None of the 97 successful rows had quartic_achieved=true.

This artifact is a diagnostic failure record, not an accepted full-scan
result. Comparing source af972... with the current scan source
ca053f58e3713b274e22f0d69bd5ca89863dab26 shows 21 intervening commits
and modifications to ptum_task1_scan.py, ptum_task1_simulation.py,
the workflow and regression tests. Therefore the 97 successful rows
must not be reused as validation of the current implementation.

The latest PR-head verification is now:
- Workflow 43702269416 on the previous head had 96 passed and 2 failed.
  Both failures came from synthetic successful-scan fixtures that did
  not contain all fields required by the strict summary schema. The
  production simulation result schema was not weakened; the fixtures
  were completed in commit ca053f58e3713b274e22f0d69bd5ca89863dab26.
- Workflow 43703059616 then passed 98 tests and all four smoke
  integrations. Its one overflow warning was the deliberate
  non-finite-state regression path; that warning is now explicitly
  asserted rather than left unexamined.
- Workflow 43703509401 on commit b0aa8b32c67a90e0981826ac44c7470c37ff7ce4
  passed 98 tests with no warnings in the pytest summary, all four
  smoke integrations, and the 42-page LaTeX build/PDF upload.
- Each smoke scenario still contains one insufficient_oscillation_data
  and one non_quartic row. The smoke test does not establish the
  quartic proxy-fluid regime.
- The final LaTeX build has zero Overfull hbox and zero float-placement
  warnings. Underfull hbox warnings remain (213 log messages across
  repeated latex passes); the final pass has no unresolved references.

A fresh 100-trajectory run is being triggered from the current PR source
using the workflow's explicit Radau profile, rtol=1e-9, atol=1e-12 and
a 1000000-RHS per-trajectory engineering budget. Its artifact must be
inspected independently. Gate 4 remains PARTIAL until time-grid and
solver-tolerance convergence are measured. Gate 10 remains PARTIAL
because the manuscript still has Underfull hbox warnings and the
current full scan is not yet validated. No physical gate is promoted
by the older DOP853 artifact or the four-row smoke scan.


## 2026-11-15 primordial-background and mode-spectrum claim audit

The public ptum_inflation_background.py module generates the
eight-point scalar-dominated FRW background and first-order
Hubble-flow table. The regression suite checks all eight rows,
the requested 60-e-fold duration, and key reference observables.
This supports reproducibility of the background scan only.

The separately described 200-mode Mukhanov-Sasaki integration is
not reproduced by that module. Its mode solver, raw spectra and
numerical outputs are absent from the repository. The manuscript's
previous wording that called the mode integration numerically
verified with the public background script has been corrected:
the mode-spectrum agreement is now explicitly AUTHOR-REPORTED.
Gate 9 remains NOT MET because neither this mode-spectrum result nor
the CLASS/Cobaya likelihood pipeline has been independently
reproduced. No observational acceptance is inferred from the
background-only CI test.

## 2026-11-15 current-source Radau scan audit and LaTeX regression repair

Workflow 43703987436 ran the 100-trajectory profile on source
f16c89d5a5d8b0506c569cc073688cb435494fad with Radau,
rtol=1e-9, atol=1e-12, and a 1,000,000-RHS engineering guard.
Its uploaded artifact ptum-two-field-full-scan has ZIP digest
sha256:464c73c9907115ce6bc57ec53722fcc4ede4d8f17d0e66db856fcef00f8876a2.
The extracted results JSON contains exactly 100 rows, parses with
non-standard JSON constants rejected, and contains no non-finite
numeric values. The extracted JSON SHA-256 is
b348651738c1a5d35d15432ef2f1d8873ddfa9ea827238f84c1772b6ac1593e3.

- High-scale threshold-matched case: 49/50 integrations succeeded;
  47 successful rows were non_quartic, two were
  insufficient_oscillation_data, and one integration exhausted the
  RHS budget.
- Low-scale underdamped control: 49/50 integrations succeeded;
  42 successful rows were non_quartic, seven were
  insufficient_oscillation_data, and one integration exhausted the
  RHS budget.
- The two failures have the same initial-condition tuple in their
  respective dimensionful benchmarks:
  psi_init=4.460941604639096e12,
  psi_dot_init=0,
  phi_offset=2.4014653823994024e16.
  Both reached 1,000,001 attempted Radau RHS evaluations against the
  1,000,000 limit. They remain failed integrations, not physical
  classifications.
- None of the 98 successful rows satisfies the joint quartic
  classifier. This is a negative result for this finite homogeneous
  post-threshold grid only; it does not rule out other parameter
  regions or inhomogeneous dynamics.
- The median/max finite-difference continuity residual normalized by
  H rho is 3.7233e-2 / 3.7234e-2 for the high-scale rows and
  4.0332e-6 / 1.7795e-4 for the low-scale rows. The chain-rule
  residuals are smaller, but the high-scale maximum reaches
  1.6846e-10. These discrepancies make output-grid and solver
  tolerance convergence mandatory; the 4001-point output is not yet
  accepted as converged.
- Comparing scan source f16c89... with PR head 31b1be... shows
  only documentation and main.tex changes; ptum_task1_scan.py,
  ptum_task1_simulation.py, and the scan workflow are unchanged.
  The artifact is therefore relevant as a diagnostic of the current
  scan implementation, but it fails the all-100-integrations-success
  acceptance requirement.

Workflow 43704489063 on source head 31b1be... passed all 98
Python regressions and the four-row smoke scan, but the LaTeX job
failed with Improper prevdepth at the section following the
Mukhanov-Sasaki subsection. The source contained an orphaned
begin{itemize} with no item and no matching end{itemize}.
Commit c75b972e9ff14d0b576a9436c0486cf8a6112b84 removes that
invalid list, rewrites the subsection so the unavailable 200-mode
calculation is consistently labelled AUTHOR-REPORTED, and avoids
presenting it as a reproduced Planck result. Two regression tests
were then added in commit
68d7a53672bd6a076bfbcd7f4e2828d554c05bfe: a nested LaTeX-environment
balance check and a mode-spectrum claim-boundary check. The source
now contains 100 test functions; these two additions and the LaTeX
repair are awaiting a fresh workflow run.

Gates 4 and 10 remain PARTIAL. Gates 5, 6, 7 and 9 remain NOT MET.
No gate is promoted by the 98 successful scan rows, the smoke scan,
or the Python-only success. PTUM is NOT 10/10.

### Follow-up CI result for the LaTeX repair

Workflow 43705365503 confirms that the orphaned-list correction compiles:
the 42-page PDF was produced, with zero Overfull hbox warnings, zero
float-placement warnings, zero Improper prevdepth errors, and no
unresolved citations or references on the final LaTeX pass. The log
still contains 138 Underfull hbox messages, so Gate 10 is not warning-free.

The same workflow ran 100 Python tests: 99 passed and one newly added
claim-boundary test failed because the phrase "not independently
reproduced" was split across a source newline. This was a brittle
whitespace assertion, not a scientific-code failure. Commit
a5f86d7c8ca746e6948cfa5c391d11a63985ab87 normalizes whitespace before
checking the phrase. The 100-test suite after this test-only correction
is pending fresh CI verification.

### Fresh full verification after the claim-test correction

Workflow 43705535067 on PR head
49933f4f1593327845944266e3412e67a3b545f3 completed successfully:
- Python regression suite: 100 passed in 12.81 s.
- Four-trajectory two-scale smoke scan: 4/4 integrations succeeded.
  Each scale still contains one insufficient_oscillation_data and one
  non_quartic row; this is not evidence of a quartic phase.
- LaTeX: 42-page PDF built and uploaded. Final pass has zero Overfull
  hbox, zero float-placement warnings, zero Improper prevdepth errors,
  and zero unresolved citation/reference warnings. There are still
  138 Underfull hbox messages across the build log.

The new environment-balance and whitespace-normalized claim-boundary
tests both pass. Gate 10 remains PARTIAL because the full 100-row scan
has two failed integrations, solver/time-grid convergence is open,
and Underfull hbox warnings remain. No physical gate is promoted.

### 2026-11-15 manuscript update from the Radau artifact

The critical numerical-status paragraph in main.tex now reports the
current 100-row Radau artifact rather than saying the revised scan is
still uninspected. It records 98 successful integrations and two
RHS-budget failures; no successful row passes the joint quartic
classifier. The high-scale maximum Q is about 1.002, below the Q>2
energy-dominance boundary. The low-scale control has transient
large-seed rows with Q up to about 11.12, w about 0.363 and virial
ratio about 0.890, but only two half-cycles in the final 20 percent,
so the late-time adiabatic diagnostic is unavailable. These are not
a sustained quartic-fluid realization.

The manuscript now states that the BDF cross-check at unchanged
rtol=1e-9, atol=1e-12 and the same RHS guard is running on isolated
execution PR #5. A regression test guards the updated scan-status
claim. The new 101-test source suite is awaiting fresh PR CI.

The 98-row Radau artifact remains diagnostic rather than accepted
converged evidence: two rows failed, output-grid/tolerance convergence
is absent, and the scan is homogeneous and post-threshold. Gates 4
and 10 remain PARTIAL; Gate 7 remains NOT MET.

### 2026-11-15 BDF versus Radau solver cross-check

The isolated BDF full scan (workflow 43705977596, execution PR #5)
produced 100 strict-JSON rows with no non-finite numeric values.
Artifact ZIP SHA-256:
8ec851ad0e92e554a34014d5f5f7227fc305519052aab60014a40ab3bac851e3.
Extracted JSON SHA-256:
7cd7c40081788262d92823846b20ddf4dcf70d30c6c1c97bda011300f6d7bd34.

BDF also completed 98/100 trajectories and exhausted the same
1,000,000-RHS guard on the exact same two rows as Radau. All 98
common successful rows have identical regime labels. Relative
differences between Radau and BDF final values are small:
max 5.99e-7 in Phi, 1.11e-6 in Phi_dot, 4.66e-5 in psi,
2.36e-3 in psi_dot, 6.06e-7 in H, 1.21e-6 in total rho,
and 2.29e-4 in final averaged w. Classification diagnostics agree
closely: max relative differences are 1.27e-5 in Q, 1.32e-6 in w,
and 3.98e-5 in the virial ratio. The maximum absolute difference in
the chain-rule residual diagnostic is 1.15e-10; for the
finite-difference residual normalized by H rho it is 3.33e-6.

This is cross-method agreement for the 98 successful rows, not a
solver-tolerance or output-grid convergence proof. Both methods
fail at the same two trajectories, and the scan remains incomplete.
The next targeted solver probe is DOP853 on those two rows; do not
raise the RHS budget without first inspecting solver behavior.

The follow-up PR #2 workflow 43706959822 on source head
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0` completed successfully:
- The current regression source contains 103 test functions; the
  Python regression job passed.
- All four two-scale smoke integrations passed.
- The LaTeX manuscript build and PDF artifact upload passed.
- The full 100-trajectory scan was skipped in this regular PR run;
  it is handled on an isolated execution branch.

The previous 101-test pending note is superseded by this fresh
successful workflow. Latest-content verification workflow 43754277984 (isolated CI PR #8)
passed all 103 Python regression tests, the four-trajectory two-scale
smoke scan, and the LaTeX build. The manuscript PDF is 42 pages.
The final LaTeX pass has zero unresolved references, zero unresolved
citations and zero Overfull hbox warnings, but 74 Underfull hbox
warnings remain. Gate 10 therefore remains PARTIAL, not warning-free.

### 2026-11-15 current-source DOP853 execution

The earlier DOP853 execution PR #6 is stale: it was based on
`4227a3e50e2a0564a44a19dea2338dafa328ca53`, while the current PR #2
source at the time of the rerun is `bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`.
Its failed full-scan artifact is retained as historical diagnostic
material and is not accepted as a same-source comparison.

A new isolated execution branch,
`ptum/full-scan-2026-11-15-dop853-current`, was created directly
from PR #2 source commit
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`. Draft execution PR #7
was opened against PR #2. Workflow 43753469944 completed successfully:
the Python regression, four-row smoke scan, LaTeX build, and full
100-trajectory DOP853 job all passed. The full-scan artifact has ZIP
SHA-256
`3e758909f191c863b358424be0d7d86a253224fe066e3ceaa279368719e39c8b`;
the extracted strict-JSON result has SHA-256
`e848ff87c8fa3741d65f5fd2909d56db4af567a903d4dc05845cb081d175372c`.
It contains exactly 100 rows, all 100 integrations successful, with
no NaN/Infinity tokens. The high-scale scenario has 48 non-quartic
and two insufficient-oscillation rows; the low-scale scenario has
43 non-quartic and seven insufficient-oscillation rows. No row
passes the joint quartic classifier.

The two trajectories that exhausted the 1,000,000-RHS guard under
both Radau and BDF complete under DOP853, with 7,718 and 1,334 RHS
evaluations, respectively. Both are classified non-quartic by DOP853.
On the 98 rows successfully integrated by all three solvers, all
regime labels are identical. DOP853 versus Radau maximum relative
differences are 3.16e-9 in Phi, 1.18e-7 in Phi_dot, 4.77e-7 in psi,
9.12e-6 in psi_dot, 2.86e-10 in H, and 5.72e-10 in total density.
The maximum relative differences in Q, averaged w and virial
diagnostics are 5.95e-8, 1.81e-8 and 1.77e-7, respectively.

This resolves the all-100-integrations-success requirement for the
declared homogeneous grid using DOP853 and gives strong cross-method
agreement on the 98 common successful rows. It does not independently
validate the two DOP853-only rows against Radau/BDF, and it is not a
solver-tolerance or output-grid convergence proof. The scan remains
homogeneous and post-threshold, not a coupled quantum-seeded
inhomogeneous waterfall. Gates 4 and 10 remain PARTIAL; Gates 5, 6,
7 and 9 remain NOT MET. No physical gate is promoted by a successful
scan or software CI alone. PTUM is NOT 10/10.


### 2026-11-15 targeted tolerance and output-grid convergence

Isolated convergence PR #9 workflow 43754922200 completed:
- 36/36 DOP853 integrations succeeded across four selected trajectories.
- Python regression: 107 passed.
- LaTeX build: successful, 42-page PDF.
- Final LaTeX pass: 73 Underfull hbox warnings; zero Overfull hboxes,
  unresolved references or unresolved citations.
- Full 100-row scan was skipped in this convergence-only workflow.

The four probes were the two rows that exhausted Radau/BDF RHS budgets,
the high-scale row with the largest high-scale Q diagnostic, and the
low-scale row with the largest low-scale Q diagnostic. Tolerances were
`1e-9/1e-12`, `1e-10/1e-13`, and `1e-11/1e-14`; output grids
were 4,001 through 256,001 points.

Across tolerance changes, the maximum final-state relative difference
was 4.75e-7 and the maximum relative difference in Q, averaged w and
virial diagnostics was 3.48e-7. Across the final grid doubling
(128,001 to 256,001), all four regime labels, quartic flags and
late-half-cycle counts were unchanged. Maximum absolute changes were
7.57e-4 in Q_final, 2.57e-4 in w_final, 2.25e-4 in virial_final,
and 6.05e-4 in the maximum finite-difference continuity diagnostic.

The script now encodes provisional targeted-probe limits:
- final-state relative difference <= 1e-6;
- classification-diagnostic relative difference <= 1e-5;
- Q_final, w_final, virial_final and maximum finite-difference
  continuity-diagnostic absolute changes <= 1e-3.

All four selected probes pass these limits. The artifact ZIP SHA-256 is
`d4f80abf0e2705d3d019e67855592efaf7242ee96a90f970798119748a6bfe51`;
the extracted strict-JSON SHA-256 is
`f99e7da8644c399e3bb5ff6d6b08cbffe272ab75c99faad311689fa283a71899`.

This is targeted stability evidence for four trajectories only.
It does not establish convergence of the complete 100-row grid.
Gate 4 remains PARTIAL, and no additional physical gate is promoted.


## 2026-11-15 complete 100-row output-grid comparison

The isolated DOP853 full-grid workflow 43757836487 completed at
256,001 output points. The artifact was downloaded and inspected, not
merely inferred from a green CI badge.

- 256,001-point result: 100/100 successful rows, zero failed rows,
  100 unique row keys, complete checkpoint, DOP853, rtol=1e-9,
  atol=1e-12, 20 mu^-1 duration and the unchanged 1,000,000 RHS guard.
- Direct 128,001 -> 256,001 comparison: all six final-state variables
  (Phi, Phi_dot, psi, psi_dot, H, rho_total) are bitwise-identical in
  the serialized JSON for all 100 rows. The adaptive solver nfev counts
  are also identical. All regime labels, quartic flags, oscillation
  counts, late-half-cycle counts and adiabaticity flags are unchanged.
- Q_final: 96 finite rows; maximum absolute change 1.1011e-3,
  median absolute change 9.5536e-7, maximum symmetric relative change
  1.1297e-4. The maximum occurs in the low-scale control with
  seed=5, velocity=1, offset=0.01.
- w_final: 96 finite rows; maximum absolute change 3.4015e-4,
  median absolute change 1.5264e-4. Its largest relative difference is
  not a useful convergence measure because at least one value is close
  to zero and the estimate changes sign.
- virial_final: 96 finite rows; maximum absolute change 3.4157e-4,
  median absolute change 2.9904e-7, maximum symmetric relative change
  3.7693e-4.
- The median ratio of the finite-difference continuity residual
  (256,001 / 128,001) is 0.5003, consistent with first-order
  output-difference refinement; the observed range is 0.4499--1.0294.
  The sampled maximum chain-rule residual is not monotone: its median
  ratio is 1.0 and its maximum ratio is 11.88, indicating a newly
  resolved local maximum rather than uniform reduction.
- Against the archived 4,001-point baseline, final-state relative
  differences remain bounded by 8.3194e-8 across the six state
  variables, and no classification field changes. However, the
  maximum absolute Q_final, w_final and virial_final changes remain
  6.5194e-2, 1.9880e-2 and 1.9403e-2, respectively. The original
  4,001-point output grid therefore undersampled some cycle-averaged
  diagnostics.
- The provisional 1e-3 absolute Q grid limit is exceeded slightly
  (1.1011e-3) in one row. No tolerance has been relaxed. Full diagnostic
  convergence is still not declared; Q requires a denser or
  independently integrated cycle-average estimator and a justified
  error bound. Gate 4 remains PARTIAL.

Artifact SHA-256:
- 4,001-point baseline ZIP:
  3e758909f191c863b358424be0d7d86a253224fe066e3ceaa279368719e39c8b
- 128,001-point ZIP:
  3e2527d127e2e32fb7ec7305086d95e44eea3bc3daf7aae5cbdf48ea8c169dec
- 256,001-point ZIP:
  882e7d72e2ab62432a0d6d9d6898aeb5922029377e2d435a619588d0f792e280

Workflow 43757836487 passed Python regression, the 100-row refined-grid
scan and LaTeX build. This verifies the scan and build at that head;
it does not close the physical waterfall, backreaction, relic or
observational gates.


## 2026-11-16 latest CI and full-scan opt-in

The last completed workflow on the pre-opt-in commit
`bc1f6dafb689be427631ae3baa79692b9fde1694` was
`43759304001`:

- Python regression: **108 passed** in 20.24 s.
- The two-scale smoke scan completed **4/4** trajectories with zero
  failed integrations.
- The LaTeX job produced a 42-page PDF. Its final pass retained
  73 Underfull hbox warnings and one Overfull hbox at source line 1937.
  The earlier-pass undefined-reference messages disappeared by the
  final pass; the build is successful, but not warning-free.
- The full 100-row scan and targeted convergence jobs were skipped
  because the PR had not yet opted into the long verification path.

To prevent that gap recurring, PR #2 was marked `[FULL-SCAN]`.
The workflow now also runs the existing four-case tolerance/output-grid
probe for that explicit PR #2 opt-in, and a regression test guards this
condition. Workflow commit:
`37b48c41b8342597e910f03e7717c70463fba93b`; test commit:
`c5b3c95e065999dc719b1052db66e3c9855d2d82`.

The new head has not yet completed CI. The next synchronize-triggered
workflow is expected to run the 100-row DOP853 scan and the targeted
four-case convergence probe. The latter is still not a 100-row
tolerance/output-grid convergence study. Gate 4 remains PARTIAL, and
no physical gate is promoted by the successful smoke scan.


## 2026-11-16 dense-output cycle estimator ported to PR #2

The dense-output cycle estimator developed on the isolated PR #11 branch
has now been ported to the canonical PR #2 branch. The PR #2
`ptum_task1_simulation.py` was byte-identical to the estimator's
pre-change base, so the source port did not overwrite later simulation
logic. The implementation:

- locates `psi_dot=0` turning points from the adaptive ODE solver mesh,
  refines root bracketing, and rejects stationary zero plateaus and
  monotonic non-oscillatory histories;
- integrates the cycle moments for Q, quartic virial, excitation
  pressure/density and mean H with adaptive vector quadrature;
- retains the former sampled estimators separately as cross-checks;
- uses one physical-time late-tail definition for the classifier and
  dense-cycle adiabaticity test.

The port includes regressions for the harmonic analytic oracle, non-unit
mu, multiple roots per accepted solver step, root-refinement stability,
adaptive-mesh invariance, real DOP853 step-size stability, malformed
inputs, stationary/monotonic histories and nonuniform physical-time
classification.

A chunked strict-JSON 100-row, 256,001-output-point rerun has also been
added. PR #2's `[FULL-SCAN]` workflow opt-in now schedules three
distinct numerical checks: the 100-row 4,001-point baseline, the
existing four-trajectory tolerance/output-grid probe, and the new
100-row 256,001-point dense-estimator run. The high-resolution job
writes incremental checkpoints and fails closed on missing, duplicate
or unsuccessful rows.

**Validation status:** implementation and tests are committed, but no
CI result or 100-row dense-estimator artifact is claimed yet. The older
PR #11 256,001-point artifact used the sampled estimator and is
historical for the new dense implementation. Gate 4 remains PARTIAL.
The 100-row comparison will be inspected only after the new artifacts
complete; four selected tolerance probes are not full-grid tolerance
convergence.


## 2026-11-16 CI-discovered dense-cycle regressions and correction

The first PR #2 workflow after the dense-estimator port,
`43841837289`, reported **122 passed and 7 failed**. The failures
identified two implementation defects rather than scientific
disagreements:

1. Five legacy classifier regressions supplied empty dense-cycle arrays.
   Because empty arrays have matching shapes, the classifier selected
   the dense branch instead of the sampled compatibility fallback and
   returned `insufficient_oscillation_data`.
2. Two analytic dense-cycle tests ended at (4\pi). Floating-point
   (sin(4\pi)) was a tiny nonzero value with the same sign as the
   preceding sample, so the final endpoint turning point was omitted.

The correction requires at least one dense cycle before selecting the
dense classifier branch and snaps only start/end derivative values
within a scale-relative floating-point roundoff bound to zero. It does
not loosen the root-refinement criteria or any physical classification
threshold. Two direct regressions were added. Fresh CI is required;
the failed run is not treated as a pass.


## 2026-11-16 pre-fix full-scan and targeted-convergence evidence

Workflow `43841837289` ran on dense-estimator head
`f4b62bd13e80466789c40ba272bcd8ad5b0471b8`. The numerical scan jobs
completed, although the workflow as a whole did not pass because the
Python regression job found seven defects later corrected in
`a172c6a72121d63ba8391af9d35ba8d225e39403`.

**100-row 4,001-point baseline job:** 100/100 integrations succeeded,
50 in each scenario, with zero failed trajectories. The provisional
classification count was 5 quartic, 89 non-quartic and 6 insufficient.
All five quartic classifications were in the low-scale underdamped
control at the largest classical seed, (psi_{m init}=5psi_0), and
the smallest threshold offset, (0.01Phi_c). Their (Q) values were
10.65--11.07, (w) 0.372--0.374, quartic virial 0.906--0.910 and
(H/omega) about (6.9	imes10^{-5}), but they contained only four
or five late half-cycles. These are large classical-seed results, not
quantum-vacuum-seeded evidence or proof of a robust attractor. The
six insufficient rows include exact zero-seed controls; this is
consistent with the classical invariant (psi=0) subspace.

**Targeted tolerance/output-grid probe:** 36/36 integrations succeeded
for four selected cases. It tested output grids 4,001 through 256,001
points and tolerances ((10^{-9},10^{-12})),
((10^{-10},10^{-13})), and ((10^{-11},10^{-14})). All four cases
passed the targeted grid and tolerance limits. The largest adjacent
grid change in the finite-difference continuity residual was
(6.043\times10^{-4}), below the declared (10^{-3}) limit; Q,
virial and w changes were zero at the reported precision. The largest
tolerance-induced classification relative difference was
(9.38\times10^{-7}), below (10^{-5}), and the largest final-state
relative difference was (4.75\times10^{-7}), below (10^{-6}).
This is a four-case probe, not a full 100-row convergence campaign.

The 100-row 256,001-point dense-estimator job was still running when
these results were recorded. The 4,001-point scan and targeted probe
are pre-fix evidence; the endpoint-root correction changes the source
and therefore requires a fresh rerun before they can support final
acceptance. The Python job had 122 passed and 7 failed; no test failure
was hidden or waived. The correction and two focused regressions are
in commit `a172c6a72121d63ba8391af9d35ba8d225e39403`.

The manuscript built successfully to 42 pages, but the final LaTeX
pass retained 73 Underfull hbox warnings and one Overfull hbox at line
1937. Gate 4 remains PARTIAL; Gate 10 remains PARTIAL.


## 2026-11-16 second CI pass: analytic fixture dimensional mismatch

The corrected-head workflow `43842597075` reached 130 passed and one
failed test. The remaining failure was isolated to the synthetic
harmonic quadrature oracle: it passed (mu=1) (and the separate unit
test used (mu=2.5)) while leaving (m_psi) at (10^{13},mathrm{GeV}),
so the model's actual (mu=sqrt{|m_{m eff}^2|}) was about
(1.41\times10^{12},mathrm{GeV}). The synthetic trajectory's kinetic
moment was therefore (O(10^{-28})) of the potential scale, and the
reported worst-component relative quadrature error correctly became
large. This was an inconsistent test fixture, not a reason to weaken
the error estimate.

The output-grid oracle now uses (mu=mathrm{params.mu}), and the
non-unit-(mu) oracle chooses (m_psi) so the model's (mu) is
exactly 2.5 in the test's units. Both retain strict (10^{-8})
quadrature-error assertions. Fresh CI is pending.


## 2026-11-16 100-row dense output-grid comparison

Workflow `43842597075` on simulation-code head
`10cba1b7419d231811c7e3117449c4caa092831a` completed the baseline,
targeted-convergence and refined-grid jobs successfully. The Python job
had 130 passes and one failure in a synthetic test fixture; the
simulation implementation itself was unchanged by the subsequent
fixture-only correction.

The 256,001-point artifact
`ptum-full-grid-convergence-256001` (artifact ID `14213598714`,
SHA-256
`5408e45ce71558474f21d16ffae92024264108cacac3d415d142240d0b915890`)
records 100/100 successful integrations, 100 unique row keys, zero
failed rows and a complete checkpoint. It uses DOP853 with
(rtol=10^{-9}), (atol=10^{-12}), and 256,001 output points per
trajectory.

A strict row-key join to the 4,001-point baseline matched all 100 rows:

- All six final state variables ((Phi,dotPhi,psi,dotpsi,H,ho))
  were identical at the reported JSON precision.
- (Q), (w), quartic virial ratio, regime labels and quartic flags
  were identical across the two output grids.
- The maximum difference in the analytic FRW continuity residual was
  (2.98\times10^{-10}).
- The maximum finite-difference continuity residual fell from
  (3.7234\times10^{-2}) at 4,001 points to
  (6.0499\times10^{-4}) at 256,001 points, a factor of 61.5
  reduction. The median fell from (9.7020\times10^{-3}) to
  (1.6127\times10^{-4}).
- Across the 96 rows with cycle data, the maximum relative quadrature
  error estimate was (5.97\times10^{-6}), and the maximum normalized
  absolute estimate was (4.19\times10^{-8}).

The four-case targeted convergence artifact also passed 36/36 runs
across seven output grids and three solver tolerances. Its maximum
continuity-residual grid change was (6.043\times10^{-4}), maximum
classification tolerance difference (9.38\times10^{-7}), and maximum
final-state relative difference (4.75\times10^{-7}).

The baseline classifier still found only five quartic rows, all at the
largest classical seed (5\psi_0) in the low-scale control and smallest
offset (0.01\Phi_c). They had only four or five late half-cycles.
This is not evidence for quantum vacuum seeding or a broad attractor.
The 100-row tolerance campaign is still incomplete, and the corrected
test fixture in commit `7af32e39757f4b4c8cd78f2bda0b1eed9d83d345`
awaits fresh CI. Gate 4 and Gate 10 remain PARTIAL.


## 2026-11-17 current-head CI audit and paired-convergence correction

Workflow 43843783240 completed successfully on PR head
32f33013d81617ac998ddd0707be374f0bb1ecb6:

- Python regression suite: **131 passed** in 25.90 s.
- Four-trajectory two-scale smoke scan: **4/4** successful.
- Homogeneous 100-row baseline: **100/100** integrations, zero failed rows.
- Dense 256,001-point rerun: **100/100** integrations, 100 unique row keys,
  zero failed rows and a complete checkpoint.
- Four-case tolerance/output-grid probe: **36/36** successful integrations.
- LaTeX build: 42-page PDF generated successfully.

Artifact SHA-256 digests reported by GitHub Actions:
- 100-row baseline ZIP: 2ae9179bc475cc83289fc4d4216c768d2dc07c5fe2ec4e1c46eeb76ff601e690.
- 256,001-point dense ZIP: 6504e95396e1799b5162f6074d705a5afc67158291752d24cdffe6ae32be97cb.
- Targeted convergence ZIP: d8a1e2cff1d7f160053068a1a5402a46b320db2d623f690a9d665af6ecb81515.

The three extracted JSON files parse under strict JSON with NaN/Infinity
rejected. Their SHA-256 digests are respectively:
5c86db1631da9efd35f956a266edbd5c30cfdae405de1cb9e6e06029c042c1a2,
663dc5cee842f81fe67d0063e7341aa6fd6c9555ae7c24f07e76a4c055d08035,
and
12af7465fb6b840ff53bbc63fcf93d2c9b21c123e8519e61fa1aaf22b84f988f.

The two separate full scans join to all 100 normalized initial-condition
keys. Their classification labels and flags agree for all rows. Maximum
absolute differences in the cycle diagnostics are 2.01e-9 for Q,
2.00e-10 for averaged w, and 1.39e-10 for the quartic virial ratio.
Maximum symmetric relative differences in the six final-state variables
are: Phi 2.86e-13, Phi_dot 1.86e-11, psi 4.42e-9, psi_dot 8.32e-8,
H 3.36e-13, and total density 6.72e-13. The dense quadrature
relative-error estimate is at most 5.97e-6.

**Important comparison limitation:** the baseline and refined-grid jobs
constructed their endpoint-matched scenario parameters independently.
Their stored Phi_c/M_Pl values differ by about 2.3e-15 relatively,
so the absolute initial conditions differ at roundoff level even though
their dimensionless row keys match. The preceding join is a strong
near-agreement diagnostic, but it is not a perfectly controlled
same-input output-grid experiment. The finite-difference continuity
residual maximum falls from 3.7234e-2 to 6.0499e-4 (about 61.5-fold),
while the maximum difference in the chain-rule residual diagnostic is
3.87e-10. No physical acceptance gate is promoted by this comparison.

To remove that ambiguity, the workflow now includes a paired study with
one shared set of scenario parameter objects and exact initial-condition
values. It will run 100 rows in each of four profiles: 4,001 points at
1e-9/1e-12, 256,001 points at the same tolerance, then 256,001 points
at 1e-10/1e-13 and 1e-11/1e-14. This is 400 integrations and 300
row-by-row comparisons. Strict-JSON checkpoints are written after each
trajectory. The new paired study is pending CI and is not yet evidence.

The scan classifications remain 89 non-quartic, six insufficient and
five quartic. All five quartic rows are in the low-scale control at the
largest classical seed and smallest threshold offset, with only four or
five late half-cycles. They are not quantum-vacuum-seeded results and
do not establish a robust quartic attractor.

The LaTeX build remains successful but not warning-free: the final log
contains 73 Underfull hbox warnings and one Overfull hbox warning at
source line 1937. Gate 10 remains PARTIAL. Gate 4 remains PARTIAL pending
the paired study and coupled inhomogeneous dynamics.


## 2026-11-17 manuscript overfull-line correction (verification pending)

The long complex-Higgs reheating equation was split across an aligned
display, moving the interaction derivative to the right-hand side without
changing the equation or its sign. The source regression now checks the
aligned form and the derivative term. This addresses the previously
reported Overfull hbox at source line 1937 in the source layout; the
next LaTeX build must confirm whether the warning is gone. The 73
Underfull hbox warnings remain unresolved. Gate 10 stays PARTIAL until
a fresh final-pass log is inspected.


## 2026-11-17 paired-study first CI audit and manuscript source correction

Workflow 44056098156 ran on pre-regression-fix head
bf91301c788f7b318f6306ca0a1373c745695d58.

- The homogeneous 100-row, 4,001-point DOP853 baseline completed
  100/100 integrations with zero failed rows. Its strict-JSON output
  contains 89 non-quartic, five quartic and six insufficient-oscillation
  classifications.
- All five quartic labels are restricted to the low-scale control,
  psi_init=5 psi_0, threshold offset 0.01 Phi_c, with four or five
  late half-cycles. They are large classical-seed results, not
  quantum-vacuum-seeded evidence or a robust attractor.
- The four-case targeted tolerance/output-grid probe completed 36/36
  integrations and reported targeted_stability_pass=true.
- The paired 400-run, identical-input study was still running at the
  time of this audit. No paired-study result is claimed.
- Python regression reported 134 passed and two failed. Both failures
  were stale source guards: the Higgs-equation assertion retained
  doubled literal backslashes after the source reflow, and the workflow
  assertion still expected the former ptum_full_grid_convergence.py
  filename. The guards were corrected in
  fbc30429e18aab5395dd21b8f71a9f9e04cbc705, and a test was added for
  the 100 unique shared input rows and all four paired profiles.
- The 42-page LaTeX build succeeded, but inspection of the final compile
  output disproved the earlier assumption that the equation reflow had
  removed the overfull box: one Overfull hbox of 40.16039 pt remains
  at source line 1939, alongside 73 Underfull hbox warnings in the
  final pass.

The displayed Higgs equation has now been shortened by defining the
fermion/Higgs source J_H separately and splitting its two derivative
contributions across an aligned display. This is an algebraic
re-expression of the same variational equation, not a change to the
action or its signs. The regression now guards both derivative terms.
A fresh LaTeX build must verify whether the overfull box is removed.
The Underfull warnings remain unresolved. Gates 4 and 10 remain
PARTIAL; no physical gate is promoted by this CI audit.


## 2026-11-17 action-derived sector-current audit

A small independent algebraic audit module, ptum_sector_currents.py,
now evaluates the transfer four-vectors from the interaction assignments
in the full action. It covers the Phi-psi portal, the psi-Higgs portal,
the dimension-five psi O_SM/Lambda operator, and the chi-Phi_res portal.
The Higgs contribution is expressed through the gauge-invariant
nabla^nu(H^dagger H) contraction, so it includes the real-component
identity corresponding to H^dagger D^nu H+(D^nu H)^dagger H.

The derivation assigns each interaction potential to the sector stated
in main.tex. The non-owner sector receives the field-gradient derivative
of that interaction; the owner receives the negative sum. The module
therefore returns Q_Phi, Q_psi, Q_SM, Q_DM and Q_DE with their total
summing to zero algebraically. All gradients are contravariant; with
(-+++), grad^0=-dot(field). Regression tests compare the portal
derivatives against independent central finite differences, check
pairwise/current-total cancellation, and cross-check the homogeneous
Q_psi^0 sign against the existing two-field solver.

This is an algebraic current audit, not a numerical Hilbert-tensor
divergence calculation and not a full SM/Higgs/fermion evolution.
Gate 3 remains PARTIAL; no conservation gate is promoted until the
full sector fields are dynamically evolved and independent variational
and numerical convergence checks are complete.


## 2026-11-17 paired 400-run study: tolerance convergence not yet met

Workflow 44056098156 completed all four profiles with 400/400
successful integrations, 100 unique rows in every profile, zero
integration failures and 300 row comparisons. The identical-input
4,001-to-256,001 output-grid comparison passed 100/100. The two
solver-tolerance comparisons passed 188/200; 12 comparisons failed
the existing numerical acceptance limits. All classification flags
and regime labels remained unchanged, and the chain-rule residual
difference remained below 3.6e-10. However, the maximum final-state
relative difference reached 9.14e-6 against the 1e-6 limit, and the
maximum relative difference in a cycle classification metric reached
4.37e-5 against the 1e-5 limit. These are real tolerance-sensitivity
failures; no threshold was relaxed.

The failures are concentrated in the phase-sensitive final psi_dot
component for selected low-scale oscillatory rows and in relative
w_final differences where the mean is close to zero for selected
high-scale rows. The absolute w_final differences are small, but the
declared relative criterion is not met. This is not treated as a
successful convergence result.

The paired study now adds a fifth 100-row profile at rtol=1e-12 and
atol=1e-15, with the same 256,001-point grid and exact shared inputs.
This raises the study to 500 integrations and 400 comparisons. The
existing 1e-6 final-state and 1e-5 classification limits are unchanged.
The additional profile tests whether the 12 discrepancies decrease
under a further solver refinement or approach a phase/roundoff floor.
The new profile is pending fresh CI; no outcome is claimed.
