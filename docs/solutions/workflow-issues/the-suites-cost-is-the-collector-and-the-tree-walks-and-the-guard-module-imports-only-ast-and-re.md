---
title: The suite's cost is the collector and the tree walks, and the source guard module may import only ast and re
date: 2026-11-22
category: workflow-issues
module: tests/conftest.py, tests/_source_guards.py
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: unmeasured_shared_setup
resolution_type: tuning
applies_when:
  - A card sets out to make the suite faster, or a worker's run time grows with no test to blame.
  - A change to tests/_source_guards.py adds an import or keeps anything about a source text.
  - A per test fixture makes a directory with tmp_path_factory.mktemp.
tags:
  - suite-speed
  - garbage-collector
  - source-guards
  - conftest
  - u326
---

# The suite's cost is the collector and the tree walks, and the source guard module may import only ast and re

## What happened

U326 profiled the shared setup every test pays, expecting the fourteen autouse
fixtures to be the cost. They were not: together about 0.8 ms a test. The
largest cost no test asked for was the cyclic garbage collector, 50 of 270
seconds in one process over an eighth of the suite, because a worker's heap
grows to hundreds of thousands of tracked objects and every full pass walks
all of it. The next was the source guards, which spend their time in the
standard library's three generator deep `ast.walk`, several walks per module
per question.

## What to do

- **Measure the collector first.** A `gc.callbacks` timer around a serial run
  of a sample of files says how much of it is collection. `tests/conftest.py`
  now sets `COLLECTOR_THRESHOLDS` at configure; freezing the collected objects
  instead does not help, since it only makes full passes more frequent.
- **Profile with `cProfile` only to rank, never to size.** It multiplies the
  cost of every generator resumption, so `ast.walk` read as most of a guard's
  time there and as a third of it by the clock.
- **`tests/_source_guards.py` may import only `__future__`, `ast` and `re`, and
  may do nothing with a `source: str` but pass it to `ast.parse`.**
  `tests/test_reserved_causes.py` pins both, so that no comment can ever reach
  a rule. A memo keyed on a source text, a `hashlib` digest, `weakref` and
  `collections.deque` are all refused there. U326 dropped a text keyed memo
  for this reason and held the walk cache to one module by identity.
- **`tmp_path_factory.mktemp` lists the whole base temp** to find its next
  number, so a per test fixture using it pays a listing that grows with every
  test the worker ran. `tempfile.mkdtemp` under one session directory lists
  nothing. On this container's filesystem the listing was cheap at the suite's
  scale; it grows linearly all the same.
