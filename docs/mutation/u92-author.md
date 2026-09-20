# Mutation table: u92-author

Measured by `scripts/mutate.py` on 2026-09-20 20:07 UTC, branch `relay/137` at `a6b107c`. Pass kind: light.

Baseline: green, 9255 collected. pytest invocations for this batch: 12.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 9255 against 9255. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 4 | killed |
| `G2_cap_is_inclusive` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 1 | killed |
| `G3_cap_coefficient` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 1 | killed |
| `G4_cap_doubled` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 1 | killed |
| `G5_guard_after_the_load` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 1 | killed |
| `G6_stat_failure_is_oversize` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 8 | killed |
| `G7_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 1 | killed |
| `G8_refused_file_tagged_zero` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 2 | killed |
| `G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 137 | 5 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `G10_is_oversize_takes_str_only`: Drop TypeError and ValueError from the caught set, leaving OSError alone Dropped because: ranked below the cap only in the sense that G6 measures the same clause's RESULT; the narrower catch is a crash rather than a wrong answer, and the row would report a death on an error rather than on a behaviour
- `G11_light_pass_cap`: Add and then revert a size cap on analysis/detect.analyse_file Dropped because: not this branch's guard. The light pass is uncapped on main and stays uncapped here, recorded as R-583, so there is nothing of this unit's to revert

## Row definitions

### `G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
(empty)
```

### `G2_cap_is_inclusive`

Refuse a file exactly AT the cap, strictly greater becomes greater or equal

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`

Old text:

```
        return Path(path).stat().st_size > VOCAL_MAX_BYTES
```

New text:

```
        return Path(path).stat().st_size >= VOCAL_MAX_BYTES
```

### `G3_cap_coefficient`

Megabytes instead of mebibytes, a realistic nearby value off by 4.9 percent

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 250 * 1000 * 1000
```

### `G4_cap_doubled`

Double the cap to 500 mebibytes, which still refuses something and refuses it late

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 500 * 1024 * 1024
```

### `G5_guard_after_the_load`

Move the guard behind the model load, the brief's literal reading, which this unit did not take

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

### `G6_stat_failure_is_oversize`

A size that cannot be read answers oversize, so a missing file names the wrong remedy

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    except (OSError, TypeError, ValueError):
        return False

```

New text:

```
    except (OSError, TypeError, ValueError):
        return True

```

### `G7_reason_reworded`

Reword the reason slug, never append, since the suite asserts with equality and with in

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`

Old text:

```
REASON_AUDIO_TOO_LARGE = "vocal-audio-too-large"
```

New text:

```
REASON_AUDIO_TOO_LARGE = "vocal-file-oversize"
```

### `G8_refused_file_tagged_zero`

Tag the refused file voxlevel 0 the way the source system did, instead of leaving an absence

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
    if is_oversize(result.get("path")):
        result = _inactive(result, REASON_AUDIO_TOO_LARGE)
        result["voxlevel"] = 0
        result["voxgender"] = "U"
        result["voxgenderconf"] = 0
        return result

```

### `G9_warning_counts_the_wrong_reason`

unscored_warning counts size refusals, so an oversize file is reported as a missing model

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`
  - `tests/test_analysis_workers.py::test_an_oversize_track_is_never_warned_about_as_a_missing_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
```

New text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_AUDIO_TOO_LARGE, 0))
```

