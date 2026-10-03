# U113 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's). The unit writes
playlists into an intake file and into the live database, so it gets the full
25 rows, scoped to its own guards, in three batches.

Three batches because a batch's baseline, its subsets and its promoted zeros
pass the harness's 600 second ceiling for one foreground call; each was moved
to a tracked job by the harness and waited on with nothing else touching the
tree. Each ran on a committed tree with a green full baseline, 12,699 collected
for a and 12,700 for b and c after one test was added between them, each valid
null control killed nothing, and every restore was verified against
`git show HEAD:`.

- `u113-a`, the split, the naming rule and the sweep's record, 8 rows, 7
  killed: A2 the queue order 3, A3 no pass splits nothing 1, A4 the batch's own
  name held 1, A5 a landing's names held against each other 1, A6 the sweep
  passing the name 1, A7 the payload recording it 21, A8 pending names read
  only from files awaiting import 1.
- **A1 zero**, promoted to the full suite, 12,699 collected, confirmed, and
  re-measured in `u113-b` after the fix round added
  `test_a_row_that_only_resembles_a_file_does_not_claim_it`, zero again at
  12,700. The row lets a `needs_review` match claim its paths. Four candidates
  were driven through `match.resolve_one` over `match.index_paths`: the plain
  file asked for as the extended mix, the extended file asked for plain, a remix
  asked for plain, and a title that merely resembles. The first three answer
  `needs_review` with NO paths, the fourth `missing`, so the guard is a second
  layer over the matcher's own contract and the mutation has nothing to claim.
  The user facing behaviour, the file staying in the batch playlist, is what
  the new test pins, and that is the composite: it holds with and without the
  guard. Counted as the table's one zero; the row is in both batches and is one
  row of the 25.
- `u113-b`, the bridge, 8 rows, 8 killed besides A1: B1 the batch playlist not
  written when empty 5, B2 the batch keeping only unclaimed files 7, B3 the
  intake record naming the playlists 2, B4 the steps naming every playlist 1,
  B5 a name the export came to hold refused before the moves 1, B6 the export's
  root names held 1, B7 the digest covering the split 1, B8 pending names held 1.
- `u113-c`, the native writer and the rotation, 9 rows, 9 killed: C1 the
  batch playlist not written when empty 6, C2 the batch keeping only unclaimed
  rows 7, C3 an account playlist created, never found by name 1, C4 the record
  naming each by identifier 2, C5 a removed node holding no name 1, C6 the name
  check before the first move 1, C7 only a proven import's names 1, C8 the batch
  folder asked of a recorded name 1, C9 the latest landing of a name 1.
- **The first run of `u113-c` was INVALID**: its null control killed
  `tests/test_queued_resume_contract.py::...[tag.retag]`, a case that spawns a
  real job driver. Its file passed 16 of 16 alone and the rerun's control
  killed nothing. Filed as R-910, the shape of R-900.

Considered and dropped below the cap, each with why:

- the engine's second name check inside `apply_rows`, which the check before
  the moves covers in every driven case; maintainer facing;
- the identifier filter on a recorded name (`not entry.get("id")`) and the
  account identifiers on a native record (`_named_ids`), each pinned by a test
  but ranked below the rows that guard a write;
- the rotation ageing a recorded name from its record rather than its row,
  which the 40 day test already reads;
- `landing_counts` dropping a playlist none of whose files landed, and the
  native screen's `_supported_only`, each reporting only.
