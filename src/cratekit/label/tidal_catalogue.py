"""The streaming provider's catalogue, behind the label package's seam.

Thin on purpose: every read is one question to the client
``acquire.provider_session.session_for`` holds for the process, and every paged
read goes through ``acquire.listing``, since a listing that quietly returns one
page looks exactly like a short one. A guard scans this file for a direct
paging call. Nothing here imports ``cratekit._vendor``, the downloader.

ISRC lookups go under the app client when one is set up (U205); every other
read stays on the account session. The account's own playlists, hearts and
playlists by reference are the account's business, and the label crawl stays
there until a unit probes the official API's cursor paging, which differs from
the limit and offset paging ``acquire.listing`` stops on a declared count with.

The failure contract is ``Catalogue``'s: :meth:`TidalCatalogue.artist_for` and
:meth:`TidalCatalogue.playlist_for` raise a named ``LookupError`` or
``ValueError``, never a ``CratekitError``, so the callers' boundaries name the
playlist or the label in their own refusals.

Layer: modules.
"""

from __future__ import annotations

import re
import time
from collections import deque
from collections.abc import Callable, Iterable, Mapping
from typing import Any

# Imported at module top, since ``catalogue.bound`` asks whether this module
# imports, client library included.
import tidalapi

from cratekit.acquire import catalogue_api, isrc_cache, isrc_screen, listing, provider_session
from cratekit.core.cause import CratekitError, answered_not_found
from cratekit.label import harvest, kept_listing, registry
from cratekit.label import verify as label_verify
from cratekit.label.catalogue import (
    PLAYLIST_HOSTS,
    RELEASE_GONE,
    SHORT_LINK_HOST,
    TRACK_SEARCH_PAGE,
    AccountPlaylist,
    HeartsShortfall,
    ListingShortfall,
    PlaylistReferenceInvalid,
    ReleaseRead,
    ReleaseUnresolvable,
    Unread,
    artist_name,
    missing_listing,
    playlist_id,
)

#: How many search hits one name lookup reads; exact names rank first.
SEARCH_LIMIT = 50

#: Numbered compilation titles the source system searched for, ``001`` through
#: ``079``, one album search each plus the bare name.
COMPILATION_RANGE = range(1, 80)

#: A seed recorded as a provider identifier; anything else is a name.
_ID_SEED = re.compile(r"^id:(\d+)$")

#: What every verdict this adapter returns names as its source.
SOURCE = "catalogue"


def _unanswered(verdict: str, notes: str) -> dict[str, str]:
    """A verdict that names no label, from this adapter."""
    return {"verdict": verdict, "resolved_label": "", "source": SOURCE, "notes": notes}


class PlaylistUnresolvable(LookupError):
    """A well formed playlist reference the provider could not resolve."""


class LabelUnresolvable(LookupError):
    """A favourite label none of whose names, or one of whose seeds, resolved.

    Also raised for a name two provider artists carry exactly, and for discovery
    that finds no credited artist.
    """


#: What the retry ladder waits with, read off the module at call time so a
#: suite can drive a retry without sleeping.
_pause = time.sleep

#: What the album read returns for a gone release, an answer the ladder does
#: not climb on.
_GONE = object()


def _gone(exc: BaseException) -> bool:
    """Whether a failure is the provider saying the release does not exist.

    By class name or by the status nearest the failure (R-1313), never by the
    text: a URL carrying an identifier such as 24040417 holds the digits 404, and
    a rejected session would read as gone. Gone is permanent and never retried
    (R-380).
    """
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)


def _year(release: Any) -> int | None:
    """The year the provider dates a release, or ``None``. Never a guess.

    ``year`` first, then ``release_date``'s, a date or older text. A boolean is
    not a year, nor is a number outside four digits.
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


class LabelRoster(listing.HeldReleases):
    """Every artist a favourite label resolved to, listed as one artist object.

    A label on the provider is a roster: its own page, the registry's seeds and
    what discovery found. Listed once, at construction, so a failure raises out
    of ``artist_for`` rather than inside the crawl's own retry ladder. Read whole
    as a ``listing.HeldReleases``, never paged under one artist's budget (R-888).

    ``unread`` is what discovery could not read plus every member lacking a
    listing (R-261, R-393). ``lister`` reads one member's listing of one method,
    from the label's kept listing first (U217); ``kept`` is what the build made
    of that store.
    """

    def __init__(
        self,
        artists: list[Any],
        unread: tuple[Unread, ...] = (),
        *,
        lister: Callable[[Any, str, list[Unread]], list[Any]] | None = None,
    ) -> None:
        self.artists = list(artists)
        self._lister = lister if lister is not None else _listed_now
        missing: list[Unread] = []
        self._listed = {
            method: self._list(method, missing) for method in listing.RELEASE_METHODS
        }
        self.unread = (*unread, *missing)
        self.kept: kept_listing.Summary | None = None

    def _list(self, method: str, missing: list[Unread]) -> list[Any]:
        """Every artist's releases for one listing, concatenated.

        Not deduplicated: ``listing.artist_releases`` does that when the crawl reads
        the roster. A member without ``method`` is recorded in ``missing``.
        """
        held: list[Any] = []
        for artist in self.artists:
            held.extend(self._lister(artist, method, missing))
        return held

    def held(self, method: str) -> list[Any] | None:
        return self._listed.get(method)


def _listed_now(artist: Any, method: str, missing: list[Unread]) -> list[Any]:
    """One artist's listing of one method, asked of the provider now."""
    skipped: list[str] = []
    rows = listing.artist_releases(artist, methods=(method,), skipped=skipped, sleep=_pause)
    missing.extend(missing_listing(artist, name) for name in skipped)
    return rows


class _Member:
    """A roster artist a kept answer named, read from the provider only when needed.

    A kept resolution gives an identifier and a name; the provider object is read
    once, the first time a listing that is not kept needs it (U217).
    """

    __slots__ = ("_object", "_read", "id", "name")

    def __init__(self, identity: str, name: str, read: Callable[[str], Any]) -> None:
        self.id = identity
        self.name = name
        self._object: Any = None
        self._read: Callable[[str], Any] | None = read

    @property
    def read_yet(self) -> bool:
        """Whether the provider object was read, or never needs to be."""
        return self._read is None

    def provider_object(self) -> Any | None:
        """The provider's artist, read now if it was not yet, ``None`` once it is gone."""
        if self._read is not None:
            read, self._read = self._read, None
            self._object = read(self.id)
        return self._object


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
    credited = getattr(release, "artists", None) or ()
    ids = (str(getattr(artist, "id", "") or "") for artist in credited)
    return tuple(identity for identity in ids if identity)


class TidalCatalogue:
    """Every provider read the ``Catalogue`` seam declares, over one logged in client."""

    def __init__(
        self, session: Any, *, catalogue: Any = None, cache: isrc_cache.Cache | None = None
    ) -> None:
        self._session = session
        #: Where ISRC lookups go: the app client when the opener built one
        #: (U205), else the account session, exactly as before.
        self._lookups = catalogue if catalogue is not None else session
        #: The codes a batch answered as filed under nothing (U207).
        self._screen = isrc_screen.Screen()
        #: The count the last hearts listing published, None when it published none.
        self.hearts_declared: int | None = None
        #: What the provider already answered for an ISRC (U206).
        self._cache = cache if cache is not None else isrc_cache.Cache()

    def _artist_named(self, name: str) -> Any | None:
        """The one artist whose name folds to exactly ``name``, or ``None``.

        ``None`` never leaves this class. Exact rather than first hit, since a search
        ranks similarly named acts beside it. Two exact matches raise, since crawling
        the wrong act reports a label with nothing new (R-135); an ``id:`` seed pins
        one without searching.
        """
        wanted = label_verify.fold_label(name)
        if not wanted:
            return None
        found = self._session.search(name, models=[tidalapi.artist.Artist], limit=SEARCH_LIMIT)
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

        A missing identifier is an unresolved seed; an outage propagates.
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

    def _artist_from_seed(self, seed: str, kept: kept_listing.KeptListing) -> Any | None:
        """Resolve one registry seed, by identifier when it is one, else by name."""
        identifier = seed_identifier(seed)
        if identifier is not None:
            return self._member_identified(identifier, kept, need_object=False)
        return self._member_named(seed, kept)

    def _member_named(self, name: str, kept: kept_listing.KeptListing) -> Any | None:
        """:meth:`_artist_named`, answered from the kept listing when it holds the name.

        Two exact matches still raise and are never kept.
        """
        held = kept.named(name)
        if held is not None:
            if not held:
                return None
            ((identity, said),) = held
            return _Member(identity, said, self._artist_identified)
        if not label_verify.fold_label(name):
            return None
        artist = self._artist_named(name)
        if artist is None:
            kept.keep_named(name, ())
            return None
        identity = str(getattr(artist, "id", "") or "")
        if identity:
            kept.keep_named(name, ((identity, str(getattr(artist, "name", "") or "")),))
        else:
            # NO IDENTIFIER TO KEY ITS LISTINGS BY, so nothing about it is kept.
            kept.asked_unkept()
        return artist

    def _member_identified(
        self, artist_id: str, kept: kept_listing.KeptListing, *, need_object: bool
    ) -> Any | None:
        """:meth:`_artist_identified`, answered from the kept listing when it can be.

        A kept artist answers a :class:`_Member` that reads the provider object only
        when needed, unless ``need_object`` asks for it now, as discovery does.
        """
        held = kept.identified(artist_id)
        if held is not None:
            found, name = held
            if not found:
                return None
            if not need_object:
                return _Member(artist_id, name, self._artist_identified)
        artist = self._artist_identified(artist_id)
        kept.keep_identified(
            artist_id,
            found=artist is not None,
            name=str(getattr(artist, "name", "") or "") if artist is not None else "",
        )
        return artist

    def _credited_by(self, query: str, needle: str, kept: kept_listing.KeptListing) -> tuple[str, ...]:
        """The artists one discovery album search credits beside the label, kept or asked.

        A search that fails skips its query and is not kept.
        """
        held = kept.searched(query)
        if held is not None:
            return held
        try:
            found = self._session.search(query, models=[tidalapi.album.Album], limit=SEARCH_LIMIT)
        except CratekitError:
            raise
        except tidalapi.exceptions.AuthenticationError:
            raise
        except Exception:  # noqa: BLE001 - one query, not the session
            kept.asked_unkept()
            return ()
        credited = tuple(
            identity
            for album in _results(found, "albums")
            if _credits_label(album, needle)
            for identity in _credited_ids(album)
        )
        kept.keep_searched(query, credited)
        return credited

    def _listed(
        self, kept: kept_listing.KeptListing, artist: Any, method: str, missing: list[Unread]
    ) -> list[Any]:
        """One member's listing of one method, from the kept listing or asked and kept.

        Kept only whole: a failure raises before anything is kept, a missing method
        is recorded in ``missing``, and an artist with no identifier is not kept.
        """
        identity = str(getattr(artist, "id", "") or "")
        if identity:
            held = kept.listed(identity, method)
            if held is not None:
                return list(held)
        if isinstance(artist, _Member):
            if not artist.read_yet:
                # The read of the object is a call, and counted (U217).
                kept.asked_unkept()
            target = artist.provider_object()
        else:
            target = artist
        if target is None:
            # A kept artist the provider no longer has: unread rather than empty.
            missing.append(
                Unread(
                    artist=str(getattr(artist, "name", "") or identity),
                    listing=method,
                    reason="the provider no longer has this artist",
                    transient=False,
                )
            )
            return []
        skipped: list[str] = []
        rows = listing.artist_releases(target, methods=(method,), skipped=skipped, sleep=_pause)
        missing.extend(missing_listing(target, name) for name in skipped)
        if skipped:
            return rows
        if identity:
            kept.keep_listed(identity, method, rows)
        else:
            kept.asked_unkept()
        return rows

    def _discover(
        self,
        entry: registry.LabelEntry,
        held: list[Any],
        unread: list[Unread],
        kept: kept_listing.KeptListing,
    ) -> list[Any]:
        """Artists album search plus a credited artist walk add to the roster.

        Runs even with a non empty roster, since an incomplete seed list is the silent
        shortfall. One artist's listing failure, after its retry ladder (R-393), skips
        that artist and is recorded in ``unread``; a ``CratekitError`` refuses.
        """
        needle = entry.match or entry.name
        seen: set[str] = set()
        queue: deque[str] = deque()

        def enqueue(artist_id: str) -> None:
            if artist_id and artist_id not in seen:
                seen.add(artist_id)
                queue.append(artist_id)

        for query in album_search_queries(entry.name):
            for identity in self._credited_by(query, needle, kept):
                enqueue(identity)

        discovered: list[Any] = []
        held_ids = {str(getattr(artist, "id", "") or "") for artist in held}
        held_ids.discard("")
        while queue:
            artist_id = queue.popleft()
            # The object only when a listing of it is not kept, read outside the skip
            # below so a failed read still raises (U217).
            artist = self._member_identified(
                artist_id,
                kept,
                need_object=not all(
                    kept.has_listing(artist_id, method) for method in listing.RELEASE_METHODS
                ),
            )
            if artist is None:
                continue
            try:
                # Both methods, each kept on its own, for the roster to reuse.
                releases = [
                    release
                    for method in listing.RELEASE_METHODS
                    for release in self._listed(kept, artist, method, [])
                ]
            except CratekitError:
                raise
            except Exception as exc:  # noqa: BLE001 - one artist's listing, not the session
                # A held artist is not recorded: the roster lists it again and that read
                # decides. Only an artist discovery alone would add is lost here.
                if str(getattr(artist, "id", "") or artist_id) in held_ids:
                    continue
                unread.append(
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
                        listing="artist_releases",
                        reason=f"{type(exc).__name__}: {exc}",
                        # A listing that cannot page or ran out of pages fails the same way again.
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

        A seed that does not resolve refuses the label before discovery runs, rather
        than narrowing the crawl in silence (R-135). Every answer is asked of the
        label's kept listing first and kept as it goes, flushed whatever stopped the
        build (U217); an unreadable kept listing refuses before any call.
        """
        kept = kept_listing.KeptListing.load(entry)
        try:
            roster = self._roster(entry, kept)
        finally:
            kept.flush()
        roster.kept = kept.summary()
        return roster

    def _roster(self, entry: registry.LabelEntry, kept: kept_listing.KeptListing) -> LabelRoster:
        """:meth:`artist_for`'s roster, every answer through ``kept``."""
        artists: list[Any] = []
        own = self._member_named(entry.name, kept)
        if own is not None:
            artists.append(own)
        unresolved: list[str] = []
        for seed in entry.seed_artists:
            artist = self._artist_from_seed(seed, kept)
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
        artists.extend(self._discover(entry, artists, unread, kept))
        if not artists:
            raise LabelUnresolvable(
                f"the provider has no artist named exactly {entry.name!r}, the "
                f"label names no seed artists, and discovery found nothing"
            )
        return LabelRoster(
            artists,
            tuple(unread),
            lister=lambda artist, method, missing: self._listed(kept, artist, method, missing),
        )

    def playlist_for(self, reference: str) -> Any:
        """The provider playlist a URL, a share link, or an identifier names."""
        identifier = playlist_id(reference)
        try:
            playlist = self._session.playlist(identifier)
        except CratekitError:
            # The gate's park passes through unchanged (R-705).
            raise
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

        A listed object without the line is read again by identifier rather than
        judged unconfirmed on an omitted field.
        """
        del claimed  # the judgement is verify_release's, not this read's
        resolved = _copyright_label(release)
        identity = str(getattr(release, "id", "") or "")
        if not resolved and identity:
            resolved = _copyright_label(self._session.album(identity))
        return {"resolved_label": resolved, "source": SOURCE}

    def reread_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Who the provider credits on the release, one album read whatever its line (R-1634).

        Read on :meth:`_album`'s ladder. A release the provider no longer has answers
        :data:`RELEASE_GONE`; one with no identifier answers ``unconfirmed``.
        """
        del claimed  # the judgement is verify_release's, not this read's
        identity = str(getattr(release, "id", "") or "").strip()
        if not identity:
            return _unanswered("unconfirmed", "no release identifier to read again")
        try:
            album = self._album(identity)
        except ReleaseUnresolvable as exc:
            return _unanswered(RELEASE_GONE, str(exc))
        return {"resolved_label": _copyright_label(album), "source": SOURCE}

    def check_label(self, name: str) -> dict:
        """Whether any release the provider finds for ``name`` credits it.

        Confirmed only on a copyright line ``labels_match`` accepts, since a search
        always answers with its nearest titles.
        """
        found = self._session.search(name, models=[tidalapi.album.Album], limit=SEARCH_LIMIT)
        for album in _results(found, "albums"):
            resolved = _copyright_label(album)
            if resolved and label_verify.labels_match(name, resolved):
                return {"verdict": "confirmed", "resolved_label": resolved, "source": SOURCE}
        return _unanswered("unconfirmed", "no release found crediting this label")

    def account_playlists(self) -> tuple[AccountPlaylist, ...]:
        """The playlists the logged in user created, paged through the listing.

        Own only, by creator identifier, so a followed editorial playlist is never
        swept. A client that cannot say who is logged in is refused.
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

        Ending on the provider's count is not reaching it (R-504): fewer rows raise
        :class:`HeartsShortfall`. No published count leaves nothing to compare. A
        client that cannot say who is logged in is refused.
        """
        user = getattr(self._session, "user", None)
        if getattr(user, "favorites", None) is None:
            raise LookupError(
                "the provider client did not expose the logged in account's "
                "favourites, so its hearts cannot be listed"
            )
        rows, declared = listing.favorite_tracks_declared(self._session)
        # Remembered for the reader that needs to know the listing is whole (U120).
        self.hearts_declared = declared
        if declared is not None and len(rows) < declared:
            raise HeartsShortfall(rows, declared)
        return tuple(rows)

    def release_tracks(self, release_id: str) -> ReleaseRead:
        """One release read again by identifier: its tracks, and its year.

        Both reads climb the one ladder; the tracks page as a playlist's do and stop
        on the declared count, and a short listing is the third element (R-515). A
        gone release is answered once; any other failure is re-raised.
        """
        album = self._album(release_id)
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
        # The count the walk ended on, off the parsed album, at no request.
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
        return tuple(tracks), _year(album), short

    def _album(self, release_id: str) -> Any:
        """One release read by identifier, on the one retry ladder. Never ``None``."""
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
        return album

    def release_artist(self, release_id: str) -> str:
        """The name of the artist one release is filed under, in one album read."""
        return artist_name(self._album(release_id))

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask the catalogue which of ``codes`` it files anything under, in batches.

        Before the lookups, never instead of them (U207); only the app client is
        asked. Returns the requests made.
        """
        # A code the ISRC cache answers is not screened (U206).
        return self._screen.screen_uncached(self._lookups, self._cache, codes)

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        """The provider's tracks for one ISRC, on the one retry ladder.

        Only a not found is an answer, the empty tuple, never retried. Everything
        else, ``InvalidISRC`` included (the client folds most HTTP errors into it),
        climbs the ladder and is re-raised. An answer is kept in the ISRC cache
        (U206), a not found only when ``isrc_cache.said_not_found``. Under the app
        client when set up (U205), whose rejected credential climbs the ladder too.
        """
        wanted = str(isrc or "").strip()
        if not wanted:
            raise ValueError("no ISRC was given to look up")
        if self._screen.absent(wanted):
            # A batch already answered this spelling as filed under nothing (U207).
            return ()
        lookup = getattr(self._lookups, "get_tracks_by_isrc", None)
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")
        # The country of the client asked (U205).
        country = isrc_cache.country_of(self._lookups)
        held = self._cache.recall(wanted, country)
        if held is not None:
            return held
        answered: list[tuple[Any, ...]] = []

        def attempt(limit: int, offset: int) -> tuple[Any, ...]:
            del limit, offset
            answered.clear()
            try:
                found = lookup(wanted)
            except Exception as exc:
                if _gone(exc):
                    # Kept only when the client said not found in so many words.
                    if isrc_cache.said_not_found(exc):
                        answered.append(())
                    return ()
                raise
            if isinstance(found, (list, tuple)):
                answered.append(tuple(found))
            return tuple(found or ())

        isrc_cache.asked()
        try:
            result = listing.fetch_with_retry(attempt, limit=0, offset=0, sleep=_pause)
        except catalogue_api.AppCredentialsRejected as exc:
            raise catalogue_api.rejected(exc, f"look up the ISRC {wanted}") from exc
        if answered:
            self._cache.remember(wanted, country, answered[-1])
        return result

    def search_tracks(self, artist: str, title: str, offset: int = 0) -> tuple[Any, ...]:
        """One page of a track search for ``artist`` and ``title``, on the one retry ladder.

        Nothing is chosen here; ``intake.candidates`` decides. ``offset`` starts the
        page (R-879). A raised not found is the endpoint failing, and an answer with
        no ``tracks`` container is raised rather than read as empty.
        """
        query = " ".join(part for part in (str(artist or "").strip(), str(title or "").strip()) if part)
        if not query:
            raise ValueError("no artist and no title were given to search for")

        def attempt(limit: int, offset: int) -> Any:
            return self._session.search(
                query, models=[tidalapi.media.Track], limit=limit, offset=offset
            )

        found = listing.fetch_with_retry(
            attempt, limit=TRACK_SEARCH_PAGE, offset=max(int(offset), 0), sleep=_pause
        )
        # After the ladder, since waiting cannot change a shape.
        present = "tracks" in found if isinstance(found, Mapping) else hasattr(found, "tracks")
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
        return tuple(_results(found, "tracks"))


def open_catalogue(cfg: Any = None) -> TidalCatalogue:
    """A fresh catalogue over the process's logged in client, from the stored session.

    The client is :func:`provider_session.session_for`'s (U261). ``cfg`` is the
    frozen configuration the pacing gate reads (R-705); None is its defaults.
    """
    held = provider_session.session_for(cfg)
    return TidalCatalogue(
        held.client,
        catalogue=held.app,
        cache=isrc_cache.Cache.from_config(cfg),
    )


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
