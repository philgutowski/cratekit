---
title: A file's ISRC is the library's claim, not the provider's, and export set matches every row twice
date: 2026-10-03
category: integration-issues
module: src/cratekit/export/set_cli.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A code read from a library file's own tag is handed to the provider account's match_track"
  - "Per row work is added inside match_rows of export set"
---

# A file's ISRC is the library's claim, not the provider's, and export set matches every row twice

## Problem

R-879 matched a typed tracklist row through its library file's ISRC before any search. The
first shape handed that code straight to the account's `match_track` in
`modules/outbound/tidal_account.py`. A second trap sat beside it, and neither is visible in
the code that triggers them.

## Cause

1. `match_track` lists a lone provider track under a code with no agreement check. That is
   safe for an ISRC the provider supplied. An ISRC read off a file's tag is the library's
   statement, and a file can carry another recording's code. Asked bare, it puts the wrong
   track on the playlist.
2. `export set` has a two act gate and runs `match_rows` once per act. Any per row cost added
   there, a volume walk or a provider call, is paid twice per export. The export set tests see
   every search and account match doubled for the same reason, so a test asserting one call
   fails for a reason that looks like a bug in the new code.

## What to do next time

- Call `match_track` with the `agree` option for any code that came from a file tag, so the
  provider's track must agree with the row before it is listed.
- Cache or hoist per row cost out of `match_rows` when it is expensive, and expect doubled
  call counts in export set tests rather than chasing them.
- Related: R-879 in `docs/residual-findings.md`, notes in `docs/mutation/r879-notes.md`.
