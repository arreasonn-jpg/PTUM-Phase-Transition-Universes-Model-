# PTUM full homogeneous scan execution manifest

- Execution branch: `ptum/full-scan-2026-11-15-r2`
- Source PR-branch commit: `5379ec8a2e85e875c9819121b0409ea454cf99e9`
- Scan command: `python ptum_task1_scan.py --profile full --output task1_parameter_scan_results.json --checkpoint task1_parameter_scan_checkpoint.json`
- Scenarios: two energy scales, 50 trajectories each (100 total)
- Grid per scenario: 5 seed scales x 5 velocity scales x 2 post-threshold offsets
- Output grid: 4001 samples over 20 mu^-1 per trajectory
- Integrator: DOP853, rtol=1e-9, atol=1e-12
- Work guard: at most 100000 RHS evaluations per trajectory

The RHS-evaluation cap is a deterministic engineering guard against a pathological adaptive solve. It is not a physical cutoff and does not relax the ODE tolerances. A trajectory that exceeds the cap is recorded as failed with its exact evaluation count; the scan must not classify it as a physical regime. The strict-JSON checkpoint is atomically updated after each completed or failed trajectory, and the workflow uploads both checkpoint and final summary even when the scan validation fails.

This is a homogeneous post-threshold sensitivity scan. It is not a coupled threshold-crossing calculation, a quantum-vacuum-seeded inhomogeneous waterfall, a nonlinear lattice simulation, or a relic-abundance calculation. No physical gate is promoted by the scan alone.
