# Mutation table: u325-after-h-03

Measured by `scripts/mutate.py` on 2026-11-23 00:26 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 71.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r664.E2_pair_rule_field_by_field` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 120 | killed |
| `r664.G5_key_not_read_from_the_tag_head` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r664.G6_tag_head_outranks_stem_head` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 4 | killed |
| `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 2 | killed |
| `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 3 | killed |
| `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 31 | killed |
| `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 4 | killed |
| `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 2 | killed |
| `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 9 | killed |
| `u212.M10_left_out` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M1_staged_match` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 6 | killed |
| `u212.M2_own_rows_both` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 3 | killed |
| `u212.M3_own_rows_by_id` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M4_own_rows_by_isrc` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M5_unread_is_empty` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M6_absent_folder` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M7_outcome_staged` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `u212.M8_summary_count` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 5 | killed |
| `u212.M9_unread_status` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1445 | 1 | killed |
| `r923.N18_policy_owns_the_fields` | `src/cratekit/core/rb_writer.py` | user | 41 file(s) | 3914 | 1 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_writer.py` | user | 41 file(s) | 3914 | 45 | killed |
| `u115.F3_file_id_policy_fill_if_empty` | `src/cratekit/core/rb_writer.py` | user | 41 file(s) | 3914 | 3 | killed |
| `u115.F4_binding_limit_coefficient` | `src/cratekit/core/rb_writer.py` | maintainer | 41 file(s) | 3914 | 1 | killed |
| `u166.C10_live_filter` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 7 | killed |
| `u166.C1_removed_row` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C2_analysed_flag` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 2 | killed |
| `u166.C3_analysis_path` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C4_blank_path` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C5_missing_row` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C6_stale_check` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C7_clear_waits_too` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 4 | killed |
| `u166.C8_read_back_lost` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C9_read_back_kept` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1066 | 2 | killed |
| `u166.C12_ack_first` | `src/cratekit/intake/analyzed_cli.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C13_read_back_call` | `src/cratekit/intake/analyzed_cli.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u152.R13_missing_lift` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R14_download_list_match` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R15_download_newest` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R16_download_cancelled` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R17_download_retry` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R20_nothing_downloaded` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R2_preflight_backup` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R6_lift_failed_checks` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R7_outbound_held` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R8_continue_open_pass` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R9_open_passes_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u190.L10_rest_of_tail_after_a_step_gate` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L11_done_keeps_the_go_outcome` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L1_no_tail_returns_untouched` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 146 | killed |
| `u190.L2_land_of_needs_a_mapping` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 56 | killed |
| `u190.L3_landing_carries_manifest` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 19 | killed |
| `u190.L4_landing_carries_pass` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 19 | killed |
| `u190.L5_land_stop_rekordbox_visit` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L6_way_on_from_the_stopped_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L7_pending_id_names_the_go` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L9_verify_verb_by_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |

## Row definitions

### `r664.E2_pair_rule_field_by_field`

Collapse the pair rule to field by field fallback, the shape that assembled an identity matching neither source

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E2_pair_rule_field_by_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`

Old text:

```
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

New text:

```
    artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E4_title_not_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 120 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resume_that_redoes_an_offered_item_asks_nothing_twice`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_and_no_intake_file_is_written`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_favorites_resolves_each_heart_owned_offered_or_missing`
  - `tests/intake/test_workers.py::test_identify_reports_an_owned_track_owned_an_offered_one_offered_and_the_rest_missing`
  - `tests/intake/test_workers.py::test_the_missing_hearts_carry_the_provider_id_acquisition_reads`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`
  - `tests/intake/test_workers.py::test_the_resolution_names_owned_offered_and_missing_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - ... and 105 more, see the JSON sidecar

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `r664.G5_key_not_read_from_the_tag_head`

Stop reading the key off a head found only inside the title tag, the first draft's precedence the review reversed

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `G5_key_not_read_from_the_tag_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = head.get("key") or tag_head.get("key")

```

New text:

```
    written_key = head.get("key")

```

### `r664.G6_tag_head_outranks_stem_head`

Let the head inside the tag outrank the head in the filename

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `G6_tag_head_outranks_stem_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = head.get("key") or tag_head.get("key")

```

New text:

```
    written_key = tag_head.get("key") or head.get("key")

```

### `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed`

Continue past a refused off-machine half instead of translating it, so the capture half runs over a mirror that never landed

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A10_an_off_machine_refusal_is_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`

Old text:

```
            except backup.BackupRefused as exc:
                raise _refused(exc) from exc
```

New text:

```
            except backup.BackupRefused:
                pulled = None
```

### `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session`

Drop the identity and mount seams from recovery_session, so the volume gate answers from this machine rather than from the caller

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A3_platform_seams_never_reach_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

Old text:

```
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ) as held:
```

New text:

```
        analysis_roots=watched,
    ) as held:
```

### `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine`

Plan with an empty discard set, so the override a person typed is dropped between the verb and the engine

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A8_discard_set_never_reaches_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=discarding,
            process_lister=process_lister,
        )
```

New text:

```
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=(),
            process_lister=process_lister,
        )
```

### `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine`

Pass no session identifier at all, so a named restore performs only the off-machine half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B2_the_named_session_never_reaches_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`
  - `tests/test_restore_cli.py::test_the_confirmation_is_two_acts_and_then_the_database_comes_back`
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
```

New text:

```
        session_id=None,
        discarding=tuple(ctx.args.discard),
```

### `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call`

Hand the engine an empty discard set from the handler, the argument-side twin of I_A8

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B3_the_discard_flag_is_dropped_at_the_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
```

New text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=(),
```

### `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call`

Perform for real whatever --dry-run said, the argument-side twin of the author's two in-function rehearsal rows

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B7_the_rehearsal_flag_is_dropped_at_the_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`

Old text:

```
        dry_run=ctx.args.dry_run,
        from_backup=ctx.args.from_backup,
```

New text:

```
        dry_run=False,
        from_backup=ctx.args.from_backup,
```

### `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable`

Take a single discard identifier rather than an appended list, so a person discarding two sessions names one and the string is iterated character by character

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C1_discard_stops_being_repeatable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        "--discard",
        action="append",
        default=[],
```

New text:

```
        "--discard",
        default="",
```

### `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required`

Make the positional mandatory, so a bare crate restore run is a usage error rather than the newest spendable capture

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C4_the_session_identifier_becomes_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 31 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[restore.run]`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_a_database_that_is_not_on_disk_yet_is_still_the_live_database`
  - `tests/test_restore_cli.py::test_a_differently_cased_ancestor_still_puts_the_target_inside_the_library`
  - `tests/test_restore_cli.py::test_a_differently_cased_database_directory_is_still_the_live_database`
  - `tests/test_restore_cli.py::test_a_differently_cased_library_root_is_still_the_library`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`
  - `tests/test_restore_cli.py::test_a_target_beside_a_capture_rollback_is_refused[extra0]`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - ... and 16 more, see the JSON sidecar

Old text:

```
        "session_id",
        nargs="?",
        default=None,
```

New text:

```
        "session_id",
```

### `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore`

Bind the read-only listing to the destructive handler

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C6_the_listing_verb_runs_the_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`
  - `tests/test_restore_cli.py::test_the_listing_answers_on_a_library_that_has_never_acknowledged_a_backup`
  - `tests/test_restore_cli.py::test_the_listing_shows_a_session_with_its_timestamp_workflow_and_per_tree_counts`

Old text:

```
    parser.set_defaults(_handler=list_restorable)
```

New text:

```
    parser.set_defaults(_handler=perform_restore)
```

### `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked`

List an unusable capture with no sentence saying why, which is the silence the field exists to avoid

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_E4_the_reason_a_capture_cannot_be_spent_is_blanked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`

Old text:

```
        "unusable": entry.unusable,
```

New text:

```
        "unusable": "",
```

### `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier`

Reword the refusal so it never repeats what was typed, which is what makes a typo diagnosable

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_F4_the_refusal_stops_naming_the_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_identifier_nothing_recorded_is_refused_by_name`

Old text:

```
                f"no write session on this library is recorded under "
                f"{session_id!r}; the listing verb shows every one that is"
```

New text:

```
                "no such write session is recorded on this library; the "
                "listing verb shows every one that is"
```

### `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened`

What the refusal-message zero DOES leave held: fold the off-machine slug into an internal error, which is the half a drive does assert. Paired with I_F1, which replaced the sentence and killed nothing

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `X5_the_refusal_reason_is_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_recovery_is_refused_underneath_a_running_rekordbox`
  - `tests/test_restore_cli.py::test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
            reason=slug,
            message=exc.detail,
```

New text:

```
            reason="internal-error",
            message=exc.detail,
```

### `u212.M10_left_out`

missing_cli._listed: drop the staged clause of the left out refusal, so a run with a failed job and every finished row staged refuses

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M10_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`

Old text:

```
    if left_out and not listed and not unlisted and not staged_rows:
```

New text:

```
    if left_out and not listed and not unlisted:
```

### `u212.M1_staged_match`

missing_cli._staged: never record a staged row, so a track a staged file carries is listed and downloaded again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M1_staged_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[neither]`
  - `tests/test_intake_missing_staged.py::test_every_missing_track_staged_is_something_to_land_not_a_no_op`

Old text:

```
        if held:
            found.append((n, held[0].path))
```

New text:

```
        if held and False:
            found.append((n, held[0].path))
```

### `u212.M2_own_rows_both`

missing_cli._staged: drop the own rows rule, so a continued pass subtracts its own staged downloads and its list is refused over its earlier copy

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M2_own_rows_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_track_this_lists_own_earlier_copy_names_stays_listed_once_staged`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
            continue
```

New text:

```
        if False:
            continue
```

### `u212.M3_own_rows_by_id`

missing_cli._staged: the own rows rule by ISRC alone, the provider id half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M3_own_rows_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if token in isrcs:
```

### `u212.M4_own_rows_by_isrc`

missing_cli._staged: the own rows rule by provider id alone, the ISRC half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M4_own_rows_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if ref and ref in ids:
```

### `u212.M5_unread_is_empty`

missing_cli._staged: an unreadable staging folder read as one holding nothing, so the staged row says nothing failed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M5_unread_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staging_folder_that_cannot_be_read_is_said_never_read_as_nothing_staged`

Old text:

```
        return _Staged(folder, unread=str(exc.strerror or exc))
```

New text:

```
        return _Staged(folder)
```

### `u212.M6_absent_folder`

missing_cli._staged: drop the absent folder guard, so a machine with no staging folder yet reports the folder unreadable

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M6_absent_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_track_this_lists_own_earlier_copy_names_stays_listed_once_staged`

Old text:

```
        if not folder.exists():
```

New text:

```
        if False:
```

### `u212.M7_outcome_staged`

missing_cli._listed: every row staged answers no_op, so a pass ends before the landing that takes them

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M7_outcome_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_every_missing_track_staged_is_something_to_land_not_a_no_op`

Old text:

```
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed or unlisted else Outcome.NO_OP,
```

### `u212.M8_summary_count`

missing_cli._listed: the summary's staged count read as zero, the number the pass reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M8_summary_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`
  - `tests/test_intake_missing_staged.py::test_every_missing_track_staged_is_something_to_land_not_a_no_op`

Old text:

```
        "staged": len(staged_rows),
```

New text:

```
        "staged": 0,
```

### `u212.M9_unread_status`

missing_cli._staged_check: an unreadable staging folder said on an info row rather than a failing one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M9_unread_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1445 against a baseline of 1445
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staging_folder_that_cannot_be_read_is_said_never_read_as_nothing_staged`

Old text:

```
            "staged",
            "fail",
```

New text:

```
            "staged",
            "info",
```

### `r923.N18_policy_owns_the_fields`

The defaults policy owns its fields outright instead of filling only an empty one

- File: `src/cratekit/core/rb_writer.py`
- Source: `r923.json`, row `N18_policy_owns_the_fields`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_every_default_is_a_real_column_and_none_is_an_analysis_column`

Old text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.FILL_IF_EMPTY)),
```

New text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.OWNED)),
```

### `r923.N19_default_is_an_analysis_column`

A tempo joins the defaults table, so the landing would declare an analysis column

- File: `src/cratekit/core/rb_writer.py`
- Source: `r923.json`, row `N19_default_is_an_analysis_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
- Kills: 45 (killed)
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
  - ... and 30 more, see the JSON sidecar

Old text:

```
        "Rating": 0,
        "ColorID": "0",
```

New text:

```
        "Rating": 0,
        "BPM": 0,
        "ColorID": "0",
```

### `u115.F3_file_id_policy_fill_if_empty`

The file id policy fills only an empty column, so a random id present on the row is never replaced

- File: `src/cratekit/core/rb_writer.py`
- Source: `u115.json`, row `F3_file_id_policy_fill_if_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.OWNED}),
```

New text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.FILL_IF_EMPTY}),
```

### `u115.F4_binding_limit_coefficient`

The binding's id limit is taken as 32 bits rather than 28

- File: `src/cratekit/core/rb_writer.py`
- Source: `u115.json`, row `F4_binding_limit_coefficient`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`

Old text:

```
BINDING_ID_LIMIT = 1 << 28
```

New text:

```
BINDING_ID_LIMIT = 1 << 32
```

### `u166.C10_live_filter`

live_members: count a removed membership as held

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C10_live_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 7 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_second_clear_plans_nothing`
  - `tests/test_inbox_analyzed.py::test_a_track_held_twice_is_one_row_cleared_and_counted_once`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`

Old text:

```
        if not rb_writer.membership_removed(song)
```

New text:

```
        if True
```

### `u166.C1_removed_row`

_member: clear a row whose collection row was removed

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C1_removed_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`

Old text:

```
    if removed:
        return Member(content_id=content_id, title=title, action=WAIT, why=ROW_REMOVED)
```

New text:

```
    if False:
        return Member(content_id=content_id, title=title, action=WAIT, why=ROW_REMOVED)
```

### `u166.C2_analysed_flag`

_member: clear a row whose Analysed is unset

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C2_analysed_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_with_an_analysis_path_and_analysed_unset_stays`

Old text:

```
    if not int(getattr(row, "Analysed", 0) or 0):
```

New text:

```
    if False:
```

### `u166.C3_analysis_path`

_member: clear a row with no analysis path

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C3_analysis_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`

Old text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or "").strip():
```

New text:

```
    if False:
```

### `u166.C4_blank_path`

_member: read a blank analysis path as present

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C4_blank_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`

Old text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or "").strip():
```

New text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or ""):
```

### `u166.C5_missing_row`

_member: clear a membership whose collection row is missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C5_missing_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`

Old text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

New text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=CLEAR)
```

### `u166.C6_stale_check`

apply_clear: apply a plan whose digest moved

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C6_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_analysis_finished_after_the_approval_is_refused_by_the_engine`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u166.C7_clear_waits_too`

apply_clear: remove every member, waiting ones too

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C7_clear_waits_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`

Old text:

```
rb_writer.remove_memberships(db, playlist, plan.clears())
```

New text:

```
rb_writer.remove_memberships(db, playlist, [m.content_id for m in plan.members])
```

### `u166.C8_read_back_lost`

assert_read_back: stop refusing a waiting row gone

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C8_read_back_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept`

Old text:

```
    if lost or kept:
```

New text:

```
    if kept:
```

### `u166.C9_read_back_kept`

assert_read_back: stop refusing a cleared row kept

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C9_read_back_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept`

Old text:

```
    if lost or kept:
```

New text:

```
    if lost:
```

### `u166.C12_ack_first`

inbox_analyzed: drop the backup acknowledgment before the plan

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C12_ack_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u166.C13_read_back_call`

inbox_analyzed: skip the read back after the commit

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C13_read_back_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`

Old text:

```
    analyzed.assert_read_back(plan, cleared)
```

New text:

```
    pass
```

### `u152.R13_missing_lift`

_missing: carry none of the listing's failing rows

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R13_missing_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`

Old text:

```
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.
    _lift_failed_checks(report, envelope)

```

New text:

```
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.

```

### `u152.R14_download_list_match`

_download_job: drop the list match, so another list's download job is read as the pass's

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R14_download_list_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`

Old text:

```
            and str((job.payload or {}).get(acquire_cli.LIST) or "") == wanted

```

New text:

```
(empty)
```

### `u152.R15_download_newest`

_download_job: read the oldest job over the list, the round two defect

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R15_download_newest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    for job in jobs.list_jobs(store):
        if (
            job.handler_key == key
```

New text:

```
    for job in reversed(jobs.list_jobs(store)):
        if (
            job.handler_key == key
```

### `u152.R16_download_cancelled`

_download_job: read a cancelled download as the pass's claim on the list

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R16_download_cancelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`

Old text:

```
            and job.state is not jobs.JobState.CANCELLED

```

New text:

```
(empty)
```

### `u152.R17_download_retry`

_download: never retry a download that failed transiently, so a continued pass reads it as settled

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R17_download_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`

Old text:

```
            job = jobs.retry(store, job.job_id)
```

New text:

```
            pass
```

### `u152.R20_nothing_downloaded`

_download: go on to the tail when the download landed nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R20_nothing_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    if not done:
        report.check(
```

New text:

```
    if False:
        report.check(
```

### `u152.R2_preflight_backup`

_preflight: drop the backup driver check, so a pass runs beside a live backup

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R2_preflight_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_running_backup_refuses_before_any_write`

Old text:

```
        try:
            jobs.assert_free(job.job_id)
        except jobs.DriverHeld as exc:
```

New text:

```
        try:
            pass
        except jobs.DriverHeld as exc:
```

### `u152.R6_lift_failed_checks`

_lift_failed_checks: carry no step's failing row, so the withheld hearts and the unnameable tracks are said nowhere

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R6_lift_failed_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
        if check.get("key") in held:
            continue
        report.checks.append(dict(check))
```

New text:

```
        if check.get("key") in held:
            continue
```

### `u152.R7_outbound_held`

_lift_failed_checks: lift the unasked outbound write's refusal as a FAIL row on every pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R7_outbound_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`

Old text:

```
        if check.get("key") in held:
            continue

```

New text:

```
(empty)
```

### `u152.R8_continue_open_pass`

_sync: never continue the one earlier pass sync all left out, so a hand typed pass ends no_op

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R8_continue_open_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`

Old text:

```
        if len(earlier) == 1:
```

New text:

```
        if False:
```

### `u152.R9_open_passes_library`

_open_intake: drop the library filter, so another library's open pass is continued

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R9_open_passes_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_that_ended_or_belongs_to_another_library_is_not_continued`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
            and job.library_id == cfg.library.volume_id
        ]


def _run_of
```

New text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
        ]


def _run_of
```

### `u190.L10_rest_of_tail_after_a_step_gate`

_attended: name nothing after a tail step's own gate, so the rest of the tail is left unsaid

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L10_rest_of_tail_after_a_step_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        after = tuple(f"then: {one}" for one in _commands(folder, landing, stop.step)[1:])
```

New text:

```
        after = ()
```

### `u190.L11_done_keeps_the_go_outcome`

label_sync: end a landing that planned nothing as NO_OP, hiding the download the go made

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L11_done_keeps_the_go_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
        outcome=envelope.outcome,
```

New text:

```
        outcome=Outcome.NO_OP,
```

### `u190.L1_no_tail_returns_untouched`

label_sync: run the chain over a go that names no tail

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L1_no_tail_returns_untouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 146 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[label.sync]`
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv3-go with --answer]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv5-goes with --answer pick]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv6---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv7---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_labels_own_offer_bounds_a_first_question`
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - ... and 131 more, see the JSON sidecar

Old text:

```
    if land is None:
        return envelope
    cfg
```

New text:

```
    if land is None:
        land = {"folder": "/nowhere", "pass": "none"}
    cfg
```

### `u190.L2_land_of_needs_a_mapping`

_land_of: read the go's report without its key, so no tail is ever run

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L2_land_of_needs_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 56 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - ... and 41 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("tail") if isinstance(report, Mapping) else None
```

### `u190.L3_landing_carries_manifest`

_landing_args: drop the manifest, so the landing files the label's rows under no label

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L3_landing_carries_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        *(["--manifest", str(manifest)] if isinstance(manifest, str) and manifest else []),
```

New text:

```
        *([] if isinstance(manifest, str) and manifest else []),
```

### `u190.L4_landing_carries_pass`

_landing_args: drop the pass, so the landing's intake file is named for nothing the go named

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L4_landing_carries_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        "--pass",
        str(land["pass"]),
    ]
```

New text:

```
    ]
```

### `u190.L5_land_stop_rekordbox_visit`

_attended: follow the landing's gate with the next tail command rather than the rekordbox visit

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L5_land_stop_rekordbox_visit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
    if stop.step == tail.LAND:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

New text:

```
    if False:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

### `u190.L6_way_on_from_the_stopped_step`

_commands: name the whole tail from its first step, so a person reruns steps that succeeded

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L6_way_on_from_the_stopped_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
tail.STEPS[tail.STEPS.index(step):]
```

New text:

```
tail.STEPS[0:]
```

### `u190.L7_pending_id_names_the_go`

_attended: name the pending action for the landing's run rather than the go's

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L7_pending_id_names_the_go`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
        id=f"label-sync-{ctx.run.run_id}",
```

New text:

```
        id=f"label-sync-{chain.summary.get('gate_run')}",
```

### `u190.L9_verify_verb_by_step`

_attended: name the landing as the verb to verify whatever step stopped

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L9_verify_verb_by_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        verify_verb=tail.LAND_VERB if stop.step == tail.LAND else ctx.entry.name,
```

New text:

```
        verify_verb=tail.LAND_VERB,
```

