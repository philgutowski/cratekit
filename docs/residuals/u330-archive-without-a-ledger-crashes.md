---
title: board.py residuals --archive with no ledger file ends in a traceback, where every other residuals command refuses or reads it as empty
found: at the build of #979, U330, 2026-11-23.
issue: no
---

**The mechanism.** `cmd_residuals` calls `archive_ledger()` for `--archive` with no check that `docs/residual-findings.md` exists, and `archive_ledger` reads it with `read_text`, so a checkout without the working file raises `FileNotFoundError` out of `main`, which catches only `Fail`. `--search` refuses the same state with a one line `board:` message and exit 2, and the listing and `--check` read it as empty.

**Measured cost.** Driven in U330's capture harness on a fixture with the ledger deleted: exit 1 and a Python traceback, identical on the base and the branch. Nothing is written. Maintainer facing only, since every checkout of the repository carries the ledger; no producer of a missing working file was found among the commands.

**Closes when:** `--archive` refuses a missing ledger the way `--search` does, with a test. Ledger only.
