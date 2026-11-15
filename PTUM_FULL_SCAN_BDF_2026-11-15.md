# PTUM isolated BDF full-scan execution

Execution source: PR #2 head bfa9d6a4917885690ab66dedf2467003a5298428.
This branch differs from the source branch only by this execution manifest.

Purpose: rerun the declared 100-trajectory homogeneous post-threshold
sensitivity grid with SciPy BDF as an independent stiff-solver
cross-check against Radau workflow 43703987436.

Unchanged physical and numerical inputs:
- Exact epsilon_H=1 threshold matching.
- 50 initial conditions per energy scale; 100 total.
- 4001 output samples over 20 mu^-1 per trajectory.
- rtol=1e-9 and atol=1e-12.
- 1,000,000 RHS evaluations per trajectory as a fail-closed
  engineering guard.
- Solver method: BDF.

The previous Radau run completed 98/100 trajectories and had two
budget-exhausted integrations at the same seed/offset grid point.
This BDF run tests solver dependence; it does not relax tolerances or
change the model. Its strict-JSON output must be validated and compared
row-by-row with Radau. Any failed integration remains a failure.
This is a homogeneous post-threshold scan, not a quantum-seeded
inhomogeneous waterfall or relic calculation.

No changes from this branch are merged or copied to main.
