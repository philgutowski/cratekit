---
title: A rerun of a pass lands its late files under a second playlist rather than the mirror
found: by U128 on `relay/295`, 2026-10-10, the conservative call on its rerun rule.
issue: no
---

**The mechanism.** A landing records each account playlist it mirrored with
the account's identifier and the pass. A later landing of the same pass, a
download that arrived late, holds only its new files for that playlist, so
nothing it owned is mirrored twice. But the late files land in a playlist of
their own under the next free name, `Sunset Warmup 2`, rather than joining
the mirror the first landing made, so the account playlist is whole across two
INBOX playlists and not in one. Adding to the first would mean finding it live
by identifier on the native medium and, on the bridge, writing an intake file
whose playlist of an imported name rekordbox merges or replaces, which no test
here can show.

**Measured cost.** Driven on the native medium in
`test_a_rerun_of_the_same_pass_adds_nothing_twice`: the late file is the only
member of `Sunset Warmup 2`. On the bridge a rerun of a pass is refused while
its intake file is unimported, and was not driven after an import.

**Closes when:** U130 keeps the two sides in step after the landing, or a
rerun adds to the recorded mirror when it is live. Ledger only, nothing is
lost and both playlists say what they hold.
