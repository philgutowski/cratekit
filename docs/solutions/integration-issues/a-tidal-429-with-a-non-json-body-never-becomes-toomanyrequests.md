---
title: "A Tidal 429 with a non JSON body never becomes TooManyRequests"
date: 2026-09-24
category: integration-issues
module: "src/cratekit/label, src/cratekit/core/cause.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "Code classifies a tidalapi failure as a rate limit"
  - "A cause walk is used to find the original HTTP error"
symptoms:
  - "A rate limit during a labels sweep is recorded as a permanent failure"
  - "A check for TooManyRequests passes in tests and misses in production"
tags:
  - tidalapi
  - rate-limit
  - exception-chain
  - r-704
---

# A Tidal 429 with a non JSON body never becomes TooManyRequests

## Problem

R-704. Sitting 11's labels sweep recorded 20 rate limit answers as `permanent_failed`, so `crate job resume` could not retry them. Fixing the classifier for `TooManyRequests` alone still missed some real 429s.

## Cause

tidalapi builds its own error class by reading the response body as JSON first. A 429 whose body is not JSON never reaches that step. It surfaces as a requests `JSONDecodeError` with no declared cause, and the 429 sits two implicit contexts down, under the stdlib decode error. A walk that follows only the declared cause chain, as `core.cause._chain` does, never sees it.

## Next time

- Test a rate limit check by driving `http_error_to_tidal_error` with a hand built `Response` that has a non JSON body, not by raising `TooManyRequests` directly.
- Walk implicit context as well as declared cause when looking for the 429.
- The mutation driver's leak guard halts every batch while the installed copy's analyze vocals job writes the real state folder. Point `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR` at an empty temp folder for the driver, and say so in the notes.
