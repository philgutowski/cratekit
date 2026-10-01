# R-796 mutation tables, read

Four tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/236`, each in the foreground and waited on. Every row ran against
`tests/test_published_genre.py`, `tests/test_tag_workers.py`,
`tests/test_tagging_engine.py` and `tests/test_catalogue_searcher.py`, 342
collected on every row of the first three and 357 on the fourth. Every null
control killed 0 of the full suite, 11,255 collected against 11,255 for the
first three and 11,270 against 11,270 for the fourth, the leak watch was on
and the watched roots were unchanged, and after each table `git diff` over
`src` and `tests` was empty.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r796-a.md`, the lookup's answers, its identity checks and its memory of a refusal | 9 | 9 | 0 |
| `r796-b.md`, which word is chosen, when the catalogue is asked, what a decline keeps | 9 | 9 | 0 |
| `r796-c.md`, the worker, the warnings, the per process lookup and its headers | 7 | 7 | 0 |
| `r796-d.md`, four of those rows again, after the second review moved their lines | 4 | 4 | 0 |

25 distinct rows, the cap, and four measured twice. No zero, so no composite
was owed.

## The second review round, and what `r796-d` is

The first three tables were measured after the first fix round. The second
review round then rewrote the line four rows mutate: L9, the ISRC found
inside a longer value, O1, a word with no folder passed over, O7, a decline
keeping the record shop's word, and O8, a tagged file not asked about. The
`old` text in `r796-a` and `r796-b` for those four no longer exists on the
branch, so their numbers describe the tree as it was. `r796-d` is the same
four guards against the lines as they stand, each row naming the one it
measures again. The other 21 rows' lines did not move.

The guards the second round ADDED are past the cap and were not measured.
Each has a test that names it in `tests/test_published_genre.py`:

- a bucket's own name counted as a folder,
  `test_a_word_that_is_a_buckets_own_name_maps_to_that_folder`. O1's
  re-measure removes the whole check and is not this guard alone;
- `no-isrc` recorded before the Beatport gate,
  `test_a_file_with_no_isrc_is_said_to_have_none_whatever_beatport_answered`;
- a body that is not JSON read as unreachable, two rows of the parametrized
  unread tests;
- a match with no genre leaving the source alone,
  `test_a_match_that_publishes_no_genre_is_a_decline_with_no_word`. O7's
  re-measure covers the condition and not this arm alone;
- the picture sentence for a genre only source, three tests that assert the
  sentence whole;
- the autouse guard in `tests/conftest.py`,
  `test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup`.

## What the cap dropped, and why each ranked below it

Fourteen candidate rows were written down and not measured. Each guard has a
test that names it. They ranked below the 25 because the cost of each is
smaller than a wrong write, a false absence or a refusal argued with.

- `_error`: a permission error read as blocked, and "service busy" read as
  unreachable. Two more arms of a table whose three costlier arms are L1 to L3.
- `_ask`: an album the catalogue does not list read as a match with no genre,
  and `_genre_names` answering None for entries with no names.
- `_ask`: the album memo, which costs requests and no correctness.
- `second_opinion`: a hit with no answers returned untouched, a file that
  needs no genre recorded as not asked, and `art_source` naming the record
  shop a kept picture came from.
- `tag.py`: `pictured_by`, the sentence about whose picture it was.
- `cli.py`: the general catalogue's zero filled row in `answers`, the
  `tagged_by` count, the wording for unread on every file against some, and
  the parse break sentence in the general catalogue's own warning.
- `searchers.py`: the `headers` default on the shared fetch, pinned by a test
  that the record shops are still asked with the old constant.

## What these tables do not show

Every answer in them is synthetic. The quota error, a 429, a 403 and a
challenge page have not been seen from Deezer, so the rows over them measure
that the code does what the published error table says and not that the
catalogue behaves that way.
