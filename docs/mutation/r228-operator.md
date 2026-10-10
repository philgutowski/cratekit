# Mutation table: r228-operator

Measured by `scripts/mutate.py` on 2026-10-10 03:27 UTC, branch `HEAD` at `ae62ab9`. Pass kind: light.

Baseline: green, 13012 collected. pytest invocations for this batch: 15.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (365158 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13012 against 13012. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_pink_name_lookup` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `D2_colour_soft_delete` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `D3_content_soft_delete` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `D4_union_playlist_first` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `D5_pink_missing_dropped` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `D6_empty_after_colour` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `D7_colour_unread_warned` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `D8_from_colour_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 5 | killed |
| `D9_from_playlist_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `D10_pink_warning_gone` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 13 | 1 | killed |
| `D11_non_pink_outside` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `D12_missing_pink_queued` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |

## Row definitions

### `D1_pink_name_lookup`

pink_colour_id: hard code ColourID 1 instead of looking up Pink by name

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_colour_id_looks_up_by_name_and_skips_soft_deleted`
  - `tests/test_favorites_pink.py::test_pink_colour_id_refuses_when_no_live_pink_row`

Old text:

```
    for row in db.get_color(Commnt=PINK_COLOUR_NAME):
        if trees.soft_delete_marker(row):
            continue
        return str(row.ID)
    raise refuse(
        PINK_COLOUR_MISSING,
```

New text:

```
    return "1"
    raise refuse(
        PINK_COLOUR_MISSING,
```

### `D2_colour_soft_delete`

pink_colour_id: keep a soft deleted Pink row as the live ColourID

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_colour_id_looks_up_by_name_and_skips_soft_deleted`
  - `tests/test_favorites_pink.py::test_pink_colour_id_refuses_when_no_live_pink_row`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        return str(row.ID)
```

New text:

```
        return str(row.ID)
```

### `D3_content_soft_delete`

pink_content_ids: keep a soft deleted pink content row in the colour source

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_content_ids_skips_soft_deleted_and_non_pink`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        if str(getattr(row, "ColorID", "") or "") == pink:
```

New text:

```
        if str(getattr(row, "ColorID", "") or "") == pink:
```

### `D4_union_playlist_first`

union_with_pink: emit pink only rows before playlist members

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
    for track_id in playlist.track_ids:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    for track_id in in_export:
```

New text:

```
    for track_id in in_export:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    for track_id in playlist.track_ids:
```

### `D5_pink_missing_dropped`

union_with_pink: drop pink rows the export lacks instead of naming them

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
        else:
            missing.append(track_id)
```

New text:

```
        else:
            pass
```

### `D6_empty_after_colour`

resolve_sweep: read colour before resolving the playlist, so empty All Favorites is rescued by pink

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_refuses_empty_favorites_before_colour`

Old text:

```
    library = source.read_library(exported)
    resolved = source.resolve(library, wanted)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    library = source.read_library(exported)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    try:
        resolved = source.resolve(library, wanted)
    except Exception:
        resolved = source.ResolvedPlaylist(key=wanted, name=wanted, track_ids=())
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `D7_colour_unread_warned`

resolve_sweep: swallow a colour read refusal and sweep the playlist alone

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_propagates_the_colour_reads_own_cause`

Old text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        try:
            pink_ids = read_pink_track_ids(loaded)
        except Exception:
            pink_ids = ()
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `D8_from_colour_zero`

union_with_pink: always report from_colour as zero

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_colour=len(in_export),
```

New text:

```
        from_colour=0,
```

### `D9_from_playlist_zero`

union_with_pink: always report from_playlist as zero

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_playlist=len(playlist.track_ids),
```

New text:

```
        from_playlist=0,
```

### `D10_pink_warning_gone`

queue_warnings: drop the pink missing warning

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
    if resolved.pink_missing:
        warnings.append(
            {
                "code": "favorites-pink-export-missing",
                "message": (
                    f"{len(resolved.pink_missing)} pink row(s) the library "
                    f"carries are not in the export's collection and are not "
                    f"queued: {', '.join(resolved.pink_missing)}"
                ),
            }
        )

```

New text:

```
(empty)
```

### `D11_non_pink_outside`

union_with_pink: queue every export row, not only pink and playlist

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
    for track_id in in_export:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    return replace(

```

New text:

```
    for track_id in library.entries:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    return replace(

```

### `D12_missing_pink_queued`

union_with_pink: queue pink rows the export lacks

- File: `src/cratekit/favorites/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
    for track_id in pink_ids:
        if track_id in library.entries:
            in_export.append(track_id)
        else:
            missing.append(track_id)

```

New text:

```
    for track_id in pink_ids:
        in_export.append(track_id)

```

