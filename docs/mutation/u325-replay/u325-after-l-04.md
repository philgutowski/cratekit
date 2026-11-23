# Mutation table: u325-after-l-04

Measured by `scripts/mutate.py` on 2026-11-22 22:22 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 108.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 5, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u95-c.C8_plan_root_assertion_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.S1_authorises_everything` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-c.S2_issued_terms_not_compared` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `r351.A2_unresolved_seed_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.A3_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r351.A5_ambiguity_takes_first` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.G10_identifier_message_says_named` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G3_unresolved_id_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r351.G4_any_remainder_is_an_id` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G5_except_everything` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r351.G7_drop_object_not_found` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G8_id_prefix_case_insensitive` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G9_all_lookuperror_is_absence` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.A2_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r352.G10_no_collaborator_enqueue` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G11_discovered_not_added` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 10 | killed |
| `r352.G13_duplicate_roster_member` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G2_skip_when_roster_nonempty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 7 | killed |
| `r352.G4_empty_message_omits_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G5_compilation_range_shrunk` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G6_name_query_only` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G7_ignore_match_needle` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r504-a.A1_lt_to_le` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r504-a.A2_lt_to_gt` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `r504-a.A3_no_none_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r504-a.A4_no_raise` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r515-operator.S7_adapter_no_count` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r840-c.C3_the_adapter_reads_a_name` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r879-b.T2_offset_not_sent` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A1_missing_playlist_returns_none` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A4_first_hit_not_exact` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A6_no_reread_for_missing_copyright` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A7_any_search_hit_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u70.A1_no_favourites_refused` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u75-c.C1_gone_is_never_retried` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `u75-c.C5_none_album_raises` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u75-c.C7_tracks_through_the_paging_wrapper` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `u78-c.D2_blank_isrc` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 3 | killed |
| `u78-c.D3_no_lookup_method` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u79-c.D1_search_shape_read_as_empty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S1_of_takes_bool` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S2_of_takes_non_int` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S4_of_short_at_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S5_of_short_over_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r1114.M10_message_reworded_many` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M11_message_reworded_one` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M12_match_step_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M13_detail_labels_empty` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M14_withheld_reads_no_op` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M15_skipped_line_not_fail` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 5 | killed |
| `r1114.M16_remedy_line_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `r1114.M17_remedy_line_only_doctor` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M1_every_skipped_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `r1114.M2_single_label_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M3_mixed_run_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M4_closing_line_ignores_skips` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M5_closing_line_names_every_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M6_nothing_new_not_counted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 13 | killed |
| `r1114.M7_refusal_drops_the_lines` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `r1114.M8_refusal_not_retryable` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u108-a.G01_unsettled_skips_settled` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 4 | killed |
| `u108-c.G19_settle_keeps` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u108-c.G24_walk_ends_at_gate` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 8 | killed |
| `u108-d.G18_settle_matches_identity_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u108-d.G20_settle_skips_settled_again` | `src/cratekit/label/sync_cli.py` | maintainer | 2 file(s) | 204 | 1 | killed |
| `u189.M11_answer_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M12_pick_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M13_walk_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M14_pick_no_release_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M15_pick_remedy_unquoted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M16_empty_label_alone_walks` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M1_next_label_refused_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 12 | killed |
| `u189.M2_label_alone_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 5 | killed |
| `u189.M3_next_release_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M4_empty_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M5_alone_hint_drops_the_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M6_label_not_passed` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 11 | killed |
| `u189.M7_unknown_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M8_entries_ignore_the_one` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 9 | killed |
| `u189.S1_saved_question_relisted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 4 | killed |
| `u189.S2_question_not_saved` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 119 | killed |
| `u16-round-8-independent-composites.V24_approximate_limit_raised` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 10 | killed |
| `u16-round-8-independent.V11_candidate_order_sorted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V12_approximate_floor_halved` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 13 | killed |
| `u16-round-8-independent.V13_withheld_not_reported` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 4 | killed |
| `u16-round-8-independent.V14_tombstone_fold_nfd` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 4 | killed |
| `u16-round-8-independent.V15_empty_identity_accepted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 1 | killed |
| `u16-round-8-independent.V16_key_leaves_item_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V18_rejection_skips_tombstones` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V1_key_check_first_copy_only` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V20_digest_width_halved` | `src/cratekit/acquire/match.py` | maintainer | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V21_suppression_asked_one_spelling` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 9 | killed |
| `u16-round-8-independent.V3_version_differs_silently_joins` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 41 | killed |
| `u16-round-8-independent.V5_ambiguous_reading_promoted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V6_reading_question_never_asked` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V7_tombstoned_counted_missing` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V8_missing_without_options` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 9 | killed |
| `u16-round-8-independent.V9_relative_key_by_letter` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 11 | killed |
| `u269.M7_match_engine_binds_lxml` | `src/cratekit/acquire/match.py` | maintainer | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V22_suppressed_warning_omitted` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 609 | 26 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 4 | killed |

## Row definitions

### `u95-c.C8_plan_root_assertion_removed`

plan drops its assertion on the rooted root, which is also where it asks whether the session is still open and is a recovery

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C8_plan_root_assertion_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`

Old text:

```
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

New text:

```
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

### `u95-c.S1_authorises_everything`

EXISTING GUARD, fixed sample: Held.authorises_path answers yes to every path, which is the original bypass

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S1_authorises_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
        return where == root or root in where.parents
```

New text:

```
        return True
```

### `u95-c.S2_issued_terms_not_compared`

EXISTING GUARD, fixed sample: still_open stops comparing the claim to what the guard issued, so a live token can be rebuilt around another directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S2_issued_terms_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round2_a_held_rebuilt_around_a_live_token_is_refused`

Old text:

```
        if terms != (self.issued_by, str(self.authorises), str(self.lock.absolute())):
            return False
```

New text:

```
(empty)
```

### `r351.A2_unresolved_seed_skipped`

crawl the seeds that resolved and skip the one that did not

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A2_unresolved_seed_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
        if unresolved:
            bits = []

```

New text:

```
        if unresolved and not artists:
            bits = []

```

### `r351.A3_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A3_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(
```

New text:

```
        if not artists:
            return LabelRoster([])
            raise LabelUnresolvable(
```

### `r351.A5_ambiguity_takes_first`

take the first of two artists named exactly the same

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A5_ambiguity_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_colliding_name_seed_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_two_artists_named_exactly_the_label_refuse_rather_than_guess`

Old text:

```
        if len(distinct) > 1:
```

New text:

```
        if len(distinct) > 2:
```

### `r351.G10_identifier_message_says_named`

an unresolved identifier is reported as a name the provider does not carry

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G10_identifier_message_says_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
                if seed_identifier(seed) is not None:
                    bits.append(f"no artist with identifier {seed!r}")
                else:
                    bits.append(f"no artist named exactly {seed!r}")

```

New text:

```
                bits.append(f"no artist named exactly {seed!r}")

```

### `r351.G3_unresolved_id_skipped`

a seed that does not resolve is skipped rather than refusing the label

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G3_unresolved_id_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_id_lookup_that_returns_none_is_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_name_seed_refuses_even_when_discovery_would_find_albums`
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
            if artist is None:
                unresolved.append(seed)

```

New text:

```
            if artist is None:
                continue

```

### `r351.G4_any_remainder_is_an_id`

treat anything after id: as an identifier, including a name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G4_any_remainder_is_an_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_is_not_digits_after_the_prefix_is_still_a_name`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(.+)$")

```

### `r351.G5_except_everything`

a provider outage looking up an identifier is read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G5_except_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_outage_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_session_dead_during_discovery_refuses_the_label`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:
            # Bare LookupError is the fake's not found. KeyError and IndexError
            # are subclasses, and those are parse failures, not a missing id.
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
        except Exception:
            return None

```

### `r351.G7_drop_object_not_found`

the live client's ObjectNotFound is no longer treated as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G7_drop_object_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:

```

New text:

```
        except LookupError as exc:

```

### `r351.G8_id_prefix_case_insensitive`

ID:99 is treated as an identifier, against the locked id:<digits> shape

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G8_id_prefix_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_uppercase_id_prefix_is_still_a_name_seed`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(\d+)$", re.IGNORECASE)

```

### `r351.G9_all_lookuperror_is_absence`

KeyError and IndexError from the identifier lookup are read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G9_all_lookuperror_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`

Old text:

```
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
            return None

```

### `r352.A2_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `A2_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(

```

New text:

```
        if False and not artists:
            raise LabelUnresolvable(

```

### `r352.G10_no_collaborator_enqueue`

BFS does not enqueue credited artists from listed matching releases

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G10_no_collaborator_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`

Old text:

```
            for release in releases:
                if _credits_label(release, needle):
                    for identity in _credited_ids(release):
                        enqueue(identity)

```

New text:

```
            for release in releases:
                if _credits_label(release, needle):
                    pass

```

### `r352.G11_discovered_not_added`

credited artists are walked but never appended to the roster

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G11_discovered_not_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_credit_starting_with_p_or_c_is_resolved_whole`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            if identity not in held_ids:
                held_ids.add(identity)

```

### `r352.G13_duplicate_roster_member`

a discovered artist already on the roster is appended again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G13_duplicate_roster_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_discovered_artist_already_on_the_roster_is_not_added_twice`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            discovered.append(artist)
            held_ids.add(identity)

```

### `r352.G2_skip_when_roster_nonempty`

discovery does not run when the label already has an artist page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G2_skip_when_roster_nonempty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_an_authentication_error_on_album_search_still_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
        needle = entry.match or entry.name
        seen: set[str] = set()

```

New text:

```
        if held:
            return []
        needle = entry.match or entry.name
        seen: set[str] = set()

```

### `r352.G4_empty_message_omits_discovery`

an empty roster still says only that the label names no seed artists

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G4_empty_message_omits_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`

Old text:

```
                f"the provider has no artist named exactly {entry.name!r}, the "
                f"label names no seed artists, and discovery found nothing"

```

New text:

```
                f"the provider has no artist named exactly {entry.name!r} and the "
                f"label names no seed artists to crawl instead"

```

### `r352.G5_compilation_range_shrunk`

numbered compilation searches stop at 001

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G5_compilation_range_shrunk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
COMPILATION_RANGE = range(1, 80)

```

New text:

```
COMPILATION_RANGE = range(1, 2)

```

### `r352.G6_name_query_only`

discovery searches the bare label name and no numbered compilations

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G6_name_query_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
    return (name, *(f"{name} {number:03d}" for number in COMPILATION_RANGE))

```

New text:

```
    return (name,)

```

### `r352.G7_ignore_match_needle`

copyright match uses the display name and ignores entry.match

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G7_ignore_match_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`

Old text:

```
        needle = entry.match or entry.name

```

New text:

```
        needle = entry.name

```

### `r504-a.A1_lt_to_le`

Adapter compares with <= instead of <, so a listing that reached its count raises a shortfall of zero

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A1_lt_to_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_complete_hearts_listing_reports_no_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_hearts_listing_pages_to_the_declared_total_through_the_listing`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) <= declared:
```

### `r504-a.A2_lt_to_gt`

Adapter compares the wrong way round, so a short listing returns and a long one raises

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A2_lt_to_gt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_longer_than_its_count_is_not_a_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) > declared:
```

### `r504-a.A3_no_none_guard`

Adapter drops the guard for a count the provider did not publish

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A3_no_none_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[-1]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[0]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[None]`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if len(rows) < declared:
```

### `r504-a.A4_no_raise`

Adapter never raises the shortfall, which is the pre R-504 behaviour

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A4_no_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
            raise HeartsShortfall(rows, declared)
```

New text:

```
            pass
```

### `r515-operator.S7_adapter_no_count`

The release adapter ignores the album's num_tracks

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r515-operator.json`, row `S7_adapter_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`

Old text:

```
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
```

New text:

```
        short = None
```

### `r840-c.C3_the_adapter_reads_a_name`

TidalCatalogue.release_artist: answer with the text of the album's artist object, which is its address, the defect R-379 named

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r840-c.json`, row `C3_the_adapter_reads_a_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limited_artist_read_waits_and_is_asked_again`
  - `tests/test_label_tidal_catalogue.py::test_a_releases_artist_is_its_name_and_never_the_objects_address`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`
  - `tests/test_label_tidal_catalogue.py::test_the_sweep_files_the_name_the_artist_read_returns`

Old text:

```
        return artist_name(self._album(release_id))
```

New text:

```
        return str(getattr(self._album(release_id), "artist", "") or "")
```

### `r879-b.T2_offset_not_sent`

TidalCatalogue.search_tracks: send offset 0 to the client whatever page was asked

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r879-b.json`, row `T2_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_track_search_asks_for_the_page_its_offset_names`

Old text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=offset
```

New text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=0
```

### `u62.A1_missing_playlist_returns_none`

Return None for a playlist the client returned nothing for

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A1_missing_playlist_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_playlist_the_client_returns_nothing_for_raises_too`

Old text:

```
        if playlist is None:
            raise PlaylistUnresolvable(
```

New text:

```
        if playlist is None:
            return None
            raise PlaylistUnresolvable(
```

### `u62.A4_first_hit_not_exact`

Take any hit the search returned rather than an exact name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A4_first_hit_not_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`

Old text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or "")) == wanted
```

New text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or ""))
```

### `u62.A6_no_reread_for_missing_copyright`

Judge a release with no copyright line unconfirmed instead of re-reading it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A6_no_reread_for_missing_copyright`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_confirms_from_its_own_copyright_line_or_a_re_read`

Old text:

```
        if not resolved and identity:
```

New text:

```
        if not resolved and not identity:
```

### `u62.A7_any_search_hit_confirms`

Confirm a harvested label on any album with a copyright line

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A7_any_search_hit_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_harvested_name_is_confirmed_only_by_a_matching_copyright_line`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
            if resolved and label_verify.labels_match(name, resolved):
```

New text:

```
            if resolved:
```

### `u70.A1_no_favourites_refused`

A client exposing no favourites is not refused by name, so the read fails as an attribute error

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u70.json`, row `A1_no_favourites_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_that_exposes_no_favourites_refuses_rather_than_holding_no_hearts`

Old text:

```
        if getattr(user, "favorites", None) is None:
```

New text:

```
        if False:
```

### `u75-c.C1_gone_is_never_retried`

Stop classifying a not found answer first, so a withdrawn release climbs the whole retry ladder

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C1_gone_is_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_404_status_is_gone_whatever_the_class_is_called`
  - `tests/test_label_tidal_catalogue.py::test_a_gone_release_has_no_artist_to_read_and_is_asked_about_once`
  - `tests/test_label_tidal_catalogue.py::test_a_release_that_is_gone_raises_at_once_and_is_never_retried`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_and_the_verb_meet_over_a_gone_release`

Old text:

```
                if _gone(exc):
                    return _GONE
                raise
```

New text:

```
                raise
```

### `u75-c.C5_none_album_raises`

Let a client that returned nothing for a release through to the listing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C5_none_album_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_the_client_returns_nothing_for_raises_too`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_read_the_client_returns_nothing_for_raises_too`

Old text:

```
        if album is _GONE or album is None:
```

New text:

```
        if album is _GONE:
```

### `u75-c.C7_tracks_through_the_paging_wrapper`

List the tracks with one direct call instead of the paging wrapper, which serves one page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C7_tracks_through_the_paging_wrapper`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_is_paged_to_its_declared_count_and_carries_its_year`
  - `tests/test_label_tidal_catalogue.py::test_a_short_window_in_the_middle_of_a_release_does_not_end_it`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_pages_nothing_by_hand`

Old text:

```
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
```

New text:

```
        tracks = album.tracks()
```

### `u78-c.D2_blank_isrc`

A blank ISRC is sent to the provider

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D2_blank_isrc`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[   ]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[None]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[]`

Old text:

```
        if not wanted:
            raise ValueError("no ISRC was given to look up")
```

New text:

```
(empty)
```

### `u78-c.D3_no_lookup_method`

A client with no ISRC lookup climbs the whole ladder before failing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D3_no_lookup_method`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_with_no_isrc_lookup_refuses_at_once_and_never_climbs_the_ladder`

Old text:

```
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")
```

New text:

```
(empty)
```

### `u79-c.D1_search_shape_read_as_empty`

A search answer with no track listing is read as no candidate

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u79-c.json`, row `D1_search_shape_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_search_answer_with_no_track_listing_is_raised_at_once_and_is_not_empty`

Old text:

```
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
```

New text:

```
        if False:
            raise LookupError("the provider's search answer carries no track listing")
```

### `r515-operator.S1_of_takes_bool`

Let ListingShortfall.of trust a bool as a declared count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S1_of_takes_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[True]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if not isinstance(declared, int) or declared <= 0:
```

### `r515-operator.S2_of_takes_non_int`

Let ListingShortfall.of trust a count that is not an integer

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S2_of_takes_non_int`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[10]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if isinstance(declared, bool) or declared is None or declared <= 0:
```

### `r515-operator.S4_of_short_at_count`

Mint a shortfall when the listing reaches the count exactly

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S4_of_short_at_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_full_release_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed > declared:
```

### `r515-operator.S5_of_short_over_count`

Mint a shortfall when the listing runs past the count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S5_of_short_over_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_that_serves_more_than_its_declared_count_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed == declared:
```

### `r1114.M10_message_reworded_many`

_unlisted_cause: reword the many label message so it no longer says none could be read

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M10_message_reworded_many`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        else f"none of the {len(entries)} labels asked about could be read ({names}), "
```

New text:

```
        else f"the {len(entries)} labels asked about were skipped ({names}), "
```

### `r1114.M11_message_reworded_one`

_unlisted_cause: reword the single label message so it no longer says the label could not be read

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M11_message_reworded_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`

Old text:

```
        f"the label asked about could not be read ({names}), so whether it has"
```

New text:

```
        f"the label asked about was skipped ({names}), so whether it has"
```

### `r1114.M12_match_step_dropped`

_UNLISTED_STEPS: drop the step naming the registry's --match needle, the remedy for a listing that confirmed nothing, from the cause and the line

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M12_match_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
    "a listing that confirmed nothing: check the label's --match needle "
    "with: crate label registry",

```

New text:

```
(empty)
```

### `r1114.M13_detail_labels_empty`

_unlisted_cause: carry no label identifiers in the detail, so a script cannot tell which labels failed

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M13_detail_labels_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        detail={"labels": [entry.label_id for entry in entries]},
```

New text:

```
        detail={"labels": []},
```

### `r1114.M14_withheld_reads_no_op`

_next, existing guard sampled: a run whose gate withheld an item ends no_op though it wrote

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M14_withheld_reads_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`

Old text:

```
        # back has left review even when no question was left to ask.
        outcome=Outcome.OK if withheld else Outcome.NO_OP,
    )


#: What to do about a label
```

New text:

```
        # back has left review even when no question was left to ask.
        outcome=Outcome.NO_OP,
    )


#: What to do about a label
```

### `r1114.M15_skipped_line_not_fail`

_skipped_check, existing guard sampled: a skipped label's line is a note rather than a fail

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M15_skipped_line_not_fail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`
  - `tests/test_label_sync.py::test_next_with_one_label_skipped_and_the_next_asked_still_asks`

Old text:

```
    return _check(f"label.{entry.label_id}", "fail", f"{entry.name}: not asked; {why}")
```

New text:

```
    return _check(f"label.{entry.label_id}", "info", f"{entry.name}: not asked; {why}")
```

### `r1114.M16_remedy_line_dropped`

_next: refuse without the info line naming what to do, so the human rendering shows no remedy, the review's round one finding

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M16_remedy_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        checks.append(_check("next", "info", _UNLISTED_REMEDY))
```

New text:

```
        pass
```

### `r1114.M17_remedy_line_only_doctor`

_UNLISTED_REMEDY: the line carries only the first step, so a listing that confirmed nothing is told to run doctor

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M17_remedy_line_only_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
_UNLISTED_REMEDY = "; ".join(_UNLISTED_STEPS)
```

New text:

```
_UNLISTED_REMEDY = _UNLISTED_STEPS[0]
```

### `r1114.M1_every_skipped_not_refused`

_next: drop the refusal of a run whose every label was skipped, so it ends no_op with exit 0 again, the defect R-1114 names

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M1_every_skipped_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
    if not nothing:
```

New text:

```
    if False:
```

### `r1114.M2_single_label_not_refused`

_next: refuse only the walk over every label, so --next --label on a label whose listing failed ends no_op with exit 0

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M2_single_label_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`

Old text:

```
    if not nothing:
```

New text:

```
    if not nothing and only is None:
```

### `r1114.M3_mixed_run_refused`

_next: refuse whenever any label was skipped, so a run with one label listed and nothing new also fails

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M3_mixed_run_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
    if not nothing:
```

New text:

```
    if len(nothing) < len(entries):
```

### `r1114.M4_closing_line_ignores_skips`

_next: say no label has anything new whatever was skipped, the false closing line on a mixed run

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M4_closing_line_ignores_skips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
            if len(nothing) == len(entries)
```

New text:

```
            if True
```

### `r1114.M5_closing_line_names_every_label`

_next: name every label in the mixed closing line, the skipped ones included, as having nothing new

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M5_closing_line_names_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
{', '.join(nothing)}"
```

New text:

```
{', '.join(one.name for one in entries)}"
```

### `r1114.M6_nothing_new_not_counted`

_next: stop counting a label listed with nothing new, so every run with no question refuses as unlisted

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M6_nothing_new_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer`
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_both_listed_with_nothing_new_is_unchanged`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`

Old text:

```
                    nothing.append(entry.name)

```

New text:

```
(empty)
```

### `r1114.M7_refusal_drops_the_lines`

_next: refuse without the run's checks as data, so the per label fail lines vanish from the refusal

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M7_refusal_drops_the_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
            cause=_unlisted_cause(entries),
            data=data,
```

New text:

```
            cause=_unlisted_cause(entries),
            data=None,
```

### `r1114.M8_refusal_not_retryable`

_unlisted_cause: mark the refusal not retryable, though a provider answering later clears it

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M8_refusal_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        retryable=True,
        origin=("label.sync",),
        detail={"labels": [entry.label_id for entry in entries]},
```

New text:

```
        retryable=False,
        origin=("label.sync",),
        detail={"labels": [entry.label_id for entry in entries]},
```

### `u108-a.G01_unsettled_skips_settled`

sync_cli.unsettled: read every saved answer as unsettled, so a go summarises answers an earlier go already took

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-a.json`, row `G01_unsettled_skips_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_settled_answer_is_not_summarised_again`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if isinstance(entry, Mapping) and not entry.get(SETTLED)
    ]
```

New text:

```
        if isinstance(entry, Mapping)
    ]
```

### `u108-c.G19_settle_keeps`

sync_cli.settle_in: an answer holding a release named in keep is settled anyway

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-c.json`, row `G19_settle_keeps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
        if isinstance(taken, list) and any(one in keep for one in taken):
            continue
```

New text:

```
        if False:
            continue
```

### `u108-c.G24_walk_ends_at_gate`

sync_cli._walk: a walk that answered every label ends without asking the gate

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-c.json`, row `G24_walk_ends_at_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_whose_catalogue_cannot_be_listed_fails_its_line_and_the_walk_goes_on`
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`
  - `tests/test_label_sync_go.py::test_the_walk_ends_at_the_gate_and_a_yes_downloads_what_it_answered`
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    if stopped_at is None:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED
```

New text:

```
    if False:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED
```

### `u108-d.G18_settle_matches_identity_again`

sync_cli.settle_in: an answer is settled by its place alone, without checking it is the answer the summary covered

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-d.json`, row `G18_settle_matches_identity_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_settling_leaves_an_answer_whose_place_now_holds_a_different_one`

Old text:

```
        if (
            _text(entry.get("label_id")) != label_id
            or _text(entry.get("answered_at")) != answered_at
        ):
            continue
```

New text:

```
        if False:
            continue
```

### `u108-d.G20_settle_skips_settled_again`

sync_cli.settle_in: an answer already settled is settled again, its first marker overwritten

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-d.json`, row `G20_settle_skips_settled_again`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_settling_an_answer_already_settled_keeps_its_first_marker`

Old text:

```
        if not isinstance(entry, Mapping) or entry.get(SETTLED):
            continue
        if (
```

New text:

```
        if not isinstance(entry, Mapping):
            continue
        if (
```

### `u189.M11_answer_remedy_plain_next`

record_answer: the remedy of an answer with nothing waiting names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M11_answer_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`

Old text:

```
                    else f"ask it first with: crate label sync --next --label {entry.label_id}"
```

New text:

```
                    else "ask it first with: crate label sync --next"
```

### `u189.M12_pick_remedy_plain_next`

record_answer: the remedy of a pick outside the question names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M12_pick_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`

Old text:

```
                    f"take the identifiers from: crate label sync --next --label "
                    f"{entry.label_id}",
```

New text:

```
                    "take the identifiers from: crate label sync --next",
```

### `u189.M13_walk_remedy_plain_next`

_walk: the unanswerable refusal's remedy names the plain --next and a placeholder label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M13_walk_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_nobody_can_answer_names_next_label_for_the_label_it_stopped_at`

Old text:

```
                        f"sync --next --label {entry.label_id}, then crate label sync "
                        f"--answer ANSWER --label {entry.label_id}",
```

New text:

```
                        f"sync --next, then crate label sync "
                        f"--answer ANSWER --label NAME",
```

### `u189.M14_pick_no_release_remedy_plain_next`

label_sync: the remedy of --answer pick with no --release names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M14_pick_no_release_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Beta Works-'Beta Works']`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Kit's Works-"Kit's Works"]`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[beta-works-'beta-works']`

Old text:

```
                f"--next --label {args.label!r}",
```

New text:

```
                f"--next",
```

### `u189.M15_pick_remedy_unquoted`

label_sync: the pick remedy names the label unquoted, so a name with a space pastes as two words

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M15_pick_remedy_unquoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Beta Works-'Beta Works']`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Kit's Works-"Kit's Works"]`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[beta-works-'beta-works']`

Old text:

```
                f"--next --label {args.label!r}",
```

New text:

```
                f"--next --label {args.label}",
```

### `u189.M16_empty_label_alone_walks`

label_sync: test --label for truth again, so an empty --label alone runs the whole walk

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M16_empty_label_alone_walks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif not args.next_question and (args.label or args.releases):
```

### `u189.M1_next_label_refused_again`

label_sync: restore the old refusal of --label without --answer, so --next --label is refused and no single label can be asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M1_next_label_refused_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_question_the_plain_next_saved_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif args.label is not None or args.releases:
```

### `u189.M2_label_alone_not_refused`

label_sync: drop the refusal of --label or --release alone, so they fall through to the interactive walk and name nothing

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M2_label_alone_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv2-go with --answer]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv3-go with --answer]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv0]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv1]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif False:
```

### `u189.M3_next_release_not_refused`

label_sync: drop the refusal of --next with --release, so the named releases are silently ignored

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M3_next_release_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv6---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv7---next would ignore the releases]`

Old text:

```
    elif args.next_question and args.releases:
```

New text:

```
    elif False:
```

### `u189.M4_empty_name_not_refused`

label_sync: drop the refusal of --next with an empty --label, so a blank name reaches the registry as an unfollowed label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M4_empty_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_with_an_empty_name_is_refused_as_no_name_given[   ]`
  - `tests/test_label_sync.py::test_next_label_with_an_empty_name_is_refused_as_no_name_given[]`

Old text:

```
    elif args.next_question and args.label is not None and not args.label.strip():
```

New text:

```
    elif False:
```

### `u189.M5_alone_hint_drops_the_label`

label_sync: reword the --label alone hint to the plain --next, which walks from the top

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M5_alone_hint_drops_the_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv0]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv1]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
            "to ask about one label: crate label sync --next --label NAME",
```

New text:

```
            "to ask about one label: crate label sync --next",
```

### `u189.M6_label_not_passed`

label_sync: call _next without the named label, so --next --label walks every label from the top

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M6_label_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
        return _next(ctx, cfg, args.label)
```

New text:

```
        return _next(ctx, cfg)
```

### `u189.M7_unknown_name_not_refused`

_next: resolve the name without refusing, so an unfollowed name walks every label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M7_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`

Old text:

```
    only = _entry_or_refuse(followed, name) if name is not None else None
```

New text:

```
    only = followed.resolve(name) if name is not None else None
```

### `u189.M8_entries_ignore_the_one`

_next: walk every followed label even when one is named

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M8_entries_ignore_the_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
    entries = [only] if only is not None else list(followed.labels.values())
```

New text:

```
    entries = list(followed.labels.values())
```

### `u189.S1_saved_question_relisted`

_next, sample of the unit's existing guards: never reuse a saved question, so every --next lists the label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S1_saved_question_relisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_question_is_printed_again_with_no_provider_call`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_question_the_plain_next_saved_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`

Old text:

```
            if isinstance(pending, Mapping) and pending.get("releases"):
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
```

New text:

```
            if False:
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
```

### `u189.S2_question_not_saved`

_next, sample of the unit's existing guards: print a new question without saving it, so no answer can apply to it

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S2_question_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 119 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv5-goes with --answer pick]`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - `tests/test_label_sync.py::test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer`
  - `tests/test_label_sync.py::test_a_saved_question_is_printed_again_with_no_provider_call`
  - `tests/test_label_sync.py::test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - ... and 104 more, see the JSON sidecar

Old text:

```
                question = listed.question
                _save_pending(cfg, question)
```

New text:

```
                question = listed.question
```

### `u16-round-8-independent-composites.V24_approximate_limit_raised`

APPROXIMATE_LIMIT coefficient raised from 5 to 10; every test referencing it compares against match.APPROXIMATE_LIMIT itself, so the hunt predicts the value can drift green

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent-composites.json`, row `V24_approximate_limit_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
APPROXIMATE_LIMIT = 5

```

New text:

```
APPROXIMATE_LIMIT = 10

```

### `u16-round-8-independent.V11_candidate_order_sorted`

Candidate groups iterate sorted instead of insertion order, so the approximate offer truncates the best hit instead of the worst

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V11_candidate_order_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
    for recording, version_key, key in grouped:

```

New text:

```
    for recording, version_key, key in sorted(grouped):

```

### `u16-round-8-independent.V12_approximate_floor_halved`

APPROXIMATE_FLOOR coefficient halved from 82 to 41, admitting resemblances the unit exists to keep out of the offer

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V12_approximate_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 13 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_unrelated_title_by_another_artist_is_still_not_offered`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 41

```

### `u16-round-8-independent.V13_withheld_not_reported`

The truncated approximate offer stops saying how many candidates were withheld, so a rejection rejects answers never shown

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V13_withheld_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`

Old text:

```
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),

```

New text:

```
            withheld=0,

```

### `u16-round-8-independent.V14_tombstone_fold_nfd`

tombstone_fold normalizes NFD instead of NFC, drifting from U24's byte-for-byte algorithm so a recorded suppression can never be found

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V14_tombstone_fold_nfd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_composed_address_still_matches_a_row_spelled_that_way[Caf\xe9 del Mar-Track-Live]`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Caf\xe9 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Cafe\u0301 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

Old text:

```
        " ", unicodedata.normalize("NFC", str(value)).casefold()

```

New text:

```
        " ", unicodedata.normalize("NFD", str(value)).casefold()

```

### `u16-round-8-independent.V15_empty_identity_accepted`

The empty tombstone identity refusal removed alone, so every unnamed candidate collides onto one suppression

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V15_empty_identity_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_identity_with_neither_an_artist_nor_a_title_is_refused`

Old text:

```
    if not folded_artist and not folded_title:

```

New text:

```
    if False:

```

### `u16-round-8-independent.V16_key_leaves_item_identity`

The list's key leaves the review item identity, so one answer settles the key question and the version question both

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V16_key_leaves_item_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_review_item_identity_is_not_the_tombstone_identity`

Old text:

```
        "key": key_token(key),

```

New text:

```
        "key": "",

```

### `u16-round-8-independent.V18_rejection_skips_tombstones`

A rejection stops consulting the tombstones, so a rejected question hands acquisition a version standing under a tombstone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V18_rejection_skips_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition`
  - `tests/test_match_states.py::test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`

Old text:

```
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )

```

New text:

```
        standing = None

```

### `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate`

An unspecific yes stops being bound to the candidate it was given about and accepts whatever the library holds today

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V19_unbound_yes_takes_todays_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`

Old text:

```
            chosen = [c for c in found.candidates if c.candidate_id == about]

```

New text:

```
            chosen = list(found.candidates)

```

### `u16-round-8-independent.V1_key_check_first_copy_only`

Exact branch reads only the first held copy's key, so an unkeyed copy that sorts first answers the key question for a keyed one

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V1_key_check_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}

```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}

```

### `u16-round-8-independent.V20_digest_width_halved`

DIGEST_WIDTH coefficient halved from 16 to 8 hex characters, dropping identifier collision resistance from 64 to 32 bits

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V20_digest_width_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_declared_width_survives_a_population_a_narrower_one_does_not`
  - `tests/test_match_states.py::test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement`

Old text:

```
DIGEST_WIDTH = 16

```

New text:

```
DIGEST_WIDTH = 8

```

### `u16-round-8-independent.V21_suppression_asked_one_spelling`

The tombstone store is asked under one spelling instead of every spelling a version could be recorded under, re-acquiring deletions recorded from another spelling

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V21_suppression_asked_one_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path - nightwave remix]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path [nightwave remix]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path [Original Version]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path-Sun Path (Original Mix)]`

Old text:

```
    for identity in wanted.suppression_spellings:

```

New text:

```
    for identity in (wanted.identity,):

```

### `u16-round-8-independent.V3_version_differs_silently_joins`

A recording owned only at another version resolves MATCHED instead of needs review, the silent join R11 forbids

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V3_version_differs_silently_joins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 41 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_persons_acceptance_being_applied_retires_nothing`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_question_answered_from_one_source_is_never_asked_again_from_another`
  - `tests/test_match_states.py::test_a_rejected_question_makes_the_track_missing_rather_than_matched`
  - `tests/test_match_states.py::test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.VERSION_DIFFERS,

```

### `u16-round-8-independent.V5_ambiguous_reading_promoted`

The other-reading question resolves MATCHED, reporting ownership of a record nobody checked

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V5_ambiguous_reading_promoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.READING_AMBIGUOUS,

```

### `u16-round-8-independent.V6_reading_question_never_asked`

The other-reading guard layer removed alone: the question is never asked and the row falls through to approximate or missing

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V6_reading_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    confirming = _other_reading_the_library_holds(wanted, index)

```

New text:

```
    confirming = None

```

### `u16-round-8-independent.V7_tombstoned_counted_missing`

Resolution never consults the tombstones, so a suppressed version reports MISSING with acquisition options and the deletion is undone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V7_tombstoned_counted_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_suppressed_track_is_in_none_of_the_three_arrays`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )

```

New text:

```
    standing = None

```

### `u16-round-8-independent.V8_missing_without_options`

A missing row carries no acquisition options, so the review queue item has nothing to offer (R12)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V8_missing_without_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[ambiguous-dash]`
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it`

Old text:

```
        acquisitions=acquisition_options(wanted),

```

New text:

```
        acquisitions=(),

```

### `u16-round-8-independent.V9_relative_key_by_letter`

Relative major or minor detected by matching letter instead of matching wheel number, so 8A vs 8B reads as outright disagreement and 8A vs 9A as relative

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V9_relative_key_by_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_relative_key_disagreement_surfaces_rather_than_picking_one`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-last]`

Old text:

```
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS

```

New text:

```
    return Why.KEY_RELATIVE if left[1] == right[1] else Why.KEY_DIFFERS

```

### `u269.M7_match_engine_binds_lxml`

acquire/match.py: bind lxml.etree under a branch that never runs, the export reader guard's lxml case, which stays as it is

- File: `src/cratekit/acquire/match.py`
- Source: `u269.json`, row `M7_match_engine_binds_lxml`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_export_guard_stays_quiet_on_correct_code[from . import match\n]`
  - `tests/test_match_states.py::test_the_match_engine_never_reaches_a_rekordbox_export`

Old text:

```
import hashlib

```

New text:

```
import hashlib

if False:
    import lxml.etree  # noqa: F401

```

### `u16-round-8-independent.V22_suppressed_warning_omitted`

The suppressed rows stop being reported on the warning channel, so a suppression is omitted silently (R36)

- File: `src/cratekit/acquire/match_cli.py`
- Source: `u16-round-8-independent.json`, row `V22_suppressed_warning_omitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_listing_both_records_answer_is_reported_under_the_tombstone`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    for track in result.suppressed:

```

New text:

```
    for track in ():

```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[awaiting-import]`
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[committed-unverified]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[awaiting-import-gone-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[committed-unverified-gone-False]`

Old text:

```
    if record.state is not SessionState.OPEN:
        return False
    recorded = record.detail.get(HOLDER_KEY)
```

New text:

```
    if record.terminal:
        return False
    recorded = record.detail.get(HOLDER_KEY)
```

