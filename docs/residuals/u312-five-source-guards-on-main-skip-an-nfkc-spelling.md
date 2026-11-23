---
title: Five source guards on main skip a module whose text spells the guarded name only in a compatibility form
found: at the second review of #869, U312, 2026-11-23.
issue: no
---

**The mechanism.** A guard that parses only modules whose raw text contains
the name it hunts misses a module that spells the name in a form Python folds
by NFKC, a fullwidth letter for one, since the parser reads that identifier
as the ASCII name. U312 found and fixed four such prefilters it had added
itself; the second review found five that were already on `main`, outside the
branch's diff: `tests/test_analysis_store.py`, `tests/test_rb_writer_db.py`,
`tests/test_analysis_key_default.py`, `tests/test_write_session.py` and
`tests/test_gate_shown_plan.py`. Driven on the first: a planted call with the
keyword's first letter fullwidth passes the guard, and the ASCII spelling
fails it. It is the shape of the ledger's entry "The monkeypatch undo ban
reads only files whose text spells the call in ASCII, so an NFKC spelling
passes it", one guard family over.

**Measured cost.** Maintainer facing: the only producer is a deliberate
spelling, and no recorded mutation uses one.

**Closes when:** each of the five folds its text with
`unicodedata.normalize("NFKC", ...)` before the membership test, as
`tests/test_adapter_listing.py` does, with a planted fullwidth spelling shown
to fail each. Three of the five are in the write path's tests, so the card
that owns them closes it.
