---
title: "A queued verb with an explicit gate must freeze its run in the payload, or nothing can ever drive the job"
date: 2026-08-23
category: workflow-issues
module: src/cratekit/adopt/apply_cli.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - "A registry entry sets long_running=True and declares a GateSpec with explicit=True"
  - "An argv_builder is being written for a verb that queues a job behind a gate"
  - "A verb's queued payload is being decided and the run identifier is not in it"
  - "A conformance suite passes for a verb whose resume branch no test drives"
  - "A mutation row measures zero on a line inside a branch nothing enters"
symptoms:
  - "The queued job exits DECISION_REQUIRED on every resume and never advances"
  - "The queue holds a job that no command, and no driver, can move out of it"
  - "Every conformance property passes while the resume branch is never entered"
  - "A mutation row on the resume branch measures zero deaths across the full suite"
  - "The child spawned by the job driver asks for an approval that was already given"
related_components:
  - testing_framework
tags:
  - explicit-gate
  - job-resume
  - argv-builder
  - run-identity
  - conformance
  - mutation-testing
  - subprocess
---

# A queued verb with an explicit gate must freeze its run in the payload, or nothing can ever drive the job

## Context

U27 landed the adopt apply shell and merged to `main` as `347244a`. The fix
inside it is `60441e9`, and the defect it fixes is that `adopt apply` queued a
job that nothing in the product could ever advance. Not a job that failed. A job
that would sit in the queue for ever, refusing identically to every attempt to
drive it, on a verb whose eight conformance properties all passed.

THE ROW THAT FOUND IT WAS ASKING SOMETHING ELSE. `G5_resume_does_not_reconcile`
in `docs/mutation/u27-adopt-apply-author.toml:158` swaps `jobs.reconcile` for
`jobs.get` in the resume branch, and its description says what it believed it was
measuring: "Report the stored job without reconciling a claim a dead driver left
behind". The table records the result at
`docs/mutation/u27-adopt-apply-author.md:429`, "Collected: 6147 against a
baseline of 6147", kills 0, promoted, zero on the full suite. Two other rows in
the same batch measured zero as well, `S3_watched_root_is_narrower_than_the_library`
and `G3_gate_offers_no_digest`.

Investigating why G5 killed nothing produced an answer larger than the row.
Nothing drove the resume branch at all, from anywhere. So the question the row
asked, whether the resume reconciles or reads a stale row, was one no test was
positioned to answer, and neither was any other question about that branch. Then
the real `argv_for` output was taken and run through the real dispatcher, and the
branch turned out not to work at all.

This is a third reading of a zero, and the
[zero death row learning](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md)
names only two. That doc says a zero is either a genuine test gap or an inert
mutation, and gives the diagnostic for telling them apart: if you cannot state
what the two trees do differently, the row is inert. G5 passes that diagnostic.
The two trees genuinely differ, so the row is not inert, and it is a real test
gap. The third thing worth naming is what happens next. **The remedy for a
genuine gap is not always the guard the row's own description names.** Writing
the test G5 asks for, a resume that reconciles a dead driver's claim, would have
closed the row and left the verb undriveable, because the branch that test drives
was refusing before it ever reached the line under mutation. A zero row on an
undriven branch indicts the branch, not the line.

## Guidance

**A verb that declares `explicit=True` and queues a job must freeze
`ctx.run.run_id` in the payload and emit it on the resume argv.** Nothing else
satisfies the gate. There is no flag, no config key, no environment variable that
can stand in, by design: `src/cratekit/cli/gates.py:317` states there is
deliberately no fourth decision source, because "a blanket affirmative flag, a
config key, or an environment variable would each satisfy every gate at once,
which is what R34 forbids". The recorded decision lives on the run, so the run is
the only thing a resume can carry that answers the question.

Before, at `src/cratekit/adopt/apply_cli.py`, the builder returned the job and
nothing else:

```python
def adopt_apply_argv(job) -> list[str]:
    return ["adopt", "apply", "--job", job.job_id]
```

and the enqueue froze only the plan:

```python
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"tree": plan.tree, "digest": plan.digest()},
            cfg=cfg,
        )
```

After, `src/cratekit/adopt/apply_cli.py:281` reads the run off the payload and
puts it in front of the verb path, and `:353` freezes it at queue time:

```python
    run_id = (job.payload or {}).get("run_id")
    resume = ["--run", str(run_id)] if run_id else []
    return [*resume, "adopt", "apply", "--job", job.job_id]
```

```python
            payload={
                "tree": plan.tree,
                "digest": plan.digest(),
                # FROZEN SO THE APPROVAL SURVIVES THE RESPAWN. See
                # ``adopt_apply_argv``: the gate is explicit, so a resume on a
                # fresh run can never be answered and the job would be
                # undriveable.
                "run_id": ctx.run.run_id,
            },
```

**The flag goes before the verb path, not after it.** `--run` is a root parser
flag, for the reason `tests/test_cli_contract.py:1279` gives about decisions
generally, that they belong to the invocation rather than to the subcommand. The
shape is `[*resume, *entry.path, *the verb's own arguments]`, and it is the same
shape `_conformance_3` builds at `tests/test_cli_contract.py:1573`.

**A payload frozen by an older build has no run, and the builder must still
return a valid command line.** `(job.payload or {}).get("run_id")` returns
`None`, the resume list stays empty, and the argv is exactly what the old build
produced. That job resumes to the same refusal it was already in, which is
honest, rather than crashing the driver on a `KeyError` in a detached subprocess
whose only output is a log file.

**Freezing the run does not launder the approval, and that is worth checking
rather than assuming.** The run holds a decision only if `crate run decide`
recorded one against it with an actor, per `src/cratekit/cli/gates.py:381`. A run
carrying no recorded decision resumes to the same `DECISION_REQUIRED` a fresh run
would produce, because `Gates.require` reaches the same `chosen is None` branch at
`src/cratekit/cli/gates.py:359`. What the frozen run buys is continuity of an
answer that was given, not a way to skip giving it.

**Drive the builder's real output through the real dispatcher.** Asserting the
argv equals a list is a unit test of a list. The property that matters is that
the command line the driver spawns is one the verb will accept, and only running
it can say so. `tests/test_adopt_apply_cli.py:668` does exactly that: it calls
`cli_jobs.argv_for(job)` on the real job and drives the result.

## Why This Matters

THE JOB WAS BEING RE-INVOKED AS A SUBPROCESS, AND THE SUBPROCESS CARRIED NO
MEMORY. `src/cratekit/core/jobs.py:1318` builds the child command as
`[executable, "-m", "cratekit.cli", *argv]`, and `:1334` spawns it detached with
`start_new_session=True` and `stdin` on the null device. That is KTD26, and the
module docstring at `src/cratekit/core/jobs.py:16` gives the reason: an in
process handler would pull every feature module into the supervising process.
The consequence is that the child inherits none of the parent's DECISION state.
It does inherit the environment and the working directory, because `spawn` passes
`env=None` when the caller supplies none, but no run identifier and no gate
answer lives in either of those, by the design at
`src/cratekit/cli/gates.py:317` that refuses an environment variable as a
decision source at all. What the child does not get is the parent's run, the
parent's gate state, or a terminal it could ask a question on. For the purpose of
answering a gate, the argv and the frozen payload are the entire inheritance.

That argv comes from the verb itself. `src/cratekit/cli/jobs.py:220`,
`argv_for`, resolves the stored handler key against the registry, imports the
owning module only after the key is known to be real, and calls the entry's named
`argv_builder`:

```python
    module = importlib.import_module(entry.module)
    return list(getattr(module, entry.argv_builder)(job))
```

For `adopt.apply` that name is `"adopt_apply_argv"`
(`src/cratekit/cli/registry.py:1275`), on an entry that also declares
`long_running=True` (`:1276`), `destructive=True` (`:1280`), and a gate named
`adopt.apply.approve` with `explicit=True` (`:1289`).

Now the two halves meet. `src/cratekit/cli/__init__.py:266`, `_run_state_for`,
loads the named run when `args.run` is set and otherwise mints a new one at
`:283` with `gates.new_run(entry)`. A fresh run has no decisions. And
`src/cratekit/cli/gates.py:344` refuses on exactly that state:

```python
        if inline is not None and spec.explicit and recorded is None:
```

with the comment that follows it stating R34's whole content, that an explicit
gate "is answered by a deliberate, separate act that is recorded with its actor,
never inline in the same invocation that discovered the gate". Even with no
inline answer at all, `chosen` is `None` at `:359` and the same
`DecisionRequired` is raised. Either path exits `DECISION_REQUIRED`, which is 10
(`src/cratekit/core/exit_codes.py:71`).

So the loop, driven rather than argued. `job resume` calls
`jobs.spawn(store, job, argv_for(job))` at `src/cratekit/cli/jobs.py:282`. The
child gets `["adopt", "apply", "--job", job_id]`, mints a new run, meets the
explicit gate with nothing recorded, exits 10, and writes its refusal into a log
file nobody is watching. Resume again and the argv is byte for byte identical, so
the child does the same thing. There is no state anywhere that a second attempt
changes. The queue held a job that no command in the product could advance, and
the person who had already approved it had approved it on a run the child could
not name.

WHY THE SUITE COULD NOT SEE ANY OF THIS, AND THIS IS THE PART THAT GENERALISES.
`_conformance_3` at `tests/test_cli_contract.py:1544` is the strongest gate
assertion in the repository. It drives every landed gated verb, asserts the set
of gates reached equals the set declared minus the exempt ones, asserts an
inline answer to an explicit gate is refused a second time, asserts the refused
answer was not recorded anyway, then records the decision through
`run decide --actor a-person` and asserts the verb reaches OK. The parametrised test over it, at
`tests/test_cli_contract.py:1640`, carries a docstring explaining that an earlier
version asserted the opposite of R34 and made every explicitly gated verb
unlandable by construction. It is a test that has already been wrong once and
been rewritten with the lesson in it.

It still could not see this defect, and the reason is one line of arithmetic. Its
argv is built from `_sample_arguments(entry)`
(`tests/test_cli_contract.py:1276`), whose mapping holds `"adopt.apply": []` at
`:1355`, and the string `--job` does not appear anywhere in
`tests/test_cli_contract.py`. (That helper's own docstring says it returns
positional arguments, and two of its entries carry flags, `review.resolve` at
`:1309` and `rebuild` at `:1372`. The overclaim does not affect this verb, whose
sample is empty either way.) The
conformance drive therefore always takes the enqueue branch of `apply_adoption`
(`src/cratekit/adopt/apply_cli.py:312`) and never the `if ctx.args.job` branch
above it. Eight properties passed on a verb whose queued work was undriveable,
because all eight were measured in the mode where a job does not exist yet.

**A contract test that drives a verb in one mode cannot see a defect in another
mode, and its passing says nothing about the mode it did not enter.** This verb
has two: queue, and resume. Conformance drives queue. Every other test in
`tests/test_adopt_apply_cli.py` called the engine functions directly, so it drove
neither the dispatcher nor the argv. The resume mode had a full brief, a
registered builder, and a `--job` flag with a help string
(`src/cratekit/adopt/apply_cli.py:241`), and no execution path anywhere in 6147
collected tests.

That is also the exact reason the mutation table's zero was informative and its
description was not. A mutation on a line inside an unentered branch is
guaranteed to measure zero regardless of what the mutation says, so the zero is a
signal about reachability rather than about the guard. The
[zero row learning](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md)
already says the table cannot distinguish a gap from an inert row. What this adds
is that when the row is a real gap, the branch it sits in is worth reading before
the line it mutates, because a branch nothing enters produces zeros for every row
in it and each row will describe a different, plausible, wrong reason.

## When to Apply

- **A registry entry sets `long_running=True` and any of its gates sets
  `explicit=True`.** Check the payload for the run and the argv builder for
  `--run`. `adopt.apply` is the first landed instance of this combination.
- **`export.playlist` HAS THIS DEFECT ON `main` TODAY, and it is live rather
  than latent.** Driven 2026-08-23 on a disposable library: answer the gate
  through `crate run decide`, drive again under `--run`, and the verb queues a
  job (`src/cratekit/export/cli.py:85`). `export_argv` at `:55` then returns
  `["export", "playlist", playlist, "--job", job_id]` with no run, so the child
  exits 10 on `export.playlist.confirm` and exits 10 again on every respawn. The
  cost is a person's confirmed export sitting in the queue for ever. The producer
  is the verb itself and it was driven, so this meets all three conditions of the
  merge bar in `docs/METHOD.md` rather than being argued from the source.
- **`delete.review` carries the same argv shape and is LATENT, not live.** Its
  gate is explicit and `delete_argv` at `src/cratekit/deletion/cli.py:120`
  returns `["delete", "review"]` with neither a run nor a job, but the handler
  never calls `jobs.enqueue`, so no job under that handler key is ever created
  and nothing can reach the defect today. Its docstring is the part that is wrong
  now: it says "the run id and the recorded gate travel on the invocation", and
  the list it returns carries neither. The day anything enqueues that verb, the
  exposure becomes live.
- **`restore.run` is NOT an instance, and the reason is worth stating because it
  looks like one.** It declares `restore.run.confirm` with `explicit=True` and it
  is destructive, so it shares the gate half. It sets neither `long_running` nor
  an `argv_builder`, so it never queues a job and there is no child to inherit a
  missing run. Checked rather than assumed: an earlier draft of this document
  named it as the next instance on the strength of the explicit gate alone. The
  combination is what bites, not either half of it.
- **`sync.favorites` IS THE SECOND LIVE INSTANCE, and it is the one worth
  studying, because it looks fixed.** `sync_favorites_argv`
  (`src/cratekit/favorites/cli.py:60`) does freeze a run in the payload and does
  emit it, and it is still broken, because the flag it emits is `--run-id` and
  not `--run`. Those are two different concepts that a reader's eye merges.
  `--run` is the root parser's gate run. `--run-id` is a subcommand argument
  declared at `:51` with `dest="run_id"`, holding the INTAKE run shared with the
  other sources in a sync, and `_run_state_for` reads `args.run` and never
  `args.run_id`. So the child restores no gate state, mints a fresh run, and
  exits 10. Driven 2026-08-23: the resume argv is
  `["sync", "favorites", "--job", job_id, "--run-id", run_id]` and it refuses on
  `sync.favorites.confirm` under a run identifier different from the approved one.
- **The rule, stated so it can be checked mechanically, AND THE WAY THE FIRST
  VERSION OF IT WAS WRONG.** A verb is exposed when `long_running`, an
  `argv_builder`, and a non exempt `explicit` gate are all present and the
  builder does not emit the root `--run` flag. On 2026-08-23 that predicate
  returns `export.playlist` and `sync.favorites` live, `delete.review` exposed
  but unreachable, and `adopt.apply` alone clean. The three verbs whose only
  explicit gate is `write.cloudsync.unreadable` are correctly excluded, because
  that gate is the sole member of `UNREACHABLE_GATES`
  (`tests/test_cli_contract.py:1501`).

  The first version of this predicate tested `"--run" in source`, and it reported
  `sync.favorites` CLEAN, because `--run-id` contains `--run` as a substring. A
  document asserting a verb is safe on the strength of a substring match is worse
  than one that says nothing, and this document said exactly that until an
  independent check drove the verb. Match the flag as a whole token, and confirm
  an exposure by driving the resume rather than by reading the builder.
- **Any new `argv_builder` is being written.** Ask what the child inherits. The
  answer is the argv and the frozen payload, and nothing else. Anything the
  parent process resolved that the gate or the handler will need again belongs in
  one of those two places.
- **A mutation row measures zero on a line inside a conditional branch.** Before
  writing the test the row's description asks for, confirm something drives the
  branch at all. If nothing does, the row's description is a hypothesis about a
  line that was never reached, and the finding is the branch.
- **A conformance or contract suite is being cited as coverage for a verb.** Name
  the modes the verb has and check which ones the suite's argv actually
  constructs. A verb with a resume flag, a dry run flag, or a second phase has
  more than one, and the suite usually drives one.

## Both live instances were fixed the same day

The two verbs this document found are no longer broken, and the measurements
above are kept as they were taken rather than rewritten, because the point of
this entry is how the defect hid rather than which commit closed it.

`export.playlist` and `sync.favorites` now freeze the gate run under one shared
key, `cratekit.core.jobs.GATE_RUN_KEY`, and emit it as the root `--run` flag
ahead of the verb path. The key is deliberately not `run_id`: `sync.favorites`
already froze a `run_id` holding the INTAKE run, and two concepts under one name
is what made its builder read as correct. `adopt.apply` moved onto the same key.
`delete.review` reads it too, so the latent case is disarmed rather than left
armed, though the mismatch between its registry entry and its shell is recorded
separately as R-149.

**Update, U60, 2026-09-10.** The latent case is gone rather than disarmed.
`delete.review` stopped declaring `long_running` and its `argv_builder`, and
`delete_argv` was deleted, because the verb never queued: the person who confirms
a deletion watches it happen. A registry entry can claim the queueing contract
over a shell that does its work inline, and every guard derived from that claim
then trusts it, so `tests/test_cli_contract.py` now parses each long-running
verb's module for an `enqueue` call.

THE GUARD IS DERIVED FROM THE REGISTRY, in
`tests/test_queued_resume_contract.py`. It walks every landed entry that is
`long_running`, names an `argv_builder`, and declares a non exempt `explicit`
gate, and holds each one to emitting `--run` carrying the frozen run. A test
naming today's four would pass for ever while the fifth verb shipped broken,
which is the same shape as a guard that forbids an implementation rather than a
feature. It also matches `--run` as a WHOLE TOKEN in the returned list rather
than as a substring of the builder's source, which is the specific mistake that
declared `sync.favorites` clean in the first place.

Two of its assertions are worth reading before adding a verb. One drives the real
`argv_for` output through the real dispatcher, because asserting the argv equals
a list is a unit test of a list. The other hands the builder a payload with no
gate run, standing in for a job frozen by an older build, and requires a valid
command line rather than a crash inside a detached subprocess whose only output
is a log file nobody is watching.

## Examples

The measured before and after, driven on 2026-08-23.

Before the fix, taking the real `argv_for` output and running it through the real
dispatcher. Approve the gate through R34's two acts, queue the job, then resume
it the way the driver would:

```python
    _code, refused = _drive(["adopt", "apply"])
    run_id = refused["run_id"]
    _drive(["run", "decide", run_id, "adopt.apply.approve", "approve", "--actor", "a-person"])
    approved, envelope = _drive(["--run", run_id, "adopt", "apply"])
    assert approved == int(ExitCode.OK), envelope

    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
    argv = cli_jobs.argv_for(job)
```

On the old tree `argv` is `["adopt", "apply", "--job", job_id]`, driving it
returns 10, and it returns 10 every subsequent time, because the argv does not
change and neither does anything the argv touches. The guard that now holds it is
`tests/test_adopt_apply_cli.py:668`, and its failure message is the finding in
one sentence:

```python
    code, resumed = _drive(argv)
    assert code == int(ExitCode.OK), (
        f"the resume the driver spawns refuses: {resumed.get('cause')}. A job "
        f"whose own resume cannot answer its gate is a job nothing can advance"
    )
    assert resumed["data"]["job_id"] == job.job_id
    assert len(_queued(installed)) == 1, "the resume queued a second record"
```

The last line is the other half of the contract, and it is why the argv names the
job rather than restating the request. A resume that dropped `--job` would exit
OK by queueing a second record for one piece of work, which is what
`V1_resume_forgets_the_job` mutates for
(`docs/mutation/u27-adopt-apply-author.toml:167`) and what it killed on.

Both payload shapes are held directly at `tests/test_adopt_apply_cli.py:452`,
including the older build's:

```python
    assert apply_cli.adopt_apply_argv(_Job()) == [
        "--run", "run-3", "adopt", "apply", "--job", "job-7",
    ]
    assert apply_cli.adopt_apply_argv(_Older()) == ["adopt", "apply", "--job", "job-7"]
```

The G5 question, the one the mutation row was actually asking, is now driven for
the first time at `tests/test_adopt_apply_cli.py:704`. It puts the job into
`RUNNING` with no driver lock held, which is the state a killed driver leaves
behind, then resumes and asserts the reported state is `QUEUED` rather than the
stale row. That test could not have been written before the fix, because the
resume it drives never returned OK.

The third zero in the same batch, `G3_gate_offers_no_digest`, resolved the same
way and is worth naming because it is the same shape one level down. Dropping
`digest=plan.digest()` from the `require` call killed nothing, since the queued
payload computes its digest straight from the plan and matches either way. The
guard now at `tests/test_adopt_apply_cli.py:620` moves the plan between the
recorded approval and the resume by giving the census a row, and the run refuses
with `decision-stale`. Three user facing zeros, three tests, none of them inert,
and one of the three was a defect in the verb rather than a gap in its suite.

## Related

- `docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`,
  the neighbouring learning and the one this extends. It gives the two readings
  of a zero and the diagnostic for choosing between them. G5 is a genuine gap by
  that diagnostic, and the addition here is that a genuine gap's remedy is not
  always the guard the row's own description names: an unentered branch produces
  a zero for every row inside it, each with a different plausible explanation.
- `src/cratekit/cli/gates.py:335` for `Gates.require`, `:344` for the explicit
  refusal branch, `:359` for the same refusal with no answer at all, and `:317`
  for why there is no fourth decision source.
- `src/cratekit/cli/jobs.py:220`, `argv_for`, the one place a handler key becomes
  a command line, and `:282` where a resume spawns a child with its output.
- `src/cratekit/core/jobs.py:1318` and `:1334`, `child_command` and `spawn`, for
  what the child does and does not inherit, and `:16` for KTD26, the reason it is
  a subprocess at all.
- `src/cratekit/cli/__init__.py:266`, `_run_state_for`, the line that mints a new
  run whenever `--run` is absent.
- `tests/test_cli_contract.py:1544` for `_conformance_3` and `:1640` for the
  parametrised test over every landed entry, both of which pass without ever
  constructing a `--job` argument.
- `src/cratekit/export/cli.py:55` for `export_argv` and `:85` for the enqueue,
  the live instance of this defect still on `main`, and
  `src/cratekit/deletion/cli.py:120` for `delete_argv`, the latent one whose
  docstring already describes the fix it does not implement.
- `docs/mutation/u27-adopt-apply-author.toml:158` for the G5 row and
  `docs/mutation/u27-adopt-apply-author.md:421` for its measured zero against a
  6147 baseline.
- Fix commit `60441e9`, "fix(adopt): the queued apply could never be resumed, and
  the table's zeros found it", and merge `347244a`, "merge: the adopt apply shell
  and the one session its engine declined to open".
