# Mutation rows, U23, round 8

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

    .venv/bin/python -m pytest --tb=no -rf --color=no

`--color=no` matters for anything that PARSES the run rather than reading it: with
colour on, each short-summary line begins with an ANSI escape rather than with
`FAILED`, so a driver matching on the prefix reports zero kills for a row that
killed twelve. That happened here, on the first pass, and is why every count below
was measured again.

Snapshot the file before applying a row and restore from the snapshot. Round 8's
driver takes the snapshot from the GIT OBJECT DATABASE, `git show HEAD:<path>`,
because the round's fix is COMMITTED before the rows are measured; it asserts the
working file's sha256 equals HEAD's before and after every row, and it restores in
a `finally` whatever the run did. A round whose fix is still uncommitted must
snapshot to a scratch file instead, because `git checkout` would throw the fix away
along with the mutation.

**Mutate a message by REWORDING it, never by appending.** The suite asserts many
messages with `in`, so an appended clause changes nothing and the resulting zero
says nothing about coverage. Four of round 7's first message mutations measured
zero for exactly that reason and were re-run as rewordings.

**A row that kills zero is a finding, not a footnote.** Three of round 8's rows
killed zero on their first measurement, and none of them was a redundant clause:
each was a load-bearing line that no assertion in the suite could observe, which is
the same defect as a claim backed by a written explanation rather than by a
measurement. All three now have a test and all three now die. Both numbers are kept
in the table, because the first one is what the suite could see.

## Baseline

**3782 passed, 15 skipped**, on `unit/u23-library-adoption` at `63a0e1e`,
2026-08-04, with round 8's fix applied. Round 7's baseline was 3771 passed and
15 skipped; the eleven new tests are round 8's.

Every count below was measured against `tests/test_adoption.py`. Four of the rows,
chosen as the ones most likely to reach outside that file, were measured against
the WHOLE suite as well, and the two agreed exactly in all four cases:
`M_legacy_width_23` 12 and 12, `M_vacant_is_mere_absence` 1 and 1,
`M_shape2_never_asks` 3 and 3, `M_hash_before_the_filters` 2 and 2. So no row has
blast radius outside `tests/test_adoption.py`. Where a count differs from round
7's, the change is stated in the row's own definition rather than left to be
noticed.

| id | measured kills | what dies |
| --- | --- | --- |
| `M_legacy_width_23` | 12 | every test that spells the legacy key |
| `M_at_risk_always_true` | 4 | every shape that asks what is at risk |
| `M_settled_refusal_becomes_a_match` | 4 | the same four, at the refusal itself |
| `M_digest_state_gate` | 4 | the four unstamped shapes |
| `M_remount_not_corroborated` | 4 | all three remount shapes, plus the replug |
| `M_shape2_never_asks` | 3 | the in-place replacement, both lengths |
| `M_no_prefetch_at_all` | 3 | the ordering, the tick, the evicted file |
| `M_reuse_accept` | 2 | the recycled-inode pair |
| `M_hash_before_the_filters` | 2 | both read-count tests |
| `M_replace_makes_a_second_record` | 2 | the `os.replace` save |
| `M_at_risk_drops_the_original` | 2 | the crash seam and the legacy migration |
| `M_msg_value_nothing_recorded` | 2 | the full pin on the new refusal |
| `M_isreg_guard` | 2 | the FIFO and the directory |
| `M_stamp_attempts_1` | 2 | the retry and its exact count |
| `M_msg_not_a_regular_file` | 2 | the FIFO and the directory |
| `M_vacant_is_mere_absence` | 1 | the unmounted volume |
| `M_shape3_never_asks` | 1 | the hardlink whose content moved |
| `M_size_never_compared` | 1, was 0 | the read count on a size mismatch |
| `M_at_risk_drops_this_call` | 1, was 0 | the third adoption |
| `M_at_risk_drops_the_record` | 1, was 0 | the second taxonomy |
| `M_doctor_prose_returns` | 1 | the absent verb |
| `M_path_always_refreshed` | 1 | the hardlink record's address |
| `M_no_search_by_bytes` | 1 | the legacy record through a rename |
| `M_group_over_selected` | 1 | the targeted revert |
| `M_confused_over_selected_only` | 1 | the targeted revert |
| `M_prefetch_inside_the_lock` | 1 | the two-read ordering |
| `M_stale_sighting_spent` | 1 | the same-tick in-place rewrite |
| `M_msg_replaced_opening_clause` | 1 | the full pin on `_replaced` |
| `M_msg_cannot_say_opening_clause` | 1 | the full pin on the ledger refusal |
| `M_msg_cannot_say_tail` | 1 | the same full pin |

Every row below is in `src/cratekit/adopt/revert.py`.

## The rows added in round 8

### `M_vacant_is_mere_absence`, kills 1

Round 7's line restored verbatim. In `_the_recorded_path_is_vacant`:

    -    recorded = Path(record.path)
    -    try:
    -        if not recorded.parent.is_dir():
    -            return False
    -        return not recorded.exists()
    -    except OSError:
    -        return False
    +    return not Path(record.path).exists()

Kills `test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`.

**Also driven on a real detachable image**, which is what the portable test stands
in for. `hdiutil create -size 40m -fs MS-DOS`, attached, a track adopted on it, a
byte identical backup taken elsewhere, the image DETACHED, the backup adopted, the
image reattached and the original re-adopted. With this row applied:

    adopted the USB track: original=('USB Own Genre',)
    a byte identical backup copy exists elsewhere: True
    volume detached, so the recorded path exists = False
    second adoption over the BACKUP: records=1
      the USB record survived = False
    volume replugged, USB file re-adopted: original=('Adopted Genre',)

and without it, same script, same image:

    second adoption over the BACKUP: records=2
      the USB record survived = True
    volume replugged, USB file re-adopted: original=('USB Own Genre',)

The image is detached in a `finally` and deleted.

### `M_hash_before_the_filters`, kills 2

Round 7's ordering restored: read the file first, discard the candidates
afterwards. In `_found_by_its_bytes`:

    -    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    -    if not vacant or size_here is None:
    -        return None
    -    same_size = [record for record in vacant if record.size == size_here]
    -    if not same_size:
    -        return None
    -    looked = look()
    -    if looked.outcome is not ByteRead.ANSWERED:
    -        return None
    -    stranded = [record for record in same_size if record.digest == looked.digest]
    +    looked = look()
    +    if looked.outcome is not ByteRead.ANSWERED:
    +        return None
    +    stranded = [
    +        record
    +        for record in possible
    +        if record.digest == looked.digest
    +        and _the_recorded_path_is_vacant(record)
    +    ]

Kills `test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN` and
`test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`.

**The second of those killed 0 before round 8**, because it adopted exactly ONE
file, and an empty ledger has no candidate to search whatever the search costs. A
test named for the first adoption OF A LIBRARY has to put a second file into a
ledger that already holds a stamped record; it now does. The eight-file test
asserts the per-file LIST rather than the total, so a read moved between files
cannot hide in the sum. Measured directly, eight files of 4 MiB each into an empty
ledger, `digest_of` calls per file:

    round 7:  [1, 2, 2, 2, 2, 2, 2, 2]  = 15 reads for 8 files
    round 8:  [1, 1, 1, 1, 1, 1, 1, 1]  =  8 reads for 8 files

### `M_shape2_never_asks`, kills 3

Round 7's shape 2 restored: two agreeing addresses return a match and the digest is
never consulted. In `_record_for`:

    -        if by_identity is by_path:
    -            return _settled_or_refused(
    -                by_identity,
    -                resolved,
    -                identity=identity,
    -                path_text=path_text,
    -                keep_path=True,
    -                written=written,
    -                look=look,
    -                current=current,
    -                size_here=size_here,
    -            )
    +        if by_identity is by_path:
    +            return _re_addressed(
    +                by_identity, identity=identity, path_text=path_text, keep_path=True
    +            )

Kills `test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`,
`test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut` and
`test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`.

### `M_shape3_never_asks`, kills 1

The same, for the hardlink shape:

    -            return _settled_or_refused(
    -                by_identity,
    -                resolved,
    -                identity=identity,
    -                path_text=path_text,
    -                keep_path=True,
    -                written=written,
    -                look=look,
    -                current=current,
    -                size_here=size_here,
    -            )
    +            return _re_addressed(
    +                by_identity, identity=identity, path_text=path_text, keep_path=True
    +            )

Kills
`test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`.
This is the cell round 7 decided by LINE ORDER: the hardlink test returned before
the byte test below it was reached, so the answer came from the order of two
branches rather than from evidence.

### `M_at_risk_always_true`, kills 4

The whole question deleted, which is round 7's behaviour reached from the other
side. In `_nothing_unrecorded_is_at_risk`:

    -    held = current()
    -    if held == record.original:
    -        return True
    -    return held in ((record.written,), (written,))
    +    return True

Kills the three from `M_shape2_never_asks` plus
`test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`.

### `M_settled_refusal_becomes_a_match`, kills 4

The same four, from the refusal end rather than the question end. In
`_settled_or_refused`:

    -    raise RecordCannotBeMatched(
    -        _a_value_nothing_recorded(record, resolved, current()), path=resolved
    -    )
    +    return _re_addressed(
    +        record, identity=identity, path_text=path_text, keep_path=keep_path
    +    )

### `M_at_risk_drops_the_original`, kills 2

    -    if held == record.original:
    -        return True

Kills `test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file` and
`test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`. The
clause is what carries a record whose write never landed: the field still holds the
original, there is no digest to ask, and refusing would strand it.

### `M_at_risk_drops_the_record`, kills 1, and killed 0 before its test

    -    return held in ((record.written,), (written,))
    +    return held == (written,)

Kills `test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`.
It killed 0 first time round: every test in the suite adopted into the same bucket
twice, so `record.written` and this call's `written` were the same string and either
clause alone carried both. The new test drives them apart.

### `M_at_risk_drops_this_call`, kills 1, and killed 0 before its test

    -    return held in ((record.written,), (written,))
    +    return held == (record.written,)

Kills
`test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`.
Also 0 first time round, for the same reason. The clause is load bearing because
`record.written` is written once, by the adoption that CREATED the record, and is
never updated: after a second adoption under a different taxonomy it names a bucket
that is on nothing, and a rule consulting only it would refuse a file whose field
already holds exactly what is about to be written.

### `M_size_never_compared`, kills 1, and killed 0 before its test

    -    if record.size is not None and size_here is not None and record.size != size_here:
    -        return False

Kills `test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`.
It killed 0 first time round and could not have done otherwise: the size can never
change an ANSWER, so every behavioural assertion stays green and the digest behind
it reaches the same refusal one whole-file read later. The claim is about COST, so
the test counts reads. Round 7 wrote this shortcut into a docstring and did not have
it: the comparison lives inside `_look_at`, which applies it only when handed a
recorded size, and the closure the lookup passes calls `_look_at` with none.

### `M_msg_value_nothing_recorded`, kills 2

A REWORDING, not an append, of the new refusal:

    -        f"its volume and inode and its path, but the bytes are not the ones "
    -        f"adoption left and its {record.field!r} now holds {held!r}, which is "
    +        f"its volume and inode and its path, but the content moved under it "
    +        f"and its {record.field!r} now holds {held!r}, which is "

Kills `test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped` and
`test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`.

### `M_doctor_prose_returns`, kills 1

Round 7's instruction put back into `_a_path_is_not_a_file`:

    -        f"file and its own tag value is untouched; the record still holds "
    -        f"{record.original!r} for {(record.path, record.field)!r}."
    +        f"file and its own tag value is untouched. Run the doctor over the ledger."

Kills
`test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`.
`crate doctor` answers `invalid choice: 'doctor'`; the registry marks the entry
`planned_in="U27"`. The residual titled "the refusal's remedy names a verb that has
not landed" carries the half deliberately not fixed here.

## The rows carried forward, and the two whose counts moved

### `M_legacy_width_23`, kills 12

    -_LEGACY_ID_WIDTH = 24
    +_LEGACY_ID_WIDTH = 23

Unchanged from round 7 at 12. Kills:
`test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse`,
`test_TWO_RECORDS_for_ONE_FILE_refuse_and_are_not_offered_a_force`,
`test_a_FORCE_KEY_that_names_two_UNIDENTIFIABLE_records_overrides_neither`,
`test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`,
`test_a_SINGLE_RECORD_group_is_never_refused_as_ambiguous`,
`test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`,
`test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`,
`test_a_legacy_record_that_is_the_only_one_for_its_file_still_reverts`,
`test_a_null_original_is_a_legitimate_record`,
`test_an_identifier_from_NEITHER_scheme_is_refused_by_the_reader`,
`test_null_and_absent_are_both_NO_DIGEST_and_neither_is_an_acceptance`,
`test_one_unreadable_record_costs_one_record_not_the_pass`.

### `M_digest_state_gate`, kills 4

In `_changed_since_adoption`, which is the revert guard rather than the lookup. The
same line exists in two other functions, so the row carries the line below it:

    -    if record.digest_state is not DigestState.RECORDED:
    -        return _replaced(record, _why_nothing_to_compare(record))
    +    if False:
    +        return _replaced(record, _why_nothing_to_compare(record))

Kills `test_a_record_with_no_digest_refuses_INSTEAD_OF_falling_back_to_the_metadata`,
`test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot`,
`test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state`,
`test_an_UNSTAMPED_record_refuses_a_file_that_was_replaced`.

### `M_remount_not_corroborated`, kills 4, and killed 3 in round 7

Shape 5's corroboration disabled, so a remount refuses instead of being recognised:

    -    assert by_path is not None
    -    if _the_bytes_agree(by_path, look, size_here):
    +    assert by_path is not None
    +    if False and _the_bytes_agree(by_path, look, size_here):

Kills all three parameters of `test_a_REMOUNT_does_not_produce_a_SECOND_record`
(`inode-renumbered`, `mounted-in-another-order`, `both`) and, new this round,
`test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`. The count
went UP because that test replugs the volume and re-adopts, which IS a remount: the
recorded path resolves again and the identity has moved, so shape 5 settles it.

### `M_reuse_accept`, kills 2

Round 6's behaviour restored. In `_record_for`, the branch where a record is keyed
to this file's identity and its recorded path is not this file:

    -        raise RecordCannotBeMatched(
    -            _an_inode_is_not_a_file(by_identity, resolved), path=resolved
    -        )
    +        return _re_addressed(
    +            by_identity, identity=identity, path_text=path_text, keep_path=False
    +        )

Kills `test_a_RECYCLED_INODE_NUMBER_never_hands_one_files_record_to_another` and
`test_a_recorded_path_is_NEVER_REFRESHED_to_a_DIFFERENT_files_path`.

### `M_path_always_refreshed`, kills 1

    -    wanted_path = record.path if keep_path else path_text
    +    wanted_path = path_text

Kills `test_one_file_under_TWO_HARD_LINKS_is_one_record`, at the assertion that the
record still points at the name it was written for.

### `M_replace_makes_a_second_record`, kills 2, and killed 1 in round 7

Shape 5's refusal removed:

    -    raise RecordCannotBeMatched(
    -        _a_path_is_not_a_file(by_path, resolved), path=resolved
    -    )
    +    return None

Kills `test_an_os_replace_SAVE_does_not_produce_a_SECOND_record` and, new this
round, `test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`,
which builds that refusal through the public API in order to inspect its wording.

### `M_no_search_by_bytes`, kills 1

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

    -        confused = _records_that_cannot_be_told_apart(ledger.snapshots)
    -        crowded = _paths_more_than_one_record_carries(ledger.snapshots)
    +        confused = _records_that_cannot_be_told_apart(selected)
    +        crowded = _paths_more_than_one_record_carries(selected)

Kills `test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`.

### `M_confused_over_selected_only`, kills 1

Only the first of those two lines, to show the group refusal is the load-bearing one
and the force-key check is not carrying it:

    -        confused = _records_that_cannot_be_told_apart(ledger.snapshots)
    +        confused = _records_that_cannot_be_told_apart(selected)

Kills the same one test.

### `M_prefetch_inside_the_lock`, kills 1

    -    _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)
    -    with config._exclusive_lock(lock_path(cfg)):
    -        ledger = read(cfg)
    +    with config._exclusive_lock(lock_path(cfg)):
    +        _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)
    +        ledger = read(cfg)

Kills
`test_the_FETCH_happens_before_the_lock_and_the_DECIDING_read_happens_under_it`,
whose expected value is the LIST `[False, True]` rather than a membership test.

### `M_no_prefetch_at_all`, kills 3

    -    _bring_the_bytes_within_reach(cfg, entry_id=entry_id, forced=forced)

Kills the ordering test above, plus
`test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway` and
`test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`.

### `M_stale_sighting_spent`, kills 1

**The most important carried-forward row**, because it is round 6's mechanism
reconstructed rather than a hypothetical. Three edits together. First, a
module-level map above `_bring_the_bytes_within_reach`:

    +_PRELOCK: dict[tuple[str, str], tuple[_Looked, tuple[int, int, int, int]]] = {}
    +
    +
     def _bring_the_bytes_within_reach(

Second, in that function's loop, record each answer beside the four-value `stat`
tuple taken with it:

    -        _look_at(Path(record.path), recorded_size=record.size)
    +        try:
    +            _info = Path(record.path).stat()
    +        except OSError:
    +            continue
    +        _PRELOCK[(record.file, record.field)] = (
    +            _look_at(Path(record.path), recorded_size=record.size),
    +            (_info.st_dev, _info.st_ino, _info.st_size, _info.st_mtime_ns),
    +        )

Third, in `_changed_since_adoption`, spend that answer whenever the tuple still
matches:

    -    looked = _look_at(target, recorded_size=record.size)
    -    if looked.outcome is ByteRead.A_DIFFERENT_SIZE:
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
    +    if looked.outcome is ByteRead.A_DIFFERENT_SIZE:

Kills exactly
`test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`, and
nothing else. That test rewrites the file in place to the same length between the
two reads and puts the modification time back with `os.utime`, so all four values
are identical while the digest is not, which is the FAT measurement reproduced
portably.

### `M_msg_replaced_opening_clause`, kills 1

    -        f"this record cannot be matched to the file at that path: {why}. "
    +        f"this record does not line up with the file at that path: {why}. "

Kills `test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught`,
which asserts the whole message by EQUALITY against a spelled literal.

### `M_msg_cannot_say_opening_clause`, kills 1

    -        f"this record cannot be spent on the file at that path: {why}. force "
    +        f"this record is not usable against the file at that path: {why}. force "

Kills `test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal`.

### `M_msg_cannot_say_tail`, kills 1

The clause carrying the group refusal's entire "leaving it costs nothing" promise:

    -        f"about the ledger. The record is "
    -        f"{(record.path, record.field)!r}; every original is still "
    -        f"recorded and nothing has been written."
    +        f"about the ledger. The record is "
    +        f"{(record.path, record.field)!r}."

Kills the same targeted-revert test.

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

    -    "what is at that path is not a regular file, so it has no bytes to compare"
    +    "the thing at that path is no kind of ordinary file, so there are no bytes"

Kills the FIFO test and the directory test.

## The three claim space, every cell mapped

A record carries three claims about which file it is about: `file` is the volume
and inode adoption saw, `path` is where it was, and `digest` is the bytes adoption
left. The SHAPES in `_record_for` are named by which ADDRESSES claim the file,
which is a different enumeration from what the three claims SAY, and a cell falling
between the two is how round 7's defect survived a review round. Both are written
out so neither can be read as the other.

| cell | the three claims | where it lands | pinned by |
| --- | --- | --- | --- |
| C1 | nothing claims it | shape 1, a new record | `test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING` |
| C2 | id and path agree, digest DIVERGES | shape 2, then `_settled_or_refused`: accepted when the field holds a value the ledger accounts for, refused otherwise | `test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`, `test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk` |
| C3 | all three agree | shape 2, accepted, no read | `test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING` |
| C4a | id agrees by a hardlink, digest agrees | shape 3, accepted, the record keeps its name | `test_one_file_under_TWO_HARD_LINKS_is_one_record` |
| C4b | id agrees by a hardlink, digest DIVERGES | shape 3, then the same function | `test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger` |
| C5 | id agrees, path is somebody else, digest agrees | shape 4, re-addressed | `test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled` |
| C6 | id agrees, path is somebody else, digest DIVERGES | shape 4, refused | `test_a_RECYCLED_INODE_NUMBER_never_hands_one_files_record_to_another` |
| C7 | id agrees, path is gone, NO digest | shape 4, refused | `test_a_record_with_no_digest_refuses_INSTEAD_OF_falling_back_to_the_metadata` |
| C8 | path agrees, id moved, digest agrees | shape 5, re-addressed | `test_a_REMOUNT_does_not_produce_a_SECOND_record` |
| C9 | path agrees, id moved, digest DIVERGES | shape 5, refused | `test_an_os_replace_SAVE_does_not_produce_a_SECOND_record` |
| C10 | two records, one by each address | shape 6, refused | `test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse` |
| C11 | no address claims it, a stranded record's bytes are these | the byte search, re-addressed | `test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled` |
| C12 | all three agree AND a hardlinked second path also has a record | never reaches `_record_for`: `read` refuses the whole document with every original in it intact | `test_TWO_RECORDS_for_ONE_FILE_AND_FIELD_never_reach_the_lookup_at_all` |
| C13 | no address claims it, a stranded record's bytes are these, but its VOLUME is merely absent | not stranded, a new record | `test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record` |
| C14 | no address claims it, TWO stranded records carry these bytes | refused, never resolved by document order | the `_one_or_none` call inside `_found_by_its_bytes`, whose sibling refusal is pinned by `test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse` |
| C15 | id and path agree, NO digest at all | shape 2, accepted, the crash seam | `test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file` |
| C16 | id and path agree, digest diverges, the field holds the ORIGINAL | shape 2, accepted, the write never landed | `M_at_risk_drops_the_original`, which kills `test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file` |
| C17 | id agrees by a hardlink AND the digest is wrong | shape 3, decided by `_settled_or_refused` rather than by which branch comes first | `test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger` |

C2, C4b and C17 were UNMAPPED before round 8: shapes 2 and 3 returned on the two
agreeing addresses and the digest was never consulted, so C17 in particular was
decided by `_live_identity` sitting above `_the_bytes_agree` rather than by any
evidence. C12 was reachable only as a document already on disk, and is now stated
as the READER's answer rather than left as a gap in the six shapes.

**C14 is the one cell with no test of its own**, and it is named rather than
quietly counted: reaching it needs two stranded records stamped from identical
bytes whose paths are both vacant and whose directories both exist, which the
suite constructs nowhere. The refusal it lands in is the same `_one_or_none` the
two other ambiguity cells use, so the branch is exercised and this arrangement of
it is not.

**What the mapping does NOT claim.** In C2 and C4b the first question asked is
about the FIELD, not about the bytes, and it is asked because its answer decides
whether the whole-file read is worth taking at all. Where a replacement's own value
in that field happens to equal the string the record says adoption wrote, it is
accepted. The residual titled "a stranger's field value that coincides with the
recorded one is accepted" carries that, states why it is not an identity claim, and
names what would close it.
