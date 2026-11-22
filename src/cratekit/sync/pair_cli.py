"""``crate sync pair``: keep the author's own account playlist and its rekordbox playlist one list.

U130, decided by Phillip on 2026-10-10: a playlist the author made, on the
account or in rekordbox, and marked for sync, stays the same list on both sides
after every sync, each side merged against the last sync. ``intake playlist``
pulls one way and ``export playlist`` pushes the other; this verb does both for
a pair, and removes as well as adds, because a removal on either side is applied
on both.

**WHAT A PAIR MAY HOLD.** One of the author's own account playlists, which is
one the account lists as the author's (the catalogue keeps only those), and one
plain rekordbox playlist, each named by its identifier and never by its name
(R-906). Refused before anything is listed track by track: the hearts, a
label's year or dated playlist, a set playlist, the label batch's debris, a
favourites placeholder, a rekordbox folder or smart playlist, and any rekordbox
playlist under one of Cratekit's own trees, which is a node under a tree root
the registry records or under a top level node carrying a name the taxonomy
declares for one of its trees. Those lists are Cratekit's to write, and a pair
writing them too would be two writers on one list.

**HOW A PAIR IS MARKED.** ``crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID``
names a pair, and the pair is recorded when its first sync is approved on
either side. ``crate sync pair ACCOUNT_ID`` syncs a marked pair, and
``crate sync pair`` with no argument syncs every marked pair. The record and the
snapshot are ``modules/outbound/pairs.py``'s, and the merge is
``sync/pair_merge.py``'s.

**EVERY PLAYLIST THE AUTHOR MADE, PAIRED BY ITSELF (U198).** Decided by
Phillip on 2026-11-04: ``crate sync pair`` with no argument also finds every
plain rekordbox playlist he made outside Cratekit's trees, the Favorites folder
and the folders ``outbound.pair_skip_folders`` names (ARCHIVE by default), as
``sync/pair_discover.py`` reads them, and pairs each one that no pair holds
with an account playlist this sync makes: one private playlist per rekordbox
playlist, in one account root folder per rekordbox top folder, titled
``<Folder> <path below> <Playlist>``, and ``Playlists`` for the rekordbox
root. It is made on the account's gate only, reserved and marked in the pairs
document before it is created, and its first sync adds only, as any pair's
does. A root folder of the name is adopted when the pairs document records
none and no other list of Cratekit's keeps it, and a playlist of the title
already in that folder is left and named, never joined. A made pair that
loses either side is unpaired, its survivor left where it is and released,
so it is never made again. A rekordbox row the account had no track for is
remembered with the ISRC it was asked under (R-988), so the next plan asks
the provider nothing about it until that ISRC changes.

**A PLAYLIST MADE ON THE ACCOUNT IN A SYNCED FOLDER COMES TO REKORDBOX (U202).**
Decided by Phillip on 2026-11-04, the other half of U198: a playlist he makes
on the account inside one of the root folders the pairs document records is
made in rekordbox at the next sync of every pair, and paired as one the
product made. ``sync/pair_discover.home_of`` says where: the account title
less ``<Folder> `` is its name, in the live rekordbox top folder of the
folder's name, down any subfolder the title reads that is there, and
``Playlists`` is the rekordbox root. It is made on the rekordbox gate only,
by ``sync/pair_reverse.py`` under the pairs lock, and its first sync adds
only, so every track the library owns lands in the account's order and every
one it lacks is queued once. Listed and never made: a playlist a pair already
holds is not offered at all; a released one (its rekordbox side was deleted),
one that is not the author's own or that a pair may not hold, one whose place
``home_of`` refuses, and two that would take one rekordbox name in one folder,
which refuse that name only.

**ONLY ONE MADE AFTER THE SYNC (U216).** A root folder a sync adopted by its
name already held the account's own playlists, and those never come to
rekordbox: the adoption records what the folder held (``MadeFolder.held``),
and a folder adopted before that record existed is read by when the account
says each playlist was made against the earliest mark of a pair made in it,
an unknown read as held. A downloaded copy (``DOWNLOADED `` titled, or taken
since U242) of a playlist a pair in the
same folder holds is that playlist again, and is not made either. Each is
named on the gate, never dropped.

**THE LATER OF TWO OPPOSITE CHANGES WINS (U202).** Where one track was added
on one side and removed on the other since the last sync, the merge applies
the later change to both (``sync/pair_merge.py``). The moments are the
account's added date for each playlist track, rekordbox's membership row
``created_at`` for an addition, and the base membership row's ``updated_at``
for a removal while that row is still there marked removed. The account keeps
no record of a removal, so an account removal never beats an addition, and
every call made with a moment unknown keeps the track and is named on the
gate. The snapshot records each account track's added date, so a track taken
out and put back on the account reads as added there (R-990).

**HOW A TRACK IS MATCHED ACROSS THE SIDES.** A match one sync made is recorded
on the pair as a link and reused. A rekordbox row with no link is matched on the
account ISRC first, through the account seam ``export playlist`` uses, with the
code read from the database and else from the row's audio file; a row it does
not match is NAMED on the gate and in the answer with the account's reason, and
stays in rekordbox. A row whose ISRC names several releases that all agree with
it is matched as one of them, as the mirror matches it (U208, decided by
Phillip at Sitting 54, reversing U198's keeping of R-572's refusal): the one
the account hearts, else the lowest numbered after the file's album narrowed
them, linked like any match, and counted on the gate; when the account
already holds several releases of it, the lowest numbered of those, so no
third is added. Every release linked to one row is that row's one key in the
merge, so removing the row takes each of them off the account, and taking one
off the account while another stays keeps the row, at the place on the
account of the release that stayed. An account track with
no link is looked for in the library: a live row carrying its ISRC, a row of
this playlist whose file carries it (U208), a row an intake job this pair
queued resolved it to, or a row of the INBOX playlist a landing made for this
account playlist (U128) whose file carries its ISRC. A track found nowhere is QUEUED FOR
ACQUISITION through the intake path, ``intake.playlist`` exactly as
``intake playlist`` queues it, and never written to rekordbox as a row without a
file. A track an earlier sync queued is not queued again and is named as
awaiting, and so is one any other pair's job still holds or an earlier pair
of the same plan queues (R-1385): a track is downloaded once for the library,
whichever pairs list it.

**A TWIN'S MISSING TRACKS WAIT FOR THE AUTHOR'S CHOICE (U221).** Decided by
Phillip on 2026-11-05: a track a custom playlist twin was made without is
never queued on its own, as a label's releases are never downloaded on their
own. ``crate sync twins`` records those tracks on the twin's pair, and here
each is named on the gate as on hold, counted per twin, and left out of the
queue (:func:`held_for_choice`), until ``crate sync release`` empties that
twin's hold. A track put on the playlist by hand after the twin was made is
not held, and a twin paired before U221 or made from a short listing, which
recorded no hold, is read by the account's added dates against the pair's mark.

**TWO GATES, BOTH ASKED BEFORE ANYTHING IS WRITTEN.** ``sync.pair.rekordbox``
and ``sync.pair.account`` each show the whole plan, every addition and every
removal on both sides by artist and title, and each answers for its own side.
Both are explicit (R34), digest bound to the plan. Rekordbox is written first, through the
session spine and the native writer's guarded commit, behind the backup
acknowledgment read before the plan; then the account, through the account
seam, whose removals and orders a pair vouches for. A side whose gate is
answered ``skip`` is not written and its snapshot is not moved, so the next sync
finishes it.

**ONE PLAN PER RUN (U209).** Each gate is answered in a later command, and
each of those used to plan every pair again, at thousands of provider calls a
gate over a hundred playlists (Sitting 54). The command that plans now holds
its plan under its run (``core/held_plan.py``), and every later command of the
run reads it back, checked against the digest each gate offered, so the gates
and the write use the plan the person was shown. Before the first write,
:func:`check` reads only the lists the plan read, each pair's rekordbox
membership and account listing and a made side's folder, and refuses
``decision-stale`` naming every list that moved, with nothing written; it
never matches a track. A held plan that cannot be used is planned again, digest
bound, and the answer says why. The answer counts each phase's provider calls,
plan, check and write.

**A WRITE STOPPED PART WAY IS FINISHED BY A CONTINUE OF THE SAME RUN (U210).**
Sitting 54's sync of every pair stopped on its call ceiling after making 94
of 101 account playlists, and its continue planned again and refused stale.
So the write records each step of each pair under its run as it lands
(``core/held_plan.Steps``): a made side begun and made, rekordbox's commit
with the memberships it left, the queued job, the account writes begun, and
the pair done. A continue reads the held plan and those steps, passes over
every pair done, checks the pair part written only for what its own write
could have done, and starts each pair at its first unfinished step, under
the answers already given; a list moved otherwise refuses stale, naming it.
A made side the stop left reserved is finished, never made twice. The gates
show the provider calls the command that writes is expected to make
(``sync/pair_calls.py``) and, when the ceiling is lower, the ``--calls`` that
lets it finish; a stop part way names the run and the ``--calls`` its
continue needs.

**A FRESH SYNC AFTER A WRITE STOPPED PART WAY THROUGH ITS ORDER FINISHES IT
(U225).** Sitting 62's write added tracks to one paired account playlist and
stopped part way through putting it in order; the next fresh sync read the
stopped write's own moves as the person's reorder and planned to put that
scramble into rekordbox. So the write records what its order was doing when it
began to move tracks, and a plan reads every run's steps still kept
(``sync/pair_stopped.py``). For a pair whose latest account write since its
snapshot began to order and never finished: its moves are not read as
anybody's when the account stands where the adapter's moves could have left
it, and the side that led it leads again unless a side changed order since;
and when it committed rekordbox too, the plan merges against what it left on
both sides, so its additions and removals are not read as the person's
either. AN ACCOUNT OFF THOSE MOVES' PATH is finished the same way (U234):
Sitting 87 read accounts left in orders no count of the moves leaves, the
provider's partial state after refused and misplaced moves, so off the path
leads only once readings kept on the pair after the stop, each off the path
and settled over the agreement window, show the account moved to another
order. The gate names the pair as finishing that run, and which of these it
read. A FIRST SYNC reads the
stop on its account playlist too, whatever the pair's mark (R-1376): a pair
released after a stop and paired again with a new rekordbox playlist has no
snapshot, so the account's half done order would lead and be put into
rekordbox. Its order is finished the same way, and nothing of it is folded,
since a first sync has no base.

**THE SNAPSHOT MOVES ONLY WHEN THE WHOLE PAIR WAS WRITTEN.** Both gates
applied, every write landed, and the account listed the whole playlist: only
then are both sides' snapshots recorded, together. Anything less, a side
skipped, a write that failed part way or a short listing, records the links the
plan made and leaves the snapshot where it was, so the next sync merges against
the same last sync and finishes what this one did not. A side's removal that
the other side never took is still a removal then, because the base that saw
the track is still the base. A first sync that did not finish is still a first
sync, and adds only.

**A SHORT ACCOUNT LISTING REMOVES NOTHING.** The provider counts tracks it will
not serve. A track it withheld would read as one the author removed, so when the
listing is short no account track is read as removed, the account side takes no
removal and no reorder, and the answer says how many were withheld.

**A TRACK THE ACCOUNT LISTS UNREADABLY IS WITHHELD BY ID (R-1264).** Each
pair's account side is read row by row, as the twins backfill reads it: a track
listed with no title or no artist is unread, kept by its id. It is never added
to rekordbox, never read as taken off the account, so a row linked to it stays,
and never offered to the account, which already lists it; a row carrying its
ISRC matches it. Unlike a withheld track it is no passing state, the provider
may list it that way for good, so the pair still syncs WHOLE: a removal on
either side lands on both, and the snapshot moves, recording the account in its
listed order with each unread id in its place, since a snapshot held back while
the account kept listing such a track would read every later removal as an
addition and undo it (the review's round one). The account's order is read and
written whole too: each key sits at its first release's place in the listing,
and a reorder puts each unread track back behind the track listed before it,
since an order withheld while the snapshot moved let the account lead the next
sync and undo a rekordbox reorder (the review's round two). At a finish of a
stopped order (R-1432) each unread track the stopped write's target names goes
behind the track that target puts before it instead, since the listing shows
where an interrupted move left it. A move of unread tracks alone, read settled
after a stop or after a write that sent no move, is no reorder of the readable
tracks (R-1446): the stopped write is still finished, so rekordbox keeps the
DJ's order, and each unread track the person moved keeps the place they gave
it. The gate names each. A listing the reader cannot use at all, a row carrying no provider id,
leaves its pair out of a sync of every pair, named, and refuses a pair named
alone.

Layer: modules.
"""

from __future__ import annotations

import shlex
from collections.abc import Sequence
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, session
from cratekit.core.cause import CratekitError, Outcome
from cratekit.modules.outbound.pairs import REKORDBOX_SIDE
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



#: U210. The warnings a continued write carries: the pairs an earlier command
#: of the run finished, and steps that could not be read.
RESUMED = "sync-pair-resumed"

STEPS_UNREAD = "sync-pair-steps-unread"


#: The verb's own words, for a command line named when the run kept none.
VERB_PATH = ("sync", "pair")



def _expected(planned: Plan, steps: Any) -> tuple[int, int]:
    """The calls the command that writes is expected to make: the check's, and the write's (U210).

    Read from what is LEFT, so at a continue a pair an earlier command
    finished costs nothing and a made playlist already made costs its filling.
    The check reads every pair left; the write counts the account side of
    each, since a rekordbox write makes no provider call.
    """
    left = [one for one in planned.pairs if not _steps_of(steps, one).has(STEP_DONE)]
    check_calls = pair_calls.check(left, create=FOLDER_CREATE)
    # A FOLDER A MADE PAIR OF THIS RUN BEGAN IN IS MADE ALREADY, by the
    # first pair that went in it, so the pairs still to make there make none.
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
            # Its listing is the check's now, as any paired playlist's is,
            # with the unpaged read beside it (U226, round one's review).
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
    """A park raised part way through the check or the write, said with how far the run got (U210).

    The pairs finished are counted off the run's steps, so the answer says
    what a continue will skip. A stop on the call ceiling names the run and a
    ``--calls`` sized from what is left (never below the ceiling it stopped
    at), which the dispatcher writes into the one command that continues it.
    """
    import dataclasses

    from cratekit.core import provider_gate

    if steps is None:
        # NOTHING WAS RECORDED (U210, from round one's review): the plan could
        # not be held, so no step was, and a continue of this run would find
        # the lists this write moved and refuse stale. Said, and no run named.
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
        # ANY OTHER PARK names the command too (round two's review), to give
        # once what parked it has passed: the same run, the same words.
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

    Built on the first refusal's own cause, so its reason and remedy stand,
    and said with how far the run got: every pair it finished, each pair whose
    order did not finish and why, and the command that continues the run.
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
    # EVERY REFUSAL'S STEPS, once each, since the message asks the person to
    # do what each one asks (round two's review).
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

    U209. The command that plans holds its plan under its run, and every later
    command of the run, an answer continued or the verb run again with
    ``--run``, reads that plan back rather than planning again, so a two gate
    sync costs one plan of provider calls. Before the first write the lists
    the plan read are checked (:func:`check`); a plan made in this same
    command needs no check. The answer counts the calls of each phase.
    """
    from cratekit.core import held_plan
    from cratekit.modules.outbound import pairs

    cfg = sync_cli._load()
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733), as every verb that
    # writes the database reads it.
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
            # R-988. WHAT THE ACCOUNT SAID OF A ROW IS A FACT ABOUT THE ROW,
            # recorded before the gate, so a plan made again asks it nothing.
            store_of_pairs.remember(planned.misses, forget=planned.matched)
            not_held = _hold(run_id, planned, plan_calls, asked)
        # U210. THE WRITE'S STEPS, recorded against the plan held now: read
        # back when an earlier command of the run held this same plan, begun
        # fresh when this command planned it, and none when it is not held.
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
            # U210. A STOP PART WAY, on the ceiling or anything else that parks
            # the run, says how far the run got and how to finish it.
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
        # U220. EVERY OTHER PAIR WAS WRITTEN, and the run stops here, held, so
        # a continue of it puts the unfinished pairs in order.
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
        # U210. Pairs an earlier command of this run finished, left as written,
        # and what the gates said this command was expected to spend.
        "finished_before": len(finished),
        "calls_expected": {"check": expected_check, "write": expected_write},
        # U226. Each reading the account's writes were judged by, with how
        # many readings it took and how long it waited, so an attended
        # sitting reads how far the provider's read lagged.
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
    "ACCOUNT_GATE",
    "RESUMED",
    "STEPS_UNREAD",
    "STEPS_UNWRITTEN",
    "STEP_ACCOUNT",
    "STEP_DONE",
    "STEP_MADE",
    "STEP_MAKING",
    "STEP_ORDERING",
    "STEP_ORDER_REFUSED",
    "STEP_MOVING",
    "STEP_MOVED",
    "SETTLE_SECONDS",
    "AGREE_AFTER",
    "ORDER_FOLDER",
    "PENDING",
    "SETTLING",
    "ORDER_REFUSALS",
    "STEP_QUEUED",
    "STEP_REKORDBOX",
    "PairSteps",
    "steps_unwritten",
    "BROUGHT_REASONS",
    "GATES",
    "HELD_KIND",
    "REPLANNED",
    "INTAKE_HANDLER",
    "PAIR_SOURCE",
    "REKORDBOX_GATE",
    "LATER_CHANGE",
    "NEW",
    "NOT_BROUGHT",
    "NOT_DISCOVERED",
    "ON_HOLD",
    "ON_HOLD_ACTION",
    "LANDING_UNREAD",
    "LANDING_UNREAD_ACTION",
    "RELEASED",
    "TIME_UNKNOWN",
    "Done",
    "Moved",
    "PairPlan",
    "Place",
    "Plan",
    "Target",
    "Unpaired",
    "apply_pair",
    "build",
    "check",
    "facts",
    "file_identity",
    "generated_tops",
    "held_for_choice",
    "landed_inbox_playlists",
    "landed_isrcs",
    "payload",
    "plan",
    "plan_pair",
    "sync_pair",
    "targets",
    "AMBIGUOUS",
    "AWAITING",
    "FINISHING",
    "FOLDER_ADOPT",
    "FOLDER_CREATE",
    "LEFT_OUT",
    "NOTHING",
    "NO_ISRC",
    "Named",
    "OWNED_STATE",
    "QUEUED_HERE",
    "STOPPED_UNREAD",
    "UNMATCHED",
    "UNPAIRED",
    "UNREAD",
    "WITHHELD",
    "WRITTEN",
    "pair_jobs",
]
