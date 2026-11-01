---
title: The Bandcamp and fallback fetch workers still fail their job over a policy refusal, where acquire download now skips it
found: at the build of #350, U169, 2026-11-01.
issue: no
---

**The mechanism.** U169 added `jobs.Declined`, and the `acquire download` worker raises it for a cause in the `REFUSED_BY_POLICY` class that is not retryable, so the item is skipped and a list whose only misses are policy refusals ends ok. Two more workers raise the same causes in jobs of their own and were left as they were, because the brief named the download's settle path: `acquire bandcamp-fetch` (`_encoding` in `src/cratekit/acquire/bandcamp_cli.py`, `lossy-refused` and `unavailable-permanent`) and `acquire fallback-fetch` (`src/cratekit/acquire/fallback_cli.py`, `lossy-refused` under the strict policy). A Bandcamp purchase of ten tracks with one offered only lossy still ends `failed (REFUSED_BY_POLICY)`.

**Measured cost.** Not driven against either verb. The same wrong impression sitting 47 paid for on the download, on two verbs with fewer tracks per job; the item causes are correct and `job show` names them.

**Closes when:** each worker wraps its body the way `acquire.cli.handle` does, declining a cause `acquire.cli.refused_for_good` accepts, with the verb naming each skipped track in a warning. Ledger only: a wording of the outcome, not data at risk.
