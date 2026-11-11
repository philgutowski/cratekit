---
title: A label go matches its own downloaded tracks to the staging folder by byte exact path
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** `label.go.beside` compares each job's recorded artifact
path with the folder's listing as resolved paths, byte for byte. A volume
that hands a name back decomposed (NFD) where the artifact was recorded
composed (NFC) makes the go's own accented track read as a file no download
names, so the go refuses its own tail. `core.locations.norm_for_compare` is
the repository's rule for such comparisons and is not used here.

**Measured cost.** Driven at the review's round two (`test_cr.py::test_cr5`)
with the artifact recorded NFC and the file NFD: the track was read as not
the go's. A refusal with the tail by hand named; nothing lands wrongly. A
volume that decomposes names cannot be made on the Linux container, so the
producer is unmeasured.

**Closes when:** the comparison normalizes as `norm_for_compare` does, with a
test over a decomposed name. Ledger only.
