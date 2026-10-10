---
title: "A gated write verb plans on a read handle, and its own stale check is reached only by a test with no gate in front"
date: 2026-10-09
category: workflow-issues
module: "src/cratekit/intake/inspiration_cli.py, src/cratekit/intake/set_playlist.py, tests/test_cli_contract.py, scripts/mutate.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
resolution_type: code_change
applies_when:
  - "A new verb that writes the database through a plan and an explicit gate fails conformance 3 with app-version-pin-unrecorded on the conformance fixture"
  - "A mutation row on a verb engine's own digest or stale check kills zero tests while a CLI test for the same situation passes"
  - "A new gated verb is modelled on intake land's ask_then_write rather than on inbox rotate's planned and written"
tags: [conformance, gate, read-handle, write-handle, mutation, zero-row, covered-guard, u121, inbox-rotate]
---

# A gated write verb plans on a read handle, and its stale check needs a gateless test

## What bites, twice

**First, at the conformance suite.** `crate intake inspiration` was first
written on `land_cli.ask_then_write`, which opens the database WITH WRITE
INTENT before the plan so a running rekordbox refuses before anything is shown.
Conformance 3 drives every gated verb to OK on the conformance fixture, and that
fixture has no rekordbox pin recorded, so the write intent open refused with
`app-version-pin-unrecorded` before the gate was ever reached, and the test
read that as a verb that does not reach its declared gate. `intake land`
survives the same suite only because its native gate is exempted: the fixture's
intake tree is on the bridge, so the write intent open never happens there.

The shape that passes is the rotation's, `inbox_rotate`: plan on a handle
opened to read (`require_closed=False, check_app_version=False`), read the
acknowledgment, ask the gate over the digested plan, then open a second handle
with write intent and TAKE THE PLAN AGAIN on it, refusing a digest that moved.
A verb written that way reaches its gate on the pinless fixture and still
writes nothing there, because its sample plan is empty.

**Second, at the mutation table.** That second plan on the write handle is a
guard, and the two rows that reverted it (the digest compare, and the removed
folder check inside the write) killed zero tests, promoted to the full suite.
The CLI tests for exactly those situations passed with the guards gone, because
the GATE re-plans on every acting drive and compares its own digest: a
collection or folder that moved between the two acts is refused by the gate
before the engine's check is reached. The engine's check is reached only by a
caller with no gate in front, which no CLI test is.

## What to do

- Model a new gated database verb on `inbox_rotate`'s `planned` and `written`,
  not on `ask_then_write`, unless its gate is genuinely unreachable on the
  conformance fixture and says so in `UNREACHABLE_GATES`.
- When a mutation row on an engine's own stale or digest check is zero, do not
  argue that the gate covers it. METHOD's rule is that a guard covered by
  another guard is a guard nothing covers. Write the test that calls the engine
  directly, `inspiration_cli.written(...)` or `set_playlist.write_members(db,
  plan)` on an open handle after changing the database underneath it, and
  measure the row again. Both became one kill each on U121.
- A removed node must be removed ON THE OPEN HANDLE for the engine test
  (`setattr(row, SOFT_DELETE_COLUMN, 1)` and `session.flush()`), since a change
  made through a second connection is not seen by a row the session already
  loaded.

## What else the table taught

- A mutation that widens a match state can be inert rather than a gap: a row
  resolving `needs_review` carries no `paths` at all, its candidates ride in
  `candidates`, so widening `is MATCHED` to `is not MISSING` tied nothing. A
  probe under `tests/` settles inert against gap in one run; reasoning from the
  unmutated tree does not.
- A rows file written through a shell heredoc turned `–—` into the
  characters themselves, twice, and the row was refused twice as "old text is
  not present". Write a row whose text carries backslash escapes through
  Python, and assert the TOML's `old` against the source before the driver
  runs.
