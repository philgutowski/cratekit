---
title: Two tests failed once each in a loaded full suite and never again
found: at the mutation table of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** `scripts/mutate.py` refused two baselines in a row on
2026-10-10, each over one failing test:
`tests/test_sync_mark.py::test_an_intake_file_of_no_pass_is_a_gated_plan_of_nothing`
and then `tests/test_sync_pair.py::test_a_short_listing_removes_nothing_from_the_account`.
Neither failed alone, in its file five times running, or in a full suite run
straight after (13,660 passed), and the driver kept no traceback.

**Measured cost.** Two refused batches. The cause was not found, so whether
either test carries a timing dependence is unmeasured.

**Closes when:** the driver keeps a refused baseline's failure text, and the
next refusal over either test is read from it. Ledger only.
