---
title: The three area cards that share core share its allowance and pin files, so "no register another card edits" holds per line there and not per file
found: while building #853, U296, 2026-11-21.
issue: no
---

**The mechanism.** U296 holds the registers one file per package, which keeps
two cards on two packages from ever editing the same file. U299, U300 and
U301 (#856, #857, #858) each own a third of `core` and may build together, so
they share `tests/ratchets/duplication/core.txt` and
`tests/ratchets/reserved_causes/core.py`. Core crosses no seam today, so it
has no import allowance to share.
Entries are one per line and sorted, the pins keyed by module, and the layer
ladder is one line per placed module, so their edits fall on different lines
and git merges them. Two deletions on adjacent lines of one allowance file
still conflict.

**Measured cost.** Not driven. `core` holds 64 window places today, so two
cards deleting neighbouring digests is possible and its cost is one conflict
resolved by deleting both lines when the second card merges `main`.
Maintainer facing.

**Closes when:** the three core cards have landed. Ledger only.
