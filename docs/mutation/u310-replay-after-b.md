# Mutation table: u310-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 23:18 UTC, branch `after-b` at `3ab6abf3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22849 collected. pytest invocations for this batch: 116.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 19, each measured by this driver.

Known failures: 254 node ids whose failure is this machine's and not the tree's, read from `../u310-replay-known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22849 against 22849. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u23-round-8-independent.X1_approval_type_check_never_fires` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 7 | killed |
| `u23-round-8-independent.X2_approval_option_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X3_approval_actor_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X4_approval_digest_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X5_grant_accepts_a_blank_actor` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `u55-collection-reader.R3_soft_delete_marker` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 54 | 1 | killed |
| `u55-collection-reader.R4_genre_proxy` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 54 | 21 | killed |
| `r797-c.G1_the_threshold_is_fifty` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 7 | killed |
| `r797-c.G2_at_the_threshold_is_named` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 4 | killed |
| `r797-c.G3_a_removed_row_is_not_counted` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 1 | killed |
| `r797-c.G4_no_genre_is_not_a_genre` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 3 | killed |
| `r797-c.G5_another_spelling_is_the_same_genre` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 3 | killed |
| `r758-b.M2_unnamed_genre_is_moved` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `r758-b.M3_renamed_playlist_is_moved_from` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A11_tree_reading_from_entry_sub` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A2_tree_path_adds_a_sub` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 8 | killed |
| `r780-a.A4_excluded_track_moved` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A5_style_doubles_decided` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A6_every_entry_claims_its_bucket` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `r780-a.A8_double_listed_beside_a_move` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r797-b.M7_a_track_still_there_is_listed` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 10 | killed |
| `u118-c.M10_no_reading_leaves_split` | `src/cratekit/adopt/move.py` | user | 2 file(s) | 100 | 3 | killed |
| `u118-c.M1_declarer_settles` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 187 | 5 | killed |
| `u118-c.M2_holder_genre_leg` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 187 | 1 | killed |
| `u118-c.M4_held_split_none` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 187 | 2 | killed |
| `u118-c.M8_asked_split` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 187 | 2 | killed |
| `u133-b-rerun.E2_former_place_only` | `src/cratekit/adopt/move.py` | user | 4 file(s) | 213 | 10 | killed |
| `r758-b.C1_gate_asked_before_the_acknowledgment` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r758-b.C3_rows_not_proven_against_the_digest` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r758-b.C5_a_sub_nobody_was_shown_is_removed` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r758-b.C6_left_target_is_added_back` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r758-b.C9_read_back_is_not_the_verdict` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-b.B1_reading_not_rechecked` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 2 | killed |
| `r780-b.B2_worker_asks_the_entry_bucket` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 8 | killed |
| `r780-b.B3_renamed_target_reads_as_done` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-b.B4_gone_named_once_per_move` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-b.B5_verdicts_not_handed_to_the_worker` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r797-b.M4_the_writer_never_files_into_one` | `src/cratekit/adopt/move_cli.py` | user | 3 file(s) | 172 | 1 | killed |
| `r797-b.M5_the_writer_can_leave_one` | `src/cratekit/adopt/move_cli.py` | user | 3 file(s) | 172 | 2 | killed |
| `r731-b.M16_skewed_registry_raises_at_the_plan` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 68 | 1 | killed |
| `r731-b.M17_bridge_tree_raises_at_the_plan` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 68 | 6 | killed |
| `r780-a.A7_doubled_rows_not_carried` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 128 | 4 | killed |
| `r788-c.L2_removed_tag_files` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 2 | killed |
| `r788-c.L4_renamed_membership_unseen` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-c.L5_renamed_bucket_unseen` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 3 | killed |
| `r788-c.L6_removed_node_is_a_place` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 1 | killed |
| `r788-c.L9_every_library_is_calibrated` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 2 | killed |
| `r797-b.M1_found_in_the_holding_folder` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 172 | 5 | killed |
| `r797-b.M2_recorded_under_the_old_sub` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 172 | 2 | killed |
| `u118-b.P1_named_place_split` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 141 | 23 | killed |
| `u118-b.P2_recorded_under_split` | `src/cratekit/adopt/placements.py` | maintainer | 3 file(s) | 141 | 1 | killed |
| `r658-c.S4c_dataless_skip_returns` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 615 | 1 | killed |
| `r759.A1_deadline_asked_only_at_the_end` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.A2_deadline_a_second_late` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 1 | 1 | killed |
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
| `u23-round-8-independent.S1_size_of_always_none` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X12_look_at_drops_the_regular_file_test` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `r722.S1_unreadable_folded` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 4 | killed |
| `r722.S2_track_drops_energy` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 7 | killed |
| `r722.S3_track_drops_flag` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 4 | killed |
| `r722.S4_default_reader_lenient` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 4 | killed |
| `r722.S5_catch_oserror_only` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 62 | killed |
| `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 5 | killed |
| `u23-round-8-independent.X14_probe_drops_the_dataless_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X7_classify_accepts_the_fallback_tier` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X8_classify_drops_the_too_coarse_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `u247.M8_scan_freezes_its_declaration` | `src/cratekit/adopt/scan_cli.py` | user | 2 file(s) | 45 | 1 | killed |
| `u55-collection-reader.R11_scan_item_ids` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 27 | 4 | killed |
| `u55-collection-reader.R9_scan_zero_item_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u55-collection-reader.R1_read_only_open` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 54 | 2 | killed |
| `r780-a.A9_refused_buckets_empty` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `r797-d.M6_again_settled_in_one_bucket` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 6 | killed |
| `r797-d.M8_again_an_unread_file_is_no_reading` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 2 | killed |
| `u118-c.M6_verdict_reason` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 56 | 1 | killed |
| `u118-c.M7_unnamed_reason` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 56 | 1 | killed |
| `r788-d.A5_move_worker_reads_vocals` | `src/cratekit/adopt/move_cli.py` | maintainer | 2 file(s) | 114 | 1 | killed |
| `r788-c.L1_any_vox_value_is_the_tag` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 161 | 2 | killed |

## Row definitions

### `u23-round-8-independent.X1_approval_type_check_never_fires`

R34: a blanket affirmative is no longer refused by type

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X1_approval_type_check_never_fires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 7 (killed)
- Killed:
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[NoneTypeNone]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[boolTrue]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'approved':]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'digest': ']`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[int1]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[strapprove]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[stryes]`

Old text:

```
    if not isinstance(approval, Approval):
```

New text:

```
    if not isinstance(approval, object):
```

### `u23-round-8-independent.X2_approval_option_unchecked`

A recorded answer that is not the approve option is accepted

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X2_approval_option_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_recorded_answer_that_is_not_an_approval_applies_nothing`

Old text:

```
    if approval.option != APPROVE:
```

New text:

```
    if approval.option is None:
```

### `u23-round-8-independent.X3_approval_actor_unchecked`

An approval naming nobody is accepted at apply time

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X3_approval_actor_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(approval.actor).strip():
```

New text:

```
    if approval.actor is None:
```

### `u23-round-8-independent.X4_approval_digest_unchecked`

An approval given for a different plan is accepted

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X4_approval_digest_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_for_a_different_plan_is_refused`

Old text:

```
    if approval.digest != current:
```

New text:

```
    if approval.digest is None:
```

### `u23-round-8-independent.X5_grant_accepts_a_blank_actor`

grant records an approval attributed to nobody

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X5_grant_accepts_a_blank_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(actor).strip():
```

New text:

```
    if actor is None:
```

### `u55-collection-reader.R3_soft_delete_marker`

R-186's exact defect: default the tombstone marker instead of reading it

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R3_soft_delete_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_row_that_cannot_report_the_marker_refuses_rather_than_defaulting`

Old text:

```
            deleted=trees.soft_delete_marker(row),
```

New text:

```
            deleted=bool(getattr(row, "rb_local_deleted", False)),
```

### `u55-collection-reader.R4_genre_proxy`

Read the raw GenreID rather than the binding's own display proxy

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R4_genre_proxy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 54 against a baseline of 54
- Kills: 21 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return str(getattr(row, "GenreName", "") or "")
```

New text:

```
    return str(getattr(row, "GenreID", "") or "")
```

### `r797-c.G1_the_threshold_is_fifty`

FOLDER_WORTH: 51, a realistic nearby value, so a genre at 50 is not named

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G1_the_threshold_is_fifty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 7 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named`
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`
  - `tests/test_report_genres.py::test_the_summary_a_person_reads_in_help_states_the_threshold_the_code_uses`
  - `tests/test_report_genres.py::test_with_nothing_at_the_threshold_the_report_says_so_in_a_row`

Old text:

```
FOLDER_WORTH = 50
```

New text:

```
FOLDER_WORTH = 51
```

### `r797-c.G2_at_the_threshold_is_named`

named: over the threshold and not at it

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G2_at_the_threshold_is_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named`
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`

Old text:

```
genre.tracks >= self.threshold
```

New text:

```
genre.tracks > self.threshold
```

### `r797-c.G3_a_removed_row_is_not_counted`

count: count a row rekordbox marked removed, so a folder is suggested for what a person deleted

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G3_a_removed_row_is_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_removed_row_is_not_counted`

Old text:

```
        if row.deleted:
            continue

```

New text:

```
(empty)
```

### `r797-c.G4_no_genre_is_not_a_genre`

count: resolve an empty genre like any other, so the tagging backlog is counted as a genre or as having a folder

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G4_no_genre_is_not_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_report_genres.py::test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged`
  - `tests/test_report_genres.py::test_every_live_track_is_counted_exactly_once`
  - `tests/test_report_genres.py::test_tracks_with_no_genre_are_counted_apart_and_never_named`

Old text:

```
        if not value:
```

New text:

```
        if False:
```

### `r797-c.G5_another_spelling_is_the_same_genre`

count: stop folding another spelling of a style sub's name onto the sub, the review's 45 and 10

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G5_another_spelling_is_the_same_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`
  - `tests/test_report_genres.py::test_another_spelling_of_a_style_subs_own_name_is_counted_with_it`

Old text:

```
        elif value.casefold() in style_subs:
```

New text:

```
        elif False:
```

### `r758-b.M2_unnamed_genre_is_moved`

a track whose genre names no style is moved to the resolver's default

- File: `src/cratekit/adopt/move.py`
- Source: `r758-b.json`, row `M2_unnamed_genre_is_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_genre_that_stopped_naming_the_style_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_the_genre_decides_a_style_move_and_a_genre_naming_no_style_is_left`

Old text:

```
    return "" if entry.genre in by_source.map else LEFT_NO_STYLE
```

New text:

```
    return ""
```

### `r758-b.M3_renamed_playlist_is_moved_from`

a sub held through a renamed playlist only is planned for a move the writer cannot make

- File: `src/cratekit/adopt/move.py`
- Source: `r758-b.json`, row `M3_renamed_playlist_is_moved_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[under-another-name]`

Old text:

```
    if unnamed:
        return LEFT_UNNAMED

```

New text:

```
(empty)
```

### `r780-a.A11_tree_reading_from_entry_sub`

the tree path takes adoption's sub as the reading in every bucket, so a track with no entry sub has no target and a double is left rather than moved

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A11_tree_reading_from_entry_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_reading_is_asked_of_the_one_resolver_in_either_bucket`

Old text:

```
    if claims(entry, bucket):
        return entry.sub
    try:
```

New text:

```
    if entry.sub:
        return entry.sub
    try:
```

### `r780-a.A2_tree_path_adds_a_sub`

in a bucket the genre does not name, a reading naming none of the held subs plans a move that adds that sub and removes the rest, filing the track by a rule adoption does not use

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A2_tree_path_adds_a_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_double_beside_a_track_left_for_another_reason_is_still_listed`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_track_with_no_genre_is_asked_in_every_bucket_it_doubles_in`
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[names-neither-elsewhere]`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_the_gate_shows_every_move_with_what_it_adds_removes_and_reads`

Old text:

```
    elif target not in held:
        reason = LEFT_NAMES_NEITHER

```

New text:

```
(empty)
```

### `r780-a.A4_excluded_track_moved`

a track whose file the census could not read is moved on the reading its row happens to carry

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A4_excluded_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[excluded-in-two-bands]`

Old text:

```
    elif entry.disposition is Disposition.EXCLUDED or entry.energy is None or not target:
```

New text:

```
    elif entry.energy is None or not target:
```

### `r780-a.A5_style_doubles_decided`

the tree path decides in style buckets too, by the genre's resolver answer, which the brief puts out of scope; the one predicate the selection, the decision and the doubled listing share

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A5_style_doubles_decided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_what_the_tree_path_never_asks_about`

Old text:

```
    return kind is routing.Competing.BAND

```

New text:

```
    return True

```

### `r780-a.A6_every_entry_claims_its_bucket`

a verdict withheld entry claims its bucket, so it goes to the R-758 path, which returns nothing for it, and the double is neither moved nor listed

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A6_every_entry_claims_its_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_a_verdict_withheld_since_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason`

Old text:

```
    if entry.disposition is Disposition.ROUTE:
        return True
    return entry.disposition is Disposition.WITHHELD and entry.held_elsewhere
```

New text:

```
    return True
```

### `r780-a.A8_double_listed_beside_a_move`

a doubled target is listed as left beside the move that keeps it, so one track reads as both moved and left in one bucket

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A8_double_listed_beside_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_doubled_target_beside_a_stale_sub_is_a_move_and_the_double_is_listed_after`

Old text:

```
                if isinstance(found, Move):
                    moves.append(found)
                    continue

```

New text:

```
                if isinstance(found, Move):
                    moves.append(found)

```

### `r797-b.M7_a_track_still_there_is_listed`

buckets_asked: never ask a bucket about a track that holds nothing there but a former place, so the old playlist reads as empty while it holds tracks

- File: `src/cratekit/adopt/move.py`
- Source: `r797-b.json`, row `M7_a_track_still_there_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[another-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[no-genre]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread-genre-names-the-old-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[holder]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[promoted]`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_digest_moves_when_a_track_turns_up_in_the_old_playlist`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
        if bucket.formerly and in_former_place_only(
```

New text:

```
        if False and in_former_place_only(
```

### `u118-c.M10_no_reading_leaves_split`

A Soul track with no reading is left in R&B rather than moved to Soul Unsorted

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M10_no_reading_leaves_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_with_no_reading_leaves_r_and_b_for_soul_unsorted`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`

Old text:

```
        return "" if set(stale) <= routing.left_only(declared, entry.bucket) else LEFT_NO_READING
```

New text:

```
        former = {place.id for _declarer, place in routing.former_places(declared, entry.bucket)}
        return "" if set(stale) <= former else LEFT_NO_READING
```

### `u118-c.M1_declarer_settles`

The declaring bucket's tree path decides on split places, so R&B tracks in two R&B bands are listed under Soul

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M1_declarer_settles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 187 against a baseline of 187
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_split_place.py::test_a_track_in_two_r_and_b_bands_whose_genre_names_neither_is_not_listed_under_soul[another-folder]`
  - `tests/test_adopt_split_place.py::test_a_track_in_two_r_and_b_bands_whose_genre_names_neither_is_not_listed_under_soul[no-genre]`
  - `tests/test_adopt_split_place.py::test_an_r_and_b_track_in_two_r_and_b_bands_is_still_r_and_bs_to_settle`

Old text:

```
        if declarer == bucket:
            settled.add(place.id)
```

New text:

```
        if declarer == bucket:
            pass
```

### `u118-c.M2_holder_genre_leg`

The holder settles its places only for an entry claiming Soul, not for one whose genre names it

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M2_holder_genre_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`

Old text:

```
        elif claims(entry, declarer) or genre_names(entry, declarer, declared):
```

New text:

```
        elif claims(entry, declarer):
```

### `u118-c.M4_held_split_none`

No unclaimed Soul track in a split place is listed

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M4_held_split_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`
  - `tests/test_adopt_split_place.py::test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved`

Old text:

```
    if not split or claims(entry, bucket) or not genre_names(entry, bucket, declared):
        return ()
```

New text:

```
    if True:
        return ()
```

### `u118-c.M8_asked_split`

The plan never asks about a bucket where the track is only in a split place nobody claims

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M8_asked_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`
  - `tests/test_adopt_split_place.py::test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved`

Old text:

```
        if held_in_split_place(entry, bucket.id, placements, declared):
            asked.append(bucket.id)
            continue

```

New text:

```
(empty)
```

### `u133-b-rerun.E2_former_place_only`

Existing guard sample: a track sitting only in a former place is never recognised as one

- File: `src/cratekit/adopt/move.py`
- Source: `u133-b-rerun.json`, row `E2_former_place_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 213 against a baseline of 213
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[another-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[no-genre]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread-genre-names-the-old-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[holder]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[promoted]`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_digest_moves_when_a_track_turns_up_in_the_old_playlist`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
    return bool(held) and set(held) <= former

```

New text:

```
    return False

```

### `r758-b.C1_gate_asked_before_the_acknowledgment`

the verb asks its gate without reading the backup acknowledgment first

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C1_gate_asked_before_the_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).

```

### `r758-b.C3_rows_not_proven_against_the_digest`

the digest of the frozen rows is not taken again, so edited rows are shown and performed under the approved digest

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C3_rows_not_proven_against_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`

Old text:

```
    if not (taken == stated == queued_under):
```

New text:

```
    if not (stated == queued_under):
```

### `r758-b.C5_a_sub_nobody_was_shown_is_removed`

a track filed in a further sub since the approval has that sub removed as well

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C5_a_sub_nobody_was_shown_is_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`

Old text:

```
        if set(now.remove) - set(move.remove):
            stale[move.content_id] = "it holds a sub nobody was shown"
            continue

```

New text:

```
(empty)
```

### `r758-b.C6_left_target_is_added_back`

a track approved as already in its target that has left it is added back and its other sub removed

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C6_left_target_is_added_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_approved_as_in_its_target_that_left_it_is_a_stale_decision`

Old text:

```
        if now.add and not move.add:
            stale[move.content_id] = "it has left the sub it was approved as holding"
            continue

```

New text:

```
(empty)
```

### `r758-b.C9_read_back_is_not_the_verdict`

the job fails only when the writer raised, so tracks still in both subs drive it to succeeded

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C9_read_back_is_not_the_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`

Old text:

```
    if interrupted is not None or unfinished:
```

New text:

```
    if interrupted is not None:
```

### `r780-b.B1_reading_not_rechecked`

the worker does not ask whether the reading still names the approved target, so a track retagged since the approval is moved to a sub its file no longer names

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B1_reading_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names`

Old text:

```
        if move_engine.reading_target(entry, move.bucket, declared) != move.target:
            stale[move.content_id] = "its reading names another place"
            continue

```

New text:

```
(empty)
```

### `r780-b.B2_worker_asks_the_entry_bucket`

the worker asks the plan's rule of the entry's own bucket rather than the bucket the move names, so every tree path move is refused as one the plan does not make

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B2_worker_asks_the_entry_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names`
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`

Old text:

```
        now = move_engine.standing_in(
            entry, move.bucket, current.placements, declared, tree=current.tree, refused=refused
        )
```

New text:

```
        now = move_engine.standing(entry, current.placements, declared, tree=current.tree)
```

### `r780-b.B3_renamed_target_reads_as_done`

a track whose one place is its target through a renamed playlist reads as finished, which nobody was shown

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B3_renamed_target_reads_as_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_target_held_only_under_another_name_is_not_done`

Old text:

```
            if held == {move.target} and not unnamed & held:
                continue
```

New text:

```
            if held == {move.target}:
                continue
```

### `r780-b.B4_gone_named_once_per_move`

a track gone from the collection is named once per move it carried, so the report lists it twice

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B4_gone_named_once_per_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_one_track_carries_a_move_in_each_bucket_it_doubles_in`

Old text:

```
    return tuple(todo), tuple(sorted(gone))
```

New text:

```
    return tuple(todo), tuple(
        sorted(move.content_id for move in approved if move.content_id in gone)
    )
```

### `r780-b.B5_verdicts_not_handed_to_the_worker`

the worker asks the plan's rule with no refused bucket, so a move approved before a verdict landed is performed into the refused folder

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B5_verdicts_not_handed_to_the_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`

Old text:

```
    refused = move_engine.refused_buckets(current.entries)
```

New text:

```
    refused = frozenset()
```

### `r797-b.M4_the_writer_never_files_into_one`

membership_moves: resolve the target the way a place left is resolved, so a frozen row naming a former place as its target is written

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r797-b.json`, row `M4_the_writer_never_files_into_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_move_whose_target_is_a_former_place_is_refused_and_nothing_is_written`

Old text:

```
            target = destination(declared, move.bucket, move.target)
```

New text:

```
            target = placements.named_place(declared, move.bucket, move.target)
```

### `r797-b.M5_the_writer_can_leave_one`

membership_moves: resolve a place left through destination, which knows no former place, so every move out of the old playlist refuses

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r797-b.json`, row `M5_the_writer_can_leave_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`

Old text:

```
                placements.named_place(declared, move.bucket, sub) for sub in move.remove
```

New text:

```
                destination(declared, move.bucket, sub) for sub in move.remove
```

### `r731-b.M16_skewed_registry_raises_at_the_plan`

a registry naming a root the library lacks raises out of the reader instead of answering unread

- File: `src/cratekit/adopt/placements.py`
- Source: `r731-b.json`, row `M16_skewed_registry_raises_at_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[no-such-root]`

Old text:

```
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
```

New text:

```
        except tree_registry.TreeModeRefused:
```

### `r731-b.M17_bridge_tree_raises_at_the_plan`

a tree on the bridge raises out of the reader instead of answering unread

- File: `src/cratekit/adopt/placements.py`
- Source: `r731-b.json`, row `M17_bridge_tree_raises_at_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 68 against a baseline of 68
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[None]`
  - `tests/test_adopt_workers.py::test_an_uncut_library_reads_neither_its_tree_nor_its_vocals`

Old text:

```
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
```

New text:

```
        except tree_registry.RegistrySkew:
```

### `r780-a.A7_doubled_rows_not_carried`

the placement reader drops the multiplicity the tree walk counted, so a pair held by two rows is never listed

- File: `src/cratekit/adopt/placements.py`
- Source: `r780-a.json`, row `A7_doubled_rows_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 128 against a baseline of 128
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_the_gate_shows_every_move_with_what_it_adds_removes_and_reads`
  - `tests/test_adopt_placements.py::test_a_double_in_a_renamed_recorded_node_is_still_a_double`
  - `tests/test_adopt_placements.py::test_a_pair_held_by_two_rows_is_held_once_and_doubled`

Old text:

```
            for content_id in {cid for node in answering for cid in node.doubled}:
```

New text:

```
            for content_id in ():
```

### `r788-c.L2_removed_tag_files`

vox_tagged: an association rekordbox removed is read as a tag, so a track a person untagged is filed

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L2_removed_tag_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_tag_a_person_took_off_is_not_a_tag`
  - `tests/test_adopt_vocals.py::test_an_association_that_cannot_say_whether_it_was_removed_refuses`

Old text:

```
        if not _removed(song, "My Tag association")
```

New text:

```
        if True
```

### `r788-c.L4_renamed_membership_unseen`

vocals_from: nobody is held under another name only, so a track in a renamed vocal playlist with a named one beside it is added to the named one too

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L4_renamed_membership_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_renamed_vocal_playlist_is_found_through_its_recorded_node_and_says_so`
  - `tests/test_adopt_vocals.py::test_a_track_held_under_both_names_is_not_held_under_another_name_only`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
        if under_another:
            unnamed[bucket.id] = frozenset(under_another)
```

New text:

```
        if False:
            unnamed[bucket.id] = frozenset(under_another)
```

### `r788-c.L5_renamed_bucket_unseen`

vocals_from: no bucket is named as having its vocal sub under another name only

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L5_renamed_bucket_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_renamed_vocal_playlist_is_found_through_its_recorded_node_and_says_so`
  - `tests/test_adopt_vocals.py::test_an_empty_renamed_vocal_playlist_still_names_its_bucket`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
        if answering and not by_display.get(names):
            renamed.add(bucket.id)
```

New text:

```
        if False:
            renamed.add(bucket.id)
```

### `r788-c.L6_removed_node_is_a_place`

_indexed: a playlist rekordbox removed is indexed with the live ones, for both readers. The existing guard this unit moved into a shared body

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L6_removed_node_is_a_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_removed_vocal_playlist_is_not_a_place`

Old text:

```
    live = [node for node in nodes if not node.removed]
```

New text:

```
    live = list(nodes)
```

### `r788-c.L9_every_library_is_calibrated`

vocal_standing: any library with a vocal sub stands, so an uncalibrated one files from its tags

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L9_every_library_is_calibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_calibration_that_cannot_be_read_refuses_before_the_library_is_walked`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`

Old text:

```
    return metadata_cli.load_vocal_threshold(cfg) is not None
```

New text:

```
    return True
```

### `r797-b.M1_found_in_the_holding_folder`

named_place: look for a former place in the declaring bucket's folder, where the old playlist never was

- File: `src/cratekit/adopt/placements.py`
- Source: `r797-b.json`, row `M1_found_in_the_holding_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_is_found_in_the_folder_of_the_bucket_that_held_it`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`

Old text:

```
    return declared.bucket(former.bucket).display, former.display
```

New text:

```
    return declared.bucket(bucket_id).display, former.display
```

### `r797-b.M2_recorded_under_the_old_sub`

recorded_under: ask for a former place's node under the bucket that now declares it, so a renamed old playlist reads as absent

- File: `src/cratekit/adopt/placements.py`
- Source: `r797-b.json`, row `M2_recorded_under_the_old_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_is_found_in_the_folder_of_the_bucket_that_held_it`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`

Old text:

```
    return former.bucket, former.sub
```

New text:

```
    return bucket_id, sub_id
```

### `u118-b.P1_named_place_split`

named_place resolves a split place as a sub of the declaring bucket

- File: `src/cratekit/adopt/placements.py`
- Source: `u118-b.json`, row `P1_named_place_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`
- Collected: 141 against a baseline of 141
- Kills: 23 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_placements.py::test_a_band_label_a_bucket_overrides_still_resolves_to_the_band`
  - `tests/test_adopt_placements.py::test_a_double_in_a_playlist_that_is_not_a_place_is_not_carried`
  - `tests/test_adopt_placements.py::test_a_double_in_a_renamed_recorded_node_is_still_a_double`
  - `tests/test_adopt_placements.py::test_a_node_carrying_the_declared_names_is_the_sub_it_names`
  - `tests/test_adopt_placements.py::test_a_pair_held_by_two_rows_is_held_once_and_doubled`
  - `tests/test_adopt_placements.py::test_a_recorded_node_that_carries_the_declared_names_is_not_unnamed`
  - `tests/test_adopt_placements.py::test_a_renamed_node_is_resolved_through_its_recorded_identifier`
  - `tests/test_adopt_placements.py::test_a_sub_class_playlist_and_a_hand_made_one_are_not_places`
  - `tests/test_adopt_placements.py::test_a_sub_held_under_both_names_is_one_the_writer_can_see`
  - `tests/test_adopt_placements.py::test_a_track_in_two_bands_holds_both`
  - `tests/test_adopt_placements.py::test_two_nodes_answering_for_one_destination_both_count`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        return named_place(declared, split.bucket, split.sub)
```

New text:

```
        return destination(declared, bucket_id, sub_id)
```

### `u118-b.P2_recorded_under_split`

recorded_under answers a split place under the declaring bucket, so a renamed holder playlist is not recognised

- File: `src/cratekit/adopt/placements.py`
- Source: `u118-b.json`, row `P2_recorded_under_split`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_place_is_found_as_the_r_and_b_place_it_is`

Old text:

```
        return recorded_under(declared, split.bucket, split.sub)
```

New text:

```
        return bucket_id, sub_id
```

### `r658-c.S4c_dataless_skip_returns`

Composite for S4, run as its own table: put back a skip that refuses to read a dataless file, which only the scoped evicted stat can reach

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r658-c.json`, row `S4c_dataless_skip_returns`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
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

### `r759.A1_deadline_asked_only_at_the_end`

the read deadline is asked only after the stream has ended, so a trickling file is read to its end before the timeout is raised

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r759.json`, row `A1_deadline_asked_only_at_the_end`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`

Old text:

```
                if not block:
                    break
                hasher.update(block)
                if time.monotonic() > give_up_at:
                    raise TimeoutError(
                        f"{path} did not finish arriving within "
                        f"{deadline_seconds} seconds"
                    )

```

New text:

```
                if not block:
                    if time.monotonic() > give_up_at:
                        raise TimeoutError(
                            f"{path} did not finish arriving within "
                            f"{deadline_seconds} seconds"
                        )
                    break
                hasher.update(block)

```

### `r759.A2_deadline_a_second_late`

the read deadline is honoured a second after it passes, so a trickling file is read fifty blocks further than the caller allowed

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r759.json`, row `A2_deadline_a_second_late`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`

Old text:

```
                if time.monotonic() > give_up_at:
                    raise TimeoutError(

```

New text:

```
                if time.monotonic() > give_up_at + 1.0:
                    raise TimeoutError(

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

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `S1_size_of_always_none`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
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

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X12_look_at_drops_the_regular_file_test`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
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

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X13_look_at_drops_the_recorded_size_shortcut`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
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

### `r722.S1_unreadable_folded`

The census reads a failed read as a file with no reading

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S1_unreadable_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
    except (tags.TagReadFailed, OSError):
        return None, True
```

New text:

```
    except (tags.TagReadFailed, OSError):
        return None, False
```

### `r722.S2_track_drops_energy`

The scanned track does not carry the level it read

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S2_track_drops_energy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
            energy=energy,
            energy_unreadable=unreadable,
```

New text:

```
            energy_unreadable=unreadable,
```

### `r722.S3_track_drops_flag`

The scanned track does not carry the unreadable flag

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S3_track_drops_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
            energy=energy,
            energy_unreadable=unreadable,
```

New text:

```
            energy=energy,
```

### `r722.S4_default_reader_lenient`

The census's default reader is the lenient one, which folds failures into None

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S4_default_reader_lenient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
    energy_reader: Callable[[Path], int | None] = tags.read_energy_checked,
```

New text:

```
    energy_reader: Callable[[Path], int | None] = tags.read_energy_from_file,
```

### `r722.S5_catch_oserror_only`

The census catches only OSError from the reader, so a failed read ends the walk

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S5_catch_oserror_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 62 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - ... and 47 more, see the JSON sidecar

Old text:

```
    except (tags.TagReadFailed, OSError):
```

New text:

```
    except OSError:
```

### `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed`

What X6 holds: the EXCLUDED disposition itself, forced to ROUTE

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent-composites.json`, row `X6_composite_excluded_becomes_routed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 5 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_every_plan_entry_identifier_is_derivable_from_the_record_it_names`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue

```

New text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.ROUTE,
                genre=row.genre,
            )
            continue

```

### `u23-round-8-independent.X14_probe_drops_the_dataless_test`

A cloud-evicted file is probed by reading it, so the census downloads

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X14_probe_drops_the_dataless_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_online_only_file_is_never_opened_by_the_probe`

Old text:

```
    if _is_dataless(info):
        return Readability.ONLINE_ONLY

```

New text:

```
(empty)
```

### `u23-round-8-independent.X7_classify_accepts_the_fallback_tier`

An unrecognised genre is routed in bulk by the router's fallback

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X7_classify_accepts_the_fallback_tier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_fallback_tier_is_never_accepted_as_an_adoption_answer`

Old text:

```
    if resolution.match is routing.Match.FALLBACK:
        return Disposition.NEEDS_GENRE, "", str(resolution.match)

```

New text:

```
(empty)
```

### `u23-round-8-independent.X8_classify_drops_the_too_coarse_test`

A generic genre is routed rather than asked about

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X8_classify_drops_the_too_coarse_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_genre_the_taxonomy_calls_too_coarse_gets_a_disposition`

Old text:

```
    if not value or declared.is_too_coarse_as_source(value):
```

New text:

```
    if not value:
```

### `u247.M8_scan_freezes_its_declaration`

adopt scan handle: judge every row of a job by the declaration its first row read, R-690's open question decided by accident

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u247.json`, row `M8_scan_freezes_its_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_active_taxonomy.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`

Old text:

```
    declared = active_taxonomy.load(cfg)
    (classified,) = scan_engine.scan_rows(
```

New text:

```
    declared = scan_engine.__dict__.setdefault(("u247", job.job_id), active_taxonomy.load(cfg))
    (classified,) = scan_engine.scan_rows(
```

### `u55-collection-reader.R11_scan_item_ids`

The scan enqueues with no items at all, which is the R-203 shape

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R11_scan_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 27 against a baseline of 27
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`

Old text:

```
            item_ids=live,
```

New text:

```
            item_ids=(),
```

### `u55-collection-reader.R9_scan_zero_item_refusal`

The scan queues a job over an empty library, which drives to SUCCEEDED having read nothing

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R9_scan_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[False]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`

Old text:

```
    if not live:
```

New text:

```
    if False:
```

### `u55-collection-reader.R1_read_only_open`

The reader asks for a WRITE intent open. The single most important row in this table.

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R1_read_only_open`
- Moved: the read only open's arguments were joined onto one line by the formatter; require_closed is flipped as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 54 against a baseline of 54
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_this_module_holds_no_write_path_at_all`

Old text:

```
rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
```

New text:

```
rb_writer.live_db_path(cfg), require_closed=True, check_app_version=False, cfg=cfg
```

### `r780-a.A9_refused_buckets_empty`

no bucket is ever read as refused, so a verdict is honoured nowhere in the tree path

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A9_refused_buckets_empty`
- Moved: the same expression joined onto one line by the formatter; it is emptied as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  - `tests/test_adopt_move.py::test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason`

Old text:

```
    return frozenset(entry.bucket for entry in entries if entry.withheld_by == WITHHELD_BY_VERDICT)
```

New text:

```
    return frozenset()
```

### `r797-d.M6_again_settled_in_one_bucket`

M6 measured again after the second review replaced its guard: read a former place the entry's own bucket settles as still held in the other, so one membership is planned twice or a track is listed beside its move

- File: `src/cratekit/adopt/move.py`
- Source: `r797-d.json`, row `M6_again_settled_in_one_bucket`
- Moved: the same expression in held_in_tree, now one line; the settled places are no longer taken away, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[another-band]`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[its-reading]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_whose_genre_names_another_style_moves_to_that_style`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[defaulted-genre]`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
    return tuple(sorted((set(placements.holds(bucket, entry.content_id)) & competing) - settled))
```

New text:

```
    return tuple(sorted(set(placements.holds(bucket, entry.content_id)) & competing))
```

### `r797-d.M8_again_an_unread_file_is_no_reading`

M8 measured again after the second review moved its condition: say a file the census could not read is left because its genre names another bucket

- File: `src/cratekit/adopt/move.py`
- Source: `r797-d.json`, row `M8_again_an_unread_file_is_no_reading`
- Moved: the former place listing now hands its fallback reason to the shared ladder _listed; an unread file never reads as no reading, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread-genre-names-the-old-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread]`

Old text:

```
    otherwise = LEFT_NO_READING if genre_names_it else LEFT_FORMER
```

New text:

```
    otherwise = LEFT_NO_READING if False else LEFT_FORMER
```

### `u118-c.M6_verdict_reason`

A Soul track a verdict refused is listed as no reading

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M6_verdict_reason`
- Moved: the split place reasons are now the ladder _listed, which the former place listing shares; a refused bucket loses its verdict reason, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`

Old text:

```
    elif refused:
        reason = LEFT_VERDICT
    else:
        reason = otherwise
```

New text:

```
    elif refused:
        reason = otherwise
    else:
        reason = otherwise
```

### `u118-c.M7_unnamed_reason`

An unclaimed Soul track in a renamed R&B band is listed as no reading

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M7_unnamed_reason`
- Moved: the split place reasons are now the ladder _listed; the unnamed reason is never given, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved`

Old text:

```
    if unnamed:
        reason = LEFT_UNNAMED
    elif refused:
```

New text:

```
    if False:
        reason = LEFT_UNNAMED
    elif refused:
```

### `r788-d.A5_move_worker_reads_vocals`

move worker: the plan it checks against is built with the vocal reads, so a refusal about a tag row or a calibration stops a move

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r788-d.json`, row `A5_move_worker_reads_vocals`
- Moved: the same call joined onto one line by the formatter; the worker reads vocals, as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`

Old text:

```
    todo, gone = remaining(approved, apply_cli.current_plan(cfg, declared, vocals=False), declared)
```

New text:

```
    todo, gone = remaining(approved, apply_cli.current_plan(cfg, declared, vocals=True), declared)
```

### `r788-c.L1_any_vox_value_is_the_tag`

vox_tagged: a value named vox under any category is the tag

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L1_any_vox_value_is_the_tag`
- Moved: the same condition joined onto one line by the formatter; the category test is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_removed_value_or_category_is_no_tag_at_all`
  - `tests/test_adopt_vocals.py::test_a_value_of_that_name_under_another_category_is_another_tag`

Old text:

```
        if str(getattr(tag, "ParentID", "") or "") in categories and not _removed(tag, "My Tag")
```

New text:

```
        if not _removed(tag, "My Tag")
```

