---
title: Three refusal origins name the package their module left
found: at review round one of #980, U331, 2026-11-23.
issue: no
---

**The mechanism.** U331 moved `analysis/check_cli.py` and `analysis/rekordbox_check.py` to `intake/`, and `core/rehearsal.py` to `intake/`. Their `_ORIGIN` tuples were kept as they were, `("analysis.check_cli",)`, `("analysis.rekordbox_check",)` and `("core", "rehearsal")`, since the card freezes what every verb prints, and the envelope prints the origin. Tests pin each one.

**Measured cost.** A refusal from `analyze check` or `intake land`'s rehearsal names a module path that no longer exists. A maintainer reading `cause.origin` looks in the wrong package. No user facing cost: the origin is a diagnostic field, and its text is what it always was.

**Closes when:** a card allowed to change printed output renames the three origins with their pinning tests. Ledger only.
