---
title: "A new test file that writes the word residual then a quoted string fails the citation scan, and only in the full suite"
date: 2026-10-10
category: workflow-issues
module: tests/test_reserved_causes.py
problem_type: workflow_issue
component: testing_framework
severity: low
root_cause: missing_tooling
resolution_type: workflow_improvement
tags:
  - "residual-citation"
  - "full-suite-only"
  - "mutation-baseline"
---

# A test that writes `residual` then a quoted string is read as a citation

## Problem

U122 added a small test module for `derive_status`. Its own tests passed. The full suite
then failed `test_every_residual_this_unit_cites_is_cited_by_title` in
`tests/test_reserved_causes.py`, and the failure cost one mutation driver baseline,
about ten minutes, before it was understood.

## Cause

`CITATION` in `tests/test_reserved_causes.py` is the regular expression
`\bresiduals?\b[\s#:]*"([^"\n]+)"`. It scans every authored file under `src`, `tests`,
`scripts` and `docs`. Any line holding the word `residual` followed, with only
whitespace, `#` or `:` between, by a double quoted string is a citation of a residual by
title. The new test wrote an inline labels list holding that label beside a body keyword
argument, so the scan read the quoted text as a residual title that no ledger heading
matched. Nothing in the file under test fails, so a single file run never shows it.

## Next time

- Hold the label in a module constant, and reference the constant, so the word and the
  quote never sit on one line.
- A new test that builds issue or board fixtures about residuals is the likely carrier.
  Run `tests/test_reserved_causes.py` alongside the new file before starting a mutation
  driver baseline, since the baseline is the expensive place to find out.
