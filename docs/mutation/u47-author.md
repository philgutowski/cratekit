# Mutation table: u47-author

Measured by `scripts/mutate.py` on 2026-09-02 02:40 UTC, branch `relay/65` at `5b420c3`. Pass kind: full.

Baseline: green, 6515 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6515 against 6515. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R197_drop_event_abort` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R197_drop_event_run` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R197_drop_progress` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R197_drop_progress_overall` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R197_event_run_left_clear` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R197_event_abort_preset` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R197_progress_enabled` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R197_argument_set_shrinks` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 158 | 2 | killed |
| `R195_drop_ffmpeg_key` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 4 | killed |
| `R195_push_empty_instead` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 4 | killed |
| `R195_swallow_missing_ffmpeg` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R195_wrong_remedy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R195_verify_skips_the_mapping` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R196_login_without_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R196_accept_device_flow_session` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 3 | killed |
| `R196_absent_marker_reads_as_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R196_no_stored_session_proceeds` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `R196_token_drops_is_pkce` | `src/cratekit/_vendor/tidal_dl_ng/config.py` | user | 2 file(s) | 158 | 3 | killed |
| `R196_persist_reads_the_wrong_symbol` | `src/cratekit/_vendor/tidal_dl_ng/config.py` | user | 2 file(s) | 158 | 2 | killed |
| `R196_token_model_loses_the_field` | `src/cratekit/_vendor/tidal_dl_ng/model/cfg.py` | user | 2 file(s) | 158 | 4 | killed |
| `R196_device_flow_returns` | `src/cratekit/_vendor/tidal_dl_ng/config.py` | user | 1 file(s) | 36 | 1 | killed |
| `CODEC_no_refusal` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 4 | killed |
| `CODEC_unreadable_accepted` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 2 | killed |
| `CODEC_none_reads_as_unreadable` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 4 | killed |
| `CODEC_alac_reads_as_lossy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `CODEC_mp3_reads_as_lossless` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `CODEC_suffix_instead_of_container` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 159 | 1 | killed |
| `CODEC_policy_ignored` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `CODEC_refusal_drops_the_codec_name` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 2 | killed |
| `CODEC_refused_track_sinks_the_run` | `src/cratekit/acquire/adapter.py` | user | 2 file(s) | 158 | 2 | killed |
| `SAMPLE_skip_reported_as_a_file` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 2 | killed |
| `SAMPLE_permanence_asked_second` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |
| `SAMPLE_quality_equality` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 158 | 1 | killed |

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `R197_drop_tidal_obj`: Drop tidal_obj from the downloader construction Dropped because: ranked below the cap: it is the one argument the pre-existing code already passed, so the row measures the old behaviour rather than this round's change. The three original arguments are covered as a family by R197_argument_set_shrinks.
- `CODEC_wave_and_aiff_flipped`: Flip WAVE and AIFF to lossy in the container table Dropped because: ranked below the cap: same guard family as CODEC_mp3_reads_as_lossless, which is measured, and neither container is reachable from this provider.
- `R196_reauthorise_hint_reworded`: Reword REAUTHORISE_HINT so it no longer names the two steps Dropped because: ranked below the cap: maintainer-facing string content, and the severity floor says such a row can never block.

## Row definitions

### `R197_drop_event_abort`

Drop event_abort from the downloader construction, the argument whose absence killed item() on its first line

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
            event_abort=event_abort,

```

New text:

```
(empty)
```

### `R197_drop_event_run`

Drop event_run from the downloader construction

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
            event_run=event_run,

```

New text:

```
(empty)
```

### `R197_drop_progress`

Drop progress from the downloader construction, half of the pair whose absence swallowed the failure

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`

Old text:

```
            progress=progress,

```

New text:

```
(empty)
```

### `R197_drop_progress_overall`

Drop progress_overall from the downloader construction

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`

Old text:

```
            progress_overall=progress_overall,

```

New text:

```
(empty)
```

### `R197_event_run_left_clear`

Pass event_run unset, the realistic nearby value: every segment worker then waits on something nothing wakes, so the failure is a hang rather than an error

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    event_run = Event()
    event_run.set()
    return Event(), event_run
```

New text:

```
    event_run = Event()
    return Event(), event_run
```

### `R197_event_abort_preset`

Pass event_abort already set, which makes item() return (False, '') before it looks at anything

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    return Event(), event_run
```

New text:

```
    aborted = Event()
    aborted.set()
    return aborted, event_run
```

### `R197_progress_enabled`

Render the progress bars, so tool chatter reaches a stream a caller may be parsing (R32)

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`

Old text:

```
    return Progress(disable=True), Progress(disable=True)
```

New text:

```
    return Progress(disable=False), Progress(disable=False)
```

### `R197_argument_set_shrinks`

Remove event_abort from the declared argument set, so the set no longer describes what fetch passes

- File: `src/cratekit/acquire/vendored.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_every_keyword_fetch_passes_exists_on_the_real_downloader`
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`

Old text:

```
        "event_abort",

```

New text:

```
(empty)
```

### `R195_drop_ffmpeg_key`

Drop path_binary_ffmpeg from the settings mapping, which is exactly the state that landed a 320k AAC file with doctor reporting green

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_applying_settings_writes_them_in_memory_and_saves_nothing`
  - `tests/test_adapter_contract.py::test_the_ffmpeg_path_is_the_one_the_binaries_module_resolves`
  - `tests/test_adapter_contract.py::test_the_vendored_settings_translation_names_every_key_that_reverted`
  - `tests/test_adapter_contract.py::test_verification_covers_the_ffmpeg_key_by_it_being_pushed`

Old text:

```
        "path_binary_ffmpeg": ffmpeg,

```

New text:

```
(empty)
```

### `R195_push_empty_instead`

Push the empty string rather than the resolved path, the tool's factory default and the value it reads as do-not-extract-FLAC

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_applying_settings_writes_them_in_memory_and_saves_nothing`
  - `tests/test_adapter_contract.py::test_the_ffmpeg_path_is_the_one_the_binaries_module_resolves`
  - `tests/test_adapter_contract.py::test_the_vendored_settings_translation_names_every_key_that_reverted`
  - `tests/test_adapter_contract.py::test_verification_covers_the_ffmpeg_key_by_it_being_pushed`

Old text:

```
        "path_binary_ffmpeg": ffmpeg,
```

New text:

```
        "path_binary_ffmpeg": "",
```

### `R195_swallow_missing_ffmpeg`

Treat an unresolvable ffmpeg as an empty path instead of refusing, so an absent encoder arrives as a successful lossy download

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_machine_with_no_ffmpeg_refuses_by_name_instead_of_landing_lossy`

Old text:

```
        raise AdapterBroken(
            f"the downloader needs ffmpeg to extract lossless audio and it could "
            f"not be resolved ({exc}); without it this run would land lossy files "
            f"and report success",
            remedy=Remedy.INSTALL_ADAPTER,
        ) from exc
```

New text:

```
        ffmpeg = ""
```

### `R195_wrong_remedy`

Reword the absent-encoder remedy to SWITCH_ADAPTER, which tells the user to change adapters when the answer is to install a binary

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_machine_with_no_ffmpeg_refuses_by_name_instead_of_landing_lossy`

Old text:

```
            remedy=Remedy.INSTALL_ADAPTER,
        ) from exc
```

New text:

```
            remedy=Remedy.SWITCH_ADAPTER,
        ) from exc
```

### `R195_verify_skips_the_mapping`

Verify a hand-named pair rather than everything pushed, which is the source system's guard that watched two keys while the tool had more

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_an_injected_session_still_has_this_runs_settings_pushed_and_verified`
  - `tests/test_adapter_contract.py::test_applying_settings_writes_them_in_memory_and_saves_nothing`
  - `tests/test_adapter_contract.py::test_verification_covers_the_ffmpeg_key_by_it_being_pushed`

Old text:

```
    applied = {key: getattr(target, key, _ABSENT) for key in expected}
```

New text:

```
    applied = {key: getattr(target, key, _ABSENT) for key in ("quality_audio",)}
```

### `R196_login_without_pkce`

Authenticate with PKCE off, which is the call that produced lossy audio for every download since July

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_adapter_authenticates_with_pkce_on`

Old text:

```
            authorised = tidal.login_token(do_pkce=True)
```

New text:

```
            authorised = tidal.login_token()
```

### `R196_accept_device_flow_session`

Stop refusing a stored device-flow session, so the product silently downloads lossy audio with it

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_device_flow_session_is_refused_with_a_remedy_that_has_a_procedure`
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored1-True-True]`
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored2-True-True]`

Old text:

```
    if not bool(getattr(stored, "is_pkce", False)):
```

New text:

```
    if False:
```

### `R196_absent_marker_reads_as_pkce`

Default a missing is_pkce to True, so a legacy device-flow token is read as a PKCE one

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored2-True-True]`

Old text:

```
    if not bool(getattr(stored, "is_pkce", False)):
```

New text:

```
    if not bool(getattr(stored, "is_pkce", True)):
```

### `R196_no_stored_session_proceeds`

Proceed when there is no stored session at all

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored3-False-True]`

Old text:

```
    if not had_stored_session:
        return "there is no stored provider session to authenticate with"
```

New text:

```
(empty)
```

### `R196_token_drops_is_pkce`

Stop persisting is_pkce, the exact upstream defect: a field the write never stores is a field the read cannot see

- File: `src/cratekit/_vendor/tidal_dl_ng/config.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_persisted_pkce_session_reloads_as_a_pkce_session`
  - `tests/test_adapter_contract.py::test_the_persisted_flag_survives_the_bool_coercion_in_set_option`
  - `tests/test_vendor_import.py::test_the_persisted_token_records_which_client_minted_it`

Old text:

```
        self.data.is_pkce = bool(getattr(self.session, "is_pkce", False))

```

New text:

```
(empty)
```

### `R196_persist_reads_the_wrong_symbol`

Persist this object's is_pkce rather than the session's; login() sets the former False before the PKCE handshake runs, so every fresh PKCE session records as device flow

- File: `src/cratekit/_vendor/tidal_dl_ng/config.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_persisted_pkce_session_reloads_as_a_pkce_session`
  - `tests/test_adapter_contract.py::test_the_persisted_flag_survives_the_bool_coercion_in_set_option`

Old text:

```
        self.data.is_pkce = bool(getattr(self.session, "is_pkce", False))
```

New text:

```
        self.data.is_pkce = bool(getattr(self, "is_pkce", False))
```

### `R196_token_model_loses_the_field`

Remove is_pkce from the Token dataclass

- File: `src/cratekit/_vendor/tidal_dl_ng/model/cfg.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_persisted_pkce_session_reloads_as_a_pkce_session`
  - `tests/test_adapter_contract.py::test_a_session_with_no_pkce_marker_reloads_as_a_device_flow_session`
  - `tests/test_adapter_contract.py::test_the_persisted_flag_survives_the_bool_coercion_in_set_option`
  - `tests/test_vendor_import.py::test_the_persisted_token_records_which_client_minted_it`

Old text:

```
    is_pkce: bool = False

```

New text:

```
(empty)
```

### `R196_device_flow_returns`

Put the device-linking login back, the client the provider serves lossy audio to

- File: `src/cratekit/_vendor/tidal_dl_ng/config.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_the_interactive_login_is_pkce_and_the_device_flow_is_gone`

Old text:

```
            self.session.login_pkce(fn_print)
```

New text:

```
            self.session.login_oauth_simple(fn_print)
```

### `CODEC_no_refusal`

Accept whatever landed, which is the state the product shipped in from July: the rule enforced at the setting and never at the file

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_is_refused_and_the_refusal_names_the_codec`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`
  - `tests/test_adapter_contract.py::test_a_refused_file_is_left_where_it_landed`

Old text:

```
    if not lossless:
        raise LosslessRefused(
            f"the provider was asked for lossless audio and the file that landed "
            f"for {key} is {name}; it is at {path}"
        )
```

New text:

```
(empty)
```

### `CODEC_unreadable_accepted`

Accept a landing the probe could not read, turning absence of evidence into evidence of losslessness

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_landing_that_cannot_be_read_is_refused_as_unreadable_not_as_lossy[empty.flac]`
  - `tests/test_adapter_contract.py::test_a_landing_that_cannot_be_read_is_refused_as_unreadable_not_as_lossy[mystery.xyz]`

Old text:

```
    if lossless is None:
        raise LosslessRefused(
            f"the file that landed for {key} could not be read as audio ({name}), "
            f"so this run cannot confirm it is lossless; it is at {path}"
        )
```

New text:

```
(empty)
```

### `CODEC_none_reads_as_unreadable`

Treat a None codec as unreadable rather than as container-decided, which refuses every genuine FLAC because mutagen exposes info.codec on MP4 alone

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_real_flac_is_accepted_even_though_mutagen_reports_no_codec`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    known = LOSSLESS_BY_CONTAINER.get(container)
    if known is None:
        return container, None
    return container, known
```

New text:

```
    return container, None
```

### `CODEC_alac_reads_as_lossy`

Drop alac from the lossless MP4 codecs, so a genuine ALAC landing is refused

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_codec_table_answers_for_every_container_it_declares`

Old text:

```
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset({"alac"})
```

New text:

```
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset()
```

### `CODEC_mp3_reads_as_lossless`

Flip MP3 to lossless in the container table, a realistic nearby value rather than a deletion

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_codec_table_answers_for_every_container_it_declares`

Old text:

```
    "MP3": False,
```

New text:

```
    "MP3": True,
```

### `CODEC_suffix_instead_of_container`

Classify by file suffix rather than by mutagen's container class, which gives the wrong answer for the .m4a this defect produced

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 159 against a baseline of 159
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_classifier_reads_mutagens_container_and_not_the_file_extension`

Old text:

```
    container = type(handle).__name__
```

New text:

```
    container = str(path.suffix).lstrip(".").upper()
```

### `CODEC_policy_ignored`

Run the check under every policy, so a permitted lossy acquisition is refused too

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_permitted_lossy_policy_does_not_refuse_the_landing`

Old text:

```
    if policy is not LosslessPolicy.STRICT:
        return path
```

New text:

```
(empty)
```

### `CODEC_refusal_drops_the_codec_name`

Reword the refusal so it no longer names the codec that actually arrived, leaving the reader with a refusal and no fact

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_is_refused_and_the_refusal_names_the_codec`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`

Old text:

```
            f"the provider was asked for lossless audio and the file that landed "
            f"for {key} is {name}; it is at {path}"
```

New text:

```
            f"the file that landed for {key} was refused by the lossless policy"
```

### `CODEC_refused_track_sinks_the_run`

Escalate a lossy landing to an adapter failure, the shape that raises an uncaught ValueError when a delisted track landed earlier in the same batch

- File: `src/cratekit/acquire/adapter.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`

Old text:

```
        return TrackResult(
            key=request.key,
            outcome=TrackOutcome.REFUSED_BY_POLICY,
            detail=str(exc),
            remedy=exc.remedy,
        )
```

New text:

```
        raise AdapterBroken(str(exc)) from exc
```

### `SAMPLE_skip_reported_as_a_file`

Existing guard: trust the tool's (succeeded, path) pair, which made a silent skip and a real download the same observation

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_download_the_tool_silently_skipped_is_not_reported_as_a_file`
  - `tests/test_adapter_contract.py::test_a_skip_reported_through_the_seam_still_raises`

Old text:

```
    if not ok:
        raise RuntimeError(f"the downloader reported no file for {key}")
```

New text:

```
(empty)
```

### `SAMPLE_permanence_asked_second`

Existing guard: ask the authentication heuristic before the permanence question, so a track whose stream token is missing aborts the whole run

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_vendored_source_escalates_a_dead_session_but_not_a_dead_track`

Old text:

```
    if classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT:
        return
    if is_authentication_failure(exc):
```

New text:

```
    if is_authentication_failure(exc):
```

### `SAMPLE_quality_equality`

Existing guard: compare the quality string for equality rather than matching, so a new lossless tier upstream starts being refused

- File: `src/cratekit/acquire/vendored.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_the_clients_quality_vocabulary[HI_RES_LOSSLESS-True]`

Old text:

```
        return Offer(lossless="LOSSLESS" in quality.upper(), detail=quality)
```

New text:

```
        return Offer(lossless=quality.upper() == "LOSSLESS", detail=quality)
```


---

## What the author read off this table

**33 rows, 33 killed, no zero row.** The null control killed 0 against a 6515
collected baseline, which is what makes the rest of these numbers mean anything.

**This is an author's table and is therefore a draft, not a result.** METHOD says
so and this project has measured the gap: every fix agent here has run its table
honestly and still missed guards its own round created, because it mutates what
it believes it changed. Measured gaps between an author's table and an
independent one on this repository: 10 against 17, 39 against 49, 49 against 83.

**One row was zero on its first measurement and is the most useful row here.**
`CODEC_suffix_instead_of_container` swaps mutagen's container class for the file
extension, and on the first run it killed nothing against the full 6514 collected
suite. The reason is worth writing down because it is not "the guard is
untested": `mutagen.File()` resolves its class from the EXTENSION as well as the
header, so for every container this product can land the two spellings agree and
the mutation is equivalent. WAV is the one exception, and only the one:
mutagen names the class `WAVE` while the file is called `.wav`. A classifier keyed
on the suffix would look correct everywhere and refuse a genuine WAV as
unreadable. The gap was closed rather than documented, with a test that lands a
real WAV, and the row then killed 1. The zero was a real hole, not an artifact.

**Three rows were considered and dropped**, and each is recorded in the rows file
with its reason rather than left silent, because a truncation nobody logged reads
as coverage. None was dropped for budget; all three were ranked below rows that
measure the same guard family.

**The driver was killed twice mid-row by the harness**, once in each of the first
two attempts, and both times it left a mutated file on disk AND a poisoned
`__pycache__`. The second is the one that cost time: the next run read a red
baseline naming a test that had nothing to do with the change, and
`PYTHONDONTWRITEBYTECODE=1` does not help, because it stops the driver's own runs
from writing bytecode and does nothing about what an earlier killed run already
wrote. Restoring the file is not enough. Purge `__pycache__` as well, and verify
the restore against `git show HEAD:<path>` rather than against anything on disk.
