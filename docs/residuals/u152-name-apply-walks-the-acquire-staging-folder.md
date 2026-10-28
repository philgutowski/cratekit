---
title: crate sync land runs name apply over the staging root, which may walk the acquire verb's own staging folder of refused files
found: at the review of #333, U152, 2026-10-28.
issue: no
---

**The mechanism.** `crate sync land` runs `crate name apply --root <staging>` over the absolute download staging folder after the tail. `name apply` walks its root recursively, and the download leaves each file it refused for good (a lossy only track) under `<staging>/.cratekit-acquire-staging/<job>/<n>/`, which `tag folder` skips and `intake land` does not list, since it reads one level. Whether `name apply` plans renames inside that hidden folder was read and not driven.

**Measured cost.** Not driven. If it does, a refused file kept as evidence is renamed in place; nothing is lost and nothing lands, but the evidence no longer carries the provider id the refusal names.

**Closes when:** a test drives `name apply` over a staging root holding a refused file under the acquire staging folder and shows it untouched, or `name apply` skips that folder the way `tag folder` does. Ledger only.
