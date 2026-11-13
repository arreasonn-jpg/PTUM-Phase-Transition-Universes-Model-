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

## 7. Regression tests and verification boundary

A pytest regression file is maintained at `tests/test_ptum_consistency.py`. The initial six-test suite passed in GitHub Actions on commit `c2007f455f4cdfc0eee7221aef350ea2ad811659` (`6 passed in 0.42s`). The subsequently added static de Sitter test failed: finite-differencing an almost exactly constant vacuum-dominated density produced round-off-sized derivatives, while normalizing by the same near-zero derivative scale generated spurious relative values of 1.

The diagnostic has now been split:
- `continuity_residual` and `continuity_residual_relative`: chain-rule evaluation using the field accelerations from the background RHS. This is an equation-consistency diagnostic, not an independent solver validation.
- `continuity_residual_finite_difference` and its relative counterpart: sampled `numpy.gradient` diagnostic retained separately for timestep/output-grid convergence studies. It is not expected to be well-conditioned for an exactly static, vacuum-dominated solution.

The expansion term is evaluated as (3H(\\dot\\Phi^2+\\dot\\psi^2)), algebraically equivalent to (3H(\\rho+p)) for the two canonical homogeneous scalar fields, but numerically avoids subtracting vacuum-sized density and pressure terms.

An independent local numerical reproduction of the static and evolving test setups gave a zero normalized chain-rule residual for the static case and a maximum relative residual of approximately (1.44\\times10^{-16}) for the evolving two-field case. This was a calculation of the diagnostic equations, not execution of the repository's full pytest suite. The current branch contains eight tests; no GitHub Actions run or combined status was visible for the latest commit at the time of this note. Therefore the latest full CI suite is still **pending verification**, not claimed as passing.

The tests and local checks cover homogeneous bookkeeping and internal equation consistency only. They do not establish the full PTUM scenario, reproduce CLASS/Cobaya, or calculate a physical dark-matter relic abundance.

## 8. Still open

1. Derive all sector divergences from one complete action including the Dirac/SM Lagrangian, then verify the interaction-stress assignment line by line.
2. Run the Python test suite and convergence tests; compare analytic and finite-difference continuity residuals.
3. Integrate chi_k modes in an expanding background, compute monodromy/Floquet bands, and include backreaction and rescattering before making relic-density claims.
4. Resolve the benchmark inconsistency between the manuscript's overdamped psi dynamics and the conditional quartic proxy-fluid closure.
5. Independently reproduce CLASS/Cobaya constraints from the public patch, production configs, chains, and data inputs.
