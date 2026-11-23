# Mutation table: u325-before-l-10

Measured by `scripts/mutate.py` on 2026-11-23 03:58 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 38.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 11, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 94 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u154.R3_repeated_name_planned_twice` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.R6_device_probe_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.R7_exact_prefix_filter_dropped` | `src/cratekit/intake/shelve.py` | maintainer | 1 file(s) | 43 | 1 | killed |
| `u235.H1_shelve_four_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `u235.H2_shelve_sixteen_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `u134-a.A10_shared_playlist` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A11_pass_unknown` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A1_outside_inbox` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A2_mirror_is_first` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A3_gone_listed` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A4_others_excluded` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A5_unreadable` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A6_pre_u128_exact_name` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A7_pass_matched` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A8_only_what_it_lacks` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 3 | killed |
| `u134-b.B1c_composite_short_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 22 | 8 | killed |
| `u134-b.B2c_composite_reversed_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 22 | 8 | killed |
| `u134-b.B4_record_on_success` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-b.B7_again_action` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F1_bridge_name_unasked` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F2_bridge_names_any_account` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F4_bridge_names_any_state` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F5_bridge_names_by_id_order` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-b.B5_no_writes_no_op` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 22 | 3 | killed |
| `u134-b.B6_ack_before_gate` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u220.A10_wrong_status` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 10 | killed |
| `u220.A11_cause_chain_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A12_no_memory_guard` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 2 | killed |
| `u220.A13_exact_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A14_multiset_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A17_settle_once` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 4 | killed |
| `u220.A1_front_target` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 12 | killed |
| `u220.A23_pause_index` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A2_keep_nothing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 20 | killed |
| `u220.A3_keep_head` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 26 | killed |
| `u220.A4_first_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 14 | killed |
| `r372-a.A1_majority_boundary` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A2_majority_coefficient` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A3_pathless_rows_count_as_unmapped` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 17 | killed |
| `r372-a.A4_verb_never_refuses` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-a.A5_apply_proceeds` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A6_decode_error_escapes` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A7_remedy_run_doctor` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-a.A8_refused_plan_reports_ok` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `u178.S1_summary_counts_labels` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 5 | killed |
| `u178.S2_unknown_label_refused` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S3_unreadable_registry_refuses_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S4_genres_frozen` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 13 | killed |
| `u178.S5_worker_takes_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 7 | killed |
| `u178.S6_outranked_needs_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 4 | killed |
| `u178-e9.E9_label_tag_reset` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E2_no_search_with_picture` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 11 | killed |
| `u178.E3_art_refusal_tolerated` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E4_isrc_withheld` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E6_label_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E7_catalogue_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u174.M10_dedupe` | `src/cratekit/sync/mark_cli.py` | maintainer | 3 file(s) | 191 | 1 | killed |
| `u174.M11_stranger_before_no_jobs` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M1_stranger_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M2_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 4 | killed |
| `u174.M3_unfinished_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 3 | killed |
| `u174.M4_unfinished_rows_outstanding` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M5_unfinished_job` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M6_unfinished_reports` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M7_digest_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M8_screen_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M9_verb_passes_the_flag` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 5 | killed |
| `u174.P1_bridge_plans_no_native_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.P2_unreachable_is_refused` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `r1091.K10_available_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K11_year_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K12_periodic_write_off` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K13_write_error_raised` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 6 | killed |
| `r1091.K14_unkept_never_cleared` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K15_reuse_uncounted` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 3 | killed |
| `r1091.K1_age_never_expires` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K2_future_is_fresh` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K3_age_boundary` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K4_age_coefficient` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 4 | killed |
| `r1091.K5_version_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K6_label_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K7_gone_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K8_year_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K9_track_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A3_companions_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A7_companion_suffix_wrong` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A8_sample_stub_check_beside` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 1 | killed |
| `r338-c.C4_bare_metal_asks_about_the_share` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 22663 | 0 (promoted) | zero |
| `r338-c.C5_report_loses_the_word` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 22663 | 0 (promoted) | zero |
| `u101.G10_ungated_not_reported_in_judged_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u101.G11_keep_read_as_drop` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 12 | killed |
| `u101.G12_reported_share_not_the_taxonomys` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G13_family_count_off_by_one` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G14_classified_counts_unjudged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G17_refusal_silent_on_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G18_no_op_claims_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G1_held_is_listed` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 7 | killed |
| `u101.G20_summary_held_empty` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 5 | killed |
| `u101.G2_judged_per_release` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 10 | killed |
| `u101.G3_all_labels_one_group` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u101.G4_unlabelled_grouped_together` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G5_unread_label_judged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G6_unread_from_every_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G7_mixed_is_a_genre` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G8_case_is_a_difference` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G9_mapping_row_unread` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u143-c.A1_kind_named` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-c.A2_ledger_claimed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-c.A3_debris_served` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-c.A4_empty_videos` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-d.A5_playlist_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-d.A6_legacy_name` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u119-b.G12r_removed_namesake_written_into` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |

## Zero rows and what they owe

- `r338-c.C4_bare_metal_asks_about_the_share` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r338-c.C5_report_loses_the_word` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u154.R3_repeated_name_planned_twice`

a batch named twice is planned twice

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R3_repeated_name_planned_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`

Old text:

```
    wanted = _candidates(cfg) if everything else list(dict.fromkeys(names))

```

New text:

```
    wanted = _candidates(cfg) if everything else list(names)

```

### `u154.R6_device_probe_dropped`

a processed tree on another device is planned and renamed into

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R6_device_probe_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_processed_tree_on_another_device_refuses_before_any_plan`

Old text:

```
    _assert_one_device(cfg, root)

```

New text:

```
    pass

```

### `u154.R7_exact_prefix_filter_dropped`

the confinement check judges the case blind LIKE result as is

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R7_exact_prefix_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_a_folder_differing_only_in_case_is_not_this_plans_business`

Old text:

```
            if str(row[1] or "").startswith(one.stored_target + os.sep)

```

New text:

```
            if True

```

### `u235.H1_shelve_four_hex_only`

intake.shelve: the run named batch pattern takes a four hex tail only, the round one finding, so a batch named for a run minted since U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H1_shelve_four_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{4}$")
```

### `u235.H2_shelve_sixteen_hex_only`

intake.shelve: the run named batch pattern takes a sixteen hex tail only, so a batch named for a run from before U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H2_shelve_sixteen_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{16}$")
```

### `u134-a.A10_shared_playlist`

Let two jobs share one playlist unless three do

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A10_shared_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_one_playlist_two_jobs_answer_to_is_neither_jobs`

Old text:

```
counts[one.playlist_id] > 1
```

New text:

```
counts[one.playlist_id] > 2
```

### `u134-a.A11_pass_unknown`

Drop the refusal of a pass with no account playlist job

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A11_pass_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pass_with_no_account_playlist_job_is_refused_naming_the_pass`

Old text:

```
    if not named:
        raise _pass_unknown(cfg, pass_name)

```

New text:

```
(empty)
```

### `u134-a.A1_outside_inbox`

Drop the refusal of a recorded mirror that is live outside INBOX

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A1_outside_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`

Old text:

```
        if str(mirror.ID) not in under:
```

New text:

```
        if False:
```

### `u134-a.A2_mirror_is_first`

Take the newest recorded entry of the pass as the mirror instead of the oldest

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A2_mirror_is_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`

Old text:

```
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
        mirror = _live_playlist(db, recorded[-1])
```

### `u134-a.A3_gone_listed`

Fall through to the name match when the recorded mirror is gone

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A3_gone_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`

Old text:

```
    if recorded:
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
    if recorded and _live_playlist(db, recorded[0]) is not None:
        mirror = _live_playlist(db, recorded[0])
```

### `u134-a.A4_others_excluded`

Let the name match take a playlist a record gives another pass

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A4_others_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_not_asked_of_a_playlist_a_record_gives_another_pass`

Old text:

```
            if key not in others
```

New text:

```
            if True
```

### `u134-a.A5_unreadable`

Trust a name match while a session record could not be read

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A5_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_not_trusted_while_a_session_record_cannot_be_read`

Old text:

```
        if unreadable:
```

New text:

```
        if False:
```

### `u134-a.A6_pre_u128_exact_name`

Match a pre U128 entry by pass alone, so the Name 2 twin counts

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A6_pre_u128_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`

Old text:

```
    return entry.account == account if entry.account else entry.name == name
```

New text:

```
    return entry.account == account if entry.account else True
```

### `u134-a.A7_pass_matched`

Drop the pass comparison, so another pass's record names the mirror

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A7_pass_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`

Old text:

```
    if entry.pass_name != pass_name:
        return False

```

New text:

```
(empty)
```

### `u134-a.A8_only_what_it_lacks`

Plan every distinct member as an add whatever the playlist holds

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A8_only_what_it_lacks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`

Old text:

```
if one not in present)
```

New text:

```
if True)
```

### `u134-b.B1c_composite_short_write`

What B1 holds: the write adds all but the first planned membership

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B1c_composite_short_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[1:])
```

### `u134-b.B2c_composite_reversed_write`

What B2 holds: the write adds the planned memberships in reverse

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B2c_composite_reversed_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[::-1])
```

### `u134-b.B4_record_on_success`

Drop the success path's record of the commit

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B4_record_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
        _record_refill_commit(record, plan, added, cfg)
        convergence.record_fingerprint(cfg, db)
```

New text:

```
        convergence.record_fingerprint(cfg, db)
```

### `u134-b.B7_again_action`

Show a repeated track's second row as held, not again

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B7_again_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`

Old text:

```
            if one.content_id in seen:
```

New text:

```
            if False:
```

### `u175.F1_bridge_name_unasked`

refill.locate: ask only the account's bare name again, so a dated playlist an intake file recorded by name alone is called unfound

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F1_bridge_name_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name} - {"", native.ANALYZE}
```

### `u175.F2_bridge_names_any_account`

refill.bridge_names: take an intake file's entry of any account, so another account playlist's dated name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F2_bridge_names_any_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
                and str(entry.get(ingest.INBOX_ACCOUNT_KEY) or "") == account
```

New text:

```
                and True
```

### `u175.F4_bridge_names_any_state`

refill.bridge_names: read an intake record that no longer stands, so an abandoned landing's name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F4_bridge_names_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW or record.state not in _STANDING:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

New text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

### `u175.F5_bridge_names_by_id_order`

refill.bridge_names: order the records by identifier alone, so a later landing whose identifier sorts first is asked as the first

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F5_bridge_names_by_id_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: (one.started, one.session_id)):
```

New text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: one.session_id):
```

### `u134-b.B5_no_writes_no_op`

Apply a plan that adds nothing instead of ending no_op

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B5_no_writes_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_under_inbox_are_neither_filled`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u134-b.B6_ack_before_gate`

Drop the backup acknowledgment read before the plan and the gate

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B6_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `u220.A10_wrong_status`

_stale_tag: look for a 409 rather than the 412 the provider answers

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A10_wrong_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`

Old text:

```
        if status == PRECONDITION_FAILED:
```

New text:

```
        if status == 409:
```

### `u220.A11_cause_chain_only`

_stale_tag: walk the cause chain alone, so a 412 the client failed to decode is missed (round one R3)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A11_cause_chain_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`

Old text:

```
(one.__cause__, one.__context__)
```

New text:

```
(one.__cause__,)
```

### `u220.A12_no_memory_guard`

order_tracks: ignore what this command's adds left, so a first reading lagging them is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A12_no_memory_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        known = self._members.get(identifier)
```

New text:

```
        known = None
```

### `u220.A13_exact_agrees`

_settled: read any reading as agreeing with the caller's expected one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A13_exact_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
            if exact:
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
            if exact:
                return True
```

### `u220.A14_multiset_agrees`

_settled: read any reading as holding what is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A14_multiset_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return True
```

### `u220.A17_settle_once`

_settled: take one reading only, never again after a pause

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A17_settle_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

New text:

```
        last: CratekitError | None = None
        for attempt in range(1):
```

### `u220.A1_front_target`

order_tracks: move each track to the playlist's length instead of the front, the move whose landing depends on how the provider counts

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A1_front_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
playlist.move_by_indices([at], 0)
```

New text:

```
playlist.move_by_indices([at], len(before))
```

### `u220.A23_pause_index`

_pause: index the pauses by the attempt with no repeat of the last

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A23_pause_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`

Old text:

```
    return ORDER_PAUSES[min(attempt, len(ORDER_PAUSES)) - 1]
```

New text:

```
    return ORDER_PAUSES[attempt - 1]
```

### `u220.A2_keep_nothing`

_to_the_front: keep no standing tail, so every asked track is moved

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A2_keep_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 20 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_nothing_to_move_tells_the_caller_nothing`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_a_track_held_twice_is_not_moved`
  - `tests/test_sync_pair_account.py::test_an_order_already_standing_sends_nothing`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if keep < len(wanted) and one == wanted[len(wanted) - 1 - keep]:
            keep += 1
```

New text:

```
        if keep < len(wanted) and one == wanted[len(wanted) - 1 - keep]:
            keep += 0
```

### `u220.A3_keep_head`

_to_the_front: match the asked order's head rather than its tail, the old to the end rule

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A3_keep_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 26 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_nothing_to_move_tells_the_caller_nothing`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before3-order3]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - ... and 11 more, see the JSON sidecar

Old text:

```
one == wanted[len(wanted) - 1 - keep]
```

New text:

```
one == wanted[keep]
```

### `u220.A4_first_first`

_to_the_front: move the tracks first first rather than last first, so the moved ones land reversed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A4_first_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
    return wanted[: len(wanted) - keep]
```

### `r372-a.A1_majority_boundary`

majority_unmapped: half is a majority, so 5 of 10 refuses

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A1_majority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 2 >= self.active
```

### `r372-a.A2_majority_coefficient`

majority_unmapped: two thirds rather than half, so 6 of 10 is not a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A2_majority_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 3 > self.active
```

### `r372-a.A3_pathless_rows_count_as_unmapped`

_survey: count every row that did not resolve as unmapped, streaming rows included

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A3_pathless_rows_count_as_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 17 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_paths_resolved.py::test_a_minority_of_unmapped_rows_stays_ok_with_the_counts_visible`
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if outcome.resolution is locations.Resolution.UNMAPPED:
```

New text:

```
        if outcome.path is None:
```

### `r372-a.A4_verb_never_refuses`

mytags_vocals: drop the majority refusal, so the plan reports ok over a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A4_verb_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if False:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A5_apply_proceeds`

mytags_vocals: refuse the plan alone and let the apply through

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A5_apply_proceeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if survey.totals.majority_unmapped and not writing:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A6_decode_error_escapes`

_survey: let a location that will not decode raise through the plan and the check

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A6_decode_error_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`

Old text:

```
        except locations.LocationDecodeError:
```

New text:

```
        except ZeroDivisionError:
```

### `r372-a.A7_remedy_run_doctor`

majority_unmapped_cause: send the person to doctor, which sends them back

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A7_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_the_two_synthetic_machines_answer_the_check_opposite_ways`

Old text:

```
        remedy=Remedy.RUN_SETUP,
        steps=(
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
        steps=(
```

### `r372-a.A8_refused_plan_reports_ok`

_refused_plan: outcome ok beside a cause, the envelope the validator rejects

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A8_refused_plan_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        outcome=Outcome.FAILED,
        code=cause.code,
        data=plan,
```

New text:

```
        outcome=Outcome.OK,
        code=cause.code,
        data=plan,
```

### `u178.S1_summary_counts_labels`

_summary: never count a file per label, so label_genres stays empty

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S1_summary_counts_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
            if wrote == tag_engine.LABEL_GENRE:
```

New text:

```
            if False:
```

### `u178.S2_unknown_label_refused`

_label_payload: a --label nobody registered queues the sweep with no label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S2_unknown_label_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_nobody_registered_is_refused_and_nothing_is_queued`

Old text:

```
        if entry is None:
            raise refuse(
                "label-unknown",
```

New text:

```
        if entry is None and False:
            raise refuse(
                "label-unknown",
```

### `u178.S3_unreadable_registry_refuses_label`

_label_payload: an unreadable registry warns rather than refusing a sweep given --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S3_unreadable_registry_refuses_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`

Old text:

```
    except CratekitError as exc:
        if label is not None:
            raise

```

New text:

```
    except CratekitError as exc:

```

### `u178.S4_genres_frozen`

_label_payload: freeze no genres, so a registered label genre never reaches the worker

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S4_genres_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
    if genres:
        frozen["label_genres"] = genres
```

New text:

```
    if False:
        frozen["label_genres"] = genres
```

### `u178.S5_worker_takes_label`

handle: hand the engine no --label, so a folder of untagged files is searched

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S5_worker_takes_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=None,
```

### `u178.S6_outranked_needs_label`

_label_warnings: warn about outranked tags on a sweep given no --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S6_outranked_needs_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_naming_no_genre_says_nothing_on_a_sweep_given_no_label`

Old text:

```
    if payload.get("label") and outranked:
```

New text:

```
    if outranked:
```

### `u178-e9.E9_label_tag_reset`

tag_one: keep the file's tag in label_tag on a file the label answered for

- File: `src/cratekit/tagging/tag.py`
- Source: `u178-e9.json`, row `E9_label_tag_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`

Old text:

```
        label_tag = ""
        _written(
```

New text:

```
        _written(
```

### `u178.E2_no_search_with_picture`

tag_one: drop the early return for a labelled file with a picture, so the catalogues are searched

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E2_no_search_with_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`

Old text:

```
        if settled is not None:
            return TagResult(path=path, **labelled, **repaired, **settled)

```

New text:

```
(empty)
```

### `u178.E3_art_refusal_tolerated`

tag_one: a refusal on a labelled file's art search fails the item

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E3_art_refusal_tolerated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`

Old text:

```
        if needs_genre:
            raise
```

New text:

```
        if not existing:
            raise
```

### `u178.E4_isrc_withheld`

tag_one: offer the general catalogue the ISRC of a labelled file searched for art

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E4_isrc_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`

Old text:

```
        wanted = needs_genre and not hit.genre
```

New text:

```
        wanted = not existing and not hit.genre
```

### `u178.E6_label_write_checked`

tag_one: the label genre write's False is ignored, so a locked file is reported tagged

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E6_label_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`

Old text:

```
        _written(path, by_label.genre, f"its label {by_label.label}")
```

New text:

```
        tags.write_genre(path, by_label.genre)
```

### `u178.E7_catalogue_write_checked`

tag_one: the catalogue genre write's False is ignored, as on main

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E7_catalogue_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_a_catalogues_genre_fails_too`

Old text:

```
        written = _written(path, hit.genre, hit.source or "a catalogue")
```

New text:

```
        tags.write_genre(path, hit.genre)
        written = hit.genre
```

### `u174.M10_dedupe`

plan_pass: keep a playlist named twice twice in the narrowing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M10_dedupe`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
```

New text:

```
    named = tuple(str(one) for one in playlists_named)
```

### `u174.M11_stranger_before_no_jobs`

plan_pass: refuse a stranger only after the no jobs return, so a file of no pass given --playlist asks a gate

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M11_stranger_before_no_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    _refuse_strangers(named, found, name)
    if not found:
```

New text:

```
    if found:
        _refuse_strangers(named, found, name)
    if not found:
```

### `u174.M1_stranger_refusal`

plan_pass: drop the refusal of a named playlist that is not the pass's, so it plans nothing and says nothing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M1_stranger_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    strangers = [identity for identity in named if identity not in held]
    if strangers:
```

New text:

```
    strangers = [identity for identity in named if identity not in held]
    if False:
```

### `u174.M2_narrowing`

plan_pass: drop the narrowing of the decided playlists, so --playlist plans the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M2_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_already_marked_is_a_skip_and_not_a_refusal`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_library_is_walked_only_for_the_named_playlist`

Old text:

```
        decided = [entry for entry in decided if entry.identity in named]
```

New text:

```
        decided = list(decided)
```

### `u174.M3_unfinished_refusal`

plan_pass: drop the refusal of a named playlist the pass did not complete, so it is shown as a skip

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M3_unfinished_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if unfinished:
```

New text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if False:
```

### `u174.M4_unfinished_rows_outstanding`

UNFINISHED: leave out rows-outstanding, so a playlist with a missing track is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M4_unfinished_rows_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE})
```

### `u174.M5_unfinished_job`

UNFINISHED: leave out job-unfinished, so a playlist whose job failed is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M5_unfinished_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

### `u174.M6_unfinished_reports`

UNFINISHED: leave out reports-unreadable, so a playlist whose reports cannot be read is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M6_unfinished_reports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, ROWS_OUTSTANDING})
```

### `u174.M7_digest_names_the_narrowing`

_payload: leave the narrowing out of the digest, so an answer to one playlist's screen carries out the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M7_digest_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
        identity["only"] = sorted(named)
```

New text:

```
        pass
```

### `u174.M8_screen_names_the_narrowing`

_shown: drop the gate screen's line naming the playlists the plan was narrowed to

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M8_screen_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`

Old text:

```
        shown[ONLY_SAID] = list(named)
```

New text:

```
        pass
```

### `u174.M9_verb_passes_the_flag`

sync_mark: hand plan_pass no playlists, so --playlist is parsed and ignored

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M9_verb_passes_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
        playlists_named=list(getattr(ctx.args, "playlist", None) or ()),
```

New text:

```
        playlists_named=(),
```

### `u174.P1_bridge_plans_no_native_pass`

native_passes: read native records on a tree on the bridge too, so every old record is planned as a refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P1_bridge_plans_no_native_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_tree_on_the_bridge_plans_no_native_record`

Old text:

```
    if not medium.native:
        return ()
    return native.landed_passes(cfg)
```

New text:

```
    return native.landed_passes(cfg)
```

### `u174.P2_unreachable_is_refused`

native_passes: read an unreachable root as no pass, so organize asks over a clean plan

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P2_unreachable_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`

Old text:

```
    if medium.declared is None:
        raise _blocked(
```

New text:

```
    if medium.declared is None:
        return ()
        raise _blocked(
```

### `r1091.K10_available_dropped`

_row: keep every track as playable, so a track the provider will not play is asked for from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K10_available_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`

Old text:

```
        "available": getattr(track, "available", True) is not False,
```

New text:

```
        "available": True,
```

### `r1091.K11_year_dropped`

keep: store no year, so a release the provider dates is planned under its listed year from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K11_year_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`

Old text:

```
                year=stated,
```

New text:

```
                year=None,
```

### `r1091.K12_periodic_write_off`

_hold: never write mid run, so a killed build keeps nothing it read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K12_periodic_write_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_reads_are_written_every_flush_and_not_only_at_the_end`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if False:
```

### `r1091.K13_write_error_raised`

flush: let a write the filesystem refuses raise, the round 1 blocking finding

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K13_write_error_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`

Old text:

```
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
```

New text:

```
        except OSError as exc:
            raise
```

### `r1091.K14_unkept_never_cleared`

flush: leave the failure said after a later write succeeds

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K14_unkept_never_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`

Old text:

```
        self._unwritten = 0
        self.unkept = ""
```

New text:

```
        self._unwritten = 0
```

### `r1091.K15_reuse_uncounted`

fresh: count no reuse, so the screen says every read was made by this run

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K15_reuse_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`

Old text:

```
        self.reused += 1
```

New text:

```
        self.reused += 0
```

### `r1091.K1_age_never_expires`

_is_fresh: drop the upper bound, so a read is kept for ever and a changed release is planned from old tracks

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K1_age_never_expires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age
```

### `r1091.K2_future_is_fresh`

_is_fresh: drop the lower bound, so a read dated in the future is kept for as long as the clock is wrong

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K2_future_is_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return age < KEPT_FOR
```

### `r1091.K3_age_boundary`

_is_fresh: a read exactly the age old is still fresh

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K3_age_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age <= KEPT_FOR
```

### `r1091.K4_age_coefficient`

KEPT_FOR: eight days instead of seven, a realistic nearby value

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K4_age_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_the_age_is_seven_days`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
KEPT_FOR = timedelta(days=7)
```

New text:

```
KEPT_FOR = timedelta(days=8)
```

### `r1091.K5_version_unchecked`

load: read a document of another version as if it were this one

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K5_version_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 99, "label_id": "kompakt", "reads": {}}-it says version 99]`

Old text:

```
        if version != VERSION:
```

New text:

```
        if False:
```

### `r1091.K6_label_unchecked`

load: read another label's document as this label's reads

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K6_label_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "another", "reads": {}}-it names the label]`

Old text:

```
        if raw.get("label_id") != label_id:
```

New text:

```
        if False:
```

### `r1091.K7_gone_shape_unchecked`

_entry: accept a gone flag that is not a bool, so a string reads as gone

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K7_gone_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written8-says gone]`

Old text:

```
    if not isinstance(gone, bool):
```

New text:

```
    if False:
```

### `r1091.K8_year_shape_unchecked`

_entry: accept a year of any type, so a string or bool year reaches the plan

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K8_year_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written7-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written9-carries the year]`

Old text:

```
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
    if False:
```

### `r1091.K9_track_shape_unchecked`

_entry: accept a malformed track entry

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K9_track_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written6-is malformed]`

Old text:

```
            not isinstance(track, Mapping)
            or not isinstance(track.get("id"), str)
            or not isinstance(track.get("available"), bool)
```

New text:

```
            not isinstance(track, Mapping)
```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = []
```

### `r592-a.A2_database_dropped_from_fileset`

recovered_database_fileset: return the companions only, so a database already at the landing path is not an occupied target

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return companions
```

### `r592-a.A3_companions_dropped_from_fileset`

recovered_database_fileset: return the database only, so a lone write-ahead log the database half would clear is not an occupied target

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A3_companions_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return (landing,)
```

### `r592-a.A4_fileset_not_rebased`

recovered_database_fileset: land the database at its bare name at the top of the target for every layout, so the guard tests a path the transfer never writes

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
```

New text:

```
        landing = target / database.name
    except ValueError:
```

### `r592-a.A5_replacing_existing_inverted`

assert_recovery_target: refuse an occupied target only when it WAS named for replacement

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 8 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if existing and replacing_existing:
```

### `r592-a.A6_old_suffix_rule_restored`

assert_recovery_target: put the recursive any-database rule back, the behaviour R-592 records, so every interrupted recovery is refused on rerun

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_opens_over_databases_it_would_not_replace`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = sorted(entry for entry in where.rglob("*.db") if entry.is_file())
```

### `r592-a.A7_companion_suffix_wrong`

recovered_database_fileset: name each companion with a dot before its suffix, master.db.-wal, so no real companion is ever found

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A7_companion_suffix_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

New text:

```
        landing.with_name(landing.name + "." + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

### `r592-a.A8_sample_stub_check_beside`

SAMPLE, existing guard: assert_recovery_target refuses only a stub at or under the configured root, not the suffixed name beside it

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A8_sample_stub_check_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if inside_configured and not probe(where):
```

### `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Source: `u27-restore-cli-independent.json`, row `X6_the_rekordbox_guard_itself_is_neutered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
```

New text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if running or not running:
        return
```

### `r338-c.C4_bare_metal_asks_about_the_share`

recover_under_bare_metal_session: let the plan ask the remote about a share the skipped database half will never pull

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C4_bare_metal_asks_about_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                pull_share=False,
```

New text:

```
                pull_share=True,
```

### `r338-c.C5_report_loses_the_word`

restore_under_one_session: stop carrying the plan's share word onto the report, so the totals say null whatever happened to the grids

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C5_report_loses_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "share": str(pulled.share),

```

New text:

```
(empty)
```

### `u101.G10_ungated_not_reported_in_judged_label`

Drop the ungated branch in a judged label, so a release with no genre is listed silently

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G10_ungated_not_reported_in_judged_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_known_is_listed_with_a_failing_line`
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
            if outcome.ungated is not None:
```

New text:

```
            if False:
```

### `u101.G11_keep_read_as_drop`

Hold on the KEEP verdict instead of DROP

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G11_keep_read_as_drop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_family_exactly_at_the_share_belongs_and_is_listed`
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_genre_the_label_makes_enough_of_is_listed`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
```

New text:

```
            elif verdict is routing.GateVerdict.KEEP and family and outcome.genre:
```

### `u101.G12_reported_share_not_the_taxonomys`

Report a share the taxonomy did not declare

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G12_reported_share_not_the_taxonomys`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`

Old text:

```
    share = declared.label_gate.out_of_place_share
```

New text:

```
    share = 0.2
```

### `u101.G13_family_count_off_by_one`

Report one more release of the family than there were

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G13_family_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
families.count(family), classified, share
```

New text:

```
families.count(family) + 1, classified, share
```

### `u101.G14_classified_counts_unjudged`

Count every release in the label as classified, including those with no genre

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G14_classified_counts_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
        classified = sum(1 for genre in genres if genre)
```

New text:

```
        classified = len(genres)
```

### `u101.G17_refusal_silent_on_held`

Drop the held clause from the nothing missing refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G17_refusal_silent_on_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
```

New text:

```
            + ""
```

### `u101.G18_no_op_claims_held`

The no op wording ignores held releases and says the library holds everything read

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G18_no_op_claims_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`

Old text:

```
            f"held by it"
            if held
            else
```

New text:

```
            f"held by it"
            if False
            else
```

### `u101.G1_held_is_listed`

Drop the skip, so a release the gate held is resolved, offered and listed anyway

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G1_held_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if release.item_id in held:
            continue

```

New text:

```
(empty)
```

### `u101.G20_summary_held_empty`

The summary carries no held releases

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G20_summary_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`

Old text:

```
        held=[one.to_json() for one in held.values()],
```

New text:

```
        held=[],
```

### `u101.G2_judged_per_release`

Group every release under itself, so each is judged alone and nothing is ever held

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G2_judged_per_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return f"release:{release.release_id}"
```

### `u101.G3_all_labels_one_group`

Group every release under one key, so labels are judged against each other

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G3_all_labels_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return "all"
```

### `u101.G4_unlabelled_grouped_together`

Group every release naming no label under one key instead of judging each alone

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G4_unlabelled_grouped_together`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return release.label_id or release.label_name or "release:"
```

### `u101.G5_unread_label_judged`

Judge a label even when one of its releases was unread this run

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G5_unread_label_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`

Old text:

```
        if label in unread:
```

New text:

```
        if label in unread and False:
```

### `u101.G6_unread_from_every_label`

Treat every label as having an unread release whenever any release failed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G6_unread_from_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if label in unread:
```

New text:

```
        if unread:
```

### `u101.G7_mixed_is_a_genre`

Rows that disagree yield their first genre instead of none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G7_mixed_is_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
    if len(said) > 1:
```

New text:

```
    if len(said) > 99:
```

### `u101.G8_case_is_a_difference`

Compare genres by exact text, so one genre in two cases reads as mixed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G8_case_is_a_difference`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_genre_in_two_cases_is_one_genre_and_is_judged`

Old text:

```
            said.setdefault(text.casefold(), text)
```

New text:

```
            said.setdefault(text, text)
```

### `u101.G9_mapping_row_unread`

Read the genre by attribute only, so a mapping shaped row reports none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G9_mapping_row_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`

Old text:

```
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
```

New text:

```
        value = getattr(row, "genre", None)
```

### `u143-c.A1_kind_named`

Adapter: drop the refusal of a kind other than debris or empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A1_kind_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if kind not in kinds.ROOT_REMOVALS:
```

New text:

```
        if False:
```

### `u143-c.A2_ledger_claimed`

Adapter: remove a root playlist a ledger record names

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A2_ledger_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if self._cfg is None or self._claimed(identifier):
```

New text:

```
        if self._cfg is None:
```

### `u143-c.A3_debris_served`

Adapter: accept any served name as debris

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A3_debris_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served0-debris]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served1-debris]`

Old text:

```
            served = is_library_debris(name)
```

New text:

```
            served = True
```

### `u143-c.A4_empty_videos`

Adapter: an empty playlist need not declare zero videos

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A4_empty_videos`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served3-empty]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served4-empty]`

Old text:

```
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
```

New text:

```
            served = _count(tracks) and tracks == 0
```

### `u143-d.A5_playlist_read_back`

Adapter: report a root playlist removed though the provider still serves it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A5_playlist_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_root_playlist_still_served_after_its_delete_is_refused_not_reported_removed`

Old text:

```
        if served_after is not _ABSENT and served_after is not None:
```

New text:

```
        if False:
```

### `u143-d.A6_legacy_name`

Adapter: remove a root folder whatever its name

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A6_legacy_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026-0-not-a-legacy-folder]`
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[Phil's Spotify-0-not-a-legacy-folder]`

Old text:

```
        if not kinds.legacy_year(name):
```

New text:

```
        if False:
```

### `u119-b.G12r_removed_namesake_written_into`

_playlist_row: a removed Favorites of the name under the folder is written into

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G12r_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removed_favorites_under_the_folder_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
```

New text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row):
            continue
```

