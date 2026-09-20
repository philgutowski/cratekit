"""``crate restore list``, ``run`` and ``bare-metal``: the history, and its undo.

WHAT THIS MODULE IS FOR. A capture nobody can spend is a directory of files, and
until this module existed the whole restore engine was reachable only from a
test. :mod:`cratekit.core.restore` decides and performs; this decides what the
person asked for, asks the one question R34 says has to be asked separately, and
then holds ONE destructive session around everything that follows.

ONE SESSION SPANS THE WHOLE VERB, and that is the second obligation
``tests/_pending.py`` registered against this module rather than a nicety. The
shape being refused is specific and was found by review: a plan that takes the
library lock and gives it back, followed by a run that takes it again, leaves a
window in which a second process passes the same gates and commits, after which
the run copies a snapshot over a commit its plan was built before.
:func:`cratekit.core.restore.recovery_session` is entered once, and both halves
of the restore run inside it. The off-machine half takes the already-open
``held.guard`` as its ``gates`` seam rather than acquiring its own, which is the
one wiring call U32 proved at the seam and could not make, because
``cratekit.core`` may not import the modules layer and
:mod:`cratekit.modules.tools.backup` is in it.

THE GATE IS ASKED BEFORE THE SESSION IS OPENED, and the ordering is forced
rather than chosen. ``restore.run.confirm`` is ``explicit``, so R34 makes it
answerable only by a separate recorded act against a run; the invocation that
discovers it exits DECISION_REQUIRED. A session opened before that question
would be opened, refused or held for nothing, and closed again on every drive
that only ever existed to raise the question. Worse, on a machine that has never
acknowledged a backup the session refuses FIRST, so the question a person has to
answer would never be asked at all and the verb would be unreachable on exactly
the library a restore is for.

WHAT THE DIGEST IS OVER, said plainly because the registry calls its source
"plan" and this is not the step list. The step list cannot exist before the
session, because :func:`cratekit.core.restore.plan` refuses without an open one,
so approving it would mean showing a person something only computable after the
lock was taken. What is digested instead is the restore's IDENTITY: the session
being restored, its recorded change summary, the sessions being discarded, and
whether the off-machine mirror is being pulled first. That is the value that
moves when the world moves, which is the whole job of a decision digest: a later
session committing between the offer and the answer changes the summary, the
digest moves, and the recorded decision is refused as stale. The step list is
then derived under the lock and checked again there, and
``restore._assert_override_names_them`` refuses independently when the discard
set does not name what a restore would actually destroy, so nothing here rests
on the digest alone.

NO WORKFLOW LABEL IS PASSED TO THE SESSION, and the whole verb is therefore
recorded under ``core.restore.CAPTURE_RESTORE_WORKFLOW``. An earlier version of
this paragraph said the point was to keep that label and
``backup.RESTORE_WORKFLOW`` distinguishable in the log, which is FALSE HERE and
was measured false by an independent review: handing the off machine half the
already open guard means ``backup._restore_gates`` returns that guard instead of
opening a session of its own, so its label never reaches the log at all, on any
path. One acquisition and two labels are mutually exclusive, and this unit chose
the acquisition. The consequence, that the session log cannot tell a run which
pulled a mirror from one which did not, is recorded rather than papered over.

THE THIRD VERB IS THE CASE THE OTHER TWO CANNOT SERVE. Everything above is
about a library that is present. When the volume itself is gone, every gate
``restore run`` passes is on the disk that died, and the recovery at the foot of
this module spends :func:`cratekit.core.restore.bare_metal_session` instead: the
off-machine mirror and the database, onto a named replacement drive, with no
session rolled back because no session log survived to read.

Layer: modules. It names :mod:`cratekit.cli.output` and
:mod:`cratekit.cli.exit_codes` and nothing else from the command-line layer, and
both of those are foundation-ranked under KTD25 for the reason
``adopt.apply_cli`` gives at length: a modules-layer file reaching for
``registry.Entry`` to annotate a builder is the layering violation KTD23
refuses, while the output contract and the reserved-cause table are ranked below
every verb on purpose.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

# ALIASED, because this package holds TWO modules called ``exit_codes`` and
# they are different things. ``cratekit.cli.exit_codes`` is the reserved-cause
# table, which is what a refusal's remediation is looked up in;
# ``cratekit.core.exit_codes`` is the status vocabulary and the remedy tokens.
# Both are foundation-ranked and both are legitimately needed here, so the one
# whose name would otherwise be ambiguous says what it is instead.
from cratekit.cli import exit_codes as reservations
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, restore
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.modules.tools import backup

#: What ``review_set`` calls this listing. NOT a :class:`cratekit.core.review.Queue`
#: member, and the absence is the point rather than an oversight. Every declared
#: queue is an ADJUDICATED surface, and ``tests/test_review_queue.py`` holds the
#: enum and the surface table to being the same set in both directions, so a
#: member added for a listing nobody adjudicates would break that agreement and
#: would promise a verdict this verb never asks for. The schema's ``queue`` field
#: is a string naming the set, and this is the honest name for it.
LISTING = "restore"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token rides through from the configuration error that raised it,
    so "no config at all" and "config written by a newer build" keep their
    different answers all the way out to the shell (D2).
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("session.restore_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _refused(exc: backup.BackupRefused) -> CratekitError:
    """One off-machine refusal, in the vocabulary every other layer reads.

    ``backup.Refusal`` is the backup module's own diagnosis set and it is NOT a
    cause: nothing downstream can classify a bare exception, so it would arrive
    as an internal error with its remediation discarded, which is exactly the
    collapse KTD25 exists to stop. Its slug is already reserved in
    ``cratekit.cli.exit_codes`` with a code and a per-slug remediation, and that
    reservation is what is read here rather than a second opinion written beside
    it: ``no-snapshot-available`` carries steps, ``rclone-missing`` carries an
    install token, and a class-level default here would throw both away.

    THE SLUG IS CARRIED THROUGH UNCHANGED rather than folded into a nearby
    reason. Nine diagnoses flattened into one is a person being told to mount a
    volume when what is missing is a program, and the reservation table already
    decided that each of them is worth telling apart.
    """
    slug = str(exc.refusal)
    return CratekitError(
        Cause(
            reason=slug,
            message=exc.detail,
            remediation=reservations.remediation_for(slug),
            origin=("modules.tools.backup", "session.restore_cli"),
            detail={"refusal": slug},
        )
    )


# ---------------------------------------------------------------------------
# restore list
# ---------------------------------------------------------------------------


def build_list(parser, entry) -> None:
    """Declare the listing's arguments, which are none. Parameters unannotated.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this layer importing the one above it. See the module docstring.
    """
    del entry
    parser.set_defaults(_handler=list_restorable)


def _listed(entry: restore.Restorable) -> dict[str, Any]:
    """One session as a listing row: when, what, how much, and whether it is spendable.

    ``unusable`` IS REPORTED RATHER THAN FILTERED, which is
    :class:`cratekit.core.restore.Restorable`'s own decision carried out to the
    surface. A session whose capture somebody deleted by hand is exactly the
    session a person is about to go looking for, and dropping it from the list
    answers their question with silence.
    """
    return {
        "session_id": entry.session_id,
        "started": entry.started,
        "workflow": entry.workflow,
        "restorable": entry.restorable,
        "unusable": entry.unusable,
        "change": [
            {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
            for tree in entry.change.trees
        ],
    }


def list_restorable(ctx) -> Envelope:
    """Every recorded session, newest first, with what it changed.

    READ ONLY, AND OUTSIDE THE SESSION GATES. Listing resolves no path on the
    library volume and writes nothing, so requiring a backup acknowledgment and
    the library lock to answer "what could I roll back to" would make the
    question unanswerable on precisely the machine that needs it: one whose
    library is busy, or one where the thing a person is deciding is whether they
    have a backup at all.

    ``unresolved`` IS ZERO AND IS NOT A COUNT OF SESSIONS. It means what is OPEN
    in an adjudication queue, and nothing here awaits a verdict: a recorded
    session is a settled fact and a listing is not a backlog. Reporting the
    number of sessions there would tell a person they have work they do not,
    which is the reasoning ``deletion.tombstone_cli`` gives for the same field.
    """
    cfg = _load()
    listed = restore.list_sessions(cfg)
    return ctx.envelope(
        data={
            "queue": LISTING,
            "items": [_listed(entry) for entry in listed],
            "unresolved": 0,
        }
    )


# ---------------------------------------------------------------------------
# restore run
# ---------------------------------------------------------------------------


def build_run(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    THERE IS NO ``--yes`` AND NO ``--confirm``. The confirmation is the recorded
    answer to the explicit gate and there is no flag anywhere in this package
    that stands in for one (R34).

    ``--discard`` IS REPEATED IDENTIFIERS AND NEVER A BOOLEAN, which is
    :func:`cratekit.core.restore.plan`'s requirement carried to the surface
    unchanged. A restore reaching back past a later session that committed is
    destroying work somebody did on purpose, and a flag saying "yes" is an answer
    to a question nobody read.
    """
    del entry
    parser.add_argument(
        "session_id",
        nargs="?",
        default=None,
        help=(
            "the write session to roll back to; omitted means the newest one "
            "whose capture is spendable"
        ),
    )
    parser.add_argument(
        "--discard",
        action="append",
        default=[],
        metavar="SESSION_ID",
        dest="discard",
        help=(
            "a later session whose committed work this restore destroys, named "
            "explicitly; repeat once per session, and the set must match what "
            "the refusal listed"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="walk every step and perform none of them, under the same gates",
    )
    parser.add_argument(
        "--from-backup",
        action="store_true",
        dest="from_backup",
        help=(
            "pull the database back from the off-machine mirror first, for the "
            "case where the volume itself was replaced and no local capture "
            "survived"
        ),
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        metavar="STAMP",
        help="which dated off-machine snapshot to pull; the newest by default",
    )
    parser.add_argument(
        "--snapshot-volume",
        default=None,
        dest="snapshot_volume",
        metavar="IDENTITY",
        help=(
            "the volume identity the snapshot is expected to record, for a "
            "library whose drive was replaced since the snapshot was taken; "
            "checked against the snapshot, used once and never recorded"
        ),
    )
    parser.add_argument(
        "--include-mirror",
        action="store_true",
        dest="include_mirror",
        help=(
            "pull the music and everything else the mirror carried, not only the "
            "database; hundreds of gigabytes, so it is off by default"
        ),
    )
    parser.add_argument(
        "--target",
        default=None,
        metavar="DIRECTORY",
        help=(
            "restore the database into this directory instead of the live "
            "library, which is how a restore is rehearsed; needs the off-machine "
            "pull, and rolls no session back"
        ),
    )
    parser.set_defaults(_handler=perform_restore)


def _target_invalid(message: str, **detail: Any) -> CratekitError:
    """The invocation, not the directory, is what this refuses.

    ONE SLUG OVER TWO SHAPES, which is the shape ``cli.review`` already settled
    for its own selection refusals: a target without the off-machine pull and a
    target beside a capture rollback are two spellings of one misunderstanding,
    that ``--target`` names somewhere to REHEARSE a database restore rather than
    a second place to perform the live one. The remedy is the same act in both,
    so a second slug would only make a consumer branch on the message text.

    NOT ``restore-target-absent`` AND NOT ``restore-target-is-live-root``, and
    the distance is worth keeping: those two are facts about a PATH, and a
    person who is told their directory is wrong will go looking at the directory,
    which here is not where the mistake is.

    THE REMEDIATION IS WRITTEN HERE RATHER THAN LOOKED UP, which is the opposite
    of what ``_refused`` does one function up, and the difference is not a style.
    ``cratekit.cli.exit_codes`` reserves the slugs a MODULE's refusal enum
    raises, and ``tests/test_reserved_causes.py`` fails a reservation nothing in
    that population produces, on the ground that a reservation with no producer
    reads as a contract and is not one. This refusal is the verb's own, so its
    registration is the closed reason registry in ``cratekit.core.cause``, and
    its sentence lives beside the condition that raises it.
    """
    return CratekitError(
        Cause(
            reason="restore-target-invalid",
            message=message,
            remediation=Remediation(
                steps=(
                    "a restore target takes the database from the off-machine "
                    "snapshot and rolls no write session back; ask for the "
                    "off-machine pull, and name either a session to roll back or "
                    "a target, never both",
                )
            ),
            origin=("session.restore_cli",),
            detail=detail,
        )
    )


def _target_is_live(message: str, **detail: Any) -> CratekitError:
    """A destination that is the live library, by either of the two ways it can be.

    ONE SLUG OVER BOTH CHECKS, because the step is one act: name a directory
    that is not this library. Naming the root and landing the database on the
    live file are different mistakes to make and the same mistake to fix, and
    ``detail`` carries which of the two fired for anything that wants to tell
    them apart without reading English.

    ITS SENTENCE IS WRITTEN HERE for the reason the function above gives at
    length: the reservation table belongs to the refusal enums a module raises,
    and this is the verb's own refusal.
    """
    return CratekitError(
        Cause(
            reason="restore-target-is-live-root",
            message=message,
            remediation=Remediation(
                steps=(
                    "name a directory the live library is not inside and does "
                    "not contain, and check where the database itself would land "
                    "when the database sits outside the library root; restoring "
                    "onto the live library is this verb with no target named",
                )
            ),
            origin=("session.restore_cli",),
            detail=detail,
        )
    )


def _same_place(one: Path, other: Path) -> bool:
    """Whether two paths name ONE place on the disk, rather than one spelling.

    ``Path.resolve`` AND ``==`` IS NOT A SAME-DIRECTORY TEST, and the difference
    is the whole reason this function exists. Every filesystem this product runs
    on in practice is case insensitive by default, which is APFS as macOS ships
    it and exFAT on the external drive a DJ library normally lives on. On one of
    those, a library root typed in a different case is the SAME directory, and
    both ``==`` and ``is_relative_to`` answer that the two paths are unrelated
    because both are string comparisons wearing a path's clothes. Measured by the
    review of this unit: a target spelled in the wrong case passed both checks
    below, the restore was pointed at the live database's own directory, and the
    live write-ahead log was unlinked.

    ``samefile`` ASKS THE FILESYSTEM, comparing device and inode, so it answers
    about the place instead of about the name. It needs both paths to exist,
    which is why the fallback is here rather than an error: a target that does
    not exist cannot be a directory the live library occupies, and
    ``backup.plan_restore`` refuses it as absent a moment later. A case folded
    spelling of a directory that DOES exist also exists on these filesystems,
    which is precisely why the stat succeeds in the case this is for.
    """
    try:
        return one.samefile(other)
    except OSError:
        return one == other


def _holds_or_is(root: Path, place: Path) -> bool:
    """Whether ``place`` IS ``root`` or sits underneath it, place by place.

    WALKED RATHER THAN PREFIX MATCHED, for the reason
    :func:`_same_place` gives: a prefix match over strings cannot see that a
    differently cased ancestor is the same directory. Each of the candidate's
    own ancestors is asked instead, so a target three directories inside a
    library root typed in another case is still inside it.

    The string test is kept as the first question and not as the only one. It is
    the cheap answer on the common path, it needs nothing to exist, and it is
    the whole answer on a case sensitive filesystem.
    """
    if place == root or place.is_relative_to(root):
        return True
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))


def _restore_target(cfg: config.Config, args) -> Path | None:
    """The directory ``--target`` names, resolved and refused, or ``None``.

    ``None`` IS TODAY'S VERB UNCHANGED. Omitting the flag restores onto
    ``cfg.library.root`` exactly as it did before this function existed, so the
    live restore keeps every one of its gates and none of these checks apply to
    it. Everything below is about the flag.

    IT REFUSES BEFORE THE GATE IS ASKED AND BEFORE ANY SESSION OPENS. A person
    who is going to be told their target is the live library should not first be
    asked to confirm a destructive restore, and a target that would land on the
    live database must not reach a code path that has already taken the library
    lock and started resolving paths against it.

    THE RESOLUTION IS THE GUARD'S FIRST STEP AND NOT A CONVENIENCE. Both
    comparisons below are between paths, and a relative path compares equal to
    nothing: ``Path("library")`` is neither the configured root nor inside it,
    whatever directory the person is standing in when they type it. Both sides
    are resolved so the comparison is about the two places on the disk rather
    than about two spellings. Resolving is not ENOUGH for that, which is what
    :func:`_same_place` is for and why neither check below is a bare ``==``.

    TWO DESTINATION CHECKS, AND THE SECOND IS NOT IMPLIED BY THE FIRST. The
    containment check refuses the library root and anything above or below it.
    That is the whole answer only while the database sits inside the root. In the
    layout ``library.db_outside_root_acknowledged_on`` exists for, which is
    rekordbox's own default, the database lives somewhere else entirely and
    :func:`cratekit.modules.tools.backup.database_target_for` rebases it as
    ``target / database.name``. So a person can name the parent directory of
    their live database, pass the containment check honestly, and have the
    restore write ``master.db`` straight over the live one. The second check asks
    the question that actually matters, which is where the DATABASE lands, and it
    asks it through the same function the plan will use rather than through a
    second opinion about vendor layout.

    EXISTENCE IS NOT CHECKED HERE. ``backup.plan_restore`` already refuses a
    target that is not a directory, with ``restore-target-absent`` and its own
    reserved remediation, and a second check here would be a guard covered by
    another guard, which is a guard nothing covers.
    """
    raw = getattr(args, "target", None)
    if raw is None:
        return None
    if not args.from_backup:
        raise _target_invalid(
            "a restore target is a place to put a database pulled from the "
            "off-machine snapshot, so it needs the off-machine pull; ask for it, "
            "or drop the target and restore the live library",
            target=str(raw),
        )
    if args.session_id is not None or args.discard:
        raise _target_invalid(
            "a restore into a directory that is not the library restores the "
            "database and nothing else; rolling a write session back moves state "
            "coupled to the live library and cannot be pointed elsewhere, so name "
            "a session or a target and not both",
            target=str(raw),
            session_id=args.session_id,
            discard=list(args.discard),
        )
    resolved = Path(raw).expanduser().resolve()
    root = Path(cfg.library.root).resolve()
    if _holds_or_is(root, resolved) or _holds_or_is(resolved, root):
        raise _target_is_live(
            f"{resolved} is the live library at {root}, or holds it, or sits "
            f"inside it; a rehearsal restores somewhere the live library is not, "
            f"and restoring onto the live library is this verb without a target",
            target=str(resolved),
            library_root=str(root),
            check="containment",
        )
    landing = backup.database_target_for(cfg, resolved).resolve()
    live = config.state_path("rekordbox_db", cfg).resolve()
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):
        raise _target_is_live(
            f"the database would land on {landing}, which is this library's live "
            f"database; the target is outside the library root and the database "
            f"is too, so naming its directory restores over it in place",
            target=str(resolved),
            database_target=str(landing),
            live_database=str(live),
            check="destination",
        )
    return resolved


def _newest_restorable(cfg: config.Config) -> restore.Restorable | None:
    """The session a bare ``crate restore run`` means, or None.

    Newest FIRST is :func:`cratekit.core.restore.list_sessions`'s ordering and is
    not re-derived here. RESTORABLE rather than merely newest, because a capture
    somebody deleted by hand is listed on purpose and choosing it by default
    would turn an informative row into a refusal every time.
    """
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
    return None


def _named(cfg: config.Config, session_id: str) -> restore.Restorable:
    """The session a person named, or a refusal that says which of the two is wrong.

    TWO DIFFERENT FACTS, TWO DIFFERENT MESSAGES, and collapsing them is the
    failure this function exists to avoid. "No session has that identifier" sends
    a person to the listing; "that session's capture cannot be spent" sends them
    to a different session, and the row itself already carries the sentence
    saying why. One message for both would send half of them to the wrong place.

    IT REFUSES AN UNUSABLE CAPTURE HERE TOO, and the docstring that used to say
    the opposite was wrong in a way a person met. It claimed the plan refuses one
    under the lock "with the engine's own diagnosis, which is more specific than
    anything this layer could restate". Measured on 2026-08-23, by driving this
    product's OWN retention to delete a capture whose session record stays in the
    log, that diagnosis is a raw errno carrying ``internal-error`` and
    ``report-defect``: a person is told to file a bug about a directory the tool
    removed on purpose, while ``restore list`` sitting beside it explains the
    situation correctly in a sentence.

    SO THE SENTENCE THE LISTING ALREADY COMPUTED IS WHAT IS RAISED, rather than a
    second opinion invented here. ``Restorable.unusable`` is one string produced
    in one place, and both surfaces now say it.

    AND IT REFUSES BEFORE ANY SESSION OPENS, which is the half that matters with
    ``--from-backup``. The off machine pull runs first, so a refusal deferred to
    the plan let two transfers complete and the live companion files be cleared
    before anything looked at whether the capture could be spent at all.
    """
    for entry in restore.list_sessions(cfg):
        if entry.session_id != session_id:
            continue
        if entry.unusable:
            raise CratekitError(
                Cause(
                    reason="restore-record-unusable",
                    message=(
                        f"session {session_id} cannot be restored: {entry.unusable}"
                    ),
                    remediation=Remediation(
                        steps=(
                            "run the restore listing and choose a session whose "
                            "capture is still spendable",
                        )
                    ),
                    origin=("session.restore_cli",),
                    detail={"session_id": session_id, "unusable": entry.unusable},
                )
            )
        return entry
    raise CratekitError(
        Cause(
            reason="restore-record-unusable",
            message=(
                f"no write session on this library is recorded under "
                f"{session_id!r}; the listing verb shows every one that is"
            ),
            remediation=Remediation(
                steps=("run the restore listing to see the sessions this library recorded",)
            ),
            origin=("session.restore_cli",),
            detail={"session_id": session_id},
        )
    )


def _offer(
    chosen: restore.Restorable | None,
    *,
    discarding: Sequence[str],
    from_backup: bool,
    snapshot: backup.ResolvedSnapshot | None,
    include_mirror: bool,
    snapshot_volume: str | None = None,
    target: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """What the person is being asked to approve, as a ``plan/1`` payload.

    THE ITEMS ARE THE HALVES OF THE RESTORE, not its steps, for the reason the
    module docstring gives at length. Each half is named separately because they
    are separately refusable and separately expensive, and an approval that
    could not tell them apart would let a person who meant "roll back one
    session" also authorise pulling a mirror off the network.

    THE CHANGE SUMMARY IS IN THE DIGEST, and that is the field that does the
    work. A later session committing between the offer and the answer changes it,
    so the digest moves and the recorded decision is refused as stale rather than
    honoured against a library that is no longer the one it described.

    THE TARGET IS IN THE DIGEST for the same reason the discard set is. Where the
    database lands is most of what a person is approving, and a decision that
    could not tell a rehearsal into a scratch directory from a restore over the
    live library would let an answer given to the harmless one be honoured
    against the destructive one. ``"library"`` names the absent flag rather than
    ``None``, so the two are different values under the digest and neither is the
    empty one.

    SO IS THE REHEARSAL FLAG, and the hole it closes is the one the target was
    added to avoid, found one flag over by this unit's own review. ``--dry-run``
    walks every step and performs none, so it is the cheapest thing a person can
    be asked to approve; with it outside the digest, the decision recorded
    against a preview matches a later invocation without the flag exactly, and
    authorises a real restore over the live database. It is digested rather than
    listed as an item because it is a property of the whole run, both halves at
    once, rather than of either half.

    THE SNAPSHOT IS THE RESOLVED STAMP, never the word for "whichever is newest".
    That word was what entered the digest when no stamp was named, so a backup
    landing between the offer and the answer changed which database arrived and
    the recorded decision still matched. With the stamp itself digested, the
    second act resolves again, the digest moves, and the decision is refused as
    stale. Whose the snapshot says it is rides beside it, along with the volume
    a person told the restore to expect, because those are what is being
    approved when the snapshot is not plainly this library's own.
    """
    items: list[dict[str, Any]] = []
    if from_backup:
        items.append(
            {
                "half": "off-machine",
                # READ DIRECTLY, with no fallback for an absent resolution. The
                # off-machine half is offered only over a resolved snapshot, and
                # a fallback here would digest "no snapshot" in silence the day
                # that stopped being true, where this fails loudly instead.
                "snapshot": snapshot.stamp,
                "snapshot_named": snapshot.named,
                "recorded_volume": snapshot.recorded_volume,
                "expected_volume": snapshot_volume,
                "include_mirror": include_mirror,
                "target": str(target) if target is not None else "library",
            }
        )
    if chosen is not None:
        items.append(
            {
                "half": "capture",
                "session_id": chosen.session_id,
                "started": chosen.started,
                "workflow": chosen.workflow,
                "change": [
                    {"tree": tree.tree, "created": tree.created, "updated": tree.updated}
                    for tree in chosen.change.trees
                ],
                "discarding": list(discarding),
            }
        )
    return {
        "digest": digest_of(
            {"kind": "restore.run", "items": items, "dry_run": dry_run}
        ),
        "items": items,
        "totals": {"halves": len(items), "dry_run": dry_run},
        "chunk": None,
    }


#: The flags that describe the off-machine pull and mean nothing without it,
#: as the attribute argparse stores and the spelling a person typed.
_PULL_FLAGS = (
    ("snapshot", "--snapshot"),
    ("snapshot_volume", "--snapshot-volume"),
    ("include_mirror", "--include-mirror"),
)


def _refuse_pull_flags_without_the_pull(args) -> None:
    """A flag about the off-machine pull, with no pull asked for, is refused.

    THEY WERE SILENTLY DROPPED, all of them, and the expected volume flag made
    that worth closing: a person who types it believes they authorised pulling a
    replaced drive's snapshot, and with the pull flag forgotten the verb went on
    to offer a capture rollback of the live library instead, saying nothing
    about the flag it had thrown away. ``--target`` was already refused in this
    position under its own slug, which is why it is not in the table.

    The verb's own slug with its sentence beside it, for the reason
    ``_target_invalid`` gives: the reservation table holds a module's refusal
    enum, and this is a fact about the invocation.
    """
    if args.from_backup:
        return
    typed = [
        spelling
        for attribute, spelling in _PULL_FLAGS
        if getattr(args, attribute, None) not in (None, False)
    ]
    if not typed:
        return
    raise CratekitError(
        Cause(
            reason="restore-flag-needs-pull",
            message=(
                f"{' and '.join(typed)} describe the off-machine pull, and this "
                f"restore did not ask for one, so it would have rolled the live "
                f"library back to a recorded session and ignored "
                f"{'them' if len(typed) > 1 else 'it'}"
            ),
            remediation=Remediation(
                steps=(
                    "add --from-backup to pull the database from the off-machine "
                    "snapshot, or drop the flag to roll back a recorded session",
                )
            ),
            origin=("session.restore_cli",),
            detail={"flags": typed},
        )
    )


def _confirm_gate(entry):
    """The explicit confirmation gate off the entry, found by digest source.

    BY ``digest_source`` RATHER THAN BY POSITION. This verb declares two gates
    and the shared cloud-sync one is raised by the guarded writer rather than
    asked here, so indexing ``gates[0]`` would bind this handler to the order
    they happen to be written in and would ask the wrong question the day
    somebody reorders them.
    """
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
                f"there is no question to ask before restoring"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("session.restore_cli",),
            detail={"verb": entry.name},
        )
    )


@dataclass(frozen=True, slots=True)
class RestoreReport:
    """What one restore did, in both halves, so neither can hide behind the other.

    TWO FIELDS RATHER THAN ONE, because a restore has two independently optional
    halves and a single value cannot say which of them ran. ``pulled`` is the
    off-machine transfers by label, empty when the mirror was not asked for;
    ``outcome`` is the capture restore, ``None`` when no session was named. Both
    empty is the honest description of a run that had nothing to do, and it is a
    different fact from either one alone.

    ``absent`` is the suffixes the off-machine snapshot did not hold, so a
    restore from a checkpointed database reports the write ahead log as missing
    rather than as transferred. Empty when the off-machine half did not run.
    """

    pulled: tuple[str, ...]
    outcome: restore.RestoreOutcome | None
    dry_run: bool
    absent: tuple[str, ...] = ()
    #: Which dated snapshot the off-machine half pulled, and the identity its
    #: marker recorded, read off the PLAN the engine built under the gates
    #: rather than off the offer, so the report names what arrived.
    snapshot: str | None = None
    recorded_volume: str | None = None


def restore_under_one_session(
    cfg: config.Config,
    *,
    session_id: str | None,
    discarding: Sequence[str] = (),
    dry_run: bool = False,
    from_backup: bool = False,
    snapshot: str | None = None,
    snapshot_volume: str | None = None,
    accept_unrecorded: bool | None = None,
    include_mirror: bool = False,
    target: Path | str | None = None,
    identity_provider: object | None = None,
    mount_enumerator: object | None = None,
    runner: object | None = None,
    process_lister: object | None = None,
) -> RestoreReport:
    """Both halves of a restore, inside ONE acquisition of the destructive gates.

    This is the function ``tests/_pending.py`` registered against this module.
    The gates are entered once, by
    :func:`cratekit.core.restore.recovery_session`, and everything after that
    point happens inside the block it yields into: the off-machine pull, the
    plan, and the write.

    ``held.guard`` IS WHAT MAKES IT ONE ACQUISITION. ``backup.plan_restore`` and
    ``backup.run_restore`` each default to taking the library lock themselves, so
    calling them plainly from in here would be three acquisitions with two
    windows in them, and taking the lock a second time IN THIS PROCESS would be
    reported as a foreign holder, which is to say the caller would be told to
    wait for itself. The guard is a pass-through that does nothing, deliberately.

    THE OFF-MACHINE HALF RUNS FIRST when both are asked for, and the order is the
    whole reason they compose. The mirror lays down the database the volume lost;
    the capture then rolls that database and its coupled state back to a recorded
    session. The reverse order would restore a session and then overwrite it with
    whatever the remote happened to hold.

    ``confirmed=True`` IS NOT A FLAG STANDING IN FOR THE DECISION. The explicit
    gate is answered, recorded against a run with its actor, and checked before
    this function is called; ``plan_restore``'s parameter is how a caller states
    that a named decision exists, and R33 is why that module refuses to prompt
    for one itself.

    ``target`` IS NOW REACHABLE FROM THE COMMAND LINE, and the hazard that kept
    it off one is answered at the verb rather than here. The capture half
    resolves every path it writes from ``cfg.library.root``, and
    :func:`cratekit.core.restore.plan` refuses a session that does not authorise
    that root, so a target pointing the mirror half somewhere else while a
    session rolled back would put the two halves of one restore on two volumes:
    the database from the remote on a replacement disk, and the coupled state
    rolled back on the configured one. ``_restore_target`` refuses that
    combination outright, so the flag can only ever produce the off-machine half
    alone, which is a database restored into a named directory and nothing else
    (R-368). Recovering a whole volume is a different verb with a different set
    of gates, :func:`recover_under_bare_metal_session` below.

    THIS FUNCTION STILL TAKES BOTH, and that is deliberate rather than an
    oversight. The parameter remains a seam, and the composition test drives both
    halves at once against a scratch directory to prove one acquisition of the
    lock. The refusal lives where the two halves are CHOSEN, which is the verb,
    and putting it here as well would break the measurement that proves the
    engine composes at all.

    ``analysis_roots`` NAMES THE LIBRARY ROOT rather than being left empty. A
    restore replaces the database and everything coupled to it, so anything under
    the library can move, and a watch that names nothing watches nothing while
    still reporting a clean session. The analysis share rides with it when the
    database sits outside the root, because in that layout the root holds no
    grid at all (R-14).

    IT REPORTS BOTH HALVES SEPARATELY, and the earlier shape that returned only
    the capture outcome was wrong in a way a person would have met. A run that
    pulled a whole mirror and named no session returned ``None``, and the verb
    then reported zero steps performed: hundreds of gigabytes moved and the
    output said nothing had happened. ``outcome`` stays ``None`` when no capture
    was spent, because inventing an empty one would report a restore that
    converged over state nothing looked at, and ``pulled`` carries the other half
    so the absence of one is not read as the absence of both.
    """
    watched: tuple[Path, ...] = analysis_store.watch_roots(cfg)
    with restore.recovery_session(
        cfg,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ) as held:
        transferred: tuple[str, ...] = ()
        missing: tuple[str, ...] = ()
        arrived: dict[str, Any] = {}
        if from_backup:
            where = Path(target) if target is not None else Path(cfg.library.root)
            try:
                pulled = backup.plan_restore(
                    cfg,
                    target=where,
                    confirmed=True,
                    snapshot=snapshot,
                    snapshot_volume=snapshot_volume,
                    accept_unrecorded=accept_unrecorded,
                    include_mirror=include_mirror,
                    gates=held.guard,
                    **_seam("runner", runner),
                    **_seam("process_lister", process_lister),
                )
                ran = backup.run_restore(
                    pulled,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
                    **_seam("runner", runner),
                )
            except backup.BackupRefused as exc:
                raise _refused(exc) from exc
            # THE RESULTS, NOT THE PLAN'S COMMANDS, and the earlier spelling of
            # this line was half of a blocking defect. Reporting the planned
            # labels said a transfer had happened whether or not it had, and
            # ``run_restore`` was returning its results unread, so a restore
            # whose every copy failed reported two completed transfers and exited
            # OK, with the live companion files already cleared. The reading is
            # now in ``run_restore`` where every caller gets it, and this line no
            # longer describes work it did not watch.
            #
            # ONE LABEL PER RESULT, zipped strictly, so a runner returning fewer
            # results than the plan holds commands is a hard failure here rather
            # than a report that quietly lists the shorter of the two.
            transferred = tuple(
                command.label
                for command, _result in zip(pulled.commands, ran, strict=True)
            )
            missing = pulled.absent_sidecars
            arrived = {
                "snapshot": pulled.snapshot,
                "recorded_volume": pulled.recorded_volume,
            }
        if session_id is None:
            return RestoreReport(
                pulled=transferred, outcome=None, dry_run=dry_run, absent=missing, **arrived
            )
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=discarding,
            process_lister=process_lister,
        )
        return RestoreReport(
            pulled=transferred,
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
                process_lister=process_lister,
            ),
            dry_run=dry_run,
            absent=missing,
            **arrived,
        )


def _seam(name: str, value: object) -> dict[str, Any]:
    """One injectable seam as keyword arguments, omitted entirely when unsupplied.

    ``backup.plan_restore`` DEFAULTS ITS RUNNER TO A REAL SUBPROCESS and reads
    ``None`` as an explicit choice of nothing, unlike the destructive-session
    helper the module docstring names, which reads ``None`` as "resolve the
    default". Forwarding ``None`` blindly would therefore hand the off-machine
    half a runner that is not callable, so the absent case has to be an absent
    ARGUMENT rather than a null one.

    THE NAME OF THAT HELPER IS NOT SPELLED HERE, and the omission is load
    bearing rather than coy. ``tests/test_restore.py`` refuses this module if its
    source contains that identifier anywhere, because entering the gates directly
    is exactly how the two acquisitions come back, and the guard reads text
    rather than intent. Prose explaining why a thing is forbidden is still the
    forbidden thing (P7).
    """
    return {} if value is None else {name: value}


def _performed(report: RestoreReport, offered: dict[str, Any]) -> dict[str, Any]:
    """The result as a ``plan/1`` payload, keeping the digest the gate answered.

    THE DIGEST DOES NOT MOVE BETWEEN THE OFFER AND THE REPORT. It identifies the
    decision this run was authorised under, so recomputing it over the performed
    steps would report a different value from the one recorded against the run,
    and a person comparing the two would be looking at evidence that the approval
    did not cover this work.

    BOTH HALVES ARE IN ``items``, in the order they happened, so a report cannot
    describe a mirror pull as nothing. ``converged`` is reported only when a
    capture was spent, because it is the capture restore's own question and
    answering it for a run that never asked would be the permissive reading of
    "nobody looked".
    """
    outcome = report.outcome
    items: list[dict[str, Any]] = [
        {"half": "off-machine", "transfer": label} for label in report.pulled
    ]
    items += [
        {
            "half": "capture",
            "act": str(step.act),
            "target": str(step.target) if step.target else None,
            "detail": step.detail,
        }
        for step in (outcome.performed if outcome is not None else ())
    ]
    totals: dict[str, Any] = {
        "transfers": len(report.pulled),
        "steps": len(outcome.performed) if outcome is not None else 0,
        "dry_run": report.dry_run,
        "absent_sidecars": list(report.absent),
    }
    if report.pulled:
        totals["snapshot"] = report.snapshot
        totals["recorded_volume"] = report.recorded_volume
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
    return {"digest": offered["digest"], "items": items, "totals": totals, "chunk": None}


def perform_restore(ctx) -> Envelope:
    """Ask the confirmation gate, then restore under one session, or say there is nothing.

    NOTHING TO RESTORE IS AN OUTCOME, NOT A FAILURE. A library with no spendable
    capture and no off-machine pull asked for is the state of every install
    before its first write session, and refusing there would report a missing
    history as a broken machine. It returns the offer it made with no steps in
    it, so the report says what was considered rather than nothing at all.

    AND IT OPENS NO SESSION ON THAT PATH. The destructive gates refuse a library
    whose backup has never been acknowledged, so opening them to do zero work
    would make the verb unreachable on exactly the machine a person is trying to
    find out about. That is the same decision ``delete.review`` takes for the
    same reason: a baseline must not take a destructive session to move zero
    files.

    THE GATE STILL FIRES WHEN THERE IS NOTHING TO DO. Conformance 3 holds every
    declared gate to firing, and "nothing to restore" is an answer a person can
    still abort; skipping the question on an empty library would also make the
    one library that most needs asking the one that is never asked.

    A TARGET SELECTS NO CAPTURE AT ALL, and the line that does it is the second
    half of ``_restore_target``'s refusal rather than a separate policy. That
    function refuses a target beside a NAMED session; this is the other way a
    capture gets into a run, which is the default, where a bare invocation means
    the newest restorable one. Leaving the default in place would take a person
    who asked to rehearse a database restore into a scratch directory and roll
    the live library back to a session as well, which is the destructive act the
    flag exists to avoid, chosen by nobody.
    """
    cfg = _load()
    target = _restore_target(cfg, ctx.args)
    _refuse_pull_flags_without_the_pull(ctx.args)
    requested = ctx.args.session_id
    chosen: restore.Restorable | None = None
    if target is not None:
        chosen = None
    elif requested is None:
        chosen = _newest_restorable(cfg)
    else:
        chosen = _named(cfg, requested)

    pulling = _snapshot_offered(cfg, ctx.args) if ctx.args.from_backup else None
    offered = _offer(
        chosen,
        discarding=tuple(ctx.args.discard),
        from_backup=ctx.args.from_backup,
        snapshot=pulling,
        include_mirror=ctx.args.include_mirror,
        snapshot_volume=ctx.args.snapshot_volume,
        target=target,
        dry_run=ctx.args.dry_run,
    )
    spec = _confirm_gate(ctx.entry)
    # SHOWN AS WELL AS DIGESTED. The digest makes a stale answer refusable; it
    # does not put anything in front of the person answering, and "restore from
    # the snapshot taken when, and whose" is the question. A display value and
    # never an input, exactly as the gate's own docstring describes it: the
    # digest above already carries every field of it.
    shown = (
        {"off_machine": next(i for i in offered["items"] if i["half"] == "off-machine")}
        if pulling is not None
        else None
    )
    option = ctx.gate.require(spec, digest=offered["digest"], context=shown)
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)

    report = restore_under_one_session(
        cfg,
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
        dry_run=ctx.args.dry_run,
        from_backup=ctx.args.from_backup,
        # THE STAMP THAT WAS OFFERED, not the flag. Handing the flag down would
        # let the engine resolve the newest snapshot a second time, after the
        # approval, which is the move the digest was just made to catch.
        # ``accept_unrecorded`` goes with it for the reason
        # ``backup.ResolvedSnapshot`` gives: a stamp that came off a listing
        # must not arrive looking like one a person typed.
        snapshot=pulling.stamp if pulling is not None else None,
        snapshot_volume=ctx.args.snapshot_volume,
        accept_unrecorded=pulling.named if pulling is not None else None,
        include_mirror=ctx.args.include_mirror,
        target=target,
    )
    return ctx.envelope(data=_performed(report, offered))


# ---------------------------------------------------------------------------
# restore bare-metal
# ---------------------------------------------------------------------------

#: The two halves of a bare-metal recovery, as the report and a refusal name
#: them. The music and everything else the mirror carried, then the database and
#: the companions a restore writes back, which is the source system's order and
#: the only order in which a failure of the first leaves nothing of the second.
MIRROR_HALF = "mirror"
DATABASE_HALF = "database"


def build_bare_metal(parser, entry) -> None:
    """Declare the recovery's arguments. The parameters are unannotated on purpose.

    ``--target`` IS REQUIRED AND HAS NO DEFAULT. The source system defaulted its
    destination to the configured volume, which is the one directory this verb
    can never be pointed at: the engine refuses unless that volume is gone, and
    the path it was mounted at is then the empty folder on the internal disk the
    stub check exists for.

    ``--accept-replacement`` IS THE ACKNOWLEDGMENT, and it is a flag because
    there is nothing else it could be. Every other destructive restore is
    answered by a decision recorded against a run, beside an acknowledgment
    recorded beside the library, and the second of those is on the volume that
    died. The engine says what the substitute is worth and refuses an invocation
    with no controlling terminal, so the flag is typed by a person or not at all.

    THERE IS NO FLAG THAT NAMES AN OCCUPIED TARGET FOR REPLACEMENT. The engine
    has the parameter and this verb never passes it, so a target that already
    holds a database is always refused.
    """
    del entry
    parser.add_argument(
        "--target",
        required=True,
        metavar="DIRECTORY",
        help=(
            "the mounted replacement volume to recover onto; it must exist, hold "
            "no database, and not be the folder the lost volume left behind"
        ),
    )
    parser.add_argument(
        "--accept-replacement",
        action="store_true",
        dest="accept_replacement",
        help=(
            "accept that a whole library is written onto the target; refused "
            "without it, and refused with it when nobody is at a terminal"
        ),
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        metavar="STAMP",
        help="which dated off-machine snapshot to pull; the newest by default",
    )
    parser.add_argument(
        "--snapshot-volume",
        default=None,
        dest="snapshot_volume",
        metavar="IDENTITY",
        help=(
            "the volume identity the snapshot is expected to record, when it is "
            "not the one this installation remembers; used once, never recorded"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="rehearse both halves and transfer nothing, under the same gates",
    )
    parser.set_defaults(_handler=perform_bare_metal)


@dataclass(frozen=True, slots=True)
class BareMetalReport:
    """What one recovery did, a half at a time.

    ``mirror`` and ``database`` are the transfers that RAN, by label, read off
    the results rather than off the plan, for the reason
    :func:`restore_under_one_session` gives. ``target`` is the directory the
    session authorised, which is the only place either half was pointed.
    """

    target: Path
    database_target: Path
    mirror: tuple[str, ...]
    database: tuple[str, ...]
    dry_run: bool
    absent: tuple[str, ...] = ()
    snapshot: str | None = None
    recorded_volume: str | None = None


def _halves(decided: backup.RestorePlan) -> tuple[tuple[str, backup.RestorePlan], ...]:
    """One plan, read as the two halves it already holds. Nothing is re-planned.

    ``backup.run_restore`` RUNS EVERY COMMAND BEFORE IT READS A RETURN CODE, so
    handing it the whole plan lets the database land after the mirror failed. On
    the live library that is a restore to run again. Here it is a dead end: a
    target holding a database is refused outright and this verb has no flag that
    names one for replacement, so the rerun the failure asks for is the one thing
    it has just made impossible. Spent a half at a time, a mirror that fails
    leaves no database behind it.

    THE SPLIT IS BY LABEL AND KEEPS THE PLAN'S ORDER, so it cannot disagree with
    the plan about what is transferred. Every other field rides along unchanged,
    which means the companions are cleared before each half exactly as the
    engine clears them before the whole.
    """
    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
    database = tuple(c for c in decided.commands if c.label != backup.RESTORE_MIRROR)
    return (
        (MIRROR_HALF, replace(decided, commands=mirror)),
        (DATABASE_HALF, replace(decided, commands=database)),
    )


def _half_failed(
    exc: backup.BackupRefused,
    half: str,
    *,
    completed: Sequence[str],
    decided: backup.RestorePlan,
    dry_run: bool,
) -> CratekitError:
    """A refusal from inside one half, saying which half and what is on the target.

    THE RESERVED SENTENCE FOR A FAILED TRANSFER IS FALSE HERE, which is why it
    is not reused. It says the live companion files were cleared and tells the
    person to run the restore again. Nothing was cleared, because the target
    held no database, and whether a rerun is possible depends on which half
    failed. The slug and its exit code are kept; the engine's own sentence,
    which carries the return code, rides in the detail.
    """
    slug = str(exc.refusal)
    detail: dict[str, Any] = {
        "refusal": slug,
        "half": half,
        "completed_halves": list(completed),
        "target": str(decided.target),
        "dry_run": dry_run,
        "engine": exc.detail,
    }
    if exc.refusal is not backup.Refusal.RESTORE_TRANSFER_FAILED:
        return CratekitError(
            Cause(
                reason=slug,
                message=exc.detail,
                remediation=reservations.remediation_for(slug),
                origin=("modules.tools.backup", "session.restore_cli"),
                detail=detail,
            )
        )
    if dry_run:
        message = (
            f"the rehearsal's {half} half failed against the remote and nothing "
            f"was written to {decided.target}"
        )
        steps = ("check the remote is reachable, then rehearse again",)
    elif half == MIRROR_HALF:
        message = (
            f"the mirror half of the recovery onto {decided.target} failed part "
            f"way, and the database half was not attempted, so the target holds "
            f"no database from this run"
        )
        steps = (
            "check the remote is reachable, then run the recovery again; files "
            "that already arrived are not transferred twice",
            "if the rerun is refused because the target holds a database file "
            "the mirror carried, move that file aside and run it again",
        )
    else:
        message = (
            f"the mirror half completed and the database half of the recovery "
            f"onto {decided.target} failed, so {decided.database_target.name} or "
            f"one of its companions may have arrived without the rest"
        )
        steps = (
            f"do not open the library; remove {decided.database_target} and its "
            f"companion files, because a target holding a database is refused",
            "check the remote is reachable, then run the recovery again; the "
            "mirror that already arrived is not transferred twice",
        )
    return CratekitError(
        Cause(
            reason=slug,
            message=message,
            remediation=Remediation(steps=steps),
            origin=("modules.tools.backup", "session.restore_cli"),
            detail=detail,
        )
    )


def recover_under_bare_metal_session(
    cfg: config.Config,
    *,
    target: Path | str,
    accepted: bool,
    dry_run: bool = False,
    snapshot: str | None = None,
    snapshot_volume: str | None = None,
    terminal: object | None = None,
    identity_provider: object | None = None,
    mount_enumerator: object | None = None,
    mount_probe: object | None = None,
    runner: object | None = None,
    process_lister: object | None = None,
) -> BareMetalReport:
    """The mirror and the database, onto a replacement drive, inside ONE session.

    THIS IS THE CALLER :func:`cratekit.core.restore.bare_metal_session` WAITED
    FOR. That guard substitutes the three library-scoped gates, which all sit on
    the disk that died, and says what each substitute is worth. Nothing here
    softens one: the library must be genuinely gone, the target must be a real
    filesystem holding no database, a person must be at a terminal, and
    ``accepted`` is the acknowledgment. All four are the engine's refusals and
    are raised before its lock is taken, so a refused recovery leaves the disk
    as it found it.

    ``held.guard`` IS THE ``gates`` SEAM FOR BOTH ENGINE CALLS, for the reason
    :func:`restore_under_one_session` gives, and with one more here: left to
    default, ``backup.plan_restore`` would ask for the library-scoped gates and
    refuse with an instruction to mount the volume this verb exists to replace.

    THE TARGET HANDED DOWN IS ``held.authorises`` AND NEVER THE ARGUMENT. The
    session validated one directory and carries it; reading the path off the
    value rather than off the invocation is what makes that validation the only
    place a path can come from.

    ``confirmed=True`` IS NOT A SECOND DECISION. The block below is reached only
    through a session the engine opened over an explicit acknowledgment at a
    terminal, and ``plan_restore``'s parameter is how a caller states that a
    named decision exists (R33).

    NO SESSION IS ROLLED BACK. The session log and every capture were on the
    lost volume, so there is nothing for a plan to read. What arrives is the
    library as the last backup saw it.

    A REHEARSAL PASSES THE SAME GATES, acknowledgment included, for the reasons
    ``backup.run_restore`` gives for the live restore.
    """
    with restore.bare_metal_session(
        cfg,
        target=target,
        acknowledged=accepted,
        terminal=terminal,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
        mount_probe=mount_probe,
    ) as held:
        try:
            decided = backup.plan_restore(
                cfg,
                target=held.authorises,
                confirmed=True,
                snapshot=snapshot,
                snapshot_volume=snapshot_volume,
                include_mirror=True,
                gates=held.guard,
                **_seam("runner", runner),
                **_seam("process_lister", process_lister),
            )
        except backup.BackupRefused as exc:
            raise _refused(exc) from exc
        ran_labels: dict[str, tuple[str, ...]] = {}
        for half, portion in _halves(decided):
            try:
                ran = backup.run_restore(
                    portion,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
                    **_seam("runner", runner),
                )
            except backup.BackupRefused as exc:
                raise _half_failed(
                    exc,
                    half,
                    completed=tuple(ran_labels),
                    decided=decided,
                    dry_run=dry_run,
                ) from exc
            ran_labels[half] = tuple(
                command.label
                for command, _result in zip(portion.commands, ran, strict=True)
            )
        return BareMetalReport(
            target=decided.target,
            database_target=decided.database_target,
            mirror=ran_labels[MIRROR_HALF],
            database=ran_labels[DATABASE_HALF],
            dry_run=dry_run,
            absent=decided.absent_sidecars,
            snapshot=decided.snapshot,
            recorded_volume=decided.recorded_volume,
        )


def _recovered(report: BareMetalReport) -> dict[str, Any]:
    """The recovery as a ``plan/1`` payload, one item per transfer, named by half.

    EACH HALF HAS ITS OWN COUNT, so a report cannot fold hundreds of gigabytes
    of music and one database into a single number that says neither.

    THE DIGEST IS AN IDENTITY AND AUTHORISES NOTHING. This verb declares no
    gate, so no recorded decision is ever compared with it; it is here because
    the schema carries one and because two reports over the same recovery
    should say so.
    """
    items: list[dict[str, Any]] = [
        {"half": MIRROR_HALF, "transfer": label} for label in report.mirror
    ]
    items += [{"half": DATABASE_HALF, "transfer": label} for label in report.database]
    return {
        "digest": digest_of(
            {
                "kind": "restore.bare-metal",
                "target": str(report.target),
                "snapshot": report.snapshot,
                "recorded_volume": report.recorded_volume,
                "dry_run": report.dry_run,
            }
        ),
        "items": items,
        "totals": {
            "mirror_transfers": len(report.mirror),
            "database_transfers": len(report.database),
            "dry_run": report.dry_run,
            "absent_sidecars": list(report.absent),
            "snapshot": report.snapshot,
            "recorded_volume": report.recorded_volume,
            "target": str(report.target),
            "database_target": str(report.database_target),
        },
        "chunk": None,
    }


def perform_bare_metal(ctx) -> Envelope:
    """Recover the mirror and the database onto the named replacement drive.

    NO GATE IS ASKED, and the registry entry says why at length. The short form:
    the acknowledgment a recorded decision would sit beside is on the lost
    volume, the flag is the explicit act, and the engine refuses it from an
    invocation nobody is sitting at.

    THE PATH IS MADE ABSOLUTE AND NOTHING ELSE. Every judgement about the
    target, that it exists, that it is a filesystem of its own, that it holds no
    database, is the engine's, made once under its own name.
    """
    cfg = _load()
    report = recover_under_bare_metal_session(
        cfg,
        target=Path(ctx.args.target).expanduser().absolute(),
        accepted=ctx.args.accept_replacement,
        dry_run=ctx.args.dry_run,
        snapshot=ctx.args.snapshot,
        snapshot_volume=ctx.args.snapshot_volume,
    )
    return ctx.envelope(data=_recovered(report))


def _snapshot_offered(cfg: config.Config, args) -> backup.ResolvedSnapshot:
    """Which snapshot this restore would pull, asked of the remote BEFORE the gate.

    THIS IS THE ONE PLACE THE VERB REACHES THE NETWORK BEFORE IT IS ANSWERED,
    and it is reached only when the off-machine pull was asked for. A restore
    that spends a local capture still touches nothing before its gate. The cost
    of asking early is two listings; the cost of not asking was an approval that
    did not say which database it approved.

    AN UNREACHABLE REMOTE THEREFORE REFUSES THE OFFER rather than the run, which
    loses nothing: the run would have refused on the same listing a moment
    later, after a person had been asked to approve a restore that could not
    happen.

    The engine checks all of this again under the gates. What is decided here is
    what the person is SHOWN; what is decided there is what is allowed.
    """
    try:
        return backup.resolve_snapshot(
            cfg, snapshot=args.snapshot, snapshot_volume=args.snapshot_volume
        )
    except backup.BackupRefused as exc:
        raise _refused(exc) from exc


__all__ = [
    "DATABASE_HALF",
    "LISTING",
    "MIRROR_HALF",
    "BareMetalReport",
    "RestoreReport",
    "build_bare_metal",
    "build_list",
    "build_run",
    "list_restorable",
    "perform_bare_metal",
    "perform_restore",
    "recover_under_bare_metal_session",
    "restore_under_one_session",
]
