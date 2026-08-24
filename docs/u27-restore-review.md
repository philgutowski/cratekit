# U27 independent adversarial review: `e2dd532`, the two restore verbs

Verifier did not write the code. Worktree `<repo>/.worktrees/u27-restore`, own venv, own scratch.

## VERDICT: BLOCKING

Two findings meet all three conditions of the merge bar. Nine more are residuals.

| # | Finding | Class | Measured cost |
| --- | --- | --- | --- |
| 1 | A failed `rclone` restore exits OK and reports its transfers as done, after deleting the live sidecars | BLOCKING | live `master.db-wal` deleted, nothing restored, exit 0, `transfers: 2` |
| 2 | A capture the listing explains is reported to the person as a defect to file | BLOCKING | exit 1, `internal-error`, `report-defect`, produced by the tool's own `restore.prune` |
| 3 | The off machine half's snapshot is not in the digest, so the newest can move between the two acts | RESIDUAL | a different snapshot restored than the one current at approval |
| 4 | Nothing asserts the pulled snapshot belongs to this library, and `--snapshot` reaches rclone unvalidated | RESIDUAL | `..` in the stamp reaches the remote path verbatim |
| 5 | The new destructive command line surface has no command line coverage | RESIDUAL | 3 flags, 0 tests, cause of 11 of the 21 user facing zeros |
| 6 | `backup.RESTORE_WORKFLOW` never lands, so the log cannot tell a mirror pull from a capture restore | RESIDUAL | only `capture-restore` recorded, on all 3 paths |
| 7 | One X equals X assertion in the new suite | RESIDUAL | `tests/test_restore_cli.py:230` |
| 8 | Two of the eight new cause slugs duplicate the meaning of slugs already in the table | RESIDUAL | 2 pairs, same `ExitCode`, 2 slugs per fact |
| 9 | The offer the digest is taken over is never shown to the person | RESIDUAL | pre-existing at all 8 `gate.require` sites |
| 10 | "All nine conformance properties" is three | RESIDUAL | prose, measured by identifier diff |
| 11 | The author's mutation spec shipped with no measured results | RESIDUAL | process |

Claims that HOLD, measured: one lock acquisition on every path including the dry run and the refusal path; nothing to restore genuinely enters no gates and opens no session; all nine backup refusal slugs carry the same `ExitCode` in both tables; the countdown discharged in all three places and the collected count reconciles by identifier.

### Battery, from inside the worktree with its own venv

    ruff check src tests scripts          All checks passed, exit 0
    pytest --tb=no                        6182 passed, 1 skipped, 270.63s
    pytest --collect-only -o addopts=     6183 collected
    scan_repo.py                          exit 0, no output

Re-run after the mutation batch, to prove the tree was restored: 6182 passed, 1 skipped, 243.07s; ruff and `scan_repo` clean; `git diff HEAD -- src tests scripts` empty.

### Mutation table

`docs/mutation/u27-restore-cli-independent.toml` and `.md`. Full pass.

- Rows run: **45**, at the cap. 39 primary plus 6 composites.
- Rows dropped and logged in the spec's `[[dropped]]` block: **9**.
- Total deaths: **33**. Killed rows 19, collect-error rows 2 (both genuine deaths the driver flags conservatively because the parametrization count moved), zero rows **24** (21 user facing, 3 maintainer facing).
- Baseline green at 6183 collected. Null control killed 0 at 6183.
- The author's table is 28 rows and has no measured results in the repository. No row here repeats one of its rows. Independent gap: 45 against 28.

---

## Finding 1. A failed rclone restore reports success, and the live write ahead log is gone

**BLOCKING.**

`backup.run_restore` clears the live database's sidecars, then hands each command to a runner, and never reads the return code. `restore_under_one_session` then builds the report from the PLAN's command labels rather than from the results, and says so in a comment: "THE PLAN'S COMMANDS RATHER THAN THE RUNNER'S RESULTS". So a transfer that failed is reported as a transfer that happened.

Reproduction, through the real dispatcher, the real argument parser, the real two act gate flow, and a real `subprocess.run` against a real executable on disk. The only substitution is the external program. `CRATEKIT_BIN_RCLONE` is the shipped per binary override that `core.binaries.find` reads before PATH; it points at a script that answers `lsf` with one snapshot name and exits 1 on `copy`, which is what rclone does when the remote is unreachable, the token has expired, or the path is not there.

    crate --output json restore run --from-backup
    crate --output json run decide <run> restore.run.confirm restore --actor a-person
    crate --output json --run <run> restore run --from-backup

Measured:

    exit 0, outcome "ok"
    data.totals  {"transfers": 2, "steps": 0, "dry_run": false}
    data.items   two rows, each {"half": "off-machine", "transfer": "restore-database"}
    rclone argv  lsf remote:database-snapshots/ --dirs-only
                 copy remote:database-snapshots/2026-08-01T000000Z/db/master.db <lib>/db/
                 copy remote:database-snapshots/2026-08-01T000000Z/db/master.db-wal <lib>/db/
    live master.db-wal   DELETED
    live master.db       UNCHANGED

The tool deleted the live write ahead log, restored nothing, and told the person it had performed two transfers. Reconfirmed on the restored tree after the mutation batch, identical numbers.

**Why it is this commit's.** `backup.run_restore` had no caller in `src` on `origin/main`; the same grep over `e2dd532` finds one, in this module. This commit is what puts the function in front of a person.

**The checking path exists on the other half of the same module.** `backup.run_backup` reads `result.returncode != 0`, stops the portion, and records a failed outcome carrying the tail of stderr. `run_restore` has no such line. METHOD's third recurring pattern, a fix that lands on the performing path while the checking path stays open, and here the performing path is the one designed with care.

No test anywhere returns a nonzero `CommandResult` to `run_restore`. Every guard in `tests/modules/test_tools.py` and every drive in `tests/test_restore_cli.py` uses a runner returning 0.

**Bar.** Driven end to end. Cost is two of the four named: data lost, and a clean report over state the tool could not read. Producer driven, an external rclone exiting nonzero, supplied through a shipped configuration surface with no cratekit source modified.

## Finding 2. A capture the tool's own listing explains is reported as a defect to file

**BLOCKING.**

`_named` returns the listing row whatever its state. Its docstring says an unusable capture is deliberately left to the engine, "which is more specific than anything this layer could restate". Measured, it is not.

**The producer is cratekit itself.** `restore.prune`, the retention sweep, deletes an older capture while its session record stays in the log. Driven:

    restore.prune(cfg, policy=RetentionPolicy(keep=1, max_age=timedelta(0)), owning=second)
    PRUNE REMOVED: ['capture-one']

Then, through the real CLI:

    crate --output json restore list
      ROW ...-6008  restorable True   unusable ""
      ROW ...-2fc6  restorable False  unusable "<path>/capture.json could not be read..."

    crate --output json restore run <the pruned session>          exit 10, decision-required
    crate --output json run decide <run> restore.run.confirm restore --actor a-person
    crate --output json --run <run> restore run <the pruned session>

      exit 1
      cause.reason       "internal-error"
      cause.remediation  {"remedy": "report-defect", "steps": []}
      cause.message      "<path>/capture.json could not be read, so there is no record
                          of what this capture holds and nothing may be restored from
                          it: [Errno 2] No such file or directory: ..."

One command earlier, on the same library, the listing verb returned the sentence `Restorable.unusable` had already computed. The run verb throws it away and tells the person to file a bug against a state the tool produced on purpose and the module's own docstrings describe twice.

A session record is opened and closed ABANDONED before the refusal, so the refusal is not free. Measured: `RECORDS: [(..., 'closed'), (..., 'abandoned')]`.

**With `--from-backup` the cost compounds.** The mirror half runs FIRST, so the transfers complete and the sidecars are cleared before the plan refuses, and the report naming those transfers is never built, because `transferred` is assigned after the try block and the exception leaves the function. Measured on that path: `TRANSFERS THAT RAN BEFORE THE REFUSAL: ['restore-database', 'restore-database']`, then `internal-error`, `WAL STILL PRESENT: False`, and a refusal that says nothing about either.

**Bar.** Driven end to end through the real CLI. Cost is "told something false" and "blocked from a verb", with a remedy token that sends a person to a bug tracker. Producer driven, and it is the tool's own retention prune rather than a person with `rm`. The refusal itself is correct; the diagnosis is what is false, so the fix is small: `_named` already holds `entry.unusable` and can refuse with the sentence the listing prints.

## Finding 3. The off machine half's snapshot is not in the digest, and the newest moves

**RESIDUAL.**

`_offer` digests `snapshot or "newest"`. With no `--snapshot`, the digest carries the word rather than a stamp, so which snapshot will actually be pulled is not in it at all.

Driven end to end. Offer made and answered while the remote lists one snapshot; a second appears; the same command line is resumed.

    first drive   remote lists 2026-08-01T000000Z, digest 2773db78d299ff13
    decision recorded
    remote now lists 2026-08-01T000000Z and 2026-08-22T235959Z
    resumed       digest 2773db78d299ff13, UNCHANGED, decision honoured
    rclone argv   copy remote:database-snapshots/2026-08-22T235959Z/db/master.db ...

The producer is an ordinary backup, driven separately: `backup.plan_backup` on the same configuration emits `copy <db> remote:database-snapshots/2026-08-24T011841Z/db/ --transfers 4`, a new dated directory per run, so `latest_snapshot` returns a different name after any backup.

R-152 records the digest's general limitation but names a different missing case, a companion file appearing beside the database, and states that the off machine half IS in the digest. Which half is in it is true. Which snapshot is not.

RESIDUAL rather than blocking because nothing false was displayed: the offer never named a stamp, and "newest" is literally what was approved and what was delivered. The cost is real and narrow, a restore to a point the person did not choose, and it is worth extending R-152 rather than opening a new one.

## Finding 4. Nothing asserts the pulled snapshot belongs to this library

**RESIDUAL.**

`plan_restore` interpolates `--snapshot` into `f"{cfg.backup.db_dest_root}/{chosen}/db"` with no check that the stamp exists, parses, or names a snapshot taken from this library. When `--snapshot` is supplied, `latest_snapshot` is never called, so there is no listing either. Driven:

    crate restore run --from-backup --snapshot ../another-library-snapshots/2020-01-01T000000Z

    rclone argv  copy remote:database-snapshots/../another-library-snapshots/2020-01-01T000000Z/db/master.db <lib>/db/
    no lsf call, no refusal, exit 0, report says 2 transfers

The only thing tying a snapshot to a library is `cfg.backup.db_dest_root`, and a stamp that climbs out of it is accepted verbatim. RESIDUAL: the traversal needs a backend that resolves `..`, and the reported-as-success half is Finding 1 rather than a second cost. Recorded because a destructive verb interpolating an unvalidated argument into a remote path is worth naming even where the blast radius is bounded.

## Finding 5. The new destructive command line surface has no command line coverage

**RESIDUAL,** and it is the cause of eleven of the twenty one user facing zeros.

`--from-backup`, `--snapshot` and `--include-mirror` appear in no test in the repository.

    git grep -n -- "--from-backup|--snapshot|--include-mirror" e2dd532 -- tests/

returns one hit, and it is prose inside a docstring in `tests/test_write_session.py`. The three `from_backup=True` uses in `tests/test_restore_cli.py` are direct calls to `restore_under_one_session` with an injected runner, below argparse and below the dispatcher.

The mutation table measures the consequence. Eleven rows changed the off machine half in ways a person would meet, and every one killed zero on the full suite: the mirror forced on for every run (`I_B6`), `--include-mirror` defaulting on (`I_C3`), `--from-backup` silently ignored (`I_B4`), the named snapshot dropped (`I_B5`), `--snapshot` defaulting to the literal `"newest"` (`I_C5`), the target argument ignored (`I_A4`), and an unsupplied seam forwarded as `None`, which would make `crate restore run --from-backup` raise `TypeError` on an uncallable runner (`I_A1`). Composite `X1` removed the backup engine's own refusal for an unconfirmed restore and killed 3, all in `tests/modules/test_tools.py`, so the engine is held and only the verb's wiring to it is not.

## Finding 6. The workflow label the docstring says is preserved is never written

**RESIDUAL,** maintainer facing.

The module docstring says `core.restore.CAPTURE_RESTORE_WORKFLOW` and `backup.RESTORE_WORKFLOW` are "two different labels landing in one log field precisely so an rclone pull and a capture restore stay distinguishable afterwards". Because the verb injects `gates=held.guard`, `backup._restore_gates` returns the injected guard and never calls `session.assert_gates(workflow=RESTORE_WORKFLOW)`.

Measured with a spy on `session.assert_gates`, on a drive performing both halves:

    dry run, both halves      ACQUISITIONS: ['capture-restore']
    wet run, both halves      ACQUISITIONS: ['capture-restore']
    refusal path              ACQUISITIONS: ['capture-restore']

`backup-restore` never lands for a restore driven by this verb, which is the opposite of what the docstring says the constant buys. The same measurement is what proves Finding 1's counterpart claim, that the restore is one acquisition, so the two travel together.

## Finding 7. One X equals X assertion in the new suite

**RESIDUAL,** maintainer facing. AST walk over all 57 `assert` statements in `tests/test_restore_cli.py`.

    tests/test_restore_cli.py:230
    assert payload["totals"]["transfers"] == len(report.pulled)

Both sides derive from `report.pulled`, and `_performed` computes the left as `len(report.pulled)`. It survives any rewrite of `_performed` that keeps reading the same field, which is the only field it could read. Measured: row `I_A9` deduplicated the transfer labels, which changes what a person is shown, and killed 0.

## Finding 8. Two of the eight new cause slugs duplicate slugs already in the table

**RESIDUAL,** maintainer facing.

Every one of the nine `backup.Refusal` slugs carries the same `ExitCode` in `cause.REASONS` and in `cli.exit_codes.RESERVED_CAUSES`. That half of the commit's claim is verified by direct comparison of all nine. No duplicate KEYS exist either; an AST walk over every dict literal in `cause.py` and `cli/exit_codes.py` finds none.

The block's own comment notices one collision, `rekordbox-running`, and says it was already declared. It misses two:

    database-absent      LIBRARY_UNAVAILABLE   vs  library-database-missing   LIBRARY_UNAVAILABLE
    library-root-absent  LIBRARY_UNAVAILABLE   vs  library-directory-missing  LIBRARY_UNAVAILABLE

Each pair names one fact with two slugs, differing only in which module refused. Anything grouping by `reason` now has to know both spellings. `cause.REASONS` went from 108 to 116 entries.

## Finding 9. The offer the digest is taken over is never shown to the person

**RESIDUAL,** and pre-existing rather than this unit's.

On the DECISION_REQUIRED path `ctx.gate.require` raises before `ctx.envelope(data=offered)` is reached, so the offer is discarded. Measured text output:

    restore.run: blocked (DECISION_REQUIRED)
    Restore this session, discarding everything after it?
      gate:    restore.run.confirm
      options: restore, abort

and the JSON envelope's `data` is `{"checks": [], "summary": {}}`. The person is not shown the session, the change summary, the discard set, whether the mirror is being pulled, or which snapshot. Every one of those is in the digest they are approving. All eight `ctx.gate.require` call sites in `src` have this shape, so it belongs to the platform.

## Finding 10. "All nine conformance properties" is three

**RESIDUAL,** prose. Removing `planned_in` armed three parametrized properties per verb, measured by differencing collected identifiers:

    test_conformance_1_structured_output_is_actually_emitted
    test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two
    test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds

Six identifiers now mention `[restore.list]` and seven mention `[restore.run]`, against four and five before.

## Finding 11. The author's mutation spec shipped with no measured results

**RESIDUAL,** process. `docs/mutation/u27-restore-cli-author.toml` is in the commit; no `u27-restore-cli-author.md` or `.json` is. METHOD says to write the table into the repository with full row descriptions and not only counts. What is in the repository is the rows, not the measurement.

---

## The claims that hold, with their measurements

**Claim 1, one acquisition, on every path.** A spy on `session.assert_gates`, installed on the module attribute and on both importing modules, recorded exactly one acquisition on the dry run, on the wet run, and on the `remote-not-configured` refusal path, on drives that performed both halves. The `Held.guard` pass-through does what it says. Corroborated by `I_A3`, which dropped the platform seams from `recovery_session` and killed 2, and by the author's S1 and S2 rows on the same seam.

**Claim 2, nothing to restore opens no session.** Spies on both `session.assert_gates` and `session.open_session` recorded nothing, and `session.records(cfg)` was empty afterwards, on a library that had never acknowledged a backup. Exit 0, outcome `no_op`. Genuinely never entered, not entered and closed.

**Claim 5, the reserved statuses.** All nine refusal slugs carry the same `ExitCode` in both tables. The collision finding above is about meaning, not about codes.

**Claim 7, the countdown.** All three edits landed. `tests/_pending.PENDING` holds only `path:skills`, and the only surviving `@requires` decorator anywhere in `tests/` is `tests/test_skills_lint.py:411 @requires("path:skills")`. Collected count reconciled by identifier under `LC_ALL=C`, using `pytest --collect-only -o addopts=` with a collection plugin rather than `-q`: 6163 on `origin/main` at `6c4f12d`, 6183 here. Three identifiers lost, all of them the guards the discharge was meant to retire. Twenty three gained: sixteen in `tests/test_restore_cli.py`, one in `tests/test_write_session.py`, six conformance parametrizations.

## The strongest zero, reported as two counts

`I_E6` reversed the CLI's walk over the session listing, so a bare `crate restore run` would roll back to the OLDEST spendable session rather than the newest. Zero deaths on the full suite. Its composite `X3` moved the same property one layer down, reversing `list_sessions`'s own `reverse=True`: also zero deaths on the full suite. `I_E1` and `I_E5` derive "spendable" from `unusable` alone, dropping the capture-verified half, and their composite `X2` widened `Restorable.restorable` itself in `cratekit.core.restore`: zero as well.

So neither "newest first" nor "verified" is pinned anywhere in 6183 tests, at either layer. `test_a_bare_run_takes_the_newest_spendable_capture_and_not_merely_the_newest` cannot see it, because the only restorable session in that fixture is also the oldest, so newest-restorable and oldest-restorable are the same answer. This is a coverage finding rather than a defect: the shipped code is correct today. It is the one I would fix first after the two blockers, because the fix is one more session in an existing fixture.

## Suggested residual numbers

Next free on this branch is R-153. Findings 3 through 11 would take R-153 through R-161, except that Finding 3 reads better as an amendment to R-152 and Finding 9 belongs to the platform rather than to this unit.

## Artifacts

- `docs/mutation/u27-restore-cli-independent.toml`, 45 rows plus 9 logged drops
- `docs/mutation/u27-restore-cli-independent.md`, the measured table with full row descriptions, the per-row killed lists, and a verifier's note mapping the five zero families to their composites
- `docs/mutation/u27-restore-cli-independent.json`, the same numbers as data

The drive files used for the findings were written into `tests/`, run, and deleted; copies are in the verifier's scratch directory. `git diff HEAD -- src tests scripts` is empty.
