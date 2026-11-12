---
title: The window's verifier reads a lineless release's album off the retry ladder with no gone answer, so a withdrawn release a kept listing still lists fails the whole label
found: at the review of #777, R-1634, 2026-11-12.
issue: no
---

**The mechanism.** `TidalCatalogue.search_release`
(`src/cratekit/label/tidal_catalogue.py`) reads the album of a release whose
listed object carries no copyright line with a bare `self._session.album`,
off the retry ladder `_album` shares and with no answer for a release the
provider no longer has. A label's listing is kept seven days (U217), so a
release withdrawn inside that time is still listed; a lineless one is read,
the client raises its not found error, `LabelSource._verifier` turns it into
`run.LookupFailure`, and the label fails as one whose listing could not be
read. R-1634 gave the forced read, `reread_release`, a `gone` answer and a
next held release to read in its place; the window's own read has neither.

**Measured cost.** Driven by round two of R-1634's review (probes p4 and p5)
with the real client's not found error over a fake session: a new lineless
release withdrawn while the kept listing lists it, and in mismatch mode a
lineless withdrawn held release, each refuse the label as unlisted on
`label sync --next`, on the branch and on `main` alike, until the keep ages
out or its file is deleted. A live withdrawal inside a keep was not driven.

**Closes when:** `search_release` reads on the ladder and answers a release
the provider no longer has as dropped (`gone`) rather than raising, so one
withdrawn release costs that release and not the label. Ledger only: the
guide's remedy, deleting the kept listing, lists the label afresh.
