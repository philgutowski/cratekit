---
title: "A seam that returns only rows reads absence as evidence of absence, one layer up from where the counts were known"
date: 2026-09-09
category: workflow-issues
module: "src/cratekit/intake/recognize.py, src/cratekit/intake/acrcloud.py, src/cratekit/intake/cli.py"
problem_type: workflow_issue
component: seam_design
severity: high
root_cause: seam_too_narrow
applies_when:
  - "A seam is typed as the rows it produces and nothing else, and an implementation lands behind it that can fail partially"
  - "A verb reports an honest zero, nothing found, over a result whose producer also knew how much it did not look at"
  - "A caller reconstructs a number the producer computed, from a side channel such as a shared ledger or a file diff"
  - "A paid or bounded producer sits behind a seam declared by an earlier unit that could not spend and so never needed counts"
  - "A structural guarantee, such as no test can spend, was a property of a refusal that binding an implementation removed"
symptoms:
  - "A set where most chunks got no answer is reported as a set nobody recognised, at exit zero"
  - "A tracklist missing forty minutes of a recording carries no warning that anything was skipped"
  - "The verb reads a shared counter before and after the paid step and clamps a negative difference to zero"
  - "The producer's docstring says incomplete coverage is not a result and no caller can see the coverage"
related_components:
  - "intake"
  - "recognition"
  - "job_engine"
tags:
  - "seam"
  - "absence-as-evidence"
  - "honest-zero"
  - "coverage"
  - "spend"
  - "no-spend-guarantee"
---
# A seam that returns only rows reads absence as evidence of absence, one layer up from where the counts were known

## Context

U57 (issue #75) put the ACRCloud identifier behind the seam `recognize.identify`
had declared since U37. The seam's type was `Callable[[Path], tuple[Wanted, ...]]`:
an identifier answers with the rows it found. U37 could not spend, so that was
the whole of what an identifier had to say, and the docstring at the seam said
the injection point existed so the suite could prove the gate and the shape
without spending.

The implementation knew more than the seam let it say. `acrcloud.identify` counted
every call it made, every chunk the grid asked for, every chunk the service
answered with nothing, and every chunk that got NO answer, and its own docstring
said that the last count was returned rather than folded into the misses
"because coverage that is incomplete is not a result". Then `bound_identifier`
returned `.rows` to fit the seam, and every one of those counts was gone.

## What happened

Two defects followed from the narrow seam, and the review found both.

The set verb wanted to say what a set cost, so it read the shared monthly ledger
before and after the paid step and subtracted, clamping a negative to zero. That
number was wrong under a second process spending in the same window and wrong
across a month boundary, and it was a reconstruction of a value the producer
had held one call earlier.

Worse, a run where most chunks got no answer and the rest named nothing returned
an empty tuple through the seam, and the set verb reported it as the honest zero
it had been built to give: "nothing identified", with the calls it cost, at exit
zero. The producer refused only when EVERY chunk was unanswered. At ninety
percent unanswered the verb told a person their recording held nothing
recognisable when nothing had listened to it. That is METHOD's first pattern,
absence read as evidence of absence, reproduced one layer above the module that
had written the rule against it.

## Why the source does not explain it

Each module was right on its own. The identifier counted and returned. The seam
declared the shape an earlier unit needed. The verb reported what it was given.
The defect lived in the seam's TYPE, which no test exercises: a test drives a
fake identifier that returns rows, and the rows are correct. The mutation table
would have found nothing either, because there was no line to revert. The narrow
seam was not a guard that could be killed; it was a channel that could not carry
the fact.

## The rule

When an implementation lands behind a seam an earlier unit declared, ask what the
implementation knows that the seam's return type cannot say, and widen the seam
before the first caller reconstructs it from a side channel. The tell is a
caller reading a shared file, a clock or a counter around the call to recover a
number the callee just computed. The second tell is an honest zero: a verb that
reports "nothing found" has to be able to distinguish "looked everywhere and
found nothing" from "looked at a tenth of it", and that distinction has to
arrive through the seam, because nothing else knows it.

The fix here was a small dataclass at the seam, `recognize.Identified`, carrying
the rows and the four counts, with the seam still accepting a bare tuple from a
fake so the old injection tests stand. The verb then freezes the counts on the
job, refuses a zero over unanswered chunks as a failure, and warns on a
tracklist with gaps. No ledger is read by the verb at all.

## The guarantee that moved when the seam was bound

Binding an implementation to a seam that used to refuse takes away whatever the
refusal guaranteed. Until U57, no test could spend: `identify` refused whenever
no identifier was injected, so a test could record credentials, find binaries
and drive the verb, and still reach no network. Once the seam bound the ACRCloud
identifier, that guarantee became per test discipline: every test that satisfied
the gate happened to patch the transport. The review named it, and an autouse
fixture in `tests/conftest.py` now replaces the shipped transport with one that
fails the test, so the property is structural again. When a seam stops refusing,
find what the refusal was quietly guaranteeing and put it back somewhere that
does not depend on the next test author remembering.

## The test that holds it

`tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`
drives two unanswered chunks and one miss through the real verb and asserts the
failure cause with the unanswered count in its detail. Its sibling asserts that
a set queued over one unanswered chunk carries the warning and that the resume
repeats it. Row C6 of `docs/mutation/u57-recognition-and-items.md` reverts the
refusal and is killed by exactly that test.

## Where else this applies

Every seam this project declares ahead of its implementation: the catalogue
protocol in `label/catalogue.py`, the adapter contract in `acquire/adapter.py`,
and any future recognition or search seam. Each returns a shape chosen before
anything could fail partially. The question to ask at binding time is the one
above: what does the implementation know that the type cannot carry.

## See also

- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`
- `docs/solutions/workflow-issues/asserting-an-absence-pins-the-observation-and-not-the-mechanism.md`
- R-304 and R-306 in `docs/residual-findings.md`, the two costs of identifying at the queue that the widened seam now reports rather than hides.
