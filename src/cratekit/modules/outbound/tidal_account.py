"""The streaming provider's account, behind the outbound package's seam.

**ONE CLASS OVER U62'S SESSION.** Every question here goes to the provider client
that ``acquire.provider_session.client_session`` logged in, and every PAGED read
goes through ``acquire.listing``, for the reason ``label.tidal_catalogue`` gives:
a listing that quietly returns one page looks exactly like a short one. A guard
in the suite scans this file for a direct paging call and for a vendored import.

**ADD ONLY, BECAUSE THE PROTOCOL IS.** ``service.RemoteAccount`` declares no
remove, and this class calls no remove on the client. The outbound gates and the
confirm digest sit in front of every write; this module adds no gate and removes
none.

**THE WORKERS RELY ON THREE RULES THAT ARE NOT VISIBLE IN THEIR CODE.**

* A match is exact or it is ``None``. ``export.plan`` reports a ``None`` as an
  unmatched row and ``hearts.heart_back`` as an unmatched favourite, so a guess
  returned here is a heart on somebody else's recording with nothing reported.
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

from cratekit.acquire import listing, provider_session
from cratekit.acquire.adapter import TrackOutcome, classify_unavailable
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


class TidalAccount:
    """The six add only ``RemoteAccount`` members, over one logged in client."""

    def __init__(
        self, session: Any, *, sleep: Callable[[float], None] | None = None
    ) -> None:
        self._session = session
        # Looked up at construction rather than bound as a default, so a caller
        # that replaced ``time.sleep`` is honoured.
        self._sleep = sleep or time.sleep
        self._hearts: set[str] | None = None
        self._members: dict[str, list[str]] = {}

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

    def match_track(self, *, identity: str, isrc: str = "") -> str | None:
        """The one provider track this row names exactly, or ``None``.

        ISRC FIRST. One ISRC can name several provider tracks, the single, the
        album cut and every compilation that carries the recording. When the
        answer holds more than one distinct identifier this returns ``None``
        rather than the first, because which release gets the heart is not
        something the ISRC decides.

        IDENTITY SECOND, and only an exact provider track reference, see
        :func:`track_reference`. Never a text search over title and artist.
        """
        wanted = str(isrc or "").strip()
        if wanted:
            found = self._call(
                f"look up the ISRC {wanted}",
                lambda: self._session.get_tracks_by_isrc(wanted),
            )
            if found is not _ABSENT:
                distinct = {str(getattr(track, "id", "") or "") for track in found or ()}
                distinct.discard("")
                if len(distinct) == 1:
                    return distinct.pop()
                if len(distinct) > 1:
                    return None
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
        self._members[identifier] = []
        return identifier

    def add_to_playlist(self, playlist_id: str, remote_id: str) -> None:
        identifier = str(remote_id)
        members = self._membership(playlist_id)
        if identifier in members:
            return
        playlist = self._playlist(playlist_id)
        self._call(
            f"add the track {identifier} to the playlist {playlist_id}",
            lambda: playlist.add([identifier]),
        )
        members.append(identifier)

    def playlist_tracks(self, playlist_id: str) -> tuple[str, ...]:
        return tuple(self._membership(playlist_id))


def open_account() -> TidalAccount:
    """An account over a freshly logged in client, from the stored session."""
    return TidalAccount(provider_session.client_session())


__all__ = [
    "NOT_FOUND_NAMES",
    "TRACK_HOSTS",
    "WRITE_RETRIES",
    "TidalAccount",
    "open_account",
    "track_reference",
]
