# Mutation rows

**This file is an ARCHIVE. The method lives in `docs/METHOD.md` and the driver
is `scripts/mutate.py`.** Everything below the horizontal rule is a historical
round, kept because a count with no row definition beside it is not evidence:
it is a claim about an experiment nobody else can perform. Two mutation tables
were lost to chat messages before this file existed, and a verifier then had to
reconstruct rows from prose before it could check a single count.

Do not follow the procedure this file used to describe. It was written for a
hand rolled driver, three of this project's recorded incidents were hand rolled
driver mistakes, and two of its instructions are now wrong:

- It said to revert with a snapshot rather than `git checkout`, which is right,
  but left the snapshot to whoever was typing. The driver holds that rule as a
  property and verifies each restore against `git show HEAD:<path>`, because a
  scratch copy that has been contaminated certifies itself.
- It said rows are measured against the WHOLE suite unless the row says
  otherwise. METHOD reversed that: confirm deaths on the subset of test files
  importing the mutated module, and spend a full suite only on the rows that
  came back zero. A death on a subset is a real death. A zero on a subset is
  not yet a zero.

New rounds are written by the driver into `docs/mutation/<name>.md` and
`<name>.json`, from a rows file supplied as data. Read the driver's docstring
for the row format, and METHOD for the row caps, the composite rule, and what
makes a finding blocking rather than residual.

    ./.venv/bin/python scripts/mutate.py rows.toml --name u16-round-9

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

## Round 8, U24 track deletion and tombstones

**Baseline: 3458 passed, 15 skipped, 3473 collected.** Measured on branch
`unit/u24-track-deletion-and-tombstones` with round eight applied to the working
tree, 2026-08-09, whole suite per row. Every number in this section was
measured. None is derived and none is carried over from an earlier round.

**What round eight is.** Round seven's ISRC discriminator folded the code with
`tombstone.fold`, the FREE TEXT folding, which keeps punctuation on purpose.
ISO 3901 defines an ISRC as twelve alphanumeric characters, so the display form
`GB-AYA-15-00001` and the raw `GBAYA1500001` are one code and compared under
`fold` they are two strings. One recording filed twice therefore reported
AMBIGUOUS_VERSION, and since `candidates.Category.AMBIGUOUS_VERSION` is not in
`candidates.HANDLED`, the watermark never passes over the row, the pass never
offers it, and nothing can ever clear it. Nothing is deleted and nothing is
suppressed, so the direction is safe; the cost is availability and it is
permanent. Round eight adds `tombstone.fold_code` and wires it in, and carries
two collateral fixes at the same site: a version value is tidied before it is
composed into a bracket, and a boolean is refused as a collection identifier.

**How the rows were run, and how this DIFFERS from round seven.** Round seven
restored each file from `git show HEAD:<path>`, which was exact because its fix
commit was made BEFORE any row was applied. **That method is not available to
this round and was not used.** Round eight was measured while UNCOMMITTED, so
`HEAD` is the round seven tree and restoring from it would have silently
discarded the whole round. Restoration is instead the file TEXT snapshotted in
memory once, before the first mutation, and the driver asserts the restored text
equals that snapshot after every row and re-runs the whole suite at the end to
confirm the baseline reproduces. The driver never invokes git for any purpose.
Rows ran synchronously in the foreground under `PYTHONDONTWRITEBYTECODE=1`.

**AN INSTRUMENT DEFECT WAS CAUGHT AND THE FIRST RESULT SET WAS RE-MEASURED
RATHER THAN CORRECTED.** The first driver took its collected count from
`pytest --co -q`. `pyproject.toml` already sets `addopts = "-q"`, so that became
`-qq`, which suppresses the node listing entirely, and every row reported
`collected=0` including the baseline. A column whose value is a constant cannot
detect the thing it exists to detect. This is the standing "never pass `-q`"
rule broken by the driver whose own docstring states it. The count now comes
from the `N tests collected` line of `--collect-only` and is cross checked
against the number of node id lines. The whole table was re-run; no row from the
first attempt is reported here.

**THE RECONCILIATION IS THE CHECK THAT THE DEATHS ARE REAL.** On every row
`passed + deaths` equals the baseline 3458 exactly, and `collected` holds at
3473. A mutation that made a test file fail to COLLECT would take its tests with
it, and pytest counts a collection error in the same summary position as a
failure, so a row could report deaths that are not test failures at all. Both
columns are here so that cannot pass unnoticed.

| deaths | passed | collected | row |
|---|---|---|---|
| 2 | 3456 | 3473 | wire: `fold_code` back to `fold` at the ISRC comparison |
| 1 | 3457 | 3473 | `fold_code`: NFKC back to NFC |
| 16 | 3442 | 3473 | `fold_code`: drop the non-alphanumeric strip entirely |
| 1 | 3457 | 3473 | `fold_code`: `[\W_]+` widened to `[^0-9a-z]+` |
| 6 | 3452 | 3473 | `version_title`: do not tidy before folding |
| 6 | 3452 | 3473 | `version_title`: tidy the fold but compose the raw value |
| 2 | 3456 | 3473 | `_as_a_bracketed_value`: stop replacing bracket characters |
| 5 | 3453 | 3473 | `_as_a_bracketed_value`: stop stripping the ends |
| 2 | 3456 | 3473 | `removed_file_identity`: drop the boolean guard |
| 1 | 3457 | 3473 | `removed_file_identity`: boolean guard by truthiness, not by type |

**Zero death rows: none.** Ten rows, ten non-zero.

**THREE ROWS KILL EXACTLY ONE TEST AND THAT IS BY CONSTRUCTION, NOT BY
ACCIDENT.** Each names a behaviour only one case can express, and the row is
reported at 1 rather than padded. `NFKC back to NFC` is killed only by the
fullwidth spelling, since NFC leaves fullwidth forms alone and every other
spelling in the set is already ASCII. `[\W_]+` widened to `[^0-9a-z]+` is killed
only by the Cyrillic case, because that widening is exactly transliteration and
nothing else in the set contains a non-ASCII alphanumeric. `boolean guard by
truthiness` is killed only by the `True` parameter, because `content_id is
False` still refuses `False` and differs from the shipped guard on `True` alone.
A row at 1 whose single killing test is the only test that COULD kill it is
covered; a row at 1 that happens to have one test is not, and these are the
former.

**THE TWO WIDENING ROWS ARE THE ONES THAT MATTER FOR SAFETY.** Dropping the
strip entirely kills 16, which is the fix doing its work. Widening `[\W_]+` to
`[^0-9a-z]+` kills 1, and that row exists to pin the OVER-suppression direction:
removing punctuation cannot merge two well formed codes, but folding away a
non-ASCII alphanumeric can, and a merged code stops the collision guard firing
and lets a deletion take out a version the person never deleted. The row is the
assertion that the fold was widened in the safe direction only.

## Round 9, U24 track deletion and tombstones

**Baseline: 3468 passed, 15 skipped, 3483 collected.** Measured on branch
`unit/u24-track-deletion-and-tombstones` with round nine applied to the working
tree, 2026-08-09, whole suite per row. Restoration is from text snapshotted in
memory before the first mutation, because round nine was measured uncommitted
and `git show HEAD:<path>` would have named the round eight tree. The driver
never invokes git.

**What round nine is.** The round eight adversarial verification returned
BLOCKING with three findings, and the first is round eight's own doing.
`stores.spellings_earlier_builds_wrote` reconstructed the spelling earlier
builds wrote by calling the LIVE `tombstone.version_title`. Round eight changed
that composer, so the reconstruction of history moved to what this build writes.

**THE FAILURE WAS SILENT RATHER THAN WRONG, AND THAT IS THE PART TO REMEMBER.**
Both sides of the comparison moved together, so `verbatim == version_of(row)`
became true and the function returned the EMPTY TUPLE: not a wrong earlier
spelling but no earlier spelling at all, reported as "there is no history here".
Measured at the round eight tip over eight version column shapes, six orphaned
the record the parent build would have written, and the cost is the one that
function's own docstring names: the row is held open forever and the person is
told to put back a file that is already in the Trash where they put it.

Round nine adds two FROZEN historical composers, reconstructs from those, and
offers three preceding spellings rather than one.

| deaths | passed | collected | row |
|---|---|---|---|
| 7 | 3461 | 3483 | F1: reconstruct history with the LIVE composer, round 8's body |
| 2 | 3466 | 3483 | F1: offer the oldest verbatim spelling only |
| 2 | 3466 | 3483 | F1: offer the previous build's spelling only |
| 1 | 3467 | 3483 | F1: drop the differs-from-current filter, offer everything |
| 2 | 3466 | 3483 | F1: drop the `version_kind` branch in the reconstruction |
| 8 | 3460 | 3483 | frozen: `version_title_before...` composes the tidied value |
| 3 | 3465 | 3483 | frozen: `remixer_title_before...` calls the live composer |
| 1 | 3467 | 3483 | F3: the FOLDING limb of the tidy, removed ALONE |

**Zero death rows: none.** Eight rows, eight non-zero. Every row reconciles,
`passed + deaths` equals 3468 and `collected` holds at 3483.

**THE FIRST RUN OF THIS TABLE HAD TWO ZERO DEATH ROWS AND THEY ARE WHY THE
SUITE GAINED A CASE.** Offering the oldest spelling only, and dropping the
`version_kind` branch, both killed nothing. The cause was one property of the
test set: every remixer in it already ended in `Remix`, so
`already_spelled_as_a_remix` fired, the designation was not appended, and the
plain composer and the remixer composer produced the SAME string. The two
historical spellings coincided on every row, so neither the second tuple entry
nor the branch that chooses it was exercised anywhere.

**AND THE FIRST ATTEMPT TO SEPARATE THEM WAS WRONG, WHICH IS THE MORE USEFUL
RECORD.** A remixer differing only in WHITESPACE does not separate them.
`'Michael Woods '` composes `Strobe (Michael Woods  Remix)` with a doubled
space, and `fold` collapses interior runs one step later, so the previous build
and this build write the SAME identity and there is no orphan to find. That is
`version_title`'s own docstring claim holding: the interior collapse changes no
identity that was not already broken. What DOES survive folding is a bracket
character and a stripped end, so `'[Michael Woods]'` is the separating shape and
it yields three distinct identities. The literals were MEASURED before they were
written into the test, after the reasoned guess failed.

**F3 IS CLOSED AND THE ROW PROVES IT.** Round eight's table mutated the tidy
through the composition limb twice and never removed the FOLDING limb alone,
which killed zero of 3458. Removed alone it now kills 1, on the reachable path
where a title that already names its version stops being recognised as naming
it and a second bracket is composed onto a title that already says everything.

## Round 10, U24 track deletion and tombstones

**The table moved.** METHOD.md asks for the table under `docs/mutation/`, so
round 10's 39 rows, their exact substitutions, their collected counts and the one
zero row live in `docs/mutation/u24-round-10.md`. This file keeps rounds 6
through 9 where earlier readers expect them; nothing was copied, because a second
copy of a count is how the two come to disagree.

Two things from round 10 that belong beside the instructions at the top of this
file rather than in one round's table:

* **A mutation that does not mutate reports a zero that reads exactly like an
  unguarded line.** Round 10's first form of one row wrapped the value in
  `(...) if False else (...)`, which evaluates to the original, and its first
  form of another bypassed the function it meant to weaken. Both reported zero
  deaths. Re-read every substitution as the interpreter will, not as the sentence
  describing it reads.
* **Restores are verified against a sha256 of `git show HEAD:<path>` taken
  outside the driver**, with the fix committed first so that HEAD is the thing to
  compare against. That satisfies both standing rules at once: no git inside the
  driver, and no scratch copy certifying itself.
## U16 round 6

**Baseline: 3480 passed, 16 skipped.** Measured on branch
`unit/u16-three-state-match-and-missing-review` at `b5532b6`, 2026-08-04. The
pre-round baseline was 3442 passed, 16 skipped. Every number below was measured
by applying the substitution, running the WHOLE suite, reading the count off the
summary line, and restoring the file, with the tree verified byte identical to
the committed one between rows. None is derived and none is remembered.

**THIS FILE IS AN ADD/ADD CONFLICT AT MERGE, and the commit that created it said
otherwise.** `b1ee22d`'s message says the file was "seeded from main so the merge
is an append rather than a conflict". The seeding claim is true and was checked:
this branch's first 242 lines are byte identical to main's file, which is 242
lines long in total, so the resolution really is "take ours" and nothing of
main's is lost. What is false is the conclusion. The file is ABSENT at the merge
base `af1d7d2`, so both sides added it, and `git merge-tree main
unit/u16-three-state-match-and-missing-review` reports `CONFLICT (add/add):
Merge conflict in docs/mutation-rows.md` over the whole file. Git will not auto
merge it. Whoever merges resolves it by keeping this side and reads no further,
but they have to be told to, which is what this paragraph is for.

**Why this section exists at all.** Three earlier rounds of this unit reported
mutation tables in a commit message and in a review reply, and a fourth round's
rows were reported in neither. Their ids, `M1..M19`, `N1..N6`, `U1..U6` and a set
of `X` ids from a verification sweep, cannot be re-run from the repository,
because a row id with no substitution beside it is not an experiment. The `M`,
`N` and `U` rows are written out below, reconstructed against the current tree
from the commit messages that named their intent, so that from this point on they
are re-runnable by anyone. **The `X` ids are not here and cannot be**: their
substitutions exist in no commit message, no document and no branch in this
repository, so their counts, 43, 14, 9, 8, 8, 7, 5, 4, 4, 3, 3, 3, 3 and 2,
cannot be confirmed by anybody, including whoever produced them. That is the
finding, not an excuse for skipping it.

### This round's rows

| id | what the substitution reverts | file | measured kills |
| --- | --- | --- | --- |
| `K1` | the key question and the version question are one item again | `acquire/match.py` | 11 |
| `K2` | `KEY_QUESTIONS` loses `KEY_RELATIVE` | `acquire/match.py` | 4 |
| `K3` | `question_identity`'s version field is empty | `acquire/match.py` | 2 |
| `K4` | a why with no shape gets a default instead of a refusal | `acquire/match.py` | 7 |
| `K5` | `APPROXIMATE_FLOOR` drops from 82 to 41 | `acquire/match.py` | 1 |
| `K6` | `DIGEST_WIDTH` drops from 16 to 8, so 64 bits become 32 | `acquire/match.py` | 1 |
| `K7` | the scorer's limit coefficient becomes `APPROXIMATE_LIMIT * 4` | `acquire/match.py` | 1 |
| `K8` | `STALLED` loses `VERDICT_UNSPECIFIC` | `acquire/match.py` | 1 |
| `K9` | `adjudicate` drops `or not held.resolved` | `acquire/match_cli.py` | 1 |
| `K10` | a tombstone over the OFFERED file is not reported | `acquire/match_cli.py` | 1 |
| `K11` | the vocabulary narrows back to this module's own 17 words | `acquire/match.py` | 12 |
| `K12` | the pending summary and step stop counting the ungated questions | `acquire/match_cli.py` | 1 |

No zero-kill row.

### This round's row definitions

**`K1`.** In `question_identity`, delete the fourth field:

        "key": key_token(key),
    -   "asks": question_shape(why),
        }

**`K2`.** `KEY_QUESTIONS: frozenset[Why] = frozenset({Why.KEY_RELATIVE, Why.KEY_DIFFERS})`
becomes `frozenset({Why.KEY_DIFFERS})`.

**`K3`.** In `question_identity`, `"version": version_token(version),` becomes
`"version": "",`.

**`K4`.** In `question_shape`, `shape = _QUESTION_SHAPES.get(why)` becomes
`shape = _QUESTION_SHAPES.get(why, ASKS_ABOUT_VERSION)`, so the refusal is
unreachable and every non-question gets an item identity.

**`K5`.** `APPROXIMATE_FLOOR = 82` becomes `APPROXIMATE_FLOOR = 41`.

**`K6`.** `DIGEST_WIDTH = 16` becomes `DIGEST_WIDTH = 8`.

**`K7`.** In `_approximate`, `limit=APPROXIMATE_LIMIT,` becomes
`limit=APPROXIMATE_LIMIT * 4,`. A COEFFICIENT rather than a constant, and it is
the first of the two spends the constant's own comment argues for.

**`K8`.** `STALLED: frozenset[Why] = frozenset({Why.CANDIDATE_GONE, Why.VERDICT_UNSPECIFIC})`
becomes `frozenset({Why.CANDIDATE_GONE})`.

**`K9`.** In `adjudicate`, `if held is None or not held.resolved:` becomes
`if held is None:`.

**`K10`.** In `_warnings`, `for candidate in track.candidates:` becomes
`for candidate in ():`, which is the whole candidate loop switched off.

**`K11`.** `_DASH_VERSIONS: frozenset[str] = VERSION_WORDS | _DASH_VERSION_HEADS`
becomes the literal 17-word set this module carried before the domain
vocabulary was taken: `acoustic, bootleg, demo, dub, edit, extended,
instrumental, live, mix, remaster, remastered, remix, reprise, rerecorded,
rework, version, vip`.

**`K12`.** In `_pending`, the `ungated` comprehension becomes
`ungated: set[str] = set()`, which silences both the summary clause and the step.

### The earlier rounds' rows, made re-runnable

Reconstructed against `b5532b6` from the intents recorded in this unit's commit
messages.

**THE SENTENCE THAT USED TO BE HERE WAS WRONG AND ROUND 7 MEASURED IT.** It said
the counts differ from the numbers those messages reported and that "every
difference is attributable to tests this round added rather than to a row
changing meaning". Driven with exactly round 6's 38 new node ids deselected, a
set independently validated because the deselected suite totals 3442, which is
the recorded pre-round baseline:

| id | round 5 recorded | round 6 whole suite | round 6 with its own 38 deselected |
| --- | --- | --- | --- |
| `M1` | 12 | 28 | **14** |
| `M4` | 12 | 28 | **14** |
| `M6` | 10 | 23 | **12** |
| `M2` | 13 | 28 | 13 |
| `N3` | 2 | 4 | 2 |
| `N4` | 2 | 16 | 2 |
| `N5` | 1 | 2 | 1 |
| `N6` | 7 | 10 | 7 |
| `U6` | 1 | 2 | 1 |

Six of the eight rows reduce EXACTLY, so for those the old sentence was right.
For `M1`, `M4` and `M6` it was not: with round 6's own additions taken out they
still kill two more each than round 5 recorded, so **six kills across three rows
come from PRE EXISTING node ids**. Either round 5's counts were wrong when they
were reported, or the reconstructed substitution is not the one round 5 ran. Both
are possible and neither can be settled, because round 5's rows were reported in a
commit message with no substitution beside them, which is the whole reason this
file exists. What is recorded here is the measurement, not the smoothing.

| id | what the substitution reverts | file | round 5 | now |
| --- | --- | --- | --- | --- |
| `N2` | a declared version drops the row's own title, credits and all | `match.py` | 4 | 4 |
| `N3` | the undecidable reading composes addresses again | `match.py` | 2 | 4 |
| `N4` | the ambiguous class gates the run again | `match_cli.py` | 2 | 16 |
| `N5` | the ungated class is not reported on the warning channel | `match_cli.py` | 1 | 2 |
| `N6` | `UNGATED` widens to the version question as well | `match_cli.py` | 7 | 10 |
| `U1` | the candidate grouping is re-sorted rather than kept in order | `match.py` | 1 | 1 |
| `U2` | the truncated offer reports nothing withheld | `match.py` | 2 | 2 |
| `U3` | an identity with neither an artist nor a title is allowed | `match.py` | 1 | 1 |
| `U4` | the URL check is not applied to a stripped name | `match_cli.py` | 1 | 1 |
| `U5` | a document row carrying a line break becomes two tracks | `match.py` | 1 | 1 |
| `U6` | a rejection never consults the tombstone store | `match.py` | 1 | 2 |
| `M1` | the ambiguity question is reported as an approximate hit | `match.py` | 12 | 28 |
| `M2` | the confirmed reading is a MATCH again | `match.py` | 13 | 28 |
| `M4` | the other reading is never consulted at all | `match.py` | 12 | 28 |
| `M5` | the bar drops to holding the head at ANY version | `match.py` | 4 | 4 |
| `M6` | the ambiguity branch loses to the approximate pass | `match.py` | 10 | 23 |
| `M8` | composition no longer requires the head to keep the credits | `match.py` | 8 | 8 |
| `M9` | a credit is looked for only in a TRAILING group | `match.py` | 9 | 9 |
| `M12` | an unlocatable version falls back to the whole spelling | `match.py` | 8 | 8 |
| `M14` | nothing is a performer credit | `match.py` | 8 | 8 |
| `M15` | only the parenthesised composition is composed | `match.py` | 7 | 12 |
| `M19` | a null qualifier has one spelling | `match.py` | 5 | 5 |

`N1` from round 5 is GONE and is not a loss. It reverted
`TrackMatch.question_identity` to take the key from whichever branch the library
chose, and the field it needed no longer exists. `K1` and `K2` assert the
opposite property in its place: the identity does not read the library at all,
and it does read which question is being asked. `M18` from round 4 is likewise a
swap rather than a loss and is recorded as such in that round's message.

**`M15` is a WIDER revert than round 5's and its 12 is not comparable to that 7.**
Round 5 removed one composed spelling; this substitution returns early from
`_spellings_of` with only the parenthesised form, which drops the square-bracket
form, the multi-group split and the dash form together. It is written down as
what it is rather than filed under the old count.

### The earlier rounds' row definitions

**`N2`.** In `_from_row`, `spelled=listed_title(raw_title, declared) if declared
else raw_title,` becomes `spelled="" if declared else raw_title,`.

**`N3`.** In `Wanted.addresses`, the `composed` generator gains a
`for reading in self.readings` clause and composes each reading's own head and
version, which is the union this round's policy removed.

**`N4`.** In `_pending`, the `open_questions` comprehension becomes
`list(result.of(match.MatchState.NEEDS_REVIEW))`, so nothing is filtered out of
the gate.

**`N5`.** In `_warnings`, the ungated loop's `if track.why not in UNGATED:`
becomes `if True:`, so every row of the class is skipped.

**`N6`.** `UNGATED` gains `match.Why.VERSION_DIFFERS`.

**`U1`.** In `_candidates_for`, `for recording, version_key, key in grouped:`
becomes `... in sorted(grouped):`.

**`U2`.** In `resolve_one`, `withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),`
becomes `withheld=0,`.

**`U3`.** In `version_identity`, `if not folded_artist and not folded_title:`
becomes `if False:`.

**`U4`.** In `read_list`, `if _URL_SCHEME.match(name.strip()):` becomes
`if _URL_SCHEME.match(name):`.

**`U5`.** In `read_text_rows`, `if "\n" in text or "\r" in text:` becomes
`if False:`.

**`U6`.** In `apply_verdict`, the rejection branch's `standing =
standing_tombstone(...)` becomes `standing = None`.

**`M1`.** In `resolve_one`'s confirming branch, `why=Why.READING_AMBIGUOUS,`
becomes `why=Why.TITLE_APPROXIMATE,`.

**`M2`.** In the same branch, `state=MatchState.NEEDS_REVIEW,` becomes
`state=MatchState.MATCHED,`.

**`M4`.** `confirming = _other_reading_the_library_holds(wanted, index)` becomes
`confirming = None`.

**`M5`.** In `_other_reading_the_library_holds`, `if _held_exactly(reading,
index):` becomes `if index.versions(reading.recording):`.

**`M6`.** `if confirming is not None:` becomes `if confirming is not None and not
_approximate(wanted, index):`, which is the observable equivalent of moving the
branch below the approximate pass without moving the code.

**`M8`.** In `Wanted.addresses`, `if _credits_in(head) == _credits_in(spelled):`
becomes `if True:`.

**`M9`.** `_ANY_GROUP` gains a `\s*$` anchor, so a credit is found only in a
trailing group.

**`M12`.** In `Wanted.addresses`, `head = _head_of(spelled, self.version) or
self.title` becomes `... or spelled`.

**`M14`.** `_CREDIT_PREFIXES` becomes the empty tuple.

**`M15`.** `_spellings_of` returns `(f"{head} ({version})",)` before building the
rest.

**`M19`.** In `_equivalent_versions`, `return ("", *sorted(_NULL_VERSIONS))`
becomes `return ("",)`.

---

## U16 round 7

**Baseline: 3496 passed, 16 skipped.** Measured on branch
`unit/u16-three-state-match-and-missing-review` at `b1ee22d` plus round 7's fixes,
2026-08-04. The pre-round baseline at `b1ee22d` was 3480 passed, 16 skipped, so
this round adds 16 node ids and renames one. Every number below was measured by
applying the substitution, running the WHOLE suite, reading the count off the
summary line, restoring the file and checksumming it against the pre-row bytes.
Runs used `PYTHONDONTWRITEBYTECODE=1`, because two mutations of identical byte
length written under a second apart make CPython reuse a stale `.pyc` and that
produced a spurious result on a sibling branch.

### This round's rows

| id | what the substitution reverts | file | measured kills |
| --- | --- | --- | --- |
| `V1` | an unspecific acceptance is applied to whatever single candidate is on offer now | `acquire/match.py` | 2 |
| `V2` | this file's imitation of U24's `version_title` goes back to a substring test | `tests/test_match_states.py` | 7 |
| `V3` | the recorder's own composition on top of the dash form is not consulted | `acquire/match.py` | 3 |
| `V4` | `DIGEST_WIDTH` 16 to 15 | `acquire/match.py` | 2 |
| `V5` | `DIGEST_WIDTH` 16 to 17 | `acquire/match.py` | 2 |
| `V6` | `DIGEST_WIDTH` 16 to 14 | `acquire/match.py` | 2 |
| `V7` | `DIGEST_WIDTH` 16 to 18 | `acquire/match.py` | 2 |
| `V8` | `APPROXIMATE_FLOOR` 82 to 77 | `acquire/match.py` | 1 |
| `V9` | `APPROXIMATE_FLOOR` 82 to 81 | `acquire/match.py` | 1 |
| `V10` | `APPROXIMATE_FLOOR` 82 to 83 | `acquire/match.py` | 1 |
| `K5` re-measured | `APPROXIMATE_FLOOR` 82 to 41 | `acquire/match.py` | 2, was 1 |
| `K6` re-measured | `DIGEST_WIDTH` 16 to 8 | `acquire/match.py` | 3, was 1 |

No zero-kill row.

**`V4` through `V10` are the free bands, closed.** Round 6 pinned `DIGEST_WIDTH`
with the literal `assert match.DIGEST_WIDTH == 16` and a behavioural half that
read `len(digest) == match.DIGEST_WIDTH`, which is derived from the constant and
therefore passes at every width: the test asked the thing it verifies for its own
expected value. `APPROXIMATE_FLOOR` was pinned only from the extremes, and 77, 81
and 83 each killed nothing, so at least [77, 83] was free. Both are now asserted
against computed expectations, and every neighbouring value dies.

### This round's row definitions

**`V1`.** In `apply_verdict`, the `option is None` branch loses the binding and
goes back to taking whatever single candidate is on offer:

    -        about = offered[0] if len(offered) == 1 else None
    -        if about is None or len(found.candidates) != 1:
    -            chosen = []
    -            unresolved = Why.VERDICT_UNSPECIFIC
    -        else:
    -            chosen = [c for c in found.candidates if c.candidate_id == about]
    -            unresolved = Why.CANDIDATE_GONE
    +        chosen = list(found.candidates) if len(found.candidates) == 1 else []
    +        unresolved = Why.VERDICT_UNSPECIFIC

Kills both directions of
`test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another`,
which drives `crate match run` and `crate review resolve` for real: a list line
asking for `Sun Path` at 03A against a library holding it at 08A is a key-differs
question, accepted without naming the copy; the 08A file is replaced by an 03B
one, the relative minor `Why.KEY_RELATIVE` exists to catch; and without the
binding the run reports `matched / verdict-accepted` at exit zero with the 03B
file in `paths`. The reverse direction, relative first and differs second, does
the same. The two key whys are ONE item by design, four identities and not five,
so the fix is on the answer and not on the identity.

**`V2`.** In `u24_already_carries`, the bracketed test becomes the substring test
U24 replaced three rounds ago:

    -    delimited = re.compile(rf"(?<!\w){re.escape(folded_version)}(?!\w)")
    -    return any(
    -        delimited.search(group)
    -        for found in U24_BRACKETED.finditer(u24_fold(title))
    -        for group in found.groups()
    -        if group is not None and not u24_is_a_credit(group)
    -    )
    +    return folded_version in u24_fold(title)

Kills six of the eleven `U24_COMPOSITIONS` rows and
`test_a_title_shape_outside_the_enumerated_ones_is_a_recorded_gap`. This is the
row that could not be run before this round, because the imitation was pinned by
nothing: the substring version was live and green.

**`V3`.** In `_spellings_of`, drop the composition the recorder writes on top of
the dash form:

    -        built.append(f"{dashed} ({version})")
    +        pass

Kills `test_every_row_spelling_is_addressed_from_every_reader_or_is_a_named_gap`,
which is the derivation guard: `missed` goes from R-69's one featured-credit entry
to four, the three additions being `('Sun Path - Nightwave Remix', 'text')` and
the same row through `spotify` and `tidal`. That is a tombstone U24 records which
none of this side's readers could address.

**`V4` to `V7`.** `DIGEST_WIDTH = 16` becomes 15, 17, 14 and 18 in turn.

**`V8` to `V10`.** `APPROXIMATE_FLOOR = 82` becomes 77, 81 and 83 in turn.

### Round 6's rows, confirmed

Re-run at `b1ee22d` plus this round's fixes, with this round's 17 changed node ids
deselected, which is 16 additions and one rename. The deselected suite is 3479
passed, 16 skipped, which is the `b1ee22d` baseline of 3480 minus the test this
round renamed. Every row below reverts exactly what its round 6 definition above
says it reverts.

| id | round 6 recorded | round 7 measured |
| --- | --- | --- |
| `M1` | 28 | 28 |
| `M2` | 28 | 28 |
| `M4` | 28 | 28 |
| `M6` | 23 | 23 |
| `N4` | 16 | 16 |
| `K11` | 12 | 12 |
| `M15` | 12 | 12 |
| `N6` | 10 | 10 |
| `M9` | 9 | 9 |
| `M8` | 8 | 8 |
| `M12` | 8 | 7, and explained below |
| `M14` | 8 | 8 |
| `K4` | 7 | 7 |
| `M19` | 5 | 5 |
| `K2` | 4 | 4 |
| `N2` | 4 | 4 |
| `N3` | 4 | 4 |
| `M5` | 4 | 4 |

**`M12` is a rename and not a coverage loss, measured rather than assumed.** Run
against the whole suite with nothing deselected it kills 8, exactly as recorded,
and the eighth is `test_the_only_doubled_address_is_the_one_the_recorder_actually_writes`.
That test is this round's rename of `test_the_consulter_never_composes_over_an_already_composed_title`,
so it sits in the deselected set as one of this round's changed ids. The same
assertion still dies; only its node id moved.
