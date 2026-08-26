# Mutation table: u40-author-round-2

Measured by `scripts/mutate.py` on 2026-08-26 16:15 UTC, branch `unit/u40-genre-retag-for-mis-tagged-arrivals` at `91d300b`. Pass kind: light.

Baseline: green, 6319 collected. pytest invocations for this batch: 19.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6319 against 6319. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `N0_null_control` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6319 | 0 (promoted) | zero |
| `S5_no_strip` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 6319 | 0 (promoted) | zero |
| `S4_missing_folder` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6319 | 0 (promoted) | zero |
| `P5_verdict_not_checked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 40 | 1 | killed |
| `P8_identity_key` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 40 | 1 | killed |
| `D1_plan_from_selection` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 40 | 1 | killed |
| `D3_zip_not_strict` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6319 | 0 (promoted) | zero |
| `C6_constant_digest` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 588 | 1 | killed |
| `C6b_folder_out_of_digest` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 588 | 1 | killed |
| `R8_not_long_running` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 15 | collection error | collect-error |

## Zero rows and what they owe

- `N0_null_control` (maintainer facing): maintainer facing, composite not required
- `S5_no_strip` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S4_missing_folder` (maintainer facing): maintainer facing, composite not required
- `D3_zip_not_strict` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `R7_not_destructive`: Declare the verb non-destructive, so the destructive-session gates never bind to it (KTD24) Dropped because: NOT MEASURABLE AS A MUTATION, and that is the answer rather than a gap. `registry.Entry.__post_init__` refuses any entry that writes files and does not declare destructive, so the mutation raises ValueError at import and takes the whole test file out of collection. Round one recorded it as a collect error for exactly that reason. The refusal itself is driven by tests/test_cli_contract.py:1143, which hands the constructor `writes={'files'}` with no destructive flag and asserts the message. A row that cannot be applied measures the type system, not the suite.
- `R1_gate_not_explicit`: Make the confirm gate ordinary, which drops the verb out of the queued-resume guard entirely Dropped because: REFUSED BY THE DRIVER in round one with a collected count of 0, because the `explicit=True,` line it anchors on is not unique in registry.py and mutate.py refuses an ambiguous match before writing anything rather than mutating the wrong site. Re-anchoring it uniquely would take the whole GateSpec block, which is what R8 above already mutates one field of. Dropped rather than re-anchored because the property it would measure, that this verb sits inside the resume guard's derived population, is exactly what R8 measures from the other flag of the same pair.

## Row definitions

### `N0_null_control`

A comment reworded and nothing else. Must kill zero, or the baseline is red and every number below it is noise.

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6319 against a baseline of 6319
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
LAYER: modules.
```

New text:

```
LAYER: modules layer.
```

### `S5_no_strip`

Round one zero, now guarded. Stop trimming the genre read off the file, so the candidate CARRIES the padded spelling into the plan and into the review payload

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6319 against a baseline of 6319
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        current = (tags.read_genre_from_file(path) or "").strip()
```

New text:

```
        current = tags.read_genre_from_file(path) or ""
```

### `S4_missing_folder`

Round one zero, RECLASSIFIED to maintainer facing rather than paired with a composite. Remove the not-a-directory guard

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6319 against a baseline of 6319
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not root.is_dir():
        return Selection()

```

New text:

```
(empty)
```

### `P5_verdict_not_checked`

Round one zero, now guarded directly. Accept a REJECTED item's chosen option as an answer, so every rejection reads as an acceptance

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_rejected_items_chosen_option_is_not_an_answer`

Old text:

```
    if item.verdict is not review.Verdict.ACCEPTED or not item.option:
```

New text:

```
    if not item.option:
```

### `P8_identity_key`

Round one zero, now guarded. Address a review item by a different key, so every item any earlier build offered is orphaned

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_review_item_is_addressed_by_the_file_path_under_that_exact_name`

Old text:

```
    return {"path": str(path)}
```

New text:

```
    return {"file": str(path)}
```

### `D1_plan_from_selection`

Round one zero, and the most useful row in the table. Plan from every result rather than from what was written; the assertion that missed it asserted an empty change list, which the mutation also produces by a different mechanism

- File: `src/cratekit/tagging/retag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_plan_is_built_from_what_was_written_and_never_from_the_selection`

Old text:

```
    written = outcome.written
```

New text:

```
    written = outcome.results
```

### `D3_zip_not_strict`

Round one zero, maintainer facing, ONE LINE and no composite per METHOD. Drop strict from the zip pairing results with matches

- File: `src/cratekit/tagging/retag.py`
- Surface: maintainer
- Subset: test files importing cratekit.tagging.retag
- Ran: `tests/test_genre_retag.py`
- Collected: 6319 against a baseline of 6319
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for result, match in zip(written, matches, strict=True):
```

New text:

```
    for result, match in zip(written, matches):
```

### `C6_constant_digest`

Round one zero, unreachable until the plan came out of the handler. Digest a constant rather than the folder and its selection

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 588 against a baseline of 588
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`

Old text:

```
        "digest": digest_of({"kind": "tag.retag", "folder": folder, "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "tag.retag"}),
```

### `C6b_folder_out_of_digest`

The half a rows-only digest would still pass: keep the selection in the digest and drop the folder, so two different empty folders are one decision

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 588 against a baseline of 588
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`

Old text:

```
        "digest": digest_of({"kind": "tag.retag", "folder": folder, "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "tag.retag", "items": items}),
```

### `R8_not_long_running`

Round one COLLECT ERROR rather than a zero, and the error was the finding. Declaring the sweep short removes the verb from every derived guard in the resume contract, so the suite loses three tests and goes green

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`
- Collected: 15 against a baseline of 17
- Kills: 1 (collect-error)
- Note: collection changed: 15 collected against a baseline of 17. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_queued_resume_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`

Old text:

```
        argv_builder="retag_argv",
        long_running=True,
```

New text:

```
        argv_builder="retag_argv",
```

