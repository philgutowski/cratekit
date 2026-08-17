---
title: A confirm gate does not accept the review items it confirms
date: 2026-08-17
category: workflow-issues
module: src/cratekit/deletion/cli.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - A CLI verb both offers review-queue items and declares an explicit confirm gate
  - The handler requires a confirm option and then calls run.apply
  - apply is about to move files that present just offered and nobody has resolved
  - A new confirm-gated destructive verb is being composed from plan, present, gate, apply
  - A CLI drive of that verb never sends one real deletable file through the dispatcher
symptoms:
  - The confirm option is honoured and the envelope reports OK, and no file moves
  - run.apply skips every offered item because decided.get(_item_id) is None
  - The review store still holds open items whose verdict is None
  - The suite stays green because every CLI drive leaves the deletable set empty
  - The person who confirmed trash believes the files were moved
related_components:
  - testing_framework
tags:
  - silent-failure
  - cli
  - confirm-gate
  - review-queue
  - accept-all
  - deletion
  - verdict
  - green-suite
---

# A confirm gate does not accept the review items it confirms

## Context

Cratekit splits deletion into two layers, and the split is load bearing rather
than decorative. The engine in `cratekit.deletion.run` offers review items and
later moves files. The shell in `cratekit.deletion.cli` puts a person in front
of those two acts. The engine will not infer a confirmation from a CLI gate. It
reads persisted verdicts. The shell that forgets to write those verdicts can
still exit OK.

`run.apply` (`src/cratekit/deletion/run.py:701`) states its job as trash every
confirmed file. Confirmation is not a flag on the call. It is a review item
whose verdict is already `Verdict.ACCEPTED`. `_verdicts` at
`src/cratekit/deletion/run.py:375` walks the deletion queue with
`include_resolved=True` and keeps only items where `item.resolved` is true.
`Item.resolved` at `src/cratekit/core/review.py:474` is `self.verdict is not
None`. An offered item with no verdict is absent from that map.

The apply loop at `src/cratekit/deletion/run.py:820` then does this, in order:

1. `decided.get(_item_id(item))` is `None`: the row is unanswered. The loop
   continues. Nothing is moved.
2. `verdict.verdict is review.Verdict.REJECTED` (`run.py:833`): the row is a
   recorded decline. The file stays. The watermark does not pass over it.
3. Everything that remains has verdict ACCEPTED. Later checks can still
   refuse a move: the candidate is no longer deletable, the re-check fails,
   or the shown path no longer matches.

`Verdict` at `src/cratekit/core/review.py:161` has two members, `ACCEPTED` and
`REJECTED`. After the two continues above, the remaining path is ACCEPTED. That
is the whole of "apply only moves candidates whose review item already has
`Verdict.ACCEPTED`."

`run.present` (`src/cratekit/deletion/run.py:329`) puts every deletable
candidate in the queue. It does not resolve anything. Re-offering returns the
item that is already there, including a verdict somebody already recorded
(`run.py:338`). A first offer arrives with `verdict is None`.

The engine tests already knew this contract. `_confirm` at
`tests/test_deletion.py:984` is three lines that open the store and call
`review.resolve`. Every engine test that moves a file goes through it first.
`test_a_confirmed_file_is_trashed_and_leaves_a_tombstone` at
`tests/test_deletion.py:1001` is the pattern: plan, present, `_confirm` at
`:1007`, then `apply` at `:1009`.

The leftover U24 shell did not do that. It required the explicit confirm gate
and then called `apply`. The offered items were still open. `apply` skipped
every one of them. The envelope was still OK.

A person answered trash. The run reported success. Nothing moved.

The battery did not catch it. Conformance and the first-run CLI tests stay
green because a first-run baseline has no deletable files, so `apply` is never
reached. `review_removals` at `src/cratekit/deletion/cli.py:152` returns OK as
soon as `found.baselined or not found.deletable`.
`test_delete_review_exits_ok_after_the_recorded_decision` at
`tests/test_deletion.py:5948` drives the two-act path against that first run
and asserts `items == []` and `unresolved == 0` (`:5961` and `:5962`). The
gate fired. The resume exited OK. The trash path was never entered.

The verified fix is on `main` at the U24 leftover merge `ce7f55d`. After the
gate returns trash, the shell resolves still-open offered items as `ACCEPTED`,
leaves recorded rejects alone, and only then calls `apply`.
`test_delete_review_trashes_a_confirmed_file` at
`tests/test_deletion.py:5977` drives a real file through the dispatcher into
Trash. That test is the pin. The engine suite was never going to grow it,
because the engine suite already wrote the verdict itself.

This is not the first-run watermark write that `docs/residual-findings.md`
already records as R-134. That finding is an earlier act on the same verb:
`plan` accepts history before anyone can refuse. This learning is the later
seam: after a person answers trash, the gate still has not written
`Verdict.ACCEPTED`.

## Guidance

Treat the confirm gate and the review verdict as two writes, not one idea
spelled twice.

The gate is R34's recorded act: this invocation may proceed. `apply` does not
read the gate. It reads the deletion queue. A shell that requires the gate and
then calls `apply` has confirmed the run and has not accepted a single item.

After the gate returns the affirmative option, and only then:

1. Walk the items `present` just returned, not a fresh listing. Those are the
   items the digest covered.
2. Resolve each still-open item as `Verdict.ACCEPTED`. `review.resolve` at
   `src/cratekit/core/review.py:1247` refuses an already resolved item rather
   than overwriting it, so the filter `if item.verdict is None` is required,
   not polite.
3. Leave a recorded `REJECTED` alone. `present` is idempotent and returns that
   verdict (`run.py:338`). Honouring it is how a decline survives a later
   trash confirmation of the rest of the set.
4. Call `apply` only after those verdicts are in the store.

Do not invent a second confirmation inside `apply`. The engine is correct. The
hole is the shell that forgot the engine's input.

Do not treat a first-run OK, or a conformance OK, as evidence that trash
works. Those paths return at `cli.py:152` before `apply` is named. A test that
never plants a deletable file after a baseline cannot see this defect. The
test that can is the one that:

- baselines the watermark itself, so the run is not a first run
- plants a removed row whose file is on disk and unreferenced
- drives `cratekit.cli.run` the way the dispatcher actually runs
- records the trash decision through `run decide`, not by calling `_confirm`
- resumes the same run
- asserts the file is gone and something landed in Trash

`_confirm` is the engine helper. Using it in a CLI test would rebuild the
blindness: the test would write the verdict the shell was supposed to write,
then certify the shell.

The same shape will recur on any later verb that both offers review items and
declares an explicit confirm gate. The engine will keep requiring ACCEPTED.
The gate will keep looking like the confirmation. The first-run fixture will
keep having nothing to delete. Write the verdicts, and drive one real file
through the dispatcher, or the next shell ships the same no-op.

Do not reopen U25 for this. The defect was in the leftover U24 shell.

## Why This Matters

The failure is silent in the way this repository has already paid for
elsewhere. The run does not refuse. It does not warn that zero files moved.
It reports OK. A person who confirmed trash reasonably believes the files are
in the Trash. They are still on disk. The review items are still open.

That is worse than a refusal. A refusal names a remedy. An OK that moved
nothing names nothing. The person has no reason to look.

The suite that should have caught it cannot see it, and for a structural
reason rather than a missed assertion. `cli.py:138` says apply runs only when
there is something deletable. A first-run baseline writes the watermark
inside `plan` and must not open a destructive session to move zero files.
That early return is right. It is also a wall in front of the only function
that would have revealed the missing verdicts. Conformance holds every
declared gate to firing. It does not hold the verb to moving a file.

So the green battery here is the same class of blindness as a subset run that
never names a file that failed to collect. The tests that ran are not the
tests that could fail.

The engine suite cannot compensate. It calls `_confirm` before `apply`. That
is the correct way to test the engine. It is a tautology as a test of the
shell: of course `apply` moves a file whose verdict the test just wrote. The
shell's job is to write that verdict from the gate. Nothing in the engine
suite invokes the shell.

The cost of getting this wrong is not a failed test. It is a successful
deletion pass that deleted nothing, reported as success, against a library
the person just confirmed they wanted cleaned.

## When to Apply

- A new shell over `run.apply`, or over any other apply that reads
  `_verdicts` or `item.resolved` before it mutates.
- A change to `review_removals` that looks like it can drop the resolve loop
  because "the gate is the confirmation." The comment at `cli.py:154` exists
  because that sentence is how the no-op shipped.
- A CLI test for such a verb that only drives a first run or an empty
  deletable set. That test is necessary for the gate. It is not a drive of
  apply. Add the dispatcher test that plants a real file.
- Any later unit that copies the delete.review shape: present, require a
  gate, then apply. Copy the resolve loop and the dispatcher test together,
  or the copy is the defect.

Do not apply this as a reason to weaken `apply`. The engine's refusal to
move an unanswered item is the safety. The shell must meet that safety, not
route around it.

Do not apply this as a reason to reopen U25.

## Examples

The silent shell, reconstructed from the contract `apply` still enforces and
from the comment the fix left at `src/cratekit/deletion/cli.py:154`. The tree
no longer holds this sequence. This is the shape that shipped the no-op:

```python
found = run.plan(cfg, handle, actor=ctx.args.actor)
offered = run.present(cfg, found, handler_key=ctx.entry.handler_key)
option = ctx.gate.require(spec, digest=_plan_digest(found))
if option == "abort":
    return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.NO_OP)
if found.baselined or not found.deletable:
    return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.OK)
run.apply(cfg, handle, actor=ctx.args.actor)
return ctx.envelope(data=_payload(cfg, offered), outcome=Outcome.OK)
```

`present` has offered items with `verdict is None`. The gate has recorded
trash. `apply` loads `_verdicts`, finds none of those items resolved
(`run.py:375` and `run.py:822`), continues, and returns a report whose
`trashed` tuple is empty. The envelope is still OK.

What `apply` does with that unanswered item, on the current tree at
`src/cratekit/deletion/run.py:820`:

```python
verdict = decided.get(_item_id(item))
if verdict is None:
    held = _the_anchor_proved_nothing(item, found.references)
    _warn_that_an_unanswered_removal_is_being_retired(
        item, recorded=recorded_now, held=held
    )
    handled.append((item.row.sequence, item.handled and not held))
    continue
```

No move. The candidate is treated as unanswered, because it is.

The engine tests never saw this because they do not take that path. They
write the verdict first, at `tests/test_deletion.py:984`:

```python
def _confirm(cfg, item_id, verdict=review.Verdict.ACCEPTED):
    with review.open_store(cfg) as store:
        review.resolve(store, item_id, verdict, actor="cli")
```

and only then call `apply` (`tests/test_deletion.py:1009`).

The first-run CLI test also never saw this. After the two-act resume it
asserts an empty review set (`tests/test_deletion.py:5961`), which is
correct for a baseline and which returns at `cli.py:152` before apply.

The fix on `main` at the U24 leftover merge `ce7f55d`, current text at
`src/cratekit/deletion/cli.py:154`:

```python
# THE GATE IS THE CONFIRMATION OF THE OFFERED SET. apply only moves
# items that already have a verdict, so an unanswered offer would
# make "trash" a no-op. Honour a recorded reject; accept the rest.
with review.open_store(cfg) as store:
    for item in offered:
        if item.verdict is None:
            review.resolve(
                store,
                item.item_id,
                review.Verdict.ACCEPTED,
                actor=ctx.args.actor,
            )
run.apply(cfg, handle, actor=ctx.args.actor)
```

Still-open items become ACCEPTED. A recorded REJECTED stays REJECTED,
because `resolve` is not called for it and would refuse if it were
(`review.py:1267`). `apply` then sees those verdicts through `_verdicts`
and moves only the accepted files.

The pin that a first-run test cannot be, at
`tests/test_deletion.py:5977`. It baselines the watermark at sequence 40,
plants a removed row at sequence 50, drives the real dispatcher, records
trash through `run decide`, resumes, and asserts the file is gone:

```python
def test_delete_review_trashes_a_confirmed_file(review_cli, tmp_path, monkeypatch):
    """The gate is the confirmation: a deletable file lands in the Trash."""
    ...
    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    run_id = json.loads(out)["run_id"]
    code, _, err = _drive(
        ["run", "decide", run_id, "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), err
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    assert not music.exists()
    assert any(home.joinpath(".Trash").iterdir()), "the confirmed file never reached the Trash"
```

`_drive` at `tests/test_deletion.py:5878` is `cratekit.cli.run`. The test
does not call `_confirm`. If the resolve loop at `cli.py:157` disappeared,
this test would fail, and the engine suite would still be green.

## Related

- `docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md`:
  the same blindness class on a different surface. A countdown discharge
  that edits the register and leaves `@requires` in place takes a whole
  file out of collection. A subset run that never names that file looks
  green. Here, a first-run CLI test that never reaches `apply` looks
  green. In both cases the suite that ran is not the suite that could
  fail, and the remedy is to stop reading an OK on the path that cannot
  see the defect.
- `docs/solutions/workflow-issues/a-watermark-as-date-floor-rebuilds-the-silent-empty-run.md`:
  another OK-and-empty success. That document owns the sync date-floor
  form and already says deletion's sequence watermark is not that bug.
  The empty success here is a missing `Verdict.ACCEPTED` after the
  confirm gate, not a watermark used as a floor.
- `tests/test_deletion.py:984` (`_confirm`) and
  `tests/test_deletion.py:1001`
  (`test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`): the
  engine's correct use of the verdict contract. Companion, not
  substitute. They prove `apply`. They do not prove the shell.
- `src/cratekit/core/review.py:1247` (`resolve`): a verdict is written
  once. The shell's `if item.verdict is None` filter is what keeps a
  recorded reject from colliding with that rule when the gate says trash.
