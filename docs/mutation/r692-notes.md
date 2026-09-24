# Mutation notes: r692

Author's table, no independent verifier (METHOD, 2026-09-07). Thirteen rows,
well under the cap, in `r692-rows.toml`. Light pass, because the unit is a
rendering on a gate that still holds the write: eight rows over the gate's
naming in `write/routing_cli.py`, five over the screen's quoting in
`cli/render.py`.

**NOT MEASURED.** There is no `r692.md` and no `r692.json`, because the driver
never got past its null control. Every row is unmeasured, so the table says
nothing about kills. The full suite was green at the branch head, and each
row names the test that was written to kill it.

Why: a real `crate sync labels` job, started from another session against the
installed copy, was running for the whole of this session. It held the job
queue under the application support directory open, and its write ahead log
changed on every child the driver started. The first attempt halted with the
entry count up by one, a `job.show` run record with no decisions and no
offers, the poll the solutions entry on null control halts describes. The
second halted with the count unchanged and the queue's log rewritten. Two
bounded waits, 560 seconds each, found the job's process still alive.

The watched roots follow `CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` on the
driver's own environment, so pointing them at an empty directory would have
let the table run. That was not done: it switches off the only check for
R-343's shape, and an unattended session is the wrong place to decide a
guard does not apply.

To measure it, with no cratekit job running from the installed copy:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/r692-rows.toml

Candidates left out, and why:

- The artist read from another row, the review's version of the uniform
  fixture finding. It is no single edit to `plan_export`, and the fixture now
  gives each track its own artist, so rows N3 and N4 cover a lookup that reads
  the wrong attribute.
- The quoting applied to a non string value. No carried value that is not a
  string holds a comma or an equals sign, so the row would be a zero that
  says nothing about the guard.
