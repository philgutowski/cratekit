# Mutation table: u325-after-h-05

Measured by `scripts/mutate.py` on 2026-11-23 02:43 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 47.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 20, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2759 | 173 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 20 file(s) | 2697 | 7 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session.py` | user | 11 file(s) | 1555 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session.py` | user | 11 file(s) | 1555 | 2 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session.py` | user | 13 file(s) | 2589 | 1 | killed |
| `u109-b.B5_refusal_reason` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1079 | 2 | killed |
| `u109-b.B9_queue_again` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1079 | 2 | killed |
| `u181.S1_profile_off_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1068 | 1 | killed |
| `u181.S2_gate_never_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1068 | 6 | killed |
| `u40-author-full.C1_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 1067 | 1 | killed |
| `u40-author-full.C2_no_gate_no_refusal` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 1067 | 1 | killed |
| `u111-d.D1_empty_plan_asks` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 1038 | 4 | killed |
| `u111-d.D2_ack_before_gate` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 1038 | 1 | killed |
| `u180.M23_in_order_asks_nothing` | `src/cratekit/favorites/order_cli.py` | user | 2 file(s) | 1027 | 4 | killed |
| `u180.M24_backup_acknowledged_first` | `src/cratekit/favorites/order_cli.py` | user | 2 file(s) | 1027 | 1 | killed |
| `u170.C1_validation_unwired` | `src/cratekit/core/config.py` | user | 5 file(s) | 1704 | 6 | killed |
| `r313.G7_handler_opens_with_write_intent` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 1611 | 1 | killed |
| `u97-b.B3_label_path_raises_the_other_token` | `src/cratekit/label/catalogue.py` | user | 3 file(s) | 1588 | 1 | killed |
| `u27-restore-cli-round-2.G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 1095 | 1 | killed |
| `u292.M16_outcome_over_unread` | `src/cratekit/tagging/backlog_cli.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u294.M19_ack_skipped` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 2 file(s) | 1053 | 1 | killed |
| `u176.V1_auth_failed_reason` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 1043 | 5 | killed |
| `r500-c.G14_located_skips_the_decode` | `src/cratekit/write/trees.py` | user | 10 file(s) | 1031 | 16 | killed |
| `u27-adopt-apply-author.A2_gate_found_by_position` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 1024 | 1 | killed |
| `u219.M2_disposition_cleared` | `src/cratekit/core/convergence.py` | user | 16 file(s) | 1014 | 1 | killed |
| `r431-b.B6_the_verb_calls_a_companion_stale` | `src/cratekit/acquire/match_cli.py` | user | 7 file(s) | 1005 | 1 | killed |

## Row definitions

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2759 against a baseline of 2759
- Kills: 173 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_identifier_is_stringified_because_the_column_need_not_be_text`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - ... and 158 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `r787.S1_set_drops_intake`

cutover_trees returns the routing tree alone, the list doctor held before R-787

- File: `src/cratekit/core/tree_registry.py`
- Source: `r787.json`, row `S1_set_drops_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_import_coexistence.py`, `tests/test_xml_splice_golden.py`
- Collected: 2697 against a baseline of 2697
- Kills: 7 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`
  - `tests/test_cutover_cli.py::test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree`

Old text:

```
    return frozenset({declared.tree.id, declared.intake.id})
```

New text:

```
    return frozenset({declared.tree.id})
```

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1555 against a baseline of 1555
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `u48-author.S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session.py`
- Source: `u48-author.json`, row `S2_remedy_fixed_at_grant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1555 against a baseline of 1555
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2589 against a baseline of 2589
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    try:
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    if True:
        return Holder.from_json(data["holder"])
    if False:
```

### `u109-b.B5_refusal_reason`

Refuse with the old empty registry slug instead of verb-retired

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B5_refusal_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1079 against a baseline of 1079
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_retired_refusal_reads_nothing_so_a_fresh_install_gets_it_too`

Old text:

```
    raise refuse(
        "verb-retired",
```

New text:

```
    raise refuse(
        "label-registry-empty",
```

### `u109-b.B9_queue_again`

The retired verb queues a sweep again: the refusal is replaced by a legacy enqueue over the registry

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B9_queue_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1079 against a baseline of 1079
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refused_sweep_carries_no_warning_because_nothing_was_queued`
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise refuse(
        "verb-retired",
```

New text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    held = labels.RegistryStore().load()
    if held.labels:
        return _queue(
            ctx,
            payload={"source_id": "labels", "run_id": ctx.run.run_id},
            item_ids=tuple(entry.label_id for entry in held.labels.values()),
        )
    raise refuse(
        "verb-retired",
```

### `u181.S1_profile_off_asked`

sync land _vocals: ask the model on a profile with the vocals module off

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S1_profile_off_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`

Old text:

```
    if not tail.vocals_on(cfg):
        report.summary["vocal_scoring"] = "off"
```

New text:

```
    if False:
        report.summary["vocal_scoring"] = "off"
```

### `u181.S2_gate_never_asked`

sync land _vocals: never stop at the gate, so a pass lands rows with no score unasked

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S2_gate_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 6 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.land]`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_cannot_score_stops_at_its_gate_before_queueing_anything`
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_gate_recorded_by_a_separate_act_continues_the_same_run`

Old text:

```
    unable = tail.vocals_unavailable()
    if unable is None:
```

New text:

```
    unable = tail.vocals_unavailable()
    if True:
```

### `u40-author-full.C1_gate_by_position`

Take gates[0] rather than the gate declared against the plan, so a reordered tuple answers the wrong question

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C1_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 1067 against a baseline of 1067
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates:
        return spec
```

### `u40-author-full.C2_no_gate_no_refusal`

Return None instead of refusing when the entry declares no plan gate, so a destructive sweep runs unconfirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C2_no_gate_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 1067 against a baseline of 1067
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_refuses_when_its_entry_declares_no_plan_gate`

Old text:

```
    raise refuse(
        "refused-by-policy",
        "this verb is destructive and its registry entry declares no decision "
        "made against the plan, so there is nothing for a person to confirm",
        remedy=Remedy.REPORT_DEFECT,
        origin=("tagging", "retag_cli"),
        detail={"verb": ctx.entry.name},
    )
```

New text:

```
    return None
```

### `u111-d.D1_empty_plan_asks`

A plan that moves and removes nothing returns without asking the gate

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u111-d.json`, row `D1_empty_plan_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_cli_contract.py`
- Collected: 1038 against a baseline of 1038
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[inbox.rotate]`
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_an_empty_inbox_still_asks_and_creates_no_old`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
```

New text:

```
    if plan.writes and ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
```

### `u111-d.D2_ack_before_gate`

The backup acknowledgment is no longer read before the plan and the gate

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u111-d.json`, row `D2_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_cli_contract.py`
- Collected: 1038 against a baseline of 1038
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    pass
```

### `u180.M23_in_order_asks_nothing`

favorites_order: a folder already in order opens the gate rather than ending NO_OP

- File: `src/cratekit/favorites/order_cli.py`
- Source: `u180.json`, row `M23_in_order_asks_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_cli_contract.py`
- Collected: 1027 against a baseline of 1027
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[favorites.order]`
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u180.M24_backup_acknowledged_first`

favorites_order: the backup acknowledgment is not read before the plan and the gate

- File: `src/cratekit/favorites/order_cli.py`
- Source: `u180.json`, row `M24_backup_acknowledged_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_cli_contract.py`
- Collected: 1027 against a baseline of 1027
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u170.C1_validation_unwired`

validate: do not check reports.open_gate_stale_days

- File: `src/cratekit/core/config.py`
- Source: `u170.json`, row `C1_validation_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 6 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[-1]`
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[0]`
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[3651]`
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[7.5]`
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[7]`
  - `tests/test_run_retire.py::test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named[True]`

Old text:

```
    problems += _validate_open_gate_staleness(data)

```

New text:

```
(empty)
```

### `r313.G7_handler_opens_with_write_intent`

the unplaced report opens the database with require_closed, so it refuses with rekordbox open

- File: `src/cratekit/write/routing_cli.py`
- Source: `r313.json`, row `G7_handler_opens_with_write_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1611 against a baseline of 1611
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_reports_with_rekordbox_open_and_writes_nothing`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg, require_closed=True)

```

### `u97-b.B3_label_path_raises_the_other_token`

catalogue.resolve: refuse a missing session with REAUTHENTICATE_PROVIDER, so a person who never had one is told theirs was rejected

- File: `src/cratekit/label/catalogue.py`
- Source: `u97-b.json`, row `B3_label_path_raises_the_other_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
```

New text:

```
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
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

### `u292.M16_outcome_over_unread`

the verb: a backlog of unread rows alone ends no_op, round one's clean report

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u292.json`, row `M16_outcome_over_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_rows_whose_file_is_not_here_are_counted_and_said`

Old text:

```
        outcome=Outcome.OK if plan.rows or plan.unread or plan.joining else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if plan.rows else Outcome.NO_OP,
```

### `u294.M19_ack_skipped`

the backup acknowledgment is not read before the plan and the gate

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M19_ack_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_cli_contract.py`
- Collected: 1053 against a baseline of 1053
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    args = ctx.args
```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).

    args = ctx.args
```

### `u176.V1_auth_failed_reason`

_auth_failed: a missing or refused session is credential-missing, a precondition, rather than auth-failed

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V1_auth_failed_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`, `tests/test_cli_contract.py`
- Collected: 1043 against a baseline of 1043
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_listing_the_session_is_refused_at_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_a_session_removed_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_an_expired_session_is_auth_failed_naming_the_login_step`
  - `tests/test_bandcamp_cli.py::test_no_recorded_session_is_auth_failed_before_any_request`

Old text:

```
        "auth-failed",
        f"{message}, so the account's purchases could not be read",
```

New text:

```
        "credential-missing",
        f"{message}, so the account's purchases could not be read",
```

### `r500-c.G14_located_skips_the_decode`

trees.located resolves the raw recorded value without decoding it, the shared locate step both writers and this verb now call

- File: `src/cratekit/write/trees.py`
- Source: `r500-c.json`, row `G14_located_skips_the_decode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 1031 against a baseline of 1031
- Kills: 16 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_adopt_workers.py::test_a_renamed_vocal_playlist_gains_no_second_one_beside_it`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_a_track_in_the_planned_sub_under_another_name_is_withheld_not_doubled`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`
  - `tests/test_adopt_workers.py::test_the_approving_actor_travels_in_the_payload`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`
  - `tests/test_adopt_workers.py::test_the_membership_write_needs_locations_and_not_content_identifiers`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    decoded = locations.location_to_path(str(recorded))
    return decoded,
```

New text:

```
    decoded = str(recorded)
    return decoded,
```

### `u27-adopt-apply-author.A2_gate_found_by_position`

Take the first declared gate rather than the one digested against the plan

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A2_gate_found_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 1024 against a baseline of 1024
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`

Old text:

```
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
```

New text:

```
    for spec in entry.gates:
        if True:
            return spec
```

### `u219.M2_disposition_cleared`

mark_unconverged: a second restore of the same reason leaves a disposed tree's acceptance standing (round two's second hold)

- File: `src/cratekit/core/convergence.py`
- Source: `u219.json`, row `M2_disposition_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`
- Collected: 1014 against a baseline of 1014
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`

Old text:

```
            if current.unconverged and current.reason == reason and current.disposition is None:
```

New text:

```
            if current.unconverged and current.reason == reason:
```

### `r431-b.B6_the_verb_calls_a_companion_stale`

The verb's report over a matched row asks for companions, so a held file crediting somebody else calls one stale

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r431-b.json`, row `B6_the_verb_calls_a_companion_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1005 against a baseline of 1005
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
                companions=not held,
```

New text:

```
                companions=True,
```

