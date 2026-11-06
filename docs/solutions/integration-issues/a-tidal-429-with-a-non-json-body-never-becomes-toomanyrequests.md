---
title: "A Tidal 429 with a non JSON body never becomes TooManyRequests"
date: 2026-09-24
category: integration-issues
module: "src/cratekit/label, src/cratekit/core/cause.py, src/cratekit/acquire/provider_session.py, src/cratekit/modules/outbound/account.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "Code classifies a tidalapi failure as a rate limit"
  - "A cause walk is used to find the original HTTP error"
  - "Code reads a rejected session, a not found or any status off a tidalapi failure"
symptoms:
  - "A rate limit during a labels sweep is recorded as a permanent failure"
  - "A check for TooManyRequests passes in tests and misses in production"
tags:
  - tidalapi
  - rate-limit
  - exception-chain
  - r-704
  - r-1305
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
- **It is every status, not only the 429** (R-1305, 2026-11-05). A 401 or 403 whose body is a page reached both readers of a rejected session as the decode error, and the person was told to wait. `provider_session.failure_links` is the walk for a status off a client failure: declared causes first, then context, never into a `CratekitError` off the declared chain, cycle guarded. Read a status on any link it yields, and a type or name only where it says the link was declared. A 404 page has the same shape and four readers still miss it (the residual filed with R-1305).
- **Build the failure through the client, not by hand.** `tests/provider_answers.client_failure(status, body)` drives the installed client's own request handler over a canned answer and returns what it raises, so the chain under test is the client's. A cycle test whose walk has no guard spins rather than fails; count the link reads (the `Looping` failure in `tests/test_provider_rejection_bodies.py`) instead of a thread with a time limit, which leaves a spinner holding whatever lock the walk was inside.
