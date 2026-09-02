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
TIDINESS.** ``label.catalogue.Catalogue`` declares four reads and no write at
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

#: Every method the ``Catalogue`` protocol declares. Derived once here rather
#: than remembered at each assertion site.
PROTOCOL_METHODS = frozenset(
    {
        "artist_for",
        "playlist_for",
        "search_release",
        "check_label",
    }
)


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
    ) -> None:
        self.artists = dict(artists or {})
        self.playlists = dict(playlists or {})
        self.confirmed = None if confirmed is None else frozenset(confirmed)
        self.known_labels = None if known_labels is None else frozenset(known_labels)
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
    "FakeCatalogue",
    "FakePagedArtist",
    "FakePagedPlaylist",
    "FakeRelease",
    "FakeTrack",
    "StrictCatalogue",
    "UnlistablePlaylist",
    "UnreadableCatalogue",
    "catalogue_factory",
]
