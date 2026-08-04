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

---

## Round 6, U24 track deletion and tombstones

**Baseline: 3408 passed, 15 skipped.** Measured on branch
`unit/u24-track-deletion-and-tombstones` at the round six stage one commit,
2026-08-04, whole suite per row. **Every number in this section was measured.**
None is derived and none is carried over from an earlier round's report.

**How the rows were run.** A private driver under this unit's own scratch
directory, one row at a time, checkpointed to disk after each row, with the
worktree verified against the git object database before AND after every row.
Failing node ids came from a pytest plugin's `pytest_runtest_logreport` objects,
never from splitting the `FAILED` line on `" - "`, which appears inside
parametrized ids in this suite.

**Restore was `git checkout --` rather than a snapshot, which is safe HERE and
is not safe in general.** The note at the top of this file is right: a fix
round's own edits are usually uncommitted while rows are being measured, and a
checkout throws them away with the mutation. It was safe here only because the
fix commit was made BEFORE any row was applied, so there was nothing uncommitted
for a checkout to discard.

**The interrupted-driver failure happened again and was caught the same way.** A
driver process was orphaned when its parent shell was killed, kept running, and
applied a mutation to a file while a second driver was measuring a different
one. It was caught by comparing the worktree against git rather than against any
snapshot, both mutations were restored, and the affected rows were re-measured.
That is the second occurrence of the same failure in this build. The lesson
stands: checkpoint per row, and verify against git.

**A ROW NAME DOES NOT IDENTIFY A MUTATION.** The confirm rows below carry names
from earlier rounds, and every one of them is DEFINED here by its exact
substitution rather than by its name. Where a count differs from the count
reported for that name in an earlier round, the difference is called out and
attributed, or is explicitly left unattributed.

### Round six findings

| id | file | measured kills |
| --- | --- | --- |
| `R6-F1-remixer` | `core/tombstone.py` | 6 |
| `R6-F1-tail` | `core/tombstone.py` | 6 |
| `R6-F9-isrc` | `deletion/stores.py` | 3 |
| `R6-F9-wiring` | `deletion/run.py` | 2 as reported, MEASURED 3, see round seven |
| `R6-F9-recheck` | `deletion/run.py` | 0, and the argument was then deleted |
| `R6-F2-hold` | `deletion/run.py` | 2 |
| `R6-F2-retire` | `deletion/run.py` | 2 |
| `R6-F3-warn` | `deletion/run.py` | 1 |
| `R6-F4-migration` | `deletion/stores.py` | 1 |
| `R6-F5-floor` | `deletion/watermark.py` | 1 |
| `R6-F6-plan` | `deletion/run.py` | 2 |
| `R6-F6-recheck` | `deletion/run.py` | 0, and the argument was then deleted |
| `R6-F7-guard` | `core/tombstone.py` | 1 |
| `R6-F7-reader` | `deletion/library.py` | 2 |
| `R6-F10-count` | `deletion/library.py` | 1 |
| `R6-F10-walk` | `deletion/library.py` | 1 |
| `R6-F10-unaddressable` | `deletion/library.py` | 1 |
| `R6-X02-attempts` | `deletion/trash.py` | 1 |
| `R6-Z-trash-access` | `deletion/trash.py` | 1 |
| `R6-Z-trash-errno` | `deletion/trash.py` | 1 |

### Confirm rows, re-measured against this round's code and this round's suite

| id | file | measured now | reported earlier | same mutation |
| --- | --- | --- | --- | --- |
| `S2-E1` | `core/tombstone.py` | 5 | 5 | yes |
| `C05b-anchor` | `deletion/candidates.py` | 5 | 5 as `C05b` | yes |
| `C05-anchor` | `deletion/candidates.py` | 1 | 1 as `C05` | yes |
| `C05b-blank` | `deletion/candidates.py` | 3 | not comparable | NO, see below |
| `G05` | `core/tombstone.py` | 4 | 4 | yes |
| `V-wide` | `core/tombstone.py` | 4 | 4 | yes |
| `G01` | `deletion/library.py` | 2 | 2 | yes |
| `G07` | `deletion/library.py` | 2 | 2 | yes |
| `X09b` | `deletion/trash.py` | 2 | 2 | yes |
| `S2-D1` | `deletion/stores.py` | 12 | 3 | yes, suite grew |
| `S2-D2` | `core/tombstone.py` | 7 | 3 | subject yes, code changed |
| `T01` | `core/tombstone.py` | 3 | 2 | yes, suite grew |
| `S1-A3` | `deletion/library.py` | 3 | 2 | yes, suite grew |
| `Z-wm-contig` | `deletion/watermark.py` | 12 | 13 | unverifiable, see below |
| `T01alt-nofold` | `core/tombstone.py` | 30 | 19 | unverifiable, see below |

**Every confirm row still dies.** The smallest is 2 and there is no zero among
them.

**Where a number moved, and whether the move is attributed.**

* `S2-D1`, `T01` and `S1-A3` rose because round six ADDED tests that the same
  mutation also kills: six parametrized false-positive rows and a spelling table
  for `S2-D1`, an unidentifiable-row test for `T01`, and an undercount test for
  `S1-A3`. The substitution is unchanged. Measured, attributed.
* `S2-D2` was reported as rising because the line it substitutes had itself been
  rewritten, "so the numbers are not two measurements of one thing". **That
  attribution is wrong and is corrected in the round seven section, where it is
  re-measured.** The mutation's end state is `spelled = f"{remixer}
  {REMIX_DESIGNATION}"` in every round, so the numbers ARE two measurements of
  one thing, and with the later suite's new node ids deselected it kills 3,
  identical to the first report. The rise is entirely suite growth.
* `C05b-blank` is MY row and is not the earlier `C05b`. I defined it as blanking
  the drive-letter pattern; the earlier row removed its `^` anchor. Blanking
  kills 3, removing the anchor kills 5. `C05b-anchor` above is the earlier row,
  re-measured, and it reproduces exactly. This is the verifier's point about row
  names, demonstrated on a row I got wrong myself.
* `Z-wm-contig` at 12 against 13, and `T01alt-nofold` at 30 against 19: reported
  here as unattributable, because neither was defined anywhere I could read and I
  would not name a mechanism I had not reproduced. **The refusal was right and it
  was applied to evidence I had not gone and got.** Both are answerable by
  restoring the previous round's `tests/test_deletion.py` and re-running, which
  an independent verifier then did: `Z-wm-contig` kills 13 against the round five
  suite, the thirteenth being the test round six deleted, and 0 new, so
  `13 - 1 + 0 = 12`; `T01alt-nofold` kills 19 against the round five suite,
  matching exactly, and 12 new, so `19 - 1 + 12 = 30`. Same mutations, both. The
  standard is: do not guess a mechanism, AND go and get the evidence when it can
  be got. Round seven uses the technique throughout.

### The round six row definitions

Every row is ONE textual substitution unless it says otherwise. The left column
is the string in the committed source; the right column is what it was replaced
with for the measurement.

**`R6-F1-remixer`.** `core/tombstone.py`, in `remixer_title`. The round five
spelling test, restored:

    -    spelled = remixer if ends_as_a_designation(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    +    spelled = remixer if reads_as_version(remixer) else f"{remixer} {REMIX_DESIGNATION}"

**`R6-F1-tail`.** `core/tombstone.py`, in `ends_as_a_designation`. The position
test widened back to "anywhere", which is what `reads_as_version` asks:

    -    return bool(words) and words[-1] in VERSION_WORDS
    +    return bool(words) and any(word in VERSION_WORDS for word in words)

**`R6-F9-isrc`.** `deletion/stores.py`, in `ambiguous_versions`. The
discriminator neutralised, so no convergence is ever refused:

    -        if len(codes) > 1:
    +        if False:

**`R6-F9-wiring`.** `deletion/run.py`, in `plan`. The predicate unwired from the
categoriser, so `categorize` falls back to its "nothing is ambiguous" default:

    -        identifiable=stores.identifiable,
    -        ambiguous=lambda row: row.content_id in ambiguous,
    +        identifiable=stores.identifiable,

**`R6-F9-recheck` and `R6-F6-recheck`.** `deletion/run.py`, in `apply`, the
`ambiguous` and the `identifiable` argument to `candidate_rules.recheck`
respectively, each deleted. **Both measured 0, and both arguments were then
DELETED from the source rather than left in place.** Neither can ever measure
otherwise: both answers are functions of the rebuilt plan `apply` has just
computed, `apply` skips any candidate that plan did not call deletable, and a
row that failed either predicate is `UNIDENTIFIABLE` or `AMBIGUOUS_VERSION` and
therefore not deletable. So the re-check could never see a row for which either
answer differed. That is one rule written twice with one copy unreachable, which
is the shape round five deleted the `read_collection` `since` parameter for. The
row is recorded rather than dropped, because a zero that led to a deletion is
evidence and a zero nobody writes down is a row somebody re-measures next round.

**`R6-F2-hold`.** `deletion/run.py`, in `_settle_a_confirmed_absence`. The round
five behaviour restored: a confirmed removal whose file is absent with no
tombstone is HELD rather than settled, which holds every removal above it too.

    -    if recorded(answered.row):
    -        return True
    +    return recorded(answered.row)

**`R6-F2-retire`.** `deletion/run.py`, same function. The round four behaviour
restored: the row is retired silently, with no tombstone and R36 quietly false.

    -    if answered.category is not Category.GONE:
    +    if answered.category is not Category.GONE or True:

**`R6-F3-warn`.** `deletion/run.py`, in `apply`. The one line telling a person
that an unanswered removal was retired with its file somewhere else, deleted:

    -                _warn_that_an_unanswered_removal_is_being_retired(item, recorded=recorded_now)

**`R6-F4-migration`.** `deletion/stores.py`, in
`spellings_earlier_builds_wrote`. The migration made to answer "no earlier
spelling", so a tombstone an earlier build wrote stops being recognised:

    -    if not row.version:
    +    if True:

**`R6-F5-floor`.** `deletion/watermark.py`, in `contiguous_sequence`. The
never-move-backwards clamp removed:

    -        reached = max(reached, sequence)
    +        reached = sequence

**`R6-F6-plan`.** `deletion/run.py`, in `plan`. The identifiable predicate
unwired, so `UNIDENTIFIABLE` is unreachable at review time and a row that can
never be deleted is offered as deletable:

    -        identifiable=stores.identifiable,
    -        ambiguous=lambda row: row.content_id in ambiguous,
    +        ambiguous=lambda row: row.content_id in ambiguous,

**`R6-F7-guard`.** `core/tombstone.py`, in `removed_file_identity`. The guard
returned to the shape where `str(None)` is `'None'` and therefore truthy:

    -    if content_id is None or not str(content_id):
    +    if not str(content_id):

**`R6-F7-reader`.** `deletion/library.py`, in `_identifier`. The reader returned
to manufacturing the string `'None'` for a row with no identifier:

    -    value = getattr(row, attribute, None)
    -    return "" if value is None else str(value)
    +    return str(getattr(row, attribute, None))

**`R6-F10-count`.** `deletion/library.py`, in `playlist_referenced`. The
completeness comparison returned to a one-sided floor, which any undercounting
source satisfies in silence:

    -    if walked != declared:
    +    if walked < declared:

**`R6-F10-walk`.** `deletion/library.py`, in `playlist_referenced`. The handler
around the walk narrowed so a failing walk escapes as a raw exception:

    -    except Exception as exc:  # noqa: BLE001 - any failure to walk is one refusal
    +    except ZeroDivisionError as exc:  # noqa: BLE001 - any failure to walk is one refusal

**`R6-F10-unaddressable`.** `deletion/library.py`, in `playlist_referenced`. The
refusal for a live membership that names no collection row, neutralised:

    -    if "" in referenced:
    +    if False:

**`R6-X02-attempts`.** `deletion/trash.py`. The bound moved by one, which is the
mutation the previous round's assertion could not see because it read the
constant under test:

    -MAX_NAME_ATTEMPTS = 1000
    +MAX_NAME_ATTEMPTS = 999

**`R6-Z-trash-access`.** `deletion/trash.py`, in `probe`. The writability check
neutralised, so a Trash this account cannot write to reports usable:

    -    if not os.access(target, os.W_OK | os.X_OK):
    +    if False and not os.access(target, os.W_OK | os.X_OK):

**`R6-Z-trash-errno`.** `deletion/trash.py`. `errno.EINVAL` deleted from
`_NAME_REFUSED_BY_FILESYSTEM`, so a name the filesystem calls invalid stops the
run instead of costing one file:

    -        errno.EINVAL,

### The confirm row definitions

**`S2-E1`.** `core/tombstone.py`, in `_already_carries`. Credit groups readmitted
as version groups:

    -        if group is not None and not _is_a_credit(group)
    +        if group is not None

**`C05b-anchor`.** `deletion/candidates.py`. The drive-letter pattern's anchor
removed, so a drive letter ANYWHERE in a recorded value excuses the row:

    -_DRIVE_LETTER = re.compile(r"^[A-Za-z]:[\\/]")
    +_DRIVE_LETTER = re.compile(r"[A-Za-z]:[\\/]")

**`C05-anchor`.** `deletion/candidates.py`. The same, for the location pattern:

    -_FILE_LOCATION = re.compile(r"^file://", re.IGNORECASE)
    +_FILE_LOCATION = re.compile(r"file://", re.IGNORECASE)

**`C05b-blank`.** `deletion/candidates.py`. The drive-letter pattern replaced
with one that matches nothing. Recorded because it is the row I defined wrongly
and its number is what exposed that a name is not a mutation:

    -_DRIVE_LETTER = re.compile(r"^[A-Za-z]:[\\/]")
    +_DRIVE_LETTER = re.compile(r"(?!x)x")

**`G05`.** `core/tombstone.py`. The word split narrowed from non-word to
whitespace, so `Re-Edit` stops reading as two words:

    -_WORD_SPLIT = re.compile(r"\W+", re.UNICODE)
    +_WORD_SPLIT = re.compile(r"\s+", re.UNICODE)

**`V-wide`.** `core/tombstone.py`. One word added to `VERSION_WORDS`:

    +        "anjunadeep",

**`S2-D1`.** `deletion/stores.py`, in `version_of`. The remixer branch bypassed,
so the artist name is composed verbatim:

    -        title = tombstone.remixer_title(row.title, row.version)
    +        title = tombstone.version_title(row.title, row.version)

**`S2-D2`.** `core/tombstone.py`, in `remixer_title`. The already-a-designation
test dropped entirely, so `Michael Woods Remix` doubles:

    -    spelled = remixer if ends_as_a_designation(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    +    spelled = f"{remixer} {REMIX_DESIGNATION}"

**`G01`.** `deletion/library.py`, in `database_identity`. The empty-DBID refusal
neutralised, so an absent identity becomes the string `'None'`:

    -    if not identity:
    +    if False:

**`G07`.** `deletion/library.py`, in `_sequence_of`. The boolean rejection
dropped, so `True` is accepted as the update sequence 1:

    -    if value is None or isinstance(value, bool):
    +    if value is None:

**`T01`.** `core/tombstone.py`, in `version_identity`. The empty-identity refusal
neutralised, so every unnamed candidate collides onto one suppression:

    -    if not folded_artist and not folded_title:
    +    if False:

**`T01alt-nofold`.** `core/tombstone.py`, in `version_identity`. The folding
dropped from the returned identity:

    -    return {"artist": folded_artist, "title": folded_title}
    +    return {"artist": str(artist), "title": str(title)}

**`X09b`.** `deletion/trash.py`, in `move_to_trash`. The placeholder cleanup
deleted, so a failed rename leaves an empty file wearing a real track's name in
the user's Trash:

    -        try:
    -            target.unlink()
    -        except OSError:  # pragma: no cover - the placeholder was already gone
    -            pass
             raise

**`S1-A3`.** `deletion/library.py`, in `playlist_referenced`. TWO substitutions
in one row, which is why it is named as a pair: both membership refusals
neutralised, back to the unguarded comprehension.

    -    if declared is None:
    +    if False:

    -    if walked != declared:
    +    if False:

**`Z-wm-contig`.** `deletion/watermark.py`, in `contiguous_sequence`. The stop at
the first outstanding sequence removed, so the watermark advances over rows
nobody has answered for:

    -        if outstanding and sequence >= outstanding[0]:
    +        if False:

---

## Round 7, U24 track deletion and tombstones

**Baseline: 3427 passed, 15 skipped, 3442 collected.** Measured on branch
`unit/u24-track-deletion-and-tombstones` at the round seven fix commit,
2026-08-04, whole suite per row. **Every number in this section was measured.**
None is derived and none is carried over from an earlier round's report.

**How the rows were run.** A private driver under this unit's own scratch
directory, one row at a time, checkpointed to disk after each row, with every
file the table touches verified against `git show HEAD:<path>` BEFORE and AFTER
every row. Restoration was `git show HEAD:<path>` written back, never a snapshot
and never `git checkout` of a directory. Failing node ids came from a pytest
plugin's `pytest_runtest_logreport` objects. The fix commit was made BEFORE any
row was applied, so `HEAD` is the unmutated state and the comparison is exact.

**One harness defect was caught and every affected row was discarded.** The first
attempt wrote the driver's own report file into the worktree, where
`tests/test_portability.py::test_the_repository_itself_is_clean` saw it and
failed on every row. That is a harness artifact inflating every count by one, and
the whole result set from that attempt was thrown away rather than corrected. The
harness was then re-baselined on its own: with no mutation applied it reports
3427 passed, 15 skipped, 0 failed, which is the check that says the driver adds
nothing.

**WHERE A COUNT MOVED IT IS ATTRIBUTED BY MEASUREMENT, NOT BY EXPLANATION.** The
technique is the one the round six report should have used: re-run the row with
this round's 25 NEW node ids deselected, so what is left is the round six suite
answering the round six question. Round seven added 25 node ids and removed 6,
for a net of 19, and the removed 6 are the reason two of the arithmetics below
do not simply subtract 25.

### Round seven findings

| id | file | measured kills |
| --- | --- | --- |
| `R7-F1-signal` | `deletion/run.py` | 2 |
| `R7-F1-settle` | `deletion/run.py` | 1 |
| `R7-F1-retire` | `deletion/run.py` | 1 |
| `R7-F1-carry` | `deletion/candidates.py` | 2 |
| `R7-F1-present` | `deletion/candidates.py` | 3 |
| `R7-F4-round6` | `core/tombstone.py` | 7 whole suite, 0 deselected |
| `R7-F4-uncond` | `core/tombstone.py` | 7 whole suite, 3 deselected |
| `R7-F3-trashed` | `deletion/stores.py` | 2 |
| `R7-F3-version` | `deletion/stores.py` | 2 |
| `R7-F8-strip` | `core/tombstone.py` | 4 |
| `R7-F9-fold` | `deletion/stores.py` | 1 |

### The round seven row definitions

**`R7-F1-signal`.** `deletion/run.py`, in `_the_anchor_proved_nothing`. The whole
repair switched off, so an anchor that indexed nothing never refuses anything:

    -    return answered.anchor is not None and answered.anchor in references.suspect_anchors
    +    return False

Kills 2, both new: the stale empty mount point writes twenty tombstones again,
and the unanswered rows are retired again. This is the row for the finding.

**`R7-F1-settle`.** `deletion/run.py`, in `_settle_a_confirmed_absence`. Only the
CONFIRMED half switched off:

    -    if _the_anchor_proved_nothing(answered, references):
    -        logger.warning(
    +    if False:
    +        logger.warning(

Kills 1, `test_a_stale_empty_mount_point_writes_no_tombstone_and_retires_no_row`.
Separate from the row above because the two halves are separate decisions and a
single row could not show that either one alone is load bearing.

**`R7-F1-retire`.** `deletion/run.py`, in `apply`, the unanswered half only:

    -                handled.append((item.row.sequence, item.handled and not held))
    +                handled.append((item.row.sequence, item.handled))

Kills 1,
`test_an_unanswered_removal_under_a_stale_mount_point_is_not_retired_either`. A
retirement is permanent whether or not a tombstone rides with it, which is why
this half exists at all.

**`R7-F1-carry`.** `deletion/candidates.py`, in `categorize`. The anchor no
longer carried out on a `GONE` answer, so the caller has nothing to ask about:

    -                        category=Category.GONE,
    -                        resolved=resolved.path,
    -                        anchor=anchor,
    +                        category=Category.GONE,
    +                        resolved=resolved.path,

Kills 2, the same pair as `R7-F1-signal`. Recorded separately because the signal
and its delivery are in two modules and a reader looking at either one alone
should find the row that pins it.

**`R7-F1-present`.** `deletion/candidates.py`, in `categorize`. The anchor
existence test forced true, so a GENUINE unmount also reads as a deletion:

    -            if anchors.present(anchor):
    -                out.append(
    +            if True:
    +                out.append(

Kills 3, one of them new: the genuine unmount now answers `GONE` on all twenty
rows instead of `UNRESOLVED`. This is the row that pins the half round seven must
not regress, and it is a different branch from the three rows above, which is
exactly why the repair had to be additional rather than a change to this test.

**`R7-F4-round6`.** `core/tombstone.py`, in `already_spelled_as_a_remix`. Round
six's rule restored, so the closed vocabulary decides the spelling again:

    -    return bool(words) and words[-1] == fold(REMIX_DESIGNATION)
    +    return bool(words) and words[-1] in VERSION_WORDS

Kills 7 whole suite and 0 with this round's new node ids deselected, and the
zero is the point rather than a hole: round six's rule is what round six's suite
pinned, so the only tests that can see it restored are the ones written this
round. Of the 7, four are the parametrized spelling rows for `The Cut`, `Todd
Terry Live`, `Michael Woods Dub` and `Extended Mix`, and three are the 65 value
measurement, the dominance measurement and the two-identity test.

**`R7-F4-uncond`.** `core/tombstone.py`, in `remixer_title`. The test dropped
entirely, so `Michael Woods Remix` doubles:

    -    spelled = remixer if already_spelled_as_a_remix(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    +    spelled = f"{remixer} {REMIX_DESIGNATION}"

Kills 7 whole suite and 3 deselected. **This is `S2-D2` at this round's tip: the
end state is character for character the same string.** See the confirm section
for what the 3 settles.

**`R7-F3-trashed`.** `deletion/stores.py`, in `summarize`. The one field that
says whether this pass moved anything, dropped:

    -        "trashed_to": record.payload.get("trashed_to", ""),

Kills 2, both new.

**`R7-F3-version`.** `deletion/stores.py`, in `summarize`. The three payload
fields the record's own comments claim an auditor can see, dropped:

    -        "version": record.payload.get("version", ""),
    -        "version_unbelieved": record.payload.get("version_unbelieved", ""),
    -        "isrc": record.payload.get("isrc", ""),

Kills 2, both new.

**`R7-F8-strip`.** `core/tombstone.py`, in `removed_file_identity`. The emptiness
test back on the unstripped value, so `'   '` is an identifier again:

    -    if content_id is None or not str(content_id).strip():
    +    if content_id is None or not str(content_id):

Kills 4, the four whitespace parametrizations. The numeric case has its own test
and does NOT die here, which is the half the strip may not cost.

**`R7-F9-fold`.** `deletion/stores.py`, in `ambiguous_versions`. The ISRC
comparison back to raw text, so case decides whether two rows are two recordings:

    -        codes = {tombstone.fold(row.isrc or "") for row in sharing}
    +        codes = {(row.isrc or "").strip() for row in sharing}

Kills 1, `test_two_spellings_of_one_isrc_are_one_recording`.

### Confirm rows, re-measured against this round's code and this round's suite

| id | file | measured now | deselected | reported earlier | same mutation |
| --- | --- | --- | --- | --- | --- |
| `T01alt-nofold` | `core/tombstone.py` | 34 | 24 | 30 | yes, arithmetic below |
| `S2-D1` | `deletion/stores.py` | 19 | 10 | 12 | yes, arithmetic below |
| `Z-wm-contig` | `deletion/watermark.py` | 14 | 12 | 12 | yes, exact |
| `S2-D2` | `core/tombstone.py` | 7 | 3 | 7 | yes, same end state |
| `R6-F1-remixer` | `core/tombstone.py` | 15 | 6 | 6 | yes, same end state |
| `R6-F1-tail` | `core/tombstone.py` | RETIRED | | 6 | NO, subject deleted |
| `S2-E1` | `core/tombstone.py` | 5 | | 5 | yes, exact |
| `C05b-anchor` | `deletion/candidates.py` | 5 | | 5 | yes, exact |
| `G05` | `core/tombstone.py` | 4 | | 4 | yes, exact |
| `V-wide` | `core/tombstone.py` | 5 | 4 | 4 | yes, exact deselected |
| `R6-F9-isrc` | `deletion/stores.py` | 4 | 3 | 3 | yes, exact deselected |
| `T01` | `core/tombstone.py` | 3 | | 3 | yes, exact |
| `C05b-blank` | `deletion/candidates.py` | 3 | | 3 | yes, exact |
| `S1-A3` | `deletion/library.py` | 3 | | 3 | yes, exact |
| `R6-F9-wiring` | `deletion/run.py` | 3 | | 2, corrected to 3 | yes, exact |
| `R6-F6-plan` | `deletion/run.py` | 2 | | 2 | yes, exact |

**Every confirm row still dies whole suite.** The smallest is 2 and there is no
zero among them.

**THE TWO ROWS ROUND SIX LEFT UNATTRIBUTED ARE BOTH ATTRIBUTED, BY ARITHMETIC
THAT CLOSES.**

* `Z-wm-contig`, 12 at round six and 14 now. Deselected it kills 12, identical.
  The two extra are this round's apply-level mount point tests, which assert the
  watermark position and therefore die when the contiguity stop is removed.
* `T01alt-nofold`, 30 at round six and 34 now. Deselected it kills 24, and
  `30 - 6 + 10 = 34`: the 6 are the parametrized spelling rows this round
  renamed out of existence, all of which died under it, and the 10 are the
  replacements plus the new spelling tests that also die. Every term is measured.
* `S2-D1`, 12 at round six and 19 now. Deselected it kills 10, and `12 - 2 = 10`:
  exactly 2 of the 6 removed parametrized rows died under it at round six, since
  bypassing the composition leaves the value verbatim and four of those six
  expected a verbatim result. The whole suite adds 9 new deaths for 19.

**`S2-D2`'S ATTRIBUTION IS CORRECTED, AND THE CORRECTION IS RE-MEASURED HERE.**
Round six reported the rise from 3 to 7 as caused by the substituted line having
been rewritten, "so the numbers are not two measurements of one thing". That is
wrong. The mutation's end state is `spelled = f"{remixer} {REMIX_DESIGNATION}"`
either way, which is the same string in all three rounds, and with this round's
new node ids deselected it kills **3**, identical to the number first reported.
The rise is entirely suite growth, exactly like `S2-D1`, `T01` and `S1-A3`.

**`R6-F9-wiring` IS 3, NOT 2.** Measured here at 3, and the three node ids are
character for character the three that `R6-F9-isrc` also kills:
`test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`,
`test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows`
and `test_two_recordings_that_land_on_one_identity_are_refused_rather_than_suppressed`.
The 2 reported at round six is the count belonging to `R6-F6-plan`, which does
kill 2 and kills a disjoint pair,
`test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable` and
`test_a_row_that_could_never_carry_a_tombstone_is_not_offered_as_deletable`. Both
re-measured here.

**`R6-F1-tail` IS RETIRED RATHER THAN REPRODUCED, and saying so is the point of
this file.** Its substitution was `words[-1] in VERSION_WORDS` replaced by an
`any(...)` over all words, inside `ends_as_a_designation`. That function is
DELETED this round, so the string on the left of that row does not exist in the
source and the row cannot be applied at all. Its successor is `R7-F4-round6`,
which restores round six's whole rule from the other direction and kills 7. A row
whose subject is gone is not a row that measures 0; it is a row that no longer
exists, and reporting the two as the same thing is how a deleted guard comes back
looking measured.

**`R6-F1-remixer` REPRODUCES EXACTLY.** Its left side also changed, since the
predicate it substitutes is now `already_spelled_as_a_remix`, but its END STATE
is `spelled = remixer if reads_as_version(remixer) else ...`, character for
character what round six wrote. Deselected it kills 6, which is round six's
number exactly.

### The confirm row definitions

Only the rows whose substitution differs from the round six section are restated.
Every other confirm row above uses the round six definition unchanged.

**`R6-F1-remixer`**, at this round's tip:

    -    spelled = remixer if already_spelled_as_a_remix(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    +    spelled = remixer if reads_as_version(remixer) else f"{remixer} {REMIX_DESIGNATION}"

**`S2-D2`**, at this round's tip, which is `R7-F4-uncond` above:

    -    spelled = remixer if already_spelled_as_a_remix(remixer) else f"{remixer} {REMIX_DESIGNATION}"
    +    spelled = f"{remixer} {REMIX_DESIGNATION}"
