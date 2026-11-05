---
title: A mirrored INBOX playlist still in INBOX but no longer read as a batch is named twice on the step, and counted twice in its left count
found: at the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `mirror.plan` names a playlist the ledger records as
mirrored, whose title is still present in INBOX but no longer reads as a
batch, with its "still in INBOX but no longer read as one to mirror" line.
Since U214 the same node is also one of `Folder.unmirrored`, so the step
carries two left lines for it and its `left` count counts it twice: "2 left as
they are; 1 node(s) in INBOX not mirrored".

**Measured cost.** Both lines are true. A person reconciling the left count
against INBOX reads one too many. Driven on the account side through the
organize step's fake account; the library side producer, a batch folder
removed after the batch was mirrored, was not driven end to end.

**Closes when:** the step names such a node once, the recorded line folded
into its unmirrored line, or the count counts nodes rather than lines. Ledger
only: a wording and count fix, nothing false.
