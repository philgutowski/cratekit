---
title: A library whose live rows hold no majority ContentLink cannot land a file natively
found: at the build of #292, U126, 2026-10-10.
issue: no
---

**The mechanism.** The native landing gives each row it makes the
ContentLink more than half the library's live rows carry,
`row_link.library_link`, because the binding's own value keeps a row off a
deck (R-928). A library with no live rows, or whose rows split so that no
value is held by more than half, or whose majority is NULL or not a whole
number, refuses before the gate with `link-majority-unclear`. The landing
does not fall back to a plurality, which would be a guess about which value
rekordbox loads, and a wrong guess is a row nobody can play. What
ContentLink means is still unknown, so the conservative call is to refuse.

**Measured cost.** None on this library: 10,312 of 10,498 live rows carry
one value, measured on a read only copy on 2026-10-10. A new library, or
one rebuilt from an export, would have to land its first files through the
xml bridge or through rekordbox until its own rows carry a majority.

**Closes when:** what rekordbox derives ContentLink from is known, so the
value can be computed rather than copied. Ledger only.
