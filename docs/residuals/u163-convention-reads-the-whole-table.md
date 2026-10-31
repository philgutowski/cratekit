---
title: The SearchStr convention reads every artist and album row once per plan and again per apply
found: at the review of #344, U163, 2026-10-31.
issue: no
---

**The mechanism.** `native.search_convention` walks the whole of `djmdArtist`
or `djmdAlbum` the first time a plan mints in it, and `_assert_words_unmoved`
builds a fresh resolver at the apply, which walks it again.

**Measured cost.** Unmeasured on the live library, about ten thousand artist
rows; probably under a second per walk.

**Closes when:** a landing on the live library is timed and the walk is either
cached on the plan or shown to cost nothing worth caching. Ledger only.
