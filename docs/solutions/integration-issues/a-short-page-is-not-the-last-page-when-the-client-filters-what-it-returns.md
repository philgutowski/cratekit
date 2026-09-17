---
title: "A short page is not the last page when the provider client filters what it returns"
date: 2026-09-17
category: integration-issues
module: src/cratekit/acquire/listing.py
problem_type: integration_issue
component: provider_listing
severity: high
root_cause: incorrect_assumption
resolution_type: recorded_residual
applies_when:
  - "A paginated provider listing is being read through listing.paginate"
  - "A new listing wrapper is being added to acquire/listing.py"
  - "A question is being answered from a provider listing, such as is this track already hearted"
  - "A live count from the provider disagrees with what the product reports"
symptoms:
  - "A listing returns a round fraction of the account's real contents and stops"
  - "A page returns fewer items than the limit asked for, on a listing that has more"
  - "An add-only sweep re-adds something the account already holds"
  - "A report's already and newly-written split is wrong while the account ends correct"
related_components:
  - outbound_hearts
  - label_crawl
tags:
  - pagination
  - tidal
  - listing
  - live-only-defect
  - short-page
---

# A short page is not the last page when the provider client filters what it returns

## Context

The fourth attended sitting, 2026-09-17, ran the first real `crate sync favorites`
against the live account. It reported 18 hearted and 41 already out of 109 rows.
Verifying that the 18 hearts had landed, a fresh read of the account's favourites
found only one of them. The hearts were fine. The read was not.

## What is actually going on

`listing.paginate` walks pages until one comes back shorter than the page size it
asked for, which is the ordinary convention for an offset and limit API: a short
page means the end of the collection.

This provider's client breaks that convention, and not in the API. `tidalapi`
drops tracks the account cannot play from each page BEFORE returning it, printing
`Track '25992145' is unavailable` as it goes. So a request for 50 returns 47, and
47 is not the end of anything. Measured on the live account: pages came back 47,
46 and 49 while walking, and the account holds **197 favourite tracks where the
shipped read returned 93**, stopping at the second page.

The offset arithmetic is not affected. The server's window is still 50 wide, so
advancing the offset by the page size skips nothing. It is only the STOP RULE
that is wrong.

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

## Where it stands

Recorded as **R-383** and deliberately not fixed in the sitting that found it.
One rule governs every listing in the product, including the label crawls and the
playlists source, and simply removing the short page stop makes any listing whose
offset parameter is broken walk until the runaway guard stops it. The fix is a
unit with a test per listing.

## What to do about it before then

- **Do not answer a membership question from a listing this helper returns**
  without checking whether that listing is one the client filters. `has_heart` is
  the live example.
- **When a live count looks like a round fraction of what you expect, walk the
  pages by hand before believing it.** That is the check that found this: keep
  requesting until a page comes back EMPTY, not until one comes back short.
- **A new listing wrapper states which rule it needs.** The convention this
  helper encodes is an assumption about the client, not about the API.
