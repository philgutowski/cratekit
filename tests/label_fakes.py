"""One stand-in for a label catalogue, shared by every suite that needs one.

**WHY IT EXISTS AT ALL, WRITTEN AT THE MOMENT THERE IS STILL ONE CONSUMER.**
``tests/outbound_fakes.py`` was extracted in U51 after three suites had already
grown private copies of one provider stand-in, which is three descriptions of a
protocol drifting apart at whatever rate each suite happens to need. U52 binds
the two label handlers and rebuilds harvest on the same seam, so the same three
consumers arrive here in one branch. One copy means a method the real
:class:`~cratekit.label.catalogue.Catalogue` protocol grows is missing in one
place rather than absent in three.

**IT REFUSES ANYTHING OUTSIDE THE PROTOCOL, AND THAT IS A GUARD RATHER THAN
TIDINESS.** ``label.catalogue.Catalogue`` declares eight reads and no write at
all: no playlist create, no heart, no follow. :class:`StrictCatalogue` raises on
any other attribute, so a worker that reached for one fails the suite instead of
failing silently against a fake permissive enough to answer.

**THE UNREADABLE VARIANT RAISES WHERE THE REAL ONE MUST.** The protocol's failure
contract says a label or a playlist the provider cannot resolve is a raise and
never a ``None``, because ``sweep.LabelSource.list_recent`` skips a missing
artist object with a bare ``continue``. A fake that returned ``None`` there would
make the suite agree with the defect. :class:`UnreadableCatalogue` is how the
refusal paths are driven instead.

Not a test module: pytest does not collect it.
"""

from __future__ import annotations

from typing import Any, Callable

from cratekit.label.catalogue import ReleaseUnresolvable

#: Every method the ``Catalogue`` protocol declares. Derived once here rather
#: than remembered at each assertion site.
PROTOCOL_METHODS = frozenset(
    {
        "artist_for",
        "playlist_for",
        "search_release",
        "check_label",
        "account_playlists",
        "favourite_tracks",
        "release_tracks",
        "tracks_for_isrc",
        "search_tracks",
    }
)


class FakeArtistLookup:
    """A session that answers ``artist(id)`` from memory.

    ``TidalCatalogue`` did not call ``session.artist`` until a seed could be
    recorded as ``id:<digits>``. The live client raises ``ObjectNotFound`` for
    an unknown identifier. This raises ``LookupError`` so a suite can drive
    that path without importing the client library.
    """

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
    """A provider release the listing wrappers can page.

    The same shape as ``tests/modules/test_labels.py``'s private ``Album``, which
    it deliberately does not replace: that class is what the existing sweep tests
    build their fixtures out of, and moving it would be a rewrite of six tests
    for no gain. This one exists so a suite that only wants a catalogue does not
    have to import from another test module to get one.
    """

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
    """A provider listing that truncates to one page when not given a limit.

    That is the real client shape: one page, no complaint. Modelled on the
    ``PagedArtist`` the label suite has used since U26, so a crawl that called it
    without the pagination wrappers would silently lose everything after the
    first hundred here too.
    """

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
    """One playlist track, with or without the copyright string harvest reads.

    ``harvest.labels_from_copyright`` reads ``copyright`` and falls back to
    ``label``, so a track carrying NEITHER is the shape that yields no candidate
    name at all. That track is not a dropped name, because no name was ever
    extracted to drop, and keeping it constructible here is what lets a suite
    tell "the catalogue said no" apart from "there was nothing to ask about".
    """

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

    def __init__(self, tracks: list[Any]) -> None:
        self._tracks = list(tracks)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Any]:
        size = self.page_size if limit is None else limit
        return self._tracks[offset : offset + size]


class UnlistablePlaylist:
    """A playlist object the pagination wrapper cannot list at all.

    It exposes no ``tracks`` method, so ``listing._paged_caller`` raises
    ``ListingNotPaginated`` at the moment it binds the method, BEFORE the retry
    ladder is entered. That matters for the suite as much as for the product: a
    playlist whose ``tracks`` merely refused pagination arguments would be
    retried five times with a real backoff, and a test driving that shape would
    sleep thirty one seconds to prove one conversion.

    A resolvable playlist that cannot then be listed is the second half of the
    unreadable surface, and it is a different failure from a playlist the
    catalogue could not resolve at all. Both become the same refusal, and having
    both here is how that claim is proven rather than assumed.
    """


class FakeCatalogue:
    """A catalogue that answers from memory and never talks to a network.

    ``artists`` is keyed by ``label_id`` rather than by display name, because
    that is the key the registry hands the seam and D5 forbids keying a record on
    a name a rename can move. ``playlists`` is keyed by the reference string a
    person typed, which is whatever the verb was given.

    ``confirmed`` names the release identifiers the search callable confirms.
    Left as ``None`` it confirms everything, which is the shape most callers
    want; given a set it confirms exactly those, which is how a suite drives the
    unconfirmed-and-dropped path. ``known_labels`` does the same job for the
    harvest side.
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
        self.confirmed = None if confirmed is None else frozenset(confirmed)
        self.known_labels = None if known_labels is None else frozenset(known_labels)
        #: Each release's tracks and its year, keyed by the release identifier,
        #: which is the only thing the seam is handed about a release.
        self.releases = dict(releases or {})
        self.releases_asked_for: list[str] = []
        #: The provider tracks filed under each ISRC. An ISRC absent here is one
        #: the provider answers with no track, which is an answer and not a
        #: failure; :class:`UnreadableCatalogue` is the failure.
        self.isrcs = dict(isrcs or {})
        self.isrcs_asked_for: list[str] = []
        #: The provider's hits for each search, keyed by the artist and the title
        #: exactly as the seam was handed them, in the provider's order. A search
        #: absent here is one the provider answers with nothing.
        self.searches = dict(searches or {})
        self.searched_for: list[tuple[str, str]] = []
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

    def search_release(self, claimed: str, release: Any) -> dict:
        release_id = str(getattr(release, "id", "") or "")
        if self.confirmed is not None and release_id not in self.confirmed:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": "fake-catalogue",
                "notes": "no catalogue match",
            }
        return {
            "verdict": "confirmed",
            "resolved_label": claimed,
            "source": "fake-catalogue",
            "notes": "",
        }

    def account_playlists(self) -> tuple[Any, ...]:
        self.account_listings += 1
        return tuple(self.account)

    def favourite_tracks(self) -> tuple[Any, ...]:
        self.heart_listings += 1
        return tuple(self.hearts)

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None]:
        self.releases_asked_for.append(release_id)
        try:
            tracks, year = self.releases[release_id]
        except KeyError as exc:
            # The seam's own exception, which is the protocol's contract for a
            # release the provider has nothing for, and never an empty listing.
            raise ReleaseUnresolvable(f"no catalogue release {release_id!r}") from exc
        return tuple(tracks), year

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        self.isrcs_asked_for.append(isrc)
        return tuple(self.isrcs.get(isrc, ()))

    def search_tracks(self, artist: str, title: str) -> tuple[Any, ...]:
        self.searched_for.append((artist, title))
        return tuple(self.searches.get((artist, title), ()))

    def check_label(self, name: str) -> dict:
        if self.known_labels is not None and name not in self.known_labels:
            return {
                "verdict": "unconfirmed",
                "resolved_label": "",
                "source": "fake-catalogue",
                "notes": "no catalogue match",
            }
        return {
            "verdict": "confirmed",
            "resolved_label": name,
            "source": "fake-catalogue",
            "notes": "",
        }


class StrictCatalogue(FakeCatalogue):
    """A :class:`FakeCatalogue` that raises on any attribute outside the protocol.

    The read-only property cannot be asserted by watching for a write that never
    happens: an absence proves nothing about the mechanism, only about this
    input. This raises instead, so the assertion is that no code path in the
    label package can even NAME a provider call the seam does not declare.
    """

    def __getattr__(self, name: str):
        raise AssertionError(
            f"the label path reached {name!r}, which the Catalogue protocol does "
            f"not declare. It declares only {', '.join(sorted(PROTOCOL_METHODS))}"
        )


class UnreadableCatalogue(FakeCatalogue):
    """A catalogue whose lookups all fail, for driving the refusal paths.

    Bound and credentialled and unable to answer, which is a different condition
    from the unbound build :func:`cratekit.label.catalogue.resolve` refuses with,
    and is the only condition ``label-playlist-unreadable`` may be raised for.
    The verification callables still answer, so a suite that reaches one has
    proved the listing was read, which it was not.
    """

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

    def release_tracks(self, release_id: str) -> tuple[tuple[Any, ...], int | None]:
        self.releases_asked_for.append(release_id)
        raise RuntimeError(f"the catalogue could not read the release {release_id!r}")

    def tracks_for_isrc(self, isrc: str) -> tuple[Any, ...]:
        self.isrcs_asked_for.append(isrc)
        raise RuntimeError(f"the catalogue could not look up the ISRC {isrc!r}")

    def search_tracks(self, artist: str, title: str) -> tuple[Any, ...]:
        self.searched_for.append((artist, title))
        raise RuntimeError(f"the catalogue could not search for {artist!r} {title!r}")


class VerificationOutage(FakeCatalogue):
    """A catalogue whose LISTINGS answer and whose VERIFICATION stops answering.

    The fourth provider read, and the one U52 left without a failure boundary on
    either label path. ``artist_for`` and ``playlist_for`` resolve normally here,
    so a suite that reaches a raise has proved the listing was read and that what
    failed is the confirmation of something already in hand. That is a different
    condition from :class:`UnreadableCatalogue`, which cannot resolve anything at
    all, and the two must not become the same refusal.

    ``answers`` IS A COUNT AND NOT A FLAG, because the interesting case is a
    PARTIAL round rather than a dead endpoint. ``review.offer`` commits per call,
    so a harvest whose second track raises has already written the first track's
    label into the review queue durably, and a refusal that did not name those
    rows would send a person to retry with no idea what is already waiting for
    them. ``answers=1`` is that shape; ``answers=0`` is the endpoint that was
    down before the first ask.

    ONE COUNTER FOR BOTH VERIFICATION METHODS. ``search_release`` and
    ``check_label`` are the same capability asked two ways, and a provider whose
    verification is rate limited or degraded is not selective about which of the
    two it refuses. No shipped path calls both in one pass.
    """

    def __init__(self, *args: Any, answers: int = 0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.answers = answers
        self.verifications = 0

    def _answer_or_fail(self) -> None:
        self.verifications += 1
        if self.verifications > self.answers:
            # THE PROVIDER'S OWN EXCEPTION SHAPE, which is what
            # ``listing.fetch_with_retry`` re-raises once its retry ladder is
            # spent. Nothing in this codebase can predict its type, so the
            # boundary under test has to catch broadly and this raises something
            # it has no special knowledge of.
            raise RuntimeError("the provider stopped answering verification calls")

    def search_release(self, claimed: str, release: Any) -> dict:
        self._answer_or_fail()
        return super().search_release(claimed, release)

    def check_label(self, name: str) -> dict:
        self._answer_or_fail()
        return super().check_label(name)


def catalogue_factory(fake: FakeCatalogue) -> Callable[[object], FakeCatalogue]:
    """A stand-in for ``label.catalogue.resolve`` that hands back ``fake``.

    Takes the configuration and ignores it, matching the real signature, so a
    monkeypatch of the module attribute is a drop-in rather than a shape a caller
    has to be written around.
    """

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
