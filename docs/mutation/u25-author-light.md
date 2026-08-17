# Mutation table: u25-author-light

Measured by `scripts/mutate.py` on 2026-08-17 15:57 UTC, branch `unit/u25-analysis-and-vocal-modules` at `23b1982`. Pass kind: light.

Baseline: green, 6016 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6016 against 6016. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_resume_prefix` | `src/cratekit/analysis/run.py` | user | 1 file(s) | 5 | 1 | killed |
| `G2_vocal_degrade` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 5 | 1 | killed |
| `G3_unchunked_only` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 5 | 1 | killed |
| `G4_sizing_countdown` | `tests/test_pool_sizing.py` | maintainer | 1 file(s) | 267 | 6 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `G5_extras_stub`: The extras stub lives in cli construction, already measured by U5 Dropped because: ranked below the cap: not this unit's code

## Row definitions

### `G1_resume_prefix`

Treat every filename as unfinished, including a complete Camelot head

- File: `src/cratekit/analysis/run.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_killed_batch_resumes_skipping_completed_tracks`

Old text:

```
    return has_head(path.name, template=_RESUME_TEMPLATE)

```

New text:

```
    return False

```

### `G2_vocal_degrade`

Let a vocal loader exception abort the batch instead of degrading

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_vocal_model_load_failure_leaves_key_and_energy_intact`

Old text:

```
    try:
        _VOCAL_MODEL = loader()
    except Exception:
        _VOCAL_FAILED = True
        _VOCAL_MODEL = None
    return _VOCAL_MODEL

```

New text:

```
    _VOCAL_MODEL = loader()
    return _VOCAL_MODEL

```

### `G3_unchunked_only`

Ignore chunk_samples and always run one whole-track pass

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces`

Old text:

```
    if chunk_samples is None or width <= chunk_samples:
        slices = [batch]
    else:
        slices = [
            batch[:, start : start + chunk_samples]
            for start in range(0, width, chunk_samples)
        ]

```

New text:

```
    slices = [batch]

```

### `G4_sizing_countdown`

Report the analysis package as correctly sized no matter what it contains

- File: `tests/test_pool_sizing.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 6 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[core-count-in-a-hand-built-plan]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[empty]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan-through-an-ancestor]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[no-sizing]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[private-pool]`

Old text:

```
    if not modules:
        return ["the analysis package landed with no modules in it"]

```

New text:

```
    return []

```

