---
title: Slice three of the test trimming is cut by a third of its share, since what is left is layout
found: at the build of #983, U334, 2026-11-24.
issue: no
---

**The mechanism.** #983 owed the 104 test files from `tests/test_label_playlists_kept.py` to `tests/test_restore_cli.py` a cut to at most 62,948 lines (16.4 percent of the 75,260 the range held at `55e958b`, four files having joined it since the brief's `d289f61`). Eight builders cut it from structure and prose to 71,653, 4.8 percent, with every test still running and every assertion kept: the groups reached 0.9, 5.95, 1.54, 1.28, 7.7, 2.95, 6.0 and 14.09 percent. Each measured why it stopped: docstrings were already one line, exact repetition inside a file is a few percent of logical lines, and a parametrize case costs two to four lines against the five to eight of the test it replaces, so folds of short tests break even. Of the 71,653 lines left, 14,219 are blank, about 6,000 of them the second of PEP 8's two between top level definitions, and several hundred are test signatures wrapped because the test's name is a sentence.

**Measured cost.** Point 5 of #847's definition of done stays unmet by 8,705 lines in this slice. No person using the verbs pays anything; the suite is as strong as before.

**Closes when:** the epic's audit decides what point 5's line bar should be measured against, or a card the audit files reaches it some other way. The question on #983 offered a blank line cut and a test rename card as options and took the recommended one, landing the gap named. Ledger only: maintainer facing.
