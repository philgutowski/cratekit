# Mutation table: u302-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 19:09 UTC, branch `cloud/859-write-layer-fifth-smaller` at `0d0528b9`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22930 collected. pytest invocations for this batch: 135.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `1cc4b9a30481`, and this tree is at `0d0528b98b36`).

Subset baselines: 12, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/d930efe3-5590-58b9-aa05-4d28a488c563/scratchpad/known-after.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22930 against 22930. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r172-a.A1_nothing_collides` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `r172-a.A2_one_round_only` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A3_shared_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r172-a.A4_occupied_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r172-a.A5_chain_held_too` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A7_targets_compared_exactly` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A9_collides_reported_as_a_rename` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `r172-b.B11_collision_step_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B12_the_first_file_is_not_named` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B13_detail_carries_nothing` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `r172-b.B14_diagnostic_surface` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 6 | killed |
| `r172-b.B16_referenced_recheck_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B17_claim_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B1_ok_whatever_happened` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 15 | killed |
| `r172-b.B2_missing_file_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B3_new_row_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B5_os_error_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B6_tag_write_answer_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r172-b.B8_tag_failure_named_where_it_was` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B9_renamed_count_is_the_promise` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r239-b.S8_naming_key_off` | `src/cratekit/write/naming_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r500-a.G1_no_refusal` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 13 | killed |
| `r500-a.G2_existence_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G3_unmapped_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G4_lexists` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G5_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r500-b.G9_plural_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G11_prefix_cap_halved` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G12_remedy_run_doctor` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G15_other_host_refuses` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r669.E1_key_from_the_head_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.E2_body_from_the_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 26 | killed |
| `r669.E3_lossy_from_the_stem_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r669.G10_apply_trusts_the_plan_for_the_hold` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G11_gate_shows_nothing` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r669.G12_shown_count_is_every_item` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G13_referenced_held_without_a_reason` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G17_held_file_never_referenced` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G18_drifted_name_renamed_anyway` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G19_no_step_for_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G1_identifier_is_no_letters` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G20_screen_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G21_artist_alone_when_no_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G2_title_alone_when_no_artist` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 5 | killed |
| `r669.G3_artist_alone_when_title_is_a_head` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G4_order_swapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 10 | killed |
| `r669.G5_first_artist_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G6_title_head_kept_in_body` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G7_unnamed_left_out_of_the_plan` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 9 | killed |
| `r669.G8_digest_ignores_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G9_unnamed_not_owed_on_apply` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r675.E2_key_not_casefolded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r675.E4_tombstones_dropped_from_the_read` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 4 | killed |
| `r675.G11_prefixes_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r675.G12_could_name_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G13_as_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r675.G14_remapped_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G15_first_location_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 4 | killed |
| `r675.G16_locations_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G17_prefixes_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G18_held_candidates_asked_about` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G19_second_step_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G1_every_dark_row_refuses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 6 | killed |
| `r675.G2_row_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 15 | killed |
| `r675.G3_candidate_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 15 | killed |
| `r675.G4_could_name_empty` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 7 | killed |
| `r675.G5_leaf_compared_as_whole_path` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 16 | killed |
| `r675.G6_plan_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G7_apply_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G8_count_reworded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `u169.N1_relative_read_against_cwd` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N2_empty_root_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u169.N3_missing_folder_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N4_name_apply_bypasses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u212.N1_second_copy_compare` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N3_taken_plain` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 2 | killed |
| `u212.N4_plan_isrc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N5_claim_plain` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 59 | 1 | killed |
| `u212.N6_cause_step` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u39-author-full.R1_filename_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u39-author-full.R2_title_fallback_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u39-author-full.R3_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 29 | killed |
| `u39-author-full.R4_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u39-author-full.R5_junk_tag_admitted` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u39-author-full.R6_lossy_flag_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u39-naming-independent.R5_bpm_wrong_type` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 71 | killed |
| `u41-author-full.R1_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u41-author-full.R6_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-author-full.T1_title_tag_fed_the_filename_body` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u41-author-full.T2_title_field_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u41-naming-independent.B1_head_precedence_swapped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-naming-independent.B2_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u41-naming-independent.B3_title_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u41-naming-independent.B7_lossy_filename_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-naming-independent.B8_lossy_title_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u41-naming-independent.C1_plan_no_op_filter_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 14 | killed |
| `u67-round-2.C1_action_filter_and_recheck` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 19 | killed |
| `u67.M2_nfc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M3_prefix_resolution` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M6_remote_host_skip` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M7_absolute_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M8_resolved_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.R1_refusal_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u67.R2_generic_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.R3_remedy_passthrough` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u130-c.C5_no_renumber` | `src/cratekit/write/playlist_pair.py` | user | 1 file(s) | 75 | 3 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 436 | 5 | killed |
| `r318.P2_withdrawn_on_single_tombstone_only` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 436 | 1 | killed |
| `r318.P3_unresolved_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 436 | 2 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 436 | 3 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 885 | 5 | killed |
| `r923.N14_verb_writes_on_abort` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 7 | killed |
| `r923.N15_verb_writes_empty_plan` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N16_ack_not_read` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N17_write_handle_not_closed` | `src/cratekit/write/row_defaults_cli.py` | maintainer | 1 file(s) | 53 | 1 | killed |
| `u115.F18_undecidable_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F19_unrenumbered_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `a32.C1_ack_after_gate` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C2_abort_writes` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C3_nothing_to_write_applies` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C4_read_back_unasserted` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |

## Row definitions

### `r172-a.A1_nothing_collides`

Hold nothing, which is the finding itself: two files rendering to one name are promised two renames and the apply performs one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A1_nothing_collides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        if not found:
            return held
        held.update(found)
```

New text:

```
        return held
```

### `r172-a.A2_one_round_only`

Ask once rather than to a fixpoint, so a file whose target a collider still holds reads as a chain sort order would resolve. This is the review's first finding, reintroduced

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A2_one_round_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`

Old text:

```
        if not found:
            return held
        held.update(found)
```

New text:

```
        held.update(found)
        return held
```

### `r172-a.A3_shared_target_ignored`

Stop holding several movers that render to one target, keeping only the occupied target half, so an arbitrary winner in sort order takes the name again

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A3_shared_target_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
            sharing = sorted(
                other.name for other in holders[_key(str(target))] if other != path
            )
```

New text:

```
            sharing = []
```

### `r172-a.A4_occupied_target_ignored`

Stop holding a mover whose rendered name a file on disk already carries, which is the collision the U67 table drove

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A4_occupied_target_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`

Old text:

```
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
            elif False:
```

### `r172-a.A5_chain_held_too`

Hold a target another mover still holds, which loses a rename that succeeds whenever sort order reaches the occupant first

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A5_chain_held_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
            elif target.exists():
```

### `r172-a.A7_targets_compared_exactly`

Compare targets as written instead of through _key, so two names differing only in case are two names on a volume that treats them as one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A7_targets_compared_exactly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        for path, target in moving:
            holders.setdefault(_key(str(target)), []).append(path)
        sources = {_key(str(path)) for path, _ in moving}
        found: dict[str, str] = {}
        for path, target in moving:
            sharing = sorted(
                other.name for other in holders[_key(str(target))] if other != path
            )
            if len(sharing) == 1:
                found[str(path)] = (
                    f"{sharing[0]} renders to the same name, and neither is renamed"
                )
            elif sharing:
                found[str(path)] = (
                    f"{', '.join(sharing)} render to the same name, and none of them "
                    f"is renamed"
                )
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
        for path, target in moving:
            holders.setdefault(str(target), []).append(path)
        sources = {str(path) for path, _ in moving}
        found: dict[str, str] = {}
        for path, target in moving:
            sharing = sorted(
                other.name for other in holders[str(target)] if other != path
            )
            if len(sharing) == 1:
                found[str(path)] = (
                    f"{sharing[0]} renders to the same name, and neither is renamed"
                )
            elif sharing:
                found[str(path)] = (
                    f"{', '.join(sharing)} render to the same name, and none of them "
                    f"is renamed"
                )
            elif str(target) not in sources and target.exists():
```

### `r172-a.A9_collides_reported_as_a_rename`

Mark a collision as an ordinary rename in the plan, so nothing in the report says which file is held and the apply attempts it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A9_collides_reported_as_a_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        elif str(path) in collides:
```

New text:

```
        elif False:
```

### `r172-b.B11_collision_step_always`

Tell a person to name a file by hand whatever the reason was, which is the review's second finding reintroduced

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B11_collision_step_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`

Old text:

```
    if collides:
        steps.append(
```

New text:

```
    if True:
        steps.append(
```

### `r172-b.B12_the_first_file_is_not_named`

Report the counts without naming the first outstanding file, which is the half of the recorded cost about nothing naming which file stayed put

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B12_the_first_file_is_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`

Old text:

```
        f"not, the first of them {incomplete[0]['from']}, {incomplete[0]['why']}",
```

New text:

```
        f"not",
```

### `r172-b.B13_detail_carries_nothing`

Drop the outstanding items from the cause detail, so a machine consumer reads a count and no names

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B13_detail_carries_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`

Old text:

```
            "incomplete": incomplete[:INCOMPLETE_SHOWN],
```

New text:

```
            "incomplete": [],
```

### `r172-b.B14_diagnostic_surface`

Answer on the default surface, which drops the plan and with it every rename that DID land

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B14_diagnostic_surface`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 6 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
```

New text:

```
    )
```

### `r172-b.B16_referenced_recheck_dropped`

A sample of an EXISTING guard: trust the plan's own referenced set instead of reading the collection again after the gate, so a file rekordbox imported while a person decided is renamed out from under its row

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B16_referenced_recheck_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`

Old text:

```
        if _is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `r172-b.B17_claim_dropped`

A sample of an EXISTING guard: rename without claiming the target first, which on this platform replaces the file that holds the name

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B17_claim_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
            if not naming.claim_target(target):
                collided += 1
```

New text:

```
            if False:
                collided += 1
```

### `r172-b.B1_ok_whatever_happened`

Answer ok however the sweep went, which is the finding itself: a plan carried out in part is reported as one carried out in full

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B1_ok_whatever_happened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 15 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

### `r172-b.B2_missing_file_unreported`

Skip a file that left while the gate waited in silence, as the shipped verb did

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B2_missing_file_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
        if not path.is_file():
            continue
```

### `r172-b.B3_new_row_unreported`

Hold back a file the collection began referencing after the gate without saying the approved rename did not happen

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B3_new_row_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`

Old text:

```
            _owed(
                item,
                "the rekordbox collection began referencing it after the plan was "
                "approved, and renaming it would strand that row",
            )
            continue
```

New text:

```
            continue
```

### `r172-b.B5_os_error_unreported`

Swallow a rename the filesystem refused, leaving a person a clean report over a file that did not move

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B5_os_error_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`

Old text:

```
                _owed(item, f"the filesystem refused the rename: {exc.strerror or exc}")
                continue
```

New text:

```
                continue
```

### `r172-b.B6_tag_write_answer_ignored`

Stop reading the answer write_tags returns, so a renamed file whose title never took the head is reported as a rename that happened in full

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B6_tag_write_answer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`

Old text:

```
        if not tags.write_tags(path, {"title": rendered.title_tag}):
            _owed(item, "it was renamed and its title tag could not be written", at=path)
```

New text:

```
        tags.write_tags(path, {"title": rendered.title_tag})
```

### `r172-b.B8_tag_failure_named_where_it_was`

Name the tag write failure at the plan's own path, which is the file's name before the rename and a file nobody can go and look at

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B8_tag_failure_named_where_it_was`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`

Old text:

```
            _owed(item, "it was renamed and its title tag could not be written", at=path)
```

New text:

```
            _owed(item, "it was renamed and its title tag could not be written")
```

### `r172-b.B9_renamed_count_is_the_promise`

Count every promised rename as performed rather than counting the ones that were, so totals.renamed is the plan's wish

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B9_renamed_count_is_the_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
        "renamed": renamed,
        "incomplete": len(incomplete),
```

New text:

```
        "renamed": len(renames),
        "incomplete": len(incomplete),
```

### `r239-b.S8_naming_key_off`

the naming verb's collection read passes unlock=False

- File: `src/cratekit/write/naming_cli.py`
- Source: `r239-b.json`, row `S8_naming_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
            require_closed=False,
            cfg=cfg,

```

New text:

```
            require_closed=False,
            unlock=False,
            cfg=cfg,

```

### `r500-a.G1_no_refusal`

Drop the refusal over dark rows in _referenced, so an unmapped row contributes only a key nothing matches and the file it names is renamed (R-500 as filed)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G1_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 13 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
    if dark:
        raise _unmapped_refusal(dark)

```

New text:

```
(empty)
```

### `r500-a.G2_existence_half_dropped`

Drop the existence half of dark, so every unmapped row refuses, including a row whose recorded file is on this machine (the first cut the review rejected)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G2_existence_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED:
```

### `r500-a.G3_unmapped_half_dropped`

Drop the UNMAPPED half of dark, so any unresolved row whose text is not a file here refuses, a streaming pseudo-location included

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G3_unmapped_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-device-relative-row]`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif not os.path.exists(decoded):
```

### `r500-a.G4_lexists`

Ask whether the recorded NAME exists rather than whether it reaches a file, so a link to nothing reads as a row that answered

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G4_lexists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`

Old text:

```
not os.path.exists(decoded):
```

New text:

```
not os.path.lexists(decoded):
```

### `r500-a.G5_recorded_key_dropped`

Drop the as recorded key. The existence rule rests on it: an unmapped row whose file exists is excused BECAUSE this key protects the file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G5_recorded_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`

Old text:

```
        keys.add(_key(decoded))

```

New text:

```
(empty)
```

### `r500-b.G9_plural_always`

Move the singular wording's bound, so one row reads as rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-b.json`, row `G9_plural_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
"collection row records" if count == 1 else
```

New text:

```
"collection row records" if count == 0 else
```

### `r500-c.G11_prefix_cap_halved`

Halve the cap on the detail's prefix list, a coefficient

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G11_prefix_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": prefixes[:10],
```

### `r500-c.G12_remedy_run_doctor`

Carry the deletion pass's run-doctor token, which sends a caller to a report no check of which reads the prefix map

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G12_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
        remedy=Remedy.FIX_CONFIG_VALUES,
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
```

### `r500-c.G15_other_host_refuses`

Existing U67 guard, sampled: a row naming another host raises out of the verb rather than being passed over

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G15_other_host_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-row-naming-another-host]`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except locations.LocationDecodeError:
            raise
```

### `r669.E1_key_from_the_head_only`

Ignore the initialkey tag and take the key from the head alone (U39)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E1_key_from_the_head_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")
```

New text:

```
    key = head.get("key")
```

### `r669.E2_body_from_the_title_tag`

Take the filename body from the title tag, the R-168 truncation, for every file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E2_body_from_the_title_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 26 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-camelot-key-without-a-tempo-renders-no-head]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    stem = naming.strip_head(path.stem, template=template)
    unnamed = None
```

New text:

```
    stem = naming.strip_head(title, template=template)
    unnamed = None
```

### `r669.E3_lossy_from_the_stem_only`

Read the lossy marker off the filename alone and miss one carried by the title

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E3_lossy_from_the_stem_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

Old text:

```
        lossy=marker in path.stem or marker in title,
```

New text:

```
        lossy=marker in path.stem,
```

### `r669.G10_apply_trusts_the_plan_for_the_hold`

Skip the post gate re-read's hold, so a body composed from a tag that is gone is still acted on

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G10_apply_trusts_the_plan_for_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`

Old text:

```
        built, why = _spec_for(path, template=template, cfg=cfg)
        if why is not None:
            _owed(item, why)
            continue
```

New text:

```
        built, why = _spec_for(path, template=template, cfg=cfg)
```

### `r669.G11_gate_shows_nothing`

Drop the gate context, which is the R-670 defect exactly

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G11_gate_shows_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_names_a_referenced_file_among_the_held`
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_omits_the_not_listed_keys_under_the_bound`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
    option = ctx.gate.require(spec, digest=plan["digest"], context=_shown(plan, root=root))
```

New text:

```
    option = ctx.gate.require(spec, digest=plan["digest"])
```

### `r669.G12_shown_count_is_every_item`

Show the item count as the rename count, so the screen overstates what will move

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G12_shown_count_is_every_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_lists_no_more_than_the_bound_and_counts_the_rest`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
        "renames": plan["totals"]["count"],
```

New text:

```
        "renames": len(items),
```

### `r669.G13_referenced_held_without_a_reason`

Carry an empty reason on a referenced item

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G13_referenced_held_without_a_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_names_a_referenced_file_among_the_held`

Old text:

```
REFERENCED_WHY = "the rekordbox collection references it"
```

New text:

```
REFERENCED_WHY = ""
```

### `r669.G17_held_file_never_referenced`

Mark every uncomposed file unnamed without asking the collection, the review's first finding

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G17_held_file_never_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed`

Old text:

```
    for path, why in uncomposed:
        if _is_referenced(path, referenced):
```

New text:

```
    for path, why in uncomposed:
        if False:
```

### `r669.G18_drifted_name_renamed_anyway`

Rename to whatever the tags render after the gate, the review's second finding

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G18_drifted_name_renamed_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`

Old text:

```
        if rendered.filename != item["to"]:
```

New text:

```
        if False:
```

### `r669.G19_no_step_for_unnamed`

Leave the unnamed step out of the report, so the remedy is to run it again

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G19_no_step_for_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    if unnamed:
        steps.append(
```

New text:

```
    if False:
        steps.append(
```

### `r669.G1_identifier_is_no_letters`

Widen the identifier test from digits only to no letters, the first draft's rule the review sent back

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G1_identifier_is_no_letters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is`

Old text:

```
    return stem.strip().isdigit()
```

New text:

```
    return not any(ch.isalpha() for ch in stem)
```

### `r669.G20_screen_uncapped`

List every planned rename on the gate screen with no bound

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G20_screen_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_lists_no_more_than_the_bound_and_counts_the_rest`

Old text:

```
        "planned": planned[:PLAN_SHOWN],
```

New text:

```
        "planned": planned,
```

### `r669.G21_artist_alone_when_no_title_tag`

An identifier with an artist and no title tag at all is renamed to its artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G21_artist_alone_when_no_title_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[an-artist-and-no-title]`

Old text:

```
    if not tagged_title:
        return None, (
            "its name is an identifier and it carries no title tag, so it is not "
            "renamed to its artist alone"
        )
```

New text:

```
    if not tagged_title:
        return artist, None
```

### `r669.G2_title_alone_when_no_artist`

An identifier with no artist tag is renamed to its title alone instead of held

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G2_title_alone_when_no_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    if not artist:
        return None, (
            "its name is an identifier and it carries no artist tag, so it is not "
            "renamed to its title alone"
        )
```

New text:

```
    if not artist:
        return title, None
```

### `r669.G3_artist_alone_when_title_is_a_head`

An identifier whose title is only a head is renamed to its artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G3_artist_alone_when_title_is_a_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`

Old text:

```
    if not title:
        return None, (
            "its name is an identifier and its title tag is only a head, empty once "
            "the head is removed, so no name can be composed for it"
        )
```

New text:

```
    if not title:
        return artist, None
```

### `r669.G4_order_swapped`

Compose Title - Artist, the other library grammar, instead of the declared Artist - Title

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G4_order_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-camelot-key-without-a-tempo-renders-no-head]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-slash-takes-the-body-form-of-a-segment]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_is_composed_from_the_artist_and_title_tags`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[an-empty-value-leads-with-no-comma]`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[every-credited-artist]`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
    return naming.compose_body(artist, title, sep=template.segment_sep), None
```

New text:

```
    return naming.compose_body(title, artist, sep=template.segment_sep), None
```

### `r669.G5_first_artist_only`

Read the artist through the single value reader, so a multi valued credit names the file for the first artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G5_first_artist_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[an-empty-value-leads-with-no-comma]`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[every-credited-artist]`

Old text:

```
    values = tags.read_tag_values(path, "artist")
    if not values:
        return None
```

New text:

```
    values = [tags.read_tag(path, "artist") or ""]
    if not values:
        return None
```

### `r669.G6_title_head_kept_in_body`

Compose from the title tag verbatim, so a head the live system wrote into the tag lands inside the body

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G6_title_head_kept_in_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`

Old text:

```
    title = naming.strip_head(tagged_title, template=template).strip() if tagged_title else ""
```

New text:

```
    title = tagged_title.strip() if tagged_title else ""
```

### `r669.G7_unnamed_left_out_of_the_plan`

Drop the held identifier files from the plan's items, so the plan omits them silently

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G7_unnamed_left_out_of_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 9 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[an-artist-and-no-title]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[no-tags-at-all]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan`
  - `tests/test_naming_apply_cli.py::test_the_digest_covers_a_held_identifier_file`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    items.extend(unnamed)
    return {
```

New text:

```
    return {
```

### `r669.G8_digest_ignores_unnamed`

Compute the digest over everything but the held identifier files, so a held file is not part of what was approved

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G8_digest_ignores_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_digest_covers_a_held_identifier_file`

Old text:

```
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides) - len(unnamed),
```

New text:

```
        "digest": digest_of(
            {"kind": "rename", "items": [i for i in items if i["action"] != UNNAMED]}
        ),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides) - len(unnamed),
```

### `r669.G9_unnamed_not_owed_on_apply`

Owe only collisions on apply, so a sweep over a held identifier file answers ok

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G9_unnamed_not_owed_on_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
        if item["action"] in (COLLIDES, UNNAMED)
    ]
```

New text:

```
        if item["action"] == COLLIDES
    ]
```

### `r675.E2_key_not_casefolded`

existing layer: the referenced key keeps case, so a row differing from the file only in case no longer protects it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `E2_key_not_casefolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-case-variant]`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `r675.E4_tombstones_dropped_from_the_read`

existing layer: _recorded reads live rows only, so a tombstone neither protects its file nor counts as dark

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `E4_tombstones_dropped_from_the_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-tombstoned-row]`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
            return tuple(str(row.FolderPath or "") for row in handle.get_content())
```

New text:

```
            return tuple(
                str(row.FolderPath or "")
                for row in handle.get_content()
                if not row.rb_local_deleted
            )
```

### `r675.G11_prefixes_dropped`

_unmapped_refusal: the grouped prefixes left out of the detail

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G11_prefixes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": [],
```

### `r675.G12_could_name_uncapped`

_unmapped_refusal: the pairs list uncapped, so a fresh setup's 9937 dark rows are 9937 pairs in one envelope

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G12_could_name_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
```

New text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark],
```

### `r675.G13_as_recorded_key_dropped`

_referenced: a row's as recorded key is not added, so a row outside every rule whose file exists no longer protects it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G13_as_recorded_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`

Old text:

```
        keys.add(_key(decoded))
        if resolved.path is not None:
```

New text:

```
        if resolved.path is not None:
```

### `r675.G14_remapped_key_dropped`

_referenced: a row's remapped key is not added, so a row under a mapped old volume name no longer protects its file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G14_remapped_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`

Old text:

```
        if resolved.path is not None:
            keys.add(_key(resolved.path))
        elif
```

New text:

```
        if resolved.path is not None:
            pass
        elif
```

### `r675.G15_first_location_dropped`

_unmapped_refusal: the first dark location no longer quoted in the message

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G15_first_location_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`

Old text:

```
        f"of a file this plan would rename, the first of them {dark[0][0]}, so "
```

New text:

```
        f"of a file this plan would rename, so "
```

### `r675.G16_locations_uncapped`

_unmapped_refusal: the locations list uncapped

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G16_locations_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_locations": locations_listed[:20],
```

New text:

```
            "unmapped_locations": locations_listed,
```

### `r675.G17_prefixes_uncapped`

_unmapped_refusal: the prefixes list uncapped

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G17_prefixes_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": prefixes,
```

### `r675.G18_held_candidates_asked_about`

_referenced: a candidate the resolved rows hold is still indexed, so a dark row under its name refuses although the file is never renamed

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G18_held_candidates_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`

Old text:

```
        if not _is_referenced(path, referenced):
            leaves.setdefault(_key(path.name), []).append(str(path))
```

New text:

```
        leaves.setdefault(_key(path.name), []).append(str(path))
```

### `r675.G19_second_step_dropped`

_unmapped_refusal: the step for a row no rule can place is left out, so a person with no volume to map is told to map one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G19_second_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
            "when no volume is missing, the row names a file that is gone and no "
            "rule can place it: rename the file it could be naming by hand, or "
            "remove that track in rekordbox, then run this again",
        ),
```

New text:

```
        ),
```

### `r675.G1_every_dark_row_refuses`

_referenced: the leaf test dropped, so every dark row refuses, which is the behaviour R-675 measured at 582 rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G1_every_dark_row_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_another_name_lets_the_repair_run`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-dark-tombstone-under-another-name-R-524]`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-streamed-catalogue-path]`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(Path(decoded).name)) or [decoded])
```

### `r675.G2_row_leaf_not_keyed`

_referenced: the dark row's leaf is looked up as spelled, so a case or composition variant of a candidate's name is another name

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G2_row_leaf_not_keyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(Path(decoded).name))
```

### `r675.G3_candidate_leaf_not_keyed`

_referenced: the candidates are indexed by their name as spelled, so a keyed lookup never finds one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G3_candidate_leaf_not_keyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        leaves.setdefault(_key(path.name), []).append(str(path))
```

New text:

```
        leaves.setdefault(path.name, []).append(str(path))
```

### `r675.G4_could_name_empty`

_referenced: the candidates in doubt are never collected, so the refusal names rows and no files

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G4_could_name_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
```

New text:

```
            "could_name": [{"row": decoded, "files": []} for decoded, named in dark[:20]],
```

### `r675.G5_leaf_compared_as_whole_path`

_referenced: the dark row is looked up by its whole decoded path rather than its leaf, so no row under another volume ever matches

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G5_leaf_compared_as_whole_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 16 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(decoded)))
```

### `r675.G6_plan_asks_with_no_candidates`

_plan_for: the plan's read hands the guard no candidates, so the plan never refuses and only the apply's read can

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G6_plan_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`

Old text:

```
        _referenced(_recorded(cfg), cfg=cfg, renaming=[path for path, _ in candidates])
```

New text:

```
        _referenced(_recorded(cfg), cfg=cfg, renaming=[])
```

### `r675.G7_apply_asks_with_no_candidates`

name_apply: the read after the gate hands the guard no candidates, so a row that went dark while the gate waited is not seen

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G7_apply_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`

Old text:

```
            _recorded(cfg), cfg=cfg, renaming=[Path(item["path"]) for item in renames]
```

New text:

```
            _recorded(cfg), cfg=cfg, renaming=[]
```

### `r675.G8_count_reworded`

_unmapped_refusal: the count's noun reworded, so the message no longer says what was counted

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G8_count_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
    rows = "collection row records" if count == 1 else "collection rows record"
```

New text:

```
    rows = "row records" if count == 1 else "rows record"
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

### `u212.N1_second_copy_compare`

naming_cli.second_copy: two different ISRCs read as one recording

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N1_second_copy_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_another_recording_keeps_the_plain_collision`

Old text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) == mine else ""
```

New text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) != "" else ""
```

### `u212.N3_taken_plain`

naming_cli._taken: always the plain collision, never a second copy

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N3_taken_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    same = second_copy(path, target)
    if same:
```

New text:

```
    same = second_copy(path, target)
    if False:
```

### `u212.N4_plan_isrc`

naming_cli._plan_for: the plan item carries no ISRC

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N4_plan_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
            if str(path) in seconds:
                item["isrc"] = seconds[str(path)]
```

New text:

```
(empty)
```

### `u212.N5_claim_plain`

naming_cli.name_apply: a name taken after the plan is always the plain collision, round one's F8

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N5_claim_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`, `tests/test_repair_rows.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`

Old text:

```
                why, same = _taken(
                    path, target, fallback=f"{rendered.filename} is already taken in the folder"
                )
```

New text:

```
                why, same = f"{rendered.filename} is already taken in the folder", ""
```

### `u212.N6_cause_step`

naming_cli._incomplete_cause: the second copy step is never added

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N6_cause_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    if any(item.get("isrc") for item in incomplete):
```

New text:

```
    if False:
```

### `u39-author-full.R1_filename_source_dropped`

Head recovery loses the filename source and keeps only the title fallback

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R1_filename_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-filename-head-wins-over-the-title-head]`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(title, template=template)
        or {}
    )

```

### `u39-author-full.R2_title_fallback_dropped`

Head recovery loses the title fallback that heals the tag then rename crash window

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R2_title_fallback_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-head-is-recovered-from-the-title-tag]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or {}
    )

```

### `u39-author-full.R3_bpm_dropped`

The recovered tempo is discarded, reproducing the head destroying defect

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R3_bpm_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 29 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_a_sweep_that_carried_out_every_rename_still_answers_ok`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - ... and 14 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=None,

```

### `u39-author-full.R4_head_key_overrules_tag`

The stale head key wins over a corrected initialkey tag

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R4_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or tag_key

```

### `u39-author-full.R5_junk_tag_admitted`

A non Camelot initialkey tag reaches the renderer instead of being ignored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R5_junk_tag_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-key-tag-not-camelot-is-ignored]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = tag_key if tag_key else head.get("key")

```

### `u39-author-full.R6_lossy_flag_dropped`

The shared spec loses the lossy flag, recreating the plan and apply disagreement

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R6_lossy_flag_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marked-plan-agrees-with-apply]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=False,

```

### `u39-naming-independent.R5_bpm_wrong_type`

The recovered tempo is coerced to float instead of int

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-naming-independent.json`, row `R5_bpm_wrong_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 71 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_database_with_no_matching_row_proceeds`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - ... and 56 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=float(head["bpm"]) if "bpm" in head else None,

```

### `u41-author-full.R1_filename_head_source_dropped`

The filename is no longer a head source, leaving the title as the only one

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R1_filename_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-filename-head-wins-over-the-title-head]`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)

```

### `u41-author-full.R6_head_key_overrules_tag`

Key precedence reversed, so a corrected key tag can no longer move a file

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R6_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or (tag_key if tag_key and naming.is_camelot(tag_key) else None)

```

### `u41-author-full.T1_title_tag_fed_the_filename_body`

The title tag is rebuilt from the filename body, which stuffs the artist and the album into every tag the apply pass rewrites

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T1_title_tag_fed_the_filename_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=naming.strip_head(path.stem, template=template),

```

### `u41-author-full.T2_title_field_dropped`

The spec stops carrying a title at all, so render_all falls back to the stem for the tag surface

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T2_title_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=None,

```

### `u41-naming-independent.B1_head_precedence_swapped`

The title's head is parsed before the filename's, so a stale tag head drags a correct filename backwards

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B1_head_precedence_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-filename-head-wins-over-the-title-head]`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)

```

### `u41-naming-independent.B2_filename_head_source_dropped`

The filename is no longer a head source, so only a tag-carried head is recovered

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B2_filename_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-filename-head-wins-over-the-title-head]`

Old text:

```
        naming.parse_head(path.name, template=template)

```

New text:

```
        None

```

### `u41-naming-independent.B3_title_head_source_dropped`

The title is no longer a head source, so the tag-then-rename crash window stops healing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B3_title_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-head-is-recovered-from-the-title-tag]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`

Old text:

```
        or naming.parse_head(title, template=template)

```

New text:

```
        or None

```

### `u41-naming-independent.B7_lossy_filename_operand_dropped`

U39's K2: the lossy OR loses its filename operand, so a file marked only in its name is renamed to its unmarked form

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B7_lossy_filename_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in title,

```

### `u41-naming-independent.B8_lossy_title_operand_dropped`

U39's K1: the lossy OR loses its title operand, so a marker surviving only in the tag stops being restored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B8_lossy_title_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in path.stem,

```

### `u41-naming-independent.C1_plan_no_op_filter_dropped`

Every audio file enters the plan, including the ones already in convention

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `C1_plan_no_op_filter_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 14 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[13A-is-no-head]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marked-plan-agrees-with-apply]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`
  - `tests/test_naming_apply_cli.py::test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[an-unpadded-head-is-padded-with-the-tempo-intact]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[no-title-tag-takes-the-body-from-the-filename]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-head-is-recovered-from-the-title-tag]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
            if rendered.filename != path.name:

```

New text:

```
            if True:

```

### `u67-round-2.C1_action_filter_and_recheck`

Composite: apply every plan item AND drop the re-check before the rename

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67-round-2.json`, row `C1_action_filter_and_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 19 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-case-variant]`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-tombstoned-row]`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[recorded-as-a-location-url]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    renames = [item for item in plan["items"] if item["action"] == RENAME]
```

New text:

```
    renames = list(plan["items"])
    _is_referenced = lambda path, referenced: False  # noqa: E731
```

### `u67.M2_nfc`

Skip NFC normalisation of the compared path

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M2_nfc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return path.casefold()
```

### `u67.M3_prefix_resolution`

Drop the prefix mapped spelling of a row

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M3_prefix_resolution`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`

Old text:

```
        if resolved.path is not None:
            keys.add(_key(resolved.path))
```

New text:

```
        if False:
            keys.add(_key(resolved.path))
```

### `u67.M6_remote_host_skip`

Let a row naming another host raise instead of being skipped

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M6_remote_host_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-row-naming-another-host]`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except ZeroDivisionError:
            continue
```

### `u67.M7_absolute_spelling`

Ask only the resolved spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M7_absolute_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.resolve())) in referenced
```

### `u67.M8_resolved_spelling`

Ask only the absolute spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M8_resolved_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.absolute())) in referenced
```

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

### `u130-c.C5_no_renumber`

Leave rekordbox's order as the adds and removals left it

- File: `src/cratekit/write/playlist_pair.py`
- Source: `u130-c.json`, row `C5_no_renumber`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`

Old text:

```
            moved = renumber(db, change.playlist_id, change.order)
```

New text:

```
            moved = 0
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 436 against a baseline of 436
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_reaching_only_soft_deleted_rows_is_withdrawn`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P2_withdrawn_on_single_tombstone_only`

row_placement: withdrawn only when exactly one tombstone claims the location, two tombstones read as not imported

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P2_withdrawn_on_single_tombstone_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 436 against a baseline of 436
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED,):
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P3_unresolved_branch_removed`

row_placement: drop the unresolved answer, so a location no prefix maps falls through to not imported, a configuration failure reported as a missing import

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P3_unresolved_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 436 against a baseline of 436
- Kills: 2 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_run_whose_locations_all_resolve_to_nothing_is_not_told_to_import`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[unresolved]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED

```

New text:

```
(empty)
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 436 against a baseline of 436
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_active_rows_on_one_location_are_ambiguous_and_never_written`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[ambiguous]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 885 against a baseline of 885
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

### `r923.N14_verb_writes_on_abort`

The verb proceeds to write whatever the gate answered

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N14_verb_writes_on_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 7 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_an_abort_writes_nothing`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`
  - `tests/test_repair_rows.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if False:
```

### `r923.N15_verb_writes_empty_plan`

An empty plan opens the database to write instead of ending as a no op

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N15_verb_writes_empty_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`

Old text:

```
    if not plan.items:
```

New text:

```
    if False:
```

### `r923.N16_ack_not_read`

The verb no longer reads the backup acknowledgment before the plan and the gate

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N16_ack_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r923.N17_write_handle_not_closed`

The write handle no longer requires rekordbox closed at open

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N17_write_handle_not_closed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u115.F18_undecidable_unsaid`

The gate and the envelope say nothing when the volume's counter has passed the binding's range

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F18_undecidable_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`

Old text:

```
    if plan.undecidable:
        notes.append(_undecidable(plan))
```

New text:

```
    if False:
        notes.append(_undecidable(plan))
```

### `u115.F19_unrenumbered_unsaid`

The envelope says nothing about the rows left with a random id because their file could not be read

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F19_unrenumbered_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if plan.unrenumbered:
        notes.append(_unrenumbered(plan))
```

New text:

```
    if False:
        notes.append(_unrenumbered(plan))
```

### `a32.C1_ack_after_gate`

The backup acknowledgment is not read before the gate

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C1_ack_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, ctx.args)
```

New text:

```
    plan = _plan(cfg, ctx.args)
```

### `a32.C2_abort_writes`

An abort at the gate proceeds to the write

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C2_abort_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_an_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) not in ("apply", "abort"):
```

### `a32.C3_nothing_to_write_applies`

A plan that writes nothing reaches the apply

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C3_nothing_to_write_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`

Old text:

```
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

New text:

```
    if False:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

### `a32.C4_read_back_unasserted`

The verb answers OK without asserting the read back

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C4_read_back_unasserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`

Old text:

```
    row_link.assert_read_back(written)
    data["totals"] = {
```

New text:

```
    data["totals"] = {
```

