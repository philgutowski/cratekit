# Mutation table: u40-author-full

Measured by `scripts/mutate.py` on 2026-08-26 15:13 UTC, branch `unit/u40-genre-retag-for-mis-tagged-arrivals` at `aea668e`. Pass kind: full.

Baseline: green, 6314 collected. pytest invocations for this batch: 65.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6314 against 6314. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `N0_null_control` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6314 | 0 (promoted) | zero |
| `S1_blank_selected` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `S2_specific_selected` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 15 | killed |
| `S3_unsorted_walk` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `S4_missing_folder` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 6314 | 0 (promoted) | zero |
| `S5_no_strip` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 6314 | 0 (promoted) | zero |
| `S6_plan_drops_current` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `P1_rejected_reasked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `P2_verdict_ignored` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `P3_coarse_answer_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `P4_decline_not_queued` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `P5_verdict_not_checked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 6314 | 0 (promoted) | zero |
| `P6_option_id_as_genre` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 2 | killed |
| `P7_coarse_offered` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `P8_identity_key` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6314 | 0 (promoted) | zero |
| `P9_settled_counted_as_asked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `P10_resolved_not_read` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 4 | killed |
| `D1_plan_from_selection` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 6314 | 0 (promoted) | zero |
| `D2_ambiguous_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `D3_zip_not_strict` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6314 | 0 (promoted) | zero |
| `D4_absent_row_silent` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `D5_no_enable` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 4 | killed |
| `D6_no_policy_assert` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `D7_unmatched_dropped` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 3 | killed |
| `D8_contested_last_wins` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `D9_contested_first_still_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 36 | 1 | killed |
| `F1_resolve_takes_first_row` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 69 | 3 | killed |
| `F2_genre_unknown_silent` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 69 | 2 | killed |
| `F3_policy_owns_more` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 69 | 2 | killed |
| `F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 695 | 3 | killed |
| `C1_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 583 | 1 | killed |
| `C2_no_gate_no_refusal` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 583 | 1 | killed |
| `C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 52 | 3 | killed |
| `C4_resume_always_runs` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 52 | 1 | killed |
| `C5_abort_queues` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 6314 | 1 (promoted) | killed |
| `C6_constant_digest` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 6314 | 0 (promoted) | zero |
| `C7_gate_run_under_intake_name` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 52 | 2 | killed |
| `C8_empty_folder_accepted` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 6314 | 1 (promoted) | killed |
| `R1_gate_not_explicit` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 0 | 0 | refused |
| `R3_ungated` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 531 | 1 | killed |
| `R4_no_db_surface` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 531 | 1 | killed |
| `R5_row_unclaimed` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 539 | 3 | killed |
| `R6_row_still_cut` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 539 | 2 | killed |
| `R7_not_destructive` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 0 | collection error | collect-error |
| `R8_not_long_running` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 544 | collection error | collect-error |

## Zero rows and what they owe

- `N0_null_control` (maintainer facing): maintainer facing, composite not required
- `S4_missing_folder` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S5_no_strip` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P5_verdict_not_checked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P8_identity_key` (maintainer facing): maintainer facing, composite not required
- `D1_plan_from_selection` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D3_zip_not_strict` (maintainer facing): maintainer facing, composite not required
- `C6_constant_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `R2_no_digest_source`: Declare no digest source on the confirm gate, so the decision is made against no artifact and cannot go stale Dropped because: dropped to stay at the 45 row cap. C1 already mutates the handler's own search for the gate declared against the plan, which is the code that reads this field, and R1 measures the same declaration's other half. This row would have measured the registry's contract suite rather than this round's code.
- `P9_handler_key_dropped`: Offer a review item with no handler key, so the queue cannot say which verb asked Dropped because: dropped to stay at the 45 row cap, and ranked below every row above it because the cost is maintainer facing: a person reading the queue loses the provenance column and every decision still lands correctly. P9 was reassigned to the settled-versus-asked row, which has a user facing cost.
- `X1_every_other_bucket_field`: Mutate each remaining Bucket field the offer does not read Dropped because: ranked below the cap: options_for reads id and display only, and P6 and P7 already measure both. The other fields are not on this unit's path at all.
- `X2_doctor_checks`: Change the declared doctor checks on the new entry Dropped because: ranked below the cap: the checks are a declaration this unit copies from repair.paths, which writes the same surface. Nothing in this round's code reads them, so a row here measures the contract suite rather than the round.
- `X3_review_offer_idempotence`: Break review.offer's already-present branch Dropped because: ranked below the cap: U11's own suite owns that function and this unit is not its first caller, four modules in src already offer into the queue. F1 to F4 spend the first-caller sample where this unit IS first, which is write.metadata and the row index.

## Row definitions

### `N0_null_control`

A comment reworded and nothing else. Must kill zero, or the baseline is red and every death below is noise.

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
LAYER: modules.
```

New text:

```
LAYER: modules layer.
```

### `S1_blank_selected`

Drop the blank-genre exclusion, so a file with no genre becomes this verb's candidate as well as tag.folder's

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_with_no_genre_is_passed_over_rather_than_selected`
  - `tests/test_genre_retag.py::test_a_second_run_over_a_corrected_folder_selects_nothing`

Old text:

```
        if not current:
            # tag.folder's, under fill-if-empty. See the module docstring.
            passed.append(Passed(path=path, reason=NO_GENRE))
            continue

```

New text:

```
(empty)
```

### `S2_specific_selected`

Invert the too-coarse predicate, so a curated genre is selected and a catch-all is not

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 15 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_catch_all_gets_a_specific_answer_and_the_taxonomy_recognises_it`
  - `tests/test_genre_retag.py::test_a_declared_catch_all_is_selected_and_a_specific_genre_is_not`
  - `tests/test_genre_retag.py::test_a_declined_answer_lands_in_the_review_queue`
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_pass_with_no_store_reports_what_it_could_not_settle`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_a_second_run_offers_one_item_rather_than_a_second`
  - `tests/test_genre_retag.py::test_a_second_run_over_a_corrected_folder_selects_nothing`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`
  - `tests/test_genre_retag.py::test_the_item_id_this_pass_computes_is_the_one_the_queue_stores`
  - `tests/test_genre_retag.py::test_the_plan_carries_the_current_value_so_the_person_sees_what_is_being_replaced`
  - `tests/test_genre_retag.py::test_the_plan_digest_changes_when_the_selection_changes`
  - `tests/test_genre_retag.py::test_the_selection_is_sorted_so_one_unchanged_folder_digests_the_same_twice`

Old text:

```
        if not declared.is_too_coarse_as_source(current):
```

New text:

```
        if declared.is_too_coarse_as_source(current):
```

### `S3_unsorted_walk`

Walk the folder unsorted, so the plan digest depends on directory order

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_selection_is_sorted_so_one_unchanged_folder_digests_the_same_twice`

Old text:

```
    for path in sorted(root.rglob("*")):
```

New text:

```
    for path in root.rglob("*"):
```

### `S4_missing_folder`

Remove the not-a-directory guard, so an absent folder raises instead of selecting nothing

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not root.is_dir():
        return Selection()

```

New text:

```
(empty)
```

### `S5_no_strip`

Stop stripping the genre read off the file, so a padded catch-all fails the predicate

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        current = (tags.read_genre_from_file(path) or "").strip()
```

New text:

```
        current = tags.read_genre_from_file(path) or ""
```

### `S6_plan_drops_current`

Drop the current value from the plan row, so the person confirms a list of paths with nothing to judge

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_plan_carries_the_current_value_so_the_person_sees_what_is_being_replaced`

Old text:

```
        {"path": str(candidate.path), "current": candidate.current}
```

New text:

```
        {"path": str(candidate.path)}
```

### `P1_rejected_reasked`

Drop the suppressed branch, so an item a person settled AGAINST is looked up and written anyway

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`

Old text:

```
            if item.suppressed:
                results.append(
                    RetagResult(
                        path=candidate.path,
                        current=candidate.current,
                        reason=DECLINED_IN_REVIEW,
                        item_id=item_id,
                    )
                )
                continue

```

New text:

```
(empty)
```

### `P2_verdict_ignored`

Never read the recorded verdict, so every run re-asks the searcher a question a person answered

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`

Old text:

```
            answer = accepted_genre(item)
```

New text:

```
            answer = ""
```

### `P3_coarse_answer_written`

Drop the refusal, so a lookup that returns another catch-all launders it onto the file

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`

Old text:

```
        if declared.is_too_coarse_as_source(answer):
            results.append(
                _ask(
                    store,
                    candidate,
                    reason=ANSWER_TOO_COARSE,
                    proposed=answer,
                    declared=declared,
                    handler_key=handler_key,
                )
            )
            continue

```

New text:

```
(empty)
```

### `P4_decline_not_queued`

Drop the decline branch, so a searcher that answered nothing writes an empty genre instead of asking

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_declined_answer_lands_in_the_review_queue`
  - `tests/test_genre_retag.py::test_a_pass_with_no_store_reports_what_it_could_not_settle`

Old text:

```
        if not answer:
            results.append(
                _ask(
                    store,
                    candidate,
                    reason=NO_ANSWER,
                    proposed="",
                    declared=declared,
                    handler_key=handler_key,
                )
            )
            continue

```

New text:

```
(empty)
```

### `P5_verdict_not_checked`

Accept a REJECTED item's option as an answer, so a rejection reads as an acceptance

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if item.verdict is not review.Verdict.ACCEPTED or not item.option:
```

New text:

```
    if not item.option:
```

### `P6_option_id_as_genre`

Return the bucket identifier rather than its display name, so the tag written is an id

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`

Old text:

```
        detail = option.detail or {}
        return str(detail.get("genre") or option.summary or "").strip()
```

New text:

```
        return str(option.option_id).strip()
```

### `P7_coarse_offered`

Offer every bucket including the fallback, so a person can choose the catch-all the write then refuses

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_offered_candidates_are_the_declared_buckets_and_never_a_catch_all`

Old text:

```
        if not declared.is_too_coarse_as_source(bucket.display)
```

New text:

```
        if bucket.display
```

### `P8_identity_key`

Address a review item by a different key, so every item already in the queue is orphaned

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return {"path": str(path)}
```

New text:

```
    return {"file": str(path)}
```

### `P9_settled_counted_as_asked`

Count any result carrying an item id as an open question, so a decision a person already made is reported back to them as work waiting

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`

Old text:

```
            if result.item_id and result.reason in {NO_ANSWER, ANSWER_TOO_COARSE}
```

New text:

```
            if result.item_id and not result.written
```

### `P10_resolved_not_read`

Read only unresolved items out of the queue, so a settled verdict is invisible and re-asked

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`

Old text:

```
        for item in review.iter_items(store, predicate=predicate, include_resolved=True)
```

New text:

```
        for item in review.iter_items(store, predicate=predicate)
```

### `D1_plan_from_selection`

Plan from every result rather than from what was written, so a refused file's row is retagged anyway

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    written = outcome.written
```

New text:

```
    written = outcome.results
```

### `D2_ambiguous_written`

Take the first of two live rows on one location instead of surfacing the collision

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both`

Old text:

```
        if match.outcome is not trees.MatchOutcome.MATCHED or match.content_id is None:
```

New text:

```
        if match.content_id is None and not match.content_ids:
```

### `D3_zip_not_strict`

Drop strict from the zip pairing results with matches, so a length mismatch silently truncates

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for result, match in zip(written, matches, strict=True):
```

New text:

```
    for result, match in zip(written, matches):
```

### `D4_absent_row_silent`

Drop the row-absent skips, so a matched row the caller did not supply vanishes from the plan

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_matched_row_the_caller_did_not_supply_is_surfaced_rather_than_silent`

Old text:

```
    if absent:
        plan = metadata.Plan(
            plan.owner,
            plan.changes,
            plan.skipped + tuple(metadata.Skipped(cid, "row-absent") for cid in absent),
        )

```

New text:

```
(empty)
```

### `D5_no_enable`

Do not register the operation, so every change decides SKIP_UNOWNED and the sweep reports a clean run over a library it did not touch

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`

Old text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
```

New text:

```
    metadata.assert_within_policy(library_plan.plan)
```

### `D6_no_policy_assert`

Drop the policy refusal, so a plan naming an unowned field writes nothing and reports success

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_apply_refuses_a_field_the_retag_policy_does_not_own`

Old text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
    return metadata.write_plan(library_plan.plan, mapped)
```

New text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    return metadata.write_plan(library_plan.plan, mapped)
```

### `D7_unmatched_dropped`

Do not surface a written file no row claims, so a half-applied sweep reports as a full one

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_genre_retag.py::test_a_written_file_no_live_row_claims_is_surfaced_rather_than_dropped`
  - `tests/test_genre_retag.py::test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both`

Old text:

```
            unmatched.append(
                Unmatched(
                    path=str(result.path),
                    outcome=str(match.outcome.value),
                    content_ids=tuple(match.content_ids),
                )
            )
            continue
```

New text:

```
            continue
```

### `D8_contested_last_wins`

Let a second file claiming one row overwrite the first, so whichever came last decides the row and the report names both as written

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins`

Old text:

```
        if content_id in claimed_by:
            contested.add(content_id)
            unmatched.append(
                Unmatched(path=str(result.path), outcome="contested", content_ids=(content_id,))
            )
            continue

```

New text:

```
(empty)
```

### `D9_contested_first_still_written`

Remove only the second layer, so the second claimant is surfaced and the FIRST one is still written to the contested row

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins`

Old text:

```
    for content_id in sorted(contested):
        genres.pop(content_id, None)
        unmatched.append(
            Unmatched(path=claimed_by[content_id], outcome="contested", content_ids=(content_id,))
        )

```

New text:

```
(empty)
```

### `F1_resolve_takes_first_row`

First caller sample: take the first genre row rather than the first ACTIVE one, so a soft-deleted namesake masks a live genre

- File: `src/cratekit/write/metadata.py`
- Surface: user
- Subset: test files importing cratekit.write.metadata
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 69 against a baseline of 69
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
    for row in db.get_genre(Name=genre_name):
        if not getattr(row, "rb_local_deleted", 0):
            return row.ID
    return None
```

New text:

```
    for row in db.get_genre(Name=genre_name):
        return row.ID
    return None
```

### `F2_genre_unknown_silent`

First caller sample: drop the genre-unknown skip, so an unresolvable answer disappears from the plan

- File: `src/cratekit/write/metadata.py`
- Surface: user
- Subset: test files importing cratekit.write.metadata
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced`
  - `tests/test_metadata_policy.py::test_a_genre_with_no_lookup_row_is_skipped_and_surfaced`

Old text:

```
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

New text:

```
        if genre_id is None:
            continue
```

### `F3_policy_owns_more`

First caller sample: widen the RETAG_GENRE policy to a second column

- File: `src/cratekit/write/metadata.py`
- Surface: user
- Subset: test files importing cratekit.write.metadata
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_apply_refuses_a_field_the_retag_policy_does_not_own`
  - `tests/test_genre_retag.py::test_the_retag_operation_owns_the_genre_column_and_nothing_else`

Old text:

```
            fields=MappingProxyType({"GenreID": rb_writer.Ownership.OWNED}),
```

New text:

```
            fields=MappingProxyType(
                {"GenreID": rb_writer.Ownership.OWNED, "Rating": rb_writer.Ownership.OWNED}
            ),
```

### `F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Surface: user
- Subset: test files importing cratekit.write.trees
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 695 against a baseline of 695
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_tree_writer.py::test_a_soft_deleted_row_beside_one_active_row_resolves_cleanly`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `C1_gate_by_position`

Take gates[0] rather than the gate declared against the plan, so a reordered tuple answers the wrong question

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 583 against a baseline of 583
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates:
        return spec
```

### `C2_no_gate_no_refusal`

Return None instead of refusing when the entry declares no plan gate, so a destructive sweep runs unconfirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 583 against a baseline of 583
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_refuses_when_its_entry_declares_no_plan_gate`

Old text:

```
    raise refuse(
        "refused-by-policy",
        "this verb is destructive and its registry entry declares no decision "
        "made against the plan, so there is nothing for a person to confirm",
        remedy=Remedy.REPORT_DEFECT,
        origin=("tagging", "retag_cli"),
        detail={"verb": ctx.entry.name},
    )
```

New text:

```
    return None
```

### `C3_resume_without_run`

Drop --run from the resume argv, so the job driver's child meets the explicit gate with nothing recorded and stalls for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 52 against a baseline of 52
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run`
  - `tests/test_queued_resume_contract.py::test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against[tag.retag]`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
```

New text:

```
    resume = []
```

### `C4_resume_always_runs`

Emit --run even when no gate run is frozen, so a job from an older build hands its child an empty run identifier

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_a_payload_from_an_older_build_still_builds_a_valid_command_line[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]
```

New text:

```
    return ["--run", str(gate_run), "tag", "retag", folder, "--job", job.job_id]
```

### `C5_abort_queues`

Ignore the abort answer, so a person who declined gets the sweep queued anyway

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 6314 against a baseline of 6314
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    if option == "abort":
```

New text:

```
    if option == "never-chosen":
```

### `C6_constant_digest`

Digest a constant rather than the selection, so a decision approved over forty files also approves a hundred and forty

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 6314 against a baseline of 6314
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "digest": digest_of({"kind": "tag.retag", "folder": folder, "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "tag.retag"}),
```

### `C7_gate_run_under_intake_name`

Freeze the gate run under a locally spelled key, which is the confusion jobs.GATE_RUN_KEY exists to end

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_gate_run_key_is_one_name_and_every_shell_uses_it`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`

Old text:

```
            payload={"folder": folder, jobs.GATE_RUN_KEY: ctx.run.run_id},
```

New text:

```
            payload={"folder": folder, "run_id": ctx.run.run_id},
```

### `C8_empty_folder_accepted`

Drop the empty-folder refusal, so the verb sweeps the current working directory

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 6314 against a baseline of 6314
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_genre_retag.py::test_an_empty_folder_argument_refuses_rather_than_sweeping_the_working_directory`

Old text:

```
    if not folder:
        raise refuse(
            "tag-retag-folder-unknown",
            "tag retag needs the folder whose genres it should correct",
            steps=("pass the folder after the verb",),
            origin=("tagging", "retag_cli"),
        )

```

New text:

```
(empty)
```

### `R1_gate_not_explicit`

Make the confirm gate ordinary, which drops the verb out of the queued-resume guard entirely

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`, `tests/test_genre_retag.py`
- Collected: 0 against a baseline of 583
- Kills: 0 (refused)
- Note: old text appears 6 times in the target, so the site is ambiguous. Widen the old text with surrounding lines until it is unique.

Old text:

```
                explicit=True,
                digest_source="plan",
```

New text:

```
                digest_source="plan",
```

### `R3_ungated`

Drop the module toggle, so a Module row ships on in the slim profile (R5)

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 531 against a baseline of 531
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`

Old text:

```
        module_id="repair",
        argv_builder="retag_argv",
```

New text:

```
        argv_builder="retag_argv",
```

### `R4_no_db_surface`

Stop declaring the database write, so the verb never asks the concurrent-writer question its work raises

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 531 against a baseline of 531
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

Old text:

```
        writes=frozenset({"files", "db_metadata"}),
        adjudicates=True,
```

New text:

```
        writes=frozenset({"files"}),
        adjudicates=True,
```

### `R5_row_unclaimed`

Claim no feature row, so row 18 becomes a Module the product owes and no verb cites

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 539 against a baseline of 539
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cutover_parity.py::test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight`
  - `tests/test_cutover_parity.py::test_the_backlog_is_every_owed_row_without_a_landed_verb`

Old text:

```
        feature_rows=(18,),
```

New text:

```
        feature_rows=(),
```

### `R6_row_still_cut`

Leave row 18 dispositioned Cut while a verb claims it, which is the coupling across two trees

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 539 against a baseline of 539
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cutover_parity.py::test_the_transcribed_dispositions_match_the_plan_when_it_is_reachable`

Old text:

```
    Feature(18, "genre correction for a tag already too coarse", "module"),
```

New text:

```
    Feature(18, "genre correction for a tag already too coarse", "cut"),
```

### `R7_not_destructive`

Declare the verb non-destructive, so the destructive-session gates never bind to it (KTD24)

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 0 against a baseline of 531
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 531. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_cli_contract.py`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="tag.retag.confirm",
```

New text:

```
        destructive=False,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="tag.retag.confirm",
```

### `R8_not_long_running`

Declare the sweep short, so it runs inline in the invocation instead of on the job engine

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 544 against a baseline of 547
- Kills: 0 (collect-error)
- Note: collection changed: 544 collected against a baseline of 547. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.

Old text:

```
        argv_builder="retag_argv",
        long_running=True,
```

New text:

```
        argv_builder="retag_argv",
```

