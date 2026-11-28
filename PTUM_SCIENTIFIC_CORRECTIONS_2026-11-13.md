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


## 2026-11-17 CI audit: paired study and Higgs-source display

The first paired-study workflow, 44056098156, completed its 100-row
4,001-point baseline (100/100 integrations, zero failures) and its
targeted four-case convergence probe (36/36, pass). The baseline
classifications were 89 non-quartic, five quartic and six
insufficient-oscillation-data. All five quartic cases were confined to
the low-scale control at the largest classical seed and smallest
threshold offset, with only four or five late half-cycles. They do not
establish a quantum-seeded attractor.

The paired 400-integration identical-input study was still running
when this record was written; its outcome is deliberately not inferred.
The Python job had 134 passes and two stale source-guard failures. One
guard used doubled literal backslashes after the Higgs equation was
reflowed; the other expected the old convergence-driver filename.
Those assertions were corrected, and a construction-level regression
now checks 100 unique row keys, shared parameter-object identity, the
4,001/256,001 grids and all three tolerance levels.

The same workflow built the 42-page PDF, but the final compile log
still contained one 40.16039 pt Overfull hbox at source line 1939 and
73 Underfull hbox warnings. The prior source reflow did not resolve
the overfull warning. The displayed Higgs equation is now written as
...=J_H, with the two derivative contributions defining J_H
on a separate aligned display. This preserves the variational equation
and signs while reducing the equation width. The next CI LaTeX log
must verify the result; no warning-free build is claimed.


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


## 2026-11-17 chiral-SM versus toy-coupling distinction

The generic \(\psi\bar f f\) Dirac example in the reheating-current
discussion is now explicitly labelled as a vector-like toy coupling,
not as the PTUM chiral Standard Model interaction. The latter remains
the gauge-invariant dimension-five operator
\(\psi\mathcal O_{\rm SM}/\Lambda\), with the chiral multiplets and
Hilbert tensor defined in the curved-space SM section. A separate
real-scalar portal example is also explicitly identified as a toy
theory rather than the actual Higgs-doublet portal.

This removes a contradictory sentence that incorrectly said the
explicit SM action and Hilbert tensor were missing. It does not add
SM dynamics, numerical conservation evidence, or reheating rates.
Gate 3 remains PARTIAL.


## 2026-11-18 paired tolerance study: forensic analysis and successive-refinement method

Workflow 44063032840 completed the five-profile paired study with 500/500 successful integrations, 100 unique shared-input rows per profile, zero integration failures and 400 comparisons. The original gate returned false because only 281/300 solver-tolerance comparisons met the fixed coarsest-reference limits. This result was not waived.

The strict-JSON artifact was downloaded and independently parsed. ZIP SHA-256:
43fc944f12866c0e74bc079b40a521dab863655215cfb91b2b0950f20748a119.
Extracted JSON SHA-256:
c01e03bdbf1de0bcb3c801488a60dd77f8d2a83d9c6144a42194e3b53b735a9e.

A row-by-row successive-pair reanalysis shows:
- Maximum state-relative differences: 8.079e-6, 1.057e-6 and 1.629e-7 across the three adjacent tolerance refinements.
- All six state-component maximum error envelopes decrease monotonically.
- Maximum natural-scale normalized absolute classification differences: 5.091e-9, 3.960e-10 and 6.646e-11; every diagnostic envelope decreases monotonically.
- All classification flags and metric-availability states agree for all 100 rows.
- Chain-rule residual differences remain below 3.93e-10.
- Finite-difference residual differences decrease from 1.61e-5 to 3.86e-6 to 1.66e-7.
- The finest adjacent tolerance pair passes all 100 rows under the existing 1e-6 state, 1e-5 dimensionless-diagnostic, 1e-8 chain-rule and 1e-3 finite-difference limits.

The former comparison divided every dimensionless classification difference by the magnitude of that observable. This made w near zero ill-conditioned: a roughly 1e-10 absolute change could appear as a 4.38e-5 relative change. The comparator now records that relative quantity diagnostically but uses abs(a-b)/max(1,abs(a),abs(b)) for acceptance of dimensionless classification observables.

The paired study now compares each tolerance profile with its immediately preceding refinement. It requires every state and classification error envelope to decrease monotonically, unchanged flags and metric availability, passing conservation diagnostics, and all rows passing the finest adjacent pair. Intermediate comparisons remain visible and can individually exceed the final tolerance; they are not discarded or relabelled as passes.

Commit f546728c02e0b3f10e9970ca55d63c34166468ba implements the revised comparator and JSON schema v2. Commit 44309ff9091426787102b60614c3f291845854c4 adds regressions for near-zero w normalization, monotonic error envelopes and fail-closed final-pair checks. Both are newer than workflow 44063032840. The revised code and tests await a fresh exact-head CI run; no new pass is claimed. This analysis concerns only the homogeneous post-threshold background scan.


## 2026-11-18 exact chiral-SM gauge-anomaly audit

The machine-readable chiral-SM representation registry now computes the perturbative gauge-anomaly sums per generation in exact rational arithmetic. Right-handed fields are converted to left-handed charge conjugates before summing. The checked coefficients are SU(3)^3, SU(3)^2 U(1)_Y, SU(2)^2 U(1)_Y, U(1)_Y^3 and mixed gravitational-U(1)_Y; all vanish exactly. The global SU(2) Witten condition is also checked: four left-handed weak doublets per generation and twelve across three generations, so the total is even.

Commit 1f2f29cbd2f90d135750936a7c32a5c9c0a02ced adds gauge_anomaly_audit and includes it in validate_action_registry. Commit 30650e05f7862b6d02f2ecbf2cdd8b2682b0fe77 adds an exact-Fraction regression test. This verifies anomaly cancellation for the declared minimal chiral-SM field content only. It is not a UV completion, a loop-level PTUM calculation, or evidence for the unresolved inhomogeneous waterfall.


## 2026-11-18 manuscript-level chiral-SM anomaly derivation

Commit 63955448934fae2ab727d54f82a350273455bb63 adds the exact per-generation chiral-SM anomaly sums to main.tex. Right-handed fields are rewritten as left-handed charge conjugates, with the stated Dynkin and cubic-index normalizations. The manuscript displays the SU(3)^3, SU(3)^2 U(1)_Y, SU(2)^2 U(1)_Y, U(1)_Y^3 and mixed gravitational-U(1)_Y cancellations, and explains that the twelve weak doublets across three generations evade the global SU(2) Witten anomaly. Commit 0acac9613abccb916810e6ac7bdd11af6bad67f3 adds a source regression. The manuscript and exact-Fraction code audit now independently present the same representation-level result. No PTUM UV completion or quantum waterfall result is implied; the latest exact-head LaTeX and Python CI is pending.


## 2026-11-18 optional convergence-metric availability

The preserved paired-study JSON reports quadratic_virial_final as unavailable in all 100 rows of every refined-grid/tolerance profile. Q_final, w_final and virial_final are available for 94 rows per profile; H_over_omega_max is available for 73. The successive-refinement summary now exposes availability counts, marks a metric consistently unavailable only when it is absent at every refinement, and does not silently treat it as measured. Per-row availability must still match between adjacent profiles, and every state component must be present in every row at every refinement.

Commit 3a8b6b557e2733163e0cf672b16e81174a8697b6 adds explicit availability reporting and fail-closed state completeness. Commit a597cc157505297b82e70387bef7a4b8fc83f598 tests both consistent unavailability and a missing intermediate state component. This does not close the missing quadratic-virial measurement or any proxy-fluid evidence gap. The new exact-head CI has not yet completed.


## 2026-11-18 explicit full-scan CI trigger and availability completeness

The paired convergence summary now reports per-diagnostic availability. The quadratic virial metric is absent in all 100 rows of all four refined-grid/tolerance profiles; it is explicitly listed as consistently unavailable, not presented as a measured converged quantity. Q, w and virial are available in 94 rows per profile and H_over_omega in 73. Adjacent-profile availability must match, and all six state components must be present in every row at every refinement. Regressions verify that a missing intermediate state component fails the summary while a consistently unavailable optional diagnostic is reported transparently.

Commit 529e02f7188e02229dd01c8c45f857d985764418 adds push triggers for the authorized branch. A normal push runs short regression/smoke/LaTeX CI; a commit message explicitly containing [FULL-SCAN] also runs the full baseline, targeted probe and paired 500-integration study. The full-scan concurrency group is isolated from ordinary commits. Commit 4daed65a0ab1e47970714dd0d99cffcfff2bd352 guards these conditions with regression assertions. The acceptance document is updated in commit f8ad891887c71179d3cf8a7173fe961fba4d2423, whose [FULL-SCAN] message triggers the first exact-head run of the revised code. No result is claimed before inspecting that run.


## 2026-11-19 exact-head paired convergence verification

Workflow 44280971987 on head
1c975a73c7e7daa17c01adffe0fd19d929e8d7bb completed all five jobs
successfully. The Python suite passed 146 tests; the smoke scan passed
4/4; the 100-row baseline passed 100/100; the targeted convergence probe
passed 36/36; and the paired study completed 500/500 integrations and
400/400 comparisons with full_study_pass=true. Every one of the five
paired profiles contains 100 unique shared-input rows and there were no
integration failures.

The 4,001-to-256,001 output-grid comparison preserved all final states
and classification flags in all 100 rows. The independently computed
finite-difference continuity residual maximum fell from 3.7233747e-2 to
6.0499428e-4. Post-hoc paired-row analysis gives a minimum reduction factor
of 1.3797 and a median observed order of 0.9906 for the 64-fold spacing
refinement. Solver tolerance refinements produced 98/100, 99/100 and
100/100 strict comparisons. All six state-component error envelopes and
all available normalized classification-diagnostic envelopes decrease
monotonically; the finest adjacent pair has maximum state-relative error
1.6279e-7, maximum normalized classification difference 6.6461e-11,
maximum chain-rule residual difference 1.5666e-10 and maximum
finite-difference residual difference 1.8113e-7. The prior 281/300
fixed-reference failure remains a historical failed criterion; it is not
retroactively called a pass.

The 100-row baseline has 89 non-quartic, 6 insufficient-oscillation and
5 quartic classifications. The five quartic labels are confined to the
low-scale underdamped control. The zero-seed rows are exact classical
invariant controls, not quantum vacuum seeds. All final H and rho values
are finite and positive, and the RHS rejects non-positive total density
at every evaluation. Gate 4 is therefore MET for the homogeneous
post-threshold two-field background domain only. Gates 2 and 5 remain
unmet/partial as previously stated.

Artifact ZIP SHA-256:
f4d6566db7984c83f3564688a0ceac762dcc4f3ee7905cd0fa0e8a2ed6d25842.
Strict-JSON SHA-256:
800661282f7a5ee0a92d887def3c6f0207028b6992741127f726a1ccdbea3f3c.

## 2026-11-19 conditional real-psi domain-wall benchmark

For the late broken-phase frozen-background limit Phi=0,
mu_eff=m_psi=1e13 GeV and lambda_psi=0.1, the analytic kink tension is
9.42809e39 GeV^3. Using the reduced-Planck radiation Friedmann equation
at T_BBN=5 MeV and g*=10.75 gives H_BBN=1.11474e-23 GeV. With the
scaling-network ansatz rho_wall=A sigma H and A=1, the corresponding
wall-domination scale is H_dom=530.035 GeV. The unbiased network therefore
reaches domination far before BBN in this conditional estimate. The
small-bias linear source needed for annihilation before both is
7.90130e28 GeV^3, or 6.49158e-11 epsilon_crit. A factor-of-two larger
source passes the analytic annihilation-before-domination and BBN checks.

This is not a wall-network simulation. It freezes Phi=0, assumes a scaling
network with A=1, and does not predict the SM-induced bias. The latter
still requires renormalized Wilson coefficients, the finite-temperature
SM expectation value and a self-consistent thermal history. Gate 5
remains NOT MET. The radiation-Hubble helper, benchmark regressions and
manuscript estimate are newer than workflow 44280971987 and await CI.


## 2026-11-19 final-pass LaTeX audit and regression correction

The LaTeX job 135459775171 on commit
82806504c37fe16be97b8c672e13e892a8f1999a completed successfully. The
long anomaly equations were wrapped; the final third pdflatex pass has
zero Overfull hbox warnings and no unresolved reference/citation
warnings. The first pass emitted undefined-reference messages while
writing labels, but these disappeared in the final pass. Seventy-four
Underfull hbox warnings remain in the final pass, including several
badness-10000 paragraphs, so the manuscript build is successful but not
warning-free.

The Python run on that commit reported 149 passed and one failed. The
failure was a source-text assertion expecting the phrase
'unbiased real-psi benchmark', while the manuscript accurately said
'For a conditional benchmark'. The test is corrected to assert the
actual wording and the existing scientific caveats; no numerical
threshold or physical criterion was weakened. The next exact-head CI
must confirm this correction.


## 2026-11-19 domain-wall area-factor threshold

For the real-$\\psi$ double-well scaling ansatz
$\\rho_{\\rm wall}\\simeq\\mathcal A\\sigma_{\\rm wall}H$,
the domination scale is
$H_{\\rm dom}=\\mathcal A\\sigma_{\\rm wall}/(3M_{\\rm Pl}^2)$.
Equating this with the radiation-era BBN Hubble scale gives the
critical network area factor
$\\mathcal A_{\\rm crit}=3M_{\\rm Pl}^2H_{\\rm BBN}/\\sigma_{\\rm wall}$.
For $\\mu_{\\rm eff}=10^{13}$ GeV, $\\lambda_\\psi=0.1$,
$T_{\\rm BBN}=5$ MeV and $g_*=10.75$ this is
$2.1031456023788425\\times10^{-26}$. The ratio is exactly
$H_{\\rm dom}/H_{\\rm BBN}=\\mathcal A/\\mathcal A_{\\rm crit}$
within the scaling ansatz. An order-unity area factor therefore gives
domination long before BBN; only an extremely small area factor below
the threshold avoids domination before BBN in this estimate.

The implementation returns the critical area factor, the domination
Hubble ratio and a boolean comparison. Regression tests evaluate the
benchmark and points on both sides of the threshold. This does not
determine the network area factor, establish that a scaling network
forms, or replace nonlinear defect evolution. The actual SM-induced
bias still requires renormalized Wilson coefficients, the finite-T
expectation value of the relevant chiral operator, and a coupled
thermal history. Gate 5 remains NOT MET.

## 2026-11-19 latest CI and source-regression repair

Workflow 44495908967 tested PR head 8a88479a9da61166c490d0fe76e866ce39e6d565.
The LaTeX job passed. The Python job reported 149 passed and one failed:
the manuscript phrase "does not evolve wall formation or annihilation"
was split by a source newline, while the test compared an unnormalized
literal substring. The regression now normalizes whitespace before
checking source prose. This is a test robustness correction only; it
does not change any physical equation, threshold or acceptance limit.
The domain-wall area-factor implementation, manuscript equation and
new tests are newer than this workflow and await exact-head CI.

## 2026-11-19 nonlinear 3-D classical waterfall lattice prototype

A new periodic cubic finite-difference solver, ptum_lattice_waterfall.py,
evolves a homogeneous fuel field and a real inhomogeneous waterfall field
on an expanding FRW background. In natural units and with comoving
coordinates measured in mu^{-1}, its equations are

\[
\ddot\psi+3H\dot\psi-a^{-2}\nabla^2\psi
+m_{\rm eff}^2(\Phi)\psi+\lambda_\psi\psi^3=0,
\]

\[
\ddot\Phi+3H\dot\Phi+V_{{\rm eff},\Phi}
+\frac12\,m_{{\rm eff},\Phi}^2\langle\psi^2\rangle=0,
\]

\[
3M_{\rm Pl}^2H^2=
\frac12\dot\Phi^2+V_{\rm eff}(\Phi)
+\left\langle\frac12\dot\psi^2+
\frac{|\nabla\psi|^2}{2a^2}
+\frac12m_{\rm eff}^2(\Phi)\psi^2
+\frac{\lambda_\psi}{4}\psi^4\right\rangle.
\]

The spatial force and Friedmann source use the same volume average.
The periodic central Laplacian and forward-difference gradient energy
satisfy a discrete integration-by-parts identity. The pressure includes
the isotropic gradient contribution -<|grad psi|^2>/(6a^2).
The nearest-neighbour sign-crossing output is a finite-grid wall-area
density estimator, not the scaling-network area factor used in the
analytic domain-wall sensitivity estimate.

The solver includes classical Phi backreaction, nonlinear mode coupling
and classical rescattering for caller-supplied real psi(x), psi_dot(x).
It deliberately does not label those inputs as quantum vacuum seeds.
There are no adiabatic vacuum counterterms, continuum renormalization,
SM fields, or UV/IR continuum extrapolations. The result is a finite-box
classical prototype only. It does not satisfy Gate 5 and cannot be used
for a quantum-seeded waterfall or relic-abundance claim.

Three regressions were added: the discrete periodic integration-by-parts
identity, agreement of the homogeneous lattice limit with the existing
two-field ODE, and an inhomogeneous run that checks gradient energy,
backreaction metadata and a nonzero sign-crossing wall estimator. These
tests and the new solver await exact-head CI.

The lattice output now also includes an instantaneous RHS-level energy-balance
residual. It differentiates the discrete energy functional by the chain rule
and checks d(rho)/d(tau)+3h(rho+p)=0 using the same discrete Laplacian,
forward-gradient operator and coupling force as the evolution equations.
The homogeneous and inhomogeneous regressions require this normalized
identity residual to remain below 1e-12. This is an internal consistency
check of the finite-lattice equations, not an independent continuum
renormalization or a full-sector Hilbert-tensor conservation proof.

The nearest-neighbour wall estimator now assigns exact-zero lattice sites
to the non-negative phase. This counts a wall passing through a lattice
site on one adjacent link rather than dropping both links. A periodic
planar test checks the expected two crossings per box length. The estimator
remains finite-grid and resolution dependent.

The manuscript appendix has been corrected to distinguish the new limited
classical lattice subsystem from the absent full quantum/four-field
calculation. It now states that the repository exposes a periodic 3-D
real-psi solver with homogeneous-Phi backreaction and classical mode
coupling, while explicitly withholding claims of adiabatic-vacuum seeds,
vacuum renormalization, full SM dynamics, continuum convergence, and
physical defect probabilities. The previous statement that no reviewable
PTUM lattice solver existed is removed. The author-reported lattice/
perturbation results are separately identified as not reproduced by this
limited prototype. A manuscript regression guards these boundaries.

The manuscript appendix now displays the actual equations evolved by the
classical lattice prototype: the inhomogeneous psi equation, the homogeneous
Phi equation with the volume-averaged mass-force term, the Friedmann source,
and the isotropic pressure. It defines the derivative of m_eff^2 and states
the periodic discrete integration-by-parts identity. These equations
describe the two-field classical truncation only; they are not the full
chiral-SM or four-field action. A source regression checks all equation
labels and the explicit quantum/renormalization limitations.

Exact-head workflow 44502156872 on commit 7ce82fec2335300de2074bfb1fa90157bebfd430
ran 156 pytest cases: 155 passed and one failed because an older appendix regression
still required the now-obsolete sentence that no reviewable PTUM lattice
solver existed. The new manuscript correctly acknowledges the classical
prototype, so the stale test was updated in commit
06164c1b7ac9c2333f9e869d7d5bd73223765e9b to require the new scope statement
and reject the obsolete claim. No physical threshold or numerical tolerance
was changed. A fresh exact-head CI run is required; the LaTeX job from
44502156872 was still running when this correction was made.



## 2026-11-20 bare first-order adiabatic-WKB lattice initializer

ptum_lattice_waterfall.py now includes a finite-volume Gaussian
initializer for the free real-psi modes before the tachyonic threshold.
It uses $X=a^{3/2}\psi/\psi_0$ and
$\Omega_k^2=\widehat{k}^2/a^2+m_{\rm eff}^2/\mu^2
-3h'/2-9h^2/4$, where $\widehat{k}^2$ is the eigenvalue of the same
periodic central-difference Laplacian used by the evolution. The
first-order WKB amplitude derivative is included in the field/velocity
cross-covariance. The Fourier normalization is stated explicitly and
real white-noise FFTs enforce Hermitian symmetry.

The sampler refuses $m_{\rm eff}^2\leq0$, non-positive canonical
frequency squared for any lattice mode, or a maximum of
$|\Omega'_k/\Omega_k^2|$ and $|h/\Omega_k|$ above the requested
adiabaticity tolerance. It computes $H,h',h''$ on the homogeneous-Phi
background and therefore omits the vacuum psi backreaction at
initialization. Deterministic seed, dispersion/frequency diagnostics,
adiabaticity summaries, and SHA-256 hashes of the two physical initial
arrays are returned. run_lattice_waterfall can verify this provenance
and labels the input as a bare adiabatic-WKB Gaussian classical sample;
it continues to report quantum_vacuum_seeded=False.

This is not a renormalized quantum initial state or quantum evolution.
The zero-point energy is retained, no vacuum subtraction or
counterterms are applied, and nonlinear classical evolution remains
UV-cutoff dependent. The helper therefore advances the initial-state
bookkeeping but does not close Gate 5. Four regressions test the
lattice dispersion and deterministic seed, tachyonic/non-adiabatic
refusal, ensemble covariance of a non-self-conjugate Fourier mode,
and provenance/hash validation by the lattice solver.


## 2026-11-20 test-field WKB versus bare lattice Friedmann mismatch

The WKB sampler computes $H,h',h''$ on the homogeneous-Phi background
and intentionally omits the bare psi vacuum energy. The subsequent
classical lattice solver, however, includes the sampled bare psi kinetic,
gradient, mass and quartic energy in its Friedmann source. Thus the
test-field H used to define the initial WKB frequencies is not the
same as the solver's initial total H. This is an explicit
non-self-consistency, not a renormalization prescription. The sampler
metadata records both sides, and the solver output reports the
relative initial-H mismatch. A regression requires the total lattice
H to exceed the Phi-only sampler H for the stable positive-energy test
configuration. No physical quantum-waterfall interpretation is allowed
until a consistent renormalized stress tensor and counterterms are
implemented.


## 2026-11-21 bare WKB finite-cutoff stress audit

The new ptum_lattice_uv_audit.py module evaluates the equal-time Gaussian
expectation of the bare lattice stress tensor implied by the existing
first-order WKB sampler. With P_k=lambda_psi/(2 Omega_k),
R_k=lambda_psi Omega_k/2 and velocity shift
nu_k=-(Omega'_k/Omega_k+3h)/2, it computes the field, velocity and
central-difference gradient variances by finite-volume mode sums. The
quartic energy and pressure use the Gaussian Wick identity
<psi^4> = 3 <psi^2>^2 after the dimensionless field normalization.
The audit also computes the bare total Friedmann H and H-prime from this
stress and compares them with the homogeneous-Phi test-field values used
by the sampler.

A fixed-box N=4,6,8,10 CI artifact is intended to quantify how the
unsubtracted bare stress changes with the lattice UV cutoff. This is
diagnostic evidence of cutoff dependence, not a renormalization scheme:
zero-point energy remains, no counterterms are applied, and no physical
continuum or quantum-waterfall prediction is claimed. Gate 5 remains
NOT MET. Exact-head CI and artifact inspection are required before
recording numerical cutoff ratios.


## 2026-11-21 UV-audit first-run correction

The first exact-head audit run (44893207629, commit 86a57c7) correctly
failed before producing an artifact. The implementation had treated the
WKB velocity shift nu_k as a scalar, but the sampler returns one value
per lattice mode. The stress sum now uses the full mode-dependent
nu_k array in <v^2> = V_c^{-1} sum_k [R_k + nu_k^2 P_k] and validates
its shape and finiteness. A manuscript source regression was also
changed to match the actual wording without changing the equations.
The initial run had 161 passing and 3 failing pytest cases. The fix
awaits a fresh exact-head CI run.


## 2026-11-21 exact-head bare WKB stress audit

Workflow 44893367362 on exact head 9d9def8ac72205bc8b912590553fcf0ab38f7f73 completed successfully: 164 Python tests, the four-trajectory/two-scale smoke scan, the four-grid WKB audit and the 44-page LaTeX build passed. The final LaTeX pass had no Overfull hboxes or unresolved references/citations, but retained 77 Underfull hbox warnings.

The fixed-box N=4,6,8,10 bare Gaussian mode sum used L=8 mu^-1 and seed 20261121. The lattice cutoff increased 1.73205 to 4.33013 mu; bare psi stress increased 18.0182-fold (1.20260e48 to 2.16686e49 GeV^4), with end-to-end log slope 3.15553. The bare-total Hubble mismatch increased from 2.13247e-7 to 3.84232e-6. The result is evidence of unsubtracted UV-cutoff dependence only. It is not a renormalized stress tensor or a physical initial state.

Artifact ZIP SHA-256: c4fd531a8de4bd6a31177514afa9e0c7f8f46b67b12cef538315c2b73b643f12.
Strict-JSON SHA-256: 3f24f7c54748b2498d9e3cf57500bd3a738b2b0491cc63ae1a2baf0076f68fbf.

The follow-up audit extends the fixed-box sequence to N=64 and adds a fixed-lattice-spacing, increasing-volume sequence. It is designed to distinguish UV-cutoff growth from finite-volume effects in the equal-time bare Gaussian mode sum. Exact-head CI is required before its results are recorded.


## 2026-11-21 extended bare WKB UV/volume audit

Exact-head workflow 44895764302 on 25b46d4 completed the dedicated
lattice-UV audit and LaTeX build. The audit artifact reports, at fixed
L=8 mu^-1 and seed 20261121, a rise in bare psi stress from
1.2025979590e48 to 2.0040371966e52 GeV^4 as N increases from 4 to 64.
The reported lattice cutoff rises from 1.7320508076 mu to
27.7128129211 mu; the N=32-to-64 log slope is 3.8822733. This is
consistent with the expected leading Lambda^4 zero-point divergence
over the tested finite range, not a renormalized observable.

At fixed dx=mu^-1, the N=8,12,16,24,32,48,64 increasing-volume
sequence has a relative bare-density spread 2.38067e-13, below the
declared 1e-8 finite-volume threshold. This supports finite-volume
stability of the equal-time mode sum at fixed spacing only. The
bare-total/Hubble mismatch relative to the homogeneous-Phi WKB
background grows from 2.13247e-7 to 3.54730e-3 across the fixed-box
sequence, so the test-field initial background becomes increasingly
inconsistent as the retained zero-point UV stress grows.

The artifact ZIP SHA-256 is
1b99b0fa6a9bc6058690aaaf2b9e60312e7e03e43c266210162201ed902d6b1d;
the extracted strict-JSON SHA-256 is
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
The exact-head Python job had 165 passes and one failure caused only by
a stale literal manuscript assertion; the dedicated audit and LaTeX
jobs passed. The 44-page final LaTeX pass had zero Overfull hboxes and
zero unresolved references/citations, with 77 Underfull hbox warnings.
A wording-aligned regression and exact-head rerun are required.


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


## 2026-11-22 tree-level reheating-width correction

The previous reheating discussion displayed only the CP-even broken-phase two-body width and left the electroweak-symmetric dimension-five decay channel unquantified. This was incomplete because the gauge-invariant operator contains the Higgs doublet and, above electroweak symmetry restoration, the Higgs expectation value does not generate the two-body fermion coupling.

The broken-phase interaction is
`-psi bar(f) (y_S + i y_P gamma5) f`. For a real scalar quasiparticle of mass M and beta=(1-4 m_f^2/M^2)^(1/2), the vacuum width is
[
\Gamma_{2}=\frac{N_cM}{8\pi}(y_S^2\beta^3+y_P^2\beta).
]
The pseudoscalar threshold factor is beta, not beta^3. The scalar/pseudoscalar interference vanishes after the spin sum.

In the electroweak-symmetric phase, one massless chiral channel from
`-(C_f/Lambda) psi (bar f_L H f_R) + h.c.` has
[
\sum|\mathcal M|^2=\frac{|C_f|^2s}{\Lambda^2},\quad
\frac{d\Phi_3}{ds}=\frac{M^2-s}{128\pi^3M^2}.
]
The integrated vacuum width is
[
\Gamma_{3,1}=\frac{|C_f|^2M^3}{1536\pi^3\Lambda^2}.
]
An explicit integer multiplicity counts orthogonal colour, weak, flavour and charge-conjugate channels. Contributions leading to the same final state must be added at amplitude level before squaring.

The new `ptum_reheating.py` module implements both limits, channel summation, branching fractions and the sudden-decay estimate using the reduced Planck mass 2.435e18 GeV. It reports conditional 5 MeV BBN, electroweak-crossover and EFT-cutoff checks. It does not include thermal masses, Pauli blocking, Bose enhancement, the Higgs-portal pair channels, nonperturbative preheating, condensate depletion, coupled Boltzmann evolution or entropy production. The Wilson matrices, EFT cutoff and time-dependent quasiparticle mass remain unspecified; therefore no PTUM benchmark decay width or reheating temperature is inferred.

Regression coverage checks the three-body phase-space integral, M^3/Lambda^2/|C|^2/multiplicity scaling, the distinct beta^3 and beta threshold factors, branching normalization, zero-width behavior and manuscript equations. These tests and the manuscript changes postdate the latest successful exact-head CI (44898158765 on be5fb4f) and require a new exact-head run.


## 2026-11-22 exact-head regression and LaTeX overflow audit

PR workflow 45009882010 on head 5c4c1756271063542bffd3d7ac5a4539313fd171 passed 173 pytest cases, the 4/4 two-scale smoke scan and the extended 11-grid bare WKB UV/volume audit. The 45-page manuscript built successfully. The second LaTeX pass had no unresolved references or citations but reported 76 Underfull and three Overfull hboxes. The three overflows were localized to the broken-phase complex Wilson matching display and the two new three-body phase-space/width displays.

Commit 32f94f30504b2db0771c45aed97d4b9e20cb840c rewrites those three displays using aligned multi-line equations. The equations and normalization are unchanged. This formatting correction requires a fresh exact-head LaTeX run; no claim of warning-free output is made yet.


## 2026-11-23 continuous perturbative reheating-fluid benchmark

Added ptum_reheating_history.py, a conditional two-fluid FRW integrator
for a condensate with constant effective w_c and constant perturbative
width Gamma, plus instantly thermalized radiation with constant g_*.
In N=ln(a/a_i), it evolves
d rho_c/dN=-3(1+w_c)rho_c-(Gamma/H)rho_c,
d rho_r/dN=-4rho_r+(Gamma/H)rho_c, and
H^2=(rho_c+rho_r)/(3 Mbar_Pl^2).

The numerical state also accumulates condensate expansion work,
radiation expansion work and transferred energy. Separate integrated
budget residuals verify that the source cancels from the total continuity
equation. The report includes radiation domination, H=Gamma,
T(N), a sampled maximum temperature and S_com(N). At H=Gamma,
the continuous/sudden temperature ratio equals Omega_r^(1/4),
which is tested directly.

Five tests were added for the zero-width limit, redshifting, entropy
conservation without injection, energy-budget closure, the
continuous/sudden identity, edge cases and manuscript equations.
The previous exact-head PR workflow 45010256204 on 50c72c7 passed
173 tests, the 4/4 smoke scan and the extended bare WKB UV/volume
audit; its 45-page LaTeX build had zero Overfull hboxes and zero
unresolved references/citations but 77 Underfull hbox warnings.
That run predates this new module and its tests. A fresh exact-head
workflow is required before the five tests or new manuscript text
are reported as verified.

This calculation is only a constant-fluid phenomenological benchmark.
It does not derive w_c(t) or Gamma(T) from the PTUM action,
does not include a changing thermal equation of state or g_*(T),
and assumes prompt thermalization. It does not establish a PTUM
benchmark reheating temperature, BBN result, full energy partition,
or microscopic entropy history. Gate 8 remains PARTIAL.


## 2026-11-23 continuous reheating solver correction

The first exact-head run for the new continuous two-fluid helper,
workflow 45152225396 on 01dc0b5, reported 176 passes and two failures.
The first exposed a genuine numerical issue: DOP853's dense interpolant
near the terminal, stiff decay tail produced an artificial decrease in
sampled comoving entropy and small late-time density wiggles. The same
equations were independently integrated with BDF at the test settings;
the integrated condensate, radiation and total budget residuals were
below 5e-15 and the sampled entropy was non-decreasing to numerical
precision. The production solver is therefore changed to BDF. The
entropy monotonicity diagnostic tolerance is tightened to 1e-5.

The second failure was only a manuscript-source assertion that searched
for an unescaped filename; main.tex correctly writes the underscores
as TeX escapes. The test now checks the actual TeX spelling. No physical
equation, decay width, or scientific acceptance criterion was weakened.
Fresh exact-head CI is required.


## 2026-11-24: coupled two-scalar heat-kernel UV coefficient

Derived the Gaussian scalar fluctuation Hessian directly from the common
tree-level potential
\(V=V_{\rm eff}(\Phi)+m_{\rm eff}^2(\Phi)\psi^2/2+
\lambda_\psi\psi^4/4\):
\[
\mathcal H=
\begin{pmatrix}
V_{\rm eff}''+c_\psi\psi^2 & 2c_\psi\Phi\psi\\
2c_\psi\Phi\psi & m_{\rm eff}^2+3\lambda_\psi\psi^2
\end{pmatrix},
\qquad c_\psi=\alpha m_\psi^2/E_{\rm th}^2.
\]
For the Euclidean Laplace-type operator
\(\mathcal D_E=-\nabla_E^2\mathbf1+\mathcal H+\Xi R_E\),
the bulk coefficient modulo covariant total derivatives is
\[
a_2^{\rm bulk}=
\frac12\operatorname{tr}
[(\mathcal H+(\Xi-\mathbf1/6)R_E)^2]
+\frac{2}{180}(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2).
\]
The off-diagonal \(\Phi\)-\(\psi\) fluctuation mixing is included.
At \(\psi=0\), the field-dependent \(m_{\rm eff}^4(\Phi)\) term
generates constant, \(\Phi^2\), and \(\Phi^4\) local structures;
the curvature cross term generates \(R_E\) and \(R_E\Phi^2\);
the geometric part requires curvature-squared counterterms. The
non-polynomial \(V_{\rm eff}''(\Phi)^2\) contribution also confirms
that a finite polynomial potential truncation is not closed.

The new ptum_renormalization.py module computes this local coefficient
and exposes its pieces. Regressions cover the flat constant-Hessian
limit, mixed Hessian contribution, conformal maximally symmetric
limit, explicit \(\xi_I\) dependence, and the tachyonic polynomial
limit. It is an algebraic UV-coefficient oracle only. No cutoff,
renormalization scale, finite conditions, pole prefactor, boundary
terms, SM/gauge/fermion or graviton loops, CTP finite part,
renormalized stress tensor or renormalized \(\Phi\) force is supplied.
Gate 5 remains NOT MET; no physical quantum-waterfall claim follows.


## 2026-11-24 exact-head R0 verification

Exact-head workflow 45364524478 on 5f190b87aa7f883ec721fd35e432f76b539c052f
passed 186 Python tests, the 4/4 two-scale smoke scan, and the 11-grid
bare-WKB UV/volume audit. The 46-page PDF built; the final pass retained
79 Underfull hbox warnings, zero Overfull hboxes and zero unresolved
references/citations. Long full scans were skipped by design. The
bare UV audit remains unsubtracted and renormalized=false.


## 2026-11-24 Euclidean scalar one-loop pole normalization

The local two-field bulk heat-kernel coefficient now has an explicit
simple-pole normalization for the declared convention
\(\Gamma_E^{(1)}=+\tfrac12\operatorname{Tr}\ln\mathcal D_E\) and
\(d=4-\epsilon\), \(\epsilon=4-d\):
\[
\frac{\Gamma_{E,\mathrm{div}}^{(1)}}{\int d^4x\sqrt{g_E}}
=-\frac{a_2^{\rm bulk}}{16\pi^2\epsilon},\qquad
\mathcal L_{E,\mathrm{ct}}^{(1)}
=+\frac{a_2^{\rm bulk}}{16\pi^2\epsilon}.
\]
The code returns the coefficients multiplying \(1/\epsilon\) and checks
the cancellation sign. The single-real-scalar flat constant-mass limit
recovers \(\Gamma_{E,\mathrm{div}}^{(1)}/V_4=-m^4/(32\pi^2\epsilon)\).
This fixes only the local scalar bulk pole convention. It does not insert
\(\mu_R\), an \(\overline{\rm MS}\) finite constant, finite matching
conditions, boundary/initial-surface terms, SM/gauge/fermion/graviton
loops, CTP finite parts, or a renormalized stress tensor. The nonlinear
lattice and its initial Friedmann source are unchanged. Gate 5 remains
NOT MET.


## 2026-11-24 field derivatives of the scalar bulk UV pole

For fixed Euclidean curvature invariants, define
\(\mathcal A=\mathcal H+(\Xi-\mathbf1/6)R_E\). The field derivatives
of the common-action Hessian are
\[
\partial_\Phi\mathcal H=
\begin{pmatrix}V_{\rm eff}'''&2c_\psi\psi\\2c_\psi\psi&2c_\psi\Phi\end{pmatrix},
\quad
\partial_\psi\mathcal H=
\begin{pmatrix}2c_\psi\psi&2c_\psi\Phi\\2c_\psi\Phi&6\lambda_\psi\psi\end{pmatrix},
\]
and \(\partial_Ia_2^{\rm bulk}=\operatorname{tr}(\mathcal A\partial_I\mathcal H)\).
The new helper returns the \(\Phi\) and \(\psi\) derivatives of the
bulk pole and cancelling counterterm coefficients. Central-difference
regressions independently check both derivatives, and the \(\psi=0\)
limit checks the real-field \(Z_2\) symmetry.

This is still only a local Euclidean bulk pole derivative at fixed
curvature. It is not a finite renormalized force, does not vary the
metric, and does not produce the renormalized stress tensor or a
real-time CTP equation. The lattice initial condition and Friedmann
source remain unchanged. Gate 5 remains NOT MET.


### Exact-head regression correction

Workflow 45368160766 on head bd9daf3317ccc6ce71bdadb4ddadb5f906ac4d7b
reported 193 passed and one failed. The failure was a source-text
assertion that expected a displayed trace identity to be contiguous
across LaTeX line breaks. The displayed mathematics was correctly
split over aligned lines; the test now checks the trace, matrix product,
and closing delimiter as separate source fragments. The two numerical
field-gradient tests passed in that run. The LaTeX build and bare-WKB
audit also passed. The failed Python job prevented the smoke scan from
running. No equation, physical tolerance, or scientific criterion was
changed; a fresh exact-head run is required.


## 2026-11-24 exact-head field-gradient verification

Workflow 45368498672 on exact head d5649884cae49ede9c4cb83915a3f0a4670d83b2
completed successfully:
- Python regression: 194 passed.
- Two-scale smoke scan: 4/4 successful trajectories, zero failed
  integrations.
- The 11-grid bare-WKB audit produced strict JSON. ZIP SHA-256:
  e435e573863d9ea253646115d5ddf16e6bae614c24f14ac5684ee404931c097c.
  JSON SHA-256:
  260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
  The fixed-box bare-stress ratio remains 16664.2325, the N=32-to-64
  cutoff slope is 3.8822733, and the fixed-spacing volume spread is
  2.38067e-13. The artifact confirms zero-point energy retained,
  vacuum subtraction and counterterms false, and continuum limit false.
- The 46-page PDF built. PDF SHA-256:
  2c6887e02f8563ac37be89d4ed71f7f704729a9a59dc19926425aa983b392b8a.
  Artifact ZIP SHA-256:
  91ec44119e4b702064e5f7396f7a1618a62e0bc97e84bde1ccb88433ac7f6d66.
  Final pass: 80 Underfull hboxes, zero Overfull hboxes, zero unresolved
  references and zero unresolved citations.
- The source-fragment assertion correction did not change the equations,
  tolerances or scientific acceptance criteria.

The two analytic field-gradient regressions passed against independent
central differences and the real-psi Z2 control. This verifies the
derivative of the local scalar bulk pole at fixed curvature only. Gate 5
remains NOT MET; Gate 10 remains PARTIAL.


The matrix row-break escapes in this Markdown derivation were normalized
after review; the Python implementation, manuscript equations and
numerical results are unchanged.



## 2026-11-25 scalar bulk-pole metric variation (pending exact-head CI)

The two-real-scalar bulk heat-kernel coefficient has been decomposed in
four dimensions into
\[
a_2^{\rm bulk}=U_0+FR_E+A R_E^2+B R_{\mu\nu}R^{\mu\nu}
+\frac{N}{180}\mathcal E_4,
\]
with
\[
U_0=\tfrac12\operatorname{tr}(\mathcal H^2),\quad
F=\operatorname{tr}[(\Xi-\tfrac16\mathbf1)\mathcal H],\quad
A=\tfrac12\operatorname{tr}[(\Xi-\tfrac16\mathbf1)^2]-\frac{N}{180},
\quad B=\frac{N}{60}.
\]
Using the inverse-metric variations of \(FR\), \(R^2\), and
\(R_{\mu\nu}R^{\mu\nu}\), the implementation now returns the local
metric Euler derivative of this bulk coefficient. The four-dimensional
Euler density has no bulk variation in exactly four dimensions; its
boundary terms and dimensional-continuation finite contribution are
explicitly omitted. The result is the coefficient of a divergent local
pole, not a renormalized stress tensor.

The function requires a positive-definite Euclidean metric, a Riemann
tensor in \(R_{\mu\alpha\nu\beta}\) slot order, its Ricci contraction,
and caller-supplied \(\Box R_{\mu\nu}\),
\(\nabla_\mu\nabla_\nu R\), and
\(\nabla_\mu\nabla_\nu F\). It validates the algebraic curvature
symmetries, Ricci/scalar contractions and derivative traces before
returning the pole and cancelling-counterterm coefficients. It does not
generate a spacetime geometry or derivative data.

New regressions cover the flat constant-background limit, the
constant-curvature reduction, the conformal-coupling trace identity,
inconsistent curvature-jet rejection, and the manuscript equations.
They are pending a fresh exact-head workflow. No lattice stress,
Friedmann source, initial condition, finite matching condition or
physical prediction has been changed. Gate 5 remains NOT MET; Gate 10
remains PARTIAL.



### Exact-head regression correction for the metric-variation extension

Workflow 45586007724 on head cadcbb316e507c8a9d8c54a94e7ddf13bdd1a619
ran the Python regression suite and reported one failure in the new
fail-closed curvature-input test. The test perturbed a curvature scalar
by an absolute 1 GeV^2 even though the benchmark curvature scale is
of order m_psi^2; that perturbation was smaller than the declared
scale-aware comparison tolerance. This was an inadequate test input,
not a failed physical equation. The test now perturbs by
10^-3 m_psi^2, which is well above the existing relative tolerance,
and the regex assertion is raw-string escaped to avoid a Python
DeprecationWarning. No production tolerance or scientific criterion
was changed. The corrected exact-head run is pending. The same workflow's
bare-WKB UV audit passed; its LaTeX job was still running when inspected.



### Metric-variation tensor audit refinement

The metric-variation helper now also checks the first algebraic Bianchi
identity, in addition to pair antisymmetry, pair exchange and the Ricci
contraction. Its output exposes the volume, field-curvature, R-squared
and Ricci-squared contributions separately, as well as the two curvature
variation tensors. A regression adds a fully antisymmetric four-form
contamination: it preserves pair symmetries and the Ricci contraction
but violates the first Bianchi identity, so the helper must reject it.
The flat-limit test also checks that the reported tensor pieces sum to
the total. These additions are pending exact-head CI.



## 2026-11-25 exact-head verification of the local pole metric variation

Workflow 45586718905 on exact head
8bfbe348675470223477cdb8e45b5b7a7f233b8d completed successfully:
- 199 Python regression cases passed.
- The two-scale smoke scan completed 4/4 with zero failed integrations.
- The fixed-box bare-WKB UV audit completed and produced strict JSON.
- The 47-page LaTeX PDF built with zero unresolved references/citations.
  Its final pass still had 66 Underfull hboxes and two Overfull hboxes,
  both localized to the newly added metric-variation displays at lines
  5308 and 5324. Those equations have now been split across aligned
  lines without changing the formulas; the new manuscript build is
  pending on the later head.

Artifact audit:
- Smoke ZIP SHA-256:
  76fff038a49fc09183d55c6382d30e774e0e29219461fde0831e3528f3e690d2.
  Strict JSON SHA-256:
  105e3c4e1e560ba5d292da7ca476b50e0e308fe9088fa4641e2b48e21d4766f6.
  It contains 4/4 successful rows across the high-scale threshold-matched
  and low-scale underdamped-control cases. All rows use
  Phi_c/M_Pl=0.9862280831209068. The metadata explicitly records
  quantum_vacuum_seeded=false. The maximum chain-rule continuity
  residual in this smoke artifact is 3.3603e-12. This is a smoke test,
  not a new 100-row physical scan.
- Bare-WKB UV-audit ZIP SHA-256:
  a1f8e24786656d4b03264f12981fd2c8e8b9af3fce582d6fec5395d7a96b6a7e.
  Strict JSON SHA-256:
  260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
  Across 11 grids, the fixed-box bare stress rises by 16664.2325 and
  the N=32-to-64 log slope is 3.8822733. The fixed-spacing volume
  density spread is 2.38067e-13. The artifact explicitly retains
  zero-point energy and records vacuum_subtraction_applied=false,
  counterterms_applied=false, continuum_limit_claimed=false and
  physical_quantum_prediction=false. It confirms the UV blocker; it
  does not renormalize the lattice.

The metric-variation helper, Bianchi validation, component decomposition,
and their regressions are verified by the 199-test run. The LaTeX
overfull equations were reformatted in a subsequent commit; no physical
formula or numerical tolerance was changed. Gate 5 remains NOT MET;
Gate 10 remains PARTIAL pending a warning-audited build.



## 2026-11-25 independent finite-difference test of the pole metric variation

A new regression evaluates the integrated scalar bulk \(a_2\) action on
the compact product geometry \(S^2(K_1)\times S^2(K_2)\), with constant
curvatures in the two orthogonal two-dimensional blocks. It varies the
inverse metric by independently rescaling each sphere radius. For each
block, a central finite difference of
\(\int d^4x\sqrt{g_E}\,a_2^{\rm bulk}\) is compared with the
corresponding block trace of the analytic metric Euler derivative,
including the full Euler-density contribution in the action. The
integrated Euler term is topological and does not alter the derivative.
This is an independent functional-variation check of the local
Euclidean pole formula, not a renormalized stress tensor or a
real-time physical prediction. The new test is pending exact-head CI.



## 2026-11-25 exact-head finite-difference verification completed

Workflow 45587737076 on exact head
ee6a7dced58f30122150fcbaae832cf356423778 completed successfully:
- 200 Python regression cases passed, including the independent
  \(S^2(K_1)\times S^2(K_2)\) finite-difference variation of the
  integrated full \(a_2\) action under separate metric rescalings.
- The two-scale smoke scan passed 4/4 with zero failed integrations.
- The 11-grid bare-WKB UV-cutoff audit passed.
- The 47-page manuscript PDF built. The final LaTeX pass had 80
  Underfull hbox warnings, zero Overfull hboxes, and zero unresolved
  references/citations.

The PDF ZIP SHA-256 is
3270d1aaac3c5d30ce229e04ebc176018e521538875e01708034724192cf5dec;
the extracted 47-page PDF SHA-256 is
e782f691a70b19a6efa372aa1f903f9368d795f6fd03182e253d1761f2a96658.
The smoke ZIP SHA-256 is
507e8623e90244eadf53c3dcbff979047c94e5869a4df018cbd25bb1d73a9a10;
its strict-JSON payload SHA-256 is
d3d85207367776136410b324d078279984224dfe1d707b43590e14700fb6e179.
It contains 4/4 successful rows at
Phi_c/M_Pl=0.9862280831209045, with quantum_vacuum_seeded=false.
The UV-audit ZIP SHA-256 is
a71d189261267972e904803fa260d6813c4974b9fa070ad70dd50e89e1ed3ac6;
its strict-JSON payload SHA-256 is unchanged at
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
It still reports the fixed-box bare-stress factor 16664.2325, the
high-cutoff slope 3.8822733, and fixed-spacing volume spread
2.38067e-13. Zero-point energy is retained; subtraction and
counterterms are false; no continuum limit or physical quantum
prediction is claimed.

The product-sphere finite-difference comparison passed for both
independent curvature blocks. This verifies the analytic metric
variation of the local divergent Euclidean coefficient under the
tested compact geometry. It does not provide finite renormalization
conditions, a renormalized stress tensor, real-time CTP backreaction,
or a lattice counterterm. The long 100-row and paired convergence jobs
were skipped by design; this workflow adds no new full-scan evidence.
Gate 5 remains NOT MET and Gate 10 remains PARTIAL.


## 2026-11-25 one-loop scalar RG projection control

A separate polynomial two-real-scalar control EFT now has explicit
one-loop MS-bar beta coefficients derived from the same local
\(a_2/(16\pi^2\epsilon)\) residue. The returned coefficients cover the
vacuum energy, both mass parameters, both quartics, the mixed quartic,
both non-minimal curvature couplings, the Einstein-curvature coefficient,
and the \(R^2\), Ricci-squared and Euler-density terms. The curvature
basis is reduced modulo the four-dimensional Euler density.

A regression reconstructs the full local pole density from the beta
coefficients at nonzero fields and nonzero constant curvature and
compares it with the matrix heat-kernel expression. Decoupled,
mixed-coupling and conformal-coupling limits are tested; unbounded
quartic inputs are rejected. These new tests and manuscript equations
require exact-head CI.

This is not the beta function of the non-polynomial PTUM plateau.
The exact plateau pole retains \([V_{\rm eff}''(\Phi)]^2\) and
\(R_E V_{\rm eff}''(\Phi)\), which require a functional or explicitly
matched infinite-operator treatment. No \(\Lambda_{\rm EFT}\),
\(\mu_R\) boundary values or finite matching conditions have been
selected. Gate 5 remains NOT MET; no lattice subtraction, renormalized
stress tensor or physical quantum prediction is claimed.


### RG-control manuscript line-break correction

The first exact-head build after adding the polynomial scalar RG control
completed, but the new compact potential display produced one Overfull
hbox on each LaTeX pass. The same equation has been split across two
aligned rows. No formula, coefficient, test threshold or scientific
claim was changed. A fresh exact-head build is required to verify the
formatting correction.


## 2026-11-25 exact-head verification of the polynomial scalar RG control

Workflow 45590315635 on exact head
977ab5919d1055bfc3545473687a9a3cea3237d3 passed 203 Python
regression cases, the 4/4 two-scale smoke scan, the 11-grid bare-WKB
UV audit, and the LaTeX build. The new beta-function regression
reconstructs the complete local \(a_2/(16\pi^2)\) residue at nonzero
fields and constant curvature, and the decoupled, mixed, conformal and
quartic-stability controls pass.

The smoke artifact ZIP SHA-256 is
86fc7c2422fcfcca2f82049af964e1b7b54ed79fbb9cb7a1f35a0ba416214b54;
its strict-JSON payload SHA-256 is
105e3c4e1e560ba5d292da7ca476b50e0e308fe9088fa4641e2b48e21d4766f6.
It contains 4/4 successful classical rows, exact
\(\Phi_c/M_{\rm Pl}=0.9862280831209068\), and
quantum_vacuum_seeded=false. The maximum chain-rule continuity
residual is \(3.3603\times10^{-12}\).

The UV-audit ZIP SHA-256 is
adee79bb4db4977ecf214cae5fd32ba4334217643875695ac9802d08ba2799ad;
its strict-JSON payload SHA-256 is
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
The fixed-box bare-stress factor is \(16664.2325\), the high-cutoff
log slope is \(3.8822733\), and the fixed-spacing volume spread is
\(2.38067\times10^{-13}\). Zero-point energy remains; subtraction and
counterterms are false; no continuum limit is claimed.

The 47-page PDF built with zero Overfull boxes and no final-pass
unresolved references/citations, but 80 Underfull hbox warnings remain.
The polynomial RG control is verified; it is not the non-polynomial
PTUM plateau beta function and does not complete R0 or Gate 5.


## 2026-11-25 exact conformal radiation-FRW free-field benchmark

A new analytic R1 control treats one free massless real scalar with
\(\xi=1/6\) in spatially flat radiation FLRW. Its conformal modes are
exact plane waves with Wronskian \(i\). The local heat-kernel trace
anomaly gives \(T^\mu{}_\mu=H^4/(240\pi^2)\); conservation and the
trace identity, with no additional state-dependent \(a^{-4}\) term,
give \(\rho=H^4/(960\pi^2)\) and \(p=H^4/(576\pi^2)\). New tests
check the exact mode equation, Wronskian, curvature invariants,
trace and continuity identities, Minkowski limit and input validation.

This is a free conformal analytic benchmark only. It does not provide
a general adiabatic subtraction, a second independent numerical
stress-tensor prescription, a massive/interacting waterfall
renormalization, or PTUM backreaction. The new code, tests and
manuscript equations require exact-head CI. Gate 5 remains NOT MET.


### Conformal radiation benchmark residual normalization correction

The first exact-head Python run for the analytic conformal-radiation
benchmark reported 2 failures and 209 passes. Both failures came from
requiring an absolute \(10^{-300}\) residual for the trace identity at
small nonzero \(H\); floating-point cancellation left a residual of
order machine precision relative to the trace, not a physical
conservation violation. The implementation now reports both absolute
and scale-normalized trace/continuity residuals, and the regressions
check the normalized quantities against \(5\times10^{-15}\). The
background equations, anomaly coefficient, stress tensor and all
physical inputs are unchanged. A fresh exact-head run is required.


## 2026-11-25 exact-head verification of the conformal radiation-FRW benchmark

Workflow 45591701409 on exact head
8c903c7575c46ddbf592e83949531f09c86a0fd4 passed 211 Python
regression cases. The new exact conformal mode/Wronskian, heat-kernel
trace anomaly, trace identity, continuity equation, Minkowski limit and
input-validation tests all passed. The earlier two residual failures
were resolved by checking scale-normalized Ward residuals at
\(5\times10^{-15}\); the anomaly and stress formulas were unchanged.

The two-scale smoke artifact ZIP SHA-256 is
ddac0fa79e71a5217c89c7418300bf2d912fa12be0f9f2fedfea9ccf8c5d680a;
its strict-JSON payload SHA-256 is
d3d85207367776136410b324d078279984224dfe1d707b43590e14700fb6e179.
All 4 rows succeeded, all were classical (quantum_vacuum_seeded=false),
the exact threshold output was
\(\Phi_c/M_{\rm Pl}=0.9862280831209045\), and the maximum
chain-rule continuity residual was \(3.2166\times10^{-12}\).

The 11-grid UV-audit artifact ZIP SHA-256 is
82ff85175562a87a6bb4e6f379f9885226ee73379b795bcd435e20a964267616;
its strict-JSON payload SHA-256 remains
260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749.
The fixed-box bare-stress factor is \(16664.2325\), the high-cutoff
log slope is \(3.8822733\), and fixed-spacing volume spread is
\(2.38067\times10^{-13}\). Zero-point energy remains; no subtraction,
counterterms or continuum limit are claimed.

The 48-page manuscript built with zero Overfull boxes and no
final-pass unresolved references/citations; 80 Underfull hbox warnings
remain. This verifies only the analytic free conformal benchmark,
not a general adiabatic or interacting waterfall renormalization.
R1 remains partial and Gate 5 remains NOT MET.


## 2026-11-25 fresh 100-row exact-endpoint scan request

A new full scan is triggered on the current PR #2 branch. The scan
source derives \(\Phi_c\) from the exact Hubble-flow endpoint and
reuses the same 100 initial conditions across the 4,001/256,001-point
output-grid comparison and four DOP853 tolerance levels. The
homogeneous post-threshold nature and classical (non-quantum) seed
interpretation are explicit. Older scan artifacts are not accepted
as current evidence until this run's JSON, checkpoints and comparison
tables are inspected. The full scan is queued; no result is claimed.


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


## 2026-11-25 second-order adiabatic field-variance subtraction

The ptum_adiabatic_subtraction.py module implements the order-two WKB
counterterm for <psi^2> in a supplied spatially flat FLRW background
with time-dependent effective mass M^2(eta) and explicit curvature
coupling xi. It derives omega_k', omega_k'', W2 and the finite-band
subtracted variance from the canonical conformal-time mode. The routine
checks the canonical Wronskian and refuses non-positive zeroth-order
frequencies.

Exact conformal-massless and Minkowski-massive controls plus an
independent background-jet finite-difference regression are included.
This is not a renormalized stress tensor or a complete expectation
value: finite-band IR/UV tails, finite matching conditions, the
interacting Phi force and lattice counterterms remain absent.
Gate 5 remains NOT MET.


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


## 2026-11-26 fourth-order adiabatic stress-tensor control

Added a local order-four WKB derivation for the Hilbert rho and pressure
counterterms of a real scalar on externally supplied spatially flat
FLRW histories. The implementation carries conformal-time jets through
fourth derivative, computes W2 and W4 from the nonlinear WKB equation,
and exposes the order-two field-variance UV subtraction separately
from an order-four matched variance completion. The finite-band
integrator checks canonical Wronskian normalization and positive
frequencies, then reports bare, counterterm and subtracted rho, pressure
and variance.

The external-mass Ward identity is recorded as
dot(rho)+3H(rho+p)=0.5 dot(M^2)<psi^2>. For the PTUM waterfall mass and
positive-Phi downward motion, dot(M^2)<0. For a classical/bare positive
psi^2 this is negative transfer under the declared split; a finite
renormalized variance may be sign-indefinite and must be evaluated.

Regression coverage includes conformal massless and Minkowski massive
exact limits, finite-band vacuum cancellation, independent W2 derivative
finite differences, a matched order-four Ward identity, and fail-closed
input checks. Exact-head CI for this new implementation is pending.
This remains a local subtraction control, not a finite renormalized
stress tensor, renormalized Phi force, self-consistent backreaction,
CTP result, or lattice counterterm. Gate 5 remains NOT MET.


Exact-head workflow 45795403829 verified 222 Python tests, a 4/4
homogeneous smoke scan, and the 11-grid bare-WKB UV audit. The strict
scan JSON retained the exact Phi_c and quantum_vacuum_seeded=false.
The UV artifact retained zero-point energy and explicitly made no
subtraction, counterterm, or continuum-limit claim. The 48-page PDF
built but exposed three overfull equations in the new R1.3 display;
the follow-up manuscript edit splits those displays and adds the
standard adiabatic-regularization references. Underfull warnings remain.

## 2026-11-26 independent massive de Sitter adiabatic-stress control

A new exact-mode regression tests the fourth-order free-field stress
counterterms in a non-conformal expanding background. For de Sitter
\(H=1\), \(a=-1/\eta\), a minimally coupled scalar with \(M^2=2\),
and \(\xi=0\), the canonical frequency is exactly \(k\) because
\(a^2M^2=a''/a\). The exact plane-wave mode has Wronskian \(i\).
At \(\eta=-1\), the exact bare Hilbert mode stresses are
\(\rho_k=k/2+3/(4k)\) and \(p_k=k/6-1/(4k)\). The new test compares
these with the local order-four counterterms for \(k=20,40,80\) and
checks the expected \(k^{-7}\) first-omitted-order residual in both
components. The manuscript records the derivation and limitation.

This is an independent analytic free-field control. It is not a
renormalized finite-band continuum result, a point-splitting
implementation, an interacting waterfall calculation, or a physical
PTUM prediction. Gate 5 remains NOT MET.

## 2026-11-26 exact-head verification of the massive de Sitter R1.3 control

Workflow [45797854235](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45797854235) on exact head 2a8d02ede094a82578cd82cac3ec07df74ebf6ad completed successfully:
- 223 Python regression cases passed, including the new exact massive minimally coupled de Sitter mode, Wronskian, analytic bare Hilbert stress and \(k^{-7}\) residual-scaling checks.
- The two-scale homogeneous smoke scan passed 4/4 with zero failed integrations. Strict JSON parsing rejected non-finite constants and succeeded. All rows use \(\Phi_c/M_{\rm Pl}=0.9862280831209045\), record quantum_vacuum_seeded=false, and have maximum chain-rule continuity residual \(3.2166\times10^{-12}\). The maximum sampled finite-difference residual ratio is \(3.72335\times10^{-2}\); it remains a diagnostic, not a strict convergence result.
- The 11-grid bare-WKB lattice UV audit passed. Its strict JSON retains zero-point energy and explicitly records vacuum_subtraction_applied=false, counterterms_applied=false, and continuum_limit_claimed=false. The high-cutoff slope is \(3.8822733\), and the fixed-spacing volume-density spread is \(2.38067\times10^{-13}\).
- The 49-page manuscript PDF built. Its final LaTeX pass has 81 Underfull hbox warnings, zero Overfull hboxes, and zero unresolved references/citations. Typography warnings remain.
- The full 100-row sensitivity scan and the paired convergence jobs were skipped because this was not a FULL-SCAN commit.

Artifact checksums: smoke ZIP 557c0f8fa91d5ade3500d47b8e01563578d7886678333775a969021f89bc52e5 (strict JSON d3d85207367776136410b324d078279984224dfe1d707b43590e14700fb6e179); UV ZIP 8ef6b08480443eb5691029e7ec98f2053832968146d6cb0cdfe890a0b499bcff (strict JSON 260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749); manuscript ZIP df1a2ec2ce4cb35b553e5125139eaacdf5434940a78c416270d6db771d42daf3 (PDF 7020736ee15667decdfbf8719301903df6248633445404914f832505ff9e8886).

The exact massive de Sitter control is verified. The lattice remains unsubtracted and cutoff dependent; no interacting renormalization, self-consistent backreaction, rescattering, or physical quantum-waterfall claim is promoted. Gate 5 remains NOT MET and Gate 10 remains PARTIAL.

## 2026-11-26 clarification of the linear inflation-to-waterfall calculation

The repository's waterfall wrapper does more than integrate a mode on
an arbitrary external history. It obtains the initial Phi and Phi-dot
from the integrated single-field inflationary solution at
Phi=(1+delta)Phi_c, evolves the expanding psi-bar=0 invariant
background through the threshold, and initializes linear psi_k
modes in a first-order adiabatic vacuum in the stable phase. The modes
are then evolved through any tachyonic interval with Wronskian and
adiabaticity checks. A new regression verifies the exact initial
inflationary field/velocity match and the subsequent stable-to-tachyonic
mass sign change.

This is a linear test-field crossing calculation, not a self-consistent
coupled quantum background. The mode stress and force do not enter the
Friedmann or Phi equations; there is no nonlinear quantum rescattering
or SM-source evolution. The homogeneous post-threshold scan and the
separate finite-cutoff classical lattice remain distinct calculations.
Gate 2 remains PARTIAL; Gates 5 and 6 remain NOT MET.

## 2026-11-26 exact-head linear-crossing scope and CI verification

The waterfall wrapper's initial state is obtained from the integrated
single-field inflationary trajectory at Phi=(1+start_fraction)Phi_c.
It evolves the expanding psi-bar=0 invariant background through the
threshold, then initializes finite-band linear psi_k modes in a
first-order adiabatic vacuum in the stable phase. The new regression
checks the exact initial Phi/Phi-dot match, positive initial and negative
post-crossing m_eff^2, expansion, the exact psi=0 homogeneous solution,
and that mode backreaction remains disabled. This is a linear test-field
crossing, not a self-consistent quantum background.

Exact-head workflow 45799709372 on cb4ee0ebeae8ced796691d0dce4690373337da70 passed 224 Python cases, the 4/4 smoke scan, the 11-grid bare-WKB UV audit and the 49-page LaTeX build. The final pass had 81 Underfull hboxes, zero Overfull hboxes and zero unresolved references/citations. Strict JSON inspection confirmed the smoke artifact uses Phi_c/M_Pl=0.9862280831209068 and quantum_vacuum_seeded=false; the UV artifact retains zero-point energy and applies no subtraction or counterterms. The 100-row scan and paired convergence jobs were skipped for this non-FULL-SCAN commit.

Two intermediate test failures are recorded transparently: f4b0b2d misplaced a source assertion in an import tuple and failed collection; 97b018f fixed the placement but exposed one stale assertion that described the nonlinear classical lattice as not nonlinear. cb4ee0e updated the assertion to the accurate quantum-renormalization scope. The final exact-head regression passed 224/224.

The next documentation commit uses the workflow's explicit FULL-SCAN opt-in to
re-evaluate the 100-row exact-endpoint scan and paired convergence on this
branch head. Gate 2 remains PARTIAL; Gates 5 and 6 remain NOT MET.


## 2026-11-26 exact-head 100-row baseline revalidation

Workflow [45800154570](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45800154570) on exact code head
\texttt{b388bfe371b46b229266320a4a3edc9812a65e18} completed the
100-row DOP853 homogeneous post-threshold baseline:
- 100/100 integrations succeeded; zero failures; 50 rows per scale.
- Exact threshold: \(\Phi_c/M_{\rm Pl}=0.9862280831209068\).
  Each trajectory uses 4,001 output points over \(20\mu^{-1}\),
  \(\mathrm{rtol}=10^{-9}\), \(\mathrm{atol}=10^{-12}\), and the
  integrated single-field FRW fuel velocity.
- The strict-JSON artifact was parsed with non-finite constants rejected.
  ZIP SHA-256:
  \texttt{f4ab5ee18afb92a6509b50fe5062a529354b2333a841457edad5fd5b5bad0916};
  extracted result JSON SHA-256:
  \texttt{5c86db1631da9efd35f956a266edbd5c30cfdae405de1cb9e6e06029c042c1a2}.
- Regimes: high scale 48 non-quartic/2 insufficient oscillation; low-scale
  underdamped control 41 non-quartic/4 insufficient oscillation/5 quartic.
  All five quartic-classifier rows are low-scale controls with
  \(\psi_{\rm init}=5\psi_0\) and offset \(0.01\Phi_c\). Their
  cycle-averaged \(w_\psi=0.37218\text{--}0.37363\),
  \(Q=10.6511\text{--}11.0710\), virial ratio
  \(0.90607\text{--}0.90962\), and \(H/\omega\) maximum
  \(6.8652\times10^{-5}\text{--}7.0139\times10^{-5}\).
- The maximum chain-rule FRW continuity residual is
  \(1.19986\times10^{-10}\); the maximum sampled finite-difference
  residual ratio is \(3.72337\times10^{-2}\). The latter remains
  sampling-sensitive and is not replaced by the chain-rule diagnostic.
- The scan explicitly records \texttt{quantum\_vacuum\_seeded=false}. It is a
  homogeneous post-threshold sensitivity scan, not a quantum-seeded
  crossing or inhomogeneous waterfall.

The paired exact-head study completed 500/500 integrations and
400 comparisons. All 100 output-grid comparisons passed; every
finite-difference residual decreased on the 64-fold output-grid
refinement, with median observed order 0.9906 and minimum reduction
factor 1.3797. The three tolerance refinements passed 98/100, 99/100,
and 100/100 adjacent comparisons. The three intermediate failures
were resolved by subsequent refinement; state and classification
error envelopes decreased monotonically, all 100 regime flags and
metric-availability patterns were unchanged across all five profiles,
and the finest adjacent comparison passed 100/100. The maximum
final-pair state relative difference was 1.63e-7 and the maximum
normalized classification-metric difference was 6.36e-11. The
convergence artifact ZIP SHA-256 is
\texttt{440c45ab73dc1ed9f8bfb8ea09f43a823a43b74f7d9b53ba4092812ef8be73e4};
the extracted strict-JSON SHA-256 is
\texttt{de97dd3d35d5c20d0ee63c00fecd1c5efa0cf3b588a3083a4c0f7838da4f5d2c}.
The 89/6/5 regime counts and all five low-scale quartic labels are
stable under the tested homogeneous grid/tolerance refinements. This
does not test inhomogeneous or quantum-waterfall convergence. Gate 7 remains NOT MET:
the five low-scale classical controls do not establish a high-scale
quartic attractor, perturbative stability, or a microscopic proxy-fluid.
Gate 5 remains NOT MET; Gate 10 remains PARTIAL.


The first documentation-only regression run on commit 6c2fb71
passed 223/224 tests. Its sole failure was a manuscript test expecting
the literal unescaped token \texttt{quantum_vacuum_seeded=false};
the LaTeX source correctly escapes underscores inside \texttt{\textbackslash texttt}.
The assertion was corrected to require the escaped LaTeX token.
Follow-up workflow [45804043025](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45804043025)
on commit \texttt{65eab8dfe3ff1e3c407946793e749f4255cfae40} passed
224/224 Python tests, the 4/4 smoke scan, and the 11-grid UV audit.
The 49-page PDF built; its final LaTeX pass had 87 Underfull hbox
warnings, zero Overfull hboxes, and no unresolved references/citations.
The smoke JSON was strictly parsed (4/4 successful, exact
\(\Phi_c/M_{\rm Pl}=0.9862280831209068\), quantum seed flag false,
maximum chain-rule residual \(3.36033\times10^{-12}\)). The UV JSON
was strictly parsed and continues to show retained zero-point energy,
no subtraction/counterterms/continuum claim, and high-cutoff slope
3.8822733. This documentation/test-only commit does not change the
simulation source; the 100-row scan and paired convergence remain tied
to exact simulation head b388bfe in workflow 45800154570.


## 2026-11-26 exact-head documentation regression and artifact verification

The corrected manuscript regression is now green on exact branch head
\texttt{65eab8dfe3ff1e3c407946793e749f4255cfae40}. Workflow
[45804043025](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45804043025)
passed 224 Python tests, 4/4 smoke trajectories, the 11-grid UV audit,
and the 49-page PDF build. Strict-JSON smoke and UV artifacts were
parsed with non-finite constants rejected.

Artifact checksums:
- smoke ZIP:
  \texttt{ad27977c5e56c9b2252bffbc4bc1c2d52df7676eca4143d9f176607a34fb87e5};
  JSON:
  \texttt{105e3c4e1e560ba5d292da7ca476b50e0e308fe9088fa4641e2b48e21d4766f6};
- UV ZIP:
  \texttt{e1cbcdab425855495d5cc95f9a878b8338695fc758d948bd504f1abeb178d4f5};
  JSON:
  \texttt{260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749};
- PDF ZIP:
  \texttt{6d1307ef8561dda4adb848784e0a3b13a7ff61e40cadd2435b1256e79451737a};
  PDF:
  \texttt{f177179f7c02cd0a8cf94d04d007f2516709a1e58356ecfb50c9092ddbf0ff07}.

The final LaTeX pass has 87 Underfull hbox warnings, zero Overfull
hboxes and zero unresolved references/citations. Gate 10 remains PARTIAL
until warning cleanup and clean-room reproducibility are complete.


## 2026-11-26 domain-wall required-source validity guard

The defect diagnostic previously returned the linearized source
\(\epsilon_{\rm req}^{\rm lin}=\Delta V_{\rm req}/(2v)\) without
separately indicating whether that *required* source itself lies in
the small-bias expansion domain. This could be extrapolated beyond the
range where \(\Delta V\simeq2\epsilon v\) is controlled even when the
actual supplied bias was small. The code now returns
\(r_{\rm req}=\epsilon_{\rm req}^{\rm lin}/\epsilon_{\rm crit}\) and
\texttt{required_linear_source_small_bias_approx_valid}, using the
explicit \texttt{small_bias_fraction} (default 0.1). A regression
covers both the benchmark-like small-ratio case and a large-network
case where the required linear source is below spinodal but outside
the declared small-bias range. No annihilation estimate is promoted
when the actual bias lies outside its own small-bias domain.
This is an analytic diagnostic guard, not a domain-wall network
simulation; Gate 5 remains NOT MET.


## 2026-11-26 domain-wall guard exact-head CI

Workflow [45805018373](https://github.com/arreasonn-jpg/PTUM-Phase-Transition-Universes-Model-/actions/runs/45805018373) on commit
\texttt{664ed12d160a0b45a484e3ca3527a5f4685f446e} passed 225/225
Python regression cases, 4/4 smoke trajectories, the 11-grid bare-WKB
audit and the 49-page manuscript build. The new required-source
small-bias validity test passed. The final LaTeX pass retained 87
Underfull hbox warnings, with zero Overfull hboxes and no unresolved
references/citations.

Strict-JSON smoke and UV artifacts were parsed with non-finite values
rejected. Artifact checksums:
- smoke ZIP \texttt{1e4cc175b32f03a81efce576ba78bc88e224ffe1080c985b29e67d66554956ea};
  JSON \texttt{d3d85207367776136410b324d078279984224dfe1d707b43590e14700fb6e179};
- UV ZIP \texttt{0793fdec1ddf35f82333cd131f8c7256c006c85c69e415e1fe816ad1cf95a430};
  JSON \texttt{260730f3857d1b65433a2a435b041d6c6779d5b75f63b6c8c2e5ba9447493749};
- PDF ZIP \texttt{e9774f0a3fabafec39d41a8822d244fb4d8d9f5334cdb23d70d86c55863703fa};
  PDF \texttt{3bbf8a154afd2c969eb54ac94a880481e9a1a87ef533158a6d9b9876970a6948}.

The smoke scan again records \texttt{quantum\_vacuum\_seeded=false};
the UV audit again retains zero-point energy and applies no vacuum
subtraction or counterterms, with high-cutoff bare-stress slope 3.8822733.
Long full-scan jobs were skipped because this commit changes only the
analytic defect diagnostic, tests and documentation. The exact-head
100-row/500-integration homogeneous scan remains verified on unchanged
simulation source head b388bfe in workflow 45800154570. Gate 5 remains
NOT MET and Gate 10 remains PARTIAL.


## 2026-11-27 general flat-FLRW conformal-anomaly oracle

Added an analytic one-real-scalar conformal-anomaly stress helper for
spatially-flat FLRW with arbitrary finite H and dot(H). The local
curvature invariants independently reduce to
Riemann^2 - Ricci^2 = -12 H^2 (H^2 + dot(H)); the declared scheme
sets the ambiguous Box(R) coefficient to zero. Conservation gives
rho = H^4/(960 pi^2) + C/a^4 and p = (trace + rho)/3, with the
state-dependent radiation constant exposed as an input. The helper
reports normalized trace and continuity residuals. Regressions cover
Minkowski, de Sitter, radiation, generic flat-FLRW kinematics and the
radiation-only specialization identity.

This is an exact analytic free-field control only. It is not an
independent point-splitting mode integral, a massive/interacting
subtraction, a PTUM renormalized stress tensor, a Phi force, or
self-consistent backreaction. Gate 5 remains NOT MET; Gate 10 remains
PARTIAL pending exact-head CI and warning/clean-room work.


## 2026-11-27 CLASS/Cobaya source-tree audit

A fresh recursive tree inspection at d2f15928ba6af8b75b0dc9d823d0a291acbf22f3
returned 86 tracked entries. PTUM.zip is present (6,248,335 bytes), but
its contents could not be verified; no conclusion about the archive's
internal files is justified. Outside it, no separately tracked CLASS
patch/diff, production Cobaya YAML, MCMC chain files or raw likelihood
bundle is exposed. Gate 9 remains NOT MET.

Exact-head workflow 45971792497 completed successfully: 227 tests,
4/4 two-scale smoke trajectories, 11-grid bare-WKB audit and 49-page
PDF. The full 100-row scan and convergence jobs were skipped. The
smoke rows are classical controls (quantum_vacuum_seeded=false), and
the bare UV audit still applies no vacuum subtraction or counterterms.
These results do not establish quantum waterfall dynamics or
observational reproducibility.


## 2026-11-28 action-matched finite-band Phi-sector source

The free-field fourth-order adiabatic stress helper now optionally accepts
\(M^2_{,\Phi}\) and \(\dot\Phi\), checks
\(\dot M^2=M^2_{,\Phi}\dot\Phi\), and reports the finite-band term
\[
\mathcal C_\Phi^{\rm band}
=\frac12M^2_{,\Phi}\langle\psi^2\rangle_{\rm band,sub}
\]
from the same order-two or order-four subtracted variance. The declared
sector split then gives
\[
Q_\psi^0=\dot\Phi\,\mathcal C_\Phi^{\rm band},
\qquad Q_\Phi^0=-Q_\psi^0.
\]
For positive \(M^2_{,\Phi}\) and downward \(\dot\Phi<0\), \(Q_\psi^0\)
is negative. New regressions check the chain rule, opposite sector
sources, fail-closed input handling, and the finite-band stress Ward
identity for a time-dependent external mass.

This is only a free-field, finite-band, externally prescribed-background
control. It is not a renormalized force on \(\Phi\), does not fix finite
matching conditions or momentum tails, and does not include interacting
self-energy, CTP backreaction, or nonlinear lattice counterterms.
Gate 5 remains NOT MET.


## 2026-11-28 R1.5 exact-head CI and equation layout correction

The action-matched finite-band Phi-source implementation passed 231
Python regressions, the 4/4 smoke scan, and the 11-grid bare-WKB audit
in workflow 46130156148. The manuscript built to 49 pages, but the
combined source equation produced one 49.91374pt Overfull hbox. The
equation is now split into aligned lines; exact-head LaTeX revalidation
is required before counting the manuscript layout as clean. The
remaining 81 Underfull hboxes are still recorded.


## 2026-11-28 R1.5 exact-head verification

Commit 93d9bea4ac92d64fe8320e36e4d6f22976d0383c passed 232 Python
tests, the 4/4 smoke scan, the 11-grid bare-WKB audit and the 49-page
LaTeX build in workflow 46130428147. The exact smoke threshold remains
\(\Phi_c/M_{\rm Pl}=0.9862280831209045\); all four trajectories completed
without integration failure, quantum_vacuum_seeded=false, and the maximum
chain-rule continuity residual is \(3.2166235\times10^{-12}\). The
nonzero seeds are classical sensitivity controls, not quantum vacuum
fluctuations. The UV audit has 11 grids, bare-stress slope 3.8822732966,
fixed-spacing density spread \(2.38067\times10^{-13}\), zero-point
energy retained, no vacuum subtraction/counterterms, and no continuum
claim. The final LaTeX pass has zero Overfull hboxes, 87 Underfull
hboxes, and no final-pass unresolved references/citations. The first
pass forward-reference warnings resolve on rerun. The full scan and
paired convergence jobs were skipped because the simulation source was
unchanged.


## 2026-11-28 R1.6 free-field finite-band momentum convergence

A pure Gaussian squeezed state in Minkowski space was used as an
independent oracle for the existing fourth-order adiabatic stress and
second-order variance subtraction. With
\(\beta_k=i\beta_0e^{-k/k_*}\) and
\(|\alpha_k|^2-|\beta_k|^2=1\), the exact vacuum-subtracted spectra are
\[
\rho_{k,\rm sub}=\omega_k|\beta_k|^2,\qquad
p_{k,\rm sub}=\frac{k^2}{3\omega_k}|\beta_k|^2,\qquad
\langle\varphi^2\rangle_{k,\rm sub}=\frac{|\beta_k|^2}{\omega_k}.
\]
The finite-band integrals were compared with independent adaptive
quadrature over the full positive momentum axis, with separate fixed-band
grid, UV-extension and IR-extension sequences. For the arbitrary
free-field control scales \(M^2=1.7\,{\rm GeV}^2\),
\(k_*=0.8\,{\rm GeV}\), \(\beta_0=0.25\), the finest relative errors
were at most \(1.79\times10^{-7}\), below the predeclared
\(2\times10^{-7}\) tolerance; the maximum normalized Wronskian error
was below \(10^{-12}\).

The strict-JSON audit is produced by ptum_adiabatic_band_audit.py
and runs as a separate CI job. Workflow 46131831457 on exact head
00784e748d73fded40fd962ddfa912a2c283ea27 passed 234 regression tests,
the 4/4 homogeneous smoke scan, the 11-grid bare-WKB audit, the new
finite-band convergence job and the 49-page PDF build. The final LaTeX
pass had zero Overfull boxes, 87 Underfull boxes and no final-pass
unresolved references/citations or warnings.

This is a free Minkowski squeezed-state numerical control, not a PTUM
waterfall prediction. It does not establish a self-consistent
time-dependent interacting stress tensor, finite matching conditions,
CTP backreaction, nonlinear lattice counterterms or a relic abundance.
Gate 5 remains NOT MET; Gate 10 remains PARTIAL.


## 2026-11-28 R0.3: field derivatives of the scalar heat-kernel pole

Added `ptum_scalar_heat_kernel_a2_field_derivatives` for the coupled
real ((\Phi,\psi)) scalar Gaussian operator. At fixed metric it
returns \(\partial_\Phi a_2\) and \(\partial_\psi a_2\), each with
mass dimension three. The calculation compares the direct matrix
derivative of \(\tfrac12\operatorname{tr}[A^2]\) with the derivative
of the expanded local operator decomposition, including the mixed
Hessian entry and the explicit curvature-coupling terms. A mismatch
above \(5\times10^{-12}\) relative is rejected.

Regression coverage uses stable and tachyonic values of the waterfall
mass, central finite differences, the real-field \(Z_2\) parity, and
invalid-input rejection. This improves the algebraic specification of
the field-dependent scalar UV-pole functional and the ingredients
needed for a later action-level counterterm force.

It does **not** choose the dimensional-regularization pole prefactor or
counterterm sign, specify the EFT cutoff/operator truncation or finite
matching conditions, include SM/gauge/fermion/graviton loops or
initial-surface terms, compute a renormalized force, or evolve a
self-consistent CTP/Friedmann system. It is not a physical quantum
waterfall result. Gate 5 remains **NOT MET**.
