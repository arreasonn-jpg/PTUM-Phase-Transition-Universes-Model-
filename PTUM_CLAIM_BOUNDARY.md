# PTUM Claim Boundary v1.2 CLEAN (updated with Task 1 numerical findings)

## Safe core claim

PTUM is an effective phenomenological cosmological framework that parametrizes a threshold-triggered discharge and its candidate dark-matter, residual dark-energy-like, and proxy-fluid dark-radiation sectors. The current homogeneous simulation does not yet establish their microscopic production or the required energy partition.

The sharp observational discriminator is the difference between fluid-like dark radiation and free-streaming relativistic species. In the effective linear proxy-fluid closure, the pfd component has

```text
w = 1/3, c_s^2 = 1/3, sigma = 0
```

and therefore does not produce the neutrino-like CMB acoustic phase shift associated with free-streaming radiation.

## Current-data status

The benchmark analysis gives

```text
Delta chi^2 = -0.26
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

The threshold-matched scan now sets $\Phi_c$ from the exact Hubble-flow endpoint, not the older potential slow-roll estimate $\Phi_{\epsilon_V=1}\simeq1.387M_{\rm Pl}$. For $\lambda_\Phi=0.02$, the exact endpoint is $0.986228M_{\rm Pl}$ and the updated local damping ratio is about $3.48$.

The old 36-point scan used the opposite sign and is historical only.
The revised code, manuscript, and tests must pass a fresh CI scan
before any new regime conclusion is accepted. The onset itself still
requires coupled quantum/inhomogeneous evolution and backreaction.
The pre-exact-endpoint revised-sign revision passed 25 regression tests in run 43393188155. The current branch additionally matches the threshold to the exact $\epsilon_H=1$ endpoint and adds an inflation-end regression test; its fresh 26-test suite, 100-point high-resolution scan, and LaTeX build are pending. No scan conclusion is claimed until that run completes.

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

For the threshold-matched benchmark $\Phi_c\simeq\Phi_{\rm end}\simeq1.387M_{\rm Pl}$, the potential-dominated local estimate is $3H_c/(2\mu)\simeq4.9>1$; the plateau-scale estimate is $3H_*/(2\mu)\simeq25$. The two-field homogeneous truncation is overdamped in this potential-dominated estimate. This makes quartic oscillations unlikely for the matched benchmark, but the actual outcome must be determined from the corrected 18-point scan and the local $H(t)$ trajectory. A nonzero seed and coupled transfer terms must be followed before making a definitive all-initial-conditions statement.

A conservative sufficient low-scale regime is:
1. $V_0 \lesssim 10^{58}\,\mathrm{GeV}^4$ ($H_* \lesssim 10^{10}\,\mathrm{GeV}$), which gives underdamped motion with a large margin in the threshold-matched estimate
2. Sufficient initial kinetic energy in $\psi$ to cross the barrier
3. Continuing energy input from rolling $\Phi$ field or rescattering

The proxy-fluid closure $w=1/3$, $c_s^2=1/3$, $\sigma=0$ is therefore a **phenomenological ansatz conditional on parameters not realized in the stated benchmark**. The observational discriminator applies *if* the quartic regime is realized; it is not a prediction of the benchmark parameters alone. The Bayesian constraints on $\Delta N_{\rm fluid}$ should be interpreted as constraints on the *phenomenological proxy-fluid model*, not as constraints on the microscopic PTUM discharge dynamics with the stated benchmark parameters.

## Claims intentionally not made

PTUM does not claim to be:
- a solution of the cosmological low-entropy initial-condition problem or a derivation of the thermodynamic arrow of time,

- a UV-complete derivation of the pre-discharge background,
- a complete gauge-invariant chiral Standard Model reheating interaction or full SM Hilbert-tensor derivation; the displayed Dirac coupling is generic EFT shorthand pending specification,
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
- For $\lambda_\Phi=0.02$, the tree-level single-field estimate gives
  $\Phi_{\rm end}\simeq1.387M_{\rm Pl}$ and
  $V(\Phi_{\rm end})/V_0\simeq0.0378$. The previous assumption that the full $V_0$ is available at the threshold is withdrawn.
- The local Floquet monodromy solver is now available, but it is a frozen-background diagnostic. It does not calculate the expanding-background relic abundance.
- The full Standard Model Hilbert tensor, complete pre-CLASS dark-matter production, and the observational MCMC pipeline remain open verification items.
