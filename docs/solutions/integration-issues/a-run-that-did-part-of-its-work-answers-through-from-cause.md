---
title: A run that carried out part of its plan answers through from_cause on its own surface, because the envelope contract admits no partial outcome
date: 2026-09-20
category: integration-issues
module: "src/cratekit/cli/output.py, src/cratekit/core/cause.py, src/cratekit/write/naming_cli.py"
problem_type: integration_issue
component: envelope_outcome
root_cause: contract_not_visible_in_the_code
resolution_type: code_fix
severity: medium
symptoms:
  - "A brief asks a verb to answer partial rather than ok and there is no partial in Outcome"
  - "Adding an Outcome member looks like a two line change and reaches the exit code vocabulary, the envelope validator and every pinned population"
  - "Raising a refusal to report a run that did work throws away the payload that says what landed"
  - "A verb wants a cause on a success shaped envelope and ctx.envelope takes no cause argument"
applies_when:
  - "A verb performs a batch and some items fail while others succeed"
  - "A brief or a ledger entry says the outcome must be something other than ok"
  - "A sweep reports ok over state it could not write, which is the merge bar's own shape"
tags:
  - "envelope"
  - "outcome"
  - "cause"
  - "from-cause"
  - "name-apply"
  - "r172"
---

# A run that did part of its work answers through from_cause

## Context

R-172: `name apply` promised two renames, performed one, and answered ok. The
brief said to "answer partial rather than ok when any exist". There is no
`Outcome.PARTIAL`, and the two obvious ways to get one are both wrong.

## The contract nothing in a verb shows you

`cli/output.envelope_problems` is where the rules actually live, and three of
them decide this together:

- `succeeded = outcome in (Outcome.OK, Outcome.NO_OP)`. Every other outcome is a
  non success.
- a non success outcome MUST carry a structured cause, and a success must not.
- a non success outcome must NOT exit 0, and a success must exit 0.

So "the outcome is not ok" and "there is a cause and a non zero status" are one
decision, not three. A new `PARTIAL` member does not get you a soft answer: it
either joins the success set, in which case it cannot carry the cause that names
what failed, or it does not, in which case it is a failure with a different word
on it. The word is the only thing a new member buys, and it is bought at the
price of the exit code vocabulary, the envelope validator, the CLI contract suite
and every pinned population in `tests/test_reserved_causes.py`.

## What the codebase had already decided

Two precedents answer it, and neither is in the module a verb author is reading:

- `adopt/apply_cli._resume` says it plainly: "IT RAISES ON A JOB THAT DID NOT
  FINISH rather than reporting one. That is R-225." Partial work is a failure
  here, not a warning.
- `cli/doctor.doctor` shows the mechanism. A report that RAN and found failures
  is not raised, it is built: `output.build(outcome=FAILED, code=cause.code,
  data=report.payload(), cause=cause)`, on the verb's own payload surface.

`output.from_cause` is the same thing with the boilerplate removed. It takes a
`schema` and a `data`, defaults the outcome to FAILED, reads the code off the
cause and appends the CLI boundary to the origin. Its docstring says the
diagnostic surface is the default "unless the caller names another, even when the
verb would have emitted a plan", and naming another is exactly what a verb that
produced a plan and carried out part of it should do.

## The shape to copy

```python
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    return output.from_cause(
        verb=ctx.entry.name,
        run_id=ctx.run.run_id,
        started=ctx.started,
        cause=_incomplete_cause(incomplete, renamed=renamed, collides=collided),
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
```

Three things make it work, and each is a trap on its own:

1. **The cause is built with `cause.refuse(...).cause`**, so the reason is
   validated against `REASONS` and the remediation defaults the way every other
   refusal's does. Hand building a `Cause` skips both.
2. **The payload travels.** Raising from the handler is the one thing that cannot
   work: `cli.run` catches `CratekitError` and calls `from_cause` with no data, so
   the answer arrives on the diagnostic surface and what the run DID do is gone.
   That is the information a person needs most.
3. **The payload is not edited after the gate.** The digest the person answered
   covers `items`, so per item outcomes go in a free form `totals` key or in the
   cause detail, never back into `items`. The plan surface is a closed set of four
   fields, `digest`, `items`, `totals` and `chunk`, with `additionalProperties`
   false, so a fifth top level key fails validation.

## What this does not license

A non zero exit for a hold the product chose on purpose. `name apply` holds back
every file the rekordbox collection references and still answers ok, because that
hold is permanent, explained in the plan, and not work anybody owes. The
distinction is whether a person can act on it: outstanding work that a person can
clear exits non zero, a designed refusal to touch a file does not.
