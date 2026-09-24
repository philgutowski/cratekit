# Mutation notes: r691

Author's table, no independent verifier (METHOD, 2026-09-07). Sixteen rows,
well under the cap. Light pass, because the unit moves the derivation from
after the gate to before it and renders the result; the write itself is
unchanged and its guards are the ones R-318, R-316 and U89 already tabled.

Two candidate rows were left out on purpose, and why:

- A `setdefault` turned into an assignment when the plan names a file's
  destination. One energy placement per file is all the derivation produces,
  so the two spellings give one answer on every fixture this suite has, and
  the row would be a zero that says nothing about the guard.
- The per source derivation cache returning a stale tuple. One registry
  source exists, so a second tree would derive the same tuple with or without
  the cache. Maintainer facing, and unmeasurable until a second source exists.

The first measurement halted on the driver's state leak guard during the null
control, before any row ran. The real installation state gained one file,
`runs/2026-09-24T20:31:40Z-e763.json`, a `status` run record with no decisions
and no offers. No test in the subset runs `status`, and every child ran under
the sandbox, so the write was another process on the machine polling the
installed copy, not a child of the driver. The count was stable afterwards and
the rerun measured every row. The table in `r691.md` is that rerun, at the
branch head that carries the review round.
