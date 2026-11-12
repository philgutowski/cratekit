---
title: The three call sites that hand the taken ledger to the pair, twins and INSPIRATION readers kill no test when the ledger is left out
found: at the review of #671, U242, round one, 2026-11-12.
issue: no
---

**The mechanism.** `sync/pair_cli.py` (`_discovered_back`), `sync/twins.py`
(`plan_backfill`) and `organize/inspiration.py` (`plan`) each read
`playlists.taken_ids(cfg)` and hand it to a reader the suite tests as a pure
function with a set it passes itself. The review's mutation of each call
site, handing the reader an empty set, killed no test.

**Measured cost.** None measured: on the branch each site was read, and the
pair site driven, and they hand the ledger in correctly. A later change that
dropped one would read a stripped copy, custom playlist or set as before the
strip only by its title, with no test to say so.

**Closes when:** a test drives each verb over a stripped playlist through the
dispatcher. Ledger only.
