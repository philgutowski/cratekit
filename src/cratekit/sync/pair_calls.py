"""What a ``crate sync pair`` write is expected to cost in provider calls (U210).

The gates show what the writing command is expected to spend, and a stop
part way what its continue will, so a call ceiling (U193) lower than the write
is said before the write rather than found part way.

**AN ESTIMATE FROM THE ACCOUNT ADAPTER'S OWN SHAPE, NOT A MEASUREMENT**
(``modules/outbound/tidal_account.py``):

* OPENING a playlist is one call, and a listing reads :data:`PLAYLIST_PAGE` a page;
* MAKING one is three calls (create, private, into its folder), a root folder one;
* ADDING goes :data:`ADD_CHUNK` a request, the membership read first unless held;
* TAKING OFF goes :data:`REMOVE_CHUNK` a request by position, each followed by
  a read back the next request reuses;
* a JUDGED reading (positions, an order's first reading, every read back)
  adds the client's unpaged read (U226), :data:`UNPAGED_READ`, and more past
  a page (R-1360), :func:`unpaged_calls`;
* an ORDER moves one track to the front per request, keeping the longest
  standing tail (U220), with NO READ BACK BETWEEN MOVES and one settle
  reading after (U231); readings and moves sent again on a lag are left to
  the ceiling's margin;
* EVERY WRITE is followed by the client's own reread for its version tag,
  :data:`REPARSE`, which the provider counts (U231).

The adapter's chunk sizes cannot be imported, since its module needs the
provider library the slim profile lacks, so a test pins these to them. A
rekordbox write makes no provider call.

Layer: modules.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from typing import Any

from cratekit.acquire import listing

#: Tracks one page of a playlist listing reads, the listing seam's own size.
PLAYLIST_PAGE = listing.PAGE_SIZES["playlist_tracks"]
#: U226. The unpaged read's one request when it holds the playlist whole;
#: :func:`unpaged_calls` counts the rest.
UNPAGED_READ = 1
#: U231. The client's reread after every write, for the next write's version tag.
REPARSE = 1
#: Tracks one add request carries and one removal request takes off, the
#: account adapter's ``ADD_CHUNK`` and ``REMOVE_CHUNK``, pinned by a test.
ADD_CHUNK = 100
REMOVE_CHUNK = 50
#: The calls making one account playlist costs: create, private, into its folder.
MAKE_PLAYLIST = 3
#: The calls making one root folder costs.
MAKE_FOLDER = 1
#: The calls reading one folder's playlists, or the root folders, for the check;
#: a synced folder holds well under a page of fifty.
READ_FOLDER = 1

#: The margin a named ``--calls`` value carries over the estimate and the step
#: it is rounded up to, so an estimate a little low still finishes.
MARGIN = 1.25
ROUND_TO = 100


def pages(count: int) -> int:
    """The page requests a listing of ``count`` tracks makes, one per full page and one more.

    Measured on the listing seam (``tests/test_sync_pair_calls.py``).
    """
    return max(0, count) // PLAYLIST_PAGE + 1


def listing_calls(count: int) -> int:
    """One playlist opened and read whole: the open and its pages."""
    return 1 + pages(count)


def unpaged_calls(count: int) -> int:
    """The requests the client's unpaged read of ``count`` tracks makes (U226, R-1360).

    One, and past a page more, each later request starting one track back.
    Counted as if the provider caps it at the window's page, as the listing
    seam records; unmeasured live, and a larger cap only spends less.
    """
    beyond = max(0, count) - PLAYLIST_PAGE
    if beyond <= 0:
        return UNPAGED_READ
    return UNPAGED_READ + math.ceil(beyond / (PLAYLIST_PAGE - 1))


def judged_calls(count: int) -> int:
    """One playlist opened and read for a write to be judged by: its pages and its unpaged read (U226)."""
    return listing_calls(count) + unpaged_calls(count)


def _moves(before: Sequence[str], order: Sequence[str]) -> int:
    """How many tracks the adapter's order moves, by its own rule (U220).

    A track held twice or not held is not moved, and the longest standing
    tail stays; every track before it moves once.
    """
    counts: dict[str, int] = {}
    for one in before:
        counts[one] = counts.get(one, 0) + 1
    wanted = [one for one in dict.fromkeys(order) if one and counts.get(one) == 1]
    asked = set(wanted)
    keep = 0
    for one in reversed(before):
        if one in asked and keep < len(wanted) and one == wanted[len(wanted) - 1 - keep]:
            keep += 1
    return len(wanted) - keep


def account_write(
    held: Sequence[str],
    *,
    adds: Sequence[str] = (),
    removes: Sequence[str] = (),
    order: Sequence[str] | None = None,
    made: bool = False,
    listed: bool = True,
    sent: bool = False,
) -> int:
    """The calls one account playlist's writes are expected to make.

    ``made``: the write made it, so its empty membership is held and the
    caller counts the make. ``listed``: the check listed it, so with nothing
    to write it is not listed again (U209). ``sent``: an earlier command
    sent the order's moves, so only the settle reading is left (U231).
    """
    if not (adds or removes or order) and listed:
        return 0
    calls = 0
    now = [str(one) for one in held]
    known = made
    gone = {str(one) for one in removes}
    held_before = set(now)
    taking = [one for one in dict.fromkeys(str(one) for one in removes) if one in held_before]
    if removes:
        # The positions are read once; each request is a send and a read back.
        calls += judged_calls(len(now))
        if taking:
            # Each request takes a chunk off, then reads back at the new length.
            length = len(now)
            owed = sum(1 for one in now if one in gone)
            while owed > 0:
                taken = min(owed, REMOVE_CHUNK)
                owed -= taken
                length -= taken
                calls += 1 + REPARSE + judged_calls(length)
            now = [one for one in now if one not in gone]
        known = True
    held_after = set(now)
    lacking = [one for one in dict.fromkeys(str(one) for one in adds) if one not in held_after]
    if adds:
        if not known:
            calls += listing_calls(len(now))
            known = True
        if lacking:
            calls += 1 + math.ceil(len(lacking) / ADD_CHUNK) * (1 + REPARSE)
            now = [*now, *lacking]
    if order and sent:
        # The moves went in an earlier command; only the reading that decides them is left.
        calls += judged_calls(len(now))
    elif order:
        calls += judged_calls(len(now))
        moves = _moves(now, order)
        if moves:
            calls += moves * (1 + REPARSE) + judged_calls(len(now))
    elif not known:
        # The write lists the playlist once to record its snapshot.
        calls += listing_calls(len(now))
    return calls


def pair_write(one: Any, *, made_before: bool = False, sent: bool = False) -> int:
    """The calls one pair's account side is expected to make, a made playlist's make included.

    ``one`` is a ``pair_model.PairPlan``. ``made_before``: an earlier command
    made the side, so a fresh adapter reads its membership first. ``sent``:
    it sent the order's moves too (U231).
    """
    new = bool(one.target.new)
    calls = MAKE_PLAYLIST if new and not made_before else 0
    return calls + account_write(
        () if new else tuple(one.account_now),
        adds=tuple(one.account_adds),
        removes=tuple(one.account_removes),
        order=one.account_order,
        made=new and not made_before,
        listed=not made_before,
        sent=sent,
    )


def folders_made(pairs: Iterable[Any], create: str) -> int:
    """The root folders the write makes: one per name a made pair's place creates."""
    return MAKE_FOLDER * len(
        {
            one.place.folder
            for one in pairs
            if one.target.new and one.place is not None and one.place.action == create
        }
    )


def check(pairs: Iterable[Any], *, create: str) -> int:
    """The calls the check before the write is expected to make (U209).

    Each paired account playlist listed once, each made side's folder read
    once, and the root folders once when the write makes a folder.
    """
    calls = 0
    folders: set[str] = set()
    root = False
    for one in pairs:
        if not one.target.new:
            # Listed with its unpaged read beside the window (U226).
            calls += judged_calls(len(one.account_now))
            continue
        place = one.place
        if place is None:
            continue
        if place.folder_id:
            folders.add(place.folder_id)
        elif place.action == create:
            root = True
    return calls + READ_FOLDER * len(folders) + (READ_FOLDER if root else 0)


def named(expected: int, line: int) -> int:
    """The ``--calls`` value to name for an expected spend: its margin, rounded, never below ``line``."""
    wanted = math.ceil(max(0, expected) * MARGIN / ROUND_TO) * ROUND_TO
    return max(int(line), int(wanted))


__all__ = [
    "ADD_CHUNK", "MAKE_FOLDER", "MAKE_PLAYLIST", "MARGIN", "PLAYLIST_PAGE", "READ_FOLDER",
    "REMOVE_CHUNK", "REPARSE", "ROUND_TO", "UNPAGED_READ", "account_write", "check",
    "folders_made", "judged_calls", "listing_calls", "named", "pages", "pair_write",
    "unpaged_calls"
]
