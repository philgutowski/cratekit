# U305's own table, notes

`docs/mutation/u305.md`, measured at `83e891d1`, its full baseline read from
the battery's verdict for that commit.

- **M5 reads collect-error, and is killed by hand.** Dropping `Wanted` from
  `match`'s re-exports makes every test module that names `match.Wanted` at
  import fail to collect, 673 of 673 in its subset. A mutation that stops the
  suite loading is caught, so the row is read as killed; the count is the
  driver's.
- **M3 was promoted to the full suite**, where it killed 3.
- **No row covers the registry's local imports in `plan` and
  `_seller_warnings`.** They feed only the `labels.empty()` branch for a
  `None` registry, which no caller passes; removing either fails no test
  (review round one and two drove both). M6 and M7 cover the two that carry
  a kill.
