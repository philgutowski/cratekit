---
title: "A mutation zero can mean the value is constant at this entry point, not that it is untested"
date: 2026-08-30
category: workflow-issues
module: "src/cratekit/backup/cli.py, src/cratekit/modules/tools/backup.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_workflow_step
resolution_type: test_fix
applies_when:
  - "A mutation row on a rendered or reported field kills zero tests and the field looks user facing"
  - "A composite for a user facing zero would have to be written through the same entry point the zero was found on"
  - "Two conditions in one call path look similar and one of them raises before the other's value is read"
  - "A property or field is computed from the same inputs an earlier guard in the same function already branches on"
  - "You are about to file a zero row as an ordinary missing-test residual without checking whether the value can vary at all from that entry point"
symptoms:
  - "A mutation that changes `all(...)` to `any(...)`, or an equivalent real semantic change, kills nothing on the full suite"
  - "Writing the composite METHOD's severity floor asks for turns out to require asserting something that is trivially true from every input the entry point accepts"
  - "The rendered field and an earlier raise in the same call share the identical boolean condition, just written once as a guard and once as a value"
  - "A test written to prove the field can be false, driven through the shell, cannot be made to fail no matter what input is constructed"
related_components:
  - development_workflow
  - documentation
  - testing_framework
tags:
  - mutation-testing
  - zero-row
  - unreachable-value
  - upstream-guard
  - layered-testing
  - residual-finding
  - method-compliance
---

# A mutation zero can mean the value is constant at this entry point, not that it is untested

## Context

U45 built `crate backup run`, the CLI shell over the backup engine that had
already shipped: `src/cratekit/backup/cli.py` over
`src/cratekit/modules/tools/backup.py`. The unit merged to `main` as `bc2eff1`
("merge: U45, the backup.run shell and the age the write session consults"),
built on feature commit `2548aca`, test commit `76bc4df`, and docs commit
`5f59b0a`.

Its round-one mutation table, `docs/mutation/u45-round-1.md`, ran 43 rows
across five files and confirmed a green baseline of 6437 collected
(`docs/mutation/u45-round-1.md:5`). Row `E5_outcome_ok_widened` targets
`src/cratekit/modules/tools/backup.py`, widening `BackupOutcome.ok` from an
`all(...)` to an `any(...)` over the exact same clause
(`docs/mutation/u45-round-1.md:1181-1189`):

```python
# old
        return all(p.refusal is not None or p.ran for p in self.portions)
# new
        return any(p.refusal is not None or p.ran for p in self.portions)
```

That property lives at `src/cratekit/modules/tools/backup.py:281-289`. `all`
and `any` disagree on plenty of inputs (a run where every portion refused
except one that genuinely failed, for instance), so this is not a cosmetic
edit, it is a real change to what the property answers. The row killed zero
on the full 6437-test suite anyway, confirmed rather than left on a subset
(`docs/mutation/u45-round-1.md:1174-1177`), and the table's own "Zero rows and
what they owe" section flagged it exactly as METHOD requires: `E5_outcome_ok_widened
(user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it`
(`docs/mutation/u45-round-1.md:65`).

`docs/METHOD.md:101-103` sets the bar for a row shaped like that: "A zero
death row on a guard with a USER FACING surface is acceptable only when a
composite shows what it does hold. Pair it with a mutation of the thing it
guards and report both counts. A prose argument is not evidence." The
question this document answers is what happened when that composite was
attempted, and why the honest answer was not a test but a residual,
`docs/residual-findings.md` R-202 (`docs/residual-findings.md:10204-10236`).

## Guidance

**Trace the call path between where you can drive the mutated line and where
its result would need to differ, and look for a guard that already reads the
same condition.** `outcome_payload`, also in the engine module, renders `.ok`
into the JSON key `"ok"`:

```python
# src/cratekit/modules/tools/backup.py:1105-1109
def outcome_payload(outcome: BackupOutcome) -> dict:
    return {
        "payload_version": PAYLOAD_VERSION,
        "stamp": outcome.stamp,
        "ok": outcome.ok,
```

The shell's `perform_backup` is the only caller in this unit's diff that
reaches `outcome_payload`, and it does not call it directly on
`run_backup`'s result. It calls `refusal_for` first:

```python
# src/cratekit/backup/cli.py:438, 455-458
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
    ...
    refusal = refusal_for(outcome)
    if refusal is not None:
        raise refusal
    report = backup.outcome_payload(outcome)
```

`refusal_for` (`src/cratekit/backup/cli.py:303`) raises on exactly one
condition, computed first in the function body:

```python
# src/cratekit/backup/cli.py:337-342
    failed = tuple(
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
    )
    if failed:
        return refuse(
            "backup-transfer-failed",
```

Read that side by side with `.ok`'s own condition
(`src/cratekit/modules/tools/backup.py:289`):
`all(p.refusal is not None or p.ran for p in self.portions)`. That `all(...)`
is `False` if and only if some portion has `p.refusal is None and not p.ran`,
which is the identical predicate `refusal_for` builds `failed` from. They are
the same boolean condition, read twice: once as a raise-or-not decision in
the shell, once as a rendered field in the engine.

So walk the call path in `perform_backup` to `outcome_payload` and ask what
`.ok` could be there. Either `refusal_for` already raised on this outcome
(because some portion satisfied the falsifying condition), in which case
`outcome_payload` is never reached and no report exists to inspect, or
`refusal_for` returned `None`, which by construction means no portion
satisfies that condition, which is exactly the condition required for `.ok`
to compute `True`. There is no third case. `report["ok"]` in every payload
`perform_backup` successfully returns is therefore unconditionally `True`,
regardless of whether `.ok` is spelled `all` or `any`. The row cannot kill
from that entry point no matter how the input space is varied, because the
input space that would distinguish `all` from `any` is exactly the space
`refusal_for` has already excluded by raising.

**Do not write the composite through the entry point where the zero was
found; write it one layer down, where the excluded input space is still
reachable.** `refusal_for` lives in the shell
(`cratekit.backup.cli`) and is what forecloses the space. `.ok` lives in the
engine (`cratekit.modules.tools.backup`), one layer under the shell, and
`run_backup` itself carries no such guard, so a portion that failed can
reach `.ok` directly there. `tests/test_backup_cli.py:845-877` drives
exactly that, calling `backup.run_backup` (the engine function), not
`perform_backup` (the shell), with a runner that selectively fails one
portion:

```python
# tests/test_backup_cli.py:845-877
def test_the_outcome_answers_not_ok_when_a_portion_failed(cfg, rclone):
    """...:func:`refusal_for` raises whenever a portion failed, which is exactly
    the condition that makes ``ok`` false, so no report this shell can emit ever
    carries ``ok: false``. That is recorded as a residual.

    So the property is driven where it is reachable, on the ENGINE's own return
    value, which this unit is the first caller of. Both directions, because ``all``
    and ``any`` agree on every outcome where nothing failed.
    """
    plan = backup.plan_backup(cfg, now=MOMENT)

    both_fine = backup.run_backup(
        cfg, plan, runner=_answering(0), now=MOMENT, publish=False
    )
    assert both_fine.ok is True, both_fine

    one_failed = backup.run_backup(
        cfg,
        plan,
        runner=_failing_on(backup.SNAPSHOT_DATABASE),
        now=MOMENT,
        publish=False,
    )
    assert one_failed.ok is False, (
        "a portion whose transfer came back non zero left the outcome reporting ok, "
        "so any caller deciding on that field would report a failed backup as done"
    )
    assert [p.ran for p in one_failed.portions] == [True, False], one_failed
```

`_failing_on` (`tests/test_backup_cli.py:189-205`) is a selective runner
built for exactly this shape: uniform failure cannot produce "one portion
completed, one did not", which is the only outcome that separates `all` from
`any` here.

```python
# tests/test_backup_cli.py:189-205
def _failing_on(label: str):
    """A runner that fails only the commands carrying one label. ..."""

    def runner(command: backup.Command) -> backup.CommandResult:
        if command.label == label:
            return backup.CommandResult(returncode=1, stderr="connection refused")
        return backup.CommandResult(returncode=0)

    return runner
```

This test kills `E5_outcome_ok_widened` if you re-mutate the property, and it
does so without going anywhere near `refusal_for`. That is the composite
METHOD asks for, moved to the layer where the guard being composited against
does not already sit in the way.

**When even the lower layer cannot separate the two values, or moving the
test down is not possible for this field, say so as a residual with the
unreachability reasoning spelled out, rather than leaving the zero
unexplained or writing a composite that asserts something trivially true
through the original entry point.** That is what U45 did once it had traced
the path: R-202 (`docs/residual-findings.md:10204-10236`) states the finding
as "`BackupOutcome.ok` can only ever be true in a report the backup shell
emits", gives the exact mechanism (`refusal_for` raises on exactly the
condition that makes `.ok` false), and is explicit about what it is not: "Not
a wrong value. Every `ok: true` this shell emits is true. The finding is that
the field is not load bearing, so a reader who trusts it as the run's verdict
is trusting the exit code twice." It also states why the fix is not this
unit's to make: dropping the key edits `outcome_payload`, a public engine
payload rendered by nothing else today, and reversing `refusal_for`'s
decision reopens an argued design choice (a failed portion earns an exit
code, not a field) rather than a defect in this unit's diff.

**The diagnostic question, stated plainly for reuse:** does anything between
the entry point the zero was measured through and the mutated line already
branch on the exact same condition the mutation changes? If yes, the value
cannot vary from that entry point by construction, and no amount of test
effort spent at that entry point will kill the row. Look one layer down for
an entry point where the excluded input space is still reachable. If none
exists anywhere in the tree, the value truly cannot be observed to differ and
the honest write-up is a residual naming the guard that forecloses it, not a
composite manufactured through the entry point that cannot show it.

## Why This Matters

**A constant-at-this-surface zero looks identical, by row count alone, to an
ordinary missing test**, and the two have opposite remedies. An ordinary gap
gets a test written at the same entry point the zero was found on, the way
the three genuine zeros in U27's round one were closed
(`docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`).
A constant-at-this-surface zero cannot be closed that way: writing "a test
that proves `ok` can be false" through `perform_backup` is not a missing
test, it is an attempt to observe something the shell's own correct behavior
makes unobservable from that vantage point. `refusal_for` is not a defect,
it is doing exactly the job its docstring describes
(`src/cratekit/backup/cli.py:304-336`, "a run in which nothing was backed up
never exits OK"). Treating the zero as a gap and pushing an author to
"just write the test" burns a round chasing a test that cannot be written,
because the input space required does not survive the trip through the
entry point in question.

**It is also not the same shape as an inert mutation.** The corpus already
has that sibling
(`docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`),
where the mutated expression is semantically identical to the original on
the tree under test, so no input anywhere could distinguish the two trees (a
deleted keyword argument whose default equals the deleted value, for
instance). `all` versus `any` over `p.refusal is not None or p.ran` is not
identical in general: give it a portion with `refusal is None` and
`ran=False` alongside a portion with `ran=True`, and `all` returns `False`
while `any` returns `True`. The mutation is live. What is dead is one
specific entry point's ability to ever construct that input, because a
different, correct piece of code sitting between the test and the property
already refuses to let that input exist by the time `.ok` would be read.
The corpus's own diagnostic for an inert row, "sit down to write the test
that would kill the row and state what behaviour it would assert; if you
cannot, the row is inert", gives a false negative here if applied only at
the surface where the zero was found: you genuinely cannot state that
assertion through `perform_backup`, but you can state it one layer down,
through `run_backup` directly. The row is not inert. It is foreclosed at one
specific altitude and open at another.

**Why this shape recurs rather than being a one-off:** a shell that wraps an
engine call and translates the engine's whole-run refusals into exceptions
is, almost by definition, going to re-derive some subset of the engine's own
success/failure logic in order to decide when to raise. Wherever that
re-derivation happens to check the identical condition a downstream rendered
field also depends on, the field becomes constant from any entry point that
goes through the shell's guard. This is a natural consequence of a shell
doing its job (translating conditions to exit codes) rather than a mistake,
which is exactly why it needs a residual rather than a fix: fixing it means
undoing the shell's guard or the field's contract, both of which are design
decisions bigger than a mutation zero.

**The cost of not distinguishing the two:** METHOD's severity floor
(`docs/METHOD.md:101-103`) exists to stop a residual from silently absorbing
an ordinary test gap. Applied indiscriminately to a constant-at-this-surface
zero, it produces the opposite failure: either a round burns cycles trying
to write an impossible composite, or, worse, someone writes a composite that
technically satisfies the letter of the rule by asserting something
trivially true through the same entry point (for instance, asserting
`report["ok"] is True` twice, once per branch, which the U45 test's own
docstring explicitly declines to do: "This file asserts `report["ok"] is
True` twice and never the other value" `tests/test_backup_cli.py:849-850`),
manufacturing the appearance of coverage over a property nobody actually
drove both ways.

## When to Apply

- A mutation row on a rendered or reported field (a JSON key, a summary
  count, a status string) kills zero, and the field looks user facing.
  Before writing a composite, find every call site between where you can
  test and where the field is built, and check whether any of them already
  branches on the mutated condition.
- Writing the composite would mean asserting something through the same
  entry point the zero was measured on, and doing so feels like it is
  proving nothing new. That feeling is the signal: check whether an earlier
  guard already forecloses the case you are trying to construct.
- Two pieces of code in the same call path compute what reads as two
  different things (a raise decision, a rendered value) from what turns out
  to be the identical boolean expression, just spelled once each. Read them
  side by side rather than trusting that "guard" and "field" are different
  concerns.
- You are about to move a test down a layer, from the shell to the engine
  it wraps, specifically to reach an input space the shell's own correct
  behavior excludes. Confirm the lower layer genuinely has no equivalent
  guard before assuming it is reachable there.
- Nothing reachable anywhere in the tree can vary the value. Write the
  residual with the specific unreachability reasoning (which guard, which
  condition, why it is the same condition) rather than leaving the zero row
  unexplained or forcing a composite that cannot demonstrate anything.

## Examples

The full round-trip, in the order it was actually worked:

1. The mutation, `docs/mutation/u45-round-1.md:1181-1189`, real and not
   inert: `all(p.refusal is not None or p.ran for p in self.portions)` to
   `any(...)`, at `src/cratekit/modules/tools/backup.py:289`, confirmed zero
   on 6437 collected on the full suite.
2. The trace, `src/cratekit/backup/cli.py:438, 455-458`, showing `refusal_for`
   runs and can raise before `outcome_payload` is ever called inside
   `perform_backup`.
3. The shared condition, `src/cratekit/backup/cli.py:337-339` next to
   `src/cratekit/modules/tools/backup.py:289`: `failed = tuple(entry for
   entry in outcome.portions if not entry.ran and entry.refusal is None)`
   against `all(p.refusal is not None or p.ran for p in self.portions)`.
   `failed` is non-empty exactly when the `all(...)` is `False`.
4. The lower-layer composite that actually kills, driving the engine
   directly and bypassing the shell's guard: `tests/test_backup_cli.py:845-877`,
   using the selective-failure runner `tests/test_backup_cli.py:189-205`.
5. The residual filed instead of a shell-level fix, `docs/residual-findings.md`
   R-202 (`:10204-10236`), naming the mechanism, the two remedies that would
   belong to other decisions, and stating explicitly that no value emitted is
   wrong, only unreachable-as-false at that surface.

## Related

- `docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`,
  the closest sibling: both documents are about a zero row's meaning not
  being obvious from the row alone. That document's mechanism is an inert
  mutation, where the new text is semantically identical to the old text on
  every input, so no test anywhere could kill it and the correct move is to
  replace the row. This document's mechanism is different: the mutation is
  semantically live in general, and only becomes unobservable at one
  specific entry point because a correct, unrelated-looking guard upstream
  in the same call path already excludes the input that would distinguish
  the two values. The remedy differs accordingly: an inert row gets replaced,
  this row gets its test moved to a layer where the excluded input space is
  still reachable, or gets filed as a residual with the specific
  unreachability reasoning if no such layer exists.
- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`,
  U45's own worked case for a different lesson. That document is about U45
  becoming the first `src` caller of `cratekit.modules.tools.backup.run_backup`
  and inheriting whatever that callee's unreviewed failure paths turn out to
  hold. This document picks up one layer further downstream, on a field
  `run_backup`'s own outcome type computes correctly, and is about diagnosing
  why a real mutation to that field's logic cannot be observed from the
  shell U45 built over it. Same unit, same call path, two distinct lessons:
  one about ownership of a callee's untested branches, one about a value made
  constant by a correct guard sitting between the test and the value.
- `docs/METHOD.md:101-103`, the user-facing zero composite rule this finding
  had to satisfy or reclassify against.
- `docs/mutation/u45-round-1.md`, the table row (`E5_outcome_ok_widened`) and
  its "Zero rows and what they owe" line.
- `docs/residual-findings.md` R-202, the filed finding.
- Merge commit `bc2eff1`, "merge: U45, the backup.run shell and the age the
  write session consults".
