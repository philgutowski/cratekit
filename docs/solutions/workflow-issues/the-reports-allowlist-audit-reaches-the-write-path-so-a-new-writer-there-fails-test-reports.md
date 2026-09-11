---
title: "The reports allowlist audit reaches the write path, so a new writer there fails test_reports"
date: 2026-09-11
category: workflow-issues
module: tests/modules/test_reports.py
problem_type: workflow_issue
component: development_workflow
severity: medium
resolution_type: documentation_update
applies_when:
  - "A unit adds or changes a function in core/session, core/rb_writer, core/snapshot, core/reconcile, core/tree_registry or core/backup_facts"
  - "test_the_allowlist_admits_no_writer_this_guard_cannot_name fails on a branch that never touched the reports package"
  - "A unit adds a first party import to a module the reports allowlist admits"
tags: [allowlist, reports, closure, qualified-mutations, guard, r-102, r-340]
---

# The reports allowlist audit reaches the write path

## What bites

`test_the_allowlist_admits_no_writer_this_guard_cannot_name`, in
`tests/modules/test_reports.py`, used to read only the modules `ALLOWED_IMPORTS`
names. Since R-102 it reads their **import closure**: every first party module
reachable by following imports out of the allowlist. That closure is eighteen
modules, and through `rbxml` to `tree_registry` to `session` it reaches
`rb_writer`, `snapshot`, `reconcile` and `backup_facts`.

So a unit that never touches the reports package can turn this test red. Add a
function to `session.py` that writes a file, or that calls anything already
named as a writer, and the audit reports it as a writer it cannot name. The
cascade is real. `config.load` writes the configuration file back, so any new
function calling it, directly or through `rb_writer._loaded_config`, counts as
a writer. Forty nine names were needed to make the tree green, most of them
for that reason.

## What to do when it fires

Read the failure. It names each module and function. Then take one of the two
answers the test's message gives:

- **Add the name to `QUALIFIED_MUTATIONS`** as `module.function`, with the short
  module name in front. This is the usual answer for the write path modules,
  since the reports package could reach them and should be caught if it calls
  them.
- **Take the module off the allowlist**, when it is an admitted module that has
  gained a write it should not have.

Do not narrow the closure to get green. Following the imports is what R-102
closed, and a closure that stops early is the one hop walk again.

Adding a first party import to an admitted module grows the closure. If the
import is one the closure cannot read, a computed `__import__` or
`importlib.import_module`, or a target with no file behind it, the audit refuses
it as unfollowed rather than treating it as clean.

## What it does not protect

Naming a writer only helps if a report calling it is caught. A report reaching
it through another module's attribute, `rbxml.tree_registry.write(x)`, is not
caught today. That is R-340, driven on the tree, and it is why the forty nine
names are the audit's argument rather than the whole of the protection.
