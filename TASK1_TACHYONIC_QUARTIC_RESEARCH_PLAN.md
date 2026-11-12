# Task 1: Tachyonic-to-Quartic Transition — Mathematical & Numerical Research Plan

**Objective**: Rigorously establish whether and under what conditions the PTUM proxy field ψ transitions from tachyonic growth to a quartic-dominated oscillatory regime with radiation-like equation of state (w = 1/3).

---

## 1. Mathematical Derivation (Analytic Foundation)

### 1.1 Homogeneous Field Equation from Existing Potential

**Starting point**: The activation sector Lagrangian (Eq. 3.9 in main.tex):
```
L_act = ½(∂_μψ)² - ½m²(1 - αΦ²/E_th²)ψ² - ¼λ_ψψ⁴
```

**Effective potential** (Eq. 3.34):
```
V_act(ψ) = ½m_eff²ψ² + ¼λ_ψψ⁴,  where m_eff² = m²(1 - αΦ²/E_th²)
```

**After threshold crossing** (Φ > Φ_c = E_th/√α): m_eff² < 0. Define μ² ≡ |m_eff²|.

**Shifted potential** (Eq. 3.35) — energy measured from minimum:
```
U(ψ) = V_act(ψ) - V_min = ¼λ_ψ(ψ² - ψ₀²)² ≥ 0
where ψ₀² = μ²/λ_ψ,  V_min = -μ⁴/(4λ_ψ)
```

**Homogeneous EOM in FRW** (Eq. 3.36):
```
ψ̈ + 3Hψ̇ - μ²ψ + λ_ψψ³ = 0
```

**Energy density and pressure** (Eq. 3.38):
```
ρ_ψ = ½ψ̇² + U(ψ)
p_ψ = ½ψ̇² - U(ψ)
w_ψ = (½ψ̇² - U) / (½ψ̇² + U)
```

**Conservation equation** (for uncoupled homogeneous field):
```
ρ̇_ψ = -3Hψ̇²
```

### 1.2 Regime Classification (Analytic)

| Regime | Condition | Oscillation Type | ⟨w_ψ⟩ |
|--------|-----------|------------------|-------|
| Tachyonic growth | |ψ| ≪ ψ₀, linear | Exponential growth | N/A (not oscillating) |
| Quadratic (matter-like) | |ψ - ψ₀| ≪ ψ₀ | Harmonic, m_osc² = 2μ² | ≈ 0 |
| **Quartic (radiation-like)** | **|ψ| ≫ ψ₀** | **Anharmonic, U ≃ ¼λ_ψψ⁴** | **= 1/3** |
| Barrier crossing | Energy > V_barrier | Crosses between ±ψ₀ | Transitional |

**Quartic dominance condition** (Eq. 3.37):
```
λ_ψψ⁴ ≫ μ²ψ²  ⇔  |ψ| ≫ ψ₀
```

**Virial theorem for quartic oscillator** (rapid oscillations, ω ≫ H):
```
⟨ψ̇²⟩ = 4⟨U⟩  →  ⟨p_ψ⟩ = ⟨ρ_ψ⟩/3  →  ⟨ρ_ψ⟩ ∝ a⁻⁴
```

### 1.3 Key Analytic Questions to Resolve

1. **Initial conditions at threshold crossing**: What are ψ(t_c), ψ̇(t_c) when Φ = Φ_c?
   - Current assumption: ψ(t_c) ≈ 0, ψ̇(t_c) ≈ 0 (field at top of barrier)
   - Need: Quantum fluctuation spectrum δψ_k ~ H_*/2π as initial seeds

2. **Does the field reach |ψ| ≫ ψ₀?**
   - Energy at t_c: E_c ≈ V(0) - V_min = μ⁴/(4λ_ψ) = ¼λ_ψψ₀⁴
   - Maximum amplitude: ψ_max = ψ₀ (for zero initial velocity)
   - **CRITICAL NUMERICAL FINDING**: With ψ(t_c)=0, ψ̇(t_c)=0, the field oscillates between 0 and ψ₀ — it NEVER reaches |ψ| ≫ ψ₀! The quartic regime is NOT achieved with natural initial conditions.
   - Quartic regime requires either:
     - Non-zero initial velocity (ψ̇(t_c) ≠ 0) — requires energy injection at threshold
     - Time-dependent m_eff²(Φ(t)) that continues to evolve past Φ_c
     - Energy transfer from Φ field during transition (coupling term)
     - H ≪ μ (very small V0) to allow underdamped oscillations

3. **Rapid oscillation condition**: ω ≫ H
   - Quartic regime: ω ~ √(λ_ψ)ψ
   - At ψ ~ ψ₀: ω ~ √(λ_ψ)ψ₀ = μ
   - Benchmark: μ ~ 10¹³ GeV, H_* ~ 10¹³ GeV → ω/H ~ 1 (NOT ≫ 1)
   - Need ψ ≫ ψ₀ for ω ≫ H

### 1.4 Critical Numerical Results (Baseline Parameters: V0=1e64, λ_ψ=0.1, μ=1e13 GeV)

| Scenario | V0 | H at Φ_c | H/μ | Damping 3H/(2ω) | Max |ψ|/ψ₀ | Zero Crossings | ⟨w⟩ | Q | Virial | Quartic? |
|----------|-----|----------|-----|-----------------|-----------|----------------|-----|-----|--------|----------|
| Baseline (ψ=0, ψ̇=0) | 1e64 | 1.25e13 | 1.25 | 1.33 (overdamped) | 1.0 | 0 | -1.0 | 1.0 | 0.0 | ❌ No |
| ψ=0.5ψ₀, ψ̇=0.5μψ₀ | 1e64 | 1.25e13 | 1.25 | 1.33 | 1.85 | 0 | -0.37 | 1.0 | 0.02 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1e64 | 1.25e13 | 1.25 | 1.33 | 1.85 | 0 | -0.37 | 1.0 | 0.02 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1.58e63 | 4.97e12 | 0.50 | 0.53 | 2.24 | 1 | -0.84 | 0.99 | 0.001 | ❌ No |
| ψ=ψ₀, ψ̇=5μψ₀ | 1e58 | 1.25e10 | 0.00125 | 0.0013 | 2.67 | 127 | **0.46** | **3.37** | **0.92** | ✅ **Yes** |
| Fixed φ=1.1Φ_c, no H | — | 0 | 0 | 0 | 2.64 | 145 | **0.42** | **5.10** | **0.77** | ✅ **Yes** |

**Key Conclusions from Numerical Experiments**:
1. **Original V0=1e64 is 6.3× too large** for oscillations (critical V0 ≈ 1.58e63 for 3H/(2ω)=1)
2. **Even at critical V0**, field crosses zero only ONCE then settles at ψ₀ — no sustained quartic regime
3. **Quartic regime ONLY achieved when H ≪ μ** (V0 ≤ 1e58) AND large initial kinetic energy
4. **Without Hubble damping**, quartic regime is natural (w→1/3, Q→5, Virial→1)
5. **The coupling term (αm²/E_th²)Φψ² is essential** — it provides energy transfer from Φ to ψ during Φ's roll past Φ_c

---

## 2. Numerical Implementation Plan

### 2.1 Equations to Solve

**Coupled background system** (Eqs. 3.18-3.21):
```
Φ̈ + 3HΦ̇ + ∂V_eff/∂Φ - (αm²/E_th²)Φψ² = 0
ψ̈ + 3Hψ̇ + m²(1 - αΦ²/E_th²)ψ + λ_ψψ³ = 0
H² = (1/3M_Pl²)(ρ_Φ + ρ_ψ + ρ_χ + ρ_res + ρ_rad)
```

**Energy densities**:
```
ρ_Φ = ½Φ̇² + V_eff(Φ) + ½m²(1 - αΦ²/E_th²)ψ²
ρ_ψ = ½ψ̇² + ½m²(1 - αΦ²/E_th²)ψ² + ¼λ_ψψ⁴
```

### 2.2 Initial Conditions at t = t_c (Threshold Crossing)

| Parameter | Baseline Value | Variation Range |
|-----------|----------------|-----------------|
| Φ(t_c) | Φ_c = E_th/√α | Fixed by threshold |
| Φ̇(t_c) | -√(2ε_V)HM_Pl | ±50% (slow-roll) |
| ψ(t_c) | 0 | [0, 0.1ψ₀] (quantum fluctuations) |
| ψ̇(t_c) | 0 | [0, 0.1μψ₀] |
| H(t_c) | H_* ~ 10¹³ GeV | From Friedmann eq |

**Quantum fluctuation initial conditions** (for ensemble runs):
```
ψ_k(t_c) = H_*/√(2k³)  (for k < aμ)
ψ̇_k(t_c) = √(μ² - k²/a²) ψ_k  (growing mode)
```
Homogeneous mode: ψ₀(t_c) = 0, ψ̇₀(t_c) = 0 (or sample from distribution)

### 2.3 Parameter Space to Explore

| Parameter | Baseline | Range | Notes |
|-----------|----------|-------|-------|
| λ_ψ | 0.1 | [0.01, 1] | Quartic coupling |
| μ = |m_eff| | 10¹³ GeV | [10¹², 10¹⁴] GeV | Tachyonic mass |
| α | 10⁻⁷ | [10⁻⁹, 10⁻⁵] | Threshold coupling |
| E_th | 10¹⁶ GeV | [10¹⁵, 10¹⁷] GeV | Threshold scale |
| Φ̇(t_c)/HM_Pl | -0.1 | [-1, -0.01] | Inflation exit velocity |
| g_ψ (reheating) | 10⁻³ | [10⁻⁵, 10⁻²] | For energy transfer |

### 2.4 Numerical Method

- **Integrator**: Adaptive 4th/5th order Runge-Kutta (Dormand-Prince)
- **Time variable**: Conformal time η or e-folds N = ln a
- **Stopping criteria**: 
  - t > 100/H_* (many oscillations)
  - ψ reaches steady oscillatory state
  - Energy transfer to radiation completes
- **Outputs**: ψ(t), ψ̇(t), H(t), ρ_ψ(t), p_ψ(t), w_ψ(t), Φ(t)

### 2.5 Diagnostics to Compute

1. **Time-averaged equation of state**: ⟨w_ψ⟩(a) over oscillation periods
2. **Oscillation amplitude**: A(t) = max|ψ| over period
3. **Quartic dominance parameter**: Q(t) = λ_ψ⟨ψ⁴⟩ / μ²⟨ψ²⟩
4. **Frequency**: ω(t) from zero-crossings or FFT
5. **Energy transfer rate**: Q_ψ = -ρ̇_ψ - 3H(ρ_ψ + p_ψ)
6. **Virial ratio**: V(t) = ⟨ψ̇²⟩ / (4⟨U⟩)

---

## 3. Validation Criteria (Success/Failure Definition)

### 3.1 Quartic Regime Achieved IF:
- [ ] Q(t) > 10 for sustained period (quartic dominance)
- [ ] ⟨w_ψ⟩ → 1/3 within 5% for > 10 oscillations
- [ ] ω/H > 10 (rapid oscillation condition)
- [ ] Virial ratio V → 1 within 10%

### 3.2 Quartic Regime NOT Achieved IF:
- [ ] Field oscillates near ±ψ₀ with ⟨w_ψ⟩ ≈ 0 (matter-like)
- [ ] Q(t) < 1 throughout evolution
- [ ] ω/H ~ 1 (no separation of scales)
- [ ] Energy drains to other sectors before quartic regime

### 3.3 Current Status (Baseline Parameters):
- **Quartic regime NOT achieved** with natural initial conditions (ψ=0, ψ̇=0 at Φ_c)
- **Quartic regime ONLY achieved** when H ≪ μ (V0 ≤ 1e58) AND large initial kinetic energy
- **Required condition**: 3H/(2ω) < 1 (underdamped) AND energy injection from Φ roll
- **Implication**: The tachyonic-to-quartic transition as currently formulated in the paper is NOT verified and requires either:
  - Fine-tuned initial kinetic energy at threshold crossing
  - Significant energy transfer from Φ during its roll past Φ_c
  - Much smaller V0 (lower inflation scale) than currently assumed

### 3.4 Required Outputs for Each Run:
- Phase space trajectory (ψ, ψ̇)
- w_ψ(t) and ⟨w_ψ⟩(a)
- Q(t) and ω(t)/H(t)
- Energy partition at end of simulation
- Parameter region map (success/failure in λ_ψ-μ-α space)

---

## 4. Deliverables

### 4.1 Mathematical Derivation Document
- Complete derivation from Lagrangian to homogeneous EOM
- Regime classification with analytic boundaries
- Energy analysis showing why ψ(t_c)=0, ψ̇(t_c)=0 fails to reach quartic regime
- Conditions for successful transition (non-zero velocity, continuing m_eff² evolution, energy transfer)

### 4.2 Numerical Code
- Python/Julia implementation of coupled background equations
- Parameter scan script
- Visualization suite (phase space, w_ψ(t), parameter maps)

### 4.3 Results Report
- Parameter region where quartic regime is achieved
- Parameter region where it fails (with explanation)
- Comparison with lattice simulation claims (App B)
- Implications for PTUM proxy-fluid closure validity

### 4.4 Honest Assessment
- **CRITICAL FINDING**: The tachyonic-to-quartic transition as currently formulated in the paper is NOT achieved with natural initial conditions and baseline parameters.
- With ψ(t_c)=0, ψ̇(t_c)=0 at Φ_c, the field oscillates between 0 and ψ₀ with ⟨w⟩ ≈ -1 (cosmological constant-like), NOT w=1/3.
- The quartic regime (w→1/3, Q≫1, Virial→1) is ONLY achieved when:
  1. H ≪ μ (V0 ≤ 1e58, i.e., inflation scale ≪ 10¹³ GeV) — 6 orders of magnitude below current assumption
  2. Large initial kinetic energy is injected at threshold crossing
  3. Energy transfer from Φ during its roll past Φ_c is significant
- If quartic regime requires fine-tuned initial conditions → report as conditional
- If quartic regime never reached for natural parameters → report failure explicitly
- If energy transfer from Φ is essential → quantify required transfer rate
- **Implication for paper**: Claims in Sec 3.5.6 about "quartic regime with w=1/3" need explicit caveats or revision. The proxy-fluid closure (Eq. 3.40) assuming w=1/3 is NOT validated for baseline parameters.

---

## 5. Timeline & Milestones

| Week | Milestone |
|------|-----------|
| 1 | Mathematical derivation complete; numerical code skeleton |
| 2 | Baseline simulation working; single trajectory validated |
| 3 | Parameter scan implemented; initial results |
| 4 | Full parameter space map; comparison with lattice claims |
| 5 | Final report with honest assessment |

---

## 6. Dependencies & Prerequisites

- **Code**: No external dependencies beyond NumPy/SciPy (or Julia DifferentialEquations.jl)
- **Validation**: Compare single trajectory with analytic limits (quadratic regime, quartic virial)
- **Cross-check**: Verify energy conservation in uncoupled limit (ρ̇_ψ = -3Hψ̇²)

---

## 7. Connection to Other Tasks

- **Task 2 (DM production)**: Parametric resonance depends on Φ_res oscillation amplitude, which depends on discharge dynamics
- **Task 3 (Energy-momentum)**: Q_ψ^ν terms need background evolution for validation
- **Task 4 (Reheating)**: ψ oscillation regime determines decay rate Γ_ψ
- **Task 5 (Observational)**: w_ψ(a) affects CMB through ΔN_fluid evolution

---

**Prepared for**: PTUM Scientific Development & Independent Verification
**Status**: Research plan ready for implementation
**Next step**: Begin mathematical derivation and code implementation