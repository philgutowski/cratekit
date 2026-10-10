---
title: A native landing writes the vox My Tag and not the male vox or female vox one
found: at the review of #296, U127, 2026-10-10.
issue: no
---

**The mechanism.** `native._vox_plan` asks `metadata_cli.vocal_tag_values`
with no gender, so a landed row clearing the cut carries `vox` alone. The
vocals verb reads `voxgender` and writes `male vox` or `female vox` beside
`vox` from the same score. The brief named the `vox` tag only, which is the
one adoption reads, so the landing keeps to it, and nothing on the screen or
in the warnings names the gender tags as owed.

**Measured cost.** A landed vocal track is missing from a My Tag filter on
`male vox` or `female vox` until `crate metadata mytags-vocals --apply` runs.
No playlist Cratekit writes reads the gender tags. How many landed rows carry
a `voxgender` was not measured.

**Closes when:** the author says whether a landing writes the gender tags too,
which is reading `voxgender` in the same open and passing it through, or says
the verb owns them. Ledger only, it is a filter a person reads and no write
or workflow depends on it.
