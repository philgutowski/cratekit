# U85 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/130`. Every zero row in this record means the
author could not kill it, not that nobody could. The unit writes pictures into
audio files the user owns, so it took the full 25 rows, split across two
batches so neither run passed the 600 second tool ceiling.

**`u85-a.md`**, 16 rows over `tagging/tag.py` and `tagging/cli.py`: the
search skipped only for a file with both a genre and a picture, any picture
settling the art, an unreadable file being `unchecked`, the three guards
before a fetch, the fetch, decode and write failures each becoming a status,
new art at the CDJ size, the review's refusal absorption for an art only
search and its limit to tagged files, the worker handing in the fetch, and the
summary counting it. Subset `tests/test_tagging_engine.py`,
`tests/test_tag_workers.py` and `tests/test_art.py` for the engine, 170
collected, and the worker file for the shell, 52. Null control 0 of 8583. 14
killed, 2 zeros promoted to the full suite, both maintainer facing:

- `A8_empty_bytes_guard`, 0 of 8583. Empty bytes are refused by
  `to_cdj_jpeg` one line later and still land as `unavailable`, only with the
  "not a usable picture" sentence instead of "could not be fetched".
- `A12_write_raise_absorbed`, 0 of 8583. `write_front_cover` raises only on
  bytes that did not come from `to_cdj_jpeg` or on a container
  `read_pictures` already refused, so no path above it reaches the catch.

**`u85-b.md`**, 9 rows over `tagging/searchers.py`: the Beatport resize and
its 1400 edge, the picture read off the winning row rather than the loop's
last row, the http and https check, the Bandcamp `_10` rewrite, the track page
fetch for a picture the listing lacked, the listing's genre winning over the
page's tags, the hit carrying the URL, and the image fetch's pace wait. Subset
`tests/test_catalogue_searcher.py` and its importers, 113 collected. 9 killed.

`B3_picture_off_the_winning_row` killed only after the test was reordered so
the winning row is not the last one scanned. With the winner last, reading the
cover off the final row gives the right answer by accident. The reorder is its
own commit, made before either table ran.

Four rows are logged as dropped in the row files, with the reason each ranked
below the cap.
