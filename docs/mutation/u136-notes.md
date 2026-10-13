# U136 author mutation notes

Capped hunt over the posted-day naming form. Driven against the suite on this
branch; rows that killed nothing are residuals here, not blockers.

| id | surface | change | killed |
| --- | --- | --- | --- |
| A1 | batch_name.set_playlist_form | drop the day argument, hardcode today | test_a_backfill_a_week_later_recomputes_the_same_posted_name |
| A2 | naming_day | ignore --posted, always use page | test_posted_flag_wins_over_the_page_upload_date |
| A3 | naming_day | ignore page, always landing | test_a_job_with_upload_date_names_playlists_for_the_posted_day |
| A4 | naming_day | no warning on landing fallback | test_a_job_without_upload_date_names_for_the_landing_day_and_warns |
| A5 | plan_for_backfill | always use today() for the name | test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day |
| A6 | _job_for_inspiration_name | match today only | test_job_for_inspiration_name_matches_a_set_from_another_day |
| A7 | playlist_name | month with leading zero | test_the_name_is_the_source_systems_form_to_the_character |
| A8 | batch_name.readable | use posted day for INBOX | test_the_inbox_batch_name_is_unchanged_by_the_posted_day |
| A9 | plan on= pin | re-resolve from page and drop on | test_a_pinned_naming_day_keeps_a_posted_override_over_the_page |
| A10 | --posted parse | accept YYYY-MM | test_a_posted_flag_that_is_not_a_day_is_refused_by_name |

All ten killed. No zero-death row kept in the table.
