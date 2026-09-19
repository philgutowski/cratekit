---
title: The reserved binary keys are remedy tokens, not reasons a verb can refuse with
date: 2026-09-19
category: integration-issues
module: "src/cratekit/core/cause.py"
problem_type: integration_issue
component: cause_vocabulary
root_cause: wrong_api
resolution_type: code_fix
severity: medium
symptoms:
  - "A verb that raises a refusal whose reason is install-binary, install-binary-source-unknown, fix-binary-override or unsupported-platform exits 1 as an internal error"
  - "The envelope's cause message reads UnknownReason and the install hint the refusal carried is gone"
applies_when:
  - "A verb shells out to an external binary and wants a missing one to refuse with the binaries module's install hint"
  - "Reading cli/exit_codes.py, which says BinaryNotFound carries one of those four as its structured cause"
tags:
  - "binaries"
  - "cause-vocabulary"
  - "reserved-causes"
  - "install-hint"
---

## The trap

`cli/exit_codes.py` reserves `install-binary`, `install-binary-source-unknown`,
`fix-binary-override` and `unsupported-platform`, and its comment says
`core.binaries.BinaryNotFound` "carries one of these four as its structured
cause". So the obvious refusal for a missing binary is one whose reason is
`exc.remedy.value`. It is not a declared reason. `core/cause.py`'s `REASONS`
does not hold any of the four, because they are canonical `Remedy` tokens that
the reservation table also keys on. `refuse()` raises `UnknownReason` for them.
A `Cause` built by hand around one gets past construction and still fails at
the envelope. Either way a person sees exit 1 and "report a defect" over a
program they only need to install. U80 hit it on its first drive.

## What to do instead

Follow `rclone-missing` (backup) and `encoder-missing` (mastering). Declare a
slug of the verb's own in `cause.REASONS` at `PRECONDITION`, for example
`yt-dlp-missing`. Raise it through `refuse()`, and pass the binaries module's
decision as the REMEDY, not as the reason:

    refuse("yt-dlp-missing", message,
           remedy=Remedy(exc.remedy.value),
           steps=(f"install ... with {hint.manager}",) if hint else (),
           detail={"binary": ..., "manager": ..., "packages": [...]})

Keeping `exc.remedy` as the remedy keeps the distinction the binaries module
drew: a broken override says fix the override, not install it again. Re-pin
`tests/test_reserved_causes.py` for the new slug. The population and the
non-reserved half each move by one and the reserved half stays put.
`acquire/fallback_cli.py:_binary_refusal` is the worked example, driven in
`tests/test_acquire_fallback.py` for both the install and the broken override
paths.
