"""A pair whose last account write stopped part way through its order, read back (U225).

A pair's snapshot does not move until the whole pair is written
(``sync/pair_write.py``), so without this the next sync would read a stopped
write's own moves as the person's reorder and put that scramble into
rekordbox. The write records what its order was doing (:func:`ordering_step`)
in its run's steps (U210), and the next plan reads them (:func:`stopped_writes`).

**ITS MOVES ARE NOT THE PERSON'S, AND ONLY ITS MOVES.** :func:`front_moves` is
the adapter's U220 rule, copied since its module needs the provider library
the slim profile lacks, and held to it by a test. The account stands where
the write left it when its order is one that rule passes through
(:func:`passed`, :func:`reached`), a track added or taken off since left out.

**OFF THE PATH IS NOT A REORDER ON THAT ALONE (U234).** A lagging or partial
provider leaves orders off the path as often as a person does, so such an
order is the stopped write's too, unless settled readings kept after the stop
show the account moved from one order to another (:func:`reordered`). One
reading shows nothing, nor two that differ, since the provider serves older
orders for minutes (``sync/pair_plan``).

**AND ITS ADDITIONS AND REMOVALS, WHEN IT WROTE BOTH SIDES.** The order begins
only once those returned, so where it also committed rekordbox the plan
merges against what it left. Where it skipped rekordbox neither base moves,
since a base moved for one side alone reads the other side's removals as
never made (``docs/solutions``, the two sided snapshot).

**SENT BLIND, A WRITE IS PENDING UNTIL IT CAN BE READ (U231).** Moves go with
no read back between them, recorded first (:func:`moving_step`). The next
plan finishes the write when the account shows the moves' end (:func:`shows`),
and otherwise waits for two readings that agree (``sync/pair_plan``). Once
every move was accepted, a reading short of the end is only a lag.

**AND HOW FAR THE MOVES CAN HAVE GOT (R-1394).** Before each move the write
records ``sent``, moves that may have reached the provider, and ``landed``,
moves it accepted; written first, both are bounds. Unless a person moved it,
the account stands at one of the orders ``landed`` to ``sent`` moves leave
(:func:`positions`), and a reading before them is a lag however long it
agrees: moved again from it, the moves land on the wrong tracks.

Pure: it reads and writes nothing. Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cratekit.cli.output import count_of

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
#: U234. That the write records its moving step before its first move, so an
#: ordering step with none beside it sent no move. Its absence says nothing.
MOVES_RECORDED = "moves_recorded"


@dataclass(frozen=True, slots=True)
class StoppedWrite:
    """One run's account write on one pair, begun and never finished, read back from its steps.

    ``start`` is the account before its first move and ``target`` the order
    asked. ``rekordbox`` is rekordbox's memberships when the order began, and
    ``written`` whether this write committed them. ``links`` is the matches
    its snapshot never recorded, so a row taken out since still reads as the
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
    #: U231. When it began sending moves, or None, and the order they leave;
    #: ``start`` is then their reading. ``moved``: every move was accepted.
    moving_at: datetime | None = None
    end: tuple[str, ...] = ()
    moved: bool = False
    #: R-1394. Moves the provider accepted and moves that may have reached it;
    #: counts missing or unfit read as none landed and every one maybe sent.
    landed: int = 0
    sent: int = 0
    #: U234. :data:`MOVES_RECORDED`, true only when the moving step was looked
    #: for and is absent or readable.
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

    ``sent`` counts the move about to be sent; ``landed`` the moves accepted.
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
    from cratekit.favorites import placeholders
    if not isinstance(value, Mapping):
        return None
    at = placeholders.parse_hearted(value.get(AT))
    start = _ids(value.get(START))
    end = _ids(value.get(TARGET))
    if at is None or start is None or end is None:
        return None
    return at, start, end, count_of(value.get(SENT)), count_of(value.get(LANDED))


def _counts(
    start: Sequence[str], target: Sequence[str], sent: int | None, landed: int | None, moved: bool
) -> tuple[int, int]:
    """``(landed, sent)`` for a pending write's moves from ``start`` toward ``target`` (R-1394).

    All landed once all were accepted; counts missing or unfit read as none
    landed and every one maybe sent.
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

    A ``moving`` step (U231) makes the write pending and its reading the
    start. ``moving_read`` says the caller looked, so absence can mean no
    move was sent (U234); an unreadable one never means that.
    """
    from cratekit.favorites import placeholders
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

    A snapshot at or after a record's ``account`` step makes it no stopped
    write (``sync/pair_read._Reader``), so it is let go. One with no time is kept.
    """
    from cratekit.favorites import placeholders
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

    ``records`` are runs' steps (``core/held_plan.Steps``); the step names
    and the new pair prefix ``new`` are the caller's.

    THE LATEST WRITE THAT BEGAN TO ORDER AND NEVER FINISHED, unless a later
    run finished the pair. A later run that stopped before its order began
    does not hide it, since its additions and removals move no track the
    stopped write ordered. A record from before U225 is no write.

    A PENDING WRITE IS NOT HIDDEN BY A LATER ONE THAT SENT NO MOVE (R-1394):
    that left the account where the pending moves did, and only their counts
    say how far, so a lagging reading would otherwise read as a reorder.
    """
    from cratekit.favorites import placeholders
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

    The adapter's own rule: a track not held, or held twice, is not asked;
    the longest standing tail stays; the rest move last first, so each lands
    in front of the one after it.
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

    Each move grows the kept tail by one, so a write that read again part
    way is still on this path.
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

    The remaining moves applied as it stands, so a track added since stays where it stood.
    """
    result = list(now)
    for one in front_moves(result, target):
        result.remove(one)
        result.insert(0, one)
    return tuple(result)


def reached(start: Sequence[str], target: Sequence[str], now: Sequence[str]) -> bool:
    """Whether the account's order ``now`` is one a write ordering ``start`` toward ``target`` left.

    A track added or taken off since is left out, since neither moves the
    others. Off the path is not on that alone a reorder (U234).
    """
    return bool(positions(start, target, now))


def positions(start: Sequence[str], target: Sequence[str], now: Sequence[str]) -> tuple[int, ...]:
    """How many moves from ``start`` toward ``target`` leave the order ``now``, each count that does (R-1394).

    Read as :func:`reached` reads it; empty when ``now`` is off the path.
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

    Read as :func:`reached` reads it; an end sharing no track is not shown.
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

    Read over the tracks both hold, so an added or removed track is no
    reorder; fewer than two shared tracks show no order.
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
