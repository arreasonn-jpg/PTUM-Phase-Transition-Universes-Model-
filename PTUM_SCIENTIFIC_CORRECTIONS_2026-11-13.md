# PTUM scientific consistency corrections (2026-11-13)

## Scope

This branch makes a bounded correction pass over the scalar action, interaction bookkeeping, dark-matter Mathieu reduction, and homogeneous two-field simulation diagnostics. It does not establish the full PTUM scenario, reproduce CLASS/Cobaya, or calculate a physical dark-matter relic abundance.

## 1. Scalar action and metric signature

For signature (-+++), the positive-energy canonical real scalar convention is

~~~tex
\mathcal L_\phi=-\frac12 g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi-V(\phi),
\qquad
T_{\mu\nu}=\partial_\mu\phi\partial_\nu\phi
-g_{\mu\nu}\left[\frac12(\partial\phi)^2+V\right].
~~~

It gives

~~~tex
\ddot\phi+3H\dot\phi+V_{,\phi}=0,\quad
\rho_\phi=\frac12\dot\phi^2+V,\quad
p_\phi=\frac12\dot\phi^2-V.
~~~

The four scalar kinetic terms in the manuscript have been changed to this convention, and the covariant Euler-Lagrange equation now uses Box(phi) - V_phi = 0. This preserves the displayed homogeneous field equations while removing the ghost-sign mismatch. The complete fermion/SM action is still needed for a fully covariant derivation of those sectors.

## 2. Activation interaction sign

Expanding the activation Lagrangian gives

~~~tex
-\frac12m^2\psi^2\left(1-\frac{\alpha\Phi^2}{E_{\rm th}^2}\right)
=-\frac12m^2\psi^2
+\frac12\alpha m^2\frac{\Phi^2}{E_{\rm th}^2}\psi^2.
~~~

Thus the isolated cross-interaction term has a positive sign in L. The contradictory negative sign in the microscopic-transfer subsection has been corrected.

## 3. Transfer-current bookkeeping

Individual sector transfer vectors are not unique until the interaction stress tensor is assigned to sectors. The manuscript now states a split convention: the Phi-psi potential and psi^2 phi_SM^2 interaction are assigned to the psi sector; the chi^2 Phi_res^2 interaction is assigned to the DM sector; and the Yukawa interaction is assigned to the SM sector.

For L_Y = -y_psi psi fbar f, the scalar equation has source y_psi fbar f. The corresponding scalar-sector current is proportional to

~~~tex
Q_{\psi,Y}^{\nu}=y_\psi\bar f f\nabla^\nu\psi,
\qquad
Q_{{\rm SM},Y}^{\nu}=-Q_{\psi,Y}^{\nu}.
~~~

Its mass dimension is 3+2=5, matching the dimension of the divergence of an energy-momentum tensor. The former fermion vector-current expression had dimension four and was not a valid energy-transfer four-vector.

With the stated assignment, the scalar-quartic reheating current signs have also been oriented oppositely between the two sectors. The displayed currents cancel pairwise algebraically. A final first-principles verification still requires writing the complete SM/fermion action and deriving each sector Hilbert tensor, including all interaction contributions, from that same action. Pairwise cancellation is a bookkeeping consistency check, not a substitute for the omitted microscopic SM derivation.

The DM--DE Hilbert tensors were also corrected: with signature $(-+++)$, the potential terms enter
$T^{\\mu\\nu}=\\partial^\\mu\\varphi\\partial^\\nu\\varphi
-g^{\\mu\\nu}[\\tfrac12(\\partial\\varphi)^2+V]$
with a plus sign. The former DM and DE tensor expressions had the potential signs reversed.

The conversion from a covariant transfer vector to the homogeneous source is now explicit. Since $\\nabla^0\\varphi=-\\dot\\varphi$,
$Q_i^0$ appears on the right-hand side of
$\\dot\\rho_i+3H(\\rho_i+p_i)=Q_i^0$.
The manuscript's homogeneous signs are now
$Q_\\psi^0=-(\\alpha m^2/E_{\\rm th}^2)\\Phi\\psi^2\\dot\\Phi$,
$Q_\\Phi^0=-Q_\\psi^0$,
$Q_{\\rm DM}^0=+2g_{\\rm DM}\\chi^2\\Phi_{\\rm res}\\dot\\Phi_{\\rm res}$,
and $Q_{\\rm DE}^0=-Q_{\\rm DM}^0$.
The former background expressions had signs inconsistent with their own covariant currents. The manuscript now shows the derivation from the assigned interaction potentials.

## 4. Dark-matter Mathieu reduction

Starting from

~~~tex
\ddot\chi_k+3H\dot\chi_k+
\left(\frac{k^2}{a^2}+m_\chi^2+
2g_{\rm DM}\Phi_{\rm res}^2\right)\chi_k=0
~~~

and Phi_res = A_res cos(omega_res t), neglecting expansion only in the controlled short-time limit gives

~~~tex
\frac{d^2\chi_k}{dz^2}+[A_k-2q\cos(2z)]\chi_k=0,\quad z=\omega_{\rm res}t,
~~~
~~~tex
A_k=\frac{k^2/a^2+m_\chi^2+g_{\rm DM}\mathcal A_{\rm res}^2}{\omega_{\rm res}^2},
\qquad
q=-\frac{g_{\rm DM}\mathcal A_{\rm res}^2}{2\omega_{\rm res}^2}.
~~~

The sign of q can be shifted by a phase translation of z; its factor of one-half and the constant mass shift in A_k cannot be omitted. The narrow primary band is centered near A_k=1, corresponding to the shifted oscillator frequency being near omega_res, not omega_res/2.

In FRW, X_k = a^(3/2) chi_k obeys an equation with the additional term -3 Hdot/2 - 9 H^2/4. The manuscript now displays this term and restricts the Mathieu reduction to H/omega_res much less than one with slowly varying parameters. The former universal broad-resonance estimate for mu_max has been removed. Floquet exponents must be computed from the monodromy matrix or direct mode integration for each actual (A_k,q); no relic abundance has been inferred from the corrected algebra alone.

## 5. Homogeneous simulation energy accounting

The simulation previously included the same Phi-psi interaction potential in both rho_phi and rho_psi. It is now assigned once, to rho_psi:

~~~python
rho_phi = 0.5 * Phi_dot**2 + V_eff(Phi)
rho_psi = 0.5 * psi_dot**2 + 0.5 * m_eff_sq(Phi) * psi**2 + 0.25 * lambda_psi * psi**4
rho_total = rho_phi + rho_psi
~~~

The corresponding total pressure includes the interaction potential once with negative sign in p_psi. The Friedmann routine no longer silently clips non-positive total density to zero; it raises an error for a non-positive or non-finite state.

The old diagnostic rho_total(t)-rho_total(0) was not a conservation law in an expanding universe. The FRW continuity residual is

~~~tex
C_{\\rm FRW}=\\dot\\rho_{\\rm tot}+3H(\\rho_{\\rm tot}+p_{\\rm tot}).
~~~

The code now exposes two distinct diagnostics. The primary `continuity_residual` applies the chain rule to the energy density and evaluates the field accelerations from the background equations. This avoids catastrophic relative normalization when a nearly constant vacuum density is differentiated numerically. It is an equation-consistency check using the same RHS, not an independent validation of the ODE solver. The separate `continuity_residual_finite_difference` differentiates the sampled density with `numpy.gradient`; it is retained for output-grid and solver-tolerance convergence studies and may be noisy when the density is vacuum dominated. The two diagnostics must not be conflated.

## 6. Oscillation diagnostics

The quartic-dominance diagnostic now uses the actual Phi(t) history and local |m_eff^2(Phi(t))| over each half-cycle. It returns NaN when no complete oscillation interval exists rather than reporting a misleading zero. The quartic virial ratio is evaluated as <K>/(2<V4>), which tends to unity for a quartic oscillator. Classification returns insufficient_oscillation_data when required diagnostics are unavailable.

## 7. Additional DM-DE transfer correction

The former DM-DE estimate contained two independent problems. First, the homogeneous transfer sign was inconsistent with the covariant current under the (-+++) convention. The correct source is
\[
Q_{\\rm DM}^{0}=+2g_{\\rm DM}\\chi^2\\Phi_{\\rm res}\\dot\\Phi_{\\rm res},
\\qquad Q_{\\rm DE}^{0}=-Q_{\\rm DM}^{0}.
\]
Second, the estimate used \(\\rho_{\\rm DM}\\simeq m_\\chi\\chi^2\), which has mass dimension three rather than four for a scalar field of mass dimension one. For a coherently oscillating quadratic scalar,
\[
\\rho_{\\rm DM}\\simeq m_\\chi^2\\langle\\chi^2\\rangle_\\chi,
\qquad
\\frac{|\\langle Q_{\\rm DM}^{0}\\rangle_\\chi|}
{H\\rho_{\\rm DM}}
\\simeq
\\frac{2g_{\\rm DM}|\\Phi_{\\rm res}\\dot\\Phi_{\\rm res}|}
{H m_\\chi^2},
\]
provided the residual field varies slowly over a chi oscillation. The previous claimed \(3\\times10^{-6}\) decoupling bound did not follow from the stated parameter ranges and has been withdrawn. A numerical bound requires explicit background histories and a defined averaging window.

## 8. Fuel-potential dimensions and inflation background

The code previously evaluated exp(-lambda_phi * Phi**2) while also defining \(\Phi_c=M_{\rm Pl}/\sqrt{\lambda_\Phi}\) and treating \(\lambda_\Phi\) as dimensionless. The exponent was therefore dimensionful. The manuscript's appendix also listed \([\lambda]=\mathrm{GeV}^{-2}\), conflicting with the code parameterization and the stated Planck-scaled field values.

The convention is now explicit and consistent:
\[
V(\Phi)=V_0\left[1-\exp\left(-\lambda_\Phi
\frac{\Phi^2}{M_{\rm Pl}^2}\right)\right],
\qquad [\lambda_\Phi]=1.
\]
The code uses the corresponding analytic derivative. The discharge threshold \(\Phi_c=E_{\rm th}/\sqrt{\alpha}\) is now an independent simulation parameter, rather than being silently tied to the plateau-shape parameter. Slow-roll initial conditions now include the required \(M_{\rm Pl}^2\) in \(\epsilon_V\) and use the local potential contribution to estimate \(H\).

The inflation-discharge section was rederived for this convention. For \(\lambda_\Phi=0.02\), the tree-level single-field estimate gives \(\Phi_{\rm end}\simeq1.387M_{\rm Pl}\), while \(M_{\rm Pl}/\sqrt{\lambda_\Phi}\simeq7.07M_{\rm Pl}\) is merely the point where the exponential argument equals one. Matching \(\Phi_c\) to the end of inflation is an additional condition. At that matched point, \(V(\Phi_c)/V_0\simeq0.0378\), so the earlier assertion \(\Delta V\simeq V_0\) at discharge was withdrawn.

A new ptum_inflation_background.py implements the dimensionless autonomous background system and the 60-e-fold scan. It computes first-order Hubble-flow estimates, not an exact Mukhanov-Sasaki spectrum. An independent numerical reproduction for \(\lambda_\Phi=0.02\), \(N_*=55\), gives \(x_i=10.71523918\), \(x_*=10.46534426\), \(n_s=0.95808593\), and \(r=0.02195265\). The scan table's old exact-background rows are now explicitly labelled author-reported until the new script's CI execution and all rows are verified.

The plateau's asymptotic logarithmic slope tends to zero; the previous statement that it tends to \(2\lambda_\Phi\Phi\) was incorrect. No swampland-compliance claim is retained. The action also does not establish an approximate shift symmetry, so super-Planckian excursions remain a UV-control issue.

## 9. Regression tests and verification boundary

The pytest regression file is maintained at `tests/test_ptum_consistency.py`. The initial six-test suite passed in GitHub Actions on commit `c2007f455f4cdfc0eee7221aef350ea2ad811659` (`6 passed in 0.42s`). The subsequently added vacuum-dominated near-static background test failed because finite-differencing an almost constant vacuum-dominated density and normalizing by a near-zero scale generated spurious relative values of 1.

The diagnostic is now split:
- `continuity_residual` and `continuity_residual_relative`: chain-rule evaluation using accelerations from the background RHS. This is an equation-consistency diagnostic, not independent solver validation.
- `continuity_residual_finite_difference` and its relative counterpart: sampled `numpy.gradient` diagnostic retained for timestep/output-grid convergence studies. It is not expected to be well-conditioned for a static vacuum-dominated solution.

The expansion term is evaluated as \(3H(\\dot\\Phi^2+\\dot\\psi^2)\), algebraically equivalent to \(3H(\\rho+p)\) for the two canonical homogeneous scalar fields, while avoiding subtraction of vacuum-sized density and pressure terms.

The cycle-averaged equation of state is now computed as \(\\langle p\\rangle/\\langle\\rho\\rangle\), not as \(\\langle p/\\rho\\rangle\). The regime classifier now evaluates the final 20% of the trajectory rather than inadvertently averaging the entire run. Regression tests cover both behaviours.

The current branch contains fifteen tests. GitHub Actions run 43387970066 (run number 114) on PR head 71148588f5f69f4cd83c7d263f031be243c50b0a ran `python -m pytest -q tests/test_ptum_consistency.py` and reported `15 passed in 6.35s`. The parallel latexmk job in run 43388241537 first exposed an unclosed roadmap `description` environment. The missing `\\end{description}` was added in commit a851c545bbdd17eca260d9a12662ced7ac7b8c41. The corrected commit passed both jobs in run 43388485828: Python `15 passed in 3.03s` and LaTeX `latexmk -pdf ... main.tex` completed successfully. Passing Python tests establish only the tested equations and numerical routines, not the complete PTUM cosmology or observational results.

These tests cover homogeneous bookkeeping and internal equation consistency only. They do not establish the full PTUM scenario, reproduce CLASS/Cobaya, or calculate a physical dark-matter relic abundance.

## 10. Still open

1. Derive all sector divergences from one complete action including the Dirac/SM Lagrangian, then verify the interaction-stress assignment line by line.
2. Run the Python test suite and convergence tests; compare analytic and finite-difference continuity residuals.
3. Integrate chi_k modes in an expanding background, compute monodromy/Floquet bands, and include backreaction and rescattering before making relic-density claims.
4. Resolve the benchmark inconsistency between the manuscript's overdamped psi dynamics and the conditional quartic proxy-fluid closure.
5. Independently reproduce CLASS/Cobaya constraints from the public patch, production configs, chains, and data inputs.


## 11. Further corrections and verification boundary

### Transfer currents and action scope
The manuscript now derives the Yukawa current from \(\mathcal L_Y=-y_\psi\psi\bar f f\), with the interaction assigned to the SM tensor:
\[
Q_{\psi,Y}^\nu=+y_\psi\bar f f\nabla^\nu\psi,
\qquad Q_{{\rm SM},Y}^\nu=-Q_{\psi,Y}^\nu.
\]
For \(U_{\rm rh}=\tfrac12g_\psi\psi^2\phi_{\rm SM}^2\), assigned to the \(\psi\) tensor:
\[
Q_{\psi,\rm rh}^\nu=-g_\psi\psi^2\phi_{\rm SM}
\nabla^\nu\phi_{\rm SM},
\qquad Q_{{\rm SM},\rm rh}^\nu=-Q_{\psi,\rm rh}^\nu.
\]
Both have mass dimension five. The conservative scalar action is now distinguished from the schematic full action. The actual SM gauge/fermion/Higgs action remains unspecified, so a complete SM Hilbert tensor has not yet been derived.

### Local damping and model truncation
The homogeneous simulation module is explicitly documented as a two-field \((\Phi,\psi)\) truncation. Its Friedmann source excludes \(\chi\), \(\Phi_{\rm res}\), SM radiation, fermions, and backreaction. It is not a full cosmological evolution or relic-density solver.

The code now distinguishes the plateau-scale damping estimate \(3H_*/(2\mu)\) from the local threshold estimate \(3H_c/(2\mu)\). With \(\lambda_\Phi=0.02\) and the additional matching \(\Phi_c\simeq\Phi_{\rm end}\simeq1.387M_{\rm Pl}\), the potential-dominated local estimate is about 4.9, whereas the plateau-scale estimate is about 25. Both are overdamped. The local value is conditional on threshold matching and must ultimately be replaced by the Hubble history from the full background trajectory.

### Floquet and relic abundance
The new ptum_floquet.py computes frozen-background Mathieu monodromy. It includes the \(-3\dot H/2-9H^2/4\) rescaling correction, checks \(\det M\simeq1\), and returns the real Floquet exponent. It is not an expanding-background calculation and does not include backreaction or rescattering. The former direct closed-form \(\Omega_\chi h^2\) estimate has been withdrawn. The momentum spectrum and post-production entropy history are still required.

### CLASS reproducibility
The legacy CLASS-patch repository URL returned HTTP 404 through the GitHub API during this review. This does not establish whether the repository is private, renamed, or deleted. The current root contains a binary PTUM.zip, but its contents were not inspected and the CLASS patch is not exposed as an individually reviewable tracked source file. Public patch availability is therefore marked UNVERIFIED until the patch, target CLASS commit, checksum, application command, and clean-tree apply log are available.

### Manuscript compilation
A LaTeX build job was added to CI using latexmk. The Python regression job passed (15/15), and the corrected manuscript compiled successfully with latexmk in run 43388485828. The first compile failure on run 43388241537 was caused by an unclosed description list; the missing closing tag was added in commit a851c545bbdd17eca260d9a12662ced7ac7b8c41.


## 12. Corrected scan classification, strict JSON, and manuscript references

The first corrected 18-point scan (GitHub Actions run 43389261756) completed all 18 integrations, but none satisfied the combined quartic criteria. Sixteen were previously labelled `barrier_crossing` solely because the late-time averaged equation-of-state diagnostic exceeded 0.5; that condition does not measure a field-space barrier crossing. The classifier has therefore been changed to the neutral `non_quartic` label unless the explicit quartic or quadratic-candidate criteria are met. The two zero-seed cases have no oscillation data because the exact `psi=psi_dot=0` solution is invariant under the deterministic homogeneous equations. This does not model quantum fluctuation seeding.

The scan export previously emitted Python's non-standard `NaN` tokens for unavailable diagnostics. The serializer now maps non-finite values to JSON `null` and uses `allow_nan=False`; the trajectory amplitude field is renamed `max_abs_psi_over_trajectory` because it is a maximum over the history, not the final-time amplitude. New regression tests cover both the regime-label semantics and strict JSON parsing. The updated scan must be rerun in CI; the prior artifact is not a validation of the corrected serializer/classifier.

The successful LaTeX build in run 43389261756 still reported two unresolved references to `sec:entropy_budget`. A dedicated `Reheating and entropy budget` subsubsection label has now been added before the reheating derivation. The next LaTeX CI run must confirm that the warnings are gone; a successful exit code alone is not sufficient if cross-references remain unresolved.

The branch now has additional tests for (i) refusing to infer barrier crossing from (w>0.5), and (ii) serializing unavailable values as strict JSON nulls. GitHub Actions run 43390565834 on commit 733b4f477112b9cc4c1b096bb791fb2e2acd9c47 reports **18 passed in 4.30 s**. Its 18-point scan completed 18/18 integrations and classified 16 as `non_quartic` and two as `insufficient_oscillation_data`; none met the quartic criteria. The newly generated scan artifact was downloaded and parsed with a strict JSON parser; all unavailable diagnostics are JSON `null`, not non-standard `NaN`. The LaTeX job for this run was still in progress when this note was updated, so the corrected entropy section and reference-label fix remain pending final compilation verification.


## 13. Reheating energy, entropy, and cosmological initial entropy

The manuscript previously set the discharge energy to $V_0$ even after the corrected fuel potential and threshold matching had shown $V(\Phi_c)/V_0\simeq0.0378$. This was inconsistent. The reheating section now defines the released energy from the actual decrease of the total energy along the coupled trajectory. Only in the potential-dominated, threshold-matched single-field approximation with negligible initial kinetic/proxy contributions is
\[
\rho_{\rm dis}\simeq V(\Phi_c)-V(0)\simeq0.0378V_0.
\]
The corresponding instantaneous-thermalization estimate for $g_*=100$ is
$T_{\rm rh}\simeq1.84\times10^{15}\,\mathrm{GeV}$
when $V_0^{1/4}=10^{16}\,\mathrm{GeV}$. This is conditional and is not a full reheating solution.

The former present-entropy estimate used $s_0\sim10^9\,\mathrm{cm}^{-3}$, which is not the present photon-plus-neutrino entropy density. The manuscript now uses $s_0\simeq2.9\times10^3\,\mathrm{cm}^{-3}$ and identifies the total entropy of order $10^{88}$ as an observed quantity obtained by multiplying by the present observable volume. It no longer presents a spurious direct $T_{\rm rh}^3$ scaling for the total observable entropy; a correct connection requires the full adiabatic thermal history and entropy degrees of freedom.

The previous claim $H_*\Delta t\sim10^{-3}$ and negligible expansion during discharge was withdrawn. Under the threshold-matched benchmark, $3H_c/(2\mu)\simeq4.9$, hence $H_c/\mu\simeq3.27$. The nominal interval $\mu^{-1}$ is therefore not short relative to the Hubble time. The actual duration and expansion factor require the coupled background solution.

A coherent homogeneous scalar may have low coarse-grained matter entropy, but this does not determine gravitational entropy or explain the low-entropy initial condition of the Universe. The manuscript now explicitly withdraws any claim that PTUM replaces the Past Hypothesis or derives the thermodynamic arrow of time.

Finally, the former list of energy-partition ratios was not produced by the homogeneous simulation or the CLASS perturbation code. It has been reframed as phenomenological/observational target quantities: $\Delta N_{\rm fluid}$, the observed dark-matter abundance, the present dark-energy density, and the SM radiation fraction. The paper now states that their microscopic production and partition have not been computed self-consistently.


## 14. Gauge invariance of the reheating fermion coupling

The schematic renormalizable operator $-y_\psi\psi\bar f f$ is gauge invariant for a gauge-singlet Dirac field or a vector-like Dirac representation with matching left/right gauge representations. It is not by itself a gauge-invariant Yukawa interaction for the chiral Standard Model fermions. The manuscript now states this limitation and displays the schematic gauge-invariant dimension-five alternatives
\[
-\frac{\psi}{\Lambda}
\left(\bar Q_L C_d H d_R+
\bar Q_L C_u\widetilde H u_R+
\bar L_L C_e H e_R\right)+\mathrm{h.c.}
\]
with the appropriate flavour matrices and Higgs doublet. After electroweak symmetry breaking these generate effective couplings proportional to $C_f v/(\sqrt2\Lambda)$. The transfer source and decay widths must be recomputed for this EFT realization. The shorthand $\phi_{\rm SM}^2$ in the scalar reheating operator must likewise denote a gauge-invariant Higgs bilinear such as $H^\dagger H$, with an explicit normalization convention.

This does not complete the SM action or Hilbert tensor. It prevents the current generic Dirac bookkeeping formula from being misrepresented as a full chiral-SM derivation.

## 15. Correcting the scan's benchmark coverage

A further audit found that the earlier 18-point scan runner used $V_0=10^{56}\,\mathrm{GeV}^4$, while the threshold-matched high-scale benchmark discussed in the claim-boundary document uses $V_0\sim10^{64}\,\mathrm{GeV}^4$. The earlier scan was therefore a low-scale underdamped control, not a direct test of the high-scale benchmark. Its 16 non-quartic and two insufficient-data classifications remain valid for that control only.

The CI scan runner has now been expanded to run both:
- `high_scale_threshold_matched`: $V_0=10^{64}\,\mathrm{GeV}^4$, $\Phi_c=1.387M_{\rm Pl}$;
- `low_scale_underdamped_control`: $V_0=10^{56}\,\mathrm{GeV}^4$, with the same threshold matching and initial-condition grid.

This produces 36 integrations. Each output row carries the scenario name, $V_0$, $\Phi_c/M_{\rm Pl}$, and both local and plateau damping ratios. A regression test verifies that the high-scale case is overdamped by the local potential estimate and the low-scale control is underdamped. The next CI run must inspect the high-scale outcome before any conclusion is drawn about whether the stated benchmark reaches the quartic regime.


## 16. Derivation of the quartic-dominance threshold

The diagnostic is
\[
Q=\frac{\lambda_\psi\langle\psi^4\rangle}
{\langle|m_{\rm eff}^2|\psi^2\rangle}.
\]
For $V_4=\lambda_\psi\psi^4/4$ and the magnitude of the tachyonic quadratic contribution $|V_2|=|m_{\rm eff}^2|\psi^2/2$, the ratio of averaged potential contributions is
\[
\frac{\langle V_4\rangle}{\langle|V_2|\rangle}=\frac{Q}{2}.
\]
Therefore quartic potential-energy dominance corresponds to $Q/2>1$, or $Q>2$. The previous classifier used $Q>5$ without documenting a physical derivation. It now reports the explicit ratio $Q/2$ and applies the energy-dominance boundary $Q>2$, together with independent cycle-averaged equation-of-state and virial conditions. A new regression test checks values on either side of this boundary. This criterion is an operational diagnostic for the homogeneous truncation, not a proof of a radiation-like effective fluid by itself.


## 17. Critical mismatch: inflationary field direction versus tachyonic activation

For the adopted fuel potential
\[
V(\Phi)=V_0\left[1-e^{-\lambda_\Phi\Phi^2/M_{\rm Pl}^2}\right],
\]
one has $V_{,\Phi}>0$ for $\Phi>0$, and canonical slow roll gives
$\dot\Phi\simeq-V_{,\Phi}/(3H)<0$. The matched inflationary trajectory therefore rolls from $\Phi_*/M_{\rm Pl}\simeq10.5$ toward $\Phi_{\rm end}/M_{\rm Pl}\simeq1.387$.

However, the current activation mass
\[
m_{\rm eff}^2=m_\psi^2\left(1-\Phi^2/\Phi_c^2\right)
\]
is negative for $|\Phi|>\Phi_c$. If $\Phi_c\simeq\Phi_{\rm end}$, the proxy mode is tachyonic throughout the observable slow-roll interval and becomes non-tachyonic as $\Phi$ falls below the threshold. This is the reverse of the manuscript's stated dormant-to-tachyonic onset at the end of inflation.

The current inflation module omits $\psi$ and does not track its stability during inflation. The homogeneous two-field scan starts at $\Phi>\Phi_c$, already on the tachyonic side, so it does not simulate the onset from a dormant state. The manuscript and claim boundary now state this explicitly. A characterization regression test verifies the sign ordering. No arbitrary sign flip has been applied: the model must derive either a different activation function or a physically motivated fuel trajectory from one consistent action before the threshold-trigger narrative can be claimed.

This is a **critical unresolved model-structure issue**, not a cosmetic wording issue. It blocks a 10/10 scientific-readiness claim until resolved and re-tested in the coupled background.


## 18. Two-scale scan result

GitHub Actions run 43391427434 on the current scientific branch completed **21 tests successfully** and ran both 18-point scenarios, for 36 successful integrations and zero integration failures.

The threshold-matched high-scale benchmark ($V_0=10^{64}\,\mathrm{GeV}^4$, $\Phi_c=1.387M_{\rm Pl}$, local damping ratio $\simeq4.87$) produced 15 non-quartic cases, two insufficient-oscillation-data cases, and one quadratic-candidate case; it produced no quartic cases. The low-scale underdamped control ($V_0=10^{56}\,\mathrm{GeV}^4$) produced 16 non-quartic and two insufficient-data cases, again with no quartic cases. The high-scale quadratic candidate is not a demonstrated quadratic attractor: its virial diagnostic is far from the quartic limit and the label is only a coarse classification based on $w$ and the small quartic-to-quadratic ratio.

For the high-scale cases with measurable oscillations, $Q$ is many orders of magnitude below two, so the quartic potential is negligible relative to the tachyonic quadratic contribution. This strengthens the conclusion that the stated high-scale benchmark does not realize the proxy-fluid quartic regime in the present homogeneous truncation. It does not prove that no parameter choice or inhomogeneous evolution can realize it.

The scan artifact was downloaded and parsed independently. It contains 36 rows, includes the scenario and damping metadata, and is strict JSON. The LaTeX job in the same run also completed successfully and produced a 38-page PDF. Its first clean build pass emitted unresolved-reference warnings while auxiliary files were being regenerated; latexmk completed its subsequent passes, and no final unresolved-reference summary was emitted. The manuscript still has a harmless float-placement warning (`h` changed to `ht`) and the workflow action versions emit Node.js 20 deprecation warnings, which should be cleaned up in a later CI-maintenance pass.


## 19. Independent quadratic-regime virial diagnostic

The previous `quadratic_candidate` label required only a matter-like cycle-averaged equation of state and a subdominant quartic ratio. That was too weak to identify a quadratic oscillator. A separate half-cycle diagnostic is now implemented:
\[
R_2=\frac{\langle K\rangle}
{\langle V_2\rangle},
\qquad
V_2=\frac12m_{\rm eff}^2(\Phi)\psi^2,
\]
and is defined only on complete half-cycles where $m_{\rm eff}^2>0$. A harmonic oscillator with slowly varying positive mass approaches $R_2=1$. The classifier now requires $|w|<0.1$, $Q<1$, and $|R_2-1|<0.2$ before assigning `quadratic_candidate`. Two new tests check the harmonic limit and reject tachyonic intervals; another verifies the classifier gate. The updated suite contains 24 tests. GitHub Actions run 43392067477 has completed the Python regression step successfully; the scan and LaTeX jobs were still running when this note was updated.


## 20. Latest regression and reclassified two-scale scan

GitHub Actions run 43392067477 completed **24 tests successfully**. Both 18-point scans also completed all 36 integrations with zero numerical integration failures. After adding the independent positive-mass quadratic virial diagnostic, the final classifications are:
- High-scale threshold-matched benchmark: 16 non-quartic, two insufficient-oscillation-data; no quartic or quadratic-candidate trajectories.
- Low-scale underdamped control: 16 non-quartic, two insufficient-oscillation-data; no quartic or quadratic-candidate trajectories.

In the measurable high-scale cases, $R_2=\langle K\rangle/\langle V_2\rangle$ is approximately 0.75--0.79, outside the required $|R_2-1|<0.2$ quadratic-candidate window. The quartic ratio $Q/2$ is many orders of magnitude below one. The prior high-scale quadratic-candidate label is withdrawn under the stricter criterion.

The newest scan artifact (run 43392067477, artifact 14021905273) was downloaded and parsed independently. It contains 36 strict-JSON rows with both scenario names and damping metadata. The Python and scan jobs are green. The LaTeX job for this run was still running when this section was written. The earlier completed LaTeX run on the same manuscript before the newest diagnostic-only code change produced a 38-page PDF.


## 21. Superseding activation-sign revision: hybrid waterfall chronology

Sections 1--20 record the first consistency pass under the manuscript's original activation sign. Their kinetic-sign, stress-tensor, energy-accounting, Mathieu-reduction, numerical-diagnostic, and claim-boundary findings remain applicable, but the earlier $Phi$--$psi$ interaction and transfer-current signs are superseded here.

The original mass $m_{\rm eff}^2=m_\psi^2(1-\Phi^2/\Phi_c^2)$ made the proxy tachyonic for $|\Phi|>\Phi_c$. The adopted fuel potential has $V_{,\Phi}>0$ for positive $Phi$, so slow roll moves downward from $\Phi_*>\Phi_c$ toward $\Phi_{\rm end}\simeq\Phi_c$. That old sign therefore made the proxy tachyonic during inflation and stable after the end, opposite to the manuscript's dormant-pre-discharge / waterfall-after-threshold chronology.

The mass has now been revised to the hybrid/waterfall form
\[
m_{\rm eff}^2(\Phi)=m_\psi^2\left(\frac{\alpha\Phi^2}{E_{\rm th}^2}-1\right)
=m_\psi^2\left(\frac{\Phi^2}{\Phi_c^2}-1\right).
\]
It is positive for $|\Phi|>\Phi_c$ and negative for $|\Phi|<\Phi_c$. This makes the proxy stable during the observable slow-roll interval and tachyonic after the field rolls below the threshold. The sign is selected from the intended phase chronology and the computed direction of the slow-roll solution, not as an arbitrary fit.

The activation potential is now
\[
U_{\Phi\psi}=\frac12\frac{\alpha m_\psi^2}{E_{\rm th}^2}\Phi^2\psi^2
-\frac12m_\psi^2\psi^2+\frac{\lambda_\psi}{4}\psi^4.
\]
With the interaction assigned to $T_\psi^{\mu\nu}$, the interaction-only currents become
\[
Q_\psi^\nu=-\frac{\alpha m_\psi^2}{E_{\rm th}^2}
\Phi\psi^2\nabla^\nu\Phi,\qquad
Q_\Phi^\nu=+\frac{\alpha m_\psi^2}{E_{\rm th}^2}
\Phi\psi^2\nabla^\nu\Phi,
\]
and
\[
Q_\psi^0=+\frac{\alpha m_\psi^2}{E_{\rm th}^2}
\Phi\psi^2\dot\Phi,\qquad Q_\Phi^0=-Q_\psi^0.
\]
For the slow-roll direction $\dot\Phi<0$, the assigned $\psi$-sector source is negative. The manuscript now explicitly avoids describing this convention-dependent signed source as positive fuel-to-proxy energy transfer.

The Python model has been updated consistently: $m_{\rm eff}^2$, $\partial m_{\rm eff}^2/\partial\Phi$, the $\Phi$ acceleration, the chain-rule continuity diagnostic, the local tachyonic scale, and initial conditions are all aligned with the revised sign. Positive $\phi$ offsets now place the initial field below $\Phi_c$, on the tachyonic side. Baseline tests and sign-characterization tests have been updated.

The previous 36-point scan (run 43392067477) used the old sign and is now historical only. It must not be cited as a result for the revised model. A fresh CI run must verify the revised equations, 24-plus regression tests, both benchmark scans, and LaTeX build. Even after that, the current two-field scan begins below threshold and does not resolve the onset itself; coupled quantum seeds, inhomogeneous waterfall growth, and backreaction remain necessary.


## 22. High-resolution initial-condition scan

The earlier 36-point post-threshold scan used only 200 output samples over $20\mu^{-1}$. The high-scale trajectories exhibited many turning points, leaving only a few output samples per half-cycle. That resolution is inadequate for reliable cycle-averaged $w$, $Q$, and virial diagnostics. The scan grid has therefore been expanded and the output resolution raised.

The revised runner now uses a $5\times5\times2$ grid in:
- initial field seed $\psi/\psi_0\in\{0,0.1,1,2,5\}$;
- initial velocity seed $\dot\psi/(\mu\psi_0)\in\{0,0.1,1,2,5\}$;
- post-threshold offset $(\Phi_c-\Phi)/\Phi_c\in\{0.01,0.1\}$.

It runs 50 initial conditions at each energy scale (100 total), with 4001 output points over $20\mu^{-1}$ per trajectory. Each JSON row records the scenario, damping ratios, time span, output resolution and seed grid. Regression tests check the 50-point grid and ensure positive offsets start below $\Phi_c$ on the tachyonic side. This remains a homogeneous post-threshold sensitivity scan, not a quantum-vacuum seed distribution or a simulation of the threshold crossing itself. The pre-exact-endpoint revision passed **25 regression tests** in run 43393188155. After the exact $\epsilon_H=1$ threshold update, the exact-endpoint, signed-transfer, moving-minimum excitation and undefined-w diagnostic regressions bring the suite to 32; the fresh 32-test run, 100 high-resolution integrations, and LaTeX build are pending.


## 23. Exact inflation endpoint replaces the potential slow-roll endpoint

A further numerical audit found that the earlier threshold match used the potential slow-roll proxy $\epsilon_V=1$, which gives $\Phi/M_{\rm Pl}=1.387175$ for $\lambda_\Phi=0.02$. The exact canonical background integration instead terminates when the Hubble-flow parameter reaches $\epsilon_H=1$. For the same model and $N_{\rm target}=60$, this gives
\[
\Phi_{\rm end}^{(H)}/M_{\rm Pl}=0.98622808,
\qquad
\epsilon_V(\Phi_{\rm end}^{(H)})=2.01657.
\]
The old $1.387175M_{\rm Pl}$ threshold is crossed about $0.31852$ e-folds before the exact end. The potential slow-roll value remains useful as a first-order estimate, but it is not the exact end field.

The inflation module now reports both $x_{\rm end}^{(V)}$ and $x_{\rm end}^{(H)}$, the potential parameter at the exact endpoint, and the e-fold offset of the old threshold. The threshold-matched high/low scan now derives $\Phi_c$ from $x_{\rm end}^{(H)}$ rather than hardcoding the potential slow-roll value. The simulation default threshold and regression tests have been updated accordingly.

This changes the threshold potential fraction from $V(1.387M_{\rm Pl})/V_0\simeq0.0378$ to
\[
V(\Phi_{\rm end}^{(H)})/V_0\simeq0.01926493.
\]
At $\epsilon_H=1$, $X_{\rm end}^2=1/3$, so the exact single-field endpoint also has
\[
K_{\rm end}/V_0\simeq0.00963246,\qquad
\rho_{\rm end}/V_0\simeq0.02889739.
\]
If all of this total energy thermalized instantaneously at $g_*=100$ and $V_0^{1/4}=10^{16}\,\mathrm{GeV}$, the idealized upper-limit estimate is $T_{\rm rh}^{\rm ideal}\simeq1.72\times10^{15}\,\mathrm{GeV}$. Converting only the potential contribution gives $1.56\times10^{15}\,\mathrm{GeV}$. The potential-only damping estimate is $3H_{c,V}/(2\mu)\simeq3.50$, while the exact endpoint including kinetic energy gives $3H_c/(2\mu)\simeq4.29$. Both are overdamped. These values supersede the earlier $0.0378V_0$, $1.84\times10^{15}\,\mathrm{GeV}$, and $4.9$ estimates in Sections 13 and 21.

The new regression test checks both end-field values and the $0.31852$ e-fold crossing offset. A fresh 100-point high-resolution scan must run with this exact threshold before its outcomes are accepted.


## 24. Observational comparison sign convention

The abstract reported $\Delta\chi^2=+0.26$, while the claim-boundary note previously displayed $-0.26$ for the same benchmark. The claim-boundary document has been aligned to the abstract and now explicitly defines
\[
\Delta\chi^2\equiv\chi^2_{\rm PTUM}-\chi^2_{\Lambda\rm CDM}.
\]
Thus the author-reported $+0.26$ indicates a slightly worse best-fit chi-square for PTUM under this convention, consistent with the reported $\Delta\mathrm{AIC}=+2.26$ preference for the simpler $\Lambda$CDM model. These numbers remain author-reported because the exact chains and likelihood configuration are not yet publicly reproducible.


## 25. Objective 10/10 acceptance matrix

Added `PTUM_10_OF_10_ACCEPTANCE.md` to the repository. It defines ten evidence gates covering the complete action, inflation-to-waterfall connection, Hilbert tensors and conservation, converged background numerics, inhomogeneous waterfall dynamics, expanding-background resonance and relic abundance, microscopic proxy-fluid realization, reheating/entropy, observational reproducibility, and software/manuscript reproducibility.

The matrix explicitly separates partial work from unmet requirements and sets a non-negotiable rule: PTUM is not called 10/10 until every gate is supported by reproducible evidence. Passing tests alone cannot satisfy the physics gates.


## 26. Signed waterfall transfer rates in the numerical model

The revised sector source is now implemented as `waterfall_transfer_rate` in `ptum_task1_simulation.py` and exposed in each simulation result as `Q_psi0` and `Q_Phi0`. For the declared split with $U_{\Phi\psi}=+\tfrac12(\alpha m_\psi^2/E_{\rm th}^2)\Phi^2\psi^2$,
\[
Q_\psi^0=+\frac{\alpha m_\psi^2}{E_{\rm th}^2}
\Phi\psi^2\dot\Phi,\qquad Q_\Phi^0=-Q_\psi^0.
\]
The new regression test checks the sign for $\dot\Phi<0$ and exact pairwise cancellation. This makes the manuscript's signed source convention directly inspectable in the simulation output; it does not replace the still-pending full SM-sector Hilbert-tensor derivation.


## 27. Real-scalar waterfall defect topology

The manuscript now distinguishes the scalar proxy from an actual string field. In the current real-$\psi$ truncation, the tachyonic quartic potential has two degenerate minima
\[
\psi_{\min}=\pm\sqrt{-m_{\rm eff}^2/\lambda_\psi}.
\]
A spatially inhomogeneous waterfall can therefore break a $Z_2$ symmetry and form domain walls. The string-tachyon comparison is explicitly labelled a structural analogy; it is not a derivation of cosmic strings. The previously reported winding analysis concerns $\Phi_{\rm res}$ and does not establish the absence of $\psi$ domain walls.

The manuscript and claim-boundary document now state this limitation, and the 10/10 acceptance matrix requires a field-topology choice and an inhomogeneous defect-network calculation. A defect-safe completion may require a complex/gauged order parameter or a physically justified bias term, but no such modification is imposed without a model-level decision because it changes the symmetry and dynamics.


## 28. Pinned scientific CI environment

Added `requirements-ci.txt` with the Python 3.11 runner's verified package versions: pip 26.3, NumPy 2.4.6, SciPy 1.17.1, pytest 9.2.0, and their iniconfig/packaging/pluggy/Pygments dependencies. The workflow now installs this lock file, enables pip caching keyed to it, and records `pip freeze` in the job log. This removes floating versions from the Python CI package stack. The Python patch release and GitHub-hosted Ubuntu image remain runner-managed and should be recorded in each CI run.


## 29. Gauge-invariant reheating EFT and Higgs-portal transfer currents

The reheating interaction has been sharpened from a generic scalar $phi_{\rm SM}$ and Dirac shorthand to an explicit gauge-invariant EFT, assuming $psi$ is a real SM gauge singlet:
\[
\mathcal O_{\rm SM}=
\bar Q_L C_d H d_R+
\bar Q_L C_u\widetilde H u_R+
\bar L_L C_e H e_R+\mathrm{h.c.},
\qquad
\mathcal L_{\rm rh}=
-\frac{\psi}{\Lambda}\mathcal O_{\rm SM}
-\frac12g_{\psi H}\psi^2H^\dagger H.
\]
The first term is dimension five and reduces after electroweak symmetry breaking to effective scalar-fermion couplings $y_{\psi f}^{\rm eff}=C_fv/(\sqrt2\Lambda)$. The second is a renormalizable gauge-invariant Higgs portal.

Under the declared sector split (fermion-Higgs operator assigned to $T_{\rm SM}$, Higgs portal assigned to $T_\psi$), the corresponding currents are now written as
\[
Q_{\psi,Y}^\nu=\frac{\mathcal O_{\rm SM}}{\Lambda}\nabla^\nu\psi,
\quad
Q_{\psi,H}^\nu=-\frac{g_{\psi H}}2\psi^2
\left[H^\dagger D^\nu H+(D^\nu H)^\dagger H\right],
\]
with $Q_{\rm SM,Y}^\nu=-Q_{\psi,Y}^\nu$ and
$Q_{\rm SM,H}^\nu=-Q_{\psi,H}^\nu$. Both currents have mass dimension five and cancel pairwise in the total tensor divergence.

For small oscillations about a fixed broken-phase minimum, the local curvature mass is $m_{\rm osc}^2=-2m_{\rm eff}^2$. A conditional perturbative width to a fermion pair is displayed using $m_{\rm osc}$ and $y_{\psi f}^{\rm eff}$; it is not a reheating prediction until $\Lambda$, flavour matrices, competing Higgs channels and the time-dependent post-waterfall background are fixed.

The dimension-five operator is odd in $psi$ and may explicitly break the $Z_2$ symmetry of the isolated real-scalar potential. Whether this lifts the two-vacuum degeneracy enough to eliminate domain walls depends on Wilson coefficients and any additional discrete charge assignments. The domain-wall issue therefore remains open, not solved by merely writing the EFT operator.


## 30. Explicit scalar Hilbert tensors and formal SM split

The manuscript now writes $T_\Phi^{\mu\nu}$ and $T_\psi^{\mu\nu}$ explicitly from the revised scalar action. The $Phi$--$psi$ interaction and Higgs portal are included exactly once in $T_\psi$; the $chi^2\Phi_{\rm res}^2$ interaction remains assigned to $T_{\rm DM}$; the dimension-five fermion-Higgs operator is assigned to $T_{\rm SM}$. A formal Hilbert definition of $T_{{\rm SM},0}^{\mu\nu}$ from the curved-spacetime chiral SM action is now displayed, with $-g^{\mu\nu}U_Y$ as the assigned interaction contribution.

This closes the bookkeeping definition of the sector split at the action level, but not the full explicit SM tensor derivation: gauge, Higgs, tetrad and spin-connection terms for all chiral fermions still need to be evaluated and checked against the displayed transfer currents. Gate 3 therefore remains PARTIAL.


## 31. Well-conditioned FRW residual normalization

The FRW continuity diagnostic now reports both the local-term normalization and a background-energy normalization:
\[
C_{\rm FRW}^{\rm bg}
=\frac{\dot\rho+3H(\rho+p)}{|H|\,|\rho|}.
\]
The latter remains well-conditioned when a vacuum-dominated solution makes both $\dot\rho$ and $3H(\rho+p)$ very small. The finite-difference estimate has the same background-energy normalization, in addition to the original local normalization. The local ratio is retained for diagnostic purposes but must not be interpreted when its denominator approaches round-off scale.

Regression tests now check the chain-rule and background-normalized finite-difference residuals for both the near-static vacuum-dominated and evolving two-field cases. The finite-difference tolerance is looser and is intended as a numerical diagnostic, not as a substitute for a timestep/tolerance convergence campaign.


## 32. Positive excitation-energy split about the moving waterfall minimum

The raw $psi$ potential is negative at its broken-phase minima, so the raw ratio $p_\psi/\rho_\psi$ is not a reliable late-time fluid diagnostic near those minima. A second, explicitly diagnostic sector split is now implemented without changing the equations of motion or total stress tensor.

For $m_{\rm eff}^2<0$,
\[
V_{\min}(\Phi)=-\frac{[\max(-m_{\rm eff}^2,0)]^2}{4\lambda_\psi},
\qquad
V_{\rm exc}(\Phi,\psi)=V_\psi(\Phi,\psi)-V_{\min}(\Phi)\ge0.
\]
The code reports $\rho_{\psi,\rm exc}=\dot\psi^2/2+V_{\rm exc}$ and
$p_{\psi,\rm exc}=\dot\psi^2/2-V_{\rm exc}$, while moving
$V_{\min}$ into the $\Phi$ bookkeeping sector:
\[
\rho_{\Phi,\rm split}=\rho_\Phi+V_{\min},\qquad
p_{\Phi,\rm split}=p_\Phi-V_{\min}.
\]
The sums of the split densities and pressures are exactly the original totals. The shifted source is
$Q_{\psi,\rm exc}^0=Q_\psi^0-\dot V_{\min}$ and
$Q_{\Phi,\rm split}^0=-Q_{\psi,\rm exc}^0$; it vanishes at the instantaneous moving minimum. The original Hilbert-sector source $Q_\psi^0$ remains available separately.

The cycle-averaged $w_\psi$ diagnostic now uses the positive excitation energy, with the raw unshifted average retained separately. The regression suite covers positivity, zero excitation potential at the instantaneous minimum up to floating-point precision, unbroken-phase behavior, conservation of the split totals, vanishing shifted transfer at the moving minimum, and NaN handling for undefined raw w. This is a diagnostic bookkeeping improvement, not a calculation of reheating or a microscopic radiation-fluid realization. It applies to the pre-reheating two-field truncation; once the Higgs background is active, the portal contribution must enter the instantaneous minimum and the shifted split must be rederived.



## 33. Post-inflation trajectory matching and fail-closed scan validation

A further initial-condition audit found that the homogeneous waterfall scan had been assigning $\dot\Phi$ from the potential slow-roll expression at displaced post-threshold field values. This is inconsistent with the exact inflation calculation, which terminates at $\epsilon_H=1$ and is already outside the potential slow-roll regime at the endpoint.

The inflation module now provides `state_at_field_value`. It starts from the calibrated 60-e-fold attractor and integrates the canonical single-field FRW equations through the exact $\epsilon_H=1$ endpoint until each requested post-threshold field value is reached. It returns $N$, $x$, $X$, $H$, $\dot\Phi$, $\rho$ and $\epsilon_H$. The two-field scan now initializes $\dot\Phi$ from this trajectory separately for each threshold offset and records the velocity source in its metadata. The potential-slow-roll initializer remains available only as an explicit fallback for exploratory calls.

This is a better-matched initial state, but it is still a staged approximation: the single-field trajectory is integrated with $\psi=0$ up to the selected post-threshold offset, and the seeded two-field evolution begins there. It does not yet resolve the coupled threshold crossing, quantum fluctuations, or backreaction during the onset.

The scan runner now validates that all 100 expected trajectories are present and that every integration succeeded. It writes the strict-JSON diagnostic summary before enforcing this gate, and CI attempts to upload the artifact even if validation fails. A regression test checks the exact endpoint ($\epsilon_H=1$, $X=-1/\sqrt3$), the post-end field trajectory, and the explicit velocity override. Another test verifies that incomplete or failed scans are rejected. Zero-$\psi$ entries are explicitly identified as exact classical invariant controls, not quantum-vacuum-seeded trajectories.

The simulation module's top-level equation documentation was also aligned with the revised hybrid-waterfall mass and interaction signs. The conservation subsection in the manuscript no longer assumes $\Delta t\ll H^{-1}$ or that all transfer terms vanish immediately after the transition; it now distinguishes the microscopic field sectors from the later effective four-fluid regrouping and states that spatial transfer components need not vanish in generic inhomogeneous configurations.

The updated regression suite and 100-trajectory scan have not yet been confirmed by a completed GitHub Actions run. These changes therefore remain pending CI verification.


## 34. Exact-endpoint damping regression and CI failure diagnosis

The latest GitHub Actions run executed 35 tests and reported 34 passed, one failed. The failure was isolated to the damping-ratio regression: the implementation correctly used
$H_{c,\rm exact}=\sqrt{3/2}\,H_{c,V}$ for a canonical single-field endpoint at $\epsilon_H=1$, while the test still expected the older potential-only value $H_{c,V}$. The implementation was not reverted. The test now checks both estimates separately, verifies the exact-endpoint relation, and compares the exact damping ratio against the exact Hubble scale.

The workflow's scan-artifact upload also produced a secondary error because pytest stopped the job before the scan output file existed. The upload step now uses `if: always()` with `if-no-files-found: ignore`: it preserves an artifact when the scan ran, without masking an earlier test failure with a second missing-file failure.

These are corrective changes after the failed run. A new CI run is required; the latest suite and scan are not yet claimed to pass.

## 35. Explicit curved-space chiral-SM action and Hilbert tensor

The microscopic-transfer section previously acknowledged that
\(\mathcal L_{\rm SM}^{(0)}\) and its Hilbert tensor were not explicitly
specified. This gap is now closed at the **classical, tree-level,
minimally coupled EFT** level.

The manuscript now fixes the gauge group
\(SU(3)_c\times SU(2)_L\times U(1)_Y\), the representations of
\(Q_L,u_R,d_R,L_L,e_R,H\), three generations, the complex Higgs doublet,
and the four real PTUM gauge singlets. It writes the curved-space gauge,
Higgs and chiral-fermion kinetic terms, the Higgs potential, ordinary SM
Yukawa matrices, the distinct PTUM dimension-five Higgs-dressed operators,
and the Higgs portal. The Einstein-Hilbert term and the absence of
nonminimal curvature couplings are stated.

The Hilbert tensor is obtained by vierbein variation. The gauge tensor,
Higgs tensor, and symmetric on-shell chiral-fermion tensor are displayed;
the standard SM Yukawa potential is included in \(T_{{\rm SM},0}^{\mu\nu}\),
and \(U_Y=\psi\mathcal O_{\rm SM}/\Lambda\) is assigned once to the SM
sector. Together with the existing scalar tensors, the stated sector
assignment gives the previously listed pairwise \(Q_i^\nu\) and
\(\sum_i Q_i^\nu=0\). The operator charges and dimensions are checked
by the new ptum_covariant_action.py registry and regression tests.

The symmetry paragraph is corrected: \(\psi\to-\psi\) is a symmetry of
the scalar-only truncation, not of the full EFT when \(C_f\ne0\);
the odd dimension-five operator explicitly breaks it if SM fields are
untransformed. The Higgs portal remains even. The continuous shift of
\(\Phi_{\rm res}\) is not a symmetry of the specified \(W(\Phi_{\rm res})\).

Important boundary: this is not a UV completion or a quantum/renormalized
effective action. The loop-corrected potential across the tachyonic branch,
SM/Higgs/fermion evolution, independent full-sector conservation convergence,
the thermal vacuum bias, and the domain-wall network are not computed.
The numerical background remains the \(\Phi\)--\(\psi\) truncation.
The full SM reheating rate and energy partition are therefore still
unavailable.



## 36. LaTeX spinor notation and on-shell SM Hilbert-tensor bookkeeping

The latest 43-test workflow run passed its Python regression step, but the LaTeX job failed because the newly introduced `\\mathscr D_\\mu` spinor derivative was used without loading the `mathrsfs` package. The preamble now loads `mathrsfs`; a regression test checks that the package declaration accompanies the notation. The full LaTeX build must still be rerun.

A separate Hilbert-tensor audit addressed the double-counting concern in the classical chiral-SM action. The displayed fermion tensor (T_f^{\\mu\\nu}) is explicitly the on-shell symmetric tensor, with the ordinary SM Yukawa equations of motion included. Its expression must therefore not be supplemented by a second explicit (-g^{\\mu\\nu}U_{{\\rm SM},Y}) term. The equation for (T_{{\\rm SM},0}^{\\mu\\nu}) now reads (T_{\\rm gauge}^{\\mu\\nu}+T_H^{\\mu\\nu}+T_f^{\\mu\\nu}), and the text explains why the ordinary Yukawa potential is already encoded in the on-shell fermion expression.

The distinct PTUM operator (U_Y=\\psi\\mathcal O_{\\rm SM}/\\Lambda) is not part of (S_{\\rm SM}^{(0)}) and remains assigned exactly once through
(T_{\\rm SM}^{\\mu\\nu}=T_{{\\rm SM},0}^{\\mu\\nu}-g^{\\mu\\nu}U_Y).
The formal variational definition now explicitly differentiates (S_{\\rm SM}^{(0)}), not an ambiguously named full SM action. Two source-level regression tests guard the package declaration and this sector bookkeeping. These are consistency guards; a full independent vierbein-variation calculation and numerical SM-sector conservation test remain outstanding.



## 37. Linear expanding-background mode evolution

The frozen Mathieu monodromy solver has been complemented by
`integrate_expanding_mode` in `ptum_floquet.py`. Given sampled
(a(t)), (H(t)), and (Phi_{\\rm res}(t)), it integrates the
physical (chi_k) equation with Hubble friction and the time-dependent
effective mass. It initializes the canonical variable
(X_k=a^{3/2}chi_k) in a first-order adiabatic vacuum only when the
initial canonical frequency is real and the WKB adiabaticity measure
(|\\dot\\Omega_k/\\Omega_k^2|) is below a declared threshold.
It returns the mode history, final instantaneous occupation estimate,
and Wronskian conservation error. It refuses to assign a particle
number when the final canonical frequency is non-positive.

Two regression tests were added: an expanding de Sitter control with
constant physical mass and zero coupling must preserve the adiabatic
vacuum to numerical accuracy; a deliberately non-adiabatic initial
history must be rejected rather than silently labelled as vacuum.

This advances Gate 6 only at the linear numerical-method level. The
solver consumes externally supplied background histories; PTUM does
not yet generate a self-consistent (Phi_{\\rm res}) trajectory
coupled to (chi), SM reheating, and the waterfall. There is no
backreaction, rescattering, nonlinear fragmentation, converged
momentum integral, relic abundance, or entropy dilution result. The
threshold-matched benchmark remains overdamped, so the coherent
oscillatory history required by the Floquet setup is not demonstrated.
The latest two tests and manuscript changes await a fresh CI run.



## 38. Finite-band momentum integration for expanding modes

The expanding-background module now includes
`integrate_expanding_spectrum`. It integrates a strictly increasing
finite comoving-momentum grid by evolving each (chi_k) mode and
evaluating
[
n_{\\chi,\\rm com}^{[k_{\\min},k_{\\max}]}
=\\frac{1}{2\\pi^2}
\\int_{k_{\\min}}^{k_{\\max}}dk\\,k^2n_k,
qquad
n_{\\chi,\\rm phys}^{[k_{\\min},k_{\\max}]}
= n_{\\chi,\\rm com}^{[k_{\\min},k_{\\max}]}/a_f^3.
]
The quadrature is trapezoidal and the output is explicitly marked
finite-band-only. The code does not invent the unresolved infrared or
ultraviolet tails. Tests cover a de Sitter vacuum control and rejection
of an unsorted momentum grid.

This is not yet a relic-abundance result. A converged prediction still
requires momentum-range and grid-spacing studies, a self-consistent
PTUM background, backreaction, rescattering, nonlinear mode coupling,
and entropy dilution. The solver's externally supplied histories do
not establish that the overdamped PTUM benchmark develops the
oscillatory (Phi_{\\rm res}) background required for resonance.
The branch now contains 49 regression tests; the latest tests and
manuscript updates still await a fresh GitHub Actions run.



## 39. FRW background consistency guard for mode evolution

The expanding-mode solver now independently checks that the supplied
scale factor and Hubble history satisfy (H=\\dot a/a), using a
cubic-spline derivative and a declared relative tolerance (default
(5\\times10^{-2})). Inconsistent histories are rejected before
the mode equation is integrated. The maximum consistency residual is
returned with the mode diagnostics. A regression test verifies both
the de Sitter consistency control and fail-closed rejection of an
inconsistent (a(t),H(t)) pair.

This prevents a subtle but serious bookkeeping error: the friction
term uses (H), while the canonical rescaling (X=a^{3/2}\\chi)
requires the same (H) to be (dot a/a). Using unrelated histories
would make the stated canonical frequency and the integrated physical
mode equation mathematically inconsistent. The branch now contains
50 regression tests; the newest changes remain unverified by a fresh
CI run.



## 40. Intermediate tachyonic intervals in the expanding mode solver

A mode-frequency audit found that the initial implementation attempted
to take (sqrt{Omega_k^2(t)}) over the entire history in order to
differentiate the frequency for the initial WKB state. That would
incorrectly reject a physically relevant history if the canonical
frequency became imaginary after the initial adiabatic vacuum had
already been specified.

The code now differentiates the real-valued (Omega_k^2(t)) spline
and obtains (dotOmega_k(t_0)=dot{Omega_k^2}(t_0)/(2Omega_k(t_0)))
only at the initial time. It can therefore evolve through intermediate
intervals with (Omega_k^2<0), while still requiring a real positive
initial frequency and a final positive frequency before assigning an
instantaneous particle number. A new regression test constructs a
smooth expanding background with an intermediate tachyonic canonical
frequency, verifies successful integration, and checks Wronskian
preservation.

This is a linear mode-level capability, not evidence that PTUM's
benchmark realizes such a history. The actual (Phi_{\\rm res})
trajectory and its coupling to the expansion remain to be derived
self-consistently. The branch now contains 51 regression tests; the
latest tests and manuscript changes still await a fresh CI run.


## 41. Final adiabatic particle-basis gate (2026-11-14)

The expanding-background mode solver previously required a positive final
canonical frequency and a conserved canonical Wronskian before reporting
an instantaneous occupation number. That was not sufficient: an oscillator
can have a real positive instantaneous frequency while its frequency is
changing too rapidly for an adiabatic particle basis to be meaningful.

The solver now evaluates the final first-order WKB measure
$|\\dot\\Omega_{k,f}/\\Omega_{k,f}^2|$ from the derivative of the same
canonical-frequency-squared spline used for the initial WKB state. The
default acceptance threshold is 0.1, exposed as
max_final_adiabaticity. A mode occupation is reported only if the final
frequency is positive, this final adiabaticity gate passes, and the
Wronskian remains within tolerance. The finite-band spectrum returns a
NaN density unless every included mode passes all three checks. The
waterfall wrapper and fixed-band resolution helper propagate the gate.

The threshold 0.1 is a numerical reliability criterion, not a physical
constant. A production result must be stable under tightening and varying
this threshold, in addition to solver tolerance, time resolution and
momentum-grid/range convergence.

Two regression tests use a positive but rapidly varying mass history:
the first confirms that the mode occupation is withheld despite a positive
final frequency and valid Wronskian; the second confirms that the
finite-band density is withheld when the included modes have no valid
final adiabatic particle basis. A manuscript regression guards the
corresponding claim boundary.

The preceding workflow 43501562655 passed 72 tests, the four-trajectory
two-scale smoke scan and the LaTeX build. The final-WKB change and its
three new tests bring the branch to 75 tests, but are newer than that
workflow and remain pending fresh CI verification.

The smoke artifact contained only four trajectories. Its two zero-seed
rows remained exact classical invariant controls; its two nonzero-seed
rows were non-quartic or insufficient-oscillation-data. These results
are a smoke-test check only, not evidence for or against the full
100-point parameter grid. No full scan, nonlinear waterfall, relic
abundance, or microscopic proxy-fluid conclusion is claimed.


## 42. 2026-11-14 CI verification and source-regression correction

The final-WKB particle-basis implementation was already documented in
the manuscript with the stronger statement that both the occupation
number and the associated finite-band number density are withheld when
the final WKB or Wronskian validity condition fails. The source regression
still expected the older shorter phrase and therefore failed on workflow
`43580694626` (74 passed, 1 failed). This was a stale test expectation,
not a physical or numerical failure. Commit
`82ab0f26014de58634386efd1d90b635f6ec9e45` aligns the assertion with
the manuscript's actual wording.

The fresh workflow `43580982470` on that head passed:
- 75/75 Python regression tests;
- all four CI smoke integrations (two high-scale and two low-scale);
- the LaTeX build and manuscript PDF upload.

The smoke classifications were, in each scenario, one
`insufficient_oscillation_data` and one `non_quartic`. Thus the smoke
run demonstrates successful integration and fail-closed classification,
not quartic-fluid production. The LaTeX log had no Overfull \\hbox
warnings, but retained Underfull \\hbox and two float-placement
warnings; the manuscript build is successful but not warning-free.

The complete 100-trajectory scan and its artifact are still outstanding.
No output-grid or solver-tolerance convergence, physical inhomogeneous
waterfall completion, backreaction, rescattering, relic abundance, or
entropy dilution is claimed from this workflow.


## 43. Latest-head CI and isolated full-scan record (2026-11-14)

After the three scientific-status documents were synchronized, PR head
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a` passed workflow
`43582227619`: 75 Python tests passed, all four two-scale smoke
integrations succeeded, and the manuscript PDF compiled and uploaded.
Each smoke scenario still classified one trajectory as
`insufficient_oscillation_data` and one as `non_quartic`; this does
not demonstrate a quartic proxy-fluid phase.

The LaTeX log has no reported Overfull \\hbox warnings or errors, but
does contain numerous Underfull \\hbox warnings and two distinct
float-placement warnings. The build is successful, not warning-free.

The isolated full-scan branch
`ptum/full-scan-2026-11-14-r2` was created from that PR head and
received manifest commit
`c101aaed58e44c9f0159ebb806a84d670cd892e2`. The manifest fixes the
100-row 5x5x2-by-two-scales profile, 4001 output samples, 20 mu^-1
duration, exact epsilon_H threshold, and integrated single-field fuel
velocity prescription. No completed workflow result or final 100-row
artifact has yet been verified; no full-scan regime claim is made.


## 44. 2026-11-14 tilted-domain-wall diagnostic return-value correction

The first CI run after adding the moderate-bias stationary-potential
regression exposed an API defect, not a physics failure:
`domain_wall_bias_diagnostics` called the exact stationary solver but
omitted its `true_minimum` and `false_minimum` values from the returned
dictionary. Workflow `43584145515` therefore reported 82 passed and
one failed with `KeyError: 'true_minimum'`.

The public diagnostic now returns both dimensionful minima when the
metastable vacuum exists, and returns `None` for both at/above the
spinodal. The regression checks that the dimensionless roots satisfy
`y^3-y-b=0), that both have positive local curvature
`3y^2-1>0`, and that their direct potential difference matches the
cancellation-safe analytic vacuum bias. The spinodal regression checks
that neither minimum is reported after metastability is lost.

This change makes the existing analytic calculation inspectable; it
does not promote the physical defect gate. The renormalized SM
condensate, Wilson coefficient, thermal history, defect formation,
network evolution, annihilation and backreaction remain uncomputed.
The correction and tests await a fresh CI run.


## 45. 2026-11-14 fresh CI verification of defect diagnostics

After the stationary-minimum API correction, workflow `43585095937`
passed on commit `3f78946668bd43d59953ead562abf158105ec595`:
83 Python tests passed; the four-trajectory, two-scale smoke scan
completed with four successful integrations and no integration
failures; and the 42-page manuscript PDF compiled and uploaded.
The smoke classifications remained one
`insufficient_oscillation_data` and one `non_quartic` in each
scenario. These are software and homogeneous-background checks only.

The final LaTeX pass has no Overfull `\\hbox` or unresolved-reference
warning, but retains numerous Underfull `\\hbox` warnings and two
float-placement warnings. Gate 10 remains PARTIAL.

The isolated 100-trajectory workflow `43582371029` is still running
on `ptum/full-scan-2026-11-14-r2`, based on the earlier
`d4f5f8b37a526c6fba35d19cb9c0396710da2e1a` source. No full-scan
artifact has been inspected. Because the current PR head includes
later defect-diagnostic changes, scan-source equivalence must be
checked before treating that run as evidence.


## 46. 2026-11-14 conditional ideal-gas thermal fermion bias

Added `thermal_dirac_scalar_condensate` and
`thermal_fermion_bias` to `ptum_defects.py`. For a free equilibrium
Dirac species with degeneracy $4N_c$, fixed broken-phase mass $m_f$,
and the diagonal real mass-basis coupling
$y_{\psi f}^{\rm eff}=\operatorname{Re}[(C_f)_{ii}]v_H/(\sqrt2\Lambda)$
in $m_f(\psi)=m_f+y_{\psi f}^{\rm eff}\psi$, the
zero-temperature-subtracted
thermal condensate is evaluated from the Fermi-Dirac integral
[
\Delta_T\langle\bar f f\rangle
=\frac{4N_c m_fT^2}{2\pi^2}
\int_0^\infty dx\,
\frac{x^2}{\sqrt{x^2+(m_f/T)^2}
[\exp(\sqrt{x^2+(m_f/T)^2})+1]}.
]
For $m_f\ll T$ it tends to $N_cm_fT^2/6$. Since the thermal
free-energy linear coefficient is
$+\sum_f y_{\psi f}\Delta_T\langle\bar f f\rangle\,\psi$,
the code returns
$\epsilon_{\rm bias}^{(T)}
=-\sum_f y_{\psi f}\Delta_T\langle\bar f f\rangle$
for the convention $V_{\rm bias}=-\epsilon_{\rm bias}\psi$.

Six regression tests cover the relativistic limit, mass/temperature
scaling, zero limits, signed-coupling cancellation, input validation,
and the manuscript's explicit assumptions. The manuscript now gives
the same integral and caveat.

This is a conditional one-loop ideal-gas estimate only. It assumes
equilibrium, fixed broken-phase masses and Higgs expectation value,
and zero chemical potential; it omits gauge/QCD corrections, thermal
masses, the electroweak crossover, non-equilibrium production, and
the renormalized T=0 condensate. No PTUM Wilson coefficients, cutoff
or thermal history are assigned. The result does not predict the
actual wall bias, network evolution, annihilation or BBN safety.
The new tests and manuscript build await fresh CI.


## 47. 2026-11-14 thermal-bias LaTeX line-break correction

The first complete build after adding the thermal ideal-gas bias
equations passed, but its log audit found an Overfull `\\hbox`
at the long inline expression for
$y_{\psi f}^{\rm eff}=\operatorname{Re}[(C_f)_{ii}]v_H/(\sqrt2\Lambda)$.
The coupling was moved into a display equation in commit
`d9455781f0a643f6c1b2badc199bf2fb6fedcab7`. A new LaTeX build is
required to verify that the overfull line is gone. The preceding
build still had numerous Underfull `\\hbox` and two float-placement
warnings; no warning-free claim is made.



## 48. 2026-11-15 deterministic solver-work guard and scan observability

The isolated full-scan workflow `43582371029` on the earlier source
head `d4f5f8b37a526c6fba35d19cb9c0396710da2e1a` reached 20 of 100
trajectories and was then terminated by a hosted-runner shutdown
signal. The full-scan step was cancelled and no JSON artifact was
uploaded. This is not a numerical result and does not support any
physical regime claim.

To prevent a single pathological adaptive solve from occupying the
runner indefinitely, `run_simulation` now counts DOP853 RHS calls and
raises `RHSWorkBudgetExceeded` after a configurable default of
100000 evaluations. `run_parameter_scan` catches this as a failed
trajectory, records the exact attempted count and limit, and continues
with the remaining initial conditions. Successful rows also preserve
DOP853 `nfev`, `njev`, `nlu`, `rtol`, and `atol`. Strict-JSON
summaries now retain the solver statistics for both successful and
failed rows. Each trajectory's initial conditions are printed before
integration so a stalled or expensive row can be identified.

This cap is an engineering resource guard, not a physical cutoff,
solver tolerance, or evidence of convergence. A budget-exhausted
trajectory remains failed and prevents the full scan from passing.
The solver tolerances remain `rtol=1e-9` and `atol=1e-12`.

Three regressions cover successful solver-stat reporting, deterministic
budget exhaustion at an exact evaluation count, and preservation of
the failed row in strict JSON. The latest completed PR workflow
`43701174233` on commit
`5379ec8a2e85e875c9819121b0409ea454cf99e9` passed **93 tests**,
all four smoke integrations, and the LaTeX build. The smoke scan still
returns one `insufficient_oscillation_data` and one `non_quartic`
row per scenario; no quartic regime is established.

The thermal Dirac-condensate integral was split over two aligned rows
and two tables were changed to flexible `[htbp]` placement. In the
fresh 42-page build there are no Overfull `\\hbox` or float-placement
warnings. Underfull `\\hbox` warnings remain; the initial LaTeX
pass reports citations before subsequent `latexmk` passes resolve
them, and the final pass has no unresolved-reference warning.

A fresh 100-trajectory run is queued as workflow `43701420639` on
commit `af9724092c94d8469fcf23a87f29438b2cf8c58a`. It was still
running at this checkpoint, so no full-scan outcome is claimed.


## 49. 2026-11-15 full-scan artifact audit and regression-fixture repair

Workflow 43701420639 uploaded a 100-row strict-JSON artifact with
SHA-256
4f98f4320ff5cfccb2917607270a8be86ee20eb9ed21b1e71ec8441660ce5722.
The workflow log confirms that this attempt used DOP853 and a
100000-RHS budget. It contains 97 successful integrations and three
failures: two rows exhausted the budget at 100001 attempted calls,
and one low-scale row developed non-finite total density. Among the
97 successful rows, the high-scale case has 47 non_quartic and two
insufficient_oscillation_data classifications; the low-scale case
has 41 non_quartic and seven insufficient_oscillation_data
classifications. None has quartic_achieved=true. The JSON contains
no NaN or Infinity tokens.

This is not an accepted current-source scan. The source comparison
from af9724092c94d8469fcf23a87f29438b2cf8c58a to
ca053f58e3713b274e22f0d69bd5ca89863dab26 spans 21 commits and
modifies both ptum_task1_scan.py and ptum_task1_simulation.py, as
well as the workflow and tests. The DOP853 artifact is therefore
kept as a diagnostic record only. A new 100-row run is queued on the
current PR source using Radau, rtol=1e-9, atol=1e-12 and a
1000000-RHS per-trajectory engineering guard (workflow 43703837000).
No current full-scan outcome is claimed until its artifact is
inspected and every integration succeeds.

The CI failure on head f694c1a0f08e28308f7596fa1b7a41246ff4b7c7
was traced to two synthetic successful-scan fixtures that omitted
time-series fields required by save_results. The production schema
was not relaxed. A complete minimal success-row helper was added in
commit ca053f58e3713b274e22f0d69bd5ca89863dab26. The deliberate
overflow warning in the non-finite-state regression was then captured
explicitly with pytest.warns in commit
b0aa8b32c67a90e0981826ac44c7470c37ff7ce4.

Workflow 43703509401 on b0aa8b32c67a90e0981826ac44c7470c37ff7ce4
passed 98 Python tests with no warnings in the pytest summary, all
four smoke integrations, and the 42-page LaTeX PDF build. The smoke
rows remain one insufficient_oscillation_data and one non_quartic
per scenario; they do not establish quartic dynamics. The LaTeX log
has no Overfull hbox or float-placement warnings, but 213 Underfull
hbox messages remain across repeated passes. The final pass has no
unresolved references. Gates 4 and 10 remain PARTIAL; no physical
acceptance gate is promoted by these engineering checks.


## 50. 2026-11-15 correction of primordial mode-spectrum reproducibility claim

The public ptum_inflation_background.py module does reproduce the
eight-point scalar-dominated background scan and first-order
Hubble-flow observables used in the primordial table. The regression
suite checks the eight-row scan, its 60-e-fold termination and key
reference values. The table caption now identifies this as a public,
CI-checked background calculation and explicitly separates it from
the CLASS/Cobaya likelihood analysis.

The manuscript previously described a separate 200-mode
Mukhanov-Sasaki calculation as numerically verified with the public
background script. That was inaccurate: the public script does not
integrate Mukhanov-Sasaki modes, and the mode solver, raw spectra and
numerical outputs are not in the repository. The text now labels the
200-mode result AUTHOR-REPORTED and states the missing reproducibility
artifacts. Gate 9 remains NOT MET. No mode-spectrum or observational
result is promoted by the background-only regression.

## 51. 2026-11-15 current-source Radau scan audit and LaTeX environment repair

The full 100-trajectory Radau run 43703987436 used the current scan
implementation: comparison from its source f16c89d5a5d8b0506c569cc073688cb435494fad
to PR head 31b1beefd1babf81e6293210d8ffe3eba83e9a09 shows only
documentation and main.tex changes, with no changes to the scan
runner, simulation module or workflow. The artifact contains 100
strict-JSON rows and no non-finite numeric values. ZIP SHA-256:
464c73c9907115ce6bc57ec53722fcc4ede4d8f17d0e66db856fcef00f8876a2.
Extracted JSON SHA-256:
b348651738c1a5d35d15432ef2f1d8873ddfa9ea827238f84c1772b6ac1593e3.

The high-scale case has 49 successful integrations (47 non_quartic,
two insufficient_oscillation_data) and one RHS-budget failure. The
low-scale case has 49 successful integrations (42 non_quartic,
seven insufficient_oscillation_data) and one RHS-budget failure.
Both failures occur at psi_init=4.460941604639096e12,
psi_dot_init=0 and phi_offset=2.4014653823994024e16; each reaches
1,000,001 Radau RHS calls against the 1,000,000 guard. None of the
98 successful trajectories passes the joint quartic classifier.
This finite homogeneous post-threshold scan does not establish the
proxy-fluid regime and does not exclude other parameter regions.

The median finite-difference residual normalized by H rho is
3.7233e-2 for the high-scale rows and 4.0332e-6 for the low-scale
rows; the high-scale maximum chain-rule relative residual is
1.6846e-10. Output-grid and solver-tolerance convergence are
therefore still required. No scan convergence or relic-density
claim is made.

Workflow 43704489063 passed 98 Python tests and the four-row smoke
scan but its LaTeX build failed with Improper prevdepth at the
Late-time dark sector section. The cause was an unclosed itemize
environment with no list items in the Mukhanov-Sasaki subsection.
Commit c75b972e9ff14d0b576a9436c0486cf8a6112b84 removes the orphaned
environment and rewrites the subsection so that the 200-mode spectrum
is consistently described as AUTHOR-REPORTED, not independently
reproduced. Commit 68d7a53672bd6a076bfbcd7f4e2828d554c05bfe adds
two regressions: nested LaTeX environment balance and the mode-spectrum
claim boundary. The source now contains 100 test functions. The
fresh Python and LaTeX workflow after these commits remains pending.

### Follow-up to correction 51: LaTeX build and regression assertion

Workflow 43705365503 confirms that the orphaned itemize fix produces
the 42-page manuscript PDF. The final LaTeX pass has no unresolved
citations/references, no Overfull hbox, no float-placement warning
and no Improper prevdepth error. There are still 138 Underfull hbox
messages, so a warning-free typography claim is not made.

The Python job reported 99 passed and one failed out of 100 tests.
The sole failure was a claim-boundary assertion that did not normalize
a phrase split by a source newline. Commit
a5f86d7c8ca746e6948cfa5c391d11a63985ab87 corrects the test to compare
whitespace-normalized text. The new full CI result remains pending.

### Follow-up verification: workflow 43705535067

On PR head 49933f4f1593327845944266e3412e67a3b545f3, all 100 Python
regression tests passed in 12.81 s, the four-row two-scale smoke scan
completed 4/4 integrations, and the 42-page manuscript PDF built and
uploaded. The final LaTeX pass has no unresolved references/citations,
Overfull hbox, float-placement warning or Improper prevdepth error.
There are 138 Underfull hbox messages across the build log. The smoke
classification remains one insufficient_oscillation_data and one
non_quartic per scale; it does not demonstrate quartic dynamics.
The full Radau scan remains a separate 98/100 diagnostic with two
budget-exhausted integrations and no joint-quartic success.

### Follow-up: current Radau scan interpretation in the manuscript

The critical numerical-status paragraph in main.tex now reports the
actual 100-row Radau artifact. There are 98 successful integrations
and two RHS-budget failures. No successful row passes the joint
quartic classifier. The high-scale maximum Q is about 1.002, below
the Q>2 energy-dominance boundary. The low-scale control contains
large-classical-seed rows with Q up to about 11.12, w about 0.363 and
virial ratio about 0.890, but only two half-cycles occur in the final
20 percent, leaving the late-time adiabatic diagnostic unavailable.
This is not a sustained quartic-fluid realization.

The manuscript explicitly distinguishes these transient averages
from a sustained proxy-fluid phase and states that the scan is
homogeneous/post-threshold, not quantum-seeded or inhomogeneous.
A BDF full-scan cross-check with unchanged tolerances and RHS guard
is running on isolated execution PR #5. One new regression guards
the manuscript's current scan-status wording; fresh CI is pending.

### Follow-up: BDF/Radau cross-solver comparison

The isolated BDF full scan (workflow 43705977596) produced 100 strict-JSON
rows, with 98 successful integrations and the same two RHS-budget
failures as the Radau run. All 98 common successful rows have identical
regime labels. Maximum relative differences in final values are
5.99e-7 for Phi, 1.11e-6 for Phi_dot, 4.66e-5 for psi,
2.36e-3 for psi_dot, 6.06e-7 for H, 1.21e-6 for total rho and
2.29e-4 for averaged w. Maximum relative differences in Q, w and
virial classifier diagnostics are 1.27e-5, 1.32e-6 and 3.98e-5.
This is strong cross-method agreement for the successful subset,
not time-grid or tolerance convergence. The two failures remain
unclassified; DOP853 is the next targeted probe.


## 2026-11-15 current-head CI and DOP853 execution isolation

PR #2 workflow 43706959822 completed successfully on source head
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`. The current test file
contains 103 test functions; the Python regression job passed, all
four two-scale smoke integrations passed, and the LaTeX build/PDF
upload passed. The full 100-row scan was skipped in the ordinary PR
workflow. A successful software workflow does not promote the physical
acceptance gates.

The BDF execution PR #5 is closed without merging. Its archived
workflow 43705977596 produced 100 strict-JSON rows: 98 successful
integrations and the same two RHS-budget failures as Radau. All 98
common successful rows have identical regime labels. This supports
cross-solver agreement on the successful subset, but does not establish
solver-tolerance or output-grid convergence.

The earlier DOP853 execution PR #6 is based on the older commit
`4227a3e50e2a0564a44a19dea2338dafa328ca53`, not the current PR #2
head, and its full-scan job failed. Its artifact is retained only as
historical diagnostic evidence.

To make a valid same-source comparison, isolated execution PR #7 was
created directly from current PR #2 head
`bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`. Workflow 43753469944
runs DOP853 on the full 100-row grid with unchanged
`rtol=1e-9`, `atol=1e-12`, 4001 samples over `20 mu^-1`, and
the 1,000,000-RHS per-trajectory guard. At this checkpoint the
workflow is in progress; no result or artifact has been accepted.

No scientific gate is promoted by the 103-test CI run, the four-row
smoke scan, or the running DOP853 workflow. Gates 4 and 10 remain
PARTIAL; Gates 5, 6, 7 and 9 remain NOT MET. PTUM is NOT 10/10.


## 2026-11-15 current-source DOP853 full-scan audit

Workflow 43753469944 on isolated execution PR #7 completed all jobs:
Python regression, four-trajectory smoke scan, LaTeX build, and the
100-trajectory DOP853 scan. The execution branch was created from PR #2
source commit `bebd0bd1e5f75e31d3d0ba8dfe84a9b53293bea0`; the subsequent
PR #2 commits changed only documentation, manuscript text and regression
assertions, not the scan or simulation implementation.

The DOP853 artifact contains exactly 100 strict-JSON rows and no
non-finite JSON constants. ZIP SHA-256:
`3e758909f191c863b358424be0d7d86a253224fe066e3ceaa279368719e39c8b`.
Extracted result JSON SHA-256:
`e848ff87c8fa3741d65f5fd2909d56db4af567a903d4dc05845cb081d175372c`.
All 100 integrations succeeded. The high-scale case has 48
`non_quartic` and two `insufficient_oscillation_data` rows; the
low-scale case has 43 `non_quartic` and seven
`insufficient_oscillation_data` rows. No row passes the joint
quartic classifier.

The two rows that exhausted the 1,000,000-RHS guard under both Radau
and BDF complete under DOP853 with 7,718 and 1,334 RHS evaluations.
Both are classified `non_quartic` by DOP853. Radau and BDF therefore
have 98 successful rows each, while DOP853 completes the full 100-row
grid. The two DOP853-only rows have no successful implicit-solver
counterpart and are not independently cross-validated.

The three artifacts use the same 100-row initial-condition grid.
Across the 98 rows successful under all three methods, all regime
labels are identical. DOP853 versus Radau maximum relative differences
are 3.16e-9 in Phi, 1.18e-7 in Phi_dot, 4.77e-7 in psi,
9.12e-6 in psi_dot, 2.86e-10 in H and 5.72e-10 in total density.
Maximum relative differences in Q, averaged w and virial diagnostics
are 5.95e-8, 1.81e-8 and 1.77e-7. These are cross-method differences
on the common successful subset, not tolerance or output-grid
convergence. In particular, the two DOP853-only trajectories still
require a tighter-tolerance self-convergence check.

The result closes the all-100-success execution issue for this
declared homogeneous post-threshold grid under DOP853. It does not
establish a quartic-fluid realization, an inhomogeneous waterfall,
backreaction, relic abundance or observational validity. Gates 4 and
10 remain PARTIAL; Gates 5, 6, 7 and 9 remain NOT MET.


## 2026-11-15 latest manuscript and regression verification

Latest-content CI verification workflow 43754277984 (execution-only
PR #8) passed all 103 tests and the four-trajectory smoke scan. The
LaTeX build completed and produced a 42-page PDF. In the final
LaTeX pass there were zero unresolved references, zero unresolved
citations and zero Overfull hboxes; 73 Underfull hbox warnings
remain. The build is successful but not warning-free. The CI-only
PR was closed without merging after verification.


## 2026-11-15 targeted DOP853 convergence audit

The isolated convergence workflow 43754922200 completed 36/36
integrations for four representative trajectories. The probe includes
the two DOP853-only rows that previously exhausted the Radau/BDF RHS
guard and two high-Q controls. It evaluates three tolerance pairs
(1e-9/1e-12, 1e-10/1e-13, 1e-11/1e-14) and seven output grids from
4,001 through 256,001 points.

All four cases passed the explicitly encoded *targeted* numerical
stability limits: final-state relative differences <=1e-6,
classification-diagnostic relative differences <=1e-5, and absolute
changes <=1e-3 for Q_final, w_final, virial_final and the maximum
finite-difference continuity diagnostic across the final grid
doubling 128,001 -> 256,001. All four regime labels, quartic flags
and late-half-cycle counts remained unchanged. The largest observed
final-state relative difference was 4.75e-7; the largest
classification-diagnostic relative difference was 3.48e-7.
Maximum absolute changes across the final grid doubling were
7.57e-4 (Q_final), 2.57e-4 (w_final), 2.25e-4 (virial_final) and
6.05e-4 (finite-difference continuity diagnostic).

Artifact ZIP SHA-256:
`d4f80abf0e2705d3d019e67855592efaf7242ee96a90f970798119748a6bfe51`.
Extracted strict-JSON SHA-256:
`f99e7da8644c399e3bb5ff6d6b08cbffe272ab75c99faad311689fa283a71899`.

This result applies only to four selected trajectories and does not
establish convergence of the full 100-row scan. Gate 4 remains PARTIAL.
The workflow also passed 107 regression tests and the LaTeX build;
74 Underfull hbox warnings remain in the final LaTeX pass.


## 2026-11-16 current verification boundary

Workflow `43759304001` completed on pre-opt-in head
`bc1f6dafb689be427631ae3baa79692b9fde1694`: 108 Python tests passed,
the two-scale smoke scan completed 4/4 trajectories with zero failed
integrations, and the manuscript built to a 42-page PDF. The final
LaTeX pass still reports 73 Underfull hbox warnings and one Overfull
hbox at source line 1937. The build succeeded, but is not warning-free.

The full 100-row scan and targeted convergence jobs were skipped in
that run. PR #2 now carries the explicit `[FULL-SCAN]` opt-in. Commit
`37b48c41b8342597e910f03e7717c70463fba93b` enables the existing
four-case convergence job for that PR opt-in; commit
`c5b3c95e065999dc719b1052db66e3c9855d2d82` adds a regression guard.
Fresh CI on the new head is pending. No full-scan, full-grid
convergence, inhomogeneous waterfall, relic, or observational claim
is inferred from the preceding smoke run.


## 2026-11-16 dense-cycle estimator integrated into the canonical branch

The dense-output half-cycle estimator previously isolated on PR #11 has
been ported into PR #2. The pre-change PR #2 simulation source matched
the estimator's base blob exactly, so this port does not discard any
intervening PR #2 simulation edits.

The reported cycle diagnostics now come from adaptive quadrature over
the ODE dense interpolant, with turning-point brackets seeded from the
accepted solver mesh and refined until successive root sets agree.
The integrated moments are used for Q, quartic virial, excitation-sector
w and physical mean H. The previous sampled Q/virial/w arrays remain
available as independent numerical cross-checks. The late-time
classifier and H/omega diagnostic share physical-time cycle windows.

The port also adds the chunked strict-JSON 100-row 256,001-point
refined-grid driver. The PR #2 full-scan workflow now schedules this
driver alongside the 4,001-point baseline and the existing four-case
targeted convergence probe. All new dense-estimator regressions and
the high-resolution scan remain unverified until the current-head CI
and artifacts complete. No convergence tolerance has been relaxed and
no physical acceptance gate is promoted by implementation alone.


## 2026-11-16 dense-cycle CI failure and numerical correction

Workflow `43841837289` exposed seven failures after the dense-output
port: five compatibility tests showed that empty dense-cycle arrays
were incorrectly accepted as a valid dense branch, and two harmonic
oracles showed that roundoff in the final (sin(4pi)) endpoint could
drop the last turning point.

The classifier now requires a nonempty dense-cycle record before using
that branch. Root detection snaps only endpoint (dotpsi) values
within a scale-relative machine-roundoff bound to zero. This restores
the sampled compatibility fallback and preserves analytic endpoint
turning points without weakening the root-refinement or physical
classification thresholds. Two focused regressions were added. The
corrected head remains unverified until fresh CI completes.


## 2026-11-16 pre-fix scan evidence and interpretation

The pre-fix dense-estimator workflow `43841837289` completed the
100-row 4,001-point DOP853 scan with 100/100 successful integrations
and zero failures. Its provisional classifier returned 5 quartic,
89 non-quartic and 6 insufficient rows. All five quartic rows were
clustered at the largest classical seed, (5psi_0), in the
low-scale underdamped control with the smallest threshold offset.
They had only four or five late half-cycles, so they do not establish
a robust attractor or a quantum-vacuum-seeded regime.

The four-case targeted convergence probe completed 36/36 integrations.
Across the tested output grids and three solver tolerances, all four
cases met the declared targeted limits: the maximum finite-difference
continuity-residual grid change was (6.043	imes10^{-4}), maximum
classification tolerance difference (9.38	imes10^{-7}), and maximum
final-state relative difference (4.75	imes10^{-7}). This evidence
covers four selected cases only, not all 100 initial conditions.

These numerical jobs ran before the Python suite exposed seven
regressions. The endpoint-root and empty-cycle fallback fixes are in
`a172c6a72121d63ba8391af9d35ba8d225e39403`; a fresh full scan and
targeted probe on the corrected head are required. The 100-row
256,001-point dense-estimator job from the pre-fix run was still
running at the time of this record.


## 2026-11-16 analytic quadrature oracle made dimensionally consistent

The latest corrected-head CI had 130 passes and one failure. The
remaining synthetic harmonic test mixed a time scale (mu=1) or 2.5
with a PTUM parameter set whose actual tachyonic scale was about
(1.41	imes10^{12}) GeV. The kinetic moment was consequently
(O(10^{-28})) of the potential scale, making the worst-component
relative quadrature error large. The error estimator was not relaxed.
The output-grid oracle now uses (mu=mathrm{params.mu}); the
non-unit-(mu) oracle selects (m_psi) to make (mu=2.5). Strict
quadrature assertions remain in place. Fresh CI is required.


## 2026-11-16 full 100-row dense output-grid result

The corrected simulation implementation completed a 100-row,
256,001-point DOP853 scan with 100/100 successful rows, 100 unique keys
and a complete checkpoint. The artifact SHA-256 is
`5408e45ce71558474f21d16ffae92024264108cacac3d415d142240d0b915890`.

All 100 rows matched the 4,001-point baseline. Final states
((Phi,dotPhi,psi,dotpsi,H,ho)), Q, w, quartic virial ratios,
regime labels and quartic flags were identical at reported precision.
The analytic continuity-residual maximum differed by at most
(2.98	imes10^{-10}). The finite-difference continuity residual
maximum decreased from (3.7234	imes10^{-2}) to
(6.0499	imes10^{-4}), a 61.5-fold reduction. The maximum dense
quadrature relative-error estimate was (5.97	imes10^{-6}).

The four-case tolerance/output-grid probe also passed 36/36 runs, with
maximum classification tolerance difference (9.38	imes10^{-7}) and
maximum final-state relative difference (4.75	imes10^{-7}). This is
not full 100-row solver-tolerance convergence.

The only remaining Python failure in workflow `43842597075` was a
dimensionally inconsistent synthetic harmonic fixture. It used a time
scale unrelated to the parameter-derived (mu), making its kinetic
moment negligible relative to the potential scale. The fixture was
corrected in `7af32e39757f4b4c8cd78f2bda0b1eed9d83d345`; fresh CI is
required. The five quartic classifications remain concentrated at
the largest classical seed and do not establish quantum-seeded
waterfall dynamics or a robust attractor.


## 2026-11-17 paired numerical-convergence correction

The current PR-head workflow 43843783240 passed 131 Python tests,
the 4/4 smoke scan, the 100-row 4,001-point baseline, the 100-row
256,001-point dense scan, and the four-case 36/36 tolerance probe.
The extracted JSON artifacts were parsed with non-finite JSON constants
rejected.

A row-key join across the two separate full scans found unchanged
classification labels and very small cycle-diagnostic differences
(maximum absolute differences: Q 2.01e-9, averaged w 2.00e-10,
quartic virial 1.39e-10). However, the jobs recomputed the exact
inflation endpoint independently. Their Phi_c/M_Pl values differ by
about 2.3e-15 relatively, so the actual initial conditions are not
bitwise identical. This must not be presented as a pure same-input
output-grid convergence proof. The maximum relative final-state
differences range from 2.86e-13 (Phi) to 8.32e-8 (psi_dot).

The finite-difference continuity residual maximum decreases from
3.7234e-2 at 4,001 points to 6.0499e-4 at 256,001 points, while
the chain-rule residual diagnostic differs by at most 3.87e-10.
These are separate diagnostics. The dense quadrature relative-error
estimate is at most 5.97e-6.

A paired 400-run study has been added. It constructs the scenario
parameters and initial conditions once, then reuses those exact objects
for 4,001 and 256,001 output points and for the three solver tolerance
levels. It records strict-JSON checkpoints and compares all 100 rows.
This paired study awaits fresh CI. No Gate 4 promotion is made yet.


## 2026-11-17 manuscript equation line-wrap correction

The complex-Higgs reheating equation was reformatted into an aligned
two-line display. The derivative source was moved algebraically to the
right-hand side; the field equation and its interaction signs are
unchanged. A regression assertion guards the aligned display and the
full derivative operator. The previous CI had one Overfull hbox at
source line 1937; a fresh LaTeX build is required to verify that this
specific warning is removed. Underfull hbox warnings have not yet been
resolved.
