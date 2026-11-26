# PTUM 10/10 Scientific Acceptance Matrix

This file defines the evidence required before PTUM can be called scientifically and computationally ready. A passing CI workflow is necessary but not sufficient. A phenomenological ansatz is not counted as a microscopic derivation, and an author-reported result is not counted as independently reproduced.

## Acceptance gates

| Gate | Required evidence for 10/10 | Current status |
|---|---|---|
| 1. Complete action and conventions | One explicit covariant action; fixed metric/sign conventions; all fields, dimensions, gauge representations, potentials, couplings, real/complex field choices and symmetry-breaking structure specified | **MET (classical tree-level EFT)**. The minimally coupled Einstein + PTUM + chiral-SM action, field representations, canonical dimensions, Higgs and Yukawa potentials, dimension-five PTUM operators, and the explicit ψ/Φ_res symmetry scope are specified. The manuscript now displays the exact per-generation SU(3)^3, SU(3)^2U(1), SU(2)^2U(1), U(1)^3 and mixed gravitational-U(1) anomaly sums; a Fraction-based registry audit checks these and the even-doublet SU(2) Witten condition. Quantum/UV completion remains outside this gate and open separately |
| 2. Inflation-to-waterfall connection | Exact inflation endpoint; threshold crossing in the same coupled background; stability of all modes before crossing; quantum seed prescription | **PARTIAL**. Exact epsilon_H endpoint is computed; post-threshold scan velocities are now taken from the integrated single-field FRW trajectory at each offset, but the coupled crossing and quantum seeds are not evolved |
| 3. Hilbert tensors and conservation | Every sector tensor derived from the same action; all Q_i^nu derived; sum of currents cancels; numerical conservation converges independently with solver tolerance and timestep | **PARTIAL**. The classical tree-level gauge, Higgs, chiral-fermion and PTUM Hilbert tensors and all interaction currents are now written from one action; the current solver does not evolve SM fields, and full-sector numerical conservation/timestep-tolerance convergence is not yet demonstrated |
| 4. Background numerical solution | Stable expanding-FRW integration; positivity/domain checks; independent energy and continuity diagnostics with robust background-energy normalization; timestep and solver-tolerance convergence | **MET for the homogeneous two-field post-threshold background domain**. The historical 500/500 DOP853 integration suite and its paired comparisons remain valid. On exact code head `c42a9a8e7007fc223297b475282a729d5a068595`, the fresh 100-row sensitivity scan completed 100/100 with zero failures. The targeted convergence study completed 36/36 runs and passed all four case summaries. The full paired study then completed 500/500 integrations and 400 comparisons across the same 100 initial conditions: all 100 output-grid comparisons passed; every finite-difference continuity residual decreased from 4,001 to 256,001 points, with median observed order 0.9906 and minimum reduction factor 1.3797. Successive tolerance refinements passed 98/100, 99/100 and 100/100 rows; the state and classification error envelopes decreased monotonically, all flags and metric availability remained unchanged, and the finest adjacent comparison passed 100/100. Three earlier pairwise comparisons exceeded the strict state threshold but were resolved by subsequent refinement; they are not hidden or counted as passing. This gate remains scoped to homogeneous post-threshold equations and does not close Gates 2 or 5 |
| 5. Waterfall/tachyonic dynamics | Inhomogeneous mode evolution, correct vacuum initial conditions, lattice or validated mode treatment, backreaction, rescattering and a defect-topology analysis (including the Z2 domain-wall risk of a real waterfall scalar) | **NOT MET**. A second-order adiabatic finite-band subtraction for the scalar field variance is implemented with Wronskian and exact-limit controls, but no renormalized stress tensor, force, or lattice counterterm is available. The branch contains a periodic 3-D nonlinear classical lattice prototype, a bare first-order WKB Gaussian initializer and a finite-grid wall estimator. The exact-head fixed-box/fixed-spacing UV audit (workflow 45152898999, commit `150487cf9f92684b2120310948e8a9d050f4f13d`) covers 11 grid sizes N=4,...,64: at fixed L=8 mu^-1 the unsubtracted psi stress rises by a factor 16664.2325; the N=32-to-64 log slope is 3.8822733, consistent with the leading three-dimensional zero-point quartic divergence; the fixed-spacing volume-density spread is 2.38067e-13. At N=64 the bare psi density is 0.7107% of rho_Phi and shifts H by 3.5473e-3. These are cutoff-dependence diagnostics, not a renormalized result. Zero-point energy remains; there is no adiabatic subtraction, counterterm matching, renormalized continuum limit or self-consistent initial Friedmann solution. The classical lattice is therefore UV-cutoff dependent. Quantum-seeded backreaction, converged rescattering and a physical defect-network prediction remain unestablished. |
| 6. Resonance and relic abundance | Expanding-background mode equations; converged monodromy/Floquet growth; momentum integration; backreaction; thermalization and entropy dilution; independently reproduced relic abundance | **NOT MET**. A linear mode integrator now evolves supplied expanding-FRW histories with an adiabatic-vacuum check and Wronskian monitor, and a finite-band trapezoidal momentum integral is implemented. The background is not generated self-consistently, the momentum tails and grid are not converged, and no backreaction or entropy dilution is available |
| 7. Proxy-fluid realization | Demonstrate a stable parameter region with the required averaged equation of state, sound speed and anisotropic stress from the dynamics; show convergence and perturbative stability | **NOT MET**. The fresh 100-row scan found 5/100 trajectories classified as quartic, all five in the low-scale underdamped control, all at the largest tested classical seed (\(\psi_{\rm init}=5\psi_0\)) and smaller field offset (\(0.01\Phi_c\)); none of the 50 high-scale threshold-matched trajectories reached the quartic class. These five controls have \(w_{\psi,\rm exc}=0.3722\text{--}0.3736\), \(Q=10.65\text{--}11.07\), virial ratio \(0.9061\text{--}0.9096\), and \(H/\omega\simeq6.9\times10^{-5}\text{--}7.0\times10^{-5}\). This is a narrow homogeneous, manually seeded control region, not a quantum-seeded attractor or a microscopic proxy-fluid realization. Sound speed, anisotropic stress, inhomogeneous stability and robust parameter-volume convergence remain absent |
| 8. Reheating and entropy | Full energy partition from the coupled trajectory; decay/thermalization rates; BBN-compatible thermal history; comoving entropy calculation | **PARTIAL**. The repository includes conditional broken-phase scalar/pseudoscalar two-body and electroweak-symmetric chiral three-body vacuum widths, plus a continuous constant-\(w_c\), constant-\(\Gamma\), constant-\(g_*\) condensate/radiation FRW integrator. On exact head `150487c`, the BDF stiff-tail correction passes the 178-test regression, including five continuous-history tests. The integrator includes radiation in \(H\), independent cumulative condensate/radiation/total energy-budget residuals, \(T(N)\), sampled \(T_{\max}\), \(H=\Gamma\), radiation-domination events and \(S_{\rm com}(N)\). This remains a conditional constant-parameter benchmark, not a PTUM-derived prediction: Wilson matrices, cutoff, quasiparticle mass history, coupled energy partition, thermal thresholds, blocking/enhancement, inverse processes, portal pair production and nonperturbative preheating are unresolved. |
| 9. Observational reproducibility | Public exact CLASS patch; pinned version/commit; complete configs, likelihoods, data, chains and commands; independent rerun reproduces posteriors and model comparison | **NOT MET**. Reported numbers are author-reported; patch availability and chains remain unverified |
| 10. Software and manuscript reproducibility | Pinned environment; deterministic seeds; strict data schemas; full CI; clean LaTeX build; no unresolved references or contradictory claims; artifact hashes | **PARTIAL**. Exact-head full-scan workflow [45260781164](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45260781164) on `c42a9a8e7007fc223297b475282a729d5a068595` passed all six jobs: 178 Python tests, the 4/4 smoke scan, the 100/100 full sensitivity scan, the 11-grid bare-WKB UV audit, the 36/36 targeted convergence study and the 500/500 full paired convergence study (400 comparisons; `full_study_pass=true`). The 45-page LaTeX PDF built; its final pass had 78 Underfull \(\hbox\) warnings, zero Overfull \(\hbox\) warnings and no unresolved references/citations. Artifacts: full scan `14860881053` (SHA-256 `f81eef07a28ee78c60001c2e8a3dd704803ccb31fec6b448ffc635f82e258239`), targeted convergence `14859383848` (SHA-256 `e3a72b6824d0cf09ea1dba79459982485c8e40832dd5230979c6085b2c74e3c1`), full paired convergence `14860754631` (SHA-256 `825f73d23c79154f47a7a1c3cd7fadc7828d529ae0029665c4fe8060b1d01541`), UV audit `14860038191` (SHA-256 `dea34e686026a031ac8379d2441b66528438c72a87a33ff1eb86089ae68ffce0`), PDF `14859578548` (SHA-256 `fe3b81d8fde0dbded525547feb0b72a8c7743d6e2d03f1ec0e2a46ae640bc5da`). The full paired convergence acceptance rule is explicit: early tolerance pairs may miss the strict state threshold, but the error envelopes must decrease monotonically and the finest adjacent pair must pass all 100 rows. Manuscript typography and clean-room reproducibility remain open |

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


## 2026-11-17 Higgs-source layout verified; workflow guard correction

Workflow 44059480978 built the revised 43-page manuscript successfully.
Its compile output contains no Overfull hbox warning, confirming that
the separately defined J_H source removed the previous 40.16039 pt
overflow. Underfull hbox warnings remain (73 in the final compile pass),
so Gate 10 is still PARTIAL and the manuscript is not warning-free.

The same workflow completed the 100-row baseline and the targeted
36-run convergence probe. Its Python regression job reported 136 passed
and one failed assertion: the workflow test expected the ungrouped
string 256001, while the actual workflow comment spells the grid as
256,001. This is a stale text guard, not a numerical or physics failure.
The assertion is corrected to match the checked-in workflow wording.

The paired four-profile 400-run job was still running on that head.
Separately, commit 17b6446c1ad2164f68a40b2ff851c834869a7b17 added a
fifth 1e-12/1e-15 tolerance profile after the first complete paired
study found 12/200 tolerance comparisons outside the unchanged limits.
That 500-run study is pending on the next exact-head workflow. The
sector-current algebra audit is also included on the current branch;
it does not promote Gate 3.


## 2026-11-17 signed Z2-bias interface

The thermal Dirac estimate returns a signed source for
V_bias=-epsilon_bias*psi. The wall-network diagnostic previously
accepted only a non-negative magnitude, so a negative thermal source
could not be passed directly and the preferred vacuum sign was lost.
The diagnostic now accepts either sign, uses the magnitude for the
spinodal and annihilation criteria, and flips the reported true/false
minima when epsilon_bias is negative. It also returns the magnitude
and the preferred-sign flag explicitly.

A regression compares positive and negative tilts: the two stationary
minima must exchange signs, while the positive vacuum-energy splitting,
wall-annihilation estimate and spinodal ratio remain invariant. This
does not predict the Wilson coefficients, renormalized SM condensate,
wall network or its cosmological evolution. Gate 5 remains NOT MET.


## 2026-11-17 chiral-SM versus toy-coupling claim-boundary correction

A stale paragraph in the reheating-current discussion described the
explicit chiral Standard Model action and its Hilbert tensor as still
missing, even though both are defined earlier in the manuscript. The
paragraph is corrected: \(\bar f f\) is now explicitly a generic
vector-like Dirac toy coupling, while the PTUM chiral-SM interaction
remains the gauge-invariant dimension-five operator
\(\psi\mathcal O_{\rm SM}/\Lambda\). The separate real-scalar portal
example is also labelled as a toy model and no longer uses a symbol
that could be mistaken for the Standard Model Higgs field.

This is a claim-boundary and manuscript-consistency correction, not
new physical evidence. Gate 1 remains MET only for the specified
classical tree-level EFT. Gate 3 remains PARTIAL: no full SM/Higgs/
fermion evolution or independent full-sector numerical conservation
convergence has been demonstrated. No other acceptance gate is
promoted by this correction. A fresh regression and LaTeX build are
required before the correction is considered verified.


## 2026-11-17 paired-study profile regression alignment

The paired convergence driver contains five execution profiles: one
4,001-point reference, one 256,001-point profile at the reference
tolerance, and three stricter 256,001-point solver-tolerance profiles
(\(10^{-10}/10^{-13}\), \(10^{-11}/10^{-14}\), and
\(10^{-12}/10^{-15}\)). A stale regression still expected only four
profiles after the fifth tolerance level was introduced. The regression
now checks all five profile names, roles, grids and exact tolerances;
the workflow comment now correctly says four distinct tolerance levels.

This corrects a test/workflow mismatch only. The five-profile, 500-run
paired study has not yet completed on the current head, and no tolerance
convergence claim is made. Gate 4 remains PARTIAL.


## 2026-11-18 paired 500-run tolerance audit and comparator correction

Workflow 44063032840 ran on PR head
6014e116ae372ca25d4f8eac185e6402963016a9 and completed:
- 142 Python tests passed;
- the four-trajectory smoke scan passed 4/4;
- the homogeneous baseline scan passed 100/100;
- the targeted four-case convergence probe passed 36/36;
- the paired study completed 500/500 integrations, 100 unique rows in each of five profiles, zero failed integrations, and 400 comparisons;
- the 43-page manuscript PDF built successfully.

The paired workflow correctly returned failure under its original comparator:
281/300 solver-tolerance comparisons passed. That comparator compared every refined tolerance directly against the 1e-9/1e-12 profile and used a pure relative difference for every dimensionless classification metric. The strict JSON artifact was downloaded and inspected:
- ZIP SHA-256: 43fc944f12866c0e74bc079b40a521dab863655215cfb91b2b0950f20748a119.
- Extracted JSON SHA-256: c01e03bdbf1de0bcb3c801488a60dd77f8d2a83d9c6144a42194e3b53b735a9e.
- 500/500 integrations succeeded; all five profiles contain 100 unique shared-input rows.

The original failure exposed two distinct comparison issues, not integration failures:
1. The 1e-9/1e-12 profile is not yet a sufficiently accurate reference for phase-sensitive final psi_dot. Its difference from tighter solutions grows when compared directly to that fixed reference, even though successive refinements converge.
2. w_final is dimensionless and can be close to zero. Dividing its difference by |w_final| produced relative errors up to 4.38e-5 for absolute changes around 1e-10, an ill-conditioned measure for a bounded dimensionless observable.

Post-hoc successive-pair analysis of the preserved raw rows gives:
- Maximum final-state relative difference by adjacent tolerance pair:
  8.079e-6, 1.057e-6, 1.629e-7.
- Every one of the six state-component error envelopes decreases monotonically across the three refinements.
- Maximum normalized absolute classification-diagnostic difference by pair:
  5.091e-9, 3.960e-10, 6.646e-11.
- Every classification-diagnostic error envelope decreases monotonically; all classification flags and metric-availability states remain unchanged for all 100 rows.
- Maximum chain-rule residual differences by pair remain below 3.93e-10.
- Maximum finite-difference residual differences decrease from 1.61e-5 to 3.86e-6 to 1.66e-7.

The convergence driver has been revised to compare adjacent solver-tolerance profiles. It retains the pure relative difference as a diagnostic, but acceptance for dimensionless classification observables now uses
abs(a-b)/max(1,abs(a),abs(b)), which is absolute for observables below their natural unit scale and relative for values above it. Acceptance requires monotonic reduction of every state and classification error envelope, unchanged flags and metric availability, passing conservation diagnostics, and all 100 rows passing the finest adjacent tolerance pair. The original 1e-6 final-state, 1e-5 normalized classification, 1e-8 chain-rule and 1e-3 finite-difference limits are unchanged.

Commit f546728c02e0b3f10e9970ca55d63c34166468ba implements the successive-refinement comparator and strict-JSON schema v2. Commit 44309ff9091426787102b60614c3f291845854c4 adds regression tests for near-zero dimensionless w and for monotonic-envelope/final-pair acceptance. These changes are newer than workflow 44063032840; the new comparator has not yet been verified by CI. Gate 4 remains PARTIAL until the exact-head 500-run rerun passes. This remains a homogeneous post-threshold scan and does not meet Gates 2, 3, or 5.


## 2026-11-18 chiral Standard Model anomaly audit

The representation registry now evaluates the perturbative gauge-anomaly sums per generation after converting right-handed fields to left-handed charge conjugates. It checks SU(3)^3, SU(3)^2 U(1)_Y, SU(2)^2 U(1)_Y, U(1)_Y^3 and mixed gravitational-U(1)_Y. All five sums vanish exactly as Python Fractions. The SU(2) Witten global-anomaly check counts four left-handed doublets per generation (three colour copies of Q_L plus L_L), twelve for three generations, an even number.

Commit 1f2f29cbd2f90d135750936a7c32a5c9c0a02ced adds the audit to ptum_covariant_action.py and makes validate_action_registry include it. Commit 30650e05f7862b6d02f2ecbf2cdd8b2682b0fe77 adds an exact-arithmetic regression. This is a representation-level consistency audit of the specified minimal SM field content; it does not calculate quantum corrections, anomaly matching in a UV completion, or any PTUM waterfall dynamics. The new test awaits exact-head CI.


## 2026-11-18 manuscript anomaly derivation

Commit 63955448934fae2ab727d54f82a350273455bb63 adds the per-generation chiral-SM anomaly sums to main.tex, explicitly rewriting right-handed fields as left-handed charge conjugates and stating the Dynkin/cubic-index conventions. It displays the SU(3)^3, SU(3)^2 U(1)_Y, SU(2)^2 U(1)_Y, U(1)_Y^3 and mixed gravitational-U(1)_Y cancellations, and the even twelve-doublet SU(2) Witten count for three generations. Commit 0acac9613abccb916810e6ac7bdd11af6bad67f3 adds a manuscript regression guarding the displayed equations and their scope statement. The action registry and manuscript now cross-check the same declared minimal SM representation content. This remains a gauge-consistency audit, not a PTUM UV completion or a quantum waterfall calculation. The latest exact-head CI has not yet been inspected.


## 2026-11-18 convergence-summary availability audit

A further review of the paired artifact showed that quadratic_virial_final is unavailable in all 100 rows of all four refined-grid/tolerance profiles; Q, w and virial are available for 94 rows, and H_over_omega for 73. The successive-refinement summary now explicitly reports per-diagnostic availability and lists diagnostics consistently unavailable across every profile, rather than treating a never-computed optional diagnostic as a numerical convergence failure. It still requires per-row availability to match between adjacent profiles, all six state components to be present for every row at every refinement, monotonic envelopes for every available diagnostic, and all 100 rows to pass the finest pair.

Commit 3a8b6b557e2733163e0cf672b16e81174a8697b6 implements the availability handling and fail-closed state completeness. Commit a597cc157505297b82e70387bef7a4b8fc83f598 adds regressions for the consistently unavailable quadratic virial metric and for a missing intermediate state component. This makes the limitation visible; it does not claim the quadratic virial diagnostic has been computed. The new exact-head CI is pending.


## 2026-11-18 explicit full-scan push trigger

The exact-head workflow started for 0a24ee1e0691ce199d3ddd8348bfeb6b519ad4c5 was cancelled when the branch advanced, and the subsequent exact-head commit had no check runs. The workflow has therefore been amended to include the authorized branch in push triggers. Normal pushes run regression/smoke/LaTeX checks; an explicit [FULL-SCAN] commit message on this branch additionally runs the full 100-row baseline, targeted convergence probe and paired 500-integration convergence study. The full-scan concurrency group is kept separate and is not cancelled by subsequent ordinary scientific commits. Workflow-dispatch now also enables the targeted and paired convergence jobs.

Commit 529e02f7188e02229dd01c8c45f857d985764418 implements the push/dispatch conditions and concurrency behavior. Commit 4daed65a0ab1e47970714dd0d99cffcfff2bd352 adds workflow regressions. The exact-head run will be triggered by the final explicit full-scan commit after this documentation update; no current-head CI result is claimed.


## 2026-11-19 exact-head convergence and defect-risk update

Workflow 44280971987 completed successfully on exact head
1c975a73c7e7daa17c01adffe0fd19d929e8d7bb. All five jobs passed:
146 Python regression tests; the four-trajectory two-scale smoke scan;
the 100-row baseline scan; 36/36 targeted convergence integrations; and
the paired 500-integration study with 400 comparisons. The paired JSON
reports full_study_pass=true, all five profiles contain 100 unique rows,
and there are zero failed integrations. The 4,001-to-256,001 output-grid
comparison preserves all final states and classification flags. The
independent finite-difference continuity residual maximum decreases from
3.7234e-2 to 6.0499e-4, a factor 61.5. A post-hoc row-wise audit gives a
minimum reduction factor 1.38 and median observed order 0.991. Solver
tolerance refinements pass 98/100, 99/100 and 100/100 strict comparisons;
all state and available classification error envelopes decrease
monotonically, and the finest adjacent pair passes every row. The original
281/300 fixed-reference failure remains historical and is not relabelled.

The 100-row baseline classifications are 89 non-quartic, 6 insufficient
oscillation data and 5 quartic. These five quartic labels occur in the
low-scale underdamped control; they do not demonstrate a benchmark-wide
quartic attractor. The zero-seed rows remain exact classical invariant
controls, not quantum seeds.

Gate 4 is promoted to MET only for the stated homogeneous two-field
post-threshold background problem. It does not imply that the coupled
inflation-to-waterfall crossing or inhomogeneous dynamics have been solved.
The exact-input strict-JSON artifact has ZIP SHA-256
f4d6566db7984c83f3564688a0ceac762dcc4f3ee7905cd0fa0e8a2ed6d25842
and JSON SHA-256
800661282f7a5ee0a92d887def3c6f0207028b6992741127f726a1ccdbea3f3c.

A conditional real-psi domain-wall benchmark has also been added. For
mu_eff=m_psi=1e13 GeV, lambda_psi=0.1, T_BBN=5 MeV, g*=10.75,
Mbar_Pl=2.435e18 GeV and scaling area factor A=1, the radiation Hubble
rate is 1.11474e-23 GeV, the static wall tension is 9.42809e39 GeV^3,
and the scaling estimate gives H_dom=530.035 GeV. With no explicit bias,
annihilation does not occur in the analytic estimate before domination or
BBN. The small-bias source required to annihilate before both is
7.90130e28 GeV^3, about 6.49158e-11 of the spinodal source. This is a
conditional scaling-network estimate with frozen Phi=0, not a network
simulation or a prediction of the actual SM-induced bias. Gate 5 remains
NOT MET.

The current LaTeX log for the verified head contains one Overfull hbox
(43.24 pt at the anomaly align block) and numerous Underfull hbox warnings.
The anomaly expressions are now line-broken, and the output-grid
finite-difference reduction is promoted to an explicit CI acceptance
condition. These newest edits await exact-head CI; Gate 10 remains PARTIAL.


## 2026-11-19 final-pass LaTeX audit

The exact-head LaTeX job 135459775171 on commit
82806504c37fe16be97b8c672e13e892a8f1999a completed successfully. The
anomaly align block no longer produces an Overfull hbox. The first
pdflatex pass reported undefined references while labels were being
written; the final third pdflatex pass has no unresolved reference or
citation warnings. Seventy-four Underfull hbox warnings remain in the
final pass, including several badness-10000 paragraphs. The build is
successful but not typographically warning-free. The source-level
regression suite on this head had 149 passes and one assertion mismatch
between test wording and the manuscript; that assertion has been aligned
with the manuscript wording without changing any scientific threshold.
A fresh exact-head Python CI run is required.


## 2026-11-19 domain-wall network geometry sensitivity

The analytic scaling estimate now reports the critical area factor
A_crit = 3 Mbar_Pl^2 H_BBN / sigma_wall. For the conditional benchmark
mu_eff=1e13 GeV, lambda_psi=0.1, T_BBN=5 MeV and g*=10.75,
A_crit=2.1031456023788425e-26. The scaling estimate predicts
H_dom/H_BBN=A/A_crit. Thus A=1 implies domination far before BBN,
whereas A below A_crit does not dominate before BBN in this ansatz.
This is an explicit sensitivity threshold, not a determination of the
network area factor or a defect-network simulation.

Commit d742d283017f704b42f54f082b5b169817f9280b adds the critical-area
diagnostics; commit acad9566af23a1a0254dfddd2499695a84a586fd adds
regressions for the threshold and its two sides. Commit
eb42b1908476e967069cfd3b9eb784836bc59ad1 displays the same relation
and benchmark value in main.tex; commit
6fae0105ded05fe0c6cb9f67df1ed6a7cc782ce4 guards the manuscript equation.
The source-text regression now normalizes whitespace before checking
the wrapped LaTeX sentence.

## 2026-11-19 latest exact-head CI status

Workflow 44495908967 ran on PR merge commit 2b3f23d5461400c0f5ad677e5ca3f65f868749aa,
whose head was branch commit 8a88479a9da61166c490d0fe76e866ce39e6d565.
The LaTeX build and PDF upload passed. Python regression reported
149 passed and one failed: a literal phrase assertion crossed a source
line break in main.tex. The four-trajectory smoke scan and all three
full-scan jobs were skipped after the Python job failed. The assertion
has since been changed to compare whitespace-normalized manuscript
text, and the area-factor regression and manuscript equation are newer
than this run. They require a fresh exact-head CI run. Seventy-four
Underfull hbox warnings remain in the last verified final LaTeX pass;
the final pass had no Overfull hbox or unresolved reference/citation
warnings. Gate 10 remains PARTIAL.


## 2026-11-19 exact-head re-verification request

The latest branch now includes the domain-wall area-factor threshold,
its two-sided regression, the manuscript equation, and a whitespace-
normalized source assertion. These changes postdate workflow 44495908967.
The next branch commit explicitly opts into a fresh full scan as well as
the normal regression, smoke and LaTeX jobs. Until those jobs complete,
the new code and manuscript edits are pending verification. The prior
workflow 44280971987 remains evidence only for the homogeneous
post-threshold two-field scan and its then-current source tree.

## 2026-11-19 nonlinear classical lattice prototype

The new periodic 3-D lattice solver includes the real psi field's spatial
gradients, nonlinear quartic dynamics, homogeneous Phi backreaction and
the Friedmann source on an expanding FRW background. It supports classical
rescattering and a finite-grid sign-crossing wall-area diagnostic for
caller-supplied classical initial fields. Regression coverage checks the
periodic discrete integration-by-parts identity, the homogeneous ODE limit,
and a nonuniform field run.

This is an important numerical foundation but not a quantum waterfall
calculation. The initial fields are not adiabatic-vacuum samples, no
vacuum counterterms or continuum renormalization are implemented, and
lattice spacing/volume/time-step convergence has not been demonstrated.
The wall-area output is not the analytic scaling area factor. Gate 5
therefore remains **NOT MET**. Exact-head CI for this prototype is pending.

The lattice solver also reports a chain-rule RHS energy-balance residual
for d(rho)/d(tau)+3h(rho+p). The homogeneous and inhomogeneous regressions
require the normalized instantaneous residual to be below 1e-12. This
checks the finite-lattice energy functional against the implemented
discrete equations; it does not establish continuum renormalization or
full-sector covariant conservation. The updated tests await exact-head CI.

The finite-grid sign-crossing estimator now assigns exact-zero sites to
the non-negative phase and has a periodic planar two-wall regression.
This removes a zero-site undercount in the diagnostic; it does not remove
its lattice-spacing, box-size or wall-resolution dependence. Gate 5
remains **NOT MET**.

The manuscript's lattice appendix now acknowledges the public
ptum_lattice_waterfall.py prototype while distinguishing it from a
quantum-seeded, renormalized, converged full-field calculation. It also
clarifies that the author-reported lattice/perturbation implementation
is distinct and remains unavailable for independent reproduction.
A new source regression guards these statements. Gate 5 remains
**NOT MET**; this is a claim-boundary correction, not new physical
evidence.

The manuscript now displays the prototype's inhomogeneous psi equation,
homogeneous Phi backreaction equation, Friedmann energy source and
isotropic pressure, together with the discrete periodic integration-by-
parts identity. A source regression checks all four equation labels and
the explicit two-field/classical scope. The four numerical lattice
regressions passed 155 Python tests on intermediate head
0b738954de21468b876e81734129b90b6d2e4cf9 (workflow 44501482600);
the later displayed-equation and manuscript-boundary regression awaits
the current exact-head run. Gate 5 remains **NOT MET**.

Workflow 44502156872 on head 7ce82fec2335300de2074bfb1fa90157bebfd430
reported 155 passed and one failed. The sole failure was a stale manuscript
test expecting the obsolete "no reviewable solver" sentence after the
appendix had correctly documented the classical prototype. Commit
06164c1b7ac9c2333f9e869d7d5bd73223765e9b updates that regression to check
the new claim boundary and reject the obsolete sentence. No scientific
tolerance was weakened. Gate 10 remains **PARTIAL** until the fresh
exact-head Python and LaTeX jobs complete.



## 2026-11-20 bare adiabatic-WKB Gaussian initializer

The classical lattice module now contains
sample_adiabatic_vacuum_initial_conditions. It uses the canonical
$X=a^{3/2}\psi/\psi_0$ mode and the central-difference lattice
dispersion, including the $-3h'/2-9h^2/4$ FRW terms. The first-order
WKB amplitude derivative is retained when constructing the correlated
field/velocity covariance. All lattice modes, including the zero mode,
must have positive canonical frequency squared and satisfy the declared
adiabaticity bound. A deterministic NumPy seed and SHA-256 hashes of
the generated physical arrays are recorded; the lattice solver verifies
the hashes if this provenance is supplied.

This is a bare Gaussian classical-statistical representation of the
symmetrized free-field two-point function at one initial time. It is not
a quantum evolution: it does not reproduce commutators or entanglement,
the zero-point energy is retained, and no vacuum subtraction,
counterterms or continuum renormalization are applied. The initial
background derivatives use homogeneous Phi only and omit psi vacuum
backreaction. Consequently the bare ensemble still has UV-cutoff
dependence and cannot support a physical quantum-waterfall, defect
probability or relic claim. Four regressions check lattice dispersion
and deterministic seeding, refusal of tachyonic/non-adiabatic states,
ensemble covariance, and provenance/hash enforcement. Gate 5 remains
**NOT MET**.

The exact-head CI before this change, workflow 44502331090 on
4ebaa7175f1ebcb460082eac6063a8ff1d07235c, passed 156 Python tests,
the four-trajectory smoke scan, and a 43-page LaTeX build. Its final
LaTeX log still contained two Overfull hbox warnings (186.03 pt and
28.77 pt) and numerous Underfull hbox warnings. The new initializer,
manuscript equations and four regressions await exact-head CI.

The full homogeneous scan workflow 44498664018 completed on
49c820b2e23e16a9109ff5a8877fdd0fd6bf71db. All five jobs passed:
100/100 baseline trajectories, 36/36 targeted convergence integrations,
500/500 paired integrations and 400/400 comparisons. The paired strict
JSON has SHA-256
15b7a0f87f709816f25cab156226d03b8dddae0ebb0ebd584403a8b41c314d14;
the 100-row baseline JSON has SHA-256
5c86db1631da9efd35f956a266edbd5c30cfdae405de1cb9e6e06029c042c1a2.
The baseline labels were 89 non-quartic, 6 insufficient-oscillation,
and 5 quartic; all five quartic labels occurred in the low-scale
underdamped control and do not establish a benchmark-wide attractor.
The scan metadata marks all 100 rows as not quantum-vacuum seeded.
A GitHub compare audit confirms that the interval from 49c820 to
4ebaa changed no homogeneous background or scan source file; the scan
artifacts remain evidence only for that unchanged homogeneous domain,
not for the new lattice initializer.


## 2026-11-21 bare WKB stress and fixed-box UV-cutoff audit

The latest exact-head workflow 44715189629 on commit
7d35cc775531bacbf1fdca729da705d34d2577d6 completed successfully:
161 Python tests passed, the four-trajectory/two-scale smoke scan passed,
and the 44-page LaTeX PDF built. The full 100-row and paired convergence
jobs were skipped because this was not a [FULL-SCAN] run. The final LaTeX
pass has no Overfull hbox or unresolved cross-reference/citation warning,
but numerous Underfull hbox warnings remain.

A new independent audit module, ptum_lattice_uv_audit.py, evaluates the
Gaussian ensemble expectation of the bare finite-lattice stress tensor
from the WKB mode covariances. It includes the velocity-shift covariance,
the central-difference gradient energy, and the Gaussian Wick estimate
< s^4 >= 3 < s^2 >^2 for the quartic term. It computes the corresponding
bare total H and H-prime, so the difference from the homogeneous-Phi
test-field background is quantified rather than hidden.

The CI audit is configured for fixed comoving box size and N=4,6,8,10.
Its purpose is to expose the cutoff dependence of the unsubtracted
zero-point stress. It applies no vacuum subtraction or counterterms and
does not claim a continuum limit. Gate 5 remains NOT MET. The actual
artifact values and SHA-256 are to be recorded after the exact-head
workflow completes.

Gate 10 remains PARTIAL: a successful Python/LaTeX build does not erase
the remaining Underfull hbox warnings, and the long homogeneous scan jobs
were skipped on this non-full-scan run.


The first exact-head run for the new audit, workflow 44893207629 on
86a57c7599e941595b2638f57bdf2ea94298dd5b, exposed an implementation
error: the WKB velocity shift is a mode-dependent array, not a scalar.
The first regression run therefore reported 161 passed and 3 failed,
and no cutoff artifact was produced. The audit now validates and sums
the full mode-dependent shift array. A manuscript source assertion was
also aligned with the exact prose already present. The corrected
implementation requires a fresh exact-head run; no numerical cutoff
ratio is claimed from the failed attempt.


## 2026-11-21 exact-head bare WKB stress artifact

Workflow 44893367362 on exact head 9d9def8ac72205bc8b912590553fcf0ab38f7f73 completed successfully. The regression suite reported 164 passed; the two-scale smoke scan had zero failed integrations; the bare WKB audit produced a strict-JSON artifact. The 44-page manuscript built successfully. Its final LaTeX pass had zero Overfull hboxes and zero unresolved references/citations, but 77 Underfull hbox warnings remain.

The fixed-box N=4,6,8,10 audit used box size 8 mu^-1 and seed 20261121. The lattice cutoff increased from 1.7320508 mu to 4.3301270 mu. The bare psi stress increased from 1.20259796e48 to 2.16686483e49 GeV^4, a factor 18.0182; the end-to-end log slope was 3.15553. The bare-total Hubble mismatch relative to the homogeneous-Phi test-field background increased from 2.13247e-7 to 3.84232e-6. The audit retains zero-point energy and applies no subtraction or counterterms. It quantifies cutoff dependence only.

Artifact ZIP SHA-256: c4fd531a8de4bd6a31177514afa9e0c7f8f46b67b12cef538315c2b73b643f12.
Extracted strict-JSON SHA-256: 3f24f7c54748b2498d9e3cf57500bd3a738b2b0491cc63ae1a2baf0076f68fbf.

The next audit extension holds the comoving box fixed through N=64 to examine the high-cutoff slope, and separately holds dx fixed while increasing the box to test finite-volume stability of the equal-time Gaussian mode sum. This is a numerical audit of the bare initial covariance, not time-evolved lattice convergence or renormalization. The extended study awaits exact-head CI.


## 2026-11-21 extended bare WKB UV/volume audit

Exact-head workflow 44895764302 on commit
25b46d4b2ec9442842af089d636259a184e16e99 completed the dedicated
lattice-UV audit and LaTeX jobs successfully. The Python job reported
165 passed and one failed. Its sole failure was a stale source assertion
expecting the phrase "fixed-box UV-cutoff audit", while the manuscript
accurately says "fixed-box sequence therefore isolates UV-cutoff
dependence". This is a test/manuscript wording mismatch, not a numerical
failure. The regression is being aligned to the actual manuscript text
and now also guards the archived numerical benchmark.

The strict-JSON audit used seed 20261121 and fixed comoving box
L=8 mu^-1 for N=4,6,8,10,12,16,20,24,32,48,64. The reported lattice
cutoff increased from 1.7320508076 mu to 27.7128129211 mu. The bare
psi stress increased from 1.2025979590e48 to 2.0040371966e52 GeV^4,
a factor 16664.2325. The N=32-to-64 high-cutoff log slope was 3.8822733,
consistent with the leading Lambda^4 zero-point divergence over this
finite range. The bare-total versus homogeneous-Phi Hubble mismatch
increased from 2.13247e-7 to 3.54730e-3, exposing the increasing
test-field/Friedmann inconsistency as the UV cutoff is raised.

The separate fixed-spacing sequence used dx=mu^-1 and
N=8,12,16,24,32,48,64. Its equal-time bare density relative spread was
2.38067e-13, below the declared 1e-8 finite-volume stability threshold.
This is finite-volume stability of the same bare Gaussian mode sum at
fixed spacing. It is not a UV continuum limit, a subtraction scheme,
a renormalized stress tensor, or time-evolved lattice convergence.

Artifact ZIP SHA-256:
1b99b0fa6a9bc6058690aaaf2b9e60312e7e03e43c266210162201ed902d6b1d.
Extracted strict-JSON SHA-256:
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.

The 44-page LaTeX build passed. Its final pass had zero Overfull hboxes
and zero unresolved references/citations, but 77 Underfull hbox warnings
remain. Gate 5 remains NOT MET because the Gaussian stress is bare,
UV divergent and not self-consistent with the WKB test-field background.
Gate 10 remains PARTIAL. The corrected Python source regression requires
a fresh exact-head run.


The first follow-up exact-head run after the extended audit, workflow
44896882170 on 26f1a4b, again reported 165 passed and one failed. The
remaining failure was a second stale source phrase: the test expected
"does not subtract the vacuum energy", while the manuscript states
"Neither sequence subtracts the vacuum energy". The numerical UV audit
and 44-page LaTeX build both passed; the final LaTeX pass retained 77
Underfull hbox warnings and had zero Overfull hboxes or unresolved
references/citations. The test is now aligned to the exact manuscript
wording. A fresh exact-head regression run is required; no physical
threshold or numerical tolerance was changed.


The next exact-head PR run 44897305916 on 8ce8d59 reported 165
passed and one failed. The sole remaining failure was another literal
wording mismatch: the test expected "define a physical continuum limit"
while the manuscript says "or defines a physical continuum limit".
The source assertion now follows the exact sentence. The lattice audit
and LaTeX jobs again passed; the fresh push run was still completing at
the time of this update. No physical criterion or tolerance changed.


## 2026-11-21 exact-head verification of extended bare WKB audit

Push workflow 44897514397 completed successfully on exact head
242552ae69baaddbfc1f5c1b671c135f636b0744:
- Python regression: 166 passed.
- Four-trajectory, two-scale smoke scan: 4/4 successful; two rows
  classified as insufficient oscillation data and two as non-quartic.
  All four records explicitly say quantum_vacuum_seeded=false.
- Extended bare WKB UV/volume audit: passed and produced strict JSON.
- LaTeX: 44-page PDF built successfully.
- The full 100-row and paired homogeneous scans were skipped because
  this commit did not opt into [FULL-SCAN]; no new full-scan result is
  claimed from this workflow.

The final LaTeX pass has 77 Underfull hbox warnings, zero Overfull
hboxes, and zero unresolved references/citations. Gate 10 therefore
remains PARTIAL.

The exact-head audit artifact reproduces the extended result recorded
above: bare stress rises by a factor 16664.2325 at fixed L=8 mu^-1,
the N=32-to-64 log slope is 3.8822733, and the fixed-spacing volume
spread is 2.38067e-13. The strict-JSON SHA-256 is
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749;
the exact-head ZIP SHA-256 is
671fb04d320d80b00abc383970c5575a8be8e863fbb591a878c4b92c0391f49b.

This confirms the source-regression correction and the bare mode-sum
diagnostics only. It does not provide vacuum subtraction, counterterms,
a renormalized continuum limit, time-evolved lattice convergence, or a
physical quantum-waterfall result. Gate 5 remains NOT MET.


## 2026-11-21 CP-resolved broken-phase fermion operator matching

The gauge-invariant dimension-five interaction
$-\psi\mathcal O_{\rm SM}/\Lambda$ is now matched in a single-flavour
mass basis with complex diagonal coefficient
$C_{f,ii}=c^S_{fi}+i c^P_{fi}$. The manuscript displays
$y^S_{\psi f}=c^S_{fi}v/(\sqrt2\Lambda)$ and
$y^P_{\psi f}=c^P_{fi}v/(\sqrt2\Lambda)$ in
$-\psi\bar f(y^S+i y^P\gamma_5)f$. The ideal CP-even equilibrium
thermal-bias estimator is explicitly restricted to the scalar
one-point function; it assumes the thermal pseudoscalar condensate
vanishes.

ptum_defects.py now maps a supplied diagonal complex Wilson
coefficient, broken-phase Higgs vev and EFT cutoff into scalar and
pseudoscalar couplings, then passes only the scalar component to the
existing ideal Dirac-gas bias integral. Regressions cover real/imaginary
parts, cutoff scaling, pure-pseudoscalar zero bias in the stated
CP-even approximation, and agreement with the direct scalar-coupling
path.

This is a matching/API consistency improvement, not a prediction of
the bias. The diagonal Wilson coefficients, cutoff, temperature-
dependent Higgs vev, renormalized zero-temperature condensates, QCD
effects, off-diagonal flavour dynamics and thermal history remain
unspecified. The free-gas result remains conditional. Gate 5 remains
NOT MET; no domain-wall network evolution or annihilation time is
claimed.


## 2026-11-22 conditional perturbative reheating-width implementation

The new `ptum_reheating.py` module implements two distinct vacuum quasiparticle limits without conflating the electroweak phases.

For one massless chiral channel from the gauge-invariant dimension-five operator, with (s=(p_f+p_{\bar f})^2),
[
\sum |\mathcal M|^2=|C_f|^2s/\Lambda^2,
\qquad
\frac{d\Phi_3}{ds}=\frac{M^2-s}{128\pi^3M^2},
\qquad
\Gamma_1=\frac{|C_f|^2M^3}{1536\pi^3\Lambda^2}.
]
An explicit multiplicity counts orthogonal colour, weak, flavour and charge-conjugate channels. Amplitudes to the same final state must be combined before squaring.

After electroweak symmetry breaking, for (-\psi\bar f(y_S+i y_P\gamma_5)f),
[
\Gamma_{2}=\frac{N_cM}{8\pi}
\left[y_S^2\left(1-\frac{4m_f^2}{M^2}\right)^{3/2}
+y_P^2\left(1-\frac{4m_f^2}{M^2}\right)^{1/2}\right].
]
The scalar and pseudoscalar pieces do not interfere in the spin-summed width.

The report builder returns partial widths, branching fractions, the sudden-decay estimate (T_{\rm rh}=(90/\pi^2g_*)^{1/4}\sqrt{\bar M_{\rm Pl}\Gamma}), and conditional 5 MeV BBN, electroweak-crossover and EFT-cutoff checks. It assumes massless final states and vacuum matrix elements for the unbroken-phase result. It does not include thermal masses, Pauli blocking, Bose enhancement, condensate depletion, Higgs-portal pair processes, nonperturbative preheating, a Boltzmann energy partition or entropy evolution. No numerical PTUM benchmark is claimed because the Wilson matrices, cutoff and time-dependent quasiparticle spectrum are not fixed.

The code, four numerical regressions and manuscript-source regression are newer than workflow 44898158765. They require exact-head CI before being counted as verified evidence. Gate 8 remains PARTIAL; Gate 10 remains PARTIAL.


## 2026-11-22 exact-head reheating implementation verification

PR workflow 45009882010 on head 5c4c1756271063542bffd3d7ac5a4539313fd171 completed successfully:
- 173 Python regression cases passed, including the new broken/unbroken-phase decay-width and sudden-decay report tests.
- The four-trajectory/two-scale smoke scan completed 4/4 with zero failed integrations.
- The 11-grid bare WKB UV/volume audit passed; it reproduced the documented bare cutoff ratio 16664.2325, high-cutoff slope 3.8822733 and fixed-spacing volume spread 2.381e-13.
- The 45-page LaTeX build completed. The second pass had no unresolved references/citations but retained 76 Underfull and 3 Overfull hbox warnings.

The Overfull warnings were localized to the long broken-phase Wilson-matching display and the two new unbroken-phase three-body displays. Commit 32f94f30504b2db0771c45aed97d4b9e20cb840c rewrites these as aligned multi-line equations without changing the formulas. Exact-head CI for 32f94 is pending. Gate 10 remains PARTIAL until the new build and all remaining warnings are audited.


## 2026-11-23 conditional continuous reheating-fluid implementation

A new ptum_reheating_history.py module integrates a homogeneous
constant-w_c, constant-Gamma, constant-g_star condensate/radiation
system in e-fold time. Radiation contributes to the Friedmann rate.
The code integrates three cumulative ledgers independently:
condensate expansion work, radiation expansion work, and energy
transferred from condensate to radiation. Their residuals test the
separate sector budgets and the total continuity equation.

The module reports the radiation-domination and H=Gamma events,
the sampled temperature maximum, the continuous bath temperature at
H=Gamma, and the comoving entropy history under prompt thermalization
and constant relativistic degrees of freedom. At H=Gamma, the identity
T_cont/T_sudden=Omega_r^(1/4) is checked; the sudden-decay expression
is recovered only if radiation already dominates at that event.

Five new regression tests cover the zero-width redshifting limit,
comoving-entropy conservation without a source, separate energy-budget
closure with decay, the continuous/sudden temperature identity,
initial radiation/width edge cases, input-domain checks, and the
manuscript equations. These tests are pending a fresh exact-head CI run.

Gate 8 remains PARTIAL. This is not a PTUM-derived reheating prediction:
w_c(t), Gamma(T), Wilson matrices, the cutoff, the evolving
quasiparticle spectrum and the scalar-to-SM energy partition are not
specified. Prompt thermalization, constant g_*, and the absence of
thermal thresholds, inverse processes, thermal blocking/enhancement,
Higgs-portal pair production, nonperturbative preheating and rescattering
are explicit limitations. Gate 10 remains PARTIAL until the new exact
head passes CI and the remaining manuscript warnings are resolved.


### 2026-11-23 exact-head regression correction

PR push workflow 45152225396 on 01dc0b5 completed the Python job with
176 passed and two failed. One failure was numerical: the non-stiff
DOP853 dense interpolant developed a non-monotone late-time entropy
sample while the decay source made the equations stiff. A local
independent solve of the same normalized equations with BDF reduced
the maximum integrated energy-budget residual below \(5\\times10^{-15}\)
and removed the observed entropy decrease. The production integrator
now uses BDF, and the sampled entropy monotonicity diagnostic tolerance
is tightened from \(10^{-4}\) to \(10^{-5}\), not relaxed.

The second failure was a source-test mismatch: main.tex correctly
escapes underscores in the filename as TeX, while the assertion searched
for the unescaped Python filename. The assertion now checks the escaped
source spelling. The BDF solver change and source-test correction are
awaiting a fresh exact-head CI run. Gate 8 remains PARTIAL.


## 2026-11-23 exact-head verification and UV-cutoff result

The continuous reheating integration was changed from DOP853 to BDF after the prior dense-output interpolant showed a non-monotone sampled comoving-entropy artifact in the stiff decay tail. The numerical monotonicity diagnostic was tightened to (10^{-5}); no physical tolerance was loosened. On exact head `150487cf9f92684b2120310948e8a9d050f4f13d`, workflow [45152898999](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45152898999) passed 178 tests, the 4/4 smoke scan, the lattice UV audit and the LaTeX build.

The bare-WKB audit artifact [14807855439](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45152898999/artifacts/14807855439) reports:
- Fixed box (L=8\,\mu^{-1}), (N=4,6,8,10,12,16,20,24,32,48,64): the unsubtracted bare (psi)-stress increases monotonically by a factor 16664.2325.
- The high-cutoff (N=32\rightarrow64) log-log slope of (ho_{\psi,\rm bare}) against the lattice cutoff is 3.8822733. This is consistent with the leading (Lambda^4) zero-point divergence in three spatial dimensions; it is not evidence of renormalization.
- At fixed (\Delta x=\mu^{-1}), increasing the box from (8\) to (64\,\mu^{-1}) gives a relative density spread (2.38067\times10^{-13}). This is a finite-volume check at fixed spacing, not a continuum-limit check.
- At (N=64), (ho_{\psi,\rm bare}/ho_\Phi=7.1072\times10^{-3}) and the bare-total Hubble mismatch is (3.5473\times10^{-3}).
- The artifact explicitly records `vacuum_subtraction_applied=false`, `counterterms_applied=false`, and `continuum_limit_claimed=false`.

**Decision:** the bare first-order WKB Gaussian sample cannot be promoted to a physical quantum initial state for nonlinear FRW evolution. The next scientific blocker is a covariantly consistent renormalization prescription for the time-dependent interacting scalar in FRW, including the renormalized stress tensor, initial Friedmann constraint, and cutoff/volume/time-step convergence. Until that prescription is derived and independently tested, the nonlinear lattice remains a finite-cutoff classical-statistical prototype. The real-(\psi) (Z_2) domain-wall risk also remains open.

The PR title now opts into a fresh full-scan run. That run must verify the current exact head rather than reusing earlier 100-row and paired-convergence artifacts. No result from that requested run is claimed here.


## 2026-11-23 fresh 100-row scan and targeted convergence

On exact code head `c42a9a8e7007fc223297b475282a729d5a068595`, the full scan artifact `14860881053` contains 100/100 successful homogeneous post-threshold trajectories. The 50 high-scale threshold-matched rows produced 48 non-quartic classifications and two exact zero-seed invariant controls with insufficient oscillation data. The 50 low-scale underdamped controls produced 41 non-quartic rows, five quartic rows and four rows with insufficient oscillation data.

All five quartic rows share the largest tested initial amplitude, (\psi_{\rm init}=5\psi_0), and the smaller field offset, (0.01\Phi_c); the initial velocity spans the five values in the scan grid. The result demonstrates a conditional quartic-like homogeneous regime in the low-scale control, but no quartic trajectory in the 50-row high-scale threshold-matched benchmark. It does not establish a quantum vacuum seed, a broad attractor, or a proxy-fluid perturbation theory.

The targeted convergence artifact `14859383848` contains 36/36 successful runs for four representative cases. The four case summaries all pass the declared state, classification, flag and diagnostic-stability checks. Maximum final-state relative differences across tolerance refinements are (3.05\times10^{-8}), (5.50\times10^{-9}), (2.24\times10^{-9}), and (4.75\times10^{-7}) for the high-scale implicit-budget, low-scale implicit-budget, high-scale largest-(Q), and low-scale largest-(Q) cases, respectively. The maximum normalized classification differences are below (9.4\times10^{-7}).

The separate all-100-row paired output-grid and four-tolerance study is still running. Its results must be added only after the artifact is complete and independently inspected.

The next quantum-waterfall requirement is documented in [`PTUM_QUANTUM_RENORMALIZATION_GATE.md`](PTUM_QUANTUM_RENORMALIZATION_GATE.md). In particular, the bare WKB cutoff divergence cannot be repaired by simply subtracting one initial vacuum-energy constant; the interacting curved-spacetime counterterm basis and finite renormalization conditions must be derived from the common action.


## 2026-11-23 full paired 100-row convergence completed

The full-grid artifact `14860754631` contains 500/500 successful integrations and all 400 expected comparisons across five numerical profiles for the same 100 initial conditions: 4,001-point reference output, 256,001-point refined output, and three successive solver-tolerance refinements.

**Output-grid result (100 paired rows):**
- 100/100 rows passed; every finite-difference FRW continuity residual decreased on refinement.
- Grid refinement ratio: 64.
- Median reduction factor: 61.5445; median observed order: 0.99059.
- Minimum reduction factor: 1.37970; minimum observed order: 0.07739.
- All diagnostics were available. The script's declared criterion is every row improving and median observed order at least 0.8; it passed.

**Solver-tolerance result (three successive 100-row comparisons):**
- First refinement: 98/100 strict comparisons passed.
- Second refinement: 99/100 strict comparisons passed.
- Finest adjacent refinement: 100/100 strict comparisons passed.
- State-error and dimensionless-classification-error envelopes decreased monotonically by field; classification flags and metric availability were unchanged; all chain-rule and finite-difference diagnostic checks passed.
- The three earlier non-passing rows were two cases at the first refinement and one case at the second refinement, all in the low-scale underdamped control with `seed=0` or `seed=5`, `velocity=1`, `offset=0.1`. Their only failing criterion was the strict final-state relative-difference limit; the next refinements reduced those errors, and the finest pair passed all rows.

The study's explicit acceptance logic therefore returns `full_study_pass=true` despite 397/400 strict pairwise comparisons passing: it requires complete coverage, no failed integrations, monotonic error envelopes, unchanged flags/availability, all output-grid rows passing, and all 100 rows passing the finest adjacent tolerance comparison. It does **not** claim that the first two tolerance refinements independently passed every strict pairwise threshold.

This closes the current homogeneous background output-grid/tolerance convergence package. It does not close the quantum waterfall, inhomogeneous dynamics, renormalization, backreaction, rescattering, or defect-network gates.


## 2026-11-24 two-scalar heat-kernel UV coefficient

The R0 renormalization work now has an algebraic scalar-sector result:
ptum_renormalization.py computes the local four-dimensional bulk
\(a_2\) coefficient for the coupled canonical \((\Phi,\psi)\) Gaussian
operator using the full \(2\times2\) potential Hessian, including its
off-diagonal mixing. The curvature couplings \(\xi_\Phi,\xi_\psi\) are
explicit inputs. The formula is checked against flat constant-Hessian,
conformal maximally symmetric, curvature-coupling and tachyonic
polynomial controls.

This is **not** a renormalized result. The EFT cutoff, renormalization
scale, finite matching conditions, pole normalization, boundary and
initial-state terms, SM/gauge/fermion and graviton loops, CTP finite
parts, renormalized stress tensor and force on \(\Phi\) remain absent.
Gate 5 remains **NOT MET**; R0 is only partially advanced. No lattice
initial condition or Friedmann source has been modified.

Exact prior head f3c05f574356e52adc55f22bc4596601fe1e5a10 was verified by
workflow 45264117068: 178 Python tests passed, the two-scale smoke scan
completed 4/4 with zero failed integrations, and the 11-grid bare-WKB
UV audit completed. The 45-page PDF was produced, but its final log
still contains Underfull-box warnings and unresolved reference/citation
warnings. This run did not opt into the long full-scan jobs; the
historical 100-row/500-integration artifacts remain the separate
homogeneous convergence evidence described above.


## 2026-11-24 exact-head R0 algebraic UV checks

On exact head 5f190b87aa7f883ec721fd35e432f76b539c052f,
workflow 45364524478 completed successfully:
- 186 Python tests passed.
- Two-scale smoke scan: 4/4 trajectories succeeded, zero failed integrations.
- 11-grid bare-WKB UV/volume audit passed. The artifact still reports
  renormalized=false; the fixed-box bare stress grows by 16664.232 and
  the N=32-to-64 cutoff slope is 3.8822733.
- 46-page LaTeX PDF built. Final pass: 79 Underfull hbox warnings,
  zero Overfull hboxes, and zero unresolved references/citations.
- Long homogeneous scans were skipped by design; the previously
  accepted 100-row/500-integration convergence artifacts remain the
  separate homogeneous-domain evidence.

The R0 code now includes both the matrix-trace a_2 coefficient and an
expanded operator-basis identity check. This does not select an EFT
truncation, cutoff, renormalization scale or finite matching conditions.
Gate 5 remains NOT MET.


## 2026-11-24 Euclidean scalar pole normalization (R0 extension)

The two-scalar bulk \(a_2\) result now has an explicit dimensional-
regularization convention. For
\(\Gamma_E^{(1)}=+\tfrac12\operatorname{Tr}\ln\mathcal D_E\),
\(d=4-\epsilon\), and \(\epsilon=4-d\), the local pole is
\(-a_2^{\rm bulk}/(16\pi^2\epsilon)\), cancelled by the Euclidean
counterterm coefficient \(+a_2^{\rm bulk}/(16\pi^2\epsilon)\).
The implementation returns the coefficients of \(1/\epsilon\), and
regressions check the single-real-scalar flat constant-mass limit,
explicit cancellation sign, finite-input validation, and manuscript
normalization.

This fixes a convention-dependent local scalar bulk pole only. It does
not supply the renormalization scale, finite \(\overline{\rm MS}\)
constant, EFT matching conditions, boundary/initial-state terms,
SM/gauge/fermion/graviton loops, real-time CTP finite parts, a
renormalized stress tensor/\(\Phi\) force, or lattice counterterm
implementation. No initial condition or Friedmann source was changed.
Gate 5 remains NOT MET. The new exact-head regression and manuscript
build are pending CI.


## 2026-11-24 exact-head pole verification and field-gradient extension

The exact head dc6ba177e84b269cfd790de9c72a6bb7054d2904 was verified by
workflow 45367381969:
- 191 Python regression cases passed.
- Two-scale smoke scan: 4/4 successful trajectories, zero failed
  integrations.
- The 11-grid bare-WKB UV audit produced strict JSON. Its ZIP SHA-256 is
  2dcb72f48f623f6000f97f0ccc67e1ce2ae39de8415633cd12ab99b0c38191ba;
  extracted JSON SHA-256 is
  260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
  The fixed-box bare-stress ratio remains 16664.2325, the N=32-to-64
  cutoff slope is 3.8822733, the fixed-spacing volume spread is
  2.38067e-13, and the artifact explicitly says zero-point energy is
  retained, vacuum subtraction/counterterms are false, and no continuum
  limit is claimed.
- The 46-page PDF built. PDF SHA-256 is
  aab465e7503caf43bb4e29e661d0ca67ce48752af0ee57e59c7ac02e8ac22c85;
  artifact ZIP SHA-256 is
  8ad74b011497f62c637e539485f3678ca04190e40e8eaca392a8bf2f6331f852.
  The final LaTeX pass had 79 Underfull hboxes, zero Overfull hboxes,
  and zero unresolved references/citations. The manuscript is not
  warning-free.
- Long homogeneous scans were skipped by design; no new 100-row scan
  or paired convergence result is claimed from this workflow.

The scalar bulk pole helper passed the flat single-real-scalar
normalization and sign tests. The next extension analytically
differentiates the same bulk coefficient with respect to both
background fields at fixed curvature, returns the divergent force
coefficients and their cancelling counterterms, and adds central-
difference plus \(Z_2\)-symmetry regressions. These new changes are
pending exact-head CI. Gate 5 remains NOT MET; Gate 10 remains PARTIAL.


### Exact-head field-gradient regression result

Workflow 45368160766 on head bd9daf3317ccc6ce71bdadb4ddadb5f906ac4d7b
reported 193 passed and one failed. The only failure was the manuscript
source assertion expecting a trace identity to be contiguous despite
intentional aligned equation line breaks. Both numerical field-gradient
regressions passed; the LaTeX build and 11-grid bare-WKB UV audit passed.
Because the Python job failed, the two-scale smoke scan did not run.
The assertion now checks separate mathematical fragments, with no
equation or tolerance change. Fresh exact-head CI is pending. Gate 5
remains NOT MET; Gate 10 remains PARTIAL.


## 2026-11-24 exact-head verification of the scalar pole derivatives

Exact-head workflow 45368498672 on d5649884cae49ede9c4cb83915a3f0a4670d83b2
completed successfully:
- 194 Python regression cases passed, including the two independent
  central-difference field-gradient checks, the real-psi Z2 control,
  and the manuscript source regression.
- Two-scale smoke scan: 4/4 successful, zero failed integrations.
- The 11-grid bare-WKB UV audit passed. Its strict-JSON artifact confirms
  the same cutoff-dependent bare stress: fixed-box ratio 16664.2325,
  N=32-to-64 log slope 3.8822733, fixed-spacing volume spread
  2.38067e-13. Zero-point energy is retained; vacuum subtraction and
  counterterms are not applied; no continuum limit is claimed.
- The 46-page manuscript PDF built. Final LaTeX pass: 80 Underfull
  hboxes, zero Overfull hboxes, zero unresolved references and zero
  unresolved citations. This is not a warning-free build.
- Long 100-row and paired convergence jobs were skipped by design.
  No new homogeneous full-scan result is claimed.

The pole derivative implementation remains a local Euclidean bulk
coefficient at fixed curvature. It is not a finite renormalized force,
metric variation, renormalized stress tensor, or real-time CTP equation.
Gate 5 remains NOT MET and Gate 10 remains PARTIAL.



## 2026-11-25 local scalar pole metric-variation extension

A new helper derives the inverse-Euclidean-metric variation of the
coupled two-scalar local bulk \(a_2\) coefficient. In four dimensions,
the curvature-squared combination is reduced modulo the Euler density
to \(A R_E^2+B R_{\mu\nu}R^{\mu\nu}\), while the field-dependent
terms contribute \(-g_{\mu\nu}U_0/2\) and
\(F G^E_{\mu\nu}+(g_{\mu\nu}\Box_E-\nabla_\mu\nabla_\nu)F\).
The \(R^2\) and Ricci-squared variations include their second
covariant-derivative terms. The helper requires and validates the
Euclidean curvature and derivative tensors as explicit inputs.

Five regressions cover the flat limit, constant-curvature limit,
conformal-coupling trace identity, inconsistent curvature data, and
the displayed manuscript equations. These newest code, test and
manuscript changes are awaiting exact-head CI. The previous exact-head
workflow 45369471261 on 9ac3ef28fb36d2eed955b9a1c8cef1ee15fcdbfb
passed 194 Python tests, the 4/4 two-scale smoke scan, the 11-grid
bare-WKB UV audit, and the 46-page LaTeX build. The final LaTeX pass
still had 80 Underfull hbox warnings; it had zero Overfull hboxes and
zero unresolved references/citations. Long scans were skipped by
design. The new metric-variation changes have not been verified by
that earlier run.

Gate 5 remains NOT MET: this is a local divergent Euclidean metric
Euler derivative, not a finite renormalized stress tensor, real-time
CTP source, or lattice counterterm. Gates 2, 3, 8 and 10 remain PARTIAL;
Gates 5, 6, 7 and 9 remain NOT MET. Gate 1 remains MET only for the
stated classical tree-level EFT, and Gate 4 remains MET only for the
homogeneous two-field post-threshold background. PTUM is not 10/10.



### 2026-11-25 metric-variation regression correction

The first workflow on the metric-variation implementation,
45586007724, reported one Python failure in the deliberately inconsistent
Ricci-scalar input test. The test changed the scalar by an absolute
1 GeV^2, which was below the scale-aware tolerance for the benchmark
curvature (of order \(m_\psi^2\)). The test input is now perturbed by
\(10^{-3}m_\psi^2\); the implementation tolerance is unchanged. A
Python regex literal was converted to a raw string to avoid a
DeprecationWarning. The UV audit passed; the LaTeX job was still in
progress at the last inspection. The corrected head requires a new
exact-head Python and manuscript run. Gate 5 remains NOT MET and
Gate 10 remains PARTIAL.



### 2026-11-25 metric-variation tensor audit refinement

The metric Euler derivative now reports its four additive tensor pieces
separately and validates the first algebraic Bianchi identity. A
regression supplies a fully antisymmetric four-form perturbation that
leaves the Ricci contraction unchanged but violates Bianchi; it must be
rejected. The flat-limit test checks the component sum. This additional
code and test revision is awaiting exact-head CI. The prior one-failure
test-stimulus correction remains documented above; no production
tolerance was altered.



## 2026-11-25 exact-head metric-variation verification

Workflow 45586718905 on exact head
8bfbe348675470223477cdb8e45b5b7a7f233b8d completed successfully:
- 199 Python tests passed, including the metric Euler-derivative limits,
  curvature-jet validation, Bianchi rejection and tensor-component sum.
- The two-scale smoke scan passed 4/4 with zero failed integrations.
- The 11-grid bare-WKB UV audit passed.
- The 47-page LaTeX build completed with zero unresolved references or
  citations, but its final pass retained 66 Underfull and two Overfull
  hbox warnings. The two Overfull warnings were traced to the newly
  added metric-variation displays and have been split across aligned
  lines in a later commit. That later exact-head build is pending.

The smoke JSON (SHA-256
105e3c4e1e560ba5d292da7ca476b50e0e308fe9088fa4641e2b48e21d4766f6)
contains 4/4 successful rows, exact Phi_c/M_Pl=0.9862280831209068,
and quantum_vacuum_seeded=false. The UV audit JSON (SHA-256
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749)
shows the fixed-box bare-stress factor 16664.2325, high-cutoff slope
3.8822733, fixed-spacing volume spread 2.38067e-13, and explicit
zero-point retention with no subtraction/counterterms/continuum claim.

The latest LaTeX formatting change is pending exact-head CI. Gate 5
remains NOT MET and Gate 10 remains PARTIAL.



### 2026-11-25 independent metric-variation finite-difference regression

A new regression constructs the compact Euclidean product
\(S^2(K_1)\times S^2(K_2)\), evaluates the complete local \(a_2\)
density and its integrated volume, and independently finite-differences
the action under separate constant rescalings of each two-sphere metric.
The numerical derivatives are compared with the corresponding block
traces of the analytic metric Euler tensor. The test includes the full
Euler-density term in the action, so it checks the expected topological
cancellation as well as the non-topological curvature terms. This new
regression is pending exact-head CI. It is a check of the divergent
local Euclidean coefficient only; Gate 5 remains NOT MET.



## 2026-11-25 exact-head metric-variation acceptance result

Workflow 45587737076 on exact head
ee6a7dced58f30122150fcbaae832cf356423778 passed:
- 200 Python regression cases, including the independent product-sphere
  finite-difference comparison of the full integrated \(a_2\) action
  against the analytic inverse-metric Euler derivative for each
  two-sphere block.
- 4/4 two-scale smoke trajectories with zero integration failures.
- The 11-grid bare-WKB UV-cutoff audit.
- The 47-page manuscript build, with zero Overfull hboxes and zero
  unresolved references/citations; 80 Underfull hbox warnings remain.

The smoke and UV artifacts were extracted and parsed with a strict JSON
parser that rejects NaN/Infinity. The smoke payload contains four
successful classical rows, uses the exact endpoint threshold
\(\Phi_c/M_{\rm Pl}=0.9862280831209045\), and explicitly records
\(\texttt{quantum\_vacuum\_seeded=false}\). The UV payload continues
to show the fixed-box bare stress factor 16664.2325 and high-cutoff
slope 3.8822733; zero-point energy remains and no subtraction,
counterterms, continuum limit or physical quantum prediction is
claimed. The PDF artifact is a valid 47-page PDF and contains the
metric-variation equations.

This closes the software verification of the new local metric Euler
derivative under the tested algebraic limits and product-sphere
finite-difference variations. It does not close Gate 5: finite
renormalization conditions, boundary/initial-state terms, the
renormalized stress tensor, SM/gauge/fermion/graviton loops, CTP
finite parts and lattice counterterm implementation remain absent.
Gate 10 remains PARTIAL because Underfull hbox warnings persist.
The long scans were skipped; no new 100-row physical scan is claimed.


### 2026-11-25 polynomial scalar RG control (pending exact-head CI)

A two-real-scalar polynomial control EFT now has one-loop MS-bar beta
coefficients derived from the existing heat-kernel pole. The beta
coefficients reconstruct the complete local \(a_2/(16\pi^2)\) density,
including the scalar potential, non-minimal curvature, Einstein and
curvature-squared terms in the declared Euclidean basis. Regressions
cover the matrix-residue reconstruction, decoupled and mixed limits,
the conformal-coupling fixed point, and fail-closed quartic stability.

This is not the RG flow of the non-polynomial PTUM plateau and does not
choose \(\Lambda_{\rm EFT}\), \(\mu_R\) boundary data or finite matching
conditions. R0 remains partial; Gate 5 remains **NOT MET**. Exact-head
Python and manuscript verification are pending. No lattice subtraction
or physical quantum result is claimed.


### 2026-11-25 exact-head verification of the polynomial RG control

Workflow 45590315635 on exact head
977ab5919d1055bfc3545473687a9a3cea3237d3 passed 203 Python tests,
the 4/4 two-scale smoke scan, the 11-grid bare-WKB UV audit and the
47-page manuscript build. The beta-function reconstruction and all
three new RG regressions passed. The smoke and UV JSON payloads were
strictly parsed. The manuscript has zero Overfull boxes and no
final-pass unresolved references/citations; 80 Underfull hbox warnings
remain.

The UV audit still reports a fixed-box bare-stress factor of 16664.2325
and a high-cutoff log slope of 3.8822733. Zero-point energy remains,
no subtraction or counterterms are applied, and no continuum limit is
claimed. The RG beta functions apply only to the polynomial control
model, not the PTUM plateau. R0 remains partial, Gate 5 remains
**NOT MET**, and Gate 10 remains **PARTIAL**.


### 2026-11-25 analytic conformal radiation-FRW benchmark (pending exact-head CI)

An exact free massless conformal-scalar benchmark has been added for
radiation-dominated spatially flat FLRW. The code returns the conformal
plane-wave modes and Wronskian, the heat-kernel trace anomaly, and the
homogeneous conserved stress tensor after setting the independent
state-dependent \(a^{-4}\) component to zero. Tests cover the trace,
continuity, curvature-invariant and Minkowski limits.

This advances R1 only as an analytic benchmark. It is not a general
adiabatic subtraction or an independent numerical point-splitting
comparison. Massive/interacting modes, numerical UV/volume/time-step
convergence and PTUM backreaction remain absent. Gate 5 remains
**NOT MET**; exact-head CI is pending.


### 2026-11-25 exact-head conformal radiation-FRW benchmark verification

Workflow 45591701409 on exact head
8c903c7575c46ddbf592e83949531f09c86a0fd4 passed 211 Python tests,
the 4/4 two-scale smoke scan, the 11-grid UV audit and the 48-page
LaTeX build. The exact conformal mode/Wronskian and trace/continuity
Ward-identity tests passed after replacing overstrict absolute-zero
assertions with scale-normalized residual checks.

The smoke artifact remains a homogeneous classical scan, not a
quantum-seeded waterfall. The UV artifact still shows a fixed-box
bare-stress factor of 16664.2325 and a high-cutoff log slope of
3.8822733, with zero-point energy retained and no subtraction,
counterterms or continuum claim. The PDF has zero Overfull boxes and
no final-pass unresolved references/citations, but 80 Underfull hbox
warnings remain. R1 remains partial, Gate 5 remains **NOT MET**, and
Gate 10 remains **PARTIAL**.


### 2026-11-25 fresh exact-endpoint full-grid revalidation queued

The current branch now requests a fresh full scan because older
100-row results predate subsequent changes to the action signs,
threshold matching and numerical diagnostics. The scan derives
\(\Phi_c\) from the exact Hubble-flow endpoint and will run 100
homogeneous post-threshold trajectories plus the paired
4,001/256,001-point and four-level solver-tolerance study on the same
initial-condition grid. The scan is explicitly classical and
quantum_vacuum_seeded=false. The run is queued; no result is inferred.
Gate 4 remains scoped to the homogeneous post-threshold equations.
Gate 5 remains **NOT MET** and Gate 7 remains **NOT MET**.


## 2026-11-25 exact-head paired convergence result

The fresh paired study in workflow 45592679131 ran on source head
4590fc37825399f668098bdf3177b261e60e071f. It completed all five
profiles and passed the declared homogeneous-domain acceptance rule:
- 500/500 integrations succeeded, zero failed runs, 400 comparisons.
  Each of the five profiles has 100/100 expected unique row keys, with
  no missing or unexpected keys.
- The 4,001-to-256,001 output-grid comparison passed 100/100 rows.
  The finite-difference FRW continuity residual decreased for every
  row; median observed order was 0.9905928, median reduction factor
  61.5445, and minimum reduction factor 1.37970.
- Successive solver-tolerance comparisons passed 98/100, 99/100 and
  100/100 rows. The first two refinements are retained as history and
  are not represented as full strict-threshold passes. All six state
  error envelopes and all measured dimensionless classification
  diagnostic envelopes decreased monotonically; classification flags,
  metric availability and conservation checks remained consistent.
  The finest adjacent tolerance pair passed 100/100. The production
  tolerances were not relaxed.
- The 400-comparison summary reports 297/300 strict pairwise tolerance
  comparisons passing, with 100/100 at the final adjacent refinement.
  The acceptance rule explicitly requires monotonic envelopes and a
  passing finest pair, not retroactive passage of earlier pairs.
- Quadratic virial data were consistently unavailable in all rows and
  are recorded as unavailable, not as measured. Q, w and the virial
  diagnostic were available in 94/100 rows; H/omega was available in
  73/100 rows.
- Artifact ZIP SHA-256:
  108f00e04b2b919572b0fe1c7ab2b1c14ec1a8fe8d18750a7ac6176d63eed2b5.
  Extracted strict-JSON SHA-256:
  de97dd3d35d5c20d0ee63c00fecd1c5efa0cf3b588a3083a4c0f7838da4f5d2c.
  Both JSON files in the ZIP were parsed with non-finite constants rejected.

All six jobs in workflow 45592679131 passed: 211 Python cases, the
4/4 two-scale smoke scan, the 100/100 baseline scan, the 36-run
targeted convergence probe, the paired 500-run study and the 11-grid
bare-WKB UV audit, plus the LaTeX build. The PDF has zero Overfull
boxes and zero unresolved references/citations, but 80 Underfull
hbox warnings remain.

This closes the fresh output-grid and solver-tolerance package only
for the homogeneous two-field post-threshold equations. It does not
simulate the threshold crossing or quantum-seeded inhomogeneous
waterfall and does not include renormalized backreaction, rescattering,
defect-network evolution or relic production. Gate 4 remains scoped
to that homogeneous domain. Gate 5 remains NOT MET; Gate 10 remains
PARTIAL.


## 2026-11-25 fresh exact-endpoint 100-row baseline scan

Workflow 45592679131 on exact source head 4590fc37825399f668098bdf3177b261e60e071f completed the baseline full scan:
- 100/100 integrations succeeded, zero failed rows; 50 rows in each scenario and 100 unique initial-condition keys.
- All rows use the exact threshold Phi_c/M_Pl = 0.9862280831209045, 4,001 output points over 20 mu^-1, DOP853, rtol=1e-9, atol=1e-12, and quantum_vacuum_seeded=false.
- Classification counts: high-scale threshold-matched, 48 non-quartic and 2 insufficient-oscillation rows, 0 quartic; low-scale underdamped control, 41 non-quartic, 4 insufficient-oscillation and 5 quartic rows. Overall: 89 non-quartic, 6 insufficient-oscillation, 5 quartic.
- Every quartic row lies in the low-scale control at the largest tested classical field seed (psi_init=5 psi_0) and the smaller offset (0.01 Phi_c). Their w_final spans 0.37218--0.37363, Q_final 10.651--11.071, virial ratio 0.90607--0.90962, and H/omega about 6.87e-5--7.01e-5. They are not quantum-vacuum-seeded attractor evidence.
- The strict JSON artifact was parsed with non-finite JSON constants rejected. ZIP SHA-256: 82d1771f15417d172152233fcd1c41fcec776df936b6b56dfc59f958dcc2556d; extracted result JSON SHA-256: 625873f9d761e6df694170c33efa02dc543464f87542d75f76ff747c856764e3.
- The maximum chain-rule FRW continuity residual was 1.33249e-10; the maximum sampled finite-difference residual ratio was 0.03723375. These are diagnostics of the homogeneous ODE/output-grid calculation, not a full inhomogeneous stress-tensor conservation result.
- Exact-head short checks on this scan head passed 211 Python cases, 4/4 two-scale smoke trajectories, targeted convergence, the 11-grid bare-WKB UV audit, and LaTeX. The PDF is 48 pages; its final pass has zero Overfull boxes and zero unresolved references/citations, but 80 Underfull hbox warnings remain.

This baseline scan is separate from the paired 500-run convergence study recorded below. It is a homogeneous post-threshold classical sensitivity scan, not the coupled threshold crossing or quantum-seeded inhomogeneous waterfall.


## 2026-11-25 R1.2 second-order adiabatic subtraction for field variance

The new ptum_adiabatic_subtraction.py helper derives the local adiabatic
counterterm for the scalar field variance in four-dimensional FLRW. For the
canonical conformal-time mode
v_k'' + [k^2+a^2 M^2+(6 xi-1)a''/a] v_k = 0, define
omega_k^2=k^2+a^2 M^2 and
W2 = (6 xi-1)a''/(2 a omega_k) - omega_k''/(4 omega_k^2)
     + 3(omega_k')^2/(8 omega_k^3),
|v_k|^2_ad^(0-2) = 1/(2 omega_k) - W2/(2 omega_k^2).
The derivatives of the supplied M^2(eta) are included in omega_k' and
omega_k''. The finite-band integral also checks the canonical Wronskian
v_k v_k'^* - v_k' v_k^* = i and rejects non-positive zeroth-order
frequencies rather than assigning a vacuum to unstable modes.

Five new regressions cover the exact conformal massless and Minkowski
massive limits, independent finite-difference checks of the frequency
derivatives, Wronskian rejection, and non-positive-frequency/grid rejection.

This is an R1 field-variance subtraction control only. The integral is
explicitly finite-band: neither IR nor UV tails are extrapolated, finite
renormalization conditions are not selected, and no stress-tensor
subtraction, renormalized Phi force, CTP finite part, initial
Friedmann closure, or lattice counterterm is supplied. It does not
renormalize the nonlinear PTUM waterfall. Gate 5 remains NOT MET.


## 2026-11-25 exact-head short CI for adiabatic variance helper

Workflow 45596418537 on code head 9171604a41e25b8fb0ee78833be09603fd592293 passed:
- 216 Python regression cases, including the five second-order adiabatic field-variance tests;
- 4/4 two-scale homogeneous smoke trajectories with zero failed integrations;
- the 11-grid bare-WKB UV cutoff audit;
- the 48-page manuscript PDF build.

The final LaTeX pass has zero unresolved references/citations and zero
Overfull hboxes. It retains 80 Underfull hbox warnings. The UV audit
still reports the bare fixed-box stress growth factor 16664.2325 and
high-cutoff log slope 3.8822733; zero-point energy remains and no
subtraction, counterterms or continuum limit are claimed. The long
full-scan jobs were skipped for this non-FULL-SCAN commit; the separate
paired 500-run convergence result remains tied to source head
4590fc37825399f668098bdf3177b261e60e071f, whose simulation source was
unchanged by the adiabatic helper.

The new field-variance routine remains a finite-band R1 control only.
It does not close the renormalized stress tensor, the Phi force, the
initial Friedmann constraint or the nonlinear lattice counterterms.
Gate 5 remains NOT MET and Gate 10 remains PARTIAL.


## 2026-11-26 R1.3 local fourth-order adiabatic stress control

A new order-four WKB stress-counterterm module and finite-band
integrator have been added for a real scalar with an external
time-dependent mass on supplied spatially flat FLRW backgrounds.
The code derives W2 and W4 from the nonlinear WKB frequency equation,
varies the same nonminimally coupled scalar Hilbert tensor into rho
and pressure, checks canonical Wronskian normalization, and refuses
non-positive adiabatic frequencies. The order-two field-variance UV
subtraction remains distinct from the order-four matched WKB variance
completion.

Regression coverage includes the exact conformal-massless and
Minkowski-massive limits, finite-band vacuum cancellation, independent
W2 derivative finite differences, the matched external-mass Ward
identity, and fail-closed inputs. Exact-head CI is pending.

This advances only the local free-field renormalization controls.
Finite renormalization conditions, momentum tails, a renormalized
Phi force, self-consistent Friedmann backreaction, CTP finite parts,
SM/gauge/fermion/graviton loops, and lattice counterterms remain absent.
Gate 5 remains NOT MET; Gate 10 remains PARTIAL until exact-head CI and
the remaining warning cleanup are complete. PTUM is not 10/10.
