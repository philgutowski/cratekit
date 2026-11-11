# Mutation table: u241-dsp

Measured by `scripts/mutate.py` on 2026-11-11 03:57 UTC, branch `cloud/649-analyze-run-parallel` at `75916a5b`. Pass kind: light.

Baseline: green, 17872 collected. pytest invocations for this batch: 10.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/cef22e36-64fb-5681-91eb-448213182d49/scratchpad/basewt/.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 17872 against 17872. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_margin_not_applied` | `src/cratekit/analysis/separation.py` | user | 1 file(s) | 48 | 14 | killed |
| `D2_silence_not_split` | `src/cratekit/analysis/separation.py` | user | 1 file(s) | 17872 | 0 (promoted) | zero |
| `D3_windows_method_reads_the_whole_track` | `src/cratekit/analysis/detect.py` | maintainer | 2 file(s) | 43 | 1 | killed |
| `D4_settings_not_handed_to_the_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 1 | 1 | killed |

## Zero rows and what they owe

- `D2_silence_not_split` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `D1_margin_not_applied`

separation: the mask ignores the margin, so the key's harmonic part is not the one librosa returns

- File: `src/cratekit/analysis/separation.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_separation.py`
- Collected: 48 against a baseline of 48
- Kills: 14 (killed)
- Killed:
  - `tests/test_analysis_separation.py::test_the_block_size_is_memory_and_never_the_result[all]`
  - `tests/test_analysis_separation.py::test_the_block_size_is_memory_and_never_the_result[hundred]`
  - `tests/test_analysis_separation.py::test_the_block_size_is_memory_and_never_the_result[one]`
  - `tests/test_analysis_separation.py::test_the_block_size_is_memory_and_never_the_result[seven]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[a-fraction-1345050]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[a-fraction-154363]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[a-fraction-22050]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[a-fraction-7680]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[a-fraction-8000]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[the-keys-margin-1345050]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[the-keys-margin-154363]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[the-keys-margin-22050]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[the-keys-margin-7680]`
  - `tests/test_analysis_separation.py::test_the_harmonic_part_is_librosas_element_for_element[the-keys-margin-8000]`

Old text:

```
            along_time, along_frequency * margin, power=POWER, split_zeros=split_zeros

```

New text:

```
            along_time, along_frequency, power=POWER, split_zeros=split_zeros

```

### `D2_silence_not_split`

separation: a bin both medians call silent is never split, so the energy pass's pair is not librosa's over silence

- File: `src/cratekit/analysis/separation.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_separation.py`
- Collected: 17872 against a baseline of 17872
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    split_zeros = margin == 1

```

New text:

```
    split_zeros = False

```

### `D3_windows_method_reads_the_whole_track`

key_profile: the windowed method reads the whole track, so it saves nothing

- File: `src/cratekit/analysis/detect.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_methods.py`, `tests/test_analysis_key_windows.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_methods.py::test_the_windowed_profile_reads_three_minutes_of_a_long_track`

Old text:

```
    if method == KEY_WINDOWS:
        ranges = key_windows(int(samples.shape[-1]), rate)

```

New text:

```
    if False:
        ranges = key_windows(int(samples.shape[-1]), rate)

```

### `D4_settings_not_handed_to_the_head`

handle_run: the item's settings are not compared with the workers', so a real run stops its pool at the first head

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead_real.py`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead_real.py::test_the_shipped_detector_in_workers_leaves_what_it_leaves_in_the_driver`

Old text:

```
    partial = ahead.head(job.job_id, str(path), settings)

```

New text:

```
    partial = ahead.head(job.job_id, str(path), None)

```

