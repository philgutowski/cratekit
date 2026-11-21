---
title: A replay resumed from a sidecar that was measured while a tracked file was changed reuses its rows once the file is put back
found: at the review of #854, U297, round two, 2026-11-21.
issue: no
---

**The mechanism.** `scripts/mutate.py` lets a replay pass reuse a row from a
prior sidecar only when the sidecar's `head` is this commit and no tracked
file differs from the commit now (`replay_resume_refusal`). The sidecar does
not record whether a tracked file differed while it was being measured. So a
replay measured with a test edited and uncommitted, then resumed after the
edit was reverted, reuses rows that were measured against the edited suite.
The same holds for a light or a full pass, which resume across commits as
they always did, and for `--allow-dirty`.

**Measured cost.** Not driven. The review drove the other half, a test
deleted and not committed after the measurement, where `killset.py check`
passed a lost kill, and that half is closed. This half takes a replay run on
a tree the procedure says is committed, which it is not. Maintainer facing.

**Closes when:** the replay's sidecar records that the tree was clean when
each row was measured and a resume reads it, or the driver refuses a replay
on a tree with a tracked change. Ledger only.
