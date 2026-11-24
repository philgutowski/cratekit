"""One stand-in for a label catalogue, shared by every suite that needs one (U52).

One copy, as ``tests/outbound_fakes.py`` is, so a method the real
:class:`~cratekit.label.catalogue.Catalogue` grows is missing in one place.
:class:`StrictCatalogue` raises on anything outside its ten reads and no
writes. :class:`UnreadableCatalogue` raises where the real one must: an
unresolvable label or playlist is a raise, never a ``None``, since
``sweep.LabelSource.list_recent`` skips a missing artist with a bare ``continue``.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

from typing import Any, Callable

from cratekit.label.catalogue import TRACK_SEARCH_PAGE, ListingShortfall, ReleaseUnresolvable

#: Every method the ``Catalogue`` protocol declares, named once here.
PROTOCOL_METHODS = frozenset(
    {
        "artist_for",
        "playlist_for",
        "search_release",
        # R-1634. The sweep's re-verification reads the provider again by identifier.
        "reread_release",
        "check_label",
        "account_playlists",
        "favourite_tracks",
        "release_tracks",
        "release_artist",
        "tracks_for_isrc",
        "search_tracks",
        # U207. Reads only: which codes intake missing will ask the provider files nothing under.
        "screen_isrcs",
    }
)


class FakeArtistLookup:
    """A session answering ``artist(id)`` from memory, raising ``LookupError`` for an unknown."""

    def __init__(self, artists: dict[str, Any] | None = None) -> None:
        self.by_id = dict(artists or {})
        self.artist_lookups: list[str] = []

    def artist(self, artist_id: str | None = None) -> Any:
        key = str(artist_id or "")
        self.artist_lookups.append(key)
        try:
            return self.by_id[key]
        except KeyError as exc:
            raise LookupError(f"no provider artist {key!r}") from exc


class FakeRelease:

    def __init__(
        self,
        release_id: str,
        *,
        year: str = "2026",
        artist: str = "Label Act",
        title: str = "",
        copyright: str = "",
    ) -> None:
        self.id = release_id
        self.year = year
        self.artist = artist
        self.title = title or f"Release {release_id}"
        self.copyright = copyright
        self.tracks = [{"artists": [artist], "title": self.title}]


class FakePagedArtist:
    """A provider listing that truncates to one page without a limit, as the real client does."""

    page_size = 100

    def __init__(self, releases: list[FakeRelease]) -> None:
        self._releases = list(releases)

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[FakeRelease]:
        size = self.page_size if limit is None else limit
        return self._releases[offset : offset + size]

    def get_ep_singles(
        self, limit: int | None = None, offset: int = 0
    ) -> list[FakeRelease]:
        del limit, offset
        return []


class FakeTrack:
    """A playlist track. With neither ``copyright`` nor ``label`` it yields no candidate
    name, which a suite must tell apart from "the catalogue said no"."""

    def __init__(
        self,
        track_id: str,
        *,
        copyright: str = "",
        label: str | None = None,
        title: str = "",
    ) -> None:
        self.id = track_id
        self.copyright = copyright
        self.label = label
        self.title = title or f"Track {track_id}"


class FakePagedPlaylist:
    """A provider playlist that pages its tracks the way the real client does."""

    page_size = 100

    def __init__(self, tracks: list[Any], *, declared: int | None = None) -> None:
        self._tracks = list(tracks)
        if declared is not None:
            # THE COUNT THE PROVIDER DECLARES, as the client parses it (R-515).
            # Absent unless given, as on a client that publishes none.
            self.num_tracks = declared

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Any]:
        size = self.page_size if limit is None else limit
        return self._tracks[offset : offset + size]


class UnlistablePlaylist:
    """No ``tracks``, so ``listing._paged_caller`` raises ``ListingNotPaginated`` before
    the retry ladder and the test never sleeps through five real retries."""


class FakeCatalogue:
    """A catalogue that answers from memory and never talks to a network.

    ``artists`` is keyed by ``label_id``, never a display name (D5);
    ``playlists`` by the reference a person typed. ``confirmed`` names the
    release identifiers the search confirms, None for all; ``known_labels`` does
    the same for harvest.
    """

    def __init__(
        self,
        artists: dict[str, Any] | None = None,
        playlists: dict[str, Any] | None = None,
        *,
        confirmed: set[str] | frozenset[str] | None = None,
        known_labels: set[str] | frozenset[str] | None = None,
        account: list[Any] | None = None,
        hearts: list[Any] | None = None,
        releases: dict[str, tuple[list[Any], int | None]] | None = None,
        release_artists: dict[str, str] | None = None,
        isrcs: dict[str, list[Any]] | None = None,
        searches: dict[tuple[str, str], list[Any]] | None = None,
    ) -> None:
        self.artists = dict(artists or {})
        self.playlists = dict(playlists or {})
        #: The account's own playlists, as ``AccountPlaylist`` records, in the
        #: order the listing serves them.
        self.account = list(account or [])
        self.account_listings = 0
        #: The account's hearted tracks, in the order the listing serves them.
        self.hearts = list(hearts or [])
        self.heart_listings = 0
        #: The count the provider publishes beside its hearts, None for none published.
        self.hearts_declared: int | None = None
        self.confirmed = None if confirmed is None else frozenset(confirmed)
        self.known_labels = None if known_labels is None else frozenset(known_labels)
        #: Each release's tracks and its year, keyed by the release identifier,
        #: which is the only thing the seam is handed about a release.
        self.releases = dict(releases or {})
        self.releases_asked_for: list[str] = []
        #: The name each release's artist reads, by release identifier; absent is
        #: nothing for it, the empty string no artist named.
        self.release_artists = dict(release_artists or {})
        self.artists_asked_for: list[str] = []
        #: The provider tracks filed under each ISRC; absent is an answer of no track,
        #: not a failure.
        self.isrcs = dict(isrcs or {})
        self.isrcs_asked_for: list[str] = []
        #: Every ``screen_isrcs`` call, its codes in the order given (U207).
        self.screened: list[tuple[str, ...]] = []
        #: The provider's hits for each search, keyed by the artist and title as the
        #: seam was handed them, in order; absent is nothing. A long list is paged.
        self.searches = dict(searches or {})
        self.searched_for: list[tuple[str, str]] = []
        #: Every page asked for, as the artist, the title and the offset.
        self.pages_asked: list[tuple[str, str, int]] = []
        self.asked_for: list[str] = []
        self.playlists_asked_for: list[str] = []

    def artist_for(self, entry: Any) -> Any:
        label_id = str(getattr(entry, "label_id", entry))
        self.asked_for.append(label_id)
        try:
            return self.artists[label_id]
        except KeyError as exc:
            # RAISED rather than returned as None, which is the protocol's
            # failure contract and the whole reason this class is not a dict.
            raise LookupError(f"no catalogue artist for label {label_id!r}") from exc

    def playlist_for(self, reference: str) -> Any:
        self.playlists_asked_for.append(reference)
        try:
            return self.playlists[reference]
        except KeyError as exc:
            raise LookupError(f"no catalogue playlist for {reference!r}") from exc

    @staticmethod
    def _verdict(known: frozenset[str] | None, asked: str, label: str) -> dict:
        if known is not None and asked not in known:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": "fake-catalogue",
                "notes": "no catalogue match",
            }
        return {"verdict": "confirmed", "resolved_label": label, "source": "fake-catalogue", "notes": ""}

    def search_release(self, claimed: str, release: Any) -> dict:
        return self._verdict(self.confirmed, str(getattr(release, "id", "") or ""), claimed)

    def reread_release(self, claimed: str, release: Any) -> dict:
        """The forced read (R-1634), answered as :meth:`search_release` answers."""
        return self.search_release(claimed, release)

    def account_playlists(self) -> tuple[Any, ...]:
        self.account_listings += 1
        return tuple(self.account)

    def favourite_tracks(self) -> tuple[Any, ...]:
        self.heart_listings += 1
        return tuple(self.hearts)

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None, Any]:
        self.releases_asked_for.append(release_id)
        try:
            tracks, year, *declared = self.releases[release_id]
        except KeyError as exc:
            # The seam's own exception, which is the protocol's contract for a
            # release the provider has nothing for, and never an empty listing.
            raise ReleaseUnresolvable(f"no catalogue release {release_id!r}") from exc
        # A THIRD ELEMENT IS THE COUNT THE PROVIDER DECLARES (R-515), so a
        # test can list a release short of it. Two elements list in full.
        short = ListingShortfall.of(tracks, declared[0]) if declared else None
        return tuple(tracks), year, short

    def release_artist(self, release_id: str) -> str:
        self.artists_asked_for.append(release_id)
        try:
            return self.release_artists[release_id]
        except KeyError as exc:
            # The seam's own exception, as ``release_tracks`` raises it.
            raise ReleaseUnresolvable(f"no catalogue release {release_id!r}") from exc

    def screen_isrcs(self, codes) -> int:
        """Recorded, and asks nothing: this catalogue has no batch form (U207)."""
        self.screened.append(tuple(codes))
        return 0

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        self.isrcs_asked_for.append(isrc)
        return tuple(self.isrcs.get(isrc, ()))

    def search_tracks(self, artist: str, title: str, offset: int = 0) -> tuple[Any, ...]:
        self.searched_for.append((artist, title))
        self.pages_asked.append((artist, title, offset))
        hits = tuple(self.searches.get((artist, title), ()))
        return hits[offset : offset + TRACK_SEARCH_PAGE]

    def check_label(self, name: str) -> dict:
        return self._verdict(self.known_labels, name, name)


class StrictCatalogue(FakeCatalogue):
    """A :class:`FakeCatalogue` raising on any attribute outside the protocol."""

    def __getattr__(self, name: str):
        raise AssertionError(
            f"the label path reached {name!r}, which the Catalogue protocol does "
            f"not declare. It declares only {', '.join(sorted(PROTOCOL_METHODS))}"
        )


class UnreadableCatalogue(FakeCatalogue):
    """Bound and credentialled yet unable to answer, the only condition for
    ``label-playlist-unreadable``, unlike the unbound build ``catalogue.resolve`` refuses."""

    def artist_for(self, entry: Any) -> Any:
        label_id = str(getattr(entry, "label_id", entry))
        self.asked_for.append(label_id)
        raise RuntimeError(f"the catalogue could not be listed for {label_id!r}")

    def playlist_for(self, reference: str) -> Any:
        self.playlists_asked_for.append(reference)
        raise RuntimeError(f"the catalogue could not read the playlist {reference!r}")

    def favourite_tracks(self) -> tuple[Any, ...]:
        self.heart_listings += 1
        raise RuntimeError("the catalogue could not list the account's favourites")

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None, Any]:
        self.releases_asked_for.append(release_id)
        raise RuntimeError(f"the catalogue could not read the release {release_id!r}")

    def release_artist(self, release_id: str) -> str:
        self.artists_asked_for.append(release_id)
        raise RuntimeError(f"the catalogue could not read the release {release_id!r}")

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        self.isrcs_asked_for.append(isrc)
        raise RuntimeError(f"the catalogue could not look up the ISRC {isrc!r}")

    def search_tracks(self, artist: str, title: str, offset: int = 0) -> tuple[Any, ...]:
        self.searched_for.append((artist, title))
        raise RuntimeError(f"the catalogue could not search for {artist!r} {title!r}")


class VerificationOutage(FakeCatalogue):
    """A catalogue whose LISTINGS answer and whose VERIFICATION stops answering.

    ``answers`` is a count, since the interesting case is partial: a harvest whose
    second track raises has already committed the first track's label. One counter
    serves ``search_release`` and ``check_label``, one capability asked two ways.
    """

    def __init__(self, *args: Any, answers: int = 0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.answers = answers
        self.verifications = 0

    def _answer_or_fail(self) -> None:
        self.verifications += 1
        if self.verifications > self.answers:
            # The provider's own exception shape, as ``listing.fetch_with_retry``
            # re-raises it, so the boundary must catch broadly.
            raise RuntimeError("the provider stopped answering verification calls")

    def search_release(self, claimed: str, release: Any) -> dict:
        self._answer_or_fail()
        return super().search_release(claimed, release)

    def check_label(self, name: str) -> dict:
        self._answer_or_fail()
        return super().check_label(name)


def catalogue_factory(fake: FakeCatalogue) -> Callable[[object], FakeCatalogue]:
    """A stand-in for ``label.catalogue.resolve`` with the real signature, handing back ``fake``."""

    def resolve(cfg: object) -> FakeCatalogue:
        del cfg
        return fake

    return resolve


__all__ = [
    "PROTOCOL_METHODS",
    "FakeArtistLookup",
    "FakeCatalogue",
    "FakePagedArtist",
    "FakePagedPlaylist",
    "FakeRelease",
    "FakeTrack",
    "StrictCatalogue",
    "UnlistablePlaylist",
    "UnreadableCatalogue",
    "VerificationOutage",
    "catalogue_factory",
]
