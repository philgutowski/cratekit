# Mutation rows, U23, round 7

This is U23's section of the shared table. It lives in its own file rather than in
`docs/mutation-rows.md` only because that file exists on `main` and this branch
does not carry it; fold this in at merge. Everything below follows that file's
rules.

**A count with no row definition beside it is not evidence.** Two mutation tables
have already been lost in this unit because they were reported in a message and
never written into the repository. Round 6 reported 39 rows; not one of them is in
`docs/`, in a commit, or derivable from its id, so the round 7 verifier could not
re-run a single one and had to build its own set. Worse, one row's deleted code
was in no commit at all: `git log -S` over `revert.py` finds nothing and
`git show HEAD` does not remove it, so the deletion happened inside a working tree
and left no artifact. **Round 6's `M01` and `M23` id correspondence is struck from
the record: it is unverifiable in principle from this branch.**

## Running a row

`pyproject.toml` already sets `addopts = "-q"`, so a second `-q` becomes `-qq` and
SUPPRESSES THE SUMMARY LINE. Use:

    .venv/bin/python -m pytest --tb=no

Snapshot the file before applying a row and restore from the snapshot, never with
`git checkout`: a fix round's own edits are uncommitted while the rows are being
measured, and `git checkout` throws them away with the mutation. The driver used
here copied `src/cratekit/adopt/revert.py` to a scratch directory, applied one
row, ran, restored, and restored again in a `finally`.

**Mutate a message by REWORDING it, never by appending.** The suite asserts many
messages with `in`, so an appended clause changes nothing and the resulting zero
says nothing about coverage. Four of round 7's first message mutations measured
zero for exactly that reason and were re-run as rewordings.

## Baseline

**3771 passed, 15 skipped**, on `unit/u23-library-adoption`, 2026-08-04, with
round 7's fix applied. Every count below was measured against the WHOLE suite. The
names beside each row come from a second pass over `tests/test_adoption.py` alone;
the whole-suite count and the adoption-only count agreed for every row, so no row
has blast radius outside that file.

| id | measured kills | what dies |
| --- | --- | --- |
| `M_reuse_accept` | 2 | the recycled-inode pair |
| `M_path_always_refreshed` | 1 | the hardlink record's address |
| `M_replace_makes_a_second_record` | 1 | the `os.replace` save |
| `M_remount_not_corroborated` | 3 | all three remount shapes |
| `M_no_search_by_bytes` | 1 | the legacy record through a rename |
| `M_group_over_selected` | 1 | the targeted revert |
| `M_confused_over_selected_only` | 1 | the targeted revert |
| `M_prefetch_inside_the_lock` | 1 | the two-read ordering |
| `M_no_prefetch_at_all` | 3 | the ordering, the tick, the evicted file |
| `M_stale_sighting_spent` | 1 | the same-tick in-place rewrite |
| `M_msg_replaced_opening_clause` | 1 | the full pin on `_replaced` |
| `M_msg_cannot_say_opening_clause` | 1 | the full pin on the ledger refusal |
| `M_msg_cannot_say_tail` | 1 | the same full pin |
| `M_legacy_width_23` | 12 | every test that spells the legacy key |
| `M_digest_state_gate` | 4 | the four unstamped shapes |
| `M_isreg_guard` | 2 | the FIFO and the directory |
| `M_stamp_attempts_1` | 2 | the retry and its exact count |
| `M_msg_not_a_regular_file` | 2 | the FIFO and the directory |

Every row below is in `src/cratekit/adopt/revert.py`.

## The row definitions

### `M_reuse_accept`, kills 2

Round 6's behaviour restored verbatim. In `_record_for`, the branch where a record
is keyed to this file's identity and its recorded path is not this file:

    -        raise RecordCannotBeMatched(
    -            _an_inode_is_not_a_file(by_identity, resolved), path=resolved
    -        )
    +        return _re_addressed(
    +            by_identity, identity=identity, path_text=path_text, keep_path=False
    +        )

Kills `test_a_RECYCLED_INODE_NUMBER_never_hands_one_files_record_to_another` and
`test_a_recorded_path_is_NEVER_REFRESHED_to_a_DIFFERENT_files_path`.

### `M_path_always_refreshed`, kills 1

The narrower half: keep the refusal, but let a matched record's address be moved
whenever the file in hand has a different name. In `_re_addressed`:

    -    wanted_path = record.path if keep_path else path_text
    +    wanted_path = path_text

Kills `test_one_file_under_TWO_HARD_LINKS_is_one_record`, at the assertion that the
record still points at the name it was written for. Before that assertion was
added this row killed 0, which is why it was added.

### `M_replace_makes_a_second_record`, kills 1

In `_record_for`, the branch where a record carries this path and the identity has
moved:

    -    raise RecordCannotBeMatched(
    -        _a_path_is_not_a_file(by_path, resolved), path=resolved
    -    )
    +    return None

Returning None writes a SECOND record whose `original` is the value adoption
itself wrote. Kills `test_an_os_replace_SAVE_does_not_produce_a_SECOND_record`.

### `M_remount_not_corroborated`, kills 3

Same branch, but disable the corroboration rather than the refusal, so a remount
refuses instead of being recognised:

    -    if _the_bytes_agree(by_path, look):
    +    if False and _the_bytes_agree(by_path, look):

Kills all three parameters of `test_a_REMOUNT_does_not_produce_a_SECOND_record`:
`inode-renumbered`, `mounted-in-another-order`, `both`.

### `M_no_search_by_bytes`, kills 1

In `_found_by_its_bytes`, empty the candidate list so no stranded record can ever
be found by its content:

    -    possible = [
    -        record
    -        for record in ledger.snapshots
    -        if record.field == field
    -        and record.digest_state is DigestState.RECORDED
    -        and record.size is not None
    -    ]
    +    possible: list[TagSnapshot] = []

Kills `test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`.

### `M_group_over_selected`, kills 1

Round 6's fix landing on the wrong object. In `revert_tags`:

    -        confused = _records_that_cannot_be_told_apart(ledger.snapshots)
    -        crowded = _paths_more_than_one_record_carries(ledger.snapshots)
    +        confused = _records_that_cannot_be_told_apart(selected)
    +        crowded = _paths_more_than_one_record_carries(selected)

Kills `test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`.

### `M_confused_over_selected_only`, kills 1

Only the first of those two lines, to show the group refusal is the load-bearing
one and the force-key check is not carrying it:

    -        confused = _records_that_cannot_be_told_apart(ledger.snapshots)
    +        confused = _records_that_cannot_be_told_apart(selected)

Kills the same one test.

### `M_prefetch_inside_the_lock`, kills 1

Move the prefetch inside the exclusive lock, which is the cost the pre-lock read
exists to avoid:

    -    _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)
    -    with config._exclusive_lock(lock_path(cfg)):
    -        ledger = read(cfg)
    +    with config._exclusive_lock(lock_path(cfg)):
    +        _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)
    +        ledger = read(cfg)

Kills
`test_the_FETCH_happens_before_the_lock_and_the_DECIDING_read_happens_under_it`,
whose expected value is the LIST `[False, True]` rather than a membership test, so
neither read can be dropped or reordered without it moving.

### `M_no_prefetch_at_all`, kills 3

Delete the prefetch call:

    -    _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)

Kills the ordering test above, plus
`test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway` (which
counts the reads) and
`test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught` (whose
fixture swaps the bytes when the first read returns and therefore needs there to
be a first read).

### `M_stale_sighting_spent`, kills 1

**The most important row in this table**, because it is round 6's mechanism
reconstructed rather than a hypothetical. Two edits together. First, give
`_bring_the_bytes_within_reach` a module-level map and have it record each answer
beside the four-value `stat` tuple taken with it:

    +_PRELOCK: dict[tuple[str, str], tuple[_Looked, tuple[int, int, int, int]]] = {}
    +
    +
     def _bring_the_bytes_within_reach(

    -        _look_at(Path(record.path), recorded_size=record.size)
    +        try:
    +            _info = Path(record.path).stat()
    +        except OSError:
    +            continue
    +        _PRELOCK[(record.file, record.field)] = (
    +            _look_at(Path(record.path), recorded_size=record.size),
    +            (_info.st_dev, _info.st_ino, _info.st_size, _info.st_mtime_ns),
    +        )

Second, in `_changed_since_adoption`, spend that answer whenever the tuple still
matches:

    -    looked = _look_at(target, recorded_size=record.size)
    +    _sighted = _PRELOCK.get((record.file, record.field))
    +    looked = _look_at(target, recorded_size=record.size)
    +    if _sighted is not None:
    +        try:
    +            _info = target.stat()
    +        except OSError:
    +            _info = None
    +        if _info is not None and (
    +            _info.st_dev,
    +            _info.st_ino,
    +            _info.st_size,
    +            _info.st_mtime_ns,
    +        ) == _sighted[1]:
    +            looked = _sighted[0]

Kills exactly
`test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`, and
nothing else. That test rewrites the file in place to the same length between the
two reads and puts the modification time back with `os.utime`, so all four values
are identical while the digest is not, which is the FAT measurement reproduced
portably.

### `M_msg_replaced_opening_clause`, kills 1

A REWORDING, not an append. In `_replaced`:

    -        f"this record cannot be matched to the file at that path: {why}. "
    +        f"this record does not line up with the file at that path: {why}. "

Killed 0 before round 7 and kills 1 now:
`test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`, which
asserts the whole message by EQUALITY against a spelled literal.

### `M_msg_cannot_say_opening_clause`, kills 1

In `_cannot_say_which_record`:

    -        f"this record cannot be spent on the file at that path: {why}. force "
    +        f"this record is not usable against the file at that path: {why}. force "

Killed 0 before round 7. Kills
`test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`.

### `M_msg_cannot_say_tail`, kills 1

The clause that carries the group refusal's entire "leaving it costs nothing"
promise, which was asserted nowhere:

    -        f"{(record.path, record.field)!r} instead; every original is still "
    -        f"recorded and nothing has been written."
    +        f"{(record.path, record.field)!r} instead."

Killed 0 before round 7. Kills the same targeted-revert test.

## The rows that had to stay dead, and did

Each of these was confirmed by re-running it against round 7's code.

### `M_legacy_width_23`, kills 12, and killed 9 before this round

    -_LEGACY_ID_WIDTH = 24
    +_LEGACY_ID_WIDTH = 23

Still load bearing, and the count went UP because three of round 7's new tests
also spell the 24 character key as a literal. Kills:
`test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`,
`test_a_legacy_record_that_is_the_only_one_for_its_file_still_reverts`,
`test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`,
`test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse`,
`test_an_identifier_from_NEITHER_scheme_is_refused_by_the_reader`,
`test_null_and_absent_are_both_NO_DIGEST_and_neither_is_an_acceptance`,
`test_TWO_RECORDS_for_ONE_FILE_refuse_and_are_not_offered_a_force`,
`test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`,
`test_a_SINGLE_RECORD_group_is_never_refused_as_ambiguous`,
`test_a_FORCE_KEY_that_names_two_UNIDENTIFIABLE_records_overrides_neither`,
`test_one_unreadable_record_costs_one_record_not_the_pass`,
`test_a_null_original_is_a_legitimate_record`.

### `M_digest_state_gate`, kills 4

    -    if record.digest_state is not DigestState.RECORDED:
    +    if False:

Kills `test_an_UNSTAMPED_record_refuses_a_file_that_was_replaced`,
`test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state`,
`test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot`,
`test_a_record_with_no_digest_refuses_INSTEAD_OF_falling_back_to_the_metadata`.

### `M_isreg_guard`, kills 2

    -    if not stat_module.S_ISREG(info.st_mode):
    +    if False:

Kills `test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever` and
`test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason`. The FIFO test
runs in a child process, so this row's run takes about twice as long as the others.

### `M_stamp_attempts_1`, kills 2

    -_STAMP_READ_ATTEMPTS = 2
    +_STAMP_READ_ATTEMPTS = 1

Kills `test_the_stamping_read_is_RETRIED_before_the_record_gives_up` and
`test_the_stamping_read_is_asked_EXACTLY_TWICE_and_not_three_times`.

### `M_msg_not_a_regular_file`, kills 2

A rewording, again:

    -_NOT_A_REGULAR_FILE = (
    -    "what is at that path is not a regular file, so it has no bytes to compare"
    -)
    +_NOT_A_REGULAR_FILE = (
    +    "the thing at that path is no kind of ordinary file, so there are no bytes"
    +)

Kills the FIFO test and the directory test.
