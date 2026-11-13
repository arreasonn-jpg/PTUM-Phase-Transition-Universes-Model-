# PTUM Claim Boundary v1.2 CLEAN (updated with Task 1 numerical findings)

## Safe core claim

PTUM is an effective phenomenological cosmological framework that parametrizes a threshold-triggered discharge and its candidate dark-matter, residual dark-energy-like, and proxy-fluid dark-radiation sectors. The current homogeneous simulation does not yet establish their microscopic production or the required energy partition.

The sharp observational discriminator is the difference between fluid-like dark radiation and free-streaming relativistic species. In the effective linear proxy-fluid closure, the pfd component has

```text
w = 1/3, c_s^2 = 1/3, sigma = 0
```

and therefore does not generate the characteristic free-streaming anisotropic-stress phase-shift contribution. This does not imply that all acoustic peak locations are unchanged: background and coupled-perturbation effects must still be computed in the full Boltzmann hierarchy.

## Current-data status

The benchmark analysis gives (with $\Delta\chi^2\equiv\chi^2_{\rm PTUM}-\chi^2_{\Lambda\rm CDM}$):

```text
Delta chi^2 = +0.26
Delta AIC = +2.26
Delta N_fluid < 0.31 at 95% credibility
```

This should be framed as follows:

```text
Current data show a weak preference for LambdaCDM while leaving PTUM viable as a falsifiable effective extension.
```

It should not be framed as positive evidence that current data prefer PTUM.

## Activation-sign revision

The activation mass has been revised to
\[
m_{\rm eff}^2(\Phi)=m_\psi^2\left(\frac{\alpha\Phi^2}{E_{\rm th}^2}-1\right),
\qquad
\Phi_c=\frac{E_{\rm th}}{\sqrt\alpha}.
\]
Thus the proxy is stable for $|\Phi|>\Phi_c$ and tachyonic for
$|\Phi|<\Phi_c$. This sign is selected to match the stated chronology:
the positive-$\Phi$ slow-roll solution moves downward from
$\Phi_*\simeq10.715M_{\rm Pl}$ to the exact $\epsilon_H=1$ endpoint
$\Phi_{\rm end}\simeq0.986228M_{\rm Pl}$,
so the waterfall instability turns on as the field crosses below
$\Phi_c\simeq\Phi_{\rm end}$. The associated interaction potential is
$U_{\Phi\psi}=+\tfrac12(\alpha m_\psi^2/E_{\rm th}^2)\Phi^2\psi^2$;
the scalar equation and sector transfer-current signs have been
rederived accordingly.

The threshold-matched scan now sets $\Phi_c$ from the exact Hubble-flow endpoint, not the older potential slow-roll estimate $\Phi_{\epsilon_V=1}\simeq1.387M_{\rm Pl}$. For $\lambda_\Phi=0.02$, the exact endpoint is $0.986228M_{\rm Pl}$. The potential-only damping estimate is $3H_{c,V}/(2\mu)\simeq3.50$, while the exact $\epsilon_H=1$ endpoint including kinetic energy gives $3H_c/(2\mu)\simeq4.29$. The endpoint energy is $\rho_{\rm end}/V_0\simeq0.02889739$ (with $V_{\rm end}/V_0\simeq0.01926493$ and $K_{\rm end}/V_0\simeq0.00963246$).

The old 36-point scan used the opposite sign and is historical only.
The revised code, manuscript, and tests must pass a fresh CI scan
before any new regime conclusion is accepted. The onset itself still
requires coupled quantum/inhomogeneous evolution and backreaction.
The latest completed scientific-base regression step passed 43 tests; the LaTeX build passed. A subsequent 100-trajectory scan run was cancelled before completion and produced no scan artifact. The latest workflow now allows 45 minutes and logs progress every ten trajectories; a fresh scan is in progress. No scan conclusion is claimed until all integrations complete, the strict-JSON artifact is inspected, and every row passes validation. The dependent claims/EFT branch adds dimensionally normalized residual-DE potential code, corrected radiation fractions, an explicit EFT cutoff boundary, and linear quantum waterfall-mode/spectrum calculations; its combined 54-test suite is pending CI.

## Task 1 baseline under the previous activation sign (historical)

**Under the previous activation-mass sign, the quartic-dominated regime was not demonstrated in either homogeneous scan.** GitHub Actions run 43392067477 completed 24 regression tests and 36/36 integrations successfully. These results are historical and do not validate the revised waterfall sign:
- High-scale threshold-matched benchmark ($V_0=10^{64}\,\mathrm{GeV}^4$, $\Phi_c=1.387M_{\rm Pl}$, local damping ratio $3H_c/(2\mu)\simeq4.87$): 16 non-quartic and two insufficient-oscillation-data trajectories; zero quartic or quadratic-candidate trajectories.
- Low-scale underdamped control ($V_0=10^{56}\,\mathrm{GeV}^4$): 16 non-quartic and two insufficient-oscillation-data trajectories; zero quartic or quadratic-candidate trajectories.

The results above were generated with the **superseded activation-mass sign** and are retained as a historical diagnostic only. They must not be used as validation of the revised waterfall model. The 36-point scan must be rerun after the sign revision before making any claim about quartic or quadratic regimes.

The two exactly zero-seed solutions remain at $\psi=0$ in the deterministic homogeneous equations; this is an invariant solution, not evidence that quantum fluctuations are absent physically. A fluctuation-seeded or inhomogeneous treatment is required to model tachyonic growth from vacuum fluctuations. Both scans are homogeneous post-trigger tests and do not establish the full inhomogeneous discharge or microscopic proxy-fluid production.

The earlier classifier label \`barrier_crossing\` has been withdrawn because $w>0.5$ does not measure a field-space barrier crossing. The classifier now uses \`non_quartic\` unless explicit quartic or quadratic-candidate criteria are met.

The benchmark inputs considered are:
- $V_0 \sim 10^{64}\,\mathrm{GeV}^4$ (plateau scale $H_* \sim 10^{13}\,\mathrm{GeV}$)
- $m_\psi \sim 10^{13}\,\mathrm{GeV}$, $\lambda_\psi \sim 0.1$
- $\psi(t_c)=0$, $\dot{\psi}(t_c)=0$ in the zero-seed limit

For the superseded potential-only threshold choice $\Phi_c\simeq1.387M_{\rm Pl}$, the historical potential-dominated local estimate was $3H_c/(2\mu)\simeq4.9>1$. The current exact-$\epsilon_H=1$ threshold is $\Phi_c\simeq0.986228M_{\rm Pl}$ with the revised local estimate $3H_c/(2\mu)\simeq4.29$; the plateau-scale estimate is $3H_*/(2\mu)\simeq25$. The two-field homogeneous truncation is overdamped in this potential-dominated estimate. This makes quartic oscillations unlikely for the matched benchmark, but the actual outcome must be determined from the corrected 18-point scan and the local $H(t)$ trajectory. A nonzero seed and coupled transfer terms must be followed before making a definitive all-initial-conditions statement.

A conservative sufficient low-scale regime is:
1. $V_0 \lesssim 10^{58}\,\mathrm{GeV}^4$ ($H_* \lesssim 10^{10}\,\mathrm{GeV}$), which gives underdamped motion with a large margin in the threshold-matched estimate
2. Sufficient initial kinetic energy in $\psi$ to cross the barrier
3. Continuing energy input from rolling $\Phi$ field or rescattering

The proxy-fluid closure $w=1/3$, $c_s^2=1/3$, $\sigma=0$ is therefore a **phenomenological ansatz conditional on parameters not realized in the stated benchmark**. The observational discriminator applies *if* the quartic regime is realized; it is not a prediction of the benchmark parameters alone. The Bayesian constraints on $\Delta N_{\rm fluid}$ should be interpreted as constraints on the *phenomenological proxy-fluid model*, not as constraints on the microscopic PTUM discharge dynamics with the stated benchmark parameters.

## Waterfall defect topology

The current $\psi$ truncation is a real scalar with an even potential. For
$m_{\rm eff}^2<0$ it has two degenerate minima
\[
\psi_{\min}=\pm\sqrt{-m_{\rm eff}^2/\lambda_\psi},
\]
so a spatially inhomogeneous transition can spontaneously break a
$Z_2$ symmetry and form domain walls. This model does not, by itself,
derive cosmic strings. The string-tachyon discussion is only a
structural analogy, and the separately reported winding analysis of
$\Phi_{\rm res}$ does not establish the absence of $\psi$ domain walls.
The dimension-five fermion-Higgs operator introduced for reheating
is odd in $\psi$ and may explicitly break this $Z_2$, but its induced
vacuum bias and domain-wall lifetime depend on the Wilson
coefficients and any additional discrete charge assignments. A
defect-safe completion requires specifying whether $\psi$ is real,
complex, or gauge charged, deriving the symmetry-breaking bias, and
simulating the resulting inhomogeneous defect network. Until then,
no defect-free or cosmic-string claim is made for the real-$\psi$
truncation.

## Claims intentionally not made

PTUM does not claim to be:
- a solution of the cosmological low-entropy initial-condition problem or a derivation of the thermodynamic arrow of time,

- a UV-complete derivation of the pre-discharge background,
- a renormalizable single-field chiral-SM Yukawa coupling for \(\psi\): the gauge-invariant Higgs-dressed dimension-five EFT operator and its classical tree-level Hilbert tensor are now specified, but its Wilson matrices/cutoff are unfixed, its quantum/thermal effective action is incomplete, and no SM reheating dynamics or branching fractions are numerically evolved,
- a fully dynamical coupled inflation-to-waterfall calculation including quantum seeds, inhomogeneous growth, and backreaction; the corrected mass sign gives the intended stable-above/tachyonic-below threshold ordering, but the current single-field inflation and post-trigger homogeneous scan do not yet evolve the onset,
- a solution of the cosmological-constant problem,
- a unique microscopic theory of the dark sector,
- a replacement for LambdaCDM already favored by current data,
- a proof of any external cross-project mechanism.

## v1.1 cleanup

All external cross-project terminology has been removed from the PTUM manuscript. The paper now stands as a self-contained effective cosmology model.


## v1.2 historical code-availability statement (superseded)

An earlier version of this document stated that
`https://github.com/ErdemEsa/ptum-cosmology.git` publicly contained
a CLASS v3.2.0 patch and that its clean-tree apply check had passed.
That statement is retained here only as a historical author-reported
claim. The URL returned HTTP 404 through the current GitHub API review,
and the current canonical repository does not expose the patch as an
individually reviewable tracked source file. The claim of public patch
availability and reproducible application is therefore **UNVERIFIED**.
See `PTUM_REPRODUCIBILITY_NOTES.md` for the current evidence boundary.

The existence of an archive named `PTUM.zip` is not, by itself,
evidence that it contains the claimed patch or that the patch applies
to a clean CLASS v3.2.0 tree.

## 2026-11-13 scientific correction addendum

- The dimensionless fuel-potential convention is now
  $V(\Phi)=V_0[1-\exp(-\lambda_\Phi\Phi^2/M_{\rm Pl}^2)]$.
- The discharge threshold $\Phi_c=E_{\rm th}/\sqrt{\alpha}$ is independent of $\lambda_\Phi$; matching it to $\Phi_{\rm end}$ is an extra model condition.
- For $\lambda_\Phi=0.02$, the potential slow-roll proxy $\epsilon_V=1$ gives
  $\Phi_{\epsilon_V=1}\simeq1.387175M_{\rm Pl}$, but the exact canonical
  background endpoint $\epsilon_H=1$ is
  $\Phi_{\rm end}^{(H)}\simeq0.986228M_{\rm Pl}$ with
  $V(\Phi_{\rm end}^{(H)})/V_0\simeq0.0192649$. Threshold-matched scans
  now use the exact Hubble-flow endpoint. The previous assumption that
  the full $V_0$ is available at the threshold is withdrawn.
- The local Floquet monodromy solver is now available, but it is a frozen-background diagnostic. It does not calculate the expanding-background relic abundance.
- The full Standard Model Hilbert tensor, complete pre-CLASS dark-matter production, and the observational MCMC pipeline remain open verification items.


## Classical covariant action status (2026-11-13)

The branch now specifies a minimally coupled classical tree-level action for
Einstein gravity, the four real PTUM singlets, the complex SM Higgs doublet,
the three chiral SM fermion generations, and the
\(SU(3)_c\times SU(2)_L\times U(1)_Y\) gauge fields. The ordinary SM Yukawa
matrices and the distinct PTUM dimension-five matrices \(C_{u,d,e}/\Lambda\)
are separated. The gauge-invariant operator charges and canonical dimensions
are machine-checked in ptum_covariant_action.py. The tree-level symmetric
Hilbert tensor is written in vierbein/Belinfante form, and the sector currents
are assigned so that each interaction appears once and the pairwise currents
cancel.

This closes the classical action specification gap for the stated EFT; it
does not close the quantum/renormalized action, EFT/UV matching, thermal
effective-potential, or dynamical reheating gaps. The homogeneous numerical
solver still evolves only the \(\Phi\)--\(\psi\) truncation. The \(\psi\)
reflection symmetry is exact only in the scalar truncation when \(C_f=0\);
for nonzero \(C_f\), the odd dimension-five operator explicitly breaks it.
The induced domain-wall bias and network evolution remain unresolved.


## Additional scientific claim boundaries (2026-11-13)

- The residual dark-energy potential is written with dimensionless Planck-normalized exponentials. Its previously reported viable-region percentages remain author-reported until the exact scan script and parameter grid are reproducible.
- For Delta N_fluid = 0.10--0.31, the pfd-to-standard-neutrino-equivalent ratio is 3.3--10.2%, while its share of total radiation including photons, standard neutrinos and itself is about 1.3--4.0%.
- The quartic scalar coupling does not establish a numerical Wilsonian cutoff. The previously quoted 4 pi psi_0/sqrt(lambda_psi) energy cutoff is withdrawn; Lambda_EFT remains UV-dependent and the dimension-five reheating operator requires coupled-channel unitarity bounds.
- The linear waterfall-mode/spectrum solver evolves adiabatic vacuum modes and tachyonic amplification on a supplied background. It is not a nonlinear lattice calculation and does not establish backreaction, rescattering, defect avoidance or relic abundance.
- The minimal curved-space SM action and standard gauge/Higgs/on-shell fermion Hilbert tensors are explicit; the full interacting-sector divergence proof and a flavour benchmark remain open.
