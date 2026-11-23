---
title: Sync ends U304 short of its line, code line and test targets, so a further card is owed for the audit
found: at the record of #861, U304, 2026-11-22.
issue: no
---

**The mechanism.** U304 split `sync/pair_cli.py` (5,785 lines) into seven modules under 1,500 lines, emptied sync's duplication allowance, cut its import allowance to one line, and shortened the prose of the package and its 27 test files to each rule and its reason. It did not simplify the code: the split adds an import block to each new module and a re-export block to `pair_cli`, and every guard's text was kept in place so the kill set replays row for row. Measured on the final head against `c9192091`: source lines 16,703 to 15,352 (target 12,574); code lines 11,066 to 11,095, up, where Phillip's answer on #847 asks every card for 15 percent fewer; test lines 21,897 to 21,323 (target 15,374); the suites' summed test time is not cut. The brief's targets were measured at `ff8e5ec`, before `removed.py` and `unavailable.py` landed.

**Measured cost.** None to a person: behaviour is unchanged. The cost is point 2 and point 5 of #847's definition of done, which the final audit (#872) measures.

**Closes when:** a later card simplifies sync's code itself (the longest functions are `plan_pair`, `check`, `sync_pair` and `_warnings`), anchoring each kill row it moves, and trims the suites where one test's kills are covered by another. Ledger only: #847's audit files a further area card for a point that falls short.
