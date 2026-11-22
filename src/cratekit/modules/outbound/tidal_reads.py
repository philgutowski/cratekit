"""The account's reads: a row matched to one provider track, the hearts, playlists and folders.

``tidal_account.TidalAccount`` is composed from :class:`Reads` and the writes
there. Every PAGED read goes through ``acquire.listing``, for the reason
``label.tidal_catalogue`` gives: a listing that quietly returns one page looks
exactly like a short one. The suite scans this file for a direct paging call, a
vendored import and a removal, as it scans ``tidal_account``.

**THE WORKERS RELY ON THREE RULES THAT ARE NOT VISIBLE IN THEIR CODE.**

* A match is exact or it is ``None``. ``export.plan`` and ``hearts.heart_back``
  report a ``None`` as unmatched, so a guess here is a heart on somebody else's
  recording with nothing reported. A ``None`` that had candidates says why
  through ``unmatched_reason``, since "never heard of it" and "three of these
  and nothing here could choose" are different things to act on.
* ``has_heart`` answers from ONE paged read of the favourites per adapter, and
  the seam hands a run one adapter: asking per candidate, a sweep of a thousand
  hearts would make a thousand listing calls.
* Catalogue lookups (the ISRC and the exact track) go to ``_lookups``, the app
  client when the opener built one (U205), else the account session; the
  account's own hearts, playlists and folders are read through the account
  session only.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

from cratekit.acquire import isrc_cache, listing, match
from cratekit.acquire.adapter import TrackOutcome, classify_unavailable
from cratekit.modules.outbound import service

#: Hosts a provider track URL is read from, the three the catalogue reads a
#: playlist URL from.
TRACK_HOSTS = frozenset({"tidal.com", "www.tidal.com", "listen.tidal.com"})

#: A provider track identifier as it appears in a track URL's last segment.
_TRACK_ID = re.compile(r"[0-9]+")

#: Client exception names that are a fact about the thing asked for rather than
#: the session or the network. ``InvalidISRC`` is an ISRC the provider will not
#: accept, which is no match rather than an outage.
NOT_FOUND_NAMES = frozenset({"ObjectNotFound", "InvalidISRC"})

#: Words a library row puts BETWEEN artists that no artist is billed under. A
#: comma and an ampersand need no entry, since ``match.fold`` takes them off.
_JOINERS = frozenset({"feat", "ft", "featuring", "with", "and", "vs", "x"})

#: The answer a lookup gives for an explicit not found, kept off the retry.
_ABSENT = object()


def _identifier(item: Any) -> str:
    """The provider identifier an item carries, as text, or ``""``."""
    return str(getattr(item, "id", "") or "")


def _not_found(exc: BaseException) -> bool:
    """Whether a failure is the provider saying it has nothing, asked FIRST."""
    if type(exc).__name__ in NOT_FOUND_NAMES:
        return True
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT


def track_reference(identity: str) -> str | None:
    """The provider track identifier an identity names EXACTLY, or ``None``.

    ONE SHAPE: a track URL on a provider host whose path ends ``track/<digits>``.
    A bare number is refused: the identity a worker hands this seam is a
    rekordbox ``TrackID``, also a bare number, and reading it as a provider
    identifier would heart whatever unrelated recording carries that number.
    """
    parts = urlsplit(str(identity or "").strip())
    if parts.scheme not in {"http", "https"} or (parts.hostname or "").lower() not in TRACK_HOSTS:
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) >= 2 and segments[-2] == "track" and _TRACK_ID.fullmatch(segments[-1]):
        return segments[-1]
    return None


def _row_of(title: str, artist: str) -> match.Wanted | None:
    """The library row in the shape the product's matcher reads, or ``None``.

    READ BY ``match.read_row``, so a bracketed version, a version after a dash,
    a featured credit and a title that reads two ways mean here what they mean
    to intake. ``None`` for a row naming no artist or no title: half a name is
    not unique to a recording.
    """
    try:
        return match.read_row(
            {"title": str(title or ""), "artist": str(artist or "")}, origin=match.TEXT, position=1
        )
    except match.UnreadableList:
        return None


def _added_at(track: Any) -> str:
    """When a playlist item was added, as ISO 8601 UTC text, or ``""`` when unknown (U201)."""
    for name in ("user_date_added", "date_added"):
        value = getattr(track, name, None)
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(timezone.utc).isoformat()
    return ""


def _artist_names(track: Any) -> list[str]:
    """Every artist a provider track bills, in its order."""
    names = (
        entry if isinstance(entry, str) else getattr(entry, "name", "")
        for entry in getattr(track, "artists", None) or ()
    )
    return [name.strip() for name in names if isinstance(name, str) and name.strip()]


def _shown_artist(track: Any) -> str:
    """The artists a provider track bills, as a person reads them on a gate."""
    lead = getattr(track, "artist", None)
    return ", ".join(_artist_names(track)) or str(getattr(lead, "name", "") or "")


def _title(track: Any) -> str:
    """A provider track's title as a person reads it, its version included."""
    return str(getattr(track, "full_name", "") or getattr(track, "name", "") or "")


def _named(items: Iterable[Any]) -> dict[str, str]:
    """Each item that carries an identifier, identifier to name."""
    return {
        _identifier(item): str(getattr(item, "name", "") or "")
        for item in items
        if _identifier(item)
    }


def _artist_agrees(row_artist: str, first_billed: str, track: Any) -> bool:
    """Whether the row's artist field names this track's artists and no others.

    COMPARED AS WORDS, NEVER SPLIT INTO NAMES, since a comma is legal inside an
    artist's own name. Two conditions, each removable alone: every word of the
    FIRST billed artist is in the row, so a row naming only the guest does not
    agree; and the row holds no word the track does not bill, joiners aside, so
    another act sharing a word does not either. Between them a row may bill the
    artists in another order, leave out a remixer the provider bills, and spell
    the join as a comma, an ampersand or "feat.". The matcher's reader keeps
    only the first artist a provider row names, so every billed artist is read
    here.
    """
    ours = set(match.fold(row_artist).split())
    first = set(match.fold(first_billed).split())
    billed = first | set(match.fold(" ".join(_artist_names(track))).split())
    return bool(first) and first <= ours and ours - billed <= _JOINERS


def _agrees(row: match.Wanted, track: Any) -> bool | None:
    """Whether a provider track is the row's recording AND version.

    ``None`` when the track cannot be read at all, which is not a disagreement
    (see :meth:`Reads._among`). EITHER READING OF EITHER TITLE COUNTS, since
    "Sun Path - Live" is a version or the end of a title and the string cannot
    say which. ``intake.candidates.sole_exact`` refuses a row that reads two
    ways outright and this does not, on purpose: here every candidate already
    carries the row's own ISRC and exactly one must still agree.
    """
    try:
        listed = match.read_row(track, origin=match.TIDAL, position=1)
    except match.UnreadableList:
        return None
    if not _artist_agrees(row.artist, listed.artist, track):
        return False
    ours = {(match.title_identity(one.title), one.version_key) for one in row.readings}
    theirs = {(match.title_identity(one.title), one.version_key) for one in listed.readings}
    return bool(ours & theirs)


def _album_name(track: Any) -> str:
    """The name of the release a provider track sits on, or ``""`` unread."""
    return str(getattr(getattr(track, "album", None), "name", "") or "")


def _lowest(remotes: list[str]) -> str:
    """The lowest provider identifier, numbers by value, the one a tie takes (R-1032).

    Not a fact about the row: the same answer on every run whatever order the
    provider lists them in, so a refresh never swaps one release for another.
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

    THE CLIENT READS A TRACK'S VERSION ONLY WHEN IT IS AVAILABLE, so a withdrawn
    extended mix reads as the plain record. It is left out of the choice, and a
    heart on a track nobody can play is not the favourite anyway.
    """
    return getattr(track, "available", True) is not False


class Reads:
    """The reads ``TidalAccount`` is composed from, over its ``_call``, ``_read``, ``_playlist``."""

    # ── matching ────────────────────────────────────────────────────────────

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask the catalogue which of ``codes`` it files anything under, in batches (U207).

        BEFORE A PLAN'S LOOKUPS, NEVER INSTEAD OF THEM: a code a batch answered
        as filed under nothing is answered not found by :meth:`match_track`
        with no request, and every other code is still asked alone there, so
        :meth:`_among` sees every release. Only the app client is asked (see
        ``acquire.isrc_screen``). Returns the requests made. A code the ISRC
        cache answers (U206) is not screened, since its lookup makes no request.
        """
        return self._screen.screen_uncached(self._lookups, self._cache, codes)

    def match_track(
        self, *, identity: str, isrc: str = "", title: str = "", artist: str = "",
        agree: bool = False, album: str = "", any_agreeing: bool = False,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.

        ISRC FIRST. One ISRC can name the single, the album cut and every
        compilation, and which release gets the heart is not the ISRC's to
        decide, so several identifiers go to :meth:`_among`, which chooses by
        what the ROW says and by what the account hearts, never by position
        (R-356). With ``agree`` one track is chosen as several are, so a code
        read off a file's tag names a track only when it is the row's recording
        and version (R-879). ``album`` is the file's own album tag (R-572), and
        ``any_agreeing`` lets a tie between agreeing releases take one (R-1032,
        U208), which :meth:`tie_broken` then says.

        IDENTITY SECOND, and only an exact track reference (:func:`track_reference`).
        Never a text search: ``title`` and ``artist`` choose among tracks the
        ISRC named and are never sent to the provider.
        """
        key = str(identity)
        self._reasons.pop(key, None)
        self._ties.discard(key)
        wanted = str(isrc or "").strip()
        if wanted:
            # A code a batch answered as filed under nothing (U207) is the empty
            # answer this lookup would give; every other is remembered or asked.
            found = _ABSENT if self._screen.absent(wanted) else self._isrc_tracks(wanted)
            tracks = {} if found is _ABSENT else {_identifier(one): one for one in found or ()}
            tracks.pop("", None)
            if len(tracks) == 1 and not agree:
                return next(iter(tracks))
            if tracks:
                chosen, reason, tied = self._among(
                    tracks, isrc=wanted, title=title, artist=artist, album=album,
                    any_agreeing=any_agreeing,
                )
                if chosen is None:
                    self._reasons[key] = reason
                elif tied:
                    self._ties.add(key)
                return chosen
        reference = track_reference(identity)
        if reference is None:
            return None
        track = self._call(f"look up the track {reference}", lambda: self._lookups.track(reference))
        if track is _ABSENT or track is None:
            return None
        resolved = _identifier(track)
        return resolved if resolved == reference else None

    def _isrc_tracks(self, wanted: str) -> Any:
        """The provider's tracks for one ISRC, remembered or asked (U206).

        A remembered not found is ``_ABSENT`` as an asked one is. Asked, an
        answer is kept only when it is one: a track list, or a not found the
        client said in so many words on the attempt that settled it
        (``isrc_cache.said_not_found``); never an ``InvalidISRC`` or anything
        the ladder raised.
        """
        # The country of the client that is ASKED, the app client when open.
        country = isrc_cache.country_of(self._lookups)
        held = self._cache.recall(wanted, country)
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said, reset on each one, so a not found on an
        # attempt the ladder retried past is not read as the settling answer.
        last = {"said_not_found": False}

        def ask() -> Any:
            last["said_not_found"] = False
            try:
                return self._lookups.get_tracks_by_isrc(wanted)
            except Exception as exc:
                last["said_not_found"] = isrc_cache.said_not_found(exc)
                raise

        isrc_cache.asked()
        found = self._call(f"look up the ISRC {wanted}", ask)
        if found is _ABSENT:
            if last["said_not_found"]:
                self._cache.remember(wanted, country, ())
        elif isinstance(found, (list, tuple)):
            self._cache.remember(wanted, country, found)
        return found

    def _among(
        self, tracks: dict[str, Any], *, isrc: str, title: str, artist: str, album: str = "",
        any_agreeing: bool = False,
    ) -> tuple[str | None, str, bool]:
        """One of several tracks sharing an ISRC, or ``None`` and why not, and whether a tie chose.

        THREE RULES, IN ORDER, AND NONE IS A GUESS.

        1. The tracks that agree with the row's artist, title and version
           (:func:`_agrees`): exactly one is the match. This separates a radio
           edit from an extended mix filed under one code.
        2. Of several agreeing, the one the account ALREADY HEARTS: the person
           chose that release once. Asked of the agreeing tracks only.
        3. Of none hearted, the one whose album name is the album tag of the
           row's own file (R-572), asked of the agreeing tracks only.

        A TRACK THAT CANNOT BE READ STOPS THE FIRST AND THIRD RULES, on
        ``intake.candidates.sole_exact``'s argument: one agreeing track beside
        an unreadable one is not known to be the only one. A track the provider
        will not play is never a candidate (:func:`_streamable`). Releases left
        tied stay unmatched: the first, earliest or lowest is a policy about the
        catalogue, not a fact about the row (R-572).

        UNLESS ``any_agreeing`` SAYS ANY WILL DO (R-1032): the mirror's
        listening copy and, since U208, the pairs (Phillip, Sitting 54). A tie
        with no unreadable candidate then takes :func:`_lowest` of the hearted
        releases if several, else of every agreeing one, narrowed first to
        those the file's album names. The refusals before it are unchanged.
        The third value is true only for a track that without ``any_agreeing``
        would have been refused.
        """
        named = f"the ISRC {isrc} names {len(tracks)} provider tracks"
        row = _row_of(title, artist)
        if row is None:
            return None, (
                f"{named} and this row carries no artist and title to choose "
                f"among them by"
            ), False
        verdicts = {
            remote: _agrees(row, track) for remote, track in tracks.items() if _streamable(track)
        }
        withdrawn = len(tracks) - len(verdicts)
        unreadable = sum(1 for verdict in verdicts.values() if verdict is None)
        agreeing = [remote for remote, verdict in verdicts.items() if verdict]
        if len(agreeing) == 1 and not unreadable:
            return agreeing[0], "", False
        aside = (
            (f", {withdrawn} cannot be streamed" if withdrawn else "")
            + (f", {unreadable} {service.UNREADABLE_CANDIDATE}" if unreadable else "")
        )
        if not agreeing:
            rest = "the rest" if aside else "them"
            return None, (
                f"{named}{aside} and none of {rest} agrees with this row's "
                f"artist, title and version"
            ), False
        hearts = self._favorites()
        hearted = [remote for remote in agreeing if remote in hearts]
        if len(hearted) == 1:
            return hearted[0], "", False
        if any_agreeing and not unreadable:
            # A TIE ONLY WHEN SOMETHING WAS LEFT TO BREAK: two hearts, or more
            # than one release after the album. One release the album names is
            # the album rule's answer, which stands without ``any_agreeing``.
            narrowed = _on_album(hearted or agreeing, tracks, album)
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
        said = (
            f"{named}{aside}, {len(agreeing)} {service.AGREEING_RELEASES} and the "
            f"account hearts {len(hearted)} of those"
        )
        if hearted:
            return None, f"{said}, so none was chosen", False
        if unreadable:
            return None, f"{said}, so none was chosen", False
        wanted = match.fold(album)
        if not wanted:
            return None, f"{said}, and the file carries no album tag, so none was chosen", False
        named_album = [
            remote for remote in agreeing if match.fold(_album_name(tracks[remote])) == wanted
        ]
        if len(named_album) == 1:
            return named_album[0], "", False
        return None, (
            f"{said}, and the file's album {album!r} names {len(named_album)} "
            f"of them, so none was chosen"
        ), False

    def unmatched_reason(self, identity: str) -> str:
        """Why the last match of this row came back ``None``, or ``""``.

        Empty for a row the provider does not have, which the workers already
        report as unmatched, and for a row that matched.
        """
        return self._reasons.get(str(identity), "")

    def tie_broken(self, identity: str) -> bool:
        """Whether the last match of this row took one of a tie between agreeing releases (U208).

        True only when ``any_agreeing`` chose a track that without it would
        have been refused; false after any other match and after a miss.
        """
        return str(identity) in self._ties

    # ── hearts ──────────────────────────────────────────────────────────────

    def _favorites(self) -> set[str]:
        if self._hearts is None:
            tracks = self._read(
                "read the account's favourite tracks",
                lambda: listing.favorite_tracks(self._session),
            )
            self._hearts = {_identifier(track) for track in tracks} - {""}
        return self._hearts

    def has_heart(self, remote_id: str) -> bool:
        return str(remote_id) in self._favorites()

    # ── playlists ───────────────────────────────────────────────────────────

    def _listed(self, playlist_id: str, playlist: Any) -> list[Any]:
        """Every track object on the playlist, in order, read now across pages."""
        return self._read(
            f"read the playlist {playlist_id}",
            lambda: listing.playlist_tracks(playlist),
        )

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        return tuple(self._membership(playlist_id))

    def track_names(self, playlist_id: str) -> dict[str, tuple[str, str]]:
        """Every track on the playlist, identifier to ``(artist, title)``, read now.

        Fresh rather than the remembered membership, since a playlist created
        or added to in this run is remembered by identifier alone; the read
        :meth:`playlist_listing` makes.
        """
        return self.playlist_listing(playlist_id).names

    def playlist_listing(self, playlist_id: str) -> service.PlaylistListing:
        """Every track on the playlist with its added time and the declared count (U201).

        One read, remembered as :meth:`track_names` remembers it. The added time
        is the client's ``user_date_added``, else ``date_added``; one with no
        zone, or none, is left out rather than guessed, since the mirror reads
        an absent time as unknown. The declared count is ``num_tracks``.
        """
        playlist = self._playlist(playlist_id)
        tracks = self._listed(playlist_id, playlist)
        ids = [_identifier(track) for track in tracks]
        self._members[playlist_id] = ids
        names: dict[str, tuple[str, str]] = {}
        added: dict[str, str] = {}
        for identifier, track in zip(ids, tracks, strict=True):
            if not identifier or identifier in names:
                continue
            names[identifier] = (_shown_artist(track), _title(track))
            if moment := _added_at(track):
                added[identifier] = moment
        declared = getattr(playlist, "num_tracks", None)
        return service.PlaylistListing(
            names=names, added=added, listed=len(ids),
            declared=declared if isinstance(declared, int) and not isinstance(declared, bool) else None,
        )

    # ── folders (R-835) ─────────────────────────────────────────────────────

    def _folder(self, folder_id: str) -> Any:
        """The client's folder object for one identifier, WITHOUT its lookup.

        The client's own lookup reads one page of fifty root folders and raises
        not found for any later one, so the object is built empty, which makes
        no request, and given the identifier every later call names it by.
        """
        handle = self._session.folder()
        handle.id = str(folder_id)
        return handle

    def _in_folder(self, folder_id: str, doing: str, reader: Callable[[Any], Any]) -> list[Any]:
        """One paged read of what one folder holds."""
        handle = self._folder(folder_id)
        return self._read(doing, lambda: reader(handle))

    def folders(self) -> dict[str, str]:
        return _named(
            self._read("read the account's folders", lambda: listing.account_folders(self._session))
        )

    def folder_playlists(self, folder_id: str) -> dict[str, str]:
        return _named(
            self._in_folder(folder_id, f"read the folder {folder_id}", listing.folder_playlists)
        )

    def folder_playlists_dated(self, folder_id: str) -> dict[str, tuple[str, datetime | None]]:
        """Each playlist one folder holds, with when the account says it was made (U216).

        The walk :meth:`folder_playlists` makes, with the creation time the
        client's parser reads off the same item; a time it does not carry, or
        one that is not a moment, is None.
        """
        found = self._in_folder(folder_id, f"read the folder {folder_id}", listing.folder_playlists)
        dated: dict[str, tuple[str, datetime | None]] = {}
        for playlist in found:
            if identifier := _identifier(playlist):
                made = getattr(playlist, "created", None)
                dated[identifier] = (
                    str(getattr(playlist, "name", "") or ""),
                    made if isinstance(made, datetime) else None,
                )
        return dated

    def folder_folders(self, folder_id: str) -> dict[str, str]:
        return _named(
            self._in_folder(folder_id, f"read the folders in {folder_id}", listing.folder_folders)
        )
