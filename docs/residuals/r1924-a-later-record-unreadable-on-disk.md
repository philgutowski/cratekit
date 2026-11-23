---
title: A restore skips a later session record it cannot read, and puts back no file that session wrote
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** `restore.plan` reads the title tag and key tag every later
session kept through `_later_started`, which borrows `session.records`, and
that reader drops a record it cannot parse ("a policy for reporting only, since
a gate that borrowed it would fail open"). `session.scan_log` returns the
unread half and nothing in the restore looks at it. `_later_committed`, which
decides the discard set, has the same shape on `main`.

**Measured cost.** Driven at review round two: an adopt stopped between its
files and its rows, its record then made unreadable three ways (truncated
JSON, a `state` this build does not know, the record removed), then `crate
restore run` of the landing before it. Exit 0, `ok`, `file_tags.planned 0`,
no warning, all five files still adopted, in three of three cases. No verb
was found that writes an unreadable record (`write_record` is atomic), so the
three were made by hand and the reachability is unmeasured.

**Closes when:** the restore reads the session log through a reader that
returns what it could not read, and a plan over a log with an unread record
says so, in the files' half and the discard set alike. Ledger only: no
shipped verb was driven to produce the input.
