"""U62: the provider catalogue adapter behind the label seam, driven against fakes.

Every scenario the unit's brief names is here, and none of them reaches the
provider. The client is a fake injected at ``provider_session.CLIENT_FACTORY``,
which is the one place a client is built, so the adapter under test is the
shipped class over a stand in for the network and nothing else. The live listing
and the live sweep belong to the next attended sitting and are recorded in
``docs/cutover.md``, not claimed here.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
import tidalapi
from tidalapi.exceptions import ObjectNotFound, TooManyRequests

from cratekit.acquire import listing, match, provider_session
from cratekit.cli import render
from cratekit.core import config, jobs, review, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue, sweep, tidal_catalogue
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import run, watermarks
from tests.cli_drive import drive
from tests.label_fakes import FakeArtistLookup
from tests.test_config import valid_data

PLAYLIST = "0f1e2d3c-4b5a-4968-8776-a5b4c3d2e1f0"
ADAPTER_SOURCE = Path(tidal_catalogue.__file__)

STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 946684800.0,
}


# ═══════════════════════════════════════════════════════════════════════════
# Fakes: a provider client and the objects it hands back
# ═══════════════════════════════════════════════════════════════════════════


class Named:
    def __init__(self, name: str, *, identity: str | None = None) -> None:
        self.name = name
        self.id = identity


class ProviderTrack:
    """The fields the live search was confirmed to carry on 2026-09-16."""

    def __init__(self, track_id: str, artist: str, name: str, *, isrc: str = "") -> None:
        self.id = track_id
        self.artists = [Named(artist)]
        self.artist = Named(artist)
        self.name = name
        self.version = None
        self.album = None
        self.isrc = isrc
        self.audio_quality = "LOSSLESS"
        self.copyright = ""


class ProviderPlaylist:
    """Pages its tracks, and serves one page when asked with no arguments."""

    def __init__(self, tracks: list[ProviderTrack]) -> None:
        self._tracks = list(tracks)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[ProviderTrack]:
        size = 100 if limit is None else limit
        return self._tracks[offset : offset + size]


class Release:
    def __init__(
        self,
        release_id: str,
        *,
        copyright: str = "",
        year: str = "2026",
        artists: list[Any] | tuple[Any, ...] = (),
    ) -> None:
        self.id = release_id
        self.copyright = copyright
        self.year = year
        self.name = f"Release {release_id}"
        self.artists = list(artists)


class ProviderArtist:
    """An artist page whose listings truncate to one page without arguments."""

    def __init__(
        self,
        name: str,
        albums: list[Release],
        singles: list[Release] = (),
        *,
        artist_id: str | None = None,
    ) -> None:
        self.name = name
        self.id = artist_id
        self._albums = list(albums)
        self._singles = list(singles)
        self.asked: list[tuple[str, int, int]] = []

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        size = 100 if limit is None else limit
        self.asked.append(("get_albums", size, offset))
        return self._albums[offset : offset + size]

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        size = 100 if limit is None else limit
        self.asked.append(("get_ep_singles", size, offset))
        return self._singles[offset : offset + size]


class UnlistableAct:
    """An artist whose listings reject pagination, so the wrapper refuses at bind.

    ``listing.artist_releases`` raises ``ListingNotPaginated`` before the retry
    ladder, which is the listing failure discovery must skip without sleeping.
    """

    def __init__(self, name: str, artist_id: str) -> None:
        self.name = name
        self.id = artist_id

    def get_albums(self) -> list[Release]:
        return []

    def get_ep_singles(self) -> list[Release]:
        return []


class MissingObject(Exception):
    """What the provider client raises for an identifier it has nothing for."""


class FakeClient:
    """A provider client that answers from memory and records what it was asked."""

    def __init__(
        self,
        *,
        accept: bool = True,
        raises: Exception | None = None,
        playlists: dict[str, ProviderPlaylist] | None = None,
        artists: list[ProviderArtist] | None = None,
        albums: list[Release] | None = None,
        albums_by_query: dict[str, list[Release]] | None = None,
    ) -> None:
        self.accept = accept
        self.raises = raises
        self.playlists = dict(playlists or {})
        self.artists = list(artists or [])
        self.albums = list(albums or [])
        self.albums_by_query = albums_by_query
        self.logins: list[dict] = []
        self.searches: list[str] = []
        self.search_calls: list[tuple[str, tuple[Any, ...]]] = []
        self._artists_by_id = FakeArtistLookup()
        self.artist_lookups = self._artists_by_id.artist_lookups
        self.token_type = None
        self.access_token = None
        self.refresh_token = None
        self.expiry_time = None

    def load_oauth_session(
        self, token_type, access_token, refresh_token=None, expiry_time=None, is_pkce=False
    ) -> bool:
        self.logins.append(
            {
                "token_type": token_type,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expiry_time": expiry_time,
                "is_pkce": is_pkce,
            }
        )
        if self.raises is not None:
            raise self.raises
        self.token_type = token_type
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiry_time = expiry_time
        return self.accept

    def playlist(self, playlist_id: str) -> ProviderPlaylist:
        try:
            return self.playlists[playlist_id]
        except KeyError as exc:
            raise MissingObject(playlist_id) from exc

    def search(self, query: str, models=None, limit: int = 50, offset: int = 0) -> dict:
        del limit, offset
        recorded = tuple(models or ())
        self.search_calls.append((query, recorded))
        self.searches.append(query)
        if self.albums_by_query is not None and tidalapi.album.Album in recorded:
            albums = list(self.albums_by_query.get(query, []))
        else:
            albums = list(self.albums)
        return {
            "artists": [artist for artist in self.artists if query.casefold() in artist.name.casefold()],
            "albums": albums,
        }

    def album(self, album_id: str) -> Release:
        for album in self.albums:
            if album.id == album_id:
                return album
        raise MissingObject(album_id)

    def artist(self, artist_id: str | None = None) -> ProviderArtist:
        self._artists_by_id.by_id = {
            str(getattr(held, "id", "") or ""): held
            for held in self.artists
            if str(getattr(held, "id", "") or "")
        }
        return self._artists_by_id.artist(artist_id)


def use_client(monkeypatch, client: FakeClient) -> FakeClient:
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    return client


def record_session(payload: dict | None = None) -> None:
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(payload or STORED))


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(valid_data(root, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


# ═══════════════════════════════════════════════════════════════════════════
# The session factory and the seam
# ═══════════════════════════════════════════════════════════════════════════


def test_a_recorded_session_resolves_the_adapter_over_a_pkce_login(cfg, monkeypatch):
    client = use_client(monkeypatch, FakeClient())
    record_session()

    found = catalogue.resolve(cfg)

    assert catalogue.bound() is True
    assert isinstance(found, tidal_catalogue.TidalCatalogue)
    assert len(client.logins) == 1
    login = client.logins[0]
    assert login["access_token"] == STORED["access_token"]
    assert login["refresh_token"] == STORED["refresh_token"]
    assert login["is_pkce"] is True


def test_with_no_session_the_seam_still_refuses_the_credential_and_builds_no_client(
    cfg, monkeypatch
):
    client = use_client(monkeypatch, FakeClient())

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    assert excinfo.value.cause.reason == "credential-missing"
    assert client.logins == []


def test_the_label_path_offers_the_same_three_act_procedure_as_doctor(cfg, monkeypatch):
    """U97, closing R-411. Two surfaces raise this refusal and one table answers both.

    ``catalogue.resolve`` and doctor's ``credential.provider`` check reach the
    person through different code, and a private copy of the words in either
    one is the second place a token becomes a sentence, which is what D2 exists
    to prevent. So the seam that matters is that this path renders the SAME
    text, asserted by rendering it here rather than by restating it.
    """
    use_client(monkeypatch, FakeClient())

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    cause = excinfo.value.cause
    assert cause.remediation.remedy is Remedy.AUTHENTICATE_PROVIDER
    line = render.remediation_line(cause)
    assert line != "  fix: crate login"
    assert "crate login provider-session --from-file" in line
    assert "docs/adapters.md" in line


class Response:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class HTTPFailure(Exception):
    """The client's HTTP error, carrying the response the way the real one does."""

    def __init__(self, status_code: int) -> None:
        super().__init__(f"{status_code} response")
        self.response = Response(status_code)


class AuthenticationError(Exception):
    """Named as the provider client names its own authentication failure."""


def _wrapped(inner: Exception) -> Exception:
    try:
        try:
            raise inner
        except Exception as exc:
            raise RuntimeError("client re-raised") from exc
    except RuntimeError as outer:
        return outer


@pytest.mark.parametrize(
    "client",
    [
        FakeClient(accept=False),
        FakeClient(raises=HTTPFailure(401)),
        FakeClient(raises=HTTPFailure(403)),
        FakeClient(raises=HTTPFailure(400)),
        FakeClient(raises=AuthenticationError("expired")),
        FakeClient(raises=_wrapped(HTTPFailure(401))),
    ],
    ids=["refused", "401", "403", "400", "client-auth-error", "chained-401"],
)
def test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one(
    cfg, monkeypatch, client
):
    """A person told only that a credential is missing records the one they have."""
    use_client(monkeypatch, client)
    record_session()

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    cause = excinfo.value.cause
    assert cause.reason == "credential-missing"
    assert cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER


@pytest.mark.parametrize(
    "failure",
    [ConnectionError("refused"), TimeoutError("slow"), HTTPFailure(503), ValueError("not json")],
    ids=["connection", "timeout", "server-error", "unparseable-page"],
)
def test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login(cfg, monkeypatch, failure):
    """Review finding: an outage told the person to log in again with a good session."""
    use_client(monkeypatch, FakeClient(raises=failure))
    record_session()

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    cause = excinfo.value.cause
    assert cause.reason == "unavailable-transient"
    assert cause.remediation.remedy == Remedy.RETRY_LATER
    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == STORED


def test_a_stored_blob_with_no_access_token_never_reaches_the_provider(cfg, monkeypatch):
    client = use_client(monkeypatch, FakeClient())
    record_session({"token": "recorded"})

    with pytest.raises(CratekitError) as excinfo:
        catalogue.resolve(cfg)

    assert excinfo.value.cause.remediation.remedy == Remedy.REAUTHENTICATE_PROVIDER
    assert client.logins == []


def test_a_refresh_during_login_is_written_back_to_the_keychain(monkeypatch):
    """One place a token is read and written back, and a datetime survives it."""

    class Refreshing(FakeClient):
        def load_oauth_session(self, *args, **kwargs):
            accepted = super().load_oauth_session(*args, **kwargs)
            self.access_token = "FAKE-value-3"
            self.expiry_time = datetime(2031, 1, 1)  # the client's naive UTC
            return accepted

    use_client(monkeypatch, Refreshing())
    record_session()

    provider_session.client_session()

    held = secrets.get_json(secrets.Credential.PROVIDER_SESSION)
    assert held["access_token"] == "FAKE-value-3"
    assert held["refresh_token"] == STORED["refresh_token"]
    assert held["expiry_time"] == datetime(2031, 1, 1, tzinfo=timezone.utc).timestamp()


def test_a_rejected_login_leaves_the_stored_session_alone(monkeypatch):
    use_client(monkeypatch, FakeClient(accept=False))
    record_session()

    with pytest.raises(provider_session.AdapterAuthFailed):
        provider_session.client_session()

    assert secrets.get_json(secrets.Credential.PROVIDER_SESSION) == STORED


# ═══════════════════════════════════════════════════════════════════════════
# The playlist reference and the playlist read
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "reference",
    [
        PLAYLIST,
        PLAYLIST.upper(),
        f"  {PLAYLIST}\n",
        f"https://tidal.com/browse/playlist/{PLAYLIST}",
        f"https://tidal.com/playlist/{PLAYLIST}",
        f"https://listen.tidal.com/playlist/{PLAYLIST}",
        f"http://www.tidal.com/browse/playlist/{PLAYLIST}/",
        f"https://tidal.com/browse/playlist/{PLAYLIST}?u",
        f"https://listen.tidal.com/playlist/{PLAYLIST}?utm_source=share",
    ],
    ids=[
        "bare",
        "bare-upper",
        "bare-padded",
        "browse-url",
        "short-path-url",
        "listen-url",
        "trailing-slash",
        "share-link",
        "share-link-query",
    ],
)
def test_a_url_a_share_link_and_a_bare_id_all_name_the_playlist(reference):
    assert tidal_catalogue.playlist_id(reference) == PLAYLIST


@pytest.mark.parametrize(
    "reference",
    [
        "",
        "not a playlist",
        PLAYLIST[:-1],
        f"{PLAYLIST}0",
        f"https://link.tidal.com/{PLAYLIST}",
        f"https://example.com/browse/playlist/{PLAYLIST}",
        f"https://tidal.com.example.com/playlist/{PLAYLIST}",
        f"ftp://tidal.com/playlist/{PLAYLIST}",
        f"https://tidal.com/browse/album/{PLAYLIST}",
        f"https://tidal.com/browse/playlist/{PLAYLIST}/tracks",
        "https://tidal.com/browse/playlist/",
    ],
    ids=[
        "empty",
        "words",
        "short-id",
        "long-id",
        "short-link-host",
        "foreign-host",
        "lookalike-host",
        "wrong-scheme",
        "album-url",
        "extra-segment",
        "no-id",
    ],
)
def test_anything_else_is_refused_by_name(reference):
    with pytest.raises(tidal_catalogue.PlaylistReferenceInvalid) as excinfo:
        tidal_catalogue.playlist_id(reference)
    assert "playlist" in str(excinfo.value)


def test_a_short_link_is_refused_with_a_way_forward():
    with pytest.raises(tidal_catalogue.PlaylistReferenceInvalid) as excinfo:
        tidal_catalogue.playlist_id("https://link.tidal.com/AbCdEf")
    assert "short share link" in str(excinfo.value)


def test_a_missing_playlist_raises_and_never_returns_an_empty_list():
    adapter = tidal_catalogue.TidalCatalogue(FakeClient())
    with pytest.raises(tidal_catalogue.PlaylistUnresolvable):
        adapter.playlist_for(PLAYLIST)


def test_a_playlist_the_client_returns_nothing_for_raises_too():
    class Empty(FakeClient):
        def playlist(self, playlist_id):
            del playlist_id

    with pytest.raises(tidal_catalogue.PlaylistUnresolvable):
        tidal_catalogue.TidalCatalogue(Empty()).playlist_for(PLAYLIST)


@pytest.mark.parametrize(
    "reference",
    [PLAYLIST, "https://link.tidal.com/AbCdEf"],
    ids=["unresolvable", "unparseable"],
)
def test_both_failures_reach_a_person_as_an_unreadable_playlist(reference):
    adapter = tidal_catalogue.TidalCatalogue(FakeClient())
    with pytest.raises(CratekitError) as excinfo:
        label_cli.playlist_tracks_or_refuse(adapter, reference)
    assert excinfo.value.cause.reason == "label-playlist-unreadable"


def test_the_rows_read_through_the_provider_row_reader_with_every_field():
    tracks = [
        ProviderTrack(str(100 + n), f"Act {n}", f"Title {n}", isrc=f"XX{n:05d}")
        for n in range(230)
    ]
    adapter = tidal_catalogue.TidalCatalogue(
        FakeClient(playlists={PLAYLIST: ProviderPlaylist(tracks)})
    )

    rows = label_cli.playlist_tracks_or_refuse(adapter, f"https://tidal.com/browse/playlist/{PLAYLIST}")
    wanted = match.read_tidal_tracks(rows)

    assert len(wanted) == 230, "the playlist was not paged to exhaustion"
    first = wanted[0]
    assert (first.ref, first.artist, first.title, first.isrc) == ("100", "Act 0", "Title 0", "XX00000")
    assert wanted[-1].ref == "329"


# ═══════════════════════════════════════════════════════════════════════════
# The label roster and the absence contract
# ═══════════════════════════════════════════════════════════════════════════


class Creator:
    def __init__(self, creator_id) -> None:
        self.id = creator_id


class AccountEntry:
    """One playlist the account listing serves, own or followed."""

    def __init__(self, playlist_id, name, creator_id, num_tracks=None) -> None:
        self.id = playlist_id
        self.name = name
        self.creator = Creator(creator_id)
        self.num_tracks = num_tracks


class AccountUser:
    def __init__(self, user_id, entries) -> None:
        self.id = user_id
        self._entries = list(entries)
        self.pages: list[tuple[int, int]] = []

    def playlist_and_favorite_playlists(self, limit: int | None = None, offset: int = 0):
        size = 50 if limit is None else limit
        self.pages.append((size, offset))
        return self._entries[offset : offset + size]


def test_the_account_listing_keeps_the_playlists_the_account_created():
    client = FakeClient()
    client.user = AccountUser(
        42,
        [
            AccountEntry("pl-own", "Warmup", 42, num_tracks=12),
            AccountEntry("pl-followed", "Editorial", 7, num_tracks=40),
            AccountEntry("pl-anon", "No Creator", None),
            AccountEntry("pl-empty", "Empty", 42, num_tracks=0),
            AccountEntry("pl-bool", "Odd Count", 42, num_tracks=True),
        ],
    )
    listed = tidal_catalogue.TidalCatalogue(client).account_playlists()
    assert listed == (
        AccountPlaylist("pl-own", "Warmup", 12),
        AccountPlaylist("pl-empty", "Empty", 0),
        AccountPlaylist("pl-bool", "Odd Count", None),
    )
    assert client.user.pages, "the account was not listed through the paging wrapper"


def test_the_account_listing_pages_past_the_first_page():
    entries = [AccountEntry(f"pl-{n}", f"List {n}", 42) for n in range(130)]
    client = FakeClient()
    client.user = AccountUser(42, entries)
    listed = tidal_catalogue.TidalCatalogue(client).account_playlists()
    assert len(listed) == 130


def test_a_client_that_cannot_name_its_account_refuses_rather_than_owning_nothing():
    client = FakeClient()
    client.user = AccountUser(None, [AccountEntry("pl-own", "Warmup", None)])
    with pytest.raises(LookupError):
        tidal_catalogue.TidalCatalogue(client).account_playlists()


# ═══════════════════════════════════════════════════════════════════════════
# U70: the account's hearts, the sixth read
# ═══════════════════════════════════════════════════════════════════════════


class HeartsFavorites:
    """The client's favourites object: pages its tracks and declares a count.

    ``endless`` serves a full window at every offset, which is what a provider
    whose offset parameter stopped advancing looks like, and is the shape that
    spends the listing's whole request budget.

    ``unservable`` names hearts the provider COUNTS and leaves out of every
    window it serves, which is the shape R-383 measured live: the window is cut
    from the counted sequence and then filtered, so a page comes back short
    and the walk still ends where the count says (R-504).
    """

    def __init__(self, tracks, *, declared=None, endless=False, unservable=()) -> None:
        self._tracks = list(tracks)
        self.declared = len(self._tracks) if declared is None else declared
        self.endless = endless
        self.unservable = set(unservable)
        self.pages: list[tuple[int, int]] = []

    def tracks(self, limit: int | None = None, offset: int = 0):
        size = 100 if limit is None else limit
        self.pages.append((size, offset))
        if self.endless:
            return self._tracks[:size]
        window = self._tracks[offset : offset + size]
        return [track for track in window if track.id not in self.unservable]

    def get_tracks_count(self) -> int:
        return self.declared


class HeartsUser:
    def __init__(self, favorites) -> None:
        self.id = 42
        self.favorites = favorites


def hearts_client(favorites) -> FakeClient:
    client = FakeClient()
    client.user = HeartsUser(favorites)
    return client


def test_the_hearts_listing_pages_to_the_declared_total_through_the_listing():
    hearts = [ProviderTrack(str(500 + n), f"Act {n}", f"Title {n}") for n in range(230)]
    favorites = HeartsFavorites(hearts)
    listed = tidal_catalogue.TidalCatalogue(hearts_client(favorites)).favourite_tracks()
    assert [track.id for track in listed] == [str(500 + n) for n in range(230)]
    assert len(favorites.pages) == 3, "the hearts were not listed through the paging wrapper"


def test_a_hearts_listing_that_never_ends_raises_and_never_returns_a_short_one():
    hearts = [ProviderTrack(str(500 + n), f"Act {n}", f"Title {n}") for n in range(100)]
    favorites = HeartsFavorites(hearts, declared=150, endless=True)
    adapter = tidal_catalogue.TidalCatalogue(hearts_client(favorites))
    with pytest.raises(listing.ListingTruncated):
        adapter.favourite_tracks()
    with pytest.raises(CratekitError) as excinfo:
        label_cli.favourite_tracks_or_refuse(adapter, "favorites")
    assert excinfo.value.cause.reason == "label-playlist-unreadable"
    assert excinfo.value.cause.detail["kind"] == "ListingTruncated"
    assert excinfo.value.cause.detail["playlist"] == "favorites"


# ═══════════════════════════════════════════════════════════════════════════
# R-504: a hearts listing shorter than the account declares is reported
# ═══════════════════════════════════════════════════════════════════════════

#: The live shape R-383 measured and R-504 drove: 197 counted, 12 withheld.
DECLARED_HEARTS = 197
WITHHELD_IDS = frozenset(str(900 + n) for n in range(0, 197, 17))


def withholding_favorites() -> HeartsFavorites:
    hearts = [ProviderTrack(str(900 + n), f"Act {n}", f"Title {n}") for n in range(197)]
    return HeartsFavorites(hearts, unservable=WITHHELD_IDS)


def test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows():
    """The walk ends where the count says and the rows still come up short.
    Before R-504 this returned 185 rows as the account and raised nothing."""
    assert len(WITHHELD_IDS) == 12
    favorites = withholding_favorites()
    adapter = tidal_catalogue.TidalCatalogue(hearts_client(favorites))
    with pytest.raises(catalogue.HeartsShortfall) as excinfo:
        adapter.favourite_tracks()
    short = excinfo.value
    assert (short.declared, short.listed, short.withheld) == (197, 185, 12)
    assert short.summary() == "197 declared, 185 listed, 12 withheld by the provider"
    assert short.block() == {"declared": 197, "listed": 185, "withheld": 12}
    served = [str(900 + n) for n in range(197) if str(900 + n) not in WITHHELD_IDS]
    assert [track.id for track in short.rows] == served
    assert len(favorites.pages) == 2, "the walk did not end on the declared count"


def test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall():
    """Not refused as an unreadable listing: the rows are hearts the provider
    served, so they are listed, and the count withheld rides beside them."""
    adapter = tidal_catalogue.TidalCatalogue(hearts_client(withholding_favorites()))
    rows, short = label_cli.favourite_tracks_or_refuse(adapter, "favorites")
    assert len(rows) == 185
    assert short is not None and short.withheld == 12


def test_a_complete_hearts_listing_reports_no_shortfall():
    hearts = [ProviderTrack(str(500 + n), f"Act {n}", f"Title {n}") for n in range(120)]
    adapter = tidal_catalogue.TidalCatalogue(hearts_client(HeartsFavorites(hearts)))
    rows, short = label_cli.favourite_tracks_or_refuse(adapter, "favorites")
    assert len(rows) == 120
    assert short is None


def test_a_listing_longer_than_its_count_is_not_a_shortfall():
    """A heart added while the read is in progress can leave more rows than
    the count the walk began on. That is not hearts withheld."""
    hearts = [ProviderTrack(str(500 + n), f"Act {n}", f"Title {n}") for n in range(40)]
    adapter = tidal_catalogue.TidalCatalogue(hearts_client(HeartsFavorites(hearts, declared=38)))
    assert len(adapter.favourite_tracks()) == 40


@pytest.mark.parametrize("declared", [0, -1, None])
def test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare(declared):
    """A zero or sentinel count is not trusted as an end by the walk, and so is
    not trusted as a total to fall short of either."""
    hearts = [ProviderTrack(str(500 + n), f"Act {n}", f"Title {n}") for n in range(30)]
    favorites = HeartsFavorites(hearts)
    favorites.declared = declared
    rows = tidal_catalogue.TidalCatalogue(hearts_client(favorites)).favourite_tracks()
    assert len(rows) == 30
    # THE LISTING SAYS SO TOO, rather than handing back a sentinel as a count.
    assert listing.favorite_tracks_declared(hearts_client(favorites)) == (hearts, None)


def test_the_listing_hands_back_the_count_the_walk_ended_on():
    favorites = withholding_favorites()
    rows, declared = listing.favorite_tracks_declared(hearts_client(favorites))
    assert (len(rows), declared) == (185, 197)


def test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall(
    cfg, monkeypatch
):
    """Driven through the real adapter and the real dispatcher."""
    use_client(monkeypatch, hearts_client(withholding_favorites()))
    record_session()
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        items = jobs.items(store, envelope["data"]["job_id"])
    assert len(items) == 185
    assert not {item.item_id for item in items} & WITHHELD_IDS
    assert envelope["data"]["progress"]["shortfall"] == {
        "declared": 197,
        "listed": 185,
        "withheld": 12,
    }
    (warning,) = [w for w in envelope["warnings"] if w["code"] == "intake-hearts-withheld"]
    assert "197 declared, 185 listed, 12 withheld by the provider" in warning["message"]


def test_a_client_that_exposes_no_favourites_refuses_rather_than_holding_no_hearts():
    client = FakeClient()
    client.user = AccountUser(42, [])
    with pytest.raises(LookupError):
        tidal_catalogue.TidalCatalogue(client).favourite_tracks()
    with pytest.raises(LookupError):
        tidal_catalogue.TidalCatalogue(FakeClient()).favourite_tracks()


def test_the_reserved_reference_is_never_a_playlist_reference():
    """``favorites`` cannot name a playlist, so reserving it shadows none.

    A playlist a person TITLED favorites is referenced by its identifier or
    its URL, which is what ``playlist_id`` accepts, so the reserved word and a
    real playlist can never be the same input.
    """
    for spelling in ("favorites", "Favorites", " FAVORITES "):
        with pytest.raises(tidal_catalogue.PlaylistReferenceInvalid):
            tidal_catalogue.playlist_id(spelling)
    titled = ProviderPlaylist([ProviderTrack("700", "Act", "Title")])
    titled.name = "favorites"
    adapter = tidal_catalogue.TidalCatalogue(FakeClient(playlists={PLAYLIST: titled}))
    rows = label_cli.playlist_tracks_or_refuse(adapter, PLAYLIST)
    assert [row.id for row in rows] == ["700"]


def test_an_unresolvable_label_raises_and_never_returns_none():
    adapter = tidal_catalogue.TidalCatalogue(FakeClient())
    entry = labels.LabelEntry(label_id="nowhere", name="Nowhere Records")
    with pytest.raises(tidal_catalogue.LabelUnresolvable):
        adapter.artist_for(entry)


def test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it():
    client = FakeClient(artists=[ProviderArtist("Harbour Lights", [Release("r1")])])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("Gone Act",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    assert "Gone Act" in str(excinfo.value)


def test_two_artists_named_exactly_the_label_refuse_rather_than_guess():
    """Review finding: the first exact hit could be an unrelated act of one name."""
    twin = ProviderArtist("Harbour Lights", [Release("x1")])
    twin.id = "2"
    first = ProviderArtist("Harbour Lights", [Release("r1")])
    first.id = "1"
    adapter = tidal_catalogue.TidalCatalogue(FakeClient(artists=[first, twin]))
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))
    assert "2 provider artists" in str(excinfo.value)


def test_an_id_seed_resolves_via_session_artist_and_does_not_search():
    pinned = ProviderArtist("Quiet Act", [Release("r1")], artist_id="99")
    other = ProviderArtist("Quiet Act", [Release("r2")], artist_id="100")
    client = FakeClient(artists=[pinned, other])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )

    roster = adapter.artist_for(entry)

    assert roster.artists == [pinned]
    assert client.artist_lookups == ["99"]
    assert "id:99" not in client.searches
    assert "Quiet Act" not in client.searches


def test_a_colliding_name_seed_still_refuses():
    first = ProviderArtist("Quiet Act", [Release("r1")], artist_id="99")
    twin = ProviderArtist("Quiet Act", [Release("r2")], artist_id="100")
    adapter = tidal_catalogue.TidalCatalogue(FakeClient(artists=[first, twin]))
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("Quiet Act",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    assert "2 provider artists" in str(excinfo.value)


def test_an_id_seed_succeeds_when_the_same_name_has_two_artists():
    pinned = ProviderArtist("Quiet Act", [Release("r1")], artist_id="99")
    twin = ProviderArtist("Quiet Act", [Release("r2")], artist_id="100")
    client = FakeClient(artists=[pinned, twin])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )

    roster = adapter.artist_for(entry)

    assert roster.artists == [pinned]
    assert client.artist_lookups == ["99"]


def test_an_unresolved_id_seed_refuses_the_label():
    own = ProviderArtist("Harbour Lights", [Release("r1")], artist_id="1")
    client = FakeClient(artists=[own])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    message = str(excinfo.value)
    assert "id:99" in message
    assert "identifier" in message
    assert "named exactly" not in message
    assert client.artist_lookups == ["99"]
    assert "id:99" not in client.searches


def test_a_provider_outage_looking_up_an_id_seed_is_not_an_unresolved_seed():
    class OutageClient(FakeClient):
        def artist(self, artist_id: str | None = None) -> ProviderArtist:
            self.artist_lookups.append(str(artist_id))
            raise ConnectionError("refused")

    adapter = tidal_catalogue.TidalCatalogue(OutageClient())
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )
    with pytest.raises(ConnectionError):
        adapter.artist_for(entry)


def test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed():
    class BrokenClient(FakeClient):
        def artist(self, artist_id: str | None = None) -> ProviderArtist:
            self.artist_lookups.append(str(artist_id))
            raise KeyError(artist_id)

    adapter = tidal_catalogue.TidalCatalogue(BrokenClient())
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )
    with pytest.raises(KeyError):
        adapter.artist_for(entry)


def test_the_client_object_not_found_is_an_unresolved_id_seed():
    class MissingClient(FakeClient):
        def artist(self, artist_id: str | None = None) -> ProviderArtist:
            self.artist_lookups.append(str(artist_id))
            raise ObjectNotFound("gone")

    adapter = tidal_catalogue.TidalCatalogue(MissingClient())
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    assert "id:99" in str(excinfo.value)


def test_an_id_lookup_that_returns_none_is_an_unresolved_seed():
    class EmptyClient(FakeClient):
        def artist(self, artist_id: str | None = None) -> ProviderArtist | None:
            self.artist_lookups.append(str(artist_id))
            return None

    adapter = tidal_catalogue.TidalCatalogue(EmptyClient())
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:99",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    assert "id:99" in str(excinfo.value)


def test_a_seed_that_is_not_digits_after_the_prefix_is_still_a_name():
    named = ProviderArtist("id:abc", [Release("r1")], artist_id="1")
    client = FakeClient(artists=[named])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("id:abc",)
    )

    roster = adapter.artist_for(entry)

    assert roster.artists == [named]
    assert client.artist_lookups == []
    assert "id:abc" in client.searches


def test_an_uppercase_id_prefix_is_still_a_name_seed():
    pinned = ProviderArtist("Quiet Act", [Release("r1")], artist_id="99")
    client = FakeClient(artists=[pinned])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("ID:99",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable):
        adapter.artist_for(entry)
    assert client.artist_lookups == []


def test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory():
    """Review finding: a lazy listing ran a retry ladder inside the crawl's own."""
    artist = ProviderArtist("Harbour Lights", [Release("r1")], [Release("s1")])
    adapter = tidal_catalogue.TidalCatalogue(FakeClient(artists=[artist]))
    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))
    listed = list(artist.asked)
    assert {call[0] for call in listed} == {"get_albums", "get_ep_singles"}

    assert [release.id for release in listing.artist_releases(roster)] == ["r1", "s1"]
    assert artist.asked == listed, "the crawl reached the provider again"


def test_a_near_name_is_not_the_label():
    client = FakeClient(artists=[ProviderArtist("Harbour Lights Tribute", [Release("r1")])])
    adapter = tidal_catalogue.TidalCatalogue(client)
    with pytest.raises(tidal_catalogue.LabelUnresolvable):
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))


def test_the_absence_contract_holds_through_the_sweep(cfg, monkeypatch):
    """R-135's shape closed: an unreadable label refuses the source, not a clean zero."""
    del cfg
    use_client(monkeypatch, FakeClient())
    record_session()
    entry = labels.LabelEntry(label_id="nowhere", name="Nowhere Records")
    source = sweep.LabelSource(
        config.load(),
        registry=labels.Registry(labels={entry.label_id: entry}),
        catalogue=catalogue.resolve(config.load()),
    )
    with pytest.raises(run.LookupFailure):
        source.list_recent(10)


def test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing(cfg, monkeypatch):
    """Paged to exhaustion across two artists and two listings, deduplicated once."""
    del cfg
    own_albums = [Release(f"a{n}", copyright="(P) 2026 Harbour Lights") for n in range(150)]
    shared = Release("shared", copyright="(P) 2025 Harbour Lights")
    label_page = ProviderArtist("Harbour Lights", own_albums, [shared])
    seed = ProviderArtist("Quiet Act", [], [shared, Release("s1", copyright="2024 Harbour Lights")])
    client = use_client(monkeypatch, FakeClient(artists=[label_page, seed]))
    record_session()
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("Quiet Act",), track_limit=500
    )
    source = sweep.LabelSource(
        config.load(),
        registry=labels.Registry(labels={entry.label_id: entry}),
        catalogue=catalogue.resolve(config.load()),
    )

    found = source.list_recent(-1)

    assert {item.identity for item in found} == {f"a{n}" for n in range(150)} | {"shared", "s1"}
    assert ("get_albums", 100, 100) in label_page.asked
    assert client.searches[:2] == ["Harbour Lights", "Quiet Act"]


def album_queries_of(client: FakeClient) -> list[str]:
    return [
        query
        for query, models in client.search_calls
        if models == (tidalapi.album.Album,)
    ]


def _credited(name: str, artist_id: str, *, copyright: str = "(P) 2026 Harbour Lights") -> tuple[ProviderArtist, Release]:
    artist = ProviderArtist(name, [Release("a1", copyright=copyright)], artist_id=artist_id)
    compilation = Release(
        "va1",
        copyright=copyright,
        artists=[Named(name, identity=artist_id)],
    )
    return artist, compilation


def test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist(
    cfg, monkeypatch
):
    del cfg
    act, compilation = _credited("Act A", "10")
    use_client(monkeypatch, FakeClient(artists=[act], albums=[compilation]))
    record_session()
    entry = labels.LabelEntry(label_id="harbour", name="Harbour Lights")
    adapter = catalogue.resolve(config.load())

    roster = adapter.artist_for(entry)
    source = sweep.LabelSource(
        config.load(),
        registry=labels.Registry(labels={entry.label_id: entry}),
        catalogue=adapter,
    )
    found = source.list_recent(-1)

    assert roster.artists == [act]
    assert {item.identity for item in found} == {"a1"}
    assert "va1" not in {item.identity for item in found}


def test_discovery_that_finds_only_copyright_mismatches_still_refuses():
    act = ProviderArtist("Act A", [Release("a1", copyright="(P) 2026 Other House")], artist_id="10")
    compilation = Release(
        "va1",
        copyright="(P) 2026 Other House",
        artists=[Named("Act A", identity="10")],
    )
    client = FakeClient(artists=[act], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))
    message = str(excinfo.value)
    assert "discovery found nothing" in message
    assert "named exactly 'Harbour Lights'" in message


def test_numbered_compilation_queries_are_the_production_range():
    client = FakeClient()
    adapter = tidal_catalogue.TidalCatalogue(client)
    with pytest.raises(tidal_catalogue.LabelUnresolvable):
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert list(tidal_catalogue.COMPILATION_RANGE) == list(range(1, 80))
    assert album_queries_of(client) == [
        "Harbour Lights",
        *(f"Harbour Lights {number:03d}" for number in range(1, 80)),
    ]


def test_a_compilation_returned_only_for_a_numbered_query_is_consumed():
    act = ProviderArtist(
        "Act A", [Release("a1", copyright="(P) 2026 Harbour Lights")], artist_id="10"
    )
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Act A", identity="10")],
    )
    compilation.name = "Harbour Lights 042"
    client = FakeClient(
        artists=[act],
        albums_by_query={"Harbour Lights 042": [compilation]},
    )
    adapter = tidal_catalogue.TidalCatalogue(client)

    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [act]


def test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page():
    own = ProviderArtist(
        "Harbour Lights",
        [Release("own1", copyright="(P) 2026 Harbour Lights")],
        artist_id="1",
    )

    class FlakySearch(FakeClient):
        def search(self, query: str, models=None, limit: int = 50, offset: int = 0) -> dict:
            recorded = tuple(models or ())
            self.search_calls.append((query, recorded))
            self.searches.append(query)
            if recorded == (tidalapi.album.Album,) and query.endswith("042"):
                raise TooManyRequests("slow down")
            return {
                "artists": [
                    artist
                    for artist in self.artists
                    if query.casefold() in artist.name.casefold()
                ],
                "albums": list(self.albums),
            }

    client = FlakySearch(artists=[own])
    adapter = tidal_catalogue.TidalCatalogue(client)
    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [own]
    assert "Harbour Lights 042" in album_queries_of(client)
    assert "Harbour Lights 043" in album_queries_of(client)


def test_an_authentication_error_on_album_search_still_refuses_the_label():
    own = ProviderArtist(
        "Harbour Lights",
        [Release("own1", copyright="(P) 2026 Harbour Lights")],
        artist_id="1",
    )

    class DeadSearch(FakeClient):
        def search(self, query: str, models=None, limit: int = 50, offset: int = 0) -> dict:
            recorded = tuple(models or ())
            self.search_calls.append((query, recorded))
            self.searches.append(query)
            if recorded == (tidalapi.album.Album,):
                raise tidalapi.exceptions.AuthenticationError("expired")
            return {
                "artists": [
                    artist
                    for artist in self.artists
                    if query.casefold() in artist.name.casefold()
                ],
                "albums": list(self.albums),
            }

    adapter = tidal_catalogue.TidalCatalogue(DeadSearch(artists=[own]))
    with pytest.raises(tidalapi.exceptions.AuthenticationError):
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))


def test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered(
    cfg, monkeypatch
):
    del cfg
    act = ProviderArtist("Act A", [Release("a1", copyright="(P) 2026 Harbour Lights")], artist_id="10")
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Act A", identity="10")],
    )
    use_client(monkeypatch, FakeClient(artists=[act], albums=[compilation]))
    record_session()
    entry = labels.LabelEntry(label_id="harbour", name="Harbour Lights")
    source = sweep.LabelSource(
        config.load(),
        registry=labels.Registry(labels={entry.label_id: entry}),
        catalogue=catalogue.resolve(config.load()),
    )

    found = source.list_recent(-1)

    assert {item.identity for item in found} == {"a1"}
    assert "va1" not in {item.identity for item in found}


def test_an_unresolved_name_seed_refuses_even_when_discovery_would_find_albums():
    act, compilation = _credited("Act A", "10")
    client = FakeClient(artists=[act], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(
        label_id="harbour", name="Harbour Lights", seed_artists=("Gone Act",)
    )
    with pytest.raises(tidal_catalogue.LabelUnresolvable) as excinfo:
        adapter.artist_for(entry)
    assert "Gone Act" in str(excinfo.value)
    assert album_queries_of(client) == []


def test_discovery_enqueues_collaborators_from_listed_matching_releases():
    lead = ProviderArtist(
        "Lead Act",
        [
            Release(
                "collab",
                copyright="(P) 2026 Harbour Lights",
                artists=[
                    Named("Lead Act", identity="10"),
                    Named("Guest", identity="11"),
                ],
            )
        ],
        artist_id="10",
    )
    guest = ProviderArtist(
        "Guest",
        [Release("g1", copyright="(P) 2026 Harbour Lights")],
        artist_id="11",
    )
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Lead Act", identity="10")],
    )
    client = FakeClient(artists=[lead, guest], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)

    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [lead, guest]


def test_a_discovered_artist_already_on_the_roster_is_not_added_twice():
    own = ProviderArtist(
        "Harbour Lights",
        [Release("own1", copyright="(P) 2026 Harbour Lights")],
        artist_id="1",
    )
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Harbour Lights", identity="1")],
    )
    client = FakeClient(artists=[own], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)

    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [own]


def test_discovery_runs_when_the_label_already_has_an_artist_page():
    own = ProviderArtist(
        "Harbour Lights",
        [Release("own1", copyright="(P) 2026 Harbour Lights")],
        artist_id="1",
    )
    collab = ProviderArtist(
        "Quiet Act",
        [Release("q1", copyright="(P) 2026 Harbour Lights")],
        artist_id="10",
    )
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Quiet Act", identity="10")],
    )
    client = FakeClient(artists=[own, collab], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)

    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [own, collab]


def test_discovery_matches_copyright_against_the_entry_match_needle():
    act, compilation = _credited("Act A", "10", copyright="(P) 2026 HL")
    client = FakeClient(artists=[act], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)
    entry = labels.LabelEntry(label_id="harbour", name="Not The Label Name", match="HL")

    roster = adapter.artist_for(entry)

    assert roster.artists == [act]


def test_a_listing_failure_on_one_discovered_artist_skips_that_artist():
    broken = UnlistableAct("Broken", "9")
    act = ProviderArtist(
        "Act A", [Release("a1", copyright="(P) 2026 Harbour Lights")], artist_id="10"
    )
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[
            Named("Broken", identity="9"),
            Named("Act A", identity="10"),
        ],
    )
    client = FakeClient(artists=[broken, act], albums=[compilation])
    adapter = tidal_catalogue.TidalCatalogue(client)

    roster = adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))

    assert roster.artists == [act]
    # R-393: the skip is recorded, and one that cannot page is not worth a resume.
    ((artist, listed, transient),) = [
        (one.artist, one.listing, one.transient) for one in roster.unread
    ]
    assert (artist, listed, transient) == ("Broken", "artist_releases", False)


def test_a_session_dead_during_discovery_refuses_the_label():
    compilation = Release(
        "va1",
        copyright="(P) 2026 Harbour Lights",
        artists=[Named("Act A", identity="10")],
    )

    class DeadLookup(FakeClient):
        def artist(self, artist_id: str | None = None) -> ProviderArtist:
            self.artist_lookups.append(str(artist_id))
            raise refuse(
                "credential-missing",
                "the stored session is gone",
                steps=("crate login",),
                scope=Scope.RUN,
                origin=("test",),
            )

    adapter = tidal_catalogue.TidalCatalogue(DeadLookup(albums=[compilation]))
    with pytest.raises(CratekitError) as excinfo:
        adapter.artist_for(labels.LabelEntry(label_id="harbour", name="Harbour Lights"))
    assert excinfo.value.cause.reason == "credential-missing"


def test_a_release_confirms_from_its_own_copyright_line_or_a_re_read():
    listed = Release("r1")
    client = FakeClient(albums=[Release("r1", copyright="(P) 2026 Harbour Lights")])
    adapter = tidal_catalogue.TidalCatalogue(client)

    assert adapter.search_release("Harbour Lights", listed)["resolved_label"] == "Harbour Lights"
    assert (
        adapter.search_release("x", Release("r2", copyright="(C) 2020 Other House"))["resolved_label"]
        == "Other House"
    )


def test_a_harvested_name_is_confirmed_only_by_a_matching_copyright_line():
    client = FakeClient(
        albums=[Release("r1", copyright="(P) 2026 Other House"), Release("r2", copyright="")]
    )
    adapter = tidal_catalogue.TidalCatalogue(client)
    assert adapter.check_label("Harbour Lights")["verdict"] == "unconfirmed"
    client.albums.append(Release("r3", copyright="(P) 2026 Harbour Lights Ltd"))
    assert adapter.check_label("Harbour Lights")["verdict"] == "confirmed"


# ═══════════════════════════════════════════════════════════════════════════
# R-261 and R-393: a crawl that did not read everything says so
# ═══════════════════════════════════════════════════════════════════════════

HARBOUR = "(P) 2026 Harbour Lights"


class RateLimitedArtist(ProviderArtist):
    """An artist whose album listing answers every request with a live 429."""

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        self.asked.append(("get_albums", limit or 0, offset))
        raise TooManyRequests("slow down")


class AlbumsOnlyArtist:
    """A client version that exposes the album listing and not the singles one."""

    def __init__(self, name: str, albums: list[Release], *, artist_id: str | None = None) -> None:
        self.name = name
        self.id = artist_id
        self._albums = list(albums)

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Release]:
        size = 100 if limit is None else limit
        return self._albums[offset : offset + size]


def _sweep_through_the_worker(monkeypatch, client: FakeClient) -> tuple[int, dict, str]:
    """Register Harbour Lights, bind the shipped adapter over ``client``, drive a sweep."""
    pauses: list[float] = []
    monkeypatch.setattr(tidal_catalogue, "_pause", pauses.append)
    code, added = drive(["label", "registry", "add", "Harbour Lights"])
    assert code == int(ExitCode.OK), added
    monkeypatch.setattr(
        catalogue, "resolve", lambda cfg: tidal_catalogue.TidalCatalogue(client)
    )
    code, queued = drive(["sync", "labels"])
    assert code == int(ExitCode.OK), queued
    job_id = queued["data"]["job_id"]
    code, done = drive(["sync", "labels", "--job", job_id])
    return code, done, job_id


def _the_item_cause(job_id: str):
    with jobs.open_store() as store:
        (item,) = jobs.items(store, job_id)
    return item.cause


def _offered() -> set[str]:
    with review.open_store(config.load()) as store:
        page = review.list_items(store, queue=str(review.Queue.LABEL_RELEASE))
    return {str(item.payload.get("identity")) for item in page.items}


def _label_with_a_discovered_pair(first: ProviderArtist) -> FakeClient:
    """The label's own page, and a compilation crediting ``first`` and Act A."""
    own = ProviderArtist("Harbour Lights", [Release("own1", copyright=HARBOUR)], artist_id="1")
    act = ProviderArtist("Act A", [Release("a1", copyright=HARBOUR)], artist_id="11")
    compilation = Release(
        "va1",
        copyright=HARBOUR,
        artists=[Named(first.name, identity=str(first.id)), Named("Act A", identity="11")],
    )
    return FakeClient(artists=[own, first, act], albums=[compilation])


def test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist(cfg, monkeypatch):
    """R-393: a 429 on one discovered artist used to read as a complete roster."""
    del cfg
    busy = RateLimitedArtist("Busy Act", [], artist_id="10")
    client = _label_with_a_discovered_pair(busy)

    code, failed, job_id = _sweep_through_the_worker(monkeypatch, client)

    assert code != int(ExitCode.OK), failed
    cause = _the_item_cause(job_id)
    assert cause is not None and cause.reason == "label-sweep-incomplete"
    assert "Busy Act" in cause.message
    assert "TooManyRequests" in cause.message
    assert cause.retryable is True
    assert cause.remediation.remedy is Remedy.RESUME_JOB
    assert [entry["artist"] for entry in cause.detail["unread"]] == ["Busy Act"]
    # What WAS read is offered before the refusal, and stays offered.
    assert _offered() == {"own1", "a1"}


def test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded(
    cfg, monkeypatch
):
    """R-393's closing condition: the 429 is retried, and the suite sleeps for none of it."""
    del cfg
    busy = RateLimitedArtist("Busy Act", [], artist_id="10")
    client = _label_with_a_discovered_pair(busy)
    pauses: list[float] = []

    monkeypatch.setattr(tidal_catalogue, "_pause", pauses.append)
    roster = tidal_catalogue.TidalCatalogue(client).artist_for(
        labels.LabelEntry(label_id="harbour-lights", name="Harbour Lights")
    )

    assert len(busy.asked) == listing.DEFAULT_MAX_RETRIES + 1
    assert len(pauses) == listing.DEFAULT_MAX_RETRIES
    assert [(one.artist, one.listing) for one in roster.unread] == [
        ("Busy Act", "artist_releases")
    ]


def test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread(
    cfg, monkeypatch
):
    """Review finding: the roster reads a held artist again, and that read is the one used."""
    del cfg

    class LimitedForOneLadder(ProviderArtist):
        """429 on every attempt discovery's ladder makes, then answers the roster."""

        def get_albums(self, limit: int | None = None, offset: int = 0) -> list[Release]:
            if len(self.asked) <= listing.DEFAULT_MAX_RETRIES:
                self.asked.append(("get_albums", limit or 0, offset))
                raise TooManyRequests("slow down")
            return super().get_albums(limit, offset)

    own = LimitedForOneLadder(
        "Harbour Lights", [Release("own1", copyright=HARBOUR)], artist_id="1"
    )
    compilation = Release(
        "va1", copyright=HARBOUR, artists=[Named("Harbour Lights", identity="1")]
    )
    client = FakeClient(artists=[own], albums=[compilation])
    monkeypatch.setattr(tidal_catalogue, "_pause", lambda seconds: None)

    roster = tidal_catalogue.TidalCatalogue(client).artist_for(
        labels.LabelEntry(label_id="harbour-lights", name="Harbour Lights")
    )

    # Discovery spent a whole ladder on it, then the roster read a page and the
    # empty page after it.
    albums_asked = [call for call in own.asked if call[0] == "get_albums"]
    assert len(albums_asked) == (listing.DEFAULT_MAX_RETRIES + 1) + 2
    assert roster.unread == ()
    assert [release.id for release in listing.artist_releases(roster)] == ["own1"]


def test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it(cfg, monkeypatch):
    """R-261: a client exposing one of two listings used to report a complete crawl."""
    del cfg
    own = AlbumsOnlyArtist("Harbour Lights", [Release("own1", copyright=HARBOUR)], artist_id="1")
    client = FakeClient(artists=[own])

    code, failed, job_id = _sweep_through_the_worker(monkeypatch, client)

    assert code != int(ExitCode.OK), failed
    cause = _the_item_cause(job_id)
    assert cause is not None and cause.reason == "label-sweep-incomplete"
    assert "Harbour Lights" in cause.message
    assert "get_ep_singles" in cause.message
    # Waiting cannot give a client a method it does not have.
    assert cause.retryable is False
    assert cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert _offered() == {"own1"}


def test_a_crawl_that_read_everything_still_succeeds(cfg, monkeypatch):
    """The control for both: the same shape with nothing unread is a clean sweep."""
    del cfg
    steady = ProviderArtist("Steady Act", [Release("b1", copyright=HARBOUR)], artist_id="10")
    client = _label_with_a_discovered_pair(steady)

    code, done, job_id = _sweep_through_the_worker(monkeypatch, client)

    assert code == int(ExitCode.OK), done
    assert _the_item_cause(job_id) is None
    assert _offered() == {"own1", "a1", "b1"}


def test_a_crawl_that_skipped_a_listing_moves_no_watermark(cfg, monkeypatch):
    """The labels source offers and never acquires, so no watermark moves, skip or not."""
    busy = RateLimitedArtist("Busy Act", [], artist_id="10")

    _sweep_through_the_worker(monkeypatch, _label_with_a_discovered_pair(busy))

    assert watermarks.WatermarkStore(cfg).all() == {}


def test_a_plain_artist_object_missing_one_listing_is_recorded_by_the_source(cfg):
    """R-261 without the roster: an object handed straight to the source."""
    entry = labels.LabelEntry(label_id="harbour", name="Harbour Lights")
    source = sweep.LabelSource(
        cfg,
        registry=labels.Registry(labels={entry.label_id: entry}),
        artists={entry.label_id: AlbumsOnlyArtist("Harbour Lights", [Release("own1")])},
        verify=lambda claimed, release: {"resolved_label": claimed, "source": "test"},
    )

    found = source.list_recent(-1)

    assert [item.identity for item in found] == ["own1"]
    assert [(one.artist, one.listing) for one in source.unread] == [
        ("Harbour Lights", "get_ep_singles")
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Structural guards over the adapter's own source
# ═══════════════════════════════════════════════════════════════════════════


def _tree() -> ast.Module:
    return ast.parse(ADAPTER_SOURCE.read_text(encoding="utf-8"))


def test_the_adapter_pages_nothing_by_hand():
    """Every paged read goes through ``listing``; a direct call here is a fourth loop."""
    guarded = set(listing.GUARDED_METHODS) | {"items"}
    calls = [
        (node.lineno, node.func.attr)
        for node in ast.walk(_tree())
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in guarded
    ]
    assert calls == [], f"the adapter calls a paging method directly: {calls}"


def test_the_paging_scan_can_see_a_violation():
    """The guard above is only worth something if it fires on the shape it forbids."""
    planted = ast.parse("def f(artist):\n    return artist.get_albums(limit=1, offset=0)\n")
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in listing.GUARDED_METHODS
        for node in ast.walk(planted)
    )


def test_the_adapter_imports_nothing_vendored():
    imported: list[str] = []
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert imported, "the scan read no imports at all"
    assert not [name for name in imported if "_vendor" in name], imported


# ═══════════════════════════════════════════════════════════════════════════
# End to end: intake a playlist, then hand its document to the download verb
# ═══════════════════════════════════════════════════════════════════════════


def test_intake_playlist_queues_one_item_per_track_and_download_accepts_the_document(
    cfg, monkeypatch, tmp_path
):
    tracks = [
        ProviderTrack("201", "Aurora Bloom", "Sun Path", isrc="XX0000000001"),
        ProviderTrack("202", "Nova Reef", "Tide", isrc="XX0000000002"),
        ProviderTrack("203", "Mira Vale", "Glass Hour", isrc="XX0000000003"),
    ]
    use_client(monkeypatch, FakeClient(playlists={PLAYLIST: ProviderPlaylist(tracks)}))
    record_session()

    code, envelope = drive(["intake", "playlist", f"https://tidal.com/browse/playlist/{PLAYLIST}"])

    assert code == int(ExitCode.OK), envelope
    with jobs.open_store() as store:
        job = jobs.get(store, envelope["data"]["job_id"])
        items = jobs.items(store, job.job_id)
    assert [item.item_id for item in items] == ["201", "202", "203"]
    frozen = job.payload[intake_cli.TRACKS]

    document = tmp_path / "playlist.json"
    document.write_text(
        json.dumps(
            {
                "list": 1,
                "origin": "tidal",
                "tracks": [
                    {
                        "id": track["ref"],
                        "title": track["title"],
                        "artists": [{"name": track["artist"]}],
                        "isrc": track["isrc"],
                    }
                    for track in frozen.values()
                ],
            }
        )
    )
    code, queued = drive(["acquire", "download", str(document)])
    assert code == int(ExitCode.OK), queued
    with jobs.open_store() as store:
        assert len(jobs.items(store, queued["data"]["job_id"])) == 3


def test_the_review_queue_is_untouched_by_a_playlist_intake(cfg, monkeypatch):
    """Intake lists and queues; offering anything for review is not its act."""
    use_client(
        monkeypatch,
        FakeClient(playlists={PLAYLIST: ProviderPlaylist([ProviderTrack("201", "A", "B")])}),
    )
    record_session()
    code, envelope = drive(["intake", "playlist", PLAYLIST])
    assert code == int(ExitCode.OK), envelope
    with review.open_store(cfg) as queue:
        assert list(review.list_items(queue)) == []


# ═══════════════════════════════════════════════════════════════════════════
# U75: one release read again by identifier
# ═══════════════════════════════════════════════════════════════════════════


class ProviderAlbum:
    """An album that pages its tracks and declares how many it counts."""

    def __init__(self, album_id: str, tracks: list[ProviderTrack], **dated: Any) -> None:
        self.id = album_id
        self._tracks = list(tracks)
        self.num_tracks = len(self._tracks)
        self.served: list[tuple[int | None, int]] = []
        for name, value in dated.items():
            setattr(self, name, value)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[ProviderTrack]:
        self.served.append((limit, offset))
        size = 100 if limit is None else limit
        return self._tracks[offset : offset + size]


class AlbumClient(FakeClient):
    """Answers ``album`` from a script of albums and exceptions, in order."""

    def __init__(self, *answers: Any) -> None:
        super().__init__()
        self.answers = list(answers)
        self.album_reads: list[str] = []

    def album(self, album_id: str) -> Any:
        self.album_reads.append(album_id)
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


@pytest.fixture
def pauses(monkeypatch) -> list[float]:
    """The retry ladder's waits, recorded instead of slept."""
    waited: list[float] = []
    monkeypatch.setattr(tidal_catalogue, "_pause", waited.append)
    return waited


def album_tracks(count: int) -> list[ProviderTrack]:
    return [ProviderTrack(str(700 + n), f"Act {n}", f"Title {n}") for n in range(count)]


def test_a_release_is_paged_to_its_declared_count_and_carries_its_year(pauses):
    album = ProviderAlbum("r-1", album_tracks(230), year=2021)
    adapter = tidal_catalogue.TidalCatalogue(AlbumClient(album))

    tracks, year = adapter.release_tracks("r-1")

    assert year == 2021
    assert len(tracks) == 230, "the release was not paged to exhaustion"
    assert [offset for _limit, offset in album.served] == [0, 100, 200]
    wanted = match.read_tidal_tracks(tracks)
    assert (wanted[0].ref, wanted[0].artist, wanted[0].title) == ("700", "Act 0", "Title 0")
    assert wanted[-1].ref == "929"
    assert pauses == []


def test_a_release_that_is_gone_raises_at_once_and_is_never_retried(pauses):
    client = AlbumClient(ObjectNotFound("album r-gone"))
    adapter = tidal_catalogue.TidalCatalogue(client)

    with pytest.raises(tidal_catalogue.ReleaseUnresolvable) as excinfo:
        adapter.release_tracks("r-gone")

    assert isinstance(excinfo.value, LookupError)
    assert "'r-gone'" in str(excinfo.value)
    assert client.album_reads == ["r-gone"]
    assert pauses == []


def test_a_release_the_client_returns_nothing_for_raises_too(pauses):
    adapter = tidal_catalogue.TidalCatalogue(AlbumClient(None))
    with pytest.raises(tidal_catalogue.ReleaseUnresolvable):
        adapter.release_tracks("r-1")


def test_a_rate_limited_album_read_waits_and_is_asked_again(pauses):
    album = ProviderAlbum("r-1", album_tracks(3), year=2020)
    client = AlbumClient(RuntimeError("429 too many requests"), album)
    adapter = tidal_catalogue.TidalCatalogue(client)

    tracks, year = adapter.release_tracks("r-1")

    assert (len(tracks), year) == (3, 2020)
    assert client.album_reads == ["r-1", "r-1"]
    assert pauses == [1.0]


def test_an_outage_is_re_raised_as_the_provider_raised_it_once_the_ladder_is_spent(pauses):
    client = AlbumClient(ConnectionError("the provider timed out"))
    adapter = tidal_catalogue.TidalCatalogue(client)

    with pytest.raises(ConnectionError):
        adapter.release_tracks("r-1")

    assert len(client.album_reads) == 6
    assert pauses == [1.0, 2.0, 4.0, 8.0, 16.0]


@pytest.mark.parametrize("blank", ["", "   ", None])
def test_no_identifier_is_refused_before_the_provider_is_asked(blank, pauses):
    client = AlbumClient(ProviderAlbum("r-1", album_tracks(1), year=2020))
    with pytest.raises(tidal_catalogue.ReleaseUnresolvable):
        tidal_catalogue.TidalCatalogue(client).release_tracks(blank)
    assert client.album_reads == []


def test_a_short_window_in_the_middle_of_a_release_does_not_end_it(pauses):
    """The provider counts a track it will not serve and omits it from the window."""

    class Withholding(ProviderAlbum):
        def tracks(self, limit: int | None = None, offset: int = 0) -> list[ProviderTrack]:
            page = super().tracks(limit, offset)
            return page[:-1] if offset == 0 else page

    album = Withholding("r-1", album_tracks(150), year=2020)
    tracks, _year = tidal_catalogue.TidalCatalogue(AlbumClient(album)).release_tracks("r-1")

    assert len(tracks) == 149
    assert tracks[-1].id == "849"


class Dated:
    def __init__(self, year: int) -> None:
        self.year = year


@pytest.mark.parametrize(
    ("dated", "expected"),
    [
        ({"year": 2021}, 2021),
        ({"year": "2019"}, 2019),
        ({"year": None, "release_date": Dated(2018)}, 2018),
        ({"year": None, "release_date": "2017-03-04"}, 2017),
        ({"release_date": "2016-01-01T00:00:00"}, 2016),
        ({"year": 0, "release_date": "2015-06-01"}, 2015),
        ({"year": True}, None),
        ({"year": "soon"}, None),
        ({"year": 99999}, None),
        ({}, None),
    ],
    ids=[
        "int", "text", "date-object", "date-text", "no-year-field", "zero-falls-through",
        "boolean", "words", "five-digits", "nothing",
    ],
)
def test_the_year_is_read_or_is_none_and_is_never_a_guess(dated, expected, pauses):
    album = ProviderAlbum("r-1", album_tracks(1), **dated)
    _tracks, year = tidal_catalogue.TidalCatalogue(AlbumClient(album)).release_tracks("r-1")
    assert year == expected


class Rejected(Exception):
    """An HTTP failure in the client's shape: a status, and the URL in its text."""

    def __init__(self, status_code: int, album_id: str) -> None:
        super().__init__(
            f"{status_code} Client Error for url: https://api.example.invalid/v1/albums/{album_id}"
        )
        self.response = Response(status_code)


def test_an_identifier_holding_the_digits_404_does_not_make_a_rejection_a_withdrawal(pauses):
    """The request URL carries the release identifier into the error's text."""
    client = AlbumClient(Rejected(401, "24040417"))
    adapter = tidal_catalogue.TidalCatalogue(client)

    with pytest.raises(Rejected):
        adapter.release_tracks("24040417")

    assert len(client.album_reads) == 6, "a rejection was answered once, as gone"


def test_a_404_status_is_gone_whatever_the_class_is_called(pauses):
    client = AlbumClient(Rejected(404, "r-gone"))
    with pytest.raises(tidal_catalogue.ReleaseUnresolvable):
        tidal_catalogue.TidalCatalogue(client).release_tracks("r-gone")
    assert client.album_reads == ["r-gone"]


def test_the_adapter_raises_the_seams_own_exception():
    assert tidal_catalogue.ReleaseUnresolvable is catalogue.ReleaseUnresolvable


def test_the_adapter_and_the_verb_meet_over_a_gone_release(cfg, monkeypatch, pauses):
    """The seam's ``LookupError`` contract, driven from the live adapter's side."""
    from cratekit.label import approved_cli

    adapter = tidal_catalogue.TidalCatalogue(AlbumClient(ObjectNotFound("album r-gone")))
    release = approved_cli._Release(
        item_id="ri_1", release_id="r-gone", title="", label_id=None, label_name=None
    )

    outcome = approved_cli._tracks_or_failure(adapter, release)

    assert isinstance(outcome, approved_cli._Failed)
    assert outcome.kind == approved_cli.GONE


# ═══════════════════════════════════════════════════════════════════════════
# U78: the tracks one ISRC is filed under
# ═══════════════════════════════════════════════════════════════════════════


class IsrcClient(FakeClient):
    """Answers ``get_tracks_by_isrc`` from a script of answers and exceptions."""

    def __init__(self, *answers: Any) -> None:
        super().__init__()
        self.answers = list(answers)
        self.isrc_reads: list[str] = []

    def get_tracks_by_isrc(self, isrc: str) -> Any:
        self.isrc_reads.append(isrc)
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


def test_an_isrc_answers_every_track_filed_under_it(pauses):
    tracks = [ProviderTrack("9001", "A", "B"), ProviderTrack("9002", "A", "B")]
    client = IsrcClient(tracks)

    found = tidal_catalogue.TidalCatalogue(client).tracks_for_isrc("QZAAA2600001")

    assert [track.id for track in found] == ["9001", "9002"]
    assert client.isrc_reads == ["QZAAA2600001"]
    assert pauses == []


def test_an_isrc_filed_under_nothing_is_an_empty_answer_asked_once(pauses):
    client = IsrcClient(ObjectNotFound("no track"))

    assert tidal_catalogue.TidalCatalogue(client).tracks_for_isrc("QZAAA2600001") == ()
    assert client.isrc_reads == ["QZAAA2600001"]
    assert pauses == []


def test_a_rate_limited_isrc_read_waits_and_is_asked_again(pauses):
    client = IsrcClient(TooManyRequests("slow down"), [ProviderTrack("9001", "A", "B")])

    found = tidal_catalogue.TidalCatalogue(client).tracks_for_isrc("QZAAA2600001")

    assert [track.id for track in found] == ["9001"]
    assert pauses == [1.0]


def test_invalid_isrc_is_not_read_as_no_track_since_the_client_hides_outages_behind_it(pauses):
    """At 0.8.11 the client raises ``InvalidISRC`` for every HTTP error but 404
    and 429, a server error and a rejected session among them."""
    client = IsrcClient(tidalapi.exceptions.InvalidISRC())

    with pytest.raises(tidalapi.exceptions.InvalidISRC):
        tidal_catalogue.TidalCatalogue(client).tracks_for_isrc("QZAAA2600001")

    assert len(client.isrc_reads) == 6
    assert pauses == [1.0, 2.0, 4.0, 8.0, 16.0]


@pytest.mark.parametrize("blank", ["", "   ", None])
def test_no_isrc_is_refused_before_the_provider_is_asked(blank, pauses):
    client = IsrcClient([])
    with pytest.raises(ValueError):
        tidal_catalogue.TidalCatalogue(client).tracks_for_isrc(blank)
    assert client.isrc_reads == []


def test_a_client_with_no_isrc_lookup_refuses_at_once_and_never_climbs_the_ladder(pauses):
    with pytest.raises(LookupError):
        tidal_catalogue.TidalCatalogue(FakeClient()).tracks_for_isrc("QZAAA2600001")
    assert pauses == []


# ═══════════════════════════════════════════════════════════════════════════
# U79: a text search for one artist and title
# ═══════════════════════════════════════════════════════════════════════════


class TrackSearchClient(FakeClient):
    """Answers ``search`` from a script of answers and exceptions."""

    def __init__(self, *answers: Any) -> None:
        super().__init__()
        self.answers = list(answers)
        self.track_searches: list[tuple[str, tuple[Any, ...], int]] = []

    def search(self, query: str, models: Any = None, limit: int = 50, **_: Any) -> Any:
        self.track_searches.append((query, tuple(models or ()), limit))
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


def test_a_track_search_returns_every_hit_in_the_providers_order_and_picks_none(pauses):
    hits = [ProviderTrack("9002", "A", "B (Remix)"), ProviderTrack("9001", "A", "B")]
    client = TrackSearchClient({"tracks": hits, "top_hit": hits[0]})

    found = tidal_catalogue.TidalCatalogue(client).search_tracks(" A ", " B ")

    assert [track.id for track in found] == ["9002", "9001"]
    assert client.track_searches == [
        ("A B", (tidalapi.media.Track,), tidal_catalogue.SEARCH_LIMIT)
    ]
    assert pauses == []


def test_a_track_search_that_finds_nothing_is_an_empty_answer(pauses):
    client = TrackSearchClient({"tracks": []})

    assert tidal_catalogue.TidalCatalogue(client).search_tracks("A", "B") == ()
    assert pauses == []


def test_a_rate_limited_track_search_waits_and_is_asked_again(pauses):
    client = TrackSearchClient(TooManyRequests("slow down"), {"tracks": [ProviderTrack("9001", "A", "B")]})

    found = tidal_catalogue.TidalCatalogue(client).search_tracks("A", "B")

    assert [track.id for track in found] == ["9001"]
    assert pauses == [1.0]


def test_a_track_search_that_keeps_failing_is_raised_and_a_not_found_is_no_answer(pauses):
    """A search endpoint answers nothing found with an empty list, so a raised
    not found is the endpoint failing, and read as empty it would report a track
    the provider carries as having no candidate."""
    client = TrackSearchClient(ObjectNotFound("search"))

    with pytest.raises(ObjectNotFound):
        tidal_catalogue.TidalCatalogue(client).search_tracks("A", "B")

    assert len(client.track_searches) == 6


def test_a_search_answer_with_no_track_listing_is_raised_at_once_and_is_not_empty(pauses):
    client = TrackSearchClient({"artists": []})

    with pytest.raises(LookupError):
        tidal_catalogue.TidalCatalogue(client).search_tracks("A", "B")

    assert len(client.track_searches) == 1, "a shape was waited on"
    assert pauses == []


@pytest.mark.parametrize(("artist", "title"), [("", ""), ("  ", None), (None, " ")])
def test_a_search_for_nothing_is_refused_before_the_provider_is_asked(artist, title, pauses):
    client = TrackSearchClient({"tracks": []})
    with pytest.raises(ValueError):
        tidal_catalogue.TidalCatalogue(client).search_tracks(artist, title)
    assert client.track_searches == []
