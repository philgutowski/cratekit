---
title: The cloud battery reads an interrupted suite run from its partial counts and never reads pytest's exit code
found: at the review of #697, U268, 2026-11-12.
issue: no
---

**The mechanism.** `scripts/cloud_battery.py failing_ids` reads the ids and
the summary line of the run and ignores its exit code, so a run that stopped
early (`pytest.exit` or a `KeyboardInterrupt` inside a test, or a collection
error, which interrupts the whole run) is read as if it were complete: the
tests that never ran cannot fail. The review drove both readers, before and
after U268, and they behave the same, so this predates the card and is out of
its scope.

**Measured cost.** Not driven to a hidden failure. In every shape the review
drove, the test that stopped the run is itself a failing id the base does not
hold, so `compare` exits 1; a collection error is read by its file and does
the same. A stop the base also holds would hide every test after it.

**Closes when:** `compare` refuses a run whose exit code says it was
interrupted, or reports the collected and run counts beside the base's. Ledger
only.
