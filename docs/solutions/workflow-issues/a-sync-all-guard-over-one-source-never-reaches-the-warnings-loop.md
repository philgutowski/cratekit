---
title: "A sync all guard over one source never reaches the warnings loop"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/sync/cli.py, tests/test_sync_all.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test drives crate sync all to assert something about ONE source's warnings or report"
  - "That test sets up only the source it is about and leaves the others to refuse"
  - "The assertion is a negative one: this code is NOT in the warnings"
  - "A mutation row over the warnings loop or the plan filter comes back zero"
symptoms:
  - "A sync all test passes and would pass with the whole warnings loop deleted"
  - "A mutation row deleting `if plan.filed or plan.not_queued == NOTHING_NEW` kills nothing"
  - "The envelope the test asserts over carries no warnings at all, whatever it does"
related_components:
  - "sync-all"
  - "mutation-table"
  - "outbound-favorites"
tags:
  - "vacuous-assertion"
  - "sync-all"
  - "mutation-zero"
  - "absence-as-evidence"
---

# A sync all guard over one source never reaches the warnings loop

## Context

`crate sync all` plans every enabled source, asks the one question favourites
needs, queues, and only then builds its envelope. Before the envelope it has a
short circuit: if nothing queued and any source refused, it RAISES that source's
own cause rather than returning a report. The warnings loop, the per source
checks and the summary are all below that raise.

A guard written on `relay/111` asserted that a DECLINED favourites source does
not report the standing warning the queued one carries. It registered no label,
bound no catalogue, and answered the confirm with abort. Every source then had
nothing to do, nothing queued, and the pass raised. The envelope it asserted
over was a refusal, which carries none of the report the loop builds, so the
assertion held over an empty collection.

It would have held with the filter deleted, with `plan.warnings` never set, and
with the entire loop removed. The mutation row that deleted the filter killed
nothing on the subset and nothing on the promoted full suite, and the zero read
as "the filter is untested" when the truth was "the test never gets there".

## Guidance

A negative assertion about `crate sync all`'s report needs a second source that
actually queues, or the pass will not produce a report to assert over. One
registered label is enough: `register(LABELS[0])` makes the labels sweep queue,
`queued_any` is true, the raise is skipped, and the loop runs. Then assert
`code == ExitCode.OK` as well, because that is the cheap signal that the
envelope came from the reporting path rather than the refusing one.

The same applies to the per source checks and to `summary["not_queued"]`. Every
existing test in `tests/test_sync_all.py` that asserts over those registers a
label first, which is not decoration.

More generally, on this verb: an assertion that something is ABSENT from a
report is only as good as the report existing. Pair it with one positive
assertion about the same envelope, so a pass that produced nothing fails
instead of agreeing with you.

## When to Apply

- Writing any `tests/test_sync_all.py` row that asserts over `warnings`,
  `checks` or `summary` for one source.
- Reading a mutation zero over `sync/cli.py`'s envelope building: check whether
  the guard's drive reaches that code at all before concluding the code is
  unguarded.
- Any verb with a "nothing happened and something refused, so raise" branch
  above its reporting path.
