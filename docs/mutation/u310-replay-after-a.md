# Mutation table: u310-replay-after-a

Measured by `scripts/mutate.py` on 2026-11-23 00:33 UTC, branch `HEAD` at `3ab6abf3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22849 collected. pytest invocations for this batch: 104.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 16, each measured by this driver.

Known failures: 254 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/sp/known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22849 against 22849. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u23-round-8-independent.X9_outstanding_returns_everything` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 615 | 2 | killed |
| `u254-m08.M08_never_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M01_mark_validates_record` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 4 | killed |
| `u254.M02_cache_identity_ignored` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 5 | killed |
| `u254.M03_cache_identity_no_size` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M04_cache_identity_no_mtime` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 743 | 1 | killed |
| `u254.M05_cache_identity_no_inode` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 743 | 1 | killed |
| `u254.M06_never_cache` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 743 | 1 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 86 | killed |
| `u254.M09_any_line_torn` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 2 | killed |
| `u254.M10_torn_needs_terminated_tail` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M11_unterminated_tail_whole` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 23 | killed |
| `u254.M12_header_upgrade` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M13_header_older_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M14_header_unterminated` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M15_header_string_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M16_journal_needs_format` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M17_document_at_journal_schema` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M18_remark_first_wins` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M19_already_inverted` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 33 | killed |
| `u254.M21_record_needs_actor` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 3 | killed |
| `r235-b.M25_adoption_refusal_names_no_verb` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `r788-d.A2_vocal_rows_never_written` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-d.A3_present_rows_handed_over` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 161 | 2 | killed |
| `u132.W1_every_apply` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 446 | 1 | killed |
| `u132.W2_coded_note` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 446 | 3 | killed |
| `u132.W3_version_from_report` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 446 | 1 | killed |
| `u165.A1_scope` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 115 | 1 | killed |
| `u165.A2_refuse_unplaced_called` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 115 | 1 | killed |
| `u165.A3_grant_first` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 115 | 1 | killed |
| `u27-adopt-apply-author.A1_approval_actor_is_the_process` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 632 | 1 | killed |
| `u27-adopt-apply-author.A2_gate_found_by_position` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 1014 | 1 | killed |
| `u27-adopt-apply-author.S1_no_session_at_all` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 17 | 6 | killed |
| `u27-adopt-apply-author.S2_analysis_watch_watches_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 165 | 2 | killed |
| `u27-adopt-apply-author.S4_workflow_is_not_the_verb` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `u55-collection-reader.R10_apply_zero_item_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `u55-collection-reader.R12_apply_item_ids` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 14 | killed |
| `u55-collection-reader.R19_collector_groups_locations` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `u55-collection-reader.R20_membership_locations_key` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 8 | killed |
| `u55-collection-reader.R24_worker_digest_check` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 3 | killed |
| `u55-collection-reader.R27_apply_no_tag_value` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `u55-round-2.R23_worker_raises_on_failure` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `r722.P1_level_none` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 4 | killed |
| `r722.P3_verdict_drops_level` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 1 | killed |
| `r722.P7_tally_counts_excluded` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 1 | killed |
| `r722.P8_tally_folds_unreadable` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 2 | killed |
| `r731-a.M01_unread_tree_withholds` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 1 | killed |
| `r731-a.M02_held_sub_class_competes` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 3 | killed |
| `r731-a.M03_same_sub_withheld` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 5 | killed |
| `r731-a.M04_renamed_sub_not_withheld` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 2 | killed |
| `r731-a.M05_unnamed_without_held` | `src/cratekit/adopt/plan.py` | maintainer | 2 file(s) | 68 | 1 | killed |
| `r731-a.M08_digest_blind_to_unread` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 1 | killed |
| `r731-a.M11_verdict_withheld_on_the_review_list` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 1 | killed |
| `r731-b.M23_collision_counts_a_listed_track` | `src/cratekit/adopt/plan.py` | maintainer | 2 file(s) | 68 | 1 | killed |
| `r731-c.M25_planned_sub_outside_the_set` | `src/cratekit/adopt/plan.py` | maintainer | 2 file(s) | 68 | 1 | killed |
| `r788-a.P1_untagged_is_added` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 11 | killed |
| `r788-a.P2_blind_plan_files` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-a.P3_uncalibrated_files` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 4 | killed |
| `r788-a.P5_withheld_gains` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-a.P6_present_is_added` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 8 | killed |
| `r788-a.P7_renamed_track_reads_present` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-a.P8_renamed_bucket_doubles` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 2 | killed |
| `r788-b.P10_manual_class_is_vocal` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 1 | killed |
| `r788-b.P12_name_clash_files_into_a_style` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 4 | killed |
| `r788-b.P14_digest_drops_vocal` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 2 | killed |
| `r788-b.P16_digest_moves_under_its_own_apply` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-b.P17_withheld_presence_is_planned` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 161 | 1 | killed |
| `r788-b.P9_unplaced_entry_gains` | `src/cratekit/adopt/plan.py` | maintainer | 4 file(s) | 161 | 1 | killed |
| `u165.P1_undeclared` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 115 | 1 | killed |
| `u165.P2_vocal_sub` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 115 | 3 | killed |
| `r239-b.S10_adopt_apply_key_off` | `src/cratekit/adopt/apply_cli.py` | user | 7 file(s) | 723 | 1 | killed |
| `r722.A1_gate_drops_tally` | `src/cratekit/adopt/apply_cli.py` | user | 3 file(s) | 61 | 1 | killed |
| `r731-b.M13_gate_without_the_review_list` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `r731-b.M14_gate_without_the_count` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `r731-b.M15_gate_without_the_read_state` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 2 | killed |
| `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `u55-round-2.R8_census_prefix_map` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 44 | 1 | killed |
| `r722.P2_build_drops_level` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 3 | killed |
| `r722.P4_entry_drops_energy` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 3 | killed |
| `r722.P5_entry_drops_unreadable` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 4 | killed |
| `r731-a.M06_competing_place_never_withholds` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 13 | killed |
| `r731-a.M07_withheld_entry_loses_its_bucket` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 6 | killed |
| `r731-a.M09_digest_blind_to_the_review_list` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 68 | 3 | killed |
| `r788-b.P19_answered_genre_files_nothing` | `src/cratekit/adopt/plan.py` | maintainer | 4 file(s) | 161 | 1 | killed |
| `u165.P3_of_vocal` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 115 | 1 | killed |
| `u23-round-8-independent.X10_entry_id_drops_the_sub` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 615 | 1 | killed |

## Row definitions

### `u23-round-8-independent.X9_outstanding_returns_everything`

A resume re-applies every entry from the top

- File: `src/cratekit/adopt/apply.py`
- Source: `u23-round-8-independent.json`, row `X9_outstanding_returns_everything`
- Surface: user
- Subset: explicit subset from the row
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

### `u254-m08.M08_never_append`

mark_applied: rewrite the whole ledger on every mark that misses the cache, the square this card ends

- File: `src/cratekit/adopt/apply.py`
- Source: `u254-m08.json`, row `M08_never_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if False:
                config.append_durable_bytes(line, path)
```

### `u254.M01_mark_validates_record`

mark_applied: drop the reader's field rules on the record before it is written, so a record the reader refuses lands

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M01_mark_validates_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`

Old text:

```
    _record_from(
        entry.to_json(),
        path=path,
        where=f"was refused a record for the entry {entry.entry_id!r}, one",
    )
```

New text:

```
    pass
```

### `u254.M02_cache_identity_ignored`

mark_applied: append whenever this process has marked the path before, whatever happened to the file since

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M02_cache_identity_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_record_another_process_left_is_cut_before_the_next_append`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`

Old text:

```
        if known is not None and known == _as_left(path):
```

New text:

```
        if known is not None:
```

### `u254.M03_cache_identity_no_size`

_as_left: leave the size out of the identity, so a same inode file another hand changed reads as left

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M03_cache_identity_no_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, found.st_ino, 0, found.st_mtime_ns)
```

### `u254.M04_cache_identity_no_mtime`

_as_left: leave the modification time out of the identity

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M04_cache_identity_no_mtime`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, found.st_ino, found.st_size, 0)
```

### `u254.M05_cache_identity_no_inode`

_as_left: leave the inode out of the identity, so a replaced file of the same size reads as left

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M05_cache_identity_no_inode`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, 0, found.st_size, found.st_mtime_ns)
```

### `u254.M06_never_cache`

mark_applied: never remember what this process left, so every mark reads the whole ledger again

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M06_never_cache`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`

Old text:

```
        if left is not None:
            _LEFT[key] = left
```

New text:

```
        if left is not None:
            pass
```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 86 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`
  - ... and 71 more, see the JSON sidecar

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if True:
                config.append_durable_bytes(line, path)
```

### `u254.M09_any_line_torn`

_read_journal: read a damaged line anywhere as torn and stop, so the records after it are lost

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M09_any_line_torn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a damaged line before the last]`

Old text:

```
            if index == len(body) - 1 and whole:
```

New text:

```
            if whole:
```

### `u254.M10_torn_needs_terminated_tail`

_read_journal: read a damaged last whole line as torn even when an unterminated line follows it

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M10_torn_needs_terminated_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[two torn lines at the end]`

Old text:

```
            if index == len(body) - 1 and whole:
```

New text:

```
            if index == len(body) - 1:
```

### `u254.M11_unterminated_tail_whole`

_read_journal: call a journal with an unterminated last line appendable

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M11_unterminated_tail_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 23 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_record_another_process_left_is_cut_before_the_next_append`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[two torn lines at the end]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-4]`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    whole = not tail
```

New text:

```
    whole = True
```

### `u254.M12_header_upgrade`

_read_journal: drop the upgrade refusal of a newer journal header

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M12_header_upgrade`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header from a newer build]`

Old text:

```
            f"{SCHEMA_VERSION}",
            Remedy.UPGRADE_CRATEKIT,
        )
    if version != SCHEMA_VERSION:
```

New text:

```
            f"{SCHEMA_VERSION}",
            Remedy.RUN_DOCTOR,
        )
    if version != SCHEMA_VERSION:
```

### `u254.M13_header_older_version`

_read_journal: accept a journal header at a schema no build wrote as a journal

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M13_header_older_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header with an older version]`

Old text:

```
    if version != SCHEMA_VERSION:
```

New text:

```
    if version > SCHEMA_VERSION:
```

### `u254.M14_header_unterminated`

_read_journal: accept a header with no line ending after it

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M14_header_unterminated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header alone with no newline]`

Old text:

```
    if len(lines) < 2:
```

New text:

```
    if len(lines) < 1:
```

### `u254.M15_header_string_version`

_read_journal: drop the integer check on the header's schema_version

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M15_header_string_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header with a string version]`

Old text:

```
    header = json.loads(lines[0].decode("utf-8"))
    version = header.get("schema_version")
    if not isinstance(version, int):
```

New text:

```
    header = json.loads(lines[0].decode("utf-8"))
    version = int(header.get("schema_version"))
    if not isinstance(version, int):
```

### `u254.M16_journal_needs_format`

_is_journal: take any object on the first line as a journal header

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M16_journal_needs_format`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_newer_document_still_asks_for_an_upgrade`

Old text:

```
    return isinstance(header, dict) and header.get("format") == JOURNAL_FORMAT
```

New text:

```
    return isinstance(header, dict)
```

### `u254.M17_document_at_journal_schema`

_read_document: read a whole document that claims schema 2

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M17_document_at_journal_schema`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_document_at_the_journal_schema_refuses`

Old text:

```
    if version > DOCUMENT_SCHEMA_VERSION:
```

New text:

```
    if version > SCHEMA_VERSION:
```

### `u254.M18_remark_first_wins`

_read_journal: fold a re-mark first one wins, unlike the document's writer

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M18_remark_first_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`

Old text:

```
        folded[record.entry_id] = record
```

New text:

```
        folded.setdefault(record.entry_id, record)
```

### `u254.M19_already_inverted`

apply_plan: report as already applied the entries the ledger does not hold

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M19_already_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 33 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-3]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id in done
```

New text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id not in done
```

### `u254.M21_record_needs_actor`

_record_from: drop actor from the fields every record must carry

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M21_record_needs_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a record missing its actor, last]`
  - `tests/test_adoption.py::test_a_wrong_applied_ledger_refuses_rather_than_reading_as_empty[11]`

Old text:

```
    for name in ("entry", "tree", "content", "actor"):
```

New text:

```
    for name in ("entry", "tree", "content"):
```

### `r235-b.M25_adoption_refusal_names_no_verb`

the adoption refusal on an uncut library is re-raised as it came, with no step

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r235-b.json`, row `M25_adoption_refusal_names_no_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`, `tests/test_adopt_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_uncut_library_refuses_adoption_and_names_the_cutover_verb`
  - `tests/test_cutover_cli.py::test_the_steps_the_refused_adoption_names_are_the_steps_that_work`

Old text:

```
        named = _naming_the_cutover(exc)
        if named is None:
```

New text:

```
        named = None
        if named is None:
```

### `r788-d.A2_vocal_rows_never_written`

planned_memberships: the vocal additions are left out of the write, so the gate lists memberships the apply never performs

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A2_vocal_rows_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_one_apply_writes_the_entries_and_the_vocal_subs_in_one_mapping`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`

Old text:

```
    for key, rows in vocal_locations(plan, declared).items():
```

New text:

```
    for key, rows in ():
```

### `r788-d.A3_present_rows_handed_over`

vocal_locations: every planned membership is handed to the writer, the present ones too

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A3_present_rows_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_only_the_additions_reach_the_writer_under_the_declared_names`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    return _locations(plan.vocal_additions(), declared, lambda entry: entry.vocal_sub)
```

New text:

```
    return _locations(plan.vocal_memberships(), declared, lambda entry: entry.vocal_sub)
```

### `u132.W1_every_apply`

The adoption runs the Favorites step only when it filed a track

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W1_every_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 446 against a baseline of 446
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`

Old text:

```
 or genre_favorites.favorites_class(declared) is None
```

New text:

```
(empty)
```

### `u132.W2_coded_note`

A skip over an undeclared class carries favorites-skipped, not its cause code

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W2_coded_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 446 against a baseline of 446
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_genre_favorites.py::test_the_undeclared_note_states_the_version_the_skip_saw`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
    if skipped and cause == genre_favorites.CLASS_UNDECLARED:

```

New text:

```
    if False:

```

### `u132.W3_version_from_report`

The job's report does not carry the version the skip saw

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W3_version_from_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 446 against a baseline of 446
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            "schema_version": declared.schema_version,

```

New text:

```
            "schema_version": None,

```

### `u165.A1_scope`

census: ignore the scope and walk the whole collection

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A1_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_the_census_a_landing_files_walks_only_the_rows_it_made`

Old text:

```
        rows = tuple(row for row in rows if row.content_id in scope)
```

New text:

```
        rows = tuple(rows)
```

### `u165.A2_refuse_unplaced_called`

file_plan: skip the unplaced refusal before the ledger is marked

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A2_refuse_unplaced_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`

Old text:

```
    refuse_unplaced(membership)

```

New text:

```
    pass

```

### `u165.A3_grant_first`

file_plan: mint no approval before the memberships are written

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A3_grant_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`

Old text:

```
    grant(plan, actor=actor)

    membership = _write_memberships
```

New text:

```
    membership = _write_memberships
```

### `u27-adopt-apply-author.A1_approval_actor_is_the_process`

Mint the approval under a fixed actor, so the record cannot say who asserted it

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A1_approval_actor_is_the_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`
- Collected: 632 against a baseline of 632
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
            approval=grant(plan, actor=actor),
```

New text:

```
            approval=grant(plan, actor="cli"),
```

### `u27-adopt-apply-author.A2_gate_found_by_position`

Take the first declared gate rather than the one digested against the plan

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A2_gate_found_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 1014 against a baseline of 1014
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`

Old text:

```
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
```

New text:

```
    for spec in entry.gates:
        if True:
            return spec
```

### `u27-adopt-apply-author.S1_no_session_at_all`

Run the apply loop with no destructive session around it (the residual's condition, unchanged)

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S1_no_session_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_a_volume_whose_identity_moved_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_an_unacknowledged_machine_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
    with session.assert_gates(
        cfg,
        workflow=WORKFLOW,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ):
```

New text:

```
    if True:
```

### `u27-adopt-apply-author.S2_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S2_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_write_session.py`
- Collected: 165 against a baseline of 165
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `u27-adopt-apply-author.S4_workflow_is_not_the_verb`

Record the session under a name that is not this verb's

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S4_workflow_is_not_the_verb`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`

Old text:

```
WORKFLOW = "adopt.apply"
```

New text:

```
WORKFLOW = "adoption"
```

### `u55-collection-reader.R10_apply_zero_item_refusal`

The apply queues a job with one item over a plan that can place nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R10_apply_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`

Old text:

```
    if not applicable:
```

New text:

```
    if False:
```

### `u55-collection-reader.R12_apply_item_ids`

The apply enqueues with no items at all

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R12_apply_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 14 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[None]`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[no-such-root]`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
            item_ids=(plan.digest(),),
```

New text:

```
            item_ids=(),
```

### `u55-collection-reader.R19_collector_groups_locations`

The collector groups content identifiers again, which is the seam defect U55 found

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R19_collector_groups_locations`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
            into.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
            into.setdefault((folder, sub), []).append(entry.content_id)
```

### `u55-collection-reader.R20_membership_locations_key`

The written mapping groups content identifiers, so the write matches nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R20_membership_locations_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
        grouped.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
        grouped.setdefault((folder, sub), []).append(entry.content_id)
```

### `u55-collection-reader.R24_worker_digest_check`

The worker applies a plan nobody approved, because the frozen digest is not compared

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R24_worker_digest_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if plan.digest() != frozen_digest:
```

New text:

```
    if False:
```

### `u55-collection-reader.R27_apply_no_tag_value`

A tag_value supplier is installed, so the apply writes a genre onto the person's files

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R27_apply_no_tag_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`

Old text:

```
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

New text:

```
    report, gathered = apply_outstanding(
        cfg, plan, declared, actor=actor, tag_value=lambda entry, _d: entry.bucket or None
    )
```

### `u55-round-2.R23_worker_raises_on_failure`

A failed apply returns rather than raising, so the job reaches SUCCEEDED over nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R23_worker_raises_on_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`

Old text:

```
    if report.failed:
        _commit(produced)
        raise refuse(
```

New text:

```
    if False:
        _commit(produced)
        raise refuse(
```

### `r722.P1_level_none`

The original defect: _sub_for resolves with a level of None for every track

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P1_level_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`

Old text:

```
    sub = routing.energy_sub(declared, bucket_id, level, source_genre=genre)
```

New text:

```
    sub = routing.energy_sub(declared, bucket_id, None, source_genre=genre)
```

### `r722.P3_verdict_drops_level`

with_verdicts resolves an answered genre with no reading

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P3_verdict_drops_level`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`

Old text:

```
        sub = _sub_for(declared, chosen, entry.genre, entry.energy)
```

New text:

```
        sub = _sub_for(declared, chosen, entry.genre, None)
```

### `r722.P7_tally_counts_excluded`

The tally counts entries the census never opened

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P7_tally_counts_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_excluded_file_is_never_opened_for_its_reading`

Old text:

```
            if entry.category is not Readability.READABLE:
                continue
            if entry.energy_unreadable:
```

New text:

```
            if entry.energy_unreadable:
```

### `r722.P8_tally_folds_unreadable`

The tally counts an unreadable file as absent

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P8_tally_folds_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
            if entry.energy_unreadable:
                readings["unreadable"] += 1
            elif entry.energy is None:
```

New text:

```
            if entry.energy is None:
```

### `r731-a.M01_unread_tree_withholds`

a tree nobody read is treated as read, so held subs a caller carried withhold

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M01_unread_tree_withholds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_an_unread_tree_withholds_nothing_even_when_it_carries_held_subs`

Old text:

```
    if not placements.read:
        return NO_COMPETING_PLACE
    kind, competing
```

New text:

```
    kind, competing
```

### `r731-a.M02_held_sub_class_competes`

a held sub is no longer filtered to the bucket's competing subs, so a sub class withholds

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M02_held_sub_class_competes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_sitting_only_in_a_sub_class_is_added_to_its_band[candy]`
  - `tests/test_adopt_placements.py::test_a_track_sitting_only_in_a_sub_class_is_added_to_its_band[favorites]`
  - `tests/test_adopt_placements.py::test_a_track_sitting_only_in_a_sub_class_is_added_to_its_band[with_vox]`

Old text:

```
    held = tuple(sorted(set(placements.holds(bucket, content_id)) & competing))
```

New text:

```
    held = tuple(sorted(set(placements.holds(bucket, content_id))))
```

### `r731-a.M03_same_sub_withheld`

a track already in the sub the plan names is withheld instead of left to the writer

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M03_same_sub_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_already_in_the_sub_the_plan_names_is_not_withheld`
  - `tests/test_adopt_placements.py::test_a_track_in_two_bands_is_not_withheld_from_the_one_the_plan_names`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    if not held:
```

### `r731-a.M04_renamed_sub_not_withheld`

a track in the planned sub under another name only is routed, so the writer doubles it

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M04_renamed_sub_not_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_in_the_planned_sub_under_another_name_only_is_withheld`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    if not held or sub in held:
```

### `r731-a.M05_unnamed_without_held`

an unnamed sub is no longer required to be one the track holds

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M05_unnamed_without_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_an_unnamed_sub_the_track_does_not_hold_changes_nothing`

Old text:

```
    unnamed = tuple(sorted(set(placements.holds_unnamed(bucket, content_id)) & set(held)))
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    unnamed = tuple(sorted(set(placements.holds_unnamed(bucket, content_id))))
    if (not held and not unnamed) or (sub in held and sub not in unnamed):
```

### `r731-a.M08_digest_blind_to_unread`

the digest no longer covers whether the tree was read

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M08_digest_blind_to_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_tree_nobody_read_is_a_different_plan_from_a_tree_holding_nothing`

Old text:

```
                "placements": self.placements.state,
                "held_elsewhere": [
```

New text:

```
                "held_elsewhere": [
```

### `r731-a.M11_verdict_withheld_on_the_review_list`

an entry a collision verdict withheld is listed as holding a place

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M11_verdict_withheld_on_the_review_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_collision_verdict_withholds_under_its_own_reason_and_own_count`

Old text:

```
        return self.disposition is Disposition.WITHHELD and bool(self.holds)
```

New text:

```
        return self.disposition is Disposition.WITHHELD
```

### `r731-b.M23_collision_counts_a_listed_track`

a track the plan withheld and listed is counted a stranger in its own folder

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-b.json`, row `M23_collision_counts_a_listed_track`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_the_plan_withheld_is_not_a_stranger_in_its_own_folder`

Old text:

```
            - planned_by_bucket[bucket_id]
            - named_by_bucket.get(bucket_id, set())
```

New text:

```
            - planned_by_bucket[bucket_id]
```

### `r731-c.M25_planned_sub_outside_the_set`

a planned sub outside the bucket's competing subs is no longer let through unasked

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-c.json`, row `M25_planned_sub_outside_the_set`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_planned_sub_outside_the_competing_set_is_never_withheld`

Old text:

```
    if sub not in competing:
        return NO_COMPETING_PLACE
    held
```

New text:

```
    held
```

### `r788-a.P1_untagged_is_added`

vocal_place: drop the tag check, so every routed track of a calibrated library is filed under the vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P1_untagged_is_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 11 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_plan_with_no_vocal_addition_hands_the_writer_what_it_always_did`
  - `tests/test_adopt_vocals.py::test_a_tagged_track_with_no_bucket_is_counted_as_one_and_not_passed_over`
  - `tests/test_adopt_vocals.py::test_a_track_without_the_tag_is_never_added`
  - `tests/test_adopt_vocals.py::test_an_untagged_track_sitting_in_a_vocal_sub_is_left_out_of_the_plan_entirely`
  - `tests/test_adopt_vocals.py::test_one_apply_writes_the_entries_and_the_vocal_subs_in_one_mapping`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_vocals.py::test_the_digest_changes_when_a_vocal_membership_is_added_to_the_plan`
  - `tests/test_adopt_vocals.py::test_the_document_names_the_count_and_lists_every_membership_it_may_write`
  - `tests/test_adopt_vocals.py::test_the_gate_shows_what_the_document_says_about_vocals`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`

Old text:

```
    if not vocals.filing or not vocals.carries(content_id):
```

New text:

```
    if not vocals.filing:
```

### `r788-a.P2_blind_plan_files`

vocal_place: drop the filing check, so a tree nobody read, a taxonomy with no vocal sub and an uncalibrated library all file from the tag

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P2_blind_plan_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_library_with_no_calibrated_cut_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_a_tree_nobody_read_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_each_reason_nothing_can_be_filed_plans_nothing_for_a_tagged_track`

Old text:

```
    if not vocals.filing or not vocals.carries(content_id):
```

New text:

```
    if not vocals.carries(content_id):
```

### `r788-a.P3_uncalibrated_files`

Vocals.filing: drop the calibration, so tags written from the default cut file a back catalogue

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P3_uncalibrated_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_library_with_no_calibrated_cut_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_each_reason_nothing_can_be_filed_plans_nothing_for_a_tagged_track`
  - `tests/test_adopt_vocals.py::test_the_digest_says_whether_the_tag_and_the_tree_were_read`
  - `tests/test_adopt_vocals.py::test_whether_the_library_is_calibrated_is_carried_and_not_assumed`

Old text:

```
        return self.read and self.has_sub and self.calibrated
```

New text:

```
        return self.read and self.has_sub
```

### `r788-a.P5_withheld_gains`

vocal_place: a withheld track is added to its vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P5_withheld_gains`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_withheld_over_another_band_stays_withheld_and_gains_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if disposition is Disposition.WITHHELD:
        return VOCAL_WITHHELD, sub
```

New text:

```
    if False:
        return VOCAL_WITHHELD, sub
```

### `r788-a.P6_present_is_added`

vocal_place: a track already in the sub is planned as an addition and handed to the writer

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P6_present_is_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_keep_separate_verdict_withholds_the_vocal_addition_with_the_entry`
  - `tests/test_adopt_vocals.py::test_a_track_already_in_the_sub_is_counted_present_and_not_added`
  - `tests/test_adopt_vocals.py::test_a_withheld_track_already_in_its_vocal_sub_reads_present_and_is_not_digested`
  - `tests/test_adopt_vocals.py::test_only_the_additions_reach_the_writer_under_the_declared_names`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_vocals.py::test_the_digest_does_not_move_when_the_membership_it_approved_lands`
  - `tests/test_adopt_vocals.py::test_the_document_names_the_count_and_lists_every_membership_it_may_write`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if vocals.sits(bucket, content_id):
        return VOCAL_PRESENT, sub
```

New text:

```
    if False:
        return VOCAL_PRESENT, sub
```

### `r788-a.P7_renamed_track_reads_present`

vocal_place: a track in the sub under another name only reads present, so it joins the digest as a membership the writer may be handed

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P7_renamed_track_reads_present`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_in_the_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_vocals.py::test_a_track_whose_bucket_has_its_vocal_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if vocals.sits_unnamed(bucket, content_id):
        return VOCAL_RENAMED, sub
```

New text:

```
    if False:
        return VOCAL_RENAMED, sub
```

### `r788-a.P8_renamed_bucket_doubles`

vocal_place: a bucket whose vocal sub answers under another name only is added to, so the writer makes a second playlist beside it

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P8_renamed_bucket_doubles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_whose_bucket_has_its_vocal_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if bucket in vocals.renamed:
        return VOCAL_RENAMED, sub
```

New text:

```
    if False:
        return VOCAL_RENAMED, sub
```

### `r788-b.P10_manual_class_is_vocal`

vocal_sub: a class of the vocal identifier that is not additive is filed under

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P10_manual_class_is_vocal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_no_additive_class_of_the_vocal_identifier_is_no_vocal_sub`

Old text:

```
        if not entry.additive or entry.id != VOX_SUB_CLASS:
```

New text:

```
        if entry.id != VOX_SUB_CLASS:
```

### `r788-b.P12_name_clash_files_into_a_style`

vocal_sub: a bucket whose own sub or band label carries the vocal sub's display name still has a vocal sub, so vocal tracks are filed into that style

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P12_name_clash_files_into_a_style`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_bucket_that_has_no_vocal_sub_is_not_read_for_one`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_band_is_labelled_with_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_own_sub_carries_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_with_no_vocal_sub_plans_nothing_for_its_tagged_tracks`

Old text:

```
        if entry.id in ids or entry.display in displays:
```

New text:

```
        if entry.id in ids:
```

### `r788-b.P14_digest_drops_vocal`

digest: no vocal membership is covered, so a plan that gained vocal additions after the approval is applied under it

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P14_digest_drops_vocal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_the_digest_changes_when_a_vocal_membership_is_added_to_the_plan`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_memberships()],
```

New text:

```
                "vocal": [],
```

### `r788-b.P16_digest_moves_under_its_own_apply`

digest: cover the additions only, so the apply's own write moves the digest and a stopped run refuses its own work

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P16_digest_moves_under_its_own_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_every_row_the_writer_may_be_handed_is_on_the_gate_whatever_the_tree_holds_now`
  - `tests/test_adopt_vocals.py::test_the_digest_does_not_move_when_the_membership_it_approved_lands`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_memberships()],
```

New text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_additions()],
```

### `r788-b.P17_withheld_presence_is_planned`

PlanEntry.vocal_planned: drop applicable, so a withheld track's vocal membership is one an apply may write

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P17_withheld_presence_is_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_withheld_track_already_in_its_vocal_sub_reads_present_and_is_not_digested`

Old text:

```
        return self.applicable and self.vocal in VOCAL_PLANNED
```

New text:

```
        return self.vocal in VOCAL_PLANNED
```

### `r788-b.P9_unplaced_entry_gains`

vocal_place: only an empty bucket is no bucket, so an entry the plan does not place gains a vocal sub when a caller hands its bucket in

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P9_unplaced_entry_gains`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_an_entry_the_plan_does_not_place_has_no_bucket_whatever_bucket_it_is_handed`

Old text:

```
    if not bucket or disposition not in (Disposition.ROUTE, Disposition.WITHHELD):
        return VOCAL_NO_BUCKET, ""
```

New text:

```
    if not bucket:
        return VOCAL_NO_BUCKET, ""
```

### `u165.P1_undeclared`

predicted_place: route a band the taxonomy declares no sub for

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P1_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_band_the_taxonomy_declares_no_sub_for_predicts_undeclared`

Old text:

```
        return Predicted(disposition=Disposition.UNDECLARED)
```

New text:

```
        return Predicted(disposition=disposition, bucket=bucket)
```

### `u165.P2_vocal_sub`

predicted_place: give every route the vocal sub, vox or not

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P2_vocal_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`
  - `tests/test_intake_land_filing.py::test_the_filed_rows_are_what_adopt_apply_then_finds_nothing_to_do_for`

Old text:

```
    vocal = (vocal_sub(declared, bucket) or "") if vox else ""
```

New text:

```
    vocal = vocal_sub(declared, bucket) or ""
```

### `r239-b.S10_adopt_apply_key_off`

adopt apply's write open passes unlock=False

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r239-b.json`, row `S10_adopt_apply_key_off`
- Moved: the write open's arguments were joined onto one line by the formatter; the mutation adds unlock=False to it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, unlock=False, cfg=cfg)
```

### `r722.A1_gate_drops_tally`

The approval gate's facts omit the reading tally

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r722.json`, row `A1_gate_drops_tally`
- Moved: the gate's facts are now read through the _FACTS key list; dropping energy from it is dropping the energy line from the gate document
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`

Old text:

```
    "counts",
    "energy",

```

New text:

```
    "counts",

```

### `r731-b.M13_gate_without_the_review_list`

the gate's facts no longer carry the list of withheld entries

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M13_gate_without_the_review_list`
- Moved: the gate's facts are now read through the _FACTS key list; dropping held_elsewhere from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    "withheld_by_placement",
    "held_elsewhere",

```

New text:

```
    "withheld_by_placement",

```

### `r731-b.M14_gate_without_the_count`

the gate's facts no longer carry the withheld count split by kind

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M14_gate_without_the_count`
- Moved: the gate's facts are now read through the _FACTS key list; dropping withheld_by_placement from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    "placements",
    "withheld_by_placement",

```

New text:

```
    "placements",

```

### `r731-b.M15_gate_without_the_read_state`

the gate's facts no longer say whether the tree was read

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M15_gate_without_the_read_state`
- Moved: the gate's facts are now read through the _FACTS key list; dropping placements from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncut_library_reads_neither_its_tree_nor_its_vocals`

Old text:

```
    "collisions",
    "placements",

```

New text:

```
    "collisions",

```

### `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason`

Report a verb declaring no approval gate as a configuration problem

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A3_missing_gate_refuses_under_the_wrong_reason`
- Moved: the refusal is now built through core.cause.refuse, whose first argument is the reason; the same reason is swapped
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`

Old text:

```
        "internal-error",
        f"{entry.name} declares no gate digested against the plan, so "
```

New text:

```
        "config-unusable",
        f"{entry.name} declares no gate digested against the plan, so "
```

### `u55-round-2.R8_census_prefix_map`

The census drops the configured volume rewrites, so an older volume name resolves nowhere

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R8_census_prefix_map`
- Moved: the census's scan_rows arguments were joined onto one line by the formatter; the prefix map is emptied as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`

Old text:

```
            rows, declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg)
```

New text:

```
            rows, declared, root=cfg.library.root, prefix_map=()
```

### `r722.P2_build_drops_level`

build_adoption_plan passes None instead of the scanned track's reading

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P2_build_drops_level`
- Moved: the resolved sub is now named sub and handed to _destined; the energy level is dropped from the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`

Old text:

```
            sub = _sub_for(declared, bucket, track.genre, track.energy)
```

New text:

```
            sub = _sub_for(declared, bucket, track.genre, None)
```

### `r722.P4_entry_drops_energy`

The plan entry does not carry the census's level

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P4_entry_drops_energy`
- Moved: the PlanEntry is now built before _destined routes it, four spaces less indented; the energy field is dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`

Old text:

```
            energy=track.energy,
            energy_unreadable=track.energy_unreadable,
```

New text:

```
            energy_unreadable=track.energy_unreadable,
```

### `r722.P5_entry_drops_unreadable`

The plan entry does not carry the unreadable flag

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P5_entry_drops_unreadable`
- Moved: the PlanEntry is now built before _destined routes it, four spaces less indented; the unreadable flag is dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
            energy=track.energy,
            energy_unreadable=track.energy_unreadable,
```

New text:

```
            energy=track.energy,
```

### `r731-a.M06_competing_place_never_withholds`

the plan reads the competing place and routes the entry anyway

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M06_competing_place_never_withholds`
- Moved: a competing place now withholds in _destined, which build_adoption_plan and with_verdicts share; the competing place is ignored as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_collision_verdict_withholds_under_its_own_reason_and_own_count`
  - `tests/test_adopt_placements.py::test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds`
  - `tests/test_adopt_placements.py::test_a_track_in_a_band_whose_file_has_no_reading_is_withheld_from_the_sink`
  - `tests/test_adopt_placements.py::test_a_track_in_one_band_whose_file_reads_another_is_withheld_and_listed`
  - `tests/test_adopt_placements.py::test_a_track_in_one_style_sub_is_withheld_from_another`
  - `tests/test_adopt_placements.py::test_a_track_in_the_no_reading_sub_whose_file_now_reads_is_withheld`
  - `tests/test_adopt_placements.py::test_a_track_in_the_planned_sub_under_another_name_only_is_withheld`
  - `tests/test_adopt_placements.py::test_a_track_in_two_bands_is_withheld_from_a_third_and_both_are_listed`
  - `tests/test_adopt_placements.py::test_the_digest_covers_every_field_the_review_list_shows`
  - `tests/test_adopt_placements.py::test_the_digest_differs_between_a_plan_with_a_withheld_entry_and_one_without`
  - `tests/test_adopt_placements.py::test_the_digest_moves_when_a_withheld_track_is_moved_to_another_band`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE
```

New text:

```
        disposition = Disposition.WITHHELD if False else Disposition.ROUTE
```

### `r731-a.M07_withheld_entry_loses_its_bucket`

a withheld entry's bucket is blanked, so its identifier and its review row lose it

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M07_withheld_entry_loses_its_bucket`
- Moved: the entry a competing place withholds now keeps its bucket in _destined; the mutation blanks it there, as the old condition did for every withheld entry
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds`
  - `tests/test_adopt_placements.py::test_a_track_in_one_band_whose_file_reads_another_is_withheld_and_listed`
  - `tests/test_adopt_placements.py::test_a_track_the_plan_withheld_is_not_a_stranger_in_its_own_folder`
  - `tests/test_adopt_placements.py::test_a_withheld_entry_keeps_the_identifier_of_the_work_it_was`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE

```

New text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE
        bucket = "" if withheld_by else bucket

```

### `r731-a.M09_digest_blind_to_the_review_list`

the digest no longer covers the rows of the review list

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M09_digest_blind_to_the_review_list`
- Moved: the digest's review list comprehension was joined onto one line by the formatter; it is emptied as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_the_digest_covers_every_field_the_review_list_shows`
  - `tests/test_adopt_placements.py::test_the_digest_moves_when_a_withheld_track_is_moved_to_another_band`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
                    {"id": entry.entry_id, **review_row(entry)} for entry in self.held_elsewhere()
```

New text:

```
                    {"id": entry.entry_id, **review_row(entry)} for entry in ()
```

### `r788-b.P19_answered_genre_files_nothing`

with_verdicts: an answered genre is asked of no vocals, so a tagged track given a bucket is never filed under its vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P19_answered_genre_files_nothing`
- Moved: with_verdicts now routes an answered entry through _destined; the plan's vocals are replaced with none as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_an_answered_genre_is_filed_under_the_vocal_sub_of_the_bucket_it_was_given`

Old text:

```
            _destined(declared, plan.placements, plan.vocals, sub_of, entry, chosen, sub)
```

New text:

```
            _destined(declared, plan.placements, NO_VOCALS, sub_of, entry, chosen, sub)
```

### `u165.P3_of_vocal`

Predicted.of: read the vocal sub of an entry whatever its vocal state

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P3_of_vocal`
- Moved: Predicted.of now names the vocal sub before building itself; the condition on it is dropped as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_an_entry_whose_vocal_is_not_added_reads_no_vocal_sub`

Old text:

```
        vocal_sub = entry.vocal_sub if entry.vocal == VOCAL_ADD else ""
```

New text:

```
        vocal_sub = entry.vocal_sub
```

### `u23-round-8-independent.X10_entry_id_drops_the_sub`

Two pieces of work differing only by sub-folder share one identifier

- File: `src/cratekit/adopt/plan.py`
- Source: `u23-round-8-independent.json`, row `X10_entry_id_drops_the_sub`
- Moved: the identifier's document was joined onto one line by the formatter; the sub is dropped from it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_entry_identifier_moves_when_the_destination_moves`

Old text:

```
        canonical_json({"tree": tree, "content": content_id, "bucket": bucket, "sub": sub}).encode()
```

New text:

```
        canonical_json({"tree": tree, "content": content_id, "bucket": bucket}).encode()
```

