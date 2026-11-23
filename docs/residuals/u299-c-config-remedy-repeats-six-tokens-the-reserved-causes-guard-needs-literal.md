---
title: config.Remedy repeats six tokens of exit_codes.Remedy, and the reserved causes guard needs them written as literals
found: at the build of #856, U299, 2026-11-22.
issue: no
---

**The mechanism.** `core/config.py`'s `Remedy` declares six tokens that
`core/exit_codes.py`'s `Remedy` also declares, the one copied block of six
logical lines left inside U299's area (two windows of one block). Writing
config's members as `exit_codes.Remedy.X.value` removes the copy and keeps
every value, and was driven: `tests/test_reserved_causes.py`'s
`test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package`
then fails, because its static rule reads a cause shaped enum's values only
from string literals in the class body, and two pinned populations move. The
change was reverted, since that suite is another card's file.

**Measured cost.** None to a user. It leaves the area's duplication allowance
with this one block, against the card's target of none.

**Closes when:** the static enum rule resolves a member written as another
enum's value, after which config's six members read from exit_codes and the
allowance line goes; or the area keeps the copy as the declared subset it is.
Ledger only.
