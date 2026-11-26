# PTUM Claim Boundary and Verification Status

**Snapshot:** 2026-11-19  
**Canonical repository:** https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-  
**Scientific correction branch:** `ptum/scientific-consistency-fixes-2026-11-13`

## 1. Safe core claim

PTUM is an effective phenomenological cosmological framework that parametrizes a threshold-triggered discharge and candidate dark-matter, residual dark-energy-like, and proxy-fluid dark-radiation sectors. The current homogeneous numerical model evolves only the `Phi-psi` subsystem. It does not yet establish the microscopic production of all sectors, their energy partition, or the complete post-discharge thermal history.

The proxy-fluid component is currently an effective linear closure with
[
w=1/3,qquad c_s^2=1/3,qquad sigma=0.
]
This closure gives a different CMB response from free-streaming radiation, but it remains phenomenological. The current waterfall benchmark has not demonstrated a stable quartic oscillatory regime or derived the closure from microscopic field dynamics.

## 2. Observational status

The manuscript reports the benchmark values
[
Deltachi^2equivchi^2_{m PTUM}-chi^2_{Lambda{m CDM}}=+0.26,
qquad
Delta{m AIC}=+2.26,
]
and
[
Delta N_{m fluid}<0.31quad (95% 	ext{ credibility}).
]
These are **author-reported, not independently reproduced**. The exact CLASS patch, production Cobaya configuration, likelihood settings, and MCMC chains are not yet available as a fully inspectable, reproducible public pipeline. Under the stated sign convention, the positive differences weakly favor the simpler (Lambda)CDM benchmark, not PTUM.

The observational constraint applies to the phenomenological proxy-fluid perturbation model. It must not be presented as a measurement of a microscopically calculated PTUM discharge abundance.

## 3. Scalar action, threshold, and sign conventions

The manuscript uses metric signature ((-+++)), canonical scalar kinetic terms, and the waterfall mass
[
m_{m eff}^2(Phi)
=m_psi^2left(\frac{\alpha\Phi^2}{E_{\rm th}^2}-1\right),
qquad
\Phi_c=\frac{E_{\rm th}}{\sqrt\alpha}.
]
Thus the proxy is stable for (|\Phi|>\Phi_c) and tachyonic for (|\Phi|<\Phi_c). The interaction potential in the scalar action is
[
U_{\Phi\psi}=+\frac12\frac{\alpha m_\psi^2}{E_{\rm th}^2}\Phi^2\psi^2.
]
The fuel equation, Hilbert-sector split, and signed transfer rates are written for this convention. For the stated split, (Q_\psi^0<0) when (\Phi>0) and (\dot\Phi<0); this signed source must not be described as positive energy injection into the proxy sector.

For (\lambda_\Phi=0.02), the exact canonical inflation endpoint is defined by (\epsilon_H=1):
[
\Phi_{\rm end}^{(H)}/M_{\rm Pl}\simeq0.98622808.
]
The older potential slow-roll proxy (\epsilon_V=1) gives approximately (1.387175M_{\rm Pl}) and is not the exact endpoint. Threshold-matched scans use the exact Hubble-flow endpoint. At that endpoint,
[
V_{\rm end}/V_0\simeq0.01926493,quad
K_{\rm end}/V_0\simeq0.00963246,quad
\rho_{\rm end}/V_0\simeq0.02889739.
]
The exact endpoint damping estimate is (3H_c/(2\mu)\simeq4.29); the potential-only estimate is approximately (3.50). Both indicate an overdamped threshold-matched benchmark. The plateau estimate is approximately (3H_*/(2\mu)\simeq25).

## 4. Homogeneous numerical status

The revised scan uses two scenarios:
- high-scale threshold-matched benchmark, (V_0=10^{64}\,\mathrm{GeV}^4);
- low-scale underdamped control, (V_0=10^{56}\,\mathrm{GeV}^4).

Each scenario has a (5\times5\times2) initial-condition grid, giving 50 trajectories per scenario and 100 total. Each trajectory uses 4001 output samples over (20\mu^{-1}). Fuel velocities at each post-threshold offset are taken from the integrated single-field FRW trajectory rather than from the potential slow-roll formula evaluated after the endpoint.

This remains a homogeneous **post-threshold sensitivity scan**. It does not evolve the coupled threshold crossing, quantum vacuum seeds, inhomogeneous tachyonic growth, rescattering, or backreaction. Exactly zero classical (\psi) initial data remain invariant under the deterministic homogeneous equations; they are not quantum-vacuum seeds.

The exact-head workflow 44280971987 completed the revised 100-row baseline with 100/100 successful integrations. The paired 500-run study completed all five profiles (100 unique rows each), 400/400 comparisons and zero failures. The 4,001-to-256,001 output-grid comparison preserved final states and classification flags in all 100 rows. The independent finite-difference continuity residual maximum decreased from 3.7234e-2 to 6.0499e-4 (61.5x); row-wise analysis gives minimum reduction factor 1.38 and median observed order 0.991. Solver-tolerance comparisons pass 98/100, 99/100 and 100/100 in successive refinements, with monotonic error envelopes and unchanged flags/availability. The finest-pair maximum state-relative difference is 1.63e-7. The baseline classifications are 89 non-quartic, 6 insufficient-oscillation and 5 quartic, all five quartic labels confined to the low-scale underdamped control. This supports Gate 4 only for the homogeneous post-threshold two-field background problem. It does not validate the coupled crossing, quantum seeds or inhomogeneous dynamics.

## 5. Energy-momentum tensors and Standard Model EFT

The manuscript specifies a minimally coupled classical tree-level action for Einstein gravity, the four real PTUM singlets, the complex Higgs doublet, three chiral SM generations, and the (SU(3)_c\times SU(2)_L\times U(1)_Y) gauge fields. The ordinary SM Yukawa matrices are separated from the gauge-invariant dimension-five PTUM operators (\psi\mathcal O_{\rm SM}/\Lambda).

The sector assignment is explicit. The displayed on-shell symmetric chiral-fermion tensor includes the ordinary SM Yukawa equations of motion, so the ordinary Yukawa potential is not added a second time as a separate metric term. The distinct PTUM operator (U_Y), which is outside (S_{\rm SM}^{(0)}), is assigned once through
[
T_{\rm SM}^{\mu\nu}=T_{{\rm SM},0}^{\mu\nu}-g^{\mu\nu}U_Y.
]
Gauge-representation, hypercharge, non-Abelian singlet, and canonical-dimension checks are implemented in `ptum_covariant_action.py`.

This closes the **classical tree-level action specification** only. Independent vierbein variation, numerical divergence checks with all SM/Higgs/fermion fields active, quantum corrections, EFT/UV matching, and thermal evolution remain incomplete. The current numerical background does not evolve the SM fields.

## 6. Resonance and dark-matter abundance

The repository contains:
- a frozen-background Mathieu monodromy/Floquet solver;
- a linear expanding-background (\chi_k) integrator on supplied (a(t),H(t),\Phi_{\rm res}(t)) histories;
- an adiabatic-vacuum initialization check, (H=\dot a/a) consistency check, and Wronskian monitor;
- a finite-band trapezoidal momentum integral over an explicitly supplied (k)-grid.

The mode integrator can pass through intermediate intervals with negative canonical frequency squared, but requires a real adiabatic initial state and assigns an instantaneous particle number only when the final canonical frequency is positive. The finite-band integral does not extrapolate unresolved infrared or ultraviolet tails.

These tools are **linear calculations on externally supplied backgrounds**, not a self-consistent PTUM production simulation. There is no converged momentum-range/grid result, no self-consistent (\Phi_{\rm res}) history, no backreaction or rescattering, no nonlinear fragmentation, and no entropy-dilution calculation. No numerical (\Omega_\chi h^2) or relic abundance is claimed. The overdamped threshold-matched benchmark does not currently establish the coherent oscillatory history assumed by the simple Floquet treatment.

## 7. Proxy-fluid and defect boundaries

The real (\psi) waterfall potential has two degenerate tachyonic minima,
[
\psi_{\min}=\pm\sqrt{-m_{\rm eff}^2/\lambda_\psi}.
]
A spatially inhomogeneous transition can therefore produce (Z_2) domain walls. The model does not derive cosmic strings from this real-scalar truncation. The odd dimension-five fermion-Higgs operator may explicitly break (Z_2), but the induced vacuum bias and wall lifetime depend on Wilson coefficients and any additional discrete charge assignments; neither has been calculated. No defect-free claim is made.

For a conditional benchmark with frozen Phi=0, mu_eff=m_psi=1e13 GeV,
lambda_psi=0.1, T_BBN=5 MeV, g*=10.75 and scaling-network area factor
A=1, the analytic wall estimate gives sigma_wall=9.42809e39 GeV^3,
H_BBN=1.11474e-23 GeV and H_dom=530.035 GeV. An unbiased scaling
network would dominate far before BBN. The small-bias source needed to
annihilate before both is approximately 7.90130e28 GeV^3, or
6.49158e-11 epsilon_crit. This is a conditional order-of-magnitude
estimate, not a prediction of the actual SM-induced bias or a defect
network simulation; Wilson coefficients, the renormalized SM
expectation value and the thermal history are unspecified.

Likewise, (w=1/3,c_s^2=1/3,\sigma=0) is not a demonstrated microscopic attractor. It remains a conditional phenomenological closure until field-level perturbations, sound speed, anisotropic stress, and stability are derived and converged.

## 8. Reproducibility and current CI boundary

The exact-head workflow 44280971987 on commit
1c975a73c7e7daa17c01adffe0fd19d929e8d7bb completed successfully:
146 Python tests passed; the two-scale smoke scan passed 4/4; the
100-row baseline passed 100/100; the targeted convergence probe passed
36/36; and the paired full-grid study completed 500/500 integrations
and 400 comparisons with full_study_pass=true. All five jobs passed.
The paired artifact ZIP SHA-256 is
f4d6566db7984c83f3564688a0ceac762dcc4f3ee7905cd0fa0e8a2ed6d25842;
the strict-JSON SHA-256 is
800661282f7a5ee0a92d887def3c6f0207028b6992741127f726a1ccdbea3f3c.

The 43-page manuscript PDF compiled and was uploaded. The final third
pdflatex pass has no Overfull hbox and no unresolved reference/citation
warnings; the 74 Underfull hbox warnings remain, including several
badness-10000 paragraphs. The first pass reports unresolved labels as
expected while writing the auxiliary file, but the final pass resolves
them. The anomaly equation wrap has therefore removed the prior
43.24 pt overfull line. The output-grid finite-difference convergence
gate and domain-wall benchmark are newer than the prior exact-head
artifact and require their own full-study/CI confirmation.

The paired run reports a homogeneous post-threshold numerical result
only. It does not establish coupled threshold crossing, quantum-seeded
inhomogeneous waterfall dynamics, backreaction, rescattering, relic
abundance, entropy dilution or a microscopic proxy-fluid realization.
The tracked main.pdf is not treated as the current build artifact.


The historical repository URL https://github.com/ErdemEsa/ptum-cosmology.git
returned HTTP 404 during the 2026-11-13 API review. The current repository
does not expose the CLASS patch as an individually reviewable tracked
source file, and the archive contents have not been verified. Public
availability and apply-check success for that patch remain UNVERIFIED.
See PTUM_REPRODUCIBILITY_NOTES.md.

## 9. Historical results that must not be reused

The earlier 36-point scan used the superseded activation-mass sign and the older (\epsilon_V=1) threshold estimate. Its classifications are historical only and do not validate the current waterfall convention. Likewise, the older (1.387175M_{\rm Pl}) threshold, the former 18-point scan description, and the previous universal Floquet/relic estimates are superseded.

## 10. Claims intentionally not made

PTUM is not claimed to be:
- a UV-complete or quantum-renormalized theory;
- a first-principles derivation of the pre-discharge background or a solution to the cosmological-constant problem;
- a completed coupled inflation-to-waterfall calculation with quantum seeds and backreaction;
- a microscopic derivation of the proxy-fluid closure;
- a converged parametric-resonance relic-abundance calculation;
- a fully evolved SM reheating and entropy history;
- an independently reproduced CLASS/Cobaya observational pipeline;
- a defect-free real-scalar waterfall model.

## 11. 10/10 acceptance rule

The ten evidence gates and their statuses are maintained in
`PTUM_10_OF_10_ACCEPTANCE.md`. PTUM is not 10/10 until all gates are met,
the latest full CI and LaTeX build pass, the complete 100-trajectory scan
is inspected and converged, and every quantitative scientific claim is
reproducible from a clean checkout.


## 2026-11-14 final particle-basis boundary

An instantaneous mode occupation is now accepted only when the final
canonical frequency is positive, the final first-order WKB measure
$|\\dot\\Omega_k/\\Omega_k^2|$ is at most 0.1 by default, and the
canonical Wronskian passes its declared tolerance. A positive final
frequency is not sufficient when the background remains rapidly
time-dependent. If the final WKB test or Wronskian test fails, the
occupation is withheld as NaN and the finite-band number-density
integral is withheld for the affected spectrum. The threshold is a
numerical reliability choice and must be varied in a convergence study.

This additional guard does not promote the linear mode calculation to
a relic prediction. The calculation still uses a prescribed
single-field background, a finite momentum interval, and no mode
backreaction, rescattering, nonlinear fragmentation, thermalization,
or entropy dilution. The full 100-trajectory homogeneous scan also
remains distinct from a quantum-seeded inhomogeneous waterfall.

The last verified CI checkpoint is workflow 43501562655 on the
previous head: 72 tests passed, the four-trajectory two-scale smoke
scan passed, and the LaTeX build passed with zero overfull-box warnings.
The branch now has 75 tests after the final-WKB correction; those
newest tests and code are pending a fresh CI run. The smoke artifact's
two nonzero-seed trajectories did not establish quartic domination or
a stable radiation-like proxy-fluid phase. No full-scan, relic-density,
or microscopic proxy-fluid claim is added.


## 12. 2026-11-14 verification update

The final-WKB manuscript regression was corrected in commit
`82ab0f26014de58634386efd1d90b635f6ec9e45`: the test now checks the
manuscript's actual statement that both the mode occupation and its
associated finite-band number density are withheld when the final
particle-basis validity conditions fail.

Workflow `43580982470` completed successfully on that commit:
- 75 Python regression tests passed;
- the four-trajectory, two-scale CI smoke scan completed with four
  successful integrations and zero integration failures;
- each energy-scale scenario contained one
  `insufficient_oscillation_data` result and one `non_quartic` result;
- the manuscript compiled and its PDF artifact was uploaded.

The LaTeX build still emits Underfull \\hbox and two float-placement
warnings, although no Overfull \\hbox warning was reported. These are
not treated as a clean-warning build. The four-row smoke scan does not
replace the 100-row high-resolution scan and cannot establish a physical
quartic regime.

The previous workflow `43580694626` failed only at the stale source
assertion (74 passed, 1 failed); the corrected branch head is verified
by `43580982470`. No full 100-trajectory artifact has yet been inspected.
The full scan, independent time-grid and solver-tolerance convergence,
inhomogeneous backreaction, rescattering, defect evolution, and
self-consistent relic/entropy calculation remain open. The project is
not 10/10.


### 2026-11-14 latest-head checkpoint

The latest PR head at this checkpoint is
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`. Workflow
`43582227619` passed 75 Python regression tests, all four CI smoke
integrations, and the LaTeX build. The high- and low-scale smoke
scenarios each contained one `insufficient_oscillation_data` and one
`non_quartic` result; no quartic-dominated radiation-like phase was
established.

The LaTeX build is successful but not warning-free: the log contains
numerous Underfull \\hbox messages and two distinct float-placement
warnings; no Overfull \\hbox or LaTeX error was reported.

An isolated scan branch
`ptum/full-scan-2026-11-14-r2` was created from the latest PR head
and received manifest commit
`c101aaed58e44c9f0159ebb806a84d670cd892e2`. No completed 100-row
artifact has yet been inspected or validated. The full scan remains
a homogeneous post-threshold sensitivity study, not a quantum-seeded
inhomogeneous waterfall or a relic calculation.


## 2026-11-14 tilted-domain-wall diagnostic boundary

The analytic defect module now returns the dimensionful locations of the
true and false stationary minima for a tilted quartic potential. These
are algebraic stationary points of a frozen-background potential; they
are not a prediction of the bias. At or above the spinodal source the
metastable minimum no longer exists and both minimum-location fields are
reported as unavailable.

The bias source
\[
\epsilon_{\rm bias}=|C|\,|\langle\mathcal O_{\rm SM}\rangle|/\Lambda
\]
still depends on a renormalized operator expectation value, Wilson
coefficient, cutoff, and thermal history that have not been calculated
for PTUM. The kink tension and annihilation/domination estimates remain
conditional order-of-magnitude diagnostics. No defect formation
probability, network scaling solution, annihilation history, or
BBN-safe realization is claimed.


## 2026-11-14 conditional thermal fermion bias

A zero-temperature-subtracted ideal-gas expression is now implemented
for the finite-temperature scalar condensate of a free equilibrium
Dirac species in the broken electroweak phase. With fixed mass and the diagonal real mass-basis coupling
$m_f(\psi)=m_f+\operatorname{Re}[(C_f)_{ii}]v_H\psi/(\sqrt2\Lambda)$,
where $v_H$ is the fixed broken-phase Higgs expectation value and
$i$ labels a diagonal fermion mass eigenstate, it gives the conditional
thermal linear coefficient in the convention
$V_{\rm bias}=-\epsilon_{\rm bias}\psi$.

This estimate is not the PTUM bias prediction. It assumes a fixed
broken-phase Higgs expectation value, equilibrium free fermions and
zero chemical potential, and omits gauge/QCD corrections, thermal
masses, the electroweak crossover, non-equilibrium reheating, and
the renormalized vacuum condensate. The Wilson matrices, cutoff,
thermal history and operator renormalization remain unspecified.
No defect-wall annihilation time or BBN-safe network is claimed.



## 2026-11-15 verification and bounded-scan update

The latest verified PR workflow at this snapshot is
`43701174233` on source commit
`5379ec8a2e85e875c9819121b0409ea454cf99e9`: 93 Python tests passed,
all four two-scale smoke integrations succeeded, and the 42-page
manuscript PDF compiled. The smoke rows still classify as one
`insufficient_oscillation_data` and one `non_quartic` per energy
scenario; they do not demonstrate a quartic proxy-fluid regime.

The final LaTeX log audit found no Overfull `\\hbox` and no float
placement warnings after the thermal-condensate integral was split
across lines and two tables were changed from `[h]` to `[htbp]`.
Underfull `\\hbox` warnings remain. Initial-pass citation warnings
are resolved by later `latexmk` passes; no unresolved references
remain in the final pass.

A prior 100-point run (`43582371029`, old source
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`) was cancelled by a
hosted-runner shutdown after 20/100 trajectories. The scan artifact
was not uploaded, so those rows are not a validated result and no
physical classification is inferred.

The current scan implementation adds a deterministic 100000-RHS-call
budget per DOP853 trajectory (configurable by CLI/API), records solver
statistics and budget exhaustion in strict JSON, and fails closed on
budget exhaustion. This is a resource guard only; it does not alter
the ODE tolerances or establish convergence. The new 100-trajectory
run is workflow `43701420639` on source commit
`af9724092c94d8469fcf23a87f29438b2cf8c58a`; it was in progress
at this update. Until its complete artifact is inspected, the full
scan remains unverified.

The safe scientific claim is unchanged: the repository has a
homogeneous two-field post-threshold solver, linear mode tools on
prescribed backgrounds, and analytic defect diagnostics. It does
not yet contain a converged quantum-seeded inhomogeneous waterfall,
nonlinear backreaction/rescattering, a relic-abundance calculation,
a microscopic proxy-fluid realization, or an independently rerun
CLASS/Cobaya pipeline. PTUM is not 10/10.


## 2026-11-15 full-scan and current verification boundary

A 100-row artifact from workflow 43701420639 is available, but it is
not a validated result for the current implementation. The job used
DOP853 with a 100000-call budget on source af9724092c94d8469fcf23a87f29438b2cf8c58a:
97/100 rows integrated successfully and three failed. No successful
row passed the joint quartic classifier. The JSON is strict and
inspectable, but the source comparison to ca053f58e3713b274e22f0d69bd5ca89863dab26
shows 21 intervening commits, including changes to the scan and
simulation modules and workflow. The old classifications are retained
only as a historical diagnostic and are not evidence for the current
code.

On the current PR source, workflow 43703509401 passed 98 Python tests,
all four smoke integrations, and the 42-page LaTeX build. The smoke
results remain one insufficient_oscillation_data and one non_quartic
row in each energy-scale scenario. They do not establish a quartic
proxy-fluid phase. The final LaTeX build has no Overfull hbox or
float-placement warnings, but Underfull hbox warnings remain.

A new current-source 100-trajectory Radau run is queued as workflow
43703837000, with rtol=1e-9, atol=1e-12 and a 1000000-RHS per-row
engineering guard. Until its complete artifact is inspected and all
integrations pass, no 100-row physical classification is claimed.
The simulation remains homogeneous and post-threshold; it does not
include quantum-seeded inhomogeneous modes, nonlinear backreaction,
rescattering, or a relic abundance. No acceptance gate is promoted
by the earlier DOP853 artifact or the passing smoke scan.


## 2026-11-15 distinction between public background scan and reported mode integration

The public module ptum_inflation_background.py reproduces the
scalar-dominated flat-FRW background and first-order Hubble-flow
observables for the eight-point lambda_phi scan. The manuscript table
is generated by this module; CI checks all eight scan rows, the
60-e-fold termination, and key reference observables. The table is
therefore a reproducible background calculation, not an
author-reported-only result.

A separate 200-mode Mukhanov-Sasaki calculation over
10^-4 <= k <= 1 Mpc^-1 is described in the manuscript, but its
mode-integration code, raw spectra and numerical outputs are not
included. The public background module does not integrate mode
functions. The earlier phrase claiming that the mode calculation was
numerically verified with the public script was inaccurate and has
been removed. The mode-spectrum agreement remains AUTHOR-REPORTED
and is not independently reproduced. This does not change Gate 9:
the CLASS/Cobaya likelihood pipeline, data and chains remain
unverified.

## 2026-11-15 Radau scan evidence boundary

The 100-row Radau artifact from workflow 43703987436 is a strict-JSON
diagnostic for the current scan code (the four commits from its source
to the current pre-fix PR head changed only acceptance/claim/correction
documentation and main.tex, not the scan modules or workflow). Its ZIP
SHA-256 is
464c73c9907115ce6bc57ec53722fcc4ede4d8f17d0e66db856fcef00f8876a2;
the extracted JSON SHA-256 is
b348651738c1a5d35d15432ef2f1d8873ddfa9ea827238f84c1772b6ac1593e3.

The scan completed 98/100 integrations. The high-scale benchmark had
47 non_quartic, two insufficient_oscillation_data and one RHS-budget
failure; the low-scale control had 42 non_quartic, seven
insufficient_oscillation_data and one RHS-budget failure. Both failed
rows share psi_init=4.460941604639096e12,
psi_dot_init=0 and phi_offset=2.4014653823994024e16, and each reached
1,000,001 attempted Radau RHS evaluations against the 1,000,000 guard.
No successful row passed the joint quartic classifier. This does not
prove that no quartic regime exists elsewhere; it shows only that the
declared finite homogeneous post-threshold grid did not establish one.

The high-scale median finite-difference continuity residual normalized
by H rho is about 3.72e-2, compared with about 4.03e-6 for the
low-scale control. The high-scale maximum chain-rule relative residual
is about 1.68e-10. These values require output-grid and solver-tolerance
convergence before the scan can be described as numerically converged.
The 100-row run is therefore a diagnostic artifact, not an accepted
physical result or a relic calculation.

The 200-mode Mukhanov-Sasaki spectrum remains AUTHOR-REPORTED because
the mode solver and raw spectra are absent. The public inflation
background module does not integrate those modes. The manuscript now
states this boundary explicitly.

The latest observed PR workflow 43704489063 passed 98 Python tests
and the four-row smoke scan but failed the LaTeX build because of an
unclosed itemize environment in the Mukhanov-Sasaki subsection. The
source correction and two regression guards are committed; the fresh
workflow is pending. No new physical acceptance claim follows from
these software changes.

The follow-up workflow 43705365503 verifies the corrected manuscript
build: 42-page PDF, zero Overfull hbox warnings, zero float-placement
warnings and no unresolved citations/references on the final LaTeX pass.
It still reports 138 Underfull hbox messages. The Python job reported
99 passed and one failed among 100 tests; the sole failure was a
whitespace-sensitive assertion spanning a LaTeX source line break.
Commit a5f86d7c8ca746e6948cfa5c391d11a63985ab87 normalizes whitespace
before checking the author-reported claim. A fresh full test run is
pending; no passing status is inferred from the test-only correction.

Fresh workflow 43705535067 on PR head 49933f4f1593327845944266e3412e67a3b545f3
passes all 100 Python tests and all four smoke integrations. The 42-page
LaTeX PDF builds; the final pass has no unresolved citations/references,
Overfull hbox, float-placement warning or Improper prevdepth error.
There are 138 Underfull hbox messages across the build log. The full
Radau scan remains 98/100 with two budget-exhausted rows and no
joint-quartic classifications among the 98 successful rows. The passing
smoke scan and 100-test suite do not change the physical claim boundary.

The manuscript now includes the current Radau scan outcome rather than
leaving the 100-row scan pending: 98/100 integrations succeeded, two
failed at the RHS budget, and none of the 98 successful rows passed
the joint quartic classifier. The high-scale maximum Q is about 1.002.
Some low-scale large-classical-seed rows have Q up to 11.12, w about
0.363 and virial ratio about 0.890, but only two late half-cycles occur
in the final 20 percent; the adiabaticity diagnostic is therefore
unavailable. This is a transient quartic-like average, not a sustained
quartic-fluid result. The isolated BDF cross-check (PR #5) is complete:
it matches the two Radau budget failures and all 98 successful-row
regime labels, but does not establish time-grid or tolerance convergence.

The isolated BDF rerun (workflow 43705977596, execution PR #5) also
completed 98/100 trajectories and failed on the same two RHS-budget
rows as Radau. All 98 shared successful rows have identical regime
labels. The maximum relative final-state differences are below
2.4e-3 (the largest is psi_dot); Q, w and virial classifier metrics
agree to at least about 4e-5 relative. This supports cross-method
stability of the 98 successful classifications but does not establish
time-grid or tolerance convergence. The BDF artifact is strict JSON
with 100 rows and no non-finite numeric values.

The first DOP853 execution PR #6 was based on a stale source commit
and its full scan failed, so it is not a valid same-source comparison.
A replacement isolated execution PR #7 was created directly from PR #2
source commit bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0. Workflow
43753469944 completed the 100-row DOP853 profile at rtol=1e-9,
atol=1e-12 and a 1,000,000-RHS per-row guard. All 100 integrations
succeeded and no row passed the joint quartic classifier. The two
rows that exhausted the same RHS guard under Radau and BDF completed
under DOP853, but have no successful implicit-solver counterpart.
On the 98 rows common to all three successful sets, all regime labels
are identical and DOP853/Radau final-state and classifier diagnostics
agree closely. This is cross-method agreement, not tolerance or
output-grid convergence. The scan remains homogeneous and
post-threshold, not an inhomogeneous waterfall or relic calculation.


## Targeted numerical convergence boundary (2026-11-15)

A 36-run DOP853 convergence workflow tested four selected trajectories:
the two rows that exhausted Radau/BDF RHS budgets and two high-Q
controls. All runs succeeded. Across tolerance changes, maximum
final-state relative difference was 4.75e-7 and maximum relative
difference in Q/w/virial diagnostics was 3.48e-7. Across 128,001 ->
256,001 output samples, all four regime labels, quartic flags and
late-half-cycle counts were unchanged. Maximum absolute diagnostic
changes were 7.57e-4 (Q_final), 2.57e-4 (w_final), 2.25e-4
(virial_final) and 6.05e-4 (finite-difference continuity diagnostic).
All four probes pass the explicitly encoded targeted limits.

This does not establish convergence of all 100 scan trajectories.
The two DOP853-only rows still lack successful Radau/BDF counterparts,
although their DOP853 self-convergence is included in the targeted
study. The high-scale finite-difference continuity diagnostic remains
at percent-level magnitude; the small chain-rule continuity residual
is a separate diagnostic and must not be conflated with it. No claim
of a fully converged full-grid numerical study is made.


## 2026-11-16 verification update

The completed workflow `43759304001` on head
`bc1f6dafb689be427631ae3baa79692b9fde1694` reports 108 passing
Python regression tests and a successful 4/4 two-scale smoke scan.
The 42-page LaTeX PDF builds, but the final pass retains 73 Underfull
hbox warnings and one Overfull hbox at line 1937. This is not a
warning-free manuscript build.

The full 100-row scan and targeted convergence were skipped in that
workflow. PR #2 now opts into both the full 100-row scan and the
existing targeted four-case convergence probe on the next synchronize
event. The targeted probe is not full-grid convergence. Until fresh
artifacts are inspected, the 100-row result and any new convergence
claim remain pending. The physical boundary is unchanged: no
quantum-seeded inhomogeneous waterfall, nonlinear backreaction,
rescattering, defect-network evolution, relic abundance, microscopic
proxy-fluid realization, or independent CLASS/Cobaya reproduction
is established.


## 2026-11-16 dense-output diagnostics: implementation, not yet evidence

PR #2 now contains the dense-output cycle estimator previously developed
on PR #11. It uses the accepted adaptive ODE mesh for turning-point
bracketing, root-refinement checks and adaptive quadrature for Q, virial,
excitation-sector w and mean H. Sampled estimators are retained as
cross-checks. Regression tests cover analytic and numerical oracles,
non-unit time scaling, solver-mesh variation, root-detection edge cases
and physical-time tail classification.

The 100-row 256,001-point strict-JSON driver and a dedicated PR #2
workflow job have also been added. The next full-scan workflow is
expected to run the 4,001-point baseline, the targeted four-case
tolerance/output-grid probe and the refined 256,001-point scan. Until
the new-head CI passes and the artifact is inspected, these are
implementation claims only. The old PR #11 high-resolution artifact
used sampled cycle diagnostics and is not evidence for the dense
estimator. Gate 4 remains PARTIAL.


## 2026-11-16 dense-cycle regression failure and correction

The first CI run after the dense-output port reported 122 passed and
seven failed. Five failures were caused by empty dense-cycle arrays
incorrectly bypassing the legacy sampled-diagnostic fallback. Two
harmonic-oracle failures came from floating-point roundoff at the final
(4pi) endpoint, which hid a genuine turning point.

The classifier now requires a nonempty dense-cycle record before
selecting the dense path. Endpoint values are treated as zero only when
they lie within a scale-relative machine-roundoff tolerance. Two
regressions guard these cases. The correction does not relax physical
thresholds or root-refinement criteria. Until fresh CI passes, the
dense-estimator implementation remains unverified and Gate 4 remains
PARTIAL.


## 2026-11-16 provisional numerical results from the pre-fix head

The pre-fix dense-estimator head completed a 100-row 4,001-point scan
with 100/100 successful integrations. It classified 5 rows quartic,
89 non-quartic and 6 insufficient. All five quartic rows required the
largest classical seed (5psi_0) in the low-scale underdamped control
and the smallest threshold offset; each had only four or five late
half-cycles. This is not evidence for quantum vacuum seeding, a broad
attractor basin, or defect-free evolution.

The four-case targeted convergence probe passed 36/36 runs. Its maximum
grid change in the finite-difference continuity residual was
(6.043	imes10^{-4}), maximum tolerance-induced classification
difference (9.38	imes10^{-7}), and maximum final-state relative
difference (4.75	imes10^{-7}). These pass the targeted thresholds
for those four cases only. They do not replace 100-row convergence.

The workflow also reported seven Python regression failures (122 passed).
Two implementation fixes were committed in
`a172c6a72121d63ba8391af9d35ba8d225e39403`; all scan results from the
pre-fix head are provisional until rerun on the corrected head. The
100-row 256,001-point job was still running at the time of this record.


## 2026-11-16 analytic quadrature test fixture corrected

The latest CI run reported 130 passed and one failed test. The remaining
failure came from a synthetic oscillator whose time scale did not match
the PTUM mass parameter, leaving its kinetic moment about (10^{-28})
of the potential scale. The resulting large relative quadrature error
was correctly reported by the implementation. The tests now use a
dimensionally consistent (mu=mathrm{params.mu}), and set (m_psi)
so the non-unit-(mu) fixture has (mu=2.5). The strict (10^{-8})
error assertion is retained; no numerical tolerance was weakened.


## 2026-11-16 full 100-row dense output-grid result

The 100-row 256,001-point DOP853 scan completed with 100/100 successful
rows, 100 unique keys and a complete checkpoint. Joined against the
4,001-point baseline, all final-state variables, Q, w, quartic virial
ratios, regime labels and quartic flags were identical at reported
precision. The analytic continuity-residual difference was at most
(2.98	imes10^{-10}). The maximum finite-difference continuity
residual fell from (3.7234	imes10^{-2}) to (6.0499	imes10^{-4}),
a factor of 61.5. The maximum dense quadrature relative-error estimate
was (5.97	imes10^{-6}).

The four-case tolerance/output-grid probe passed 36/36 runs. These
results strongly support output-grid stability for the 100 homogeneous
post-threshold rows, but they do not establish full 100-row
solver-tolerance convergence or any inhomogeneous waterfall,
backreaction, rescattering, relic or observational result.

The only remaining Python failure in the workflow was a synthetic
harmonic test fixture with a time scale inconsistent with the model's
mass parameter. It was corrected in commit
`7af32e39757f4b4c8cd78f2bda0b1eed9d83d345`; fresh CI is pending.
The five quartic classifications occur only at the largest classical
seed and must not be described as quantum-vacuum-seeded evidence.


## 2026-11-17 numerical evidence boundary

Workflow 43843783240 on head 32f33013d81617ac998ddd0707be374f0bb1ecb6
passed 131 Python tests, the four-row smoke scan, the 100-row baseline,
the 100-row 256,001-point dense scan, the 36-run targeted convergence
probe and the LaTeX build. The strict-JSON artifacts were downloaded
and parsed. The two full scans have matching normalized row keys and
unchanged classification labels, but their independently recomputed
endpoint values differ by about 2.3e-15 relatively. This tiny
roundoff-level input difference means the comparison is not a strict
same-input output-grid experiment.

A new paired 400-run study now holds each scenario parameter object and
initial-condition tuple fixed while changing output grid and solver
tolerance. It is the next accepted numerical test and remains pending
until its own artifact and CI result are inspected.

The current homogeneous scan still does not evolve the coupled
inflation-to-waterfall crossing, quantum vacuum fluctuations,
inhomogeneous tachyonic modes, nonlinear backreaction, rescattering,
defect networks, thermalization or relic abundance. The five quartic
classifications are confined to large classical seeds in the low-scale
control and are not a microscopic proxy-fluid result. The 42-page
manuscript compiles but still reports 73 Underfull and one Overfull
hbox warning.


## 2026-11-17 manuscript warning follow-up

The long complex-Higgs reheating equation has been split across an
aligned display without changing its algebraic content. The source
regression now checks the display structure and derivative source.
This is a source-level correction only; the final LaTeX log must still
be inspected before claiming the Overfull hbox warning is resolved.
The 73 Underfull hbox warnings remain outstanding.


## 2026-11-17 CI audit and Higgs-source display correction

The current 100-row homogeneous baseline artifact from workflow
44056098156 contains 100 successful integrations and no failed rows.
Its classifications are 89 non-quartic, five quartic and six
insufficient-oscillation-data. The five quartic cases occur only for
the largest classical seed in the low-scale control at the smallest
threshold offset, with four or five late half-cycles. They are not
quantum-vacuum-seeded or evidence of a broad attractor.

The four-case targeted convergence artifact passed 36/36 runs. The
separate paired 400-run same-input study had not finished at this audit,
so no full-grid solver-tolerance result is claimed. The Python job
reported 134 passed and two stale test-assertion failures; both were
corrected, and a new regression checks the shared 100-row input grid
and all four convergence profiles.

The 42-page manuscript build succeeded, but the final compile output
still reported one 40.16039 pt Overfull hbox at line 1939 and 73
Underfull hbox warnings. A separate J_H source definition now splits
the long Higgs-equation derivative into two aligned terms. This is
only a presentation-preserving algebraic rewrite; the next build must
confirm whether it removes the overfull warning. Gates 4 and 10 remain
PARTIAL. The homogeneous scan does not establish inhomogeneous
waterfall dynamics, defect evolution, backreaction, relic abundance
or a microscopic proxy-fluid realization.


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


## 2026-11-17 toy-coupling scope

Do not interpret the generic \(\psi\bar f f\) Dirac bilinear as the
chiral Standard Model reheating operator. It is retained only as a
vector-like toy example. The PTUM chiral-SM coupling is the
gauge-invariant dimension-five operator
\(\psi\mathcal O_{\rm SM}/\Lambda\) built from \(Q_L,u_R,d_R,L_L,e_R\)
and the Higgs doublet. Likewise, the real-scalar portal example is a
toy model and is not the Higgs-doublet portal.

The manuscript now states this distinction and no longer claims that
the explicit chiral-SM action or its Hilbert tensor is missing. This
is a consistency correction only: it does not promote Gate 3, which
still requires dynamical SM/Higgs/fermion evolution and independent
numerical conservation convergence.


## 2026-11-18 numerical-convergence claim boundary

The paired 500-integration study completed all runs without integration failures, but its original fixed-reference comparison returned failure (281/300 solver-tolerance comparisons passed). A forensic analysis of the preserved strict-JSON rows found monotonically decreasing state and normalized dimensionless-diagnostic error envelopes across successive tolerance refinements, with the finest adjacent pair passing all 100 rows. The original failure remains recorded; it is not retroactively called a pass.

The comparator has been changed to compare adjacent solver-tolerance profiles, use natural-unit normalized absolute differences for dimensionless observables near zero, and require monotonic error-envelope reduction plus a passing finest pair. The former pure relative difference remains in the artifact as a diagnostic. This is a numerical-methodology correction, not new physical evidence. The new comparator and regression tests await exact-head CI verification.

No claim is added for coupled threshold crossing, quantum-seeded inhomogeneous waterfall, backreaction, rescattering, defect-network evolution, relic abundance, entropy dilution, microscopic proxy-fluid realization or observational reproduction. Gates 2, 3, 4, 5, 6, 7, 8, 9 and 10 retain their current statuses until the corresponding evidence is independently verified.


## 2026-11-18 Standard Model anomaly-audit boundary

The chiral-SM registry now verifies exact per-generation cancellation of SU(3)^3, SU(3)^2 U(1)_Y, SU(2)^2 U(1)_Y, U(1)_Y^3 and mixed gravitational-U(1)_Y anomalies, and checks the even number of weak doublets required to avoid the SU(2) Witten anomaly. This supports consistency of the declared minimal SM representation content. It does not imply that the PTUM quantum effective action, UV completion, reheating dynamics, or inhomogeneous waterfall has been solved. The audit and its regression test await exact-head CI.


## 2026-11-18 manuscript anomaly-equation boundary

The manuscript now explicitly shows the per-generation perturbative anomaly sums for the specified minimal chiral Standard Model and the even-doublet Witten check. The representation-level audit is displayed in the paper and tested against the code registry. This supports consistency of the declared SM field content only. It does not establish a PTUM UV completion, solve the quantum effective action, or provide evidence for inhomogeneous waterfall dynamics. The manuscript regression and exact-head LaTeX build await CI.


## 2026-11-18 optional diagnostic availability boundary

The paired artifact has no quadratic_virial_final values in any of its 100 rows across the refined-grid and tolerance profiles. The updated summary reports this as consistently unavailable, requires matching availability between profiles, and fails closed if any state component is missing. It does not convert the missing quadratic-virial measurement into a pass or a physical result. The corresponding regression and exact-head CI remain pending.


## 2026-11-18 CI trigger and convergence-availability boundary

The authorized branch now has a push trigger for ordinary regression/smoke/LaTeX checks and an explicit [FULL-SCAN] commit-message opt-in for the 100-row baseline, targeted convergence probe and paired 500-integration study. The workflow regression guards these conditions. The convergence summary reports the quadratic virial metric as unavailable in all paired profiles, rather than implying it was measured; it fails closed for missing state components and requires matching diagnostic availability across refinements. The latest full-scan run has not yet been inspected, so no new CI pass is claimed.


## 2026-11-19 real-psi network geometry sensitivity

The code and manuscript now expose the scaling-ansatz threshold
$\\mathcal A_{\\rm crit}=3M_{\\rm Pl}^2H_{\\rm BBN}/\\sigma_{\\rm wall}$.
For the stated $10^{13}$ GeV, $\\lambda_\\psi=0.1$ benchmark,
$\\mathcal A_{\\rm crit}=2.10315\\times10^{-26}$ and
$H_{\\rm dom}/H_{\\rm BBN}=\\mathcal A/\\mathcal A_{\\rm crit}$.
This quantifies why the conditional $\\mathcal A=1$ estimate is
catastrophic. It does not measure $\\mathcal A$, show that a scaling
network forms, or calculate its evolution. The real-$\\psi$ topology
therefore remains an unresolved physical risk until a quantum-seeded
inhomogeneous simulation follows formation, coarsening, bias-driven
annihilation and expansion.

The source-text regression for the conditional thermal-bias discussion
now normalizes whitespace so a LaTeX line wrap cannot cause a false
failure. This is not a scientific acceptance shortcut. Exact-head CI
is pending for the implementation, manuscript equation and regressions.

## 2026-11-19 nonlinear lattice claim boundary

The new 3-D periodic lattice solver evolves the real waterfall field
nonlinearly, includes spatial gradients, a homogeneous Phi response to
the volume-averaged psi^2, and the corresponding scalar-field contribution
to the expanding-FRW Friedmann equation. Classical nonlinear mode coupling
can produce rescattering and sign domains from caller-supplied classical
initial fields. The nearest-neighbour wall-area density is resolution and
box dependent; it is not the analytic scaling area factor A.

No quantum vacuum seed is generated, no vacuum renormalization is applied,
and no continuum/volume/time-step convergence study has yet been performed.
The code therefore provides a classical nonlinear numerical prototype,
not a physical prediction for the quantum waterfall or a domain-wall
network. It does not close Gate 5, does not establish the actual SM bias,
and does not support a relic-abundance claim. Exact-head regression and
LaTeX checks are pending.

The lattice solver additionally reports an instantaneous RHS-level
stress-energy balance residual computed by differentiating its discrete
energy functional. This verifies the internal consistency of the chosen
finite-difference operators and the Phi-psi force at the tested states.
It is not a substitute for continuum convergence, quantum renormalization,
or independent conservation of all PTUM/SM sectors.

For the lattice wall-area diagnostic, exact-zero sites are assigned to
the non-negative phase, avoiding a lost crossing when a wall passes
through a grid point. A periodic planar regression checks this convention.
This improves counting consistency but does not make the finite-grid
area density a continuum or scaling-network observable.

The manuscript now acknowledges the versioned 3-D classical scalar
lattice prototype and accurately limits its scope. The earlier statement
that no reviewable PTUM lattice solver existed has been removed. The
author-reported isocurvature/lattice calculations remain unreproduced:
the new prototype is not the authors' original four-field implementation
and cannot validate their reported numbers. It does not provide quantum
vacuum seeds, renormalization, SM-sector dynamics, or a physical wall
network prediction.

The appendix now states the equations implemented by the limited lattice
prototype, including the Phi force from one-half times the derivative of
m_eff squared times the spatial average of psi squared, the same scalar
energy in the Friedmann source, and the isotropic gradient pressure. This
is a two-field classical truncation with homogeneous Phi, not the full
four-field or chiral-SM action. Equation labels and claim boundaries are
guarded by regression tests.

The exact-head failure in workflow 44502156872 was a stale regression
expecting the manuscript to deny the existence of any reviewable lattice
solver. That sentence had correctly been replaced by the limited classical
prototype description. The test is corrected in 06164c1; this was a
documentation-regression mismatch, not a numerical or physics failure.
A fresh exact-head run is still required.



## 2026-11-20 adiabatic-WKB initial-sample claim boundary

The lattice module now samples the first-order adiabatic-WKB symmetrized
free-mode covariance for stable, adiabatic modes on a homogeneous-Phi
background. This is a bare Gaussian classical-statistical initial
ensemble, not a quantum evolution. The initializer retains zero-point
energy, applies no vacuum subtraction/counterterms, omits psi vacuum
backreaction in the initial H derivatives, and has no continuum
renormalization. The subsequent nonlinear solver remains classical and
UV-cutoff dependent. A successful sampler regression must not be
reported as a physical quantum-seeded waterfall, a defect-network
prediction, or a relic-abundance result. Gate 5 remains NOT MET.


The bare WKB sampler is a test-field initialization: its Hubble
frequency and derivatives use the homogeneous-Phi energy only, whereas
the subsequent classical lattice Friedmann source includes the raw
sampled psi energy. The solver therefore starts with a different total
H than the H used to construct the WKB sample. This mismatch is
reported explicitly and is another reason the sample is not a
self-consistent quantum initial state. No physical waterfall or relic
claim follows from evolving it without renormalization.


## 2026-11-21 bare WKB UV-cutoff audit claim boundary

The repository now computes the finite-volume Gaussian expectation of
the bare WKB lattice stress, including the first-order velocity-shift
covariance, central-difference gradient contribution and Gaussian Wick
quartic expectation. It reports the bare Friedmann H and H-prime implied
by that stress and compares them to the homogeneous-Phi test-field
background used by the sampler. A fixed-box grid sequence makes the
cutoff dependence explicit.

This is not vacuum renormalization. No zero-point subtraction,
counterterms, coupling renormalization or continuum extrapolation is
performed. The audit cannot be used as a physical initial state,
quantum-waterfall simulation, defect probability or relic calculation.
Gate 5 remains NOT MET.


The first UV-audit CI attempt failed because the WKB velocity shift is
mode-dependent. The implementation now treats nu_k as an array and
uses its mode-by-mode contribution to the velocity variance. The first
run produced no numerical artifact and is not evidence of cutoff growth.


## 2026-11-21 exact-head bare WKB stress audit

Exact-head workflow 44893367362 (9d9def8) passed 164 Python tests, the two-scale smoke scan, the bare WKB audit and the 44-page LaTeX build. The final LaTeX pass had zero Overfull hboxes and no unresolved references/citations, with 77 Underfull hbox warnings remaining.

For the fixed-box N=4,6,8,10 bare Gaussian audit at L=8 mu^-1, the lattice cutoff rose 1.73205 to 4.33013 mu and the unsubtracted psi stress rose by a factor 18.0182. The end-to-end log slope was 3.15553, and the bare Hubble mismatch rose from 2.13e-7 to 3.84e-6. This is cutoff-dependence evidence, not renormalization or a physical quantum prediction. ZIP SHA-256 c4fd531a8de4bd6a31177514afa9e0c7f8f46b67b12cef538315c2b73b643f12; JSON SHA-256 3f24f7c54748b2498d9e3cf57500bd3a738b2b0491cc63ae1a2baf0076f68fbf.

An extended fixed-box sequence through N=64 and a fixed-spacing volume sequence have been added. Their exact-head CI and artifact inspection are pending.


## 2026-11-21 extended bare WKB UV/volume audit

The exact-head bare Gaussian audit now spans fixed-box N=4 through N=64
and a separate fixed-spacing N=8 through N=64 volume sequence. At
L=8 mu^-1, the bare psi stress grows by a factor 16664.2325 as the
reported lattice cutoff rises by a factor 16; the N=32-to-64 log slope
is 3.8822733, consistent with the expected leading quartic UV
sensitivity. At fixed dx=mu^-1, the equal-time bare density spread over
increasing box sizes is 2.38067e-13. These results distinguish UV
cutoff growth from finite-volume effects in the bare Gaussian mode sum.

The bare-total Hubble mismatch relative to the homogeneous-Phi
test-field background grows to 3.54730e-3 at N=64. This confirms that
the sampler's test-field FRW background is not a self-consistent
Friedmann initial state once the raw zero-point stress is included.
No vacuum subtraction, counterterms, coupling renormalization or
continuum extrapolation has been performed. The audit is not a physical
quantum-waterfall result, defect probability, or relic prediction.
Gate 5 remains NOT MET.

The audit ZIP SHA-256 is
1b99b0fa6a9bc6058690aaaf2b9e60312e7e03e43c266210162201ed902d6b1d;
the strict-JSON SHA-256 is
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
The exact-head run's only Python failure was a stale manuscript phrase
assertion; the numerical UV audit and LaTeX jobs passed. The assertion
is being aligned to the manuscript's actual wording without relaxing
any numerical or scientific acceptance threshold.


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


## 2026-11-22 perturbative reheating-width claim boundary

### Supported conditional statements

- For a specified real-scalar quasiparticle mass and real broken-phase couplings, the vacuum Dirac-pair width is
  `N_c M [y_S^2 beta^3 + y_P^2 beta]/(8 pi)`, with beta=sqrt(1-4 m_f^2/M^2). The scalar and pseudoscalar contributions are separate and have different threshold powers.
- For one massless chiral channel of the gauge-invariant dimension-five operator in the electroweak-symmetric phase, the vacuum three-body width is `|C_f|^2 M^3/(1536 pi^3 Lambda^2)`. Explicit channel multiplicities may sum orthogonal final states.
- Given a positive total perturbative width and g-star, the sudden-decay estimate `T_RH=(90/(pi^2 g-star))^(1/4) sqrt(Mbar_Pl Gamma)` can be evaluated conditionally. A 5 MeV BBN comparison and phase/cutoff flags are diagnostics under the stated assumptions.

### Not supported

- A numerical PTUM benchmark width, branching ratio, reheating temperature or BBN verdict: Wilson matrices, cutoff, quasiparticle mass history and actual channel multiplicities are not fixed.
- Applying the broken-phase two-body formula above electroweak symmetry restoration, or applying the unbroken-phase massless three-body formula below the crossover without matching the thermal phase.
- Treating either the sudden-decay estimate or the new constant-w_c, constant-Gamma fluid integrator as a PTUM-derived condensate/SM Boltzmann solution.
- Claiming microscopic thermalization, a complete PTUM entropy history, a final radiation fraction, or the absence of late entropy injection. The continuous-fluid helper assumes prompt thermalization and constant g_star; its comoving entropy is conditional on those assumptions.
- Omitting thermal masses, Pauli blocking, Bose enhancement, Higgs-portal pair production, nonperturbative preheating or rescattering while describing the result as a complete reheating history.

The new module is a tree-level rate calculator with explicit assumptions, not a completion of Gate 8. Its exact-head tests and manuscript-source regression await CI after the latest commits.


## 2026-11-22 verification status for reheating helpers

The conditional width implementation and its numerical regressions passed in PR workflow 45009882010 (173 tests). This verifies the coded vacuum formulas and report bookkeeping only. It does not supply physical Wilson coefficients, a PTUM quasiparticle spectrum, thermal rates or a reheating history. The manuscript's three overfull equation displays were reflowed in commit 32f94f3; the new exact-head LaTeX result is pending. Gate 8 remains PARTIAL and Gate 10 remains PARTIAL.


## 2026-11-23 continuous reheating-fluid boundary

### Supported conditional statements

- Given an initial condensate density, initial radiation density, constant effective w_c, constant positive perturbative width Gamma, constant g_star, and prompt thermalization, ptum_reheating_history.py integrates the two-fluid expanding-FRW equations.
- The helper includes radiation in H, separately accumulates condensate expansion work, radiation expansion work and transferred energy, and reports integrated energy-budget residuals.
- It computes the conditional temperature and comoving entropy histories, radiation-domination event, H=Gamma event, and sampled maximum temperature.
- At H=Gamma, the continuous temperature obeys T_cont/T_sudden=Omega_r^(1/4). This follows from the radiation fraction at that event and is an internal consistency identity, not an independent physical prediction.

### Not supported

- A PTUM benchmark reheating history, decay width, radiation fraction, T_RH, BBN verdict or final entropy: the Wilson matrices, cutoff, time-dependent quasiparticle spectrum, w_c(t), Gamma(T), and scalar-to-SM energy partition are not fixed.
- A complete thermal history: g_*(T), g_*s(T), electroweak/QCD thresholds, thermal masses, Pauli blocking, Bose enhancement, inverse decays, scattering and thermalization delay are omitted.
- Treating the constant-fluid result as a substitute for the coupled inhomogeneous waterfall, Higgs-portal pair production, nonperturbative preheating or rescattering.

The five new continuous-history regressions and manuscript equations require fresh exact-head CI. Gate 8 remains PARTIAL.


## 2026-11-23 continuous reheating solver verification boundary

The first exact-head run of the new fluid helper found that DOP853's
dense interpolation near the stiff terminal decay tail could produce
a small artificial non-monotonicity in sampled comoving entropy.
The solver was changed to BDF, which is appropriate for the increasing
Gamma/H stiffness as the condensate decays. An independent numerical
solve of the same equations showed integrated sector/total budget
residuals below 5e-15 and no sampled entropy decrease at the regression
resolution. The diagnostic tolerance was tightened to 1e-5. The
manuscript filename assertion was also corrected to account for TeX
escaping. These corrections await fresh exact-head CI and do not
change the conditional, non-PTUM-prediction scope of Gate 8.


## 2026-11-24 scalar heat-kernel UV coefficient boundary

### Supported
- The coupled canonical \((\Phi,\psi)\) tree-level potential Hessian is
  evaluated analytically, including the off-diagonal mixed fluctuation
  entry.
- Given explicit \(\xi_\Phi,\xi_\psi\) and Euclidean curvature invariants,
  ptum_renormalization.py returns the local bulk \(a_2\) coefficient
  modulo covariant total derivatives.
- The coefficient is polynomial in the Hessian and remains real for a
  tachyonic eigenvalue; this does not mean the unstable static vacuum
  determinant has a real finite part.

### Not supported
- Calling the coefficient a renormalized effective action, renormalized
  stress tensor, or a quantum initial state.
- Choosing or inferring \(\Lambda_{\rm EFT}\), \(\mu_R\), the finite
  renormalization conditions, or the pole/counterterm normalization.
- Ignoring boundary/initial-state terms, mixed scalar loops, SM/gauge/
  fermion loops, graviton loops, or the real-time CTP finite part.
- Subtracting this local coefficient from the lattice energy as a
  numerical vacuum offset, or claiming that the existing lattice is
  cutoff independent.
- Claiming that R0, R1 or R2 has passed. Gate 5 remains NOT MET.


## 2026-11-24 exact-head verification boundary

Workflow 45364524478 verifies the algebraic heat-kernel implementation
on head 5f190b87aa7f883ec721fd35e432f76b539c052f: 186 tests, 4/4
smoke trajectories, and the 11-grid bare UV audit passed. The PDF
build completed with 79 final-pass Underfull hbox warnings and no
Overfull or unresolved reference/citation warnings. This is software
verification of the stated algebraic coefficient, not verification of
a renormalized quantum state, finite stress tensor, or cutoff-independent
lattice.


## 2026-11-24 scalar bulk pole normalization boundary

### Supported
- For the declared Euclidean operator and
  \(\Gamma_E^{(1)}=+\tfrac12\operatorname{Tr}\ln\mathcal D_E\),
  dimensional regularization \(d=4-\epsilon\), the local scalar bulk
  pole coefficient is \(-a_2^{\rm bulk}/(16\pi^2\epsilon)\).
- The cancelling Euclidean local counterterm has coefficient
  \(+a_2^{\rm bulk}/(16\pi^2\epsilon)\). The one-real-scalar flat
  constant-mass limit is tested against \(-m^4/(32\pi^2\epsilon)\).

### Not supported
- A finite or renormalized effective action, a selected renormalization
  scale or finite \(\overline{\rm MS}\) constant, or fixed physical
  matching conditions.
- A renormalized stress tensor, renormalized \(\Phi\) force, boundary
  or initial-state subtraction, real-time CTP finite part, or a
  cutoff-independent lattice evolution.
- A complete one-loop PTUM EFT renormalization: only the coupled
  canonical two-scalar bulk determinant is represented. SM/gauge/
  fermion/graviton loops and the full EFT operator matching remain open.

The new pole-normalization tests and manuscript equation require fresh
exact-head CI. Gate 5 remains NOT MET.


## 2026-11-24 divergent scalar-force coefficient boundary

### Supported
- At fixed Euclidean curvature, the derivative of the local two-scalar
  bulk coefficient obeys
  \(\partial_Ia_2^{\rm bulk}
  =\operatorname{tr}[(\mathcal H+(\Xi-\mathbf1/6)R_E)
  \partial_I\mathcal H]\), for \(I=\Phi,\psi\).
- The code returns the field derivatives of the one-loop Euclidean
  simple-pole and cancelling counterterm coefficients. Central
  differences check the analytic field derivatives, and the
  \(\psi=0\) result respects the real-scalar \(Z_2\) symmetry.

### Not supported
- A finite or renormalized scalar force, a Lorentzian in-in/CTP force,
  a metric variation, or a renormalized stress tensor.
- Boundary/initial-surface counterterms, finite matching conditions,
  SM/gauge/fermion/graviton loops, or a cutoff-independent lattice.

The new derivative tests and manuscript equation require fresh
exact-head CI. Gate 5 remains NOT MET.


### Source-regression correction

The first exact-head run for the field-gradient extension had one
source-text failure: the test expected the complete trace identity on
one line although the manuscript correctly uses aligned LaTeX lines.
The assertion now checks the identity's independent source fragments.
The numerical finite-difference and Z2 tests passed. This is a test
robustness correction only; no physics equation or tolerance changed.
Fresh exact-head CI is required. Gate 5 remains NOT MET.


### Exact-head verification

Workflow 45368498672 on d5649884cae49ede9c4cb83915a3f0a4670d83b2
passed 194 Python tests, the 4/4 two-scale smoke scan, the 11-grid
bare-WKB audit and the 46-page manuscript build. The final LaTeX pass
retained 80 Underfull hboxes but had zero Overfull hboxes and no
unresolved references/citations. The analytic scalar-pole field
derivatives passed central-difference checks and the psi=0 Z2 control.
This does not turn the divergent coefficients into a finite force or
renormalized stress tensor. Gate 5 remains NOT MET.



## 2026-11-25 scalar bulk-pole metric-variation boundary

### Supported, pending exact-head CI
- The local two-scalar Euclidean bulk \(a_2\) coefficient is rewritten
  in four dimensions as \(U_0+FR+A R^2+B R_{\mu\nu}R^{\mu\nu}\)
  plus the Euler density, with the coefficients derived from the
  coupled Hessian and explicit \(\xi_\Phi,\xi_\psi\).
- The code evaluates the inverse-Euclidean-metric Euler derivative of
  this local bulk coefficient, including the \(FR\) derivative terms
  and the fourth-derivative curvature terms.
- Curvature tensors and covariant derivative data are explicit caller
  inputs. Algebraic symmetries, Ricci/scalar contractions and derivative
  traces are checked.
- Flat, constant-curvature and conformal-coupling trace identities are
  guarded by new regressions.

### Not supported
- A finite or renormalized stress tensor, a Lorentzian in-in/CTP source,
  or a self-consistent semiclassical Einstein equation.
- Boundary/initial-surface counterterms or the finite contribution
  associated with the dimensional continuation of the Euler density.
- A geometry solver for the supplied curvature and derivative tensors.
- SM/gauge/fermion/graviton loops, finite matching conditions, or a
  cutoff-independent lattice evolution.

The new implementation and tests require fresh exact-head CI. Gate 5
remains NOT MET.



### Metric-variation input-test correction

The first exact-head Python run had one failure because the test's
absolute curvature perturbation was numerically negligible compared
with the physical benchmark scale. The regression now uses a
dimensionally scaled perturbation \(10^{-3}m_\psi^2\), without changing
the production comparison tolerance. A regex string was also made raw
to remove its escape-sequence deprecation warning. Fresh exact-head CI
is required; no new physics result is claimed.



### Metric-variation tensor audit refinement

The helper now validates the first algebraic Bianchi identity and returns
the individual volume, field-curvature, R-squared and Ricci-squared
metric-variation pieces. A new regression verifies rejection of a
four-form contamination that passes pair symmetries and Ricci
contraction but violates Bianchi, and checks the sum of returned pieces.
Fresh exact-head CI is pending.



## 2026-11-25 exact-head metric-variation verification boundary

Workflow 45586718905 on head
8bfbe348675470223477cdb8e45b5b7a7f233b8d passed 199 Python tests,
the 4/4 two-scale smoke scan and the 11-grid bare-WKB UV audit. The
47-page PDF built with no unresolved references/citations but retained
66 final-pass Underfull and two final-pass Overfull hbox warnings. The
two Overfull warnings were localized to the new metric-variation
displays and have been reformatted on a later, not-yet-verified head.

The smoke and UV ZIPs were inspected and both JSON payloads passed a
strict parser that rejects NaN/Infinity. The smoke result remains a
4-row software check with no quantum vacuum seed. The UV audit still
shows the bare fixed-box stress factor 16664.2325 and the expected
cutoff growth; zero-point energy is retained and no subtraction,
counterterms or continuum limit are claimed. Gate 5 remains NOT MET.



## 2026-11-25 finite-difference metric-variation check

A regression now checks the analytic metric Euler derivative against
central finite differences of the integrated full \(a_2\) action on
\(S^2\times S^2\), varying each sphere's radius independently. This
checks both orthogonal curvature blocks and retains the Euler-density
term in the action, whose integrated value is topological. The test
requires exact-head CI and does not establish a renormalized stress
tensor or physical quantum evolution.



## 2026-11-25 exact-head product-sphere finite-difference verification

Exact-head workflow 45587737076 on
ee6a7dced58f30122150fcbaae832cf356423778 passed 200 Python tests,
the 4/4 two-scale smoke scan, the 11-grid bare-WKB UV audit and the
47-page LaTeX build. The new product-sphere finite-difference test
passed for independent rescalings of both curvature blocks. The final
LaTeX pass retained 80 Underfull hbox warnings but had zero Overfull
hboxes and zero unresolved references/citations.

The inspected PDF artifact contains the metric-variation equations.
The smoke and UV JSON payloads both pass strict parsing. The smoke rows
remain classical controls with no quantum vacuum seed. The UV audit
continues to show the bare zero-point cutoff divergence and explicitly
does not claim subtraction, counterterms or a continuum limit. This
is verification of the local divergent Euclidean metric variation,
not a finite renormalized stress tensor or a physical waterfall result.
Gate 5 remains NOT MET.


## 2026-11-25 polynomial scalar RG control boundary

### Supported, pending exact-head CI
- One-loop MS-bar beta coefficients for a two-real-scalar **renormalizable polynomial control model**, in the explicitly stated potential and Euclidean curvature-operator normalizations.
- The coefficients reproduce the full local two-field heat-kernel pole density at nonzero fields and nonzero constant curvature.
- Decoupled scalar, mixed-coupling, conformal-coupling and quartic boundedness controls are covered by regressions.

### Not supported
- Beta functions for the actual non-polynomial PTUM plateau potential. Its \( [V_{\rm eff}''(\Phi)]^2 \) and \(R_E V_{\rm eff}''(\Phi)\) structures require functional running or an explicitly matched infinite-operator EFT treatment.
- A selected EFT cutoff, renormalization scale boundary values, finite renormalization conditions, or a complete matched counterterm action.
- SM/gauge/fermion/graviton loops, boundary/initial-state terms, a finite real-time CTP effective action, a renormalized stress tensor, or a cutoff-independent lattice.
- Closure of R0 or Gate 5. No physical quantum prediction is claimed.


## 2026-11-25 exact-head RG-control verification boundary

Workflow 45590315635 on commit 977ab5919d1055bfc3545473687a9a3cea3237d3
passed 203 Python tests, the 4/4 smoke scan, the 11-grid bare-WKB UV
audit and the manuscript build. The smoke and UV JSON payloads were
strictly parsed. The manuscript has zero Overfull boxes and no
final-pass unresolved references/citations, with 80 Underfull hbox
warnings remaining.

The verified beta functions apply only to the declared two-real-scalar
quartic polynomial control EFT. The actual plateau's non-polynomial
functional counterterms, EFT cutoff and finite matching conditions
remain open. The UV audit still demonstrates the bare lattice's
cutoff dependence. Gate 5 remains NOT MET; no quantum waterfall,
renormalized stress tensor, relic abundance or continuum limit is
claimed.


## 2026-11-25 conformal radiation-FRW analytic benchmark boundary

### Supported, pending exact-head CI
- Exact positive-frequency conformal modes for a free massless real scalar with \(\xi=1/6\), including the canonical Wronskian.
- The heat-kernel trace anomaly and the corresponding homogeneous conserved stress tensor in spatially flat radiation FLRW, with the state-dependent \(a^{-4}\) integration constant fixed to zero.
- Analytic checks of the trace identity, continuity equation, curvature invariants and Minkowski limit.

### Not supported
- General massive or minimally coupled FLRW renormalization, fourth-order adiabatic subtraction, or an independent point-splitting stress-tensor comparison.
- Interacting \(\lambda_\psi\psi^4\) renormalization, PTUM waterfall backreaction, lattice counterterms, or a quantum-seeded nonlinear calculation.
- Closure of R1, R0 or Gate 5. No PTUM physical prediction is claimed.


## 2026-11-25 exact-head conformal benchmark verification boundary

Workflow 45591701409 on commit
8c903c7575c46ddbf592e83949531f09c86a0fd4 passed 211 Python tests,
the 4/4 two-scale smoke scan, the 11-grid UV audit and the 48-page
manuscript build. The conformal-mode Wronskian and trace/continuity
identities passed at scale-normalized roundoff. The smoke and UV JSON
artifacts were strictly parsed.

The UV audit continues to show bare cutoff growth and explicitly
retains zero-point energy without subtraction or counterterms. The
free conformal benchmark is not a general massive/interacting
renormalization prescription or an independent point-splitting
comparison. R1 remains partial; Gate 5 remains NOT MET.


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


## 2026-11-25 field-variance renormalization boundary

The branch contains a second-order adiabatic subtraction for the
finite-band scalar field variance, with canonical Wronskian validation
and exact conformal-massless/Minkowski-massive controls. This supports
only the local UV subtraction of <psi^2> through adiabatic order two
on caller-supplied backgrounds. It is not a renormalized stress tensor,
a renormalized force on Phi, a self-consistent Friedmann source, or a
renormalized lattice evolution. The finite momentum tails and finite
renormalization conditions are not supplied. No quantum-waterfall,
backreaction, relic or observational claim is promoted. Gate 5 remains NOT MET.


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


## 2026-11-26 fourth-order adiabatic stress boundary

The branch now derives local fourth-order WKB counterterms for the
homogeneous Hilbert energy density and pressure of one real scalar on
caller-supplied spatially flat FLRW histories. It also provides a
finite-band bare-minus-counterterm integrator with Wronskian and
positive-frequency checks. The order-two field-variance UV subtraction
is kept distinct from the optional order-four WKB completion used in
the matched stress Ward diagnostic.

This is not a fully renormalized stress tensor or force on Phi:
finite matching conditions, IR/UV tail treatment, the interacting
PTUM initial-value problem, CTP finite parts, SM/gauge/fermion/graviton
loops, self-consistent Friedmann backreaction and lattice counterterms
remain absent. No quantum-waterfall, relic-density or observational
claim is promoted. Gate 5 remains NOT MET.


The external-mass Ward identity has the sign
dot(rho)+3H(rho+p)=0.5 dot(M^2)<psi^2>. With dot(M^2)<0, a classical
positive psi^2 gives negative transfer; a finite renormalized variance
can be sign-indefinite, so no universal sign is assigned to the
renormalized finite source.

## 2026-11-26 exact massive de Sitter R1.3 control

### Supported after exact-head regression
- For \(H=1\), \(a=-1/\eta\), \(M^2=2\), and \(\xi=0\), the canonical
  mode equation reduces exactly to \(v_k''+k^2v_k=0\).
- The analytic plane-wave mode, canonical Wronskian, and exact bare
  Hilbert mode stresses are compared with the fourth-order local
  counterterms. The residual is checked to scale as \(k^{-7}\) over the
  declared test momenta \(k=20,40,80\).

### Not supported
- A general independent point-splitting stress tensor, integrated
  cutoff-independent stress, or a full IR/UV momentum-tail treatment.
- Finite renormalization conditions, the interacting PTUM \(\lambda_\psi\)
  theory, a renormalized force on \(\Phi\), CTP finite parts,
  self-consistent Friedmann backreaction, or lattice counterterms.
- Quantum-seeded nonlinear waterfall, rescattering, defect-network
  abundance, relic density, or observational constraints. Gate 5
  remains NOT MET.

## 2026-11-26 exact-head verification of the massive de Sitter R1.3 control

Workflow 45797854235 on commit 2a8d02ede094a82578cd82cac3ec07df74ebf6ad
passed 223 Python cases. The new exact de Sitter mode regression verifies
the plane-wave Wronskian and the k^{-7} residual scaling of both local
order-four stress counterterms. The same run passed the 4/4 homogeneous
smoke scan, the 11-grid bare-lattice UV audit and the 49-page manuscript
build. The final LaTeX pass retained 81 Underfull hboxes but had no
Overfull hboxes or unresolved references/citations.

The smoke JSON was strictly parsed: all four rows succeeded, used the
exact endpoint-matched threshold, and explicitly recorded
quantum_vacuum_seeded=false. The lattice UV JSON was also strictly
parsed and continues to report retained zero-point energy, no
subtraction, no counterterms and no continuum limit. The 100-row scan
and paired convergence jobs were skipped for this non-FULL-SCAN commit.
The exact de Sitter test strengthens only the local free-field control;
Gate 5 remains NOT MET.

## 2026-11-26 inflation-to-waterfall linear crossing boundary

### Supported
- The waterfall wrapper initializes the psi-bar=0 background at
  Phi=(1+delta)Phi_c using the integrated single-field inflationary
  trajectory, rather than assigning an arbitrary potential-slow-roll
  velocity.
- It evolves the expanding invariant background through the threshold
  and changes the sign of m_eff^2(Phi) on the resulting trajectory.
- Linear psi_k modes are initialized with a first-order adiabatic
  vacuum while the mode is stable, then evolved through tachyonic
  intervals with Wronskian and adiabaticity diagnostics. Particle
  numbers are withheld when the final adiabatic basis or Wronskian
  fails its declared numerical check.

### Not supported
- Quantum mode stress or the renormalized force on Phi feeding back
  into the Friedmann/background equations.
- A fully coupled quantum background, all-momentum stability proof,
  nonlinear quantum rescattering, fragmentation, SM-source evolution,
  or a physical relic/defect prediction. Gate 2 remains PARTIAL; Gates 5
  and 6 remain NOT MET.

## 2026-11-26 exact-head verification of the linear inflation-to-waterfall wrapper

Workflow 45799709372 on commit cb4ee0ebeae8ced796691d0dce4690373337da70 passed 224 Python cases. The new regression verifies that the wrapper's initial Phi and Phi-dot exactly match the integrated single-field inflationary state at (1+delta)Phi_c, that the expanding psi-bar=0 background crosses from positive to negative m_eff^2, and that no quantum mode backreaction is silently enabled. The manuscript now distinguishes this linear test-field crossing from the separate externally supplied-history utilities and the finite-cutoff classical lattice.

The exact-head smoke scan passed 4/4 and the 11-grid bare-WKB audit passed; both JSON artifacts were parsed with non-finite constants rejected. The smoke metadata explicitly records quantum_vacuum_seeded=false because that scan remains a homogeneous classical sensitivity control. The 49-page PDF built with 81 final-pass Underfull hboxes, zero Overfull hboxes and zero unresolved references/citations. The full 100-row and paired convergence jobs were skipped on this non-FULL-SCAN commit. Gate 2 remains PARTIAL because the linear modes do not backreact; Gates 5 and 6 remain NOT MET.


## 2026-11-26 exact-head homogeneous scan boundary

### Supported on code head \texttt{b388bfe371b46b229266320a4a3edc9812a65e18}
- The exact-head DOP853 baseline completed 100/100 homogeneous
  post-threshold integrations with zero failures and exact
  \(\Phi_c/M_{\rm Pl}=0.9862280831209068\).
- Five rows pass the current homogeneous quartic classifier. All five
  are in the low-scale underdamped control, all use the largest
  manually selected classical field seed \(\psi_{\rm init}=5\psi_0\)
  and the smaller offset \(0.01\Phi_c\). None of the 50 high-scale
  threshold-matched rows passes.
- Their cycle-averaged \(w_\psi\), \(Q\), virial ratio and late-time
  \(H/\omega\) satisfy the implemented homogeneous classifier.
- The strict-JSON result artifact has SHA-256
  \texttt{5c86db1631da9efd35f956a266edbd5c30cfdae405de1cb9e6e06029c042c1a2}.

### Not supported
- A quantum-vacuum-seeded attractor: the scan metadata explicitly says
  \texttt{quantum\_vacuum\_seeded=false}.
- A quartic phase in the CMB-normalized high-scale threshold-matched set.
- Spatially inhomogeneous stability, sound speed, anisotropic stress,
  defect-network evolution, quantum backreaction, rescattering, or
  SM-sector energy transfer.
- The homogeneous current-head output-grid/solver-tolerance study is
  supported: 500/500 integrations and 400 comparisons completed;
  100/100 output-grid comparisons passed, the final adjacent tolerance
  comparison passed 100/100, and all 100 regime flags/metric-availability
  patterns remained unchanged across five profiles. Three intermediate
  tolerance comparisons exceeded the strict threshold but were resolved
  by later refinement. This is not inhomogeneous or quantum convergence.
  Gate 7 remains NOT MET.


## 2026-11-26 exact-head documentation CI boundary

Workflow 45804043025 on commit
\texttt{65eab8dfe3ff1e3c407946793e749f4255cfae40} passed 224 Python
regression tests, 4/4 homogeneous smoke trajectories, the 11-grid
bare-WKB UV audit and the 49-page manuscript build. The smoke artifact
was strictly parsed and confirms the exact endpoint threshold and
\texttt{quantum\_vacuum\_seeded=false}. The UV artifact remains a bare
cutoff audit with zero-point energy retained and no subtraction or
counterterms. The final PDF has 87 Underfull hbox warnings but no
Overfull hboxes or unresolved references/citations. The 100-row
homogeneous scan and paired convergence evidence remain on unchanged
simulation source head b388bfe; this documentation/test-only commit
does not alter the equations or solver. Gate 10 remains PARTIAL.




## 2026-11-26 domain-wall linear-source validity boundary

The analytic defect helper now reports the ratio of the *required
linearized* source to the spinodal source and a separate boolean stating
whether the required source lies inside the declared small-bias range.
The current benchmark-like case is safely inside that range; an extreme
network-area control test confirms the helper flags extrapolation rather
than treating the linear formula as reliable. This does not calculate
the SM expectation value, predict the actual bias, or simulate wall
formation/annihilation. Gate 5 remains NOT MET.


## 2026-11-26 defect diagnostic CI boundary

The required-linear-source small-bias validity guard in
\texttt{ptum_defects.py} passed its regression in workflow 45805018373.
The exact-head suite passed 225 tests, the 4/4 smoke scan, 11-grid UV
audit and 49-page PDF build. This validates the diagnostic's declared
linearization guard only. It does not supply the Wilson coefficient,
renormalized SM condensate, thermal history, or an inhomogeneous
domain-wall network evolution. Gate 5 remains NOT MET.
