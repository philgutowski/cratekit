"""The streaming provider's account, behind the outbound package's seam.

**ONE CLASS OVER U62'S SESSION.** Every question here goes to the provider client
that ``acquire.provider_session.client_session`` logged in, and every PAGED read
goes through ``acquire.listing``, for the reason ``label.tidal_catalogue`` gives:
a listing that quietly returns one page looks exactly like a short one. A guard
in the suite scans this file for a direct paging call and for a vendored import.

**ADD ONLY, BECAUSE THE PROTOCOL IS.** ``service.RemoteAccount`` declares no
remove, and this class calls no remove on the client. The outbound gates and the
confirm digest sit in front of every write; this module adds no gate and removes
none. ``rename_playlist`` is the one member that writes to something the product
did not create, and it is still not a removal: it retitles, changes no membership
and deletes nothing. The suite scans this file for a removal shape and a retitle
is not one.

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

from cratekit.acquire import listing, match, provider_session
from cratekit.acquire.adapter import TrackOutcome, classify_unavailable
from cratekit.core import provider_gate
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.modules.outbound import account

#: How many times a write or a single lookup is retried after its first attempt.
WRITE_RETRIES = 1

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


def _billed(track: Any) -> str:
    """Every artist a provider track bills, in its order, as one string.

    A library row spells a record by two artists as one artist field holding
    both, and the matcher's reader keeps only the first a provider row names.
    """
    names = []
    for entry in getattr(track, "artists", None) or ():
        name = entry if isinstance(entry, str) else getattr(entry, "name", "")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return " ".join(names)


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


def _streamable(track: Any) -> bool:
    """Whether the provider will play this track, absent a statement that it will not.

    THE CLIENT READS A TRACK'S VERSION ONLY WHEN IT IS AVAILABLE, so an extended
    mix the provider has withdrawn arrives with no version at all and reads as
    the plain record. It is left out of the choice rather than compared, for that
    reason and because a heart on a track nobody can play is not the favourite.
    """
    return getattr(track, "available", True) is not False


class TidalAccount:
    """The eight ``RemoteAccount`` members, over one logged in client.

    Six add only, one that retitles a playlist the account owns, and one that
    says why the last match of a row came back empty.
    """

    def __init__(
        self, session: Any, *, sleep: Callable[[float], None] | None = None
    ) -> None:
        self._session = session
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
        self, *, identity: str, isrc: str = "", title: str = "", artist: str = ""
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

        IDENTITY SECOND, and only an exact provider track reference, see
        :func:`track_reference`. Never a text search over title and artist:
        ``title`` and ``artist`` choose among tracks the ISRC already named and
        are never sent to the provider.
        """
        key = str(identity)
        self._reasons.pop(key, None)
        wanted = str(isrc or "").strip()
        if wanted:
            found = self._call(
                f"look up the ISRC {wanted}",
                lambda: self._session.get_tracks_by_isrc(wanted),
            )
            if found is not _ABSENT:
                tracks = {
                    str(getattr(track, "id", "") or ""): track for track in found or ()
                }
                tracks.pop("", None)
                if len(tracks) == 1:
                    return next(iter(tracks))
                if len(tracks) > 1:
                    chosen, reason = self._among(
                        tracks, isrc=wanted, title=title, artist=artist
                    )
                    if chosen is None:
                        self._reasons[key] = reason
                    return chosen
        reference = track_reference(identity)
        if reference is None:
            return None
        track = self._call(
            f"look up the track {reference}", lambda: self._session.track(reference)
        )
        if track is _ABSENT or track is None:
            return None
        resolved = str(getattr(track, "id", "") or "")
        return resolved if resolved == reference else None

    def _among(
        self, tracks: dict[str, Any], *, isrc: str, title: str, artist: str
    ) -> tuple[str | None, str]:
        """One of several tracks sharing an ISRC, or ``None`` and why not.

        TWO RULES, IN ORDER, AND NEITHER IS A GUESS.

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

        A TRACK THAT CANNOT BE READ STOPS THE FIRST RULE FROM CHOOSING, on
        ``intake.candidates.sole_exact``'s argument: one agreeing track beside
        one unreadable one is not known to be the only one that agrees. A track
        the provider will not play is never a candidate, see :func:`_streamable`.

        RELEASES SPELLED ALIKE WITH NONE HEARTED STAY UNMATCHED, and that is
        the larger half of what was measured. Nothing the seam carries tells a
        single from its album cut, and the first, the earliest or the lowest
        numbered is a policy rather than a fact about the row.
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
            + (f", {unreadable} could not be read" if unreadable else "")
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
        return None, (
            f"{named}{aside}, {len(agreeing)} of them agree with this row's "
            f"artist, title and version and the account hearts {len(hearted)} "
            f"of those, so none was chosen"
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

    def _membership(self, playlist_id: str) -> list[str]:
        if playlist_id not in self._members:
            playlist = self._playlist(playlist_id)
            tracks = self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks(playlist),
            )
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

        A client with no such call is passed over rather than refused, for the
        same reason; a guard in the suite pins the call on the client library,
        so an upgrade that renames it fails there instead of here.
        """
        private = getattr(created, "set_playlist_private", None)
        if not callable(private):
            return
        try:
            self._call(f"make the playlist {identifier} private", private)
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


def open_account(cfg: Any = None) -> TidalAccount:
    """An account over a freshly logged in client, from the stored session.

    The configuration is what the pacing gate reads its interval and cooldown
    off (R-705), the FROZEN one a job carries rather than a fresh load. None
    means the gate's own defaults, which are still a gate.
    """
    gate = provider_gate.Gate(
        provider_gate.GateSettings.from_config(cfg) if cfg is not None else None
    )
    return TidalAccount(provider_session.client_session(gate=gate))


__all__ = [
    "NOT_FOUND_NAMES",
    "TRACK_HOSTS",
    "WRITE_RETRIES",
    "TidalAccount",
    "open_account",
    "track_reference",
]
