---
title: Two names behind a toggle are served by a module __getattr__, so they leave __all__, dir() and resolved type hints
found: at the review of #866, U309, 2026-11-22.
issue: no
---

**The mechanism.** Moving organize's and the outbound source's top level imports behind their toggles left two names served lazily: `organize/inspiration.py` answers `PREFIX` and `modules/outbound/source.py` answers `library_export` through a module `__getattr__`. Attribute access, `from ... import` and `monkeypatch.setattr` all work, and the patch `tests/test_outbound_workers.py` makes on `source.library_export.read_export_file` still bites. But `PREFIX` left `inspiration.__all__` (ruff refuses a name there that is not bound at top level), neither name is in `dir()`, `typing.get_type_hints(source.Library)` raises `NameError` where the base resolved it, and patching `inspiration.PREFIX` no longer changes `account_sets`' message, which reads `MARK_PREFIX` itself. `organize/mirror_edits.Change` also gained defaults for `path` through `energy` that the base required.

**Measured cost.** None a person sees: nothing outside the card's files uses any of these, and `inspiration.PREFIX`'s one user is the card's own test.

**Closes when:** `inspiration.PREFIX` is dropped in favour of `folders.MARK_PREFIX` at its one test, and `source.Library`'s annotation names its type under `TYPE_CHECKING` only. Ledger only.
