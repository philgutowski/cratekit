# R-796 mutation tables, read

Three tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/236`, each in the foreground and waited on. Every row ran against
`tests/test_published_genre.py`, `tests/test_tag_workers.py`,
`tests/test_tagging_engine.py` and `tests/test_catalogue_searcher.py`, 342
collected on every row. Every null control killed 0 of the full suite, 11,255
collected against 11,255, the leak watch was on and the watched roots were
unchanged, and after each table `git diff` over `src` and `tests` was empty.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r796-a.md`, the lookup's answers, its identity checks and its memory of a refusal | 9 | 9 | 0 |
| `r796-b.md`, which word is chosen, when the catalogue is asked, what a decline keeps | 9 | 9 | 0 |
| `r796-c.md`, the worker, the warnings, the per process lookup and its headers | 7 | 7 | 0 |

25 rows, the cap. No zero, so no composite was owed.

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
