"""The one place the label package gets the catalogue it reads a provider through.

``cratekit.label.tidal_catalogue`` implements :class:`Catalogue` over the client
``acquire.provider_session.session_for`` holds for the process (U62, U261).
``label-catalogue-unbound`` is kept for a build in which the adapter or its
client library does not import.

This module only asks whether ``secrets.Credential.PROVIDER_SESSION`` is
recorded; every read of the token is the session module's (R4), so doctor and
the verbs agree about the credential.

It is its own seam and not the outbound one: that is add only writes against an
account, this is reads against a catalogue, and the two share a credential
rather than a capability.

A test replaces :func:`resolve` on this module and callers look it up at call
time. The child ``crate job resume`` spawns inherits nothing and resolves the
real adapter.

Layer: modules.
"""

from __future__ import annotations

import importlib
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import urlsplit

from cratekit.acquire import provider_session
from cratekit.acquire.adapter import AdapterAuthFailed, AdapterBroken
from cratekit.acquire.provider_session import ProviderUnavailable
from cratekit.core import config, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import registry

#: The module that implements :class:`Catalogue`, imported by name through
#: ``importlib``, since a ``from`` import answers from the package attribute once
#: the module has loaded anywhere in the process.
ADAPTER_MODULE = "cratekit.label.tidal_catalogue"


#: How many rows :meth:`Catalogue.search_tracks` returns at most. On the seam
#: because the caller reads an answer this long as possibly cut off.
TRACK_SEARCH_PAGE = 50


# The reference parser is pure and lives on the seam because a core reader
# needs it and core cannot import the adapter. The adapter re-exports it.

#: A provider playlist identifier, which the provider mints as a UUID.
_UUID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE
)

#: Hosts a playlist URL or a share link (the URL with a query) is read from.
PLAYLIST_HOSTS = frozenset({"tidal.com", "www.tidal.com", "listen.tidal.com"})

#: The short link host, refused by name since only the provider can expand it.
SHORT_LINK_HOST = "link.tidal.com"


class PlaylistReferenceInvalid(ValueError):
    """A reference that is not a playlist URL, a share link, or an identifier."""


def playlist_id(reference: str) -> str:
    """The playlist identifier inside what a person typed, or a named refusal.

    A bare identifier, a URL on a provider host whose path ends
    ``playlist/<id>``, or that URL with a query. Anything else is refused rather
    than searched for, since a guess could list someone else's playlist.
    """
    text = str(reference or "").strip()
    if _UUID.fullmatch(text):
        return text.lower()
    parts = urlsplit(text)
    host = (parts.hostname or "").lower()
    if parts.scheme in {"http", "https"} and host == SHORT_LINK_HOST:
        raise PlaylistReferenceInvalid(
            f"{reference!r} is a short share link, which only the provider can "
            f"expand; open it and pass the playlist URL it lands on"
        )
    if parts.scheme in {"http", "https"} and host in PLAYLIST_HOSTS:
        segments = [segment for segment in parts.path.split("/") if segment]
        if len(segments) >= 2 and segments[-2] == "playlist" and _UUID.fullmatch(segments[-1]):
            return segments[-1].lower()
    raise PlaylistReferenceInvalid(
        f"{reference!r} is not a playlist URL, a share link, or a playlist "
        f"identifier"
    )


@dataclass(frozen=True, slots=True)
class AccountPlaylist:
    """One playlist the account itself created, reduced to what a sweep decides on.

    ``playlist_id`` is the identity (D5). ``name`` is read only for naming
    conventions and never stored. ``tracks`` is the reported count, ``None``
    when none was reported, which is unknown rather than empty.
    """

    playlist_id: str
    name: str
    tracks: int | None = None


@dataclass(frozen=True, slots=True)
class Unread:
    """One part of a label's catalogue a crawl could not read, and why (R-261, R-393).

    A skip is deliberate, but recorded, so skipped releases never read as
    releases that were never there. ``artist`` is the provider's name, or its
    identifier. ``listing`` is the method not read, or ``artist_releases`` when
    one artist's whole listing failed. ``transient`` says whether another
    attempt can differ: a rate limit clears, a missing method does not.
    """

    artist: str
    listing: str
    reason: str
    transient: bool


def missing_listing(artist: Any, method: str) -> Unread:
    """The record for a listing method ``artist`` does not expose."""
    name = str(getattr(artist, "name", "") or getattr(artist, "id", "") or "")
    return Unread(
        artist=name or type(artist).__name__,
        listing=method,
        reason=f"the provider client exposes no {method} listing",
        transient=False,
    )


class ReleaseUnresolvable(LookupError):
    """A release identifier the provider has nothing for, or none at all.

    On the seam because a caller settles a withdrawn release differently from
    every other failure. It catches this class, never ``LookupError``, so a
    client's ``KeyError`` is not reported as a release that is gone.
    """


#: The verdict :meth:`Catalogue.reread_release` answers for a release the
#: provider no longer has (R-1634): the provider answered, and said nothing of
#: a credit. The sweep asks the next held release rather than refusing on it.
RELEASE_GONE = "gone"


def artist_name(release: Any) -> str:
    """The name of a release's artist, never a provider object's repr (R-379).

    A plain string is the name; an object is read for its ``name``, and one with
    none is the empty string. One reader for the sweep and the repair (R-840).
    """
    artist = getattr(release, "artist", None)
    if artist is None:
        return ""
    if isinstance(artist, str):
        return artist
    name = getattr(artist, "name", None)
    return name if isinstance(name, str) else ""


#: How many reads of release tracks in a row may fail before
#: :class:`ReleaseTracks` stops asking: one is a bad release, two a coincidence,
#: and each has already spent a full retry ladder.
READS_FAILED_IN_A_ROW = 3


class ReleasesUnasked(RuntimeError):
    """A release whose tracks were not asked for, because the provider is failing.

    Raised by :class:`ReleaseTracks`, never by the provider, so a caller says
    nobody asked rather than calling it failed or gone.
    """


class ReleaseTracks:
    """One sweep item's reads of release tracks, each release read once (R-798).

    Ownership and the genre gate read the same rows, so the second asker gets
    the first one's answer. A failure is remembered and raised again, a gone
    release included; a ``CratekitError`` is not, since it stops the item.

    The outage rule lives here once: after :data:`READS_FAILED_IN_A_ROW` failed
    reads in a row, a release not yet read raises :class:`ReleasesUnasked`
    without a call. A gone release is the provider answering and ends the run.
    Built per label, so nothing outlives the sweep that met it.
    """

    def __init__(self, catalogue: "Catalogue") -> None:
        self.catalogue = catalogue
        self._read: dict[str, ReleaseRead | Exception] = {}
        self._failed_in_a_row = 0

    @property
    def given_up(self) -> bool:
        """Whether the outage rule has ended the asking for a release not yet read (R-815)."""
        return self._failed_in_a_row >= READS_FAILED_IN_A_ROW

    def forget(self) -> None:
        """Drop every remembered read and keep the count of failures in a row.

        For a reader that outlives one sweep item and reads each release once
        (R-815), so a long run does not carry every row and traceback.
        """
        self._read.clear()

    def release_tracks(self, release_id: str) -> ReleaseRead:
        held = self._read.get(release_id)
        if isinstance(held, Exception):
            raise held
        if held is not None:
            return held
        if self.given_up:
            raise ReleasesUnasked(
                f"the provider failed {READS_FAILED_IN_A_ROW} releases in a row, so "
                f"the rest were not asked for"
            )
        try:
            rows, year, short = self.catalogue.release_tracks(release_id)
        except CratekitError:
            raise
        except ReleaseUnresolvable as exc:
            self._failed_in_a_row = 0
            self._read[release_id] = exc
            raise
        except Exception as exc:
            self._failed_in_a_row += 1
            self._read[release_id] = exc
            raise
        self._failed_in_a_row = 0
        answer = (tuple(rows), year, short)
        self._read[release_id] = answer
        return answer


class _Shortfall:
    """The three numbers a short listing is reported by, one spelling everywhere."""

    __slots__ = ()
    declared: int
    listed: int

    @property
    def withheld(self) -> int:
        return self.declared - self.listed

    def summary(self) -> str:
        """The three numbers as a person reads them."""
        return (
            f"{self.declared} declared, {self.listed} listed, "
            f"{self.withheld} withheld by the provider"
        )

    def block(self) -> dict[str, int]:
        """The three numbers as a report carries them."""
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}


class HeartsShortfall(_Shortfall, Exception):
    """The hearts listing came back shorter than the account declares (R-504).

    The provider counts hearts it will not serve. The rows it did serve ride on
    the exception, and a caller that does not know this class fails closed.
    Which hearts were withheld is not known; only the count is.
    """

    def __init__(self, rows: Any, declared: int) -> None:
        self.rows = tuple(rows)
        self.declared = declared
        super().__init__(self.summary())

    @property
    def listed(self) -> int:
        return len(self.rows)


@dataclass(frozen=True, slots=True)
class ListingShortfall(_Shortfall):
    """A playlist or release listing shorter than its declared count (R-515).

    Not a failure to read: carried beside the rows rather than raised, and only
    never reported as complete. Only the count of **Withheld** is known.
    """

    declared: int
    listed: int

    @classmethod
    def of(cls, rows: Any, declared: Any) -> "ListingShortfall | None":
        """The shortfall of ``rows`` against ``declared``, or ``None`` when there is none.

        ``None`` too for no usable count: zero, negative, non integer or missing.
        """
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
            return None
        listed = len(tuple(rows))
        if listed >= declared:
            return None
        return cls(declared=declared, listed=listed)


#: What :meth:`Catalogue.release_tracks` answers: the rows, the year, and the
#: shortfall when the release listed short of its declared count (R-515).
ReleaseRead = tuple[tuple[Any, ...], int | None, ListingShortfall | None]


class Catalogue(Protocol):
    """Every provider read the product makes through this seam, one member per call site.

    The failure contract is part of the type: :meth:`artist_for` and
    :meth:`playlist_for` raise for what the provider cannot resolve and never
    return ``None`` or an empty stand in, since a sweep would read that as a
    label with nothing new (R-135, R11). Every listing likewise raises when it
    cannot be read, so an empty answer always means the provider answered.
    """

    def artist_for(self, entry: registry.LabelEntry) -> Any:
        """The provider artist object this label's catalogue hangs off, paged by the crawl.

        May be a roster; one whose releases are in memory is a
        ``listing.HeldReleases``, read whole (R-888). It may carry ``unread``, a
        tuple of :class:`Unread` for parts of the roster it could not read
        (R-261, R-393).
        """

    def playlist_for(self, reference: str) -> Any:
        """The provider playlist object for a URL or an identifier a person typed."""

    def search_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Who is actually credited on one release, ``verify.verify_release``'s ``search``."""

    def reread_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """:meth:`search_release`'s answer, read again by identifier, never from the line (R-1634).

        A release the provider no longer has answers :data:`RELEASE_GONE`, and
        one with no identifier is never read and answers ``unconfirmed``.
        """

    def check_label(self, name: str) -> dict:
        """Whether a harvested label name is a real imprint, for ``harvest.from_tracks``."""

    def account_playlists(self) -> tuple[AccountPlaylist, ...]:
        """Every playlist the logged in account created, across every page."""

    def favourite_tracks(self) -> tuple[Any, ...]:
        """Every track the logged in account has hearted, across every page.

        Raises :class:`HeartsShortfall` with the rows when they come back fewer
        than the provider's count, so a tuple returned reached the count.
        """

    def release_tracks(self, release_id: str) -> ReleaseRead:
        """Every track on one release read by identifier, its year, and any shortfall.

        Raises :class:`ReleaseUnresolvable` for a release the provider has
        nothing for. The year is ``None`` when unreadable, and the shortfall is
        the :class:`ListingShortfall` of a short listing (R-515).
        """

    def release_artist(self, release_id: str) -> str:
        """The name of the artist one release is filed under, in one read (R-840).

        Raises :class:`ReleaseUnresolvable` for a release the provider has
        nothing for.
        """

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask in batches which codes the provider files nothing under (U207).

        Raises nothing for a batch it could not answer; returns the requests made.
        """

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        """Every provider track filed under one ISRC (R-356); the rows carry ``id``."""

    def search_tracks(self, artist: str, title: str, offset: int = 0) -> tuple[Any, ...]:
        """One page of a text search for an artist and title, a proposal and never a pick.

        In the provider's order, at most :data:`TRACK_SEARCH_PAGE` rows starting
        at ``offset`` (U79, R-302, R-879); a shorter page is the end.
        """


def bound() -> bool:
    """Whether this build can produce a catalogue at all, asked without trying.

    A queueing verb warns with it before a person confirms; :func:`resolve`
    would spend a login. It reads no credential, only whether the adapter and
    its client library import.
    """
    return provider_session.importable(ADAPTER_MODULE)


#: The session module's remedy in the product's vocabulary, named per value so
#: an unknown one lands on reauthenticating rather than on a crash.
_REMEDIES = {
    Remedy.REAUTHENTICATE_PROVIDER.value: Remedy.REAUTHENTICATE_PROVIDER,
    Remedy.REPAIR_CREDENTIAL_STORE.value: Remedy.REPAIR_CREDENTIAL_STORE,
}


def _unbound(exc: BaseException) -> Exception:
    return refuse(
        "label-catalogue-unbound",
        "a provider session is stored and the catalogue adapter that would use "
        f"it to list a label or a playlist does not import in this build ({exc}), "
        "so the queued work cannot be carried out. Nothing was offered for review",
        steps=("reinstall the product so its core dependencies are present, then retry",),
        scope=Scope.RUN,
        origin=("label", "catalogue"),
    )


def resolve(cfg: config.Config) -> Catalogue:
    """The catalogue this library's label reads go through, or why there is none.

    Four refusals, each undone by a different act: an unreachable provider is a
    wait and keeps the session; a missing credential is the person's to record;
    a rejected session or unreadable keychain takes the session module's remedy;
    an adapter that does not import is this build's gap.

    A fresh catalogue over one login per process (U261), with the presence
    check first on every resolve. The frozen configuration is handed on for
    the pacing gate (R-705).
    """
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no catalogue "
            "to read this label or this playlist from",
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        )
    try:
        tidal_catalogue = importlib.import_module(ADAPTER_MODULE)
    except ImportError as exc:
        raise _unbound(exc) from exc
    try:
        return tidal_catalogue.open_catalogue(cfg)
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
            f"the streaming provider could not be reached to open the catalogue "
            f"({exc}); the stored session was not judged and is kept",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
        ) from exc
    except (AdapterAuthFailed, AdapterBroken) as exc:
        raise refuse(
            "credential-missing",
            f"the stored streaming provider session could not be used to open "
            f"the catalogue ({exc})",
            remedy=_REMEDIES.get(exc.remedy.value, Remedy.REAUTHENTICATE_PROVIDER),
            scope=Scope.RUN,
            origin=("label", "catalogue"),
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},
        ) from exc


__all__ = [
    "ADAPTER_MODULE",
    "PLAYLIST_HOSTS",
    "SHORT_LINK_HOST",
    "AccountPlaylist",
    "Catalogue",
    "HeartsShortfall",
    "ListingShortfall",
    "ReleaseRead",
    "PlaylistReferenceInvalid",
    "READS_FAILED_IN_A_ROW",
    "ReleaseTracks",
    "ReleaseUnresolvable",
    "ReleasesUnasked",
    "TRACK_SEARCH_PAGE",
    "Unread",
    "artist_name",
    "bound",
    "missing_listing",
    "playlist_id",
    "resolve",
]
