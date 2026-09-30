---
title: A slow rclone sync against Google Drive is the listing asked once per folder, not the comparison
date: 2026-09-29
category: integration-issues
module: "src/cratekit/modules/tools/backup.py"
problem_type: integration_issue
component: backup
root_cause: incorrect_assumption
resolution_type: code_fix
severity: medium
symptoms:
  - "A backup of a library that barely changed spends 35 to 55 minutes before and around a small transfer"
  - "The changes it will send are all logged in the first thirty seconds, then nothing for minutes"
  - "The checks counter advances at a steady rate that more checkers do not move"
  - "rclone lsf -R of the same remote finishes in about a minute"
applies_when:
  - "An rclone sync, copy or check against a cloud remote is slow however little changed"
  - "The remote is Google Drive or another remote whose requests are paced and whose listing is per folder by default"
  - "A brief attributes the time to the comparison and asks for more checkers or a narrower walk"
related_components:
  - "restore"
  - "doctor"
tags:
  - "rclone"
  - "google-drive"
  - "fast-list"
  - "backup"
  - "measure-first"
  - "r-757"
---

# A slow rclone sync against Google Drive is the listing asked once per folder, not the comparison

## Context

R-757 recorded that a backup of the library took most of an hour however
little had changed, and that where the time went had not been measured. The
brief for issue #226 named four candidates, the remote's recursive listing
option, more checkers, a comparison by size and modification time only, and a
walk limited to files changed since the last backup, and said to measure
before choosing. The library was assumed to hold about 10,000 files.

## What was measured

Read only, on the live volume and the live remote, 2026-09-29.

| Step | Time |
| --- | --- |
| `rclone lsf -R` of the volume | 1.5 s for 91,265 files in 22,433 folders |
| `rclone lsf -R` of the remote | 66 s and 139 s on two runs |
| the product's mirror, `--dry-run` | 18,774 of 91,235 files compared at 220 s, killed at 540 s |
| the same with 64 checkers | 37 files a second against 59 with 16, a burst then the same rate |
| the same with `--fast-list` | all 91,235 compared in 190 s, 48 to send |

The changes were all logged inside the first thirty seconds of the slow run.
What followed was the listing. `rclone sync` lists a remote one folder at a
time unless told otherwise, and Drive's request pacing allows about ten calls
a second, so 22,433 folders is most of forty minutes whatever the checkers are
set to. `rclone lsf -R` is fast because a recursive listing command already
uses the remote's recursive listing where the remote offers one; `sync` does
not unless `--fast-list` is passed.

## Why the other candidates were refused

More checkers add concurrency to a rate the remote sets, measured above. A
comparison by size alone skips a tag write that keeps the file's length, and
the brief forbids skipping a changed file. A walk limited by age never sees a
removal and skips a file copied in with an old date, since copies keep their
modification time. The local walk was 1.5 seconds, so nothing about the
volume was the cost.

## What was done

The mirror carries `--fast-list` by default and `crate backup run --full`
builds the command without it, the full mode being the absence of one option
so the two modes cannot drift in anything else. Both compare every file by
size and modification time, which is what every backup before this did.
`tests/test_backup_comparison.py` drives the real rclone between two temporary
folders, with `RCLONE_CONFIG` pointed at a temporary file declaring each
remote as an alias of a temporary folder, because the configuration refuses a
destination that is not spelled `remote:path`.

## What to carry forward

- Measure the listing separately from the comparison before attributing time
  to either. `rclone lsf -R` against the remote and against the volume, each
  timed, splits the question in two commands.
- A rehearsal of the product's own command with `--stats 20s -v --log-file`
  shows when the changes were found and how fast the checks advance. Killing
  it at a bound is harmless, it is a dry run.
- Between two local folders `--fast-list` is accepted and changes nothing, so
  a test there proves the two modes agree and proves nothing about the
  remote's recursive listing being complete. R-766 holds that for the
  attended sitting.
- The other rclone commands in the module, the restore's copy of the mirror,
  the share sync and the settings copy, still list folder by folder. R-768.
