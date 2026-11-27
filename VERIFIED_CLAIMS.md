# PTUM Verified Claims Registry

This document tracks every quantitative claim from the PTUM manuscript that
has been independently verified by a standalone reimplementation and/or
matched against the production code. Each entry records:

- **Claim ID**: unique identifier
- **Location**: section / equation / table in `main.tex`
- **Method**: how it was verified
- **Status**: VERIFIED / CLARIFIED / CORRECTED / PENDING

---

## Tier 1: Numeric claims fully verified

### V1. `tab:exactscan` (main.tex Section 3.3)
**Status: VERIFIED** (triple-redundant)
- Production code: `ptum_inflation_background.py::compute_observables`
- Independent code: `verify_tab_exactscan.py`
- Colab cross-check: DOP853 + bracketed brentq (separate environment)
- Result: 8/8 rows match to `max rel = 1.42e-09`
- Commit: `1c3b32d`

### V2. Section 3.4 identities
**Status: VERIFIED**
- Production keys match paper text exactly:
  - `x_end_slow_roll` = 1.3871750383 (paper: 1.387175)
  - `x_end_hubble_flow` = 0.9862280831 (paper: 0.986228)
  - `epsilon_V_at_hubble_end` = 2.0165698791 (paper: 2.01657)
  - `V_end_over_V0` = 0.0192649296 (paper: 0.01926493)
  - `kinetic_end_over_V0` = 0.0096324648 (paper: 0.00963246)
  - `rho_end_over_V0` = 0.0288973944 (paper: 0.02889739)
  - `old_potential_end_threshold_lead_efolds` = 0.3185198402 (paper: 0.31852)
  - `epsilon_2_star` = 0.0391699924 (paper: 0.03917)

### V3. Section 2.6 domain-wall tension
**Status: VERIFIED** (Colab, independent BVP)
- Formula: sigma_wall = 2*sqrt(2)/3 * mu^3 / lambda
- Numerical BVP energy: 0.9428115611 (2*sqrt(2)/3 = 0.9428090416)
- rel diff: 2.67e-06
- kink profile: max|psi_BVP - tanh(z/sqrt(2))| = 1.44e-06

### V4. Section 2.4 18-point scan
**Status: VERIFIED** (SHA-256 byte-for-byte)
- Reference: SHA = 5738649b6e6322396e36ca60dbf6aef8eacc80a19205ee64123213eac6bf7187
- Reproduced: identical SHA on Colab DOP853

### V5. Section 4.2 gamma(z) analytic form
**Status: VERIFIED as LambdaCDM identity**
- c = 0.3854 -> gamma(0) = 0.721813 (paper 0.722) OK
- NOTE: "residual < 1e-14" applies only in the exact w_DE = -1 limit
- For 1+w_DE ~ 1e-3, |Delta gamma / gamma| ~ 5e-3 (visible in CLASS)
- Action: paper Section 4.2 should rephrase as "LambdaCDM limit check"

### V6. Section 3.5 Mukhanov-Sasaki 200-mode
**Status: VERIFIED** (Colab, independent DOP853)
- n_s fit vs n_s_HF: +3.5e-4 to +5.7e-4 across 4 lambdas
- V_0^{1/4} = 5.8e15 to 1.27e16 GeV (matches Section 3.4 range)
- Quadratic residual < 5.2e-5 (paper: <1e-4)
- Action: "author-reported" tag can be removed

### V7. Mathieu narrow-resonance (q << 1)
**Status: VERIFIED** (Colab, numerical Floquet)
- mu_z/q = 0.484 to 0.500 for q in [0.01, 1.0]
- Paper's "0.2 omega_res was narrow-resonance estimate" retraction:
  q ~ 0.4 confirmed

---

## Tier 2: Claims requiring clarification

### C1. `3H/(2 mu)` benchmark values
**Status: CLARIFIED** (3 different mu reference points)
- Paper: 3.50 / 4.29 / 25 -> mu = 2.32e12 GeV at Phi/Phi_c ~ 0.9727
- Code default: mu = 1.42e12 at Phi/Phi_c = 1.01
- Plateau value: mu = 1.0e13
- Physical conclusion (overdamped): unchanged in all three cases
- Action: paper Section 2.4 should state the reference point for mu

### C2. Section 4.2 "residual < 1e-14"
**Status: CLARIFIED** (misleading phrasing)
- True in exact w_DE = -1 limit only
- In viable region (1+w_DE < 0.01): residual can reach 5e-3
- Action: rephrase as "LambdaCDM limit consistency check"

---

## Tier 3: Claims found incorrect

### X1. Mathieu q definition (Section Discussion)
**Status: FACTOR-2 ERROR + SIGN**

**Paper:** q ≡ g_DM A_res^2 / omega_res^2   (positive, coefficient 1)
**Code:**  q = -g_dm A_res^2 / (2 omega_res^2)   (negative, coefficient 1/2)

Physical derivation from chi Lagrangian:
  L = -1/2 (d chi)^2 - 1/2 m_chi^2 chi^2 - g chi^2 Phi_res^2
  EOM: chi'' + 3H chi' + (k^2/a^2 + m_chi^2 + 2g Phi_res^2) chi = 0
  With Phi_res = A cos(omega t):
    2g A^2 cos^2(omega t) = g A^2 (1 + cos(2 omega t))
  Standard Mathieu form X'' + [A_k - 2q cos(2z)] X = 0, z = omega t:
    -2q = +g A^2 / omega^2  =>  q = -g A^2 / (2 omega^2)

Conclusion: **Code matches physical derivation; paper formula has factor 2
in the numerator (instead of 1/2) and wrong sign convention.**

Impact on paper's claims:
- Narrow-regime mu_max ~ |q|/2 estimate: paper is 2x too large
- Broad-regime "mu_max ~ q omega/2" formula uses 2x q: also incorrect
- PTUM benchmark (q ~ 0.1 in code's convention) — used only for illustration
  in Discussion, no quantitative prediction depends on it

Action: fix paper's q definition OR state explicitly that paper's q is
2x the standard Mathieu q in the X'' + [A - 2q cos(2z)]X = 0 convention.

### X2. Mathieu broad-resonance formula (q >> 1)
**Status: INCORRECT EXTRAPOLATION** (independent of X1)
- Paper: "For q >> 1, mu_max ~ q omega_res / 2"
- Numerical (q=100, physical band A_k in [0, 1.5]): mu_max/(q/2) = 0.105
- Deep-band asymptotic (A_k = -2q): mu_z/sqrt(q) -> 4/pi = 1.2732
- Physical band asymptotic: mu_max ~ sqrt(|q|), not linear in q
- Action: restrict formula to q <~ 1 (narrow); add numerical result for q >> 1

---

## Summary

| Tier | Count |
|------|-------|
| VERIFIED | 7 |
| CLARIFIED | 2 |
| CORRECTED | 2 |
| PENDING | (CLASS patch, Cobaya chains) |

## Additional finding: Production modules are comprehensive

All paper sections have corresponding production code:
- ptum_inflation_background.py (320 lines) -> tab:exactscan + Section 3.4
- ptum_task1_simulation.py (74 KB) -> Sections 2.3-2.5
- ptum_task1_scan.py -> Section 2.4 (100-point scan)
- ptum_solver_crosscheck.py (104 KB) -> Section 2.4 (DOP853/Radau/BDF)
- ptum_floquet.py (18 KB) -> Section Discussion (Mathieu/Floquet)
- ptum_waterfall_modes.py (11.5 KB) -> Sections 2.5, 3.5
- ptum_defects.py (12.9 KB) -> Section 2.6

Therefore the "author-reported" labels in the paper correspond to
author-verified but not independently reproduced quantities. This
document represents the independent verification layer.

Generated by independent verification against repository commits
`5fd2ee6` through `1c3b32d`. All numeric verifications use DOP853 at
rtol=1e-10, atol=1e-12, unless otherwise noted.

### X3. Low-scale quartic classification (paper vs code)

Paper §2.4: "No trajectory passes the joint quartic classifier."
Code (DOP853 full profile, current HEAD): **5 low-scale rows** ARE `quartic_achieved=True`.

Five rows (psi_init=2.23e13 GeV, phi_offset=0.01 Phi_c):
Q=10.6-11.1, w=0.372-0.374, virial=0.906-0.910, n_late=4-5, adiabatic=True.

Classification thresholds in ptum_task1_simulation.py::classify_outcome:
  virial_ratio defined as <K>/(2<V4>) -> quartic = 1.0
  5 rows virial~0.906 (within 10% of 1.0) -> classified quartic

Code is correct; paper's "0 quartic" statement predates current classifier
or refers to a different virial convention. The 5 rows do NOT establish a
sustained attractor but the automated classifier reports them as quartic.

Impact: paper §2.4 should acknowledge the 5 low-scale quartic-flagged rows.
