# Mutation table: u325-after-l-25

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 130.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:20 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 26, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u322.M21_suggest_uses_folder_binder` | `src/cratekit/tagging/suggest_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M20_backlog_uses_folder_binder` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M24_backlog_line_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 2 | killed |
| `u42-author.C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P1_unresolved_from_the_page` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 24 | 5 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 2 | killed |
| `r777.N16_pass_not_recorded` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 1 | killed |
| `r923.N1_landing_sets_nothing` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 1 | killed |
| `u115.F1_landing_keeps_random_id` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 38 | killed |
| `r1031.M10_filter_against_raw_links` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M11_filter_removed` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M12_link_keeps_its_miss` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `r1031.M13_miss_written_over_a_link` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `r1031.M8_misses_not_a_map_read` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M9_malformed_miss_kept` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `r1184.M17_verb_takes_step` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 3 | killed |
| `r1184.M18_verb_nothing_to_do` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W18_carrying_several_genres` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W19_carrying_unread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 2 | killed |
| `u194.W22_unwritten_refusal` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W23_root_missing` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u174.N1_landed_passes_closed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N2_landed_passes_committed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N3_landed_passes_workflow` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `u174.N4_landed_passes_pass_key` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `u120.P1_live_plain_attribute` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 4 | killed |
| `u120.P2_two_sources_accepted` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 2 | killed |
| `u120.P4_into_source_always` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 3 | killed |
| `u120.P7_bypass_only_when_absent` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 3 | killed |
| `u120.P8_source_name_default` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 1 | killed |
| `u185.R3_favorites_home` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 66 | 1 | killed |
| `r1313.A1_classifier_failure_alone` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 7 | killed |
| `r1313.A2_status_before_no_file_landed` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 2 | killed |
| `r1313.A3_classifier_name_on_any_link` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 1 | killed |
| `u205.O2_no_country_still_opens` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 1 | killed |
| `u205.O3_unreadable_values_read_as_absent` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 1 | killed |
| `u205.O4_app_attached_as_account` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 6 | killed |
| `u261.H2_reuse_ignores_a_replaced_session` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 4 | killed |
| `u261.H7_nothing_held` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 12 | killed |
| `u261.R1_watch_not_installed` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 3 | killed |
| `u261.R2_answered_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 2 | killed |
| `r740-b.I1_tag_key_first` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 114 | 3 | killed |
| `r740-b.I3_stem_is_the_title` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 114 | 2 | killed |
| `r740-b.I4_lossy_is_the_parameter` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 114 | 1 | killed |
| `r740-b.I5_body_marker_marks` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 114 | 1 | killed |
| `r740-c.I2_no_stem_fallback` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 114 | 1 | killed |
| `u172-b.C3_left_miscounted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `r375-b.T3_a_noop_claims_a_commit` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-b.T4_noop_bound_off_by_one` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 4 | killed |
| `r375-b.T7_commit_recorded_after_the_fingerprint` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-b.T8_counts_filed_as_updates` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 3 | killed |
| `u113-a.A8_pending_any_state` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 32 | 1 | killed |
| `u113-b.B3_record_unnamed` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 32 | 4 | killed |
| `u113-b.B8_pending_names_unheld` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u128-b.B3_owned_unresolved_at_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 32 | 6 | killed |
| `u128.L1_bridge_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 32 | 3 | killed |
| `u113-b.B6_root_names_unheld` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 32 | 1 | killed |
| `u27-reports-round-1.S1_limit_floor` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.S2_truncation_row` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S3_summary_total` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `r515-operator.S14_harvest_no_warning` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B4_resume_dropped` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 47 | killed |
| `u109-b.B6_message_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B7_step_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B8_itemless_branch` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `r1184.M19_tag_folder_wiring` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M20_tag_folder_fallback` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M21_guess_wiring` | `src/cratekit/tagging/guess_cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `u145.M3_landing_heart_undated` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 19 | 11 | killed |
| `u120.C1_no_skip_note` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 19 | 2 | killed |
| `u120.C2_hearts_not_claimed` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 19 | 14 | killed |
| `u153.L3_notes_colour_skipped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `u120.N3_identity_without_hearts` | `src/cratekit/intake/native.py` | user | 1 file(s) | 19 | 1 | killed |
| `u120.N4_skipped_is_raised` | `src/cratekit/intake/native.py` | user | 1 file(s) | 19 | 2 | killed |
| `r835-b.T1_folder_create_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `r835-b.T2_refused_move_raised` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `r835-c.T3_short_answer_read_again_again` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `u44-author.C2_argv_drops_overwrite` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C3_argv_drops_output_dir` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C4_refusal_not_translated` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 23 | killed |
| `u44-author.C6_overwrite_always_true` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 4 | killed |
| `u44-author.C7_output_dir_ignored_at_the_work` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 3 | killed |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 891 | 2 | killed |
| `u261.W1_unchanged_skip_removed` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 481 | 5 | killed |
| `u261.W2_changed_session_skipped` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 481 | 5 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 886 | 5 | killed |
| `u278.M18_reading_noop` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 3 | killed |
| `u278.M4_no_budget_check` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 17 | killed |
| `u278.M8_no_reserve` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 23 | killed |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 9 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 19 | killed |

## Row definitions

### `u322.M21_suggest_uses_folder_binder`

suggest_cli.read_plan: tag suggest asks through tag folder's binder

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u322.json`, row `M21_suggest_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
```

### `u322.M20_backlog_uses_folder_binder`

backlog_cli.read_plan: the backlog asks through tag folder's binder, so Deezer is held behind a refusing Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M20_backlog_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
```

### `u322.M24_backlog_line_gone`

backlog_cli.checks: no catalogue line

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M24_backlog_line_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_backlog.py::test_the_catalogue_line_names_the_rows_the_walk_stopped_before`

Old text:

```
    if plan.catalogue:
        found.append(_check("backlog.catalogue"
```

New text:

```
    if False:
        found.append(_check("backlog.catalogue"
```

### `u42-author.C3_strict_consults_the_marker`

Make strict behave like the permissive policy, admitting a marked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C3_strict_consults_the_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

New text:

```
                if policy is LosslessPolicy.STRICT and marker and not marked:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

### `u42-author.C4_marked_lossless_dropped`

Stop reporting a lossless file that wears the lossy marker

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C4_marked_lossless_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`

Old text:

```
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
```

New text:

```
            elif False:
                found.append(_item(path, root, "marked-lossless"))
```

### `u42-author.C5_empty_marker_matches_everything`

Drop the empty-marker guard, so '' in stem marks every file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C5_empty_marker_matches_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`

Old text:

```
            marked = bool(marker) and marker in path.stem
```

New text:

```
            marked = marker in path.stem
```

### `u42-author.P1_unresolved_from_the_page`

Report zero outstanding regardless of what the walk found

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P1_unresolved_from_the_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
            "unresolved": len(found),
```

New text:

```
            "unresolved": 0,
```

### `u42-author.P2_relative_path_leaks_the_root`

Report the absolute path, putting a real directory layout in the payload (R1)

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P2_relative_path_leaks_the_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_permissive_policy_reports_only_the_unmarked_lossy_file`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`

Old text:

```
        where = str(path.relative_to(root))
```

New text:

```
        where = str(path)
```

### `r777.N15_any_pass`

landings_of_pass counts a landing of another pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N15_any_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`

Old text:

```
            and record.detail.get(PASS_KEY) == name

```

New text:

```
(empty)
```

### `r777.N16_pass_not_recorded`

The native landing's commit no longer records the pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N16_pass_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`

Old text:

```
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
```

New text:

```
    if False:
        record.detail[PASS_KEY] = plan.pass_name
```

### `r923.N1_landing_sets_nothing`

The native landing no longer sets rekordbox's defaults on a row it creates

- File: `src/cratekit/intake/native.py`
- Source: `r923.json`, row `N1_landing_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`

Old text:

```
        if getattr(content, column, None) is None:
```

New text:

```
        if False:
```

### `u115.F1_landing_keeps_random_id`

The native landing keeps the random rb_file_id the binding minted instead of the landed file's inode

- File: `src/cratekit/intake/native.py`
- Source: `u115.json`, row `F1_landing_keeps_random_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 38 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))

```

New text:

```
(empty)
```

### `r1031.M10_filter_against_raw_links`

ledger._load: drop a miss beside a raw link entry with no account track, the review's round one finding

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M10_filter_against_raw_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_link_with_no_account_track_does_not_hide_a_miss`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and str(content_id) not in links
```

### `r1031.M11_filter_removed`

ledger._load: keep a miss of a row the ledger links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M11_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_holding_a_link_and_a_miss_of_one_row_reads_the_link`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and True
```

### `r1031.M12_link_keeps_its_miss`

ledger.record_mirror_links: leave the row's miss in the document when it is linked

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M12_link_keeps_its_miss`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_linking_a_row_takes_its_miss_out_of_the_document`

Old text:

```
                document["mirror_misses"].pop(str(content_id), None)
```

New text:

```
                pass
```

### `r1031.M13_miss_written_over_a_link`

ledger.record_mirror_misses: write a miss for a row the ledger already links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M13_miss_written_over_a_link`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_linked_row_is_never_written_to_the_document`

Old text:

```
            if str(content_id) in document["mirror_links"]:
                continue
```

New text:

```
            if False:
                continue
```

### `r1031.M8_misses_not_a_map_read`

ledger._load: read a mirror_misses that is not a map instead of refusing

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M8_misses_not_a_map_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_whose_misses_are_not_a_map_refuses`

Old text:

```
    if not isinstance(misses, Mapping):
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

New text:

```
    if False:
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

### `r1031.M9_malformed_miss_kept`

ledger._load: keep a miss whose key is not a list

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M9_malformed_miss_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_malformed_miss_is_dropped_and_asked_again_rather_than_refusing`

Old text:

```
            and isinstance(value.get("under"), list)
```

New text:

```
            and True
```

### `r1184.M17_verb_takes_step`

taxonomy alias verb: ignore the refusal's own step, so the bare folder and own name refusals say leave the word

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M17_verb_takes_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_the_bare_folder_refusal_names_the_folder_verb_as_its_step`

Old text:

```
    if exc.step:

```

New text:

```
    if False:

```

### `r1184.M18_verb_nothing_to_do`

taxonomy alias verb: the no change sentence for an own name claims a tagging alias

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M18_verb_nothing_to_do`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
                        if edit.own_name

```

New text:

```
                        if False

```

### `u194.W18_carrying_several_genres`

carrying: plan a write for a file carrying the word beside another genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W18_carrying_several_genres`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_with_two_genres_is_left_and_named`

Old text:

```
        current = _JOINED.join(values)
        if len(values) == 1:
```

New text:

```
        current = _JOINED.join(values)
        if True:
```

### `u194.W19_carrying_unread`

carrying: read a file whose genre could not be read as one carrying no genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W19_carrying_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_whose_genre_cannot_be_read_is_named_and_never_called_clean`
  - `tests/test_taxonomy_word.py::test_nothing_to_do_does_not_claim_a_file_it_could_not_read`

Old text:

```
        if values is None:
            items.append(FileItem(path=path, relative=relative, change=UNREAD))
            continue
```

New text:

```
        if values is None:
            continue
```

### `u194.W22_unwritten_refusal`

alias verb: leave a file the writer could not write out of the refusal, so the run reports success

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W22_unwritten_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes`

Old text:

```
    if done.moved or done.failed or done.wrong:
```

New text:

```
    if done.moved or done.wrong:
```

### `u194.W23_root_missing`

_root: drop the refusal of a folder that is not there, so the walk plans nothing and reads clean

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W23_root_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folder_that_is_not_there_is_refused_with_nothing_written`

Old text:

```
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

New text:

```
    if False:
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

### `u174.N1_landed_passes_closed`

landed_passes: drop the closed state check, so an open landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N1_landed_passes_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N2_landed_passes_committed`

landed_passes: drop the committed source check, so a refused landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N2_landed_passes_committed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and record.state is session.SessionState.CLOSED
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N3_landed_passes_workflow`

landed_passes: drop the workflow check, so any closed session naming a pass is read as a landing

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N3_landed_passes_workflow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                if record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N4_landed_passes_pass_key`

landed_passes: drop the pass key check, so a landing of no pass is listed as a pass named None

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N4_landed_passes_pass_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
            }
```

### `u120.P1_live_plain_attribute`

_live_plain: a folder or a smart playlist counts as plain

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P1_live_plain_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_smart_playlist_of_the_months_name_is_not_written_to_and_a_plain_one_is_made`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[folder]`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[smart]`
  - `tests/test_favorites_placement.py::test_the_home_is_the_one_plain_live_source_its_folder_and_the_months_there`

Old text:

```
if int(getattr(row, "Attribute", -1) or 0) == 0 and not rb_writer.node_removed(row)
```

New text:

```
if int(getattr(row, "Attribute", -1) or 0) >= 0 and not rb_writer.node_removed(row)
```

### `u120.P2_two_sources_accepted`

resolve_home: two live sources are accepted and the first chosen

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P2_two_sources_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[two]`

Old text:

```
    if len(live) != 1:
        count =
```

New text:

```
    if len(live) < 1:
        count =
```

### `u120.P4_into_source_always`

plan_placements: every heart is planned into the source whether it is there or not

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P4_into_source_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_plan_over_a_library_already_placed_writes_nothing`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make`

Old text:

```
                into_source=key not in in_source,
```

New text:

```
                into_source=True,
```

### `u120.P7_bypass_only_when_absent`

place: the source memberships are inserted directly rather than through add_memberships

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P7_bypass_only_when_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_members_marked_removedhip_in_the_month_is_added_again_live`
  - `tests/test_favorites_placement.py::test_place_adds_to_the_source_and_to_each_month_making_an_absent_one`
  - `tests/test_favorites_placement.py::test_placing_the_same_heart_twice_adds_nothing_twice`

Old text:

```
    added_source = len(rb_writer.add_memberships(db, source, ordered))
```

New text:

```
    added_source = 0
    for content_id in ordered:
        db.add_to_playlist(source, content_id)
        added_source += 1
```

### `u120.P8_source_name_default`

source_name: the outbound default is answered whatever the class declares

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P8_source_name_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_source_is_the_classs_playlist_else_the_outbound_default`

Old text:

```
    if sub is not None and sub.signal_playlist:
        return sub.signal_playlist
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

New text:

```
    del sub
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

### `u185.R3_favorites_home`

resolve_home: count a playlist of the source's name inside the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u185.json`, row `R3_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(
        _live_plain(list(db.get_playlist(Name=name))), list(db.get_playlist())
    )
```

New text:

```
    live = _live_plain(list(db.get_playlist(Name=name)))
```

### `r1313.A1_classifier_failure_alone`

classify_unavailable: read the 404 off the failure alone, as before R-1313, so a track answered with a 404 page is retried for ever

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A1_classifier_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_a_404_page_is_permanent_with_no_retry`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

New text:

```
    if getattr(getattr(exc, "response", None), "status_code", None) == 404:
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

### `r1313.A2_status_before_no_file_landed`

classify_unavailable: ask the nearest status before NoFileLanded, so a download whose swallowed cause was a 404 page quarantines a live track

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A2_status_before_no_file_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_marker_wins_over_a_status_code`
  - `tests/test_provider_not_found_bodies.py::test_no_file_landed_carrying_a_404_page_stays_transient`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

New text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

### `r1313.A3_classifier_name_on_any_link`

classify_unavailable: read a not found class name on any link the walk reaches, so a name met only as context is read as the provider's answer

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A3_classifier_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

New text:

```
    from cratekit.core.cause import failure_links  # noqa: PLC0415

    if any("notfound" in type(one).__name__.lower() for one, _ in failure_links(exc)):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

### `u205.O2_no_country_still_opens`

opener: an account naming no country still gets an app client, asked in no country

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O2_no_country_still_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_an_account_that_names_no_country_gets_no_app_client`

Old text:

```
    if country is None:
        return None
```

New text:

```
    if False:
        return None
```

### `u205.O3_unreadable_values_read_as_absent`

opener: recorded app values the keychain will not give are read as absent, putting every lookup back on the account without a word

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O3_unreadable_values_read_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_keychain_that_could_not_be_read_for_the_app_is_refused_not_read_as_absent`

Old text:

```
        raise catalogue_api.unreadable(exc) from exc
```

New text:

```
        return None
```

### `u205.O4_app_attached_as_account`

opener: the app client is attached under the account identity, so its calls are reported as the account's

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O4_app_attached_as_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
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
    if not gate.attach(client, identity=provider_gate.APP):
```

New text:

```
    if not gate.attach(client, identity=provider_gate.ACCOUNT):
```

### `u261.H2_reuse_ignores_a_replaced_session`

session_for: reuse the held client whatever the keychain now holds, so a session replaced or refreshed elsewhere is never picked up

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H2_reuse_ignores_a_replaced_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_replaced_after_an_open_is_logged_in_afresh_from_the_new_value`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
        if _canonical(stored) == current.blob:
```

New text:

```
        if True:
```

### `u261.H7_nothing_held`

session_for: hold nothing after a login, so every opener logs in again as before the unit

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H7_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 12 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_the_index_no_longer_records_is_refused_by_both_seams`
  - `tests/test_provider_session_hold.py::test_an_answer_that_judges_no_session_keeps_the_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`
  - `tests/test_provider_session_hold.py::test_the_surveys_drive_logs_in_once_and_writes_nothing`

Old text:

```
    _watch(opened)
    _HELD = opened
    return opened
```

New text:

```
    _watch(opened)
    return opened
```

### `u261.R1_watch_not_installed`

session_for: install no watch on the shared client, so a 401 or 403 the catalogue meets leaves the refused client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R1_watch_not_installed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
    _watch(opened)
    _HELD = opened
```

New text:

```
    _HELD = opened
```

### `u261.R2_answered_refusal_ignored`

_watch: ignore a 401 or 403 the transport answers, so a refused client stays held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R2_answered_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`

Old text:

```
        if getattr(response, "status_code", None) in SESSION_REFUSED_STATUSES:
            drop(session)
```

New text:

```
        if False:
            drop(session)
```

### `r740-b.I1_tag_key_first`

read_meta: prefer the key tag over the head's key, so a disagreeing tag drops the whole head

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I1_tag_key_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 114 against a baseline of 114
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_landing_head.py::test_an_off_wheel_key_tag_under_a_headed_title_lands_the_head`
  - `tests/test_landing_head.py::test_the_title_head_wins_over_a_disagreeing_key_tag`

Old text:

```
            key=head.get("key") or key,
```

New text:

```
            key=key or head.get("key"),
```

### `r740-b.I3_stem_is_the_title`

read_meta: pass the title as the stem, so the filename's head never reaches normalize_spec

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I3_stem_is_the_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 114 against a baseline of 114
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`

Old text:

```
            stem=path.stem,
            suffix=path.suffix,
            key=head.get("key") or key,
```

New text:

```
            stem=title,
            suffix=path.suffix,
            key=head.get("key") or key,
```

### `r740-b.I4_lossy_is_the_parameter`

read_meta: report the caller's lossy parameter, not the flag the Name was rendered from

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I4_lossy_is_the_parameter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`

Old text:

```
        "lossy": spec.lossy,
```

New text:

```
        "lossy": lossy,
```

### `r740-b.I5_body_marker_marks`

read_meta: read the marker anywhere in the title or stem, the round one defect, doubling an acquired marker

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I5_body_marker_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_an_acquired_body_marker_is_not_doubled_into_the_head`

Old text:

```
            lossy=lossy,
            title=title,
```

New text:

```
            lossy=lossy or "[MP3]" in title or "[MP3]" in path.stem,
            title=title,
```

### `r740-c.I2_no_stem_fallback`

round two, after the disagreeing key tag test, read_meta: read the head from the title only, never the filename stem

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-c.json`, row `I2_no_stem_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`

Old text:

```
        or naming.parse_head(path.stem, template=template)

```

New text:

```
(empty)
```

### `u172-b.C3_left_miscounted`

guess: count the files left as the candidates written rather than the files still without a genre

- File: `src/cratekit/cli/tail.py`
- Source: `u172-b.json`, row `C3_left_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_the_files_left_are_the_files_still_without_a_genre`

Old text:

```
    left = count - after - unread
```

New text:

```
    left = count - before - written - unread
```

### `u172.C1_tail_skips_guess`

through_name: never run the guess after tag folder

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C1_tail_skips_guess`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp.py::test_the_tail_runs_on_the_absolute_batch_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
        if step == TAG:
            guess(chain, folder, pass_name)
```

New text:

```
        if False:
            guess(chain, folder, pass_name)
```

### `u172.C2_guess_without_pass`

guess_argv: never name the pass, so no playlist votes in a pass

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C2_guess_without_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`
  - `tests/test_tag_guess.py::test_the_guess_is_named_with_a_pass_only_when_one_is_given`

Old text:

```
*([PASS_FLAG, pass_name] if pass_name else [])
```

New text:

```
*([])
```

### `r375-b.T3_a_noop_claims_a_commit`

_record_membership_commit: record a commit for a pass that added nothing, so a restore refuses over sessions that created nothing

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T3_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `r375-b.T4_noop_bound_off_by_one`

_record_membership_commit: move the no-op bound by one, so a pass that added exactly one membership claims no commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T4_noop_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 4 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    if added <= 1:
        return
    session.record_commit(
```

### `r375-b.T7_commit_recorded_after_the_fingerprint`

write_tree_membership: record the commit AFTER the fingerprint write, so a failure there closes a committed write as empty

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T7_commit_recorded_after_the_fingerprint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`

Old text:

```
        _record_membership_commit(record, tree_id, added, cfg)

        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT. It is what
        # lets the next run tell a database recovered out of band from one this
        # product changed itself, and taking it before the commit would record a
        # database this session then moved, so the next run would read its own
        # write as somebody else's restore. It sits outside the try above because
        # by here the commit has landed and there is nothing pending to roll
        # back; a failure now is a state write that failed, not a database write
        # that half happened.
        convergence.record_fingerprint(cfg, db)

```

New text:

```
        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT. It is what
        # lets the next run tell a database recovered out of band from one this
        # product changed itself, and taking it before the commit would record a
        # database this session then moved, so the next run would read its own
        # write as somebody else's restore. It sits outside the try above because
        # by here the commit has landed and there is nothing pending to roll
        # back; a failure now is a state write that failed, not a database write
        # that half happened.
        convergence.record_fingerprint(cfg, db)
        _record_membership_commit(record, tree_id, added, cfg)

```

### `r375-b.T8_counts_filed_as_updates`

_record_membership_commit: file the added memberships as updated rather than created

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T8_counts_filed_as_updates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`

Old text:

```
session.TreeChange(tree=tree_id, created=added)
```

New text:

```
session.TreeChange(tree=tree_id, updated=added)
```

### `u113-a.A8_pending_any_state`

Names held by intake files are read from records whatever their state, not only those awaiting import

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A8_pending_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
        and record.state is session.SessionState.AWAITING_IMPORT
```

New text:

```
        and record.state is not session.SessionState.AWAITING_IMPORT
```

### `u113-b.B3_record_unnamed`

The intake session record does not list the account playlists, so the rotation cannot age them

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B3_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_an_abandoned_landing_is_not_read_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_the_intake_record_names_each_playlist_and_its_batch_folder`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
```

### `u113-b.B8_pending_names_unheld`

Names an intake file still waiting on its import holds are not held

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B8_pending_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
    taken = (*(held if isinstance(held, tuple) else ()), *account_playlists.pending_names(cfg))
```

New text:

```
    taken = held if isinstance(held, tuple) else ()
```

### `u128-b.B3_owned_unresolved_at_gate`

The bridge verb does not find the owned tracks in the export before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128-b.json`, row `B3_owned_unresolved_at_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
    split, emptied = landing.owned_in_export(cfg, split, export)
```

New text:

```
    emptied = ()
```

### `u128.L1_bridge_warning_unsaid`

The bridge landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128.json`, row `L1_bridge_warning_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
            *account_playlists.left_warning((*emptied, *landed.left)),
```

New text:

```
            *account_playlists.left_warning(()),
```

### `u113-b.B6_root_names_unheld`

Names at the export's playlist root, where an import lands first, are not held

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B6_root_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`

Old text:

```
    return (*held, *at_root)
```

New text:

```
    return held
```

### `u27-reports-round-1.S1_limit_floor`

Pass the limit through unfloored, so a negative one becomes a slice from the end

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S1_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end`

Old text:

```
    limit = max(0, int(ctx.args.limit))
```

New text:

```
    limit = int(ctx.args.limit)
```

### `u27-reports-round-1.S2_truncation_row`

Drop the row that says the list was capped

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S2_truncation_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )

```

New text:

```
(empty)
```

### `u27-reports-round-1.S3_summary_total`

Derive the summary total from the truncated list, the arithmetic that hides the cap

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S3_summary_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
            "uncovered": len(report.uncovered),
```

New text:

```
            "uncovered": len(listed),
```

### `u27-reports-round-2.S5_handler_key_wrong`

Round 1's S5 was inert because the engine default matched; pass a WRONG key instead

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-2.json`, row `S5_handler_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`
  - `tests/test_reports_cli.py::test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg), handler_key="duplicates"
```

### `u27-reports-round-3-fixes.F1_as_of_falsiness`

Restore the falsiness test, so an explicitly empty as-of is read as an absent flag

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F1_as_of_falsiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_explicitly_empty_as_of_refuses_rather_than_answering_for_today`

Old text:

```
    if written is None:
```

New text:

```
    if not written:
```

### `u27-reports-round-3-fixes.F5_gap_row_flood`

Render one gap row per declared bucket again when the governed tree is absent

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F5_gap_row_flood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket`

Old text:

```
    if stats.shape.folders == 0:
```

New text:

```
    if False:
```

### `r515-operator.S14_harvest_no_warning`

A harvest over a short playlist carries no warning

- File: `src/cratekit/label/cli.py`
- Source: `r515-operator.json`, row `S14_harvest_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`

Old text:

```
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
```

New text:

```
        warnings=(),
```

### `u109-b.B4_resume_dropped`

sync labels refuses even with --job, so a sweep queued before U109 can never run

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B4_resume_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 47 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_verb_will_not_drive_a_job_queued_for_another_verb`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise refuse(
        "verb-retired",
```

New text:

```
    raise refuse(
        "verb-retired",
```

### `u109-b.B6_message_drops_verb`

Reword the refusal message so it no longer names crate label sync

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B6_message_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"by label with {GUIDED_VERB}, which asks before it downloads anything",
```

New text:

```
        "by label, asking before anything downloads",
```

### `u109-b.B7_step_drops_verb`

Drop the step that names the guided verb from the retired refusal

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B7_step_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
            f"take label releases with: {GUIDED_VERB}",
            "a sweep queued before this change still runs with: crate sync labels "
```

New text:

```
            "a sweep queued before this change still runs with: crate sync labels "
```

### `u109-b.B8_itemless_branch`

The itemless refusal tells a sweep job to queue the import again, never naming the guided verb

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B8_itemless_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`

Old text:

```
                if job.handler_key == sweep.HANDLER_KEY
```

New text:

```
                if False
```

### `r1184.M19_tag_folder_wiring`

tag folder report: never hand the warning the taxonomy, so the own name answer is dropped

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M19_tag_folder_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
_off_taxonomy_warning(summary, _declared(cfg) if summary.get("off_taxonomy") else None)
```

New text:

```
_off_taxonomy_warning(summary, None)
```

### `r1184.M20_tag_folder_fallback`

tag folder report: drop the catch of an unreadable copy, so the report is refused over a sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M20_tag_folder_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
    try:
        return active_taxonomy.load(cfg)
    except CratekitError:
        return None
```

New text:

```
    return active_taxonomy.load(cfg)
```

### `r1184.M21_guess_wiring`

tag guess: drop the own name sentence from the off taxonomy warning

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `r1184.json`, row `M21_guess_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`

Old text:

```
                    + taxonomy_word.own_names(declared, found.off_taxonomy)

```

New text:

```
(empty)
```

### `u145.M3_landing_heart_undated`

Hearted.month: a landed heart whose job dated it goes to Undated

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M3_landing_heart_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_dated_the_twentieth_of_october_joins_its_month_and_no_quarter_is_made`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
        return placeholders.month_label(self.hearted) if self.known else None
```

New text:

```
        return placeholders.UNDATED if self.known else None
```

### `u120.C1_no_skip_note`

favorites_notes: a skipped placement is not said

- File: `src/cratekit/intake/land_cli.py`
- Source: `u120.json`, row `C1_no_skip_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    if skipped:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

New text:

```
    if False:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

### `u120.C2_hearts_not_claimed`

intake_land: no file is a heart

- File: `src/cratekit/intake/land_cli.py`
- Source: `u120.json`, row `C2_hearts_not_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 14 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_dated_the_twentieth_of_october_joins_its_month_and_no_quarter_is_made`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_homes_refusal_that_is_not_the_missing_source_refuses_the_landing`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_an_undated_heart_lands_in_the_undated_playlist`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    hearted = account_playlists.hearted(cfg, pass_name, planned.items)
```

New text:

```
    hearted = ()
```

### `u153.L3_notes_colour_skipped`

land_cli favorites_notes: never emit the missing-Pink note, so a landing that coloured nothing says nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u153.json`, row `L3_notes_colour_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
    if placed.colour_skipped:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

New text:

```
    if False:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

### `u120.N3_identity_without_hearts`

identity: the digest leaves the hearts out

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N3_identity_without_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`

Old text:

```
    favorites = {"favorites": plan.favorites.identity()} if plan.favorites is not None else {}
```

New text:

```
    favorites = {}
```

### `u120.N4_skipped_is_raised`

_favorites_plan: a home that cannot be resolved raises through the landing

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N4_skipped_is_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    try:
        home = placement.resolve_home(db, source)
    except CratekitError as exc:
```

New text:

```
    try:
        home = placement.resolve_home(db, source)
    except ValueError as exc:
```

### `r835-b.T1_folder_create_never_retried`

TidalAccount.create_folder: a create that timed out after reaching the provider is retried into a second folder

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T1_folder_create_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_create_is_never_retried_into_a_second_folder`

Old text:

```
            doing, lambda: self._session.user.create_folder(name), retries=0
```

New text:

```
            doing, lambda: self._session.user.create_folder(name), retries=1
```

### `r835-b.T2_refused_move_raised`

TidalAccount.move_to_folder: a move the client answers False is returned as done

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T2_refused_move_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_move_the_client_answers_false_is_a_failure_not_a_quiet_return`

Old text:

```
        if moved is False or moved is _ABSENT:
```

New text:

```
        if moved is _ABSENT:
```

### `r835-c.T3_short_answer_read_again_again`

TidalAccount.add_tracks: an add answer that leaves a track out is trusted, so a track the playlist holds is reported refused

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-c.json`, row `T3_short_answer_read_again_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_an_add_answered_with_nothing_is_read_again_and_not_reported_refused`

Old text:

```
            if unconfirmed:
                del self._members[playlist_id]
```

New text:

```
            if False:
                del self._members[playlist_id]
```

### `u44-author.C2_argv_drops_overwrite`

Drop --overwrite from the resume argv, so a respawned child meets the refusal the first run was told to ignore

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C2_argv_drops_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag`

Old text:

```
    if payload.get(OVERWRITE):
        argv.append("--overwrite")
```

New text:

```
(empty)
```

### `u44-author.C3_argv_drops_output_dir`

Drop --output-dir from the resume argv, so the child writes the master somewhere the person did not ask for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C3_argv_drops_output_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag`

Old text:

```
    if output_dir:
        argv += ["--output-dir", str(output_dir)]
```

New text:

```
(empty)
```

### `u44-author.C4_refusal_not_translated`

Let MasteringRefused escape, so every engine refusal reaches the person as internal-error

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C4_refusal_not_translated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 23 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    except mastering.MasteringRefused as exc:
        raise refuse(
            str(exc.refusal),
            exc.detail,
            origin=("master", "cli"),
            detail={"path": str(exc.path) if exc.path is not None else None},
        ) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise refuse(
            str(exc),
            "unreachable",
            origin=("master", "cli"),
        ) from exc
```

### `u44-author.C6_overwrite_always_true`

Freeze overwrite as always true, so every run replaces an existing master without being asked to

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C6_overwrite_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
        OVERWRITE: bool(overwrite),
```

New text:

```
        OVERWRITE: True,
```

### `u44-author.C7_output_dir_ignored_at_the_work`

Ignore the frozen output directory, so the master lands beside the source whatever was asked for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C7_output_dir_ignored_at_the_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`
  - `tests/test_master_cli.py::test_the_output_directory_is_honoured_and_never_the_source`

Old text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=None,
```

### `r382.M16_parser_moved_lowercase`

The moved parser keeps a bare identifier's case, checking the move kept its tests

- File: `src/cratekit/label/catalogue.py`
- Source: `r382.json`, row `M16_parser_moved_lowercase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 891 against a baseline of 891
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_url_a_share_link_and_a_bare_id_all_name_the_playlist[bare-upper]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`

Old text:

```
    if _UUID.fullmatch(text):
        return text.lower()
```

New text:

```
    if _UUID.fullmatch(text):
        return text
```

### `u261.W1_unchanged_skip_removed`

write_back: drop the unchanged comparison, so every login writes the value already stored back to the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W1_unchanged_skip_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 481 against a baseline of 481
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_an_unchanged_session_makes_no_keychain_write`
  - `tests/test_provider_session_hold.py::test_an_unchanged_toml_session_is_not_written_back`
  - `tests/test_provider_session_hold.py::test_the_surveys_drive_logs_in_once_and_writes_nothing`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
            return False
```

New text:

```
        if False:
            return False
```

### `u261.W2_changed_session_skipped`

write_back: read any encodable session as unchanged, so a refreshed token is never stored (the merge blocker the card names)

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W2_changed_session_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 481 against a baseline of 481
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_refreshed_session_goes_back_to_the_keychain`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refreshed_session_is_written_once_through_the_index`
  - `tests/test_provider_session_hold.py::test_a_session_the_tool_changed_is_written_back_from_the_scope`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
```

New text:

```
        if unchanged is not None:
```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 886 against a baseline of 886
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    for genre in bucket.genre_subs:
        if genre.id == sub_id:
            return bucket.display, genre.display
```

New text:

```
(empty)
```

### `u278.M18_reading_noop`

reading: never narrow the command

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M18_reading_noop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`

Old text:

```
    scope.reserve = False
    if settings is not None:
```

New text:

```
    if settings is not None:
```

### `u278.M4_no_budget_check`

Gate.call: drop the hour's line, so a call past it is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M4_no_budget_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 17 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
  - `tests/test_provider_budget.py::test_a_raised_ceiling_never_spends_the_reserve`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`
  - `tests/test_provider_budget.py::test_the_budget_counts_every_command_and_every_gate_on_the_file`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`
  - ... and 2 more, see the JSON sidecar

Old text:

```
                if spent >= hour_line:
```

New text:

```
                if False:
```

### `u278.M8_no_reserve`

line_for: a read reaches the whole budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M8_no_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 23 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
  - `tests/test_provider_budget.py::test_a_raised_ceiling_never_spends_the_reserve`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve`
  - `tests/test_provider_budget.py::test_doctor_names_an_identity_at_its_read_line_and_when_it_frees`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return budget - reserve_of(budget, settings.reserve_share)
```

New text:

```
    return budget
```

### `r1289.M10_warning_ready_filter`

_plan_playlists: the unread warning covers a playlist that was not queued, saying its other tracks are

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M10_warning_ready_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if identity in sweep.ready
```

New text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if True
```

### `r1289.M11_warning_absent`

_plan_playlists: no unread warning at all

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M11_warning_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
    if left:
```

New text:

```
    if False:
```

### `r1289.M12_warning_promise`

_plan_playlists: the warning reworded to promise a later sync offers the playlist again, which is false once its job succeeds

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M12_warning_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                    "playlist's intake job succeeds no later sync offers it again, so "
```

New text:

```
                    "playlist's intake job succeeds the next sync takes it up again, so "
```

### `r1289.M13_warning_names`

_plan_playlists: the warning names each playlist but not its unread tracks

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M13_warning_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                        + ", ".join(f"{ref} ({one['why']})" for ref, one in tracks.items())
```

New text:

```
                        + "some tracks"
```

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 262 against a baseline of 262
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_from_the_same_source_gets_a_distinct_name`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_for_the_date_and_tidal_playlists`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_landing.py::test_three_tagged_files_land_in_one_intake_file`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_the_labelled_intake_file_golden`
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`

Old text:

```
            playlist=plan.batch,

```

New text:

```
(empty)
```

### `u110-c.C7_intake_lock_prefix`

The intake lock shares its key with a batch of the same name

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C7_intake_lock_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 262 against a baseline of 262
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output`
  - `tests/test_intake_land.py::test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared`
  - `tests/test_intake_land.py::test_the_landed_envelope_carries_an_import_that_blocks_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_held_for_the_whole_of_the_apply`
  - `tests/test_intake_land.py::test_the_lock_is_released_after_a_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_every_target_taken]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
lock_key("intake file\0" + stem)
```

New text:

```
lock_key(stem)
```

