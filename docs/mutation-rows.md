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
which is the derivation guard: `missed` goes from R-20's one featured-credit entry
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
