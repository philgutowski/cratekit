# Mutation table: u329-before-03

Measured by `scripts/mutate.py` on 2026-11-23 17:24 UTC, branch `HEAD` at `36dadb92`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22622 collected. pytest invocations for this batch: 94.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 17:24 UTC for commit `36dadb92a615`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 18, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22622 against 22622. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r647-a.B4_infinite_boot_accepted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B5_drift_margin_halved` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 2 | killed |
| `r647-a.B6_drift_margin_doubled` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B7_margin_boundary_exclusive` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B8_direction_ignored` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B9_platform_silence_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `u300.S13_process_exists_local` | `src/cratekit/core/session_holders.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session_holders.py` | user | 13 file(s) | 2575 | 1 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session_volumes.py` | maintainer | 2 file(s) | 479 | 1 | killed |
| `r44-a.S1_empty_slot` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 6 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 5 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `u300.S17_mapped_reasons_local` | `src/cratekit/core/session_volumes.py` | maintainer | 1 file(s) | 148 | 1 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 72 | 2 | killed |
| `r1255.R2_plan_carries_unlisted` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 72 | 1 | killed |
| `u111-c.C3_inboxed_suffix` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-c.C4_removal_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-c.C5_move_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-c.C6_plan_taken_again` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-c.C7_old_creation_planned` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-d.C10_two_olds_refused` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-d.C9_committed_records_only` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u113-c.C7_unproven_import_names` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 35 | 1 | killed |
| `u113-c.C9_earliest_name_wins` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 35 | 1 | killed |
| `u166.R2_rotate_reserved` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 49 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 4 file(s) | 83 | 3 | killed |
| `u214.M15_unread_is_not_none` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 2 | killed |
| `u214.M16_old_only_under_inbox` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 1 | killed |
| `u214.M18_folder_unknown` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 1 | killed |
| `u214.M19_folder_unread_reason` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 1 | killed |
| `u214.M1_old_named_as_old` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 5 | killed |
| `u214.M20_unread_unlisted` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 1 | killed |
| `u214.M2_left_row_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 4 | killed |
| `u214.M3_live_left_collected` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 8 | killed |
| `u214.M4_digest_without_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 1 | killed |
| `u214.M5_rotation_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 3 | killed |
| `u214.M6_live_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 3 | killed |
| `u214.M7_label_rows` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 174 | 2 | killed |
| `u307.R8_anchored_root_drops_cutover_step` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 57 | 2 | killed |
| `u307.R9_watched_roots_accepts_empty` | `src/cratekit/intake/rotate.py` | maintainer | 3 file(s) | 57 | 1 | killed |
| `a32.J3_bookkeeping_counted_as_moved` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 113 | 6 | killed |
| `r923.N11_digest_drops_items` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N12_digest_drops_values` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 22622 | 0 (promoted) | zero |
| `r923.N13_judge_compares_raw` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `r923.N2_plan_lists_tombstones` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 13 | killed |
| `r923.N3_plan_sees_no_null` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 8 | killed |
| `r923.N4_stale_fill_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N5_stale_tombstone_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N6_judge_blind_to_wrong` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N7_judge_blind_to_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N8_read_back_never_refuses` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F11_stale_file_id_not_checked` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F12_read_back_ignores_file_id` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F13_planned_renumber_read_as_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F14_renumber_never_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F17_bound_is_zero` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 22622 | 0 (promoted) | zero |
| `u115.F21_other_volume_compared` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F22_off_apfs_decides` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F23_loose_digits` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F5_bound_boundary` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F6_every_id_above` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 12 | killed |
| `u115.F7_zero_is_not_zero` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `u115.F8_matching_inode_renumbered` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 22622 | 0 (promoted) | zero |
| `u115.F9_unreadable_file_dropped_silently` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 5 | killed |
| `u298.H24_record_commit_nothing_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 100 | 1 | killed |
| `u302.W10_empty_watch_accepted` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 113 | 1 | killed |

## Zero rows and what they owe

- `r923.N12_digest_drops_values` (maintainer facing): maintainer facing, composite not required
- `u115.F17_bound_is_zero` (maintainer facing): maintainer facing, composite not required
- `u115.F8_matching_inode_renumbered` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r647-a.B4_infinite_boot_accepted`

_gone_since_an_earlier_boot: drop the finiteness check, so a boot recorded as minus infinity reads as infinitely earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B4_infinite_boot_accepted`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not finite-changes6]`

Old text:

```
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
    if earlier_by <= BOOT_DRIFT_SECONDS:
```

### `r647-a.B5_drift_margin_halved`

BOOT_DRIFT_SECONDS: 60 to 30, a realistic nearby value, so a clock adjustment of forty seconds reads as a restart

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B5_drift_margin_halved`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 30.0
```

### `r647-a.B6_drift_margin_doubled`

BOOT_DRIFT_SECONDS: 60 to 120, so a restart a minute and a half apart is kept for no reason

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B6_drift_margin_doubled`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 120.0
```

### `r647-a.B7_margin_boundary_exclusive`

_gone_since_an_earlier_boot: less than instead of less than or equal, so a boot exactly at the margin is judged earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B7_margin_boundary_exclusive`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
earlier_by < BOOT_DRIFT_SECONDS:
```

### `r647-a.B8_direction_ignored`

_gone_since_an_earlier_boot: take the distance between the boots rather than which came first, so a LATER boot reading reads as an earlier boot

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B8_direction_ignored`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a later boot-changes4]`

Old text:

```
        earlier_by = float(reference.boot) - float(holder.boot)
```

New text:

```
        earlier_by = abs(float(reference.boot) - float(holder.boot))
```

### `r647-a.B9_platform_silence_read_as_gone`

_gone_since_an_earlier_boot: read a platform declining to say whether the process exists as gone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B9_platform_silence_read_as_gone`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probe read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return _session().process_exists(holder.pid) is not True
```

### `u300.S13_process_exists_local`

a holder's death since an earlier boot is judged by the part's own process_exists

- File: `src/cratekit/core/session_holders.py`
- Source: `u300.json`, row `S13_process_exists_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return process_exists(holder.pid) is False
```

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session_holders.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Moved: U953 merged read_lock_holder's JSON parse and holder coercion under one try, so narrowing its except to the parse error alone is the same removed coercion guard, the parse still answering None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2575 against a baseline of 2575
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    except json.JSONDecodeError:
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_volumes.py, the same lookup read through the module as every name of it in a part is
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _session()._MAPPED_REASONS.get(status.state, "mapped-volume-mismatch")
```

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record`
  - `tests/test_write_session.py::test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it`

Old text:

```
        source = preflight.identity_source(probe)
        if source is None:
```

New text:

```
        source = preflight.identity_source(probe)
        if False:
```

### `r44-a.S2_proved_widened`

Let NOT_MOUNTED count as a proved identity, which is the pass set widening by one verdict

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`
  - `tests/test_write_session.py::test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once[MountState.NOT_MOUNTED]`
  - `tests/test_write_session.py::test_the_verdicts_that_prove_a_rule_target_are_spelled_out`

Old text:

```
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)
```

New text:

```
    {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.NOT_MOUNTED,
    }
)
```

### `r44-a.S3_default_to_library`

Hold a rule outside the library root with nothing recorded to the LIBRARY'S identity instead of refusing it

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return cfg.library.volume_id
```

### `r44-a.S4_inside_root_unheld`

Hold a rule inside the library root to nothing of the library's, so a nested foreign volume is judged as unrecorded rather than foreign

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 6 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule`
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_volume_nested_under_the_library_root_is_not_the_library`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    return None
```

### `r44-a.S5_not_destructive`

Assert a rule target at read strength, where an unreadable or unrecorded identity is tolerated

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_rule_target_whose_identity_cannot_be_read_refuses`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`
  - `tests/test_write_session.py::test_the_seams_handed_in_are_the_seams_used`

Old text:

```
                expected_rule_identity(cfg, rule),
                destructive=True,
```

New text:

```
                expected_rule_identity(cfg, rule),
                destructive=False,
```

### `r44-a.S6_oserror_escapes`

Let an OSError from the walk or the identity read escape the gate instead of becoming a refusal

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_volumes.py, the same handler with its comment cut to its rule and reason by the prose pass
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`

Old text:

```
    except OSError as exc:
        # Could not look is its own refusal, not an internal defect.
```

New text:

```
    except KeyboardInterrupt as exc:
        # Could not look is its own refusal, not an internal defect.
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
        rules[index],
        Path(path).parent,
```

New text:

```
        rules[index],
        Path(rules[index].target or "/"),
```

### `r44-a.S8_wording_held_to`

Say the volume was recorded on the rule when the identity compared was the library's

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
    return "the library's volume, which a target inside the library root is held to"
```

New text:

```
    return "the volume recorded on that rule"
```

### `r44-a.S9_offer_to_record_nested`

Offer to record the foreign volume's identity on a rule that recorded none

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
        if rule.volume_id and observed:
```

New text:

```
        if observed:
```

### `u300.S17_mapped_reasons_local`

the mapped volume gate reads the part's own reason table, so a patched table is not read

- File: `src/cratekit/core/session_volumes.py`
- Source: `u300.json`, row `S17_mapped_reasons_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _MAPPED_REASONS[status.state]
```

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    unlisted = session.log_unlisted(unreadable, cfg)
```

New text:

```
    unlisted = False
```

### `r1255.R2_plan_carries_unlisted`

plan_rotation: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R2_plan_carries_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        log_unlisted=found.unlisted,
```

New text:

```
        log_unlisted=False,
```

### `u111-c.C3_inboxed_suffix`

A name ending _inboxed is no longer recognised as a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C3_inboxed_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    if name.endswith(INBOXED_SUFFIX):
```

New text:

```
    if False:
```

### `u111-c.C4_removal_threshold`

A batch in Old is removed after the stale threshold instead of the expired one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C4_removal_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
        action = REMOVE if age > expired_days else KEEP
```

New text:

```
        action = REMOVE if age > stale_days else KEEP
```

### `u111-c.C5_move_threshold`

A batch in INBOX moves only after the expired threshold instead of the stale one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C5_move_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
        action = MOVE if age > stale_days else KEEP
```

New text:

```
        action = MOVE if age > expired_days else KEEP
```

### `u111-c.C6_plan_taken_again`

The write no longer takes the plan again on its own handle and compares digests

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C6_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_inbox_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u111-c.C7_old_creation_planned`

The folder the write creates for Old is not named to the confinement judge

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C7_old_creation_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`

Old text:

```
                created.append(str(old.ID))
```

New text:

```
                pass
```

### `u111-d.C10_two_olds_refused`

Two live Old folders under INBOX are no longer refused, the first is used

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C10_two_olds_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_empty_inbox_still_asks_then_no_old_declared_or_two_olds_are_refused_by_name`

Old text:

```
    if len(olds) > 1:
```

New text:

```
    if len(olds) > 99:
```

### `u111-d.C9_committed_records_only`

A landing record dates its batch whether or not its commit landed

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C9_committed_records_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_landing_record_that_committed_nothing_dates_nothing`

Old text:

```
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
```

New text:

```
        if False:
```

### `u113-c.C7_unproven_import_names`

The rotation reads an intake file's recorded names whether or not its import was proven

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C7_unproven_import_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_a_recorded_name_whose_batch_folder_is_gone_is_left_alone[never-imported]`

Old text:

```
        if session.IMPORT_VERIFIED_KEY in record.detail:
```

New text:

```
        if True:
```

### `u113-c.C9_earliest_name_wins`

The earliest landing of a recorded name ages it, not the latest

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C9_earliest_name_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_the_latest_landing_of_a_name_is_the_one_it_is_aged_by`

Old text:

```
                if name not in by_name or landed >= by_name[name][0]:
```

New text:

```
                if name not in by_name or landed <= by_name[name][0]:
```

### `u166.R2_rotate_reserved`

_classify: let the rotation take Analyze for a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u166.json`, row `R2_rotate_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says`

Old text:

```
    if not in_old and name == native.ANALYZE:
```

New text:

```
    if False:
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_organize_mirror_inbox.py::test_a_passs_dated_account_playlist_is_mirrored_beside_its_batch_under_its_dated_name`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u214.M15_unread_is_not_none`

_classify: say no landing record names an unrecognised playlist even while a session record could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M15_unread_is_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
            if unread
            else
```

New text:

```
            if False
            else
```

### `u214.M16_old_only_under_inbox`

_classify: read a folder named Old inside Old as the Old folder too

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M16_old_only_under_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if old_display is not None and name == old_display:
```

### `u214.M18_folder_unknown`

_batch_folder: read a refused batch folder as absent, so a batch is said to have none

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M18_folder_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
    except OSError:
        return None
```

New text:

```
    except OSError:
        return False
```

### `u214.M19_folder_unread_reason`

_classify: say no batch folder carries the name even while the music folder could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M19_folder_unread_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
            if folder_unread

```

New text:

```
            if False

```

### `u214.M1_old_named_as_old`

_classify: never name the declared Old as Old, so it reads as any folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M1_old_named_as_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if False:
```

### `u214.M20_unread_unlisted`

Landings.unread: say nothing of a log that could not be listed

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M20_unread_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        if self.unlisted:
```

New text:

```
        if False:
```

### `u214.M2_left_row_count`

_classify: count no rows for a left playlist, so the unrecognised label playlist is named without its 36 rows

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M2_left_row_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_payload_shows_each_left_node_with_its_row_count`

Old text:

```
        tracks = _track_count(db, row) if counted else None
```

New text:

```
        tracks = None
```

### `u214.M3_live_left_collected`

live_batches: collect no left node, so the mirror drops them unsaid again

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M3_live_left_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_inbox_unmirrored.py::test_an_undeclared_old_is_named_as_a_folder`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        else:
            left.append(classified)
    return Live(
```

New text:

```
        else:
            pass
    return Live(
```

### `u214.M4_digest_without_count`

identity: digest each left node with its row count, so adding a track to a person's playlist stales the rotation gate

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M4_digest_without_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`

Old text:

```
        "left": [node.identity() for node in plan.left],
```

New text:

```
        "left": [node.to_json() for node in plan.left],
```

### `u214.M5_rotation_old_display`

plan_rotation: pass no Old display, so the rotation plan names Old as a folder and the mirror as Old

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M5_rotation_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
            old_display=old.display,
```

New text:

```
            old_display=None,
```

### `u214.M6_live_old_display`

live_batches: read no Old display, so the mirror names Old as a plain folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M6_live_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
    old_display = declared.intake_old.display if declared.intake_old is not None else None
```

New text:

```
    old_display = None
```

### `u214.M7_label_rows`

Left.label: leave the row count out of the line a person reads

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M7_label_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`

Old text:

```
        rows = f" ({self.tracks} row(s))" if self.tracks is not None else ""
```

New text:

```
        rows = ""
```

### `u307.R8_anchored_root_drops_cutover_step`

rotate.anchored_root: the bridge refusal shared by every INBOX writer no longer names crate tree cutover as its step

- File: `src/cratekit/intake/rotate.py`
- Source: `u307.json`, row `R8_anchored_root_drops_cutover_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_refill.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`
  - `tests/test_inbox_rotate.py::test_an_intake_tree_on_the_bridge_is_refused_naming_the_cutover`

Old text:

```
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
```

New text:

```
                "move the intake tree to the database",
```

### `u307.R9_watched_roots_accepts_empty`

rotate.watched_roots: accept an empty list of analysis roots, so a write's analysis watch watches nothing and reports itself clean

- File: `src/cratekit/intake/rotate.py`
- Source: `u307.json`, row `R9_watched_roots_accepts_empty`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_analyzed.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_empty_analysis_watch_is_refused_for_every_write_that_shares_it`

Old text:

```
    watched = [Path(root) for root in analysis_roots]
    if not watched:
```

New text:

```
    watched = [Path(root) for root in analysis_roots]
    if False:
```

### `a32.J3_bookkeeping_counted_as_moved`

The shared moved column rule counts the binding's bookkeeping columns as moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `a32.json`, row `J3_bookkeeping_counted_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_judge_accepts_values_read_back_as_the_live_tables_types`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    skip = set(planned) | rb_writer.BOOKKEEPING_COLUMNS
```

New text:

```
    skip = set(planned)
```

### `r923.N11_digest_drops_items`

The digest no longer covers the rows and columns the plan fills

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N11_digest_drops_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_random_id_is_replaced_elsewhere`

Old text:

```
                "items": [item.to_json() for item in self.items],
```

New text:

```
                "items": [],
```

### `r923.N12_digest_drops_values`

The digest no longer covers the values written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N12_digest_drops_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 22622 against a baseline of 22622
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "defaults": {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()},

```

New text:

```
(empty)
```

### `r923.N13_judge_compares_raw`

The read back compares a default by raw value, so the live table's integer reads as wrong against the binding's string

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N13_judge_compares_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            or str(now[column]) != str(rb_writer.CONTENT_ROW_DEFAULTS[column])
```

New text:

```
            or now[column] != rb_writer.CONTENT_ROW_DEFAULTS[column]
```

### `r923.N2_plan_lists_tombstones`

The repair plans soft deleted rows beside live ones

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N2_plan_lists_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 13 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_plan_that_renumbers_nothing_registers_no_file_id_policy`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
            ""
```

### `r923.N3_plan_sees_no_null`

The repair never finds a NULL default, so it plans nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N3_plan_sees_no_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 8 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        missing = tuple(column for column in COLUMNS if row[column] is None)
```

New text:

```
        missing = tuple(column for column in COLUMNS if False)
```

### `r923.N4_stale_fill_accepted`

A planned column set since the plan is written over anyway

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N4_stale_fill_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`

Old text:

```
        if filled:
```

New text:

```
        if False:
```

### `r923.N5_stale_tombstone_accepted`

A row soft deleted since the plan is still written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N5_stale_tombstone_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-row-deleted]`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `r923.N6_judge_blind_to_wrong`

The read back no longer names a planned column that did not take its default

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N6_judge_blind_to_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`

Old text:

```
        if off:
```

New text:

```
        if False:
```

### `r923.N7_judge_blind_to_moved`

The read back no longer names a column outside the plan that moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N7_judge_blind_to_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r923.N8_read_back_never_refuses`

assert_read_back returns whatever the read back found

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N8_read_back_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-moved-column]`
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-wrong-value]`

Old text:

```
    if not written.wrong and not written.moved:
        return
```

New text:

```
    if True:
        return
```

### `u115.F11_stale_file_id_not_checked`

A file id changed since the plan is written over without a staleness refusal

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F11_stale_file_id_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-file-id-renumbered]`

Old text:

```
        if item.renumbers and str(row.get(FILE_ID) or "").strip() != item.file_id_was:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

New text:

```
        if False:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

### `u115.F12_read_back_ignores_file_id`

The read back never checks that the inode took, so a renumber that did not land reads as written

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F12_read_back_ignores_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_renumber_that_did_not_take`

Old text:

```
        if item.renumbers and str(now.get(FILE_ID) or "").strip() != str(item.file_id):
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

New text:

```
        if False:
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

### `u115.F13_planned_renumber_read_as_moved`

The read back forgets the file id was planned, so every renumber is reported as a column the guard let move

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F13_planned_renumber_read_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            planned.add(FILE_ID)
```

New text:

```
        if False:
            planned.add(FILE_ID)
```

### `u115.F14_renumber_never_written`

The apply fills the defaults and never writes the planned file id

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F14_renumber_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            writes.append((file_owner, FILE_ID, item.file_id))
```

New text:

```
        if False:
            writes.append((file_owner, FILE_ID, item.file_id))
```

### `u115.F17_bound_is_zero`

The volume's inode bound is reported as zero rather than measured from a fresh file

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F17_bound_is_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22622 against a baseline of 22622
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        inode=measured.st_ino, device=measured.st_dev, filesystem=filesystem_of(directory)
```

New text:

```
        inode=0, device=measured.st_dev, filesystem=filesystem_of(directory)
```

### `u115.F21_other_volume_compared`

A file on another volume than the bound is stat'ed and its inode compared, so rekordbox's rows there can be renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F21_other_volume_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`

Old text:

```
    if found.st_dev != device:
        return None, ON_ANOTHER_VOLUME
```

New text:

```
    if False:
        return None, ON_ANOTHER_VOLUME
```

### `u115.F22_off_apfs_decides`

The bound is trusted on any filesystem, so an exFAT or HFS+ library has rekordbox's rows renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F22_off_apfs_decides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`

Old text:

```
        if self.filesystem != APFS:
            named = self.filesystem or "unknown"
```

New text:

```
        if False:
            named = self.filesystem or "unknown"
```

### `u115.F23_loose_digits`

A signed or underscored text, or a digit from another script, is parsed as a number and judged above the bound

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F23_loose_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[+200000000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[300_000_000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663-within]`

Old text:

```
    if not (text.isascii() and text.isdigit()):
        return WITHIN
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    try:
        number = int(text)
    except ValueError:
        return WITHIN
    return ABOVE if number > bound else WITHIN
```

### `u115.F5_bound_boundary`

An id equal to the bound is judged above it

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F5_bound_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE if int(text) >= bound else WITHIN
```

### `u115.F6_every_id_above`

Every nonzero id is judged above the bound, so stale rows rekordbox tolerates are renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F6_every_id_above`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 12 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[1-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE
```

### `u115.F7_zero_is_not_zero`

A stored 0 is no longer read as the zero form rekordbox tolerates

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F7_zero_is_not_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero1]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`

Old text:

```
    if text in ("", "0"):
        return ZERO
```

New text:

```
    if text == "":
        return ZERO
```

### `u115.F8_matching_inode_renumbered`

A row above the bound whose file reads the same inode is renumbered to itself rather than left

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F8_matching_inode_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22622 against a baseline of 22622
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            elif str(inode) == str(row[FILE_ID]).strip():
                matched += 1
```

New text:

```
            elif False:
                matched += 1
```

### `u115.F9_unreadable_file_dropped_silently`

A row above the bound whose file cannot be read is neither listed nor written, and the gate says nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F9_unreadable_file_dropped_silently`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            if inode is None:
                unrenumbered.append(
```

New text:

```
            if False:
                unrenumbered.append(
```

### `u298.H24_record_commit_nothing_written`

record_commit: a run that wrote nothing claims a commit a restore would discard

- File: `src/cratekit/write/row_defaults.py`
- Source: `u298.json`, row `H24_record_commit_nothing_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_row_write_that_wrote_nothing_claims_no_commit`

Old text:

```
    if written <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `u302.W10_empty_watch_accepted`

watched_roots: a watch over no roots is accepted, so the session reports itself clean

- File: `src/cratekit/write/row_defaults.py`
- Source: `u302.json`, row `W10_empty_watch_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_repair_link.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_apply_refuses_an_empty_watch_before_touching_the_database`

Old text:

```
    watched = [Path(root) for root in analysis_roots]
    if not watched:
```

New text:

```
    watched = [Path(root) for root in analysis_roots]
    if False:
```

