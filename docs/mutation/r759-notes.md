# R-759 mutation notes

Author's table, no independent verifier (METHOD, 2026-09-07). Every zero row
would read "the author could not kill it"; there are none.

## What was mutated

Nothing in `src/` changed on this branch. The unit rewrote two tests, so
every row mutates the code those tests guard and names the rewritten test
alone as its subset: a death is that test's, not a fake clock test's.

- `r759.md`, table a, eight distinct mutations, eight killed.
  - P1 to P3 and P6 on the interval, against
    `test_two_processes_keep_the_interval_between_every_call`: the interval
    dropped, halved, measured from now, and the wait skipped while the stamp
    still reads the due time. P6 is the shape the built in review raised:
    stamps spaced correctly and requests sent back to back. It is killed by
    the send start bound, not by the stamp chain.
  - P4 and P5 on the lock, against
    `test_two_processes_never_have_a_call_in_flight_together`: the lock
    never taken, and taken shared.
  - A1 and A2 on the adoption read deadline, against
    `test_the_deadline_ends_a_read_that_keeps_arriving_forever`: asked only
    once the stream has ended, and honoured a second late.
- `r759-b.md`, table b, P4 repeated ten times: **killed 10 of 10.** It is
  the one row whose death rests on real timing, since two processes have to
  race into a call still in flight. The interval rows are not repeated:
  after the rewrite their deaths are comparisons of the gate's own stamps
  and hold by construction. A first version of table b also repeated P2 ten
  times, 10 of 10, and was cut when the review pointed out the repeat
  measured nothing.

Eighteen row runs across the two tables, eight distinct mutations, under the
cap of 25.

## Load, measured

The brief's scenario, run by `/tmp` scripts that start the full suite in a
second process, relaunch it if it finishes first, and stop it in a `finally`:

| Run | What | Load average | Result |
|---|---|---|---|
| 1 | the three rewritten tests, 20 runs, first version | 3.4 to 12.1 | 20 of 20 passed |
| 2 | the old test, from `main`, 20 runs | 11.5 to 15.4 | 20 of 20 passed |
| 3 | the three rewritten tests, 20 runs, after the review fixes | 7.0 to 11.0 | 20 of 20 passed |

Run 2 is the honest part: this harness did NOT reproduce the old test's
failure in twenty runs, so runs 1 and 3 alone show the new tests pass under
load and do not show the old one fails under it. The mechanism was measured
separately instead. Two real processes through one gate at a fifty
millisecond interval, forty trials beside the full suite at load 13.3,
recording both the gate's stamp and the send's start:

- the delay from stamp to send start varied by up to 13.57 milliseconds
  within one trial, median 0.67;
- the smallest gap between send starts was 40.70 milliseconds, under the
  old test's floor of 45, so the old assertion would have failed that trial;
- the smallest gap between the gate's stamps was 50.11 milliseconds.

The state file write between the stamp and the send is fsynced, by
`config.atomic_write_bytes`, which is where the variable delay sits.
