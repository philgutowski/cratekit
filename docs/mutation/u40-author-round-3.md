# Mutation table: u40-author-round-3

Measured by `scripts/mutate.py` on 2026-08-26 16:44 UTC, branch `unit/u40-genre-retag-for-mis-tagged-arrivals` at `46b2e56`. Pass kind: light.

Baseline: green, 6319 collected. pytest invocations for this batch: 9.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6319 against 6319. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `N0_null_control` | `src/cratekit/tagging/retag.py` | maintainer | 1 file(s) | 6319 | 0 (promoted) | zero |
| `T1_reader_does_not_trim` | `src/cratekit/core/tags.py` | user | 9 file(s) | 1297 | 1 | killed |
| `R8_not_long_running` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 531 | collection error | collect-error |

## Zero rows and what they owe

- `N0_null_control` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `S5_no_strip`: Stop trimming the genre read off the file in select() Dropped because: NOT A GUARD AND NO LONGER PRESENT. Two rounds measured it at zero, and the reason is that `tags.read_tag` already trims every value it returns, so no input can reach `select` padded. Driven directly on 2026-08-26: writing a genre of '  Electronica ' through the real writer and reading it back through the real reader returns 'Electronica'. The strip is deleted rather than paired with a composite, because a composite would have documented dead code instead of removing it. T1 above is the composite that matters, on the module that owns the normalization.

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

### `T1_reader_does_not_trim`

The composite for the deleted S5 strip: stop trimming in core.tags.read_tag, the module that actually owns the normalization, and show what a padded value costs the retag pass

- File: `src/cratekit/core/tags.py`
- Surface: user
- Subset: test files importing cratekit.core.tags
- Ran: `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_genre_retag.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 1297 against a baseline of 1297
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_padded_catch_all_reaches_the_selection_already_trimmed`

Old text:

```
        return str(value).strip() or None
```

New text:

```
        return str(value) or None
```

### `R8_not_long_running`

Re-measured against the moved guard. Declaring the sweep short removes the verb from every derived guard in the resume contract; the guard that catches it now lives where the collected count does not move with it

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 531 against a baseline of 532
- Kills: 1 (collect-error)
- Note: collection changed: 531 collected against a baseline of 532. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`

Old text:

```
        argv_builder="retag_argv",
        long_running=True,
```

New text:

```
        argv_builder="retag_argv",
```

