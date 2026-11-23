# Mutation table: u339-composites

Measured by `scripts/mutate.py` on 2026-11-23 19:26 UTC, branch `cloud/988-give-chosen-tracks-a-genre-over` at `62445fdc`. Pass kind: light.

Baseline: green, 22724 collected. pytest invocations for this batch: 8.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `d25bc0a8e515`, and this tree is at `62445fdc73a9`).

Subset baselines: 2, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22724 against 22724. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M24_discharge_moved` | `src/cratekit/adopt/move_cli.py` | user | 5 file(s) | 223 | 1 | killed |
| `C6_census_tombstone` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 22724 | 49 (promoted) | killed |
| `C20_still_moved_names` | `src/cratekit/adopt/move.py` | user | 5 file(s) | 223 | 1 | killed |

## Row definitions

### `M24_discharge_moved`

handle: an entry is spent though the track was not read back moved

- File: `src/cratekit/adopt/move_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_workers.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_move_stopped_before_its_removal_keeps_its_entry_and_a_resume_finishes`

Old text:

```
        if move.target_bucket and move.content_id in found["moved"]:
```

New text:

```
        if move.target_bucket:
```

### `C6_census_tombstone`

scan_rows: a tombstoned row is read as live by the census, the layer M6_tombstone_row's guard sits on (its composite)

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 22724 against a baseline of 22724
- Kills: 49 (killed)
- Promoted: subset killed 0, full suite killed 49
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
  - `tests/test_tag_backlog.py::test_a_catch_all_is_left_to_tag_retag`
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes`
  - `tests/test_tag_backlog.py::test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal`
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_only_a_row_with_no_genre_is_asked_of_the_catalogue`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        if row.deleted:
            continue
```

New text:

```
(empty)
```

### `C20_still_moved_names`

still_moved: a bucket the track's genre names again stays in the moves, the layer M20_moved_back_names's guard sits behind (its composite)

- File: `src/cratekit/adopt/move.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_workers.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_bucket_any_entry_of_the_track_claims_is_never_left`

Old text:

```
        held -= {bucket for bucket in held if genre_names(entry, bucket, declared)}

```

New text:

```
(empty)
```

