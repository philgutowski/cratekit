# U144 mutation table, notes

Twenty five rows over the unit's own guards and one sample of an existing
U121 guard the unit now shares, measured by `scripts/mutate.py` on macOS in
three batches (`u144-a` to `u144-c`). Batch a ran at `53e9737a`, batch b at
`53e9737a`, batch c at `946b19e3`, after the one test change below. Each
batch passed the session tool's ten minute ceiling and was moved by the
harness to a tracked background job, waited on in the foreground with
nothing else touching the tree. Every baseline green at 13,948 collected,
every null control 0 of 13,948, every restore verified against
`git show HEAD`, and `git status` showed no source change after each batch.

**24 killed, 1 zero, and the zero killed once its test was fixed.** The
author ran it, so a zero means only that the author could not kill it.

- **B3_again_now_held, zero, user facing.** The plan taken again on the
  write handle skips a set given its INSPIRATION playlist since the plan.
  Removed, such a set is decided as before and its tracks would be added to
  the playlist a person made since. The test meant to hold it created the
  INSPIRATION folder after the plan, so the folder's id moved the digest
  and refused the write whatever the skip did. The test was changed to make
  the folder before the plan (`946b19e3`), and the same mutation, measured
  again as **C1_again_now_held** in batch c, killed 1.

Rows kept inside the cap: the skip, the two of one name and unprefixed
rules, the sets folder rule by name and by ledger record, the slash
spelling, the MATCHED only bar, the empty set rule, both write guards
(unnamed membership, stale digest), the convergence latch, both read back
checks, the membership write, the commit record, the unread folder row,
the withheld count and its coefficient in the totals, the export module
gate, the bridge refusal, the folder warning, the unanswered question's
reason, and one shared U121 guard (the parent check of a playlist found by
name, 11 kills across both suites).

Dropped below the cap: the read handle closed across provider calls (a
property of when handles open, which no fixture can observe without a
timing seam), the sort order of the plan's rows, and the gate's detail
sentence wording.
