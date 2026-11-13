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

It runs 50 initial conditions at each energy scale (100 total), with 4001 output points over $20\mu^{-1}$ per trajectory. Each JSON row records the scenario, damping ratios, time span, output resolution and seed grid. Regression tests check the 50-point grid and ensure positive offsets start below $\Phi_c$ on the tachyonic side. This remains a homogeneous post-threshold sensitivity scan, not a quantum-vacuum seed distribution or a simulation of the threshold crossing itself. The pre-exact-endpoint revision passed **25 regression tests** in run 43393188155. After the exact $\epsilon_H=1$ threshold update, the exact-endpoint and signed-transfer regressions bring the suite to 27; the fresh 27-test run, 100 high-resolution integrations, and LaTeX build are pending.


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
If all of this total energy thermalized instantaneously at $g_*=100$ and $V_0^{1/4}=10^{16}\,\mathrm{GeV}$, the idealized upper-limit estimate is $T_{\rm rh}^{\rm ideal}\simeq1.72\times10^{15}\,\mathrm{GeV}$. Converting only the potential contribution gives $1.56\times10^{15}\,\mathrm{GeV}$. The potential-only damping estimate is $3H_{c,V}/(2\mu)\simeq3.48$, while the exact endpoint including kinetic energy gives $3H_c/(2\mu)\simeq4.26$. Both are overdamped. These values supersede the earlier $0.0378V_0$, $1.84\times10^{15}\,\mathrm{GeV}$, and $4.9$ estimates in Sections 13 and 21.

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
