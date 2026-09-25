# R-668 mutation notes

**Verdict: measured, 12 rows over two batches, every row killed.** Written on
`relay/208`, 2026-09-24, by the author, so a kill here is the author's.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r668-a` | 12 | 10 | 2 |
| `r668-b` | 2 | 2 | 0 |

`r668-b` is `r668-a`'s two zero rows, M8 and M12, measured again after a test
was written for each. The row text is identical in both batches.

## What the rows cover

- **M1 and M2, the surface.** The list positional required again, which is
  sitting 7's defect exactly, and the resume argv carrying the list again,
  which is also the "drive it with" line the queueing half prints.
- **M3 to M5, the head of the verb.** The empty `--job` guard removed, the
  missing list guard removed, and the missing list guard moved after the
  configuration read.
- **M6 to M12, the list named beside `--job`.** The check removed, the
  identity compared as strings, the named path not absolutised, another verb's
  job read, the check moved after the sweep and the reconcile, the empty frozen
  list skip removed, and the home expansion fallback raising.

## The two zeros in `r668-a`, and what closed them

- **M8, the named path not absolutised.** Killed nothing while the frozen list
  is on disk, because `samefile` resolves a relative spelling against the
  working directory and answers for it alone. The absolutising matters once the
  file is gone, when the filesystem cannot answer and only the string equality
  can. `test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`
  drives that, and M8 kills 1 in `r668-b`.
- **M12, the home expansion fallback.** No test named an unknown home.
  `test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name` does,
  and M12 kills 1 in `r668-b`.

M11, the empty frozen list skip, is marked maintainer facing, since only a job
queued by a build before U54 carries no list, and it was killed on the full
suite rather than the subset.

## What the batches did not see

- **The real installation state was not the watched root.** The installed
  copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8` was still writing
  `jobs/` under the real root, and the first attempt stopped on that with 36
  new entries during the full baseline, before any row. Both batches were
  rerun with `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR` pointed at an empty
  temporary root, removed afterwards with `rmdir`, so it held nothing. Every
  child still ran in the driver's own sandbox. Around `r668-a` the real root
  was fingerprinted by path, size, mtime and inode, plus a content hash of
  every file at or under 64 KiB, leaving out only `jobs/analysis-artifacts`,
  `jobs/analysis-staging` and `jobs/queue.db*`, the paths the live job writes.
  The digest was identical before and after.
