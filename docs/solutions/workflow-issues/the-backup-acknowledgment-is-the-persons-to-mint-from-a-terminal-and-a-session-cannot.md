---
title: The backup acknowledgment is the person's to mint from a terminal, and a session cannot mint it or answer it into existence
date: 2026-09-16
category: workflow-issues
module: src/cratekit/session/cli.py, src/cratekit/core/session.py, src/cratekit/cli/gates.py
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - An attended sitting is about to run any destructive verb, a restore, a write session, a vocal restamp
  - A session's shell, including the Claude Code Bash tool, hits backup-acknowledgment-missing
  - crate run decide reported ok for session.ack.backup and the next command still says ACK_REQUIRED
  - The last acknowledgment is more than twelve hours old
symptoms:
  - "this destructive session has no backup acknowledgment within its validity window"
  - "backup-acknowledgment-no-terminal: this invocation has no controlling terminal"
  - run.decide reports ok and read_acknowledgment still returns None
  - A session ack run is marked failed after a continuation from a shell with no terminal
related_components:
  - cli_gates
tags:
  - attended-sitting
  - backup-acknowledgment
  - destructive-session
  - explicit-gate
  - terminal
  - r34
---

# The backup acknowledgment is the person's to mint from a terminal, and a session cannot mint it or answer it into existence

## Context

Every destructive verb in Cratekit runs behind `session.assert_gates`, and one
of its three gates is `assert_backup_acknowledged` in `core/session.py`. It
reads a record on the library volume, `.cratekit/local/backup_ack.json`, and
refuses when the record is absent or older than `DEFAULT_ACK_VALIDITY`, which
is twelve hours. The docstring is exact about what it is not: "there is no
parameter here that says yes, and the gate deliberately has no way to be told
to skip itself."

The record is minted by `crate session ack`, and that verb is shaped as two
invocations on purpose, R34. The first invocation discovers the explicit gate
`session.ack.backup`, prints both backup ages, and exits `DECISION_REQUIRED`
naming a run. A person answers with `crate run decide <run>
session.ack.backup acknowledged`. A second invocation, `crate --run <run>
session ack`, reads the recorded answer, calls `session.record_acknowledgment`,
and pops the decision so the run cannot be re-driven into a second window. An
inline `-d session.ack.backup=acknowledged` is refused whatever the run holds,
which `cli/gates.py` explains at length: the thing the gate protects must not
be able to answer it.

`record_acknowledgment` refuses without a controlling terminal, and that
refusal is what stops a detached job from minting the gate that stands in
front of every destructive write.

The second attended U29 sitting, 2026-09-16, paid for the shape. The restore
rehearsal for R-9 refused on `backup-acknowledgment-missing` from the
session's Bash tool. The operator ran `crate session ack` and `crate run
decide` through the `!` prefix and both reported ok. The session then ran the
continuation itself, from the Bash tool, which has no controlling terminal.
It failed `ACK_REQUIRED` with `fix: crate session ack`, marked that run
failed, and wrote nothing: `read_acknowledgment` still returned `None`. The
same three commands from a Terminal window, run by the operator, minted the
record in one round, the actor recorded as the account on this machine, and the rehearsal then passed the
gates. Two rounds were spent learning that `run.decide: ok` is an answer on
record and not an acknowledgment on record. R-369 carries the message defect.

## Guidance

Treat the acknowledgment as the person's act, done in a real terminal, before
the session reaches for a destructive verb. Concretely, at the start of any
attended sitting that will write:

1. Check the record first, from the session, read only:
   `session.read_acknowledgment(cfg)` returns the actor, `recorded_at` and
   `expires_at`, or `None`. Do not start a destructive verb to find out.
2. When it is absent or expired, hand the person three commands for a
   Terminal window, not the `!` prefix, not the session's shell:
   `crate session ack`, then `crate run decide <run> session.ack.backup
   acknowledged` with the run id the first command printed, then
   `crate --run <run> session ack`. The third command is the one that writes.
3. Read the record again before proceeding, and quote the actor and the
   expiry in the sitting's record. The window is twelve hours, so a sitting
   that runs past it needs a fresh mint, and a session that starts the next
   morning almost certainly does.
4. Never run the continuation from the session. It will fail for the right
   reason, and it will leave the run marked failed, so the person has to open
   a new one.

Do not read this as a gate to route around. There is no flag, and the
refusal without a terminal is the property that makes the acknowledgment mean
something: it was made by a person who was there.

## Why This Matters

The gate is what stands between a detached worker and a restore over the live
database. Its whole value is that nothing automated can satisfy it. A session
that tries to help by minting it is trying to remove that value, and the
product is right to refuse. What the session can do is tell the person
exactly what to type, where, and read the result back. The cost of not
knowing this is not damage, it is two lost rounds and a failed run at the
moment an attended sitting is the expensive resource in the room.

## When to Apply

- Before the vocal restamp R-133, the first write the cutover will run on the
  live library.
- Before any restore, including a rehearsal into a scratch directory, since
  `restore_under_one_session` enters `recovery_session` and that holds all
  three gates unchanged.
- Whenever a sitting resumes after a break, because the window is twelve hours
  and the doctor does not report the acknowledgment's age.

## Related

- `docs/residual-findings.md`, R-9: the sitting this was learned in, and the
  restore rehearsal it unblocked.
- `docs/residual-findings.md`, R-369: the message that sends the person back
  to `crate session ack` after a continuation with no terminal.
- `src/cratekit/session/cli.py`, `ack`: the two invocation shape and why the
  decision is spent after the mint.
- `src/cratekit/cli/gates.py`: why an inline answer to this gate is refused
  whatever the run already holds.
