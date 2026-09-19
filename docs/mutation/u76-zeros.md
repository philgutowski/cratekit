# Mutation table: u76-zeros

Measured by `scripts/mutate.py` on 2026-09-19 07:19 UTC, branch `relay/121` at `be19821`. Pass kind: light.

Baseline: green, 8123 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 8123 against 8123. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `P1_join_pairs` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 203 | 1 | killed |
| `X5_entries_absent` | `src/cratekit/write/rbxml.py` | maintainer | 4 file(s) | 203 | 1 | killed |

## Row definitions

### `P1_join_pairs`

_merged_pairs: keep every pair as given, so a caller naming one playlist twice emits two siblings of that name

- File: `src/cratekit/write/rbxml.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 203 against a baseline of 203
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(name, dedupe_track_ids(ids)) for name, ids in playlists]
```

### `X5_entries_absent`

_extend_playlist: write the ids into a held playlist with no Entries attribute rather than refusing

- File: `src/cratekit/write/rbxml.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 203 against a baseline of 203
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`

Old text:

```
    if entries is None:
        return f"Entries attr not found for playlist {playlist.name!r}"
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    if entries is None:
        entries = (playlist.tag_end, playlist.tag_end)
    total = _read_int(content, entries) + len(fresh) if entries[0] != entries[1] else len(fresh)
```

