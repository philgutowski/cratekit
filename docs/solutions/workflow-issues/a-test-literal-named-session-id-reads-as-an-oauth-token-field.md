---
title: A test literal named session_id reads as an OAuth token field
date: 2026-10-14
category: workflow-issues
module: "scripts/scan_repo.py"
problem_type: workflow_issue
component: secret_scan
root_cause: shape_over_identity
resolution_type: workaround
severity: low
symptoms:
  - "A commit touching a test helper that stamps a fake session id is refused by the pre-commit hook"
  - "The scan reports an OAuth token field at a line with no real credential in it"
applies_when:
  - "A test helper assigns a string sixteen characters or longer to a keyword literally spelled session_id, client_id, access_token, refresh_token, id_token, client_secret, or consumer_key/secret, in `key = \"value\"` or `\"key\": \"value\"` form"
tags:
  - "secret-scan"
  - "pre-commit-hook"
  - "test-helper"
---

## Problem

A test helper in R-1017's suite stamped a fixture's session id with a
keyword-value pair shaped like `session_id` followed by `=` and a quoted
timestamp-plus-suffix string. The repo scan's pre-commit hook refused the
commit, reporting an OAuth token field at that line.

## Cause

`scripts/scan_repo.py`'s "OAuth token field" pattern matches on shape, not on
whether the value is a real secret: any of `session_id`, `client_id`,
`access_token`, `refresh_token`, `id_token`, `client_secret`,
`consumer_key`/`consumer_secret` assigned a quoted value of sixteen characters
or more trips it, in either `key = "value"` or `"key": "value"` form. A
session id long enough to be useful as a fixture (a timestamp plus a suffix)
is long enough to match. This is deliberate: the scan is written to catch
credential shapes even when nobody remembered to name a new field in a
keyword list (see the sibling entry on the camelCase miss in this same
pattern), so it does not special case "this one is just a test id."

## What to do next time

Give a test helper's stamped identifier a keyword that is not on the list,
for example `fixture_session` or `fake_session`, instead of `session_id`.
Do not loosen the scan pattern to carve out test files or short-looking
values; the pattern is intentionally shape-based and a carve-out is exactly
the kind of gap it exists to avoid.
