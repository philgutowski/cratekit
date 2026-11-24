---
title: No battery check holds the 1,500 line bar on a source file, and two files sit within eight lines of passing it
found: at the build of #977, U328, 2026-11-23.
issue: no
---

**The mechanism.** Point 2 of #847, U290, asks that no source file under
`src/cratekit` outside `_vendor` pass 1,500 lines. The measure,
`scripts/refactor_measure.py lines --files`, prints the files over it, and
nothing in the battery runs that reading: `cli/registry.py` stood at 2,459
lines and then 2,544 under a green suite until an audit measured it. U328
split the registry and added a test that holds the registry and its parts to
the bar (`tests/test_cli_contract.py`), and holds no other file, since a check
over every source file would redden cards building beside it.

**Measured cost.** None to a person using a verb. On the head U328 merged,
`core/review.py` is 1,495 lines and `cli/setup.py` 1,493, so six more lines
on the first or eight on the second pass the bar with the suite green, and
the next audit of #847 finds point 2 short again. The next four are `intake/native.py` 1,438,
`modules/tools/backup.py` 1,429, `core/cause.py` 1,419 and
`label/sync_cli.py` 1,409.

**Closes when:** a battery test fails on any file under `src/cratekit`
outside `_vendor` over `LARGE_FILE`, landed when no card that grows one of
the two files is building, or the audit card of #847 decides the bar is read
at audits only. Ledger only: a maintainer facing count.
