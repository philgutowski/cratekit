---
title: "A label's listing is kept since U217, reversing R-1091's choice to read it every run, and a continue resumes it only because every answer the roster is built from is kept on its own"
date: 2026-11-05
category: integration-issues
module: "src/cratekit/label/kept_listing.py, src/cratekit/label/tidal_catalogue.py, src/cratekit/label/sweep.py"
problem_type: decision_reversed
component: catalogue_crawl
severity: medium
tags:
  - "label-sweep"
  - "kept-listing"
  - "call-ceiling"
  - "roster"
  - "decision-reversed"
---
# A label's listing is kept, reversing R-1091, and the roster is kept answer by answer

## Problem

R-1091 kept a full `label playlists` build's release reads and deliberately
did NOT keep the label's listing, so a release the label put out since would
never be missed. At sitting 60 the listing alone was the cost: Defected's
roster is about 1,800 provider calls, the call ceiling stopped it at 500 and
1,000, and each continue read it again from the first call, under a ceiling
message that said "what it did is kept". A second identical run with nothing
new paid 1,800 again. Phillip filed U217 to keep it.

## Decision, reversed with its reason

The listing is kept for R-1091's seven days, the same number read from
`kept_reads.KEPT_FOR` at call time. The cost R-1091 named is real and is now
said rather than avoided: every screen that lists a label says whether the
listing was kept and how old it is, and deleting the file it names lists the
label afresh. A question on the card asks Phillip whether the scheduled sweep
should list fresh instead.

## What a future session would get wrong

1. **Keeping the roster whole does not resume a continue.** The roster is
   built from four kinds of answer: an exact name search, an identifier read,
   eighty discovery album searches, and each artist's paged listing of each
   release method. A ceiling stops the build in the middle of them, so only
   keeping each answer on its own, and flushing in a `finally` on the way out
   of the park, lets the continue ask only what is left.
2. **The roster listed every discovered artist twice.** Discovery paged each
   artist's releases to walk the credits, then `LabelRoster` paged them all
   again at construction. Reading the roster's listings back from the store
   halved the first run too.
3. **A kept release must satisfy every reader of a provider album.** The
   sweep, the verifier, the tombstone check, the gate and the playlists build
   read `id`, `title` or `name`, `year` then `release_date`, `copyright` then
   `label`, `artist` as an object or a name, and `artists[].id`.
   `kept_listing.KeptRelease` carries exactly those; a new reader of a listed
   release that needs another attribute must add it to `release_row` too.
4. **The listing line counts answers, not calls, and speaks for the listing
   only.** Verification can still read an album whose kept copyright line is
   empty, so the line says the listing made no call, never that the provider
   was asked nothing. The gate's spend line is the call count.
5. **A kept artist has no provider object.** `_Member` reads it by identifier
   only when a listing of it is not kept, and that read is counted.
