# Mutation table: u42-author

Measured by `scripts/mutate.py` on 2026-08-29 01:33 UTC, branch `unit/u42-the-two-acquire-command-line-shells-rows` at `a1b4b45`. Pass kind: light.

Baseline: green, 6473 collected. pytest invocations for this batch: 21.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6473 against 6473. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `W1_onerror_hook` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `W3_onerror_silent` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 6473 | 0 (promoted) | zero |
| `C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `P1_unresolved_from_the_page` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 24 | 6 | killed |
| `Q1_argv_drops_the_job` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `Q2_payload_loses_the_list` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `R1_planned_marker_returns` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 627 | collection error | collect-error |
| `R2_handler_lookup_imports` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 6473 | 0 (promoted) | zero |

## Zero rows and what they owe

- `C2_unknown_defaults_lossless` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R2_handler_lookup_imports` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `C6_lossless_exts_membership`: Move .wav from LOSSLESS_EXTS to LOSSY_EXTS Dropped because: ranked below C1 and C2, which measure the same partition from the side that can fail silently; a membership swap is caught by the partition test in one line and buys no information the two rows above do not already carry
- `P3_queue_constant`: Change AUDIT_QUEUE to a different literal Dropped because: maintainer surface with no consumer in this build; the constant exists so a later consumer can scope a set, and nothing yet reads it, so a zero here would document an absence rather than measure a guard

## Row definitions

### `W1_onerror_hook`

Revert the walk to Path.rglob, which swallows the PermissionError

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_directory_it_cannot_list_is_reported`
  - `tests/test_acquire_cli.py::test_the_unreadable_row_counts_toward_the_outstanding_total`

Old text:

```
    for dirpath, _dirnames, filenames in os.walk(root, onerror=note):
        here = Path(dirpath)
        for name in filenames:
            path = here / name
```

New text:

```
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if True:
```

### `W2_unreadable_reported`

Collect the unreadable directories and then never report them

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_directory_it_cannot_list_is_reported`
  - `tests/test_acquire_cli.py::test_the_unreadable_row_counts_toward_the_outstanding_total`

Old text:

```
    found += [_item(path, root, "path-unreadable") for path in unreadable]
```

New text:

```
(empty)
```

### `W3_onerror_silent`

Keep os.walk but make the error hook a no-op, the half-fix

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_directory_it_cannot_list_is_reported`
  - `tests/test_acquire_cli.py::test_the_unreadable_row_counts_toward_the_outstanding_total`

Old text:

```
        unreadable.append(Path(exc.filename) if exc.filename else root)
```

New text:

```
        return None
```

### `C1_undecided_derived`

Empty the undecided remainder, so an MP4 container falls out as 'other'

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_every_audio_container_the_renamer_knows_has_a_classification`
  - `tests/test_acquire_cli.py::test_the_undecided_remainder_is_the_mp4_container_today`

Old text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS
```

New text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset()
```

### `C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 6473 against a baseline of 6473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
```

### `C3_strict_consults_the_marker`

Make strict behave like the permissive policy, admitting a marked lossy file

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

New text:

```
                if policy is LosslessPolicy.STRICT and marker and not marked:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

### `C4_marked_lossless_dropped`

Stop reporting a lossless file that wears the lossy marker

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`

Old text:

```
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
```

New text:

```
            elif False:
                found.append(_item(path, root, "marked-lossless"))
```

### `C5_empty_marker_matches_everything`

Drop the empty-marker guard, so '' in stem marks every file

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`

Old text:

```
            marked = bool(marker) and marker in path.stem
```

New text:

```
            marked = marker in path.stem
```

### `P1_unresolved_from_the_page`

Report zero outstanding regardless of what the walk found

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`
  - `tests/test_acquire_cli.py::test_the_unreadable_row_counts_toward_the_outstanding_total`

Old text:

```
            "unresolved": len(found),
```

New text:

```
            "unresolved": 0,
```

### `P2_relative_path_leaks_the_root`

Report the absolute path, putting a real directory layout in the payload (R1)

- File: `src/cratekit/acquire/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 6 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_a_directory_it_cannot_list_is_reported`
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_permissive_policy_reports_only_the_unmarked_lossy_file`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`

Old text:

```
        where = str(path.relative_to(root))
```

New text:

```
        where = str(path)
```

### `Q1_argv_drops_the_job`

Resume argv without the job identifier, so the child queues a second job

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`

Old text:

```
    return ["acquire", "download", wanted, "--job", job.job_id]
```

New text:

```
    return ["acquire", "download", wanted]
```

### `Q2_payload_loses_the_list`

Freeze an empty list path, so the resumed worker acquires nothing

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`

Old text:

```
            payload={"list": str(ctx.args.list)},
```

New text:

```
            payload={"list": ""},
```

### `R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_cutover_parity.py`, `tests/test_cli_contract.py`
- Collected: 627 against a baseline of 630
- Kills: 7 (collect-error)
- Note: collection changed: 627 collected against a baseline of 630. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_cli.py::test_download_on_an_absent_job_refuses_with_a_vocabulary_code`
  - `tests/test_acquire_cli.py::test_download_over_an_absent_list_queues_and_exits_ok`
  - `tests/test_acquire_cli.py::test_download_reaches_no_provider_and_no_network`
  - `tests/test_acquire_cli.py::test_the_verb_appears_in_help_and_dispatches[acquire.download]`
  - `tests/test_acquire_cli.py::test_the_verb_is_landed_rather_than_planned[acquire.download]`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[acquire.download]`

Old text:

```
        doctor_checks=("credential.provider", "binary.ffmpeg"),
        # U42 LANDED IT.
```

New text:

```
        doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
        # U42 LANDED IT.
```

### `R2_handler_lookup_imports`

Make by_handler_key import the module, which is what the rewritten guard forbids

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 6473 against a baseline of 6473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
def by_handler_key(key: str) -> Entry:
```

New text:

```
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

