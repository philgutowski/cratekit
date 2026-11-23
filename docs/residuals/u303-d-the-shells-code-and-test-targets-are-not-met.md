---
title: The command shell misses its code, line and test targets under the refactor epic
found: at the build of #860, U303, 2026-11-22.
issue: no
---

**The mechanism.** #860's brief set targets on the 28 files the survey of
#847 counted: at most 19,914 lines and 13,243 code lines, and the 23 test
files at most 18,547 lines with their summed test time 30 percent lower.
Three files landed in the area since (`schedule.py`, `sync_night.py`,
`verbs/tag_campaign.py`), so the area U303 started from was 31 files,
28,051 lines and 17,787 code lines. U303 split doctor, emptied the shell's
import and copy allowances and shortened its prose; it did not rewrite code
for size, since behaviour is frozen and every line changed is a kill set row
to carry.

**Measured cost.** Measured by `scripts/refactor_measure.py lines` on the
merged head, given in `docs/restart/u303.md`: the lines target missed, the
code lines target missed by a wide margin (the 15 percent code cut #847's
prose answer asks of every card is not met), the test lines target missed,
and the test time not cut, since no test was removed or rewritten. No cost
to a person.

**Closes when:** #872, the final audit, reads the shortfall against the
193,000 line bar and files a further card for the shell's code and tests if
the total needs it. Ledger only.
