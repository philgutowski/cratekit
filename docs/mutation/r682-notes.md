# R-682 mutation notes

**Verdict: measured, 15 rows in one batch, every row killed.** Written on
`relay/209`, 2026-09-24, by the author, so a kill here is the author's.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r682-a` | 15 | 15 | 0 |

## What the rows cover

- **M1 to M6, the summary.** `by_reason` dropped from the summary, a `why`
  that is not a string counted, an empty `why` counted, the state keys not
  seeded, each row counted twice, and a reason counted before the state word
  is checked.
- **M7 to M15, the rendering.** The line never printed, the reasons in slug
  order only, the tie break dropped, the unstated shortfall never said, the
  shortfall bound made inclusive, a bool accepted as a count, a zero count
  printed, and each of the two mapping gates removed.

M9, the tie break, was a zero before the table ran: the render test held its
reasons in slug order already, so a sort without the tie break printed the same
line. The test's mapping was reordered in `dd4fe68`, before the batch, and M9
kills 1.

## The leak guard

The first attempt stopped during the full baseline with 29 new entries under
the real installation root, all in `jobs/analysis-artifacts` and
`jobs/queue.db-wal`, the paths the installed copy's `analyze vocals` job
writes. The batch was rerun with `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR`
pointed at an empty temporary root, removed afterwards with `rmdir`, so it held
nothing. Every child still ran in the driver's own sandbox. Around the batch
the real root was fingerprinted by path, size, mtime and inode, plus a content
hash of every file at or under 64 KiB, leaving out only
`jobs/analysis-artifacts`, `jobs/analysis-staging` and `jobs/queue.db*`. The
digest over 1,617 files was identical before and after.
