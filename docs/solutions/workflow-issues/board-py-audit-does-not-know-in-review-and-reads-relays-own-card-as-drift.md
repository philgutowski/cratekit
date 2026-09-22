---
title: "board.py audit does not know In review, and reads Relay's own card as drift"
date: 2026-09-22
category: workflow-issues
module: "scripts/board.py"
problem_type: workflow_issue
component: tooling
severity: low
root_cause: missing_status_case
resolution_type: workflow_improvement
applies_when:
  - "audit or closing runs while a Relay task is mid-flight on its own card"
  - "the board shows a status derive_status does not produce"
tags: [board, audit, relay, In-review, R-345]
---

# board.py audit does not know In review, and reads Relay's own card as drift

## Problem

`derive_status` (`scripts/board.py:155`) computes what a card's status should
be from closure and the dependency graph alone, and only ever returns one of
five values: `Done`, `Attended`, `Blocked`, `Ready`, `In Progress`. Every
Relay manifest (`~/.relay/manifests/cratekit-*.toml`) sets
`in_review_status = "In review"` and moves a card there itself while its own
review phase runs, before the merge that would close the issue. `board.py
audit`, run from inside that same task, compares the live board against
`derive_status` and finds a mismatch: the card reads `In review`, the
function has no such case and falls through to `Blocked` or `Ready`. That is
reported as drift, exit 1, with the standard remedy printed: run `board.py
sync`.

## Why running sync is the wrong fix here

`sync` would move the card. The card is Relay's own, mid-run, on a status
`derive_status` cannot express, not a card that fell out of date. Moving it
mid task is exactly the failure `derive_status`'s own comment on the `In
Progress` branch warns about for a different status: "recomputing it back to
Ready is how a session loses track of work already underway." Running `sync`
on an `In review` card would do that.

## The rule

An `audit` exit 1 seen from inside a Relay task, on the task's own card, while
that card is `In review`, is expected and is not a reason to run `sync`. It is
a gap in what `derive_status` models, not a claim the board is lying. Treat it
the same way `board.py`'s own `audit`/`sync` split already treats drift versus
contradiction: confirm the mismatched card is the one the running task owns
and is showing `In review`, and leave it alone. Only run `sync` for a genuine
drift, a card whose status is stale for a reason unrelated to being mid-review.

Fixing this for good means teaching `derive_status` (or the comparison in
`reconcile`, `scripts/board.py:926`) an `In review` case, sourced from the
manifest's `in_review_status` rather than hardcoded, so a Relay-owned card in
review stops reading as drift at all. That has not been done; this file
documents the workaround until it is.
