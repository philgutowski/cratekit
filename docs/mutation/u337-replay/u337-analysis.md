# Mutation table: u337-analysis

Measured by `scripts/mutate.py` on 2026-11-24 19:52 UTC, branch `HEAD` at `bd7fe681`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23513 collected. pytest invocations for this batch: 40.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-24 19:52 UTC for commit `bd7fe68104c9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 6, each measured by this driver.

Known failures: 253 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23513 against 23513. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u241-dsp.D4_settings_not_handed_to_the_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 1 | 1 | killed |
| `u263.D3_libsndfile_opens_always` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 16 | killed |
| `u263.D4_resampler` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 36 | killed |
| `u263.D6_window_round` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 1 | killed |
| `u264.M10_window_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 7 | killed |
| `u264.M11_ffmpeg_left_channel` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 10 | killed |
| `u264.M12_resampler` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 36 | killed |
| `u264.M14_ffmpeg_numpy_mean` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 1 | killed |
| `u264.M1_fast_path_never` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 23513 | 0 (promoted) | zero |
| `u264.M7_three_channels_one_add` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23513 | 1 (promoted) | killed |
| `u264.M8_finite_check` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23513 | 0 (promoted) | zero |
| `u264.M9_read_at_target_rate` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 126 | 27 | killed |
| `r744-b.E7_no_prior` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 1 | killed |
| `r744.E1_no_floor` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 3 | killed |
| `r744.E2_no_ceiling` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 2 | killed |
| `r744.E3_no_interpolation` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 11 | killed |
| `r744.E4_offset_not_held` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 1 | killed |
| `r744.E5_answer_not_held_in_window` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 2 | killed |
| `r744.E6_flat_run_divides` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 18 | 1 | killed |
| `u157.D10_verdict_cut` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 1 | killed |
| `u157.D1_band_narrow` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 4 | killed |
| `u157.D2_band_wide` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 1 | killed |
| `u157.D3_pulse_gate` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 3 | killed |
| `u157.D4_onset_floor` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 2 | killed |
| `u157.D6_min_counted` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 3 | killed |
| `u157.D8_percentile` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 1 | killed |
| `u157.D9_no_interpolation` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 83 | 1 | killed |
| `u263.D16_head_no_decoder` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 302 | 1 | killed |
| `u241-dsp.D1_margin_not_applied` | `src/cratekit/analysis/separation.py` | user | 1 file(s) | 50 | 14 | killed |
| `u263.D17_vocal_reraise` | `src/cratekit/analysis/vocal.py` | user | 3 file(s) | 302 | 1 | killed |

## Zero rows and what they owe

- `u264.M1_fast_path_never` (maintainer facing): maintainer facing, composite not required
- `u264.M8_finite_check` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u241-dsp.D4_settings_not_handed_to_the_head`

handle_run: the item's settings are not compared with the workers', so a real run stops its pool at the first head

- File: `src/cratekit/analysis/cli.py`
- Source: `u241-dsp.json`, row `D4_settings_not_handed_to_the_head`
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

### `u263.D3_libsndfile_opens_always`

libsndfile_opens: answer yes for every file, so an M4A never reaches ffmpeg

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D3_libsndfile_opens_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 16 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_an_alac_m4a_measures_exactly_what_its_wav_measures`
  - `tests/test_analysis_decode_librosa.py::test_an_m4a_gets_the_tempo_the_flac_gets[aac-installed]`
  - `tests/test_analysis_decode_librosa.py::test_an_m4a_gets_the_tempo_the_flac_gets[aac-none]`
  - `tests/test_analysis_decode_librosa.py::test_an_m4a_gets_the_tempo_the_flac_gets[alac-installed]`
  - `tests/test_analysis_decode_librosa.py::test_an_m4a_gets_the_tempo_the_flac_gets[alac-none]`
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_between_frames_cut_as_libsndfile_cuts`
  - `tests/test_analysis_decode_librosa.py::test_no_ffmpeg_names_the_decoder_for_an_m4a_and_spares_a_flac`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_measure_decodes_an_m4a_once_and_reads_what_two_decodes_read[aac]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_measure_decodes_an_m4a_once_and_reads_what_two_decodes_read[alac]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_measure_takes_the_centre_of_an_m4a`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_of_an_alac_m4a_is_its_wavs`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_an_m4a_to_its_wavs_bits`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[22050]`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[32000]`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[44100]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        soundfile.info(str(path))
    except Exception:
        return False
    return True
```

New text:

```
        soundfile.info(str(path))
    except Exception:
        return True
    return True
```

### `u263.D4_resampler`

decode.load: resample the ffmpeg samples with soxr_mq rather than librosa's soxr_hq

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D4_resampler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 36 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-mono]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-mono]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-aiff]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-mp3]`
  - ... and 21 more, see the JSON sidecar

Old text:

```
res_type="soxr_hq")
```

New text:

```
res_type="soxr_mq")
```

### `u263.D6_window_round`

_window: round the frame count rather than truncate it as libsndfile does

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D6_window_round`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_between_frames_cut_as_libsndfile_cuts`

Old text:

```
    return native[..., start : start + int(duration * native_rate)]
```

New text:

```
    return native[..., start : start + round(duration * native_rate)]
```

### `u264.M10_window_dropped`

decode.load: read the whole file through librosa, dropping the offset and duration

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M10_window_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_decode_to_librosas_bits[float]`
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_decode_to_librosas_bits[mp3]`
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_decode_to_librosas_bits[pcm]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_and_duration_are_librosas_for_those_formats[aiff]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_and_duration_are_librosas_for_those_formats[flac]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_and_duration_are_librosas_for_those_formats[mp3]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_and_duration_are_librosas_for_those_formats[wav]`

Old text:

```
        native, native_rate = librosa.load(str(path), sr=None, mono=False, **window)
```

New text:

```
        native, native_rate = librosa.load(str(path), sr=None, mono=False)
```

### `u264.M11_ffmpeg_left_channel`

decode.load: mix the ffmpeg path's samples by keeping the left channel

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M11_ffmpeg_left_channel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_an_alac_m4a_measures_exactly_what_its_wav_measures`
  - `tests/test_analysis_decode_librosa.py::test_an_offset_and_a_duration_between_frames_cut_as_libsndfile_cuts`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_measure_decodes_an_m4a_once_and_reads_what_two_decodes_read[aac]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_measure_decodes_an_m4a_once_and_reads_what_two_decodes_read[alac]`
  - `tests/test_analysis_decode_librosa.py::test_the_energy_segment_of_an_alac_m4a_is_its_wavs`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_an_m4a_to_its_wavs_bits`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[22050]`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[32000]`
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[44100]`
  - `tests/test_analysis_decode_librosa.py::test_the_vocal_pass_decodes_an_m4a_at_the_models_rate`

Old text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    return _mono_at(librosa, native, native_rate, rate), rate
```

New text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    native = native[0] if native.ndim == 2 else native
    return _mono_at(librosa, native, native_rate, rate), rate
```

### `u264.M12_resampler`

_mono_at: resample with soxr_mq rather than librosa.load's soxr_hq

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M12_resampler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 36 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-mono]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-mono]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-aiff]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-mp3]`
  - ... and 21 more, see the JSON sidecar

Old text:

```
    return librosa.resample(mono(native), orig_sr=native_rate, target_sr=rate, res_type="soxr_hq")
```

New text:

```
    return librosa.resample(mono(native), orig_sr=native_rate, target_sr=rate, res_type="soxr_mq")
```

### `u264.M14_ffmpeg_numpy_mean`

decode.load: mix the ffmpeg path's samples with numpy's mean, the arithmetic before librosa 1.0, rather than the shared mix

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M14_ffmpeg_numpy_mean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_the_ffmpeg_path_mixes_minus_zero_frames_as_to_mono_does[44100]`

Old text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    return _mono_at(librosa, native, native_rate, rate), rate
```

New text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    samples = native.mean(axis=0) if native.ndim == 2 else native
    return librosa.resample(samples, orig_sr=native_rate, target_sr=rate, res_type="soxr_hq"), rate
```

### `u264.M1_fast_path_never`

mono: never take the one add, so every mix is librosa.to_mono (the speed is lost, the samples are not)

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M1_fast_path_never`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23513 against a baseline of 23513
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `u264.M7_three_channels_one_add`

_two_float32_channels: take the one add for two or more channels, so a three channel file mixes its first two

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M7_three_channels_one_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23513 against a baseline of 23513
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`

Old text:

```
        and samples.shape[0] == 2
```

New text:

```
        and samples.shape[0] >= 2
```

### `u264.M8_finite_check`

mono: drop librosa's valid_audio before the one add, so mono no longer refuses audio that is not finite itself

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M8_finite_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23513 against a baseline of 23513
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    librosa.util.valid_audio(samples)
    return _mean_of_two(samples, zero_after=zero_after)
```

New text:

```
    return _mean_of_two(samples, zero_after=zero_after)
```

### `u264.M9_read_at_target_rate`

decode.load: read through librosa.load at the target rate, so the channels are resampled before the mix rather than after

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M9_read_at_target_rate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 126 against a baseline of 126
- Kills: 27 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[22050-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-float]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-pcm]`
  - `tests/test_analysis_decode_librosa.py::test_a_file_decodes_to_the_bits_librosa_load_gives[32000-three]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-aiff]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-flac]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-mp3]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[22050-wav]`
  - `tests/test_analysis_decode_librosa.py::test_a_format_libsndfile_reads_decodes_exactly_as_librosa_load[32000-aiff]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        native, native_rate = librosa.load(str(path), sr=None, mono=False, **window)
```

New text:

```
        native, native_rate = librosa.load(str(path), sr=rate, mono=False, **window)
```

### `r744-b.E7_no_prior`

the prior over metrical levels is dropped, so of two levels inside the window the stronger raw peak wins rather than the one nearer the centre

- File: `src/cratekit/analysis/detect.py`
- Source: `r744-b.json`, row `E7_no_prior`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_the_prior_prefers_the_level_nearer_the_centre_inside_the_window`

Old text:

```
    score = np.where(inside, np.nan_to_num(strength * prior, nan=-np.inf), -np.inf)
```

New text:

```
    score = np.where(inside, strength, -np.inf)
```

### `r744.E1_no_floor`

the window's floor is not applied, so a pulse below it is named at its own level rather than by the level inside the window

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E1_no_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_a_pulse_above_the_ceiling_is_named_by_its_value_inside_the_window`
  - `tests/test_analysis_tempo.py::test_a_window_no_bin_falls_in_answers_none`
  - `tests/test_analysis_tempo.py::test_the_window_the_file_is_analysed_under_is_the_one_handed_in`

Old text:

```
    inside = (frequencies >= floor) & (frequencies <= ceiling)
```

New text:

```
    inside = (frequencies > 0) & (frequencies <= ceiling)
```

### `r744.E2_no_ceiling`

the window's ceiling is not applied, so a 166 pulse is named 166 under the shipped window instead of 83

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E2_no_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_a_peak_outside_the_window_is_not_named_and_the_one_inside_is`
  - `tests/test_analysis_tempo.py::test_a_window_no_bin_falls_in_answers_none`

Old text:

```
    inside = (frequencies >= floor) & (frequencies <= ceiling)
```

New text:

```
    inside = (frequencies >= floor) & (frequencies <= 10 * ceiling)
```

### `r744.E3_no_interpolation`

the strongest bin alone is named, which is the six beat bin width R-744 recorded as off by one to three

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E3_no_interpolation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_a_click_train_is_named_within_a_beat_of_its_tempo[122.0]`
  - `tests/test_analysis_tempo.py::test_a_click_train_is_named_within_a_beat_of_its_tempo[128.0]`
  - `tests/test_analysis_tempo.py::test_a_click_train_is_named_within_a_beat_of_its_tempo[140.0]`
  - `tests/test_analysis_tempo.py::test_a_peak_outside_the_window_is_not_named_and_the_one_inside_is`
  - `tests/test_analysis_tempo.py::test_a_pulse_above_the_ceiling_is_named_by_its_value_inside_the_window`
  - `tests/test_analysis_tempo.py::test_a_pulse_below_the_floor_is_named_by_its_subdivision`
  - `tests/test_analysis_tempo.py::test_a_vertex_leaning_past_the_window_edge_is_held_at_the_edge`
  - `tests/test_analysis_tempo.py::test_the_measure_equals_the_known_tempo_of_a_fixture_set_and_names_no_key`
  - `tests/test_analysis_tempo.py::test_the_peak_between_bins_is_named_to_a_fraction_of_a_bin`
  - `tests/test_analysis_tempo.py::test_the_strongest_bin_alone_would_be_off_by_bins`
  - `tests/test_analysis_tempo.py::test_the_window_the_file_is_analysed_under_is_the_one_handed_in`

Old text:

```
    lag = _interpolated_peak(strength, index)
    if lag <= 0.0:
```

New text:

```
    lag = float(index)
    if lag <= 0.0:
```

### `r744.E4_offset_not_held`

the parabola's offset is not held to half a bin, so a stronger raw neighbour pulls the vertex past the midpoint toward a bin the score did not choose

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E4_offset_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_the_interpolated_offset_is_held_to_half_a_bin`

Old text:

```
    return index + max(-0.5, min(0.5, offset))
```

New text:

```
    return index + offset
```

### `r744.E5_answer_not_held_in_window`

the interpolated answer is not held inside the window, so an edge bin's parabola can name a tempo below the floor

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E5_answer_not_held_in_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_a_head_never_names_a_value_outside_the_window`
  - `tests/test_analysis_tempo.py::test_a_vertex_leaning_past_the_window_edge_is_held_at_the_edge`

Old text:

```
    return float(min(max(60.0 * rate / (hop * lag), float(floor)), float(ceiling)))
```

New text:

```
    return 60.0 * rate / (hop * lag)
```

### `r744.E6_flat_run_divides`

a flat run of three equal bins is fitted anyway, dividing by a zero curvature

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E6_flat_run_divides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_tempo.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_tempo.py::test_an_edge_bin_or_a_flat_run_answers_the_bin_itself`

Old text:

```
    if curvature >= 0.0:
        return float(index)
```

New text:

```
    if curvature > 0.0:
        return float(index)
```

### `u157.D10_verdict_cut`

analyse_file: read the verdict against the shipped default, not the bound cut

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D10_verdict_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_the_verdict_follows_the_cut_the_run_binds`

Old text:

```
drift_words.verdict(drift, drift_cut)
```

New text:

```
drift_words.verdict(drift, DEFAULT_DRIFT_CUT)
```

### `u157.D1_band_narrow`

DRIFT_BAND: back to the first band of 0.12, so the other section of a two tempo track falls outside it

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D1_band_narrow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_step_wider_than_the_heads_own_section_still_scores_variable[down-a-seventh]`
  - `tests/test_analysis_drift.py::test_a_step_wider_than_the_heads_own_section_still_scores_variable[up-a-quarter]`
  - `tests/test_analysis_drift.py::test_a_step_wider_than_the_heads_own_section_still_scores_variable[up-a-sixth-slower]`
  - `tests/test_analysis_drift.py::test_a_step_wider_than_the_heads_own_section_still_scores_variable[up-a-sixth]`

Old text:

```
DRIFT_BAND = 0.25
```

New text:

```
DRIFT_BAND = 0.12
```

### `u157.D2_band_wide`

DRIFT_BAND: widened to 0.5, so a window reaches a related metrical level

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D2_band_wide`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_section_of_hats_at_three_to_two_over_a_steady_pulse_is_not_a_drift`

Old text:

```
DRIFT_BAND = 0.25
```

New text:

```
DRIFT_BAND = 0.5
```

### `u157.D3_pulse_gate`

drift_from_tempogram: drop the pulse contrast gate, so a breakdown's window counts

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D3_pulse_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_beatless_or_very_short_file_scores_unknown[noise]`
  - `tests/test_analysis_drift.py::test_a_constant_tempo_with_a_long_beatless_breakdown_still_scores_steady`
  - `tests/test_analysis_drift.py::test_a_section_of_hats_at_three_to_two_over_a_steady_pulse_is_not_a_drift`

Old text:

```
(peak - float(column[around].mean())) / peak < DRIFT_PULSE_CONTRAST
```

New text:

```
(peak - float(column[around].mean())) / peak < -1.0
```

### `u157.D4_onset_floor`

drift_from_tempogram: drop the absolute onset floor, so a pad alone is judged

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D4_onset_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_beatless_or_very_short_file_scores_unknown[pad]`
  - `tests/test_analysis_drift.py::test_a_track_with_a_pulse_in_only_two_windows_scores_unknown`

Old text:

```
if strength[i] < DRIFT_ONSET_FLOOR or strength[i]
```

New text:

```
if strength[i] < -1.0 or strength[i]
```

### `u157.D6_min_counted`

drift_from_tempogram: judge on a single counted window

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D6_min_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_beatless_or_very_short_file_scores_unknown[twenty-seconds]`
  - `tests/test_analysis_drift.py::test_a_pulse_with_too_little_pulse_to_judge_carries_unknown_and_no_drift`
  - `tests/test_analysis_drift.py::test_a_track_with_a_pulse_in_only_two_windows_scores_unknown`

Old text:

```
    if len(tempos) < DRIFT_MIN_WINDOWS:
```

New text:

```
    if len(tempos) < 1:
```

### `u157.D8_percentile`

DRIFT_PERCENTILE: the whole range instead of the tenth to ninetieth

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D8_percentile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_a_human_timing_wobble_on_a_constant_tempo_scores_steady`

Old text:

```
DRIFT_PERCENTILE = 10.0
```

New text:

```
DRIFT_PERCENTILE = 0.0
```

### `u157.D9_no_interpolation`

drift_from_tempogram: the window's bin instead of its interpolated peak

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D9_no_interpolation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_drift.py::test_the_score_grows_with_how_far_the_tempo_moves`

Old text:

```
        lag = _interpolated_peak(column, index)
        if lag <= 0.0:
            continue
```

New text:

```
        lag = float(index)
        if lag <= 0.0:
            continue
```

### `u263.D16_head_no_decoder`

detect.analyse_file: report a missing decoder as undecodable, blaming the file

- File: `src/cratekit/analysis/detect.py`
- Source: `u263.json`, row `D16_head_no_decoder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 302 against a baseline of 302
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_no_ffmpeg_names_the_decoder_for_an_m4a_and_spares_a_flac`

Old text:

```
    except decode.DecoderMissing:
        return {"path": path, "terminal": TERMINAL_NO_DECODER}

```

New text:

```
(empty)
```

### `u241-dsp.D1_margin_not_applied`

separation: the mask ignores the margin, so the key's harmonic part is not the one librosa returns

- File: `src/cratekit/analysis/separation.py`
- Source: `u241-dsp.json`, row `D1_margin_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_separation.py`
- Collected: 50 against a baseline of 50
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

### `u263.D17_vocal_reraise`

vocal.decode: swallow a missing decoder as an undecodable file

- File: `src/cratekit/analysis/vocal.py`
- Source: `u263.json`, row `D17_vocal_reraise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 302 against a baseline of 302
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode_librosa.py::test_no_ffmpeg_names_the_decoder_for_an_m4a_and_spares_a_flac`

Old text:

```
    except decoder.DecoderMissing:
        raise

```

New text:

```
(empty)
```

