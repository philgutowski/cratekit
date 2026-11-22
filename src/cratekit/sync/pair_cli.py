"""``crate sync pair``: keep the author's own account playlist and its rekordbox playlist one list.

U130. Each side is merged against the last sync (``sync/pair_merge.py``), so a
removal on either side lands on both, as an addition does, and a first sync,
having no base, adds only. A pair holds one of the author's own account
playlists and one plain rekordbox playlist, each named by its identifier, never
its name (R-906). Refused before any track is read: the hearts, a label's, a
set's or a mirrored playlist, the source system's debris and placeholders, a
rekordbox folder or smart playlist, and anything under Cratekit's own trees,
since those lists already have a writer. A pair is named with
``crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID`` and recorded when its
first sync is approved (``modules/outbound/pairs.py``); with no argument every
marked pair syncs.

A sync of every pair also pairs each plain rekordbox playlist the author made
outside Cratekit's trees, Favorites and ``outbound.pair_skip_folders`` with an
account playlist it makes (U198, ``sync/pair_discover.py``), and makes in
rekordbox each playlist made on the account in a synced folder (U202,
``sync/pair_reverse.py``). A playlist a folder already held when it was adopted,
and a downloaded copy of a paired one, are named and never made (U216). A made
pair that loses a side is unpaired and its survivor released, so it is never
made again.

A track is matched through a recorded link, else on its ISRC, the database's
and else its file's; an unmatched row is named and stays. An ISRC naming
several agreeing releases takes the hearted one, else the lowest numbered
(U208). An account track the library lacks is queued once through
``intake.playlist``, never written as a row without a file, and a track any
pair already queued awaits it (R-1385); a twin's missing tracks are held for the
author's choice until ``crate sync release`` (U221). Where one side added a
track and the other removed it, the later change wins (U202); the account keeps
no removal date, so its removal never beats an addition, and a moment unknown
keeps the track.

Two gates, ``sync.pair.rekordbox`` and ``sync.pair.account``, each show the
whole plan and answer for their own side before anything is written; rekordbox
is written first, behind the backup acknowledgment. The snapshot moves only when
both sides were applied, every write landed and the account listed the whole
playlist, so anything less merges again against the same base and the next sync
finishes it. A short account listing removes and reorders nothing, since a
withheld track would read as removed. A track listed with no title or artist is
unread, kept by its id in its place, and the pair still syncs whole, since the
provider may list it so for good (R-1264, R-1446); a row with no provider id
leaves its pair out.

One plan per run (U209), held by the command that plans (``core/held_plan.py``)
and read back by digest in its later commands, and :func:`check` refuses
``decision-stale`` before the first write when a list it read has moved. The
write records each step as it lands (U210), so a continue starts each pair at
its first unfinished step and never makes a side twice. A fresh plan reads
every run's kept steps (U225, ``sync/pair_stopped.py``), so a write stopped part
way through its account order is finished rather than its moves read as the
person's reorder, an account off those moves' path leading only once settled
readings show it moved (U234), and a first sync reads such a stop too (R-1376).

Layer: modules.
"""

from __future__ import annotations

import shlex
from collections.abc import Sequence
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, session
from cratekit.core.cause import CratekitError, Outcome
from cratekit.sync import cli as sync_cli
from cratekit.sync import pair_calls
from cratekit.sync.pair_check import (
    GATES,
    HELD_KIND,
    REPLANNED,
    Moved,
    _asked,
    _calls_said,
    _held_plan,
    _hold,
    _release,
    _spent,
    _steps_of,
    _with_calls,
    check,
)
from cratekit.sync.pair_model import (
    ACCOUNT_GATE,
    AMBIGUOUS,
    APPLY,
    AWAITING,
    BROUGHT_REASONS,
    FINISHING,
    FOLDER_ADOPT,
    FOLDER_CREATE,
    INTAKE_HANDLER,
    LANDING_UNREAD,
    LANDING_UNREAD_ACTION,
    LATER_CHANGE,
    LEFT_OUT,
    NEW,
    NO_ISRC,
    NOT_BROUGHT,
    NOT_DISCOVERED,
    NOTHING,
    ON_HOLD,
    ON_HOLD_ACTION,
    ORDER_FOLDER,
    ORDER_REFUSALS,
    OWNED_STATE,
    PAIR_SOURCE,
    PENDING,
    QUEUED_HERE,
    REKORDBOX_GATE,
    RELEASED,
    SETTLING,
    SKIPPED,
    STEP_ACCOUNT,
    STEP_DONE,
    STEP_MADE,
    STEP_MAKING,
    STEP_MOVED,
    STEP_MOVING,
    STEP_ORDER_REFUSED,
    STEP_ORDERING,
    STEP_QUEUED,
    STEP_REKORDBOX,
    STEPS_UNWRITTEN,
    STOPPED_UNREAD,
    TIME_UNKNOWN,
    UNMATCHED,
    UNPAIRED,
    UNREAD,
    WITHHELD,
    WRITTEN,
    Named,
    PairPlan,
    Place,
    Target,
    generated_tops,
    targets,
)
from cratekit.sync.pair_model import _scope_account as _scope_account  # noqa: PLC0414
from cratekit.sync.pair_plan import (
    AGREE_AFTER,
    held_for_choice,
    plan_pair,
)
from cratekit.sync.pair_read import (
    file_identity,
    landed_inbox_playlists,
    landed_isrcs,
    pair_jobs,
)
from cratekit.sync.pair_screen import (
    Plan,
    Unpaired,
    _warnings,
    facts,
    payload,
    plan,
)
from cratekit.sync.pair_write import (
    SETTLE_SECONDS,
    Done,
    PairSteps,
    _settle,
    apply_pair,
    steps_unwritten,
)


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "account",
        nargs="?",
        default=None,
        metavar="ACCOUNT_PLAYLIST",
        help=(
            "the account playlist's identifier; with no argument every marked "
            "pair is synced"
        ),
    )
    parser.add_argument(
        "--rekordbox",
        default=None,
        metavar="PLAYLIST_ID",
        help=(
            "the rekordbox playlist's identifier, to mark a new pair; a marked "
            "pair needs none"
        ),
    )
    parser.set_defaults(_handler=sync_pair)



#: U210. Warnings for pairs an earlier command of the run finished, and for
#: steps that could not be read.
RESUMED = "sync-pair-resumed"

STEPS_UNREAD = "sync-pair-steps-unread"


#: The verb's own words, for a command line named when the run kept none.
VERB_PATH = ("sync", "pair")



def _expected(planned: Plan, steps: Any) -> tuple[int, int]:
    """The calls the writing command is expected to make, the check's and the write's (U210).

    Counted from what is LEFT, so at a continue a finished pair costs nothing
    and a made playlist only its filling; a rekordbox write makes no call.
    """
    left = [one for one in planned.pairs if not _steps_of(steps, one).has(STEP_DONE)]
    check_calls = pair_calls.check(left, create=FOLDER_CREATE)
    # A FOLDER THIS RUN BEGAN A MADE PAIR IN EXISTS ALREADY, so the rest make none.
    begun_in = {
        one.place.folder
        for one in planned.pairs
        if one.place is not None and _steps_of(steps, one).has(STEP_MAKING)
    }
    write_calls = pair_calls.folders_made(
        [one for one in left if one.place is None or one.place.folder not in begun_in],
        FOLDER_CREATE,
    )
    for one in left:
        made = one.target.new and bool(_steps_of(steps, one).get(STEP_MADE))
        if made:
            # The check reads its listing like any paired playlist's, with the
            # unpaged read beside it (U226).
            check_calls += pair_calls.judged_calls(0)
        write_calls += pair_calls.pair_write(
            one, made_before=made, sent=_steps_of(steps, one).has(STEP_MOVING)
        )
    return check_calls, write_calls



def _ceiling(cfg: config.Config) -> int:
    """The call ceiling this command runs under: ``--calls`` when given, else the configured."""
    from cratekit.core import provider_gate

    return provider_gate.ceiling(provider_gate.GateSettings.from_config(cfg))



def _stopped(
    cause: Any,
    planned: Plan,
    steps: Any,
    *,
    run_id: str,
    argv: Sequence[str] | None,
    cfg: config.Config,
) -> Any:
    """A park raised in the check or the write, said with how far the run got (U210).

    A stop on the call ceiling names the run and a ``--calls`` sized from what
    is left, never below the ceiling it stopped at.
    """
    import dataclasses

    from cratekit.core import provider_gate

    if steps is None:
        # NOTHING WAS RECORDED, so a continue would refuse stale on the lists
        # this write moved; no run is named.
        return dataclasses.replace(
            cause,
            message=(
                f"{cause.message}; this run's plan could not be held, so the steps it "
                f"wrote were not recorded and it cannot be continued: run crate sync "
                f"pair again and answer both gates over the plan it shows"
            ),
            detail={**dict(cause.detail or {}), "fresh": True},
        )
    finished = sum(1 for one in planned.pairs if _steps_of(steps, one).has(STEP_DONE))
    said = (
        f"; run {run_id} finished {finished} of {len(planned.pairs)} pair(s) before it "
        f"stopped and recorded each step it took, so continuing the run writes only what "
        f"is left, with no new plan and no new answer"
    )
    detail = {**dict(cause.detail or {}), "run_id": run_id, "finished": finished}
    if cause.reason != provider_gate.CEILING:
        # ANY OTHER PARK names the same command too, to give once it has passed.
        said += ", once that has passed: " + shlex.join(
            ["crate", "--run", run_id, *(argv or VERB_PATH)]
        )
    if cause.reason == provider_gate.CEILING:
        check_calls, write_calls = _expected(planned, steps)
        line = int(detail.get("ceiling") or _ceiling(cfg))
        higher = pair_calls.named(check_calls + write_calls, line)
        # THE HOUR TOO (U278), when the ceiling named is above it, or the
        # continue printed here is refused as printed.
        hour = provider_gate.hour_to_name(higher, provider_gate.GateSettings.from_config(cfg))
        detail.update(
            {"higher": higher, "expected": check_calls + write_calls, "calls_per_hour": hour}
        )
        said += (
            f"; what is left is expected to take about {check_calls + write_calls} calls, "
            f"so continue it with --calls {higher}: "
            + shlex.join(
                [
                    "crate",
                    "--calls",
                    str(higher),
                    *(["--calls-per-hour", str(hour)] if hour is not None else []),
                    "--run",
                    run_id,
                    *(argv or VERB_PATH),
                ]
            )
        )
    return dataclasses.replace(cause, message=f"{cause.message}{said}", detail=detail)



def _unordered(
    unordered: Sequence[Done],
    planned: Plan,
    steps: Any,
    *,
    run_id: str,
    argv: Sequence[str] | None,
) -> Any:
    """The stop a write ends in when a pair's account order did not finish (U220).

    Built on the first refusal's own cause, so its reason and remedy stand.
    """
    import dataclasses

    first = unordered[0].order_refused
    named = "; ".join(
        f"{one.name or one.account_id} ({one.order_refused.message})" for one in unordered
    )
    said = (
        f"the account order of {len(unordered)} pair(s) did not finish, so their "
        f"tracks are all on the account and not yet in rekordbox's order: {named}"
    )
    detail: dict[str, Any] = {
        **dict(first.detail or {}),
        "unordered": [
            {"account_id": one.account_id, "name": one.name, "why": one.order_refused.message}
            for one in unordered
        ],
    }
    if steps is None:
        said += (
            "; every other pair was written, and this run's plan could not be held, "
            "so it cannot be continued: run crate sync pair again and answer both "
            "gates over the plan it shows"
        )
        detail["fresh"] = True
    else:
        finished = sum(1 for one in planned.pairs if _steps_of(steps, one).has(STEP_DONE))
        said += (
            f"; run {run_id} finished {finished} of {len(planned.pairs)} pair(s), wrote "
            f"every other write of these, and recorded each step it took, so "
            f"continuing the run tries their order again with no new plan and no "
            f"new answer, and moves nothing until its reading agrees with the "
            f"check's, while an order whose moves had begun is only read, never "
            f"moved again; first do what each refusal above asks, then: "
            + shlex.join(["crate", "--run", run_id, *(argv or VERB_PATH)])
        )
        detail.update({"run_id": run_id, "finished": finished})
    # EVERY REFUSAL'S STEPS, once each, since the message asks for each.
    steps_said = tuple(
        dict.fromkeys(
            step for one in unordered for step in one.order_refused.remediation.steps
        )
    )
    return dataclasses.replace(
        first,
        message=said,
        detail=detail,
        remediation=dataclasses.replace(first.remediation, steps=steps_said),
    )



def sync_pair(ctx) -> Envelope:
    """Plan every asked pair once, ask both gates, check the lists, then write each side approved.

    U209. A later command of the run reads the held plan back rather than
    planning again; a plan made in this same command needs no check.
    """
    from cratekit.core import held_plan
    from cratekit.modules.outbound import pairs
    from cratekit.modules.outbound.pairs import REKORDBOX_SIDE

    cfg = sync_cli._load()
    # BEFORE THE PLAN AND THE GATE (R-733), as every verb writing the database.
    session.assert_backup_acknowledged(cfg)
    store_of_pairs = pairs.PairStore(cfg)
    wanted = targets(
        store_of_pairs, getattr(ctx.args, "account", None), getattr(ctx.args, "rekordbox", None)
    )
    run_id = ctx.run.run_id
    offered = {gate: ctx.run.offers[gate] for gate in GATES if gate in ctx.run.offers}
    notes: list[dict[str, str]] = []
    with jobs.open_store() as store:
        every = not getattr(ctx.args, "account", None)
        asked = _asked(wanted, every)
        planned: Plan | None = None
        plan_calls = 0
        if offered:
            # A LATER COMMAND OF A RUN THAT SHOWED A GATE reads its plan back.
            planned, plan_calls, why = _held_plan(run_id, offered, asked)
            if planned is None:
                notes.append(
                    {
                        "code": REPLANNED,
                        "message": (
                            f"{why}, so the pairs were planned again; the gates compare "
                            f"this plan with the one they showed"
                        ),
                    }
                )
        held = planned is not None
        not_held = ""
        if planned is None:
            before = _spent()
            planned = plan(cfg, wanted, store=store, every=every)
            plan_calls = _spent() - before
            # R-988. WHAT THE ACCOUNT SAID OF A ROW is recorded before the gate,
            # so a plan made again asks it nothing.
            store_of_pairs.remember(planned.misses, forget=planned.matched)
            not_held = _hold(run_id, planned, plan_calls, asked)
        # U210. THE WRITE'S STEPS, read back when an earlier command held this
        # plan, begun fresh when this command planned it, none when not held.
        steps: held_plan.Steps | None = None
        steps_notes: list[dict[str, str]] = []
        steps_unread = ""
        if held:
            steps, steps_why = held_plan.load_steps(run_id, planned.digest)
            steps_unread = steps_why
            if steps_why:
                steps_notes.append(
                    {
                        "code": STEPS_UNREAD,
                        "message": (
                            f"{steps_why}, so every list is read as the plan read it and "
                            f"anything an earlier command of run {run_id} wrote refuses "
                            f"stale rather than being written twice"
                        ),
                    }
                )
        elif not not_held:
            steps = held_plan.Steps(run_id, planned.digest)
        data = payload(planned)
        shown = facts(planned)
        expected_check, expected_write = _expected(planned, steps)
        line = _ceiling(cfg)
        writing = (expected_check if not not_held else plan_calls) + expected_write
        shown["provider calls"] = (
            f"the plan took {plan_calls}; the command that writes is expected to make "
            f"about {writing}, "
            + (
                f"{expected_check} to check the lists"
                if not not_held
                else f"{plan_calls} to plan the pairs again"
            )
            + f" and {expected_write} to write; one command may make {line}"
        )
        if writing > line:
            higher = pair_calls.named(writing, line)
            # THE HOUR TOO (U278), when the ceiling named is above it.
            from cratekit.core import provider_gate  # noqa: PLC0415 - as _ceiling does

            hour_words = provider_gate.hour_args(
                higher, provider_gate.GateSettings.from_config(cfg)
            )
            shown["call ceiling"] = (
                f"too low for this write: about {writing} calls are expected and one "
                f"command may make {line}, so the write would stop part way; give the "
                f"command that writes --calls {higher}"
                + (f" and {' '.join(hour_words)}" if hour_words else "")
                + ", for example "
                + shlex.join(
                    ["crate", "--calls", str(higher), *hour_words, "--run", run_id,
                     *(ctx.run.argv or VERB_PATH)]
                )
                + " once both gates are answered"
            )
        if not_held:
            shown["plan held"] = (
                f"no, {not_held}; an answer given in a later command plans the pairs again"
            )
        for note in notes:
            # SAID ON THE SCREEN AS WELL, since a gate's refusal carries no warning.
            shown["planned again"] = note["message"]
        warnings = [*notes, *steps_notes, *_warnings(planned)]
        gates = {spec.name: spec for spec in ctx.entry.gates}
        on_rekordbox = (
            ctx.gate.require(gates[REKORDBOX_GATE], plan=data, context=shown) == APPLY
        )
        on_account = ctx.gate.require(gates[ACCOUNT_GATE], plan=data, context=shown) == APPLY
        calls = {"plan": plan_calls, "check": 0, "write": 0}
        if not planned.pairs and not planned.unpaired:
            _release(run_id)
            if planned.listed or planned.listed_back:
                return ctx.envelope(
                    data=_with_calls(data, calls), outcome=Outcome.NO_OP, warnings=warnings
                )
            return ctx.envelope(
                data=_with_calls(data, calls),
                outcome=Outcome.NO_OP,
                warnings=[
                    *warnings,
                    {
                        "code": NOTHING,
                        "message": (
                            "no playlist is paired yet and none of your own was found "
                            "in rekordbox to pair; pair one with crate sync pair "
                            "ACCOUNT_PLAYLIST --rekordbox PLAYLIST_ID"
                        ),
                    },
                ],
            )
        if not (on_rekordbox or on_account):
            _release(run_id)
            return ctx.envelope(
                data=_with_calls(data, calls),
                outcome=Outcome.NO_OP,
                warnings=[
                    *warnings,
                    {"code": SKIPPED, "message": "both sides were skipped, nothing was written"},
                ],
            )
        listed: dict[str, tuple[str, ...]] = {}
        finished = [one for one in planned.pairs if _steps_of(steps, one).has(STEP_DONE)]
        if finished:
            warnings.append(
                {
                    "code": RESUMED,
                    "message": (
                        f"run {run_id} continued: {len(finished)} of {len(planned.pairs)} "
                        f"pair(s) an earlier command of it finished were left as written, "
                        f"and the rest were written from their first unfinished step "
                        f"under the plan and the answers already given"
                    ),
                }
            )
        done: list[Done] = []
        try:
            if held:
                before = _spent()
                try:
                    listed = check(cfg, planned, steps, store=store, unread=steps_unread)
                finally:
                    calls["check"] = _spent() - before
            if steps is not None:
                try:
                    steps.begin()
                except OSError as exc:
                    raise steps_unwritten(run_id, exc) from None
            before = _spent()
            try:
                for one in planned.pairs:
                    if _steps_of(steps, one).has(STEP_DONE):
                        continue
                    done.append(
                        apply_pair(
                            cfg,
                            one,
                            rekordbox=on_rekordbox,
                            account=on_account,
                            store=store,
                            account_listed=listed.get(one.target.account_id),
                            steps=_steps_of(steps, one),
                        )
                    )
                # U231. EVERY ORDER SENT IS READ ONCE, after the others' writes.
                _settle(cfg, done)
            finally:
                calls["write"] = _spent() - before
        except jobs.Parked as exc:
            # U210. A STOP PART WAY says how far the run got and how to finish it.
            raise jobs.Parked(
                _stopped(exc.cause, planned, steps, run_id=run_id, argv=ctx.run.argv, cfg=cfg)
            ) from None
    pending = [one for one in done if one.pending]
    if pending:
        warnings.append(
            {
                "code": PENDING,
                "message": (
                    f"the account order of {len(pending)} pair(s) was sent and the "
                    f"provider does not yet serve it, so each is pending: every track "
                    f"is on the account, rekordbox's order is untouched, and a later "
                    f"crate sync pair finishes it once the provider's readings agree, "
                    f"moving nothing again: "
                    + "; ".join(one.name or one.account_id for one in pending)
                ),
            }
        )
    unordered = [one for one in done if one.order_refused is not None]
    if unordered:
        # U220. EVERY OTHER PAIR WAS WRITTEN; the run stops held, so a continue
        # orders the rest.
        raise CratekitError(
            _unordered(unordered, planned, steps, run_id=run_id, argv=ctx.run.argv)
        )
    forgotten = [
        one
        for one in planned.unpaired
        if not one.made
        and store_of_pairs.unmark(one.account_id, one.rekordbox_id) is not None
    ]
    # U198. A MADE PAIR THAT LOST A SIDE IS UNPAIRED AND ITS SURVIVOR RELEASED,
    # so a sync of every pair never makes the lost side again.
    released = [
        one
        for one in planned.unpaired
        if one.made
        and store_of_pairs.release(one.account_id, one.rekordbox_id, side=one.gone) is not None
    ]
    if released:
        warnings.append(
            {
                "code": RELEASED,
                "message": (
                    f"{len(released)} pair(s) lost a side and were unpaired; the other "
                    f"side is left as it was and is not made again: "
                    + "; ".join(
                        (
                            f"{one.name or one.account_id} stays on the account (its "
                            f"rekordbox playlist is {one.why or 'gone'})"
                            if one.gone == REKORDBOX_SIDE
                            else f"{one.rekordbox_name or one.rekordbox_id} stays in "
                            f"rekordbox (its account playlist is gone)"
                        )
                        for one in released
                    )
                ),
            }
        )
    if forgotten:
        warnings.append(
            {
                "code": UNPAIRED,
                "message": (
                    f"{len(forgotten)} custom playlist twin(s) lost their account "
                    f"playlist and were unpaired; each is left in rekordbox as it was: "
                    + "; ".join(
                        f"{one.rekordbox_name or one.rekordbox_id} (was paired with "
                        f"{one.name or one.account_id})"
                        for one in forgotten
                    )
                ),
            }
        )
    totals = {
        **data["totals"],
        "rekordbox_added": sum(d.rekordbox.added for d in done if d.rekordbox),
        "rekordbox_removed": sum(d.rekordbox.removed for d in done if d.rekordbox),
        "account_added": sum(d.account_added for d in done),
        "account_removed": sum(d.account_removed for d in done),
        "queued_jobs": [d.queued for d in done if d.queued],
        "marked": sum(1 for d in done if d.marked),
        "unpaired": len(forgotten) + len(released),
        "created_playlists": [d.created for d in done if d.created],
        "created_in_rekordbox": [d.created_in_rekordbox for d in done if d.created_in_rekordbox],
        # U210. Pairs finished earlier in the run, and the calls the gates expected.
        "finished_before": len(finished),
        "calls_expected": {"check": expected_check, "write": expected_write},
        # U226. Each reading the account's writes were judged by, so a sitting
        # sees how far the provider lagged.
        "read_backs": [record for d in done for record in d.read_backs],
        # U231. The pairs whose order was sent and is pending.
        "pending": [d.account_id for d in done if d.pending],
    }
    answered = {"rekordbox": on_rekordbox, "the account": on_account}
    sides = [side for side, on in answered.items() if on]
    skipped = [side for side, on in answered.items() if not on]
    message = (
        f"{len(done) - len(pending)} pair(s) synced on {' and '.join(sides)}"
        + (f" and {len(pending)} pending" if pending else "")
        + (f" ({len(finished)} more finished earlier in this run)" if finished else "")
        + (
            f", {len(totals['created_playlists'])} account playlist(s) made"
            if totals["created_playlists"]
            else ""
        )
        + (
            f", {len(totals['created_in_rekordbox'])} rekordbox playlist(s) made"
            if totals["created_in_rekordbox"]
            else ""
        )
        + ": "
        f"{totals['rekordbox_added']} added and {totals['rekordbox_removed']} taken off "
        f"in rekordbox, {totals['account_added']} added and "
        f"{totals['account_removed']} taken off on the account, "
        f"{len(totals['queued_jobs'])} acquisition job(s) queued; no track left the "
        f"collection or the account"
        + (f"; {' and '.join(skipped)} skipped, its snapshot unchanged" if skipped else "")
    )
    message += "; " + _calls_said(calls, held=held)
    wrote = (
        any(d.wrote for d in done) or bool(forgotten) or bool(released) or bool(finished)
    )
    _release(run_id)
    return ctx.envelope(
        data={**data, "totals": {**totals, "calls": calls}},
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
        warnings=[*warnings, {"code": WRITTEN if wrote else NOTHING, "message": message}],
    )



__all__ = [
    "ACCOUNT_GATE", "RESUMED", "STEPS_UNREAD", "STEPS_UNWRITTEN", "STEP_ACCOUNT", "STEP_DONE",
    "STEP_MADE", "STEP_MAKING", "STEP_ORDERING", "STEP_ORDER_REFUSED", "STEP_MOVING", "STEP_MOVED",
    "SETTLE_SECONDS", "AGREE_AFTER", "ORDER_FOLDER", "PENDING", "SETTLING", "ORDER_REFUSALS",
    "STEP_QUEUED", "STEP_REKORDBOX", "PairSteps", "steps_unwritten", "BROUGHT_REASONS", "GATES",
    "HELD_KIND", "REPLANNED", "INTAKE_HANDLER", "PAIR_SOURCE", "REKORDBOX_GATE", "LATER_CHANGE",
    "NEW", "NOT_BROUGHT", "NOT_DISCOVERED", "ON_HOLD", "ON_HOLD_ACTION", "LANDING_UNREAD",
    "LANDING_UNREAD_ACTION", "RELEASED", "TIME_UNKNOWN", "Done", "Moved", "PairPlan", "Place",
    "Plan", "Target", "Unpaired", "apply_pair", "build", "check", "facts", "file_identity",
    "generated_tops", "held_for_choice", "landed_inbox_playlists", "landed_isrcs", "payload",
    "plan", "plan_pair", "sync_pair", "targets", "AMBIGUOUS", "AWAITING", "FINISHING",
    "FOLDER_ADOPT", "FOLDER_CREATE", "LEFT_OUT", "NOTHING", "NO_ISRC", "Named", "OWNED_STATE",
    "QUEUED_HERE", "STOPPED_UNREAD", "UNMATCHED", "UNPAIRED", "UNREAD", "WITHHELD", "WRITTEN",
    "pair_jobs"
]
