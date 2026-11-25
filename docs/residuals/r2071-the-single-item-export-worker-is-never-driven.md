---
title: The single item export worker is never called by the job driver since U270
found: at the build of #1073, R-2071, 2026-11-25.
issue: no
---

**The mechanism.** `export.cli.handle` is the worker registered for `export.playlist`, and it carries `handle.batched = (handle_batch, BATCH)`. The job driver reads that attribute (`cli/handlers.py`, `BATCH_ATTRIBUTE`) and, once it names a valid batch form, hands every queued track to `handle_batch`, so `handle`'s own body, which exports one item through `run_export_item`, is reached by no drive. u51-item-derivation H1 mutated that body (the item's track taken from the payload instead of the item) and no test killed it; R-2071's card kills it with a test that calls `handle` directly on a queued job's item.

**Measured cost.** None to a user: the batch form is what runs. A maintainer reading `handle` sees a per item worker that production never calls, guarded by a test that drives it alone. Not driven past that: whether `handle` should be removed, leaving the batch form registered on its own, depends on whether the driver must keep a per item callable for a batch that fails whole, which was not measured.

**Closes when:** `handle` is shown needed by a path the driver takes and a test drives it through that path, or the registration names the batch form alone and `handle`'s body is removed with the test that drives it. Ledger only: maintainer facing.
