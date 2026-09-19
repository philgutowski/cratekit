---
title: "Dropping the release in a generator context manager kills nothing under CPython, and keeping the exception alive does not change that"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/intake/landing.py, src/cratekit/core/jobs.py, scripts/mutate.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
resolution_type: workflow_improvement
applies_when:
  - "A mutation row drops the release, the close or the __exit__ call in the finally clause of a contextlib.contextmanager lock"
  - "A test is being written to prove a lock is released when the body raises"
  - "A zero row on a lock release is about to be read as a missing test"
symptoms:
  - "The release row reads zero on the subset and zero again on the promoted full suite"
  - "A test that keeps the raised exception alive across the second take still passes on the mutated tree"
tags:
  - "mutation-driver"
  - "locks"
  - "contextmanager"
  - "inert-mutation"
  - "composite"
---

# Dropping the release in a generator context manager kills nothing under CPython

## What happened

R-432's unit added `landing.batch_lock`, a `@contextmanager` that enters
`jobs.driver_lock` by hand and releases it in a `finally`. Mutation row A4
replaced that release with `pass`. It killed nothing of 106 and nothing of
8857, in two separate tables.

The release still happens on the mutated tree. When the `with` ends, the
generator behind `batch_lock` finishes, CPython frees its frame at once, the
frame's only reference to the inner lock goes with it, the inner generator is
closed, and its own `finally` closes the descriptor, which is what drops a
`flock`. No test can see a difference, because there is none to see on an
interpreter that counts references. This is the inert half of
[`a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md).

## The trap that cost a table

The obvious way to separate the two is to keep the raised exception alive
across the second take, on the theory that its traceback holds the lock's
frame and so holds the lock open. It does not. `contextlib`'s `__exit__` puts
the CALLER's traceback back on the exception before it lets it go, so the
generator's frame is never in it. A test written on that theory passed on the
mutated tree, carried a comment that was false, and cost a six minute batch to
find out.

## The rule

For a lock built on a generator context manager, do not spend a row or a test
trying to pin the release line alone. Measure the row once, expect zero, and
pair it with a composite that makes the leak real: drop the release AND keep
the lock object alive, for example by appending it to a module level list. In
R-432's table that composite killed 7, which is the evidence that the release
tests hold a lock that outlives its `with`. Keep the explicit release anyway,
for an interpreter that does not count references.

## Related

- `docs/mutation/r432-a.md` row A4, `docs/mutation/r432-b.md` rows A4r and A4c.
- `docs/residual-findings.md`, R-535.
