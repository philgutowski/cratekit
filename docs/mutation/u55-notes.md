# U55's mutation table, read as a verdict

Two rounds, both measured by `scripts/mutate.py` on 2026-09-02 on branch
`relay/73`. Round one is `u55-collection-reader.{md,json}`, thirty rows against
the branch's own diff. Round two is `u55-round-2.{md,json}`, the nine rows round
one read as zero, re-measured after the tests round one asked for.

Read this file first. The two tables carry every row's description and count; this
one carries what the numbers mean and which of them cost anything.

## The headline

**Round one: 30 rows, 23 killed, 7 zero.** Null control killed 0 against a green
6669 collected baseline, which is what makes the rest of the table believable.

**Round two: 9 rows re-measured, 5 now kill, 4 still zero.** The four are inert
mutations rather than test gaps, and each one's reason is a measurement rather
than an argument. Collected held at 6675 on every promoted row, so no row took a
file out of collection and reported a calm false zero.

**Four rows drove a change to the code or the tests before merge.** Round one's
seven zeros were not seven gaps: four were, and closing them is
`e81cb2a` and `b0c7d5e`.

## What each zero turned out to be

### R8, the census dropped the configured volume rewrite. A REAL gap, closed.

Round one: 0. Round two: 1.

Nothing in this repository drove a library whose rows are recorded under a
different prefix from the one it is mounted at, so removing `prefix_map` from
`census` changed nothing any test could see. That is S1's whole failure shape:
the source library records most of its active rows under an older volume name,
and a resolver without the map resolves none of them.
`test_a_configured_volume_rewrite_reaches_the_census` drives both sides, the
unmapped row classifying `unmapped` and the mapped one classifying `readable`.

### R16, the apply's resume had no zero item guard. A REAL gap, closed.

Round one: 0. Round two: 1. The scan's sibling guard killed 1 in round one, so
this was one verb covered and one not.

### R17 and R18, both R-225 predicates. A REAL gap, closed.

Round one: 0 each. Round two: 1 each. Every failure driven anywhere in this
branch reaches FAILED, so narrowing "closed and carrying a cause" to "FAILED"
killed nothing. A run stopped by a signal is CANCELLED and carries the cause
`jobs.cancel` builds, and the narrow predicate reports that through a normal
envelope and exits 0. That exact shape was measured on the two outbound verbs on
2026-09-02 as exit 0 over a job with none of its items done, so this is a defect
this repository has already shipped once.

### R23, the worker's raise on a failed report. A REAL gap, closed.

Round one: 0. Round two: 1. `apply_plan` RETURNS its failed entries and
`jobs.drive` fails an item only when the handler raises, so a worker that returned
would flip the item to done and drive the job to SUCCEEDED over an apply that
placed nothing. Every failure driven elsewhere in this branch comes out of the
membership write instead, which raises on its own, so the branch that converts a
returned failure had no cover at all.

### R2 and R6, the encryption probe. INERT, and the reason is a missing fixture.

Round one and two: 0. Both mutations make the probe answer "not encrypted".
Every database in this suite is a disposable one built from the binding's own
schema and none of them is encrypted, so the correct answer and the mutated one
agree on every input the suite has. A real library is encrypted and both
mutations fail against it.

**This is a measured absence rather than a covered guard**, and it is recorded as
part of R-239 rather than dismissed. Supplying `CRATEKIT_TEST_DB` pointing at a
real snapshot is what would give these rows an input; this run had none, and
saying so is the point.

### R5, the reader's cache key. INERT.

Round one and two: 0, and it is `maintainer` surface, so METHOD gives it one line
rather than a composite. `rb_writer.live_db_path` already returns an absolute
path, so `.resolve()` is a no-op on every input the suite produces. It earns its
place against a configuration carrying a relative or symlinked database path,
which nothing here builds.

### R26, the apply's write intent open. INERT IN HALF, and the composite says which half.

Round one and two: 0, including after
`test_the_apply_opens_its_own_handle_with_write_intent` was added and passes.

The reason is the one METHOD names: a guard covered by another guard is a guard
nothing covers. `require_closed=True` does two things at the open, and the
two-process refusal is asserted a second time inside the session
(`core/session.py:1820` asserts rekordbox closed before it verifies a commit), so
reverting the flag still refuses, just from one layer down.

**The composite is `test_the_application_pin_is_what_the_write_intent_open_uniquely_holds`.**
`assert_app_version` runs ONLY inside `open_db`'s `require_closed` branch, and
nothing else on the membership path asks it, so a rekordbox that has updated
itself since the pin was recorded reaches the commit with the flag off. That test
drives `app-version-pin-drift` through `_write_memberships` directly. It was
written after round two measured the row, so the row's zero stands as measured and
the composite is what says what the flag holds alone.

## Rows dropped below the cap, and why

Round one logged four, in the row file itself:

- `R31_check_app_version`: inert by construction. `open_db` consults
  `check_app_version` only inside its `require_closed` branch, so on the reader's
  read-only open it can kill nothing. Recorded in the plan's KTD1 instead.
- `R32_apply_handler_bound`: the sibling of `R30`, same guard, same table, same
  derivation. `tests/test_handlers.py` derives its population from the registry,
  so one of the pair measures the mechanism and the second buys nothing.
- `R33_artifact_ordinal`: the same guard `modules/outbound/artifacts` already
  carries and U51 already measured. This unit's copy adds no new decision, which
  is R-240.
- `R34_analysis_roots`: `write_tree_membership` raises `ValueError` on an empty
  `analysis_roots` by construction, so the row would measure that function's own
  guard rather than this unit's caller.

Thirty rows against a cap of forty five, so nothing was dropped for room.

## The rows worth reading twice

- **`R1_read_only_open`, 2 kills.** The single most important row in this table.
  Flipping the reader's `require_closed` to True makes it a write intent open, and
  two tests refuse it: the recorded-call assertion and the AST walk over the
  module. Not a large number, and it is the number that matters most.
- **`R4_genre_proxy`, 19 kills.** Reading `GenreID` instead of the binding's
  display proxy breaks nineteen tests, which is the census's whole routing
  surface.
- **`R21_membership_from_the_plan`, 9 kills.** Deriving the membership write from
  what this run applied rather than from the plan. Nine, because the crash-repair
  property and the happy path both die.
- **`R22_membership_before_the_mark`, 2 kills.** The ordering the drive reversed:
  apply first, write memberships second, which left the ledger holding every entry
  while the database held no membership row. It kills 2 rather than 20 because
  only two tests read the ledger back after a refusal, and those two are the ones
  that found it.
- **`R19_collector_groups_locations`, 1 kill.** Thin, and it is thin honestly: the
  collector's mapping is reported rather than written, so exactly one assertion
  reads it. What is written is `R20`'s mapping, which kills 4.
