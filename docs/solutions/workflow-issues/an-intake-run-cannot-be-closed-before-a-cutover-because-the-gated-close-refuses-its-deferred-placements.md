---
title: An intake run cannot be closed before a cutover, because the gated close refuses its deferred placements
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/write/routing_pass.py"
problem_type: workflow_issue
component: seam_design
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A brief or a residual says place_files should close the session it opened, and close_run refuses routing-outstanding the moment it is tried"
  - "assert_cutover_ready refuses cutover-open-run over a landing that finished and was imported"
  - "A search for readers of SessionState.OPEN finds none, and the cutover precheck refuses on the record anyway"
applies_when:
  - "Deciding how an intake session, or any session that records routing intents, reaches a terminal state"
  - "Adding a reader of session records that asks whether a run is still open"
  - "Searching for who depends on a session state before calling it unused"
tags:
  - "session"
  - "deferred-routing"
  - "cutover-precheck"
  - "awaiting-import"
  - "intake"
---

## The trap

R-433 said `place_files` should close the session it opened "through
`routing_pass.close_run` on success". R-501's brief offered a verb that "marks
it closed". Both read as obviously right and neither can be done.

`place_files` records one routing intent per track, because the placement is
deferred until the library holds a row. `routing_pass.close_run` is the only
close the intake and routing packages may use, two AST walks in
`tests/test_deferred_routing.py` enforce that, and it refuses
`routing-outstanding` while a run holds an intent that has not settled. An
intent settles when `route pending` places it, and `route pending` places
nothing until a tree is database native. A tree becomes native at a cutover.
The cutover precheck refuses while any run is not terminal.

So the run cannot close until the cutover, and the cutover cannot pass until
the run closes. That circle is the whole of R-501, and it is invisible from
any one of the four files.

## What was done

The circle is cut at the precheck, the one place where the refusal's own
stated reason is false. It refuses an open run because the run "still holds a
capture and possibly an un-imported export". A landing whose import was proven
against a Fresh Export holds neither. `session.owes_only_deferred_routing`
asks three facts of a record, open, no capture, proof recorded, and the
precheck excuses a run that answers yes to all three. Each is mutation pinned
alone.

Abandoning was the other way to a terminal state and it is ungated, but it
records that a run was given up, which is false of a landing that worked.

The routing pass never reads the intake session record, it works from the
ledger alone, so a proven run staying open costs the deferred placement
nothing. After a cutover `route pending` places the tracks and closes the run.

## Two smaller traps on the same path

**Settled is not imported.** An intent settles by being routed, which takes a
row, or by a person acknowledging the track is gone, which takes none. Treating
"nothing outstanding" as proof of an import records a proof for a run nobody
imported. The built in review caught this in the first cut.

**Search for the property, not the member.** R-433 measured its cost as none
after searching `src` for readers of `SessionState.OPEN`. The reader that
mattered asks `not record.terminal`, and so do doctor and `restore.prune`.
When asking who depends on a state, search for every property derived from it.
