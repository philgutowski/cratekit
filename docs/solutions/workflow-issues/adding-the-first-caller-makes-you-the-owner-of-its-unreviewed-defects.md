---
title: Adding the first caller to an existing function makes you the owner of its unreviewed defects
date: 2026-08-23
category: workflow-issues
module: "src/cratekit/modules/tools/backup.py, src/cratekit/session/restore_cli.py"
problem_type: workflow_issue
component: development_workflow
root_cause: missing_workflow_step
resolution_type: code_fix
severity: high
symptoms:
  - "A restore whose every rclone copy failed exits OK and reports two transfers completed"
  - "The live master.db-wal is deleted and master.db is unchanged after that failed restore"
  - "run_restore's own suite drives it extensively and never once returns a nonzero CommandResult to it"
  - "run_backup reads result.returncode in its own body and again in its only helper, and run_restore's performing half reads it nowhere"
  - "A review returns BLOCKING on a defect that predates the branch, and the branch is still what owns it"
applies_when:
  - "A unit adds the first caller in src to an internal function that already existed on main"
  - "A review returns a finding against code the unit did not write, and ownership is being decided"
  - "A callee's own suite is green and no test has ever handed it a failing result object"
  - "A sibling function in the same file already reads the return code the function under review ignores"
  - "A destructive clear runs before the transfer it protects, so a failed transfer leaves the world half changed"
related_components:
  - "testing_framework"
tags:
  - "first-caller"
  - "reachability"
  - "dormant-defect"
  - "silent-failure"
  - "return-code"
  - "merge-bar"
  - "restore"
  - "green-suite"
---

# Adding the first caller to an existing function makes you the owner of its unreviewed defects
## Context

U27's last owed module, `cratekit.session.restore_cli`, merged to `main` as
`363823d`. The fix inside it is `ebdfa05`, verified reachable from `main` with
`git merge-base --is-ancestor ebdfa05 main`, which returned exit 0. This
repository forbids pull requests by contract, so the commit is the citation and
there is no PR number to give.

An independent adversarial review returned BLOCKING on that branch, and the
finding was not in a line the unit wrote. It was in
`cratekit.modules.tools.backup.run_restore`, which landed in U35 as `c09fea8`
and which this unit did not touch. What the unit did was call it.

`run_restore` clears the live database's write ahead sidecars, then hands each
rclone command to a runner, and never read a return code. Its sibling
`run_backup`, defined 339 lines earlier in THE SAME FILE at
`src/cratekit/modules/tools/backup.py:635`, has always read
`result.returncode` and recorded a failed portion. So the checking path already
existed inside the same module and this one call site was the hole, which is
`docs/METHOD.md:163` exactly, pattern 3, "a fix that lands on the performing
path instead of the checking path".

The defect sat on `main` doing nothing, because `run_restore` had NO CALLER
ANYWHERE IN `src`. Verified by `git grep -n "run_restore" 6c4f12d -- src`,
which returns two hits, the `def` at `:969` and the `__all__` entry at `:1093`,
and nothing else. Its own suite drove it six times across three files and every
one of those six handed it a runner that returns zero. Then
`src/cratekit/session/restore_cli.py` became the first caller, at `:511` in
`e2dd532` and `:546` at `HEAD`, and the same grep over `e2dd532` finds it.

That is what turned a dormant defect into a BLOCKING one under the merge bar at
`docs/METHOD.md:15`, whose third condition is "its input is reachable, and the
producer was DRIVEN". The input was not reachable the day before. It was
reachable the day this unit landed, and the unit is what made it so.

## Guidance

**Adding the first caller to an existing internal function makes you the owner
of its unreviewed defects.** The question that decides whether a finding is
yours or somebody else's is not who wrote the line. It is "was this reachable
before my change". If the answer is no, the finding belongs to the change that
made it reachable, and it counts against that change's merge bar rather than
being filed as an old problem in an old module.

**The cheap check, before the call is written.** Grep for the function's
existing callers in `src`:

    git grep -n "run_restore" -- src

If that returns only the definition and an export line, you are the first
caller. Read the function's failure paths yourself, and drive at least one of
them before you merge. An old function with a green suite is not a reviewed
function. It is a function whose tests were shaped by whoever last had a reason
to care, and a path nobody called is a path nobody shaped a test for.

**"No caller" does not cause the defect, it hides it, and the sibling is the
proof.** `run_backup` has no caller in `src` today either, verified at `HEAD`,
and it reads its return codes anyway. Two functions in one module, equally
uncalled, one checked and one not. Absence of a caller is what let the
difference between them go unnoticed for a whole unit, not what created it.

**Land the fix on the checking path, so every future caller is covered rather
than the one you added.** The fix could have gone in the new verb, reading the
results after the call. It went into `run_restore` instead, in `_ran` at
`src/cratekit/modules/tools/backup.py:1035`, whose docstring names the
measurement it exists because of:

```python
def _ran(results: tuple[CommandResult, ...], plan: RestorePlan) -> tuple[CommandResult, ...]:
    """Every transfer's return code, READ. Raises on the first one that failed.
```

and whose reading is four lines of it:

```python
    for command, result in zip(plan.commands, results, strict=True):
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

`Refusal.RESTORE_TRANSFER_FAILED` is a new member at
`src/cratekit/modules/tools/backup.py:152`, and its comment says why it is its
own member rather than reusing one of the three refusals above it: "every one of
those is decided BEFORE anything is attempted and this one is the attempt
failing: the remote was reachable enough to plan against and then was not". The
slug is registered at `src/cratekit/core/cause.py:1237` as
`ExitCode.PRECONDITION`, so an unreachable remote is not classified as a defect
in this program.

**Raising rather than reporting a partial run is a deliberate difference from
the sibling, and it is worth stating rather than copying.** `run_backup` records
per portion outcomes because a backup that copied three of four portions has
still improved the world. A restore that copied some of a database and its
companions has produced a set that matches nothing, and there is no shape of
"partly restored" a caller can do anything with.

**The strict zip is load bearing.** Both branches build their results by
walking `plan.commands` exactly once, so a length mismatch is a driver defect
rather than a short list to tolerate, and tolerating it would skip the tail
unread. The same `strict=True` appears again at the call site,
`src/cratekit/session/restore_cli.py:569`.

**Then check whether your own new code compounded it.** The verb built its
report from the PLAN's command labels rather than from what ran, and the
comment above that line said so out loud. So the reporting path lied
independently of the checking path, and fixing only one of the two would have
left a green looking failure. Two paths, two fixes, in one round.

**Then ask what else has this shape, which is METHOD's implied fifth pattern at
`docs/METHOD.md:171`, "a fix round fixes the instance it was handed and
reproduces the class one file over".** Here the class reproduced ONE BRANCH
OVER, in the `dry_run` arm of the same function, which returned its results
unread exactly as the real arm did. That one falsified `run_restore`'s own
docstring, which argues a rehearsal is worth running because "a rehearsal that
passes is then evidence the real run will reach its work". A person rehearses
precisely to find out whether the remote is reachable, so a failing preview
that reads as a passing one makes the docstring's third reason false.

## Why This Matters

WHAT THE SILENCE COST, MEASURED RATHER THAN ARGUED. The review drove it through
the real dispatcher, the real argument parser, the real two act gate flow, and a
real `subprocess.run` against a real executable on disk. The only substitution
was the external program, supplied through `CRATEKIT_BIN_RCLONE`, the shipped
per binary override `core.binaries.find` reads before PATH. The stand in answers
`lsf` with one snapshot name and exits 1 on `copy`, which is what rclone does
when the remote is unreachable, the token has expired, or the path is not there.

The numbers, from `docs/history/u27-restore-review.md:60` onward:

    exit 0, outcome "ok"
    data.totals  {"transfers": 2, "steps": 0, "dry_run": false}
    data.items   two rows, each {"half": "off-machine", "transfer": "restore-database"}
    rclone argv  lsf remote:database-snapshots/ --dirs-only
                 copy remote:database-snapshots/<stamp>/db/master.db <lib>/db/
                 copy remote:database-snapshots/<stamp>/db/master.db-wal <lib>/db/
    live master.db-wal   DELETED
    live master.db       UNCHANGED

Read that against the ordering the module is built around. The sidecars are
cleared BEFORE the first command, on purpose, and `run_restore`'s docstring says
why it is one function rather than two the caller sequences: "a caller that
copied first and cleared afterwards would have already handed SQLite a database
and a log that disagree". A stale write ahead log replayed onto a replaced
database corrupts it in a way that opens without complaint. The clearing is
correct. What was missing is the reading that decides whether the copy which
justifies the clearing actually happened.

The write ahead log holds transactions committed since the last checkpoint. By
construction those are in no capture, because a capture is taken at a
checkpoint. So the file the tool deleted is the only copy of the most recent
work in the library, and the one report a person acts on said the library had
been restored at the moment it had silently lost that work. Two of METHOD's four
named user facing costs at once, data lost and a clean report over state the
tool could not read.

WHY THE SUITE COULD NOT SEE IT, AND THIS IS THE PART THAT GENERALISES. There
were six drives of `run_restore` on `main` before this unit, at
`tests/modules/test_tools.py:1652`, `:1682` and `:1771`,
`tests/test_restore.py:1210`, and `tests/test_write_session.py:1051` and
`:1588`. Every one of the six passes a runner returning `returncode=0`. The
review states it flatly: "No test anywhere returns a nonzero `CommandResult` to
`run_restore`."

The sharpest detail is that the apparatus for failing existed and was pointed
somewhere else. `Recorder` at `tests/modules/test_tools.py:129` takes a
`fail_labels` set and returns 1 for any command whose label is in it:

```python
    def __call__(self, command):
        self.commands.append(command)
        rc = 1 if command.label in self.fail_labels else 0
```

`fail_labels` is PASSED BY EXACTLY TWO TESTS at `6c4f12d`, at `:1340` and
`:1352`, and BOTH are drives of `run_backup`. (A grep for the name returns five
lines, the other three being its parameter, its assignment and its read inside
`Recorder` itself.) The person who wrote the failure
runner was testing the function that reads return codes, because that is the
function whose behaviour on failure there was something to assert. The one that
ignored them offered nothing to assert, so nothing was asserted, and the green
suite recorded that as coverage.

That is the mechanism behind the rule. A test suite is shaped by what its author
had a reason to check, and the reason usually comes from a caller. No caller, no
reason, no test, and a green suite that proves the happy path and nothing else.
Coverage does not catch it either: every line of `run_restore` RAN in those six
tests. What did not exist was a line that would have failed if the return code
were ignored, which is the distinction `scripts/mutate.py:22` already states,
that "coverage measures which lines RAN and a mutation table measures which
lines MATTER".

WHY OWNERSHIP IS THE RIGHT FRAMING RATHER THAN A COURTESY. The merge bar at
`docs/METHOD.md:15` is three conditions, and condition 3 was added on 2026-08-10
after a verifier returned BLOCKING on a document it had hand mutated. It exists
to stop findings over inputs nothing produces. Applied here it cuts the other
way and cuts hard. Before `e2dd532`, a finding against `run_restore` would have
been a RESIDUAL, correctly, because no producer could be driven. After
`e2dd532`, the producer is a shipped verb a person types, so the same defect in
the same unchanged lines clears all three conditions. The unit that supplies the
producer is the unit that owes the fix, and `ebdfa05`'s own message says so in
one sentence: "run_restore had no caller in src on main. This unit is what put
it in front of a person, which is why the finding is this unit's rather than the
backup module's."

The alternative framing, that the defect predates the branch and belongs to
whoever wrote it, is the one that lets it ship. Nobody is going back to U35.
THE REPOSITORY ALREADY RAN THIS CONDITION IN THE OTHER DIRECTION, which is why
the framing needed writing down (session history). Reachability had been used
several times to CLOSE findings rather than open them: `AgingPolicyInvalid` was
ruled unreachable from the CLI because `config.validate` enforces the same
invariants at load time, an unreachable fallback branch in a doctor check was
filed as a residual rather than a blocker, and an untestable branch in
`adopt.apply` was deleted outright rather than filed. Every one of those is the
condition saying "not reachable, so not blocking". This is the first time it
said "reachable now, because of you".

AND THE SAME VERB HAD ALREADY BEEN CLEARED OF A DIFFERENT DEFECT, CORRECTLY
(session history). One session earlier, and one merge earlier for the sweep
itself though two for the module it followed, the work that landed
`cratekit.adopt.apply_cli` swept four verbs for the queued job payload defect and
checked `restore.run` against the registry rather than believing a subagent's
claim about it. The verdict was that `restore.run` sets neither `long_running`
nor an `argv_builder`, so it never queues and is not an instance. That verdict
was right, and it is still right at `363823d`. The verb was then landed carrying
a different dormant defect, in the function it had just been wired to call.
Clearing a verb of one shape says nothing about what it inherits from its
callee, and the sweep that clears it is not the sweep that would have caught
this.

## When to Apply

- **You are about to call an internal function that `src` does not already
  call.** Run the grep. Two hits, a `def` and an `__all__` entry, means you are
  the first caller and its failure paths are now yours to drive.
- **The function you are calling returns a value your code does not read.** A
  return type of `tuple[CommandResult, ...]` that nobody inspects is the same
  defect wearing a type annotation. Read it, or say in a comment why the value
  is safe to drop.
- **The function has a sibling in the same module doing a similar job.** Diff
  their error handling before assuming they agree. `run_backup` and
  `run_restore` sit in one file, share one `Runner` type and one `CommandResult`
  dataclass, and disagreed about whether a nonzero exit is worth noticing.
- **The function is destructive before it is productive.** `run_restore` deletes
  live files before it copies replacements. Any function ordered that way turns
  an unchecked failure into data loss rather than into a no op, so the reading is
  not optional the way it might be for a function that only adds.
- **Your new code builds a report, a summary, or a count from a PLAN rather than
  from a RESULT.** That is the reporting half of this defect and it fails
  independently. Zip the plan against the results strictly and derive the report
  from the pairs.
- **You just fixed one instance.** Sweep for the shape before you close the
  round. The `dry_run` branch here was found by asking what else had it, not by
  anybody reporting it, and it was three lines away from the line already being
  edited.
- **A docstring in the function you are fixing makes a claim about what a
  passing run proves.** Check the claim against the fix. `run_restore`'s third
  argument for gating its rehearsal was false for as long as the rehearsal could
  report a failure as a pass.
- **You are deciding whether a finding holds a merge or goes in
  `docs/residual-findings.md`.** Ask when the input became reachable, not when
  the line was written. A defect whose reachability your branch created is
  BLOCKING on your branch.

## Examples

THE BEFORE, at `git show ebdfa05^1:src/cratekit/modules/tools/backup.py`. The
whole body of `run_restore`, under a docstring thirty three lines long that
argues carefully for the ordering and never mentions the return codes:

```python
    with _restore_gates(cfg, gates):
        if dry_run:
            return tuple(
                runner(Command(label=c.label, argv=dry_run_argv(c))) for c in plan.commands
            )
        plan.database_target.parent.mkdir(parents=True, exist_ok=True)
        for stale in plan.clears:
            stale.unlink(missing_ok=True)
        return tuple(runner(command) for command in plan.commands)
```

Every command runs, every result is collected, no result is looked at, and both
branches have the defect.

THE SIBLING, unchanged by any of this, at
`src/cratekit/modules/tools/backup.py:686`:

```python
            result = runner(command)
            results.append(result)
            if result.returncode != 0:
                failed = result
                break
```

Same module, same runner protocol, same result type. Three lines that the other
function did not have.

THE FIRST CALLER, at commit `e2dd532`, in
`src/cratekit/session/restore_cli.py:520`, with the comment that argued for the
second half of the defect:

```python
            # THE PLAN'S COMMANDS RATHER THAN THE RUNNER'S RESULTS. A dry run
            # neutralizes every transfer, so the results describe a rehearsal
            # either way; what a person needs reported is which transfers this
            # restore was made of, and ``dry_run`` on the report already says
            # whether they happened.
            transferred = tuple(command.label for command in pulled.commands)
```

The reasoning is coherent and it is about the wrong risk. It treats the
rehearsal case as the thing that could make the results misleading, and never
reaches the case where the results are the only evidence the transfers happened
at all.

THE AFTER, both halves. `src/cratekit/modules/tools/backup.py:1022` and `:1032`
now route both branches through one reading:

```python
            return _ran(
                tuple(
                    runner(Command(label=c.label, argv=dry_run_argv(c)))
                    for c in plan.commands
                ),
                plan,
            )
        plan.database_target.parent.mkdir(parents=True, exist_ok=True)
        for stale in plan.clears:
            stale.unlink(missing_ok=True)
        return _ran(tuple(runner(command) for command in plan.commands), plan)
```

and `src/cratekit/session/restore_cli.py:567` derives the report from the pairs:

```python
            transferred = tuple(
                command.label
                for command, _result in zip(pulled.commands, ran, strict=True)
            )
```

THE REFUSAL A PERSON NOW GETS, at `src/cratekit/modules/tools/backup.py:1069`,
written so that what it promises about the world is true of the world:

```python
                f"the transfer {command.label!r} exited {result.returncode} and the "
                f"restore did not complete. The live companion files beside "
                f"{plan.database_target.name} were cleared before it began and have "
                f"not been put back, so run the restore again once the remote is "
                f"reachable rather than opening the library first.",
```

The sidecars are not put back, and the message says so rather than pretending
otherwise, because clearing them first is the safety property the ordering
exists for and a silent repair is not something this module can make.

THE GUARDS, and the second one is the one that would not have existed without
the sweep. `tests/test_restore_cli.py:932` drives the real condition, a runner
that answers the listing and fails the copy, and asserts the state the refusal
leaves behind rather than only the refusal:

```python
    def failing(command):
        if "lsf" in command.argv:
            return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z/\n")
        return backup.CommandResult(returncode=1, stdout="", stderr="connection refused")
```

```python
    assert cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert cause.code is not ExitCode.INTERNAL, (
        "an unreachable remote is not a defect in this program"
    )
```

```python
    assert not wal.exists()
    assert str(wal.name) in cause.message or "companion" in cause.message
```

`tests/test_restore_cli.py:987` holds the branch one over, and its last
assertion is the difference between the two paths stated as a property:

```python
    assert excinfo.value.cause.reason == str(backup.Refusal.RESTORE_TRANSFER_FAILED)
    assert wal.exists(), "a rehearsal cleared the live companion files"
```

`tests/test_restore_cli.py:1027` then drives the other direction, a transfer
that succeeds and is still reported, because a guard that fires on every run is
indistinguishable from a broken verb.

ONE CORRECTION TO THE IN TREE RECORD, since this corpus is where a later reader
will check. Both `ebdfa05`'s message and `_ran`'s docstring at
`src/cratekit/modules/tools/backup.py:1050` describe `run_backup` as being "one
file over". It is in the same file, `src/cratekit/modules/tools/backup.py`, at
`:635`, and `run_restore` is at `:974`. The distance is 339 lines inside one
module, which makes the point stronger rather than weaker: the checking path was
not in a neighbouring module somebody could reasonably not have read.

THE ROUND'S COST, for scale. The independent pass ran a 45 row mutation table
against a green baseline of 6183 collected, with the null control killing 0, and
produced 24 zero rows of which 21 were user facing. It returned two BLOCKING
findings. Both were driven again locally before being acted on, because
`docs/METHOD.md:166` names "a fix justified by a measurement taken on a fixture
rather than on the tree" as the most dangerous of the four patterns and a fix
justified by somebody else's confident number is that pattern. The battery after
the round was ruff clean, `scan_repo` clean, and 6199 passed with 1 skipped
against 6189 and 1 before it, rising to 6200 and 1 after the `dry_run` branch and
its guard landed in `9397453`.

## Related

- [An explicit gate makes a queued job undriveable without the run id](an-explicit-gate-makes-a-queued-job-undriveable-without-the-run-id.md).
  The sibling case, one merge earlier in the same unit. There a resume branch
  inside a landed verb was never driven, so a mutation zero on it indicted the
  branch rather than the line. Here a whole function had no caller in `src`,
  which is that condition taken to its limit. That document also examined
  `restore.run` and cleared it as NOT an instance of the gate defect, which was
  correct then and is still correct now, and this learning is why the same verb
  shipped a different one anyway.
- [A confirm gate does not accept review items](a-confirm-gate-does-not-accept-review-items.md).
  The other verb that told a person a destructive act had happened when it had
  not, with the fix deliberately placed at the opposite layer. There the engine
  was correct and the shell was the hole, so the document refuses to invent a
  second confirmation inside the engine. Here the shell was the symptom and the
  shared function was the hole, so the fix moved down rather than up. Two
  opposite altitudes, each argued from where the defect actually lives.
- [Merge falsifies a guard invariant and every remedy breaks something](merge-falsifies-a-guard-invariant-and-every-remedy-breaks-something.md).
  Where the merge bar's three conditions are worked in the corpus. It runs the
  reachability condition in the direction where a finding does NOT block, which
  is the direction this one turns around.
- [A cause read from a log is not a cause driven by reproducing it](a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it.md).
  The corpus entry for the discipline this round followed when the review came
  back BLOCKING: both findings were driven again locally before being acted on,
  because a fix justified by somebody else's confident number is METHOD's fourth
  pattern.
- `docs/history/u27-restore-review.md` holds the independent review in full, including
  the reproduction for this finding and the 45 row mutation table behind it.
  `docs/residual-findings.md` R-150 through R-157 are what this unit recorded
  rather than fixed, and they arrived in two batches rather than one: R-150 to
  R-152 were filed with the feature commit, before any review existed, and only
  R-153 to R-157 came out of the independent pass. The merge commit blurs the two
  and this line is the correction.
