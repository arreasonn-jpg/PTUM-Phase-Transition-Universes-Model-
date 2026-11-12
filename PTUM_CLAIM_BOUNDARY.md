# PTUM Claim Boundary v1.2 CLEAN (updated with Task 1 numerical findings)

## Safe core claim

PTUM is an effective phenomenological cosmological framework in which a threshold-triggered discharge event can generate a dark-matter candidate sector, a residual near-Lambda dark-energy-like sector, and a proxy-fluid dark-radiation component.

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

## Critical numerical finding (Task 1)

**The quartic-dominated regime (w=1/3) is NOT achieved with the benchmark parameters stated in the paper.**

Numerical integration of the coupled background equations with:
- $V_0 \sim 10^{64}\,\mathrm{GeV}^4$ ($H_* \sim 10^{13}\,\mathrm{GeV}$)
- $m_\psi \sim 10^{13}\,\mathrm{GeV}$, $\lambda_\psi \sim 0.1$
- $\psi(t_c)=0$, $\dot{\psi}(t_c)=0$ (field at top of barrier)

Shows the system is **overdamped**: $3H/(2\mu) \approx 25 \gg 1$. The field remains at $\psi=0$ with $w_\psi=0$. The quartic regime is never reached.

Achieving the quartic regime requires:
1. $V_0 \lesssim 10^{58}\,\mathrm{GeV}^4$ ($H_* \lesssim 10^{10}\,\mathrm{GeV}$) for underdamped oscillations
2. Sufficient initial kinetic energy in $\psi$ to cross the barrier
3. Continuing energy input from rolling $\Phi$ field or rescattering

The proxy-fluid closure $w=1/3$, $c_s^2=1/3$, $\sigma=0$ is therefore a **phenomenological ansatz conditional on parameters not realized in the stated benchmark**. The observational discriminator applies *if* the quartic regime is realized; it is not a prediction of the benchmark parameters alone. The Bayesian constraints on $\Delta N_{\rm fluid}$ should be interpreted as constraints on the *phenomenological proxy-fluid model*, not as constraints on the microscopic PTUM discharge dynamics with the stated benchmark parameters.

## Claims intentionally not made

PTUM does not claim to be:

- a UV-complete derivation of the pre-discharge background,
- a solution of the cosmological-constant problem,
- a unique microscopic theory of the dark sector,
- a replacement for LambdaCDM already favored by current data,
- a proof of any external cross-project mechanism.

## v1.1 cleanup

All external cross-project terminology has been removed from the PTUM manuscript. The paper now stands as a self-contained effective cosmology model.


## v1.2 corrected code-availability update

The exact public repository is:

```text
https://github.com/ErdemEsa/ptum-cosmology.git
```

The repository contains the public PTUM `CLASS v3.2.0` patch. This supports a code-availability claim for the core Boltzmann-code implementation. It does not by itself complete the full public Bayesian pipeline, because production Cobaya YAML files and full MCMC chains remain pending or external-archive items.
