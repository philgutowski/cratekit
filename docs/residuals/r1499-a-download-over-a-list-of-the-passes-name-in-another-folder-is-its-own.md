---
title: A download over a list of the pass's name in another folder is read as the pass's own
found: at the review of #665, R-1499, round one, 2026-11-11.
issue: no
---

**The mechanism.** `_own_downloads` in `cli/sync_land.py` takes every download of the library whose list is named `<pass>.list.json`, the reading `cli.tail` names a pass's download by, wherever the list sits.

**Measured cost.** Driven at round one (d8) with a list copied by hand under the pass's exact name: the foreign download's track ran on with the pass. The producer is contrived; nothing writes such a list.

**Closes when:** a pass's own downloads are matched by the list's whole path under the staging folder's lists directory. Ledger only.
