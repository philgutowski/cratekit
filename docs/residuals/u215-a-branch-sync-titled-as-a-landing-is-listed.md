---
title: A branch sync titled in the landing form off the first parent line is listed as a release landing
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** `landings_since` in `scripts/release.py` lists a merge no
pull request claimed when it is off the first parent line and its subject
matches `LANDING_RE`, `merge(uN): ...` or `merge(r-N): ...`. A session that
titled a merge of `main` into its own branch in that form, as three did before
v0.2.0 (`merge(u52): main into relay/70 ...`, `merge(u132): main at e686759
into the branch ...`, `merge(u142): U140 from main at cdd42fd ...`), has it
counted as a unit landing.

**Measured cost.** Driven by Fable over the real history: `plan --since
<root> --tip v0.2.0` lists the three as minor landings. Zero such merges in any
range since v0.2.0, so no range a release would cut again carries one, and the
cloud unit pipeline titles its syncs with git's default or `merge: main into
the branch`, which do not match. Notes and the bump are wrong only for a range
nobody will cut.

**Closes when:** the off line rule stops trusting the subject alone, for
instance by following each local merge of `main`'s second parent first parent
line instead. Ledger only.
