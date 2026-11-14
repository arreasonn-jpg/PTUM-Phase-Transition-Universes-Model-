# PTUM transient quartic episode diagnostic

The scan now distinguishes two separate questions:

1. Does a trajectory end in a sustained late-time quartic-like regime?
2. Does it pass through a transient quartic-like episode before leaving that regime?

The late-time classifier remains unchanged. It is not relaxed to increase the number of positive classifications.

A transient half-cycle is marked as a candidate only when all four conditions hold in the same complete half-cycle:

- (Q = \lambda_\psi\langle\psi^4\rangle / (\langle|m_{\rm eff}^2|\psi^2\rangle) > 2)
- (|w-1/3| < 0.05)
- (|R_{\rm vir}-1| < 0.2)
- (H/\omega < 0.1)

A transient episode requires at least three consecutive candidate half-cycles. The summary records the number of candidate half-cycles, the longest consecutive run, the number of qualifying episodes, and the longest episode duration in units of (mu^{-1}).

This diagnostic does not call a transient episode a late-time attractor, does not claim quantum vacuum seeding, and does not substitute for an inhomogeneous lattice calculation.
