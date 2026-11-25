"""The three way merge of one playlist pair: the last sync, the account now, rekordbox now.

U130. A pair is an account playlist and the rekordbox playlist marked to stay
the same list. This decides the list now from four sequences alone, each side
now and at the last sync, reading and writing nothing, so every rule is
drivable without a database, an account or a gate.

**THE KEYS ARE THE CALLER'S.** Both sides arrive in one key space, so this
never asks what a key means. ``sync/pair_plan.py`` gives a rekordbox row the
account has no match for a key of its own, so it is kept in rekordbox and
never asked off the account.

**EACH SIDE HAS ITS OWN BASE.** The sides can rightly differ after a sync, so
each side's changes are measured against what it held, and a track a side
never held is never read as one it removed.

**THE RULE.** A track is kept when a side holds it and no side removed it, or
when a side added it and the other's removal is not known to be later, so
nothing is lost unless its removal is the later change. A track taken out and
put back counts as added: a new membership row in rekordbox, a later added
date on the account (U202, R-990).

**THE LATER OF TWO OPPOSITE CHANGES WINS (U202).** A track added on one side
and removed on the other goes the way of the later change. A moment at or
before ``Base.synced``, or with no zone, is unknown. Where either moment is
unknown, as a removal's usually is, the addition wins, and every such call is
returned (``Merged.calls``) so the gate names it. A tie keeps the track.

**THE FIRST SYNC ADDS ONLY.** With no base nothing can have been removed.

**THE ORDER FOLLOWS THE SIDE THAT CHANGED ORDER.** Rekordbox leads when it
alone changed relative order since the base; the account leads otherwise.
The leading order stands, and each track only the other side holds goes
right after the track it follows there, so a track added mid playlist stays
mid playlist.

**EXCEPT WHERE THE BASE'S TWO SIDES DISAGREE ON ORDER (R-1404).** Such a base
records a rekordbox order that never crossed to the account (U231 writes no
account order outside GIG READY), so with neither side changed since,
rekordbox leads rather than the account putting its older order back. The
account still leads when it changed order since the base.

**EXCEPT ON THE FIRST SYNC OF A PAIR WHOSE ACCOUNT ORDER IS NOT KEPT (R-1416).**
With ``order_kept`` false, no stopped write handed in (U234) and rekordbox
holding a track, rekordbox leads, or its order is lost for good. Its order
then stands until the account changes order. An empty rekordbox playlist is
led by the account.

**AFTER A WRITE STOPPED PART WAY THROUGH ITS ORDER, CHANGED SINCE THAT WRITE
(U225).** The caller hands in what it left (:class:`Stopped`), and each
side's change of order is measured against that instead of the base, so the
write's own moves are never read as a person's reorder. With neither side
changed since, the side that led it leads again and its order is finished.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType

#: The two sides, as a leading side is named.
ACCOUNT = "account"
REKORDBOX = "rekordbox"

#: What a call between an addition on one side and a removal on the other came to.
ADDITION_LATER = "addition-later"
REMOVAL_LATER = "removal-later"
TIME_UNKNOWN = "time-unknown"

#: No moments, the default a side that knows none carries.
_NO_MOMENTS: Mapping[str, datetime] = MappingProxyType({})


def distinct(keys: Iterable[str]) -> tuple[str, ...]:
    """The keys in order, each once at its first position, empties dropped.

    A second copy is not a second track, so copies are left where they are.
    """
    return tuple(dict.fromkeys(str(key) for key in keys if str(key)))


@dataclass(frozen=True, slots=True)
class Side:
    """One side as a sync reads it: its tracks in order, the ones it put back, and when.

    ``readded`` is the tracks it took out and put back since the base (U202);
    a key it does not hold is ignored. ``added_at`` and ``removed_at`` say
    when, where the side can (U202); a missing key is a moment unknown.
    """

    keys: tuple[str, ...]
    readded: frozenset[str] = frozenset()
    added_at: Mapping[str, datetime] = _NO_MOMENTS
    removed_at: Mapping[str, datetime] = _NO_MOMENTS

    def __post_init__(self) -> None:
        object.__setattr__(self, "keys", distinct(self.keys))
        object.__setattr__(self, "added_at", MappingProxyType(dict(self.added_at)))
        object.__setattr__(self, "removed_at", MappingProxyType(dict(self.removed_at)))


@dataclass(frozen=True, slots=True)
class Base:
    """What each side held when the previous sync finished, in order, and when it finished.

    ``synced`` is the moment that sync recorded, or None when it is not known;
    a change dated at or before it was not made since it (U202).
    """

    account: tuple[str, ...]
    rekordbox: tuple[str, ...]
    synced: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "account", distinct(self.account))
        object.__setattr__(self, "rekordbox", distinct(self.rekordbox))


@dataclass(frozen=True, slots=True)
class Stopped:
    """What a write stopped part way through its account order left, as the order rule reads it (U225).

    ``account`` is the order it was writing, ``rekordbox`` rekordbox's order
    when it began, and ``leader`` the side that led it.
    """

    account: tuple[str, ...]
    rekordbox: tuple[str, ...]
    leader: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "account", distinct(self.account))
        object.__setattr__(self, "rekordbox", distinct(self.rekordbox))


@dataclass(frozen=True, slots=True)
class Call:
    """One track added on one side and removed on the other since the last sync, decided (U202).

    ``added_at`` and ``removed_at`` are the two moments as the merge read them,
    None where unknown. The later one wins; unknown, or a tie, keeps the track.
    """

    key: str
    #: The side that added it; the other side removed it.
    added_on: str
    added_at: datetime | None
    removed_at: datetime | None

    @property
    def outcome(self) -> str:
        if self.added_at is None or self.removed_at is None:
            return TIME_UNKNOWN
        return REMOVAL_LATER if self.removed_at > self.added_at else ADDITION_LATER

    @property
    def kept(self) -> bool:
        return self.outcome != REMOVAL_LATER

    @property
    def removed_on(self) -> str:
        return REKORDBOX if self.added_on == ACCOUNT else ACCOUNT


@dataclass(frozen=True, slots=True)
class Merged:
    """The list both sides should hold, and what each side must do to hold it.

    Additions are in ``order``, removals in the side's own order, the order a
    write should take them.
    """

    order: tuple[str, ...]
    leader: str
    first: bool
    add_account: tuple[str, ...] = ()
    remove_account: tuple[str, ...] = ()
    add_rekordbox: tuple[str, ...] = ()
    remove_rekordbox: tuple[str, ...] = ()
    #: Tracks a side removed that the other side added again, and kept.
    readded_over_removal: tuple[str, ...] = field(default=())
    #: U202. Every track added on one side and removed on the other, decided.
    calls: tuple[Call, ...] = field(default=())

    @property
    def changes(self) -> int:
        return (
            len(self.add_account)
            + len(self.remove_account)
            + len(self.add_rekordbox)
            + len(self.remove_rekordbox)
        )


def order_changed(now: Sequence[str], base: Sequence[str]) -> bool:
    """Whether the tracks held both now and at the base stand in another order."""
    held_now = set(now)
    held_then = set(base)
    return [key for key in now if key in held_then] != [key for key in base if key in held_now]


def placed(leading: Sequence[str], other: Sequence[str]) -> tuple[str, ...]:
    """The leading order, with each track only ``other`` holds put after its predecessor.

    A run of new tracks keeps its own order; one with nothing placed before it
    goes at the start.
    """
    result = list(distinct(leading))
    at = {key: index for index, key in enumerate(result)}
    anchor = -1
    for key in distinct(other):
        if key in at:
            anchor = at[key]
            continue
        anchor += 1
        result.insert(anchor, key)
        at = {held: index for index, held in enumerate(result)}
    return tuple(result)


def merge(
    base: Base | None,
    account: Side,
    rekordbox: Side,
    *,
    stopped: Stopped | None = None,
    order_kept: bool = True,
) -> Merged:
    """Decide the list both sides should hold. Pure.

    ``base`` is None on a pair's first sync. ``stopped`` (U225) and
    ``order_kept`` (U231, R-1416) steer the order rule, as the module says.
    """
    held_account = set(account.keys)
    held_rekordbox = set(rekordbox.keys)
    first = base is None
    then_account = set(base.account) if base is not None else set()
    then_rekordbox = set(base.rekordbox) if base is not None else set()

    since = base.synced if base is not None else None

    def moment(times: Mapping[str, datetime], key: str) -> datetime | None:
        # A MOMENT NOT AFTER THE BASE'S SYNC IS NOT A CHANGE SINCE IT, and one
        # with no zone cannot be ordered against one with, so both are unknown.
        at = times.get(key)
        if not isinstance(at, datetime) or at.tzinfo is None:
            return None
        if since is not None and (since.tzinfo is None or not at > since):
            return None
        return at

    kept: set[str] = set()
    over_removal: list[str] = []
    calls: list[Call] = []
    for key in distinct((*account.keys, *rekordbox.keys)):
        if first:
            kept.add(key)
            continue
        added_account = key in held_account and (
            key not in then_account or key in account.readded
        )
        added_rekordbox = key in held_rekordbox and (
            key not in then_rekordbox or key in rekordbox.readded
        )
        removed = (key in then_account and key not in held_account) or (
            key in then_rekordbox and key not in held_rekordbox
        )
        added = added_account or added_rekordbox
        if added and removed:
            # ONE SIDE ADDED IT AND THE OTHER REMOVED IT: a side that removed
            # a track does not hold it, so the adder is the side holding it.
            adder, adding, removing = (
                (ACCOUNT, account, rekordbox) if added_account else (REKORDBOX, rekordbox, account)
            )
            call = Call(key, adder, moment(adding.added_at, key), moment(removing.removed_at, key))
            calls.append(call)
            if call.kept:
                kept.add(key)
                over_removal.append(key)
            continue
        # R-2071: an added track that was also removed took the branch above,
        # so here an added track is never removed, and not removed is the test.
        if not removed:
            kept.add(key)

    leader = ACCOUNT
    if stopped is not None:
        # U225. CHANGED SINCE THE STOPPED WRITE, NOT SINCE THE BASE.
        account_moved = order_changed(account.keys, stopped.account)
        if order_changed(rekordbox.keys, stopped.rekordbox) and not account_moved:
            leader = REKORDBOX
        elif not account_moved and stopped.leader == REKORDBOX:
            leader = REKORDBOX
    elif base is None and not order_kept and rekordbox.keys:
        # R-1416. A FIRST SYNC WHOSE ACCOUNT ORDER IS NEVER WRITTEN keeps the
        # order rekordbox stands in, or the DJ's arrangement is lost for good.
        leader = REKORDBOX
    elif base is not None and not order_changed(account.keys, base.account):
        # R-1404. A BASE WHOSE SIDES DISAGREE ON ORDER HOLDS REKORDBOX'S, so with
        # neither side changed since, rekordbox's order stands.
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
            leader = REKORDBOX
    leading, other = (
        (rekordbox.keys, account.keys) if leader == REKORDBOX else (account.keys, rekordbox.keys)
    )
    order = tuple(
        key for key in placed(leading, other) if key in kept
    )
    return Merged(
        order=order,
        leader=leader,
        first=first,
        add_account=tuple(key for key in order if key not in held_account),
        remove_account=tuple(key for key in account.keys if key not in kept),
        add_rekordbox=tuple(key for key in order if key not in held_rekordbox),
        remove_rekordbox=tuple(key for key in rekordbox.keys if key not in kept),
        readded_over_removal=tuple(over_removal),
        calls=tuple(calls),
    )


def as_held(order: Sequence[str], holds: Iterable[str] | Mapping[str, object]) -> tuple[str, ...]:
    """``order`` narrowed to the tracks one side will hold once the sync is written."""
    wanted = set(holds)
    return tuple(key for key in order if key in wanted)


def appended(now: Sequence[str], removed: Iterable[str], added: Sequence[str]) -> tuple[str, ...]:
    """The order a side holds after removals and plain appends, before any reorder."""
    gone = set(removed)
    kept = [key for key in distinct(now) if key not in gone]
    present = set(kept)
    return tuple(kept + [key for key in distinct(added) if key not in present])


__all__ = [
    "ACCOUNT", "ADDITION_LATER", "REKORDBOX", "REMOVAL_LATER", "TIME_UNKNOWN", "Base", "Call",
    "Merged", "Side", "Stopped", "appended", "as_held", "distinct", "merge", "order_changed",
    "placed"
]
