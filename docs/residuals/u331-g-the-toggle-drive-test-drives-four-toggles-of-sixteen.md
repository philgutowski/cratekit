---
title: The toggle drive test drives four hand listed toggles of sixteen
found: at review round two of #980, U331, 2026-11-24.
issue: no
---

**The mechanism.** `tests/test_import_rules.py::test_with_a_toggle_off_every_remaining_verb_builds_and_formats_its_help` blocks the homes of four toggles it lists by hand, builds every remaining verb and formats its help, in a fresh interpreter. The other twelve toggles are read by the static rule alone, which follows top level imports. An import only a run makes, `importlib.import_module("cratekit.label.cli")` at the top of `sync/cli.py`, leaves the test green with `labels` off; the same line naming `cratekit.vocals.cli` fails it.

**Measured cost.** Maintainer facing. A verb left dangling by a dynamic import under one of the twelve toggles passes the suite. Round two found no producer in the tree: the static reading and a drive of every toggle both read 0. Driving all sixteen takes 25.8 s against about 8 s for the four, over METHOD's ten second bar for a test.

**Closes when:** every toggle is driven in a time under that bar, or `refactor_measure.py imports --drive` runs in the battery. Ledger only.
