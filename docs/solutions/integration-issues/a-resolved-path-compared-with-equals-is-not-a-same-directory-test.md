---
title: A resolved path compared with equals is not a same-directory test
date: 2026-09-18
category: integration-issues
module: "src/cratekit/session/restore_cli.py"
problem_type: integration_issue
component: restore
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A guard refuses the library root and accepts the same directory typed in another case"
  - "Path.resolve does not fold case, so two spellings of one directory stay two strings"
  - "is_relative_to answers about a string prefix, so a differently cased ancestor reads as unrelated"
  - "The suite is green and the mutation row for the guard kills, because every test spells the path one way"
  - "A restore aimed at a scratch directory clears the live write-ahead log, which is in no capture by construction"
applies_when:
  - "A guard decides whether two paths are the same place, or whether one is inside the other"
  - "A path comes from a person's command line and is compared against configuration"
  - "The property is about a place on the disk rather than about a string"
related_components:
  - "backup"
  - "write_session"
tags:
  - "paths"
  - "case-insensitive"
  - "guard-bypass"
  - "green-suite"
  - "restore"
  - "macos"
---

# A resolved path compared with equals is not a same-directory test

## Context

R-368 added `--target` to `crate restore run`, a database restore into a
directory that is not the live library, so that a person can rehearse a restore
before they need one. The whole safety of the flag is two refusals: the target
must not be the library root, hold it, or sit inside it, and the place
`backup.database_target_for` would put the database must not be the live
database.

Both were written the obvious way, and the obvious way is wrong:

```python
resolved = Path(raw).expanduser().resolve()
root = Path(cfg.library.root).resolve()
if resolved == root or resolved.is_relative_to(root) or root.is_relative_to(resolved):
```

`resolve()` reads as "make this comparable". It does resolve symlinks, `..`
segments and a relative path against the working directory, all of which the
guard needs. It does not fold case, because case folding is not a property of
the path, it is a property of the filesystem the path sits on. So `==` and
`is_relative_to` are still string comparisons, and they answer that
`/Volumes/LIBRARY` and `/Volumes/library` are two unrelated directories.

On this product's own platforms they are one directory. macOS ships APFS case
insensitive, and the external drive a DJ library normally lives on is
frequently exFAT, which is case insensitive as well. The guard therefore
refused the spelling in the config and accepted every other spelling of the
same place.

## What it cost

Driven through the real dispatcher with the shipped fake-rclone seam, on a
target spelled `LIBRARY` where the configuration said `library`: exit 0, the
`rclone copy` pointed at the live database's own directory, and the live
`master.db-wal` unlinked. `run_restore` clears the companion files beside the
database it is about to replace, and the write-ahead log holds transactions
committed since the last checkpoint, which are in no capture by construction.
A rehearsal a person ran to find out whether their restore works would destroy
the one piece of their library no backup holds.

The suite was green before and after, and the mutation row that deletes the
guard entirely killed two tests. Both facts are true and neither one is
evidence: every test spelled the path the same way the configuration did, so
the guard was being measured against the only input that could not defeat it.

## The fix

Ask the filesystem instead of comparing the names.

```python
def _same_place(one: Path, other: Path) -> bool:
    try:
        return one.samefile(other)
    except OSError:
        return one == other
```

`samefile` stats both paths and compares device and inode, so it answers about
the place. It needs both to exist, which is why the fallback is there rather
than an error, and the fallback is sound here for a reason worth stating: a
path that does not exist cannot be a directory the live library occupies, and
on the very filesystems this is for, a case folded spelling of a directory that
exists also exists, so the stat succeeds in exactly the case the guard is for.

Containment needs one more step. A prefix match cannot see a differently cased
ANCESTOR, so the candidate's own ancestors are asked one at a time:

```python
def _holds_or_is(root: Path, place: Path) -> bool:
    if place == root or place.is_relative_to(root):
        return True
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))
```

The string test stays as the first question. It needs nothing to exist, it is
the cheap answer on the common path, and it is the whole answer on a case
sensitive filesystem.

## What the tests have to do differently

A test written for this cannot assert the refusal unconditionally, because on a
case sensitive volume the two spellings really are two directories and refusing
would be naming the wrong fact. Nor can it be skipped there, which would make
the property invisible on the machine it happens not to hold on. It probes the
directory it is about to use, by making `Case_Probe` and asking whether
`case_probe` is a directory, and flips its expectation on the answer. The probe
is of the VOLUME rather than of `sys.platform`, because macOS can be formatted
either way and the library usually lives on a drive formatted by something
else.

## The general shape

Three questions about paths look alike and are not:

1. Is this the same STRING, which is `==`, and is about spelling.
2. Is this the same PATH after symlinks and relative segments, which is
   `resolve()` followed by `==`, and is still about spelling.
3. Is this the same PLACE, which is `samefile`, and is the only one of the
   three that asks the filesystem anything.

A guard whose failure is destructive wants the third. Reach for `resolve()` and
`==` and you have written the second while believing you wrote the third, and
nothing about the code says so.

A note on the surrounding fix, because it is the same lesson pointed the other
way. Once `samefile` is in place the `resolve()` no longer carries the
comparison at all: `samefile` stats a relative path against the working
directory and answers correctly without it. The mutation row that removed the
resolution therefore killed nothing, which is not a sign the resolution is
dead. What it still carries is the REPORT, the absolute directory the refusal
echoes back to the person, and that is what its test now asserts.
