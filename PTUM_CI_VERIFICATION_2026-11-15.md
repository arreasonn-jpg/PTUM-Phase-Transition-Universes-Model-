# PTUM latest-head CI verification manifest

This isolated branch is based on PR #2 source commit
`32040330014eef0d0c7ac595b4fee5bf10331dbc`.

Purpose:
- Re-run the 103-test Python regression suite after the manuscript
  status and claim-boundary assertions were updated for the completed
  DOP853 scan.
- Re-run the four-trajectory two-scale smoke scan.
- Rebuild the current LaTeX manuscript and inspect its final log.

This is a CI-only verification branch. It does not change model code,
solver settings, scan data or physical claims. The 100-row DOP853
execution and artifact audit are recorded separately in the
acceptance matrix, scientific corrections, claim boundary and
reproducibility notes.
