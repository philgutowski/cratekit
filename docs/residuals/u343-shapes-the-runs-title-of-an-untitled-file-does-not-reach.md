---
title: The title analyze run gives a file with no title tag misses five shapes, each as main missed it
found: at review round two of #995, U343, 2026-11-23.
issue: no
---

**The mechanism.** Since review round one of U343, `analyze run` writes the
naming engine's headless title (the stem, a lossy marker set first) on a file
with no title tag, so `analyze adopt` can stamp the landed row
(`analysis/cli.py` `_untitled`). Round two drove five shapes it does not settle,
each behaving as origin/main does with its headed title:

1. A file the run does not measure, a name already carrying a head
   (`skipped-prefixed`) or one the detector cannot read (`skipped-undecodable`,
   a FLAC or M4A cut short), keeps no title tag; adopt leaves its row
   `title-tag-differs` on every pass, and the check counts it among the bare
   titles (the line says adopt names any it leaves).
2. A title the reader cannot read is overwritten by the stem: a FLAC whose
   first TITLE value is empty, an M4A whose title atom holds Latin 1 bytes.
3. An identifier stem (`92654769`) is titled with the identifier, so `name
   apply` composes `Artist - 92654769`, or holds a file with no artist as "not
   renamed to its title alone".
4. The library matcher misses a file with an artist tag and a title spelled
   `Artist - Title`, the title the stem gives (`acquire/match_library.py`).
5. `analyze run` pointed at a landed folder writes the stem as title onto a
   file the collection references, so its tag and its row disagree (main
   renamed such a file).

**Measured cost.** Driven on fixtures by the round two reviewer, every shape
identical on main but the fifth, where main's cost was larger. Whether a real
download or rekordbox produces the first four was not measured; nobody was
shown to point the run at a landed folder.

**Closes when:** each shape is given a title the landing lands (or is refused
by name), or recorded as accepted. Ledger only: no shape is new with U343.
