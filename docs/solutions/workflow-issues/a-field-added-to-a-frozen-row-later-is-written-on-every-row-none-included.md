---
title: "A field added to a frozen row later is written on every row, None included, so absence means an older freeze and nothing else"
date: 2026-10-10
category: workflow-issues
module: "src/cratekit/intake/cli.py, src/cratekit/intake/account_playlists.py, src/cratekit/favorites/backfill.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
resolution_type: code_change
applies_when:
  - "A job's frozen row, a review option or any record a later reader thaws gains a new key"
  - "Two readers of the same record decide something from the key, and one of them can also ask the source again"
  - "The value the key carries can itself be empty or None"
tags: [frozen-row, tri-state, hearts, quarter, u120, intake, backfill]
---

## The trap

U120 froze each heart's date onto its job row under `hearted` so a landing
could put the heart into the quarter it was hearted in. The first version
wrote the key only when the account dated the heart, so a row with no key
read as "undated" and the landing filed it into `Undated`. Every job frozen
before the key existed also had no key, so the landing of such a job filed
every heart into `Undated` with no warning, and the backfill, which asks the
account for a date when the job knows none, then added the same heart to
`2026-Q3`. One heart in two quarter playlists, and the add only rule means
nothing ever takes one out.

The review found it; the suite was green, because every test froze its rows
with the new build.

## The rule

A key added to a frozen record later has three states, not two: the record
says a value, the record says there is no value, and the record was written
before anybody asked. Collapsing the last two is the defect. So:

- **Write the key on every row the new build freezes**, `None` included.
  `list_favorites` sets `hearted` for every heart, and `hearted_on` answers
  `None` when the account dates it nowhere.
- **Read the key's presence as a fact of its own.** `HeartRow.known` is
  `HEARTED in said`, and `Hearted.quarter` is `None` when the job never said,
  distinct from `Undated` when it said there is no date.
- **Give the unknown state its own behaviour that cannot collide with the
  other reader's.** The landing puts an unknown heart into All Favorites and
  leaves its quarter alone; the backfill, the one reader that may ask the
  account, dates it and adds exactly the quarter. Neither ever writes
  `Undated` for a row that merely predates the key.
- **One tie break for every reader of the same record.** Two jobs can carry
  the same heart, one old and one new; `account_playlists.prefer_dated` is the
  rule both the landing's claims and the backfill use, so they cannot pick
  different mentions and place one heart twice.

## How to check

Freeze a row with the key absent, one with the key `None` and one with a
value, and drive every reader over all three. The test the review added is
`test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_quarter`
in `tests/test_intake_land_hearts_native.py`, and its backfill half is
`test_a_heart_the_landing_placed_without_a_quarter_takes_it_from_the_backfill`.
