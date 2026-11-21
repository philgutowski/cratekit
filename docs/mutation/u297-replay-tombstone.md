# Mutation table: u297-replay-tombstone

Measured by `scripts/mutate.py` on 2026-11-21 15:21 UTC, branch `cloud/854-one-command-replays-the-recorded` at `1b3010b7`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 21638 collected. pytest invocations for this batch: 5.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 1, each measured by this driver.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/e430c5e9-2857-5af3-b23c-47770527940b/scratchpad/known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 21638 against 21638. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1270 | 21 | killed |
| `r431-a.A2_one_kind_for_both` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1270 | 17 | killed |

## Row definitions

### `r431-a.A1_a_plain_row_gains_a_companion`

uncredited_title answers the stripped title even when nothing was stripped, so a plain deletion writes a companion

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A1_a_plain_row_gains_a_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1270 against a baseline of 1270
- Kills: 21 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently`
  - `tests/test_deletion.py::test_a_listing_says_which_suppressions_moved_no_file`
  - `tests/test_deletion.py::test_a_run_interrupted_after_trashing_resumes_without_re_offering`
  - `tests/test_deletion.py::test_a_tombstone_that_cannot_be_written_puts_the_file_back`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[ctrl-c]`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[sigterm]`
  - `tests/test_deletion.py::test_one_file_deleted_by_hand_under_a_healthy_anchor_is_still_settled`
  - `tests/test_deletion.py::test_the_listing_carries_the_column_value_a_missed_tombstone_was_built_from`
  - `tests/test_deletion.py::test_tombstone_list_revokes_and_then_shows_the_lifted_record`
  - `tests/test_deletion.py::test_tombstone_list_shows_what_the_deletion_pass_suppressed`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_writes_no_companion`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_tombstones.py::test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return stripped if dropped else ""
```

New text:

```
    return stripped
```

### `r431-a.A2_one_kind_for_both`

The companion is recorded under the tombstone's own kind, where every verbatim lookup lands on it

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A2_one_kind_for_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1270 against a baseline of 1270
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_never_the_answer_to_a_verbatim_lookup`
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_companion_never_says_a_run_recorded_a_different_rows_deletion`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_deleting_again_after_a_full_lift_suppresses_both_halves_again`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_plain_tombstone_touches_no_companion_it_does_not_own`
  - `tests/test_uncredited_tombstone.py::test_lifting_the_companion_alone_leaves_the_tombstone_standing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
KIND_VERSION_UNCREDITED = "version-uncredited"
```

New text:

```
KIND_VERSION_UNCREDITED = "version"
```

