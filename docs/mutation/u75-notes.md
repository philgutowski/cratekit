# U75 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/120`. They are batches rather than one table
because Relay runs every command in the foreground and a 25 row table passes the
harness ceiling of 600 seconds, the precedent `u90-a` to `u90-d` set.

**`u75-a.md`**, 9 rows at `352f37d`, over how the verb reads the queue and one
release. Null control 0 of 8106, no collect drift, every restore verified
against `git show HEAD`. 8 killed on the first run.

**`u75-b.md`**, 10 rows at `77d239c`, over the outage count, the three
refusals, the dedupe, the offer, the name's digest and the write failure. Null
control 0 of 8107, no collect drift. 9 killed on the first run.

**`u75-c.md`**, 6 rows at `aedb045`, over the live adapter's `release_tracks`.
Null control 0 of 8108, no collect drift. 6 of 6 killed.

**`u75-zeros.md`**, the two zeros run again at `1c51cb0` after a test was
written for each. They are the same two rows, so the count stays at 25. Both
killed.

25 rows in all, which is the cap. Eight more were considered and are logged as
dropped with a reason each, in `u75-b-rows.toml` and `u75-c-rows.toml`: the
provenance first wins rule (B7 measures the dedupe that makes a second
provenance for one id unreachable), the `--out` that is a file guard (the
guard `intake missing` carries, asserted by one test here), the adapter's blank
identifier guard (A6 measures the verb's guard on the same input, which runs
first), the two maintainer facing year rows, the list prefix, the failure
wording per kind, and the undated check.

## The two zeros of the first runs

- **A8, the identity read before the payload.** User facing. The sweep writes
  the release identifier into both the item's identity and its payload, so no
  fixture held an item whose two disagreed and either order read the same
  release. `test_the_items_identity_names_the_release_and_a_payload_that_disagrees_does_not`
  was written for it, and `u75-zeros` measures 1 kill. The disagreeing item is
  built by `review.offer`, since the sweep's own producer cannot make one, so
  the reachability of that input through a shipped verb is not measured.
- **B6, the refusal when nothing missing can be asked for.** User facing. One
  test held the MIXED case, a listable row beside one with no provider
  identifier, which writes a list and never reaches the refusal.
  `test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`
  was written for it, and `u75-zeros` measures 1 kill.

Every zero was read as "the author could not kill it" until the fourth table,
and then it was killed.

## What the tables do not measure

Every row ran against fakes. The live adapter's member has never met the
provider: that the client's album pages its tracks under `limit` and `offset`,
parses `numberOfTracks` onto `num_tracks`, and dates itself through a `year`
property was read off the installed client's source at 0.8.11, not driven. The
first live call is owed to an attended sitting.
