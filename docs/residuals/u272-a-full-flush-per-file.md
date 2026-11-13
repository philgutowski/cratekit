---
title: A capture asks the drive for a full flush once per file and per directory, and falls back to the plain sync without a word
found: at the review of #701, U272, 2026-11-13.
issue: no
---

**The mechanism.** `snapshot._flush` calls `config.flush_to_disk` on every file
and every directory of a capture, deepest first, then the store, and the
capture directory and the store again after the manifest: ten calls for the
suite's fixture capture. On macOS each is `F_FULLFSYNC`, which empties the
drive's whole write cache, so a plain sync per file followed by one full flush
at the end would give the same guarantee for less. Where a filesystem answers
that it has no full flush, `flush_to_disk` takes the plain sync, the strongest
flush it has, and says nothing, so a restore point on such a drive is weaker
than on the Mac's own disk with no line in any log saying so.

**Measured cost.** Not driven: the container has no full flush to ask for. The
seconds one flushed capture of the real database costs on the library's drive
are owed on the Mac as an attended card, and the same sitting answers whether
a directory flush there returns an error outside the unsupported set, which
would refuse every guarded write.

**Closes when:** the Mac measurement is in, and if it is more than a second
or two, the per file flushes become plain syncs with one full flush last; and
the fallback logs once per capture. Ledger only.
