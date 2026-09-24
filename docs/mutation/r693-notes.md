# Mutation notes: r693

Author's table, no independent verifier (METHOD, 2026-09-07). Twenty one
rows, under the cap, in two files so each foreground run stays under the
harness tool ceiling: `r693-a-rows.toml`, thirteen rows over the gate
layer's body in `cli/gates.py` and the adopt, repair and profile gates, and
`r693-b-rows.toml`, eight rows over the retag, outbound, favourites, sync
all and routing gates. Light pass, because the unit is a rendering on gates
that still hold their writes; the writes and their guards are tabled by the
units that built them.

**NOT MEASURED.** There is no `r693-a.md`, `r693-b.md` or JSON sidecar,
because the driver never got past its full baseline. Every row is
unmeasured, so the table says nothing about kills. The full suite was green
at the branch head, and each row names the tests written to kill it; every
row that reverts a gate to a digest alone is also caught by the sweep guard
in `tests/test_gate_shown_plan.py`, which is in every row's subset.

Why: a real `crate analyze vocals --recursive` job over the whole DJ library,
started from another session against the installed copy, was running for
the whole of this session. It writes one analysis artifact per track under
the application support directory's `jobs/analysis-artifacts/`, so the
watched root grew by 28 entries while the baseline ran and the driver's
state leak guard stopped the batch. That is the second shape in the
solutions entry on null control halts, a live job from the installed copy,
with the count growing rather than a log rewritten in place. The job's own
process was alive when the halt was read, and a whole library walk does not
end inside a session.

The watched roots follow `CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` on
the driver's own environment, so pointing them at an empty directory would
have let the table run. That was not done, for the reason R-692's notes
give: it switches off the only check for R-343's shape, and an unattended
session is the wrong place to decide a guard does not apply.

To measure it, with no cratekit job running from the installed copy:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/r693-a-rows.toml
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/r693-b-rows.toml

Candidates left out, and why:

- The sweep guard's allowance losing a file. That is an edit to the test,
  and the driver mutates `src`; the guard's own count check is what holds
  it.
- `_named` in `write/routing_cli.py` dropping the names. R-692's rows N1 to
  N4 already cover it and nothing in this unit touched it.
- The adopt resume rebuilding the plan from a different census than the
  first ask. The two share `current_plan`, so the row would be a change to
  the census reader, which is another unit's file.
