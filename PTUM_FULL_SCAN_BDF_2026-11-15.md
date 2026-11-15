# PTUM isolated BDF full-scan execution

This branch is an isolated execution copy of PR #2 head
e2968d30406a368b9f2365ac382121d3e95970c4.

Purpose: rerun the declared 100-trajectory homogeneous post-threshold
sensitivity grid with SciPy BDF as an independent stiff-solver
cross-check against the archived Radau run 43703987436.

Unchanged physical and numerical inputs:
- Exact epsilon_H=1 threshold matching.
- 50 initial conditions per energy scale; 100 total.
- 4001 output samples over 20 mu^-1 per trajectory.
- rtol=1e-9 and atol=1e-12.
- 1,000,000 RHS evaluations per trajectory as a fail-closed
  engineering guard.
- Solver method: BDF.

The previous Radau run completed 98/100 trajectories and had two
budget-exhausted integrations at the same dimensionless seed/offset
grid point. This BDF run is intended to test solver dependence; it
does not relax tolerances or change the model. Its output must be
strictly validated and compared row-by-row with Radau. Any failed
integration remains a failure. This is a homogeneous post-threshold
scan, not a quantum-seeded inhomogeneous waterfall or relic calculation.

No changes from this branch are merged or copied to main.
