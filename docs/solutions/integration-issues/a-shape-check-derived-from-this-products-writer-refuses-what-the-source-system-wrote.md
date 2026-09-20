---
title: A shape check derived from this product's writer refuses what the source system wrote
date: 2026-09-19
category: integration-issues
module: "src/cratekit/modules/tools/backup.py"
problem_type: integration_issue
component: snapshot_restore
root_cause: incomplete_input_model
resolution_type: code_fix
severity: high
symptoms:
  - "A validation on a name read back from shared storage is written as the inverse of the function that writes that name"
  - "Every test passes, because every fixture was written by the same author from the same function"
  - "On the day of a cutover the restore reports no snapshot available over a remote full of them, and refuses each one by name as malformed"
applies_when:
  - "A guard validates the name of a file, a folder or a key that lives somewhere the source system also writes"
  - "The guard is derived from this product's own writer, by pattern, by parse, or by a round trip test holding the two together"
  - "The guard also filters a listing, so what it refuses is hidden as well as refused"
tags:
  - "backup"
  - "restore"
  - "snapshot"
  - "validation"
  - "cutover"
  - "source-system"
  - "r154"
---

# A shape check derived from this product's writer refuses what the source system wrote

## Context

A restore put whatever `--snapshot` held straight into a remote path. The fix
refused any value that was not the dated folder name a backup writes, checked
against `backup.stamp_for` by pattern and by a calendar parse, and a test held
the two ends together so the check could never drift from the writer. The same
check filtered the listing that picks the newest snapshot, so a stray folder
could not be offered as one. Green suite, clean mutation rows.

The built in review read `DJ_tools/src/dj_tools/DJ_backup/backup.sh` and found
the source system names its dated folder `2026-08-01_123456`: local time, an
underscore, no zone letter. It writes the same `<root>/<name>/db/` layout, and a
cutover points this product at the same remote directory. So on the first day,
every snapshot a person owns was refused by name as malformed, and because the
listing used the same check, `restore run --from-backup` said no snapshot
existed. On main, before the fix, naming one of them worked.

## Why the suite could not see it

The round trip test is the trap, not the defence. "Everything the writer
produces passes the check" is true and is half the contract. The other half is
"everything that is ALREADY THERE passes the check", and nothing in a repository
describes what is already there. Every fixture in the suite was a stamp typed by
the person who had just read `stamp_for`.

## How to apply it

- Before validating a name that lives in shared storage, a remote, the library
  volume, a state directory the source system also used, find the source
  system's writer of that name and read its format. `git grep` in `DJ_tools`
  for the directory or the key, not for the function.
- Say what the check is FOR and hold it to that. This one exists so a value
  reaching a remote path is a name and never a path. Two spellings of a dated
  folder are both names. `is_stamp` stayed the narrow statement of what a backup
  writes, and `is_snapshot_name` is what is enforced.
- When the same check filters a listing, ask what disappears. A refusal is
  visible. A filtered listing is a product saying nothing is there.
- An older artifact will usually lack whatever the new guard reads. Decide what
  that absence means on purpose: here an unmarked snapshot is never the default
  and is pulled only when it is named.
