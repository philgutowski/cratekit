"""``crate session ack`` and ``crate session release``: minting and unsticking.

WHAT THIS MODULE IS FOR. Every destructive thing this product does goes through
:func:`cratekit.core.session.assert_gates`, which calls
:func:`cratekit.core.session.assert_backup_acknowledged`, which refuses unless a
recorded acknowledgment is inside its validity window. Until this file existed,
:func:`cratekit.core.session.record_acknowledgment` had no caller anywhere in
``src`` or ``scripts``, so nothing a person could type could produce that record
and every write, every trash and every restore in the product refused. The suite
was green the whole time because tests mint through the core API directly, which
is the shape ``docs/solutions/workflow-issues/a-guard-safe-only-because-its-
subject-is-unimplemented-expires-when-it-lands.md`` was written about: a guard
measured in a world where its premise could not fail.
:func:`cratekit.core.session.release_stale_lock` was in the same state, so a lock
left behind by an installation that is gone could only be cleared by editing a
file by hand.

THE VERBS ARE THE REGISTRY'S, NOT THIS FILE'S. Both entries have been declared
since U8 with their module path, their builder names, their handler keys, their
emitted schema and one explicit gate each. This unit implements that declaration
and changes none of it, including a gate prompt that asks about a holder the
release path may already know is absent. A unit that lands a declared module and
edits the declaration in the same commit cannot say afterwards which half its
tests were measuring, so the wording stands and the observation is in the ledger
instead.

WHAT ``session.release`` IS. It releases the LIBRARY LOCK, not the
acknowledgment. The registry's summary says "release a library lock whose holder
is gone, explicitly", its gate prompt says "Release the lock held by another
installation?", and ``release_stale_lock`` is the engine that answers exactly
that. The issue this unit came from described the verb as releasing what ``ack``
recorded; the registry is what the dispatcher reads and the issue is a
description of it, so the registry wins. The consequence, that no verb withdraws
an acknowledgment inside its window, is recorded rather than left in a closed
issue.

THE FACTS ARE READ BEFORE THE GATE IS ASKED, in both verbs, and the ordering is
forced. A gate's prompt is fixed at declaration and cannot name a backup age or
a lock holder, so what a person is deciding over has to ride on the refusal
(:class:`cratekit.cli.gates.DecisionRequired`). Reading after the answer would
put the facts in the report of a decision already made. It also means an ABSENT
fact file must not refuse here, or the verb would be unreachable on exactly the
library that has never been backed up, which is every library before its first
backup. An UNREADABLE one does refuse, carrying the remedy the exception raised
rather than a token chosen here, because ``backup_facts.Remedy`` declares three
and one of them is a permission on a directory, which repairing a file does not
touch.

NEITHER VERB OPENS A SESSION AND NEITHER DECLARES A WRITE. ``session.ack``
opening one would need the acknowledgment it exists to create, which is a verb
that can never run on the library it is for. ``session.release`` acquires the
lock file directly through the engine and gives it straight back.

``session.release`` ALSO ENDS WHAT A DEAD HOLDER LEFT OPEN (R-598). A gated
write that was hard killed ran no exit code, so its session record stays open,
keeps its capture from retention and refuses every cutover. The record names the
process that held the lock, and once that process is provably gone the record is
abandoned here, through the ungated close. It is the same proof this verb
already makes about the lock, so it is the same verb.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, and that one is foundation-ranked under KTD25 for the reason
``session.restore_cli`` gives beside it: a modules-layer file reaching for
``registry.Entry`` to annotate a builder is the layering violation KTD23
refuses, while the output contract is ranked below every verb on purpose.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import backup_facts, config, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token rides through from the configuration error that raised it,
    so "no config at all" and "config written by a newer build" keep their
    different answers all the way out to the shell (D2). Copied in shape from
    ``session.restore_cli._load``, the sibling in this package.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("session", "cli"),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _gate(entry, name: str):
    """The gate this verb asks, looked up BY NAME off the entry.

    By name rather than by index, because ``gates[0]`` binds a handler to the
    order the specs happen to be written in and asks the wrong question the day
    somebody adds a second one. ``entry`` is unannotated for the layering reason
    the module docstring gives.
    """
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate called {name!r}, so there is no "
                f"question to ask before it acts"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("session", "cli"),
            detail={"verb": entry.name, "gate": name},
        )
    )


# ---------------------------------------------------------------------------
# session ack
# ---------------------------------------------------------------------------


def build_ack(parser, entry) -> None:
    """Declare the verb's arguments, which are none. Parameters unannotated.

    THERE IS NO ``--yes``, NO ``--actor`` AND NO ``--hours``. R34's sharpest
    clause is that a caller must not be able to name who acknowledged or to
    assert the answer, because an agent driving the command line would then mint
    the gate protecting the one operation that removes files and the audit trail
    would record whatever name it chose. ``record_acknowledgment`` has no
    parameter that could carry either, and this shell adds none.
    """
    del entry
    parser.set_defaults(_handler=record_ack)


def _rendered_ages(cfg: config.Config, now: datetime) -> list[dict[str, Any]]:
    """The published backup ages, read from the FACT FILE and rendered for here.

    ONE SOURCE, PER SURFACE RENDERING, which is the rule
    ``cratekit.backup.cli.published_ages`` states for itself: "The SOURCE is
    shared with :func:`cratekit.core.session._shown_ages`, which is the thing
    that must not be duplicated. The rendering is per surface." This is the
    fourth consumer of :func:`cratekit.core.backup_facts.ages` and it answers
    from the same file as the other three, so what this refusal shows and what
    the acknowledgment records cannot disagree about where they came from.

    AND THE REMEDY TRAVELS. ``read_facts`` distinguishes a permission from a
    damaged file from a newer schema at three separate raise sites, and naming
    one token over all three is the defect R-201 recorded on this exact path: a
    person whose configuration directory this account cannot traverse being told
    to repair or reset the record of when their music was last protected. This
    is spelled the way ``cli.doctor`` and the backup shell spell it.
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
            f"the backup ages this acknowledgment has to show cannot be read: "
            f"{exc}. Asking a person to acknowledge now would ask them over a "
            f"clean sheet nobody has seen",
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    return [
        {
            "portion": str(entry.portion),
            "state": str(entry.state),
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
            "completed_at": (
                entry.completed_at.isoformat() if entry.completed_at is not None else None
            ),
        }
        for entry in reported
    ]


def _on_record(cfg: config.Config, now: datetime) -> dict[str, Any] | None:
    """The acknowledgment currently on record, or None when there is none.

    FOUR STATES AND NOT TWO. Absent, live, expired and unreadable are different
    facts with different next moves, and a person deciding whether to
    acknowledge again is entitled to know which one they are in before they
    answer rather than after. Expired is reported with the moment it lapsed
    rather than as absent, for the reason ``read_acknowledgment`` gives about its
    own file: reporting one condition as another sends somebody to redo
    something already done.

    AN UNREADABLE RECORD IS DESCRIBED HERE AND NOT RAISED, which is the opposite
    of what this function does with an unreadable BACKUP FACT file, and the
    asymmetry is the point. The ages are the thing a person is being asked to
    decide over, so showing a clean sheet nobody saw would be a lie. This record
    is not being decided over at all: it is context, and this verb OVERWRITES it
    unconditionally a few lines later. Letting the read raise would mean a
    library whose acknowledgment file somebody corrupted could never be
    acknowledged again, because the one command that replaces the file refuses
    before it gets there. That is a trap with no exit, and it costs more than the
    thing it protects.
    """
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
    if recorded is None:
        return None
    return {
        "actor": recorded.actor,
        "recorded_at": recorded.recorded_at.isoformat(),
        "expires_at": recorded.expires_at.isoformat(),
        "valid": recorded.valid_at(now),
    }


def record_ack(ctx) -> Envelope:
    """Show the ages, ask the question, and record the answer as a separate act.

    THE SHAPE IS TWO INVOCATIONS AND THAT IS R34, not an ergonomic accident. The
    gate is ``explicit``, so the invocation that discovers it cannot answer it:
    it exits DECISION_REQUIRED naming the run, a person answers with ``crate run
    decide``, and a later invocation resumes with ``--run``. An affirmative that
    could be typed on the command that raised the question is a blanket flag
    wearing a different name.

    IT RE-MINTS ON EVERY ANSWERED DRIVE and does not refuse because a live
    record exists. ``record_acknowledgment`` overwrites unconditionally, and a
    freshness check added here would be a second rule about one record living in
    a different file from the rule it copies.

    THE ACT NEEDS A PERSON AT A TERMINAL, and that refusal comes from the engine
    rather than from anything here. It is what stops a detached job from minting
    the gate that protects every destructive verb.
    """
    cfg = _load()
    now = datetime.now(timezone.utc)
    shown = _rendered_ages(cfg, now)
    spec = _gate(ctx.entry, "session.ack.backup")
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )
    # THE SAME MOMENT, handed down rather than taken again. Without it
    # ``record_acknowledgment`` reads its own clock and derives the record's
    # ``shown`` list from that instant instead of this one. ``now`` is the ONLY
    # thing handed over: there is deliberately no way to tell that function what
    # a person was shown, because a caller that could say so could say anything,
    # which is the same clause that keeps the actor out of its signature.
    acknowledgment = session.record_acknowledgment(cfg, now=now)
    # AND THE REPORT COMES FROM THE RECORD, not from the read above it. Both
    # describe the same portions and after ``now=now`` they agree, but they are
    # two reads of one file and only one of them is the thing that was written
    # down. Rendering ``checks`` from ``shown`` and ``summary`` from the record
    # would put two answers to one question in one payload, separated by however
    # long the write took, and that is the drift this whole layer exists to
    # remove. What the person is told is what a destructive session will consult.
    recorded_ages = [entry.to_json() for entry in acknowledgment.shown]
    # THE DECISION IS SPENT. R34 asks for a deliberate act per acknowledgment,
    # and a recorded answer that survives the mint is not that: a run identifier
    # kept from an earlier session could be re-driven at any later time and each
    # drive would restart the validity window with nobody asked again, which
    # ``DEFAULT_ACK_VALIDITY`` calls "a permanent affirmative wearing a
    # timestamp". Popped HERE rather than in the resolver, so what a recorded
    # answer means for every other gate in the product is untouched: this is one
    # verb deciding that its own authorisation is single use, which is a
    # property of what it mints rather than of the gate machinery.
    ctx.run.decisions.pop(spec.name, None)
    return ctx.envelope(
        data={
            "checks": [
                {
                    # ``key``, because that is the field ``cli.render``'s check
                    # table reads. A row keyed ``name`` renders as "[ok] ?" and
                    # the person is shown a question mark where the portion
                    # should be, on the one surface they read without asking for
                    # JSON.
                    "key": f"backup.age.{entry['portion']}",
                    "status": "ok",
                    "detail": entry["state"],
                }
                for entry in recorded_ages
            ],
            "summary": {
                "recorded": True,
                "actor": acknowledgment.actor,
                "recorded_at": acknowledgment.recorded_at.isoformat(),
                "expires_at": acknowledgment.expires_at.isoformat(),
                "shown": recorded_ages,
            },
        }
    )


# ---------------------------------------------------------------------------
# session release
# ---------------------------------------------------------------------------


def build_release(parser, entry) -> None:
    """Declare the verb's arguments, which are none. Parameters unannotated.

    No ``--force``. Which holders are releasable is the engine's judgment, made
    from whether the recorded process is still running, and a flag that overrode
    it would be one run clearing another run's claim on the library mid-write.
    """
    del entry
    parser.set_defaults(_handler=release_lock)


def release_lock(ctx) -> Envelope:
    """Show the holder, ask the question, and clear a claim whose owner is gone.

    FOUR OUTCOMES, because ``release_stale_lock`` has four and a shell that
    reported three would collapse two of them. Nothing recorded is a no-op. A
    holder still running refuses ``session-lock-held`` with WAIT_FOR_HOLDER. A
    holder that is gone whose lock file still cannot be taken refuses the same
    way, and it is the least obvious of the four: the record is stale and
    something else is holding the file anyway. Only the fourth clears anything.

    NOTHING RECORDED IS AN OUTCOME, NOT A FAILURE. It is the state of every
    healthy library, and refusing there would report a working machine as a
    broken one and hand a person a remedy for a condition with no remedy. That
    is ``restore_cli.perform_restore``'s decision for the same shape.

    THE GATE STILL FIRES WHEN THERE IS NOTHING TO RELEASE. Conformance 3 holds
    every declared gate to firing, and a verb that skipped its question on the
    quiet path would be a verb whose question is asked only when the answer
    matters least. The declared prompt asserts a holder that may not be there,
    which is recorded in the ledger rather than reworded here.
    """
    cfg = _load()
    path = session.lock_path(cfg)
    holder = session.read_lock_holder(path)
    # A LOCK FILE WITH NO READABLE HOLDER IS ITS OWN STATE, and the shell has to
    # say so because the engine cannot. ``read_lock_holder`` answers None for
    # "nobody holds this" and None again for "there is a file here I could not
    # understand", and those have different next moves: the first is a healthy
    # library and the second is a record somebody should look at. Reporting the
    # second as the first tells a person nothing is wrong on the one surface
    # that could have told them something is.
    unreadable = holder is None and path.exists() and bool(path.read_bytes().strip())
    # THE OPEN RECORDS A DEAD HOLDER LEFT ARE SHOWN BEFORE THE QUESTION (R-598),
    # for the reason the holder is: the person decides over what will be ended.
    orphans = [record for record in session.records(cfg) if session.orphaned(record)]
    spec = _gate(ctx.entry, "session.release.confirm")
    option = ctx.gate.require(
        spec,
        context={
            "holder": holder.to_json() if holder is not None else None,
            "record": "unreadable" if unreadable else ("present" if holder else "absent"),
            "orphans": [
                {"session_id": record.session_id, "workflow": record.workflow}
                for record in orphans
            ],
        },
    )
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"released": False, "aborted": True}},
            outcome=Outcome.NO_OP,
        )
    # THE LOCK FIRST, so a holder still running refuses before any record is
    # ended behind it. The records are judged again rather than taken from the
    # list shown: the answer may come long after the question.
    cleared = session.release_stale_lock(cfg)
    abandoned = [record.session_id for record in session.abandon_orphaned_sessions(cfg)]
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
    # ``key``, for the reason the acknowledgment's rows give: it is the field the
    # check table renders and ``name`` prints as a question mark.
    checks = [
        {
            "key": "session.record",
            "status": "ok",
            "detail": f"abandoned {session_id}, its holder is gone",
        }
        for session_id in abandoned
    ]
    if cleared is None:
        return ctx.envelope(
            data={
                "checks": checks,
                "summary": {
                    "released": False,
                    "recorded": False,
                    "unreadable": unreadable,
                    "abandoned": abandoned,
                    "kept": kept,
                },
            },
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
        )
    return ctx.envelope(
        data={
            "checks": [
                {"key": "session.lock", "status": "ok", "detail": cleared.describe()},
                *checks,
            ],
            "summary": {
                "released": True,
                "holder": cleared.to_json(),
                "abandoned": abandoned,
                "kept": kept,
            },
        }
    )


__all__ = [
    "build_ack",
    "build_release",
    "record_ack",
    "release_lock",
]
