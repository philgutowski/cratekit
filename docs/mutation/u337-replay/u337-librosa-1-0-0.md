# Mutation table: u337-librosa-1-0-0

Measured by `scripts/mutate.py` on 2026-11-24 20:58 UTC, branch `HEAD` at `8db7401d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23513 collected. pytest invocations for this batch: 4.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-24 20:58 UTC for commit `8db7401d52fe`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 1, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23513 against 23513. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u264.M1_fast_path_never` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 126 | 1 | killed |
| `u264.M8_finite_check` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 3 | killed |

## Row definitions

### `u264.M1_fast_path_never`

mono: never take the one add, so every mix is librosa.to_mono (the speed is lost, the samples are not)

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M1_fast_path_never`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_the_installed_release_takes_the_one_add`

Old text:

```
        and samples.shape[0] == 2
        and samples.dtype == np.float32
    )
```

New text:

```
        and samples.shape[0] == 2
        and samples.dtype == np.float32
        and False
    )
```

### `u264.M8_finite_check`

mono: drop librosa's valid_audio before the one add, so mono no longer refuses audio that is not finite itself

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M8_finite_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_the_mix_itself_refuses_audio_that_is_not_finite_as_to_mono_does[-inf]`
  - `tests/test_analysis_decode_librosa.py::test_the_mix_itself_refuses_audio_that_is_not_finite_as_to_mono_does[inf]`
  - `tests/test_analysis_decode_librosa.py::test_the_mix_itself_refuses_audio_that_is_not_finite_as_to_mono_does[nan]`

Old text:

```
    librosa.util.valid_audio(samples)
    return _mean_of_two(samples, zero_after=zero_after)
```

New text:

```
    return _mean_of_two(samples, zero_after=zero_after)
```

