---
title: "A json only driver cannot see a blank human renderer"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/cli/render.py, tests/cli_drive.py, tests/test_label_workers.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A verb already puts the answer on the envelope and the default renderer drops it"
  - "The suite drives that verb through tests.cli_drive.drive or another helper that requests json"
  - "A live run printed only the verb, the outcome, and a run id"
  - "A green battery is being taken as evidence that a person can read the result"
symptoms:
  - "crate label harvest prints label.harvest: ok and a run id, nothing else"
  - "Every harvest test still passes, because drive always requests json"
  - "The envelope carries queue, items, and unresolved, and none of those reach the default output"
related_components:
  - "cli-render"
  - "label-harvest"
  - "review-set"
tags:
  - "human-renderer"
  - "json-driver"
  - "review-set"
  - "silent-failure"
  - "label-harvest"
---

# A json only driver cannot see a blank human renderer

## Context

The first live `crate label harvest`, 2026-09-17, found four labels and six
unresolved tracks and printed `label.harvest: ok` and a run id. The envelope
already carried both. `cli.render.render` had no case for `review_set/1`.

The suite never saw it. `tests.cli_drive.drive` always requests json, validates
the envelope, and returns the payload. Every harvest test in
`tests/test_label_workers.py` went through that helper, so a blank default
output and a complete json envelope were the same green.

The fix is not only to render the set. A new harvest test that goes through
`drive` will stay green if the renderer is deleted. The tests that pin this
call `cli.run` without requesting json and assert the name as its own
indented line, which a dump of the envelope as text would not satisfy.

## Guidance

When the defect is what a person reads by default, drive the dispatcher in
the default human mode. `tests.cli_drive.drive` is the right helper for the
envelope contract and the wrong helper for the renderer. If the stored shape
is already tested in json, the human test still has to be a second invocation,
not a render of the json the first one returned, unless that render is how
the process actually prints.

## When to Apply

- A verb emits a structured surface and the default renderer has no case for it.
- The suite's driver for that verb always requests json.
- A live run printed only the verb, the outcome, and a run id.
