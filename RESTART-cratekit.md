# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-08, U58 on `relay/76`, taken from the board as issue
#76 and run as relay task 76.** Five commits of the unit already existed on
the local branch `u58/pre-relay-76`, built by relay task 76's first run on
2026-09-07 and ended by a session limit while it was writing the record. This
session fast forwarded them onto `relay/76`, then did what that record still
owed: the built in review ran again over the whole diff against main from
eight angles, fourteen of its findings held and were fixed with a test each
that fails on the tree before the fix, the rest are R-283 through R-288 with
amendments to R-216, R-248 and R-278, one learning is filed, and this file is
rewritten. The mutation table was measured on the first run and stands; the
second fix round did not re-run it, by the brief's instruction, and the
table's zero row note says which change it does not cover. **The pending
register is still EMPTY.**

**BOTH ANALYSIS WORKERS RUN, AND BOTH ENGINE DEFECTS ARE FIXED.** `crate
analyze run` and `crate analyze restamp` queue their folder's audio filenames
as items and drive each through `cratekit.analysis.cli.handle_run` and
`handle_restamp`, bound under their own names in `src/cratekit/cli/handlers.py`.
The vocal pass no longer reads a `wav` key nothing set: the partial carries a
path and `vocals.analyse` decodes it at the model's rate of 32000 through a
bound decoder, so a fake model driven through the path yields a nonzero level
and the model's gender call. Energy is computed by the source system's method,
a fixed feature vector z scored against a library calibration and mapped to a
level by nine decile cuts with a beatless cap, from the samples the head
already decoded; without a calibration the level is an honest None with
`energy_status` saying why, and the worker writes no `energylevel` tag for
it, so routing reads the taxonomy's no energy sink. `crate analyze calibrate`
is real and writes both state files; `crate analyze validate` says plainly
that no scorer ships. **The vocals side moved, not the light pass**, for two
reasons that each stand alone: the head decodes at 22050 and the model was
trained at 32000, and a partial carrying samples would hold every track's
audio in the parent across the pool boundary. `analysis/vocals.py`'s docstring
carries both.

**R-203 IS DOWN TO SEVEN.** `acquire.download`, `delete.review`,
`intake.playlist`, `intake.set`, `rebuild`, `route.resort` and `sync.all`.
The title still says eighteen deliberately; `tests/test_handlers.py` derives
the population from `registry.ENTRIES` and is what fails when a queued verb
is in neither table.

**THAT HAS NOT CHANGED ABOUT WHO DOES U29.** Issue 29 is attended, Phillip's to
perform against the live library one workflow at a time, which an agent cannot
touch by standing constraint. METHOD's do-not-touch section says so and the
reason does not expire. **`board.py next` will say "Take #29" and you must not.**

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite on `main` before this merge was **6928 passed and 1
skipped**. The last measured suite on `relay/76` was **6946 passed and 1
skipped**, on the second fix round's commit, which is the commit before the
record that rewrote this file; the record touched documents only. **Main's
highest residual is R-288 once this branch merges**, no duplicate headings,
no heading deleted. Append only, and gaps are fine.

**The board: 61 units, 53 done, 8 ready, 0 blocked, and `board.py audit`
exits 1 on purpose.** Four drift items. #78 and #79, U60 and U61, are on the
tracker and not on the board, the operator's to add. #70 is Done on the
tracker and still In review on the board, which `sync` would repair. #76 is
In review, a status `board.py` does not preserve across a recomputation, so
`sync` would flip it back to Ready while the relay runner still owns its
merge; R-265 records that. Do not run `sync` to make the audit green while
#76 is under review.

## Read this before touching analysis again

**THE RESUME READS A RENAME INTENT, NEVER THE FOLDER.** The item is the pre
rename filename and the finalize renames the file inside the handler, before
the engine flips the row, so a kill in that window leaves a finished file
under its head and a pending row under its old name. The finalize writes
`rename-intent.json` into the item's staging directory immediately before the
rename, and `_finalized_twin` reads that and nothing else. The first version
scanned the folder for a headed file whose stripped stem equalled the item,
which reported a deleted source as analysed when an older twin sat beside it
and missed every file the naming template deduped or truncated. The learning
is filed at `docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`
and applies to every remaining R-203 worker, all of which move files.

**THE TEST FOR A KILL DIES IN THE WINDOW.** `kill_after_the_rename` in
`tests/test_analysis_workers.py` raises a `BaseException` subclass out of the
staging call on the first finalized report, because `jobs.drive` converts
`Exception` at the item boundary and a kill is not one. A test that renames
the file by hand is a test of the hand rename, and that is what hid both
defects above through a green suite and a killed mutation row.

**THE HEAVY STACK STAYS BEHIND THE EXTRA, AND SO DOES NUMPY.** Every librosa,
torch and model touch is a lazy import inside a function.
`analysis/cli.py` never imports `analysis/vocal.py` at module scope, because
`cli.jobs.argv_for` imports the verb module by name to build a resume line
and the model module needs numpy at import time, which the slim profile does
not declare. `test_the_analysis_package_imports_with_the_heavy_stack_blocked`
runs a fresh interpreter with all five blocked. The model is behind the
separate `vocals` extra while the registry declares `analysis` for the verb,
so a run on a machine with one and not the other finalizes every track with
no vocal tags; the resume envelope now warns, counting them, and R-277 says
those tracks are never scored again until `analyze.vocals` lands.

**ONE TEMPO METHOD ON BOTH PATHS.** `energy.features_from_samples` measures
its own tempo from the central slice on every path, and the head decodes at
`energy.MEASURE_RATE`. The first version handed the head's whole track
integer tempo down on the run path and measured its own on the restamp path,
so one file scored through the two verbs carried two tempo readings against
one calibration. The window difference that remains is R-287.

**A KEBAB LITERAL IS A PINNED POPULATION.** Two joined this round,
`skipped-unanalysable` and `vocal-inference-failed`, and the pin in
`tests/test_reserved_causes.py` moved by two, differenced as sets against
main's tree extracted into a scratch directory. Any new kebab shaped string
in `src` moves it again and the re-pin names what joined.

## What U58 left behind, beyond the code

Fifteen residuals, R-274 through R-288, nine from the first review and six
from the second, plus amendments to R-133, R-203, R-216, R-248 and R-278.
Five are worth knowing before touching analysis again:

- **R-276.** The vocal calibration is written and nothing reads it.
  `cli/converge.py` passes `vocal_threshold=None` with a comment saying so.
  The reader belongs to U53's routing and rebuild workers.
- **R-277.** A track finalized while the model was unavailable is never
  scored again, because the head in its name is the resume marker and the
  re-score verb is the planned one.
- **R-283.** The restamp has no rename recovery, and the intent cannot give
  it one, because its file is renamed by another job.
- **R-285.** The detector seam carries state the worker has to recognise: a
  shadow binding, a per item calibration re-read, and two tempo keys.
- **R-278, R-286, R-287.** Every efficiency number in these is the reviewer's
  estimate and none was taken on the tree.

## What is open

| issue | unit | state |
|---|---|---|
| #76 | U58, the analysis workers | In review on `relay/76`, the relay runner owns the merge |
| #78 | U60, the deletion pass | On the tracker, not yet on the board |
| #79 | U61, `crate sync all` composes the source increments | On the tracker, not yet on the board |
| #71 | U53, routing and rebuild workers | Ready |
| #72 | U54, the acquisition worker | Ready |
| #75 | U57, the recognition identifier | Ready |
| #77 | U59, land the conformance branch | Ready |
| #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**Next is `#72`, U54**, per METHOD's serialized order, once U58 is merged.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch. A worker that
   moves files reads the rename intent entry before it binds.

## The branches

| branch | state |
|---|---|
| `relay/76` | U58, in review, the relay runner merges it |
| `u58/pre-relay-76` | U58's first five commits, local only, fully contained in `relay/76`; delete after the merge |
| `u52/pre-relay-70` | U52's pre relay branch, local only, merged through `relay/70`; delete |
| `fix/conformance-3-and-soft-delete-reader` | U59's input, in `.worktrees/conformance`, far behind main |

## What U52 left behind, beyond the code

Seventeen residuals, R-257 through R-273, and an amendment to R-248 for the
fifth copy of the resume tail. Four are worth knowing before touching labels
again:

- **R-258.** No catalogue adapter ships. Every label verb resolves to a constant
  refusal and the test substitution carries R-226's limit: the in process
  callers pick up a replaced `resolve`, and the child a resume spawns inherits
  nothing.
- **R-259 and R-137.** The labels path applies no ownership filtering at all,
  because nothing on it produces an owned identity set.
- **R-263.** A successful labels sweep still reads as "never ran" in
  `crate doctor`, because R-140's fix stopped the watermark and the reader was
  not told.
- **R-267 and R-268.** `bound()` and `resolve()` are two constants that must
  move together the day an adapter lands.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
