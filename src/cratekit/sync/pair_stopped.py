"""A pair whose last account write stopped part way through its order, read back (U225).

WHY THIS EXISTS. Sitting 62's ``crate sync pair`` added six tracks to one
paired account playlist and then stopped part way through putting it in
order, leaving the account in an order neither side held. The pair's snapshot
does not move until the whole pair is written (``sync/pair_cli.py``), so the
next sync merged against the base from before that write, read the stopped
write's own moves as the person's reorder on the account, let the account
lead, and planned to put that scramble into rekordbox.

So the write records, in its run's steps (U210), what its order was doing
when it began to move tracks (:func:`ordering_step`), and the next plan reads
every run's steps still kept (:func:`stopped_writes`): the latest run that
began an account write on a pair since its last snapshot, when it began to
order that pair and never finished it, is that pair's stopped write.

**ITS MOVES ARE NOT THE PERSON'S, AND ONLY ITS MOVES.** The account adapter
moves one track to the front at a time, by a rule fixed by U220
(:func:`front_moves`, the adapter's own rule copied, since its module needs
the provider library the slim profile does not install, and held to it by a
test). From the order the write started from, the orders it can have left
are the ones that rule passes through on the way to the asked order
(:func:`passed`). The account is read as standing where the stopped write
left it when its order is one of those (:func:`reached`), leaving out of the
comparison any track added or taken off since, which moves nothing.

**OFF THE PATH IS NOT A REORDER ON THAT ALONE (U234).** Sitting 87 read
accounts a stopped write left in orders none of its moves leaves, after moves
answered 412 or sent by position on a reading that lagged: the provider's
partial state as often as a person's edit. Such an order is read as the
stopped write's too, finished as one on the path is, unless readings plans
kept after the stop, each off the path and settled over the agreement window,
show the account moved from one order to another (:func:`reordered`). One reading shows
nothing, and nor do two that differ, since the provider serves a playlist's
older orders for minutes after a change (``sync/pair_cli``).

**AND ITS ADDITIONS AND REMOVALS, WHEN IT WROTE BOTH SIDES.** A write begins
its order only once its removals and additions on the account have returned,
so where it also committed rekordbox both sides hold what it wrote: the plan
then merges against what that write left, the account as its removals and
additions left it and rekordbox as its commit did, which is the snapshot it
would have recorded had its order finished. Where it skipped rekordbox
neither base moves, since a base moved for one side alone reads the other
side's removals as never made (``docs/solutions``, the two sided snapshot).

**SENT BLIND, A WRITE IS PENDING UNTIL IT CAN BE READ (U231).** Since U231
the adapter sends an order's moves with no read back between them, and the
write records, before the first is sent, the reading they were planned from
and the order they leave (:func:`moving_step`); it records too when every
move was accepted. Sitting 86 measured the provider serving old orders for
minutes after the moves landed, so a write that began sending is read as
pending: the next plan finishes it when the account shows the order the
moves leave (:func:`shows`), and otherwise waits for two readings that agree
(``sync/pair_cli``). When every move was accepted, a reading on the moves'
path short of their end can only be a lag, however long it agrees.

**AND HOW FAR THE MOVES CAN HAVE GOT (R-1394).** Before each move is sent the
write records two counts on its moving step: ``sent``, the moves that may
have reached the provider, this one included, and ``landed``, the moves it
accepted. Written before the move, both are bounds by construction: no move
past ``sent`` was ever sent, and every move up to ``landed`` was accepted. A
move that ended on its last 412, which changed nothing (Sitting 62), brings
``sent`` back down. So the account, unless a person moved it, stands at one
of the orders ``landed`` to ``sent`` moves leave (:func:`positions`), and a
reading on the path before them is a lag however long it agrees: moved again
from it, the remaining moves land by position on the wrong tracks.

Pure: it reads and writes nothing. Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cratekit.favorites import placeholders

#: The fields an ordering step records, by name.
AT = "at"
START = "from"
TARGET = "to"
LEADER = "leader"
REKORDBOX = "rekordbox"
WRITTEN = "rekordbox_written"
LINKS = "links"
#: R-1394. The moves that may have reached the provider, and the moves it accepted.
SENT = "sent"
LANDED = "landed"
#: U234. That the write records its moving step before its first move is
#: sent, as every write has since U231, so its ordering step with no moving
#: step beside it sent no move. A record without it, written before U234,
#: says nothing either way: before U231 the moves were sent with no record.
MOVES_RECORDED = "moves_recorded"


@dataclass(frozen=True, slots=True)
class StoppedWrite:
    """One run's account write on one pair, begun and never finished, read back from its steps.

    ``start`` is the account playlist as the write's removals and additions
    left it, in order, before its first move, and ``target`` the order it was
    putting it in, both by remote identifier. ``rekordbox`` is the rekordbox
    playlist as it stood when the order began, its memberships as
    ``(content_id, row_id)``, and ``written`` whether this write committed
    them, so whether rekordbox holds what this write merged. ``links`` is
    each account track the write matched with a rekordbox row, remote
    identifier to content row, which its snapshot would have recorded and
    never did, so a row taken out of rekordbox since is still read as the
    account track it was.
    """

    run_id: str
    account_id: str
    at: datetime
    start: tuple[str, ...]
    target: tuple[str, ...]
    leader: str
    rekordbox: tuple[tuple[str, str], ...]
    written: bool
    links: Mapping[str, str]
    #: U231. When the write began sending its moves, None for a write that
    #: sent none or recorded none (any write before U231), and the order they
    #: leave; ``start`` is then the reading they were planned from. ``moved``
    #: says every move was accepted.
    moving_at: datetime | None = None
    end: tuple[str, ...] = ()
    moved: bool = False
    #: R-1394. How many of the moves from ``start`` toward ``target`` the
    #: provider accepted, and how many may have reached it, so the account
    #: stands at one of the orders ``landed`` to ``sent`` moves leave. A
    #: moving step whose counts are missing or do not fit its moves is read as
    #: nothing known, none landed and every one maybe sent.
    landed: int = 0
    sent: int = 0
    #: U234. Whether its ordering step says the write records its moving
    #: step before its first move (:data:`MOVES_RECORDED`), read only when its
    #: moving step was looked for and is absent or readable.
    moves_recorded: bool = False

    @property
    def sent_nothing(self) -> bool:
        """Whether this write is known to have sent no move: it records its moves, and recorded none (U234)."""
        return self.moves_recorded and self.moving_at is None

    @property
    def pending(self) -> bool:
        """Whether its moves were sent with no read back, so it is read as pending (U231)."""
        return self.moving_at is not None


def moving_step(
    *, at: str, start: Sequence[str], end: Sequence[str], sent: int = 0, landed: int = 0
) -> dict[str, Any]:
    """What a write records just before its first move is sent (U231), and before each after (R-1394).

    ``start`` is the reading the adapter planned the moves from and ``end``
    the order they leave. ``sent`` is how many moves may have reached the
    provider, the one about to be sent included, and ``landed`` how many it
    accepted.
    """
    return {
        AT: str(at),
        START: [str(one) for one in start],
        TARGET: [str(one) for one in end],
        SENT: int(sent),
        LANDED: int(landed),
    }


def _moving(
    value: Any,
) -> tuple[datetime, tuple[str, ...], tuple[str, ...], int | None, int | None] | None:
    """A moving step read back: when, the reading moved from, the order left and its counts, or None.

    A count that is not a whole number at least zero is read as None, not known.
    """
    if not isinstance(value, Mapping):
        return None
    at = placeholders.parse_hearted(value.get(AT))
    start = _ids(value.get(START))
    end = _ids(value.get(TARGET))
    if at is None or start is None or end is None:
        return None
    return at, start, end, _count(value.get(SENT)), _count(value.get(LANDED))


def _count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _counts(
    start: Sequence[str], target: Sequence[str], sent: int | None, landed: int | None, moved: bool
) -> tuple[int, int]:
    """``(landed, sent)`` for a pending write's moves from ``start`` toward ``target`` (R-1394).

    Every move landed once all were accepted. Counts that are missing, as on a
    write from before R-1394, or that do not fit the moves, are read as
    nothing known: none landed, and every one maybe sent.
    """
    total = len(front_moves(start, target))
    if moved:
        return total, total
    if sent is None or landed is None or not landed <= sent <= total:
        return 0, total
    return landed, sent


def ordering_step(
    *,
    at: str,
    start: Sequence[str],
    target: Sequence[str],
    leader: str,
    rekordbox: Iterable[tuple[str, str]],
    written: bool,
    links: Mapping[str, str],
) -> dict[str, Any]:
    """What a write records as it begins an account order, for a later plan to read."""
    return {
        MOVES_RECORDED: True,
        AT: str(at),
        START: [str(one) for one in start],
        TARGET: [str(one) for one in target],
        LEADER: str(leader),
        REKORDBOX: [[str(content_id), str(row_id)] for content_id, row_id in rekordbox],
        WRITTEN: bool(written),
        LINKS: {str(remote): str(row) for remote, row in sorted(links.items())},
    }


def _ids(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(one, str) and one for one in value):
        return None
    return tuple(value)


def _read(
    run_id: str,
    account_id: str,
    value: Any,
    moving: Any = None,
    moved: bool = False,
    *,
    moving_read: bool = False,
) -> StoppedWrite | None:
    """One ordering step read back, or None when it is not one this module wrote.

    ``moving`` is the pair's moving step (U231), when it has one: its write
    is then pending, and its start is the reading the moves were planned
    from, the truest record of where the account stood. ``moving_read``
    says the caller looked for one, so its absence can mean no move was
    sent (U234); a moving step present and unreadable never means that.
    """
    if not isinstance(value, Mapping):
        # A RECORD WRITTEN BEFORE U225 says only that the order began.
        return None
    at = placeholders.parse_hearted(value.get(AT))
    start = _ids(value.get(START))
    target = _ids(value.get(TARGET))
    leader = value.get(LEADER)
    rows = value.get(REKORDBOX)
    written = value.get(WRITTEN)
    links = value.get(LINKS)
    if (
        at is None
        or start is None
        or target is None
        or not isinstance(leader, str)
        or not isinstance(written, bool)
        or not isinstance(links, Mapping)
        or not all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in links.items())
        or not isinstance(rows, list)
        or not all(
            isinstance(one, list)
            and len(one) == 2
            and all(isinstance(part, str) and part for part in one)
            for one in rows
        )
    ):
        return None
    sent = _moving(moving)
    begin = sent[1] if sent is not None else start
    landed, reached_by = (
        _counts(begin, target, sent[3], sent[4], bool(moved)) if sent is not None else (0, 0)
    )
    return StoppedWrite(
        run_id=run_id,
        account_id=account_id,
        at=at,
        start=begin,
        target=target,
        leader=leader,
        rekordbox=tuple((one[0], one[1]) for one in rows),
        written=written,
        links=dict(links),
        moving_at=sent[0] if sent is not None else None,
        end=sent[2] if sent is not None else (),
        moved=sent is not None and bool(moved),
        landed=landed,
        sent=reached_by,
        moves_recorded=(
            value.get(MOVES_RECORDED) is True
            and moving_read
            and (moving is None or sent is not None)
        ),
    )


def _account_of(key: str, steps: Mapping[str, Any], *, new: str, made: str) -> str:
    """The account playlist one pair's steps are about: its key, or what a new pair was made as."""
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key


def passed_by(
    records: Iterable[Any],
    *,
    account_id: str,
    moment: datetime,
    new: str,
    account: str,
    made: str,
) -> list[tuple[str, str]]:
    """The carried records of one pair a snapshot taken at ``moment`` has passed, as ``(run_id, key)`` (R-1372).

    A pair's carried record is about a write that began at its ``account``
    step. Once the pair's snapshot is taken at or after that moment, the
    next plan reads it as no stopped write (``sync/pair_cli._Reader``), so it
    is let go. A record with no time, or of another pair, is not this
    snapshot's to let go.
    """
    passed: list[tuple[str, str]] = []
    for record in records:
        for key, steps in record.done.items():
            if not isinstance(steps, Mapping):
                continue
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None and not began > moment:
                passed.append((record.run_id, key))
    return passed


def stopped_writes(
    records: Iterable[Any],
    *,
    new: str,
    account: str,
    ordering: str,
    made: str,
    done: str,
    moving: str = "",
    moved: str = "",
) -> dict[str, tuple[datetime, StoppedWrite]]:
    """Each pair's write stopped part way through its order, by account playlist, with when it began.

    ``records`` are runs' steps (``core/held_plan.Steps``). The step names are
    the caller's: ``account`` is recorded with when the account write began,
    ``ordering`` with :func:`ordering_step`, ``made`` with the account
    playlist a pair whose account side was new was made as, and ``done`` once
    the pair finished. ``new`` is the prefix a pair whose account side is new
    is keyed by.

    THE LATEST WRITE THAT BEGAN TO ORDER AND NEVER FINISHED, unless a run
    that began its account write later finished the pair. A later run that
    began its account write and stopped before its order began does not hide
    it (round one's review): its steps are kept as the stopped write's are,
    and its additions and removals move no track the stopped write ordered.
    A record written before U225 carries no detail and no time, and is read
    as no write at all, as it was. ``moving`` and ``moved`` name the steps a
    write records as it begins sending its moves and once every one was
    accepted (U231).

    A PENDING WRITE IS NOT HIDDEN BY A LATER ONE THAT SENT NO MOVE (R-1394,
    round two's review), for the reason a later run stopped before its order
    began hides nothing: a later write whose order was refused before its
    first move (a finish whose reading was not the agreed one, a read that
    failed) left the account where the pending write's moves left it, and
    only the pending write's counts say how far that was. Read in its place,
    the next plan would take a reading lagging those moves as the person's
    reorder and merge it into rekordbox.
    """
    stopped: dict[str, tuple[datetime, StoppedWrite]] = {}
    finished: dict[str, datetime] = {}
    for record in records:
        for key, steps in record.done.items():
            if not isinstance(steps, Mapping):
                continue
            account_id = _account_of(key, steps, new=new, made=made)
            if not account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is None:
                continue
            if done in steps:
                if account_id not in finished or began > finished[account_id]:
                    finished[account_id] = began
                continue
            write = _read(
                record.run_id,
                account_id,
                steps.get(ordering),
                steps.get(moving) if moving else None,
                bool(moved) and moved in steps,
                moving_read=bool(moving),
            )
            if write is None:
                continue
            held = stopped.get(account_id)
            if held is None or (write.pending, write.at) > (held[1].pending, held[1].at):
                stopped[account_id] = (began, write)
    return {
        account_id: (began, write)
        for account_id, (began, write) in stopped.items()
        if account_id not in finished or not finished[account_id] > began
    }


def front_moves(before: Sequence[str], order: Iterable[str]) -> list[str]:
    """The tracks the account adapter moves to the front, in the order it moves them (U220).

    A copy of the adapter's rule (``_to_the_front`` in the account adapter),
    held to it by a test: a track the playlist does not hold, or holds twice,
    is not asked; the longest run at the tail of the asked order already
    standing in that order stays; every asked track before that run is moved,
    the last of them first.
    """
    counts: dict[str, int] = {}
    for one in before:
        counts[one] = counts.get(one, 0) + 1
    wanted = [str(one) for one in dict.fromkeys(order) if str(one) and counts.get(str(one)) == 1]
    asked = set(wanted)
    keep = 0
    for one in reversed([one for one in before if one in asked]):
        if keep < len(wanted) and one == wanted[len(wanted) - 1 - keep]:
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))


def passed(start: Sequence[str], target: Sequence[str]) -> tuple[tuple[str, ...], ...]:
    """Every order the adapter's moves pass through from ``start`` toward ``target``, both ends included.

    The moves from any reading part way are the rest of the moves from the
    start, since each move grows the kept tail by one, so a write that read
    the playlist again after a stale tag or a lag is still on this path.
    """
    now = list(start)
    seen = [tuple(now)]
    for one in front_moves(now, target):
        now.remove(one)
        now.insert(0, one)
        seen.append(tuple(now))
    return tuple(seen)


def finished(now: Sequence[str], target: Sequence[str]) -> tuple[str, ...]:
    """The account as a write ordering it toward ``target`` would leave it, had it finished.

    The adapter's remaining moves applied to the playlist as it stands, so a
    track added since stays where it stood among the tracks the write kept,
    as the write itself would have left it.
    """
    result = list(now)
    for one in front_moves(result, target):
        result.remove(one)
        result.insert(0, one)
    return tuple(result)


def reached(start: Sequence[str], target: Sequence[str], now: Sequence[str]) -> bool:
    """Whether the account's order ``now`` is one a write ordering ``start`` toward ``target`` left.

    A track added or taken off since is left out of the comparison, since
    neither moves the tracks both hold. A track the write would have moved
    standing anywhere else is off the path, which is a move somebody made or
    the provider's partial state, and is read as neither on that alone (U234).
    """
    return bool(positions(start, target, now))


def positions(start: Sequence[str], target: Sequence[str], now: Sequence[str]) -> tuple[int, ...]:
    """How many moves from ``start`` toward ``target`` leave the order ``now``, each count that does (R-1394).

    Read as :func:`reached` reads it, a track added or taken off since left
    out, so two orders on the path that differ only by such a track both
    count. Empty when ``now`` is off the path.
    """
    current = list(dict.fromkeys(now))
    common = set(current) & set(start)
    shown = [one for one in current if one in common]
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )


def shows(end: Sequence[str], now: Sequence[str]) -> bool:
    """Whether the account's order ``now`` is the order ``end`` a write's moves leave (U231).

    A track added or taken off since is left out of the comparison, as
    :func:`reached` leaves it out, since neither moves the tracks both hold.
    An end sharing no track with ``now`` is not shown.
    """
    current = list(dict.fromkeys(now))
    common = set(current) & set(end)
    if not common:
        return False
    return [one for one in current if one in common] == [
        one for one in dict.fromkeys(end) if one in common
    ]


def reordered(kept: Sequence[str], now: Sequence[str]) -> bool:
    """Whether the account's order ``now`` differs from a reading ``kept`` after the stop (U234).

    Read over the tracks both hold, each at its first place, so a track added
    or taken off between the two readings, which moves nothing, is no
    reorder. Two readings sharing fewer than two tracks show no order.
    """
    current = list(dict.fromkeys(now))
    common = set(current) & set(kept)
    if len(common) < 2:
        return False
    return [one for one in current if one in common] != [
        one for one in dict.fromkeys(kept) if one in common
    ]


__all__ = [
    "StoppedWrite",
    "finished",
    "front_moves",
    "moving_step",
    "shows",
    "ordering_step",
    "passed",
    "passed_by",
    "positions",
    "reached",
    "reordered",
    "stopped_writes",
]
