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
comparison any track added or taken off since, which moves nothing. Any other
order is a move somebody made, and the account then leads as it always has.

**AND ITS ADDITIONS AND REMOVALS, WHEN IT WROTE BOTH SIDES.** A write begins
its order only once its removals and additions on the account have returned,
so where it also committed rekordbox both sides hold what it wrote: the plan
then merges against what that write left, the account as its removals and
additions left it and rekordbox as its commit did, which is the snapshot it
would have recorded had its order finished. Where it skipped rekordbox
neither base moves, since a base moved for one side alone reads the other
side's removals as never made (``docs/solutions``, the two sided snapshot).

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


def _read(run_id: str, account_id: str, value: Any) -> StoppedWrite | None:
    """One ordering step read back, or None when it is not one this module wrote."""
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
    return StoppedWrite(
        run_id=run_id,
        account_id=account_id,
        at=at,
        start=start,
        target=target,
        leader=leader,
        rekordbox=tuple((one[0], one[1]) for one in rows),
        written=written,
        links=dict(links),
    )


def stopped_writes(
    records: Iterable[Any],
    *,
    new: str,
    account: str,
    ordering: str,
    made: str,
    done: str,
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
    as no write at all, as it was.
    """
    stopped: dict[str, tuple[datetime, StoppedWrite]] = {}
    finished: dict[str, datetime] = {}
    for record in records:
        for key, steps in record.done.items():
            if not isinstance(steps, Mapping):
                continue
            account_id = key
            if key.startswith(new):
                account_id = steps.get(made) if isinstance(steps.get(made), str) else ""
            if not account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is None:
                continue
            if done in steps:
                if account_id not in finished or began > finished[account_id]:
                    finished[account_id] = began
                continue
            write = _read(record.run_id, account_id, steps.get(ordering))
            if write is None:
                continue
            held = stopped.get(account_id)
            if held is None or write.at > held[1].at:
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
    neither moves the tracks both hold; a track the write would have moved
    standing anywhere else is a move somebody made.
    """
    current = list(dict.fromkeys(now))
    common = set(current) & set(start)
    shown = [one for one in current if one in common]
    return any(
        [one for one in dict.fromkeys(state) if one in common] == shown
        for state in passed(start, target)
    )


__all__ = [
    "StoppedWrite",
    "finished",
    "front_moves",
    "ordering_step",
    "passed",
    "reached",
    "stopped_writes",
]
