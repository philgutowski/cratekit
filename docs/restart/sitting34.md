**Sitting 34, 2026-10-09, attended. The 207 native rows replaced, and
`rb_file_id` named.** The author needed playable tracks, so every native
row in INBOX was removed from the collection in rekordbox and its folder
dropped back from Finder: three playlists named for their folders, 164, 42
and 1, rekordbox's own rows, analysed with KEY unticked, one from each
folder loaded to a deck. `adopt apply` placed 196 on an equal digest. The
five emptied native playlists were left in place. Then `stat` named the
column: **`rb_file_id` is the file's inode number at import**, matched on
every row rekordbox made this month, stale or zero on rows it tolerates,
random on the rows it refuses, so U115 (#272) sets `st_ino` on the landed
file and `repair rows` writes it onto the rows that carry a random one (the
A8 row and the sampler rows remain). The record is `docs/cutover.md`
sitting 34, R-928 carries the finding, #272 a comment. **Owed, the
author's:** the review items, #178 lines 7, 8, 9, the twelve hand made
playlists in INBOX / Old, the five empty INBOX playlists.
