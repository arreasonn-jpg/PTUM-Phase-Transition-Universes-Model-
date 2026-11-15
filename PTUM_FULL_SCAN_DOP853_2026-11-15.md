# PTUM isolated DOP853 full-scan execution

Execution source: PR #2 head 4227a3e50e2a0564a44a19dea2338dafa328ca53.
This branch differs from the source branch only by this execution manifest.

Purpose: run the declared 100-trajectory homogeneous post-threshold
sensitivity grid with SciPy DOP853 as a third solver comparison against
the archived Radau (workflow 43703987436) and BDF (workflow 43705977596)
runs.

Unchanged physical and numerical inputs:
- Exact epsilon_H=1 threshold matching.
- 50 initial conditions per energy scale; 100 total.
- 4001 output samples over 20 mu^-1 per trajectory.
- rtol=1e-9 and atol=1e-12.
- 1,000,000 RHS evaluations per trajectory as a fail-closed
  engineering guard.
- Solver method: DOP853.

The Radau and BDF runs both completed 98/100 trajectories and exhausted
the same RHS guard on the same two initial-condition rows. DOP853 tests
whether an explicit high-order method handles those rows more
efficiently. No tolerance or physical input is changed. Failed
integrations remain failures. This is a homogeneous post-threshold
scan, not a quantum-seeded inhomogeneous waterfall or relic calculation.

No changes from this branch are merged or copied to main.
