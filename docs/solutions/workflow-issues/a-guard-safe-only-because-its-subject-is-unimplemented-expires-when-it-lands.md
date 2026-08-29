---
title: A guard that is safe only because its subject is unimplemented expires the day somebody implements it, and the obvious restatement measures nothing
date: 2026-08-28
category: workflow-issues
module: tests/test_cli_contract.py, tests/test_jobs.py, src/cratekit/cli/registry.py, src/cratekit/acquire/cli.py
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test asserts that a lookup, a build, or a dispatch did NOT import, load, or construct something"
  - "A guard's subject is a module, a verb, or a path that the repository has not landed yet, so the assertion has never had a chance to be false"
  - "A unit is about to land the very module some existing test names in a not-in assertion"
  - "A guard is being restated as a difference, a delta, or a before and after comparison over shared process state such as sys.modules"
  - "A restated guard goes green on the first run and no mutation row has been taken against the line it claims to protect"
symptoms:
  - "A test that passed for eleven units fails on the merge that lands the module it names, on a lookup that imported nothing"
  - "The failing assertion is `registry.entry(\"acquire.download\").module not in sys.modules`, and the module is in sys.modules because the test session already imported it"
  - "The restated difference guard is green across fifty nine parametrised cases and a real importlib.import_module inserted into by_handler_key kills zero of them"
  - "The zero holds on the promoted full suite as well as the subset, so the table rather than the battery is the only thing that can see it"
  - "The same hand picked guard exists a second time one test file over, and the full battery rather than a search is what surfaced it"
related_components:
  - "development_workflow"
  - "tooling"
tags:
  - "mutation-testing"
  - "zero-row"
  - "test-fidelity"
  - "guard"
  - "silent-failure"
  - "observation-window"
  - "unlanded-subject"
  - "lazy-import"
---

# A guard that is safe only because its subject is unimplemented expires the day somebody implements it, and the obvious restatement measures nothing

## Context

`registry.by_handler_key` is a plain dictionary lookup, and it is a dictionary
lookup on purpose. `_BY_HANDLER` is built once at import time as a mapping proxy
over every declared entry (`src/cratekit/cli/registry.py:1610`), and the function
does nothing but index it and re-raise a `KeyError` with a better message
(`src/cratekit/cli/registry.py:1640` through `:1650`). Its docstring states the
property it is written to hold, quoted exactly from
`src/cratekit/cli/registry.py:1643`:

> Resolving a handler must not import anything (KTD26): the engine validates a
> queued job's handler before spawning, and validating by import would defeat
> the lazy-import stubs the whole scheme rests on.

The caller is `src/cratekit/cli/jobs.py:220`, `argv_for`, and it is where the
property earns its keep. The lookup happens at `:230`, inside a `try` that turns a
missing key into an `internal-error` cause. The landed check happens at `:244`.
Only then, at `src/cratekit/cli/jobs.py:257`, does
`importlib.import_module(entry.module)` run, and only for the one module that owns
the key. The function's own docstring says why the order is the point
(`src/cratekit/cli/jobs.py:223`), that the import "happens only after the key is
known to be real, and only for the one module that owns it, which is what keeps a
queued analysis job from pulling the analysis dependencies into a process that is
merely listing jobs".

So the property is about a PROCESS, not about a function's return value. The
supervisor is a process holding the registry and nothing else, and the claim is
that walking a handler key through it leaves it still holding nothing else. Every
mistake below is a mistake about where that process state was measured.

**This repository forbids pull requests by contract, so commits are the
citation and there is no PR number to give.** `a1b4b45` landed U42 and the second
shape of the guard. `bf2b8a9` is the fix for both of the table's zero rows and
carries the reasoning in its body. `3632094` is the merge onto `main`. Each was
checked with `git merge-base --is-ancestor <sha> HEAD`, and all three returned
exit 0 against `HEAD`, which is `3632094` on `main`.

### The first shape, and why it held for eleven units

`tests/test_cli_contract.py` carried
`test_a_handler_key_resolves_without_importing_the_module` with
`acquire.download` as its single hand picked subject, asserting
`registry.entry("acquire.download").module not in sys.modules`. That assertion had
been green since U31, and it was green for a reason that had nothing to do with
`by_handler_key`. `src/cratekit/acquire/cli.py` did not exist. A module that is
not implemented is never in `sys.modules`, whatever any lookup does, so the test
was measuring the absence of a file and reporting it as a property of a function.

U42 landed that module. An earlier drive in the same session imported it, and the
assertion failed on a lookup that had imported nothing. The commit body of
`a1b4b45` records it in those words: "asserted that acquire.download's module was
not in sys.modules, which held because the module was unimplemented rather than
because the lookup imports nothing".

### The second shape, and the row that proved it empty

The obvious repair was to stop naming a subject and start measuring a difference.
Snapshot `sys.modules` before the lookup, snapshot after, assert the set
difference is empty, and walk it over every landed verb with
`@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)`. That is what
`a1b4b45` shipped. The battery went green at 6473 collected, recorded in that
commit's own body as "6472 passed and 1 skipped".

Then the mutation table measured it. `docs/mutation/u42-author.md` is a light pass
of 14 measured rows against `a1b4b45`, with its null control at 0 kills over 6473
collected, which is what makes the rest of the table believable. Row
`R2_handler_lookup_imports` inserted a real import into the body of
`by_handler_key`:

```
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

Its result, quoted from the row definition in `docs/mutation/u42-author.md`:
"Collected: 6473 against a baseline of 6473. Kills: 0 (zero). Promoted: subset
killed 0, full suite killed 0." The zero survived promotion to the whole suite.
The table's own "Zero rows and what they owe" section flags it as a "USER FACING
ZERO WITH NO COMPOSITE".

The reason is one sentence and it generalises past this repository. By the time
the conformance suite reaches `tests/test_cli_contract.py`, the feature modules
are already in `sys.modules`, imported by earlier tests in the same interpreter.
`importlib.import_module` on a cached module returns from the cache and adds no
new key. The difference had nothing to differ against. **A difference is only a
measurement where the thing could have differed.**

Note what the second shape did fix and what it did not. It removed a hand picked
subject that would expire again the next time a verb landed, and it broadened the
population from one verb to fifty nine. Both are real improvements. Neither
touches the reason the assertion cannot fail, so a rewrite that fixed the visible
complaint left the guard exactly as empty as it found it.

Round one's other outcomes are worth stating so the table is not read as one row.
Eleven of the fourteen killed. Two returned zero, `C2_unknown_defaults_lossless`
and the `R2` row above. The fourteenth, `R1_planned_marker_returns`, is logged as
a collect-error rather than a kill count, with the note that "a file that fails to
collect takes its tests with it and the run still looks green, so this is not a
zero". Two rows were considered and dropped under METHOD's 25 row cap for a light
pass, `C6_lossless_exts_membership` and `P3_queue_constant`, and both dropped rows
are logged with the reason, because a truncation nobody logged reads as coverage.

### The third shape, and where the property is actually claimed

`bf2b8a9` measures the property in the state the claim is about. A subprocess runs
a probe that imports `cratekit.cli.registry` and nothing else, walks every landed
entry, calls `by_handler_key`, and collects any module whose name starts with
`cratekit` that entered `sys.modules` across the call
(`tests/test_cli_contract.py:1256` through `:1320`). That fresh interpreter is
what the supervisor genuinely is when it validates a queued job's handler before
spawning. One subprocess covers every landed verb, so no hand picked subject
remains to expire, and the population is derived rather than named, so the next
verb to land is covered without this file being edited.

Round two, `docs/mutation/u42-author-round-2.md`, re-ran the same mutation against
`bf2b8a9` with a baseline of 6414 collected and a null control of 0. Row
`R2_handler_lookup_imports` now reads "Collected: 540 against a baseline of 540.
Kills: 1 (killed)", and the one killed identifier is
`tests/test_cli_contract.py::test_a_handler_key_resolves_without_importing_the_module`.
The second zero in that table, `C2_unknown_defaults_lossless`, was resolved in the
same commit for an unrelated fixture reason and also went from 0 to 1.

### The class reproduced one file over

`tests/test_jobs.py` held a second copy of the same guard,
`test_resolving_a_handler_key_imports_nothing`, with the same hand picked
`acquire.download` subject and the same failure on the same day. It was found by
the full battery rather than by looking, which is `docs/METHOD.md:171`, the
implied fifth defect pattern, "a fix round fixes the instance it was handed and
reproduces the class one file over".

It was found in round one and restated in round one, alongside its twin, into the
same in-process difference form. So the class reproduced, was noticed, and was
then fixed with the fix that did not work, in both files at once. Round two
removed it rather than restating it a second time, and put a comment block in its
place at `tests/test_jobs.py:686` through `:700` recording where the property
lives now and why this file does not hold a copy. The two tests immediately below
it are what that file genuinely owes, and they were already there:
`test_a_job_queued_for_a_handler_this_build_does_not_register_refuses`
(`tests/test_jobs.py:702`) and
`test_a_job_queued_for_a_verb_that_has_not_landed_refuses_rather_than_importing`
(`tests/test_jobs.py:712`). The second of those still asserts
`unlanded[0].module not in sys.modules` (`tests/test_jobs.py:726`), and that
assertion is sound where it stands, because an unlanded module genuinely cannot be
in `sys.modules` and the test is about the refusal reaching the caller, not about
the interpreter's state.

### The count, reconciled by identifier

6473 collected before, 6414 after, verified at `HEAD` with
`.venv/bin/python -m pytest --co`, which reports "6414 tests collected". The
delta is 59 and every identifier in it is accounted for. `registry.entries()`
returns 64 entries of which 59 are landed, checked directly against the tree, so
the parametrised guard contributed 59 collected cases and the subprocess form
contributes one. The duplicate in `tests/test_jobs.py` contributed one and is
gone. 6473 minus 59 minus 1 plus 1 is 6414, and nothing else moved.

## Guidance

**A difference is only a measurement where the thing could have differed.** Before
trusting an assertion of the form "before and after are the same", ask what state
the process is in when the before snapshot is taken, and whether the mutation you
are guarding against could still change anything from there. Caches make this
question urgent and invisible at once. `sys.modules` is a cache, an
`lru_cache`ed resolver is a cache, a session-scoped fixture that already opened
the connection is a cache. A mutation that populates a cache which is already
populated is a no-op with respect to every observation downstream of it, and the
test that watches the cache will pass for as long as anything earlier in the run
warmed it.

**The interpreter is a fixture, and it is the one nobody wrote.** `CONCEPTS.md`
already names the fourth cause of a zero row, a fixture that never puts the system
into the state where the mutated line could change anything, and this is that
cause with the process standing in for the fixture. The distinguishing question is
the same: read the fixture rather than the assertion. What is different here is
that the fixture is ambient. Nothing in the test file constructs it, no `conftest`
declares it, and it is assembled incrementally by every test that ran before this
one, in an order pytest is free to change. That makes it the hardest fixture to
notice and the easiest one to believe you controlled.

**Measure a property in the state it is claimed about, not in the state the suite
happens to be in.** The docstring said "the engine validates a queued job's
handler BEFORE spawning". A supervisor at that moment has imported the registry
and not the feature modules. A pytest process 1250 lines into a conformance file
has imported most of the product. Those are different worlds, and an assertion
evaluated in the second one is not evidence about the first. When the claimed
state cannot be reached in-process, reach it out of process. A subprocess running
a small probe with `capture_output=True` and a JSON line on stdout is cheap, is
deterministic, and is the only form of this test that can fail.

**A subject picked because it is unimplemented is a subject that expires the day
somebody implements it.** This is the general form of shape one and the corpus has
its sibling at `docs/solutions/workflow-issues/asserting-an-absence-pins-the-observation-and-not-the-mechanism.md`.
An assertion that something is absent is satisfied by every route to that absence,
and "the file was never written" is a route. Derive the population from the tree,
walk it, and the guard stops depending on a fact about what has not been built
yet.

**A rewrite is not a re-measurement.** The second shape was written by someone who
had just been shown exactly how the first shape was empty, and it was written
carefully, with a docstring explaining the failure it was fixing. It was still
empty, for a second reason the rewrite never considered, and nothing in the
battery could say so. The corpus already carries this at
`docs/solutions/workflow-issues/a-rewrite-is-not-a-re-measurement-of-the-claim-inside-it.md`
for prose claims. It holds for guards too, and it is worse for guards, because a
rewritten guard is green and a green guard is taken as answered. The only thing
that separated shape two from shape three was a mutation row.

**When the class reproduces one file over, ask what the second file owes rather
than copying the fix into it.** Round one did the copy, which is the natural move
and puts two identical guards in two files. Round two asked the different question
and found that `tests/test_jobs.py` never owed this property at all. What it owes
is the supervisor's refusal path, which two tests beside it already drive. A
second in-process copy of an empty measurement is not redundancy, it is two things
to keep in step that both hold nothing. Deleting it, with a comment saying where
the property went and why, leaves the repository smaller and more honest than
leaving it.

**Reconcile a moved test count by identifier, never by total.** 6473 to 6414 is a
delta of 59, and 59 is also the number of landed entries, which is exactly the
kind of coincidence that lets a silent loss hide inside a matching arithmetic.
`CONCEPTS.md`'s Pinned population entry states the rule for the general case, "a
re-pin names its members rather than matching a delta, because a member leaving
while another joins reads as no change". Here the members were named: 59
parametrised cases collapsed to one, one duplicate removed, one subprocess test
added. The corpus sibling is
`docs/solutions/workflow-issues/a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md`.

**Fifty nine empty assertions are worth less than one that kills, and say so in
the commit.** Removing tests looks like removing coverage and will be read that
way unless the trade is written down. Each of the 59 was provably vacuous, proved
by a promoted full suite mutation run rather than argued, and that proof is what
makes the removal a strengthening. The number to report is not the count, it is
the kill.

**The vacuity guard has to count the population it protects, not a neighbouring
one, and this document's own first draft got it wrong.** The probe guards against
walking nothing with `assert result["walked"] > 0`. It was written as
`result["checked"] > 0` where `checked` was `len(registry.entries())`, every
declared entry, while the loop it guards skips entries that are not landed. So the
guard counted 64 and the walk covered 59, and in a build where nothing had landed
the guard would have passed over a loop that did nothing. That state cannot occur
in this build, so it was never wrong in practice. It was the same species of
imprecision this whole document is about at a much smaller radius, a check
counting a different set than the one it certifies, and it was caught while
writing this doc rather than by the battery, which is itself the point. It now
counts from the loop.

## Why This Matters

**The suite was 6473 tests deep and could not see a real import inserted into a
hot seam.** That is the finding, and it is a finding about the suite rather than
about the product. `by_handler_key` on the tree is correct and always was. What
the mutation table established is that if it stopped being correct, in the most
direct way possible, by literally importing a feature module in its own body,
every one of 6473 tests would still have passed. The guard named for that exact
property, in the file whose whole job is conformance, was among the tests that
passed.

**Be precise about the cost, because the merge bar is precise.**
`docs/METHOD.md:15` requires a blocking finding to be driven end to end, to have a
named user facing cost, and to have a reachable input with a driven producer. This
is not that. Nothing in the product imports the feature modules from the lookup,
so there is no user facing cost to drive and nothing was lost. The cost is
conditional and it is about the future, that the seam protecting the supervisor's
process from the acquisition dependency stack was unguarded, and any later change
to `by_handler_key` would have landed on a green suite that could not contradict
it. `docs/METHOD.md:166` through `:167` names the shape to distrust, "a fix justified by a
measurement taken on a fixture rather than on the tree", and calls it the most
dangerous because it arrives with a confident number and a green suite. Shape two
had all three: a confident restatement, a passing run, and a docstring explaining
the failure it had just fixed.

**Nothing in the battery could have caught this and nothing was misconfigured.**
The battery is `ruff check src tests scripts`, `pytest`, and `scan_repo.py`, and
`CONCEPTS.md`'s Battery entry is exact about the limit, that it checks "code,
imports and repository structure". A test that passes is a test that passes.
Coverage would have been no help either, since the parametrised guard did execute
`by_handler_key` fifty nine times, and coverage measures which lines ran while a
mutation table measures which lines mattered. Only the mutation table asks the
question that separates the two, and only its promoted full suite run made the
zero trustworthy rather than an artifact of a narrow subset.

**The sequence is the lesson, not any one of its stages.** Shape one was a bad
test that failed loudly the day its premise expired, which is the good case. Shape
two was a careful, well reasoned, green repair that measured nothing. Shape three
is the one that kills, and it exists only because somebody ran a mutation row over
a guard that had just been fixed. The instinct after fixing a test is to move on,
because the complaint is answered and the suite is green. This is the case that
argues against that instinct: the second shape looked more rigorous than the
first, was written with full knowledge of the first's defect, and was equally
empty.

## When to Apply

- A test's central assertion is that a snapshot of ambient process state did not
  change across a call: `sys.modules`, an environment mapping, a registry of
  loaded plugins, a connection pool, a cache's key set.
- A guard is being repaired after it failed for a reason unrelated to the property
  it names, and the repair broadens the population without changing where the
  measurement is taken.
- A property is documented as holding in a specific process state, a supervisor
  before it spawns, a worker before it forks, a cold start, an import-time
  bootstrap, and it is being tested from the middle of a suite that has already
  imported the world.
- A mutation row measures zero over a whole promoted suite on a line whose
  behaviour genuinely differs between the two trees, and inertness has already
  been ruled out by reading the mutated site.
- The same guard exists in two test files, and one of the two is about to receive
  a copy of a fix.
- A collected test count moves and the delta happens to equal a population size
  the change also touched.

## Examples

**Shape two, the version that could not fail.** From
`tests/test_cli_contract.py` at `a1b4b45`:

```python
@pytest.mark.parametrize("entry", LANDED, ids=lambda e: e.name)
def test_a_handler_key_resolves_without_importing_the_module(entry):
    before = set(sys.modules)
    assert registry.by_handler_key(entry.handler_key) is entry
    assert set(sys.modules) - before == set(), (
        f"resolving the handler key {entry.handler_key!r} imported a module; the "
        f"job engine validates a handler before it spawns, so a lookup that "
        f"imports pulls the verb into the engine's own process"
    )
```

**The mutation it did not notice**, row `R2_handler_lookup_imports`, quoted from
`docs/mutation/u42-author.md`. Kills 0, promoted to the full suite, still 0:

```python
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

**Shape three, the version that kills it.** From
`tests/test_cli_contract.py:1282` onward, the probe body:

```python
    probe = textwrap.dedent(
        """
        import json, sys
        from cratekit.cli import registry

        leaked = {}
        for entry in registry.entries():
            if not entry.landed:
                continue
            before = set(sys.modules)
            assert registry.by_handler_key(entry.handler_key) is entry
            added = sorted(m for m in set(sys.modules) - before if m.startswith("cratekit"))
            if added:
                leaked[entry.handler_key] = added
        print(json.dumps({"leaked": leaked, "walked": walked}))
        """
    )
```

and its run and assertions at `tests/test_cli_contract.py:1301` through `:1320`:

```python
    finished = subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert finished.returncode == 0, finished.stderr
    result = json.loads(finished.stdout.strip().splitlines()[-1])
    assert result["walked"] > 0, (
        "the probe walked no entries, so it measured nothing. COUNTED FROM THE "
        "LOOP, not from len(registry.entries()) ..."
    )
    assert result["leaked"] == {}, (
        f"resolving a handler key imported a cratekit module: {result['leaked']}. "
        f"The supervisor validates a queued job's handler before it spawns, so a "
        f"lookup that imports pulls the feature module into its own process"
    )
```

The `before` snapshot is still a difference, and it is a real one here, because
the interpreter it runs in has imported `cratekit.cli.registry` and nothing else.
The same three lines are a measurement in one process and a formality in the
other, which is the whole point.

**The duplicate, removed rather than restated.** What now stands at
`tests/test_jobs.py:686`, in place of the second copy:

```python
# THE HANDLER-KEY IMPORT PROPERTY LIVES IN tests/test_cli_contract.py NOW, and a
# copy of it stood here until U42 removed this one. Both copies named
# ``acquire.download`` as their subject and asserted its module was not in
# ``sys.modules``, which held only because the module was unimplemented. When U42
# landed it, both failed on the same day on a lookup that had imported nothing,
# and the second copy was found by the full battery rather than by looking, which
# is METHOD's implied fifth pattern.
#
# Restating it here as well would have put a second weak measurement beside the
# real one: the property is about a CLEAN interpreter, which a test running late
# in this suite cannot be, and a mutation table proved the in-process form empty.
# What this file genuinely owes is the SUPERVISOR'S path, which the two tests
# below already drive: an unknown handler and a verb that has not landed both
# refuse before anything is imported.
```

**The seam the property protects**, so the reason the guard exists is readable
from one place. `src/cratekit/cli/jobs.py:229` through `:257`, abridged to the
ordering that matters:

```python
    try:
        entry = registry.by_handler_key(job.handler_key)
    except KeyError:
        raise CratekitError(...) from None
    if not entry.landed or not entry.argv_builder:
        raise CratekitError(...)
    module = importlib.import_module(entry.module)
```

Lookup, then two refusals, then exactly one import. Every line above the import is
a line the supervisor runs on a key it does not trust, and the guard's whole job
is to keep them import free.


## Related

**This is the position-to-fail branch, and the name is a correction of this
document's own first draft.**
`docs/solutions/workflow-issues/asserting-an-absence-pins-the-observation-and-not-the-mechanism.md`
states the family taxonomy at `:108` through `:110`, and closes it with "This doc
is the assertion branch".
`docs/solutions/workflow-issues/a-fixture-where-the-mutated-line-cannot-matter-fails-red-first.md`
answers with "This is the fixture branch". The third term used to read "the
observation window", and stage two is that: the assertion was correct and the
registry was the real one, and the interpreter had already imported everything the
difference was measuring before the assertion ran.

**Stage one is NOT a fourth collapser, and the first draft of this section said it
was.** That draft argued the SUBJECT collapses the two trees on its own because
the assertion was well formed, the fixture was the real registry, and the
observation window was irrelevant. It contradicted this document's own Guidance
two sections up, which says an absence assertion "is satisfied by every route to
that absence, and 'the file was never written' is a route". That is the assertion
branch, in this document's own words. Well formed and DISCRIMINATING are the two
different things the assertion branch exists to separate, and stage one's
assertion was the first without being the second.

What is genuinely shared between the two stages is narrower and better named: in
neither was the guard ever in a POSITION to fail. The taxonomy's third term was
renamed to that on 2026-08-29 rather than growing a fourth, which also makes it
agree with `CONCEPTS.md`'s Guard entry, whose sixth axis had arrived at the same
carve independently and separates the two on the remedy: restating a guard as a
difference repairs an unlanded subject and does nothing at all for warmed ambient
state. Recorded here rather than quietly corrected, because a document arguing
that a careful restatement can be as empty as the thing it replaced should show
its own.

- `docs/solutions/workflow-issues/asserting-an-absence-pins-the-observation-and-not-the-mechanism.md`
  is the nearest neighbour and the parent that named this territory in advance.
  **Do not re-derive the family from here.** Its trigger at `:318`, "a mutation
  table row measures zero on a guard that has a test named after it, read the
  test's assertion, not just its name", is what fired on stage two, and it is
  worth recording that the trigger fired correctly and was still not sufficient:
  the assertion read fine, and the thing that was wrong was the interpreter.
- `docs/solutions/workflow-issues/a-fixture-where-the-mutated-line-cannot-matter-fails-red-first.md`
  is the sibling branch, and `:136` carries the nearest existing rule to one that
  would have caught stage two in advance, that a test written to kill a zero row
  owes a mutation row breaking the test's premise and not only the code's. Here
  the detector was an ordinary re-run of the original row against the rewritten
  guard, which is the cheaper half of that rule and was enough.
- `docs/solutions/workflow-issues/a-rewrite-is-not-a-re-measurement-of-the-claim-inside-it.md`
  is the same shape for prose. It is worse for a guard, because a rewritten guard
  is green and a green guard reads as answered.
- `docs/solutions/workflow-issues/a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md`
  is why 6473 to 6414 was reconciled by naming its 59 members rather than by
  noticing that the delta matched a population size the same change touched.
- `docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`
  and
  `docs/solutions/workflow-issues/dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md`
  are the two entries on reading a zero. Both apply, and the mutated site here was
  read before the zero was accepted: a real `importlib.import_module` in the body
  of the function under test is not an inert mutation.
- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`
  is the same structure in production code rather than in a test. There a suite
  was green because every drive handed the function a runner returning zero, not
  because it read return codes. Its sentence "an old function with a green suite
  is not a reviewed function" is one substitution away from this document's
  thesis, and in both cases a LANDING EVENT, becoming the first caller there and
  landing the module here, converts a meaningless green into a real measurement,
  and the unit that lands it owns the result.
- `docs/solutions/workflow-issues/a-false-claim-in-the-auto-loaded-contract-compounds-silently.md`
  is the same failure with no executing check at all, so "green" there has to be
  read as the absence of red. Stated precisely it holds: in both cases a claim was
  true when written, was falsified by an act its author never saw, and nothing
  could go red. This learning is the harder version, because there a guard could
  not be written and here one WAS written and still could not go red.

  **That document has now received the narrowing, applied by the 2026-08-29
  refresh rather than by this capture.** Its lines 260 through 263 reassured the
  reader that a universal about CODE is the safe kind, because "falsifying it
  requires somebody to write an import, which is an act, which is reviewable, and
  which a guard can be written against". U42 is the counterexample, and it lands
  in that sentence's own register, since the example it reaches for is itself an
  import property. Here the guard WAS written, the act happened, the act was
  reviewable, and the guard stayed green, so the reassurance holds only where the
  guard's subject exists. The narrowing is now in that file, dated and pointing
  back here.

  The history is worth keeping. An earlier draft of this paragraph claimed the
  narrowing had already been recorded there when no text in that file mentioned
  this learning at all, which was an unbacked claim of a reciprocal edit and is the
  same defect this whole document is about. A grounding check caught it, the
  paragraph was rewritten to say the edit was recommended and not performed, and
  the refresh then performed it. Three states, one paragraph, and only the middle
  one was ever true.

**The mechanism for this existed and was not used.** `tests/_pending.py` is the
register built precisely for a guard whose subject has not landed yet, and neither
copy of the broken guard ever called `requires(`. A working countdown,
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`, sat in the
same file as the broken guard the whole time. The rule that follows: a guard that
names a subject the repository has not landed either registers that dependency in
the pending register, so it is a countdown rather than a wish, or derives its
subject from the tree so there is no unlanded name in it at all.
