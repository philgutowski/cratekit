"""What a ``crate sync pair`` write is expected to cost in provider calls (U210).

WHY THIS EXISTS. Sitting 54's live sync of every pair stopped on its call
ceiling after making 94 of 101 account playlists. The ceiling (U193) is a line
per command, and nothing said before the write that the line was lower than
the write planned. So the gates show what the command that writes is expected
to spend, and a stop part way says what the continue is expected to spend,
both from this module.

**AN ESTIMATE FROM THE ACCOUNT SEAM'S OWN SHAPE, NOT A MEASUREMENT.** The
account adapter (``modules/outbound/tidal_account.py``) makes its calls in a
fixed shape, and each count here follows it:

* a playlist is OPENED with one call, and its tracks are read a page of
  :data:`PLAYLIST_PAGE` at a time, so a listing is one call and its pages;
* a playlist is MADE with one call, set private with one more, and put in its
  folder with a third; a root folder is made with one call, once per folder;
* tracks are ADDED :data:`ADD_CHUNK` a request, after the playlist is opened,
  and the membership is read first unless the adapter already holds it;
* tracks are TAKEN OFF :data:`REMOVE_CHUNK` a request by position: the
  positions are read once, and each request is followed by a fresh open and
  read, which the next request reuses;
* a reading a removal or an order is JUDGED by, the positions read, the
  first reading of an order and every read back, reads the playlist twice,
  its pages and then the client's unpaged read (U226), so it costs one call
  more than a listing, :data:`UNPAGED_READ`, and more past a page, since the
  unpaged read walks on past a capped first page one track back per request
  (R-1360), :func:`unpaged_calls`;
* an ORDER moves one track to the front per request, each followed by a
  fresh open and read, after the longest run at the tail of the asked order
  already standing is kept (U220). A reading the adapter takes again, after a
  read that lags a write or a stale tag, is not counted: it happens only when
  the provider lags, and the ceiling's margin is what covers it.

The adapter's own chunk sizes cannot be imported here, since its module needs
the provider library the slim profile does not install, so a test pins these
to the adapter's. A rekordbox write makes no provider call at all.

Layer: modules.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from typing import Any

from cratekit.acquire import listing

#: Tracks one page of a playlist listing reads, the listing seam's own size.
PLAYLIST_PAGE = listing.PAGE_SIZES["playlist_tracks"]
#: U226. The one request the client's unpaged read of a playlist makes, beside
#: its pages, wherever a write is judged or an order planned, when its first
#: request holds the playlist whole; :func:`unpaged_calls` counts the rest.
UNPAGED_READ = 1
#: Tracks one add request carries and one removal request takes off, the
#: account adapter's ``ADD_CHUNK`` and ``REMOVE_CHUNK``, pinned by a test.
ADD_CHUNK = 100
REMOVE_CHUNK = 50
#: The calls making one account playlist costs: the create, the private step
#: and the move into its folder.
MAKE_PLAYLIST = 3
#: The calls making one root folder costs.
MAKE_FOLDER = 1
#: The calls reading one folder's playlists, or the account's root folders,
#: for the check before the write. Read a page of fifty at a time; a folder a
#: sync of every pair keeps holds well under a page, so one call is the count.
READ_FOLDER = 1

#: The margin a named ``--calls`` value carries over the estimate, and the
#: step it is rounded up to, so a value a person types is a round one and an
#: estimate a little low still finishes.
MARGIN = 1.25
ROUND_TO = 100


def pages(count: int) -> int:
    """The page requests a listing of ``count`` tracks makes.

    Measured on the listing seam itself (``tests/test_sync_pair_calls.py``):
    a walk on the declared total asks one page per full page and one more,
    so an empty playlist costs a page and one of exactly a hundred costs two.
    """
    return max(0, count) // PLAYLIST_PAGE + 1


def listing_calls(count: int) -> int:
    """One playlist opened and read whole: the open and its pages."""
    return 1 + pages(count)


def unpaged_calls(count: int) -> int:
    """The requests the client's unpaged read of ``count`` tracks makes (U226, R-1360).

    One, and past a page as many more as its walk asks: each later request
    starts one track back, so it reads one page less a track that is new.
    Counted as if the provider caps the unpaged read at the window's page,
    which is what the listing seam records and was not measured live; a
    provider serving more a request spends less than counted here.
    Measured on the listing seam itself (``tests/test_sync_pair_calls.py``).
    """
    beyond = max(0, count) - PLAYLIST_PAGE
    if beyond <= 0:
        return UNPAGED_READ
    return UNPAGED_READ + math.ceil(beyond / (PLAYLIST_PAGE - 1))


def judged_calls(count: int) -> int:
    """One playlist opened and read for a write to be judged by: its pages and its unpaged read (U226)."""
    return listing_calls(count) + unpaged_calls(count)


def _moves(before: Sequence[str], order: Sequence[str]) -> int:
    """How many tracks the adapter's order moves, by its own rule.

    A track held twice, or not held, is not moved. The longest run at the
    tail of the asked order already standing in that order stays; every track
    before it is moved to the front once (U220).
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
) -> int:
    """The calls one account playlist's writes are expected to make.

    ``held`` is what the playlist holds before the write, ``made`` that the
    write made it, so the adapter already holds its (empty) membership and
    the make itself is counted by the caller. ``listed`` says the check before
    the write listed it, which a playlist with nothing to write records as its
    snapshot rather than listing again (U209).
    """
    if not (adds or removes or order) and listed:
        return 0
    calls = 0
    now = [str(one) for one in held]
    known = made
    gone = {str(one) for one in removes}
    taking = [one for one in dict.fromkeys(str(one) for one in removes) if one in set(now)]
    if removes:
        # The positions are read once; each request is a send and a read back.
        calls += judged_calls(len(now))
        if taking:
            # Each request takes up to a chunk of positions off, then reads
            # the playlist back at its new length.
            length = len(now)
            owed = sum(1 for one in now if one in gone)
            while owed > 0:
                taken = min(owed, REMOVE_CHUNK)
                owed -= taken
                length -= taken
                calls += 1 + judged_calls(length)
            now = [one for one in now if one not in gone]
        known = True
    lacking = [one for one in dict.fromkeys(str(one) for one in adds) if one not in set(now)]
    if adds:
        if not known:
            calls += listing_calls(len(now))
            known = True
        if lacking:
            calls += 1 + math.ceil(len(lacking) / ADD_CHUNK)
            now = [*now, *lacking]
    if order:
        calls += judged_calls(len(now))
        calls += _moves(now, order) * (1 + judged_calls(len(now)))
    elif not known:
        # The write lists the playlist once to record its snapshot.
        calls += listing_calls(len(now))
    return calls


def pair_write(one: Any, *, made_before: bool = False) -> int:
    """The calls one pair's account side is expected to make, a made playlist's make included.

    ``one`` is a ``pair_cli.PairPlan``. ``made_before`` says an earlier command
    of the run made the account side, so only its filling is left, and the
    adapter, a fresh process's, reads its membership first rather than
    holding the empty one its own make left.
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
    """The calls the check before the write is expected to make (U209's check).

    Each paired account playlist listed once, each folder a made side goes in
    read once, and the root folders read once when a made side's folder is
    one the write makes.
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
    "ADD_CHUNK",
    "MAKE_FOLDER",
    "MAKE_PLAYLIST",
    "MARGIN",
    "PLAYLIST_PAGE",
    "READ_FOLDER",
    "REMOVE_CHUNK",
    "ROUND_TO",
    "UNPAGED_READ",
    "account_write",
    "check",
    "folders_made",
    "judged_calls",
    "listing_calls",
    "named",
    "pages",
    "pair_write",
    "unpaged_calls",
]
