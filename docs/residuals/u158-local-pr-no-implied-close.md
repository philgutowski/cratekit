---
title: A local unit's pull request is judged on its range only, so its close is caught on the push to main
found: at the review of #339, U158, 2026-10-28.
issue: no
---

**The mechanism.** CI reads the card a merge will close off the head branch
only when it is `cloud/N-slug` (`pull_request_card` in `scripts/board.py`).
A local unit's branch is `unit/uN-slug`, as `board.py start` names it, and
its number is a unit number rather than an issue number, so a pull request
from it is judged on the trailers in its range, which carry none. Its close,
written by the merge, is judged by the push to `main`, after the cascade.

**Measured cost.** Driven by the review: `pull_request_card("unit/u36-converge")`
is None, and `cmd_closing` with that head and U36 owed exits 0. No local
session has opened a pull request yet, and `owed_by_unit()` is empty today,
so nothing has paid it.

**Closes when:** local units open pull requests, and the head reader learns
`unit/uN-` with the unit to issue map `board.py` already keeps; or METHOD says
local units keep the local merge. Ledger only.
