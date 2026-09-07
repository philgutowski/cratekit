# Mutation table: u56-catalogue-searcher-and-tag-workers

Measured by `scripts/mutate.py` on 2026-09-07 19:44 UTC, branch `relay/74` at `5402ff8`. Pass kind: full.

Baseline: green, 6781 collected. pytest invocations for this batch: 35.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6781 against 6781. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R1_fallback_order` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R2_unreachable_counts_as_an_answer` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 3 | killed |
| `R3_parse_break_folds_into_unreachable` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 2 | killed |
| `R4_nothing_answered_declines` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 3 | killed |
| `R5_bare_alias_lookup` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 7 | killed |
| `R6_too_coarse_guard` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R7_pacer_does_not_sleep` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 3 | killed |
| `R8_no_jitter` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R9_minimum_interval_halved` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 6781 | 0 (promoted) | zero |
| `R10_no_backoff_growth` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R11_no_attempt_cap` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R12_no_request_timeout` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 5 | killed |
| `R13_query_unescaped` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 96 | 1 | killed |
| `R14_walk_unsorted` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 126 | 3 | killed |
| `R15_walk_not_recursive` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 126 | 2 | killed |
| `R16_fill_if_empty_dropped` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 126 | 4 | killed |
| `R17_unmapped_reads_as_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 126 | 2 | killed |
| `R18_folder_pass_walks_itself` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 6781 | 0 (promoted) | zero |
| `R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | full suite | 6781 | 8 | killed |
| `R20_unnamed_folder_sweeps_cwd` | `src/cratekit/tagging/cli.py` | user | full suite | 6781 | 1 | killed |
| `R21_two_zeroes_read_as_one` | `src/cratekit/tagging/cli.py` | user | full suite | 6781 | 1 | killed |
| `R22_vanished_file_reports_done` | `src/cratekit/tagging/cli.py` | user | full suite | 6781 | 1 | killed |
| `R23_summary_from_the_queue` | `src/cratekit/tagging/cli.py` | user | full suite | 6781 | 3 | killed |
| `R24_resume_digests_a_fresh_walk` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 6 (promoted) | killed |
| `R25_digest_drops_the_folder` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 43 | 2 | killed |
| `R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 12 (promoted) | killed |
| `R27_empty_plan_skips_the_gate` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 17 (promoted) | killed |
| `R28_worker_trusts_the_frozen_row` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 1 (promoted) | killed |
| `R29_blank_genre_is_corrected` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 1 (promoted) | killed |
| `R30_specific_genre_is_overwritten` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 2 (promoted) | killed |
| `R31_artifact_drops_the_previous_value` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 6781 | 1 (promoted) | killed |
| `R32_r225_predicate_narrowed` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 49 | 1 | killed |
| `R33_no_op_job_id_is_null` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 49 | 8 | killed |
| `R34_empty_job_is_driven` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 49 | 1 | killed |
| `R35_extra_rides_beside_progress` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 49 | 15 | killed |
| `R36_artifact_sorted_as_text` | `src/cratekit/tagging/artifacts.py` | user | 1 file(s) | 49 | 1 | killed |
| `R37_artifact_named_by_item_id` | `src/cratekit/tagging/artifacts.py` | user | 1 file(s) | 49 | 1 | killed |
| `R38_staging_not_cleared` | `src/cratekit/tagging/artifacts.py` | user | 1 file(s) | 49 | 1 | killed |
| `R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 197 | 10 | killed |
| `R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 197 | 13 | killed |

## Zero rows and what they owe

- `R9_minimum_interval_halved` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R18_folder_pass_walks_itself` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `R1_fallback_order`

Reverse the fallback order, so Bandcamp answers before Beatport

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`

Old text:

```
_SEARCHES = (_search_beatport, _search_traxsource, _search_bandcamp)
```

New text:

```
_SEARCHES = (_search_bandcamp, _search_traxsource, _search_beatport)
```

### `R2_unreachable_counts_as_an_answer`

METHOD's first pattern: an unreachable source reads as a miss, so a catalogue that was down reports as a catalogue that has never heard of the track

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal`
  - `tests/test_catalogue_searcher.py::test_a_source_that_never_answered_raises_rather_than_declining`
  - `tests/test_catalogue_searcher.py::test_a_traxsource_page_holding_rows_the_parser_cannot_read_is_a_parse_break`

Old text:

```
    if any(outcome.answer is Answer.MISS for outcome in outcomes):
        return None
```

New text:

```
    if any(
        outcome.answer in {Answer.MISS, Answer.UNREACHABLE} for outcome in outcomes
    ):
        return None
```

### `R3_parse_break_folds_into_unreachable`

The same mistake one layer along: a moved page shape reports as a network problem, which is a permanent state wearing a transient remedy

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal`
  - `tests/test_catalogue_searcher.py::test_a_traxsource_page_holding_rows_the_parser_cannot_read_is_a_parse_break`

Old text:

```
    broken = [outcome for outcome in outcomes if outcome.answer is Answer.PARSE_BREAK]
    if broken:
```

New text:

```
    broken: list[SourceOutcome] = []
    if broken:
```

### `R4_nothing_answered_declines`

A searcher no source answered returns None, so every item of a job reports done over answers nobody got

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal`
  - `tests/test_catalogue_searcher.py::test_a_source_that_never_answered_raises_rather_than_declining`
  - `tests/test_catalogue_searcher.py::test_a_traxsource_page_holding_rows_the_parser_cannot_read_is_a_parse_break`

Old text:

```
    if any(outcome.answer is Answer.MISS for outcome in outcomes):
        return None

    broken
```

New text:

```
    return None

    broken
```

### `R5_bare_alias_lookup`

The defect the document review found: hand roll the resolution out of tagging_alias instead of routing.suggest_tag, which loses the sub display and every declared refusal

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 7 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_matched_track_whose_genre_is_declined_still_names_the_raw_string`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_that_aliases_to_a_sub_resolves_to_the_subs_display`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_that_aliases_to_the_fallback_bucket_declines`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_the_taxonomy_refuses_outright_declines[electronic]`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_the_taxonomy_refuses_outright_declines[electronica]`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_the_taxonomy_refuses_outright_declines[techno]`
  - `tests/test_catalogue_searcher.py::test_a_source_genre_with_surrounding_whitespace_resolves_the_same_as_the_trimmed_one`

Old text:

```
    suggestion = routing.suggest_tag(declared, outcome.source_genre)
    tag = suggestion.tag
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
        tag = None
```

New text:

```
    hit = declared.tagging_alias(outcome.source_genre.casefold())
    tag = declared.bucket(hit[0]).display if hit is not None else None
```

### `R6_too_coarse_guard`

Write a suggestion the taxonomy calls too coarse to be a final tag, which launders a catch all into a value tag.retag would never select again

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_genre_that_aliases_to_the_fallback_bucket_declines`

Old text:

```
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
```

New text:

```
    if suggestion.declined or not tag:
```

### `R7_pacer_does_not_sleep`

The pacer reports an interval it never took, so a headless worker hammers a catalogue at full speed

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`
  - `tests/test_catalogue_searcher.py::test_the_pacer_sleeps_before_every_fetch_including_the_first`

Old text:

```
        delay = self.minimum_s * (1.0 + self.entropy.random() * self.jitter_fraction)
        self.sleep(delay)
        return delay
```

New text:

```
        delay = self.minimum_s * (1.0 + self.entropy.random() * self.jitter_fraction)
        return delay
```

### `R8_no_jitter`

Fixed intervals, so two runs that started together stay in step and trip the same limit together

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`

Old text:

```
    jitter_fraction: float = JITTER_FRACTION
```

New text:

```
    jitter_fraction: float = 0.0
```

### `R9_minimum_interval_halved`

Halve the floor between two touches. A bound whose coefficient can be halved with a green suite is not pinned

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 6781 against a baseline of 6781
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
MIN_INTERVAL_S = 1.0
```

New text:

```
MIN_INTERVAL_S = 0.5
```

### `R10_no_backoff_growth`

The 429 wait stops growing with the attempt, so three retries arrive inside one window

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew`

Old text:

```
                    sleep(RATE_LIMIT_BASE_WAIT_S * (attempt + 1))
```

New text:

```
                    sleep(RATE_LIMIT_BASE_WAIT_S)
```

### `R11_no_attempt_cap`

One attempt per fetch, so a single 429 is unreachable and a source that would have answered on the second try never does

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew`

Old text:

```
RATE_LIMIT_ATTEMPTS = 3
```

New text:

```
RATE_LIMIT_ATTEMPTS = 1
```

### `R12_no_request_timeout`

The fetch carries no timeout, so a hung request stalls a job item for ever and looks exactly like work

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_non_200_other_than_429_is_unreachable_rather_than_a_miss`
  - `tests/test_catalogue_searcher.py::test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew`
  - `tests/test_catalogue_searcher.py::test_a_source_that_spends_its_attempts_on_429_is_unreachable`
  - `tests/test_catalogue_searcher.py::test_a_transport_failure_is_unreachable_rather_than_a_miss`
  - `tests/test_catalogue_searcher.py::test_the_default_fetch_passes_its_timeout_to_the_http_getter`

Old text:

```
                response = getter(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_S)
```

New text:

```
                response = getter(url, headers=HEADERS)
```

### `R13_query_unescaped`

An unescaped query truncates at the first ampersand, so a different search is reported as this track's miss

- File: `src/cratekit/tagging/searchers.py`
- Surface: user
- Subset: test files importing cratekit.tagging.searchers
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`

Old text:

```
    return quote_plus(f"{artist} {title}".strip())
```

New text:

```
    return f"{artist} {title}".strip()
```

### `R14_walk_unsorted`

The walk stops sorting, so an enqueue and a later walk disagree about ordinal order and one file's report is filed under another's name

- File: `src/cratekit/tagging/tag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.tag
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 126 against a baseline of 126
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in root.rglob("*")
```

### `R15_walk_not_recursive`

The walk stops recursing, so a folder of subfolders queues nothing and reports the honest zero over a library

- File: `src/cratekit/tagging/tag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.tag
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in sorted(root.glob("*"))
```

### `R16_fill_if_empty_dropped`

tag.folder overwrites a genre somebody curated, which is the field's other owner losing to whichever verb ran last

- File: `src/cratekit/tagging/tag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.tag
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tagging_engine.py::test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten`
  - `tests/test_tagging_engine.py::test_the_folder_pass_asks_once_per_untagged_file`

Old text:

```
    existing = tags.read_genre_from_file(path)
    if existing:
        return TagResult(path=path, genre_written=None, skipped=HAS_GENRE)
```

New text:

```
    existing = None
    if existing:
        return TagResult(path=path, genre_written=None, skipped=HAS_GENRE)
```

### `R17_unmapped_reads_as_no_hit`

The taxonomy gap and the catalogue miss report as one reason, so a person cannot tell which of the two is theirs to fix

- File: `src/cratekit/tagging/tag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.tag
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tagging_engine.py::test_a_catalogue_answer_the_taxonomy_could_not_map_is_its_own_reason`

Old text:

```
        reason = UNMAPPED_GENRE if hit.source_genre else NO_HIT
```

New text:

```
        reason = NO_HIT
```

### `R18_folder_pass_walks_itself`

The sweep derives its own file list instead of audio_files, which is the second opinion KTD7 exists to prevent

- File: `src/cratekit/tagging/tag.py`
- Surface: user
- Subset: test files importing cratekit.tagging.tag
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 6781 against a baseline of 6781
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return [tag_one(path, searcher=searcher) for path in audio_files(root)]
```

New text:

```
    return [
        tag_one(path, searcher=searcher)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in AUDIO_EXTS
    ]
```

### `R19_folder_queues_no_items`

The zero item rule broken at its source: a job with nothing to claim drives straight to SUCCEEDED over a folder nothing walked

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.tagging.cli: none found)
- Collected: 6781 against a baseline of 6781
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - `tests/test_tag_workers.py::test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`

Old text:

```
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
```

New text:

```
            item_ids=(),
```

### `R20_unnamed_folder_sweeps_cwd`

Path("") is the current directory, so an unnamed folder writes genres into whatever the person is standing in

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.tagging.cli: none found)
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`

Old text:

```
    named = str(ctx.args.folder or "")
    if not named.strip():
```

New text:

```
    named = str(ctx.args.folder or "")
    if False:
```

### `R21_two_zeroes_read_as_one`

A mistyped path reports as a folder with nothing to tag, which is the answer most likely to stop somebody looking

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.tagging.cli: none found)
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
```

New text:

```
            if True
            else _empty(
                "tag-folder-absent",
```

### `R22_vanished_file_reports_done`

An item whose file is gone reports done having tagged nothing, which is the clean report over unreadable state the merge bar names

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.tagging.cli: none found)
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`

Old text:

```
    path = folder / item.item_id
    if not path.is_file():
```

New text:

```
    path = folder / item.item_id
    if False:
```

### `R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/cli.py`
- Surface: user
- Subset: full suite (test files importing cratekit.tagging.cli: none found)
- Collected: 6781 against a baseline of 6781
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`

Old text:

```
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

New text:

```
    for report in []:
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

### `R24_resume_digests_a_fresh_walk`

The stall this unit closed: the resume rebuilds the plan, so the first corrected file shrinks the selection and every respawn meets DecisionStale for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 6 (killed)
- Promoted: subset killed 0, full suite killed 6
- Killed:
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_with_a_slug_of_its_own`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
            digest=digest_for(
                str(payload.get(FOLDER_KEY) or ""),
                [dict(row) for row in payload.get(ITEMS_KEY) or ()],
            ),
```

New text:

```
            digest=plan_for(
                str(payload.get(FOLDER_KEY) or ""), taxonomy.default_taxonomy()
            )["digest"],
```

### `R25_digest_drops_the_folder`

Two different empty folders digest identically, so a decision recorded against one satisfies the gate for the other

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`
  - `tests/test_genre_retag.py::test_two_different_empty_folders_digest_differently_through_the_pure_function`

Old text:

```
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
```

New text:

```
            ITEMS_KEY: [dict(row) for row in items],
```

### `R26_retag_queues_no_items`

The zero item rule broken on the second verb, over work somebody explicitly confirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 12 (killed)
- Promoted: subset killed 0, full suite killed 12
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_with_a_slug_of_its_own`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_through_a_retag_fails_only_its_own_item`
  - `tests/test_tag_workers.py::test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue`
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`
  - `tests/test_tag_workers.py::test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre`

Old text:

```
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
```

New text:

```
            item_ids=(),
```

### `R27_empty_plan_skips_the_gate`

The reversal this unit made: an empty plan is not asked about, so a declared gate sometimes does not fire

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 17 (killed)
- Promoted: subset killed 0, full suite killed 17
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[tag.retag]`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_with_a_slug_of_its_own`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_through_a_retag_fails_only_its_own_item`
  - `tests/test_tag_workers.py::test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`
  - `tests/test_tag_workers.py::test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    option = ctx.gate.require(_plan_gate(ctx), digest=plan["digest"])
    if option == "abort":
        return ctx.envelope(data=shell.no_op("declined"), outcome=Outcome.NO_OP)

    if not plan["items"]:
```

New text:

```
    if not plan["items"]:
```

### `R28_worker_trusts_the_frozen_row`

The genre is not re-read at drive time, so a file somebody corrected by hand between the confirmation and the drive is corrected again

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    current = tags.read_genre_from_file(path) or ""
    if not current:
```

New text:

```
    current = tags.read_genre_from_file(path) or ""
    if False:
```

### `R29_blank_genre_is_corrected`

The retag writes into a field tag.folder owns under fill if empty, which is one field under two policies

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

New text:

```
    if current == "\\u0000":
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

### `R30_specific_genre_is_overwritten`

A queued job overwrites somebody's own curation, which is the write this verb exists to avoid making

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 2 (killed)
- Promoted: subset killed 0, full suite killed 2
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
    elif not declared.is_too_coarse_as_source(current):
```

New text:

```
    elif False:
```

### `R31_artifact_drops_the_previous_value`

R-185's only record: without the previous genre the artifacts stop naming which library rows went stale, so the deferred database half has no population to read

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`
- Collected: 6781 against a baseline of 6781
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`

Old text:

```
            "current": result.current,
            "written": result.written,
```

New text:

```
            "written": result.written,
```

### `R32_r225_predicate_narrowed`

R-225 reintroduced: a run stopped with a signal closes CANCELLED, so the narrower predicate hands an interrupted sweep back as a payload and exits 0

- File: `src/cratekit/tagging/shell.py`
- Surface: user
- Subset: test files importing cratekit.tagging.shell
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_cancelled_job_raises_rather_than_reporting_through_a_normal_envelope`

Old text:

```
    if not job.is_open() and job.cause is not None:
```

New text:

```
    if job.state is jobs.JobState.FAILED:
```

### `R33_no_op_job_id_is_null`

R-234 reintroduced: cli.output types job_id as a required string, so a null fails the verb's own schema on every zero path

- File: `src/cratekit/tagging/shell.py`
- Surface: user
- Subset: test files importing cratekit.tagging.shell
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`
  - `tests/test_tag_workers.py::test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing`
  - `tests/test_tag_workers.py::test_the_honest_zero_names_an_empty_job_id_rather_than_a_null`
  - `tests/test_tag_workers.py::test_the_honest_zero_validates_against_the_job_state_surface`

Old text:

```
    return {"job_id": "", "state": state, "cause": None, "progress": {}}
```

New text:

```
    return {"job_id": None, "state": state, "cause": None, "progress": {}}
```

### `R34_empty_job_is_driven`

A job frozen with no items drives straight to SUCCEEDED, which is a clean report over work it never did

- File: `src/cratekit/tagging/shell.py`
- Surface: user
- Subset: test files importing cratekit.tagging.shell
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
        if not jobs.items(store, job.job_id):
```

New text:

```
        if False:
```

### `R35_extra_rides_beside_progress`

A per verb detail at the top level is an undeclared field on job_state/1, so a consumer generated from the committed schema rejects every envelope

- File: `src/cratekit/tagging/shell.py`
- Surface: user
- Subset: test files importing cratekit.tagging.shell
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue`
  - `tests/test_tag_workers.py::test_an_extra_mapping_rides_under_progress_and_never_beside_it`
  - `tests/test_tag_workers.py::test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre`

Old text:

```
    progress = dict(jobs.progress(store, job.job_id))
    if extra:
        progress.update(extra)
    return {
        "job_id": job.job_id,
```

New text:

```
    progress = dict(jobs.progress(store, job.job_id))
    return {
        **dict(extra or {}),
        "job_id": job.job_id,
```

### `R36_artifact_sorted_as_text`

Four digits sort as text in item order and the ten thousandth does not, so a large folder's reports come back out of order

- File: `src/cratekit/tagging/artifacts.py`
- Surface: user
- Subset: test files importing cratekit.tagging.artifacts
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_reports_past_the_four_digit_name_come_back_in_item_order`

Old text:

```
    for path in sorted(directory.glob("*.json"), key=lambda item: int(item.stem)):
```

New text:

```
    for path in sorted(directory.glob("*.json")):
```

### `R37_artifact_named_by_item_id`

A filename built from a tagging item identifier is a path traversal wearing a report, because the identifier is a path relative to a folder

- File: `src/cratekit/tagging/artifacts.py`
- Surface: user
- Subset: test files importing cratekit.tagging.artifacts
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_item_identifier_holding_a_separator_cannot_escape_the_directory`

Old text:

```
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"
```

New text:

```
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal}.json"
```

### `R38_staging_not_cleared`

A half written report from an attempt that did not finish is committed by the next attempt as though it described that attempt

- File: `src/cratekit/tagging/artifacts.py`
- Surface: user
- Subset: test files importing cratekit.tagging.artifacts
- Ran: `tests/test_tag_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_staging_is_cleared_before_an_attempt_writes_into_it`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
    if False:
        shutil.rmtree(directory)
```

### `R39_tag_folder_unbound`

The handler key goes back to declaring no worker, which is the state this whole unit exists to leave

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 10 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - `tests/test_tag_workers.py::test_the_counts_are_read_off_the_artifacts_rather_than_accumulated_in_memory`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_the_tag_folder_key_resolves_to_a_worker`

Old text:

```
    "tag.folder": "cratekit.tagging.cli:handle",
```

New text:

```
(empty)
```

### `R40_tag_retag_unbound`

The same for the correction verb

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 13 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_with_a_slug_of_its_own`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_through_a_retag_fails_only_its_own_item`
  - `tests/test_tag_workers.py::test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue`
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`
  - `tests/test_tag_workers.py::test_the_tag_retag_key_resolves_to_a_worker`
  - `tests/test_tag_workers.py::test_three_confirmed_files_go_from_pending_to_done_and_carry_a_specific_genre`

Old text:

```
    "tag.retag": "cratekit.tagging.retag_cli:handle",
```

New text:

```
(empty)
```


---

# After the pass, added by hand on 2026-09-07

Everything above this line is what `scripts/mutate.py` measured and wrote. This
section was appended afterwards and changes none of the numbers. A regenerated
table drops it, which is correct, because each item below is about this one run
rather than about the rows.

## The pass ran forty rows over a twenty five row cap, deliberately

`docs/METHOD.md` on `main` caps a pass at 25 rows. This spec holds 40 and was
authored under the previous method, which allowed 45 on a full pass. Phillip was
asked and chose to run all forty rather than truncate. The overrun is recorded
here rather than left to be read as coverage, which is what the cap rule asks
for at a truncation, and the same argument applies to an overrun.

**The measured cost of the extra fifteen rows was about twenty five minutes**,
against a full suite of 5 minutes 13 seconds and a subset run of roughly ten
seconds. The rows below the old cap were not the cheap ones: `R24` through `R31`
cover the frozen confirm digest and the retag worker, and `R27` alone killed 17.
Truncating at 25 would have dropped the sharpest rows in the spec, which is the
ranking the cap rule requires you to do before you cut.

## The two zero rows, and the composites they owe

`docs/METHOD.md`: a zero row on a USER FACING guard is acceptable only when a
composite shows what it does hold. Both composites are already in the table, so
no second pass was run. Both counts are reported, as the rule asks.

| zero row | kills | its composite | kills | what the pair says |
| --- | --- | --- | --- | --- |
| `R9_minimum_interval_halved` | 0 | `R7_pacer_does_not_sleep` | 3 | THAT the pacer sleeps is pinned. That its floor is 1.0 second rather than 0.5 is not pinned by anything. |
| `R18_folder_pass_walks_itself` | 0 | `R14_walk_unsorted`, `R15_walk_not_recursive` | 3, 2 | The walk's own behaviour, sorted and recursive, is pinned in `audio_files`. A second copy of that walk inlined into `tag_folder` is not distinguishable from the first. |

`R18` deserves its own sentence, because a zero row is a claim about the mutated
tree and this one is not the claim it looks like. Its mutant reproduces
`audio_files`' body exactly, and the ONLY input the two disagree about is a root
that is not a directory, which `audio_files` answers with an empty tuple and the
mutant would answer by raising. `tag_folder`'s callers exclude that input before
they reach it, `tag.folder` through `folder.is_dir()` and `R21` is the row that
pins it. So this is a true null mutation over every input the suite can reach,
and it kills zero for the same reason the null control does. What it points at
is the duplication rather than a missing guard, and the duplication is R-248.

## One node id in this table no longer exists

`tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_with_a_slug_of_its_own`
appears in the kill lists of four rows. It was RENAMED after this pass, in the
same commit that carries this note, to
`test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`.

The old name was wrong and contradicted this unit's own ledger. The test asserts
the SHARED reserved slug `source-missing`, not a slug of its own, and R-251
records that reuse as the open decision. A name that claims the opposite of the
finding filed beside it is worse than a stale node id in one table, so the name
was corrected and the mapping recorded here.

## The driver exited zero with a mutant still on disk

**Observed, not explained.** After this pass exited with code 0 and reported all
forty rows, `src/cratekit/cli/handlers.py` still held `R40`'s mutation, the one
that deletes the `tag.retag` handler binding. The working tree was clean before
the run, `git status` names the driver as the only writer, and the file's mtime
of 16:48:42 local sits seven seconds BEFORE the driver wrote this table and its
sidecar at 16:48:49, so the last write to it was the driver's own.

**What this did not damage.** `R40` is the last row in the spec, so the
contamination began after every measurement in this table had been taken. The
null control killed zero on the full suite, no row reported collect drift or a
collect error, and `R39` and `R40` killed 10 and 13 against an independent two
row rerun's 10 and 14 on a larger suite. Nothing here was measured against the
mutated tree.

**What was tried.** A two row reproduction, the same two mutations against the
same file on a clean tree, restored correctly and left the tree clean. The
driver's source has exactly two writes to a mutation target, both inside the
`finally` that restores from an in-memory snapshot and then verifies the result
against `git show HEAD:`, and that verification raises rather than warning. So
the mechanism is not visible in the source and was not reproduced. No mechanism
is offered here, because METHOD asks for none without a measurement showing it
operating.

**The mitigation is mechanical and belongs to every future pass**: run
`git status --porcelain` after `scripts/mutate.py` returns, before running the
battery and before trusting any row, and restore from `git show HEAD:<path>`
rather than with a checkout. This is R-256, and
`docs/solutions/workflow-issues/a-mutation-driver-can-exit-clean-and-leave-a-mutant.md`
is the durable form.

A note on one field, because it reads as more than it is: the sidecar's
`head_verified` is set from the driver's INPUT flag, not from the verification's
result, so it records that HEAD verification was requested rather than that it
passed. It is `true` on all forty rows here and that is not evidence the restores
held.
