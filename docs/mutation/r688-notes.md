# Mutation notes: r688

Author's table, no independent verifier (METHOD, 2026-09-07). Fifteen rows,
well under the cap, so nothing was dropped.

The first measurement, on the fix round's head, had two rows that did not
kill:

- `V3_declined_envelope_drops_warning` was a zero on the full suite, 10155
  collected. No test read the abort answer's warnings. The abort answer is
  how a person reads a plan without applying it, so the zero was user facing.
  `test_a_declined_run_still_says_which_ratings_are_owed` was added in the
  second fix round, and it kills the row.
- `C1_rates_flag_ignored` was refused by the driver. Its `old` text ended
  partway through a line, so it matched nothing. The row was rewritten to
  replace the whole guard, and it kills.

The table in `r688.md` is the re-measurement after both changes, at the
branch head that carries the new test. Every row was run from scratch, and
all fifteen killed.
