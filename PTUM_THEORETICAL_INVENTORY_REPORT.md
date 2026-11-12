# PTUM Theoretical Inventory & Critical Gaps Report

**Date**: Current session
**Status**: Post-referee report revision (8/11 tasks complete, PDF compiles to 41 pages)

---

## Executive Summary

The PTUM manuscript has been revised to address 4 P0 (critical) and 4 P1 (major) issues from the referee report. The PDF compiles successfully. However, fundamental theoretical gaps remain in the **tachyonic-to-quartic transition mechanism** — the core dynamical claim of the model. This report inventories all theoretical assumptions, separates proven results from phenomenological closures, and identifies the 5 most critical scientific gaps.

---

## 1. Theoretical Assumptions Inventory (55 items)

| Category | Proven | Phenomenological | Assumed | Unresolved |
|----------|--------|------------------|---------|------------|
| Creation sector | 2 | 0 | 3 | 0 |
| Tachyonic-to-quartic | 4 | 1 | 5 | 0 |
| Sound speed | 3 | 1 | 0 | 0 |
| Energy-momentum | 4 | 0 | 2 | 0 |
| Dark matter | 3 | 1 | 5 | 0 |
| Reheating | 0 | 0 | 4 | 0 |
| EFT hierarchy | 4 | 0 | 0 | 0 |
| Observational | 6 | 0 | 0 | 0 |
| Open problems | 0 | 0 | 0 | 7 |
| **TOTAL** | **26** | **3** | **19** | **7** |

**Key insight**: Only 26/55 (47%) of theoretical elements are proven from first principles. The tachyonic-to-quartic transition — the model's central dynamical mechanism — has 5 assumed and only 4 proven elements.

---

## 2. Separation: Proven Results vs. Assumptions vs. Phenomenological Closures

### ✅ PROVEN (Derived from Lagrangian + validated numerically)

1. **Slow-roll inflation** from V(Φ) = V₀(1 - e^{-λΦ²}) — validated by exact-background integration (Δn_s ~ 5×10⁻⁴)
2. **Threshold condition**: m_eff²(Φ) = m²(1 - αΦ²/E_th²) changes sign at Φ_c = E_th/√α
3. **Tachyonic growth rate**: Γ_k ≈ √(|m_eff²| - k²/a²) for k ≲ a|m_eff|
4. **Quartic dominance condition**: |ψ| ≫ ψ₀ ⇔ λ_ψψ⁴ ≫ μ²ψ²
5. **Small oscillations about ±ψ₀**: m_osc² = 2μ², ⟨w⟩ ≈ 0 (matter-like)
6. **Virial theorem for quartic oscillator**: ⟨ψ̇²⟩ = 4⟨U⟩ → ⟨w⟩ = 1/3, ρ ∝ a⁻⁴
7. **Sound speed reconciliation**: c_a² = 1/3 (adiabatic), c_eff²(k,a) → 1/3 for observable modes
8. **Energy-momentum conservation**: ∑Q_i^ν = 0 identically from Lagrangian
9. **EFT hierarchy**: Λ_EFT ~ V₀¹/⁴ ~ 10¹⁵–10¹⁶ GeV, H_*/Λ_EFT ~ 10⁻³–10⁻⁴
10. **CLASS implementation**: ΛCDM recovery, gauge invariance, cross-code validation (CLASS vs CAMB <0.1%)
11. **Observational bounds**: ΔN_fluid < 0.31 (95% CL), phase-shift discriminator
12. **Isocurvature suppression**: β_iso ~ 10⁻¹²–10⁻⁶ ≪ Planck bounds

### ⚠️ PHENOMENOLOGICAL CLOSURES (Conditional, not derived)

1. **Proxy-fluid closure**: w_ψ = 1/3, c_s,ψ² = 1/3, σ_ψ = 0 in CLASS — *conditional on coherent quartic-dominated regime*
2. **Dark matter relic**: Ω_χh² ~ 0.12 is a *parametric resonance target*, not a CLASS output
3. **Reheating parametrization**: L_rh = -y_ψψf̄f - ½g_ψψ²φ_SM² — *phenomenological, not from UV completion*

### ❌ ASSUMED (Not derived, not validated)

**Tachyonic-to-quartic (5 critical assumptions):**
1. Transition to quartic oscillations occurs at ψ ~ ψ₀ (lattice claim, unverified)
2. Non-linear effects only significant after ψ reaches O(ψ₀) (lattice claim, unverified)
3. Energy transfer Φ→ψ consistent with Q_ψ ≈ -Q_Φ (lattice claim, unverified)
4. No topological defects produced (lattice claim, unverified)
5. Benchmark scales (μ ~ 10¹³ GeV, λ_ψ ~ 0.1, ψ₀ ~ 10¹³ GeV, H_* ~ 10¹³ GeV) do NOT demonstrate ω ≫ H_*

**Dark matter (5 assumptions):**
1. Φ_res oscillates with ω_res ~ 10¹³ GeV during discharge
2. Broad resonance regime q ≫ 1
3. Lattice μ_max = 0.198±0.005 ω_res matches analytic
4. Lattice Ω_χh² = 0.118±0.015 consistent with target
5. Φ_res dual role (high-freq during discharge, light DE today)

**Reheating (4 assumptions):**
1. Perturbative decay, parametric resonance, thermalization are separable
2. Γ_ψ ~ y²m_ψ/8π
3. T_rh ~ 10¹⁴–10¹⁵ GeV from instantaneous thermalization
4. Entropy production S_obs ~ 10⁸⁸

### ❓ UNRESOLVED (Explicitly acknowledged limitations)

1. Metastable background not derived from first principles
2. Cosmological constant problem: V_res/V₀ ~ 10⁻¹⁰⁸ reparameterizes, not solves
3. Reheating sector not specified from first principles
4. No concrete UV completion
5. Full self-consistent coupling of non-equilibrium resonance to post-discharge Boltzmann
6. Lattice simulation artifacts not publicly released
7. Production Cobaya YAML files and full MCMC chains not public

---

## 3. Five Most Critical Scientific Gaps (Priority Order)

### 🔴 GAP 1: Tachyonic-to-Quartic Transition — **Does it actually happen?**

**The core problem**: With initial conditions ψ(t_c) = 0, ψ̇(t_c) = 0 (field at top of barrier), the field oscillates between 0 and ψ₀. It **never reaches |ψ| ≫ ψ₀** required for quartic dominance.

- Energy at threshold: E_c = ¼λ_ψψ₀⁴
- Maximum amplitude: ψ_max = ψ₀ (for zero initial velocity)
- Quartic regime requires ψ ≫ ψ₀ → needs additional energy input

**CRITICAL NUMERICAL FINDINGS** (from Task 1 simulation with baseline parameters V0=1e64, λ_ψ=0.1, μ=1e13 GeV):

| Scenario | V0 | H at Φ_c | H/μ | Damping 3H/(2ω) | Max |ψ|/ψ₀ | Zero Crossings | ⟨w⟩ | Q | Virial | Quartic? |
|----------|-----|----------|-----|-----------------|-----------|----------------|-----|-----|--------|----------|
| Baseline (ψ=0, ψ̇=0) | 1e64 | 1.25e13 | 1.25 | 1.33 (overdamped) | 1.0 | 0 | -1.0 | 1.0 | 0.0 | ❌ No |
| ψ=0.5ψ₀, ψ̇=0.5μψ₀ | 1e64 | 1.25e13 | 1.25 | 1.33 | 1.85 | 0 | -0.37 | 1.0 | 0.02 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1e64 | 1.25e13 | 1.25 | 1.33 | 1.85 | 0 | -0.37 | 1.0 | 0.02 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1.58e63 | 4.97e12 | 0.50 | 0.53 | 2.24 | 1 | -0.84 | 0.99 | 0.001 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1e58 | 1.25e10 | 0.00125 | 0.0013 | 2.67 | 127 | **0.46** | **3.37** | **0.92** | ✅ **Yes** |
| Fixed φ=1.1Φ_c, no H | — | 0 | 0 | 0 | 2.64 | 145 | **0.42** | **5.10** | **0.77** | ✅ **Yes** |

**Key Conclusions**:
1. **Original V0=1e64 is 6.3× too large** for oscillations (critical V0 ≈ 1.58e63 for 3H/(2ω)=1)
2. **Even at critical V0**, field crosses zero only ONCE then settles at ψ₀ — no sustained quartic regime
3. **Quartic regime ONLY achieved when H ≪ μ** (V0 ≤ 1e58) AND large initial kinetic energy
4. **Without Hubble damping**, quartic regime is natural (w→1/3, Q→5, Virial→1)
5. **The coupling term (αm²/E_th²)Φψ² is essential** — it provides energy transfer from Φ to ψ during Φ's roll past Φ_c

**What's missing**:
- Demonstration that time-dependent m_eff²(Φ(t)) evolution provides energy
- Demonstration that energy transfer from Φ field pushes ψ into quartic regime
- Numerical background evolution showing actual trajectory

**Current status**: Manuscript treats quartic-fluid as "phenomenological late-time closure conditional on quartic-dominance and rapid-oscillation conditions" (Sec 3.5.6). Lattice claims transition occurs but artifacts not released.

**Required**: Task 1 numerical research plan (created) to map parameter space where transition succeeds/fails.

---

### 🔴 GAP 2: Dark Matter Production — **Self-consistent parametric resonance?**

**The problem**: Ω_χh² ~ 0.12 is a *target benchmark* from parametric resonance during discharge, but:
- Φ_res has dual role: ω_res ~ 10¹³ GeV during discharge, m ~ H₀ today
- Resonance calculation assumes Φ_res oscillation amplitude, which depends on discharge dynamics (Gap 1)
- Lattice results (μ_max, Ω_χh²) not independently verified
- No coupling of non-equilibrium resonance to post-discharge Boltzmann evolution

**Current status**: Clarified in P1 Task 1 fix that this is a target, not CLASS output. But production mechanism remains conditional on unverified discharge dynamics.

---

### 🔴 GAP 3: Reheating — **No self-consistent temperature calculation**

**The problem**: T_rh ~ 10¹⁴–10¹⁵ GeV comes from two inconsistent estimates:
1. Perturbative: T_rh ~ √(Γ_ψM_Pl) with Γ_ψ ~ y²m_ψ/8π
2. Instantaneous: T_rh ~ (30V₀/π²g_*)¹/⁴

Neither includes:
- Condensate-averaged decay rate
- Branching fractions
- Non-perturbative particle production
- Thermalization efficiency
- Backreaction on ψ oscillations

**Current status**: Manuscript explicitly states "No numerical value of T_rh is claimed... not computed self-consistently" (Sec 7.3).

---

### 🔴 GAP 4: Lattice Simulations — **Not independently reproducible**

**The problem**: Appendix B reports lattice results that are **author-reported, not independently auditable**:
- Code version, input parameters, random seeds not released
- Raw field snapshots, diagnostic outputs not released
- Convergence tests not publicly available
- Docker image referenced but not verified as public

**Current status**: Reproducibility notes acknowledge "lattice calculation should be treated as unverified until code version, input parameters, random seeds, convergence tests, raw outputs, and analysis scripts are released."

---

### 🔴 GAP 5: Full Bayesian Pipeline — **Not end-to-end public**

**The problem**: 
- CLASS patch is public ✅
- Cobaya production YAML files: **pending**
- Full MCMC chains: **pending or external archive**
- CI/build logs: **not available**

**Current status**: Reproducibility notes explicitly state "The full Bayesian pipeline should not yet be described as completely end-to-end public."

---

## 4. Implications for Manuscript Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| "PTUM generates radiation-like proxy fluid" | **Conditional** | Requires quartic regime (Gap 1 unverified) |
| "Ω_χh² ~ 0.12 from parametric resonance" | **Target benchmark** | Not a derived result (Gap 2) |
| "T_rh ~ 10¹⁴–10¹⁵ GeV" | **Estimate only** | Not self-consistent (Gap 3) |
| "Lattice confirms linear perturbation results" | **Unverified** | Artifacts not public (Gap 4) |
| "Bayesian analysis constrains ΔN_fluid < 0.31" | **Validated** | CLASS patch public, but full pipeline not (Gap 5) |
| "EFT hierarchy self-consistent" | **Proven** | P0 Task 4 fix complete |
| "Sound speed contradiction resolved" | **Proven** | P0 Task 2 fix complete |
| "Energy-momentum conservation closed" | **Proven** | P0 Task 3 fix complete |

---

## 5. Recommended Path Forward

### Immediate (before resubmission):
1. **Complete Task 1 numerical research** — determine if/when quartic regime is reached
2. **Release lattice artifacts** — code, configs, seeds, outputs, analysis scripts
3. **Release Cobaya YAML files and MCMC chain summaries**
4. **Add explicit caveats** in manuscript where claims depend on Gap 1-3

### Medium-term (next paper/revision):
1. **Self-consistent reheating calculation** — kinetic theory or lattice + Boltzmann
2. **Coupled resonance + Boltzmann evolution** for DM production
3. **UV completion exploration** — string theory embedding or alternative

### Long-term:
1. **First-principles derivation** of metastable background
2. **Dynamical solution** to cosmological constant hierarchy
3. **Full non-perturbative discharge simulation** with all sectors

---

## 6. Files Created This Session

1. **TASK1_TACHYONIC_QUARTIC_RESEARCH_PLAN.md** — Complete mathematical derivation framework and numerical implementation plan for Task 1
2. **PTUM_THEORETICAL_INVENTORY_REPORT.md** — This report

---

**Bottom line**: The manuscript is now internally consistent and addresses referee's specific technical objections. However, the **central dynamical claim (tachyonic→quartic transition) remains unverified**. The model should be presented as: *"An effective framework where a threshold-triggered discharge CAN generate [dark sectors], conditional on the quartic-dominance regime being dynamically achieved — which requires further numerical demonstration."*

This honest framing aligns with the PTUM_CLAIM_BOUNDARY.md and the referee's demand for "mathematically and physically verifiable" theory.