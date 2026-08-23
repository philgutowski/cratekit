# Mutation table: u27-restore-cli-author

Measured by `scripts/mutate.py` on 2026-08-23 22:12 UTC, branch `unit/u27-restore-cli` at `e2dd532`. Pass kind: full.

Baseline: green, 6183 collected. pytest invocations for this batch: 47.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6183 against 6183. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 156 | 2 | killed |
| `S2_run_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 156 | 2 | killed |
| `S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 6183 | 0 (promoted) | zero |
| `S4_watched_root_is_narrower_than_the_library` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `S5_the_off_machine_half_runs_second` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `S7_a_rehearsal_performs_the_mirror_pull` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 6183 | 0 (promoted) | zero |
| `G2_the_gate_is_never_offered_a_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `G4_the_gate_is_skipped_when_there_is_nothing_to_do` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 536 | 2 | killed |
| `O1_the_change_summary_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `O3_the_off_machine_half_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `N2_an_unknown_identifier_is_not_refused` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `P2_a_mirror_pull_is_reported_as_nothing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6183 | 0 (promoted) | zero |
| `R3_a_backup_slug_leaves_the_cause_vocabulary` | `src/cratekit/core/cause.py` | user | 2 file(s) | 91 | 2 | killed |
| `R4_a_backup_slug_takes_the_wrong_status` | `src/cratekit/core/cause.py` | maintainer | 1 file(s) | 75 | 1 | killed |
| `L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `L2_the_listing_reports_a_backlog_it_does_not_have` | `src/cratekit/session/restore_cli.py` | maintainer | 1 file(s) | 6183 | 0 (promoted) | zero |
| `L3_the_listing_drops_the_per_tree_counts` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `V1_the_expected_comparison_set_is_not_checked` | `tests/test_cli_contract.py` | maintainer | 1 file(s) | 6183 | 0 (promoted) | zero |

## Zero rows and what they owe

- `S3_analysis_watch_watches_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S4_watched_root_is_narrower_than_the_library` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S5_the_off_machine_half_runs_second` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S7_a_rehearsal_performs_the_mirror_pull` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `G1_gate_found_by_position` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `O2_the_discard_set_leaves_the_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `O3_the_off_machine_half_leaves_the_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `N2_an_unknown_identifier_is_not_refused` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R2_the_reserved_remediation_is_replaced_by_the_class_default` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L2_the_listing_reports_a_backlog_it_does_not_have` (maintainer facing): maintainer facing, composite not required
- `V1_the_expected_comparison_set_is_not_checked` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `S1_plan_takes_its_own_lock`

Let the off-machine PLAN acquire the library lock itself instead of taking the open guard

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 156 against a baseline of 156
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock`

Old text:

```
                    include_mirror=include_mirror,
                    gates=held.guard,
```

New text:

```
                    include_mirror=include_mirror,
```

### `S2_run_takes_its_own_lock`

Let the off-machine RUN acquire the library lock itself, leaving a window between plan and run

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 156 against a baseline of 156
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock`

Old text:

```
                    dry_run=dry_run,
                    gates=held.guard,
```

New text:

```
                    dry_run=dry_run,
```

### `S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `S4_watched_root_is_narrower_than_the_library`

Watch only the Music folder, so a restore writing elsewhere under the library is unwatched

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    watched: tuple[Path, ...] = (Path(cfg.library.root),)
```

New text:

```
    watched: tuple[Path, ...] = (Path(cfg.library.root) / "Music",)
```

### `S5_the_off_machine_half_runs_second`

Pull the mirror AFTER the capture restore, so the remote overwrites the session just restored

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        transferred: tuple[str, ...] = ()
        if from_backup:
```

New text:

```
        transferred: tuple[str, ...] = ()
        if session_id is not None and from_backup:
            decided = restore.plan(cfg, session_id, held=held, discarding=discarding)
            restore.run(decided, cfg, held=held, dry_run=dry_run)
        if from_backup:
```

### `S6_the_named_decision_is_withdrawn`

Tell the off-machine restore no decision exists, which R33 makes it refuse on

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock`

Old text:

```
                    confirmed=True,
```

New text:

```
                    confirmed=False,
```

### `S7_a_rehearsal_performs_the_mirror_pull`

Ignore dry_run on the off-machine half, so a preview transfers for real

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    pulled,
                    cfg,
                    dry_run=dry_run,
```

New text:

```
                    pulled,
                    cfg,
                    dry_run=False,
```

### `S8_a_rehearsal_performs_the_capture_restore`

Ignore dry_run on the capture half, so a preview replaces the live database

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`

Old text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
```

New text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=False,
```

### `G1_gate_found_by_position`

Take gates[0] rather than the gate digested against the plan

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `G2_the_gate_is_never_offered_a_digest`

Ask the confirmation with no digest, so a decision can never go stale

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused`
  - `tests/test_restore_cli.py::test_the_report_keeps_the_digest_the_decision_was_recorded_against`

Old text:

```
    option = ctx.gate.require(spec, digest=offered["digest"])
```

New text:

```
    option = ctx.gate.require(spec)
```

### `G3_abort_restores_anyway`

Treat an aborted confirmation as an approval

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_aborted_confirmation_restores_nothing`

Old text:

```
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
```

New text:

```
    if option == "never-an-option":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
```

### `G4_the_gate_is_skipped_when_there_is_nothing_to_do`

Return early before asking, so an empty library is the one never asked

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 536 against a baseline of 536
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[restore.run]`
  - `tests/test_restore_cli.py::test_nothing_to_restore_is_an_outcome_and_opens_no_session`

Old text:

```
    spec = _confirm_gate(ctx.entry)
    option = ctx.gate.require(spec, digest=offered["digest"])
```

New text:

```
    if chosen is None and not ctx.args.from_backup:
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    spec = _confirm_gate(ctx.entry)
    option = ctx.gate.require(spec, digest=offered["digest"])
```

### `O1_the_change_summary_leaves_the_digest`

Digest the session identifier without its change summary, so later work moving does not move it

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused`

Old text:

```
                "change": [
                    {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
                    for tree in chosen.change.trees
                ],
                "discarding": list(discarding),
```

New text:

```
                "discarding": list(discarding),
```

### `O2_the_discard_set_leaves_the_digest`

Digest without the sessions being discarded, so an approval covers a wider destruction

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "discarding": list(discarding),
            }
```

New text:

```
            }
```

### `O3_the_off_machine_half_leaves_the_digest`

Digest without the mirror half, so approval for one session also authorises a network pull

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if from_backup:
        items.append(
            {
                "half": "off-machine",
                "snapshot": snapshot or "newest",
                "include_mirror": include_mirror,
            }
        )
```

New text:

```
    if False:
        items.append({})
```

### `N1_the_default_takes_the_newest_unusable_capture`

Choose the newest session regardless of whether its capture can be spent

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_bare_run_takes_the_newest_spendable_capture_and_not_merely_the_newest`

Old text:

```
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
    return None
```

New text:

```
    for entry in restore.list_sessions(cfg):
        return entry
    return None
```

### `N2_an_unknown_identifier_is_not_refused`

Fall through to the newest session when the named one does not exist

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for entry in restore.list_sessions(cfg):
        if entry.session_id == session_id:
            return entry
    raise CratekitError(
```

New text:

```
    for entry in restore.list_sessions(cfg):
        if entry.session_id == session_id:
            return entry
    for entry in restore.list_sessions(cfg):
        return entry
    raise CratekitError(
```

### `P1_the_report_recomputes_the_digest`

Report a digest computed here rather than the one the decision was recorded against

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_report_keeps_the_digest_the_decision_was_recorded_against`

Old text:

```
    return {"digest": offered["digest"], "items": items, "totals": totals, "chunk": None}
```

New text:

```
    return {"digest": digest_of(items), "items": items, "totals": totals, "chunk": None}
```

### `P2_a_mirror_pull_is_reported_as_nothing`

Leave the off-machine transfers out of the report, which is the defect this shape fixed

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`

Old text:

```
    items: list[dict[str, Any]] = [
        {"half": "off-machine", "transfer": label} for label in report.pulled
    ]
```

New text:

```
    items: list[dict[str, Any]] = []
```

### `P3_convergence_is_reported_for_a_run_that_spent_no_capture`

Answer the capture restore's own question when no capture restore happened

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`

Old text:

```
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
```

New text:

```
    totals["converged"] = outcome.converged if outcome is not None else True
    if outcome is not None:
        totals["outstanding"] = len(outcome.outstanding)
```

### `R1_a_backup_refusal_becomes_an_internal_error`

Flatten every off-machine diagnosis into report-a-defect

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`

Old text:

```
            reason=slug,
            message=exc.detail,
            remediation=reservations.remediation_for(slug),
```

New text:

```
            reason="internal-error",
            message=exc.detail,
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `R2_the_reserved_remediation_is_replaced_by_the_class_default`

Discard the per-slug remediation the reservation table holds

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `R3_a_backup_slug_leaves_the_cause_vocabulary`

Remove one refusal from cause.REASONS, so building its cause raises

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "remote-not-configured": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `R4_a_backup_slug_takes_the_wrong_status`

Give one refusal a status the reservation table does not give it

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 75 against a baseline of 75
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "no-snapshot-available": ExitCode.PRECONDITION,
```

New text:

```
        "no-snapshot-available": ExitCode.INTERNAL,
```

### `L1_an_unusable_capture_is_filtered_out_of_the_listing`

Drop the sessions a person is most likely to be looking for

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`

Old text:

```
            "items": [_listed(entry) for entry in listed],
```

New text:

```
            "items": [_listed(e) for e in listed if e.restorable],
```

### `L2_the_listing_reports_a_backlog_it_does_not_have`

Report every recorded session as unresolved work

- File: `src/cratekit/session/restore_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            "unresolved": 0,
```

New text:

```
            "unresolved": len(listed),
```

### `L3_the_listing_drops_the_per_tree_counts`

List a session with no change summary, which is what makes the override unjudgeable

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_listing_shows_a_session_with_its_timestamp_workflow_and_per_tree_counts`

Old text:

```
        "change": [
            {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
            for tree in entry.change.trees
        ],
```

New text:

```
        "change": [],
```

### `V1_the_expected_comparison_set_is_not_checked`

Drop the anti-vacuity expectation, so the two registers stop being compared silently

- File: `tests/test_cli_contract.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    assert {entry.name for entry in compared} == EXPECTED_COMPARED, (
```

New text:

```
    assert {entry.name for entry in compared} <= EXPECTED_COMPARED | {"anything"}, (
```

