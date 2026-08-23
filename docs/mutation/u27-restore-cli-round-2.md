# Mutation table: u27-restore-cli-round-2

Measured by `scripts/mutate.py` on 2026-08-23 23:14 UTC, branch `unit/u27-restore-cli` at `e2dd532`. Pass kind: full.

Baseline: green, 6190 collected. pytest invocations for this batch: 20.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6190 against 6190. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 98 | 1 | killed |
| `S4_watched_root_is_narrower_than_the_library` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `S5_the_off_machine_half_runs_second` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 6190 | 0 (promoted) | zero |
| `S7_a_rehearsal_performs_the_mirror_pull` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 543 | 1 | killed |
| `O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `O3_the_off_machine_half_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `N2_an_unknown_identifier_is_not_refused` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `L2_the_listing_reports_a_backlog_it_does_not_have` | `src/cratekit/session/restore_cli.py` | maintainer | 1 file(s) | 6190 | 0 (promoted) | zero |
| `V1_the_expected_comparison_set_is_not_checked` | `tests/test_cli_contract.py` | maintainer | 1 file(s) | 6190 | 0 (promoted) | zero |

## Zero rows and what they owe

- `S5_the_off_machine_half_runs_second` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L2_the_listing_reports_a_backlog_it_does_not_have` (maintainer facing): maintainer facing, composite not required
- `V1_the_expected_comparison_set_is_not_checked` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

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
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

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
- Collected: 6190 against a baseline of 6190
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

### `S7_a_rehearsal_performs_the_mirror_pull`

Ignore dry_run on the off-machine half, so a preview transfers for real

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_neutralizes_the_mirror_transfers_too`

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

### `G1_gate_found_by_position`

Take gates[0] rather than the gate digested against the plan

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 543 against a baseline of 543
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

### `O2_the_discard_set_leaves_the_digest`

Digest without the sessions being discarded, so an approval covers a wider destruction

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_discard_set_moves`

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
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_mirror_half_is_added`

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

### `N2_an_unknown_identifier_is_not_refused`

Fall through to the newest session when the named one does not exist

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_identifier_nothing_recorded_is_refused_by_name`

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

### `R2_the_reserved_remediation_is_replaced_by_the_class_default`

Discard the per-slug remediation the reservation table holds

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `L2_the_listing_reports_a_backlog_it_does_not_have`

Report every recorded session as unresolved work

- File: `src/cratekit/session/restore_cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 6190 against a baseline of 6190
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

### `V1_the_expected_comparison_set_is_not_checked`

Drop the anti-vacuity expectation, so the two registers stop being compared silently

- File: `tests/test_cli_contract.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 6190 against a baseline of 6190
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

