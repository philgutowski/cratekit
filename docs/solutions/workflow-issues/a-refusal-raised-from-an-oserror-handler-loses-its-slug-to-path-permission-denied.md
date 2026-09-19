---
title: "A refusal raised from an OSError handler loses its slug to path-permission-denied when the OS refused on permission"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/write/metadata_cli.py, src/cratekit/cli/cause.py, tests/test_reserved_causes.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: inadequate_documentation
resolution_type: documentation_update
applies_when:
  - "A new refusal slug is raised from inside an except OSError handler"
  - "A test needs the permission-denied case of an unreadable file"
symptoms:
  - "A test asserting the site's own slug fails with path-permission-denied"
  - "A chmod based permission test needs a skipif for root"
tags:
  - refusals
  - exit-codes
  - testing
---

# A refusal raised from an OSError handler loses its slug to path-permission-denied

## Problem

R-342 made an unreadable vocal calibration raise `vocal-calibration-unreadable`. The test for the permission case expected that slug and got `path-permission-denied`.

## Cause

`cause.classified` runs in the `CratekitError.cause` property. It rewrites any refusal chained from a `PermissionError` to `path-permission-denied`. The site's slug survives only on `declared_cause`. Separately, a `skipif` in any test file outside `tests/_pending.py` fails `test_pending_units`, so the usual chmod plus skip-for-root pattern is not allowed.

## What to do next time

- Assert the site's slug on `declared_cause`, and the corrected one on `cause.reason`.
- Build the permission case by monkeypatching the read to raise `PermissionError`, not by chmod behind a root skip. This also works when the suite runs as root.
- Pin both the declared and the classified slug, so neither can drift.
