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

