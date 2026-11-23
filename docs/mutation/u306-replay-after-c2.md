# Mutation table: u306-replay-after-c2

Measured by `scripts/mutate.py` on 2026-11-23 00:43 UTC, branch `HEAD` at `1102a864`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22940 collected. pytest invocations for this batch: 86.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `c919209162e4`, and this tree is at `1102a864ff95`).

Subset baselines: 15, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22940 against 22940. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1476.M5_tag_one_drops_folder_seam` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 286 | 2 | killed |
| `r650-a.B1_searcher_drops_the_flag` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 1 | killed |
| `r650-a.B2_searcher_flags_a_decline` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 1 | killed |
| `r650-a.D2_too_coarse_as_source` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R11_no_attempt_cap` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 5 | killed |
| `u56-catalogue-searcher-and-tag-workers.R3_parse_break_folds_into_unreachable` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 29 | killed |
| `u56-catalogue-searcher-and-tag-workers.R7_pacer_does_not_sleep` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 189 | 6 | killed |
| `u56-catalogue-searcher-and-tag-workers.R8_no_jitter` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 189 | 1 | killed |
| `u85-b.B1_beatport_resized` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 2 | killed |
| `u85-b.B2_edge_coefficient` | `src/cratekit/tagging/shops.py` | maintainer | 3 file(s) | 189 | 2 | killed |
| `u85-b.B3_picture_off_the_winning_row` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 1 | killed |
| `u85-b.B4_only_web_addresses` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 2 | killed |
| `u85-b.B5_bandcamp_original_size` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 2 | killed |
| `u85-b.B6_bandcamp_page_for_art` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 1 | killed |
| `u85-b.B7_listing_genre_wins` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 189 | 1 | killed |
| `u85-b.B9_image_fetch_paced` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 2 | killed |
| `u241.M14_a_changed_file_keeps_its_old_head` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 4 | killed |
| `u241.M15_identity_without_the_time` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M16_changed_settings_keep_old_heads` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 3 | killed |
| `u241.M23_identity_without_the_size` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M24_identity_after_the_read` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M13_vocal_model_not_kept_back` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M19_failed_run_does_not_say_its_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 4 | killed |
| `u241.M20_held_job_records_a_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M21_no_check_line_on_the_answer` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 12 | killed |
| `u241.M25_an_idle_resume_overwrites_the_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M11_cost_from_the_cheapest_track` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 272 | 13 | killed |
| `u241.M22_decode_not_costed` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 272 | 29 | killed |
| `r395.M10_vocals_literal` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 4 | killed |
| `u92-author.G2_cap_is_inclusive` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G3_cap_coefficient` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G4_cap_doubled` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G5_guard_after_the_load` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G6_stat_failure_is_oversize` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 8 | killed |
| `u92-author.G7_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 1 | killed |
| `u92-author.G8_refused_file_tagged_zero` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 2 | killed |
| `u92-author.G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 5 | killed |
| `r185-r246-author.E1_plan_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.E3_empty_plan_queues_anyway` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.M1_folder_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 5 | killed |
| `r185-r246-author.W1_queue_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W2_resume_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W3_resume_warning_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W4_refusal_step_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r185-r246-author.W5_refusal_step_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.W6_refusal_counts_the_plan` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `sitting3.G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 2 | killed |
| `u181.C1_unscored_head_or_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u181.C2_unscored_ignores_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u25.G6_always_rewrite` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D23_vocals_resume_warning` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D25_vocals_join` | `src/cratekit/vocals/cli.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `u282.C1_refused_token_not_counted` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 443 | 1 | killed |
| `u282.C2_refused_token_not_warned` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 443 | 1 | killed |
| `u282.C3_label_genre_counted_as_owed` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 443 | 1 | killed |
| `u276.K5_stages_of_plain_keeps_harmonic` | `src/cratekit/analysis/detect.py` | maintainer | 2 file(s) | 24 | 3 | killed |
| `u276.K6_stages_of_refuses_nothing` | `src/cratekit/analysis/detect.py` | maintainer | 2 file(s) | 24 | 1 | killed |
| `u244.M01_no_token_not_asked` | `src/cratekit/tagging/discogs.py` | user | 5 file(s) | 470 | 11 | killed |
| `u244.M21_passed_over_rides_unread` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 470 | 6 | killed |
| `r791-b.T1_sources_unread_disposition` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 239 | 12 | killed |
| `r791-b.T2_art_names_unread` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 239 | 1 | killed |
| `u167.M22_analysed_reading` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 3 | killed |
| `u294.M26_needing_disposition` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 118 | 5 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `r1534.M17_beatport_empty_credit` | `src/cratekit/tagging/shops.py` | user | 5 file(s) | 1194 | 1 | killed |
| `u84-b.T4_default_unchecked` | `src/cratekit/tagging/tag.py` | maintainer | 2 file(s) | 172 | 1 | killed |

## Row definitions

### `r1476.M5_tag_one_drops_folder_seam`

tag_one: never hand the folder seam to _by_label

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M5_tag_one_drops_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        else _by_label(path, label_genre, label, copyright_labels, folder_genre)
```

New text:

```
        else _by_label(path, label_genre, label, copyright_labels)
```

### `r650-a.B1_searcher_drops_the_flag`

The hit never carries the flag, so nothing above the resolver can see it

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `B1_searcher_drops_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`

Old text:

```
        off_taxonomy=tag is not None and suggestion.off_taxonomy,
```

New text:

```
        off_taxonomy=False,
```

### `r650-a.B2_searcher_flags_a_decline`

A pass through the taxonomy calls too coarse carries the flag as well as declining

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `B2_searcher_flags_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`

Old text:

```
        off_taxonomy=tag is not None and suggestion.off_taxonomy,
```

New text:

```
        off_taxonomy=suggestion.off_taxonomy,
```

### `r650-a.D2_too_coarse_as_source`

Existing: an answer too coarse to be a final tag is a decline, not a hit

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `D2_too_coarse_as_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[acapella]`
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`

Old text:

```
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
```

New text:

```
    if suggestion.declined or not tag:
```

### `u56-catalogue-searcher-and-tag-workers.R11_no_attempt_cap`

One attempt per fetch, so a single 429 is unreachable and a source that would have answered on the second try never does

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R11_no_attempt_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew`
  - `tests/test_catalogue_searcher.py::test_an_image_fetch_that_meets_a_rate_limit_backs_off_like_a_search`

Old text:

```
RATE_LIMIT_ATTEMPTS = 3
```

New text:

```
RATE_LIMIT_ATTEMPTS = 1
```

### `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped`

An unescaped query truncates at the first ampersand, so a different search is reported as this track's miss

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R13_query_unescaped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`

Old text:

```
    return quote_plus(f"{artist} {title}".strip())
```

New text:

```
    return f"{artist} {title}".strip()
```

### `u56-catalogue-searcher-and-tag-workers.R3_parse_break_folds_into_unreachable`

The same mistake one layer along: a moved page shape reports as a network problem, which is a permanent state wearing a transient remedy

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R3_parse_break_folds_into_unreachable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal[beatport payload missing]`
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal[traxsource rows unread]`

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

### `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup`

The defect the document review found: hand roll the resolution out of tagging_alias instead of routing.suggest_tag, which loses the sub display and every declared refusal

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R5_bare_alias_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 29 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_a_beatport_match_carries_the_tag_the_source_name_and_the_raw_genre`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[miss]`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[unreachable]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[acapella]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronic]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronica]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[techno]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[declared tag with no bucket]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[padded genre]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`
  - `tests/test_catalogue_searcher.py::test_a_match_after_an_unreachable_source_names_it_in_unread_too`
  - ... and 14 more, see the JSON sidecar

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

### `u56-catalogue-searcher-and-tag-workers.R7_pacer_does_not_sleep`

The pacer reports an interval it never took, so a headless worker hammers a catalogue at full speed

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R7_pacer_does_not_sleep`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`
  - `tests/test_catalogue_searcher.py::test_the_pacer_sleeps_before_every_fetch_including_the_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

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

### `u56-catalogue-searcher-and-tag-workers.R8_no_jitter`

Fixed intervals, so two runs that started together stay in step and trip the same limit together

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R8_no_jitter`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
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

### `u85-b.B1_beatport_resized`

The Beatport release image URL is asked for at the size the payload named, not the source edge

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B1_beatport_resized`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
    return _BEATPORT_IMAGE_SIZE.sub(f"image_size/{edge}x{edge}/", uri)
```

New text:

```
    return uri
```

### `u85-b.B2_edge_coefficient`

The Beatport edge drops from 1400 to 1200

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B2_edge_coefficient`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
BEATPORT_IMAGE_EDGE = 1400
```

New text:

```
BEATPORT_IMAGE_EDGE = 1200
```

### `u85-b.B3_picture_off_the_winning_row`

The picture is read off the loop's last row rather than the winning row, the wrong cover hazard

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B3_picture_off_the_winning_row`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
    return best


def _search_beatport(
```

New text:

```
    return best and _Pick(best.genre, _beatport_art(track))


def _search_beatport(
```

### `u85-b.B4_only_web_addresses`

A payload value that is not an http or https URL becomes a GET

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B4_only_web_addresses`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_release_picture_that_is_not_a_web_address_is_no_picture[file:///etc/passwd]`
  - `tests/test_catalogue_searcher.py::test_a_release_picture_that_is_not_a_web_address_is_no_picture[javascript:alert(1)]`

Old text:

```
    return text if text.startswith(("https://", "http://")) else ""
```

New text:

```
    return text
```

### `u85-b.B5_bandcamp_original_size`

The Bandcamp picture is asked for at the thumbnail size the page named

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B5_bandcamp_original_size`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
    return _BC_IMAGE_SIZE.sub("_10.jpg", _web_url(found.group(1)))
```

New text:

```
    return _web_url(found.group(1))
```

### `u85-b.B6_bandcamp_page_for_art`

A listing with a genre and no picture never reads the track page's og:image

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B6_bandcamp_page_for_art`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
        if not genre or not art_url:
```

New text:

```
        if not genre:
```

### `u85-b.B7_listing_genre_wins`

The track page's tags overwrite a genre the listing already gave

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B7_listing_genre_wins`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
genre = genre or _bandcamp_tag(
```

New text:

```
genre = _bandcamp_tag(
```

### `u85-b.B9_image_fetch_paced`

The image fetch skips the pace wait, so a folder opens with a burst of picture requests

- File: `src/cratekit/tagging/searchers.py`
- Source: `u85-b.json`, row `B9_image_fetch_paced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    def fetch_image(url: str) -> bytes | None:
        pacer.wait()

```

New text:

```
    def fetch_image(url: str) -> bytes | None:

```

### `u241.M14_a_changed_file_keeps_its_old_head`

ahead: a head measured ahead is used whatever file now sits at the path

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M14_a_changed_file_keeps_its_old_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_replaced_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_in_place_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    if measured_identity is None or measured_identity != identity_of(path):

```

New text:

```
    if False:

```

### `u241.M15_identity_without_the_time`

ahead.identity_of: no modification time, so a file rewritten at the same length keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M15_identity_without_the_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, found.st_size, 0)

```

### `u241.M16_changed_settings_keep_old_heads`

ahead: heads measured under the old calibration are used after it changes

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M16_changed_settings_keep_old_heads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[drift-cut]`
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[tempo-window]`
  - `tests/test_analysis_ahead.py::test_settings_that_changed_mid_run_stop_the_pool_and_the_rest_is_measured_here`

Old text:

```
    if settings != session.settings:
        session.stop(STOPPED_SETTINGS)
        return None

```

New text:

```
(empty)
```

### `u241.M23_identity_without_the_size`

ahead.identity_of: no size, so a file rewritten with its time put back keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M23_identity_without_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, 0, found.st_mtime_ns)

```

### `u241.M24_identity_after_the_read`

ahead.measure: the identity is taken after the read, so a file written while it was read carries the written file's identity

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M24_identity_after_the_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_the_identity_a_worker_returns_is_the_files_before_the_read`

Old text:

```
    found = identity_of(path)
    return found, light.analyse(path)

```

New text:

```
    head = light.analyse(path)
    return identity_of(path), head

```

### `u241.M13_vocal_model_not_kept_back`

_open_ahead: the driver's vocal model is not kept back from the light pool's budget

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M13_vocal_model_not_kept_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`

Old text:

```
        reserve += vocals.VOCAL_WORKER_BYTES
    return ahead.open_session(
```

New text:

```
        pass
    return ahead.open_session(
```

### `u241.M19_failed_run_does_not_say_its_pool`

_resume: a run that failed or was stopped leaves without its pool line

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M19_failed_run_does_not_say_its_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_analysis_ahead.py::test_an_interrupt_during_a_run_ahead_ends_the_workers_and_the_resume_finishes`
  - `tests/test_analysis_ahead.py::test_an_unreadable_calibration_is_each_items_refusal_and_opens_no_pool`

Old text:

```
                if pooled is None:
                    raise
                raise _with_pool(failed, pooled) from failed

```

New text:

```
                raise

```

### `u241.M20_held_job_records_a_pool`

_heads_ahead: a call that drove nothing, because another driver holds the job, records a pool anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M20_held_job_records_a_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_job_another_driver_holds_records_no_pool_and_adds_none_to_the_refusal`

Old text:

```
        drove = False
        raise

```

New text:

```
        raise

```

### `u241.M21_no_check_line_on_the_answer`

_resume: the answer no longer carries the analyze.pool check

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M21_no_check_line_on_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 12 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_closure_bound_by_a_test_is_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_job_whose_record_is_gone_says_it_does_not_know`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_pool_record_that_cannot_be_written_is_a_missing_line_and_never_a_failed_job`
  - `tests/test_analysis_ahead.py::test_a_resume_of_a_finished_job_still_says_what_pool_it_ran_with`
  - `tests/test_analysis_ahead.py::test_a_worker_that_dies_costs_the_run_nothing_but_its_pool`
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`
  - `tests/test_analysis_ahead.py::test_the_person_reads_the_check_line_without_asking_for_json`
  - `tests/test_analysis_ahead.py::test_two_cores_leave_no_ceiling_for_a_pool`

Old text:

```
            summary["checks"] = [_pool_check(artifacts.pool_record(cfg, job.job_id))]

```

New text:

```
(empty)
```

### `u241.M25_an_idle_resume_overwrites_the_pool`

_worth_recording: a drive that measured nothing overwrites the record of the drive that did

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M25_an_idle_resume_overwrites_the_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`

Old text:

```
        return True
    return artifacts.pool_record(cfg, job_id) is None

```

New text:

```
        return True
    return True

```

### `u241.M11_cost_from_the_cheapest_track`

light.costliest: the cheapest track sets the worker's cost

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M11_cost_from_the_cheapest_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

### `u241.M22_decode_not_costed`

light.worker_bytes: the decode's line is dropped, so a 192 kilohertz file is declared at its length alone, 1310 MB where 2180 was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M22_decode_not_costed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 29 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-86400.0]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return LIGHT_BASE_BYTES + max(analysis, decode)

```

New text:

```
    return LIGHT_BASE_BYTES + analysis

```

### `r395.M10_vocals_literal`

Put the old bare pip literal back in the vocals install text

- File: `src/cratekit/analysis/vocals.py`
- Source: `r395.json`, row `M10_vocals_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    return extras.install_command("vocals")
```

New text:

```
    return "pip install 'cratekit[vocals]'"
```

### `u92-author.G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G1_guard_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
(empty)
```

### `u92-author.G2_cap_is_inclusive`

Refuse a file exactly AT the cap, strictly greater becomes greater or equal

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G2_cap_is_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`

Old text:

```
        return Path(path).stat().st_size > VOCAL_MAX_BYTES
```

New text:

```
        return Path(path).stat().st_size >= VOCAL_MAX_BYTES
```

### `u92-author.G3_cap_coefficient`

Megabytes instead of mebibytes, a realistic nearby value off by 4.9 percent

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G3_cap_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 250 * 1000 * 1000
```

### `u92-author.G4_cap_doubled`

Double the cap to 500 mebibytes, which still refuses something and refuses it late

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G4_cap_doubled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 500 * 1024 * 1024
```

### `u92-author.G5_guard_after_the_load`

Move the guard behind the model load, the brief's literal reading, which this unit did not take

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G5_guard_after_the_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

### `u92-author.G6_stat_failure_is_oversize`

A size that cannot be read answers oversize, so a missing file names the wrong remedy

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G6_stat_failure_is_oversize`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    except (OSError, TypeError, ValueError):
        return False

```

New text:

```
    except (OSError, TypeError, ValueError):
        return True

```

### `u92-author.G7_reason_reworded`

Reword the reason slug, never append, since the suite asserts with equality and with in

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G7_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`

Old text:

```
REASON_AUDIO_TOO_LARGE = "vocal-audio-too-large"
```

New text:

```
REASON_AUDIO_TOO_LARGE = "vocal-file-oversize"
```

### `u92-author.G8_refused_file_tagged_zero`

Tag the refused file voxlevel 0 the way the source system did, instead of leaving an absence

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G8_refused_file_tagged_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
    if is_oversize(result.get("path")):
        result = _inactive(result, REASON_AUDIO_TOO_LARGE)
        result["voxlevel"] = 0
        result["voxgender"] = "U"
        result["voxgenderconf"] = 0
        return result

```

### `u92-author.G9_warning_counts_the_wrong_reason`

unscored_warning counts size refusals, so an oversize file is reported as a missing model

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G9_warning_counts_the_wrong_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`
  - `tests/test_analysis_workers.py::test_an_oversize_track_is_never_warned_about_as_a_missing_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
```

New text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_AUDIO_TOO_LARGE, 0))
```

### `r185-r246-author.E1_plan_gate_by_position`

Index gates[0] instead of searching by digest source, the guard the repaired case in test_genre_retag.py measures

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E1_plan_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates[:1]:
        return spec
```

### `r185-r246-author.E3_empty_plan_queues_anyway`

Queue a job over an empty selection, which core.jobs drives straight to SUCCEEDED over a folder nothing touched

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E3_empty_plan_queues_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_queues_nothing_and_says_which_zero[False]`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_queues_nothing_and_says_which_zero[True]`

Old text:

```
    if not plan["items"]:
        payload, warnings = (
```

New text:

```
    if False:
        payload, warnings = (
```

### `r185-r246-author.M1_folder_dropped`

Drop the folder from the instruction, so a person reading one envelope beside others cannot tell which sweep it names

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `M1_folder_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
```

New text:

```
            f"this correction writes the genre onto the files it selected and "
            f"does not update the library rows, which go on carrying the old "
```

### `r185-r246-author.W1_queue_warning_dropped`

The queueing envelope stops naming the reload, so the person walks away told nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W1_queue_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            warnings=(library_row_warning(folder),),

```

New text:

```
(empty)
```

### `r185-r246-author.W2_resume_warning_dropped`

A successful resume stops naming the reload

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W2_resume_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))

```

New text:

```
(empty)
```

### `r185-r246-author.W3_resume_warning_unconditional`

Name the reload on every resume, including one that corrected nothing and made no row stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W3_resume_warning_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
```

New text:

```
        warnings = (*warnings, library_row_warning(folder))
```

### `r185-r246-author.W4_refusal_step_dropped`

A half corrected sweep leaves through its cause with nothing said about the rows it made stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W4_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=("tagging", "retag_cli"),
                nothing_to_run="report a correction over files it never looked at",
            )
        except CratekitError as failed:
            # THE REFUSAL CARRIES THE RELOAD WHEN ANYTHING WAS CORRECTED. The
            # artifacts are committed per item before the failure, so this
            # counts what actually landed rather than what was confirmed, and a
            # sweep that refused on its first item adds nothing to a refusal it
            # has no reload to name. See ``with_reload_step``.
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
        job, warnings = shell.advance(
            ctx,
            store,
            queued,
            origin=("tagging", "retag_cli"),
            nothing_to_run="report a correction over files it never looked at",
        )
```

### `r185-r246-author.W5_refusal_step_unconditional`

Append the reload to every refusal, including one that corrected nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W5_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
            raise with_reload_step(failed, folder) from failed
```

### `r185-r246-author.W6_refusal_counts_the_plan`

Count the confirmed items instead of the committed artifacts, so a sweep that wrote nothing still reports a correction

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W6_refusal_counts_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
```

New text:

```
            if not payload.get(ITEMS_KEY):
                raise
```

### `sitting3.G8_queue_skips_readiness`

File the job whatever is missing, so a restamp scores nothing and reports ok

- File: `src/cratekit/vocals/cli.py`
- Source: `sitting3.json`, row `G8_queue_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return

```

New text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if True:
        return

```

### `u181.C1_unscored_head_or_score`

analyze vocals --unscored: queue a file carrying the head OR no score, so an unheaded file is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C1_unscored_head_or_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.carries_head(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.carries_head(path, cfg) or tags.read_vox_from_file(path) is None:
```

### `u181.C2_unscored_ignores_score`

analyze vocals --unscored: queue every headed file, scored or not

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C2_unscored_ignores_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.carries_head(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.carries_head(path, cfg):
```

### `u25.G6_always_rewrite`

Rewrite vocal tags even when the values did not move

- File: `src/cratekit/vocals/cli.py`
- Source: `u25.json`, row `G6_always_rewrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_an_unchanged_score_is_not_rewritten`

Old text:

```
    if (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

New text:

```
    if True or (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

### `u93-recursive-analysis.D23_vocals_resume_warning`

The vocals resume drops the walk's omissions, the same hole on the other verb

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D23_vocals_resume_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        unscored = _unscored_warning(summary)
```

New text:

```
        unscored = _unscored_warning(summary)
```

### `u93-recursive-analysis.D25_vocals_join`

The vocals worker joins with the operator, the same reversion one file over

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D25_vocals_join`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `u282.C1_refused_token_not_counted`

_summary: a refused token's not-asked is never counted, so the sweep says nothing about it (round two's BLOCKING)

- File: `src/cratekit/tagging/summary.py`
- Source: `u282.json`, row `C1_refused_token_not_counted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                discogs_refused += 1
```

New text:

```
                discogs_refused += 0
```

### `u282.C2_refused_token_not_warned`

_discogs_warnings: the refused token's warning is never raised

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C2_refused_token_not_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
    if refused:
        warnings.append(
```

New text:

```
    if False:
        warnings.append(
```

### `u282.C3_label_genre_counted_as_owed`

_summary: a file whose label gave its genre is counted as having no token, overstating the warning

- File: `src/cratekit/tagging/summary.py`
- Source: `u282.json`, row `C3_label_genre_counted_as_owed`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_the_no_token_count_leaves_out_files_whose_genre_was_their_own_or_their_labels`

Old text:

```
                and str(report.get("source") or "") != tag_engine.LABEL_GENRE
            )
```

New text:

```
            )
```

### `u276.K5_stages_of_plain_keeps_harmonic`

stages_of: answer every stage for plain too, so the stage report counts a separation the plain chroma never ran

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K5_stages_of_plain_keeps_harmonic`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_analysis_key_methods.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_stage_report_under_plain_counts_no_separation`
  - `tests/test_analysis_key_default.py::test_the_stage_totals_under_plain_carry_no_separation_in_the_json_either`
  - `tests/test_analysis_key_default.py::test_the_stages_a_run_times_are_the_methods_own`

Old text:

```
    if method == KEY_PLAIN:
        return tuple(stage for stage in STAGES if stage != "harmonic")
    return STAGES
```

New text:

```
    return STAGES
```

### `u276.K6_stages_of_refuses_nothing`

stages_of: drop the refusal of a method nobody built, so a misspelt method reads as one that separates

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K6_stages_of_refuses_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_analysis_key_methods.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_a_stage_set_for_a_method_nobody_built_is_refused`

Old text:

```
    if method not in KEY_METHODS:
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {method!r}")
    if method == KEY_PLAIN:
```

New text:

```
    if method == KEY_PLAIN:
```

### `u244.M01_no_token_not_asked`

DiscogsAsker.ask: answer MISS for a searcher with no token instead of not-asked, so a sweep with no token records no-hit

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M01_no_token_not_asked`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`, `tests/test_catalogue_searcher.py`, `tests/test_published_genre.py`
- Collected: 470 against a baseline of 470
- Kills: 11 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_recorded_token_the_keychain_lost_is_not_asked_and_says_so`
  - `tests/test_discogs_searcher.py::test_a_searcher_built_with_no_asker_has_no_token_and_reads_no_keychain`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_beatport_unreachable_and_discogs_unasked_refuse_as_an_outage_naming_the_token`
  - `tests/test_discogs_searcher.py::test_no_recorded_token_reads_no_keychain_and_is_not_asked`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`

Old text:

```
        if self.token is None:
            return NotAsked(DISCOGS, self.unasked)
```

New text:

```
        if self.token is None:
            return SourceOutcome(DISCOGS, Answer.MISS)
```

### `u244.M21_passed_over_rides_unread`

_unread_sources: leave a source passed over for want of a token out of unread, so the file reads no-hit

- File: `src/cratekit/tagging/searchers.py`
- Source: `u244.json`, row `M21_passed_over_rides_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`, `tests/test_catalogue_searcher.py`, `tests/test_published_genre.py`
- Collected: 470 against a baseline of 470
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`

Old text:

```
    ) + tuple(skipped.source for skipped in passed)
```

New text:

```
    )
```

### `r791-b.T1_sources_unread_disposition`

tag_one: a decline naming unread sources is reported no-hit

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T1_sources_unread_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        elif hit.unread:
```

New text:

```
        elif False:
```

### `r791-b.T2_art_names_unread`

_art_embedded: the picture decline never names the unread sources

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T2_art_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        unread = hit.unread if hit is not None else ()
```

New text:

```
        unread = ()
```

### `u167.M22_analysed_reading`

read_row: a row the clear would leave waiting is read as analysed

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M22_analysed_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`

Old text:

```
    if one.action != analyzed.CLEAR:
```

New text:

```
    if one.why == analyzed.NOT_ANALYSED:
```

### `u294.M26_needing_disposition`

the census after a step counts every row it scanned, not only the needs genre ones: the one filter needing keeps once its dead checks were taken out

- File: `src/cratekit/tagging/backlog.py`
- Source: `u294.json`, row `M26_needing_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_backlog.py`
- Collected: 118 against a baseline of 118
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_person_reads_the_campaign_and_the_resort_it_leaves`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads`
  - `tests/test_tag_campaign.py::test_needing_counts_only_live_rows_with_a_readable_file`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
        if track.disposition is adopt_scan.Disposition.NEEDS_GENRE
    )
```

New text:

```
        if True
    )
```

### `r1103.H2_refusal_slug`

handle: the item fails under the general analysis-write-failed slug instead of retag's own

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H2_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
        raise refuse(
            retag.UNWRITTEN_REASON,
```

New text:

```
        raise refuse(
            "analysis-write-failed",
```

### `r1534.M17_beatport_empty_credit`

_beatport_best: keep a credit with no name, contained in every searched artist

- File: `src/cratekit/tagging/shops.py`
- Source: `r1534.json`, row `M17_beatport_empty_credit`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`
- Collected: 1194 against a baseline of 1194
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_beatport_reads_no_artist_from_a_row_crediting_an_empty_name`

Old text:

```
        credited = [other for other in credited if other]

```

New text:

```
(empty)
```

### `u84-b.T4_default_unchecked`

A result built without the repair claims the repair passed

- File: `src/cratekit/tagging/tag.py`
- Source: `u84-b.json`, row `T4_default_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_result_built_without_the_repair_does_not_claim_it_passed`

Old text:

```
    art_repair: str = art.REPAIR_UNCHECKED
```

New text:

```
    art_repair: str = art.REPAIR_OK
```

