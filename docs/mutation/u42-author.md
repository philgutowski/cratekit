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


---

## Round two: both zero rows resolved, 2026-08-28

Neither zero was a guard that holds nothing. Both were tests that could not reach
the guard, which is what a zero on a user facing surface is supposed to make you
go and look at. Re-measured in `u42-author-round-2.md`, one kill each.

**`C2_unknown_defaults_lossless`, 0 to 1.** The row reverts `classify`'s unknown
suffix from `other` to `lossless`. It killed nothing, subset and promoted full
suite alike, because `test_non_audio_files_are_not_reported` held `cover.jpg`,
`.DS_Store` and `notes.txt` and none of them carries the lossy marker, so all
three take the same path under either answer. The file that actually reaches the
guard is artwork named after its track, `Artist - Title [MP3].jpg`, which the
mutation reports as a lossless file wearing a lossy marker. The test now holds
one and the row kills.

**`R2_handler_lookup_imports`, 0 to 1, and this one mattered.** The row inserts a
real `importlib.import_module` into `by_handler_key`, and the guard this unit had
rewritten earlier the same day did not notice. The reason is the same shape as
the defect that rewrite was for: by the time the conformance suite runs, the
feature modules are already in `sys.modules`, so importing a cached module adds
nothing and a difference over `sys.modules` has nothing to differ against. A
difference is only a measurement where the thing could have differed. The
property is now measured in a fresh interpreter that has imported the registry
and nothing else, which is the state the supervisor is genuinely in when it
validates a queued job's handler.

The in process copy in `tests/test_jobs.py` was removed rather than restated,
because a second empty measurement beside the real one is worse than none.

**Collected count, reconciled by identifier rather than by total.** 6473 to 6414.
Fifty nine parametrised cases of
`test_a_handler_key_resolves_without_importing_the_module` and one duplicate in
`tests/test_jobs.py` were removed, and one subprocess test was added. Every
removed identifier is accounted for and nothing else left. The fifty nine were
each an empty measurement, proven so by this table, so the trade is fifty nine
vacuous assertions for one that kills.

## `R1_planned_marker_returns`: the collection delta, reconciled

The driver flagged this row `collect-error` on 627 collected against a baseline
of 630, and was right to refuse to read it as a clean result. Reconciled by
identifier rather than by total: four parametrisations over `LANDED` legitimately
cease to exist when the verb stops being landed
(`test_a_handler_key_resolves_without_importing_the_module`, and conformance 1, 2
and 3, each at `[acquire.download]`), and one appears,
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[acquire.download]`.
Net minus three. No test FILE failed to collect, so the seven kills are real and
the row is a genuine kill with an explained delta rather than a masked zero. The
restore was verified against `git show HEAD:src/cratekit/cli/registry.py`.
