---
title: Two of the rehearsal's guards kill no test, the refusal of owned hearts alone and the hold of a dangling link's name
found: at the review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** The review reverted four of the rehearsal's guards and found none killed a test. The fix round gave three of them a test each (the witness on the success path, the integrity check, the two read backs). The fourth, `--rehearse` on an empty staging folder whose pass holds owned hearts refusing by name rather than reaching the owned hearts' own write, has none, because building a pass with owned hearts is a fixture of its own. The second review found a fifth: the hold of a staged name the live batch folder carries as a dangling symbolic link (`is_symlink()` beside `exists()`) is handled, driven by hand, and pinned by no test.

**Measured cost.** Not driven. With the guard gone, the rehearsal would fall through to the owned hearts' path, which asks its explicit gate: the session is asked a live question it did not mean to ask, and nothing is written without an answer.

**Closes when:** a test of a dangling link in the live batch folder, and a test over the owned hearts fixture of `tests/test_favorites_backfill.py` drives `--rehearse` with an empty staging folder. Ledger only.
