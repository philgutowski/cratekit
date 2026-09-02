# Mutation table: u49-author

Measured by `scripts/mutate.py` on 2026-09-02 08:00 UTC, branch `relay/67` at `bb9cc17`. Pass kind: light.

Baseline: green, 6555 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6555 against 6555. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_the_mint_never_happens` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 4 | killed |
| `A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 2 | killed |
| `A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 3 | killed |
| `A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 1 | killed |
| `R1_hard_code_the_repair_token` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 2 | killed |
| `R2_hard_code_the_permission_token` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 2 | killed |
| `R3_an_unreadable_file_reads_as_empty` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 3 | killed |
| `L1_a_live_holder_reads_as_cleared` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 3 | killed |
| `L2_the_refusal_names_no_holder` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 2 | killed |
| `L3_nothing_recorded_reports_a_release` | `src/cratekit/session/cli.py` | user | full suite | 6555 | 2 | killed |
| `G1_an_explicit_gate_takes_an_inline_answer_again` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 6555 | 1 (promoted) | killed |
| `G2_the_second_raise_site_drops_the_context` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1238 | 1 | killed |
| `G3_absent_context_becomes_an_empty_shown` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1238 | 1 | killed |
| `V1_the_terminal_screen_stops_showing_it` | `src/cratekit/cli/render.py` | user | 4 file(s) | 1355 | 1 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `A5_the_report_comes_from_the_pre_gate_read`: Render checks and summary from the pre-gate read instead of from the record, restoring the two-read payload the simplification pass removed Dropped because: inert at this surface, not a missing test. After record_acknowledgment is handed the same moment the handler already read, both reads answer from one file at one instant and produce identical values, so no assertion can tell the mutated tree from this one. Writing a test for it would be the empty measurement the corpus warns about, and filing it as a residual would be worse than dropping it. The property the change buys is structural: one read reaches the payload rather than two, which removes the race rather than narrowing it.

## Row definitions

### `A1_the_mint_never_happens`

Delete the record_acknowledgment call and keep the envelope, so session.ack reports minting and mints nothing

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    acknowledgment = session.record_acknowledgment(cfg, now=now)
```

New text:

```
    acknowledgment = session.read_acknowledgment(cfg) or session.Acknowledgment(
        actor="nobody", recorded_at=now, expires_at=now
    )
```

### `A2_the_abort_mints_anyway`

Drop the abort branch in record_ack, so a person who declines gets an acknowledgment

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
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

### `A3_the_refusal_names_no_ages`

Drop the context argument from the ack gate, so the refusal asks the question over nothing

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 3 (killed)
- Killed:
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

### `A4_the_record_on_file_is_not_shown`

Show the ages but not the acknowledgment already on record, so a person cannot see whether they are covered

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
```

New text:

```
        spec, context={"ages": shown}
```

### `R1_hard_code_the_repair_token`

Name repair-backup-facts over every unreadable condition, which is R-201's defect reproduced on the new consumer

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[permission-grant-path-access]`

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

### `R2_hard_code_the_permission_token`

The same defect mirrored: name grant-path-access over every condition. Both directions are driven because a carry measured one way leaves the other unasserted

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
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

### `R3_an_unreadable_file_reads_as_empty`

Swallow BackupFactsUnreadable and show no ages, collapsing could-not-read into never-backed-up

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[permission-grant-path-access]`

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

### `L1_a_live_holder_reads_as_cleared`

Report the release as done whatever the engine returned, so a lock nobody cleared is reported cleared

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_stale_record_over_a_file_something_else_holds_is_still_refused`

Old text:

```
    cleared = session.release_stale_lock(cfg)
    if cleared is None:
```

New text:

```
    cleared = session.read_lock_holder(session.lock_path(cfg))
    if cleared is None:
```

### `L2_the_refusal_names_no_holder`

Drop the context from the release gate, so a person is asked to release a claim nobody described

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first`
  - `tests/test_session_cli.py::test_releasing_a_lock_nobody_holds_asks_anyway_and_reports_a_no_op`

Old text:

```
    option = ctx.gate.require(
        spec, context={"holder": holder.to_json() if holder is not None else None}
    )
```

New text:

```
    option = ctx.gate.require(spec)
```

### `L3_nothing_recorded_reports_a_release`

Report a release when nothing was recorded, which is the no-op branch collapsing into success

- File: `src/cratekit/session/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.session.cli: none found)
- Collected: 6555 against a baseline of 6555
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.release]`
  - `tests/test_session_cli.py::test_releasing_a_lock_nobody_holds_asks_anyway_and_reports_a_no_op`

Old text:

```
    if cleared is None:
        return ctx.envelope(
            data={
                "checks": [],
                "summary": {"released": False, "recorded": False},
            },
            outcome=Outcome.NO_OP,
        )
```

New text:

```
(empty)
```

### `G1_an_explicit_gate_takes_an_inline_answer_again`

Restore the recorded-is-None qualifier this unit removed, so a flag can overturn a recorded abort and mint the acknowledgment

- File: `src/cratekit/cli/gates.py`
- Surface: user
- Subset: test files importing cratekit.cli.gates
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6555 against a baseline of 6555
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`

Old text:

```
        if inline is not None and spec.explicit:
```

New text:

```
        if inline is not None and spec.explicit and recorded is None:
```

### `G2_the_second_raise_site_drops_the_context`

Carry the context at the no-answer refusal only, so what a person sees depends on whether they typed a flag

- File: `src/cratekit/cli/gates.py`
- Surface: user
- Subset: test files importing cratekit.cli.gates
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 1238 against a baseline of 1238
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_explicit_inline_refusal_carries_the_context_too`

Old text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id, context)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

New text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

### `G3_absent_context_becomes_an_empty_shown`

Materialise shown for every refusal, collapsing shows-nothing into looked-and-found-nothing

- File: `src/cratekit/cli/gates.py`
- Surface: user
- Subset: test files importing cratekit.cli.gates
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 1238 against a baseline of 1238
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_gate_refusal_with_no_context_carries_no_shown_key_at_all`

Old text:

```
        if context is not None:
            detail["shown"] = dict(context)
```

New text:

```
        detail["shown"] = dict(context or {})
```

### `V1_the_terminal_screen_stops_showing_it`

Remove the shown branch from render_gate, so the carried facts reach JSON and never reach a person

- File: `src/cratekit/cli/render.py`
- Surface: user
- Subset: test files importing cratekit.cli.render
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`
- Collected: 1355 against a baseline of 1355
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_human_mode_renders_what_the_verb_showed_and_is_unchanged_without_it`

Old text:

```
    shown = detail.get("shown")
    if isinstance(shown, Mapping) and shown:
        lines.append("")
        lines += _shown_lines(shown)
```

New text:

```
(empty)
```

