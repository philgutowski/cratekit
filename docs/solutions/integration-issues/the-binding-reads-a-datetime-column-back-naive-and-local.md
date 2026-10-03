---
title: The binding reads a datetime column back naive and already local, not aware at UTC
date: 2026-10-03
category: integration-issues
module: "src/cratekit/intake/rotate.py, src/cratekit/write/collection_export.py"
problem_type: integration_issue
component: database
severity: low
root_cause: wrong_assumption
resolution_type: documentation_update
applies_when:
  - "Code takes a day or an age from created_at or updated_at on a rekordbox row"
  - "A review says the value is timezone aware at UTC and must be converted"
symptoms:
  - "A mutation that reads the date on the UTC calendar kills no test"
  - "A review finding about an evening row aging a day young cannot be reproduced"
tags:
  - "pyrekordbox"
  - "datetime"
  - "timezone"
  - "created-at"
---

# The binding reads a datetime column back naive and local

## What is stored and what is returned

rekordbox stores `created_at` and `updated_at` as text at UTC,
`2026-10-03 03:30:00.000 +00:00`. pyrekordbox 0.4.4, the pinned binding,
parses that in `tables.string_to_datetime` and returns
`dt.astimezone().replace(tzinfo=None)`: a NAIVE datetime already converted to
the machine's local time. `row.created_at.date()` is the local day.

## The trap

U111's built in review read the text format and concluded the value comes
back aware at UTC, so an evening import would date to the next day. A fix
converted aware values, and its mutation row, the conversion removed, killed
nothing across the full suite. Driving the producer showed why: the binding
never returns an aware value. The conversion stays as a guard for another
binding, and the evening test pins the local day through the binding.

**The rule.** Before acting on a claim about what the binding returns, read it
off a row in the suite. `collection_export.py` converts only an aware value for
the same reason.
