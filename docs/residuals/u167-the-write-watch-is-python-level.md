---
title: analyze check's no write test watches Python opens and the bytes, and cannot see a C level create
found: at the review of #348, U167, 2026-10-31.
issue: no
---

**The mechanism.** `test_no_file_under_the_library_is_opened_for_writing`
patches `open`, `io.open` and `os.open` and compares the bytes of the database
and every analysis file before and after. A new file created under the library
by SQLite's own C code, which none of those patches sees, passes it. Two
guards in the analysis file walker are also layered so that each kills nothing
alone: the tag that overruns the file and the file whose stated length is not
its size are both caught by the other check.

**Measured cost.** None to a person: the branch makes no such write, which the
review confirmed by mutation (an UPDATE of the live database and a rewrite of
an analysis file both fail the test). Maintainer facing.

**Closes when:** the test also lists the library tree before and after, or is
left as is. Ledger only.
