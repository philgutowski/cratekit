---
title: "A test that counts index reads across two walks must age its files, or the window answers every line"
date: 2026-11-12
category: workflow-issues
module: "src/cratekit/acquire/match.py _read_from_disk, src/cratekit/core/tags.py read_tags_noting, tests/test_library_reads_remembered.py"
problem_type: workflow_issue
component: library_index
severity: medium
root_cause: convention_not_visible_in_code
resolution_type: test_fix
applies_when:
  - "A test indexes the same library twice in one process and counts opens, or patches a tag reader between the walks"
  - "A test changes a fixture file between two index walks and expects the second to see the change"
  - "A test needs a FLAC fixture's size to change after a tag write"
tags: [library-index, match, memo, mtime, fixtures, flac, padding, u249]
---

# A test that counts index reads across two walks must age its files

## What U249 changed

Since U249 the library index reader, `match._read_from_disk`, remembers each
file's `Owned` for the life of the process, keyed on the path, the name
template and the file's size, modification time, change time, inode and
device. A remembered file is answered only when its modification time is at
least two seconds older than the moment the entry was made, which is the FAT
volume's step.

## The traps

- **A fresh fixture is never answered from memory.** A file written by the
  test a moment ago is inside the window, so two walks open it twice and a
  test meant to prove the memory passes against code with no memory at all.
  Set the file's times back, `os.utime(path, ns=(old, old))` with `old` an
  hour ago, as `tests/test_library_reads_remembered.py` does. To pin the
  window itself, hold `match._now_ns` rather than reading the wall clock twice.
- **An aged fixture IS answered from memory.** A test that ages its files
  (or copies an old fixture with `shutil.copy2`, which keeps the time) and
  then patches `tags.read_tags_noting`, `tags.read_tags` or `mutagen.File`
  between two walks sees the first walk's answer, because nothing on the disk
  changed. Call `match.reset_cache()` between the walks, or change the file.
  The suite clears the memory around every test (`_forget_library_reads` in
  `tests/conftest.py`), never inside one.
- **A tag write need not change a FLAC's size.** ffmpeg writes about 8 KB of
  padding into a FLAC, and mutagen spends the padding before it grows the
  file: an 8,000 character tag left an 8,430 byte fixture at 8,430 bytes. A
  test that needs a new size writes about 20,000 characters, and asserts the
  size moved before it relies on it.
- **Change time moves on every write and every `os.utime`** on APFS and
  Linux, so a test that means to isolate one stamp field wraps
  `match._stamp_of` and holds the others still.
