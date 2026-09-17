# Mutation table: sitting4

Measured by `scripts/mutate.py` on 2026-09-17 16:58 UTC, branch `sitting/tidal-runs` at `7bbc92c`. Pass kind: light.

Baseline: green, 7566 collected. pytest invocations for this batch: 16.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7566 against 7566. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_export_rows_carry_no_isrc` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |
| `G2_heart_rows_carry_no_isrc` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 2 | killed |
| `G3_builders_ignore_the_prefix_map` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |
| `G4_no_fold` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 2 | killed |
| `G5_malformed_value_passed_on` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |
| `G6_shape_prefix_only` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |
| `G7_missing_file_not_checked` | `src/cratekit/modules/outbound/source.py` | maintainer | 2 file(s) | 7566 | 0 (promoted) | zero |
| `G8_remote_host_raises` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |
| `G9_tag_key_wrong` | `src/cratekit/core/tags.py` | user | 1 file(s) | 7566 | 0 (promoted) | zero |
| `G10_absent_root_reads_as_untagged` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 104 | 1 | killed |

## Zero rows and what they owe

- `G7_missing_file_not_checked` (maintainer facing): maintainer facing, composite not required
- `G9_tag_key_wrong` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `G1_export_rows_carry_no_isrc`

local_tracks stops reading the file, the R-355 defect on the export path

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
            artist=entry.artist,
            isrc=isrc_for(entry, root=cfg.library.root, prefix_map=rules),
        )
```

New text:

```
            artist=entry.artist,
            isrc="",
        )
```

### `G2_heart_rows_carry_no_isrc`

heart_candidates stops reading the file, the R-355 defect on the hearts path

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_matches_through_the_isrc_the_file_carries`
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
            row_id=track_id,
            isrc=isrc_for(entry, root=cfg.library.root, prefix_map=rules),
        )
```

New text:

```
            row_id=track_id,
            isrc="",
        )
```

### `G3_builders_ignore_the_prefix_map`

The builders hand the resolver an empty map, so a renamed drive resolves no row (R-372)

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
    return [
        locations.PrefixRule(source_prefix, target)
        for source_prefix, target in cfg.resolved_prefix_map()
    ]
```

New text:

```
    return []
```

### `G4_no_fold`

A hyphenated or lowercase tag value is no longer folded before the shape check

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_matches_through_the_isrc_the_file_carries`
  - `tests/test_outbound_workers.py::test_the_isrc_is_read_through_the_prefix_map_and_folded`

Old text:

```
    folded = re.sub(r"[\s-]", "", raw).upper()
```

New text:

```
    folded = raw
```

### `G5_malformed_value_passed_on`

A value that is not an ISRC is handed to the provider rather than dropped

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_missing_file_or_a_value_that_is_not_an_isrc_reads_as_none`

Old text:

```
    return folded if _ISRC.fullmatch(folded) else ""
```

New text:

```
    return folded
```

### `G6_shape_prefix_only`

The shape check matches a prefix rather than the whole value, so a thirteen character value passes

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_missing_file_or_a_value_that_is_not_an_isrc_reads_as_none`

Old text:

```
    return folded if _ISRC.fullmatch(folded) else ""
```

New text:

```
    return folded if _ISRC.match(folded) else ""
```

### `G7_missing_file_not_checked`

The existence check is dropped, so a gone file reaches the tag reader

- File: `src/cratekit/modules/outbound/source.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 7566 against a baseline of 7566
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not path.is_file():
        return ""
    raw =
```

New text:

```
    raw =
```

### `G8_remote_host_raises`

A location naming another host raises instead of reading as no ISRC

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_location_with_no_local_file_reads_as_no_isrc[remote-host]`

Old text:

```
    except locations.LocationDecodeError:
        return ""
```

New text:

```
    except OSError:
        return ""
```

### `G9_tag_key_wrong`

The ISRC field names the wrong ID3 frame, so AIFF, WAV and MP3 files lose it

- File: `src/cratekit/core/tags.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tags.py`
- Collected: 7566 against a baseline of 7566
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    "isrc": TagSpec("isrc", "TSRC", "----:com.apple.iTunes:ISRC"),
```

New text:

```
    "isrc": TagSpec("isrc", "TXXX:ISRC", "----:com.apple.iTunes:ISRC"),
```

### `G10_absent_root_reads_as_untagged`

The mount guard is removed, so an unplugged volume reads as a library of untagged files and the sweep succeeds unmatched

- File: `src/cratekit/modules/outbound/source.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged`

Old text:

```
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
```

New text:

```
    root = Path(cfg.library.root)
    if True:
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
```

