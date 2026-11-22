"""The writes of ``crate sync pair``: the steps each run records, the rekordbox side and the account side (U130, U304)."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import analysis_store, config, jobs, rb_writer
from cratekit.core.cause import CratekitError, refuse
from cratekit.favorites import placeholders
from cratekit.intake import cli as intake_cli
from cratekit.sync import pair_merge, pair_model, pair_stopped
from cratekit.sync.pair_model import (
    _ORIGIN,
    FOLDER_ADOPT,
    INTAKE_HANDLER,
    NEW,
    ORDER_REFUSALS,
    PAIR_SOURCE,
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
    PairPlan,
)
from cratekit.write import playlist_pair

# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


@dataclass
class Done:
    """What one pair's sync did."""

    account_id: str
    rekordbox: playlist_pair.Written | None = None
    account_added: int = 0
    account_removed: int = 0
    account_ordered: bool = False
    queued: str = ""
    marked: bool = False
    #: Whether both sides' snapshots moved, which only a whole pair does.
    snapshot: bool = False
    #: U198. The account playlist made for a discovered rekordbox playlist.
    created: str = ""
    #: U202. The rekordbox playlist made for an account playlist.
    created_in_rekordbox: str = ""
    #: U220. Why the account order of this pair did not finish, or None.
    order_refused: Any = None
    #: U220. The pair's name, said when its order did not finish.
    name: str = ""
    #: U226. The account adapter's record of each reading it judged this
    #: pair's writes by: its readings, its wait and its window's lag.
    read_backs: list[dict[str, Any]] = field(default_factory=list)
    #: U231. The pair's order, sent and not yet read, which the write reads
    #: once every pair is written; None once read, or for a pair with none.
    settle: Settle | None = None
    #: U231. Whether its order was read short of where its moves leave it,
    #: so it is pending on the pair for a later sync.
    pending: bool = False

    @property
    def wrote(self) -> bool:
        written = self.rekordbox
        return bool(
            (written and (written.added or written.removed or written.renumbered))
            or self.account_added
            or self.account_removed
            or self.account_ordered
            or self.queued
            or self.marked
            or self.created
            or self.created_in_rekordbox
        )



@dataclass
class Settle:
    """One pair's account order sent with no read back, waiting for the reading that decides it (U231)."""

    one: PairPlan
    steps: PairSteps
    #: The order the moves leave the account playlist in.
    end: tuple[str, ...]
    #: When its last move was sent, or the moves began in an earlier command.
    moved_at: datetime
    rekordbox_after: tuple[playlist_pair.Row, ...] | None



def _record(
    cfg: config.Config,
    one: PairPlan,
    *,
    rekordbox_after: Sequence[playlist_pair.Row] | None,
    account_after: Sequence[str] | None,
) -> bool:
    """Record both sides' snapshots when the whole pair was written, else the links alone.

    Returns whether the snapshot moved. Every live rekordbox membership is
    recorded, a track held twice with both its rows, so a later sync can tell
    a copy that was removed from a track that was taken out and put back.
    """
    from cratekit.modules.outbound import pairs

    # AN UNREAD TRACK DOES NOT HOLD THE SNAPSHOT BACK (R-1264, the review's
    # round one): the account may list it that way for good, and a base that
    # never moved would read every later removal as an addition. The account
    # after the write names it in its place, and the next plan strips it from
    # the base as it does now.
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
    held_after = pair_merge.distinct(account_after or ())
    recorded = pairs.PairStore(cfg).record(
        one.target.account_id,
        account=list(held_after) if whole else None,
        # U202. THE ADDED DATES THE PLAN LISTED, for the tracks the account
        # holds after the write; a track this sync added is dated by the next.
        account_added=(
            {one_id: one.account_dates[one_id] for one_id in held_after if one_id in one.account_dates}
            if whole
            else None
        ),
        rekordbox=(
            [pairs.Membership(row.content_id, row.row_id) for row in rekordbox_after]
            if whole
            else None
        ),
        links=one.links,
        name=one.name,
    )
    if whole:
        _let_go_passed(one.target.account_id, recorded.synced)
    return whole



def _let_go_passed(account_id: str, synced: str) -> None:
    """Let go of every carried record of this pair its new snapshot passed (R-1372).

    A record that cannot be read or let go is left; the next plan reads one
    the snapshot passed as no write, so leaving it costs a file, never a
    write.
    """
    from cratekit.core import held_plan

    moment = placeholders.parse_hearted(synced)
    if moment is None:
        return
    records, _problems = held_plan.carried()
    for run_id, key in pair_stopped.passed_by(
        records,
        account_id=account_id,
        moment=moment,
        new=NEW,
        account=STEP_ACCOUNT,
        made=STEP_MADE,
    ):
        held_plan.let_go(run_id, key)



def _made(
    cfg: config.Config, one: PairPlan, *, resumed: bool = False
) -> tuple[PairPlan, bool]:
    """Make a discovered playlist's account side in its root folder, and pair it (U198).

    The folder and the playlist are each reserved in the pairs document under
    its lock before they are created, and the playlist is marked in the same
    write, so an unwritable document refuses before anything is made and a
    sync stopped part way leaves what it made recorded for the next one. The
    playlist is moved into its folder only when this sync made it.

    ``resumed`` says an earlier command of this run began making it and
    stopped (U210). The reservation then answers the playlist that command
    made, and it is moved into its folder again, since the stop may have come
    between the make and the move and the move asks for one fixed place; only
    a pair the pairs document records as made for this rekordbox playlist in
    this folder is moved, so a playlist the author paired by hand in between
    is never moved into Cratekit's folder. Answers the pair and whether this
    call made the playlist.
    """
    from dataclasses import replace

    from cratekit.modules.outbound import account as outbound_account
    from cratekit.modules.outbound import pairs

    place = one.place
    assert place is not None
    remote = outbound_account.resolve(cfg)
    store = pairs.PairStore(cfg)
    folder_id, _created = store.reserve_folder(
        place.folder,
        lambda: remote.create_folder(place.folder),
        adopt=place.folder_id if place.action == FOLDER_ADOPT else "",
        stale=place.stale,
        held=place.held,
    )
    account_id, made = store.reserve_made(
        one.target.rekordbox_id,
        name=place.title,
        folder=place.folder,
        create=lambda: remote.create_playlist(place.title),
    )
    if made or (resumed and _made_here(store.get(account_id), one)):
        remote.move_to_folder(account_id, folder_id)
    return replace(one, target=replace(one.target, account_id=account_id, marked=True)), made



def _made_here(held: Any, one: PairPlan) -> bool:
    """Whether the pairs document records this account playlist as made for this pair here (U210)."""
    place = one.place
    return (
        held is not None
        and bool(held.made)
        and held.rekordbox_id == one.target.rekordbox_id
        and place is not None
        and held.folder == place.folder
    )



def _made_in_rekordbox(
    cfg: config.Config, one: PairPlan
) -> tuple[PairPlan, playlist_pair.Written | None]:
    """Make an account playlist's rekordbox side at its home, and pair it (U202).

    The pairs lock is taken before the database is opened, so an unwritable
    document refuses before anything is made, and the pair is marked as the
    product's straight after the commit. An account playlist another sync
    paired first makes nothing and answers None. The playlist is read back
    after it is recorded, so a read back that refuses leaves it paired.
    """
    from dataclasses import replace

    from cratekit.modules.outbound import pairs
    from cratekit.sync import pair_reverse

    home = one.home
    assert home is not None
    holder: dict[str, Any] = {}

    def landed(playlist_id: str) -> None:
        holder["landed"] = playlist_id

    def create() -> str:
        db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
        try:
            holder["written"] = pair_reverse.create(
                cfg,
                db,
                home,
                one.change.order,
                source=f"{PAIR_SOURCE}:{one.target.account_id}",
                analysis_roots=analysis_store.watch_roots(cfg),
                on_commit=landed,
            )
        except BaseException as exc:
            # A FAILURE AFTER THE COMMIT LANDED still pairs what landed (U202,
            # from the review), so the playlist is never left in rekordbox
            # unpaired; the failure is raised once the pair is recorded.
            if not holder.get("landed"):
                raise
            holder["failed"] = exc
            return holder["landed"]
        finally:
            rb_writer.close_db(db)
        return holder["written"].playlist_id

    rekordbox_id, made = pairs.PairStore(cfg).reserve_made_rekordbox(
        one.target.account_id, name=one.name, folder=home.folder, create=create
    )
    if "failed" in holder:
        raise holder["failed"]
    if not made:
        return one, None
    change = replace(one.change, playlist_id=rekordbox_id)
    playlist_pair.assert_read_back(holder["written"], change)
    return (
        replace(
            one,
            target=replace(one.target, rekordbox_id=rekordbox_id, marked=True),
            change=change,
        ),
        holder["written"],
    )



def _queue(cfg: config.Config, one: PairPlan, store) -> str:
    """Queue the pair's missing tracks through the intake path, once. The job id, or ``""``."""
    if not one.acquire:
        return ""
    job = intake_cli.queue_playlist(
        store,
        cfg,
        handler_key=INTAKE_HANDLER,
        reference=one.target.account_id,
        tracks=one.acquire,
        source_id=PAIR_SOURCE,
        name=one.name,
    )
    return job.job_id



#: U231. Seconds from an order's last move to the one reading that decides it.
#: Spent on the other pairs' writes where there are any, and slept only for
#: what is left. UNMEASURED as a fit: Sitting 86 read most moves back on the
#: first reading, 18 on a second and 41 not after seven seconds, and some
#: orders not after 28 minutes; what this window does not cover is pending.
SETTLE_SECONDS = 30.0



class PairSteps:
    """One pair's steps in its run's record (U210), or no record at all.

    ``steps`` is the run's :class:`cratekit.core.held_plan.Steps`, or None for
    a write that keeps no record, which marks nothing and has done nothing.
    ``key`` is the pair as the gate names it, which the plan holds whatever
    the write makes.
    """

    def __init__(self, steps: Any, key: str) -> None:
        self.steps = steps
        self.key = key

    def has(self, step: str) -> bool:
        return self.steps is not None and self.steps.has(self.key, step)

    def get(self, step: str, default: Any = None) -> Any:
        return default if self.steps is None else self.steps.get(self.key, step, default)

    def mark(self, step: str, value: Any = True) -> None:
        """Record one step, and stop the write when the record cannot be written."""
        if self.steps is None:
            return
        try:
            self.steps.mark(self.key, step, value)
        except OSError as exc:
            raise steps_unwritten(self.steps.run_id, exc) from None

    def carry(self) -> None:
        """Keep this pair's steps past its run (R-1372), and stop the write when they cannot be kept."""
        if self.steps is None:
            return
        from cratekit.core import held_plan

        try:
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            raise steps_unwritten(self.steps.run_id, exc) from None

    def carried(self, step: str) -> Any:
        """One step of what this pair's steps carried past its run, or None (U231).

        Read when the run's own steps do not hold it: a continue whose steps
        file could not be read, or is gone, still finds the moves its order
        sent in the record carried beside it, so it never sends them again.
        """
        if self.steps is None:
            return None
        from cratekit.core import held_plan

        return held_plan.carried_step(self.steps.run_id, self.key, step)

    def let_go(self) -> None:
        """Let go of what this pair's steps carried past its run, once the pair is done (R-1372).

        A record that cannot be let go is left: the snapshot the pair's write
        recorded is later than it, so a later plan reads it as no write.
        """
        if self.steps is None:
            return
        from cratekit.core import held_plan

        held_plan.let_go(self.steps.run_id, self.key)



def steps_unwritten(run_id: str, exc: OSError) -> CratekitError:
    """The refusal a write stops with when its steps cannot be recorded (U210)."""
    return refuse(
        STEPS_UNWRITTEN,
        f"the steps of run {run_id} could not be recorded ({type(exc).__name__}: {exc}), "
        f"so the write stopped rather than go on with nothing a continue could start from; "
        f"what it wrote before that is kept",
        steps=(
            "make Cratekit's state directory writable, then run crate sync pair again and "
            "answer both gates over the plan it shows",
        ),
        origin=_ORIGIN,
        detail={"run_id": run_id, "error": f"{type(exc).__name__}: {exc}"},
    )



def _landed(playlist_id: str, rows: Sequence[playlist_pair.Row]) -> dict[str, Any]:
    """What a rekordbox step records: the playlist and its memberships as the commit left them."""
    return {
        "playlist_id": str(playlist_id),
        "rows": [[str(row.content_id), str(row.row_id)] for row in rows],
    }



def _members(cfg: config.Config, playlist_id: str) -> tuple[playlist_pair.Row, ...]:
    """A rekordbox playlist's live memberships, read with nothing written (U210)."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return playlist_pair.members(db, playlist_id)
    finally:
        rb_writer.close_db(db)



def _with_account_id(one: PairPlan, account_id: str) -> PairPlan:
    from dataclasses import replace

    return replace(one, target=replace(one.target, account_id=account_id, marked=True))



def _with_rekordbox_id(one: PairPlan, rekordbox_id: str) -> PairPlan:
    from dataclasses import replace

    return replace(
        one,
        target=replace(one.target, rekordbox_id=rekordbox_id, marked=True),
        change=replace(one.change, playlist_id=rekordbox_id),
    )



def _queue_once(cfg: config.Config, one: PairPlan, store, steps: PairSteps) -> str:
    """Queue the pair's missing tracks unless an earlier command of the run did (U210).

    The job id queued now, or ``""``: a job an earlier command queued is that
    command's to report, and queueing it again would ask for every track twice.
    """
    if steps.has(STEP_QUEUED):
        return ""
    job_id = _queue(cfg, one, store)
    steps.mark(STEP_QUEUED, job_id)
    return job_id



def apply_pair(
    cfg: config.Config,
    one: PairPlan,
    *,
    rekordbox: bool,
    account: bool,
    store,
    account_listed: Sequence[str] | None = None,
    steps: PairSteps | None = None,
) -> Done:
    """Write one pair: mark it, rekordbox and the queue, then the account, then its snapshot.

    ``account_listed`` is the account playlist as the check before the write
    read it (U209), equal to what the plan read until this run's moves of
    the pair's order begin. On a continue of an order whose moves never
    began and that finishes no stopped write, it was read in order and is
    handed to the adapter to agree with first (R-1420); once the moves
    began it is checked for what it holds and not its order, and a finish
    is held to the plan's own reading (R-1411). A pair with nothing to write
    on the account records it as the side's snapshot rather than listing the
    playlist again; a pair that writes there lists it after the write, as
    every pair did before.

    ``steps`` is this pair's record in its run (U210). Each step is recorded
    the moment it lands, and a step a stopped command of the same run already
    recorded is not done again: a made side is not made again, a rekordbox
    commit that landed is read back rather than written, and a queued job is
    not queued twice. The account writes are begun again whole, since each of
    them skips what the playlist already holds as asked.
    """
    from cratekit.modules.outbound import pairs

    steps = steps if steps is not None else PairSteps(None, one.target.key)
    done = Done(account_id=one.target.account_id)
    if not (rekordbox or account):
        return done
    rekordbox_after: tuple[playlist_pair.Row, ...] | None = None
    account_after: tuple[str, ...] | None = None
    if one.target.rekordbox_new:
        # U202. THE REKORDBOX SIDE IS MADE ONLY ON REKORDBOX'S GATE, and with
        # nothing made there is nothing to pair, so an account side approved
        # alone writes nothing; the next sync finds the playlist again.
        if not rekordbox:
            return done
        landed = steps.get(STEP_REKORDBOX)
        if isinstance(landed, dict) and landed.get("playlist_id"):
            # U210. MADE BY AN EARLIER COMMAND OF THIS RUN, so it is read back.
            one = _with_rekordbox_id(one, str(landed["playlist_id"]))
            rekordbox_after = _members(cfg, one.target.rekordbox_id)
        else:
            one, written = _made_in_rekordbox(cfg, one)
            if written is None:
                return done
            steps.mark(STEP_REKORDBOX, _landed(one.target.rekordbox_id, written.read_back))
            done.marked = True
            done.created_in_rekordbox = one.target.rekordbox_id
            done.rekordbox = written
            rekordbox_after = written.read_back
        done.queued = _queue_once(cfg, one, store, steps)
        # Nothing further on rekordbox: the playlist was made holding the plan.
        rekordbox = False
    elif one.target.new:
        # U198. THE ACCOUNT SIDE IS MADE ONLY ON THE ACCOUNT'S GATE, and with
        # nothing made there is nothing to pair, so a rekordbox side approved
        # alone writes nothing; the next sync finds the playlist again.
        if not account:
            return done
        made = steps.get(STEP_MADE)
        if isinstance(made, str) and made:
            # U210. MADE AND IN ITS FOLDER IN AN EARLIER COMMAND OF THIS RUN.
            one = _with_account_id(one, made)
            done.account_id = made
        else:
            resumed = steps.has(STEP_MAKING)
            steps.mark(STEP_MAKING)
            one, created = _made(cfg, one, resumed=resumed)
            steps.mark(STEP_MADE, one.target.account_id)
            done.account_id = one.target.account_id
            done.marked = True
            if created:
                done.created = one.target.account_id
    else:
        pairs.PairStore(cfg).mark(one.target.account_id, one.target.rekordbox_id, name=one.name)
        done.marked = not one.target.marked

    if rekordbox:
        landed = steps.get(STEP_REKORDBOX)
        if isinstance(landed, dict):
            # U210. THE COMMIT LANDED IN AN EARLIER COMMAND OF THIS RUN, and the
            # check before the write found the playlist as that commit left it.
            rekordbox_after = _members(cfg, one.target.rekordbox_id)
        else:
            db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
            try:
                if one.rekordbox_writes:
                    written = playlist_pair.apply(
                        cfg,
                        db,
                        one.change,
                        source=f"{PAIR_SOURCE}:{one.target.rekordbox_id}",
                        analysis_roots=analysis_store.watch_roots(cfg),
                    )
                    playlist_pair.assert_read_back(written, one.change)
                    done.rekordbox = written
                    rekordbox_after = written.read_back
                else:
                    rekordbox_after = playlist_pair.members(db, one.target.rekordbox_id)
            finally:
                rb_writer.close_db(db)
            steps.mark(STEP_REKORDBOX, _landed(one.target.rekordbox_id, rekordbox_after))
        done.queued = _queue_once(cfg, one, store, steps)

    if account:
        from cratekit.modules.outbound import account as outbound_account

        # BEFORE THE FIRST ACCOUNT CALL (U210), so a continue knows this
        # playlist may hold part of this write and reads it that way, and
        # WHEN (U225), so a later plan knows which write was the latest.
        steps.mark(STEP_ACCOUNT, timestamp())
        remote = outbound_account.resolve(cfg)
        playlist_id = one.target.account_id
        # U226. WHAT THE ADAPTER RECORDS FROM HERE IS THIS PAIR'S: the
        # readings its writes were judged by, read off whatever way they end.
        first = len(remote.read_backs())
        try:
            account_after = _write_account(
                one,
                remote,
                playlist_id,
                done,
                steps,
                account_listed=account_listed,
                rekordbox_after=rekordbox_after,
            )
        finally:
            done.read_backs = list(remote.read_backs()[first:])
        if account_after is None:
            if done.settle is not None:
                done.settle.rekordbox_after = (
                    tuple(rekordbox_after) if rekordbox_after is not None else None
                )
            return done
    done.snapshot = _record(
        cfg, one, rekordbox_after=rekordbox_after, account_after=account_after
    )
    steps.mark(STEP_DONE, done.account_id or one.target.key)
    steps.let_go()
    return done



def _write_account(
    one: PairPlan,
    remote: Any,
    playlist_id: str,
    done: Done,
    steps: PairSteps,
    *,
    account_listed: Sequence[str] | None,
    rekordbox_after: Sequence[playlist_pair.Row] | None = None,
) -> tuple[str, ...] | None:
    """The account side of one pair's write, and the playlist after it, or None when its order stopped (U220).

    Split out of :func:`apply_pair` by U226, so what the adapter records of
    the pair's readings is read whether the write finishes, stops or raises.
    """
    account_after: tuple[str, ...]
    removed: tuple[str, ...] = ()
    added: tuple[str, ...] = ()
    if one.account_removes:
        removed = tuple(remote.remove_tracks(playlist_id, one.account_removes))
        done.account_removed = len(removed)
    if one.account_adds:
        added = tuple(remote.add_tracks(playlist_id, one.account_adds))
        done.account_added = len(set(added))
    if one.account_order:
        moving = steps.get(STEP_MOVING)
        if not isinstance(moving, Mapping):
            # ROUND TWO'S REVIEW: the run's steps unreadable or gone, the
            # record carried beside them still says the moves went.
            moving = steps.carried(STEP_MOVING)
        if isinstance(moving, Mapping):
            # U231. AN EARLIER COMMAND OF THIS RUN BEGAN SENDING THESE MOVES,
            # and how many reached the provider before it stopped is not
            # known: sent again from a reading, a move lands on whatever now
            # stands at its position. So none is sent; the order is read once
            # the other pairs are written, and pending if it has not landed.
            end = moving.get(pair_stopped.TARGET)
            began = placeholders.parse_hearted(moving.get(pair_stopped.AT))
            done.settle = Settle(
                one=one,
                steps=steps,
                end=tuple(str(x) for x in end) if isinstance(end, list) else (),
                moved_at=began or pair_model._now(),
                rekordbox_after=None,
            )
            return None
        if steps.steps is None:
            # U231, ROUND ONE'S REVIEW. MOVES SENT WITH NO READ BACK MUST BE
            # RECORDED, or nothing tells a later sync they were sent, and it
            # sends them again by position from a reading that lags them. A
            # write that keeps no record sends no order; this pair alone
            # stops, its additions and removals landed.
            done.order_refused = refuse(
                STEPS_UNWRITTEN,
                f"the account order of {one.name or playlist_id} was not sent: this "
                f"run's plan could not be held, so it keeps no record of its steps, and "
                f"moves sent with no read back between them that no record names "
                f"would be sent again by the next sync",
                steps=(
                    "make Cratekit's state directory writable, then run crate sync "
                    "pair again and answer both gates over the plan it shows",
                ),
                origin=_ORIGIN,
                detail={"account_id": playlist_id},
            ).cause
            done.name = one.name
            return None
        # R-1420, ROUND ONE'S REVIEW. WHETHER AN EARLIER COMMAND OF THIS RUN
        # BEGAN THIS ORDER, read before this one marks it: with no move sent
        # (the branch above returned otherwise), it was refused, parked or
        # stopped with the whole write, and its continue agrees first. A
        # finish keeps what R-1411 holds it to. ROUND TWO'S REVIEW: the run's
        # steps unreadable or gone, the record carried beside them still
        # says the order began, as it says the moves went.
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is not None
        # BEFORE THE FIRST MOVE (U210): from here the order is this run's.
        # U225. AND WHAT THE ORDER IS DOING, so a later fresh plan that finds
        # it stopped reads its moves as this write's: the order it starts
        # from, the order it asks, the side that led, and rekordbox as it
        # stands, committed by this write or as the plan read it. THE START IS
        # WHAT THE ADAPTER ANSWERED, not what was asked: it leaves out of its
        # answer a track the provider would not add, and a plan that took the
        # asked additions as landed would read that track as taken off the
        # account and take it out of rekordbox.
        steps.mark(
            STEP_ORDERING,
            pair_stopped.ordering_step(
                at=timestamp(),
                start=pair_merge.appended(
                    one.account_before or one.account_now, removed, added
                ),
                target=one.account_order,
                leader=one.merged.leader,
                rekordbox=(
                    [(row.content_id, row.row_id) for row in rekordbox_after]
                    if rekordbox_after is not None
                    else one.rekordbox_before
                ),
                written=rekordbox_after is not None,
                links=one.links,
            ),
        )
        # R-1372. AND KEPT PAST THE RUN, before the first move: the run's
        # steps are released when it ends and pruned once older than a held
        # plan is kept, and a pair left part ordered is part ordered for as
        # long as nothing writes over it, so a later plan reads this record
        # whatever its age until the pair's snapshot passes it.
        steps.carry()
        # U220. AN ORDER THIS RUN ALREADY SAW REFUSED moves nothing until
        # the adapter's reading agrees with the check's own listing of it.
        # R-1420. AND ONE AN EARLIER COMMAND BEGAN AND STOPPED BEFORE ANY
        # MOVE, whatever stopped it, not only a refusal (round one's review).
        # That listing was judged in order by the check where this is no
        # finish, so a person's reorder before the check stopped the write
        # before here (`_ordered_by_this_run`), and one after it is refused
        # by the adapter's agreement with it.
        # R-1394. NOR DOES ONE THAT FINISHES A STOPPED ORDER: the plan read
        # the playlist where that order's moves left it, at or past what was
        # sent, and a reading the adapter takes seconds later may still lag
        # them, which its own check of what the playlist holds cannot see.
        # Where this write also adds or removes, the listing no longer is
        # the playlist, and the adapter's check of what it holds stands.
        expect = (
            tuple(account_listed)
            if account_listed is not None
            and (
                steps.has(STEP_ORDER_REFUSED)
                or (continued and not one.finishing_order)
                or (one.finishing_order and not (one.account_removes or one.account_adds))
            )
            else None
        )
        # R-1411. AND HELD TO THE ORDER THE PLAN AGREED ON, whatever else this
        # write does: a reading that holds every track the additions and
        # removals left, in the order from before the stopped moves, passes
        # the check of what it holds, and moves sent by position from it
        # scramble the playlist. Every track of the plan's reading the
        # adapter's still holds must stand in that order; one added may stand
        # anywhere. THE PLAN'S READING, the one its stopped write was judged
        # from and carried in the held plan, NOT THE CHECK'S LISTING (round
        # one's review): a continue's check reads what the playlist holds and
        # not its order, and a plan made again in this command has no check
        # at all. Passed only when set, so a stand in for the adapter that
        # does not take it is asked what it always was. R-1418: and only when
        # the plan read the account, since an empty reading agrees on no
        # order. No plan reaches here with one: with nothing listed the
        # additions go in the merged order, so the plan asks no order.
        agreed = (
            {"agreed": tuple(one.account_before)}
            if one.finishing_order and one.account_before
            else {}
        )

        moves_sent: list[tuple[str, ...]] = []

        def begun(
            start: tuple[str, ...], end: tuple[str, ...]
        ) -> Callable[[int, int], None]:
            # U231. RECORDED AND CARRIED BEFORE THE FIRST MOVE IS SENT, so a
            # continue or a later plan knows the moves went blind and never
            # sends them again from a reading that may lag them.
            at = timestamp()
            steps.mark(STEP_MOVING, pair_stopped.moving_step(at=at, start=start, end=end))
            steps.carry()
            moves_sent.append(end)

            def sending(sent: int, landed: int) -> None:
                # R-1394. AND HOW FAR THEY CAN HAVE GOT, before each move is
                # sent, so a later plan never finishes the order from a reading
                # before the moves the provider accepted: one that cannot be
                # recorded sends no further move.
                steps.mark(
                    STEP_MOVING,
                    pair_stopped.moving_step(
                        at=at, start=start, end=end, sent=sent, landed=landed
                    ),
                )
                steps.carry()

            return sending

        try:
            sent = tuple(
                remote.order_tracks(
                    playlist_id, one.account_order, expect=expect, begun=begun, **agreed
                )
            )
        except jobs.Parked:
            raise
        except CratekitError as exc:
            if exc.cause.reason not in ORDER_REFUSALS:
                raise
            # U220. THIS PAIR ALONE STOPS. Its adds and removals landed and
            # its rekordbox side is written; it is left unfinished, its
            # snapshot unmoved, for a continue of the run to put in order,
            # and the write goes on to every other pair.
            steps.mark(STEP_ORDER_REFUSED, exc.cause.message)
            done.order_refused = exc.cause
            done.name = one.name
            return None
        if not moves_sent:
            # NOTHING MOVED: the adapter's one judged reading already stood
            # in the asked order, so it is the playlist as it stands.
            return sent
        steps.mark(STEP_MOVED, timestamp())
        steps.carry()
        done.account_ordered = True
        done.settle = Settle(
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
        )
        return None
    elif account_listed is not None and not (one.account_removes or one.account_adds):
        account_after = tuple(account_listed)
    else:
        account_after = tuple(remote.playlist_tracks(playlist_id))
    return account_after



def _settle(cfg: config.Config, done: Sequence[Done]) -> None:
    """Read each order sent this command once, after its window, and finish or leave it pending (U231).

    RUN ONCE EVERY PAIR IS WRITTEN, so each order's window from its last
    move is spent on the other pairs' writes and only what is left of it is
    slept, earliest first. One judged reading each (``settled_order``).
    Read as the moves leave it: the pair's snapshot is recorded and the pair
    is done, as a pair whose writes all read back always was. Anything else,
    a lag, another order or a reading refused: the pair is left pending, its
    snapshot unmoved, its reading kept on the pair for the next plan to agree
    with, and its carried record (R-1372) keeps the moves it sent.
    """
    from cratekit.modules.outbound import account as outbound_account
    from cratekit.modules.outbound import pairs

    settling = sorted((one for one in done if one.settle is not None), key=lambda d: d.settle.moved_at)
    if not settling:
        return
    remote = outbound_account.resolve(cfg)
    for one in settling:
        settle = one.settle
        assert settle is not None
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
        first = len(remote.read_backs())
        reading: tuple[str, ...] | None
        try:
            reading = remote.settled_order(settle.one.target.account_id, wait=max(0.0, left))
        except jobs.Parked:
            raise
        except CratekitError as exc:
            if exc.cause.reason not in ORDER_REFUSALS:
                raise
            reading = None
        finally:
            one.read_backs.extend(remote.read_backs()[first:])
        one.settle = None
        if reading is not None and tuple(reading) == tuple(settle.end):
            one.snapshot = _record(
                cfg,
                settle.one,
                rekordbox_after=settle.rekordbox_after,
                account_after=reading,
            )
            settle.steps.mark(STEP_DONE, one.account_id or settle.one.target.key)
            settle.steps.let_go()
            continue
        one.pending = True
        one.name = settle.one.name
        if reading is not None:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
