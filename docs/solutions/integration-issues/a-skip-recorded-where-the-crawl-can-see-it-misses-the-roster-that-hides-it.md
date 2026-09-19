---
title: "A skip recorded where the crawl can see it misses the roster that hides it, and discovery records stale failures for artists the roster reads again"
date: 2026-09-19
category: integration-issues
module: "src/cratekit/label/tidal_catalogue.py, src/cratekit/label/catalogue.py, src/cratekit/label/sweep.py, src/cratekit/acquire/listing.py"
problem_type: integration_issue
component: catalogue_crawl
severity: high
tags:
  - "label-sweep"
  - "partial-read"
  - "roster"
  - "unread"
  - "honest-zero"
---
# A skip recorded where the crawl can see it misses the roster that hides it

## Problem

R-261 and R-393 (issue #162). A label crawl that skipped a listing, either a
method the provider client lacks or an artist whose listing failed on a rate
limit, was reported as a complete crawl. New releases were missing from a sweep
that said success.

## Cause

The obvious fix is to count skips inside the crawl that pages the catalogue.
That cannot work for the Tidal label path, because the crawl never pages the
artists. It pages a `LabelRoster`, which builds both release listings eagerly
and always exposes both methods. A member lacking a method is skipped inside
the roster's constructor, one layer below anything the crawl can inspect.
Discovery has the same shape: it skips an artist after a failed listing before
the roster exists.

Two smaller traps sat in the same seam:

- Discovery also lists seed and own-page artists that the roster then lists
  again. A failure recorded for one of those is stale, because the roster read
  is the one the crawl uses, and it either succeeds or refuses the label. Only
  an artist discovery alone would have added may be recorded.
- A live 429 is `TooManyRequests`, not a `CratekitError`, so the broad
  `except Exception` in discovery skipped it in silence, with no retry ladder.

## What to do next time

- Put a skip on the object the sweep reads, not on the loop that made it. The
  roster carries `unread`, a tuple of `Unread`, and the sweep reads it with a
  default of nothing so a plain artist object needs no attribute.
- Any adapter that skips something while building a roster must append to
  `unread`. A skip with no record is indistinguishable from a release that was
  never there.
- Before recording a discovery failure, ask whether a later read of the same
  artist supersedes it.
- A crawl that skipped anything fails the sweep item as
  `label-sweep-incomplete` after offering what it did read, and does not
  advance that label's watermark.
- Look one file over for the same shape, which is METHOD's fifth pattern.

Neighbour: [a seam that returns only rows reads absence as evidence of
absence](../workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md).
Open follow-up: R-470, `tests/test_rebuild.py` fails 25 tests on some full
parallel runs and makes `scripts/mutate.py` refuse its baseline; a plain rerun
clears it.
