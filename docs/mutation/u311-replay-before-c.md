# Mutation table: u311-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-23 00:58 UTC, branch `HEAD` at `48a0103d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 135.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 21:22 UTC for commit `48a0103d4f0a`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 12, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r187-a.C1_blank_not_key` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `r187-a.C2_uncapped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C3_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `r187-a.C4_key_beside_name` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C5_empty_name_scans` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C6_no_cache_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u43-author-light.A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.C1_no_lower_bound` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.C2_bound_off_by_one` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P1_anchor_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P3_pool_leads_the_items` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-light.P4_no_positions_at_all` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.P5_role_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P7_vox_threshold_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.A2_no_resolved_second_pass` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P2_items_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P6_count_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V1_pool_total_is_the_union` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.K1_key_off_wheel` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 7 | killed |
| `u98-a.T1_tempo_nonfinite` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.T2_tempo_zero` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U1_empty_label` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U2_key_missing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.U3_reported_owned` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 5 | killed |
| `u98-a.U4_tempo_dropped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-a.X1_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.E1_existing_containment` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-b.H1_held_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H2_held_not_reported` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H3_held_fuzzy` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.S1_supplied_beside_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.S2_tempo_half` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.A10_ambiguous_falls_through` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-a.A11_no_cutoff` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 4 | killed |
| `r187-a.A12_partial_message` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-a.A1_exact_first` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 2 | killed |
| `r187-a.A3_holds_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 4 | killed |
| `r187-a.A4_word_threshold_low` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-a.A5_word_threshold_high` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-a.A6_first_of_several` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 4 | killed |
| `r187-a.A7_partial_never` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 3 | killed |
| `r187-a.A8_walk_order` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-a.A9_key_discarded` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B10_bad_track_is_current` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 7 | killed |
| `r187-b.B12_not_carried_forward` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B1_size_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B3_entry_not_a_mapping` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 2 | killed |
| `r187-b.B4_empty_read_cached` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B5_empty_walk_writes` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B6_stamp_unchecked` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `r187-b.B8_bool_is_a_number` | `src/cratekit/modules/tools/setbuilder.py` | maintainer | 2 file(s) | 295 | 1 | killed |
| `u43-author-light.E1_anchor_is_its_own_companion` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 8 | killed |
| `u43-author-light.E2_tempo_band_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 1 | killed |
| `u43-author-light.E3_tempo_serialized_as_bpm` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 5 | killed |
| `u98-b.P1_either_twice` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 295 | 2 | killed |
| `u105-a.E10_parts_archived` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E11_join_dir_removed` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E12_join_rf64` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E13_joined_suffix` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 5 | killed |
| `u105-a.E14_single_part_name` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 4 | killed |
| `u105-a.E15_payload_parts_conditional` | `src/cratekit/modules/tools/mastering.py` | maintainer | 3 file(s) | 284 | 1 | killed |
| `u105-a.E1_lufs_range_removed` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 7 | killed |
| `u105-a.E2_lufs_high_bound` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 2 | killed |
| `u105-a.E3_lufs_nan` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 2 | killed |
| `u105-a.E4_duplicate_part` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E5_mixed_containers` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E6_joined_output_exists` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E7_layout_rate` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E8_layout_channels` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `u105-a.E9_layout_codec` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 284 | 1 | killed |
| `r598-b.B1_sweep_before_the_lock` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B3_orphans_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r598-b.B4_abandon_only_reported_as_no_op` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B5_kept_reports_nothing` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A6_the_authorisation_is_not_spent` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A7_the_check_rows_are_keyed_wrong` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A8_a_damaged_record_locks_the_verb_out` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R1_hard_code_the_repair_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R2_hard_code_the_permission_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.R3_an_unreadable_file_reads_as_empty` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u45-round-1.E1_rehearsal_publishes` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 7 | killed |
| `u45-round-1.E2_publish_unconditional` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 7 | killed |
| `u45-round-1.E4_return_codes_unread` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 21 | killed |
| `u45-round-2.E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 1 | killed |
| `u48-author.E1_listing_return_code_inverted` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 18 | killed |
| `u48-author.P1_listing_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 4 | killed |
| `u48-author.P2_purge_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 1 | killed |
| `u48-author.P4_warning_not_recorded_on_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 5 | killed |
| `u48-author.P6_purge_count_not_named` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 1 | killed |
| `u48-author.P7_listing_message_reworded` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 725 | 1 | killed |
| `u44-author-round-2.A1_archive_verify_dropped` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 1 | killed |
| `u44-author-round-2.A4_digest_reads_first_chunk_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 1 | killed |
| `u44-author-round-2.B3_concat_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 1 | killed |
| `u44-author.A2_archive_collision_skips` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 3 | killed |
| `u44-author.A3_archive_after_the_first_pass` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 1 | killed |
| `u44-author.B1_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 3 | killed |
| `u44-author.B2_output_existence_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 282 | 1 | killed |
| `u44-author.C2_argv_drops_overwrite` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C3_argv_drops_output_dir` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C4_refusal_not_translated` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 23 | killed |
| `u44-author.C6_overwrite_always_true` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 4 | killed |
| `u44-author.C7_output_dir_ignored_at_the_work` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 3 | killed |
| `u28-skills-independent.S10_stamp_skill_name` | `src/cratekit/skills/cli.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u28-skills-independent.S13_expanduser` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u28-skills-independent.S17_outcome_always_ok` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u28-skills-independent.S20_packaged_root_via_file` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u181.E1_direct_reference_unread` | `src/cratekit/modules/extras.py` | user | 3 file(s) | 464 | 3 | killed |
| `u192.F6_queue_only_never` | `src/cratekit/modules/foreground.py` | user | 4 file(s) | 409 | 20 | killed |
| `u211.B1_backup_database_portion_refuses_alone` | `src/cratekit/modules/tools/backup.py` | user | 3 file(s) | 180 | 1 | killed |
| `u27-restore-cli-round-2.G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 1095 | 1 | killed |

## Zero rows and what they owe

- `u28-skills-independent.S10_stamp_skill_name` (maintainer facing): maintainer facing, composite not required
- `u28-skills-independent.S13_expanduser` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S17_outcome_always_ok` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S20_packaged_root_via_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r187-a.C1_blank_not_key`

names_something: ask the text and not the comparison key, so a name of punctuation alone is searched for

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C1_blank_not_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_with_nothing_in_it_is_an_unknown_anchor[ - ]`
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
    return bool(setbuilder.match_key("", text))
```

New text:

```
    return bool(text.strip())
```

### `r187-a.C2_uncapped`

named_anchor: list every candidate, so a vague name prints a whole label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C2_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    shown = matched.candidates[: setbuilder.CANDIDATE_LIMIT]
```

New text:

```
    shown = matched.candidates
```

### `r187-a.C3_mutex`

build: declare --named on the parser and not in the exclusive group, so it can sit beside a path or a label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C3_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`

Old text:

```
    anchor.add_argument(
        "--named",
```

New text:

```
    parser.add_argument(
        "--named",
```

### `r187-a.C4_key_beside_name`

set_build: a key beside --named is let through and silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C4_key_beside_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.named is None and (ctx.args.key is not None or ctx.args.tempo is not None):
```

### `r187-a.C5_empty_name_scans`

set_build: an empty name pays for the library walk before it is refused

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C5_empty_name_scans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
```

New text:

```
        index = _index(cfg, root)
```

### `r187-a.C6_no_cache_path`

_index: pass no cache path, which is R-188 itself, every set a full scan

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C6_no_cache_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys`

Old text:

```
        cache_path=config.state_path("setbuilder_index_cache", cfg),
```

New text:

```
        cache_path=None,
```

### `u43-author-light.A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A1_first_track_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated`
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `u43-author-light.A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A3_containment_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if _within(candidate, root) and False:
```

### `u43-author-light.A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A4_empty_anchor_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_is_refused_rather_than_defaulted`
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_refuses_through_the_dispatcher`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `u43-author-light.C1_no_lower_bound`

positive_count stops refusing zero and negatives, so build_plan's pool[: count or DEFAULT_POOL] silently turns 0 into 8 and -1 into a dropped last companion

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C1_no_lower_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-1]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-8]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value
```

New text:

```
    return int(text)
```

### `u43-author-light.C2_bound_off_by_one`

The bound is loosened by one rather than removed, so zero passes and negatives do not. A guard whose constant can be moved without a death is a guard that pins nothing.

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C2_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    if value < 1:
```

New text:

```
    if value < 0:
```

### `u43-author-light.P1_anchor_absent_from_digest`

The digest stops covering the anchor, so two plans over the same companions and different anchors are indistinguishable

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P1_anchor_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "items": items}),
```

### `u43-author-light.P3_pool_leads_the_items`

The pool leads and the sequence follows, so the recommendation is no longer at the top of the array a consumer reads

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P3_pool_leads_the_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]
```

New text:

```
    ordered = [s for s in plan.pool if id(s) not in placed] + list(plan.sequence)
```

### `u43-author-light.P4_no_positions_at_all`

Every item reports position null, so the suggested sequence is not recoverable from the payload

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P4_no_positions_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
        {**entry, "position": placed.get(id(scored))}
```

New text:

```
        {**entry, "position": None}
```

### `u43-author-light.P5_role_ignored`

The role flag is dropped on the way to the engine, so --role before answers with both sides

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P5_role_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_role_narrows_the_answer_to_one_side`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=None)
```

### `u43-author-light.P7_vox_threshold_ignored`

The vocal threshold is dropped on the way to the ranker, which makes the fifth ranking signal permanently neutral and its whole weight dead

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P7_vox_threshold_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied`

Old text:

```
        vox_threshold=vox_threshold,
    )
    plan = setbuilder.build_plan
```

New text:

```
        vox_threshold=None,
    )
    plan = setbuilder.build_plan
```

### `u43-author-round-2.A2_no_resolved_second_pass`

ROUND ONE: zero. Drop the resolved second pass in anchor_in_index, so a path spelled through a symlink or a different absolute form never matches

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `A2_no_resolved_second_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`

Old text:

```
    try:
        resolved = path.resolve()
    except OSError:
        return None
    for track in index:
        if not track.path:
            continue
        try:
            if Path(track.path).resolve() == resolved:
                return track
        except OSError:
            continue
    return None
```

New text:

```
    return None
```

### `u43-author-round-2.H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H2_empty_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `u43-author-round-2.H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H3_missing_root_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `u43-author-round-2.P2_items_absent_from_digest`

ROUND ONE: zero. The digest stops covering the items, so two entirely different sets of recommendations for one anchor carry one identity

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P2_items_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_two_plans_over_the_same_anchor_and_different_companions_digest_apart`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"]}),
```

### `u43-author-round-2.P6_count_ignored`

ROUND ONE: zero. The count flag is dropped on the way to the engine, so the pool is always the default eight

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P6_count_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=None, role=role)
```

### `u43-author-round-2.V1_pool_total_is_the_union`

totals reports the union size where it says pool, which is the wrong number and the one a reader would otherwise have to derive. The round-one arithmetic surprise is exactly this confusion, so the new count guard owes a death here

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V1_pool_total_is_the_union`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
        "pool": len(plan.pool),
```

New text:

```
        "pool": len(items),
```

### `u43-author-round-2.V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V3_root_check_reports_instead_of_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

### `u98-a.K1_key_off_wheel`

camelot_key: drop the refusal, so a code off the wheel parses to the empty string

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `K1_key_off_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 7 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[0A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[8C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[eight]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_the_parsers_verdict`

Old text:

```
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")

```

New text:

```
(empty)
```

### `u98-a.T1_tempo_nonfinite`

positive_tempo: drop the finiteness half, so NaN and inf parse

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T1_tempo_nonfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[inf]`
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[nan]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if value <= 0:
```

### `u98-a.T2_tempo_zero`

positive_tempo: move the bound to strictly negative, so zero parses

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T2_tempo_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[0]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if not math.isfinite(value) or value < 0:
```

### `u98-a.U1_empty_label`

unowned_anchor: drop the empty label refusal, so an empty label resolves by key alone

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U1_empty_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_unowned_label_refuses_as_an_unknown_anchor`

Old text:

```
    if not label:
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=("pass a label with --unowned, and its Camelot key with --key",),
            origin=("setbuilder", "cli"),
        )

```

New text:

```
(empty)
```

### `u98-a.U2_key_missing`

unowned_anchor: drop the key missing refusal, so an unresolved anchor reaches the engine

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U2_key_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses_through_the_dispatcher`

Old text:

```
    if resolved.key is None:
```

New text:

```
    if False:
```

### `u98-a.U3_reported_owned`

unowned_anchor: return the anchor marked owned and confirmed, the envelope's honesty flags

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U3_reported_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 5 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_in_8a_ranks_the_library_against_it`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved
```

New text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return setbuilder.Anchor(
        key=resolved.key, bpm=resolved.bpm, owned=True, display=resolved.display
    )
```

### `u98-a.U4_tempo_dropped`

unowned_anchor: pass no tempo to the engine, so --bpm is silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U4_tempo_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`

Old text:

```
resolve_anchor(label, (), key=key, bpm=tempo)
```

New text:

```
resolve_anchor(label, (), key=key, bpm=None)
```

### `u98-a.X1_mutex`

build: declare the anchor and --unowned on the parser, not in an exclusive group

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `X1_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`
  - `tests/test_setbuilder_cli.py::test_a_path_and_an_unowned_label_together_are_the_parsers_verdict`

Old text:

```
    anchor = parser.add_mutually_exclusive_group()
```

New text:

```
    anchor = parser
```

### `u98-b.E1_existing_containment`

existing sample: anchor_path drops the library containment refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `E1_existing_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if False:
```

### `u98-b.H1_held_not_excluded`

plan_for: report the exact match copies but leave them in the ranked index

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H1_held_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
(empty)
```

### `u98-b.H2_held_not_reported`

plan_for: exclude the exact match copies but report none

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H2_held_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        totals["held"] = held
```

New text:

```
        totals["held"] = []
```

### `u98-b.H3_held_fuzzy`

plan_for: widen the exact match to containment, the fuzzy shape the empty index exists to avoid

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H3_held_fuzzy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
        index = [t for t in index if not (label and label in t.match)]
```

### `u98-b.S1_supplied_beside_path`

set_build: drop the refusal of --key or --bpm beside a path anchor, so both are silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S1_supplied_beside_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[key]`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if False:
```

### `u98-b.S2_tempo_half`

set_build: drop only the tempo half of that refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S2_tempo_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.key is not None:
```

### `r187-a.A10_ambiguous_falls_through`

resolve_anchor: only a partial reach answers unresolved, so an ambiguous name falls through to not in your library

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A10_ambiguous_falls_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_engine_says_ambiguous_and_never_not_in_your_library`

Old text:

```
    if matched.track is None and matched.candidates and not (matched.partial and key):
```

New text:

```
    if matched.track is None and matched.partial and not key:
```

### `r187-a.A11_no_cutoff`

match_in_index: score cutoff to zero, so a name nothing answers to reaches the whole index

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A11_no_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_web_lookup_is_a_seam_that_is_absent_by_default`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_name_the_library_does_not_hold_refuses_as_not_indexed`

Old text:

```
        score_cutoff=threshold,
```

New text:

```
        score_cutoff=0,
```

### `r187-a.A12_partial_message`

resolve_anchor: a partial reach uses the several owned tracks sentence, which is false when one was reached

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A12_partial_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`

Old text:

```
        if matched.partial:
            why = (
```

New text:

```
        if False:
            why = (
```

### `r187-a.A1_exact_first`

match_in_index: never find an exact hit, so an exact name falls to the fuzzy score that cannot separate it from a longer title

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A1_exact_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    exact = [t for t in index if t.match == wanted]
```

New text:

```
    exact = []
```

### `r187-a.A3_holds_dropped`

match_in_index: count every hit at the threshold as holding the name, so one differing word in a long title resolves

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A3_holds_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_file_with_no_artist_tag_is_reachable_by_the_name_the_refusal_lists`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`
  - `tests/test_setbuilder_cli.py::test_one_differing_word_in_a_long_title_is_a_different_version`

Old text:

```
    holding = tuple(t for t in ordered if _holds_every_word(t.match, wanted))
```

New text:

```
    holding = ordered
```

### `r187-a.A4_word_threshold_low`

WORD_THRESHOLD 80 to 50, so club counts as dub

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A4_word_threshold_low`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_one_differing_word_in_a_long_title_is_a_different_version`

Old text:

```
WORD_THRESHOLD = 80
```

New text:

```
WORD_THRESHOLD = 50
```

### `r187-a.A5_word_threshold_high`

WORD_THRESHOLD 80 to 95, so a slip of the finger no longer lands

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A5_word_threshold_high`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_typed_short_resolves_when_only_one_track_answers_to_it`

Old text:

```
WORD_THRESHOLD = 80
```

New text:

```
WORD_THRESHOLD = 95
```

### `r187-a.A6_first_of_several`

match_in_index: resolve to the first of several holding hits instead of listing them, the defect itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A6_first_of_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_that_reaches_two_versions_lists_both_and_picks_neither`
  - `tests/test_setbuilder_cli.py::test_an_ambiguous_name_refuses_through_the_dispatcher_and_lists_the_paths`
  - `tests/test_setbuilder_cli.py::test_the_engine_says_ambiguous_and_never_not_in_your_library`
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    if len(holding) == 1:
        return AnchorMatch(track=holding[0])
```

New text:

```
    if holding:
        return AnchorMatch(track=holding[0])
```

### `r187-a.A7_partial_never`

match_in_index: never report a partial reach, so a different version reads as a choice between owned tracks

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A7_partial_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`
  - `tests/test_setbuilder_cli.py::test_one_differing_word_in_a_long_title_is_a_different_version`

Old text:

```
    return AnchorMatch(candidates=ordered, partial=bool(ordered))
```

New text:

```
    return AnchorMatch(candidates=ordered, partial=False)
```

### `r187-a.A8_walk_order`

match_in_index: order candidates by score alone, so the listing follows the filesystem walk

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A8_walk_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_that_reaches_two_versions_lists_both_and_picks_neither`

Old text:

```
            hits, key=lambda hit: (-hit[1], index[hit[2]].match, index[hit[2]].path)
```

New text:

```
            hits, key=lambda hit: -hit[1]
```

### `r187-a.A9_key_discarded`

resolve_anchor: a partial reach with a supplied key answers unresolved, discarding the key

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A9_key_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`

Old text:

```
    if matched.track is None and matched.candidates and not (matched.partial and key):
```

New text:

```
    if matched.track is None and matched.candidates:
```

### `r187-b.B10_bad_track_is_current`

_entry_is_current: a cached track that cannot be rebuilt still counts as current, so it is served as a keyless file

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B10_bad_track_is_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-missing-fields]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-not-a-mapping]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[bpm-124]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[title-None]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[vox-value2]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[voxgender-4]`

Old text:

```
        and (entry.get("track") is None or _track_from_cache(entry.get("track")) is not None)

```

New text:

```
(empty)
```

### `r187-b.B12_not_carried_forward`

build_index: a current entry is served and not carried into the next cache, so every other run is a full scan

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B12_not_carried_forward`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`

Old text:

```
            track = _track_from_cache(entry.get("track"))
            fresh[key] = entry
```

New text:

```
            track = _track_from_cache(entry.get("track"))
```

### `r187-b.B1_size_dropped`

_entry_is_current: drop the size, so new bytes restored under an old modification time serve the old track

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B1_size_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_new_bytes_under_an_old_modification_time_are_re_read`

Old text:

```
        and entry.get("size") == identity["size"]

```

New text:

```
(empty)
```

### `r187-b.B3_entry_not_a_mapping`

_entry_is_current: accept any entry that is present, so a list where a mapping belongs raises mid scan

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B3_entry_not_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[list]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[text]`

Old text:

```
        isinstance(entry, dict)
        and entry.get("mtime_ns")
```

New text:

```
        entry is not None
        and entry.get("mtime_ns")
```

### `r187-b.B4_empty_read_cached`

build_index: cache a read that returned no field at all, so one failed read drops the track until the file is touched

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B4_empty_read_cached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer`

Old text:

```
            if identity is not None and any(value is not None for value in raw.values()):
```

New text:

```
            if identity is not None:
```

### `r187-b.B5_empty_walk_writes`

build_index: write the cache after an empty walk, creating a state directory inside a leftover mountpoint

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B5_empty_walk_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_empty_walk_writes_no_cache`

Old text:

```
    if files:
        _save_cache(cache_path, fresh, stamp)
```

New text:

```
    if True:
        _save_cache(cache_path, fresh, stamp)
```

### `r187-b.B6_stamp_unchecked`

_load_cache: trust a cache parsed under another template, so a changed lossy marker serves the old titles

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B6_stamp_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_parsed_under_another_template_is_discarded`

Old text:

```
    if data.get("template") != stamp:
        return {}

```

New text:

```
(empty)
```

### `r187-b.B8_bool_is_a_number`

_is_number: let a bool through as an int, so a cached energy of true is served

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B8_bool_is_a_number`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`

Old text:

```
    return value is None or (isinstance(value, int | float) and not isinstance(value, bool))
```

New text:

```
    return value is None or isinstance(value, int | float)
```

### `u43-author-light.E1_anchor_is_its_own_companion`

build_pool stops excluding the anchor by match key, so the best companion for a track is itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E1_anchor_is_its_own_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        if anchor_match and track.match == anchor_match:
            continue
```

New text:

```
        if anchor_match and track.match != anchor_match:
            pass
```

### `u43-author-light.E2_tempo_band_dropped`

in_band returns True for everything, so a track a hundred BPM away enters the pool on its key alone

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E2_tempo_band_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_anchor_with_no_tempo_drops_the_tempo_constraint`

Old text:

```
    if anchor_bpm is None:
        return True
    if candidate_bpm is None:
        return False
```

New text:

```
    if anchor_bpm is None or candidate_bpm is None:
        return True
```

### `u43-author-light.E3_tempo_serialized_as_bpm`

as_payload spells the tempo key the way the Vorbis tag dialect does, which is one splat from handing a tempo to a tag writer and seeding a grid at half or double time (R17)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E3_tempo_serialized_as_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_no_structured_payload_in_this_unit_carries_a_tempo_TAG_key`
  - `tests/modules/test_tools.py::test_the_structured_payload_carries_a_version`
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
            "tempo": plan.anchor.bpm,
```

New text:

```
            "bpm": plan.anchor.bpm,
```

### `u98-b.P1_either_twice`

build_plan: the after side draws from the whole ranked list again, so either filler is placed on both sides

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u98-b.json`, row `P1_either_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 295 against a baseline of 295
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`

Old text:

```
            [s for s in ranked if id(s) not in taken], "after", DEFAULT_SIDE
```

New text:

```
            ranked, "after", DEFAULT_SIDE
```

### `u105-a.E10_parts_archived`

Stop archiving the parts, reporting each part as its own archive

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E10_parts_archived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
    archives = tuple(archive_source(p, p.parent / ARCHIVE_DIRNAME) for p in paths)
```

New text:

```
    archives = tuple(paths)
```

### `u105-a.E11_join_dir_removed`

Leave the private join directory, and the joined set inside it, behind

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E11_join_dir_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_two_parts_produce_one_master_whose_duration_is_their_sum`

Old text:

```
        shutil.rmtree(join_dir, ignore_errors=True)
```

New text:

```
        pass
```

### `u105-a.E12_join_rf64`

Write a joined WAV without -rf64 auto

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E12_join_rf64`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be`

Old text:

```
    container = ("-rf64", "auto") if destination.suffix.lower() == ".wav" else ()
```

New text:

```
    container = ()
```

### `u105-a.E13_joined_suffix`

Name the joined set after the first part alone, colliding with part one's own master

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E13_joined_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 5 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_the_engine_refuses_an_existing_joined_master_before_archiving`
  - `tests/test_master_cli.py::test_the_parts_are_joined_in_the_order_given_and_never_sorted`
  - `tests/test_master_cli.py::test_two_parts_produce_one_master_whose_duration_is_their_sum`

Old text:

```
JOINED_SUFFIX = "_set"
```

New text:

```
JOINED_SUFFIX = ""
```

### `u105-a.E14_single_part_name`

Name a single recording's master as if it were joined

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E14_single_part_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`

Old text:

```
    paths = [Path(p) for p in parts]
    if len(paths) == 1:
        return output_path(paths[0], output_dir=output_dir)
```

New text:

```
    paths = [Path(p) for p in parts]
```

### `u105-a.E15_payload_parts_conditional`

Emit parts and archives in every report payload, single recordings included

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E15_payload_parts_conditional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_one_input_masters_through_the_unchanged_engine_path`

Old text:

```
    if report.parts:
```

New text:

```
    if True:
```

### `u105-a.E1_lufs_range_removed`

Delete the target_lufs range check in Settings.__post_init__

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E1_lufs_range_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 7 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[-4.0]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[-70.5]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[inf]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[nan]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
        if not low_lufs <= self.target_lufs <= high_lufs:
```

New text:

```
        if False:
```

### `u105-a.E2_lufs_high_bound`

Move the loud bound one LU louder, -5 to -4, a realistic nearby value

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E2_lufs_high_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[-4.0]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`

Old text:

```
LUFS_RANGE = (-70.0, -5.0)
```

New text:

```
LUFS_RANGE = (-70.0, -4.0)
```

### `u105-a.E3_lufs_nan`

Rewrite the range check as two positive comparisons, which admit NaN

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E3_lufs_nan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_is_refused_by_the_engine[nan]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
        if not low_lufs <= self.target_lufs <= high_lufs:
```

New text:

```
        if self.target_lufs < low_lufs or self.target_lufs > high_lufs:
```

### `u105-a.E4_duplicate_part`

Delete the part-named-twice refusal in master_parts

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E4_duplicate_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`

Old text:

```
        if key in seen:
```

New text:

```
        if False:
```

### `u105-a.E5_mixed_containers`

Delete the mixed-container refusal in master_parts

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E5_mixed_containers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_parts_in_different_containers_refuse`

Old text:

```
    if len(containers) > 1:
```

New text:

```
    if False:
```

### `u105-a.E6_joined_output_exists`

Delete master_parts' own output-exists check, leaving master's later one

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E6_joined_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_engine_refuses_an_existing_joined_master_before_archiving`

Old text:

```
    target = planned_output(paths, output_dir=output_dir)
    if target.exists() and not overwrite:
```

New text:

```
    target = planned_output(paths, output_dir=output_dir)
    if False:
```

### `u105-a.E7_layout_rate`

Drop sample rate from the layout the parts must share, the brief's named hazard

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E7_layout_rate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_parts_at_different_sample_rates_refuse_before_anything_is_written`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_fmt, p.channels, p.codec) for p in probes}
```

### `u105-a.E8_layout_channels`

Drop channel count from the layout the parts must share

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E8_layout_channels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_parts_differing_in_any_copied_field_refuse[mono-beside-stereo]`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.codec) for p in probes}
```

### `u105-a.E9_layout_codec`

Drop codec from the layout the parts must share

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E9_layout_codec`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels) for p in probes}
```

### `r598-b.B1_sweep_before_the_lock`

release_lock: abandon the orphans before releasing the lock, so a live holder's refusal arrives after records were already ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B1_sweep_before_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_lock_holder_refuses_and_abandons_nothing`

Old text:

```
    cleared = session.release_stale_lock(cfg)
    abandoned = [
```

New text:

```
    abandoned_first = session.abandon_orphaned_sessions(cfg)
    cleared = session.release_stale_lock(cfg)
    abandoned = [record.session_id for record in abandoned_first] + [
```

### `r598-b.B3_orphans_not_shown`

release_lock: show an empty orphan list at the gate, so the person decides without seeing what will be ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B3_orphans_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`

Old text:

```
                for record in orphans
            ],
```

New text:

```
                for record in orphans[:0]
            ],
```

### `r598-b.B4_abandon_only_reported_as_no_op`

release_lock: report a release that only abandoned records as a no-op, telling a person nothing changed

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B4_abandon_only_reported_as_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`

Old text:

```
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
```

New text:

```
            outcome=Outcome.NO_OP,
```

### `r598-b.B5_kept_reports_nothing`

release_lock: report no kept records, hiding an open record the verb deliberately left

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B5_kept_reports_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_record_whose_holder_is_alive_is_kept_open`
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`

Old text:

```
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
```

New text:

```
    kept = []
```

### `u49-author.A2_the_abort_mints_anyway`

Drop the abort branch in record_ack, so a person who declines gets an acknowledgment

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A2_the_abort_mints_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`
  - `tests/test_session_cli.py::test_answering_abort_records_nothing_and_says_so`

Old text:

```
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )

```

New text:

```
(empty)
```

### `u49-author.A3_the_refusal_names_no_ages`

Drop the context argument from the ack gate, so the refusal asks the question over nothing

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A3_the_refusal_names_no_ages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer`
  - `tests/test_session_cli.py::test_the_refusal_before_acknowledging_names_the_ages_it_consulted`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
```

New text:

```
    option = ctx.gate.require(spec)
```

### `u49-author.A4_the_record_on_file_is_not_shown`

Show the ages but not the acknowledgment already on record, so a person cannot see whether they are covered

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A4_the_record_on_file_is_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
```

New text:

```
        spec, context={"ages": shown}
```

### `u49-author.A6_the_authorisation_is_not_spent`

Leave the recorded decision in place after the mint, so one run id re-mints the acknowledgment forever (R-217's defect restored)

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A6_the_authorisation_is_not_spent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`

Old text:

```
    ctx.run.decisions.pop(spec.name, None)
```

New text:

```
(empty)
```

### `u49-author.A7_the_check_rows_are_keyed_wrong`

Key the ack check rows by name rather than key, so the human check table prints a question mark where the portion should be

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A7_the_check_rows_are_keyed_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`

Old text:

```
                    "key": f"backup.age.{entry['portion']}",
```

New text:

```
                    "name": f"backup.age.{entry['portion']}",
```

### `u49-author.A8_a_damaged_record_locks_the_verb_out`

Let the display read of the acknowledgment raise, so a corrupt record makes the one verb that replaces it refuse

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A8_a_damaged_record_locks_the_verb_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`

Old text:

```
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
```

New text:

```
    recorded = session.read_acknowledgment(cfg)
```

### `u49-author.R1_hard_code_the_repair_token`

Name repair-backup-facts over every unreadable condition, which is R-201's defect reproduced on the new consumer

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R1_hard_code_the_repair_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R2_hard_code_the_permission_token`

The same defect mirrored: name grant-path-access over every condition. Both directions are driven because a carry measured one way leaves the other unasserted

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R2_hard_code_the_permission_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R3_an_unreadable_file_reads_as_empty`

Swallow BackupFactsUnreadable and show no ages, collapsing could-not-read into never-backed-up

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R3_an_unreadable_file_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
```

New text:

```
    except backup_facts.BackupFactsUnreadable:
        return []
    except NotImplementedError as exc:
        raise refuse(
```

### `u45-round-1.E1_rehearsal_publishes`

Let a dry run publish, so a preview records a backup age for a run that copied not one byte

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E1_rehearsal_publishes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if dry_run:
        publish = False
```

New text:

```
    pass
```

### `u45-round-1.E2_publish_unconditional`

Publish regardless of the flag, the same hole reached from the other side

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E2_publish_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        if publish:
            backup_facts.record(
```

New text:

```
        if True:
            backup_facts.record(
```

### `u45-round-1.E4_return_codes_unread`

Stop reading return codes in run_backup, which is exactly the defect its sibling run_restore shipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E4_return_codes_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 21 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it`
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_failing_rehearsal_is_not_reported_as_a_passing_one`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion`
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_written_does_not_replace_the_transfer_failure`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            if result.returncode != 0:
                failed = result
                break
```

New text:

```
            pass
```

### `u45-round-2.E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-2.json`, row `E5_outcome_ok_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

### `u48-author.E1_listing_return_code_inverted`

Existing guard: purge on a failed listing and report a good one as failed

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `E1_listing_return_code_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 18 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_prune_that_completed_warns_about_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_folder_the_last_completed_run_wrote_is_settled_not_held`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_and_removes_the_rest`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
```

New text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode == 0:
```

### `u48-author.P1_listing_classification_dropped`

A failed listing returns no warning, so the rotation stops silently again

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P1_listing_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

New text:

```
    if result.returncode != 0:
        return out, None
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

### `u48-author.P2_purge_classification_dropped`

Failed purges return no warning, so folders survive with nothing saying so

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P2_purge_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

New text:

```
    if False:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

### `u48-author.P4_warning_not_recorded_on_the_portion`

run_backup reads the classification and drops it instead of carrying it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P4_warning_not_recorded_on_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
```

New text:

```
                results += pruned
                continue
```

### `u48-author.P6_purge_count_not_named`

The purge message drops how many folders survived it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P6_purge_count_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
```

New text:

```
                f"the archive rotation did not finish: some dated folder(s) "
```

### `u48-author.P7_listing_message_reworded`

Reword the listing message, not append: the suite asserts with `in`

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P7_listing_message_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 725 against a baseline of 725
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`

Old text:

```
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
```

New text:

```
                f"nothing was removed and the rotation will stay stopped "
                f"until it succeeds. The backup itself completed"
```

### `u44-author-round-2.A1_archive_verify_dropped`

Drop the post-copy digest verification, so a corrupt archive is reported safe

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `A1_archive_verify_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`

Old text:

```
    shutil.copy2(source, destination)
    if digest(destination) != source_digest:
```

New text:

```
    shutil.copy2(source, destination)
    if False:
```

### `u44-author-round-2.A4_digest_reads_first_chunk_only`

Digest only the first chunk, so two sets differing later in the file hash identically

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `A4_digest_reads_first_chunk_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
        while True:
            block = handle.read(chunk)
            if not block:
                break
            hasher.update(block)
```

New text:

```
        hasher.update(handle.read(chunk))
```

### `u44-author-round-2.B3_concat_output_unread`

Drop the same check from the join, one function over

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `B3_concat_output_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning`

Old text:

```
    _wrote_or_refuse(destination, "join")
    return destination
```

New text:

```
    return destination
```

### `u44-author.A2_archive_collision_skips`

Restore the source system's behaviour: an existing archive entry is skipped rather than verified

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `A2_archive_collision_skips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_archive_entry_with_the_same_name_and_different_content_refuses`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
    if destination.exists():
        if digest(destination) == source_digest:
            return destination
```

New text:

```
    if destination.exists():
        return destination
```

### `u44-author.A3_archive_after_the_first_pass`

Move the archive AFTER the probe, so a crash between them leaves no verified copy

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `A3_archive_after_the_first_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_archive_is_taken_before_any_encoding_stage`

Old text:

```
    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )

    probe = probe_source(source, runner=runner, ffprobe=ffprobe)
```

New text:

```
    probe = probe_source(source, runner=runner, ffprobe=ffprobe)

    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )
```

### `u44-author.B1_output_unread`

Drop the post-encode output check, restoring the success report over a file that is not there

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `B1_output_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    _wrote_or_refuse(target, "normalize-and-encode")
    return Report(
```

New text:

```
    return Report(
```

### `u44-author.B2_output_existence_only`

Check existence but not size, so a zero-byte encode still reports a saving of 1.0

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `B2_output_existence_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    if not target.exists() or target.stat().st_size == 0:
```

New text:

```
    if not target.exists():
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

### `u28-skills-independent.S10_stamp_skill_name`

the stamp stops recording which skill it belongs to, so a copied stamp cannot be told from its own

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S10_stamp_skill_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
\nskill = "{name}"
```

New text:

```
(empty)
```

### `u28-skills-independent.S13_expanduser`

--into stops expanding a tilde, so a target given as ~/skills is created as a literal directory named ~

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S13_expanduser`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = Path(ctx.args.into) if ctx.args.into else default_target()
```

### `u28-skills-independent.S17_outcome_always_ok`

the envelope reports OK even when nothing was installed, so an empty package reads as a successful install

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S17_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        outcome=Outcome.OK if checks else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u28-skills-independent.S20_packaged_root_via_file`

packaged_root resolves by path arithmetic from __file__ rather than through importlib.resources

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S20_packaged_root_via_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return Path(__file__).resolve().parent / "assets"
```

### `u181.E1_direct_reference_unread`

extras.install_command: never read the direct reference, so the release install falls back to the folder form and drops analysis

- File: `src/cratekit/modules/extras.py`
- Source: `u181.json`, row `E1_direct_reference_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`, `tests/test_vocals_cli.py`, `tests/test_doctor.py`
- Collected: 464 against a baseline of 464
- Kills: 3 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit @ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit[]@ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_release_install_pipx_recorded_as_a_direct_reference_keeps_it_and_its_extras`

Old text:

```
        reference = _pipx_reference(prefix / PIPX_METADATA)
        if reference is not None:
```

New text:

```
        reference = _pipx_reference(prefix / PIPX_METADATA)
        if False:
```

### `u192.F6_queue_only_never`

queue_only: always False, so --queue-only drives the job anyway

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F6_queue_only_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`, `tests/test_sync_land.py`
- Collected: 409 against a baseline of 409
- Kills: 20 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return False
```

### `u211.B1_backup_database_portion_refuses_alone`

backup _plan_database: let the unconfirmed refusal escape the plan, so the files portion is lost with the database portion

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u211.json`, row `B1_backup_database_portion_refuses_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_backup_cli.py`, `tests/test_analysis_store.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`

Old text:

```
    except AbsenceUnconfirmed as exc:
        return PortionPlan(
```

New text:

```
    except LookupError as exc:
        return PortionPlan(
```

### `u27-restore-cli-round-2.G1_gate_found_by_position`

Take gates[0] rather than the gate digested against the plan

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `G1_gate_found_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1095 against a baseline of 1095
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_confirmation_gate_is_found_by_digest_source_and_not_by_position`

Old text:

```
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
```

New text:

```
    for spec in entry.gates:
        return spec
```

