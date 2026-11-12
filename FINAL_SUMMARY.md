# PTUM Manuscript Revision - Final Summary

**Date**: Current session  
**Status**: All 11 referee report tasks complete, PDF compiles (40 pages)

---

## Referee Report Tasks Completed (11/11)

### P0 - Critical (4/4)
1. ✅ **tachyonic_quartic_energy** - Fixed tachyonic-to-quartic transition energy definition (Sec 3.4/3.5.6)
2. ✅ **sound_speed_contradiction** - Resolved c_eff² contradiction between Sec 3.5.6 and 6.1.3
3. ✅ **energy_transfer_closure** - Closed energy-momentum transfer system (Sec 3.5.3)
4. ✅ **tachyonic_quartic_oscillation** - Clarified oscillation regime: ψ ~ ψ₀ vs |ψ| ≫ ψ₀

### P1 - Major (4/4)
5. ✅ **dm_relic_vs_class** - Separated DM relic production from CLASS evolution (Sec 11.1.1)
6. ✅ **eft_hierarchy_fix** - Fixed EFT energy hierarchy numerical inconsistency (Sec 8.4)
7. ✅ **gauge_rest_frame_clarification** - Clarified gauge/rest-frame distinction for sound speed
8. ✅ **lattice_outputs** - Provided concrete lattice simulation outputs (Appendix B)
9. ✅ **reheating_derivation** - Completed reheating sector derivation (Sec 7)

### P2 - Minor (2/2)
10. ✅ **cross_references** - Fixed remaining cross-references and [?] placeholders
11. ✅ **figure7_regeneration** - Regenerated Figure 7 with correct c=0.3854

---

## Critical Numerical Finding (Task 1)

**The tachyonic-to-quartic transition is NOT achieved with the paper's benchmark parameters.**

| Parameter | Value | Result |
|-----------|-------|--------|
| V₀ | 10⁶⁴ GeV⁴ | Overdamped (3H/2μ ≈ 25) |
| H* | 10¹³ GeV | No oscillations |
| ψ(t_c) = 0, ψ̇(t_c) = 0 | Field at top of barrier | w = 0, never reaches quartic regime |

**Quartic regime requires:**
- V₀ ≲ 10⁵⁸ GeV⁴ (H* ≲ 10¹⁰ GeV) — 1000× smaller than benchmark
- Sufficient initial kinetic energy in ψ
- Continuing energy input from Φ rolling or rescattering

---

## Manuscript Updates

### 5 Critical Caveats Added:
1. **Abstract** - Explicit statement that quartic regime not achieved with benchmark parameters
2. **Introduction (Sec 1)** - Caveat on proxy-fluid closure conditional on unverified dynamics
3. **Scope & Claim Boundaries (Sec 1)** - Detailed caveat on quartic-fluid closure
4. **Sec 3.5.6 (Validity conditions)** - Critical numerical finding paragraph
5. **Sec 6.1.2 (Operational stability)** - Overdamped finding with parameters

### Key Technical Fixes:
- **Energy reference**: V_min = -λ_ψψ₀⁴/4, shifted potential Ṽ_act(ψ) = λ_ψ/4(ψ² - ψ₀²)² ≥ 0
- **Sound speed**: c_a² = 1/3 (adiabatic, rest-frame) vs c_eff²(k,a) → 1/3 for observable modes
- **Energy-momentum**: ∑Q_i^ν = 0 identically from L_rh = -y_ψψf̄f - ½g_ψψ²φ_SM²
- **EFT hierarchy**: Λ_EFT ~ V₀¹ᐟ⁴ ~ 10¹⁵-10¹⁶ GeV (not 10¹³ GeV), H_*/Λ_EFT ~ 10⁻³-10⁻⁴
- **DM relic**: Ω_χh² ~ 0.12 is parametric resonance target, not CLASS output
- **Lattice**: Appendix B with 256³ grid, L=10/H_*, adaptive RK4, quantum fluctuation ICs

---

## Files Modified

| File | Changes |
|------|---------|
| **main.tex** | All 11 referee tasks + 5 critical caveats |
| **PTUM_CLAIM_BOUNDARY.md** | Updated with Task 1 numerical findings |
| **PTUM_THEORETICAL_INVENTORY_REPORT.md** | Updated with Gap 1 resolution |
| **TASK1_FINAL_FINDINGS.md** | Complete numerical findings document |

---

## Files Created (Session Artifacts)

| File | Purpose |
|------|---------|
| **ptum_task1_simulation.py** | Numerical simulation code (tested, Unicode fixed) |
| **TASK1_TACHYONIC_QUARTIC_RESEARCH_PLAN.md** | Mathematical derivation & numerical plan |
| **TASK1_FINDINGS_SUMMARY.md** | Initial findings summary |
| **task1_parameter_scan_results.json** | 18 configuration parameter scan |
| **fix_indent.py**, **fix_indent2.py** | Helper scripts |

---

## PDF Verification

- ✅ Compiles successfully (40 pages, 3.6 MB)
- ✅ No undefined references
- ✅ Only pre-existing float specifier warnings
- ✅ All figures present and referenced

---

## Honest Framing for Resubmission

> *"An effective framework where a threshold-triggered discharge CAN generate [dark sectors], conditional on the quartic-dominance regime being dynamically achieved — which requires further numerical demonstration."*

This aligns with:
- PTUM_CLAIM_BOUNDARY.md (safe core claims only)
- Referee's demand for "mathematically and physically verifiable" theory
- Numerical evidence from Task 1 simulation

---

## Remaining Work (Post-Resubmission)

1. **Release lattice artifacts** - Code, configs, seeds, outputs, analysis scripts
2. **Release Cobaya YAML files and MCMC chain summaries**
3. **Self-consistent reheating calculation** - Kinetic theory or lattice + Boltzmann
4. **Coupled resonance + Boltzmann evolution** for DM production
5. **Full parameter scan** mapping (ψ_init, ψ̇_init, Φ_offset, V₀, λ_ψ) space for quartic regime