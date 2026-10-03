# U111 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's). The unit moves and
removes playlist nodes in the live database, so it gets the full 25 rows,
scoped to its own guards, in four batches, four considered rows dropped.

Four batches because a batch's baseline, its subsets and its promoted zeros
pass the harness's 600 second ceiling for one foreground call. Each ran on a
committed tree with a green full baseline, 12,666 collected for a to c and
12,667 for d after one test was added between them, each null control killed
nothing, and every restore was verified against `git show HEAD:`.

- `u111-a`, the writer's node primitives, 6 rows, 5 killed: A1 the folder
  refusal 1, A3 the parent that is not a folder 1, A4 the node's memberships
  marked 2, A5 the node itself marked 2, A7 the content comparison 1.
- **A6 reads `collect-error` with 6 deaths.** It removes the playlist table
  from `REMOVABLE_TABLES`, and `tests/test_rb_writer_guard.py` parametrizes
  over the tables NOT in that set, so the mutation adds a case and the
  collected count moves 226 to 227. Six tests died, the rotation's applies
  among them. Counted as killed.
- `u111-b`, the judge and the membership move, 6 rows, 6 killed: A8 a
  membership outside a removed playlist 2, A9 a planned move made 4, A10 a
  renumbering only where a node left or joined 1, A12 a removed node keeps no
  live membership 2, A13 the confinement check raises 2, B1 the membership
  move names its own table 1, by the source guard on who names removals.
- `u111-c`, the engine, 7 rows, 6 killed: C2 the batch folder asked of a dated
  name 3, C3 the `_inboxed` suffix 3, C4 removal after the expired threshold 2,
  C5 the move after the stale one 2, C6 the plan taken again on the write
  handle 1, C7 the created Old named to the judge 2.
- **C1 zero**, promoted to the full suite, 12,666 collected, confirmed. The row
  reads an aware `created_at` on the UTC calendar. The one producer, the pinned
  binding pyrekordbox 0.4.4, was driven and hands the column back naive and
  already local, so the aware branch has no reachable input and the evening
  test pins the local day through the binding either way. One candidate
  driven and it does not produce the input; maintainer facing, one line.
- `u111-d`, the verb, the landing record and the taxonomy, 6 rows, 6 killed:
  C9 a record that committed nothing dates nothing 1, C10 two Old folders
  refused 1, D1 the empty plan still asks 4, D2 the acknowledgment before the
  gate 1, E1 the landing names its batch playlist 1, F1 Old differs from the
  intake flow 2.

25 rows: 24 killed, one zero with no reachable input.

C9's death is on a test written for it between batches c and d, since before
that nothing drove an uncommitted landing record.

Dropped, ranked below the cap:

- A2, the writer's refusal of a node already removed. The plan reads live
  children only, so no planned node reaches the writer removed, and A1 in the
  same refusal is measured.
- A11, the judge's refusal of an unplanned playlist row. Pinned by its
  parametrized case and by C7, which reverts the one planned creation and was
  killed by this check.
- C8, the earliest of two landing records winning. Two records name one
  playlist only when a person lands twice under one `--name`, R-896's input.
- C11, a batch dated after the as-of day left alone. A negative age bands as
  keep, the conservative band, so the cost is a listing and never a write.

Batch c stopped once on the driver's state leak check, two new entries in the
real installation's run directory during row C7. They were a `crate status`
and a `crate job list` run at 15:23 local, from outside this session: the
driver points every child's state at its own workspace and C7's subset drives
neither verb. The batch was resumed with `--resume` and C7 measured clean.
