---
title: The lock file cannot prove who owned a session record, so the record carries its own holder
date: 2026-09-21
category: workflow-issues
module: "src/cratekit/core/session.py"
problem_type: workflow_issue
component: seam_design
root_cause: incorrect_assumption
resolution_type: code_fix
severity: medium
symptoms:
  - "A gated write was SIGKILLed and its session record reads `open` for ever"
  - "The cutover precheck refuses with `cutover-open-run` and its first step is one no verb offers"
  - "`session release` reports nothing recorded, although a dead process left the record"
applies_when:
  - "Deciding whether some state a process left behind can be cleaned up because that process is gone"
  - "Reusing the stale lock proof (`holder_alive`) for anything other than the lock itself"
  - "Staging a hard kill in a test"
  - "Judging a holder recorded by another boot, or comparing process start times across boots"
  - "Adding an open state that can outlive its process on purpose, like an intake landing"
tags:
  - "session"
  - "lock"
  - "hard-kill"
  - "holder"
  - "r-598"
  - "r-647"
  - "power-loss"
  - "machine-identity"
---

# The lock file cannot prove who owned a session record

## Problem

A gated write that is hard killed runs no exit code, so the session record the
gates opened stays `open`. The ledger entry and the card both suggested
`session release` as the fix, on the reasoning that it already proves the lock's
holder is dead and a record opened under that lock belongs to the same process.

## Why the obvious fix does not hold

The lock file names only the LAST holder. On a local filesystem the kernel drops
the lock when the process dies, so the next gated session acquires it and
overwrites the holder record. The gates do not refuse on an open record, only on
a `committed-unverified` one, so that next session runs. After it, the lock file
names a live or cleanly finished process and says nothing about the one that
left the record. A release keyed on the lock file's holder would work only if
the person ran it before any other write, which is not a property a verb can
rely on.

## What was done

The record carries its own copy of the holder. `assert_gates` works out one
claimant, `holder or current_holder()`, and hands the same value to the lock and
to the record, under `detail.holder`. `session.orphaned` then asks three things
of a record: the state is exactly `open`, a holder is recorded, and
`holder_alive` says that holder is gone.

Each condition keeps a record somebody still needs:

- `awaiting-import` is ended by an import and `committed-unverified` by a
  restore. Widening the state check to `not terminal` abandons both.
- An intake landing opens without the lock, names no holder, and stays `open`
  across processes ON PURPOSE when its only debt is a deferred placement
  (R-501). Reading "no holder" as "holder gone" would end every one of them.
  That is the trap in this area: `open` does not mean "a process is running".
- `holder_alive` fails towards alive on another host and a missing start time.
  A power loss, where the holder is from the previous boot, was not proven gone
  until R-647 added a machine identity two machines cannot share. See the
  section below before touching the cross boot judgment.

## Judging a holder from another boot (R-647)

The host name is not the proof, because two machines share one and a library
drive moves between them. The holder records `machine`, a digest of the
platform's machine identifier, and `_gone_since_an_earlier_boot` needs it known
and equal on both sides, the recorded boot earlier past `BOOT_DRIFT_SECONDS`,
and no live process with the recorded identifier.

**Do not compare start times across boots.** The boot identity is
`psutil.boot_time()`, a wall clock reading that a stepped clock moves. On Linux
psutil also derives a process's start time from that boot reading plus a tick
count, so a forward step moves a LIVE holder's boot and its start time by the
same amount. Read after the step, that holder looks like an earlier boot whose
identifier was recycled, and a start time comparison clears its claim mid write.
The first build did exactly that and the built in review caught it. On macOS the
start time is a fixed reading taken at launch, so a suite running there cannot
show the failure; the test that pins it models the Linux shape by hand. Any live
process with the identifier keeps the claim instead, and the cost is a record
kept until an unrelated process that inherited the number exits.

Test the cross boot judgment with an explicit `here=` holder carrying a pinned
machine and a numeric boot, and pin `machine_identity` with monkeypatch in verb
level tests, so no test depends on what the platform reports.

## Staging a real hard kill in the suite

A gate entered and never exited in the test process is not a kill: the lock
stays held by that process and the record's holder is alive. Fork instead. The
child inherits the test's monkeypatched platform seams, enters the gates with
`Keep.RECORD`, and sends itself `SIGKILL`. The parent waits and asserts the child
died by that signal. Put `signal.alarm` in the child, because a lock another
thread held at the fork stays held in the child and would hang the suite
instead of failing it. Every path in the child ends in `os._exit`. See
`_hard_killed_gated_write` in `tests/test_session_cli.py`.

Do not add a `pytest.mark.skipif` for platforms without fork. The pending
registry refuses a skip built anywhere but `tests/_pending.py`.

## An explicit gate's answer is not bound to what its question showed

The question and the answer are two invocations. `session.release.confirm`
declares no digest, so the answering invocation acts on what it reads then, not
on what was shown. Narrowing the engine to a list the shell hands it does not
help, because the shell builds that list in the answering invocation. The
mutation row for that narrowing is a zero for exactly this reason. Binding needs
`digest_source` on the gate, which is R-648.
