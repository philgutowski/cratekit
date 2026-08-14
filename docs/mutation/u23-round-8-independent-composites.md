# Mutation table: u23-round-8-independent-composites

Measured by `scripts/mutate.py` on 2026-08-14 14:21 UTC, branch `unit/u23-library-adoption` at `83ae047`. Pass kind: full.

Baseline: green, 3801 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3801 against 3801. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `X6_adoptable_widens_to_online_only__rerun` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 1 | killed |
| `X6_composite_excluded_becomes_routed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 3 | killed |

## Row definitions

### `X6_adoptable_widens_to_online_only__rerun`

The X6 row again, now that a guard test for it exists. Was zero against the branch as delivered.

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption_hardware.py::test_a_cloud_backed_track_on_a_fat_volume_is_EXCLUDED_and_never_applicable`

Old text:

```
ADOPTABLE: frozenset[Readability] = frozenset({Readability.READABLE})
```

New text:

```
ADOPTABLE: frozenset[Readability] = frozenset(
    {Readability.READABLE, Readability.ONLINE_ONLY}
)
```

### `X6_composite_excluded_becomes_routed`

What X6 holds: the EXCLUDED disposition itself, forced to ROUTE

- File: `src/cratekit/adopt/scan.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 3 (killed)
- Composite for: `X6_adoptable_widens_to_online_only__rerun`
- Killed:
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`
  - `tests/test_adoption_hardware.py::test_a_cloud_backed_track_on_a_fat_volume_is_EXCLUDED_and_never_applicable`

Old text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue

```

New text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.ROUTE,
                genre=row.genre,
            )
            continue

```

