# PTUM full 100-trajectory validation

**Run date:** 2026-11-14  
**Validation branch:** `ptum/independent-trajectory-scan-2026-11-14`

## Purpose

Run the complete two-field waterfall trajectory grid after the half-cycle diagnostics were changed to use interpolated turning points and time-integrated observables. This scan checks coverage, deterministic execution, artifact retention, and aggregate-report integrity across all 100 configured initial-condition combinations.

## Execution protocol

The GitHub Actions workflow `.github/workflows/ptum-scientific-tests.yml` launches one isolated worker for each trajectory index from 0 through 99. Each worker uses:

- Dimensionless integration horizon: `mu*t = 120`
- Output samples: `24,001`
- Solver: DOP853
- Relative tolerance: `1e-9`
- Absolute tolerance: `1e-12`
- Maximum dimensionless solver step: `0.05`

Each completed trajectory is uploaded as an individual artifact. The aggregation job must validate all 100 expected indices before producing the combined scan report.

## Interpretation limits

This is a homogeneous classical background scan. The configured scan does not include a quantum-vacuum seed, nonlinear mode backreaction, rescattering, or lattice fragmentation. A successful scan therefore validates the declared numerical workflow and its sampled classical parameter grid; it does not establish quantum particle production or a complete reheating calculation.

The aggregate report, not the workflow's green status alone, is the evidence for trajectory coverage and classification counts.
