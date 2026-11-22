---
title: How the depth walk treats a truncated NODE open tag is pinned by no test, on the base and the branch alike
found: at the review of #859, U302, 2026-11-22.
issue: no
---

**The mechanism.** `rbxml._node_tokens`, which U302 folded out of
`depth_of` and `matching_close`, stops at an open tag with no end. Counting
that tag as a level before stopping changes only `depth_of`, and no test
fails: 90 passed under the mutation, and the base form in `depth_of`
survives the same mutation.

**Measured cost.** None driven: a document holding an unterminated open tag
inside the playlist section is one `playlists_span` and `node_at` already
read as unusable, so no writer reaches the depth it would misread.

**Closes when:** a test feeds the walk a truncated tag inside an otherwise
readable playlist section, if such a document can be produced. Ledger only.
