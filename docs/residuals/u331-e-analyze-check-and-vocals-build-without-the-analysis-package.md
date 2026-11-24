---
title: analyze check and analyze vocals build without the analysis package and cannot run without it
found: at review round one of #980, U331, 2026-11-23.
issue: no
---

**The mechanism.** U331 made both verbs build with the `analysis` toggle's homes blocked by importing their analysis helpers at call time: `intake/rekordbox_check.py` takes `cratekit.analysis.agreement` inside the two functions that read it, and `vocals/cli.py` takes `cratekit.analysis.cli` and the loader's module inside the functions that call them. So rule four and the drive of each toggle off read both verbs as built. A run that reaches those functions still imports the package.

**Measured cost.** Not driven against a real install: no profile removes the analysis package's source, which every install ships, so no producer of a missing package was found. A toggle off hides the package from the import rules' drive, not from the interpreter.

**Closes when:** the helpers both verbs borrow move to a package no toggle owns, or the rules read a call time import of a toggle's home as a dependency of the verb. Ledger only.
