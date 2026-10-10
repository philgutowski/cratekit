---
title: Nothing numbers a landed residual file on its own, and the lane instructions still name the old places
found: building #287, U124, 2026-10-09.
issue: no
---

**The mechanism.** `board.py residuals --land` numbers a residual file on
main, and nothing runs it: the Relay runner merges a task's branch with its
residual files unnumbered, and the post cycle landing hook and the watcher
are outside this repository. Two instruction surfaces outside it also still
tell a builder to write a paragraph at the head of `RESTART-cratekit.md` and
number residuals in the ledger: the board-lanes skill in the agent-config
repository, and the Grokbot standing instructions on #279, which only the
watcher edits by adding a version. A builder following either writes the
paragraph `scan_repo.py` now refuses, so its branch fails the battery
rather than conflicting.

**Measured cost.** Files wait on main until somebody numbers them;
`board.py audit` names them on every run, so they are seen. A builder
following the old instructions is refused by the scan with the remedy in
the message, and loses one fix round.

**Closes when:** the watcher's landing runs `board.py residuals --land`
after each merge that carries a residual file, and both instruction
surfaces say `docs/restart/<unit>.md` and `docs/residuals/<unit>-<slug>.md`.
Ledger only, it closes in an attended session; the follow up card filed by
this unit carries it.
