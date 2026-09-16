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

import pytest

from cratekit.acquire import listing, match, provider_session
from cratekit.core import config, jobs, review, secrets
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue, sweep, tidal_catalogue
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.sync import run
from tests.cli_drive import drive
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
    def __init__(self, name: str) -> None:
        self.name = name


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
    def __init__(self, release_id: str, *, copyright: str = "", year: str = "2026") -> None:
        self.id = release_id
        self.copyright = copyright
        self.year = year
        self.name = f"Release {release_id}"


class ProviderArtist:
    """An artist page whose listings truncate to one page without arguments."""

    def __init__(self, name: str, albums: list[Release], singles: list[Release] = ()) -> None:
        self.name = name
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
    ) -> None:
        self.accept = accept
        self.raises = raises
        self.playlists = dict(playlists or {})
        self.artists = list(artists or [])
        self.albums = list(albums or [])
        self.logins: list[dict] = []
        self.searches: list[str] = []
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
        del models, limit, offset
        self.searches.append(query)
        return {
            "artists": [artist for artist in self.artists if query.casefold() in artist.name.casefold()],
            "albums": list(self.albums),
        }

    def album(self, album_id: str) -> Release:
        for album in self.albums:
            if album.id == album_id:
                return album
        raise MissingObject(album_id)


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
