---
title: U250's test helper patches single readers no routing test reads, and its energy failure no longer chains its cause
found: at the review of #679, U250, 2026-11-12.
issue: no
---

**The mechanism.** Two small things round two of the review measured and the
two round cap left. `serve_readings` in `tests/_readings.py` serves each field
at `tags.read_tags` and also patches the matching single field reader, "so a
path that reads one field alone sees the same fake"; removing those side
patches kills no test in `tests/test_routing_workers.py` or
`tests/test_export_collection.py`, since every served read there comes through
`read_truth` (272 of 272 calls). And `tags.read_energy_checked` now raises
`TagReadFailed` for a stored energy that is not a number without
`from exc`, so the exception carries no `ValueError` as its `__cause__`; its
three callers discard it, and its message, which only a debug line shows, is
identical to main's and pinned by no test.

**Measured cost.** None: 98 inputs over five containers read, raise and word
identically to main; only `__cause__` differs, and nothing reads it.

**Closes when:** the side patches are dropped or a test reads one, and the raise
chains its cause again. Ledger only.
