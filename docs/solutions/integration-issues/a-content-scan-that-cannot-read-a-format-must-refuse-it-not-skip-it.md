---
title: A content scan that cannot read a format must refuse it, not skip it
date: 2026-09-10
category: integration-issues
module: "scripts/scan_repo.py"
problem_type: integration_issue
component: secret_scan
root_cause: missing_validation
resolution_type: code_fix
severity: high
symptoms:
  - "The scan reports a tracked archive as clean because its content reader returns None for anything binary"
  - "A credential inside a .tar.gz or .zip is invisible to the scan even though the file is tracked"
  - "The residual's mitigation only catches a credential store carried in by a credential-shaped filename, not one carried inside an opaque container under an ordinary name"
applies_when:
  - "A repo-hygiene or secret scan reads file content and treats an unreadable file as skip-and-move-on"
  - "A new binary container format (archive, database file, compiled blob) can be tracked without the scan noticing it cannot inspect it"
tags:
  - "secret-scan"
  - "archive-detection"
  - "fail-closed"
  - "r3"
  - "r334"
---

# A content scan that cannot read a format must refuse it, not skip it

## Context

`scripts/scan_repo.py`'s content reader returns `None` for any file it treats
as binary (images, audio, compiled artifacts, and archives were all in the same
`BINARY_SUFFIXES` set). The scan loop then moved on as though the file were
clean. For an image that is correct: there is nothing to find. For an archive
it is not, because a `.tar.gz` or `.zip` can hold a credential file and the
scan has no way to see it. R-3 recorded this as a residual because the actual
incident was concrete: a downloader artifact vendored into the tree sat in the
same directory as a live session cache, an env file, and a web token, all of
which would have been invisible if bundled into an archive.

## The fix

Archives got pulled out of "skip silently" and into their own check,
`archive_violations`, that runs before the content read and REFUSES a tracked
archive outright rather than reporting it clean. Detection is suffix first,
then magic bytes at the offset each format's own extractor reads (zip's
`PK\x03\x04`, gzip's `\x1f\x8b`, tar's `ustar` at offset 257, and so on), so a
renamed archive is still caught. The message tells the author what to do
instead: commit the tree unpacked with its provenance recorded, which is
exactly how the vendoring unit (U13) already closes R-3's stated condition.

The built-in review during this same unit ran a `.tar.lz4` holding a session
file through the scan and it came back clean anyway: no listed suffix, no
listed magic. `git show 09a9c8d` adds eight more formats (lz4, Unix compress,
lzip, ar/deb, rpm, cpio, cab) found by the same method. The list is still
closed by construction, not exhaustive, and that limit is recorded as a
residual rather than treated as fixed.

## What to do next time

- When a scanner's content reader can return "I could not read this," that
  return value must not be treated as "this is clean." Skip-on-unreadable is
  fail-open; a repo-hygiene or secret scan needs fail-closed, i.e. refuse
  anything it cannot actually inspect.
- A closed list of magic bytes is real coverage but never total coverage.
  Treat a new binary container format as a candidate for the refuse list
  before assuming the existing skip behavior is safe for it. R-334 is the
  live example: the same skip-as-clean gap exists for database files
  (`.db`, `.sqlite`), left open with the choice deferred to a decision about
  scope rather than folded into this unit silently.
- Prove new formats against the scan the way this unit did: construct a
  minimal file of that format and confirm the scan refuses it, rather than
  reasoning about the header from documentation alone.
