# R-879 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's).

Two batches, 25 rows, the unit's light cap. Split in two because one batch
passes the harness's ten minute foreground ceiling.

- `r879-a`: 11 rows over `intake.candidates`: `Answer.full` reading the last
  page, the walk's stop on a short page, each of the four early stops, the
  bound and its coefficient, `read_pages` carrying the last page, the offset
  per page, and one existing guard sampled, `sole_exact`'s full condition.
  9 of 11 killed. Two zeros, both promoted to the full suite.
- `r879-b`: 14 rows over `export.set_cli`, the account and the adapter: the
  library route, the agreement it asks for, a question taken as held, several
  codes, codes from every version, the absent music folder, a person's answer
  first, the three refusal wordings, the account's one track agreement, the
  adapter's offset, and reruns of the two zeros of batch A. 13 of 14 killed.

## The zeros

- `C5`, the early stop on an exact candidate with no identifier, maintainer
  facing: the walk read on and the answer was refused the same. A test of a
  full page holding one was added; rerun as `C5r`, killed.
- `C8`, the ceiling raised from 300 to 350, user facing: the bound test read
  its page count off the constant it checked, an X equals X assertion. A test
  with the client's documented 300 written as a literal was added; rerun as
  `C8r`, killed.
- `S3`, a library answer that is a question taken as held, user facing in a
  sentence only: no file is asked about, because a question carries no paths,
  and the row would be told "the library holds it and its file carries no
  ISRC". A test of a row held only at another version was added after the
  pass, with the table at its cap, so its kill is the author's reading and was
  not measured by the driver.

Every row's restore was verified against `git show HEAD:` by the driver, and
the tree was clean after each batch.

## The review, one round

Ten findings from the built in `/code-review`.

- Fixed with a test: a file's ISRC listed its one provider track with no
  agreement check, so a file tagged with another recording's code would put
  the wrong track on the playlist; `match_track` gains `agree` and the library
  route asks for it (`S2`, `T1`). The library route ran before a person's
  answer in review (`S7`). The refusal said the bound was reached for a title
  read two ways that stopped after one page (`S9`), and said none resembles it
  after naming an exact match with no identifier (`S10`). `SEARCH_PAGES` is
  derived from the ceiling and the page (`C8r`).
- Filed: R-882, `intake missing` still reads one page; R-883, both acts of the
  gate walk the volume and repeat the searches, and a tombstone store that
  cannot be read now refuses the verb.
- Not acted on, recorded here: the walk stops on a title read two ways even
  with no exact candidate yet, which costs nothing here because `export set`
  never offers and such a row is always refused; `search_pages` is its own
  loop beside `listing.paginate`, whose stop rules do not fit a walk that ends
  on what the answer says, and a provider that ignored the offset would serve
  the first page six times, which leaves the last page full and is refused at
  the bound.
