# Mutation table: u27-adopt-apply-author

Measured by `scripts/mutate.py` on 2026-08-23 18:06 UTC, branch `unit/u27-adopt-apply-cli` at `2be8a66`. Pass kind: full.

Baseline: green, 6147 collected. pytest invocations for this batch: 34.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6147 against 6147. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S1_no_session_at_all` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 19 | 5 | killed |
| `S2_analysis_watch_watches_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `S3_watched_root_is_narrower_than_the_library` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 6147 | 0 (promoted) | zero |
| `S4_workflow_is_not_the_verb` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 19 | 1 | killed |
| `C1_collector_writes_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `C2_collector_records_the_wrong_identifier` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `C3_collector_drops_the_sub_playlist` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `A1_approval_actor_is_the_process` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 634 | 1 | killed |
| `A2_gate_found_by_position` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 1 | killed |
| `A3_missing_gate_refuses_under_the_wrong_reason` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 19 | 1 | killed |
| `G1_abort_branch_inverted` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 2 | killed |
| `G2_abort_queues_anyway` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 1 | killed |
| `G3_gate_offers_no_digest` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6147 | 0 (promoted) | zero |
| `G4_queued_payload_loses_the_digest` | `src/cratekit/adopt/apply_cli.py` | maintainer | 2 file(s) | 535 | 1 | killed |
| `G5_resume_does_not_reconcile` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6147 | 0 (promoted) | zero |
| `V1_resume_forgets_the_job` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 1 | killed |
| `V2_resume_names_the_sibling_verb` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 1 | killed |
| `P1_tree_is_a_literal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 1 | killed |
| `P2_census_returns_a_row` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 535 | 6 | killed |
| `R1_marker_restored` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1138 | collection error | collect-error |
| `R2_register_entry_restored` | `tests/_pending.py` | user | 2 file(s) | 624 | 2 | killed |

## Zero rows and what they owe

- `S3_watched_root_is_narrower_than_the_library` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `G3_gate_offers_no_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `G5_resume_does_not_reconcile` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `S1_no_session_at_all`

Run the apply loop with no destructive session around it (the residual's condition, unchanged)

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_a_volume_whose_identity_moved_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_an_unacknowledged_machine_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
    with session.assert_gates(
        cfg,
        workflow=WORKFLOW,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ):
```

New text:

```
    if True:
```

### `S2_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_write_session.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `S3_watched_root_is_narrower_than_the_library`

Watch only the Music folder, so a tag write outside it is unwatched

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 6147 against a baseline of 6147
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    watched: tuple[Path, ...] = (cfg.library.root,)
```

New text:

```
    watched: tuple[Path, ...] = (cfg.library.root / "Music",)
```

### `S4_workflow_is_not_the_verb`

Record the session under a name that is not this verb's

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`

Old text:

```
WORKFLOW = "adopt.apply"
```

New text:

```
WORKFLOW = "adoption"
```

### `C1_collector_writes_nothing`

Place collects nothing, so the ledger marks entries applied with no membership recorded

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`

Old text:

```
        into.setdefault((folder, sub), []).append(entry.content_id)
```

New text:

```
        _ = (into, entry, folder, sub)
```

### `C2_collector_records_the_wrong_identifier`

Collect the plan entry id instead of the content id the tree writer matches on

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`

Old text:

```
        into.setdefault((folder, sub), []).append(entry.content_id)
```

New text:

```
        into.setdefault((folder, sub), []).append(entry.entry_id)
```

### `C3_collector_drops_the_sub_playlist`

Group by folder alone, so every energy band collapses into one destination

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`

Old text:

```
        into.setdefault((folder, sub), []).append(entry.content_id)
```

New text:

```
        into.setdefault((folder, ""), []).append(entry.content_id)
```

### `A1_approval_actor_is_the_process`

Mint the approval under a fixed actor, so the record cannot say who asserted it

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`
- Collected: 634 against a baseline of 634
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_names_whoever_answered_the_gate`

Old text:

```
            approval=grant(plan, actor=actor),
```

New text:

```
            approval=grant(plan, actor="cli"),
```

### `A2_gate_found_by_position`

Take the first declared gate rather than the one digested against the plan

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 535 against a baseline of 535
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

### `A3_missing_gate_refuses_under_the_wrong_reason`

Report a verb declaring no approval gate as a configuration problem

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_verb_declaring_no_plan_digested_gate_refuses_rather_than_applying`

Old text:

```
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
```

New text:

```
            reason="config-unusable",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
```

### `G1_abort_branch_inverted`

Treat an approval as a decline and a decline as an approval

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adopt_apply_cli.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`

Old text:

```
    if option == "abort":
        return ctx.envelope(
```

New text:

```
    if option == "approve":
        return ctx.envelope(
```

### `G2_abort_queues_anyway`

Queue the pass even when the person declined it

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adopt_apply_cli.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`

Old text:

```
    if option == "abort":
        return ctx.envelope(
            data={"job_id": None, "state": "declined", "cause": None, "progress": {}},
            outcome=Outcome.NO_OP,
        )
```

New text:

```
    if option == "abort":
        pass
```

### `G3_gate_offers_no_digest`

Ask the approval gate with no digest, so an approval survives the plan moving

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adopt_apply_cli.py`
- Collected: 6147 against a baseline of 6147
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    option = ctx.gate.require(spec, digest=plan.digest())
```

New text:

```
    option = ctx.gate.require(spec)
```

### `G4_queued_payload_loses_the_digest`

Freeze the job without the digest the plan was approved against

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adopt_apply_cli.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`

Old text:

```
            payload={"tree": plan.tree, "digest": plan.digest()},
```

New text:

```
            payload={"tree": plan.tree},
```

### `G5_resume_does_not_reconcile`

Report the stored job without reconciling a claim a dead driver left behind

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_jobs.py`
- Collected: 6147 against a baseline of 6147
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

New text:

```
            return ctx.envelope(data=_reported(store, jobs.get(store, ctx.args.job)))
```

### `V1_resume_forgets_the_job`

Return a command line that queues a second record instead of continuing the one queued

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_resume_names_the_job_rather_than_restating_the_request`

Old text:

```
    return ["adopt", "apply", "--job", job.job_id]
```

New text:

```
    return ["adopt", "apply"]
```

### `V2_resume_names_the_sibling_verb`

Re-invoke the census instead of the apply

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_resume_names_the_job_rather_than_restating_the_request`

Old text:

```
    return ["adopt", "apply", "--job", job.job_id]
```

New text:

```
    return ["adopt", "scan", "--job", job.job_id]
```

### `P1_tree_is_a_literal`

Spell the routing tree here instead of resolving it from the declared taxonomy

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag`

Old text:

```
    return plan_engine.build_adoption_plan(census(cfg), declared, tree=declared.tree.id)
```

New text:

```
    return plan_engine.build_adoption_plan(census(cfg), declared, tree="genre_energy")
```

### `P2_census_returns_a_row`

Give the census a row, so the plan the gate digests is no longer the empty plan

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 535 against a baseline of 535
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_an_empty_plan_still_has_a_digest_to_approve_against`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_empty_because_no_unit_lands_a_collection_reader`
  - `tests/test_adopt_apply_cli.py::test_the_tree_comes_off_the_declared_taxonomy_rather_than_a_flag`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[adopt.apply]`

Old text:

```
    del cfg
    return ()
```

New text:

```
    del cfg
    return (None,)
```

### `R1_marker_restored`

Put planned_in back on the entry, so the conformance suite stops driving the landed verb

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adoption.py`, `tests/test_pending_units.py`
- Collected: 1138 against a baseline of 1140
- Kills: 3 (collect-error)
- Note: collection changed: 1138 collected against a baseline of 1140. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adoption.py::test_no_landed_adoption_verb_still_owes_the_file_the_board_reads`
  - `tests/test_adoption.py::test_the_planned_marker_on_the_apply_verb_CAN_ACTUALLY_FIRE`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[adopt.apply]`

Old text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, TWO MODULES, and the split is the decision ────
```

New text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in=ADOPT_APPLY_CLI_UNIT,
    ),
    # ── Deletion: one surface, TWO MODULES, and the split is the decision ────
```

### `R2_register_entry_restored`

Owe the module again in the register while it is importable, the contradiction board.py audit exits 2 on

- File: `tests/_pending.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_adoption.py`
- Collected: 624 against a baseline of 624
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_no_landed_adoption_verb_still_owes_the_file_the_board_reads`
  - `tests/test_pending_units.py::test_the_declared_pending_set_is_exactly_the_intended_set`

Old text:

```
    "cratekit.session.restore_cli": (
```

New text:

```
    "cratekit.adopt.apply_cli": ("U27", "explicit, two gates, no destructive session and no library lock"),
    "cratekit.session.restore_cli": (
```

