# Mutation table: u304-replay-after-p2h

Measured by `scripts/mutate.py` on 2026-11-23 04:34 UTC, branch `HEAD` at `fd78d188`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22911 collected. pytest invocations for this batch: 15.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 5, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/cc6c934b-9743-5b0a-bc60-d462f78fd3d6/scratchpad/u304-replay-after-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22911 against 22911. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1446.S1_u234_settled_reorder_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 10 | killed |
| `u198.C12_archive_move` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 3 | killed |
| `u208.M10_here_database_only` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u231.M11_snapshot_from_the_order_sent` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 15 | killed |
| `u231.M13_settle_sleeps_the_whole_window` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `u231.M17_agreement_gap_ignored` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 1 | killed |
| `u234.O10_after_not_compared` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O9_after_without_the_window` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |

## Row definitions

### `r1446.S1_u234_settled_reorder_never_leads`

sample, U234: a reorder settled readings show never leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S1_u234_settled_reorder_never_leads`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return False
```

### `u198.C12_archive_move`

plan: a made pair moved under a skipped folder keeps syncing

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C12_archive_move`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py; the line also stands in favorites/order.py, another package's own guard, so rows --after would not choose
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[favorites]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[foreign]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_archive_is_let_go_and_never_written_again`

Old text:

```
                if moved:
```

New text:

```
                if False:
```

### `u208.M10_here_database_only`

here: read only the database ISRC, never the row's file

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M10_here_database_only`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; file_identity is read through pair_read, its home since the split
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
            if code is None:
                code = match.isrc_token(row.isrc) or pair_read.file_identity(cfg, row.path)[0]
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

New text:

```
            if code is None:
                code = match.isrc_token(row.isrc)
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

### `u231.M11_snapshot_from_the_order_sent`

write: the order as sent is recorded as the snapshot, with no settle reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M11_snapshot_from_the_order_sent`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_settle_reading_refused_for_another_reason_stops_the_write`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_at_once_finishes_in_the_one_run`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        done.settle = Settle(
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
        )
        return None
```

New text:

```
        return sent
```

### `u231.M13_settle_sleeps_the_whole_window`

settle: the whole window is waited, the time spent on other pairs' writes not counted

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M13_settle_sleeps_the_whole_window`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS
```

### `u231.M17_agreement_gap_ignored`

plan: a reading equal to the one kept agrees however soon after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M17_agreement_gap_ignored`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept
```

### `u234.O10_after_not_compared`

the order after a settled one leads whatever the reading now, so an order that moved again leads unsettled

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O10_after_not_compared`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
        and not pair_stopped.reordered(kept.after, reading)
        and pair_model._now() - since
```

New text:

```
        and pair_model._now() - since
```

### `u234.O9_after_without_the_window`

the order after a settled one leads on its next reading however soon

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O9_after_without_the_window`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
    ):
        return True
```

