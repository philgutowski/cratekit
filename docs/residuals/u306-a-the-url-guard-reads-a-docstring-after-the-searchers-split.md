---
title: The catalogue URL guard in test_locations now passes on a docstring line in searchers.py, not on the URLs, which moved to shops.py
found: at the review of #863, U306, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_locations.py`, in
`test_the_one_permitted_call_is_still_there_and_is_still_a_query_string`,
asserts that `src/cratekit/tagging/searchers.py` holds `https://` and no
`file://`, to keep the one permitted `quote_plus` building a query string. U306
split `searchers.py` by source: the catalogue search URLs now live in
`tagging/shops.py`, and the only `https://` left in `searchers.py` is a line of
`_query`'s docstring. The round one reviewer set `BANDCAMP_SEARCH` in
`shops.py` to a `file://` path and the test passed; the same edit in the base
`searchers.py` fails it. Rewording the docstring fails it with no behaviour
change.

**Measured cost.** None to a person today: the URLs are unchanged and the
behaviour comparison is clean. The guard has lost its object, so a later
`file://` search URL in `shops.py` would pass it.

**Closes when:** the guard reads the module that builds the URLs (`shops.py`,
or whatever module `_query`'s callers take their bases from). `tests/test_locations.py`
is on no area card's list, so it is the suite card's, #869 (U312). Ledger only.
