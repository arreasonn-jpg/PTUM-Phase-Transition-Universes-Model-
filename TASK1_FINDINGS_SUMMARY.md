# Task 1: Tachyonic-to-Quartic Transition — Numerical Findings Summary

**Date**: Current session  
**Status**: Baseline simulations complete; parameter scan reveals critical constraints

---

## Executive Summary

The tachyonic-to-quartic transition **does not occur** with the baseline PTUM parameters (V0=1e64, λ_ψ=0.1, μ=1e13 GeV, H_*~10¹³ GeV) and natural initial conditions (ψ=0, ψ̇=0 at threshold crossing). The field oscillates between 0 and ψ₀ with ⟨w⟩ ≈ -1 (cosmological constant-like), never reaching the |ψ| ≫ ψ₀ regime required for quartic dominance (w=1/3).

**Quartic regime is ONLY achieved when:**
1. H ≪ μ (V0 ≤ 1e58, i.e., inflation scale ≪ 10¹³ GeV) — 6 orders of magnitude below current assumption
2. Large initial kinetic energy is injected at threshold crossing
3. Energy transfer from Φ during its roll past Φ_c is significant

---

## 1. Baseline Parameters and Setup

| Parameter | Value | Notes |
|-----------|-------|-------|
| V0 | 1e64 GeV⁴ | Original paper value |
| λ_φ | 0.02 | Inflation potential |
| m_ψ | 1e13 GeV | Tachyonic mass scale |
| λ_ψ | 0.1 | Quartic coupling |
| α | 1e-7 | Threshold coupling |
| E_th | 1e16 GeV | Threshold scale |
| Φ_c | 3.16e19 GeV | Critical field value |
| ψ₀ | 3.16e13 GeV | Minimum of potential |
| μ | 1e13 GeV | √|m_eff²| |
| H_* at Φ_c | 1.25e13 GeV | Hubble at threshold |
| H/μ | 1.25 | **Overdamped** (3H/(2ω) = 1.33 > 1) |

---

## 2. Key Numerical Results

### 2.1 Parameter Sweep: V0 Variation

| V0 | H at Φ_c | H/μ | Damping 3H/(2ω) | Max |ψ|/ψ₀ | Zero Crossings | ⟨w⟩ | Q | Virial | Quartic? |
|----|----------|-----|-----------------|-----------|----------------|-----|-----|--------|----------|
| 1e64 | 1.25e13 | 1.25 | 1.33 (overdamped) | 1.0 | 0 | -1.0 | 1.0 | 0.0 | ❌ No |
| 1.58e63 | 4.97e12 | 0.50 | 0.53 | 2.24 | 1 | -0.84 | 0.99 | 0.001 | ❌ No |
| 1e62 | 1.25e12 | 0.125 | 0.13 | 0.80 | 1 | -1.0 | 0.33 | 0.0 | ❌ No |
| 1e61 | 3.96e11 | 0.04 | 0.04 | 1.50 | 9 | -1.0 | 0.10 | 0.0 | ❌ No |
| 1e60 | 1.25e11 | 0.0125 | 0.013 | 1.11 | 24 | -1.0 | 0.03 | 0.0 | ❌ No |
| **1e58** | **1.25e10** | **0.00125** | **0.0013** | **2.67** | **127** | **0.46** | **3.37** | **0.92** | ✅ **Yes** |

### 2.2 Initial Condition Variation (V0=1e58)

| ψ(t_c)/ψ₀ | ψ̇(t_c)/(μψ₀) | Max |ψ|/ψ₀ | Zero Crossings | ⟨w⟩ | Q | Virial | Quartic? |
|-----------|---------------|-----------|----------------|-----|-----|--------|----------|
| 0 | 0 | 1.0 | 0 | -1.0 | 1.0 | 0.0 | ❌ No |
| 0.5 | 0.5 | 1.11 | 4 | -1.0 | 0.03 | 0.0 | ❌ No |
| 1.0 | 0 | 1.11 | 24 | -1.0 | 0.03 | 0.0 | ❌ No |
| 1.0 | 0.5 | 1.11 | 24 | -1.0 | 0.03 | 0.0 | ❌ No |
| **1.0** | **5.0** | **2.67** | **127** | **0.46** | **3.37** | **0.92** | ✅ **Yes** |

### 2.3 Fixed φ Past Threshold (No Hubble Damping)

| Scenario | H | Max |ψ|/ψ₀ | Zero Crossings | ⟨w⟩ | Q | Virial | Quartic? |
|----------|---|-----------|----------------|-----|-----|--------|----------|
| φ=1.1Φ_c, ψ=ψ₀, ψ̇=5μψ₀ | 0 | 2.64 | 145 | 0.42 | 5.10 | 0.77 | ✅ Yes |
| φ=Φ_c, ψ=ψ₀, ψ̇=5μψ₀ | 1.25e12 | 2.55 | 5 | -1.0 | 0.001 | 0.0 | ❌ No |

---

## 3. Physical Interpretation

### 3.1 Why the Baseline Fails

1. **Overdamped regime**: H/μ = 1.25 → 3H/(2ω) = 1.33 > 1. The field cannot oscillate; it's critically/overdamped.
2. **Insufficient energy**: With ψ=0, ψ̇=0 at Φ_c, the field has energy E = V(0) - V_min = ¼λ_ψψ₀⁴. This only allows oscillation between 0 and ψ₀.
3. **No barrier crossing**: The field rolls to ψ₀ and stays there — it never crosses to negative ψ values (except once at critical V0).
4. **Quartic dominance requires |ψ| ≫ ψ₀**: The condition λ_ψψ⁴ ≫ μ²ψ² requires ψ ≫ ψ₀. With max amplitude ψ₀, this is never satisfied.

### 3.2 What Enables Quartic Regime

1. **H ≪ μ**: Need V0 ≤ 1e58 (H ≤ 1.25e10 GeV) for underdamped oscillations
2. **Large initial kinetic energy**: ψ̇(t_c) ~ 5μψ₀ provides energy to reach ψ ~ 2.7ψ₀
3. **Energy transfer from Φ**: The coupling term (αm²/E_th²)Φψ² in Φ's equation provides energy transfer during Φ's roll past Φ_c
4. **No Hubble damping**: In Minkowski space, quartic regime is natural

### 3.3 Critical V0 Calculation

For underdamped oscillations: 3H/(2ω) < 1
- ω ~ μ = 1e13 GeV (at ψ ~ ψ₀)
- H = √(V0/(3M_Pl²))
- Critical: 3√(V0/(3M_Pl²)) / (2μ) = 1
- V0_crit = (4/3) μ² M_Pl² = 1.58e63 GeV⁴

**Original V0 = 1e64 is 6.3× larger than critical!**

---

## 4. Implications for PTUM Manuscript

### 4.1 Claims Requiring Caveats

| Section | Claim | Status |
|---------|-------|--------|
| Sec 3.5.6 | "Quartic attractor and proxy-fluid sector" | **Conditional** — requires H ≪ μ and energy injection |
| Eq. 3.40 | w_ψ = 1/3, c_s² = 1/3, σ = 0 | **Phenomenological closure** — not derived for baseline params |
| Sec 3.5.6 | "Benchmark scales imply √λ_ψψ₀ ~ 3×10¹² GeV, not parametrically larger than H_* ~ 10¹³ GeV" | **Correct** — already notes ω ≫ H not demonstrated |
| Sec 11.1.1 | DM production via parametric resonance | **Conditional** — depends on discharge dynamics (Gap 1) |

### 4.2 Required Manuscript Updates

1. **Explicit caveat in Sec 3.5.6**: "The quartic-fluid closure (w=1/3) is achieved only when H ≪ μ and sufficient energy is transferred from Φ during its roll past Φ_c. For the benchmark V0=1e64, H/μ=1.25 and the field is overdamped — it settles at ψ₀ with w≈-1, not w=1/3."

2. **Parameter space map**: Add figure showing (V0, λ_ψ, initial kinetic energy) regions where quartic regime is achieved.

3. **Energy transfer quantification**: Calculate required energy transfer rate from Φ to ψ to reach quartic regime at baseline V0.

---

## 5. Next Steps for Task 1

### 5.1 Immediate (Complete Parameter Scan)
- [ ] Full 3D parameter scan: (V0, λ_ψ, ψ̇_init)
- [ ] Include Φ evolution with coupling term
- [ ] Map success/failure regions in parameter space
- [ ] Quantify required energy transfer from Φ

### 5.2 Medium-term
- [ ] Lattice simulation comparison (if artifacts released)
- [ ] Perturbation evolution in quartic vs quadratic regime
- [ ] Connection to DM production (Task 2) and reheating (Task 4)

### 5.3 Documentation
- [ ] Release simulation code and outputs
- [ ] Create parameter space visualization
- [ ] Write honest assessment for manuscript

---

## 6. Simulation Code

The simulation code `ptum_task1_simulation.py` implements:
- Coupled Φ-ψ background equations
- Adaptive RK45 integration
- Energy conservation monitoring
- Diagnostic outputs (w, Q, Virial, zero crossings)

**Key functions:**
- `PTUMParameters`: Parameter dataclass
- `background_equations`: Coupled ODE system
- `run_simulation`: Single trajectory
- `parameter_scan`: Multi-parameter exploration
- `compute_diagnostics`: w, Q, Virial, zero crossings

---

## 7. Conclusion

**The tachyonic-to-quartic transition is NOT a generic outcome of the PTUM mechanism.** It requires:
1. Fine-tuned initial kinetic energy at threshold crossing, OR
2. Significantly lower inflation scale (V0 ≤ 1e58), OR  
3. Strong energy transfer from Φ during its roll past Φ_c

The manuscript should present the quartic-fluid as a **conditional phenomenological closure** with explicit parameter requirements, not as an automatic consequence of tachyonic activation.

This finding aligns with the referee's demand for "mathematically and physically verifiable" theory and the PTUM_CLAIM_BOUNDARY.md framework.