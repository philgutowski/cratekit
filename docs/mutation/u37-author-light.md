# Mutation table: u37-author-light

Measured by `scripts/mutate.py` on 2026-08-17 14:11 UTC, branch `unit/u37-intake-pipeline-recognition-ingest-taggi` at `2ddbf05`. Pass kind: light.

Baseline: green, 6004 collected. pytest invocations for this batch: 11.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6004 against 6004. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_stub_listing` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 17 | 1 | killed |
| `G2_recognition_gate` | `src/cratekit/intake/recognize.py` | user | 1 file(s) | 10 | 2 | killed |
| `G3_gridless_bpm` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 42 | 1 | killed |
| `G4_staging` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 10 | 1 | killed |
| `G5_path_repair_queue` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 150 | 3 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `G7_lossy_policy`: Permit unmarked lossy under strict policy Dropped because: ranked below the cap: decide_lossless already has its own U15 table
- `G8_inherited_location`: Re-encode an inherited Location Dropped because: ranked below the cap: KTD27 is already pinned in tests/test_locations.py
- `G9_close_session`: Call close_session from intake Dropped because: the AST guard is the test; a mutation that adds a call is a rewrite not a revert

## Row definitions

### `G1_stub_listing`

Treat a U22 stub listing as a spliceable Fresh Export

- File: `src/cratekit/intake/collection_xml.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`

Old text:

```
    if is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

New text:

```
    if False and is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

### `G2_recognition_gate`

Skip the recognition presence gate

- File: `src/cratekit/intake/recognize.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_a_missing_recognition_key_is_reported_before_any_spend`
  - `tests/intake/test_pipeline.py::test_identification_only_downloads_nothing_and_writes_a_tracklist`

Old text:

```
    missing = recognition_ready()
    if not missing:
        return
    raise refuse(
```

New text:

```
    missing = recognition_ready()
    if True:
        return
    raise refuse(
```

### `G3_gridless_bpm`

Write a real AverageBpm instead of the gridless constant

- File: `src/cratekit/intake/collection_xml.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_the_gridless_constant_even_when_bpm_is_present`

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="124.00"
```

### `G4_staging`

Allow inbox of files still under download staging

- File: `src/cratekit/intake/ingest.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_staging_files_are_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False and (resolved == staging or staging in resolved.parents):
```

### `G5_path_repair_queue`

Offer path repair into the adoption queue instead

- File: `src/cratekit/intake/repair.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/intake/test_repair.py`
- Collected: 150 against a baseline of 150
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_repair.py::test_offer_repairs_writes_path_repair_queue_items`
  - `tests/test_review_queue.py::test_every_new_adjudication_surface_is_owed_by_a_registered_unit`
  - `tests/test_review_queue.py::test_the_path_repair_pass_offers_its_proposals_into_the_path_repair_queue`

Old text:

```
            queue=Queue.PATH_REPAIR,
```

New text:

```
            queue=Queue.ADOPTION,
```

