"""The three way merge of one playlist pair: the last sync, the account now, rekordbox now.

U130. A pair is one of the author's own account playlists and the rekordbox
playlist marked to stay the same list as it. Each sync compares each side with
what that side held when the previous sync finished, and this module decides,
from those four sequences alone, what the list is now. It reads nothing and
writes nothing, so every rule below is drivable without a database, an account
or a gate.

**THE KEYS ARE THE CALLER'S.** Both sides arrive in ONE key space, a track the
caller has matched across the two sides carrying one key on both, so this
module never asks what a key means. ``sync/pair_cli.py`` gives a track the
account carries its remote identifier, and a rekordbox row the account has no
match for a key of its own, so such a row is kept in rekordbox and is never
something the account could be asked to take off.

**EACH SIDE HAS ITS OWN BASE.** The two sides can rightly hold different lists
after a sync: a rekordbox row the account has no match for stays in rekordbox
only, and an account track waiting to be acquired is on the account only. So
each side's changes are measured against what that side itself held, and a
track one side never held is never read as one it removed.

**THE RULE.** A track is kept when a side holds it now and no side removed
it, or when a side added it and the other side's removal is not known to be
later. Added means held now and not held at the base; removed means held at
the base and not now. An addition beats a removal it is not known to precede,
so nothing is lost unless somebody removed it somewhere and that removal is
the later change. A track taken out and put back on one side between two syncs
counts as added there: rekordbox shows it by a membership row that is not the
row the base recorded, and the account by an added date later than the one
the base recorded and than the base's own sync (U202, which closes R-990).

**THE LATER OF TWO OPPOSITE CHANGES WINS (U202).** Decided by Phillip on
2026-11-04: where a track was added on one side and removed on the other since
the last sync, the change made later is applied to both, so a track taken out
in rekordbox after it was put back on the account comes off both, and one put
back on the account after it was taken out in rekordbox stays on both. Each
side says when it added a track it holds (``Side.added_at``) and when it lost
a track the base held (``Side.removed_at``), when it knows. A moment at or
before the base's own sync (``Base.synced``) cannot be a change made since it,
and a moment with no zone cannot be compared with one that has, so both are
read as unknown. Where either moment is unknown, which a removal's usually is
since the account keeps no record of one, the addition wins as before, and
every such call is returned (``Merged.calls``) so the gate names it. A tie
keeps the track, since a tie loses nothing.

**THE FIRST SYNC ADDS ONLY.** With no base nothing can have been removed, so
every track either side holds is kept.

**THE ORDER FOLLOWS THE SIDE THAT CHANGED ORDER.** A side changed order when the
tracks it holds now and held at the base stand in a different relative order.
Rekordbox leads when it alone changed order; the account leads otherwise, which
is when it alone did, when both did, when neither did, and on the first sync of
a pair whose account order is kept. The leading side's order is kept as it stands, and each track only the other
side holds is placed right after the track it follows on that side, so a track
added mid playlist stays mid playlist rather than going to the end.

**EXCEPT WHERE THE BASE'S TWO SIDES DISAGREE ON ORDER (R-1404).** A whole write
always puts rekordbox in the merged order, so a base whose rekordbox order
disagrees with its account order, on the tracks both held, records an order
that never crossed to the account: since U231 a pair outside GIG READY has no
account order written, so a rekordbox reorder, or a track rekordbox placed mid
playlist that the account appended, leaves its base so. The order the last
sync settled on is then rekordbox's, and with neither side changed since,
rekordbox leads, rather than the account putting its older order back into
rekordbox two syncs after the person's reorder. The account still leads when
it changed order since the base. A base whose sides agree, which every pair
whose account order is written holds, leaves the rule above as it was.

**EXCEPT ON THE FIRST SYNC OF A PAIR WHOSE ACCOUNT ORDER IS NOT KEPT (R-1416).**
Decided by Phillip on #608 (608-outside-order-2). Outside GIG READY, unless
``outbound.pair_order_every_pair`` keeps every pair's, the account's order is
never written (U231), so a first sync led by the account would put rekordbox
in the account's order for good. The caller says whether the order is kept
(``order_kept``), and when it is not, no stopped write is handed in (none was
found, or the account stands off its path) and rekordbox holds a track,
rekordbox leads that first sync: its tracks keep their order, and each track
only the account holds is placed after its neighbour there.
The next sync then reads a base whose sides disagree, so rekordbox's order
stands until the account changes order, which brings the account's whole
order. An empty or new rekordbox playlist has no order to keep, and is led by
the account as before.

**AFTER A WRITE STOPPED PART WAY THROUGH ITS ORDER, CHANGED SINCE THAT WRITE
(U225).** Sitting 62's write stopped part way through putting the account in
order, and the next sync read the stopped write's own moves as the person's
reorder on the account and put that scramble into rekordbox. So the caller
hands the merge what that write left (:class:`Stopped`): the order it was
putting the account in and rekordbox's order as it stood, and each side's
change of order is measured against those instead of the base. Rekordbox
leads when it alone changed order since; the account leads when it did; and
when neither did, the side that led the stopped write leads again, so the
order it was writing is finished rather than read as anybody's edit.

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

    A playlist may hold one track twice. A pair is a list of tracks, and a
    second copy is not a second track, so the merge reads each side as its
    first occurrences and leaves the copies where they are.
    """
    return tuple(dict.fromkeys(str(key) for key in keys if str(key)))


@dataclass(frozen=True, slots=True)
class Side:
    """One side as a sync reads it: its tracks in order, the ones it put back, and when.

    ``readded`` is the tracks this side holds that it took out and put back
    since the base, which rekordbox tells by a membership row newer than the
    one the base recorded, and the account by an added date later than the
    one the base recorded (U202). A key in it that the side does not hold is
    ignored.

    ``added_at`` is when this side put a track it holds now there, and
    ``removed_at`` when it lost a track the base held, each only where the
    side can say (U202). A key missing from either is a moment unknown.
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

    ``account`` is the order that write was putting the account in, and
    ``rekordbox`` rekordbox's order as it stood when that order began, both as
    keys; ``leader`` is the side that led that write.
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

    ``order`` is every kept track in the merged order. The four lists are in
    the order a write should take them: additions in ``order``, removals in the
    side's own order. ``account_order`` and ``rekordbox_order`` are ``order``
    as each side can hold it, which the caller narrows further for a track one
    side cannot carry.
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

    A track ``other`` holds and ``leading`` does not goes immediately after the
    nearest track before it in ``other`` that is already placed, and after the
    tracks already inserted there, so a run of new tracks keeps its own order.
    A new track with nothing placed before it goes at the start.
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

    ``base`` is None on the first sync of a pair, which adds only.
    ``stopped`` is what a write stopped part way through its account order
    left, when the caller found one, and the order rule then reads each side's
    change of order against it (U225). ``order_kept`` is whether the account
    is put in the merged order, which the caller decides (U231); a first sync
    whose order is not kept, with no ``stopped`` handed in, is led by
    rekordbox when it holds a track (R-1416).
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
        if added or not removed:
            kept.add(key)

    leader = ACCOUNT
    if stopped is not None:
        # U225. CHANGED SINCE THE STOPPED WRITE, NOT SINCE THE BASE: its own
        # moves are nobody's edit, and with no edit since it, the side that
        # led it leads again.
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
        # R-1404. A BASE WHOSE SIDES DISAGREE ON ORDER HOLDS REKORDBOX'S as the
        # order the last sync settled on, the account's never written there,
        # so with neither side changed since, rekordbox's order stands.
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
    "ACCOUNT",
    "ADDITION_LATER",
    "REKORDBOX",
    "REMOVAL_LATER",
    "TIME_UNKNOWN",
    "Base",
    "Call",
    "Merged",
    "Side",
    "Stopped",
    "appended",
    "as_held",
    "distinct",
    "merge",
    "order_changed",
    "placed",
]
