---
title: The order a release plan lists its landings in is not pinned by any test
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** `range_commits` in `scripts/release.py` passes
`--date-order`, so landings from both sides of a local merge of `main` come out
in the order they were committed rather than one side after the other. Reverting
it to git's default order kills no test in `tests/test_release.py`.

**Measured cost.** None measured: the default order and `--date-order` agree
over v0.6.0 to v0.7.0 and over the root to v0.2.0, so no real release lists
differently. A future range whose clocks disagree could list out of merge order
in its notes, which is cosmetic.

**Closes when:** a test builds two landings on either side of a local merge
with commit dates that differ from their topological order. Ledger only.
