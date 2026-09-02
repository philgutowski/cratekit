# Mutation table: u51-item-derivation

Measured by `scripts/mutate.py` on 2026-09-02 16:03 UTC, branch `relay/69` at `bd147d0`. Pass kind: light.

Baseline: green, 6634 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6634 against 6634. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_unknown_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 2 | killed |
| `D2_ambiguous_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 1 | killed |
| `D3_empty_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 1 | killed |
| `D4_dangling_reported` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 2 | killed |
| `D5_repeated_deduped` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 2 | killed |
| `D6_export_required` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 2 | killed |
| `H1_export_item_not_payload` | `src/cratekit/export/cli.py` | user | 1 file(s) | 51 | 9 | killed |
| `H2_hearts_item_not_payload` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 51 | 8 | killed |
| `H3_frozen_config_ignored` | `src/cratekit/export/cli.py` | user | 1 file(s) | 51 | 1 | killed |
| `H4_item_absent_silent` | `src/cratekit/export/cli.py` | user | 1 file(s) | 51 | 1 | killed |
| `S1_resume_closed_job` | `src/cratekit/modules/outbound/shell.py` | user | full suite | 6634 | 6 | killed |
| `S2_resume_cancelled_only` | `src/cratekit/modules/outbound/shell.py` | user | full suite | 6634 | 1 | killed |
| `S3_empty_job_driven` | `src/cratekit/modules/outbound/shell.py` | user | full suite | 6634 | 1 | killed |
| `S4_digest_drops_tracks` | `src/cratekit/export/cli.py` | user | 1 file(s) | 51 | 1 | killed |
| `S5_payload_shape` | `src/cratekit/modules/outbound/shell.py` | user | full suite | 6634 | 32 | killed |
| `L1_reserve_lock_last` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 62 | 1 | killed |
| `A1_no_colour_writer` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 6634 | 0 (promoted) | zero |
| `A2_default_favorites_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 67 | 14 | killed |
| `A1b_colour_writer_passed` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 51 | 1 | killed |

## Zero rows and what they owe

- `A1_no_colour_writer` (user facing): paired with `A1b_colour_writer_passed`, which killed 1

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `D7_memo_invalidation`: Drop the per process export memo so every item reparses the document Dropped because: a performance shape rather than a guard: removing it changes no answer, so a zero row would be correct and would say nothing
- `S6_queue_warnings_unbound`: Drop the unbound provider warning from the queued envelope Dropped because: ranked below the cap; the same warning family as A2, which is measured, and its branch is now driven by two tests
- `L2_record_track_dedup`: Let record_playlist_track append a remote id it already holds Dropped because: engine lines this unit did not write and whose input it does not newly reach: apply already filters on playlist_added before calling it

## Row definitions

### `D1_unknown_playlist`

Drop the refusal for a playlist name the document does not carry

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_that_is_a_folder_refuses_rather_than_resolving`
  - `tests/test_outbound_workers.py::test_an_export_naming_a_playlist_the_document_lacks_queues_nothing`

Old text:

```
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder "
            f"of that name is not a match either, because a folder holds "
            f"playlists rather than tracks",
            steps=(
                "name the playlist by its display name, or by its full path "
                "joined with /",
            ),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": wanted},
        )

```

New text:

```
(empty)
```

### `D2_ambiguous_playlist`

Take the first match instead of refusing when several carry the name

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_two_playlists_carry_refuses_and_names_both_paths`

Old text:

```
    if len(matched) > 1:
```

New text:

```
    if False:
```

### `D3_empty_playlist`

THE ZERO ITEM RULE: let a playlist with no writable track queue

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `D4_dangling_reported`

Stop reporting a TrackID the playlist names and the collection lacks

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_dangling_track_id_is_reported_and_not_queued`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
            dangling.append(track_id)
            continue
```

New text:

```
            continue
```

### `D5_repeated_deduped`

Queue a repeated identifier twice instead of once

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_repeated_track_id_becomes_one_item`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
        if track_id in seen:
```

New text:

```
        if False:
```

### `D6_export_required`

Let a verb queue with no export document named

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[export.playlist]`
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[sync.favorites]`

Old text:

```
    if not text:
```

New text:

```
    if False:
```

### `H1_export_item_not_payload`

The export handler reads the playlist key as its track, not the claimed item

- File: `src/cratekit/export/cli.py`
- Surface: user
- Subset: test files importing cratekit.export.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_ledger_that_cannot_be_read_stops_the_write_rather_than_duplicating`
  - `tests/test_outbound_workers.py::test_a_relative_export_argument_still_resumes`
  - `tests/test_outbound_workers.py::test_a_second_export_of_the_same_playlist_adds_nothing_and_creates_nothing`
  - `tests/test_outbound_workers.py::test_an_export_runs_pending_to_done_and_its_artifact_reads_back`
  - `tests/test_outbound_workers.py::test_an_export_the_provider_matches_nothing_of_says_so_in_the_envelope`
  - `tests/test_outbound_workers.py::test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing`
  - `tests/test_outbound_workers.py::test_the_envelope_names_the_tracks_the_provider_could_not_match`
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[export.playlist]`

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
```

### `H2_hearts_item_not_payload`

The sweep handler reads the playlist key as its row, not the claimed item

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: test files importing cratekit.favorites.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sweep_reaches_nothing_outside_the_add_only_protocol`

Old text:

```
    report = run_heart_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_heart_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
```

### `H3_frozen_config_ignored`

KTD9: the export handler loads a fresh configuration instead of using the frozen one

- File: `src/cratekit/export/cli.py`
- Surface: user
- Subset: test files importing cratekit.export.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[export.playlist]`

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(
        payload, str(item.item_id), config.load(), account.resolve(cfg)
    )
```

### `H4_item_absent_silent`

An item whose track left the frozen export writes nothing and reports done

- File: `src/cratekit/export/cli.py`
- Surface: user
- Subset: test files importing cratekit.export.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing`

Old text:

```
    if not tracks:
        raise refuse(
            "outbound-item-absent",
```

New text:

```
    if False:
        raise refuse(
            "outbound-item-absent",
```

### `S1_resume_closed_job`

R-225: report a closed failed or cancelled job through a normal envelope

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: full suite (test files importing cratekit.modules.outbound.shell: none found)
- Collected: 6634 against a baseline of 6634
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing`
  - `tests/test_outbound_workers.py::test_the_resume_of_a_half_failed_export_does_not_exit_ok`
  - `tests/test_outbound_workers.py::test_the_resume_of_a_half_failed_sweep_does_not_exit_ok`

Old text:

```
        if not job.is_open() and job.cause is not None:
            raise CratekitError(job.cause)
```

New text:

```
(empty)
```

### `S2_resume_cancelled_only`

Narrow the same guard back to FAILED, which is the shape the review found

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: full suite (test files importing cratekit.modules.outbound.shell: none found)
- Collected: 6634 against a baseline of 6634
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`

Old text:

```
        if not job.is_open() and job.cause is not None:
```

New text:

```
        if job.state is jobs.JobState.FAILED and job.cause is not None:
```

### `S3_empty_job_driven`

Drive a job with no items, which core.jobs reports as SUCCEEDED

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: full suite (test files importing cratekit.modules.outbound.shell: none found)
- Collected: 6634 against a baseline of 6634
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success`

Old text:

```
            if not jobs.items(store, job.job_id):
```

New text:

```
            if False:
```

### `S4_digest_drops_tracks`

The confirm digest names the file again instead of the write set

- File: `src/cratekit/export/cli.py`
- Surface: user
- Subset: test files importing cratekit.export.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_confirm_does_not_authorise_a_different_track_set_at_the_same_path`

Old text:

```
            # THE TRACK SET, not just the file it came from. A path names where
            # the answer was read; only this names what will be written.
            "tracks": list(tracks),
```

New text:

```
(empty)
```

### `S5_payload_shape`

Put the outbound summary back at the top level, off the declared schema

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: full suite (test files importing cratekit.modules.outbound.shell: none found)
- Collected: 6634 against a baseline of 6634
- Kills: 32 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_dangling_track_is_named_in_the_queued_envelope`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success`
  - `tests/test_outbound_workers.py::test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success`
  - `tests/test_outbound_workers.py::test_a_ledger_that_cannot_be_read_stops_the_write_rather_than_duplicating`
  - `tests/test_outbound_workers.py::test_a_ledger_that_cannot_be_written_creates_no_remote_playlist_at_all`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_queued_export_holds_one_item_per_track`
  - `tests/test_outbound_workers.py::test_a_relative_export_argument_still_resumes`
  - `tests/test_outbound_workers.py::test_a_second_export_of_the_same_playlist_adds_nothing_and_creates_nothing`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_an_export_runs_pending_to_done_and_its_artifact_reads_back`
  - ... and 17 more, see the JSON sidecar

Old text:

```
        "progress": {
            **jobs.progress(store, job.job_id),
            "outbound": dict(summary(cfg, job.job_id)),
        },
```

New text:

```
        "progress": jobs.progress(store, job.job_id),
        "outbound": dict(summary(cfg, job.job_id)),
```

### `L1_reserve_lock_last`

Take the ledger lock AFTER the create, which is the ordering that duplicated

- File: `src/cratekit/modules/outbound/ledger.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.ledger
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_ledger_that_cannot_be_written_creates_no_remote_playlist_at_all`

Old text:

```
    lock = _locked(cfg)
    try:
        record = _load(cfg)["playlists"].get(playlist_key) or {}
        recorded = record.get("remote_id")
        if recorded:
            return str(recorded), False
        remote_id = create()
        _record_playlist_locked(cfg, playlist_key, remote_id)
        return remote_id, True
    finally:
        lock.__exit__(None, None, None)
```

New text:

```
    recorded = playlist_remote_id(cfg, playlist_key)
    if recorded:
        return str(recorded), False
    remote_id = create()
    record_playlist(cfg, playlist_key, remote_id)
    return remote_id, True
```

### `A1_no_colour_writer`

Pass a colour writer to the hearts engine from a queued sweep

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: test files importing cratekit.favorites.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 6634 against a baseline of 6634
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    report = hearts.heart_back(cfg, remote, candidates, colors=None)
```

New text:

```
    report = hearts.heart_back(cfg, remote, candidates)
```

### `A2_default_favorites_playlist`

Default the sweep to the FOLDER name the live library uses

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: test files importing cratekit.modules.outbound.source
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 67 against a baseline of 67
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_job_show_reports_the_bound_worker_for_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_the_default_favourites_playlist_is_the_one_the_fixture_carries`
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_resume_of_a_half_failed_sweep_does_not_exit_ok`
  - `tests/test_outbound_workers.py::test_the_sweep_reaches_nothing_outside_the_add_only_protocol`
  - `tests/test_queued_resume_contract.py::test_the_favorites_intake_run_and_its_gate_run_are_separate_fields`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[sync.favorites]`

Old text:

```
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"
```

New text:

```
DEFAULT_FAVORITES_PLAYLIST = "Favorites"
```

### `A1b_colour_writer_passed`

Pass a REAL colour writer, which A1 could not: colors=None is the engine's own default, so removing the keyword changed nothing

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: test files importing cratekit.favorites.cli
- Ran: `tests/test_outbound_workers.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Composite for: `A1_no_colour_writer`
- Killed:
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`

Old text:

```
    report = hearts.heart_back(cfg, remote, candidates, colors=None)
```

New text:

```
    class _Pink:
        def color_pink(self, row_id):
            return None

        def is_pink(self, row_id):
            return False

    report = hearts.heart_back(cfg, remote, candidates, colors=_Pink())
```

