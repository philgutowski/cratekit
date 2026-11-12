"""The streaming provider's catalogue, behind the label package's seam.

**THIN ON PURPOSE.** Every read here is one question to the provider client
``acquire.provider_session.session_for`` logged in and holds for the process,
and every PAGED read
goes through ``acquire.listing``. That module's docstring is the argument: a
listing that quietly returns one page looks exactly like a short one, and a
paging loop written here would be the fourth copy of that defect. A guard in the
suite scans this file for a direct paging call.

**IT IS NOT THE DOWNLOADER.** The vendored tool also holds a logged in client,
and reaching through it would have been shorter. It was rejected because the
tool is a downloader and this seam is a catalogue, so nothing here imports
``cratekit._vendor``, and a guard in the suite says so.

**ISRC LOOKUPS GO UNDER THE APP WHEN IT IS SET UP, AND THE CRAWL STAYS ON THE
ACCOUNT (U205).** :meth:`TidalCatalogue.tracks_for_isrc` asks the client
``acquire.provider_session.catalogue_client`` builds under Cratekit's own app
credentials when the opener built one, and the account session otherwise. Every
other read here stays on the account session, and these are they:

* :meth:`TidalCatalogue.account_playlists`, :meth:`TidalCatalogue.favourite_tracks`
  and :meth:`TidalCatalogue.playlist_for` read the account's own things, which
  are the account's business and which no app credential can see.
* The label crawl, :meth:`TidalCatalogue.artist_for` and its discovery,
  :meth:`TidalCatalogue.release_tracks`, :meth:`TidalCatalogue.release_artist`,
  :meth:`TidalCatalogue.search_release`, :meth:`TidalCatalogue.reread_release`,
  :meth:`TidalCatalogue.check_label` and
  :meth:`TidalCatalogue.search_tracks`. The official catalogue API has reads for
  most of these, but its listings page by cursor, and every listing this module
  makes pages through ``acquire.listing`` by limit and offset and stops on a
  declared count. A mapping between the two, written without a live probe of
  the official API's paging, is the "a short page is the end" defect this
  package has already paid for, so the crawl moves only in a unit that opens
  with that probe. Its calls are counted under the account meanwhile, where a
  person reading the spend sees them.

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
from collections.abc import Callable, Iterable, Mapping
from typing import Any

# Imported at module top rather than deferred, because ``catalogue.bound`` asks
# whether THIS module imports, and the answer has to include the client library.
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

    The status is the one nearest the failure, ``core.cause.answered_not_found``
    (R-1313), since a 404 whose body is a page arrives as the client's decode
    error with the 404 three context links down; the class name is read off
    the failure alone.
    """
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)


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


class LabelRoster(listing.HeldReleases):
    """Every artist a favourite label resolved to, listed as one artist object.

    ``Catalogue.artist_for`` hands ``crawl.releases`` ONE object, and a label on
    the provider is a roster: the label's own artist page when it has one, plus
    the seed artists the registry names, plus artists discovery found by album
    search and a credited artist walk. This presents the roster in the shape
    ``listing.artist_releases`` reads.

    THE LISTING HAPPENS HERE, ONCE, AT CONSTRUCTION. Listing lazily inside a
    method the crawl pages would run a whole retry ladder inside each attempt of
    the crawl's own ladder, so one failure that does not clear would be retried
    dozens of times and every retry would list every artist from the start.
    Built eagerly, a failure raises out of ``artist_for``, which is where a
    sweep already turns a foreign exception into its refusal.

    THE CRAWL READS WHAT IT HOLDS WHOLE, as a ``listing.HeldReleases``, and never
    pages it under one artist's budget (R-888). It has no paging methods, so
    nothing can page it, and ``crawl.can_list`` asks it what it holds.

    THE ROSTER ALWAYS EXPOSES BOTH LISTINGS, so the crawl paging it can never
    see a member that lacks one. ``unread`` is where that fact goes instead:
    what discovery could not read, handed in, plus every member whose client
    object lacks a listing, found here. The sweep reads it (R-261, R-393).

    ``lister`` READS ONE MEMBER'S LISTING OF ONE METHOD (U217). The catalogue
    hands one that answers from the label's kept listing first and keeps what
    it asks, so a member discovery already listed is not listed again and a
    second build asks nothing; left out, each member is listed now, as before.
    ``kept`` is what the build made of that store, for the screen.
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

        NOT DEDUPLICATED HERE. ``listing.artist_releases`` deduplicates by
        identifier when the crawl reads this roster, and the copy that used to sit
        here killed no test in U62's mutation table because that one always ran
        after it. One place decides what a repeat is.

        A member without ``method`` is skipped by the wrapper and recorded in
        ``missing``.
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

    A kept resolution gives the artist's identifier and name and no provider
    object. The object is what a listing that is NOT kept pages, so it is read
    once, by identifier, the first time such a listing needs it, and never when
    every listing of the member is kept (U217).
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
    held: list[str] = []
    for artist in getattr(release, "artists", None) or ():
        identity = str(getattr(artist, "id", "") or "")
        if identity:
            held.append(identity)
    return tuple(held)


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

    def _artist_from_seed(self, seed: str, kept: kept_listing.KeptListing) -> Any | None:
        """Resolve one registry seed, by identifier when it is one, else by name."""
        identifier = seed_identifier(seed)
        if identifier is not None:
            return self._member_identified(identifier, kept, need_object=False)
        return self._member_named(seed, kept)

    def _member_named(self, name: str, kept: kept_listing.KeptListing) -> Any | None:
        """:meth:`_artist_named`, answered from the kept listing when it holds the name.

        Two exact matches still raise and are never kept, so the refusal is
        said again on every run until the registry pins one by identifier.
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

        A kept "the provider has no such artist" answers ``None``. A kept
        artist answers a :class:`_Member` that reads the provider object only
        when an unkept listing needs it, unless ``need_object`` asks for it
        now, which discovery does so a read that fails still fails where it
        always did, outside the listing's own skip.
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

        A search that fails skips its query, as it always did, and is not kept.
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

        A LISTING IS KEPT ONLY WHOLE. One the provider failed raises out of
        here before anything is kept, one the client does not expose is
        recorded in ``missing`` and not kept, and an artist with no identifier
        to key it by is listed and not kept.
        """
        identity = str(getattr(artist, "id", "") or "")
        if identity:
            held = kept.listed(identity, method)
            if held is not None:
                return list(held)
        if isinstance(artist, _Member):
            if not artist.read_yet:
                # THE READ OF THE OBJECT IS A CALL, and counted, so a line that
                # says no call was made is true (U217 review round one).
                kept.asked_unkept()
            target = artist.provider_object()
        else:
            target = artist
        if target is None:
            # A KEPT ARTIST THE PROVIDER NO LONGER HAS. Its listing cannot be
            # read, and a roster missing it is not the whole label, so it is
            # unread rather than empty.
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
            for identity in self._credited_by(query, needle, kept):
                enqueue(identity)

        discovered: list[Any] = []
        held_ids = {str(getattr(artist, "id", "") or "") for artist in held}
        held_ids.discard("")
        while queue:
            artist_id = queue.popleft()
            # THE OBJECT ONLY WHEN A LISTING OF IT IS NOT KEPT, read here and
            # not inside the listing's skip below, where a failed read of it
            # always raised (U217).
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
                # BOTH METHODS, EACH KEPT ON ITS OWN, so the roster below reads
                # this member's listings from the store and does not ask again.
                releases = [
                    release
                    for method in listing.RELEASE_METHODS
                    for release in self._listed(kept, artist, method, [])
                ]
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

        EVERY ANSWER IS ASKED OF THE LABEL'S KEPT LISTING FIRST (U217), and
        what is asked is kept, written as it goes and once more on the way out
        whatever stopped the build, a call ceiling or a breaker park included.
        So a continue asks only what the stopped build did not finish, and a
        second build inside the kept life asks nothing. A kept listing that
        cannot be read refuses, ``label-listing-kept-unusable``, before any
        call. The roster carries what the build made of the store as ``kept``.
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
            # The gate's park passes through unchanged (R-705), as it does at
            # the other seam boundaries in this module: wrapped into an
            # unresolvable playlist it would lose the lift time and the engine
            # would read a cooldown as an unreadable playlist.
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

    def reread_release(self, claimed: str, release: Any) -> Mapping[str, Any]:
        """Who the provider credits on the release, ONE ALBUM READ whatever line it carries (R-1634).

        :meth:`search_release` judges a release carrying a line from that line
        with no call, which is right for the window and wrong for the sweep's
        re-verification, whose question is whether the provider is answering.
        Read on the retry ladder :meth:`_album` shares. A release the provider
        no longer has answers :data:`RELEASE_GONE`, which the sweep reads as
        neither confirmed nor unanswered; one with no identifier is never read
        and answers ``unconfirmed``, so it cannot make a listing look answered.
        """
        del claimed  # the judgement is verify_release's, not this read's
        identity = str(getattr(release, "id", "") or "").strip()
        if not identity:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": SOURCE,
                "notes": "no release identifier to read again",
            }
        try:
            album = self._album(identity)
        except ReleaseUnresolvable as exc:
            return {
                "verdict": RELEASE_GONE,
                "resolved_label": "",
                "source": SOURCE,
                "notes": str(exc),
            }
        return {"resolved_label": _copyright_label(album), "source": SOURCE}

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
        # REMEMBERED FOR THE READER THAT NEEDS TO KNOW THE LISTING IS WHOLE
        # (U120): a count that was published and reached says every heart is
        # here; none published says nothing, and a heart absent from such a
        # listing is not known to be gone.
        self.hearts_declared = declared
        if declared is not None and len(rows) < declared:
            raise HeartsShortfall(rows, declared)
        return tuple(rows)

    def release_tracks(self, release_id: str) -> ReleaseRead:
        """One release read again by identifier: its tracks, and its year.

        TWO READS, AND BOTH CLIMB THE ONE LADDER. The album itself goes through
        ``listing.fetch_with_retry`` so a rate limit on the ninetieth release of
        a long approval waits rather than failing it, and the tracks go through
        ``listing.playlist_tracks``, because an album pages its tracks exactly
        as a playlist does and counts the ones it will not serve the same way.
        That wrapper stops on the declared count, so a short window is never
        read as the end of the release. ENDING ON THE COUNT IS NOT REACHING IT,
        so the rows are compared with the count and the third element is the
        :class:`ListingShortfall` when they fall short (R-515).

        A RELEASE THAT IS GONE IS ANSWERED ONCE. See :class:`ReleaseUnresolvable`.
        Every other failure is re-raised as the provider raised it once the
        ladder is spent, and the caller names the release it belongs to.
        """
        album = self._album(release_id)
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
        # THE COUNT THE WALK ENDED ON, read off the album the client already
        # parsed, so the comparison costs no request (R-515).
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
        return tuple(tracks), _year(album), short

    def _album(self, release_id: str) -> Any:
        """One release read by identifier, on the one retry ladder. Never ``None``.

        The read :meth:`release_tracks` and :meth:`release_artist` share, so a
        release that is gone is the same answer to both and a rate limit climbs
        the same ladder for both.
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
        return album

    def release_artist(self, release_id: str) -> str:
        """The name of the artist one release is filed under. ONE PROVIDER READ.

        The album and nothing else: the client fills ``artist`` from the album's
        own payload, so the name costs no second call. A release that is gone
        is answered once, as :meth:`release_tracks` answers it.
        """
        return artist_name(self._album(release_id))

    def screen_isrcs(self, codes: Iterable[str]) -> int:
        """Ask the catalogue which of ``codes`` it files anything under, in batches.

        BEFORE THE LOOKUPS, NEVER INSTEAD OF THEM (U207). A code a batch
        answered as filed under nothing is answered as the empty tuple by
        :meth:`tracks_for_isrc` with no request; every other code is asked
        alone there as before, so a code filed under several releases is still
        seen as several. Only the app client is asked, see
        ``acquire.isrc_screen``. Returns the requests made.
        """
        # A CODE THE ISRC CACHE ANSWERS IS NOT SCREENED (U206): its lookup
        # makes no request, so a batch about it would be the one request a
        # second run over the same codes still paid.
        country = isrc_cache.country_of(self._lookups)
        return self._screen.screen(
            self._lookups,
            [code for code in codes if not self._cache.holds(str(code or ""), country)],
        )

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

        AN ANSWER IS ASKED ONCE (U206). A track list, or the not found above,
        is kept in the ISRC cache, and a later lookup of the same code in the
        same country is answered from it with no call. Nothing the ladder
        re-raises is kept, and the app client's own not found, which this
        route never raises for a code with nothing filed, is answered empty
        and not kept: only ``isrc_cache.said_not_found`` keeps a not found.

        UNDER THE APP CREDENTIALS WHEN THEY ARE SET UP (U205). The app client
        answers a code it files nothing under with an empty list and a missing
        resource with its own not found, both read here as the empty tuple, and
        raises no ``InvalidISRC`` at all. A rejected app credential climbs the
        ladder like any failure, since an expired token is its ordinary reason
        and the next attempt asks for a fresh one, and when the ladder is spent
        it refuses naming the app's credentials, never the account session.
        """
        wanted = str(isrc or "").strip()
        if not wanted:
            raise ValueError("no ISRC was given to look up")
        if self._screen.absent(wanted):
            # A batch already answered this exact spelling as filed under
            # nothing (U207), the answer this lookup would give.
            return ()
        lookup = getattr(self._lookups, "get_tracks_by_isrc", None)
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")
        # The country the client that is ASKED asks in (U205's app client
        # carries the account's own).
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
                    # Answered as gone as it always was, and KEPT only when the
                    # client said so in so many words: ``_gone`` reads any class
                    # named for a not found, and a file or module one raised
                    # inside the lookup is not the provider's answer.
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

        NOTHING IS CHOSEN HERE. The hits come back in the provider's order,
        every one of them, and ``intake.candidates`` decides what is exact and
        offers the rest to a person. One page of ``TRACK_SEARCH_PAGE``, because a
        candidate list is read by a person and the caller truncates it again.
        The seam's own page, so the caller can tell a full answer from a short one.
        ``offset`` is handed to the client as the start of the page, so the
        caller reads the next page of the same search (R-879).

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
            return self._session.search(
                query, models=[tidalapi.media.Track], limit=limit, offset=offset
            )

        found = listing.fetch_with_retry(
            attempt, limit=TRACK_SEARCH_PAGE, offset=max(int(offset), 0), sleep=_pause
        )
        # AFTER THE LADDER, because waiting cannot change a shape.
        present = "tracks" in found if isinstance(found, Mapping) else hasattr(found, "tracks")
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
        return tuple(_results(found, "tracks"))


def open_catalogue(cfg: Any = None) -> TidalCatalogue:
    """A fresh catalogue over the process's logged in client, from the stored session.

    The client is the one :func:`provider_session.session_for` holds for the
    process (U261): the first open logs in, and a later one, or the outbound
    account's, reuses it while the keychain still holds the session it was
    opened from. The catalogue itself is built fresh on every open, as before.

    The configuration is what the pacing gate reads its interval and cooldown
    off (R-705), the FROZEN one a job carries rather than a fresh load. None
    means the gate's own defaults, which are still a gate.
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
