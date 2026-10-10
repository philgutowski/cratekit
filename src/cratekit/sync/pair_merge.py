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

**EACH SIDE HAS ITS OWN BASE.** One shared snapshot would say what the list was,
and a sync whose account half was declined, or failed after the rekordbox half
landed, leaves the two sides holding different lists. Compared with one base,
the side that was not written would read as having removed what the other side
gained. Compared each with its own, a side that was not written simply has not
changed, and the next sync finishes the job.

**THE RULE.** A track is kept when a side holds it now and no side removed it,
or when a side added it, whatever the other side did. Added means held now and
not held at the base; removed means held at the base and not now. An addition
beats a removal, so a track removed on one side and added again on the other is
kept, and nothing is lost unless somebody removed it somewhere. A rekordbox
membership whose row is not the row the base recorded was taken out and put
back since, and counts as added: that is the one way a removal and a re-add on
the same side between two syncs can be seen at all, and the account has no
row identity to show it.

**THE FIRST SYNC ADDS ONLY.** With no base nothing can have been removed, so
every track either side holds is kept.

**THE ORDER FOLLOWS THE SIDE THAT CHANGED ORDER.** A side changed order when the
tracks it holds now and held at the base stand in a different relative order.
Rekordbox leads when it alone changed order; the account leads otherwise, which
is when it alone did, when both did, when neither did, and on the first sync.
The leading side's order is kept as it stands, and each track only the other
side holds is placed right after the track it follows on that side, so a track
added mid playlist stays mid playlist rather than going to the end.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

#: The two sides, as a leading side is named.
ACCOUNT = "account"
REKORDBOX = "rekordbox"


def distinct(keys: Iterable[str]) -> tuple[str, ...]:
    """The keys in order, each once at its first position, empties dropped.

    A playlist may hold one track twice. A pair is a list of tracks, and a
    second copy is not a second track, so the merge reads each side as its
    first occurrences and leaves the copies where they are.
    """
    return tuple(dict.fromkeys(str(key) for key in keys if str(key)))


@dataclass(frozen=True, slots=True)
class Side:
    """One side as a sync reads it: its tracks in order, and the ones it put back.

    ``readded`` is the tracks this side holds through a membership newer than
    the one the base recorded, which only rekordbox can tell. A key in it that
    the side does not hold is ignored.
    """

    keys: tuple[str, ...]
    readded: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        object.__setattr__(self, "keys", distinct(self.keys))


@dataclass(frozen=True, slots=True)
class Base:
    """What each side held when the previous sync finished, in order."""

    account: tuple[str, ...]
    rekordbox: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "account", distinct(self.account))
        object.__setattr__(self, "rekordbox", distinct(self.rekordbox))


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
    #: Tracks a side removed that the other side added again, so they are kept.
    readded_over_removal: tuple[str, ...] = field(default=())

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


def merge(base: Base | None, account: Side, rekordbox: Side) -> Merged:
    """Decide the list both sides should hold. Pure.

    ``base`` is None on the first sync of a pair, which adds only.
    """
    held_account = set(account.keys)
    held_rekordbox = set(rekordbox.keys)
    first = base is None
    then_account = set(base.account) if base is not None else set()
    then_rekordbox = set(base.rekordbox) if base is not None else set()

    kept: set[str] = set()
    over_removal: list[str] = []
    for key in distinct((*account.keys, *rekordbox.keys)):
        if first:
            kept.add(key)
            continue
        added = (key in held_account and key not in then_account) or (
            key in held_rekordbox
            and (key not in then_rekordbox or key in rekordbox.readded)
        )
        removed = (key in then_account and key not in held_account) or (
            key in then_rekordbox and key not in held_rekordbox
        )
        if added or not removed:
            kept.add(key)
            if added and removed:
                over_removal.append(key)

    leader = ACCOUNT
    if base is not None and order_changed(rekordbox.keys, base.rekordbox):
        if not order_changed(account.keys, base.account):
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
    "REKORDBOX",
    "Base",
    "Merged",
    "Side",
    "appended",
    "as_held",
    "distinct",
    "merge",
    "order_changed",
    "placed",
]
