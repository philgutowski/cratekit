# Mutation table: sitting3

Measured by `scripts/mutate.py` on 2026-09-17 12:12 UTC, branch `sitting/r133-vocal-restamp` at `9613489`. Pass kind: light.

Baseline: green, 7557 collected. pytest invocations for this batch: 22.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7557 against 7557. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_columns_by_number` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 4 | killed |
| `G2_missing_target_read_as_fixture` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 2 | killed |
| `G3_analyse_ignores_columns` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 7557 | 0 (promoted) | zero |
| `G4_clip_wrapper` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `G5_loader_skips_readiness` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `G6_no_labels_check` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 28 | 1 | killed |
| `G7_chatter_on_stdout` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 11 | 2 | killed |
| `G9_tail_sent_alone` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 5 | killed |
| `G10_lone_clip_not_padded` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 3 | killed |
| `G11_tail_dropped` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 2 | killed |
| `G12_columns_per_track` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 17 | 1 | killed |
| `G13_padded_frames_kept` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `G14_unchunked_floor_is_width` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `G15_fold_any_ragged_tail` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 3 | killed |
| `G16_torch_by_lookup` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 17 | 1 | killed |

## Zero rows and what they owe

- `G3_analyse_ignores_columns` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `G1_columns_by_number`

Read the first three columns whatever the label table says, the R-370 defect

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    labels = getattr(model, "labels", None)
    if labels is None:
        raise ValueError(

```

New text:

```
    labels = getattr(model, "labels", None)
    if True:
        return (0, 1, 2)
        raise ValueError(

```

### `G2_missing_target_read_as_fixture`

A label table lacking a target falls back to the first three columns instead of raising

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`

Old text:

```
    except ValueError as exc:
        raise ValueError(
            f"the vocal model's label table does not name all of {TARGET_LABELS}"
        ) from exc
    return (first, second, third)

```

New text:

```
    except ValueError:
        return (0, 1, 2)
    return (first, second, third)

```

### `G3_analyse_ignores_columns`

The scorer resolves the columns and then does not pass them

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 7557 against a baseline of 7557
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        score = reduce_frames(*infer_frames(model, samples, class_idx=columns))

```

New text:

```
        score = reduce_frames(*infer_frames(model, samples))

```

### `G4_clip_wrapper`

Build the clip level wrapper again

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    from panns_inference import SoundEventDetection

    # The wrapper prints its checkpoint path and device to stdout on
    # construction, and stdout is where the JSON envelope goes.
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    from panns_inference import AudioTagging

    with contextlib.redirect_stdout(io.StringIO()):
        return AudioTagging(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `G5_loader_skips_readiness`

Ask the library for files that are not there, which is the wget shell out

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_refuses_before_the_extra_is_asked_for_a_missing_checkpoint`

Old text:

```
    missing = scoring.missing_requirement()
    if missing is not None:
        raise FileNotFoundError(missing)

```

New text:

```
    missing = None
    if missing is not None:
        raise FileNotFoundError(missing)

```

### `G6_no_labels_check`

Readiness does not check the label table, so the extra is imported without it

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 28 against a baseline of 28
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_refuses_before_the_extra_is_asked_for_a_missing_checkpoint`

Old text:

```
    if not labels_ready():
        return (
            f"the vocal model's label table is not at {LABELS}; place "

```

New text:

```
    if False:
        return (
            f"the vocal model's label table is not at {LABELS}; place "

```

### `G7_chatter_on_stdout`

Let the wrapper print onto the JSON envelope's stream

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    with contextlib.nullcontext():
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `G8_queue_skips_readiness`

File the job whatever is missing, so a restamp scores nothing and reports ok

- File: `src/cratekit/vocals/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 11 against a baseline of 11
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return

```

New text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if True:
        return

```

### `G9_tail_sent_alone`

Send a short tail to the network as its own piece, the R-371 defect

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_a_short_tail_is_folded_into_the_chunk_before_it`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    slices = _without_a_short_tail(slices, floor=floor)

```

New text:

```
    slices = list(slices)

```

### `G10_lone_clip_not_padded`

A lone clip shorter than the floor goes to the network unpadded

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    if len(slices) == 1:
        pad = floor - int(last.shape[-1])
        return [np.concatenate([last, np.zeros((last.shape[0], pad), last.dtype)], axis=-1)]

```

New text:

```
    if len(slices) == 1:
        return slices

```

### `G11_tail_dropped`

Drop a short tail instead of folding it, so its frames are never scored

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_short_tail_is_folded_into_the_chunk_before_it`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`

Old text:

```
    merged = np.concatenate([slices[-2], last], axis=-1)
    return [*slices[:-2], merged]

```

New text:

```
    return slices[:-1]

```

### `G12_columns_per_track`

Resolve the columns per track after the decode instead of once at load

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`

Old text:

```
        _VOCAL_COLUMNS = class_indices(model)
        _VOCAL_MODEL = model

```

New text:

```
        _VOCAL_COLUMNS = None
        _VOCAL_MODEL = model

```

### `G13_padded_frames_kept`

Count the frames the padding added, so a short clip's presence is diluted

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    if padded > width and vocals.size:

```

New text:

```
    if False:

```

### `G14_unchunked_floor_is_width`

Let the unchunked path's floor collapse to the signal's own width

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = min(MIN_CHUNK_SAMPLES, chunk_samples or width)

```

### `G15_fold_any_ragged_tail`

Fold every tail shorter than the chunk, not only one under the floor

- File: `src/cratekit/analysis/vocal.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else chunk_samples

```

### `G16_torch_by_lookup`

Answer torch by a lookup, so an installed torch that will not load passes the queue

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_torch_that_will_not_load_is_the_first_missing_requirement`

Old text:

```
    try:
        import torch  # noqa: F401
    except Exception as exc:  # noqa: BLE001 - a torch that will not load is the case
        return f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {INSTALL}"

```

New text:

```
    if not _installed("torch"):
        return f"the 'vocals' extra is not usable here; {INSTALL}"

```

