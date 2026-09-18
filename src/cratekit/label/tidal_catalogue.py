"""The streaming provider's catalogue, behind the label package's seam.

**THIN ON PURPOSE.** Every read here is one question to the provider client
that ``acquire.provider_session.client_session`` logged in, and every PAGED read
goes through ``acquire.listing``. That module's docstring is the argument: a
listing that quietly returns one page looks exactly like a short one, and a
paging loop written here would be the fourth copy of that defect. A guard in the
suite scans this file for a direct paging call.

**IT IS NOT THE DOWNLOADER.** The vendored tool also holds a logged in client,
and reaching through it would have been shorter. It was rejected because the
tool is a downloader and this seam is a catalogue, so nothing here imports
``cratekit._vendor``, and a guard in the suite says so.

**THE FAILURE CONTRACT IS ``Catalogue``'s, AND EVERY RAISE HERE SERVES IT.**
:meth:`TidalCatalogue.artist_for` and :meth:`TidalCatalogue.playlist_for` raise a
named ``LookupError`` or ``ValueError`` for something the provider cannot
resolve and never return ``None``. None of those is a ``CratekitError``, which
is deliberate: the callers turn a foreign exception into their own refusal
(``label-playlist-unreadable``, ``sync-source-lookups-failed``) and pass a
``CratekitError`` through untouched, so raising one of the product's own causes
here would skip the boundary that names the playlist or the label.

Layer: modules.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

# Imported at module top rather than deferred, because ``catalogue.bound`` asks
# whether THIS module imports, and the answer has to include the client library.
import tidalapi

from cratekit.acquire import listing, provider_session
from cratekit.label import harvest, registry
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import AccountPlaylist

#: A provider playlist identifier. The provider mints playlists as UUIDs, so a
#: reference that is not one cannot name a playlist and is refused before a
#: request is spent on it.
_UUID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE
)

#: Hosts a playlist URL or a share link is read from. A share link is the same
#: URL with a query string on it, so it needs no host of its own.
PLAYLIST_HOSTS = frozenset({"tidal.com", "www.tidal.com", "listen.tidal.com"})

#: The short link host. Its path is an opaque code that only the provider can
#: expand, so it is refused BY NAME rather than followed: following it is a
#: network redirect this parser would have to trust.
SHORT_LINK_HOST = "link.tidal.com"

#: How many search hits one name lookup reads. The provider serves at most 300
#: and ranks exact names first, so the first page is where an exact match is.
SEARCH_LIMIT = 50

#: A seed recorded as a provider identifier rather than a name. The digits
#: after the prefix are what ``session.artist`` is called with. Anything else
#: is still a name, resolved by exact fold.
_ID_SEED = re.compile(r"^id:(\d+)$")

#: What every verdict this adapter returns names as its source.
SOURCE = "catalogue"


class PlaylistReferenceInvalid(ValueError):
    """A reference that is not a playlist URL, a share link, or an identifier."""


class PlaylistUnresolvable(LookupError):
    """A well formed playlist reference the provider could not resolve."""


class LabelUnresolvable(LookupError):
    """A favourite label none of whose names, or one of whose seeds, resolved.

    Also raised for a name more than one provider artist carries exactly, since
    picking one of them is a guess.
    """


def playlist_id(reference: str) -> str:
    """The playlist identifier inside what a person typed, or a named refusal.

    THREE SHAPES AND NO FOURTH: a bare identifier, a full URL on a provider host
    whose path ends ``playlist/<id>``, and a share link, which is that URL with a
    query string. Anything else is refused rather than searched for, because a
    guess that lands on a different playlist would list someone else's tracks
    under the one the person named.
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
        if (
            len(segments) >= 2
            and segments[-2] == "playlist"
            and _UUID.fullmatch(segments[-1])
        ):
            return segments[-1].lower()
    raise PlaylistReferenceInvalid(
        f"{reference!r} is not a playlist URL, a share link, or a playlist "
        f"identifier"
    )


class LabelRoster:
    """Every artist a favourite label resolved to, listed as one artist object.

    ``Catalogue.artist_for`` hands ``crawl.releases`` ONE object, and a label on
    the provider is a roster: the label's own artist page when it has one, plus
    the seed artists the registry names. This presents the roster in the shape
    ``listing.artist_releases`` pages.

    THE LISTING HAPPENS HERE, ONCE, AT CONSTRUCTION, and the two methods serve
    slices of what it read. Listing lazily inside a method the crawl pages would
    run a whole retry ladder inside each attempt of the crawl's own ladder, so
    one failure that does not clear would be retried dozens of times and every
    retry would list every artist from the start. Built eagerly, a failure
    raises out of ``artist_for``, which is where a sweep already turns a foreign
    exception into its refusal, and the crawl pages memory that cannot fail.
    """

    def __init__(self, artists: list[Any]) -> None:
        self.artists = list(artists)
        self._listed = {method: self._list(method) for method in listing.RELEASE_METHODS}

    def _list(self, method: str) -> list[Any]:
        """Every artist's releases for one listing, concatenated.

        NOT DEDUPLICATED HERE. ``listing.artist_releases`` deduplicates by
        identifier when the crawl pages this roster, and the copy that used to sit
        here killed no test in U62's mutation table because that one always ran
        after it. One place decides what a repeat is.
        """
        held: list[Any] = []
        for artist in self.artists:
            held.extend(listing.artist_releases(artist, methods=(method,)))
        return held

    def get_albums(self, limit: int, offset: int = 0) -> list[Any]:
        return self._listed["get_albums"][offset : offset + limit]

    def get_ep_singles(self, limit: int, offset: int = 0) -> list[Any]:
        return self._listed["get_ep_singles"][offset : offset + limit]


def _results(found: Any, key: str) -> list[Any]:
    """One model's hits out of a search answer, whatever container it came in."""
    if isinstance(found, Mapping):
        return list(found.get(key) or [])
    return list(getattr(found, key, None) or [])


def _copyright_label(release: Any) -> str:
    """The label a release's copyright line credits, by harvest's one extractor."""
    names = harvest.labels_from_copyright(release)
    return names[0] if names else ""


def seed_identifier(seed: str) -> str | None:
    """The provider artist id inside an ``id:<digits>`` seed, else ``None``."""
    matched = _ID_SEED.fullmatch(str(seed or "").strip())
    return matched.group(1) if matched else None


class TidalCatalogue:
    """The five provider reads the ``Catalogue`` seam declares, over one logged in client."""

    def __init__(self, session: Any) -> None:
        self._session = session

    def _artist_named(self, name: str) -> Any | None:
        """The one artist whose name folds to exactly ``name``, or ``None``.

        ``None`` is private to this class and never leaves it: the public method
        turns it into a raise. Exact rather than first hit, because a search for
        a label name ranks similarly named acts beside it and crawling one of
        those would offer another label's releases.

        TWO EXACT MATCHES RAISE rather than take the first. The provider carries
        unrelated acts under one name, and crawling the wrong one verifies no
        release and reports a label with nothing new, which is R-135 again. A
        name seed still refuses on that collision. An ``id:<digits>`` seed pins
        one of them by identifier and does not search.
        """
        wanted = label_verify.fold_label(name)
        if not wanted:
            return None
        found = self._session.search(
            name, models=[tidalapi.artist.Artist], limit=SEARCH_LIMIT
        )
        exact = [
            artist
            for artist in _results(found, "artists")
            if label_verify.fold_label(str(getattr(artist, "name", "") or "")) == wanted
        ]
        distinct = {str(getattr(artist, "id", "") or id(artist)) for artist in exact}
        if len(distinct) > 1:
            raise LabelUnresolvable(
                f"{len(distinct)} provider artists are named exactly {name!r}, and "
                f"crawling the wrong one would offer another act's releases"
            )
        return exact[0] if exact else None

    def _artist_identified(self, artist_id: str) -> Any | None:
        """The artist ``session.artist`` returns for ``artist_id``, or ``None``.

        ``None`` is private, the same contract as ``_artist_named``. A missing
        identifier is an unresolved seed. A provider outage is not, and
        propagates rather than being read as absence.
        """
        try:
            artist = self._session.artist(artist_id)
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:
            # Bare LookupError is the fake's not found. KeyError and IndexError
            # are subclasses, and those are parse failures, not a missing id.
            if type(exc) is not LookupError:
                raise
            return None
        return artist or None

    def _artist_from_seed(self, seed: str) -> Any | None:
        """Resolve one registry seed, by identifier when it is one, else by name."""
        identifier = seed_identifier(seed)
        if identifier is not None:
            return self._artist_identified(identifier)
        return self._artist_named(seed)

    def artist_for(self, entry: registry.LabelEntry) -> LabelRoster:
        """The label's roster: its own artist page if one exists, and every seed.

        A SEED THAT DOES NOT RESOLVE REFUSES THE LABEL rather than narrowing the
        crawl in silence. A sweep over four of five seeds reports that it looked
        and offers less than the label released, which is the R-135 reading this
        contract exists to stop. The label's own page is optional because most
        labels have none, and a label with seeds is fully described by them.
        """
        artists: list[Any] = []
        own = self._artist_named(entry.name)
        if own is not None:
            artists.append(own)
        unresolved: list[str] = []
        for seed in entry.seed_artists:
            artist = self._artist_from_seed(seed)
            if artist is None:
                unresolved.append(seed)
            else:
                artists.append(artist)
        if unresolved:
            bits = []
            for seed in unresolved:
                if seed_identifier(seed) is not None:
                    bits.append(f"no artist with identifier {seed!r}")
                else:
                    bits.append(f"no artist named exactly {seed!r}")
            raise LabelUnresolvable(
                f"the provider has {', '.join(bits)}, a seed of the label "
                f"{entry.name!r}"
            )
        if not artists:
            raise LabelUnresolvable(
                f"the provider has no artist named exactly {entry.name!r} and the "
                f"label names no seed artists to crawl instead"
            )
        return LabelRoster(artists)

    def playlist_for(self, reference: str) -> Any:
        """The provider playlist a URL, a share link, or an identifier names."""
        identifier = playlist_id(reference)
        try:
            playlist = self._session.playlist(identifier)
        except Exception as exc:
            raise PlaylistUnresolvable(
                f"the provider could not resolve the playlist {identifier!r} ({exc})"
            ) from exc
        if playlist is None:
            raise PlaylistUnresolvable(
                f"the provider returned nothing for the playlist {identifier!r}"
            )
        return playlist

    def search_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Who the release's copyright line credits, for ``verify_release`` to judge.

        The listed object usually carries the line already. When it does not, the
        release is read again by identifier rather than judged unconfirmed on a
        field the listing happened to omit, which would drop a real release.
        """
        del claimed  # the judgement is verify_release's, not this read's
        resolved = _copyright_label(release)
        identity = str(getattr(release, "id", "") or "")
        if not resolved and identity:
            resolved = _copyright_label(self._session.album(identity))
        return {"resolved_label": resolved, "source": SOURCE}

    def check_label(self, name: str) -> dict:
        """Whether any release the provider finds for ``name`` credits it.

        CONFIRMED ONLY ON A COPYRIGHT LINE THAT MATCHES, by the same
        ``labels_match`` rule a sweep verifies a release with. A search hit alone
        confirms nothing, because the provider answers every query with its
        nearest titles whether or not any of them is on that label.
        """
        found = self._session.search(
            name, models=[tidalapi.album.Album], limit=SEARCH_LIMIT
        )
        for album in _results(found, "albums"):
            resolved = _copyright_label(album)
            if resolved and label_verify.labels_match(name, resolved):
                return {"verdict": "confirmed", "resolved_label": resolved, "source": SOURCE}
        return {
            "verdict": "unconfirmed",
            "resolved_label": "",
            "source": SOURCE,
            "notes": "no release found crediting this label",
        }

    def account_playlists(self) -> tuple[AccountPlaylist, ...]:
        """The playlists the logged in user created, paged through the listing.

        OWN ONLY, BY CREATOR IDENTIFIER. The provider's only paged listing mixes
        the account's playlists with the ones it follows, and sweeping a followed
        editorial playlist would queue somebody else's selection. A client that
        cannot say who is logged in is REFUSED rather than read as owning
        nothing, because an empty answer here is a clean sweep of an account
        nobody looked at.
        """
        user = getattr(self._session, "user", None)
        user_id = str(getattr(user, "id", "") or "")
        if not user_id:
            raise LookupError(
                "the provider client did not say which account is logged in, so "
                "its own playlists cannot be told from the ones it follows"
            )
        own: list[AccountPlaylist] = []
        for playlist in listing.account_playlists(self._session):
            creator = str(getattr(getattr(playlist, "creator", None), "id", "") or "")
            identity = str(getattr(playlist, "id", "") or "")
            if creator != user_id or not identity:
                continue
            count = getattr(playlist, "num_tracks", None)
            own.append(
                AccountPlaylist(
                    playlist_id=identity,
                    name=str(getattr(playlist, "name", "") or ""),
                    tracks=count if isinstance(count, int) and not isinstance(count, bool) else None,
                )
            )
        return tuple(own)


def open_catalogue() -> TidalCatalogue:
    """A catalogue over a freshly logged in client, from the stored session."""
    return TidalCatalogue(provider_session.client_session())


__all__ = [
    "PLAYLIST_HOSTS",
    "SHORT_LINK_HOST",
    "LabelRoster",
    "LabelUnresolvable",
    "PlaylistReferenceInvalid",
    "PlaylistUnresolvable",
    "TidalCatalogue",
    "open_catalogue",
    "playlist_id",
]
