# Mutation table: u23-round-8-independent

Measured by `scripts/mutate.py` on 2026-08-14 14:06 UTC, branch `unit/u23-library-adoption` at `23b8465`. Pass kind: full.

Baseline: green, 3797 collected. pytest invocations for this batch: 10.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3797 against 3797. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S1_size_of_always_none` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `S2_size_of_oserror_is_zero` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 3797 | 0 (promoted) | zero |
| `A1_at_risk_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `A2_at_risk_always_false` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 6 | killed |
| `A3_at_risk_drops_the_original_clause` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `A4_at_risk_drops_the_record_value` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `A5_at_risk_drops_this_call` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `A6_at_risk_original_by_identity` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `B1_settled_never_refuses` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `B2_settled_drops_the_bytes_acceptance` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `B3_settled_bytes_clause_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `C1_shape2_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `C2_shape3_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `D1_bytes_agree_drops_the_size_gate` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `D2_bytes_agree_size_gate_inverted` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 6 | killed |
| `D3_bytes_agree_drops_the_digest_state_gate` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `D4_bytes_agree_ignores_the_outcome` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `E1_vacancy_is_mere_absence` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `E2_vacancy_parent_check_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `E3_vacancy_oserror_is_vacant` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `E4_vacancy_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `F1_byte_search_drops_the_vacancy_filter` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `F2_byte_search_drops_the_size_here_guard` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 3797 | 0 (promoted) | zero |
| `F3_byte_search_drops_the_size_filter` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 3797 | 0 (promoted) | zero |
| `F4_byte_search_reads_before_it_filters` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `F5_byte_search_admits_sizeless_records` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `F6_byte_search_admits_unstamped_records` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `G1_locked_passes_no_size` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `G2_locked_current_is_not_memoised` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 3797 | 0 (promoted) | zero |
| `H1_unrecorded_value_refusal_reworded` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `X1_approval_type_check_never_fires` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 7 | killed |
| `X2_approval_option_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `X3_approval_actor_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `X4_approval_digest_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `X5_grant_accepts_a_blank_actor` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `X6_adoptable_widens_to_online_only` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `X7_classify_accepts_the_fallback_tier` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `X8_classify_drops_the_too_coarse_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `X9_outstanding_returns_everything` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 615 | 2 | killed |
| `X10_entry_id_drops_the_sub` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 615 | 1 | killed |
| `X11_restore_writes_absence_as_empty` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 3797 | 0 (promoted) | zero |
| `X12_look_at_drops_the_regular_file_test` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `X13_look_at_drops_the_recorded_size_shortcut` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `X14_probe_drops_the_dataless_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `X15_save_drops_the_id3v1_trailer` | `src/cratekit/core/tags.py` | user | 3 file(s) | 778 | 1 | killed |

## Zero rows and what they owe

- `S2_size_of_oserror_is_zero` (maintainer facing): maintainer facing, composite not required
- `B2_settled_drops_the_bytes_acceptance` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D3_bytes_agree_drops_the_digest_state_gate` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D4_bytes_agree_ignores_the_outcome` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `E3_vacancy_oserror_is_vacant` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `F2_byte_search_drops_the_size_here_guard` (maintainer facing): maintainer facing, composite not required
- `F3_byte_search_drops_the_size_filter` (maintainer facing): maintainer facing, composite not required
- `F5_byte_search_admits_sizeless_records` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `F6_byte_search_admits_unstamped_records` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `G2_locked_current_is_not_memoised` (maintainer facing): maintainer facing, composite not required
- `H1_unrecorded_value_refusal_reworded` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `X6_adoptable_widens_to_online_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `X11_restore_writes_absence_as_empty` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `H2_one_or_none_refusal_reworded`: Reword the ambiguous-record refusal round 8 rewrote to drop the doctor Dropped because: ranked below the cap: same message family as H1, which is measured, and round 8's own table already reports non-zero counts for three of the five rewordings
- `H3_two_records_refusal_reworded`: Reword the two-records-claim refusal round 8 rewrote Dropped because: ranked below the cap: same message family as H1
- `H4_cannot_say_which_record_reworded`: Reword the force-does-not-apply refusal round 8 rewrote Dropped because: ranked below the cap: same message family as H1
- `H5_inode_refusal_tail_reworded`: Reword the tail round 8 appended to _an_inode_is_not_a_file Dropped because: ranked below the cap: same message family as H1
- `H6_path_refusal_tail_reworded`: Reword the tail round 8 appended to _a_path_is_not_a_file Dropped because: ranked below the cap: same message family as H1
- `P1_prefetch_skips_forced_records`: The prefetch loop stops skipping a forced record Dropped because: ranked below the cap: not touched by round 8's diff, and carried forward from round 7's table at 1 and 3 deaths
- `P2_prefetch_recorded_size_not_passed`: The prefetch calls _look_at with no recorded size Dropped because: ranked below the cap: X13 measures the same shortcut at the place it is implemented, which is strictly stronger
- `P3_placeholder_beside_oserror_true`: A directory that refuses the stub question is read as holding a stub Dropped because: ranked below the cap: same OSError-is-not-evidence shape as E3, which is measured on round 8's own new code
- `Q1_find_collisions_merges_silently`: An existing rekordbox folder with different contents is merged rather than surfaced Dropped because: ranked below the cap: a brief test scenario, but untouched since round 5 and outside round 8's diff; F and E rows buy more per row on the round that is actually under review
- `Q2_applied_ledger_version_unchecked`: The applied ledger reader stops refusing an unknown version Dropped because: ranked below the cap: maintainer facing document validation, untouched by round 8
- `Q3_registry_planned_in_u27`: The doctor verb's planned_in marker is removed from the CLI registry Dropped because: ranked below the cap: round 8 only cites this marker in prose, it changed no code there, and U27 owns the surface
- `Q4_stamped_records_pre_write_digest`: _stamped takes the digest before the tag write rather than after Dropped because: ranked below the cap: untouched by round 8 and already load bearing under the D3 and F6 rows, which both fail closed if the stamp moves
- `Q5_original_taken_by_read_field_again`: _record_locked builds a new record from read_field rather than from the memoised current() Dropped because: ranked below the cap: semantically an identity mutation, so it can only move a read COUNT, and G2 already measures that closure

## Row definitions

### `S1_size_of_always_none`

_size_of never answers, so every size shortcut on every path is disabled

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    try:
        return target.stat().st_size
    except OSError:
        return None

```

New text:

```
    return None

```

### `S2_size_of_oserror_is_zero`

_size_of turns an unaskable size into the realistic nearby value 0

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return target.stat().st_size
    except OSError:
        return None

```

New text:

```
    try:
        return target.stat().st_size
    except OSError:
        return 0

```

### `A1_at_risk_always_true`

Nothing is ever at risk, so _settled_or_refused can never refuse

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return True

```

### `A2_at_risk_always_false`

Everything is at risk, so every re-run falls through to the digest

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`
  - `tests/test_adoption.py::test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk`
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return False

```

### `A3_at_risk_drops_the_original_clause`

A field holding this record's own original is no longer accounted for

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    return held in ((record.written,), (written,))

```

### `A4_at_risk_drops_the_record_value`

The value the record says adoption wrote no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((written,),)

```

### `A5_at_risk_drops_this_call`

The value THIS call is about to write no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,),)

```

### `A6_at_risk_original_by_identity`

The original clause compares by object identity rather than by value

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held is record.original:
        return True
    return held in ((record.written,), (written,))

```

### `B1_settled_never_refuses`

Round 7 restored: the two converging-address shapes accept unconditionally

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    if _nothing_unrecorded_is_at_risk(record, written=written, current=current):
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

New text:

```
    if True:
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

### `B2_settled_drops_the_bytes_acceptance`

An at-risk field refuses even when the bytes are exactly what adoption left

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT, so whatever is in the field
        # was put there by adoption, however little ``written`` still resembles
        # it. Nothing unrecorded is present and first-write-wins is right.
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    raise RecordCannotBeMatched(

```

New text:

```
    raise RecordCannotBeMatched(

```

### `B3_settled_bytes_clause_inverted`

The bytes acceptance fires when the bytes DISAGREE

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    if _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

New text:

```
    if not _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

### `C1_shape2_bypasses_the_check`

Shape 2, both addresses agreeing, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
        if by_identity is by_path:
            return _settled_or_refused(
                by_identity,
                resolved,
                identity=identity,
                path_text=path_text,
                keep_path=True,
                written=written,
                look=look,
                current=current,
                size_here=size_here,
            )

```

New text:

```
        if by_identity is by_path:
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )

```

### `C2_shape3_bypasses_the_check`

Shape 3, one file under two names, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`

Old text:

```
            # a different question and the shape below is where it is asked.
            return _settled_or_refused(

```

New text:

```
            # a different question and the shape below is where it is asked.
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )
            return _settled_or_refused(

```

### `D1_bytes_agree_drops_the_size_gate`

The size shortcut round 8 restored is removed again

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
        return False

```

New text:

```
(empty)
```

### `D2_bytes_agree_size_gate_inverted`

The size shortcut refuses on AGREEING sizes

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[both]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[inode-renumbered]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[mounted-in-another-order]`
  - `tests/test_adoption.py::test_a_file_RENAMED_between_two_adoptions_is_still_one_record`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
```

New text:

```
    if record.size is not None and size_here is not None and record.size == size_here:
```

### `D3_bytes_agree_drops_the_digest_state_gate`

An unstamped record is allowed to reach the digest comparison

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if record.digest_state is not DigestState.RECORDED:
        return False
    if record.size is not None and size_here is not None and record.size != size_here:
```

New text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
```

### `D4_bytes_agree_ignores_the_outcome`

A read that did not answer is compared on its empty digest anyway

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return looked.outcome is ByteRead.ANSWERED and looked.digest == record.digest
```

New text:

```
    return looked.digest == record.digest
```

### `E1_vacancy_is_mere_absence`

Round 7 restored: an unmounted volume reads as a deleted file

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
    recorded = Path(record.path)
    try:
        return not recorded.exists()
    except OSError:
        return False

```

### `E2_vacancy_parent_check_inverted`

Vacancy requires the containing directory to be ABSENT

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

New text:

```
        if recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

### `E3_vacancy_oserror_is_vacant`

A directory that refuses the question is read as a vacant path

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
        return not recorded.exists()
    except OSError:
        return True

```

### `E4_vacancy_always_true`

Every record is stranded, so every record is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
    return True

```

### `F1_byte_search_drops_the_vacancy_filter`

A record whose path still holds its file is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
```

New text:

```
    vacant = list(possible)
```

### `F2_byte_search_drops_the_size_here_guard`

A file whose own size cannot be asked still reaches the size filter

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not vacant or size_here is None:
        return None
```

New text:

```
    if not vacant:
        return None
```

### `F3_byte_search_drops_the_size_filter`

Every vacant record is hashed against, whatever size it recorded

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    same_size = [record for record in vacant if record.size == size_here]
```

New text:

```
    same_size = list(vacant)
```

### `F4_byte_search_reads_before_it_filters`

Round 7 order restored: the whole-file read runs before the filters that empty the list

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None

```

New text:

```
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None

```

### `F5_byte_search_admits_sizeless_records`

A record carrying no size is admitted to the candidate list

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if record.field == field
        and record.digest_state is DigestState.RECORDED
        and record.size is not None
    ]
```

New text:

```
        if record.field == field
        and record.digest_state is DigestState.RECORDED
    ]
```

### `F6_byte_search_admits_unstamped_records`

A record whose write never stamped is admitted to the candidate list

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if record.field == field
        and record.digest_state is DigestState.RECORDED
        and record.size is not None
    ]
```

New text:

```
        if record.field == field
        and record.size is not None
    ]
```

### `G1_locked_passes_no_size`

_record_locked hands size_here=None, disabling every size gate below it

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
        size_here=_size_of(resolved),
```

New text:

```
        size_here=None,
```

### `G2_locked_current_is_not_memoised`

The tag-field closure re-reads the field on every call

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    def current() -> tuple[str, ...] | None:
        if not known:
            known.append(read_field(resolved, field))
        return known[0]

```

New text:

```
    def current() -> tuple[str, ...] | None:
        return read_field(resolved, field)

```

### `H1_unrecorded_value_refusal_reworded`

Reword the opening clause of the refusal round 8 added

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        f"{resolved} is the file a record in the revert ledger is about, by both "
        f"its volume and inode and its path, but the bytes are not the ones "
```

New text:

```
        f"{resolved} answers to a ledger record on both addresses at once, "
        f"and yet the bytes are not the ones "
```

### `X1_approval_type_check_never_fires`

R34: a blanket affirmative is no longer refused by type

- File: `src/cratekit/adopt/approval.py`
- Surface: user
- Subset: test files importing cratekit.adopt.approval
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 7 (killed)
- Killed:
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[NoneTypeNone]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[boolTrue]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'approved':]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'digest': ']`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[int1]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[strapprove]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[stryes]`

Old text:

```
    if not isinstance(approval, Approval):
```

New text:

```
    if not isinstance(approval, object):
```

### `X2_approval_option_unchecked`

A recorded answer that is not the approve option is accepted

- File: `src/cratekit/adopt/approval.py`
- Surface: user
- Subset: test files importing cratekit.adopt.approval
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_recorded_answer_that_is_not_an_approval_applies_nothing`

Old text:

```
    if approval.option != APPROVE:
```

New text:

```
    if approval.option is None:
```

### `X3_approval_actor_unchecked`

An approval naming nobody is accepted at apply time

- File: `src/cratekit/adopt/approval.py`
- Surface: user
- Subset: test files importing cratekit.adopt.approval
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(approval.actor).strip():
```

New text:

```
    if approval.actor is None:
```

### `X4_approval_digest_unchecked`

An approval given for a different plan is accepted

- File: `src/cratekit/adopt/approval.py`
- Surface: user
- Subset: test files importing cratekit.adopt.approval
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_for_a_different_plan_is_refused`

Old text:

```
    if approval.digest != current:
```

New text:

```
    if approval.digest is None:
```

### `X5_grant_accepts_a_blank_actor`

grant records an approval attributed to nobody

- File: `src/cratekit/adopt/approval.py`
- Surface: user
- Subset: test files importing cratekit.adopt.approval
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(actor).strip():
```

New text:

```
    if actor is None:
```

### `X6_adoptable_widens_to_online_only`

A cloud-backed track becomes adoptable

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
ADOPTABLE: frozenset[Readability] = frozenset({Readability.READABLE})
```

New text:

```
ADOPTABLE: frozenset[Readability] = frozenset(
    {Readability.READABLE, Readability.ONLINE_ONLY}
)
```

### `X7_classify_accepts_the_fallback_tier`

An unrecognised genre is routed in bulk by the router's fallback

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_fallback_tier_is_never_accepted_as_an_adoption_answer`

Old text:

```
    if resolution.match is routing.Match.FALLBACK:
        return Disposition.NEEDS_GENRE, "", str(resolution.match)

```

New text:

```
(empty)
```

### `X8_classify_drops_the_too_coarse_test`

A generic genre is routed rather than asked about

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_genre_the_taxonomy_calls_too_coarse_gets_a_disposition`

Old text:

```
    if not value or declared.is_too_coarse_as_source(value):
```

New text:

```
    if not value:
```

### `X9_outstanding_returns_everything`

A resume re-applies every entry from the top

- File: `src/cratekit/adopt/apply.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one`
  - `tests/test_adoption.py::test_a_second_run_over_a_finished_plan_writes_nothing`

Old text:

```
    return tuple(entry for entry in plan.applicable() if entry.entry_id not in done)
```

New text:

```
    return tuple(plan.applicable())
```

### `X10_entry_id_drops_the_sub`

Two pieces of work differing only by sub-folder share one identifier

- File: `src/cratekit/adopt/plan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.plan
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_entry_identifier_moves_when_the_destination_moves`

Old text:

```
            {"tree": tree, "content": content_id, "bucket": bucket, "sub": sub}
```

New text:

```
            {"tree": tree, "content": content_id, "bucket": bucket}
```

### `X11_restore_writes_absence_as_empty`

An absent field is restored as an empty string rather than removed

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 3797 against a baseline of 3797
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if original is None:
        return tags.clear_tags(path, [tag_field])
    return tags.write_tag_values(path, tag_field, original)
```

New text:

```
    return tags.write_tag_values(path, tag_field, original or ())
```

### `X12_look_at_drops_the_regular_file_test`

A directory or a fifo at the recorded path reaches the hash

- File: `src/cratekit/adopt/revert.py`
- Surface: user
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason`
  - `tests/test_adoption.py::test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever`

Old text:

```
    if not stat_module.S_ISREG(info.st_mode):
        return _Looked(ByteRead.NOT_A_REGULAR_FILE)

```

New text:

```
(empty)
```

### `X13_look_at_drops_the_recorded_size_shortcut`

The prefetch reads a file whose size already rules the record out

- File: `src/cratekit/adopt/revert.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.revert
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_file_of_a_DIFFERENT_SIZE_is_refused_without_reading_it`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)

```

New text:

```
(empty)
```

### `X14_probe_drops_the_dataless_test`

A cloud-evicted file is probed by reading it, so the census downloads

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_online_only_file_is_never_opened_by_the_probe`

Old text:

```
    if _is_dataless(info):
        return Readability.ONLINE_ONLY

```

New text:

```
(empty)
```

### `X15_save_drops_the_id3v1_trailer`

A tag write destroys an mp3's legacy ID3v1 trailer

- File: `src/cratekit/core/tags.py`
- Surface: user
- Subset: test files importing cratekit.core.tags
- Ran: `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 778 against a baseline of 778
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert[.mp3]`

Old text:

```
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)

```

New text:

```
    handle.save()

```

