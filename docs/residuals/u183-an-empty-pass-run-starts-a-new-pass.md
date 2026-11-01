---
title: crate sync land --pass-run with an empty value starts a new pass instead of refusing
found: at the first review of #380, U183, 2026-11-01.
issue: no
---

**The mechanism.** `sync_land` in `src/cratekit/cli/sync_land.py` reads the
`--pass-run` value as truthy or not, so an empty string is the same as no flag,
and a script that passes an unset variable starts a fresh `sync all` where it
meant to continue one. The same was true on `main` before U183.

**Measured cost.** Driven: `crate sync land --pass-run ""` queues a new pass.
No file or row is lost; the new pass is the same work a plain `crate sync land`
does, and the earlier pass stays continuable.

**Closes when:** the flag refuses an empty value at the parser. Ledger only.
