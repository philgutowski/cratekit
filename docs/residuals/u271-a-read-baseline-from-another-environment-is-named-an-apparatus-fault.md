---
title: A battery record read across an environment difference ends in an invalid batch blamed on the apparatus, not in a refusal naming the difference
found: at review round one of #700, U271, 2026-11-13.
issue: no
---

**The mechanism.** `scripts/mutate.py`'s `read_battery_verdict` keys the
battery's record on the commit, the tree, the host and boot id, the checkout,
the interpreter, the known failures file, an inherited `PYTEST_ADDOPTS`, and
a run that ran all it collected. It does not key the rest of the environment
the battery's suite ran in: `HOME`, the XDG directories and the Cratekit
state directories, which the driver sandboxes for its own children and the
battery does not, or a `TMPDIR` that moves where the inode bound test writes.
A difference there that changes what the suite collects or fails is caught
by the null control, a full run in the driver's own environment held to the
read collected count, so the batch is declared invalid with "the apparatus
is what is broken", where a measured baseline would have refused naming the
failing test.

**Measured cost.** No wrong table: every candidate round one drove ended in
an invalid batch. The cost is a misattributed refusal and a session sent
looking at the apparatus. On the real tree a collect only count was 20,403
in both environments, and round two's real suite run read the record and ran
a zero null control at 20,414, so the producer was not reached here.

**Closes when:** the invalid batch's message, when the full baseline was read,
says so and names `--measure-baseline` as the first thing to try, or the
battery records and the driver compares the environment it sandboxes. Ledger
only.
