# Mutation table: u325-after-l-21

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 123.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 16, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1017.M6_oldest_first` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M7_names_not_deduplicated` | `src/cratekit/intake/set_playlist.py` | maintainer | 4 file(s) | 195 | 1 | killed |
| `r740-a.N1_no_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 17 | killed |
| `r740-a.N2_no_agreement` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 3 | killed |
| `r740-a.N3_key_compared_raw` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 3 | killed |
| `r740-a.N4_stem_before_title` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 1 | killed |
| `r740-a.N5_no_marker_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 4 | killed |
| `r740-a.N6_current_ignores_filled` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 1 | killed |
| `r740-b.E1_library_name_from_stem` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 4 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_writer.py` | user | 7 file(s) | 327 | 2 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_writer.py` | user | 7 file(s) | 327 | 21 | killed |
| `r1665.W2_failed_copy_passes` | `src/cratekit/core/rb_writer.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.W4_quick_check_ignored` | `src/cratekit/core/rb_writer.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_writer.py` | user | 7 file(s) | 327 | 2 | killed |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 327 | 4 | killed |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72-b.M21_empty_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 3 | killed |
| `u72-b.M22_listing_without_isdir` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 32 | killed |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 3 | killed |
| `u72.M2_empty_plan_applied` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72-b.M23_listing_unfiltered` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 48 | 1 | killed |
| `r791-b.C1_artifact_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 15 | killed |
| `r791-b.C2_artifact_unread` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 6 | killed |
| `r791-b.C3_summary_counts_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 15 | killed |
| `r791-b.C6_not_asked_excluded` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 1 | killed |
| `r791-b.C7_parse_break_said` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 1 | killed |
| `r791-b.C8_one_file` | `src/cratekit/tagging/cli.py` | maintainer | 3 file(s) | 240 | 1 | killed |
| `r791-b.C9_unread_skip_zero_filled` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 11 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 3 | killed |
| `r263.W3_stale_record_as_completion` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `r263.W4_stale_suffix` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `u284-composite.C3x_unread_discogs_and_outage_named` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C1_tagged_file_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C2_outage_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C4_stop_never_collected` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C5_sweep_stop_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C6_token_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 3 | killed |
| `u284.C7_rejected_token_told_to_wait` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u177.B10_land_command` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 3 | killed |
| `u177.B1_seller_by_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 5 | killed |
| `u177.B2_plan_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 12 | killed |
| `u177.B3_unregistered_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u177.B4_labels_of_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u177.B5_registry_unread_empty` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u177.B6_frozen_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 8 | killed |
| `u177.B7_tag_not_written` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 4 | killed |
| `u177.B8_write_false_ignored` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u177.B9_untagged_refusal` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `r815-a.W1_withhold_only_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 5 | killed |
| `r815-a.W2_a_returned_hold_is_not_withheld` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W3_the_floor_is_never_lowered` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W5_a_refresh_keeps_the_withheld_word` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W6_redescribe_only_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 2 | killed |
| `r815-a.G2_forgetting_keeps_the_failure_count` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 214 | 2 | killed |
| `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands` | `src/cratekit/label/judge_cli.py` | user | 2 file(s) | 214 | 1 | killed |
| `u165.A1_scope` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.A2_refuse_unplaced_called` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.A3_grant_first` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.L1_bridge_skip` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 2 | killed |
| `u165.L2_land_only` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 3 | killed |
| `u165.L3_filing_tail` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 4 | killed |
| `u165.L4_files_into` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 2 | killed |
| `u165.N1_digest` | `src/cratekit/intake/native.py` | user | 4 file(s) | 152 | 1 | killed |
| `u261.H3_reuse_swallows_a_missing_session` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 141 | 2 | killed |
| `u261.H4_failed_read_keeps_the_hold` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `u261.H9_no_forget_before_a_new_login` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `u261.R3_raised_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 141 | 1 | killed |
| `u261.A1_account_forget_keeps_the_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 28 | killed |
| `u261.A2_account_reuse_ignores_the_hold` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 3 | killed |
| `u261.A3_account_records_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 5 | killed |
| `u261.A4_refusal_drops_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 5 | killed |
| `u27-round-8-independent.E6_write_table_shares_read` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 3 | killed |
| `r663-a.M10_detail_size_pinned` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 51 | 1 | killed |
| `r663-a.M1_empty_not_refused_before_open` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 4 | killed |
| `r663-a.M3_unlistable_read_as_empty` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M4_one_canary_table_not_enough` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M5_failed_listing_returns_empty_set` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M6_listing_opened_with_the_key_always` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M7_message_drops_the_size` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r663-a.M8_message_names_the_copy` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 5 | killed |
| `r663-a.M9_remedy_restore` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r663-b.M2_every_open_refusal_classified` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 1 | killed |
| `u279.M10_tilde_not_expanded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M11_excluded_anchor_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 2 | killed |
| `u279.M13_wrong_folder_named` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M8_index_call_unexcluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 6 | killed |
| `u279.M9_staging_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 4 | killed |
| `u205.G1_app_call_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 5 | killed |
| `u205.G2_app_rate_limit_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G3_attach_drops_identity` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 6 | killed |
| `u205.G5_app_share_unclamped` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G6_file_account_share_is_the_total` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 2 | killed |
| `u205.G7_process_spend_drops_app` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G8_since_keeps_earlier_app_calls` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 6 | killed |
| `u96-b.C1_engine_terminal` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u96-b.C2_engine_acknowledged` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C4_engine_stub` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 5 | killed |
| `u96-b.C5_engine_library_is_mounted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |

## Row definitions

### `r1017.M6_oldest_first`

Landing records: read them oldest first, which recorded_playlist also depends on

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M6_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=True)
```

New text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=False)
```

### `r1017.M7_names_not_deduplicated`

recorded_names: return a name twice when two landings recorded it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M7_names_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

New text:

```
        list(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

### `r740-a.N1_no_fill`

normalize_spec: never fill a spec field from the stripped head, the R-740 loss itself

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N1_no_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 17 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_landing_head.py::test_a_lossy_file_keeps_its_marker_on_all_three_surfaces`
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_a_title_head_with_no_key_tag_still_lands_whole`
  - `tests/test_landing_head.py::test_a_title_headed_file_with_no_tempo_elsewhere_lands_named_as_its_title`
  - `tests/test_landing_head.py::test_an_off_wheel_key_tag_under_a_headed_title_lands_the_head`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_title_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_in_the_stripped_head_marks_the_spec`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            filled.update(
                (name, value) for name, value in values.items() if current[name] is None
            )
```

New text:

```
            pass
```

### `r740-a.N2_no_agreement`

normalize_spec: fill from the head whatever the spec supplied, so a fresh key takes the old tempo

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N2_no_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_fresh_key_is_never_paired_with_the_tempo_it_replaces`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_off_wheel_key_is_not_completed_into_a_refused_shape`

Old text:

```
        if all(_agrees(name, current[name], values[name]) for name in values):
```

New text:

```
        if True:
```

### `r740-a.N3_key_compared_raw`

_agrees: compare the key as raw text instead of on the wheel, so 8a disagrees with 08A

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N3_key_compared_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`

Old text:

```
        return parsed is not None and parsed == parse_camelot(str(written))
```

New text:

```
        return str(supplied) == str(written)
```

### `r740-a.N4_stem_before_title`

normalize_spec: read the stem head before the title head

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N4_stem_before_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_title_head_is_read_before_the_stem_head`

Old text:

```
    for head, fields in ((title_head, title_fields), (stem_head, stem_fields)):
```

New text:

```
    for head, fields in ((stem_head, stem_fields), (title_head, title_fields)):
```

### `r740-a.N5_no_marker_fill`

normalize_spec: a marker in the stripped head no longer marks the spec, so R21's marker is dropped

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N5_no_marker_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_lossy_file_keeps_its_marker_on_all_three_surfaces`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_in_the_stripped_head_marks_the_spec`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_only_head_marks_the_spec_and_invents_no_field`

Old text:

```
            if rule.literal in head:
                filled[rule.field] = True
```

New text:

```
            if rule.literal in head:
                pass
```

### `r740-a.N6_current_ignores_filled`

normalize_spec: judge the stem head against the spec alone, so it overwrites what the title head filled

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N6_current_ignores_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_title_head_is_read_before_the_stem_head`

Old text:

```
        current = {name: filled.get(name, getattr(spec, name)) for name in values}
```

New text:

```
        current = {name: getattr(spec, name) for name in values}
```

### `r740-b.E1_library_name_from_stem`

existing guard sample: render_all derives the library name from the filename stem instead of the title tag

- File: `src/cratekit/core/naming.py`
- Source: `r740-b.json`, row `E1_library_name_from_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_landing_head.py::test_an_acquired_body_marker_is_not_doubled_into_the_head`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`

Old text:

```
        library_name=title_tag,
```

New text:

```
        library_name=head + spec.stem,
```

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
```

New text:

```
            except RekordboxUnavailable:
                return True
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return True
```

### `r1665.W1_check_opens_the_capture`

integrity_ok: open the file it is given rather than its throwaway copy, the defect itself

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665.json`, row `W1_check_opens_the_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 21 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - `tests/test_intake_land_rehearse.py::test_a_temporary_volume_with_no_room_for_the_rehearsal_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_own_mount_the_rehearsal_is_as_it_was`
  - `tests/test_intake_land_rehearse.py::test_the_rehearsal_digest_equals_the_live_plans_and_the_live_gate_says_so`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                db = open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `r1665.W2_failed_copy_passes`

integrity_ok: a throwaway copy that cannot be made answers True

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665.json`, row `W2_failed_copy_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_whose_copy_cannot_be_made_has_not_passed`

Old text:

```
            exc,
        )
        return False
```

New text:

```
            exc,
        )
        return True
```

### `r1665.W4_quick_check_ignored`

integrity_ok: answer True whatever quick_check says

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665.json`, row `W4_quick_check_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_damage_only_the_consistency_check_sees_fails_the_check`

Old text:

```
                return str(result).lower() == "ok"
```

New text:

```
                return True
```

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except RekordboxUnavailable:
                return False
```

New text:

```
            except RekordboxUnavailable:
                return True
```

### `r1665.R1_log_not_restored`

restore._file_steps: never write back a restored companion, so the log's rows are lost

- File: `src/cratekit/core/restore.py`
- Source: `r1665.json`, row `R1_log_not_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_only_the_companion_the_inventory_declares_restored_is_written_back`
  - `tests/test_restore.py::test_round3_a_staged_log_is_counted_as_permanent_growth`
  - `tests/test_restore.py::test_round3_a_volume_between_the_two_rules_is_refused`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`

Old text:

```
        if entry.source in restored_companions:
            if entry.captured is not None:
```

New text:

```
        if entry.source in restored_companions:
            if False:
```

### `u72-b.M20_shown_files`

The gate context lists no file names

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M20_shown_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_moves_nothing`
  - `tests/test_intake_land.py::test_the_gate_screen_a_person_reads_names_the_files_and_the_intake_file`

Old text:

```
        "files": [item.name for item in planned.items],
```

New text:

```
        "files": [],
```

### `u72-b.M21_empty_to_engine`

An empty folder goes to the engine, which refuses it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M21_empty_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_of_nothing_asks_nothing_of_the_export`
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if False:
```

### `u72-b.M22_listing_without_isdir`

The empty check lists a folder that may not exist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M22_listing_without_isdir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_folder_that_is_not_there_is_refused_before_the_gate`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if not landing.listing(folder):
```

### `u72.M10_default_folder`

The default folder is the library root, not download staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M10_default_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_plan_over_a_usable_export_reaches_the_gate_with_the_digest_it_had_before`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_a_collection_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_without_the_intake_folder_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_intake_land.py::test_a_stale_answer_is_refused_and_moves_nothing`
  - `tests/test_intake_land.py::test_an_abort_is_no_op_and_moves_nothing`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
```

New text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.library.root)
```

### `u72.M1_abort_applies`

An abort no longer stops the verb: only an empty plan returns NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M1_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_an_export_that_went_missing`
  - `tests/test_intake_land.py::test_an_abort_is_no_op_and_moves_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if not planned.items:
```

### `u72.M2_empty_plan_applied`

An empty plan is handed to the engine after the answer instead of returning NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M2_empty_plan_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if option != "apply":
```

### `u72.M3_digest_drops_where`

The digest drops the batch, the target and the intake file, so an answer for one name applies under another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M3_digest_drops_where`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_given_for_one_batch_name_is_stale_for_another`

Old text:

```
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),

```

New text:

```
(empty)
```

### `u72.M5_digest_drops_export`

The digest drops the export path

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M5_digest_drops_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_stale_answer_stays_stale_over_an_export_that_is_not_there`
  - `tests/test_intake_land.py::test_an_answer_given_against_one_export_is_stale_for_another`

Old text:

```
        "export": str(export),

```

New text:

```
(empty)
```

### `u72.M9_default_name_colons`

The default batch name keeps the run id's colons

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M9_default_name_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_folder_defaults_to_staging_the_batch_to_the_date_and_the_file_to_the_run`

Old text:

```
    return run_id.replace(":", "")
```

New text:

```
    return run_id
```

### `u72-b.M23_listing_unfiltered`

The engine's public listing returns every entry, not only audio

- File: `src/cratekit/intake/landing.py`
- Source: `u72-b.json`, row `M23_listing_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    return _list(folder)


def _digest(
```

New text:

```
    return tuple(folder.iterdir())


def _digest(
```

### `r791-b.C1_artifact_answers`

handle: the artifact records only the first source's answer

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C1_artifact_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                for said in result.answers
            ],
```

New text:

```
                for said in result.answers[:1]
            ],
```

### `r791-b.C2_artifact_unread`

handle: the artifact's unread map is always empty

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C2_artifact_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                if said.source in result.unread
```

New text:

```
                if False
```

### `r791-b.C3_summary_counts_answers`

_summary: count no answers

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C3_summary_counts_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                counted[word] += 1
```

New text:

```
                counted[word] += 0
```

### `r791-b.C6_not_asked_excluded`

_unread_warnings: count not-asked as asked, so a Beatport match hides a blocked fallback

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C6_not_asked_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`

Old text:

```
        asked = sum(count for word, count in counted.items() if word != searchers.NOT_ASKED)
```

New text:

```
        asked = sum(count for word, count in counted.items())
```

### `r791-b.C7_parse_break_said`

_unread_warnings: never say a parse break is a defect a rerun will not move

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C7_parse_break_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
                        if broken
                        else ""
```

New text:

```
                        if False
                        else ""
```

### `r791-b.C8_one_file`

_files: say 1 files were

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C8_one_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
    return "1 file was" if count == 1 else f"{count} files were"
```

New text:

```
    return f"{count} files were"
```

### `r791-b.C9_unread_skip_zero_filled`

_summary: count only the three skip reasons that predate R-791

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C9_unread_skip_zero_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
```

New text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS[:3], 0)
```

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r263.W3_stale_record_as_completion`

A stale record on a cursorless source is reported as its last completion again

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W3_stale_record_as_completion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
        if reason is not None:
```

New text:

```
        if reason is not None and mark is None:
```

### `r263.W4_stale_suffix`

Drop the note that an earlier build's cursor no longer moves

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W4_stale_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
            if mark is not None:
                detail += (
```

New text:

```
            if False:
                detail += (
```

### `u284-composite.C3x_unread_discogs_and_outage_named`

tagging.cli._refused_out: the composite for C3's zero, both the Discogs was read guard and the every other catalogue refused guard removed, so any file left with no genre is named as one the catalogues refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284-composite.json`, row `C3x_unread_discogs_and_outage_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if said.get(searchers.DISCOGS) not in (searchers.Answer.MISS.value, searchers.Answer.MATCHED.value):
        return ()
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
        return ()
```

New text:

```
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others:
        return ()
```

### `u284.C1_tagged_file_named_refused`

tagging.cli._refused_out: a file with a genre written is named among those left with none

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C1_tagged_file_named_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_file_discogs_tagged_while_beatport_refused_its_picture_is_not_named`

Old text:

```
    if reason not in (tag_engine.SOURCES_UNREAD, tag_engine.UNMAPPED_GENRE):
        return ()
```

New text:

```
    if False:
        return ()
```

### `u284.C2_outage_named_refused`

tagging.cli._refused_out: a file another catalogue was down for is named as refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C2_outage_named_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
```

New text:

```
    if not others:
```

### `u284.C4_stop_never_collected`

tagging.cli._summary: no failed file is read as one every catalogue refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C4_stop_never_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        if cause is not None and isinstance((cause.detail or {}).get(searchers.REFUSED_DETAIL), dict):
```

New text:

```
        if False:
```

### `u284.C5_sweep_stop_unsaid`

tagging.cli._with_report: the sweep's own refusal says nothing of who refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C5_sweep_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`

Old text:

```
    if stop:
        # WHO REFUSED
```

New text:

```
    if False:
        # WHO REFUSED
```

### `u284.C6_token_unsaid`

tagging.cli._refusal_stop: Discogs unasked is never said and its token step never given

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C6_token_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
    if unasked:
        why = 
```

New text:

```
    if False:
        why = 
```

### `u284.C7_rejected_token_told_to_wait`

tagging.cli._refusal_stop: a stop over a rejected token says waiting mends it

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C7_rejected_token_told_to_wait`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`

Old text:

```
    if unasked != searchers.DISCOGS_TOKEN_REFUSED:
```

New text:

```
    if True:
```

### `u177.B10_land_command`

land_command: name no landing, so the fetch never says how to file the batch by label

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B10_land_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`

Old text:

```
    if not any(isinstance(one, Mapping) and one.get("label") for one in releases.values()):
        return None

```

New text:

```
    if True:
        return None

```

### `u177.B1_seller_by_label`

_sellers: take every name as an account, so --seller PULS plans nothing of pulsromania

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B1_seller_by_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_seller_by_label_name_fetches_only_that_labels_releases`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`

Old text:

```
        found.add(entry.bandcamp if entry is not None and entry.bandcamp else name.casefold())

```

New text:

```
        found.add(name.casefold())

```

### `u177.B2_plan_label`

plan: never ask the registry, so no row names a label and nothing is tagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B2_plan_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 12 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_seller_is_named_with_the_command_that_registers_it`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`
  - `tests/test_bandcamp_labels.py::test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names`

Old text:

```
        label = known.by_bandcamp(purchase.seller) if purchase.seller else None

```

New text:

```
        label = None

```

### `u177.B3_unregistered_filter`

unregistered: name sellers with nothing to fetch too, so a filtered seller is asked to register

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B3_unregistered_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`

Old text:

```
            if one.disposition in TO_FETCH and one.label is None and one.purchase.seller

```

New text:

```
            if one.label is None and one.purchase.seller

```

### `u177.B4_labels_of_filter`

labels_of: name a label whose purchases are all filtered, so the check says it stages

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B4_labels_of_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_label_whose_purchases_are_all_filtered_is_not_said_to_stage`

Old text:

```
        if one.disposition in TO_FETCH and one.label is not None
    }

```

New text:

```
        if one.label is not None
    }

```

### `u177.B5_registry_unread_empty`

registry: read an unreadable registry as empty, so every purchase stages untagged with a clean plan

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B5_registry_unread_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_an_unreadable_registry_refuses_the_plan_rather_than_staging_untagged[{"version": 99, "labels": {}}]`
  - `tests/test_bandcamp_labels.py::test_an_unreadable_registry_refuses_the_plan_rather_than_staging_untagged[{not json]`

Old text:

```
    del origin
    return labels.RegistryStore().load()

```

New text:

```
    del origin
    try:
        return labels.RegistryStore().load()
    except CratekitError:
        return labels.empty()

```

### `u177.B6_frozen_label`

frozen_release: freeze no label, so the worker tags nothing

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B6_frozen_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 8 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`

Old text:

```
        "label": planned.label.name if planned.label is not None else None,

```

New text:

```
        "label": None,

```

### `u177.B7_tag_not_written`

handle_fetch: skip the label write, so a registered seller's files stage untagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B7_tag_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`

Old text:

```
        if label and not tags.write_tags(path, {"label": label}):

```

New text:

```
        if False:

```

### `u177.B8_write_false_ignored`

handle_fetch: ignore the writer's False, so a file that would not take the tag is reported tagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B8_write_false_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`

Old text:

```
        if label and not tags.write_tags(path, {"label": label}):
            untagged.append(final.name)

```

New text:

```
        if label:
            tags.write_tags(path, {"label": label})

```

### `u177.B9_untagged_refusal`

handle_fetch: drop the refusal naming the untagged files, so the item succeeds over them

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B9_untagged_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`

Old text:

```
    if untagged:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `r815-a.W1_withhold_only_an_open_item`

withhold: move an item whatever its verdict column says

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W1_withhold_only_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[accepted]`
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[rejected]`
  - `tests/test_label_judge.py::test_a_release_decided_while_it_was_being_judged_is_not_held`
  - `tests/test_label_judge.py::test_a_superseded_item_is_not_withheld`
  - `tests/test_label_judge.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_not_withheld`

Old text:

```
        if row is None or row["verdict"] is not None:
            return None
        queue = row["queue"]
```

New text:

```
        if row is None:
            return None
        queue = row["queue"]
```

### `r815-a.W2_a_returned_hold_is_not_withheld`

withhold: take back a release a person returned

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W2_a_returned_hold_is_not_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_a_person_returned_is_never_withheld_again`

Old text:

```
        if standing is not None and standing["state"] == HOLD_RETURNED:
            return None
        try:
```

New text:

```
        if False:
            return None
        try:
```

### `r815-a.W3_the_floor_is_never_lowered`

withhold: let a lower ordinal replace the floor

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W3_the_floor_is_never_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = MAX(ordinal, excluded.ordinal)",
```

New text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = excluded.ordinal",
```

### `r815-a.W5_a_refresh_keeps_the_withheld_word`

_CARRIED_ACROSS_A_REFRESH: carry the filing run and drop the withheld word

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W5_a_refresh_keeps_the_withheld_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_refreshed_hold_keeps_the_run_its_release_was_filed_under`

Old text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD, WITHHELD_FIELD)
```

New text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD,)
```

### `r815-a.W6_redescribe_only_an_open_item`

redescribe: rewrite an item whatever its verdict column says

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W6_redescribe_only_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_redescribing_a_decided_item_changes_nothing`
  - `tests/test_label_judge.py::test_redescribing_an_item_with_an_unreadable_verdict_changes_nothing`

Old text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ? AND verdict IS NULL",
```

New text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ?",
```

### `r815-a.G2_forgetting_keeps_the_failure_count`

ReleaseTracks.forget: forget the failures in a row as well

- File: `src/cratekit/label/catalogue.py`
- Source: `r815-a.json`, row `G2_forgetting_keeps_the_failure_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_reader_forgets_each_release_and_keeps_its_count_of_failures`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
        self._read.clear()

    def release_tracks
```

New text:

```
        self._read.clear()
        self._failed_in_a_row = 0

    def release_tracks
```

### `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`

judge_cli._stamp: keep the fields of the item as it was read before the catalogue was asked, so an artist repaired in that time reads its address again

- File: `src/cratekit/label/judge_cli.py`
- Source: `r840-c.json`, row `C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_artist_put_right_while_a_release_was_being_judged_is_kept_by_the_stamp`

Old text:

```
        kept = {field: value for field, value in current.items() if field not in _STAMP_FIELDS}
```

New text:

```
        kept = {field: value for field, value in item.payload.items() if field not in _STAMP_FIELDS}
```

### `u165.A1_scope`

census: ignore the scope and walk the whole collection

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A1_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
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
- Collected: 152 against a baseline of 152
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
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_the_approval_is_refused_before_anything_is_written`

Old text:

```
    grant(plan, actor=actor)

    membership = _write_memberships
```

New text:

```
    membership = _write_memberships
```

### `u165.L1_bridge_skip`

_land_native: predict a filing on a routing tree still on the bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L1_bridge_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if medium.files_natively
```

New text:

```
            if True
```

### `u165.L2_land_only`

planner: predict and file under --land-only too

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L2_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_filing.py::test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if unfiled:
                return made
```

New text:

```
            if False:
                return made
```

### `u165.L3_filing_tail`

_land_native: never file after the landing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L3_filing_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`
  - `tests/test_intake_land_filing.py::test_the_filed_rows_are_what_adopt_apply_then_finds_nothing_to_do_for`

Old text:

```
    if predicted is not None:
        # THE FILING
```

New text:

```
    if False:
        # THE FILING
```

### `u165.L4_files_into`

_native_payload: drop each item's files into

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L4_files_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
        if str(row.target) in sorted_into:
```

New text:

```
        if False:
```

### `u165.N1_digest`

identity: leave the predictions out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u165.json`, row `N1_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files`

Old text:

```
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
```

New text:

```
        {}
```

### `u261.H3_reuse_swallows_a_missing_session`

session_for: answer a keychain that no longer holds the session with the held client, so a withdrawn session is reused

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H3_reuse_swallows_a_missing_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_keychain_that_cannot_be_read_on_a_reuse_says_repair_it`
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            return current
```

### `u261.H4_failed_read_keeps_the_hold`

session_for: refuse a keychain that cannot be read on a reuse but keep the hold, so the account's held adapter goes on over it

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H4_failed_read_keeps_the_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            raise _to_auth_failure(exc) from exc
```

### `u261.H9_no_forget_before_a_new_login`

session_for: keep the old hold while a replaced session is logged in afresh, so a login that fails leaves the account's adapter over the replaced session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H9_no_forget_before_a_new_login`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    forget()
    gate = provider_gate.Gate(settings)
```

New text:

```
    gate = provider_gate.Gate(settings)
```

### `u261.R3_raised_refusal_ignored`

_watch: ignore a 401 or 403 the transport raises, so a refusal that arrives as an exception leaves the client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R3_raised_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
            if answered_status(exc) in SESSION_REFUSED_STATUSES:
```

New text:

```
            if False:
```

### `u261.A1_account_forget_keeps_the_session`

account.forget: drop the adapter and keep the shared session, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A1_account_forget_keeps_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 28 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[rejected]`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[unreachable]`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_provider_failure_on_one_heart_fails_that_item_and_no_other`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_matches_through_the_isrc_the_file_carries`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[rejected]`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[unreachable]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    _OPENED_OVER = None
    provider_session.forget()
```

New text:

```
    _OPENED_OVER = None
```

### `u261.A2_account_reuse_ignores_the_hold`

account.resolve: hand out the held adapter whatever became of its session, so a client the catalogue saw refused is reused by the account

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A2_account_reuse_ignores_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    if _OPENED is not None and _OPENED_OVER is provider_session.held():
```

New text:

```
    if _OPENED is not None:
```

### `u261.A3_account_records_no_session`

account.resolve: record no session under the adapter, so the adapter is opened afresh on every resolve and the one login per process is lost

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A3_account_records_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
    _OPENED_OVER = provider_session.held()
    return opened
```

New text:

```
    _OPENED_OVER = None
    return opened
```

### `u261.A4_refusal_drops_no_session`

account._forget_refused: drop the adapter and keep the shared session it was built over, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A4_refusal_drops_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`

Old text:

```
    else:
        provider_session.drop(over)
```

New text:

```
    else:
        pass
```

### `u27-round-8-independent.E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E4_path_missing_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_preflight.py::test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause`
  - `tests/test_write_session.py::test_a_matched_volume_with_the_directory_absent_is_left_to_the_pass_that_follows_the_rule`

Old text:

```
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
```

New text:

```
            MountState.OK,
```

### `u27-round-8-independent.E5_unmounted_reads_foreign`

An absent volume resolves to FOREIGN_VOLUME instead of NOT_MOUNTED

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E5_unmounted_reads_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 5 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all`
  - `tests/test_preflight.py::test_a_volume_that_is_not_mounted_refuses_with_its_own_cause`
  - `tests/test_preflight.py::test_the_three_refusals_are_distinguishable_from_each_other`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`

Old text:

```
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
```

New text:

```
        MountState.FOREIGN_VOLUME,
```

### `u27-round-8-independent.E6_write_table_shares_read`

Make the write table refuse LIBRARY_PATH_MISSING, the row it differs from the read table on

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E6_write_table_shares_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused`
  - `tests/test_doctor.py::test_every_mount_outcome_permits_exactly_what_it_is_declared_to[_STATE_WRITABLE-expected1]`
  - `tests/test_doctor.py::test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed`

Old text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
```

New text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
```

### `r663-a.M10_detail_size_pinned`

the detail's size is written as zero whatever the copy measured

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M10_detail_size_pinned`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
        detail={"path": str(source), "size": size, "tables_read": list(CANARY_TABLES)},
```

New text:

```
        detail={"path": str(source), "size": 0, "tables_read": list(CANARY_TABLES)},
```

### `r663-a.M1_empty_not_refused_before_open`

the size of the copy is no longer asked before the open, so an empty copy reaches the binding and is classified only if the canary is what fails

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M1_empty_not_refused_before_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 4 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_file_whose_tables_are_listed_is_only_ever_a_copy[empty]`

Old text:

```
        refusal = None if copied.stat().st_size else _not_a_library(Path(source), copied)

```

New text:

```
        refusal = None

```

### `r663-a.M3_unlistable_read_as_empty`

a copy whose tables could not be listed is no longer kept apart from one with none, so the None check is dropped

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M3_unlistable_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_that_is_not_sqlite_at_all_keeps_the_canarys_refusal`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables and tables.intersection(CANARY_TABLES):
```

### `r663-a.M4_one_canary_table_not_enough`

a copy holding one of the two canary tables is classified as not a library, so schema drift is sent to setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M4_one_canary_table_not_enough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_is_drift_and_keeps_the_canarys_refusal[agentRegistry]`
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_is_drift_and_keeps_the_canarys_refusal[djmdContent]`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables is None or tables.issuperset(CANARY_TABLES):
```

### `r663-a.M5_failed_listing_returns_empty_set`

a table listing whose query fails answers an empty set rather than None, so a file that could not be read is reported as holding nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M5_failed_listing_returns_empty_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_that_is_not_sqlite_at_all_keeps_the_canarys_refusal`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
```

New text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return set()
```

### `r663-a.M6_listing_opened_with_the_key_always`

the table listing opens every copy with the key rather than asking the header, so a plain foreign file cannot be listed

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M6_listing_opened_with_the_key_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
        db = Rekordbox6Database(path=str(copied), unlock=unlock_needed(copied))
```

New text:

```
        db = Rekordbox6Database(path=str(copied), unlock=True)
```

### `r663-a.M7_message_drops_the_size`

the empty file's message no longer names the size

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M7_message_drops_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        what = "is empty, 0 bytes"
```

New text:

```
        what = "is not a database"
```

### `r663-a.M8_message_names_the_copy`

the message names the temporary copy rather than the configured path

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M8_message_names_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 5 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        f"the file configured as the rekordbox database, {source}, {what}, so it "
```

New text:

```
        f"the file configured as the rekordbox database, {copied}, {what}, so it "
```

### `r663-a.M9_remedy_restore`

the refusal carries the snapshot restore remedy instead of setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M9_remedy_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        remedy=Remedy.RUN_SETUP,
```

New text:

```
        remedy=Remedy.RESTORE_FROM_SNAPSHOT,
```

### `r663-b.M2_every_open_refusal_classified`

the canary reason gate is removed, so any refusal on the way in, a pin or a failed open, is also asked whether the copy is a library

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-b.json`, row `M2_every_open_refusal_classified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_refusal_on_the_way_in_is_not_reclassified_as_a_wrong_path`

Old text:

```
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _not_a_library(Path(source), copied)
```

New text:

```
            refusal = _not_a_library(Path(source), copied)
```

### `u279.M10_tilde_not_expanded`

excluded_folders: read the staging path without expanding a tilde, round one's finding

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M10_tilde_not_expanded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
Path(cfg.paths.download_staging).expanduser())
```

New text:

```
Path(cfg.paths.download_staging))
```

### `u279.M11_excluded_anchor_not_refused`

set_build: drop the excluded anchor refusal, so an anchor in staging gets the generic not indexed wording

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M11_excluded_anchor_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
    _refuse_if_excluded(candidate, cfg, root)

```

New text:

```
(empty)
```

### `u279.M13_wrong_folder_named`

_refuse_if_excluded: say the state folder whichever folder holds the anchor

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M13_wrong_folder_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`

Old text:

```
    if holder == folders[0]:
```

New text:

```
    if True:
```

### `u279.M8_index_call_unexcluded`

setbuild _index: drop exclude, so the verb's index walks the state and staging folders again

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M8_index_call_unexcluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        exclude=excluded_folders(cfg),

```

New text:

```
(empty)
```

### `u279.M9_staging_not_excluded`

excluded_folders: leave download staging out of the exclusion, the state folder only

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M9_staging_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())
```

New text:

```
    return (config.library_state_dir(cfg), config.library_state_dir(cfg))
```

### `u205.G1_app_call_not_counted`

gate: a call under the app identity is counted in the totals and not under the app, so every report reads it as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G1_app_call_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
        if app:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

New text:

```
        if False:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

### `u205.G2_app_rate_limit_not_counted`

gate: a rate limit answer to the app is counted as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G2_app_rate_limit_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`

Old text:

```
            if app:
                state.app_rate_limited += 1
```

New text:

```
            if False:
                state.app_rate_limited += 1
```

### `u205.G3_attach_drops_identity`

gate attach: the wrapped transport counts every call under the account whatever identity it was attached under

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G3_attach_drops_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
            return self.call(lambda: original(method, url, *args, **kwargs), identity=identity)
```

New text:

```
            return self.call(lambda: original(method, url, *args, **kwargs), identity=ACCOUNT)
```

### `u205.G5_app_share_unclamped`

gate state load: an app share above the total is kept, so the account's share reads negative and is shown as zero

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G5_app_share_unclamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_an_app_share_larger_than_the_total_is_clamped_to_it`

Old text:

```
            state.app_calls = min(_as_int(app.get("calls")), state.calls)
```

New text:

```
            state.app_calls = _as_int(app.get("calls"))
```

### `u205.G6_file_account_share_is_the_total`

gate state write: the account's entry under identities is written as the total, the app's calls in it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G6_file_account_share_is_the_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`

Old text:

```
                    "calls": max(0, self.calls - self.app_calls),
```

New text:

```
                    "calls": self.calls,
```

### `u205.G7_process_spend_drops_app`

process spend: the app's share of this process's calls is not reported, so the spend line says every call was the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G7_process_spend_drops_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`

Old text:

```
        app_calls=_PROCESS_APP_CALLS,
```

New text:

```
        app_calls=0,
```

### `u205.G8_since_keeps_earlier_app_calls`

spend since: the app's share is not differenced, so a run is charged the app calls made before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G8_since_keeps_earlier_app_calls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_spend_line_survives_a_refusal`

Old text:

```
            app_calls=max(0, self.app_calls - earlier.app_calls),
```

New text:

```
            app_calls=self.app_calls,
```

### `u96-b.C1_engine_terminal`

SAMPLE of the engine's guards, now reachable from a verb. bare_metal_session: disarm the controlling terminal refusal

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C1_engine_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[nobody is at a terminal]`

Old text:

```
    if not probe():
        raise _refuse_target(
            "this invocation has no controlling terminal
```

New text:

```
    if False:
        raise _refuse_target(
            "this invocation has no controlling terminal
```

### `u96-b.C2_engine_acknowledged`

SAMPLE. bare_metal_session: disarm the acknowledgment refusal

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C2_engine_acknowledged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the replacement was not accepted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
    if not acknowledged:
```

New text:

```
    if False:
```

### `u96-b.C3_engine_occupied_target`

SAMPLE. assert_recovery_target: disarm the refusal of a target that already holds a database

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C3_engine_occupied_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if False:
```

### `u96-b.C4_engine_stub`

SAMPLE. assert_recovery_target: disarm the refusal of the stub an unmounted volume leaves on the internal disk

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C4_engine_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 5 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stub_an_unmounted_volume_leaves_behind`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library/Music-why0]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the target is the stub on the internal disk]`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if False:
```

### `u96-b.C5_engine_library_is_mounted`

SAMPLE. assert_library_volume_is_gone: answer gone when the library is mounted and is the recorded volume

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C5_engine_library_is_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_is_refused_while_the_library_is_reachable`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the library is still mounted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_while_the_library_is_mounted`

Old text:

```
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

New text:

```
    return preflight.MountState.NOT_MOUNTED
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

