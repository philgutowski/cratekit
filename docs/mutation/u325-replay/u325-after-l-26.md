# Mutation table: u325-after-l-26

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 116.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 32, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r703-a.A1_classifier_reads_text` | `src/cratekit/acquire/adapter.py` | user | 7 file(s) | 872 | 1 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 3 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 5 | killed |
| `u208.M20_adapter_stale_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `u208.M21_adapter_every_choice_a_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `u208.M22_adapter_hearts_half` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `u197-m6.M6_composite` | `src/cratekit/core/config.py` | user | 3 file(s) | 815 | 2 | killed |
| `r572.L1_local_track_drop_album` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `r572.S1_album_not_read` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 3 | killed |
| `r879-b.T1_one_track_never_asked_to_agree` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 236 | 1 | killed |
| `r746-a.G1_asking_for_any_table_is_not_refused` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 234 | 5 | killed |
| `r746-a.G2_admitted_row_judged_without_the_column_policy` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 234 | 11 | killed |
| `r746-a.G8_key_dropped_from_the_content_policy` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 233 | collection error | collect-error |
| `u156.L23_label_beside_manifest` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 117 | 2 | killed |
| `u156.L18_digest_native` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 5 | killed |
| `u156.L19_write_called` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 21 | killed |
| `u156.L20_recorded` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 3 | killed |
| `u169.N1_relative_read_against_cwd` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N2_empty_root_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u169.N3_missing_folder_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N4_name_apply_bypasses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u147-c.M14_made_in_mirror` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 1 | killed |
| `u147-c.M15_malformed_mirrors_read` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 1 | killed |
| `u147-c.M16_folder_made_twice` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 2 | killed |
| `u147-c.M17_playlist_made_twice` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 5 | killed |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r837-a.A7_reserve_reuses_recorded` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 406 | 1 | killed |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 406 | 20 | killed |
| `r770-a.A1_switch_reads_the_other_mode` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 106 | 77 | killed |
| `r770-b.B2_gate_asked_before_the_acknowledgment` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 106 | 2 | killed |
| `r770-b.B3_an_abort_writes` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 106 | 2 | killed |
| `r770-d.C7_unresolved_target_planned_as_an_add` | `src/cratekit/intake/native.py` | user | 2 file(s) | 106 | 1 | killed |
| `r1313.I1_cache_failure_alone` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 401 | 5 | killed |
| `r1313.I2_cache_keeps_any_status` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 401 | 3 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1434.S2_positions_compare_every_track_listed` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 2 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 753 | 3 | killed |
| `r1305.L1_login_name_on_any_link` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `r1305.L2_login_status_declared_only` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 5 | killed |
| `r1305.L3_login_name_dropped` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `u145.M2_placement_undated` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 97 | 21 | killed |
| `u153.P3_writes_colours` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 97 | 4 | killed |
| `u153.P4_identity_pink` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 97 | 1 | killed |
| `u153.P5_recolour_dedup` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 97 | 3 | killed |
| `u284.T1_pass_names_nothing` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u284.T2_pass_stop_unsaid` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u27-reports-round-3-fixes.F4_absent_flag_never_set` | `src/cratekit/deletion/trash.py` | user | 2 file(s) | 744 | 1 | killed |
| `u278.M24_label_sync_not_narrowed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `u278.M25_sweep_never_refuses` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `u128-b.N3_native_owned_not_found` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 5 | killed |
| `u128.L2_native_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 2 | killed |
| `u113-c.C3_native_found_by_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 1 | killed |
| `u113-c.C4_native_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 4 | killed |
| `u113-c.C5_removed_node_holds_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1255.R3_rotation_warning_gate` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 89 | 3 | killed |
| `r1255.R4_rotation_warning_wording` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 89 | 2 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 2 | killed |
| `r1255.R2_plan_carries_unlisted` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 1 | killed |
| `r1305.A1_account_name_on_any_link` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 1 | killed |
| `r1305.A2_account_status_declared_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 6 | killed |
| `r1305.A4_account_reads_its_own_link_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 7 | killed |
| `u108-c.G21_listing_skips_already` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 2 | killed |
| `u108-c.G22_listing_excuse_applies` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 1 | killed |
| `r432-b.B5_lock_on_the_library_volume` | `src/cratekit/core/config.py` | user | 4 file(s) | 360 | 30 | killed |
| `r432-b.B6_lock_directory_renamed` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 360 | 1 | killed |
| `u82-a.A1_stat_oserror_is_the_refusal` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 4 | killed |
| `u82-a.A2_a_folder_is_not_a_file` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A3_an_empty_file_is_not_proof` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 2 | killed |
| `u180.M11_new_month_seated` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 6 | killed |
| `u180.M12_new_month_knows_the_source` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 5 | killed |
| `u180.M13_never_above_all_favorites` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 1 | killed |
| `r835-a.L1_load_carries_the_label_map` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 350 | 28 | killed |
| `r835-a.L3_recorded_year_never_created_again` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 350 | 4 | killed |
| `u128-b.B1_engine_stale_unchecked` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 344 | 1 | killed |
| `u128-b.B2_foreign_host_indexed` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 344 | 1 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 336 | 2 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 336 | 2 | killed |
| `u270.J2_claim_batch_order` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 167 | 22 | killed |
| `u270.J3_park_releases_the_batch` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 167 | 4 | killed |
| `u270.J4_signal_releases_the_batch` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 167 | 1 | killed |
| `r770-a.A3_assertion_refuses_nothing` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 47 | 4 | killed |

## Row definitions

### `r703-a.A1_classifier_reads_text`

classify_unavailable no longer holds NoFileLanded transient by type

- File: `src/cratekit/acquire/adapter.py`
- Source: `r703-a.json`, row `A1_classifier_reads_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`, `tests/test_provider_gate.py`
- Collected: 872 against a baseline of 872
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT

```

New text:

```
(empty)
```

### `u110-c.C8_plain_dot`

A name starting with a dot passes the plain name rule

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C8_plain_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 262 against a baseline of 262
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_landing.py::test_a_batch_name_that_is_not_one_plain_folder_is_refused[..]`
  - `tests/test_landing.py::test_a_batch_name_that_is_not_one_plain_folder_is_refused[.hidden]`

Old text:

```
        and not text.startswith(".")

```

New text:

```
(empty)
```

### `u208.M19_adapter_never_records_tie`

match_track: never record a broken tie

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M19_adapter_never_records_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
                    elif tied:
                        self._ties.add(key)
```

New text:

```
                    elif False:
                        self._ties.add(key)
```

### `u208.M20_adapter_stale_tie`

match_track: keep the last match's tie flag across a later match of the same row

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M20_adapter_stale_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`

Old text:

```
        self._ties.discard(key)
```

New text:

```
        pass
```

### `u208.M21_adapter_every_choice_a_tie`

_among: call every any_agreeing choice a broken tie, an album naming one included

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M21_adapter_every_choice_a_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", True
```

### `u208.M22_adapter_hearts_half`

_among: drop the hearts half of the tie flag, so two hearts the album narrows to one are not a tie

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M22_adapter_hearts_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", len(narrowed) > 1
```

### `r1255.S3_log_file_absent`

_listed: read a log path that is itself a file as not there, so it is no record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S3_log_file_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_path_that_is_a_file_is_there_and_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        return None
```

### `r1255.S4_under_a_file_unread`

_listed: read a log under a file as there and refused, rather than not there

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S4_under_a_file_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_under_a_file_is_not_there`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        raise
```

### `u197-m6.M6_composite`

What the default does hold: default to the alternative, a name the fold leaves alone, so a fresh configuration selects streamrip

- File: `src/cratekit/core/config.py`
- Source: `u197-m6.json`, row `M6_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`
- Collected: 815 against a baseline of 815
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_configured_adapter_name_resolves_through_the_registry`
  - `tests/test_config.py::test_the_vendored_adapter_is_the_default_under_its_neutral_name`

Old text:

```
    adapter: str = "vendored"
```

New text:

```
    adapter: str = "streamrip"
```

### `r572.L1_local_track_drop_album`

local_tracks stops carrying the file's album

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `L1_local_track_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`

Old text:

```
            isrc=found.isrc,
            album=found.album,
            release_title=release_title(entry, template=template),
        )
```

New text:

```
            isrc=found.isrc,
            release_title=release_title(entry, template=template),
        )
```

### `r572.S1_album_not_read`

file_identity drops the album it read

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `S1_album_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`
  - `tests/test_outbound_workers.py::test_the_files_album_is_read_beside_its_isrc_in_one_read`

Old text:

```
        album=str(read["album"] or "").strip(),
```

New text:

```
        album="",
```

### `r879-b.T1_one_track_never_asked_to_agree`

TidalAccount.match_track: return one track under a code whether or not agree is asked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r879-b.json`, row `T1_one_track_never_asked_to_agree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_code_asked_to_agree_lists_its_one_track_only_when_it_is_the_row`

Old text:

```
                if len(tracks) == 1 and not agree:
```

New text:

```
                if len(tracks) == 1:
```

### `r746-a.G1_asking_for_any_table_is_not_refused`

guard_violations: a creation asked for in a table outside ADMITTABLE_ROW_TABLES is no longer itself a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G1_asking_for_any_table_is_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 234 against a baseline of 234
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdBeatGrid]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdLabel]`

Old text:

```
    for table in sorted(creatable - ADMITTABLE_ROW_TABLES):
        violations.append(
```

New text:

```
    for table in ():
        violations.append(
```

### `r746-a.G2_admitted_row_judged_without_the_column_policy`

guard_violations: an admitted content row may declare any column, the ten included

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G2_admitted_row_judged_without_the_column_policy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 234 against a baseline of 234
- Kills: 11 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitDepth]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[CueUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[ImagePath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[KeyID]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[SampleRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_creation_still_refuses_a_second_content_row_nobody_asked_about`

Old text:

```
            declared = {column for column in columns if column in CONTENT_ROW_EMPTY_COLUMNS}
```

New text:

```
            declared = set()
```

### `r746-a.G8_key_dropped_from_the_content_policy`

CONTENT_ROW_EMPTY_COLUMNS: KeyID is no longer a column a new content row must leave empty

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G8_key_dropped_from_the_content_policy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 233 against a baseline of 234
- Kills: 1 (collect-error)
- Note: collection changed: 233 collected against a baseline of 234. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_wider_content_policy_contains_the_playlist_policy`

Old text:

```
        "KeyID",
        "SampleRate",
```

New text:

```
        "SampleRate",
```

### `u156.L23_label_beside_manifest`

_label_flag: accept --label beside --manifest, so one of two answers silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L23_label_beside_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_label_beside_a_manifest_is_refused_before_the_gate`
  - `tests/test_intake_land_labels_native.py::test_label_from_tags_beside_another_label_source_is_refused_before_the_gate[--manifest]`

Old text:

```
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

New text:

```
    if False:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

### `u156.L18_digest_native`

native.identity: leave the label plan out of the landing's digest

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L18_digest_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`
  - `tests/test_intake_land_labels_native.py::test_an_answer_given_for_one_label_is_stale_for_another`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_between_one_label_and_each_files_own`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_label`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_manifests_bytes`

Old text:

```
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
```

New text:

```
    filed = {}
```

### `u156.L19_write_called`

apply_rows: plan the labels and never write them

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L19_write_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 21 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_file_two_rows_file_in_two_years_names_both_on_its_item`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_with_its_label_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_left_in_staging_is_not_said_to_be_in_the_intake_playlist`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
```

New text:

```
                labels_written = None
```

### `u156.L20_recorded`

_record_landing_commit: write the labels and record nothing of them on the session

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L20_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_year_filed_and_counts_it_under_the_catalogue_tree`

Old text:

```
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
```

New text:

```
    if False:
        label_filing.record_commit(record, labels_written, cfg)
```

### `u169.N1_relative_read_against_cwd`

root_path: take a relative root as it is, read under the working directory, the base's reading

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N1_relative_read_against_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_a_relative_root_is_read_against_the_library_root`
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`
  - `tests/test_root_option.py::test_repair_paths_scans_a_relative_root_inside_the_library`

Old text:

```
    return named if named.is_absolute() else library / named
```

New text:

```
    return named
```

### `u169.N2_empty_root_accepted`

root_path: read an empty root as the working directory instead of refusing it

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N2_empty_root_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_an_empty_root_is_refused_rather_than_read_as_the_working_directory[   ]`
  - `tests/test_root_option.py::test_an_empty_root_is_refused_rather_than_read_as_the_working_directory[]`

Old text:

```
    if not given.strip():
```

New text:

```
    if False:
```

### `u169.N3_missing_folder_accepted`

root_folder: accept a folder that is not there

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N3_missing_folder_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_file_where_the_folder_should_be_is_refused`
  - `tests/test_root_option.py::test_a_missing_absolute_root_refuses_naming_it`
  - `tests/test_root_option.py::test_a_missing_library_root_is_refused_when_no_root_was_given`
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_paths_refuses_a_root_with_no_folder`

Old text:

```
    if tried.is_dir():
        return tried
```

New text:

```
    if True:
        return tried
```

### `u169.N4_name_apply_bypasses`

name apply: read --root as the base did, bypassing the helper

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N4_name_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`

Old text:

```
    root = root_folder(ctx.args.root, cfg, verb="name apply")
```

New text:

```
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
```

### `u147-c.M14_made_in_mirror`

ledger._made_in: a mirrored playlist is no longer vouched for, so no track may come off it (R-836)

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M14_made_in_mirror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`

Old text:

```
    # U147. A mirrored playlist is only ever created, never adopted.
    for record in document["mirrors"].values():
        for entry in (record.get("playlists") or {}).values():
            if str(entry.get("remote_id") or "") == wanted:
                return True

```

New text:

```
(empty)
```

### `u147-c.M15_malformed_mirrors_read`

ledger._load: a malformed mirror record is read rather than refused

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M15_malformed_mirrors_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_malformed_mirror_record_refuses_rather_than_reading_as_none`

Old text:

```
        raise _unusable(path, "mirrors must be a map of mirrored folder records")
```

New text:

```
        mirrors = {}
```

### `u147-c.M16_folder_made_twice`

ledger.reserve_mirror_folder: a recorded folder is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M16_folder_made_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        record = _mirror_entry(document, name)
        recorded = str(record.get("folder_id") or "")
        if recorded and recorded != stale:
            return recorded, False

```

New text:

```
        record = _mirror_entry(document, name)
        recorded = str(record.get("folder_id") or "")

```

### `u147-c.M17_playlist_made_twice`

ledger.reserve_mirror_playlist: a recorded playlist is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M17_playlist_made_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        playlists = _mirror_entry(document, folder)["playlists"]
        recorded = str((playlists.get(name) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False

```

New text:

```
        playlists = _mirror_entry(document, folder)["playlists"]

```

### `u147-c.M19_sweep_handoff`

sync.cli: the sync source hands the sweep no mirrored playlist

- File: `src/cratekit/sync/cli.py`
- Source: `u147-c.json`, row `M19_sweep_handoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_sync_pass_hands_the_sweep_every_mirrored_playlist`

Old text:

```
            mirrored=mirrored,
```

New text:

```
(empty)
```

### `r837-a.A7_reserve_reuses_recorded`

ledger.reserve_set_playlist: a recorded set playlist is not reused, so the create runs again

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A7_reserve_reuses_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`

Old text:

```
        recorded = str((document["sets"].get(name) or {}).get("remote_id") or "")
        if recorded:
```

New text:

```
        recorded = str((document["sets"].get(name) or {}).get("remote_id") or "")
        if False:
```

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 406 against a baseline of 406
- Kills: 20 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_archive_with_no_landed_file_refuses_before_anything`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `r770-a.A1_switch_reads_the_other_mode`

IntakeMedium.native: answer native for a tree on the bridge and bridge for a native one

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A1_switch_reads_the_other_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 106 against a baseline of 106
- Kills: 77 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_changed_playlist_or_an_added_file_still_moves_the_digest`
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - ... and 62 more, see the JSON sidecar

Old text:

```
        return self.registry.is_database_native(self.declared.intake.id)
```

New text:

```
        return self.registry.is_on_the_bridge(self.declared.intake.id)
```

### `r770-b.B2_gate_asked_before_the_acknowledgment`

ask_then_write: ask the gate without reading the backup acknowledgment first, on both verbs

- File: `src/cratekit/intake/land_cli.py`
- Source: `r770-b.json`, row `B2_gate_asked_before_the_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 106 against a baseline of 106
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_acknowledgment_refuses_before_the_gate`
  - `tests/test_intake_writers_native.py::test_no_acknowledgment_refuses_before_the_gate`

Old text:

```
        session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r770-b.B3_an_abort_writes`

ask_then_write: write whatever the answer was

- File: `src/cratekit/intake/land_cli.py`
- Source: `r770-b.json`, row `B3_an_abort_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 106 against a baseline of 106
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_abort_moves_nothing_and_writes_nothing`
  - `tests/test_intake_writers_native.py::test_an_abort_writes_nothing`

Old text:

```
        if option != "apply":
```

New text:

```
        if option == "never":
```

### `r770-d.C7_unresolved_target_planned_as_an_add`

native.plan_rows: read a target the matcher could not resolve as a file the collection does not hold

- File: `src/cratekit/intake/native.py`
- Source: `r770-d.json`, row `C7_unresolved_target_planned_as_an_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add`

Old text:

```
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
```

New text:

```
        if False:
```

### `r1313.I1_cache_failure_alone`

said_not_found: read the 404 off the failure alone, as before R-1313, so an ISRC answered with a 404 page is never kept

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I1_cache_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 401 against a baseline of 401
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.I2_cache_keeps_any_status`

said_not_found: keep any failure carrying a status, so an outage is remembered for a week as filed under nothing

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I2_cache_keeps_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 401 against a baseline of 401
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[500-json-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[503-empty-isrc_cache]`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return answered_not_found(exc) or getattr(getattr(exc, "response", None), "status_code", None) is not None
```

### `r1418.F7_composite_ordering_start_unread`

what F7 holds: a stopped write with no moving step reads no start from its ordering step, so the start F7 narrows is never read

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1418.json`, row `F7_composite_ordering_start_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 20 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_stopped.py::test_a_write_begun_ordered_and_not_finished_is_read_back_whole`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    begin = sent[1] if sent is not None else start
```

New text:

```
    begin = sent[1] if sent is not None else ()
```

### `r1434.S2_positions_compare_every_track_listed`

existing guard, U225: the path compares every track listed now, a track added since included, so an addition reads the account off the path

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1434.json`, row `S2_positions_compare_every_track_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current)
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 753 against a baseline of 753
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

### `r1305.L1_login_name_on_any_link`

_rejected: read the client's authentication error by name on any link, so a reset met while handling one asks for a login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L1_login_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_authentication_error_reached_only_as_context_is_a_wait`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if type(link).__name__ == "AuthenticationError":
            return True
    return False

```

### `r1305.L2_login_status_declared_only`

_rejected: read a status on the declared chain only, so a login answered 401 or 403 with a page is told to wait

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L2_login_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[400-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_with_a_page_tells_the_person_to_log_in_again`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`

Old text:

```
        if answered_status(link) in REJECTED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in REJECTED_STATUSES:
```

### `r1305.L3_login_name_dropped`

_rejected: drop the client's authentication error by name, a sample of the guard as it stood before R-1305

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L3_login_name_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[client-auth-error]`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if False:
            return True
    return False

```

### `u145.M2_placement_undated`

plan_placements: every heart is planned into Undated, its date ignored

- File: `src/cratekit/favorites/placement.py`
- Source: `u145.json`, row `M2_placement_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 97 against a baseline of 97
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        month = placeholders.month_label(hearted)
```

New text:

```
        month = placeholders.month_label(None)
```

### `u153.P3_writes_colours`

PlacementPlan.writes: ignore the colour count, so a colour-only plan reports no write and ends NO_OP

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P3_writes_colours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
        return self.adds > 0 or self.colours > 0
```

New text:

```
        return self.adds > 0
```

### `u153.P4_identity_pink`

identity: drop the Pink row from the digest, so a colour change between plan and write is not caught

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P4_identity_pink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
            "pink": self.pink,
```

New text:

```
            "pink": "",
```

### `u153.P5_recolour_dedup`

plan_placements recolour: drop the not-in-seen check, so a heart also named as a recolour is listed twice

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P5_recolour_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`

Old text:

```
            if row in titles and row not in seen
```

New text:

```
            if row in titles
```

### `u284.T1_pass_names_nothing`

tail.tail_step: the pass never names the files the catalogues refused

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T1_pass_names_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files`

Old text:

```
    if step == TAG:
        refused_files(chain, chain.settled.get(step))
```

New text:

```
    if False:
        refused_files(chain, chain.settled.get(step))
```

### `u284.T2_pass_stop_unsaid`

tail.tail_step: the pass's stop at its tag step says nothing of who refused or the token

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T2_pass_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        raise Stop(step, refused_stop(error, chain.settled.get(step)) if step == TAG else error)
```

New text:

```
        raise Stop(step, error)
```

### `u27-reports-round-3-fixes.F4_absent_flag_never_set`

Never mark an absent Trash as absent, so doctor cannot tell it from an unwritable one

- File: `src/cratekit/deletion/trash.py`
- Source: `u27-reports-round-3-fixes.json`, row `F4_absent_flag_never_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_doctor.py`
- Collected: 744 against a baseline of 744
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_two_probe_answers_that_made_the_false_red_are_really_different`

Old text:

```
            absent=not target.exists(),
```

New text:

```
            absent=False,
```

### `u278.M24_label_sync_not_narrowed`

label sync: ask and walk spend the reserve

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M24_label_sync_not_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if not args.go:
        provider_gate.reading(
```

New text:

```
    if False:
        provider_gate.reading(
```

### `u278.M25_sweep_never_refuses`

label sync: the estimate never refuses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M25_sweep_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if calls > left:
```

New text:

```
    if False:
```

### `u128-b.N3_native_owned_not_found`

The native verb asks no candidate row for the owned tracks, so every one is left

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128-b.json`, row `N3_native_owned_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`

Old text:

```
        cfg, named, native.candidate_rows(db, names)
```

New text:

```
        cfg, named, ()
```

### `u128.L2_native_warning_unsaid`

The native landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128.json`, row `L2_native_warning_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    warnings.extend(account_playlists.left_warning(landed.collection.left))
```

New text:

```
    warnings.extend(account_playlists.left_warning(()))
```

### `u113-c.C3_native_found_by_name`

An account playlist is found by its name under INBOX and added to, rather than created

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C3_native_found_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
                created = db.create_playlist(one.name, parent=anchor)
```

New text:

```
                created = rb_writer.ensure_playlist(db, one.name, anchor)
```

### `u113-c.C4_native_record_unnamed`

The native landing record does not list the account playlists by identifier

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C4_native_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
```

### `u113-c.C5_removed_node_holds_name`

A removed node under INBOX still holds its name, so a free exact name takes a count

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C5_removed_node_holds_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
        if not rb_writer.node_removed(row):
```

New text:

```
        if True:
```

### `r1255.R3_rotation_warning_gate`

records_warnings: never warn, so the rotation ages a batch from its playlist's date unsaid

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R3_rotation_warning_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_records_it_could_not_read_as_it_did`

Old text:

```
    if not plan.unreadable_records:
        return []
    unread = (
```

New text:

```
    if True:
        return []
    unread = (
```

### `r1255.R4_rotation_warning_wording`

records_warnings: word an unlisted log as a count of records

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R4_rotation_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list`

Old text:

```
        if plan.log_unlisted
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

New text:

```
        if False
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
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
- Collected: 89 against a baseline of 89
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

### `r1305.A1_account_name_on_any_link`

_session_refused: read the client's authentication error by name on any link, so a reset met while handling one drops the account and asks for a login

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A1_account_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_an_authentication_error_reached_only_as_context_is_not_a_rejected_session`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
```

New text:

```
        if type(link).__name__ == "AuthenticationError":
```

### `r1305.A2_account_status_declared_only`

_session_refused: read a status on the declared chain only, so a session rejected mid sweep with a page is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A2_account_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_outage_met_while_handling_a_rejected_session_is_a_wait`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login`

Old text:

```
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `r1305.A4_account_reads_its_own_link_only`

_session_refused: read the failure alone and no link of it, so a rejection the client rewraps is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A4_account_reads_its_own_link_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session`
  - `tests/test_provider_rejection_bodies.py::test_a_login_outage_met_while_handling_a_rejected_session_is_a_wait`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login`

Old text:

```
    for link, declared in failure_links(exc):
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
    for link, declared in [(exc, True)]:
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `u108-c.G21_listing_skips_already`

approved_cli.list_releases: a track another job already holds is listed again

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G21_listing_skips_already`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            elif str(settled.wanted.ref or "").strip() in already:
```

New text:

```
            elif False:
```

### `u108-c.G22_listing_excuse_applies`

approved_cli.list_releases: an excused failure kind still refuses an empty listing

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G22_listing_excuse_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
    unexcused = [one for one in failures if one.kind not in excuse]
```

New text:

```
    unexcused = list(failures)
```

### `r432-b.B5_lock_on_the_library_volume`

config: declare the landing locks library scoped, which puts them on the volume that is commonly exFAT

- File: `src/cratekit/core/config.py`
- Source: `r432-b.json`, row `B5_lock_on_the_library_volume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`, `tests/test_config.py`
- Collected: 360 against a baseline of 360
- Kills: 30 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_does_not_stop_anybody_reading_the_plan`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_intake_land.py::test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output`
  - `tests/test_intake_land.py::test_another_spelling_of_a_held_batch_folder_is_refused`
  - `tests/test_intake_land.py::test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared`
  - `tests/test_intake_land.py::test_the_folder_defaults_to_staging_the_batch_to_the_date_and_the_file_to_the_run`
  - `tests/test_intake_land.py::test_the_landed_envelope_carries_an_import_that_blocks_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_held_for_the_whole_of_the_apply`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        key="landing_locks",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.INSTALLATION,
```

New text:

```
        key="landing_locks",
        snapshot=SnapshotRole.NEVER_RESTORED,
        root=StateRoot.LIBRARY,
```

### `r432-b.B6_lock_directory_renamed`

config: move the landing locks to another directory name under the state root

- File: `src/cratekit/core/config.py`
- Source: `r432-b.json`, row `B6_lock_directory_renamed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`, `tests/test_config.py`
- Collected: 360 against a baseline of 360
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_batch_lock_is_on_the_state_disk_and_never_under_the_library`

Old text:

```
        relative="landing_locks",
```

New text:

```
        relative="landings",
```

### `u82-a.A1_stat_oserror_is_the_refusal`

require_output: stop turning an OSError out of the one stat into sync-marks-blocked, so a file gone at that moment is a bare FileNotFoundError again, which is R-398

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A1_stat_oserror_is_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    except OSError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

### `u82-a.A2_a_folder_is_not_a_file`

require_output: drop the regular file check, so a folder named like the intake file counts as the importable file

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A2_a_folder_is_not_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if not stat.S_ISREG(found.st_mode):
```

New text:

```
    if False:
```

### `u82-a.A3_an_empty_file_is_not_proof`

require_output: drop the empty file check, so a zero byte file lets the renames through

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A3_an_empty_file_is_not_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if found.st_size == 0:
```

New text:

```
    if False:
```

### `u180.M11_new_month_seated`

month_row: a month made under the folder is left at the end, the behaviour before U180

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M11_new_month_seated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
- Kills: 6 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    if parent is not None:
        _seat_new(db, made, parent_id, source_id)
```

New text:

```
    if False:
        _seat_new(db, made, parent_id, source_id)
```

### `u180.M12_new_month_knows_the_source`

_seat_new: the month just made is ranked as any other playlist, so it is seated at the end of the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M12_new_month_knows_the_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    mine = rank(made, source_id)
```

New text:

```
    mine = (placeholders.RANK_OTHER, 0)
```

### `u180.M13_never_above_all_favorites`

_seat_new: the slot is looked for from the top of the folder, so a month can be seated above All Favorites, the round one finding

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M13_never_above_all_favorites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`

Old text:

```
        (n for n, row in enumerate(others) if n >= floor and rank(row, source_id) > mine),
```

New text:

```
        (n for n, row in enumerate(others) if rank(row, source_id) > mine),
```

### `r835-a.L1_load_carries_the_label_map`

ledger._load: the label map is dropped on load, so any other write to the ledger forgets every label's folder and year playlists

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L1_load_carries_the_label_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 350 against a baseline of 350
- Kills: 28 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        "labels": {str(key): _label_document(path, value) for key, value in labels.items()},
```

New text:

```
        "labels": {},
```

### `r835-a.L3_recorded_year_never_created_again`

ledger.reserve_label_year: a year already recorded is created again, so a resumed build makes a second playlist for it

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L3_recorded_year_never_created_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 350 against a baseline of 350
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        recorded = str((years.get(year) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
```

New text:

```
        recorded = str((years.get(year) or {}).get("remote_id") or "")
        if False:
            return recorded, False
```

### `u128-b.B1_engine_stale_unchecked`

The bridge engine does not read the owned entries again before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B1_engine_stale_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 344 against a baseline of 344
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`

Old text:

```
    if now != planned:
```

New text:

```
    if False:
```

### `u128-b.B2_foreign_host_indexed`

Index an export entry whose Location names another machine, which raises out of the index

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B2_foreign_host_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 344 against a baseline of 344
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`

Old text:

```
        try:
            locations.location_to_path(recorded)
        except locations.LocationDecodeError:
            continue
        found.append
```

New text:

```
        found.append
```

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 336 against a baseline of 336
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        with _binding_probe(strict=True):
            db.commit()
```

New text:

```
        with nullcontext():
            db.commit()
```

### `u211.W5_probe_wrapped_at_open`

open_db: construct the binding without the careful probe, so the dying process reads as a damaged library

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W5_probe_wrapped_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 336 against a baseline of 336
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

New text:

```
        with nullcontext():
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

### `u270.J2_claim_batch_order`

claim_batch: claim the highest ordinals first, so a batch writes its tracks in the reverse of the crate's order

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J2_claim_batch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 22 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`
  - `tests/test_jobs_batch.py::test_a_batch_is_claimed_in_ordinal_order_up_to_its_size`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_jobs_batch.py::test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other`
  - `tests/test_jobs_batch.py::test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left`
  - `tests/test_jobs_batch.py::test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs`
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            "ORDER BY ordinal LIMIT ?",
```

New text:

```
            "ORDER BY ordinal DESC LIMIT ?",
```

### `u270.J3_park_releases_the_batch`

drive: ignore a Parked among a batch's outcomes, so the batch is settled as failed and the next batch is the second request into a block

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J3_park_releases_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_park_answered_for_one_item_releases_the_whole_batch`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`

Old text:

```
                if parked is not None:
                    release_claims(store, job_id, driver=driver)
```

New text:

```
                if False:
                    release_claims(store, job_id, driver=driver)
```

### `u270.J4_signal_releases_the_batch`

drive: commit a batch answered under a signal, so a stop part way settles what the handler cut short

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J4_signal_releases_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`

Old text:

```
                    return result
                if interrupt.signalled:
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break
                for item in claimed:
```

New text:

```
                    return result
                for item in claimed:
```

### `r770-a.A3_assertion_refuses_nothing`

assert_intake_on_the_bridge: return for every tree, so a splice at a native tree reaches the emitter guard and its report-defect

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A3_assertion_refuses_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 47 against a baseline of 47
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_bridge_apply_on_a_native_tree_moves_nothing_and_keeps_the_splices_cause`
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_intake_tree_naming_the_landing`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_tree_before_it_looks_for_the_export`

Old text:

```
    if not IntakeMedium(declared=declared, registry=registry).native:
```

New text:

```
    if True:
```

