---
title: The brief's live check names sync all --report, which does not exist, so the strip's last proof is read off the next ordinary sync pass
found: at the build of #671, U242, 2026-11-12.
issue: no
---

**The mechanism.** U242's verification says to finish the live strip with "a
`sync all --report` offers none of them". `crate sync all` takes only
`--export` and `--favorites-playlist`; it has no report only mode, so a run
of it queues whatever it finds new. The attended card's step reads the proof
off the next ordinary pass instead, its `data.summary.playlists` block
excluding each stripped playlist as `already-swept`.

**Measured cost.** None to the account or the library; the check is one pass
later than the brief asked. The offering rule itself is driven on fakes in
`tests/test_u242_taken.py`.

**Closes when:** `sync all` gains a report only mode, or the attended sitting
reads the check off its next pass. Ledger only.
