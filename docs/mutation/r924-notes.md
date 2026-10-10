# r924 mutation notes

Author's table, 22 rows, one pass, measured on head a9a57be. 19 killed, 3
zero, each zero promoted to the full suite of 12847. The author ran it, so a
zero reads as "the author could not kill it".

The unit writes and deletes nothing: it adds lines on standard error and a
watcher thread that reads a scratch folder. The table is scoped to the new
guards, and each zero gets one line.

- **D4_unflushed, zero.** The suite drives the dispatcher over StringIO,
  which has no buffer to hold a line, so `flush=True` is invisible to it.
  User facing in principle (a line held until the verb ends). A composite
  needs a real pipe and a child process and was not built. Recorded as
  unmeasured, not covered.
- **F6_watcher_without_progress, zero, test fixed after the table.** The
  JSON test shortened the watcher interval to 0.01 s. With the guard removed,
  the watcher calls None on its first tick and dies with a TypeError before
  the fake looks for it, so the test passed over a watcher that should never
  have started. The test now runs at the shipped interval. The fix landed
  after this one pass, so the driver has not re-measured the row (METHOD
  allows one pass per unit per session).
- **F7_interval_halved, zero.** A cadence constant that no test pins, by
  design, because a test at fifteen seconds would be a fifteen second test.
  Maintainer facing.
