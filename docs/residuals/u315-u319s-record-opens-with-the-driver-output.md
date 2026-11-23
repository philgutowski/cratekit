---
title: U319's record opens with twenty two lines of a mutation table's head, an invalid batch's, where its own opening paragraph should be
found: at the build of #872, U315, 2026-11-23.
issue: no
---

**The mechanism.** `docs/restart/u319.md`, lines 1 to 22, is the head of a mutation table the driver printed for an invalid batch ("# Mutation table: u319" down to "THIS BATCH IS INVALID"), and the record's own opening paragraph, which names the unit and what landed, is not in the file; it was committed that way in `094a0a4d`. The record proper starts at line 24 with "Measured".

**Measured cost.** Maintainer facing: a reader of U319's record meets a driver printout first and no statement of what the unit landed.

**Closes when:** the driver's printout moves under the record's own head, or into `docs/mutation/`, in a docs sweep card. Ledger only.
