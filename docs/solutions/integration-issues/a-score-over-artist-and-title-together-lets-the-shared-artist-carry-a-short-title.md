---
title: "A score over artist and title together lets the shared artist carry a short title"
date: 2026-11-13
category: integration-issues
module: src/cratekit/acquire/match.py
problem_type: integration_issue
component: acquire
severity: medium
resolution_type: code_fix
applies_when:
  - "A unit scores a fuzzy resemblance over a string that joins two fields, an artist and a title"
  - "A unit filters the hits of a scorer that is itself capped at a number of results"
  - "A unit changes APPROXIMATE_FLOOR, APPROXIMATE_TITLE_FLOOR or the approximate pass"
tags: [match, approximate, rapidfuzz, token-set-ratio, title-floor, short-title, filter-before-cap, u286]
---

# A score over artist and title together lets the shared artist carry a short title

## Problem

The approximate pass scores the folded recording token, artist and title
joined, with `token_sort_ratio` against a floor of 82. The artist's letters
are most of a short token, so an unrelated short title by the same artist
clears the floor on the artist alone: `Monkey Safari, Joy` scored 84.2
against `Monkey Safari, Goodbye` and was held for review rather than
downloaded, and four of the five open title approximate items at that sitting
were the same shape (U286).

## What to do

- **Score the title alone as well.** The joined score is discovery; a hit is
  offered only when its folded title also reaches `APPROXIMATE_TITLE_FLOOR`
  by `token_set_ratio`, which gives a dropped, added or reordered word 100 and
  a typo the score of a typo.
- **Filter before the cap, never after it.** The scorer was capped at five
  recordings. Filtering those five lets a prolific artist's unrelated short
  titles, each outscoring a real near match through the shared artist, fill
  the five and push the real one out; the row then reads missing and a record
  the library holds is downloaded. Ask discovery for every hit
  (`_approximate(..., limit=None)`), filter, then cap (`_resembling`).
- **Keep what the joined score got right.** A swapped listing, title first,
  scores 100 joined and is the same record, so each half may stand for the
  other; a title that folds to nothing cannot be read, so the title test says
  nothing about it. Dropping either would download a duplicate.
- **A floor between short titles is narrow.** One changed letter in a three
  letter title scores 66.67 and `Get Out` against `Agenou` 61.5, so the free
  band is a few points wide: pin it with computed neighbours either side, as
  `TITLE_FLOOR_NEIGHBOURS` does, never a remembered number.
