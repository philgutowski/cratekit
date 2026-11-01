---
title: shlex.quote anywhere in src fails the location guard, which reads any call named quote
date: 2026-11-01
category: workflow-issues
module: tests/test_locations.py, src/cratekit/label/sync_cli.py
problem_type: workflow_issue
component: development_workflow
severity: low
root_cause: hidden_contract
resolution_type: code_fix
applies_when:
  - A remedy or a printed command quotes a value for a shell
  - Any module outside cratekit.core.locations calls something named quote, quote_plus, unquote or unquote_plus
tags:
  - shell-quoting
  - location-guard
  - remediation-steps
---

# shlex.quote anywhere in src fails the location guard

`tests/test_locations.py::test_no_module_outside_this_one_decodes_a_location_itself`
walks every module under `src` and fails on any call whose name is `quote`,
`quote_plus`, `unquote` or `unquote_plus`, by name alone, so that rekordbox
Location encoding lives in `cratekit.core.locations` and nowhere else. It does
not look at what the call is an attribute of, so `shlex.quote` is refused the
same as `urllib.parse.quote`.

U189 quoted a label name in a refusal's remedy with `shlex.quote`. The label
sync test files were green, and the first sign was the mutation driver's
baseline refusing as red on this one test, a full suite run later.

**Do instead.** Name the label by its registry identifier when the entry is in
hand, as the other remedies in `label/sync_cli.py` do. When only the typed name
is in hand, `repr` quotes a name with a space or an apostrophe as one shell
word. Do not add an exemption to the guard for a shell quote, and do not reach
the same function through another name to step around it.
