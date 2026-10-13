# U143 mutation table, notes

Twenty four rows over the unit's own guards, measured by `scripts/mutate.py`
on macOS at `e89727ce`, the rows commit over `207e20b`, in five
batches (`u143-a` to `u143-e`) so each batch could finish inside the session
tool's ten minute ceiling. Batch a took 13.5 minutes and was moved to a
tracked background job by the harness; b to e ran as one tracked background
job, waited on in the foreground. Every baseline green at 13,918 collected,
every null control 0 of 13,918, every restore verified against `git show HEAD`.

**23 killed, 1 zero.** The author ran it, so a zero means only that the author
could not kill it.

- **R4_no_downloaded, zero, user facing.** The check that a label folder holds
  a `DOWNLOADED` playlist. With it gone, the held track set is empty, so every
  debris track reads as missing and the row is still left, with the missing
  track reason instead of the folder's. The outcome, debris left, is held by
  the missing track check, R1, which killed. So the guard's only effect is its
  reason, and the test asserted a substring both reasons share ("no
  DOWNLOADED playlist"). After the table the test was tightened to the
  folder's own wording ("folder holds no DOWNLOADED playlist"). That
  tightening was not measured again by the driver; it is read off the two
  message texts, one of which carries the phrase and the other does not.

Dropped below the cap, each logged in `u143-e-rows.toml`: the apply's order of
moves before removals, the part way failure's message wording, and the gate's
`deletes` line.
