"""What an intake item is: one track, keyed and frozen at the queue, and the listings that freeze it.

THE ITEMS ARE THE TRACKS, AND THEY ARE KNOWN AT THE QUEUE (KTD9). Each verb
queues one item per track with what was learned about it frozen in the
payload, so the worker reads nothing off the network or the source, and a
playlist edited between queueing and driving cannot change what an item means.
:mod:`cratekit.intake.cli` re-exports every public name here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from cratekit.acquire import listing, match
from cratekit.acquire.match import Wanted
from cratekit.cli.output import load_config
from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: The reserved reference that lists the account's hearts instead of a
#: playlist. It cannot collide with a real playlist, because
#: ``tidal_catalogue.playlist_id`` accepts only an identifier or a URL.
FAVORITES = "favorites"

#: When the account says a heart was made, on a hearts job's frozen row, ISO
#: 8601 in UTC (U120), so a landing never asks the account again. On every row
#: a hearts job freezes, ``None`` when the account dates it nowhere, so the
#: key's absence means only a job an older build froze.
HEARTED = "hearted"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    return load_config(("intake.cli",))


def _unusable(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        origin=("intake.cli",),
        detail=detail,
    )


def item_key(row: Wanted) -> str:
    """The stable identifier one track is queued under, never a display name.

    A provider row is keyed by the provider's own identifier, the one thing a
    later acquisition can ask for. A recognised track carries none, so it is
    keyed by the match module's digest over the recording's identity, the
    version token and the ISRC: two recordings cannot share it and the same
    recording from two chunks folds to it.
    """
    if row.ref:
        return row.ref
    return "rc_" + match.digest(row.distinct, row.version_key, row.isrc or "")


def frozen(row: Wanted) -> dict[str, Any]:
    """One track as the payload carries it. :func:`thawed` is the mirror.

    Public because ``intake.candidates`` keeps a provider candidate on a review
    option through the same freeze, so a field added here reaches both.
    """
    return {
        "artist": row.artist,
        "title": row.title,
        "version": row.version,
        "key": row.key,
        "isrc": row.isrc,
        "origin": row.origin,
        "ref": row.ref,
        "spelled": row.spelled,
        # The other reading travels, or the worker would resolve a narrower
        # question than the reader built, on exactly the ambiguous titles.
        "other_reading": list(row.other_reading) if row.other_reading else None,
        # The worker decides SUPPRESSED from this, so a freeze that dropped it
        # could withhold the companion of a deletion that credited somebody else.
        "several_artists": row.several_artists,
    }


def _refuse_unidentified(missing: list[int]) -> None:
    """Refuse a listing whose rows at ``missing`` carry no provider identifier."""
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this playlist carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing could ever be asked "
            f"about them",
            "fetch the playlist again so every row carries its id",
            positions=missing,
        )


def frozen_rows(rows: tuple[Wanted, ...]) -> dict[str, dict[str, Any]]:
    """The items, as the listing identifies them, in order and folded once.

    A provider row without an identifier is refused by position, and the whole
    listing with it: a queue that dropped a row would report every item done
    over a playlist it did not finish. The same identifier twice folds to one
    item, first wins, because the queue keys items by identifier.
    """
    _refuse_unidentified(
        [
            position
            for position, row in enumerate(rows, start=1)
            if row.origin != match.TEXT and not row.ref
        ]
    )
    held: dict[str, dict[str, Any]] = {}
    for row in rows:
        held.setdefault(item_key(row), frozen(row))
    return held


def thawed(said: Mapping[str, Any]) -> Wanted:
    """The frozen track as the ``Wanted`` the match engine reads."""
    other = said.get("other_reading")
    reading = (
        (str(other[0]), str(other[1]))
        if isinstance(other, (list, tuple)) and len(other) == 2
        else None
    )
    return Wanted(
        artist=str(said.get("artist") or ""),
        title=str(said.get("title") or ""),
        version=str(said.get("version") or ""),
        key=str(said["key"]) if said.get("key") else None,
        isrc=str(said["isrc"]) if said.get("isrc") else None,
        origin=str(said.get("origin") or match.TEXT),
        ref=str(said.get("ref") or ""),
        spelled=str(said.get("spelled") or ""),
        other_reading=reading,
        # An older payload did not look, so its absence reads as "may have
        # billed several": one missed suppression rather than a withheld track.
        several_artists=bool(said.get("several_artists", True)),
    )


def _read_rows(rows: list, reference: str) -> tuple[Wanted, ...]:
    """Provider rows as ``Wanted`` rows, refusing a list this verb cannot use."""
    try:
        return match.read_tidal_tracks(rows)
    except match.UnreadableList as exc:
        raise _unusable(str(exc), source=reference) from exc


def list_playlist(found: catalogue.Catalogue, reference: str) -> dict[str, dict[str, Any]]:
    """One playlist's tracks, frozen and keyed by item, as a playlist job queues them.

    The listing and its failure boundary are the label verb's own, so
    ``label-playlist-unreadable`` means one thing wherever a playlist could not
    be read. A playlist only: the hearts are :func:`list_favorites`.
    """
    from cratekit.label import cli as label_cli  # noqa: PLC0415 - labels is toggleable

    return frozen_rows(_read_rows(label_cli.playlist_tracks_or_refuse(found, reference), reference))


def list_playlist_declared(
    found: catalogue.Catalogue, reference: str
) -> tuple[dict[str, dict[str, Any]], catalogue.ListingShortfall | None]:
    """:func:`list_playlist`, and the shortfall when it listed short (R-515)."""
    from cratekit.label import cli as label_cli  # noqa: PLC0415 - labels is toggleable

    rows, short = label_cli.playlist_listing_or_refuse(found, reference)
    return frozen_rows(_read_rows(rows, reference)), short


@dataclass(frozen=True, slots=True)
class Unreadable:
    """One track of a listing the reader would not read, named by its id (U213)."""

    ref: str
    artist: str
    #: The title as the row spells it, unsplit, which may be empty.
    title: str
    isrc: str
    #: What the reader found wanting, in the words a gate screen shows.
    why: str

    def said(self) -> dict[str, str]:
        """The track in the keys a frozen row names it by, for naming it beside them."""
        return {"artist": self.artist, "title": self.title, "isrc": self.isrc}


@dataclass(frozen=True, slots=True)
class Readable:
    """One playlist read row by row, the tracks the reader refused set aside (U213).

    ``tracks`` is what :func:`list_playlist_declared` freezes less the refused
    rows; ``unread`` each refused track by id; ``order`` every id the listing
    holds, once at its first position, refused ones included.
    """

    tracks: dict[str, dict[str, Any]]
    short: catalogue.ListingShortfall | None
    unread: dict[str, Unreadable]
    order: tuple[str, ...]
    #: R-1264. When the account says each read track was added, by id.
    dates: dict[str, str] = field(default_factory=dict)
    #: U226. How the window read stood beside the unpaged read, one of
    #: ``listing``'s ``WINDOW_`` answers; ``WINDOW_AGREES`` when not asked.
    window: str = listing.WINDOW_AGREES


def _absent(title: str) -> str:
    """The half a refused row names nothing for, read as the reader reads it."""
    return "artist" if match.split_title(title)[0] else "title"


def set_aside(row: object) -> Unreadable:
    """One provider row the reader refused, named by its id as the account lists it (U213).

    The reader's own rule for which half it names, so every caller that sets a
    row aside says the same word. The id is empty for a row that carries none.
    """
    ref, artist, title = match.listed_names(row)
    code = match.row_isrc(row)
    return Unreadable(
        ref=ref,
        artist=artist,
        title=title,
        isrc=str(code).strip() if code else "",
        why=f"the account lists it with no {_absent(title)}",
    )


def list_playlist_readable(
    found: catalogue.Catalogue, reference: str, *, current: bool = False
) -> Readable:
    """:func:`list_playlist_declared`, with a row the reader refuses set aside, not fatal (U213).

    For a caller that plans many playlists in one run, where one track listed
    with no title must not stop every other playlist. A single playlist verb
    keeps :func:`list_playlist_declared`, whose refusal is the answer there.
    ``current`` also reads the client's unpaged read beside the window (U226)
    for a caller that plans a write from the order it reads.

    The listing as a whole still refuses where the declared reader does,
    since a track with no id cannot be named, set aside or asked about.
    """
    from cratekit.label import cli as label_cli  # noqa: PLC0415 - labels is toggleable

    window = listing.WINDOW_AGREES
    if current:
        rows, short, window = label_cli.playlist_listing_judged(found, reference)
    else:
        rows, short = label_cli.playlist_listing_or_refuse(found, reference)
    read: list[Wanted] = []
    refused: dict[str, Unreadable] = {}
    order: dict[str, None] = {}
    nameless: list[int] = []
    for position, row in enumerate(rows, start=1):
        ref = match.listed_names(row)[0]
        if not ref:
            nameless.append(position)
            continue
        order.setdefault(ref, None)
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
        except match.UnreadableList:
            if ref not in refused:
                refused[ref] = set_aside(row)
    _refuse_unidentified(nameless)
    tracks = frozen_rows(tuple(read))
    unread = {ref: one for ref, one in refused.items() if ref not in tracks}
    return Readable(
        tracks=tracks,
        short=short,
        unread=unread,
        order=tuple(order),
        dates=_added_dates(rows, tracks),
        window=window,
    )


def _row_id(row: object) -> str:
    return str(row.get("id", "") if isinstance(row, Mapping) else getattr(row, "id", ""))


def _added_dates(rows: Sequence[object], frozen: Mapping[str, Any]) -> dict[str, str]:
    """When the account says each frozen track was added, by id (U202).

    Off the listing's own rows, so no request is added; the first mention's
    for a track listed twice, and a track dated nowhere is missing, never guessed.
    """
    dates: dict[str, str] = {}
    for row in rows:
        key = _row_id(row)
        if key in frozen and key not in dates:
            moment = hearted_on(row)
            if moment:
                dates[key] = moment
    return dates


def list_favorites(
    found: catalogue.Catalogue,
) -> tuple[dict[str, dict[str, Any]], catalogue.HeartsShortfall | None]:
    """The account's hearts, frozen as a playlist job queues them, and any shortfall.

    Read, frozen and resolved exactly as a playlist's rows are, so owned,
    offered and missing mean the same. The shortfall rides beside the rows
    (R-504) because the provider counts hearts it will not serve, and the job
    alone would resolve a short listing as if it were the account.
    """
    from cratekit.label import cli as label_cli  # noqa: PLC0415 - labels is toggleable

    rows, short = label_cli.favourite_tracks_or_refuse(found, FAVORITES)
    frozen = frozen_rows(_read_rows(rows, FAVORITES))
    # The date rides on EVERY row by its key (U120), None when the account
    # dates it nowhere, so a row with no key is one an older build froze.
    for row in rows:
        key = _row_id(row)
        if key in frozen and HEARTED not in frozen[key]:
            frozen[key][HEARTED] = hearted_on(row)
    return frozen, short


def hearted_on(row: object) -> str | None:
    """When the account says ``row`` was hearted, as ISO 8601 UTC text, or None.

    The client copies the favourite's timestamp onto the track as
    ``user_date_added`` and, in older versions, ``date_added``; anything that
    is not a moment is no date.
    """
    from cratekit.favorites import placeholders  # noqa: PLC0415 - favorites is toggleable

    for name in ("user_date_added", "date_added"):
        value = row.get(name) if isinstance(row, Mapping) else getattr(row, name, None)
        moment = placeholders.parse_hearted(value)
        if moment is not None:
            return moment.isoformat()
    return None
