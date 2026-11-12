---
title: Discogs asks with only the last bracket group stripped, and a title cut to one letter still matches any track
found: at the review of #673, U244, round two, 2026-11-12.
issue: no
---

**The mechanism.** Round one's fix asks Discogs with the title's last bracketed
group stripped, so "Foo (feat. X) (Extended Mix)" is asked as "Foo (feat. X)"
where it was "Foo", and "Foo (Bar (Baz) Remix)" is asked whole. And
`_discogs_title_matches` refuses only a title the shared strip empties: "A
(Warm Summer Night)" or a bare "I" strips to one letter, which is a substring
of most titles, so a release by the artist without the track matches. The
other way, "(Foo) Bar (feat. X) (Extended Mix)" misses its own track "(Foo)
Bar".

**Measured cost.** Driven at round two on recorded JSON over twenty titles.
Whether the live search answers such a track field with nothing, which would
make a Beatport miss read `no-hit`, or with releases lacking the track, was not
measured.

**Closes when:** the search asks with the shared strip wherever it leaves
something, and the matcher refuses a stripped title under a few letters, both
driven on the attended Discogs trial. Ledger only until measured.
