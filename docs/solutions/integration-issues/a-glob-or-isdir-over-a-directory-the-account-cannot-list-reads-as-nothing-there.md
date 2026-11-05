---
title: "A glob or os.path.isdir over a directory the account cannot list reads as nothing there, not as unread"
date: 2026-11-05
category: integration-issues
module: "src/cratekit/intake/rotate.py, src/cratekit/core/session.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
tags: [unread-is-not-none, permissions, session-log, rotate, account-mirror]
applies_when:
  - "A reason, a report or a gate states that no record, file or folder exists"
  - "Code reads a directory with Path.glob, os.path.isdir, os.path.exists or Path.is_dir"
  - "A test runs on the cloud container, which runs as root"
symptoms:
  - "A batch with a landing record and a batch folder is named not recognised, with no record and no folder"
  - "A session scan answers no record and no unreadable one, and no warning fires"
---

# A glob or os.path.isdir over a directory the account cannot list reads as nothing there

## Problem

U214 put the rotation classifier's reason for an unrecognised INBOX playlist
on the account mirror's step ("no landing record names it, ..., and no batch
folder under the music folder carries its name"). Round two of its review
drove the classifier as an unprivileged account with the session log and then
the music folder closed to it: both statements came out false, with no
warning anywhere, and the batch dropped off the mirror.

## Cause

Neither read raises. `Path.glob` over a directory that cannot be listed
yields nothing, so `session.scan_log` returns no record and no unreadable one.
`os.path.isdir` swallows `PermissionError` from its stat and answers False, the
same as a folder that is not there. Absence was read as evidence of absence.

## What was done

`rotate.landings` asks `os.listdir` of the log once and records
`Landings.unlisted` when it exists and is refused; `rotate._batch_folder`
stats the folder and answers None, not False, on any refusal other than not
found. The reason then says which read was refused and that it may hold what
would recognise the playlist. `scan_log`'s own empty answer for its other
consumers is a residual filed by U214.

## How to test it here

The cloud container runs as root, which no file mode bars, so a chmod proves
nothing there. Refuse the one OS call for the one path in the test
(`tests/test_inbox_unmirrored.py`, `_refuse_under`), and keep a readable case
beside it so the plain wording is still pinned.
