---
title: A native landing that fails after its commit landed says no row was added, though the rows were committed
found: at the round one review of #864, U307, 2026-11-22.
issue: no
---

**The mechanism.** In `native.apply_rows`, a failure raised after `rb_writer.commit_guarded` has committed (the witness reads the commit as landed) is recorded in the session record with the rows the commit wrote, and then raised. The landing's refusal for it reads "the collection could not be written (after the commit); no row was added and N file(s) were already moved". The reviewer drove it on base `c919209` and on the branch by making `commit_guarded` commit and then raise: both printed that sentence while the database held the two landed rows and the session record named them. Behaviour is unchanged by U307; the sentence is the base's.

**Measured cost.** A person reading the refusal is told nothing landed when the rows did, the shape of METHOD's first defect pattern. Reachability is unmeasured beyond the reviewer's fault injection: no producer of a real failure between the commit and the end of the apply was driven.

**Closes when:** the refusal past a landed commit names what the session record holds (the rows committed, the files moved) and a test drives a failure after the commit and reads the sentence. Ledger only, since the reachability is unmeasured.
