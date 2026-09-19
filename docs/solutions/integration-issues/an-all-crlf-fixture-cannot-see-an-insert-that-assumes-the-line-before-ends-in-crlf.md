---
title: An all-CRLF fixture cannot see an insert that assumes the line before ends in CRLF
date: 2026-09-19
category: integration-issues
module: "src/cratekit/write/rbxml.py"
problem_type: integration_issue
component: xml_writer
root_cause: missing_validation
resolution_type: code_fix
severity: high
symptoms:
  - "The creating writer reports success and the exported XML is corrupt, a '/>' is split"
  - "Every test passes, because every fixture is CRLF throughout"
applies_when:
  - "A writer splices a node into an export at an offset computed from a close line's start"
  - "A new export sweep calls a bridge writer with tree=None"
tags:
  - "rbxml"
  - "line-endings"
  - "fixtures"
  - "R-447"
---

# An all-CRLF fixture cannot see an insert that assumes the line before ends in CRLF

## Problem

U91 (`route unplaced --export X`) was the first caller of `trees.apply_unplaced_changes`. Over a real-shaped export with a bare LF line just before a genre folder's close, the create branch wrote a node one byte early, splitting a `/>`, and reported success.

## Cause

Every lead broken insert in `write/rbxml.py` puts its node at the close line's start minus two bytes. That silently assumes the previous line ends in CRLF. rbxml's own header says real exports still carry bare LF lines. Every test fixture is CRLF throughout, so no suite could see it, and the author's green battery proved nothing about it.

A second, smaller trap. With `tree=None` the bridge writers search the whole playlist section instead of refusing, so a namesake genre folder outside the routing tree takes the write. Only a fixture holding such a namesake can catch it.

## Next time

- Before trusting a splice offset, ask `rbxml._break_before` rather than subtracting two. `splice_into_subplaylist`'s create branch now does this and warns.
- Give fixtures a mixed-ending case (a bare LF line before the close) whenever a writer computes byte offsets.
- The four sibling inserts still have the defect, recorded as R-447 in `docs/residual-findings.md`. Fix them the same way.
- A new export sweep should pass a routing tree, or add a namesake-folder fixture.
