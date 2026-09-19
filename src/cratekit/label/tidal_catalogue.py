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
import time
from collections import deque
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

# Imported at module top rather than deferred, because ``catalogue.bound`` asks
# whether THIS module imports, and the answer has to include the client library.
import tidalapi

from cratekit.acquire import listing, provider_session
from cratekit.core.cause import CratekitError
from cratekit.label import harvest, registry
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import (
    TRACK_SEARCH_PAGE,
    AccountPlaylist,
    HeartsShortfall,
    ReleaseUnresolvable,
    Unread,
    missing_listing,
)

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

#: Numbered compilation titles the source system searched for, ``001`` through
#: ``079``. Discovery issues one album search per value, plus the bare name.
COMPILATION_RANGE = range(1, 80)

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
    picking one of them is a guess. Discovery that finds no credited artist is
    the same refusal, with a message that names that search found nothing.
    """


#: What the retry ladder waits with, read off the module AT CALL TIME. The
#: ladder's own default is bound when that function is defined, so a suite
#: could not otherwise drive a retry here without sleeping for real.
_pause = time.sleep

#: What the album read returns for a release that is gone, so the retry ladder
#: sees an answer rather than an exception it would climb on.
_GONE = object()


def _gone(exc: BaseException) -> bool:
    """Whether a failure is the provider saying the release does not exist.

    BY CLASS NAME OR BY STATUS, AND NEVER BY THE TEXT. The acquisition adapter's
    classifier also reads "404" and "not found" out of the message, which is
    right for a downloader's output and wrong here: the client's HTTP errors
    carry the request URL, the URL carries the release identifier, and an
    identifier such as 24040417 holds the digits 404. A rejected session on that
    release would then be answered once, as gone, and a person would be told to
    revoke an acceptance over a login problem. A release that is gone is
    PERMANENT and is never retried, because R-380 is what the other order costs.
    """
    if "notfound" in type(exc).__name__.lower():
        return True
    return getattr(getattr(exc, "response", None), "status_code", None) == 404


def _year(release: Any) -> int | None:
    """The year the provider dates a release, or ``None``. Never a guess.

    ``year`` first, then the year of ``release_date``, which the client parses
    to a date and an older payload carries as text. A boolean is not a year,
    and neither is a number outside four digits.
    """
    for held in (getattr(release, "year", None), getattr(release, "release_date", None)):
        if held is None or isinstance(held, bool):
            continue
        found = getattr(held, "year", held)
        if isinstance(found, bool):
            continue
        if isinstance(found, int):
            if 1000 <= found <= 9999:
                return found
            continue
        text = str(found).strip()[:4]
        if len(text) == 4 and text.isdigit() and int(text) >= 1000:
            return int(text)
    return None


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
    the seed artists the registry names, plus artists discovery found by album
    search and a credited artist walk. This presents the roster in the shape
    ``listing.artist_releases`` pages.

    THE LISTING HAPPENS HERE, ONCE, AT CONSTRUCTION, and the two methods serve
    slices of what it read. Listing lazily inside a method the crawl pages would
    run a whole retry ladder inside each attempt of the crawl's own ladder, so
    one failure that does not clear would be retried dozens of times and every
    retry would list every artist from the start. Built eagerly, a failure
    raises out of ``artist_for``, which is where a sweep already turns a foreign
    exception into its refusal, and the crawl pages memory that cannot fail.

    THE ROSTER ALWAYS EXPOSES BOTH LISTINGS, so the crawl paging it can never
    see a member that lacks one. ``unread`` is where that fact goes instead:
    what discovery could not read, handed in, plus every member whose client
    object lacks a listing, found here. The sweep reads it (R-261, R-393).
    """

    def __init__(self, artists: list[Any], unread: tuple[Unread, ...] = ()) -> None:
        self.artists = list(artists)
        missing: list[Unread] = []
        self._listed = {
            method: self._list(method, missing) for method in listing.RELEASE_METHODS
        }
        self.unread = (*unread, *missing)

    def _list(self, method: str, missing: list[Unread]) -> list[Any]:
        """Every artist's releases for one listing, concatenated.

        NOT DEDUPLICATED HERE. ``listing.artist_releases`` deduplicates by
        identifier when the crawl pages this roster, and the copy that used to sit
        here killed no test in U62's mutation table because that one always ran
        after it. One place decides what a repeat is.

        A member without ``method`` is skipped by the wrapper and recorded in
        ``missing``.
        """
        held: list[Any] = []
        for artist in self.artists:
            skipped: list[str] = []
            held.extend(listing.artist_releases(artist, methods=(method,), skipped=skipped))
            missing.extend(missing_listing(artist, name) for name in skipped)
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


def album_search_queries(name: str) -> tuple[str, ...]:
    """The album searches discovery issues for one label.

    The bare name, then each numbered compilation in :data:`COMPILATION_RANGE`.
    Single shot each, not a page loop. The range is the source system's numbered
    compilation titles, ``001`` through ``079``.
    """
    return (name, *(f"{name} {number:03d}" for number in COMPILATION_RANGE))


def _credits_label(release: Any, needle: str) -> bool:
    """Whether harvest's copyright extractor names this label on ``release``."""
    return any(
        label_verify.labels_match(needle, name)
        for name in harvest.labels_from_copyright(release)
    )


def _credited_ids(release: Any) -> tuple[str, ...]:
    """Provider artist ids credited on one album, skipping blanks."""
    held: list[str] = []
    for artist in getattr(release, "artists", None) or ():
        identity = str(getattr(artist, "id", "") or "")
        if identity:
            held.append(identity)
    return tuple(held)


class TidalCatalogue:
    """The seven provider reads the ``Catalogue`` seam declares, over one logged in client."""

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

    def _discover(
        self, entry: registry.LabelEntry, held: list[Any], unread: list[Unread]
    ) -> list[Any]:
        """Artists album search plus a credited artist walk add to the roster.

        Runs even when ``held`` is already non empty, because an incomplete
        seed list is the silent shortfall, not only an empty roster. A listing
        failure on one artist skips that artist. A session dead failure, a
        ``CratekitError``, still refuses the label.

        THE SKIP IS RECORDED IN ``unread``, and the listing climbs the retry
        ladder first (R-393). A live 429 is ``TooManyRequests``, not a
        ``CratekitError``, so before this it skipped the artist in silence and
        the roster read as complete. The ladder waits with :data:`_pause`, so
        a suite can drive it without sleeping 31 seconds for real.
        """
        needle = entry.match or entry.name
        seen: set[str] = set()
        queue: deque[str] = deque()

        def enqueue(artist_id: str) -> None:
            if artist_id and artist_id not in seen:
                seen.add(artist_id)
                queue.append(artist_id)

        for query in album_search_queries(entry.name):
            try:
                found = self._session.search(
                    query, models=[tidalapi.album.Album], limit=SEARCH_LIMIT
                )
            except CratekitError:
                raise
            except tidalapi.exceptions.AuthenticationError:
                raise
            except Exception:  # noqa: BLE001 - one query, not the session
                continue
            for album in _results(found, "albums"):
                if _credits_label(album, needle):
                    for identity in _credited_ids(album):
                        enqueue(identity)

        discovered: list[Any] = []
        held_ids = {str(getattr(artist, "id", "") or "") for artist in held}
        held_ids.discard("")
        while queue:
            artist_id = queue.popleft()
            artist = self._artist_identified(artist_id)
            if artist is None:
                continue
            try:
                releases = listing.artist_releases(artist, sleep=_pause)
            except CratekitError:
                raise
            except Exception as exc:  # noqa: BLE001 - one artist's listing, not the session
                # A HELD ARTIST IS NOT RECORDED. The roster lists every held
                # artist again when it is built, and that read is the one the
                # crawl uses: it succeeds and this record would be stale, or it
                # fails and refuses the label. Only an artist discovery alone
                # would have added is lost here.
                if str(getattr(artist, "id", "") or artist_id) in held_ids:
                    continue
                unread.append(
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
                        listing="artist_releases",
                        reason=f"{type(exc).__name__}: {exc}",
                        # A listing that cannot page, or ran out of pages, reads
                        # the same way on every attempt; ``fetch_with_retry``
                        # skips its ladder for the first on that argument.
                        transient=not isinstance(
                            exc, (listing.ListingNotPaginated, listing.ListingTruncated)
                        ),
                    )
                )
                continue
            for release in releases:
                if _credits_label(release, needle):
                    for identity in _credited_ids(release):
                        enqueue(identity)
            identity = str(getattr(artist, "id", "") or artist_id)
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)
        return discovered

    def artist_for(self, entry: registry.LabelEntry) -> LabelRoster:
        """The label's roster: own page, every seed, then discovery.

        A SEED THAT DOES NOT RESOLVE REFUSES THE LABEL rather than narrowing the
        crawl in silence, and refuses before discovery runs, so an unresolved
        seed is not rescued by albums the search would have found. A sweep over
        four of five seeds reports that it looked and offers less than the label
        released, which is the R-135 reading this contract exists to stop. The
        label's own page is optional because most labels have none. Discovery
        still runs when the roster already has members, because the silent
        shortfall is an incomplete seed list, not only an empty roster.
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
        unread: list[Unread] = []
        artists.extend(self._discover(entry, artists, unread))
        if not artists:
            raise LabelUnresolvable(
                f"the provider has no artist named exactly {entry.name!r}, the "
                f"label names no seed artists, and discovery found nothing"
            )
        return LabelRoster(artists, tuple(unread))

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

    def favourite_tracks(self) -> tuple[Any, ...]:
        """The account's hearted tracks, through the one favourites listing.

        ``listing.favorite_tracks_declared`` ends on the provider's declared
        count and raises ``ListingTruncated`` rather than returning what it
        collected. ENDING ON THE COUNT IS NOT REACHING IT (R-504): the provider
        leaves the hearts it will not serve out of every page while counting
        them, so the rows are compared with the count here and a shortfall
        raises :class:`HeartsShortfall` with the rows it did serve. A count the
        provider did not publish leaves nothing to compare, and the rows are
        returned as the walk found them. A client that cannot say who is
        logged in is REFUSED rather than read as an account with no hearts, for
        the reason :meth:`account_playlists` gives.
        """
        user = getattr(self._session, "user", None)
        if getattr(user, "favorites", None) is None:
            raise LookupError(
                "the provider client did not expose the logged in account's "
                "favourites, so its hearts cannot be listed"
            )
        rows, declared = listing.favorite_tracks_declared(self._session)
        if declared is not None and len(rows) < declared:
            raise HeartsShortfall(rows, declared)
        return tuple(rows)

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None]:
        """One release read again by identifier: its tracks, and its year.

        TWO READS, AND BOTH CLIMB THE ONE LADDER. The album itself goes through
        ``listing.fetch_with_retry`` so a rate limit on the ninetieth release of
        a long approval waits rather than failing it, and the tracks go through
        ``listing.playlist_tracks``, because an album pages its tracks exactly
        as a playlist does and counts the ones it will not serve the same way.
        That wrapper stops on the declared count, so a short window is never
        read as the end of the release.

        A RELEASE THAT IS GONE IS ANSWERED ONCE. See :class:`ReleaseUnresolvable`.
        Every other failure is re-raised as the provider raised it once the
        ladder is spent, and the caller names the release it belongs to.
        """
        identity = str(release_id or "").strip()
        if not identity:
            raise ReleaseUnresolvable("no release identifier was given to read")

        def attempt(limit: int, offset: int) -> Any:
            del limit, offset
            try:
                return self._session.album(identity)
            except Exception as exc:
                if _gone(exc):
                    return _GONE
                raise

        album = listing.fetch_with_retry(attempt, limit=0, offset=0, sleep=_pause)
        if album is _GONE or album is None:
            raise ReleaseUnresolvable(
                f"the provider has no release {identity!r}; it was withdrawn or "
                f"the identifier was never a release"
            )
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
        return tuple(tracks), _year(album)

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        """The provider's tracks for one ISRC, on the one retry ladder.

        ONLY A NOT FOUND IS AN ANSWER. The client answers an ISRC it files no
        track under by raising ``ObjectNotFound``, and that is returned as the
        empty tuple, once and never retried. Everything else climbs the ladder
        and is re-raised, INCLUDING ``InvalidISRC``: at 0.8.11 the client folds
        every HTTP error except 404 and 429 into that one class, a server error
        and a rejected session among them, so reading it as "no track" would
        read an outage as an answer. A malformed code is the caller's to keep
        from asking, and ``intake.missing_cli`` checks the shape first.
        """
        wanted = str(isrc or "").strip()
        if not wanted:
            raise ValueError("no ISRC was given to look up")
        lookup = getattr(self._session, "get_tracks_by_isrc", None)
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")

        def attempt(limit: int, offset: int) -> tuple[Any, ...]:
            del limit, offset
            try:
                return tuple(lookup(wanted) or ())
            except Exception as exc:
                if _gone(exc):
                    return ()
                raise

        return listing.fetch_with_retry(attempt, limit=0, offset=0, sleep=_pause)

    def search_tracks(self, artist: str, title: str) -> tuple[Any, ...]:
        """One track search for ``artist`` and ``title``, on the one retry ladder.

        NOTHING IS CHOSEN HERE. The hits come back in the provider's order,
        every one of them, and ``intake.candidates`` decides what is exact and
        offers the rest to a person. One page of ``TRACK_SEARCH_PAGE``, because a
        candidate list is read by a person and the caller truncates it again.
        The seam's own page, so the caller can tell a full answer from a short one.

        A search that fails climbs the ladder and is re-raised, a not found
        among it: a search endpoint answers nothing found with an empty list,
        so a raised not found is the endpoint failing and never an answer. An
        answer with no ``tracks`` container at all is an empty answer only when
        the container is there and empty. One that is absent is a shape this
        adapter does not know and is raised, because read as empty it would
        report a track the provider carries as having no candidate.
        """
        query = " ".join(part for part in (str(artist or "").strip(), str(title or "").strip()) if part)
        if not query:
            raise ValueError("no artist and no title were given to search for")

        def attempt(limit: int, offset: int) -> Any:
            del offset
            return self._session.search(query, models=[tidalapi.media.Track], limit=limit)

        found = listing.fetch_with_retry(attempt, limit=TRACK_SEARCH_PAGE, offset=0, sleep=_pause)
        # AFTER THE LADDER, because waiting cannot change a shape.
        present = "tracks" in found if isinstance(found, Mapping) else hasattr(found, "tracks")
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
        return tuple(_results(found, "tracks"))


def open_catalogue() -> TidalCatalogue:
    """A catalogue over a freshly logged in client, from the stored session."""
    return TidalCatalogue(provider_session.client_session())


__all__ = [
    "COMPILATION_RANGE",
    "PLAYLIST_HOSTS",
    "SHORT_LINK_HOST",
    "LabelRoster",
    "LabelUnresolvable",
    "PlaylistReferenceInvalid",
    "PlaylistUnresolvable",
    "ReleaseUnresolvable",
    "TidalCatalogue",
    "album_search_queries",
    "open_catalogue",
    "playlist_id",
]
