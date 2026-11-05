---
title: The label crawl still reads the catalogue under the account session after U205, since the official API pages by cursor and the crawl's listings page by offset to a declared count
found: at the plan of #495, U205, 2026-11-05.
issue: no
---

**The mechanism.** U205 moved ISRC lookups and exact track reads to the app
client. Every read of the label crawl in `label/tidal_catalogue.py` (the name
search, an artist by identifier and its release listings, an album and its
tracks, the copyright re read, the label check, the track search) still goes to
the account session. Each listing pages through `acquire.listing` by limit and
offset and stops on a count the provider declares; the official catalogue API
pages its relationships by cursor. A mapping between the two written without a
live probe of the official API's paging is the short page read as the end
defect this package has paid for four times, so the brief's requirement to
move the label reads was taken as far as its own carve out allows and no
further. The module docstring names each read that stays and why.

**Measured cost.** None to a DJ: the crawl works as before and its calls are
counted under the account, where the spend line and doctor show them. What the
person pays is the account carrying a label sweep's calls, about 3,000 for a
full label build (U193), which the card set out to remove.

**Closes when:** a unit opens with one read only probe of the official API's
artist albums, album items and search relationships on the app client, records
their paging in `docs/solutions/`, and moves the crawl's reads behind an
adapter that walks the cursor inside `acquire.listing`. Asked of Phillip on the
card's plan; ledger only until he answers, since an account carrying calls is
none of the board bar's four costs.
