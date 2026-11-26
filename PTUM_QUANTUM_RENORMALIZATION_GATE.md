# PTUM Quantum Waterfall Renormalization Gate

**Status:** BLOCKING REQUIREMENT. This document is a derivation and acceptance plan, not a claim that the quantum waterfall has been renormalized or simulated.

**Reference model:** metric signature `(-+++)`, real (Z_2) waterfall field (psi), and
[
m_{\rm eff}^{2}(\Phi)
=m_\psi^{2}\left(\frac{\alpha\Phi^{2}}{E_{\rm th}^{2}}-1\right),
\qquad
\Phi_c=\frac{E_{\rm th}}{\sqrt{\alpha}}.
]
The mass is positive above the threshold and tachyonic below it. The sign convention and threshold matching are not changed by this renormalization plan.

## 1. Why the present bare-WKB lattice cannot be promoted to a quantum prediction

The exact-head fixed-box audit on commit `150487cf9f92684b2120310948e8a9d050f4f13d` (workflow [45152898999](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45152898999), artifact [14807855439](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45152898999/artifacts/14807855439)) found:

- At fixed (L=8\,\mu^{-1}), the bare (psi)-stress increases monotonically by a factor (16664.2325) over (N=4,6,8,10,12,16,20,24,32,48,64).
- The (N=32\to64) log-log slope against the lattice UV cutoff is (3.8822733), consistent with the leading (Lambda^4) zero-point divergence in three spatial dimensions.
- At fixed (Delta x=\mu^{-1}), the density spread as the box grows from (8) to (64\,\mu^{-1}) is (2.38067\times10^{-13}). This is a finite-volume check at fixed spacing, not a continuum-limit result.
- At (N=64), (ho_{\psi,\rm bare}/\rho_\Phi=7.1072\times10^{-3}), and the bare-total Hubble mismatch is (3.5473\times10^{-3}).
- The artifact explicitly reports zero-point energy retained, no vacuum subtraction, no counterterms and no continuum limit.

Therefore the existing Gaussian initializer is a **bare first-order adiabatic-WKB classical-statistical sample**. Its metadata is accurate. It is not yet a renormalized quantum initial state, and the subsequent nonlinear lattice evolution is cutoff dependent.

## 2. The renormalization problem is interacting and curved-spacetime, not merely a vacuum offset

The fluctuation operator about the homogeneous (psi=0) background has the schematic form
[
\mathcal D_\psi
=-\Box + m_{\rm eff}^{2}(\Phi)+\xi_\psi R
+\text{interaction/self-energy terms}.
]
A one-loop in-in calculation begins from a closed-time-path effective action, schematically
[
\Gamma^{(1)}_\psi
=\frac{i}{2}\operatorname{Tr}_{\rm CTP}\log\mathcal D_\psi.
]
The (Phi)-dependent mass means that the divergent and finite terms feed back into the (Phi) equation as well as the (psi) stress tensor.

A consistent counterterm basis must be derived from the same action and must include, as applicable to the chosen EFT truncation:

1. Waterfall-sector mass and quartic renormalization, (delta m_\psi^2) and (delta\lambda_\psi).
2. The mixed (Phi^2\psi^2) coupling and the induced (Phi)-potential terms. Since (m_{\rm eff}^2(\Phi)) is field dependent, the one-loop determinant generates terms proportional to (m_{\rm eff}^4(\Phi)), which contain constant, (Phi^2), and (Phi^4) pieces.
3. Curvature couplings for both scalar fields, `R\psi^2` and `R\Phi^2`, with renormalized \(\xi_\psi(\mu_R)\) and \(\xi_\Phi(\mu_R)\). The one-loop divergence proportional to \(M_\psi^2(\Phi)R\) contains an \(R\Phi^2\) term because the waterfall mass depends on \(\Phi\). Minimal classical values can be imposed as renormalization conditions at a specified scale; they must not be silently assumed to remain zero under quantum renormalization.
4. Gravitational counterterms for the cosmological constant, the Einstein term, and curvature-squared operators such as (R^2) and (R_{\mu\nu}R^{\mu\nu}).
5. The derivative operators required by the chosen EFT truncation when the background-dependent mass varies in spacetime.

The plateau potential (V_{\rm eff}(\Phi)=V_0[1-e^{-\lambda_\Phi\Phi^2/M_{\rm Pl}^2}]) is not a closed renormalizable polynomial under quantum corrections. PTUM must therefore be treated as an EFT with an explicit cutoff and matching conditions for the retained Wilson coefficients. A renormalization prescription cannot be completed while the cutoff and these finite conditions are unspecified.

## 3. Do not apply a naive fourth-order subtraction to the interacting model

Fourth-order adiabatic subtraction is a standard tool for the stress tensor of a **free** scalar in FLRW. It is not automatically a complete action-level prescription for an interacting (\lambda\psi^4) theory with a field-dependent mass.

Markkanen and Tranberg derive an action-consistent one-loop renormalization procedure for a self-interacting scalar in FRW and explicitly find that, once interactions are included, naive adiabatic subtraction can introduce finite terms that cannot be obtained merely by redefining the constants of the classical action. Their analysis motivates deriving counterterms from the action and fixing finite parts with explicit renormalization conditions rather than subtracting a convenient WKB expression by itself: [arXiv:1303.0180](https://arxiv.org/abs/1303.0180).

Physical-scale adiabatic regularization is a relevant comparison for **free** cosmological scalar modes. It was developed to remove UV divergences while reducing infrared distortions in light-field examples, but it does not by itself solve the interacting PTUM waterfall: [Phys. Rev. D 109, 045015 (2024)](https://doi.org/10.1103/PhysRevD.109.045015).

The static one-loop effective potential is also insufficient across the waterfall. When (m_{\rm eff}^2<0), its logarithm develops an imaginary part, signalling instability of the chosen background rather than supplying a real-time nonlinear evolution. The transition must be treated with a real-time in-in framework.

## 4. Required implementation sequence

### R0. Fix the renormalized EFT definition

- State the EFT cutoff (\Lambda_{\rm EFT}) and the operator truncation.
- Choose a stable reference background for the renormalization conditions. A convenient reference point to evaluate is (\Phi_{\rm ref}=\sqrt{2}\,\Phi_c), where the tree-level waterfall mass equals (m_\psi^2); this is a proposed reference point, not an already adopted parameter choice.
- Fix (m_\psi(\mu_R)), (\lambda_\psi(\mu_R)), the mixed coupling, (\xi_\psi(\mu_R)), the (Phi)-potential coefficients and the gravitational finite parts.
- Derive the counterterms from one common action and verify that the renormalized sector currents still sum to zero.

### R1. Free-field curved-FRW renormalization oracle

Before nonlinear evolution, implement the free test-field limit and compare two independently derived stress-tensor prescriptions where their domains overlap.

Required controls:
- Minkowski stable vacuum with the declared finite renormalization condition.
- A known expanding-FRW free-field benchmark.
- Wronskian preservation and positive-frequency initialization in the stable phase.
- Separate UV-cutoff, volume, time-step and arithmetic-precision convergence.
- Renormalized continuity (\dot\rho_\psi+3H(\rho_\psi+p_\psi)=0) within a measured error budget.
- No subtraction that removes the amplified infrared tachyonic modes.

### R2. Interacting one-loop backreaction

- Derive the (Phi)-dependent self-energy and renormalized (\langle\psi^2\rangle), (\rho_\psi), and (p_\psi) from the same in-in approximation.
- Include the corresponding force in the (Phi) equation and the renormalized stress in the Friedmann constraint.
- Demonstrate conservation of the combined (Phi+psi) system, not just finiteness of one density integral.
- Verify that the renormalized initial Friedmann constraint closes as the cutoff is varied.

### R3. Nonlinear evolution and defect network

Only after R0-R2 pass:
- evolve the nonlinear real-(Z_2) field with the matched lattice counterterms;
- separate highly occupied classical IR modes from UV vacuum modes instead of treating every half-quantum UV mode as a classical degree of freedom;
- demonstrate lattice-spacing, volume, time-step and ensemble convergence;
- measure domain-wall area density and its scaling independently of the analytic (A\)-factor estimate;
- test whether any thermal or explicit bias is present in the action before claiming domain-wall removal.

## 5. Acceptance rule

The quantum waterfall gate remains **NOT MET** until the renormalized stress tensor, renormalized force on (Phi), initial Friedmann constraint, combined conservation law, and cutoff/volume/time-step convergence all pass. A finite plot, a Wronskian check, a first-order WKB sample, or subtraction of the leading (\Lambda^4) term alone is not sufficient.

Until then:
- retain the current classical lattice as a finite-cutoff prototype;
- keep `vacuum_renormalized=false` and `vacuum_subtraction_applied=false` in its metadata;
- do not report quantum-seeded waterfall production, a physical wall-network abundance, reheating yield, or relic abundance from it.

## References

- T. Markkanen and A. Tranberg, “A Simple Method for One-Loop Renormalization in Curved Space-Time,” arXiv:1303.0180 (2013), [https://arxiv.org/abs/1303.0180](https://arxiv.org/abs/1303.0180).
- A. Ferreiro, S. Monin and F. Torrenti, “Physical scale adiabatic regularization in cosmological spacetimes,” *Phys. Rev. D* **109**, 045015 (2024), [https://doi.org/10.1103/PhysRevD.109.045015](https://doi.org/10.1103/PhysRevD.109.045015).


## 2026-11-24 scalar-sector heat-kernel UV coefficient (R0 partial)

The branch now derives the coupled two-real-scalar Hessian of the common
PTUM potential and evaluates its local four-dimensional Gaussian
one-loop heat-kernel coefficient a_2 modulo covariant total derivatives:
\[
a_2^{\rm bulk}=
\frac12\operatorname{tr}\left[
\left(\mathcal H+(\Xi-\tfrac16\mathbf1)R\right)^2
\right]
+\frac{2}{180}(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2).
\]
Here \(\mathcal H=V_{,IJ}\) includes the off-diagonal \(\Phi\)-\(\psi\)
mixing from the same tree-level potential, and
\(\Xi=\mathrm{diag}(\xi_\Phi,\xi_\psi)\) is explicit input. The code
does not silently set the quantum-renormalized curvature couplings or
their scale; tests use \(\xi_I=0\) only as the declared classical
minimal-coupling control.

ptum_renormalization.py reports the Hessian/curvature and geometric
pieces separately. The regression controls cover the flat constant-
Hessian limit, off-diagonal mixing, a conformal maximally symmetric
limit, explicit curvature-coupling dependence, and a tachyonic Hessian.
The coefficient remains real in the tachyonic region because the UV
heat-kernel coefficient is polynomial in the operator; no unstable
static logarithm or imaginary effective potential is evaluated.

**This is not renormalization.** The implementation does not choose
\(\Lambda_{\rm EFT}\), \(\mu_R\), finite matching conditions, the
dimensional-regularization pole normalization, boundary/initial-state
counterterms, SM/gauge/fermion or graviton loops, a CTP finite part,
a renormalized stress tensor, or the renormalized force on \(\Phi\).
The two-scalar Gaussian coefficient is an R0 algebraic check only.
Gate 5 remains **NOT MET**. The next required step is to fix the EFT
operator truncation and renormalization conditions, then derive and
match the complete counterterm action before implementing the R1
free-field oracle.


### R0.1 exact scalar operator-basis expansion

The two-field matrix coefficient is now expanded into independent local
pieces. With \(U=V_{\rm eff}''\), \(M^2=m_{\rm eff}^2(\Phi)\),
\(c=\alpha m_\psi^2/E_{\rm th}^2\), and
\(\delta\xi_I=\xi_I-1/6\):
\[
\begin{aligned}
a_2^{\rm bulk}
&=\tfrac12U^2+\tfrac12M^4
+\psi^2(cU+3\lambda_\psi M^2+4c^2\Phi^2)
+\tfrac12(c^2+9\lambda_\psi^2)\psi^4\\
&\quad+R(\delta\xi_\Phi U+\delta\xi_\psi M^2)
+R\psi^2(\delta\xi_\Phi c+3\delta\xi_\psi\lambda_\psi)\\
&\quad+\tfrac12R^2(\delta\xi_\Phi^2+\delta\xi_\psi^2)
+\tfrac{2}{180}(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2).
\end{aligned}
\]
The \(M^4\) term expands into \(1,\Phi^2,\Phi^4\), and
\(R M^2\) into \(R,R\Phi^2\). The independent \(U^2\) and \(RU\)
terms retain the non-polynomial plateau dependence. The new
ptum_scalar_heat_kernel_a2_decomposition helper expands the same
coefficient and checks it against the matrix trace; this is an
algebraic identity check, not an independent loop calculation.

The exact-head workflow 45364524478 on 5f190b87aa7f883ec721fd35e432f76b539c052f
completed successfully: 186 Python tests passed; the two-scale smoke
scan passed 4/4 with zero failed integrations; the 11-grid bare-WKB
UV audit passed and retained renormalized=false; the 46-page PDF built.
Its final LaTeX pass had 79 Underfull hbox warnings, zero Overfull
hboxes, and zero unresolved reference/citation warnings. Long scans
were skipped by design. Gate 5 remains NOT MET.


### R0.2 one-loop RG projection in a polynomial scalar control EFT

A separate two-real-scalar polynomial control model is now used to test
the map from the local pole residue to renormalization-group beta
functions. For
\[
V_{\rm poly}=\rho_{\rm vac}
+\tfrac12m_\Phi^2\Phi^2+\tfrac12m_\psi^2\psi^2
+\tfrac14\lambda_{\Phi,4}\Phi^4
+\tfrac14\lambda_\psi\psi^4
+\tfrac12c\Phi^2\psi^2,
\]
the code returns the one-loop MS-bar beta functions for the vacuum
energy, both masses, both quartics, the mixed coupling, both
non-minimal curvature couplings, the Einstein-curvature coefficient,
and the \(R^2\), Ricci-squared and Euler-density coefficients. The
curvature basis is reduced modulo the four-dimensional Euler density.
The quartic boundedness condition is checked before any coefficient is
returned.

Three regressions were added: reconstruction of the complete
\(a_2/(16\pi^2)\) residue from the beta coefficients at nonzero fields
and nonzero constant curvature; decoupled single-scalar and mixed
coupling limits, including the conformal \(\xi=1/6\) fixed point; and
fail-closed rejection of an unbounded quartic potential and invalid
scalar inputs.

This is an RG consistency oracle for the **polynomial control theory**,
not a beta-function solution for the non-polynomial PTUM plateau.
The plateau retains the functional counterterms
\([V_{\rm eff}''(\Phi)]^2\) and \(R_E V_{\rm eff}''(\Phi)\), so a finite
quartic truncation cannot be silently substituted. The code does not
select \(\Lambda_{\rm EFT}\), \(\mu_R\), renormalized boundary values or
finite matching conditions. It includes no SM/gauge/fermion/graviton
loops, boundary/initial-surface terms or real-time CTP finite part.
R0 remains partial, Gate 5 remains **NOT MET**, and no lattice vacuum
subtraction or physical quantum prediction is claimed.


## 2026-11-25 exact-head verification of the polynomial RG control

Workflow [45590315635](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45590315635) on exact code head 977ab5919d1055bfc3545473687a9a3cea3237d3 completed successfully:
- 203 Python regression cases passed, including the full pole-residue reconstruction, decoupled and mixed beta-function limits, conformal-coupling fixed point, and fail-closed quartic stability checks.
- The two-scale homogeneous smoke scan passed 4/4 with zero failed integrations. Its strict-JSON payload uses \(\Phi_c/M_{\rm Pl}=0.9862280831209068\), records quantum_vacuum_seeded=false, and has maximum chain-rule continuity residual \(3.3603\times10^{-12}\).
- The 11-grid bare-WKB UV audit passed and its JSON was parsed with non-finite constants rejected. The fixed-box bare stress grows by \(16664.2325\), the high-cutoff log slope is \(3.8822733\), and the fixed-spacing volume spread is \(2.38067\times10^{-13}\). Zero-point energy remains; subtraction and counterterms are false; no continuum limit is claimed.
- The 47-page LaTeX PDF built. The polynomial-control display was split after the preceding exact-head run showed an Overfull box. This run has zero Overfull boxes and no unresolved references/citations after the bibliography rerun. 80 Underfull hbox warnings remain.

The exact-head RG-control regressions and the manuscript equations are therefore verified. The polynomial model remains a control theory only. R0 is still incomplete because the plateau functional counterterms, EFT cutoff, renormalized boundary data, finite matching conditions, full loop content and boundary/initial-state terms remain unresolved. Gate 5 remains **NOT MET**.


### R1.1 exact conformal-scalar radiation-FRW benchmark

The branch now includes an exact analytic free-field control for one
massless real scalar with \(\xi=1/6\) on spatially flat radiation FLRW.
The conformal mode \(v_k=a\varphi_k\) is an exact plane wave with
Wronskian \(i\). The heat-kernel trace anomaly is obtained from
\(a_2^{\rm bulk}=(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2)/180\).
For \(a\propto t^{1/2}\), this gives
\(\langle T^\mu{}_\mu\rangle=H^4/(240\pi^2)\).
Homogeneous conservation and the trace identity, with the independent
state-dependent \(a^{-4}\) component set to zero, give
\(\rho=H^4/(960\pi^2)\) and \(p=H^4/(576\pi^2)\).

Regression tests check the exact mode equation and Wronskian, the
curvature invariants, the trace identity, continuity, the Minkowski
limit and invalid-input rejection. This is an analytic R1 benchmark,
not a general adiabatic-subtraction implementation and not a second
numerical stress-tensor prescription. Massive/minimally coupled modes,
independent point-splitting comparison, numerical UV/volume/time-step
convergence and a renormalized PTUM waterfall remain open. Gate 5
remains **NOT MET**.


## 2026-11-25 exact-head verification of the conformal radiation benchmark

Workflow [45591701409](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45591701409) on exact head 8c903c7575c46ddbf592e83949531f09c86a0fd4 completed successfully:
- 211 Python regression cases passed. The new tests cover exact conformal mode equation/Wronskian, the heat-kernel anomaly, trace and continuity Ward identities, the Minkowski limit and invalid-input rejection.
- The two-scale smoke scan passed 4/4 with zero failed integrations. Its strict-JSON payload uses \(\Phi_c/M_{\rm Pl}=0.9862280831209045\), records quantum_vacuum_seeded=false, and has maximum chain-rule continuity residual \(3.2166\times10^{-12}\).
- The 11-grid bare-WKB UV audit passed. Its strict-JSON payload retains the same cutoff-growth evidence: fixed-box bare-stress factor \(16664.2325\), high-cutoff log slope \(3.8822733\), and fixed-spacing volume spread \(2.38067\times10^{-13}\). Zero-point energy remains; subtraction and counterterms are false; no continuum limit is claimed.
- The 48-page LaTeX PDF built with zero Overfull boxes and no unresolved references/citations after the bibliography rerun. 80 Underfull hbox warnings remain.

The analytic conformal-scalar benchmark is verified as a free-field control only. It is not a general adiabatic subtraction, an independent point-splitting comparison, or a renormalization of the massive interacting PTUM waterfall. R1 remains partial and Gate 5 remains **NOT MET**.


## 2026-11-26 R1.3 fourth-order adiabatic stress-tensor control

The new ptum_adiabatic_stress.py module derives the order-four WKB
frequency and the corresponding Hilbert energy-density and isotropic
pressure counterterms for a real scalar with external time-dependent
mass and curvature coupling on a supplied spatially flat FLRW history.
The implementation uses conformal-time derivative jets through fourth
order, expands the nonlinear WKB equation consistently, and returns
both order-two and order-four field-variance completions. The standard
field-variance UV subtraction is still identified as order two; the
order-four variance is exposed separately for the matched WKB
energy-transfer identity.

The finite-band integrator checks the canonical Wronskian and requires
positive zeroth-order and full mode frequencies on the supplied band.
It returns bare, counterterm and subtracted finite-band rho, pressure
and variance, plus the external-mass source
(1/2) dot(M^2) <psi^2>. For M^2=m_eff^2(Phi), positive-Phi downward
motion has dot(M^2)<0. At the classical/bare level with psi^2>=0
this is negative transfer; a finite renormalized variance can be
sign-indefinite, so its finite source must be evaluated explicitly.

Six regressions cover exact conformal-massless and Minkowski-massive
limits, exact finite-band vacuum subtraction in both controls, independent
finite-difference checks of W2' and W2'', the matched order-four
external-mass Ward identity, and fail-closed Wronskian/frequency/jet
validation.

This closes only a local free-field adiabatic stress-counterterm
derivation/control. The integrals remain finite-band; no IR/UV tails,
finite renormalization conditions, finite CTP part, renormalized Phi
force, self-consistent Friedmann backreaction, SM/gauge/fermion/graviton
loops, or lattice counterterms are included. No physical quantum
waterfall or relic result is claimed. Gate 5 remains NOT MET and Gate
10 remains PARTIAL pending exact-head CI and the outstanding warning
cleanup.


## 2026-11-26 exact-head verification of R1.3

Workflow [45795403829](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45795403829) on code head 91aea66bf2fd8101d850c9ab30d8b190d99da8ea completed successfully:
- 222 Python regression cases passed.
- The two-scale homogeneous CI smoke scan passed 4/4 with zero failed integrations. The strict-JSON rows use the exact endpoint-matched Phi_c/M_Pl=0.9862280831209068, explicitly record quantum_vacuum_seeded=false, and have maximum chain-rule continuity residual 3.3603e-12.
- The 11-grid bare-WKB UV audit passed. Its fixed-spacing volume spread is 2.38067e-13 and its high-cutoff log slope is 3.8822733. The artifact explicitly retains zero-point energy and records vacuum_subtraction_applied=false, counterterms_applied=false and continuum_limit_claimed=false.
- The 48-page manuscript PDF built. The first exact-head pass exposed three overfull equations in the newly added R1.3 subsection; those equations are split in the follow-up layout commit. Underfull boxes remain elsewhere, and the full scan/convergence jobs were skipped by design.

The Python and numerical control jobs are green, but this does not convert the finite-band WKB helper into a complete renormalization prescription. Gate 5 remains NOT MET.

## 2026-11-26 R1.3 exact massive de Sitter mode control

An additional independent analytic control now tests the fourth-order
stress counterterms on a **massive, minimally coupled** scalar in de
Sitter, not only on the conformal-massless and Minkowski-massive limits.
For \(H=1\), \(a(\eta)=-1/\eta\), \(M^2=2\), and \(\xi=0\), the mass
and curvature terms cancel in the canonical mode equation:
\[
\Omega_k^2=k^2+a^2M^2-a''/a=k^2,\qquad
v_k=e^{-ik\eta}/\sqrt{2k}.
\]
At \(\eta=-1\), the exact bare Hilbert mode contributions are
\[
\rho_{k,\mathrm{bare}}=k/2+3/(4k),\qquad
p_{k,\mathrm{bare}}=k/6-1/(4k).
\]
The new regression checks the exact mode Wronskian and compares these
closed-form expressions with the order-four local counterterms at
\(k=20,40,80\). The residuals scale as \(k^{-7}\), consistent with the
first omitted sixth adiabatic order. The manuscript displays the same
analytic control.

This is a stronger R1 free-field UV check, but it does **not** supply
momentum-tail integration, a cutoff-independent finite stress tensor,
independent point-splitting in a general background, finite matching
conditions, a renormalized \(\Phi\) force, or self-consistent
Friedmann/CTP backreaction. It does not change the bare lattice
initializer or its UV divergence. Gate 5 remains **NOT MET**.
