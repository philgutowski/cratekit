---
title: "The conformance sample mapping is built whole on every call, so a sample that writes state writes it under every verb's drive"
date: 2026-09-27
category: workflow-issues
module: "tests.test_cli_contract"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: logic_error
resolution_type: test_fix
applies_when:
  - "A new verb needs sample arguments in tests/test_cli_contract.py"
  - "The sample has to prepare library state, not only name a path"
  - "A verb under conformance reads library state another sample may have left"
symptoms:
  - "A verb that passes its own suite refuses under conformance 3 on state nothing in its sample created"
  - "An intake file appears under the fixture library in a drive of an unrelated verb"
related_components:
  - "tooling"
tags:
  - "conformance"
  - "sample-arguments"
  - "test-isolation"
  - "cutover"
---

## The trap

`_sample_arguments` returns one verb's arguments by building a mapping of
every verb's arguments and indexing it. Every value expression runs on every
call, whichever verb is being driven. Most are literals. A few write: the
sample for `sync mark` writes an export and renames it to a name ending
`_synced_inboxed.xml`, under the fixture library.

That was harmless until a verb read library state. `crate tree cutover`
refuses while an intake file is pending, so under conformance it refused
`cutover-xml-pending` over a file its own sample never made. The reverse is
worse: a sample that recorded a cutover, built eagerly, would have put a
native tree under every other verb's drive, and the routing verbs behave
differently over one.

## The rule

A value in that mapping may be a callable, and the mapping's caller resolves
it only for the verb being driven. A sample that writes anything is written
as a callable. `sync.mark`, `tree.cutover` and `tree.revert` are.

Conformance 3 holds a gated verb to reaching its gate and ending OK once it
is answered. A verb that refuses an unready library before its gate therefore
needs a sample that makes the library ready, and
`tests/cutover_fixtures.py` `ready` is that, shared with the verb's own suite
so the two cannot build different libraries.

## Related

`docs/solutions/workflow-issues/a-disposable-database-copy-does-not-make-library-state-disposable.md`,
the same fact from the other side: library state is written beside the library
root, by whoever runs.
