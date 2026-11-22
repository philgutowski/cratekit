# Mutation table: u325-after-l-03

Measured by `scripts/mutate.py` on 2026-11-22 22:22 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 73.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u67.R1_refusal_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u67.R2_generic_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.R3_remedy_passthrough` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u254-m08.M08_never_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M01_mark_validates_record` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 4 | killed |
| `u254.M02_cache_identity_ignored` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 5 | killed |
| `u254.M03_cache_identity_no_size` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M04_cache_identity_no_mtime` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 770 | 1 | killed |
| `u254.M05_cache_identity_no_inode` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 770 | 1 | killed |
| `u254.M06_never_cache` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 770 | 1 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 93 | killed |
| `u254.M09_any_line_torn` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 2 | killed |
| `u254.M10_torn_needs_terminated_tail` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M11_unterminated_tail_whole` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 23 | killed |
| `u254.M12_header_upgrade` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M13_header_older_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M14_header_unterminated` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M15_header_string_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M16_journal_needs_format` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M17_document_at_journal_schema` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M18_remark_first_wins` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 1 | killed |
| `u254.M19_already_inverted` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 33 | killed |
| `u254.M21_record_needs_actor` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 770 | 3 | killed |
| `r658-c.S4c_dataless_skip_returns` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.A1_at_risk_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.A2_at_risk_always_false` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 6 | killed |
| `u23-round-8-independent.A3_at_risk_drops_the_original_clause` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.A4_at_risk_drops_the_record_value` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.A5_at_risk_drops_this_call` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.A6_at_risk_original_by_identity` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.B1_settled_never_refuses` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.B3_settled_bytes_clause_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.C1_shape2_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.C2_shape3_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.D2_bytes_agree_size_gate_inverted` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 6 | killed |
| `u23-round-8-independent.E1_vacancy_is_mere_absence` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.E2_vacancy_parent_check_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.E4_vacancy_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.F4_byte_search_reads_before_it_filters` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.G1_locked_passes_no_size` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.S1_size_of_always_none` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X12_look_at_drops_the_regular_file_test` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X9_outstanding_returns_everything` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 615 | 2 | killed |
| `u95-a.A1_never_rerooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-a.A2_library_sessions_rerooted_too` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A3_database_not_carried` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 4 | killed |
| `u95-a.A4_outside_database_refusal_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A5_capture_path_not_rebased` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A6_manifest_not_rebased_in_plan` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-a.A7_manifest_not_rebased_in_preflight` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A8_run_not_rooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-b.B2_manifest_database_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B3_sources_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-b.B4_captured_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B5_not_idempotent` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B6_recorded_path_not_normalised` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B8_outside_path_moved_anyway` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 2 | killed |
| `u95-b1.B1_manifest_root_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C1_plan_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C2_run_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-c.C3_step_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-c.C4_restorable_membership_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C5_staging_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-c.C6_staging_store_rule_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-c.C7_staging_store_itself_admitted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |

## Row definitions

### `u67.R1_refusal_to_empty`

A classified open failure reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R1_refusal_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_an_unopenable_database_refuses_and_renames_nothing`

Old text:

```
    except CratekitError as exc:
        inner = exc.cause
```

New text:

```
    except CratekitError as exc:
        return ()
        inner = exc.cause
```

### `u67.R2_generic_to_empty`

A read that fails after the open reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R2_generic_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_read_that_fails_after_the_open_refuses_and_renames_nothing`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        raise refuse(
```

New text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        return ()
        raise refuse(
```

### `u67.R3_remedy_passthrough`

Drop the inner remedy, so the refusal defaults to restore-from-snapshot

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R3_remedy_passthrough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`

Old text:

```
            remedy=inner.remediation.remedy or (None if steps else Remedy.REPORT_DEFECT),
            steps=steps,
```

New text:

```
            remedy=None,
            steps=(),
```

### `u254-m08.M08_never_append`

mark_applied: rewrite the whole ledger on every mark that misses the cache, the square this card ends

- File: `src/cratekit/adopt/apply.py`
- Source: `u254-m08.json`, row `M08_never_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
- Kills: 93 (killed)
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
  - ... and 78 more, see the JSON sidecar

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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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
- Collected: 770 against a baseline of 770
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

### `r658-c.S4c_dataless_skip_returns`

Composite for S4, run as its own table: put back a skip that refuses to read a dataless file, which only the scoped evicted stat can reach

- File: `src/cratekit/adopt/revert.py`
- Source: `r658-c.json`, row `S4c_dataless_skip_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    try:
        found = digest_of(target)

```

New text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    if getattr(info, "st_flags", 0) & 0x40000000:
        return _Looked(ByteRead.UNREADABLE)
    try:
        found = digest_of(target)

```

### `u23-round-8-independent.A1_at_risk_always_true`

Nothing is ever at risk, so _settled_or_refused can never refuse

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A1_at_risk_always_true`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.A2_at_risk_always_false`

Everything is at risk, so every re-run falls through to the digest

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A2_at_risk_always_false`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.A3_at_risk_drops_the_original_clause`

A field holding this record's own original is no longer accounted for

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A3_at_risk_drops_the_original_clause`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.A4_at_risk_drops_the_record_value`

The value the record says adoption wrote no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A4_at_risk_drops_the_record_value`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.A5_at_risk_drops_this_call`

The value THIS call is about to write no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A5_at_risk_drops_this_call`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.A6_at_risk_original_by_identity`

The original clause compares by object identity rather than by value

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A6_at_risk_original_by_identity`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.B1_settled_never_refuses`

Round 7 restored: the two converging-address shapes accept unconditionally

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B1_settled_never_refuses`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.B3_settled_bytes_clause_inverted`

The bytes acceptance fires when the bytes DISAGREE

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B3_settled_bytes_clause_inverted`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.C1_shape2_bypasses_the_check`

Shape 2, both addresses agreeing, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C1_shape2_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.C2_shape3_bypasses_the_check`

Shape 3, one file under two names, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C2_shape3_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate`

The size shortcut round 8 restored is removed again

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D1_bytes_agree_drops_the_size_gate`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u23-round-8-independent.D2_bytes_agree_size_gate_inverted`

The size shortcut refuses on AGREEING sizes

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D2_bytes_agree_size_gate_inverted`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u23-round-8-independent.E1_vacancy_is_mere_absence`

Round 7 restored: an unmounted volume reads as a deleted file

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E1_vacancy_is_mere_absence`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.E2_vacancy_parent_check_inverted`

Vacancy requires the containing directory to be ABSENT

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E2_vacancy_parent_check_inverted`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.E4_vacancy_always_true`

Every record is stranded, so every record is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E4_vacancy_always_true`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter`

A record whose path still holds its file is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F1_byte_search_drops_the_vacancy_filter`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.F4_byte_search_reads_before_it_filters`

Round 7 order restored: the whole-file read runs before the filters that empty the list

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F4_byte_search_reads_before_it_filters`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u23-round-8-independent.G1_locked_passes_no_size`

_record_locked hands size_here=None, disabling every size gate below it

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `G1_locked_passes_no_size`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u23-round-8-independent.S1_size_of_always_none`

_size_of never answers, so every size shortcut on every path is disabled

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `S1_size_of_always_none`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u23-round-8-independent.X12_look_at_drops_the_regular_file_test`

A directory or a fifo at the recorded path reaches the hash

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `X12_look_at_drops_the_regular_file_test`
- Surface: user
- Subset: explicit subset from the row
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

### `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut`

The prefetch reads a file whose size already rules the record out

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `X13_look_at_drops_the_recorded_size_shortcut`
- Surface: maintainer
- Subset: explicit subset from the row
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

### `u95-a.A1_never_rerooted`

_rooted hands every session its configuration back unchanged, which is main's state: a bare-metal session resolves from the configured root again

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A1_never_rerooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    if held.issued_by is not None:
        return cfg
    target = Path(held.authorises)
```

### `u95-a.A2_library_sessions_rerooted_too`

Drop the guard test in _rooted, so a library session handed a configuration for ANOTHER library is quietly re-aimed at what it authorises instead of refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A2_library_sessions_rerooted_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_live_recovery_session_plan_is_unchanged_by_golden`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    target = Path(held.authorises)
```

### `u95-a.A3_database_not_carried`

The relocated root no longer carries its database: db_path stays at the configured root while the root moves to the target

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A3_database_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    return replace(cfg, library=replace(cfg.library, root=target, db_path=database))
```

New text:

```
    return replace(cfg, library=replace(cfg.library, root=target))
```

### `u95-a.A4_outside_database_refusal_removed`

Delete the by-name refusal for a database kept outside the library, leaving the defect-flavoured authorisation refusal to catch it later

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A4_outside_database_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`

Old text:

```
    if not held.authorises_path(database):
        raise _refuse_target(
```

New text:

```
    if False:
        raise _refuse_target(
```

### `u95-a.A5_capture_path_not_rebased`

plan reads the session record's capture path as written, so the capture is taken from the configured root, the volume the identity gate refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A5_capture_path_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    root = capture_root_of(_rebased(record.snapshot_path, recorded_root, rooted_at))
```

New text:

```
    root = capture_root_of(record.snapshot_path)
```

### `u95-a.A6_manifest_not_rebased_in_plan`

plan uses the manifest as read from disk, every path in it still naming the dead root

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A6_manifest_not_rebased_in_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    captured = _rebased_capture(snapshot.read_manifest(root), recorded_root, rooted_at)
```

New text:

```
    captured = snapshot.read_manifest(root)
```

### `u95-a.A7_manifest_not_rebased_in_preflight`

The run's preflight re-reads the manifest and checks it un-rebased, so it asks the DEAD volume whether the capture is still whole

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A7_manifest_not_rebased_in_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    captured = _rebased_capture(
        snapshot.read_manifest(decided.capture_root),
        recorded_root,
        Path(cfg.library.root),
    )
```

New text:

```
    captured = snapshot.read_manifest(decided.capture_root)
```

### `u95-a.A8_run_not_rooted`

run resolves from the caller's configuration while plan resolves from the session, the two sources for one answer R-20 forbids

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A8_run_not_rooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    cfg = _rooted(configured, held)
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

New text:

```
    cfg = configured
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

### `u95-b.B2_manifest_database_not_moved`

_rebased_capture leaves Capture.database at the dead root, the file assert_verified asks the disk about

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B2_manifest_database_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
        database=moved(captured.database),
```

New text:

```
        database=captured.database,
```

### `u95-b.B3_sources_not_moved`

The WRITE side is not re-based: every manifest source still names the configured root

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B3_sources_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
                source=_rebased(entry.source, recorded_root, root),
```

New text:

```
                source=entry.source,
```

### `u95-b.B4_captured_not_moved`

The READ side is not re-based: writes aim at the target while the bytes come from the dead volume, the bypass run the other way

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B4_captured_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
                captured=moved(entry.captured),
```

New text:

```
                captured=entry.captured,
```

### `u95-b.B5_not_idempotent`

Drop the already-under-the-new-root clause, so a path naming a target mounted inside the configured root is moved twice

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B5_not_idempotent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
```

New text:

```
    if parts[: len(there)] != there:
```

### `u95-b.B6_recorded_path_not_normalised`

Compare the recorded path's raw parts, so a dotted spelling config calls inside is left unmoved and one it calls outside is moved

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B6_recorded_path_not_normalised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    parts = Path(os.path.normpath(str(recorded))).parts
```

New text:

```
    parts = recorded.parts
```

### `u95-b.B8_outside_path_moved_anyway`

A path under NEITHER root is joined onto the target instead of left where it says it is

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B8_outside_path_moved_anyway`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

New text:

```
    if parts[: len(here)] == here:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

### `u95-b1.B1_manifest_root_not_moved`

RE-MEASURED after test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else learned to compare decisions. _rebased_capture leaves Capture.root at the dead root, which is what _captured_by_key composes coupled entries from

- File: `src/cratekit/core/restore.py`
- Source: `u95-b1.json`, row `B1_manifest_root_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`

Old text:

```
        root=_rebased(captured.root, recorded_root, root),
```

New text:

```
        root=captured.root,
```

### `u95-c.C1_plan_side_guard_removed`

plan no longer checks its own answer, so only a run would find a plan naming an outside path

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C1_plan_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`

Old text:

```
    _assert_plan_is_authorised(steps, pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C2_run_side_guard_removed`

The preflight no longer asks the session about a plan value, so a plan built for one directory runs under a session for another

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C2_run_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    _assert_plan_is_authorised(decided.steps, decided.pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C3_step_authorisation_removed`

Inside the guard, drop the per step authorisation and leave only the membership test

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C3_step_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
        assert_gates_are_open(held, writing=step.target)
        if step.target not in allowed:
```

New text:

```
        if step.target not in allowed:
```

### `u95-c.C4_restorable_membership_removed`

Inside the guard, drop the re-derived membership test, so a step aimed at the authorised directory itself is admitted

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C4_restorable_membership_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`

Old text:

```
        if step.target not in allowed:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u95-c.C5_staging_authorisation_removed`

Inside the guard, drop the authorisation of the staging directory and leave only the store rule

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C5_staging_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    assert_gates_are_open(held, writing=pre_restore_root)
    store = _pre_restore_root(cfg).parent
```

New text:

```
    store = _pre_restore_root(cfg).parent
```

### `u95-c.C6_staging_store_rule_removed`

Inside the guard, drop the store rule, so an authorised staging directory such as the library root hands the closing prune the directory ABOVE the library

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C6_staging_store_rule_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if False:
```

### `u95-c.C7_staging_store_itself_admitted`

A nearby value: admit the store itself as the staging directory, which makes the prune run one level up, inside the database directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C7_staging_store_itself_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if pre_restore_root.parent != store and pre_restore_root != store:
```

