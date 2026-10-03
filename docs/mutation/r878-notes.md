# R-878 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's).

Two batches, 25 rows, the unit's light cap. Split in two because one batch of
25 passes the harness's ten minute foreground ceiling.

- `r878-a`: 13 rows over `paginate_cursor`, the cursor walk: the rule
  refusals in both walks, the budget guard, the declared count check and its
  coefficient, the latest count winning, both end conditions, the cursor
  advancing, the non page refusal and its count only exception, the per item
  parse retry, and the shared dedupe. 13 of 13 killed.
- `r878-b`: 12 rows over the folder request and the two wrappers: the
  TypeError translation, the missing client part refusal, `includeOnly` at
  the root and in a folder, the root folder id, the order, no offset, no
  cursor on the first request, the v2 base, the root dedupe key, the stop
  rule table, and the folder's own identifier. 12 of 12 killed.

No zero rows, so no composite and no promotion to the full suite. Every
row's restore was verified against `git show HEAD:` by the driver.

Dropped below the cap, logged in `r878-b-rows.toml`: B13, the playlist
parser handed the whole item rather than its `data`, equivalent on the real
client because `Playlist.parse` reads `obj.get("data", obj)`.

## The review, one round

Eight findings from the built in `/code-review`.

- Fixed with a test: the playlist parser can be a request of its own and is
  retried per item (A12); a response with neither items nor a count is
  refused rather than read as an empty listing (A10, A11); a TypeError from
  the client's request object is translated, not slept on (B1); the dedupe
  both walks run is one helper (A13).
- Filed: R-880, the declared count may count more than the filtered items;
  R-881, an unchanged cursor costs the whole budget.
- Not acted on, recorded here: a duplicate item is parsed before the dedupe
  drops it, which for a playlist the account created costs one paced request
  per duplicate, on a path no read has produced; the `PAGE_CAPS` reach figures
  assume the provider fills the page it is asked for, which the comment above
  them now says; the `_Answer` stand in is written in two test files.
