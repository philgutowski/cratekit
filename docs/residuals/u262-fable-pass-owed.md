---
title: U262 was reviewed by Opus 5.5 because Fable was out of usage, and a Fable pass on its merged range is owed
found: at the review of #691, U262, 2026-11-12.
issue: no
---

**The mechanism.** The `fable-reviewer` agent was refused on Fable's usage
limit at round one, so the same reviewer definition ran on Opus 5.5 at high
effort under the same merge bar, as the cloud lane allows since 2026-11-08.

**Measured cost.** None measured. The review that ran was a different model
from the one the pipeline names.

**Closes when:** a Fable review at high effort reads U262's merged range,
`acquire/match.py` `_is_a_credit` and `_CREDIT_MARKERS` and the U262 tests in
`tests/test_match_states.py`, and its findings are driven. Ledger only.
