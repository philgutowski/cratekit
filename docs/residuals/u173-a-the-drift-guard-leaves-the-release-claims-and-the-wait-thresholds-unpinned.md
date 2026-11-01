---
title: The rekordbox visit skill's drift guard leaves its release claims and its wait thresholds unpinned
found: at the second Fable review of #354, U173, 2026-11-01.
issue: no
---

**The mechanism.** `tests/test_rekordbox_visit_skill.py` reads every value the skill spells from the module that owns it, except four: the claim that `crate analyze check` landed after v0.4.0, the claim that rows landed by v0.4.0 or later need no Reload Tags, and the wait loop's twenty second quiet and five minute stall. A mutation of each survived the review's table. The rehearsal's own backup acknowledgment in the redirected state is also left to the solutions entry the skill cites, rather than said in the skill.

**Measured cost.** None today: each claim was verified true by hand at the review (`git show v0.4.0` has `inbox.analyzed` and no `analyze.check`; U163 is in v0.4.0). The release claims go stale the day a release carries U167, when the precondition reads as a copy problem that no longer exists.

**Closes when:** the release that carries `crate analyze check` rewords the precondition to name that version, or the claims are read from the tags by the test. Ledger only, a maintainer facing gap.
