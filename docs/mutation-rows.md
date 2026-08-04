# Mutation rows

Each row below is ONE exact textual substitution in ONE file. Apply it, run the
suite, count the failures, revert. A row is written down so that a later reader
can re-run it by id and get the same number, which is the whole reason this file
exists: two mutation tables have already been lost in this build because they
were reported in a message and never written into the repository, and a verifier
then had to reconstruct rows from prose before it could check a single count.

**A count with no row definition beside it is not evidence.** It is a claim about
an experiment nobody else can perform.

## Running a row

`pyproject.toml` already sets `addopts = "-q"`, so a second `-q` on the command
line becomes `-qq` and SUPPRESSES THE SUMMARY LINE ENTIRELY. Use:

    .venv/bin/python -m pytest --tb=no          # counts
    .venv/bin/python -m pytest --collect-only -o addopts=   # collected count

Revert by restoring the file from a snapshot taken BEFORE the row was applied,
not with `git checkout`, because a fix round's own edits are uncommitted while
the rows are being measured and `git checkout` throws them away with the
mutation. That mistake was made and caught during round 7.

Rows are measured against the WHOLE suite unless the row says otherwise, because
a row that kills only inside its own file is a row whose blast radius nobody
looked at.

---

## Round 7

**Baseline: 3308 passed, 16 skipped.** Measured on branch
`unit/u32-restore-retention-and-reconciliation` at `80771aa` plus round 7's three
findings, 2026-08-04. Every number in this section was measured, none is derived.

| id | file | measured kills |
| --- | --- | --- |
| `SN_raise` | `core/restore.py` | 1 |
| `SN_empty` | `core/restore.py` | 2 |
| `W1_shared_filter` | `tests/test_cli_contract.py` | 1 |
| `W2_drop_guard` | `tests/test_cli_contract.py` | 0, and argued below |
| `W3_disagree_filter` | `tests/test_cli_contract.py` | 0, and argued below |
| `W4_registry_side` | `cli/registry.py` | 93 whole suite, 1 targeted |
| `W5_pending_side` | `tests/_pending.py` | collection error, 0 tests run |
| `N1_preflight_call` | `core/restore.py` | 3 |
| `N3_slug` | `core/restore.py` | 6 |
| `N6_resting_read` | `core/restore.py` | 1 |
| `PF_skip_dry` | `core/restore.py` | 1, at the rehearsal assertion |
| `PF_only_dry` | `core/restore.py` | 1, at the half done assertion |
| `N14_rehearsal_block` | `tests/test_restore.py` | 1 |
| `N1_preflight_call` and `N14_rehearsal_block` together | both | 3 |

### The row definitions

**`SN_raise`.** In `_staged_names`, delete the `try` and the `except OSError`
and let the listing raise:

    -    try:
    -        return tuple(sorted(entry.name for entry in staging.iterdir()))
    -    except OSError:
    -        return ()
    +    return tuple(sorted(entry.name for entry in staging.iterdir()))

Killed 0 before round 7 and kills 1 now:
`test_round7_an_unreadable_staging_directory_still_refuses_the_same_way`. The
docstring on that function claims it never raises, because it runs only to
DESCRIBE a refusal that is already decided; the claim was load bearing and
undriven. The shape that reaches it is a staging directory at mode `0o111`, which
this account may traverse and may not read, so `os.path.lexists` still answers
True for the occupant and the guard still decides to refuse while `iterdir`
raises `PermissionError`.

**`SN_empty`.** Same region, return the empty tuple unconditionally:

    -    try:
    -        return tuple(sorted(entry.name for entry in staging.iterdir()))
    -    except OSError:
    -        return ()
    +    return ()

Kills 2, unchanged by round 7. The VALUE was already pinned. It was the SWALLOW
that was not, and the two are separate rows for exactly that reason.

**`W1_shared_filter`.** In
`test_a_planned_verb_and_the_pending_register_name_the_same_unit`, neuter the
filter on the one list both statements now read:

    -        if not entry.landed and entry.module in _pending.PENDING
    +        if False

Kills 1, that test, by name. Before round 7 the equivalent row killed 0: the
comparison and its anti vacuity guard were two independent comprehensions
spelling the same predicate, so neutering the comparison left the guard building
a populated list of its own and reporting the comparison healthy while it
compared nothing. One list is now built once and both statements read it.

**`W2_drop_guard`.** Delete the anti vacuity assertion entirely, leaving the
comparison:

    -    assert {"restore.list", "restore.run"} <= {entry.name for entry in compared}, (
    -        f"the two restore verbs are no longer compared against the register; "
    -        f"what is compared is {sorted(entry.name for entry in compared)}"
    -    )

Kills 0, and that is correct rather than a hole. A guard exists to fail when
something ELSE has gone wrong; deleting it cannot itself fail while nothing else
is wrong. What makes the guard real is `W1_shared_filter`, which is the wrong
thing it exists to catch, and that row kills.

**`W3_disagree_filter`.** Neuter the comparison's inner filter, so the
disagreement dictionary is empty whatever the two registers say:

    -        if entry.planned_in != _pending.PENDING[entry.module][0]
    +        if False

Kills 0, and this one IS a surviving hole, recorded rather than closed. A test
that asserts two registers AGREE cannot also assert that a disagreement exists,
because the repository's healthy state is agreement. What is measurable is the
SET being compared, which the guard now measures. Closing this row would take a
second test that constructs a disagreeing pair in memory and asserts the
comparison reports it.

**`W4_registry_side`.** Empty the registry side of the intersection by deleting
the marker on the `restore.list` entry, which makes it landed:

    -        # now asserts the two agree.
    -        planned_in="U27",

Kills 93 across the whole suite and 1 when run against the guard's own test,
where the failure is the guard firing by name: "the two restore verbs are no
longer compared against the register". The other 92 are collateral, because a
verb marked landed drives the conformance assertions against a module that is not
in this build. The targeted run is the one that answers the question this row
asks.

**`W5_pending_side`.** Empty the register side by renaming its key:

    -    "cratekit.session.restore_cli": (
    +    "cratekit.session.restore_cli_renamed": (

Does not reach the guard at all. `_pending.requires` raises `KeyError` at IMPORT
for a key that is gone, so pytest reports `Interrupted: 1 error during
collection` and runs NOTHING. That is a louder failure than a red test and it is
the reason the guard does not need to cover this direction.

**`N1_preflight_call`.** Delete the staging check from `_preflight`, putting it
back on the performing path alone:

    -        if step.act is Act.CLEAR and step.target is not None:
    -            _assert_staging_is_free(step.target, decided.pre_restore_root)

Kills 3. Round 6 reported 2 for this row, which was wrong.

**`N3_slug`.** Take the refusal's own reason back to the generic one:

    -        "restore-staging-occupied",
    +        "internal-error",

Kills 6 with round 7's new test present, and killed 5 without it. Round 6
reported 1 for this row, which was wrong.

**`N6_resting_read`.** Ask the resting name with the read that follows symlinks:

    -    if not os.path.lexists(resting):
    +    if not resting.exists():

Kills 1:
`test_round6_a_dangling_link_at_the_resting_name_is_a_name_already_taken`. Round
6 reported 4 for this row, which was wrong.

**`PF_skip_dry` and `PF_only_dry`.** Two halves of one question, and they are
two facts rather than two spellings of one:

    # PF_skip_dry: the preflight runs on the real run only
    -    _preflight(decided, cfg, held=held)
    +    if not dry_run:
    +        _preflight(decided, cfg, held=held)

    # PF_only_dry: the preflight runs on the rehearsal only
    -    _preflight(decided, cfg, held=held)
    +    if dry_run:
    +        _preflight(decided, cfg, held=held)

Each kills 1, and it is the SAME test,
`test_round6_the_rehearsal_refuses_the_collision_the_real_run_refuses`, failing
at a different line. Measured:

* `PF_skip_dry` fails at `tests/test_restore.py:3639` with "DID NOT RAISE
  CratekitError", the rehearsal that no longer refuses, and the half done
  assertion at `:3655` is never reached.
* `PF_only_dry` passes `:3642`, the rehearsal's own assertion, and fails at
  `:3655` with `FileNotFoundError` on `master.db-wal`, which is the live log the
  real run moved before refusing. That is the half done state itself, measured.

So the rehearsal assertion and the half done assertion are each load bearing and
neither implies the other.

**`N14_rehearsal_block`.** Delete the rehearsal block from that test:

    -    with pytest.raises(CratekitError) as rehearsal:
    -        restore.run(decided, cfg, held=held, dry_run=True)
    -
    -    assert rehearsal.value.cause.reason == "restore-staging-occupied"
    -    assert log.read_bytes() == (
    -        b"the live log, transactions committed since the checkpoint"
    -    ), "the rehearsal moved the first companion, which a rehearsal performs nothing"

Kills 1 on its own, because the deletion leaves `rehearsal` undefined at the line
that compares the two modes, so the test raises `NameError` whatever the source
does.

**The pairing is arithmetically empty and is recorded so nobody re-derives it.**
`N1_preflight_call` alone kills 3. `N1_preflight_call` with
`N14_rehearsal_block` also kills 3. A pairing whose total equals one of its
members contributes nothing, and round 6 offered exactly that as evidence for
the rehearsal assertions being necessary. The conclusion is still true and
`PF_skip_dry` and `PF_only_dry` above prove it directly.

---

## Round 6 corrections

Round 6 reported a table whose row definitions were never written into the
repository, so the counts could not be re-run by id. Three counts in it were
wrong and one pairing in it was empty. All four were caught by the independent
verification of `80771aa` and all four are re-measured above:

| row | round 6 claimed | measured |
| --- | --- | --- |
| `N1_preflight_call` | 2 | 3 |
| `N3_slug` | 1 | 5 at `80771aa`, 6 with round 7's test |
| `N6_resting_read` | 4 | 1 |
| `N1` paired with `N14` | offered as evidence | 3, the same as `N1` alone |

Nothing in round 6's conclusions changes. The relocation of the staging check
into `_preflight` is right, both `lexists` reads are right, and the refusal's own
slug is right. What was wrong was the arithmetic offered for them, which is its
own kind of defect: a reader who trusts a wrong count trusts it in both
directions, and a row reported as killing 4 when it kills 1 hides three tests
that were never written.
