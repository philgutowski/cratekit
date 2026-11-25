---
title: The app's runner shows a verb that printed a whole envelope and then died of a signal as a signal death alone
found: at the review round two of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `CrateRunner.runBlocking` returns `.signalled` whenever `terminationReason` is an uncaught signal, before it reads standard output, so a verb that printed a complete envelope and then died of a signal (in interpreter shutdown, say) is shown only as a signal death, its envelope dropped. The fix round chose this so a signal's number is never read as one of crate's exit codes (a SIGBUS, 10, read as a gate).

**Measured cost.** Argued from reading only; no verb was driven to die of a signal after printing its envelope, and no shipped caller runs a verb yet.

**Closes when:** the card that first shows a verb's result in the app carries the envelope, when one decodes, beside the signal in the `.signalled` case, with a test over a fake that prints an envelope and then kills itself. Ledger only.
