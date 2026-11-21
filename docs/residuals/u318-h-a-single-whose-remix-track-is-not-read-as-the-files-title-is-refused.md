---
title: A Discogs single whose track writes the file's mix in full is refused when that track is not read as the file's own title or artist
found: at the review of #882, U318, round two, 2026-11-21.
issue: no
---

**The mechanism.** Since round one the single fallback counts another
track only when it is the mix alone, so a single "Two Months Off" whose
track "Two Months Off (Tim Green Remix)" is credited to a name sharing none
with the file's artist, or written "Two Months Off, Pt. 1 (Tim Green
Remix)", "The Two Months Off (...)" or "... (Tim Green Remix) - Bonus
Track", which the matcher does not read as the file's title, is refused.
The note then says the release holds no track with the version while a
track writes it.

**Measured cost.** Round two drove 24 track shapes by 7 file spellings:
the credited track and 8 of 44 full row spellings lost against main. Hand
built; whether Discogs credits a single's remix track that way is
unmeasured. The cost is a miss with a note false on its face.

**Closes when:** the fallback reads a track writing the full title and
mix by the release's credit, without reading another title's remix
(round one's finding 6). Ledger only.
