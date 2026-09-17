---
title: "No page shape says where a filtered listing ends, and the provider's own count is the only thing that does"
date: 2026-09-17
category: integration-issues
module: src/cratekit/acquire/listing.py
problem_type: integration_issue
component: provider_listing
severity: high
root_cause: incorrect_assumption
resolution_type: fixed_in_unit
applies_when:
  - "A paginated provider listing is being read through listing.paginate"
  - "A new listing wrapper is being added to acquire/listing.py"
  - "A question is being answered from a provider listing, such as is this track already hearted"
  - "A live count from the provider disagrees with what the product reports"
symptoms:
  - "A listing returns a round fraction of the account's real contents and stops"
  - "A listing stops in the middle of a collection on a page that came back empty"
  - "A page returns fewer items than the limit asked for, on a listing that has more"
  - "An add-only sweep re-adds something the account already holds"
  - "A report's already and newly-written split is wrong while the account ends correct"
related_components:
  - outbound_hearts
  - label_crawl
tags:
  - pagination
  - declared-total
  - tidal
  - listing
  - live-only-defect
  - short-page
---

# No page shape says where a filtered listing ends, and the provider's own count is the only thing that does

## Context

The fourth attended sitting, 2026-09-17, ran the first real `crate sync favorites`
against the live account. It reported 18 hearted and 41 already out of 109 rows.
Verifying that the 18 hearts had landed, a fresh read of the account's favourites
found only one of them. The hearts were fine. The read was not.

## What is actually going on

`listing.paginate` walked pages until one came back shorter than the page size it
asked for, which is the ordinary convention for an offset and limit API: a short
page means the end of the collection.

This provider breaks that convention. It serves a WINDOW of a counted collection
and omits from that window the items it will not serve, so a request for 50
returns 47, and 47 is not the end of anything. Measured on the live account: pages
came back 47, 46 and 49 while walking, and the account holds **197 favourite
tracks where the shipped read returned 93**, stopping at the second page.

**Where the omission happens, corrected by U65.** The sitting that found this
recorded the cause as the client, `tidalapi` dropping unplayable tracks from each
page before returning it, and that is wrong. Read against tidalapi 0.8.11:
`user.Favorites.tracks` hands the response to `request.map_request`, which hands
it to `map_json`, which does `list(map(parse, items))` with no filtering anywhere.
The `Track '25992145' is unavailable` line that was visible during the sitting
comes from `session.track()`, a per identifier lookup that is not on the listing
path at all. The omission is the API's. Its own client says so in the place that
matters most: `Favorites.get_tracks_count` documents that the total it returns
"also includes track that may not be available for playback", so the API counts
what it does not serve.

That correction is what makes the fix possible, because it means the count and the
windows are cut from the same sequence.

The offset arithmetic was never affected. The server's window is still 50 wide, so
advancing the offset by the page size skips nothing. It was only the STOP RULE
that was wrong.

## What makes it hard to see

Three things, and they compound:

1. **Nothing fails.** The listing returns a list, the job succeeds, and every
   count in the report is internally consistent with the truncated read.
2. **The writes stay correct.** Hearting is add only and idempotent, so the
   account ends in the right state even when the product asks the wrong question.
   What is wrong is the report, which is the artifact nobody can check.
3. **The ordering hides it.** The favourites listing is newest first, so the 93
   rows that DO come back are the most recent hearts. A second sweep in the same
   sitting therefore read all 59 matched rows as already hearted and wrote
   nothing. The defect bites on OLD state, which is the state nobody is looking at.

## The scope, measured rather than assumed

Not every listing truncates. In the same sitting, on the same session: the
account's playlists read 599 both through the shipped wrapper and through a hand
walk, and a 197 track playlist's membership read 197 both ways. The provider
serves those in full pages. It is the listings the client FILTERS that arrive
short, and today that is the favourite tracks read.

## The trap, and it cost U65 a whole fix round

The obvious fix is to stop on an EMPTY page instead of a short one. U65 wrote
exactly that, with a test per listing, and a green suite. Its review found the
hole: an empty page is a page shape too. A window in which every counted item is
unservable comes back empty in the MIDDLE of a collection, and the walk reads that
as the end. Reproduced against the fix as first written, 300 counted rows with
rows 100 to 199 unservable, page size 100: it returned 100 of the 200 servable
rows in two requests, silently.

That is reachable on this listing specifically, not a theoretical worry. The
favourites listing is ordered by date added, and `dj-label-batch` hearts a whole
label catalogue in one go, so a label later withdrawn from the provider leaves
exactly the required shape, a contiguous run of unservable hearts. A run of 100 is
enough on a track listing, and 50 on account playlists.

**No page shape says where a filtered collection ends.** Not a short page, not an
empty one, not two empty ones. The end is a fact about the collection and the only
thing that reports it is the provider.

## Where it stands

Fixed by **U65**. `listing.StopRule` names three rules and every shape declares
one in `STOP_RULES`:

- `DECLARED_TOTAL` walks until the offset passes a count the provider publishes
  for the collection it is serving, and reads nothing from a page's shape.
  `favorite_tracks` ends on `get_tracks_count`, `playlist_tracks` on the
  `numberOfTracks` already parsed onto the playlist object. Neither costs a
  request: the count replaces the page that would have ended the walk, and the
  playlist's is free.
- `EMPTY_PAGE` is the fallback for a shape whose provider publishes no count, and
  it is SAFER rather than safe. `account_playlists` and `artist_releases` take it,
  and **R-385** records that they are narrowed rather than closed.
- `SHORT_PAGE` is what was wrong here. No shape declares it.

`max_pages` became a budget of requests that RAISES `ListingTruncated` when spent,
rather than returning quietly, since a capped length answer is indistinguishable
from a complete one. **R-384** records the request cost of the fallback rule.

## What to carry forward

- **A near miss count is worse than no count.** `Favorites.get_playlists_count`
  looks like the total for `account_playlists` and is not: it counts the root
  collection folder, while the listing serves `playlistsAndFavoritePlaylists`,
  which also carries followed playlists. Ending a walk on a count of a different
  collection is a wrong answer arriving with a confident number.
- **When a live count looks like a round fraction of what you expect, walk the
  pages by hand before believing it.** That is the check that found this.
- **A new listing wrapper declares which rule it needs and why.** A guard asserts
  its docstring names the rule its table declares, so the prose cannot keep
  arguing for a rule that changed.
