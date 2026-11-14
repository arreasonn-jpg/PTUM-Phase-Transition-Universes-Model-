# PTUM Full Waterfall Scan Execution Record

- Scientific source branch: `ptum/scientific-consistency-fixes-2026-11-13`
- Source head: `d4f5f8b37a526c6fba35d19cb9c0396710da2e1a`
- Execution branch: `ptum/full-scan-2026-11-14-r2`
- Profile: `full`
- Expected trajectories: 100 (50 high-scale threshold-matched + 50 low-scale underdamped control)
- Grid per scale: 5 seed amplitudes x 5 velocity amplitudes x 2 post-threshold offsets
- Output points per trajectory: 4001
- Duration per trajectory: 20 mu^-1
- Threshold: exact epsilon_H=1 endpoint, Phi_c/M_Pl ~= 0.9862280831
- Fuel velocity: integrated single-field FRW trajectory at each post-threshold offset
- Quantum seeding: no; this is a homogeneous classical sensitivity scan
- Backreaction / rescattering: not included
- Artifact acceptance: require exactly 100 unique expected rows, all integrations successful, strict JSON (no NaN/Infinity tokens), and inspect checkpoint plus final summary before any regime claim.

This branch exists only to run the expensive scan in isolation. It does not alter the draft PR branch or main. A completed scan will not by itself satisfy the inhomogeneous waterfall or relic-abundance acceptance gates.
