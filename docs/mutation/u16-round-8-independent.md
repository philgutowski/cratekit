# Mutation table: u16-round-8-independent

Measured by `scripts/mutate.py` on 2026-08-13 23:11 UTC, branch `unit/u16-three-state-match-and-missing-review` at `3262bc8`. Pass kind: light.

Baseline: green, 3512 collected. pytest invocations for this batch: 26.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3512 against 3512. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `V1_key_check_first_copy_only` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 2 | killed |
| `V3_version_differs_silently_joins` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 24 | killed |
| `V4_fuzzy_becomes_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 9 | killed |
| `V5_ambiguous_reading_promoted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 28 | killed |
| `V6_reading_question_never_asked` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 28 | killed |
| `V7_tombstoned_counted_missing` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 23 | killed |
| `V8_missing_without_options` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 4 | killed |
| `V9_relative_key_by_letter` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 8 | killed |
| `V10_candidate_key_grouping_dropped` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 5 | killed |
| `V11_candidate_order_sorted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 1 | killed |
| `V12_approximate_floor_halved` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 2 | killed |
| `V13_withheld_not_reported` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 2 | killed |
| `V14_tombstone_fold_nfd` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 3 | killed |
| `V15_empty_identity_accepted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 1 | killed |
| `V16_key_leaves_item_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 3 | killed |
| `V17_asks_leaves_item_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 10 | killed |
| `V18_rejection_skips_tombstones` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 2 | killed |
| `V19_unbound_yes_takes_todays_candidate` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 2 | killed |
| `V20_digest_width_halved` | `src/cratekit/acquire/match.py` | maintainer | 1 file(s) | 330 | 3 | killed |
| `V21_suppression_asked_one_spelling` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 9 | killed |
| `V22_suppressed_warning_omitted` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 330 | 20 | killed |
| `V23_suppressed_message_reworded` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 3512 | 0 (promoted) | zero |

## Zero rows and what they owe

- `V23_suppressed_message_reworded` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `D1_relative_loses_reporting`: The why choice when duplicate exact copies produce both disagreement kinds picks KEY_DIFFERS over KEY_RELATIVE Dropped because: ranked below the cap: fires only when duplicate exact copies disagree two ways at once; V9 measures the relative boundary itself and V1 measures the duplicate-copy seam
- `D2_approximate_limit_raised`: APPROXIMATE_LIMIT 5 to 10 Dropped because: ranked below the cap: same coefficient family as V12, and V13 measures the truncation reporting seam directly
- `D3_key_absence_flip`: key_disagreement absence guard, or flipped to and Dropped because: ranked below the cap: the flip crashes parse_camelot on the common keyless path rather than misclassifying, so it measures reachability of keyless rows rather than the boundary; V9 covers the same function
- `D4_offered_length_gate`: apply_verdict binds an unspecific yes when several options were offered, offered[0] if offered Dropped because: ranked below the cap: same identity-binding family as V19, which mutates the binding equality itself
- `D5_payload_states_widened`: PAYLOAD_STATES gains SUPPRESSED, widening the envelope to four arrays Dropped because: ranked below the cap: the suppression channel is measured from both sides by V7 and V22
- `D6_held_exactly_any_version`: _held_exactly bar lowered from exact version to any version of the head Dropped because: ranked below the cap: same reading-question family as V5 and V6
- `D7_reader_normalization`: read_tidal_tracks, read_spotify_items, read_text_lines identical-results rows (R13) Dropped because: ranked below the cap: upstream of the three state boundaries this light pass is scoped to
- `D8_missing_writes_a_file`: adjudicate passes missing through untouched, no file written (R12) Dropped because: not mutable: the behavior is the absence of file-writing code; there is no guard text to revert
- `D9_candidate_key_first_spelling`: Candidate displays the first file's key spelling instead of the folded grouping key Dropped because: ranked below the cap: same grouping family as V10
- `D10_identity_refusal_reworded`: version_identity refusal message reworded Dropped because: ranked below the cap: one message row per pass, and V23 already rewords a message on the R36 surface; V15 measures the same guard's presence

## Row definitions

### `V1_key_check_first_copy_only`

Exact branch reads only the first held copy's key, so an unkeyed copy that sorts first answers the key question for a keyed one

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}

```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}

```

### `V3_version_differs_silently_joins`

A recording owned only at another version resolves MATCHED instead of needs review, the silent join R11 forbids

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 24 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_question_answered_from_one_source_is_never_asked_again_from_another`
  - `tests/test_match_states.py::test_a_rejected_question_makes_the_track_missing_rather_than_matched`
  - `tests/test_match_states.py::test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get`
  - `tests/test_match_states.py::test_a_run_blocked_by_an_unapplicable_verdict_names_the_verb_that_can_act`
  - `tests/test_match_states.py::test_a_run_over_an_answered_question_reports_matched_and_writes_nothing`
  - `tests/test_match_states.py::test_a_tombstone_does_not_pre_empt_a_question_about_a_version_the_library_holds`
  - `tests/test_match_states.py::test_a_track_owned_only_as_a_different_remix_needs_review_and_names_the_difference`
  - `tests/test_match_states.py::test_a_verdict_this_build_cannot_read_leaves_the_item_answerable`
  - `tests/test_match_states.py::test_a_verdict_travels_between_two_machines_that_hold_different_versions`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_a_version_question_becomes_an_addressable_item_with_its_candidates`
  - `tests/test_match_states.py::test_an_acceptance_naming_no_candidate_is_applied_only_when_there_is_one`
  - `tests/test_match_states.py::test_an_accepted_candidate_that_has_since_gone_is_not_reported_matched`
  - ... and 9 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.VERSION_DIFFERS,

```

### `V4_fuzzy_becomes_identity`

An approximate title hit resolves MATCHED, making a discovery heuristic an identity

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it[David Bowie - Ziggy Stardust - Reprise-David Bowie - Ziggy Stardust-Ziggy Stardust - Reprise]`
  - `tests/test_match_states.py::test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it[Nova Reef - Nice Up - Dub-Nova Reef - Nice Up-Nice Up - Dub]`
  - `tests/test_match_states.py::test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it[The Beatles - Sgt Peppers - Reprise-The Beatles - Sgt Peppers-Sgt Peppers - Reprise]`
  - `tests/test_match_states.py::test_an_approximate_hit_is_a_question_and_never_a_match`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`
  - `tests/test_match_states.py::test_two_approximate_recordings_with_no_qualifier_stay_two_candidates`

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.TITLE_APPROXIMATE,

```

### `V5_ambiguous_reading_promoted`

The other-reading question resolves MATCHED, reporting ownership of a record nobody checked

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.READING_AMBIGUOUS,

```

### `V6_reading_question_never_asked`

The other-reading guard layer removed alone: the question is never asked and the row falls through to approximate or missing

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    confirming = _other_reading_the_library_holds(wanted, index)

```

New text:

```
    confirming = None

```

### `V7_tombstoned_counted_missing`

Resolution never consults the tombstones, so a suppressed version reports MISSING with acquisition options and the deletion is undone (R36)

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 23 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_suppressed_track_is_in_none_of_the_three_arrays`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path - Nightwave Remix]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path [Nightwave Remix]]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path]`
  - `tests/test_match_states.py::test_a_tombstone_still_suppresses_when_the_library_can_say_nothing`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )

```

New text:

```
    standing = None

```

### `V8_missing_without_options`

A missing row carries no acquisition options, so the review queue item has nothing to offer (R12)

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[ambiguous-dash]`
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it`

Old text:

```
        acquisitions=acquisition_options(wanted),

```

New text:

```
        acquisitions=(),

```

### `V9_relative_key_by_letter`

Relative major or minor detected by matching letter instead of matching wheel number, so 8A vs 8B reads as outright disagreement and 8A vs 9A as relative

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 8 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_relative_key_disagreement_surfaces_rather_than_picking_one`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-last]`

Old text:

```
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS

```

New text:

```
    return Why.KEY_RELATIVE if left[1] == right[1] else Why.KEY_DIFFERS

```

### `V10_candidate_key_grouping_dropped`

Candidates group without the key, so a person shown one key accepts paths at other keys

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_an_ungated_question_still_gates_once_its_verdict_cannot_be_applied`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`

Old text:

```
        grouped.setdefault((held.recording, held.version_key, held.key_key), []).append(held)

```

New text:

```
        grouped.setdefault((held.recording, held.version_key, ""), []).append(held)

```

### `V11_candidate_order_sorted`

Candidate groups iterate sorted instead of insertion order, so the approximate offer truncates the best hit instead of the worst

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
    for recording, version_key, key in grouped:

```

New text:

```
    for recording, version_key, key in sorted(grouped):

```

### `V12_approximate_floor_halved`

APPROXIMATE_FLOOR coefficient halved from 82 to 41, admitting resemblances the unit exists to keep out of the offer

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 41

```

### `V13_withheld_not_reported`

The truncated approximate offer stops saying how many candidates were withheld, so a rejection rejects answers never shown

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`

Old text:

```
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),

```

New text:

```
            withheld=0,

```

### `V14_tombstone_fold_nfd`

tombstone_fold normalizes NFD instead of NFC, drifting from U24's byte-for-byte algorithm so a recorded suppression can never be found

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_composed_address_still_matches_a_row_spelled_that_way[Caf\xe9 del Mar-Track-Live]`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Caf\xe9 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Cafe\u0301 del Mar'-'caf\xe9 del mar']`

Old text:

```
        " ", unicodedata.normalize("NFC", str(value)).casefold()

```

New text:

```
        " ", unicodedata.normalize("NFD", str(value)).casefold()

```

### `V15_empty_identity_accepted`

The empty tombstone identity refusal removed alone, so every unnamed candidate collides onto one suppression

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_identity_with_neither_an_artist_nor_a_title_is_refused`

Old text:

```
    if not folded_artist and not folded_title:

```

New text:

```
    if False:

```

### `V16_key_leaves_item_identity`

The list's key leaves the review item identity, so one answer settles the key question and the version question both

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_review_item_identity_is_not_the_tombstone_identity`

Old text:

```
        "key": key_token(key),

```

New text:

```
        "key": "",

```

### `V17_asks_leaves_item_identity`

The asks field collapses to one constant, so a key question and a version question about one recording are one item again

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_and_a_version_question_are_two_items_on_one_line`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[candidate-gone]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[exact]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[not-in-library]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[tombstoned]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[verdict-accepted]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[verdict-rejected]`
  - `tests/test_match_states.py::test_a_row_that_is_not_a_question_has_no_review_item_identity[verdict-unspecific]`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`

Old text:

```
        "asks": question_shape(why),

```

New text:

```
        "asks": ASKS_ABOUT_VERSION,

```

### `V18_rejection_skips_tombstones`

A rejection stops consulting the tombstones, so a rejected question hands acquisition a version standing under a tombstone (R36)

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition`
  - `tests/test_match_states.py::test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`

Old text:

```
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )

```

New text:

```
        standing = None

```

### `V19_unbound_yes_takes_todays_candidate`

An unspecific yes stops being bound to the candidate it was given about and accepts whatever the library holds today

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`

Old text:

```
            chosen = [c for c in found.candidates if c.candidate_id == about]

```

New text:

```
            chosen = list(found.candidates)

```

### `V20_digest_width_halved`

DIGEST_WIDTH coefficient halved from 16 to 8 hex characters, dropping identifier collision resistance from 64 to 32 bits

- File: `src/cratekit/acquire/match.py`
- Surface: maintainer
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_declared_width_survives_a_population_a_narrower_one_does_not`
  - `tests/test_match_states.py::test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement`

Old text:

```
DIGEST_WIDTH = 16

```

New text:

```
DIGEST_WIDTH = 8

```

### `V21_suppression_asked_one_spelling`

The tombstone store is asked under one spelling instead of every spelling a version could be recorded under, re-acquiring deletions recorded from another spelling

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path - nightwave remix]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path [nightwave remix]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path [Original Version]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path-Sun Path (Original Mix)]`

Old text:

```
    for identity in wanted.suppression_spellings:

```

New text:

```
    for identity in (wanted.identity,):

```

### `V22_suppressed_warning_omitted`

The suppressed rows stop being reported on the warning channel, so a suppression is omitted silently (R36)

- File: `src/cratekit/acquire/match_cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match_cli
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 20 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path - Nightwave Remix]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path [Nightwave Remix]]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path]`
  - `tests/test_match_states.py::test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition`
  - `tests/test_match_states.py::test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    for track in result.suppressed:

```

New text:

```
    for track in ():

```

### `V23_suppressed_message_reworded`

The suppression warning message reworded, not appended, to check the sentence is pinned rather than a substring

- File: `src/cratekit/acquire/match_cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match_cli
- Ran: `tests/test_match_states.py`
- Collected: 3512 against a baseline of 3512
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    f"{track.wanted.artist} / {track.wanted.title} is suppressed by "
                    f"a tombstone and was not counted missing"

```

New text:

```
                    f"{track.wanted.artist} / {track.wanted.title} was skipped "
                    f"because a tombstone stands over it"

```

