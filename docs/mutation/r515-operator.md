# Mutation table: r515-operator

Measured by `scripts/mutate.py` on 2026-10-10 05:19 UTC, branch `HEAD` at `e8d46aa`. Pass kind: light.

Baseline: green, 13016 collected. pytest invocations for this batch: 22.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (365158 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13016 against 13016. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S1_of_takes_bool` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 172 | 1 | killed |
| `S2_of_takes_non_int` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 172 | 1 | killed |
| `S3_of_takes_non_positive` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 13016 | 0 (promoted) | zero |
| `S4_of_short_at_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 172 | 1 | killed |
| `S5_of_short_over_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 172 | 1 | killed |
| `S6_cache_drops_short` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 55 | 1 | killed |
| `S7_adapter_no_count` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 172 | 1 | killed |
| `S8_short_of_keeps_zero` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 55 | 1 | killed |
| `S9_question_no_short` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 55 | 1 | killed |
| `S10_intake_all_withheld_quiet` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `S11_intake_playlist_no_warning` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 72 | 6 | killed |
| `S12_sweep_no_withheld_block` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 106 | 1 | killed |
| `S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 106 | 1 | killed |
| `S14_harvest_no_warning` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |

## Zero rows and what they owe

- `S3_of_takes_non_positive` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `S1_of_takes_bool`

Let ListingShortfall.of trust a bool as a declared count

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[True]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if not isinstance(declared, int) or declared <= 0:
```

### `S2_of_takes_non_int`

Let ListingShortfall.of trust a count that is not an integer

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[10]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if isinstance(declared, bool) or declared is None or declared <= 0:
```

### `S3_of_takes_non_positive`

Let ListingShortfall.of trust a zero or negative count

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 13016 against a baseline of 13016
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if isinstance(declared, bool) or not isinstance(declared, int):
```

### `S4_of_short_at_count`

Mint a shortfall when the listing reaches the count exactly

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_full_release_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed > declared:
```

### `S5_of_short_over_count`

Mint a shortfall when the listing runs past the count

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_that_serves_more_than_its_declared_count_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed == declared:
```

### `S6_cache_drops_short`

The caching release reader stores the rows and year but drops the shortfall

- File: `src/cratekit/label/catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
        answer = (tuple(rows), year, short)
```

New text:

```
        answer = (tuple(rows), year, None)
```

### `S7_adapter_no_count`

The release adapter ignores the album's num_tracks

- File: `src/cratekit/label/tidal_catalogue.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`

Old text:

```
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
```

New text:

```
        short = None
```

### `S8_short_of_keeps_zero`

Read a saved shortfall block back even when it withheld nothing

- File: `src/cratekit/label/sync_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall`

Old text:

```
    if any(value is None for value in block.values()) or not block["withheld"]:
```

New text:

```
    if any(value is None for value in block.values()):
```

### `S9_question_no_short`

The label sync question drops the release shortfall

- File: `src/cratekit/label/sync_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
    if question.provider_withheld:
```

New text:

```
    if False:
```

### `S10_intake_all_withheld_quiet`

An intake playlist with every track withheld is a quiet no op

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        if not tracks:
            return ctx.envelope(
                data=_no_op("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
```

New text:

```
        if not tracks:
            return ctx.envelope(
                data=_no_op("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
```

### `S11_intake_playlist_no_warning`

An intake playlist listed short carries no warning

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_playlist_shortfall`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_shortfall`

Old text:

```
        warnings = (warned(short),) if short is not None else ()
```

New text:

```
        warnings = ()
```

### `S12_sweep_no_withheld_block`

The sync all sweep records no shortfall per playlist

- File: `src/cratekit/sync/playlists.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
            sweep.short[playlist.playlist_id] = short.block()
```

New text:

```
            pass
```

### `S13_sweep_no_warning`

The sync all sweep says nothing of a short playlist

- File: `src/cratekit/sync/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
    if sweep.short:
```

New text:

```
    if False:
```

### `S14_harvest_no_warning`

A harvest over a short playlist carries no warning

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`

Old text:

```
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
```

New text:

```
        warnings=(),
```

