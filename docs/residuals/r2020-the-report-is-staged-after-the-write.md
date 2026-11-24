---
title: the rebuild and resort workers build and stage their item report after the write landed, so a failure there fails an item whose write is done
found: at the review of #1036, R-2020, 2026-11-24.
issue: no
---

**The mechanism.** `cli/rebuild.handle` and `routing_cli.handle_resort` call
`rebuild.after_report`, which loads the taxonomy again, and stage the report
under the queue store, after `rebuild_governed_tree` committed the membership
and cleared the flag. A raise there (an unreadable taxonomy, a queue store
that cannot be written) fails the item over a write that landed, and a resume
drives the tree again, which adds nothing the second time. The resort had this
shape on the base; the rebuild has it from R-2020.

**Measured cost.** Not driven: the producer, a queue store that refuses a write
between the commit and the staging, was not built.

**Closes when:** the report's inputs are read before the write, or a failure
staging it is said rather than failing the item. Ledger only.
