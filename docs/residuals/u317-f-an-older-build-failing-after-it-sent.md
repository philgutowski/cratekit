---
title: A run of a build before U317 that sends and then fails does not strike the record's token, so this installation's record may be trusted over a mirror it changed
found: at the round two review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** Since round two a U317 run strikes the files record's
token from the library's fact before it sends, so a failed run of any U317
installation leaves no record trusted. A build before U317 knows no token: its
completed run publishes a fact without one, which is caught, and its failed
run publishes nothing, which leaves the token in place.

**Measured cost.** One candidate driven at round two, the build on `main` on
one state directory, and it did not produce a wrong skip: the next run was
full. Which write removed the token there was not measured. It needs an older
build to send, fail, and the library to be put back before the next run.

**Closes when:** every installation runs U317 or later, which the next
release and its installed copy close. Ledger only.
