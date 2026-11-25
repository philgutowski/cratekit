---
title: crate started by the app inherits the app's controlling terminal when the app was started from one, so the session reads a person at a terminal
found: at the review of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `CrateRunner` sets standard input to the null device but cannot detach crate from the app's session, since Foundation's `Process` has no `setsid`. When the app is started from Terminal (as `swift run` does), crate's `has_controlling_terminal` in `cratekit.core.session` finds the terminal, so a gate answered through the app may be recorded as answered at the command line. The app started from Finder or as a login item has no terminal and is unaffected.

**Measured cost.** Argued from reading; not driven, since no container runs Swift and the app in U965 runs no gated verb.

**Closes when:** the gate card (the one gate view) starts crate in a new session, or passes the actor explicitly, and a test reads the recorded actor of a gate answered through the runner. Ledger only.
