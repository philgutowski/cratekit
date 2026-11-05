"""The streaming provider's account, behind the outbound package's seam.

**ONE CLASS OVER U62'S SESSION.** Every question here goes to the provider client
that ``acquire.provider_session.client_session`` logged in, and every PAGED read
goes through ``acquire.listing``, for the reason ``label.tidal_catalogue`` gives:
a listing that quietly returns one page looks exactly like a short one. A guard
in the suite scans this file for a direct paging call and for a vendored import.

**ONE REMOVAL, BECAUSE THE PROTOCOL DECLARES ONE (R-836).** ``remove_tracks``
takes tracks off a playlist the outbound ledger records as one the product
created, and refuses any other before a provider call. It is the one place this
class names a removal on the client, and the suite's scan of this file admits
that one call inside that one member and nothing else. The outbound gates and the
confirm digest sit in front of every write; this module adds no gate and removes
none. ``remove_playlist`` (U123) is the same rule for a whole playlist. The
account root's removals (U143), ``remove_root_playlist`` and
``remove_legacy_folder``, are the members that remove something the product did
not create, each narrowed to a kind the provider's own answer must confirm
before anything is sent. ``rename_playlist`` writes to something the product did
not create too, and it is not a removal: it retitles, changes no membership and
deletes nothing.

**THE WORKERS RELY ON THREE RULES THAT ARE NOT VISIBLE IN THEIR CODE.**

* A match is exact or it is ``None``. ``export.plan`` reports a ``None`` as an
  unmatched row and ``hearts.heart_back`` as an unmatched favourite, so a guess
  returned here is a heart on somebody else's recording with nothing reported.
  A ``None`` that had candidates says so through ``unmatched_reason``, because
  "the provider has never heard of this" and "the provider has three of these
  and nothing here could choose" are different things to do something about.
* ``has_heart`` answers from ONE paged read of the favourites per adapter, and
  the seam hands a run one adapter. The rejected alternative asked the provider
  per candidate, and a sweep of a thousand hearts would have made a thousand
  listing calls where one paged read answers all of them.
* ``add_heart`` and ``add_to_playlist`` check before they write, so a resumed
  item that already reached the provider makes no second write.

**A PROVIDER FAILURE IS THE ITEM'S CAUSE, NOT A DEAD SESSION.** Every provider
call is translated by ``account.provider_failure``, which asks the not found
question FIRST, on the ordering ``acquire.vendored.raise_if_session_dead``
argues, and raises at item scope. The job engine then fails that one item and
claims the next, rather than converting a foreign exception into an internal
error.

**CATALOGUE LOOKUPS GO UNDER THE APP WHEN IT IS SET UP (U205).** The ISRC
lookup and the exact track read in ``match_track`` ask ``catalogue`` when the
opener built one, the client ``acquire.provider_session.catalogue_client``
holds under Cratekit's own app credentials, and the account session only when
it did not. Every write, and every read of the account's own things (its
hearts, playlists and folders), goes to the account session and to nothing
else, so the app client is never handed a write: it has none.

**ONE RETRY ON A WRITE, NO MORE**, through ``listing.fetch_with_retry``. A rate
limit on a write is real, and a ladder of five would hold a sweep for a minute
per item against a provider that is refusing it. Creating a playlist is not
retried at all: a create that reached the provider and then timed out would be
retried into a second playlist, and nothing records the first.

Layer: modules.
"""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from typing import Any
from urllib.parse import urlsplit

# Imported at module top rather than deferred, because ``account.bound`` asks
# whether THIS module imports, and the answer has to include the client library.
import tidalapi  # noqa: F401

from cratekit.acquire import catalogue_api, listing, match, provider_session
from cratekit.acquire.adapter import TrackOutcome, classify_unavailable
from cratekit.core import provider_gate
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import account, kinds, ledger, pairs
from cratekit.modules.outbound.service import (
    AGREEING_RELEASES,
    UNREADABLE_CANDIDATE,
    PlaylistListing,
)

#: How many times a write or a single lookup is retried after its first attempt.
WRITE_RETRIES = 1

#: How many tracks one add to a playlist carries (R-835). The client's own add
#: asks the provider for a limit of a hundred per request, so a chunk of that
#: size is what one request is known to take.
ADD_CHUNK = 100

#: How many positions one removal request names (R-836). The client's own
#: clear takes fifty a request, so a request of that size is one it makes.
REMOVE_CHUNK = 50

#: Hosts a provider track URL is read from, the same three the catalogue reads a
#: playlist URL from.
TRACK_HOSTS = frozenset({"tidal.com", "www.tidal.com", "listen.tidal.com"})

#: A provider track identifier as it appears in a track URL's last segment.
_TRACK_ID = re.compile(r"[0-9]+")

#: Client exception names that are a fact about the thing asked for rather than
#: about the session or the network. ``InvalidISRC`` is what the client raises for
#: an ISRC the provider will not accept, which is no match rather than an outage.
NOT_FOUND_NAMES = frozenset({"ObjectNotFound", "InvalidISRC"})


class _Absent:
    """The answer a lookup gives for an explicit not found, kept off the retry."""


_ABSENT = _Absent()


def _not_found(exc: BaseException) -> bool:
    """Whether a failure is the provider saying it has nothing, asked FIRST."""
    if type(exc).__name__ in NOT_FOUND_NAMES:
        return True
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT


def track_reference(identity: str) -> str | None:
    """The provider track identifier an identity names EXACTLY, or ``None``.

    ONE SHAPE: a track URL on a provider host whose path ends ``track/<digits>``.
    A bare number is refused on purpose. The identity the outbound workers hand
    this seam today is a rekordbox ``TrackID``, which is also a bare number, and
    reading it as a provider identifier would heart whatever unrelated recording
    happens to carry that number.
    """
    parts = urlsplit(str(identity or "").strip())
    if parts.scheme not in {"http", "https"}:
        return None
    if (parts.hostname or "").lower() not in TRACK_HOSTS:
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) >= 2 and segments[-2] == "track" and _TRACK_ID.fullmatch(segments[-1]):
        return segments[-1]
    return None


def _row_of(title: str, artist: str) -> match.Wanted | None:
    """The library row in the shape the product's matcher reads, or ``None``.

    READ BY ``match.read_row`` AND BY NOTHING WRITTEN HERE, so a version in
    brackets, a version after a dash, a featured credit and a title that reads
    two ways all mean to this adapter what they mean to intake. ``None`` for a
    row naming no artist or no title: half a name is not unique to a recording,
    which is that reader's own refusal, and a row with nothing to compare
    chooses nothing.
    """
    try:
        return match.read_row(
            {"title": str(title or ""), "artist": str(artist or "")},
            origin=match.TEXT,
            position=1,
        )
    except match.UnreadableList:
        return None


def _count(value: Any) -> bool:
    """Whether a declared count is a whole number and not a flag."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _added_at(track: Any) -> str:
    """When a playlist item was added, as ISO 8601 UTC text, or ``""`` when unknown (U201)."""
    from datetime import datetime, timezone

    for name in ("user_date_added", "date_added"):
        value = getattr(track, name, None)
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).isoformat()
    return ""


def _shown_artist(track: Any) -> str:
    """The artists a provider track bills, as a person reads them on a gate."""
    names = _artist_names(track)
    if names:
        return ", ".join(names)
    lead = getattr(track, "artist", None)
    return str(getattr(lead, "name", "") or "")


def _artist_names(track: Any) -> list[str]:
    """Every artist a provider track bills, in its order."""
    names = []
    for entry in getattr(track, "artists", None) or ():
        name = entry if isinstance(entry, str) else getattr(entry, "name", "")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return names


def _billed(track: Any) -> str:
    """Every artist a provider track bills, in its order, as one string.

    A library row spells a record by two artists as one artist field holding
    both, and the matcher's reader keeps only the first a provider row names.
    """
    return " ".join(_artist_names(track))


#: Words a library row puts BETWEEN artists that no artist is billed under. A
#: comma and an ampersand need no entry, since ``match.fold`` takes them off.
_JOINERS = frozenset({"feat", "ft", "featuring", "with", "and", "vs", "x"})


def _artist_agrees(row_artist: str, first_billed: str, track: Any) -> bool:
    """Whether the row's artist field names this track's artists and no others.

    COMPARED AS WORDS AND NEVER SPLIT INTO NAMES, because a comma is legal inside
    an artist's own name and guessing where one artist ends is the wrong join
    ``match._first_named`` refuses to make. Two conditions, each removable alone.
    Every word of the FIRST billed artist is in the row, so a row naming only the
    guest does not agree. And the row holds no word the track does not bill,
    joiners aside, so another act sharing a word does not agree either. Between
    them a row may bill the artists in another order, may leave out a remixer the
    provider bills, and may spell the join as a comma, an ampersand or "feat.".
    """
    ours = set(match.fold(row_artist).split())
    first = set(match.fold(first_billed).split())
    billed = first | set(match.fold(_billed(track)).split())
    return bool(first) and first <= ours and ours - billed <= _JOINERS


def _agrees(row: match.Wanted, track: Any) -> bool | None:
    """Whether a provider track is the row's recording AND version.

    ``None`` when the track cannot be read at all, which is not a disagreement:
    see :meth:`TidalAccount._among`.

    EITHER READING OF EITHER TITLE COUNTS, since "Sun Path - Live" is a version
    or the end of a title and the string cannot say which, whichever side spelled
    it that way. ``intake.candidates.sole_exact`` refuses a row that reads two
    ways outright, and this does not, ON PURPOSE: there the candidates came from
    a text search and anything may be among them, and here every candidate
    already carries the row's own ISRC and the caller still needs exactly one of
    them to agree. That module's reader is not reused because it scores every row
    with a fuzzy matcher this path has no use for.
    """
    try:
        listed = match.read_row(track, origin=match.TIDAL, position=1)
    except match.UnreadableList:
        return None
    if not _artist_agrees(row.artist, listed.artist, track):
        return False
    ours = {(match.fold(one.title), one.version_key) for one in row.readings}
    theirs = {(match.fold(one.title), one.version_key) for one in listed.readings}
    return bool(ours & theirs)


def _album_name(track: Any) -> str:
    """The name of the release a provider track sits on, or ``""`` unread."""
    return str(getattr(getattr(track, "album", None), "name", "") or "")


def _lowest(remotes: list[str]) -> str:
    """The lowest provider identifier, numbers by value, the one a tie takes (R-1032).

    Not a fact about the row and not offered as one: it is the same answer on
    every run and every machine whatever order the provider lists them in, so
    a refresh never swaps one release for another.
    """
    return min(remotes, key=lambda remote: (len(remote), remote))


def _on_album(remotes: list[str], tracks: dict[str, Any], album: str) -> list[str]:
    """The releases among ``remotes`` on the file's album, or all of them if none is."""
    wanted = match.fold(album)
    named = [
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
    ]
    return named or remotes


def _streamable(track: Any) -> bool:
    """Whether the provider will play this track, absent a statement that it will not.

    THE CLIENT READS A TRACK'S VERSION ONLY WHEN IT IS AVAILABLE, so an extended
    mix the provider has withdrawn arrives with no version at all and reads as
    the plain record. It is left out of the choice rather than compared, for that
    reason and because a heart on a track nobody can play is not the favourite.
    """
    return getattr(track, "available", True) is not False


class TidalAccount:
    """The fifteen ``RemoteAccount`` members, over one logged in client.

    Eight add only, two that read folders, one that puts a playlist in a
    folder, one that retitles a playlist the account owns, one that says why
    the last match of a row came back empty, one that names a playlist's
    tracks, and the one removal, from a playlist the product made. Since U143
    also the account root's two removals, each of a kind a gate named.
    """

    def __init__(
        self,
        session: Any,
        *,
        sleep: Callable[[float], None] | None = None,
        cfg: Any = None,
        catalogue: Any = None,
    ) -> None:
        self._session = session
        #: Where catalogue lookups go: the app client when the opener built
        #: one (U205), else the account session, exactly as before.
        self._lookups = catalogue if catalogue is not None else session
        #: The configuration whose outbound ledger says which playlists the
        #: product made (R-836). None refuses every removal, since a ledger
        #: that cannot be named cannot say yes.
        self._cfg = cfg
        # Looked up at construction rather than bound as a default, so a caller
        # that replaced ``time.sleep`` is honoured.
        self._sleep = sleep or time.sleep
        self._hearts: set[str] | None = None
        self._members: dict[str, list[str]] = {}
        self._reasons: dict[str, str] = {}

    def _call(self, doing: str, fn: Callable[[], Any], *, retries: int = WRITE_RETRIES) -> Any:
        """One provider call, retried ``retries`` times, translated on failure.

        An explicit not found is returned as ``_ABSENT`` from inside the retried
        callable, so a lookup the provider has answered is never asked again.
        """

        def attempt(limit: int, offset: int) -> Any:
            del limit, offset
            try:
                return fn()
            except Exception as exc:
                if _not_found(exc):
                    return _ABSENT
                raise

        try:
            return listing.fetch_with_retry(
                attempt, limit=0, offset=0, max_retries=retries, sleep=self._sleep
            )
        except catalogue_api.AppCredentialsRejected as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S. Read by the account's
            # translation it would be a wait, and the held account would not be
            # the thing to forget.
            raise catalogue_api.rejected(exc, doing) from exc
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise account.provider_failure(exc, doing) from exc

    def _read(self, doing: str, fn: Callable[[], list[Any]]) -> list[Any]:
        """One paged read through ``listing``, translated on failure."""
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - translated, never swallowed
            raise account.provider_failure(exc, doing) from exc

    # ── matching ────────────────────────────────────────────────────────────

    def match_track(
        self,
        *,
        identity: str,
        isrc: str = "",
        title: str = "",
        artist: str = "",
        agree: bool = False,
        album: str = "",
        any_agreeing: bool = False,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.

        ISRC FIRST. One ISRC can name several provider tracks, the single, the
        album cut and every compilation that carries the recording, and which
        release gets the heart is not something the ISRC decides. So several
        distinct identifiers go to :meth:`_among`, which chooses by what the ROW
        says and by what the account already hearts, never by position, and
        otherwise answers ``None`` and leaves the count in
        :meth:`unmatched_reason`. Measured live on 2026-09-17, returning ``None``
        for every such answer left half of a small playlist unmatched (R-356).

        WITH ``agree`` ONE TRACK IS CHOSEN AS SEVERAL ARE, through
        :meth:`_among`, so a code read off a library file's tag lists a track
        only when that track is the row's recording and version (R-879).

        ``album`` is the album tag of the row's own file, read beside its ISRC,
        and only :meth:`_among` reads it (R-572).

        ``any_agreeing`` lets :meth:`_among` take one of a tie between agreeing
        releases rather than refuse it, for the mirror's listening copy only
        (R-1032).

        IDENTITY SECOND, and only an exact provider track reference, see
        :func:`track_reference`. Never a text search over title and artist:
        ``title`` and ``artist`` choose among tracks the ISRC already named and
        are never sent to the provider.

        BOTH READS ARE CATALOGUE QUESTIONS and go to the app client when one is
        open (U205). The favourites :meth:`_among` asks are the account's own
        and stay on the account session.
        """
        key = str(identity)
        self._reasons.pop(key, None)
        wanted = str(isrc or "").strip()
        if wanted:
            found = self._call(
                f"look up the ISRC {wanted}",
                lambda: self._lookups.get_tracks_by_isrc(wanted),
            )
            if found is not _ABSENT:
                tracks = {
                    str(getattr(track, "id", "") or ""): track for track in found or ()
                }
                tracks.pop("", None)
                if len(tracks) == 1 and not agree:
                    return next(iter(tracks))
                if tracks:
                    chosen, reason = self._among(
                        tracks,
                        isrc=wanted,
                        title=title,
                        artist=artist,
                        album=album,
                        any_agreeing=any_agreeing,
                    )
                    if chosen is None:
                        self._reasons[key] = reason
                    return chosen
        reference = track_reference(identity)
        if reference is None:
            return None
        track = self._call(
            f"look up the track {reference}", lambda: self._lookups.track(reference)
        )
        if track is _ABSENT or track is None:
            return None
        resolved = str(getattr(track, "id", "") or "")
        return resolved if resolved == reference else None

    def _among(
        self,
        tracks: dict[str, Any],
        *,
        isrc: str,
        title: str,
        artist: str,
        album: str = "",
        any_agreeing: bool = False,
    ) -> tuple[str | None, str]:
        """One of several tracks sharing an ISRC, or ``None`` and why not.

        THREE RULES, IN ORDER, AND NONE IS A GUESS.

        1. The tracks that agree with the row's artist, title and version under
           the product's own fold, see :func:`_agrees`. Exactly one is the match.
           This is what separates a radio edit from an extended mix filed under
           one code, and what refuses a code the provider filed on the wrong
           record.
        2. When several agree, which is the ordinary case since a single and its
           album cut are spelled alike, the one the account ALREADY HEARTS. The
           person chose that release once and nothing here chooses it for them.
           It is asked of the agreeing tracks only, so a heart on a track the
           row does not name decides nothing.
        3. When the account hearts none of them, the one whose album name is
           the album tag of the row's own file (R-572). The file says which
           release it was cut from, which is a fact about the row. A file with
           no album tag, or one naming none or several of them, chooses nothing.
           An unreadable track among the candidates stops this rule too: the
           album is asked of the agreeing tracks only, and a lone agreeing
           track the first rule already refused must not come back through the
           album (R-572).

        A TRACK THAT CANNOT BE READ STOPS THE FIRST RULE FROM CHOOSING, on
        ``intake.candidates.sole_exact``'s argument: one agreeing track beside
        one unreadable one is not known to be the only one that agrees. It
        stops the album rule the same way. A track the provider will not play
        is never a candidate, see :func:`_streamable`.

        RELEASES SPELLED ALIKE WITH NONE HEARTED AND NO ALBUM TO TELL THEM
        APART STAY UNMATCHED. The first, the earliest or the lowest numbered is
        a policy about the catalogue rather than a fact about the row, and
        R-572 refused each of them.

        UNLESS ``any_agreeing`` SAYS ANY OF THEM WILL DO (R-1032), which the
        mirror says because its playlist is a listening copy and writes nothing
        back as the row's identity. Then a tie with no unreadable candidate is
        broken by :func:`_lowest` over the hearted releases if the account
        hearts several, else over every agreeing one, narrowed first to those
        the file's album names when it names any. Only the tie is broken: the
        refusals before it, no agreeing release, no row to judge agreement by,
        a candidate that could not be read, are unchanged.
        """
        named = f"the ISRC {isrc} names {len(tracks)} provider tracks"
        row = _row_of(title, artist)
        if row is None:
            return None, (
                f"{named} and this row carries no artist and title to choose "
                f"among them by"
            )
        verdicts = {
            remote: _agrees(row, track)
            for remote, track in tracks.items()
            if _streamable(track)
        }
        withdrawn = len(tracks) - len(verdicts)
        unreadable = sum(1 for verdict in verdicts.values() if verdict is None)
        agreeing = [remote for remote, verdict in verdicts.items() if verdict]
        if len(agreeing) == 1 and not unreadable:
            return agreeing[0], ""
        aside = (
            (f", {withdrawn} cannot be streamed" if withdrawn else "")
            + (f", {unreadable} {UNREADABLE_CANDIDATE}" if unreadable else "")
        )
        if not agreeing:
            rest = "the rest" if aside else "them"
            return None, (
                f"{named}{aside} and none of {rest} agrees with this row's "
                f"artist, title and version"
            )
        hearts = self._favorites()
        hearted = [remote for remote in agreeing if remote in hearts]
        if len(hearted) == 1:
            return hearted[0], ""
        if any_agreeing and not unreadable:
            return _lowest(_on_album(hearted or agreeing, tracks, album)), ""
        said = (
            f"{named}{aside}, {len(agreeing)} {AGREEING_RELEASES} and the "
            f"account hearts {len(hearted)} of those"
        )
        if hearted:
            return None, f"{said}, so none was chosen"
        if unreadable:
            return None, f"{said}, so none was chosen"
        wanted = match.fold(album)
        if not wanted:
            return None, f"{said}, and the file carries no album tag, so none was chosen"
        named_album = [
            remote for remote in agreeing if match.fold(_album_name(tracks[remote])) == wanted
        ]
        if len(named_album) == 1:
            return named_album[0], ""
        return None, (
            f"{said}, and the file's album {album!r} names {len(named_album)} "
            f"of them, so none was chosen"
        )

    def unmatched_reason(self, identity: str) -> str:
        """Why the last match of this row came back ``None``, or ``""``.

        Empty for a row the provider simply does not have, which the workers
        already report as unmatched, and for a row that matched.
        """
        return self._reasons.get(str(identity), "")

    # ── hearts ──────────────────────────────────────────────────────────────

    def _favorites(self) -> set[str]:
        if self._hearts is None:
            tracks = self._read(
                "read the account's favourite tracks",
                lambda: listing.favorite_tracks(self._session),
            )
            self._hearts = {str(getattr(track, "id", "") or "") for track in tracks}
            self._hearts.discard("")
        return self._hearts

    def has_heart(self, remote_id: str) -> bool:
        return str(remote_id) in self._favorites()

    def add_heart(self, remote_id: str) -> None:
        identifier = str(remote_id)
        hearts = self._favorites()
        if identifier in hearts:
            return
        doing = f"heart the track {identifier}"
        accepted = self._call(
            doing, lambda: self._session.user.favorites.add_track(identifier)
        )
        # The client answers a refused heart with ``False`` rather than a raise,
        # and recording that as hearted would put a heart in the ledger that the
        # account does not hold.
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the heart"), doing
            )
        hearts.add(identifier)

    # ── playlists ───────────────────────────────────────────────────────────

    def _playlist(self, playlist_id: str) -> Any:
        found = self._call(
            f"open the playlist {playlist_id}",
            lambda: self._session.playlist(playlist_id),
        )
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"),
                f"open the playlist {playlist_id}",
            )
        return found

    def _listed(self, playlist_id: str, playlist: Any) -> list[Any]:
        """Every track object on the playlist, in order, read now across pages."""
        return self._read(
            f"read the playlist {playlist_id}",
            lambda: listing.playlist_tracks(playlist),
        )

    def _membership(self, playlist_id: str) -> list[str]:
        if playlist_id not in self._members:
            tracks = self._listed(playlist_id, self._playlist(playlist_id))
            self._members[playlist_id] = [
                str(getattr(track, "id", "") or "") for track in tracks
            ]
        return self._members[playlist_id]

    def create_playlist(self, name: str) -> str:
        """Create one playlist on the account, private, and return its identifier.

        PRIVATE BECAUSE THE SOURCE SYSTEM MAKES EVERY PLAYLIST IT CREATES
        PRIVATE (R-834). The client takes no visibility on the create itself, so
        it is set on the object the create returned, through the client's own
        ``set_playlist_private``. A playlist this account did not create is never
        asked: the ledger's check before write means a resumed item that finds
        its playlist recorded never reaches this member at all.

        THE IDENTIFIER IS RETURNED EVEN WHEN THE PRIVATE STEP IS REFUSED, see
        :meth:`_make_private`.
        """
        created = self._call(
            f"create the playlist {name!r}",
            lambda: self._session.user.create_playlist(name, ""),
            retries=0,
        )
        identifier = str(getattr(created, "id", "") or "") if created is not _ABSENT else ""
        if not identifier:
            raise account.provider_failure(
                LookupError("the provider assigned the new playlist no identifier"),
                f"create the playlist {name!r}",
            )
        self._make_private(created, identifier)
        self._members[identifier] = []
        return identifier

    def _make_private(self, created: Any, identifier: str) -> None:
        """Set a playlist this account just created private.

        RETRIED LIKE A WRITE, NOT LIKE A CREATE, on ``rename_playlist``'s
        argument: the call names the playlist it changes and asks for one fixed
        state, so a retry asks for what the first attempt asked for.

        A REFUSAL IS NOT RAISED, AND THAT IS THE WHOLE POINT OF ITS SHAPE. The
        playlist already exists by the time this runs. Raising would keep its
        identifier out of the ledger, and the next item of the same export would
        read no record and create another, one public playlist per track: the
        orphan shape ``ledger.reserve_playlist`` was rebuilt to end, driven on
        2026-09-02 as three playlists from one three track export. So the one
        playlist is recorded and the refusal costs its visibility instead, which
        is R-849.

        THAT INCLUDES A PARK FROM THE PROVIDER GATE, deliberately. A park raised
        here would leave the same unrecorded playlist, and swallowing it does
        not let the run go on: a cooldown is written to the shared gate file,
        so the next gated call refuses at once, and a held lock is waited on
        again by the next call.

        IT RUNS INSIDE THE LEDGER'S LOCK, since the reserve resolves the create
        under it, so the window in which a kill leaves an unrecorded playlist is
        now the create plus this step rather than the create alone. R-849
        records that too.

        A client with no such call fails the step like any refusal and is
        passed over for the same reason; a guard in the suite pins the call on
        the client library, so an upgrade that renames it fails there instead.
        """
        try:
            self._call(
                f"make the playlist {identifier} private",
                lambda: created.set_playlist_private(),
            )
        except CratekitError:
            return

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        identifier = str(remote_id)
        members = self._membership(playlist_id)
        if identifier in members:
            return
        playlist = self._playlist(playlist_id)
        doing = f"add the track {identifier} to the playlist {playlist_id}"
        added = self._call(doing, lambda: playlist.add([identifier]))
        if added is _ABSENT:
            raise account.provider_failure(
                LookupError(f"the provider no longer has the playlist {playlist_id!r}"),
                doing,
            )
        # THE CLIENT SKIPS A TRACK IT CANNOT FIND AND RAISES NOTHING, answering
        # with the identifiers it added. An answer that does not name this track
        # is read again from the playlist rather than trusted either way: the
        # track may have been added elsewhere since the membership was read, and
        # recording one the playlist does not hold would make a resume skip it.
        if identifier not in {str(item) for item in added or ()}:
            del self._members[playlist_id]
            if identifier not in self._membership(playlist_id):
                raise account.provider_failure(
                    LookupError(
                        f"the provider added nothing for the track {identifier!r}"
                    ),
                    doing,
                )
            return
        members.append(identifier)

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        return tuple(self._membership(playlist_id))

    def rename_playlist(self, playlist_id: str, name: str) -> None:
        """Retitle the playlist, leaving its membership and description alone.

        RETRIED LIKE A WRITE AND NOT LIKE A CREATE. The reason ``create_playlist``
        takes no retry is that a create which reached the provider and then timed
        out would be retried into a second playlist nothing records. A retitle
        names the playlist it edits and asks for one fixed title, so the retry
        asks for the state the first attempt asked for.

        A PLAYLIST THE SESSION DOES NOT OWN COMES BACK WITHOUT AN EDITOR, since
        the client hands out a read only object for somebody else's playlist.
        That is refused rather than passed over, because a rename reported as
        done over a playlist that still carries its old title is how the source
        system is told a sweep finished that it will offer again.

        AN EMPTY TITLE IS REFUSED HERE AND NOT AT THE PROVIDER. The client's own
        edit reads a falsy title as "keep the current one" and answers True, so
        an empty string would be a write that changed nothing, reported as a
        rename that succeeded. That is the same wrong answer the two refusals
        above exist to prevent, arriving through the one door neither watches.
        """
        # The title is NOT stripped for the write, only for the emptiness test.
        # A caller that asked for a title with a trailing space asked for it.
        wanted = str(name)
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
        if not wanted.strip():
            # NOT ``provider_failure``. The provider did not fail, and its
            # remedy is "resume the job to retry this item", which is advice
            # that cannot work: the same empty title fails the same way.
            raise refuse(
                "internal-error",
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id)},
            )
        playlist = self._playlist(playlist_id)
        retitle = getattr(playlist, "edit", None)
        if not callable(retitle):
            raise account.provider_failure(
                LookupError(
                    f"the provider's playlist {playlist_id!r} cannot be retitled by "
                    f"this account"
                ),
                doing,
            )
        # The client answers a refused edit with ``False`` rather than a raise,
        # on ``add_heart``'s shape, and returning here would report a mark the
        # account does not carry.
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"),
                doing,
            )

    # ── folders (R-835) ─────────────────────────────────────────────────────

    def add_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Add every asked track the playlist lacks, :data:`ADD_CHUNK` per request.

        RETRIED LIKE A WRITE. The client asks the provider to skip a track the
        playlist already holds, so a retried chunk that landed the first time
        adds nothing twice.

        THE ANSWER IS READ, NOT TRUSTED, on :meth:`add_to_playlist`'s argument:
        the client skips a track it cannot find and raises nothing. When an
        answer leaves out a track it was asked for, the playlist is read again
        and the answer is what it holds. A track still absent is left out of
        the return rather than raised, since the provider has said all it will.
        """
        wanted = [str(one) for one in dict.fromkeys(remote_ids) if str(one)]
        members = self._membership(playlist_id)
        held = set(members)
        lacking = [one for one in wanted if one not in held]
        if lacking:
            playlist = self._playlist(playlist_id)
            doing = f"add {len(lacking)} tracks to the playlist {playlist_id}"
            unconfirmed = False
            for start in range(0, len(lacking), ADD_CHUNK):
                chunk = lacking[start : start + ADD_CHUNK]
                added = self._call(doing, lambda chunk=chunk: playlist.add(chunk))
                if added is _ABSENT:
                    raise account.provider_failure(
                        LookupError(
                            f"the provider no longer has the playlist {playlist_id!r}"
                        ),
                        doing,
                    )
                named = {str(item) for item in added or ()}
                members.extend(one for one in chunk if one in named)
                unconfirmed = unconfirmed or any(one not in named for one in chunk)
            if unconfirmed:
                del self._members[playlist_id]
                members = self._membership(playlist_id)
            held = set(members)
        return tuple(one for one in wanted if one in held)

    def _folder(self, folder_id: str) -> Any:
        """The client's folder object for one identifier, WITHOUT its lookup.

        The client's own lookup reads one page of fifty root folders and raises
        not found for any later one, so the object is built empty, which makes
        no request, and given the identifier. Every call made on it after that
        names the folder by that identifier and nothing else.
        """
        handle = self._session.folder()
        handle.id = str(folder_id)
        return handle

    def folders(self) -> dict[str, str]:
        found = self._read(
            "read the account's folders", lambda: listing.account_folders(self._session)
        )
        return {
            str(getattr(folder, "id", "") or ""): str(getattr(folder, "name", "") or "")
            for folder in found
            if str(getattr(folder, "id", "") or "")
        }

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        handle = self._folder(folder_id)
        found = self._read(
            f"read the folder {folder_id}", lambda: listing.folder_playlists(handle)
        )
        return {
            str(getattr(playlist, "id", "") or ""): str(getattr(playlist, "name", "") or "")
            for playlist in found
            if str(getattr(playlist, "id", "") or "")
        }

    def folder_folders(self, folder_id: str) -> dict[str, str]:
        handle = self._folder(folder_id)
        found = self._read(
            f"read the folders in {folder_id}", lambda: listing.folder_folders(handle)
        )
        return {
            str(getattr(folder, "id", "") or ""): str(getattr(folder, "name", "") or "")
            for folder in found
            if str(getattr(folder, "id", "") or "")
        }

    def create_folder(self, name: str) -> str:
        """Create one root folder and return its identifier. NEVER RETRIED.

        A folder needs no visibility step: the source system sets none, and the
        provider keeps an account's folders to the account.
        """
        doing = f"create the folder {name!r}"
        created = self._call(
            doing, lambda: self._session.user.create_folder(name), retries=0
        )
        identifier = str(getattr(created, "id", "") or "") if created is not _ABSENT else ""
        if not identifier:
            raise account.provider_failure(
                LookupError("the provider assigned the new folder no identifier"), doing
            )
        return identifier

    def move_to_folder(self, playlist_id: str, folder_id: str) -> None:
        """Put the playlist in the folder. RETRIED LIKE A WRITE.

        The call names the playlist and the folder and asks for one fixed
        place, so a retry asks for what the first attempt asked for, on
        :meth:`rename_playlist`'s argument. The client answers a refused move
        with ``False`` rather than a raise, and returning here would record a
        playlist in a folder the account does not show it in.
        """
        handle = self._folder(folder_id)
        doing = f"put the playlist {playlist_id} in the folder {folder_id}"
        moved = self._call(
            doing, lambda: handle.move_items_to_folder([str(playlist_id)], str(folder_id))
        )
        if moved is False or moved is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the move into the folder"),
                doing,
            )

    # ── the removals (R-836, U123) ──────────────────────────────────────────

    def track_names(self, playlist_id: str) -> dict[str, tuple[str, str]]:
        """Every track on the playlist, identifier to ``(artist, title)``, read now.

        Read fresh rather than from the membership this adapter remembers,
        since a playlist created or added to in this run is remembered by
        identifier alone.
        """
        tracks = self._listed(playlist_id, self._playlist(playlist_id))
        self._members[playlist_id] = [str(getattr(track, "id", "") or "") for track in tracks]
        return {
            str(getattr(track, "id", "") or ""): (
                _shown_artist(track),
                str(getattr(track, "full_name", "") or getattr(track, "name", "") or ""),
            )
            for track in tracks
            if str(getattr(track, "id", "") or "")
        }

    def playlist_listing(self, playlist_id: str) -> PlaylistListing:
        """Every track on the playlist with its added time and the declared count (U201).

        One read, as :meth:`track_names` reads, and the membership it read is
        remembered the same way. The added time is the client's
        ``user_date_added``, else ``date_added``, which it copies from the
        playlist item's own ``dateAdded``; a time with no zone, or none, is
        left out rather than guessed, since the mirror reads an absent time as
        unknown. The declared count is the playlist's ``num_tracks``.
        """
        playlist = self._playlist(playlist_id)
        tracks = self._listed(playlist_id, playlist)
        ids = [str(getattr(track, "id", "") or "") for track in tracks]
        self._members[playlist_id] = ids
        names: dict[str, tuple[str, str]] = {}
        added: dict[str, str] = {}
        for identifier, track in zip(ids, tracks, strict=True):
            if not identifier or identifier in names:
                continue
            names[identifier] = (
                _shown_artist(track),
                str(getattr(track, "full_name", "") or getattr(track, "name", "") or ""),
            )
            moment = _added_at(track)
            if moment:
                added[identifier] = moment
        declared = getattr(playlist, "num_tracks", None)
        return PlaylistListing(
            names=names,
            added=added,
            listed=len(ids),
            declared=declared if isinstance(declared, int) and not isinstance(declared, bool) else None,
        )

    def _positions(self, playlist_id: str, playlist: Any) -> list[str]:
        """The playlist's tracks by position, refused when a position is unknowable.

        THE PROVIDER LEAVES OUT A TRACK THIS ACCOUNT CANNOT PLAY AND STILL
        COUNTS IT (``listing.playlist_tracks``), so a read shorter than the
        declared total has its positions shifted from the provider's, and a
        removal by position would take off the wrong track. Refused, with
        nothing sent. A playlist declaring no total cannot be checked and is
        refused the same way.

        A VIDEO SHIFTS THEM TOO. The client removes by ITEM position, items
        are tracks and videos together, and the read here is of tracks alone,
        so a playlist declaring any video, or declaring no video count, is
        refused as well.
        """
        tracks = self._listed(playlist_id, playlist)
        declared = getattr(playlist, "num_tracks", None)
        videos = getattr(playlist, "num_videos", None)
        if (
            not _count(declared)
            or declared != len(tracks)
            or not _count(videos)
            or videos != 0
        ):
            raise refuse(
                "outbound-remove-refused",
                f"the playlist {playlist_id} declares {declared!r} track(s) and "
                f"{videos!r} video(s), and {len(tracks)} track(s) could be read, so "
                f"which position holds which track is not known and nothing was "
                f"taken off it",
                steps=(
                    "take the tracks off by hand in the provider's own player, or "
                    "remove the tracks this account cannot play first",
                ),
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id), "problem": "positions-unknown"},
            )
        members = [str(getattr(track, "id", "") or "") for track in tracks]
        self._members[playlist_id] = members
        return members

    def _vouched(self, identifier: str, kept: str) -> None:
        """Refuse, before any provider call, a playlist nothing vouches for changing.

        TWO RECORDS VOUCH, AND ONLY TWO. The outbound ledger, for a playlist
        the product made (R-836), and the playlist pairs, for one of the
        author's own playlists the author marked to stay the same list as a
        rekordbox playlist (U130). Any other playlist, the source system's, a
        label year adopted by its name, or the author's own unpaired, is
        refused with nothing sent. ``kept`` says what was not done.
        """
        if self._cfg is not None and (
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
        ):
            return
        raise refuse(
            "outbound-remove-refused",
            f"the outbound ledger does not record the playlist {identifier} as "
            f"one this product created and no playlist pair names it, so "
            f"{kept} and the provider was not asked",
            steps=("change the playlist by hand in the provider's own player",),
            scope=Scope.SOURCE,
            origin=("outbound", "account"),
            detail={"playlist_id": identifier, "problem": "not-product-made"},
        )

    def order_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Put the playlist's tracks in this order, one move at a time. NEVER RETRIED.

        THE SAME TWO RECORDS ARE ASKED FIRST as :meth:`remove_tracks` asks,
        before the playlist is opened.

        EVERY MOVE IS TO THE END, the one position whose meaning does not
        depend on how the provider counts a move's target. The longest run at
        the head of ``remote_ids`` already standing in that order stays where
        it is, and every track after it is moved to the end in turn, which
        leaves the playlist in exactly the asked order.

        BY POSITION, through :meth:`_positions`, which refuses a playlist whose
        positions cannot be trusted, and READ BACK after every move, which must
        be what it held with that one track moved to the end. Any other answer
        is refused, ``outbound-remove-refused``, and nothing more is sent: a
        move by position that landed elsewhere would make every later one
        wrong. A move changes no membership, so a refusal part way leaves every
        track on the playlist.

        A track the playlist does not hold, or holds twice, is not moved. The
        return is the playlist's order once the moves are done.
        """
        identifier = str(playlist_id)
        self._vouched(identifier, "no track was moved")
        playlist = self._playlist(identifier)
        before = self._positions(identifier, playlist)
        counts: dict[str, int] = {}
        for one in before:
            counts[one] = counts.get(one, 0) + 1
        wanted = [
            str(one)
            for one in dict.fromkeys(remote_ids)
            if str(one) and counts.get(str(one)) == 1
        ]
        asked = set(wanted)
        standing = [one for one in before if one in asked]
        keep = 0
        for one in standing:
            if keep < len(wanted) and one == wanted[keep]:
                keep += 1
        doing = f"put the playlist {identifier} in order"
        for one in wanted[keep:]:
            at = before.index(one)
            accepted = self._call(
                doing,
                lambda at=at, playlist=playlist: playlist.move_by_indices([at], len(before)),
                retries=0,
            )
            if accepted is False or accepted is _ABSENT:
                raise account.provider_failure(
                    RuntimeError("the provider did not accept the move"), doing
                )
            expected = [*before[:at], *before[at + 1 :], one]
            playlist = self._playlist(identifier)
            before = self._positions(identifier, playlist)
            if before != expected:
                raise refuse(
                    "outbound-remove-refused",
                    f"the playlist {identifier} read back after a move is not what it "
                    f"held with that track moved to the end, so nothing more was "
                    f"moved; every track is still on it",
                    steps=("check the playlist's order by hand in the provider's own player",),
                    scope=Scope.RUN,
                    origin=("outbound", "account"),
                    detail={"playlist_id": identifier, "problem": "read-back-differs"},
                )
        return tuple(before)

    def remove_tracks(self, playlist_id: str, remote_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Take tracks off one playlist the product made or the author paired. NEVER RETRIED.

        THE LEDGER AND THE PAIRS ARE ASKED FIRST, before the playlist is even
        opened: a playlist neither ``ledger.product_made`` nor
        ``pairs.paired`` vouches for is refused with no provider call at all.

        BY POSITION, BECAUSE THE CLIENT'S REMOVE BY IDENTIFIER READS ONE PAGE.
        Its own lookup of an identifier's position reads the first window of
        the playlist and nothing after it, so the positions are read here
        through ``listing`` instead, and :meth:`_positions` refuses when they
        cannot be trusted. The playlist object is opened fresh for each
        request, so the request carries the version tag the provider issued
        with that read, and the client's own reread after the request is what
        the next one carries.

        NOT RETRIED, on ``create_playlist``'s argument and more so: a removal
        by position that reached the provider and then timed out, sent again,
        would take off whatever moved into those positions.

        READ BACK, NOT TRUSTED. After each request the playlist is read again
        and must equal what it held with exactly those positions gone. Any
        other answer is refused, ``outbound-remove-refused`` and not retryable,
        since a removal that took the wrong track is the one outcome this
        member exists to rule out.
        """
        identifier = str(playlist_id)
        wanted = [str(one) for one in dict.fromkeys(remote_ids) if str(one)]
        self._vouched(identifier, "no track was taken off it")
        asked = set(wanted)
        doing = f"take {len(wanted)} tracks off the playlist {identifier}"
        playlist = self._playlist(identifier) if wanted else None
        before = self._positions(identifier, playlist) if wanted else []
        while playlist is not None:
            at = sorted(i for i, one in enumerate(before) if one in asked)[:REMOVE_CHUNK]
            if not at:
                break
            accepted = self._call(
                doing, lambda at=at, playlist=playlist: playlist.remove_by_indices(at), retries=0
            )
            if accepted is False or accepted is _ABSENT:
                raise account.provider_failure(
                    RuntimeError("the provider did not accept the removal"), doing
                )
            gone = set(at)
            expected = [one for i, one in enumerate(before) if i not in gone]
            # THE READ BACK IS THE NEXT REQUEST'S READ, so a second chunk opens
            # and reads the playlist once rather than twice.
            playlist = self._playlist(identifier)
            before = self._positions(identifier, playlist)
            if before != expected:
                # NOT ``provider_failure``, whose remedy is to run it again: a
                # playlist that did not change as asked may have lost the wrong
                # track, and another removal by position would compound it.
                raise refuse(
                    "outbound-remove-refused",
                    f"the playlist {identifier} read back after a removal is not "
                    f"what it held with the asked positions gone, so a track other "
                    f"than the asked ones may have come off, and nothing more was sent",
                    steps=(
                        "check the playlist by hand in the provider's own player "
                        "before running the prune again",
                    ),
                    scope=Scope.RUN,
                    origin=("outbound", "account"),
                    detail={"playlist_id": identifier, "problem": "read-back-differs"},
                )
        held = set(self._members.get(identifier, ()))
        return tuple(one for one in wanted if one not in held)

    def remove_playlist(self, playlist_id: str) -> None:
        """Remove one playlist the product made (U123). NEVER RETRIED.

        THE LEDGER IS ASKED FIRST, as :meth:`remove_tracks` asks it: a
        playlist ``ledger.product_made`` does not vouch for is refused with no
        provider call at all.

        A PLAYLIST THE PROVIDER NO LONGER HAS IS ALREADY REMOVED, so a resume
        that asks again after a removal landed and its answer was lost ends
        here and removes nothing.

        NOT RETRIED, on ``create_playlist``'s argument: the outcome of a
        request that timed out is read back below rather than sent again.

        READ BACK, NOT TRUSTED. The playlist is opened again after the
        request and must be gone; one the provider still serves is refused,
        ``outbound-remove-refused``, so a removal that did not happen is never
        reported as one that did.
        """
        identifier = str(playlist_id)
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise refuse(
                "outbound-remove-refused",
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
                f"was not asked",
                steps=("remove the playlist by hand in the provider's own player",),
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": identifier, "problem": "not-product-made"},
            )
        doing = f"remove the playlist {identifier}"
        found = self._call(doing, lambda: self._session.playlist(identifier))
        if found is _ABSENT or found is None:
            self._members.pop(identifier, None)
            return
        # THE CLIENT HANDS BACK A PLAYLIST IT OWNS WITH A DELETE AND ANY OTHER
        # WITHOUT ONE, so a playlist it does not read as this account's is
        # refused here in words rather than failing on a missing attribute.
        # Read as an attribute, so the suite's removal scan still sees it.
        try:
            remove = found.delete
        except AttributeError:
            remove = None
        if not callable(remove):
            raise refuse(
                "outbound-remove-refused",
                f"the provider does not serve the playlist {identifier} as one this "
                f"account owns, so it was not removed",
                steps=("remove the playlist by hand in the provider's own player",),
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": identifier, "problem": "not-owned"},
            )
        accepted = self._call(doing, remove, retries=0)
        if accepted is False:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the removal"), doing
            )
        again = self._call(doing, lambda: self._session.playlist(identifier))
        if again is not _ABSENT and again is not None:
            raise refuse(
                "outbound-remove-refused",
                f"the playlist {identifier} is still served by the provider after "
                f"it was asked to remove it, so it was not removed",
                steps=("check the playlist by hand in the provider's own player",),
                scope=Scope.RUN,
                origin=("outbound", "account"),
                detail={"playlist_id": identifier, "problem": "read-back-differs"},
            )
        self._members.pop(identifier, None)

    # ── the account root's removals (U143) ──────────────────────────────────

    def _root_refusal(self, what: str, said: str, problem: str, **detail: str) -> CratekitError:
        """A root removal refused with nothing sent, in words and by problem."""
        return refuse(
            "outbound-remove-refused",
            f"{said}, so {what} was not removed",
            steps=(f"remove {what} by hand in the provider's own player",),
            scope=Scope.SOURCE,
            origin=("outbound", "account"),
            detail={**detail, "problem": problem},
        )

    def _claimed(self, identifier: str) -> bool:
        """Whether any ledger record names the playlist, made or adopted."""
        cfg = self._cfg
        return (
            ledger.product_made(cfg, identifier)
            or identifier in ledger.label_playlist_ids(cfg)
            or identifier in ledger.set_playlist_ids(cfg)
            or identifier in ledger.exported_playlist_ids(cfg)
        )

    def remove_root_playlist(self, playlist_id: str, kind: str) -> None:
        """Remove one root playlist of the named kind (U143). NEVER RETRIED.

        THE KIND IS ASKED FIRST, then the ledger: a kind other than debris or
        empty, and a playlist any ledger record names, are refused with no
        provider call, since the product's own playlists are
        :meth:`remove_playlist`'s and its rule.

        THE PROVIDER'S OWN ANSWER MUST BE OF THE KIND. The playlist is opened
        and its served name must carry the label batch's suffix, case exactly,
        for debris; for an empty one, it must declare no track and no video,
        both counts readable. Anything else is refused before the delete, so a
        playlist renamed, or an empty one given a track, since the gate was
        answered stays. WHAT IS NOT ASKED HERE is where the playlist sits and
        whether a debris playlist's tracks are still filed: the caller reads
        both again before it asks (``organize.root.apply``).

        Absent, read back and not retried on :meth:`remove_playlist`'s
        arguments.
        """
        from cratekit.sync.playlists import is_library_debris

        identifier = str(playlist_id)
        what = f"the playlist {identifier}"
        if kind not in kinds.ROOT_REMOVALS:
            raise self._root_refusal(
                what,
                f"{kind!r} is not a kind of root playlist this account removes",
                "not-a-root-kind",
                playlist_id=identifier,
            )
        if self._cfg is None or self._claimed(identifier):
            raise self._root_refusal(
                what,
                "a ledger record names it, or no ledger could be read, and the "
                "product's own playlists are not removed as root debris or empties",
                "ledger-claimed",
                playlist_id=identifier,
            )
        doing = f"remove the {kind} playlist {identifier}"
        found = self._call(doing, lambda: self._session.playlist(identifier))
        if found is _ABSENT or found is None:
            self._members.pop(identifier, None)
            return
        name = str(getattr(found, "name", "") or "")
        tracks = getattr(found, "num_tracks", None)
        videos = getattr(found, "num_videos", None)
        if kind == kinds.DEBRIS:
            served = is_library_debris(name)
        else:
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
        if not served:
            raise self._root_refusal(
                what,
                f"the provider serves it as {name!r} with {tracks!r} track(s) and "
                f"{videos!r} video(s), which is not {kind}",
                "not-this-kind",
                playlist_id=identifier,
                kind=kind,
            )
        try:
            remove = found.delete
        except AttributeError:
            remove = None
        if not callable(remove):
            raise self._root_refusal(
                what,
                "the provider does not serve it as one this account owns",
                "not-owned",
                playlist_id=identifier,
            )
        accepted = self._call(doing, remove, retries=0)
        if accepted is False:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the removal"), doing
            )
        served_after = self._call(doing, lambda: self._session.playlist(identifier))
        if served_after is not _ABSENT and served_after is not None:
            raise refuse(
                "outbound-remove-refused",
                f"the {kind} playlist {identifier} is still served by the provider "
                f"after it was asked to remove it, so it was not removed",
                steps=("check the playlist by hand in the provider's own player",),
                scope=Scope.RUN,
                origin=("outbound", "account"),
                detail={"playlist_id": identifier, "problem": "read-back-differs"},
            )
        self._members.pop(identifier, None)

    def remove_legacy_folder(self, folder_id: str) -> None:
        """Remove one empty legacy year folder at the root (U143). NEVER RETRIED.

        READ FIRST, ON THE PROVIDER'S ANSWER: the root's folders are listed and
        the folder must be among them under a legacy year folder's name, and
        it must hold no playlist and no folder. A folder the root no longer
        lists is already removed. Anything else is refused before the removal.

        THROUGH THE COLLECTION'S OWN REMOVAL, which names the folder by its
        identifier, rather than the client's folder object, whose lookup reads
        one page of fifty root folders (R-835).

        READ BACK: the root is listed again and must not name the folder.
        """
        identifier = str(folder_id)
        what = f"the folder {identifier}"
        root = self.folders()
        if identifier not in root:
            return
        name = root[identifier]
        if not kinds.legacy_year(name):
            raise self._root_refusal(
                what,
                f"its name {name!r} is not a legacy year folder's",
                "not-a-legacy-folder",
                folder_id=identifier,
            )
        held = len(self.folder_playlists(identifier)) + len(self.folder_folders(identifier))
        if held:
            raise self._root_refusal(
                what,
                f"{name!r} still holds {held} playlist(s) or folder(s)",
                "not-empty",
                folder_id=identifier,
            )
        doing = f"remove the folder {identifier}"
        # THE CLIENT IS REACHED INSIDE THE CALL, so a session with no user is
        # translated like any other provider failure. A NOT FOUND ANSWER IS
        # READ BACK rather than failed: the folder may have gone since the read.
        accepted = self._call(
            doing,
            lambda: self._session.user.favorites.remove_folders_playlists(
                [identifier], type="folder"
            ),
            retries=0,
        )
        if accepted is False:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the folder removal"), doing
            )
        if identifier in self.folders():
            raise refuse(
                "outbound-remove-refused",
                f"the folder {identifier} is still listed at the root after it was "
                f"asked to remove it, so it was not removed",
                steps=("check the folder by hand in the provider's own player",),
                scope=Scope.RUN,
                origin=("outbound", "account"),
                detail={"folder_id": identifier, "problem": "read-back-differs"},
            )


def open_account(cfg: Any = None) -> TidalAccount:
    """An account over a freshly logged in client, from the stored session.

    The configuration is what the pacing gate reads its interval and cooldown
    off (R-705), the FROZEN one a job carries rather than a fresh load. None
    means the gate's own defaults, which are still a gate.
    """
    gate = provider_gate.Gate(
        provider_gate.GateSettings.from_config(cfg) if cfg is not None else None
    )
    client = provider_session.client_session(gate=gate)
    return TidalAccount(
        client, cfg=cfg, catalogue=provider_session.catalogue_client(client, gate=gate)
    )


__all__ = [
    "ADD_CHUNK",
    "NOT_FOUND_NAMES",
    "REMOVE_CHUNK",
    "TRACK_HOSTS",
    "WRITE_RETRIES",
    "TidalAccount",
    "open_account",
    "track_reference",
]
