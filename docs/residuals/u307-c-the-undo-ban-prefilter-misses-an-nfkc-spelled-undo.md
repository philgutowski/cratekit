---
title: The monkeypatch undo ban reads only files whose text spells the call in ASCII, so an NFKC spelling passes it
found: at the round two review of #864, U307, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_isolation_survives_undo.py` bans a test that calls `monkeypatch.undo()`, which would undo the suite's isolation. U307 narrowed the files its syntax tree walk reads from every test file holding the text "undo" to those matching an ASCII regex (`_CALL`), for speed. Python folds identifiers with NFKC, so `ｍonkeypatch.undo()` (a fullwidth m) or `monkeypatch.ｕndo()` parses to the same attribute; the reviewer planted five files and the base ban flagged three of them, the branch's one. Neither version catches an aliased fixture (`mp = monkeypatch; mp.undo()`) or `pytest.MonkeyPatch().undo()`.

**Measured cost.** None to a person: no test in the repository spells the call that way, and the producer is contrived. The guard is narrower than it was.

**Closes when:** the prefilter folds the text with NFKC before matching, or the walk reads every file again, and a planted fullwidth spelling is refused by the ban's self check. Ledger only.
