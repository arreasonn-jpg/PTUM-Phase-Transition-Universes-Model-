# PTUM Claim Boundary and Verification Status

**Snapshot:** 2026-11-13  
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

The latest observed scan attempt was cancelled when a newer commit superseded its workflow run. No complete 100-row artifact has been validated. No regime conclusion from the revised 100-point scan is currently claimed.

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

Likewise, (w=1/3,c_s^2=1/3,\sigma=0) is not a demonstrated microscopic attractor. It remains a conditional phenomenological closure until field-level perturbations, sound speed, anisotropic stress, and stability are derived and converged.

## 8. Reproducibility and current CI boundary

The latest branch contains **51 regression tests**, including scalar/action checks, FRW diagnostics, frozen Floquet tests, expanding-mode vacuum and Wronskian checks, FRW history consistency, intermediate tachyonic evolution, and finite-band momentum-grid validation.

The latest previously completed workflow run (43400134268) passed its 43-test Python regression step but failed the LaTeX job because `mathrsfs` was not loaded for `\mathscr D_\mu`. The package was added, the on-shell SM tensor double-counting issue was corrected, and further mode tests were added. A new workflow run (43405427845) has been triggered for the latest branch; at the time of this snapshot it is pending, so the 51-test suite, 100-trajectory scan, and corrected LaTeX build are **not yet claimed as passing**.

The tracked `main.pdf` is an older library artifact and is not the current compiled manuscript. Fresh PDF and scan outputs must come from the CI artifacts. Generated LaTeX auxiliary files and stale scan summaries are excluded from the correction branch.

The historical repository URL `https://github.com/ErdemEsa/ptum-cosmology.git` returned HTTP 404 during the 2026-11-13 API review. The current repository does not expose the CLASS patch as an individually reviewable tracked source file, and the archive contents have not been verified. Public availability and apply-check success for that patch are therefore **UNVERIFIED**. See `PTUM_REPRODUCIBILITY_NOTES.md`.

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
