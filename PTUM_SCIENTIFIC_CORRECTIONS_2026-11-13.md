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

The pytest regression file is maintained at `tests/test_ptum_consistency.py`. The initial six-test suite passed in GitHub Actions on commit `c2007f455f4cdfc0eee7221aef350ea2ad811659` (`6 passed in 0.42s`). The subsequently added static de Sitter test failed because finite-differencing an almost constant vacuum-dominated density and normalizing by a near-zero scale generated spurious relative values of 1.

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

The branch now has additional tests for (i) refusing to infer barrier crossing from (w>0.5), and (ii) serializing unavailable values as strict JSON nulls. The full test count and the corrected scan/LaTeX artifacts remain pending the next CI run.
