---
title: Five of U129's mutation rows were left unmeasured when the fifth round moved their code
found: at the measured table handoff of #297, U129, 2026-10-10.
issue: no
---

**The mechanism.** A1, A2, A14, A15 and A16 (the gate before the queue, the gate ask itself, the two backfill failure namings, and the soft skip) were refused as stale against 74fb854 when the measured table was joined. The fifth round moved the code those rows named, so the old text no longer matched the tip. The code they guard is covered by the driven tests named in the fifth round; the kill scores for the other applicable rows stand.

**Measured cost.** The five rows have no fresh kill score on this tip. A person cannot treat the table as complete for A1, A2, A14, A15 and A16 until each row is re-copied and re-run.

**Closes when:** each of the five rows has its old text re-copied from the file and `scripts/mutate.py docs/mutation/u129-rows.toml --name u129-author --resume` has been run on macOS so the measured table carries a kill score for every applicable row again.
