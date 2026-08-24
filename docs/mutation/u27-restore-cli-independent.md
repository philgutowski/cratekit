# Mutation table: u27-restore-cli-independent

Measured by `scripts/mutate.py` on 2026-08-24 00:46 UTC, branch `HEAD` at `e2dd532`. Pass kind: full.

Baseline: green, 6183 collected. pytest invocations for this batch: 20.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6183 against 6183. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `I_A1_seam_forwards_none` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_A3_platform_seams_never_reach_the_session` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 2 | killed |
| `I_A4_target_argument_is_ignored` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_A6_plan_loses_the_process_lister` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_A7_run_loses_the_process_lister` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_A8_discard_set_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_A9_transfers_are_deduplicated` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_A10_an_off_machine_refusal_is_swallowed` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_B1_from_backup_recovery_becomes_a_no_op` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_B2_the_named_session_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 3 | killed |
| `I_B3_the_discard_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_B4_the_from_backup_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_B5_the_named_snapshot_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_B6_the_mirror_half_is_forced_on` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_B7_the_rehearsal_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_C1_discard_stops_being_repeatable` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_C3_include_mirror_defaults_on` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 4 | killed |
| `I_C5_snapshot_defaults_to_a_literal` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_C6_the_listing_verb_runs_the_restore` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 3 | killed |
| `I_D1_the_named_snapshot_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_D2_the_mirror_half_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_D6_the_digest_stops_seeing_the_offer` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_E1_spendable_is_derived_from_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_E2_the_listing_claims_an_adjudicated_queue` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_E4_the_reason_a_capture_cannot_be_spent_is_blanked` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_E5_the_default_is_chosen_on_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_E6_the_default_takes_the_oldest_spendable_capture` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_F1_the_refusal_message_becomes_its_slug` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_F3_an_unknown_identifier_becomes_a_defect_report` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_F4_the_refusal_stops_naming_the_identifier` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `I_F5_the_configuration_remedy_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 6183 | 0 (promoted) | zero |
| `I_G1_a_second_backup_slug_takes_the_wrong_status` | `src/cratekit/core/cause.py` | maintainer | 3 file(s) | 319 | 2 | killed |
| `I_H1_the_landed_verb_keeps_its_marker` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 526 | collection error | collect-error |
| `I_H3_the_new_agreement_guard_is_made_vacuous` | `tests/test_write_session.py` | maintainer | 1 file(s) | 6183 | 0 (promoted) | zero |
| `I_H4_the_discharged_countdown_is_put_back` | `tests/test_pending_units.py` | maintainer | 2 file(s) | 529 | collection error | collect-error |
| `I_H5_the_anti_vacuity_set_names_a_landed_verb` | `tests/test_cli_contract.py` | maintainer | 1 file(s) | 520 | 1 | killed |
| `I_H6_the_newly_armed_text_guard_is_defused` | `tests/test_restore.py` | maintainer | 1 file(s) | 6183 | 0 (promoted) | zero |
| `I_I1_the_package_imports_its_own_verb_module` | `src/cratekit/session/__init__.py` | maintainer | 3 file(s) | 6183 | 0 (promoted) | zero |
| `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore` | `src/cratekit/modules/tools/backup.py` | user | 3 file(s) | 216 | 3 | killed |
| `X2_the_engines_own_definition_of_spendable_is_widened` | `src/cratekit/core/restore.py` | user | 2 file(s) | 6183 | 0 (promoted) | zero |
| `X3_the_engines_own_ordering_is_reversed` | `src/cratekit/core/restore.py` | user | 2 file(s) | 6183 | 0 (promoted) | zero |
| `X4_the_capture_half_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `X5_the_refusal_reason_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 676 | 1 | killed |
| `X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 156 | 1 | killed |

## Zero rows and what they owe

- `I_A1_seam_forwards_none` (user facing): paired with `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`, which killed 3
- `I_A4_target_argument_is_ignored` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_A6_plan_loses_the_process_lister` (user facing): paired with `X6_the_rekordbox_guard_itself_is_neutered`, which killed 1
- `I_A7_run_loses_the_process_lister` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_A9_transfers_are_deduplicated` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_B1_from_backup_recovery_becomes_a_no_op` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_B4_the_from_backup_flag_is_dropped_at_the_call` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_B5_the_named_snapshot_is_dropped_at_the_call` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_B6_the_mirror_half_is_forced_on` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_C3_include_mirror_defaults_on` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_C5_snapshot_defaults_to_a_literal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_D1_the_named_snapshot_leaves_the_digest` (user facing): paired with `X4_the_capture_half_leaves_the_digest`, which killed 1
- `I_D2_the_mirror_half_leaves_the_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_E1_spendable_is_derived_from_the_wrong_half` (user facing): paired with `X2_the_engines_own_definition_of_spendable_is_widened`, which killed 0
- `I_E2_the_listing_claims_an_adjudicated_queue` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_E5_the_default_is_chosen_on_the_wrong_half` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_E6_the_default_takes_the_oldest_spendable_capture` (user facing): paired with `X3_the_engines_own_ordering_is_reversed`, which killed 0
- `I_F1_the_refusal_message_becomes_its_slug` (user facing): paired with `X5_the_refusal_reason_is_flattened`, which killed 1
- `I_F5_the_configuration_remedy_is_flattened` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I_H3_the_new_agreement_guard_is_made_vacuous` (maintainer facing): maintainer facing, composite not required
- `I_H6_the_newly_armed_text_guard_is_defused` (maintainer facing): maintainer facing, composite not required
- `I_I1_the_package_imports_its_own_verb_module` (maintainer facing): maintainer facing, composite not required
- `X2_the_engines_own_definition_of_spendable_is_widened` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `X3_the_engines_own_ordering_is_reversed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `I_A5_target_resolves_to_the_library_parent`: Restore the off-machine half one directory above the library root Dropped because: ranked below the cap: I_A4 already measures whether the target argument is honoured at all, and this is the same seam one step further out
- `I_C2_from_backup_defaults_on`: Declare --from-backup on by default Dropped because: ranked below the cap: I_B4 measures the same plumbing from the argument side, and the fixture's configured remote makes the declaration's death a property of rclone's absence rather than of a guard
- `I_D3_the_offer_totals_are_constant`: Report zero halves in the offer's totals Dropped because: ranked below the cap: the totals block is a display field the envelope schema owns, and the digest rows above already measure whether the items move
- `I_D4_the_chunk_field_becomes_an_integer`: Report a chunk index on a payload that has no chunks Dropped because: ranked below the cap: the plan/1 schema validator owns this field for every verb, so a death here would measure the validator rather than this unit
- `I_D5_the_offer_drops_the_session_start`: Leave the started timestamp out of the offered capture item Dropped because: ranked below the cap: the author's O1 already measures one field leaving the offer, and the session identifier and change summary are the two that carry the identity
- `I_E3_the_listing_name_moves`: Rename the LISTING constant Dropped because: ranked below the cap: I_E2 measures the same field with a value that would actually mislead, which is the stronger question
- `I_F2_the_refusal_detail_is_emptied`: Drop the refusal slug from the cause's detail map Dropped because: ranked below the cap: maintainer facing, and I_F1 already measures the half of the same cause a person reads
- `I_F6_the_missing_gate_branch_returns_none`: Return None rather than refusing when the entry declares no plan-digested gate Dropped because: ranked below the cap: the branch is unreachable while the registry entry declares the gate, and the author's G1 already drives the lookup
- `I_H2_the_new_guard_loses_its_anti_vacuity_line`: Delete the assertion that the refusal enum is not empty Dropped because: ranked below the cap: I_H3 makes the same guard vacuous in a way a reader would not spot, which is the harder question

## Row definitions

### `I_A1_seam_forwards_none`

Forward an unsupplied seam as None instead of omitting the argument, which hands the off-machine half a runner that is not callable

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return {} if value is None else {name: value}
```

New text:

```
    return {name: value}
```

### `I_A3_platform_seams_never_reach_the_session`

Drop the identity and mount seams from recovery_session, so the volume gate answers from this machine rather than from the caller

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock`

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

### `I_A4_target_argument_is_ignored`

Restore the off-machine half onto the configured library root even when a target was named, putting the two halves of one restore on two volumes

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            where = Path(target) if target is not None else Path(cfg.library.root)
```

New text:

```
            where = Path(cfg.library.root)
```

### `I_A6_plan_loses_the_process_lister`

Stop threading the injected process lister into the capture plan, so the rekordbox-closed guard answers from this machine

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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
            discarding=discarding,
        )
```

### `I_A7_run_loses_the_process_lister`

Stop threading the injected process lister into the capture run, the second half of the same seam

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
                process_lister=process_lister,
            ),
```

New text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
            ),
```

### `I_A8_discard_set_never_reaches_the_engine`

Plan with an empty discard set, so the override a person typed is dropped between the verb and the engine

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_A9_transfers_are_deduplicated`

Report one row per distinct transfer label rather than one per command, so a restore that copied a database and its log reports a single transfer

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            transferred = tuple(command.label for command in pulled.commands)
```

New text:

```
            transferred = tuple(dict.fromkeys(command.label for command in pulled.commands))
```

### `I_A10_an_off_machine_refusal_is_swallowed`

Continue past a refused off-machine half instead of translating it, so the capture half runs over a mirror that never landed

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`

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

### `I_B1_from_backup_recovery_becomes_a_no_op`

Return NO_OP whenever no local capture is spendable, so a --from-backup recovery on a replaced volume reports nothing to restore and pulls nothing

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if chosen is None and not ctx.args.from_backup:
```

New text:

```
    if chosen is None:
```

### `I_B2_the_named_session_never_reaches_the_engine`

Pass no session identifier at all, so a named restore performs only the off-machine half

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_B3_the_discard_flag_is_dropped_at_the_call`

Hand the engine an empty discard set from the handler, the argument-side twin of I_A8

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_B4_the_from_backup_flag_is_dropped_at_the_call`

Never ask for the off-machine half, so --from-backup is accepted, digested, approved and then ignored

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        dry_run=ctx.args.dry_run,
        from_backup=ctx.args.from_backup,
```

New text:

```
        dry_run=ctx.args.dry_run,
        from_backup=False,
```

### `I_B5_the_named_snapshot_is_dropped_at_the_call`

Pull the newest snapshot whatever --snapshot named, so a person restoring to a dated point gets the newest one instead

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        snapshot=ctx.args.snapshot,
        include_mirror=ctx.args.include_mirror,
    )
    return ctx.envelope(data=_performed(report, offered))
```

New text:

```
        snapshot=None,
        include_mirror=ctx.args.include_mirror,
    )
    return ctx.envelope(data=_performed(report, offered))
```

### `I_B6_the_mirror_half_is_forced_on`

Always pull the whole file mirror, so every --from-backup run transfers hundreds of gigabytes nobody asked for

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        snapshot=ctx.args.snapshot,
        include_mirror=ctx.args.include_mirror,
    )
    return ctx.envelope(data=_performed(report, offered))
```

New text:

```
        snapshot=ctx.args.snapshot,
        include_mirror=True,
    )
    return ctx.envelope(data=_performed(report, offered))
```

### `I_B7_the_rehearsal_flag_is_dropped_at_the_call`

Perform for real whatever --dry-run said, the argument-side twin of the author's two in-function rehearsal rows

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_C1_discard_stops_being_repeatable`

Take a single discard identifier rather than an appended list, so a person discarding two sessions names one and the string is iterated character by character

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_C3_include_mirror_defaults_on`

Declare the mirror half on by default, so the flag documented as off by default is on

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "--include-mirror",
        action="store_true",
        dest="include_mirror",
```

New text:

```
        "--include-mirror",
        action="store_true",
        default=True,
        dest="include_mirror",
```

### `I_C4_the_session_identifier_becomes_required`

Make the positional mandatory, so a bare crate restore run is a usage error rather than the newest spendable capture

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[restore.run]`
  - `tests/test_restore_cli.py::test_nothing_to_restore_is_an_outcome_and_opens_no_session`

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

### `I_C5_snapshot_defaults_to_a_literal`

Default --snapshot to the word the offer prints, which is then interpolated into the remote path as if it were a stamp

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "--snapshot",
        default=None,
```

New text:

```
        "--snapshot",
        default="newest",
```

### `I_C6_the_listing_verb_runs_the_restore`

Bind the read-only listing to the destructive handler

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 3 (killed)
- Killed:
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

### `I_D1_the_named_snapshot_leaves_the_digest`

Digest the word newest whatever snapshot was named, so two approvals for two different dated snapshots carry one digest

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "snapshot": snapshot or "newest",
```

New text:

```
                "snapshot": "newest",
```

### `I_D2_the_mirror_half_leaves_the_digest`

Digest the off-machine half as database-only always, so an approval for a database pull also authorises the whole file mirror

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "include_mirror": include_mirror,
```

New text:

```
                "include_mirror": False,
```

### `I_D6_the_digest_stops_seeing_the_offer`

Digest the verb name alone, so every restore on every library carries one constant digest and no decision can ever go stale

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused`

Old text:

```
        "digest": digest_of({"kind": "restore.run", "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "restore.run"}),
```

### `I_E1_spendable_is_derived_from_the_wrong_half`

Call a row spendable whenever it carries no unusable sentence, dropping the capture-verified half, so a capture whose integrity check never passed is listed as restorable

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "restorable": entry.restorable,
```

New text:

```
        "restorable": not entry.unusable,
```

### `I_E2_the_listing_claims_an_adjudicated_queue`

Name a declared review queue rather than this listing, so a surface nobody adjudicates promises a verdict

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            "queue": LISTING,
```

New text:

```
            "queue": "deletion",
```

### `I_E4_the_reason_a_capture_cannot_be_spent_is_blanked`

List an unusable capture with no sentence saying why, which is the silence the field exists to avoid

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`

Old text:

```
        "unusable": entry.unusable,
```

New text:

```
        "unusable": "",
```

### `I_E5_the_default_is_chosen_on_the_wrong_half`

Choose the newest row carrying no unusable sentence, dropping the verified half, the twin of I_E1 on the choosing path

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
```

New text:

```
    for entry in restore.list_sessions(cfg):
        if not entry.unusable:
            return entry
```

### `I_E6_the_default_takes_the_oldest_spendable_capture`

Walk the listing backwards, so a bare run rolls back to the oldest recorded session rather than the newest

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
```

New text:

```
    for entry in reversed(restore.list_sessions(cfg)):
        if entry.restorable:
            return entry
```

### `I_F1_the_refusal_message_becomes_its_slug`

Carry the slug where the sentence belongs, so a person is told rclone-missing and not what rclone is or where it was looked for

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            message=exc.detail,
```

New text:

```
            message=slug,
```

### `I_F3_an_unknown_identifier_becomes_a_defect_report`

Refuse a typo as an internal error, so a person who mistyped a session is told to report a defect

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_identifier_nothing_recorded_is_refused_by_name`

Old text:

```
            reason="restore-record-unusable",
```

New text:

```
            reason="internal-error",
```

### `I_F4_the_refusal_stops_naming_the_identifier`

Reword the refusal so it never repeats what was typed, which is what makes a typo diagnosable

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
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

### `I_F5_the_configuration_remedy_is_flattened`

Throw away the remedy token a configuration failure carried, so no config at all and config from a newer build get the same answer

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
```

New text:

```
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `I_G1_a_second_backup_slug_takes_the_wrong_status`

Give an unconfirmed restore a hard failure status the reservation table does not give it, a different member from the author's row so the derived guard is shown to cover the enum rather than one entry

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_where_this_table_and_the_closed_reason_registry_overlap_they_agree`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "restore-not-confirmed": ExitCode.DECISION_REQUIRED,
```

New text:

```
        "restore-not-confirmed": ExitCode.PRECONDITION,
```

### `I_H1_the_landed_verb_keeps_its_marker`

Put planned_in back on restore.list, which is what would disarm the conformance properties again

- File: `src/cratekit/cli/registry.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_pending_units.py`
- Collected: 526 against a baseline of 528
- Kills: 1 (collect-error)
- Note: collection changed: 526 collected against a baseline of 528. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[restore.list]`

Old text:

```
        # U27 LANDED IT. The marker was U32's, then U27's, and it is now gone
```

New text:

```
        planned_in="U27",
        # U27 LANDED IT. The marker was U32's, then U27's, and it is now gone
```

### `I_H3_the_new_agreement_guard_is_made_vacuous`

Compare the cause table against itself, so the two vocabularies stop being compared while the guard stays green

- File: `tests/test_write_session.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if REASONS.get(str(refusal)) is not reservations.reserved(str(refusal)).code
```

New text:

```
        if REASONS.get(str(refusal)) is not REASONS.get(str(refusal))
```

### `I_H4_the_discharged_countdown_is_put_back`

Restore the mirrored pending key, so the register owes a module that has landed

- File: `tests/test_pending_units.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_cli_contract.py`
- Collected: 529 against a baseline of 528
- Kills: 2 (collect-error)
- Note: collection changed: 529 collected against a baseline of 528. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_pending_units.py::test_a_pending_target_that_has_landed_must_be_removed_from_the_registry[cratekit.session.restore_cli]`
  - `tests/test_pending_units.py::test_the_declared_pending_set_is_exactly_the_intended_set`

Old text:

```
        "path:skills",  # U28, the shipped operator skills
    }
)
```

New text:

```
        "path:skills",  # U28, the shipped operator skills
        "cratekit.session.restore_cli",
    }
)
```

### `I_H5_the_anti_vacuity_set_names_a_landed_verb`

Expect a comparison that cannot happen, the opposite direction from the author's row on the same assertion

- File: `tests/test_cli_contract.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 520 against a baseline of 520
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_and_the_pending_register_name_the_same_unit`

Old text:

```
EXPECTED_COMPARED: frozenset[str] = frozenset()
```

New text:

```
EXPECTED_COMPARED: frozenset[str] = frozenset({"restore.list"})
```

### `I_H6_the_newly_armed_text_guard_is_defused`

Make the armed guard's third clause always true, so entering the destructive gates directly stops being refused

- File: `tests/test_restore.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    assert "assert_gates" not in source, (
```

New text:

```
    assert "assert_gates" not in source or True, (
```

### `I_I1_the_package_imports_its_own_verb_module`

Import the verb module from the package init, which is the KTD7 cost crate --help would then pay to name a subcommand

- File: `src/cratekit/session/__init__.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`, `tests/test_layering.py`, `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
letting the shorter name shadow the longer one.
"""
```

New text:

```
letting the shorter name shadow the longer one.
"""

from cratekit.session import restore_cli as restore_cli
```

### `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`

What the from-backup zeros DO leave held: remove the refusal that stops a restore with no recorded decision, in the backup module the verb calls. Paired with I_A1 and with the whole from-backup family of zeros, which are one hole rather than eleven

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 216 against a baseline of 216
- Kills: 3 (killed)
- Composite for: `I_A1_seam_forwards_none`
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`
  - `tests/test_write_session.py::test_the_restore_is_the_recovery_and_reaches_its_own_refusals`
  - `tests/test_write_session.py::test_the_restores_own_refusals_survive_the_gates_being_added`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
```

New text:

```
(empty)
```

### `X2_the_engines_own_definition_of_spendable_is_widened`

What the listing zeros DO leave held: make every recorded session report itself restorable in core.restore, the definition the CLI copies out. Paired with I_E1 and I_E5

- File: `src/cratekit/core/restore.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite
- Composite for: `I_E1_spendable_is_derived_from_the_wrong_half`

Old text:

```
    def restorable(self) -> bool:
        return not self.unusable and self.capture is not None and self.capture.verified
```

New text:

```
    def restorable(self) -> bool:
        return not self.unusable
```

### `X3_the_engines_own_ordering_is_reversed`

What the oldest-capture zero DOES leave held: sort the listing oldest first in core.restore. Paired with I_E6, which reversed the CLI's walk over the same list and killed nothing

- File: `src/cratekit/core/restore.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 6183 against a baseline of 6183
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite
- Composite for: `I_E6_the_default_takes_the_oldest_spendable_capture`

Old text:

```
    return tuple(sorted(listed, key=lambda entry: entry.started, reverse=True))
```

New text:

```
    return tuple(sorted(listed, key=lambda entry: entry.started))
```

### `X4_the_capture_half_leaves_the_digest`

What the digest zeros DO leave held: take the change summary out of the offer's capture item, the half a drive does move. Paired with I_D1 and I_D2, which took the off-machine half's two fields out and killed nothing

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Composite for: `I_D1_the_named_snapshot_leaves_the_digest`
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

### `X5_the_refusal_reason_is_flattened`

What the refusal-message zero DOES leave held: fold the off-machine slug into an internal error, which is the half a drive does assert. Paired with I_F1, which replaced the sentence and killed nothing

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 676 against a baseline of 676
- Kills: 1 (killed)
- Composite for: `I_F1_the_refusal_message_becomes_its_slug`
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`

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

### `X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 156 against a baseline of 156
- Kills: 1 (killed)
- Composite for: `I_A6_plan_loses_the_process_lister`
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


---

## Verifier's note on the pairings

`mutate.py` resolves `pairs_with` one to one, so fifteen of the twenty one user
facing zeros are printed above as unpaired. They are not. The zeros arrived in
FIVE FAMILIES with one shared cause each, and one composite was run per family
rather than one per row, because fifteen composites measuring the same hole is
fifteen full suite runs buying one fact. The mapping, with both counts:

**Family 1, the off machine half has no command line coverage.** Eleven zeros:
`I_A1`, `I_A4`, `I_A9`, `I_B1`, `I_B4`, `I_B5`, `I_B6`, `I_C3`, `I_C5`, `I_D1`,
`I_D2`. Composite `X1` removed the backup engine's own refusal for an
unconfirmed restore and killed 3, all in `tests/modules/test_tools.py`. So the
engine under the off machine half is held and the verb's wiring to it is not.
Measured independently: `--from-backup`, `--snapshot` and `--include-mirror`
appear in no test in this repository, and the three `from_backup=True` uses in
`tests/test_restore_cli.py` are direct calls below argparse and below the
dispatcher.

**Family 2, what makes a capture spendable, and in what order.** Three zeros:
`I_E1`, `I_E5`, `I_E6`. Composites `X2` and `X3` moved the same two properties
in `cratekit.core.restore` rather than in the verb, and BOTH killed 0 on the
full suite. This is the one family where the composite found nothing held on
either side: neither the capture-verified half of `Restorable.restorable` nor
`list_sessions`'s newest-first ordering is pinned anywhere in 6183 tests, so a
bare `crate restore run` could choose the oldest session, or an unverified
capture, with the suite green. Reported as two counts rather than argued.

**Family 3, the digest's off machine fields.** Two zeros: `I_D1`, `I_D2`.
Composite `X4` took the change summary out of the offer's CAPTURE item and
killed 1, `test_a_decision_recorded_against_an_offer_the_world_has_moved_past_is_refused`.
The digest mechanism is held for the half a drive moves and unheld for the half
no drive touches.

**Family 4, the refusal a person reads.** One zero: `I_F1`. Composite `X5`
flattened the same cause's REASON instead of its message and killed 1. The slug
is pinned; the sentence beside it is not.

**Family 5, the injected process lister.** Two zeros: `I_A6`, `I_A7`. Composite
`X6` neutered the rekordbox-closed assertion the seam feeds and killed 1. The
guard is held; the verb's threading of its seam is not.

`I_E2` is the only user facing zero outside a family. It is R-151, already
recorded by this commit, and its composite would measure a queue table this unit
deliberately did not join.
