# R-154 and R-153, the mutation tables read together

Author run, 2026-09-19, on `relay/153`. Three tables, `r154-a.md`, `r154-b.md`
and `r154-c.md`, run as three FOREGROUND batches because a Relay session cannot
wait on a background job and one 25 row invocation can pass the 600 second tool
ceiling. Each batch took under four minutes. Every table is valid, every row's
restore was verified against HEAD, and each null control killed 0 of 9005
collected.

**25 rows, the cap, 25 killed. No zero.** That is the author's count and reads
as "the author could kill every row the author thought to write". The
independent tables in this repository's history found more than the author's
every time they were run.

Two rows kill only because the author saw the zero coming and wrote the test
first, which is said here so the 25 is not read as 25 guards that were covered
by the unit's first suite:

- `A1_stamp_pattern`. Nothing in the first suite carried a value the calendar
  parse accepts and the pattern refuses. `2026-8-01T000000Z` was added.
- `C3_hand_down_the_flag`. The window inside the second act could not be
  driven until the fake remote learned to change its answer after one listing.

## Considered and dropped at the cap

Ranked below the 25 because each is covered by a kept row one layer down, is a
report field rather than a guard, or guards an input a saved configuration
cannot produce. **None of these was measured.**

- The calendar half of the source system's spelling, `2026-02-30_123456`. A test
  asserts it. `A2` measures the same guard on this product's own spelling.
- The marker's normalization on WRITE. `A7` measures the read side, and the
  round trip test holds the two ends together.
- `plan_restore` forwarding `snapshot_volume` to the resolver. `C5` measures the
  same value one layer up, at the verb.
- The verb handing `accept_unrecorded` down. The offer refuses an unmarked
  newest snapshot before the engine is reached, so at the verb this guard is
  covered by another guard and would read zero. `B3` measures it at the engine,
  where it stands alone.
- The off-machine item reaching the gate as `shown`. Seven tests read it, and
  it is a display value.
- The unmarked snapshot warning at QUEUE time. `C6` measures the resume site,
  which is the run that writes the snapshot.
- `snapshot` and `recorded_volume` on the report's totals. One test reads them.
- The identity warning for a configuration with NO identity. A saved
  configuration refuses a missing `library.volume_id`, so only a configuration
  built in memory reaches it.
