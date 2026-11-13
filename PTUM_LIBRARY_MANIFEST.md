# PTUM Library Final v1.2, Code-Availability Corrected Package

This package supersedes `PTUM_LIBRARY_FINAL_v1.1_CLEAN` and the earlier v1.2 draft.

## Contents

```text
main.tex
main.pdf
figures/
svjour.cls
svepj.clo
cover_letter.txt
highlights.txt
PTUM_LIBRARY_SUPPLEMENTARY_NOTE.tex
PTUM_LIBRARY_SUPPLEMENTARY_NOTE.pdf
PTUM_CLAIM_BOUNDARY.md
PTUM_REPRODUCIBILITY_NOTES.md
PTUM_FINAL_AUDIT.md
PTUM_FINAL_AUDIT.json
compile logs
```

## Legacy repository reference and current verification status

Historical package metadata points to:

```text
https://github.com/ErdemEsa/ptum-cosmology.git
```

The repository API returned HTTP 404 during the 2026-11-13 review. This
does not establish whether the repository is private, renamed, or
otherwise inaccessible, but its contents could not be verified.

The current canonical PTUM repository contains `PTUM.zip`, but the
CLASS patch is not exposed as an individually reviewable file in the
tracked root inventory, and the archive was not inspected. Therefore
the earlier statement that the CLASS v3.2.0 patch is publicly available
and apply-check verified is **UNVERIFIED** in the current audit.

## Reproducibility boundary

Until the patch source, target CLASS version, checksum, apply command,
and clean-tree apply log are available in an accessible location, the
CLASS code-availability claim must remain unverified. Production
`Cobaya` YAML files and full MCMC chains also remain pending or
external-archive items.
