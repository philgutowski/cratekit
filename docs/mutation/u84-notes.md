# U84 mutation tables, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/129`. Every zero row in this record means the
author could not kill it, not that nobody could. The unit writes to audio files
the user owns, so it took the full 25 rows.

**`u84-a.md`**, 12 rows over `core/art.py`'s broken block test, its three
statuses that write nothing, its native resolution rule, its dimension fill,
its all or nothing rule and its unreadable file path. Subset
`tests/test_tagging_engine.py`, `tests/test_tag_workers.py` and
`tests/test_art.py`, 170 collected. Null control 0 of 8440. 11 killed, 1 zero
promoted to the full suite: `A4_undecodable_is_broken`, 0 of 8440. It is user
facing, since reading undecodable bytes as sound reports `ok` over art a player
shows blank, and every corrupt image the suite held sat in a ZEROED block, so
the dimension check caught it first.

**`u84-b.md`**, 13 rows: the save failure path, the kept sound blocks, the
shrink fallback the review asked for and its two limits, the mime rewrite, the
repair running before the has-genre return, the status carried on every
return, the default, the artifact key, the zero filled summary and the old
report rule. Same three files for the art rows, the two tagging files for
`tag.py`, and `tests/test_tag_workers.py` alone for `cli.py`. Null control 0 of
8440. All 13 killed.

**`u84-a4.md`**, the one zero measured again at `69aff7a`, after
`test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok` was written for
it, with a not an image case and a truncated JPEG case. Null control 0 of 8442.
Killed, 2 deaths.

25 distinct mutations, which is the cap, and one re-measure on top of it, so 26
runs. The re-measure is the same mutation as A4 and is what turns that zero
into a kill.

**Dropped at the cap.** `A3_zero_depth`, a block declaring a zero depth no
longer broken. Ranked below the cap because it is the same guard family as A1
and A2, and `test_any_one_zeroed_dimension_is_broken` parametrizes the depth
case beside them. Not measured, so not coverage.

**Not in any table.** The widened catch in the repair loop, `828a0ed`, landed
after the tables were measured. It has its own test,
`test_an_encoder_failure_that_is_not_an_art_error_is_still_an_error`, which
fails against the narrower catch by construction, since the fake raises
`OSError`. It was not run through the driver.
