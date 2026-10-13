# U136 author mutation notes

Capped hunt over the posted-day naming form, the freeze in `intake set`, the
landing's name read, `export set`'s name match, and the fallback warning.
Rows are `docs/mutation/u136-rows.toml`. The watcher measures on macOS with:

    .venv/bin/python scripts/mutate.py docs/mutation/u136-rows.toml --out-dir docs/mutation

Author read of the first ten rows against the suite on this branch (all
killed at least one listed test). Review round one adds the early freeze
guard, land `--posted` pass through, apply_alone posted carry, and the
driven never-a-twin backfill.

| id | surface | change | killed |
| --- | --- | --- | --- |
| A1 | batch_name.set_playlist_form | drop the day argument, hardcode today | test_a_backfill_a_week_later_recomputes_the_same_posted_name |
| A2 | naming_day | ignore --posted, always use page | test_posted_flag_wins_over_the_page_upload_date |
| A3 | naming_day | ignore page, always landing | test_a_job_with_upload_date_names_playlists_for_the_posted_day |
| A4 | naming_day | no warning on landing fallback | test_a_job_without_upload_date_names_for_the_landing_day_and_warns |
| A5 | plan_for_landing name | always use today() for the name | test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day |
| A6 | _job_for_inspiration_name | match today only | test_job_for_inspiration_name_matches_a_set_from_another_day |
| A7 | set_day_word | month with leading zero | test_the_name_is_the_source_systems_form_to_the_character |
| A8 | batch_name.readable | use posted day for INBOX | test_the_inbox_batch_name_is_unchanged_by_the_posted_day |
| A9 | plan on= pin | re-resolve from page and drop on | test_a_pinned_naming_day_keeps_a_posted_override_over_the_page |
| A10 | --posted parse | accept YYYY-MM | test_a_posted_flag_that_is_not_a_day_is_refused_by_name |
| A11 | intake set freeze | keep early whenever it has a name | test_intake_set_with_all_three_words_freezes_the_page_upload_date |
| A11b | intake set keep early | drop posted guard on keep-early | test_intake_set_with_all_three_words_freezes_the_page_upload_date |
| A12 | land --posted | drop posted= on plan_for_landing | test_a_landing_honours_posted_on_a_pre_freeze_job |
| A13 | apply_alone | drop posted on re-plan | test_posted_equal_to_landing_day_on_a_pageless_job_is_not_decision_stale |
| A14 | backfill name | use today when page has upload_date | test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name |

All fifteen killed on the author's subset run. No zero-death row kept.
