---
title: "A helper that can return its argument unchanged makes `raise x from x` reachable, and it truncates the cause chain"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/backup/cli.py, src/cratekit/tagging/retag_cli.py"
problem_type: workflow_issue
component: error_handling
root_cause: incorrect_assumption
resolution_type: code_fix
applies_when:
  - "A refusal is extended with an extra remediation step before being re-raised"
  - "The extending helper has a branch that returns the error it was handed, unchanged"
  - "The call site reads `raise helper(exc, ...) from exc`"
  - "A queued verb adds an advisory to the refusals its resume can raise"
symptoms:
  - "A refusal's declared cause chain ends at the refusal itself"
  - "A cause that classified as one reason before the change classifies as a different one after"
  - "A person is told to retry later where they used to be told to grant path access"
  - "Every test stays green, because the reason and the steps are both still correct"
related_components:
  - job_engine
  - cli_dispatcher
tags:
  - cause-trail
  - exception-chaining
  - queued-verbs
  - remediation-steps
  - r-221
  - r-225
---

# A helper that can return its argument unchanged makes `raise x from x` reachable

## Context

`crate backup run --job` had to say, on every ending, whether the job it drove
was a rehearsal. Three of those endings are refusals, and a refusal envelope
carries no warnings at all, so the word had to ride on the cause as an appended
remediation step. That is the shape
[a queued verb has two exits](a-queued-verb-has-two-exits-and-an-advisory-on-the-envelope-only-reaches-one.md)
records for `tag retag`, and `retag_cli.with_reload_step` is the function this
one was written from.

The helper appends a step by replacing two fields of the cause it was handed,
so the origin trail, the nested cause, the detail, the scope and the retryable
flag all travel through by construction rather than being rebuilt. It also has
a branch the retag one does not: a job that is a real backup gets the error back
untouched, because telling a person whose real backup failed that nothing was
copied is false in the direction that stops them looking for the half that was.

## What went wrong

The call site read:

```python
except CratekitError as exc:
    raise _with_rehearsal_step(exc, job) from exc
```

On a rehearsal that is correct. On a real run the helper returns the same
object, so the line is `raise exc from exc`. The exception becomes its own
`__cause__`.

Nothing failed. The reason was right, the steps were right, the message was
right, and the suite was green, because no test looks at `__cause__`.

What moved was classification. `cause.classified` walks the declared chain to
find the underlying condition, and a chain that points at itself ends there. A
`no-evidence` refusal raised over a `PermissionError` had rendered as
`path-permission-denied` with `grant-path-access`; after the self-cause it
rendered as `no-evidence` with `retry-later`. A person whose state directory was
not writable was told to try again in a while.

## The rule

**When a helper can return its argument unchanged, the call site has to branch on
identity, not on the helper's name reading as if it always builds something new.**

```python
extended = _with_rehearsal_step(error, job)
if extended is error:
    raise error
raise extended from error
```

`retag_cli` reaches the same place a different way: its caller asks whether
anything was corrected and takes a bare `raise` when nothing was, so its helper
is never called on the pass-through case at all. Either shape works. What does
not work is a helper with a pass-through branch whose result is raised `from`
the same name unconditionally.

## How wide it is here

An AST sweep of `src` for `raise <helper>(<name>, ...) from <name>` found
fourteen sites, and a second pass over each helper asked whether it has a
`return <first argument>` at all. **None of the fourteen does.** Every one of
them builds a new refusal on every path, so the shape does not reproduce
anywhere else in the package today. The one that could was this branch's own,
and it is now guarded by
`test_a_refusal_this_verb_re_raises_is_never_its_own_cause`, which drives both
branches and asserts on the identity rather than on a rendered remedy, because
which remedy moves depends on what the chain happened to carry underneath.

## The general shape to remember

A green suite cannot see an exception chain. The reason, the message and the
steps are all asserted somewhere, and `__cause__` is asserted nowhere, so a
defect that changes only the chain arrives looking exactly like a correct
change. If a round touches how a refusal is re-raised, the chain is the thing to
drive on purpose.
