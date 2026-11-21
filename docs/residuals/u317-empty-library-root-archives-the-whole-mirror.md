---
title: A backup over an empty library root moves the whole mirror into its dated archive, quick or full, with no check that the root is the library
found: at the build of #877, U317, 2026-11-21.
issue: yes
---

**The mechanism.** `_plan_files` refuses only a library root that is not a
directory. An empty directory at the configured root, the mount point a lost or
unmounted drive can leave, is walked as a library with no files. A full check
then runs `rclone sync` from it, which moves every file on the mirror into the
run's dated archive, and since U317 a quick run of a library under
`QUICK_LIMIT` files plans the same thing as one `rclone move` of every path. The
archive rotation at a keep of one purges that folder at the second completed
run after it. U317 did not make this reachable; it was the full sync's
behaviour before, and the quick run inherits it rather than adding a guard of
its own.

**Measured cost.** Driven on a local alias remote only: a library whose files
were all removed after a completed backup plans a quick run whose archive list
is every path. Not driven against a real empty mount point or the live remote.

**Closes when:** the files portion refuses, before any transfer, a root that
does not carry this library's identity (the volume identity assertion the
restore gates already use), or one whose walk is empty while the last record
held files. It earns an issue because a guard on a path that deletes from the
backup is absent.
