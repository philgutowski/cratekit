---
title: Guards in the needs genre backlog that round two's mutation table left unpinned
found: at round two of the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** Round two ran 32 mutation rows over the fix round's guards in `tagging/backlog.py` and `backlog_cli.py` against `tests/test_tag_backlog.py`, and 19 survived. The unit's own table killed its 16 rows, so these survivors remain:
- `_fixed_target`'s own folder branch, which no shipped folder name reaches, since every one routes by keyword in another case, and its sub alias test;
- `not edit.writes` on the settled path, and `_edit`'s `TaxonomyError` catch;
- `alone` against `carrying` in the alias reach, and the exact case tests in the folder's row count;
- `follow` and `asked` in the campaign's last two steps;
- the joining row's route test and its check row, and the unread check row;
- `text=text` on the `--catalogue` branch of `_plan`, where every word would read `no-copy` with the flag and no test would notice;
- the Discogs `unasked` set copied from `suggest_cli`.

**Measured cost.** Unpinned behaviour, so a later change could break any of them with a green suite. None was driven to a wrong report by round two.

**Closes when:** each has a test that kills its mutant, `--catalogue`'s copy text first. Ledger only.
