# Mutation table: u325-before-h-03

Measured by `scripts/mutate.py` on 2026-11-22 22:31 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 29.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:21 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 11, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u231.M5_positions_not_advanced` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 38 | killed |
| `u231.M6_settle_lag_taken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 4 | killed |
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
| `r313.G7_handler_opens_with_write_intent` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 1611 | 1 | killed |
| `u97-b.B3_label_path_raises_the_other_token` | `src/cratekit/label/catalogue.py` | user | 3 file(s) | 1588 | 1 | killed |
| `u27-restore-cli-round-2.G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 1095 | 1 | killed |
| `u292.M16_outcome_over_unread` | `src/cratekit/tagging/backlog_cli.py` | user | 2 file(s) | 1059 | 1 | killed |
| `r500-c.G14_located_skips_the_decode` | `src/cratekit/write/trees.py` | user | 10 file(s) | 1031 | 16 | killed |

## Row definitions

### `u231.M5_positions_not_advanced`

adapter order: each move's position is read off the reading as it was, not with the moves before it applied

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M5_positions_not_advanced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 38 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_a_reading_that_agrees_with_the_expected_one_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            now = _fronted(now, one)
            note["moved"] += 1
```

New text:

```
            note["moved"] += 1
```

### `u231.M6_settle_lag_taken`

adapter settle: a reading whose window lags is answered as the order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M6_settle_lag_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
        if window == listing.WINDOW_LAGS:
            note["window_lagged"] += 1
            note["outcome"] = "lags"
            return None
```

New text:

```
        if False:
            return None
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

