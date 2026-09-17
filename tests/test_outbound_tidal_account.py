"""U63: the provider account adapter behind the outbound seam, driven against fakes.

Every scenario the unit's brief names is here, and none of them reaches the
provider. The client is a fake injected at ``provider_session.CLIENT_FACTORY``,
the one place a client is built, so the adapter under test is the shipped class
over a stand in for the network. The live sweep and the live export belong to the
attended sitting and are recorded in ``docs/cutover.md``, not claimed here.

**ONE SUBSTITUTION BEYOND THE CLIENT, AND IT IS NAMED.** The end to end drives
give the export's rows an ISRC through ``source.local_tracks`` and
``source.heart_candidates``, because a rekordbox collection export carries none
and the adapter matches nothing without one. That is the shipped build's real
behaviour and it is a residual, not something this file hides: the drives with no
ISRC are here too, and they match nothing.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.acquire import listing, provider_session
from cratekit.core import config, jobs, locations, secrets, tags
from cratekit.core.cause import CratekitError, Scope
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import account, artifacts, ledger, source, tidal_account
from cratekit.modules.outbound.service import RemoteAccount
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive
from tests.test_config import valid_data

ADAPTER_SOURCE = Path(tidal_account.__file__)

STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 946684800.0,
}


# ═══════════════════════════════════════════════════════════════════════════
# Fakes: a provider client that answers from memory and counts what it is asked
# ═══════════════════════════════════════════════════════════════════════════


class ObjectNotFound(Exception):
    """Named as the client names its not found, which is how the adapter reads it."""


class Response:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class HTTPFailure(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"HTTP {status_code}")
        self.response = Response(status_code)


class Track:
    def __init__(self, track_id: str) -> None:
        self.id = int(track_id)


class Playlist:
    """An owned playlist that pages its tracks and records every add."""

    def __init__(self, playlist_id: str, members: list[str] = ()) -> None:
        self.id = playlist_id
        self.members = list(members)
        self.adds: list[list[str]] = []
        self.pages: list[tuple[int, int]] = []

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Track]:
        size = 100 if limit is None else limit
        self.pages.append((size, offset))
        return [Track(member) for member in self.members[offset : offset + size]]

    def add(self, media_ids: list[str], allow_duplicates: bool = False) -> list[str]:
        del allow_duplicates
        self.adds.append(list(media_ids))
        self.members.extend(media_ids)
        return list(media_ids)


class Favorites:
    def __init__(self, hearts: list[str]) -> None:
        self.hearts = list(hearts)
        self.pages: list[tuple[int, int]] = []
        self.added: list[str] = []
        self.fail: list[Exception] = []

    def tracks(self, limit: int = 50, offset: int = 0) -> list[Track]:
        self.pages.append((limit, offset))
        return [Track(heart) for heart in self.hearts[offset : offset + limit]]

    def add_track(self, track_id: str) -> bool:
        self.added.append(track_id)
        if self.fail:
            raise self.fail.pop(0)
        self.hearts.append(track_id)
        return True


class User:
    def __init__(self, client: FakeClient, hearts: list[str]) -> None:
        self._client = client
        self.favorites = Favorites(hearts)
        self.created: list[str] = []
        self.create_fail: Exception | None = None

    def create_playlist(self, title: str, description: str) -> Playlist:
        del description
        self.created.append(title)
        if self.create_fail is not None:
            raise self.create_fail
        playlist = Playlist(f"00000000-0000-4000-8000-{len(self.created):012d}")
        self._client.playlists[playlist.id] = playlist
        return playlist


class FakeClient:
    def __init__(
        self,
        *,
        isrcs: dict[str, list[str]] | None = None,
        tracks: set[str] | None = None,
        hearts: list[str] = (),
        playlists: dict[str, Playlist] | None = None,
        login_raises: Exception | None = None,
    ) -> None:
        self.isrcs = dict(isrcs or {})
        self.tracks = set(tracks or ())
        self.playlists = dict(playlists or {})
        self.user = User(self, list(hearts))
        self.login_raises = login_raises
        self.logins = 0
        self.isrc_asked: list[str] = []
        self.track_asked: list[str] = []
        self.token_type = self.access_token = self.refresh_token = self.expiry_time = None

    def load_oauth_session(self, token_type, access_token, refresh_token=None,
                           expiry_time=None, is_pkce=False) -> bool:
        del token_type, access_token, refresh_token, expiry_time, is_pkce
        self.logins += 1
        if self.login_raises is not None:
            raise self.login_raises
        return True

    def get_tracks_by_isrc(self, isrc: str) -> list[Track]:
        self.isrc_asked.append(isrc)
        if isrc not in self.isrcs:
            raise ObjectNotFound(isrc)
        return [Track(track_id) for track_id in self.isrcs[isrc]]

    def track(self, track_id: str) -> Track:
        self.track_asked.append(track_id)
        if track_id not in self.tracks:
            raise ObjectNotFound(track_id)
        return Track(track_id)

    def playlist(self, playlist_id: str) -> Playlist:
        try:
            return self.playlists[playlist_id]
        except KeyError as exc:
            raise ObjectNotFound(playlist_id) from exc


def use_client(monkeypatch, client: FakeClient) -> FakeClient:
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    return client


def record_session() -> None:
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))


def no_sleep(seconds: float) -> None:
    del seconds


def adapter(client: FakeClient) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(client, sleep=no_sleep)


@pytest.fixture
def installed(tmp_path, monkeypatch) -> config.Config:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    built = config.from_dict(valid_data(root, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    source.forget_libraries()
    yield built
    source.forget_libraries()


# ═══════════════════════════════════════════════════════════════════════════
# 1. The seam
# ═══════════════════════════════════════════════════════════════════════════


def test_a_recorded_session_resolves_the_adapter_and_the_build_is_bound(
    installed, monkeypatch
):
    client = use_client(monkeypatch, FakeClient())
    record_session()

    found = account.resolve(installed)

    assert account.bound() is True
    assert isinstance(found, tidal_account.TidalAccount)
    assert all(callable(getattr(found, name)) for name in outbound_fakes.PROTOCOL_METHODS)
    assert client.logins == 1


def test_one_process_logs_in_once_however_many_items_resolve(installed, monkeypatch):
    client = use_client(monkeypatch, FakeClient())
    record_session()

    first = account.resolve(installed)
    assert account.resolve(installed) is first
    assert client.logins == 1

    account.forget()
    assert account.resolve(installed) is not first
    assert client.logins == 2


def test_with_no_session_the_seam_refuses_the_credential_and_logs_nothing_in(
    installed, monkeypatch
):
    client = use_client(monkeypatch, FakeClient())

    with pytest.raises(CratekitError) as excinfo:
        account.resolve(installed)

    assert excinfo.value.cause.reason == "credential-missing"
    assert client.logins == 0


def test_a_session_removed_after_an_open_is_refused_rather_than_reused(
    installed, monkeypatch
):
    use_client(monkeypatch, FakeClient())
    record_session()
    account.resolve(installed)
    monkeypatch.setattr(secrets, "exists", lambda name: False)

    with pytest.raises(CratekitError) as excinfo:
        account.resolve(installed)

    assert excinfo.value.cause.reason == "credential-missing"


@pytest.mark.parametrize(
    ("failure", "reason"),
    [
        (HTTPFailure(401), "credential-missing"),
        (ConnectionError("refused"), "unavailable-transient"),
    ],
    ids=["rejected", "unreachable"],
)
def test_a_login_that_fails_names_whether_to_log_in_again_or_wait(
    installed, monkeypatch, failure, reason
):
    use_client(monkeypatch, FakeClient(login_raises=failure))
    record_session()

    with pytest.raises(CratekitError) as excinfo:
        account.resolve(installed)

    assert excinfo.value.cause.reason == reason
    with pytest.raises(CratekitError):
        account.resolve(installed)


# ═══════════════════════════════════════════════════════════════════════════
# 2. Matching is exact or it is None
# ═══════════════════════════════════════════════════════════════════════════


def test_an_isrc_naming_one_track_is_the_match():
    client = FakeClient(isrcs={"AA0000000001": ["101", "101"]})
    assert adapter(client).match_track(identity="7", isrc="AA0000000001") == "101"
    assert client.track_asked == []


def test_an_isrc_naming_two_tracks_is_no_match_rather_than_the_first():
    client = FakeClient(
        isrcs={"AA0000000001": ["101", "202"]}, tracks={"101"}
    )
    found = adapter(client).match_track(
        identity="https://tidal.com/browse/track/101", isrc="AA0000000001"
    )
    assert found is None


def test_an_isrc_the_provider_lacks_falls_back_to_an_exact_track_reference():
    client = FakeClient(tracks={"303"})
    found = adapter(client).match_track(
        identity="https://listen.tidal.com/track/303", isrc="ZZ0000000009"
    )
    assert found == "303"
    assert client.isrc_asked == ["ZZ0000000009"], "a not found must not be retried"


def test_a_bare_row_identifier_is_never_read_as_a_provider_track():
    """A rekordbox TrackID is a bare number, and so is a provider track id."""
    client = FakeClient(tracks={"42"})
    assert adapter(client).match_track(identity="42") is None
    assert client.track_asked == []


@pytest.mark.parametrize(
    "identity",
    [
        "https://example.com/browse/track/42",
        "https://tidal.com/browse/album/42",
        "tidal.com/browse/track/42",
        "https://tidal.com/browse/track/42abc",
        "",
    ],
)
def test_nothing_but_a_provider_track_url_is_a_reference(identity):
    assert tidal_account.track_reference(identity) is None


def test_a_reference_to_a_track_the_provider_lacks_is_no_match():
    client = FakeClient()
    assert adapter(client).match_track(identity="https://tidal.com/track/9") is None
    assert client.track_asked == ["9"]


def test_a_reference_the_provider_answers_with_another_track_is_no_match():
    """A lookup that lands on a different identifier is a redirect, not the track."""
    client = FakeClient(tracks={"9"})
    client.track = lambda track_id: Track("10")
    assert adapter(client).match_track(identity="https://tidal.com/track/9") is None


class InvalidISRC(Exception):
    """Named as the client names an ISRC it will not accept."""


def test_an_isrc_the_provider_will_not_accept_is_no_match_and_is_not_retried():
    client = FakeClient()
    asked: list[str] = []

    def refuse_isrc(isrc: str):
        asked.append(isrc)
        raise InvalidISRC(isrc)

    client.get_tracks_by_isrc = refuse_isrc
    assert adapter(client).match_track(identity="1", isrc="bad") is None
    assert asked == ["bad"]


def test_a_row_with_neither_an_isrc_nor_a_reference_asks_the_provider_nothing():
    client = FakeClient(isrcs={"AA0000000001": ["101"]})
    assert adapter(client).match_track(identity="1", isrc="") is None
    assert client.isrc_asked == [] and client.track_asked == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. One paged read answers every heart question
# ═══════════════════════════════════════════════════════════════════════════


def test_has_heart_answers_a_whole_sweep_from_one_paged_read():
    hearts = [str(1000 + index) for index in range(250)]
    client = FakeClient(hearts=hearts)
    remote = adapter(client)

    answers = [remote.has_heart(str(1000 + index)) for index in range(400)]

    assert answers == [index < 250 for index in range(400)]
    # U65: the walk now ends on the empty page at offset 300, not on the short
    # page at 200. One extra request for the whole sweep, and the point of the
    # test is unchanged: 400 questions cost one walk.
    assert client.user.favorites.pages == [(100, 0), (100, 100), (100, 200), (100, 300)]


def test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one():
    client = FakeClient(hearts=["5"])
    remote = adapter(client)

    remote.add_heart("5")
    assert client.user.favorites.added == []

    remote.add_heart("6")
    remote.add_heart("6")
    assert client.user.favorites.added == ["6"]
    assert remote.has_heart("6") is True
    # One complete walk and no second one. Under U65 a complete walk over a
    # corpus this small is two requests, the page and the empty page that ends
    # it; a cache miss would show a second (100, 0).
    assert client.user.favorites.pages == [(100, 0), (100, 100)]


def test_a_member_already_on_the_playlist_makes_no_write():
    playlist = Playlist("00000000-0000-4000-8000-00000000000a", ["11", "12"])
    client = FakeClient(playlists={playlist.id: playlist})
    remote = adapter(client)

    remote.add_to_playlist(playlist.id, "12")
    assert playlist.adds == []

    remote.add_to_playlist(playlist.id, "13")
    remote.add_to_playlist(playlist.id, "13")
    assert playlist.adds == [["13"]]
    assert remote.playlist_tracks(playlist.id) == ("11", "12", "13")
    # One complete walk and no second one. Under U65 a complete walk over a
    # corpus this small is two requests, the page and the empty page that ends
    # it; a cache miss would show a second (100, 0).
    assert playlist.pages == [(100, 0), (100, 100)]


def test_a_created_playlist_returns_the_identifier_the_provider_assigned():
    client = FakeClient()
    remote = adapter(client)

    created = remote.create_playlist("Crate")

    assert created == "00000000-0000-4000-8000-000000000001"
    assert client.user.created == ["Crate"]
    assert remote.playlist_tracks(created) == ()


# ═══════════════════════════════════════════════════════════════════════════
# 4. A provider failure is the item's cause, with one retry on a write
# ═══════════════════════════════════════════════════════════════════════════


def test_a_write_the_provider_refuses_once_is_retried_once_and_lands():
    client = FakeClient()
    client.user.favorites.fail = [HTTPFailure(429)]
    adapter(client).add_heart("8")
    assert client.user.favorites.added == ["8", "8"]


def test_a_write_refused_twice_is_the_items_cause_and_is_not_tried_a_third_time():
    client = FakeClient()
    client.user.favorites.fail = [HTTPFailure(429), HTTPFailure(429), HTTPFailure(429)]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    assert client.user.favorites.added == ["8", "8"]
    assert excinfo.value.cause.reason == "unavailable-transient"
    assert excinfo.value.cause.scope is Scope.ITEM


def test_a_rejected_session_mid_sweep_asks_for_a_login_at_item_scope():
    client = FakeClient()
    client.user.favorites.fail = [HTTPFailure(401), HTTPFailure(401)]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    assert excinfo.value.cause.reason == "credential-missing"
    assert excinfo.value.cause.scope is Scope.ITEM


def test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session():
    client = FakeClient()
    try:
        raise HTTPFailure(401)
    except HTTPFailure as inner:
        wrapped = RuntimeError("the client's own error")
        wrapped.__cause__ = inner
    client.user.favorites.fail = [wrapped, wrapped]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    assert excinfo.value.cause.reason == "credential-missing"


def test_a_heart_the_client_answers_false_is_not_recorded_as_held():
    client = FakeClient()
    client.user.favorites.add_track = lambda track_id: False
    remote = adapter(client)

    with pytest.raises(CratekitError):
        remote.add_heart("8")
    assert remote.has_heart("8") is False


def test_a_playlist_create_is_never_retried_into_a_second_playlist():
    client = FakeClient()
    client.user.create_fail = TimeoutError("timed out")

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).create_playlist("Crate")

    assert client.user.created == ["Crate"]
    assert excinfo.value.cause.reason == "unavailable-transient"


def test_an_add_the_client_answers_with_nothing_is_not_recorded_as_a_member():
    """The client skips a track it cannot find and raises nothing."""
    playlist = Playlist("00000000-0000-4000-8000-00000000000b", ["11"])
    playlist.add = lambda media_ids, allow_duplicates=False: []
    client = FakeClient(playlists={playlist.id: playlist})
    remote = adapter(client)

    with pytest.raises(CratekitError) as excinfo:
        remote.add_to_playlist(playlist.id, "14")

    assert excinfo.value.cause.scope is Scope.ITEM
    assert remote.playlist_tracks(playlist.id) == ("11",)


def test_an_empty_answer_for_a_track_the_playlist_now_holds_is_not_a_failure():
    playlist = Playlist("00000000-0000-4000-8000-00000000000c", ["11"])

    def add_elsewhere(media_ids, allow_duplicates=False):
        del allow_duplicates
        playlist.members.extend(media_ids)
        return []

    playlist.add = add_elsewhere
    client = FakeClient(playlists={playlist.id: playlist})
    remote = adapter(client)

    remote.add_to_playlist(playlist.id, "15")

    assert remote.playlist_tracks(playlist.id) == ("11", "15")


def test_an_add_to_a_playlist_deleted_mid_run_is_the_items_cause():
    playlist = Playlist("00000000-0000-4000-8000-00000000000d", ["11"])

    def gone(media_ids, allow_duplicates=False):
        raise ObjectNotFound(playlist.id)

    playlist.add = gone
    client = FakeClient(playlists={playlist.id: playlist})
    remote = adapter(client)

    with pytest.raises(CratekitError) as excinfo:
        remote.add_to_playlist(playlist.id, "16")

    assert excinfo.value.cause.reason == "unavailable-transient"
    assert "16" not in remote.playlist_tracks(playlist.id)


def test_a_bad_request_on_a_write_is_not_read_as_a_rejected_session():
    client = FakeClient()
    client.user.favorites.fail = [HTTPFailure(400), HTTPFailure(400)]

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).add_heart("8")

    assert excinfo.value.cause.reason == "unavailable-transient"


def test_a_session_rejected_mid_run_drops_the_held_account(installed, monkeypatch):
    use_client(monkeypatch, FakeClient())
    record_session()
    held = account.resolve(installed)

    account.provider_failure(HTTPFailure(401), "heart a track")

    assert account.resolve(installed) is not held


def test_a_build_whose_client_library_does_not_import_is_not_bound(monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "tidalapi", None)
    monkeypatch.delitem(sys.modules, account.ADAPTER_MODULE, raising=False)

    assert account.bound() is False


# ═══════════════════════════════════════════════════════════════════════════
# 5. The real workers, end to end, against the fake client
# ═══════════════════════════════════════════════════════════════════════════


def isrc_for(row: str) -> str:
    return f"AA00000000{int(row):02d}"


def give_rows_an_isrc(monkeypatch) -> None:
    """The one substitution beyond the client. See the module docstring."""
    real_tracks = source.local_tracks
    real_candidates = source.heart_candidates

    def tracks(library, track_ids, *, cfg):
        return tuple(
            replace(track, isrc=isrc_for(track.identity))
            for track in real_tracks(library, track_ids, cfg=cfg)
        )

    def candidates(library, track_ids, *, cfg):
        return tuple(
            replace(item, isrc=isrc_for(item.row_id))
            for item in real_candidates(library, track_ids, cfg=cfg)
        )

    monkeypatch.setattr(source, "local_tracks", tracks)
    monkeypatch.setattr(source, "heart_candidates", candidates)


def _resume(job_id: str) -> tuple[int, dict]:
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    return drive(cli_jobs.argv_for(job))


def export_verb(exported: Path) -> list[str]:
    return ["export", "playlist", outbound_fakes.CRATE, "--export", str(exported)]


def favorites_verb(exported: Path) -> list[str]:
    return ["sync", "favorites", "--export", str(exported)]


def test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart(
    installed, monkeypatch
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1, 2, 3)
    )
    client = use_client(
        monkeypatch,
        FakeClient(
            isrcs={isrc_for(str(row)): [str(500 + row)] for row in (1, 2, 3)},
            hearts=["502"],
        ),
    )
    record_session()
    give_rows_an_isrc(monkeypatch)
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert client.user.favorites.added == ["501", "503"]
    assert ledger.recorded_hearts(installed) == frozenset({"501", "503"})
    assert client.logins == 1
    # One complete walk and no second one. Under U65 a complete walk over a
    # corpus this small is two requests, the page and the empty page that ends
    # it; a cache miss would show a second (100, 0).
    assert client.user.favorites.pages == [(100, 0), (100, 100)]


def test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add(
    installed, monkeypatch
):
    exported = outbound_fakes.write_export(installed.library.root / "outbound")
    client = use_client(
        monkeypatch,
        FakeClient(isrcs={isrc_for(str(row)): [str(700 + row)] for row in (1, 2, 3)}),
    )
    record_session()
    give_rows_an_isrc(monkeypatch)
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert client.user.created == [outbound_fakes.CRATE]
    (playlist,) = client.playlists.values()
    assert playlist.members == ["701", "702", "703"]
    assert playlist.adds == [["701"], ["702"], ["703"]]
    assert ledger.playlist_remote_id(installed, outbound_fakes.CRATE) == playlist.id
    assert ledger.playlist_added(installed, outbound_fakes.CRATE) == frozenset(
        {"701", "702", "703"}
    )
    reports = artifacts.committed(installed, job_id)
    assert [report["remote_id"] for report in reports] == [playlist.id] * 3


def test_a_provider_failure_on_one_heart_fails_that_item_and_no_other(
    installed, monkeypatch
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1, 2, 3)
    )
    client = use_client(
        monkeypatch,
        FakeClient(isrcs={isrc_for(str(row)): [str(500 + row)] for row in (1, 2, 3)}),
    )
    monkeypatch.setattr(tidal_account.time, "sleep", no_sleep)
    real_add = client.user.favorites.add_track

    def add_track(track_id: str) -> bool:
        if track_id == "502":
            raise HTTPFailure(503)
        return real_add(track_id)

    client.user.favorites.add_track = add_track
    record_session()
    give_rows_an_isrc(monkeypatch)
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, _resumed = _resume(job_id)

    assert code != int(ExitCode.OK)
    with jobs.open_store() as store:
        causes = {
            item.item_id: (item.cause.reason if item.cause else None)
            for item in jobs.items(store, job_id)
        }
    assert causes == {"1": None, "2": "unavailable-transient", "3": None}
    assert ledger.recorded_hearts(installed) == frozenset({"501", "503"})


def test_a_row_whose_file_carries_no_isrc_matches_nothing(installed, monkeypatch):
    """No substitution of the rows, and no file behind them.

    Before R-355 closed this was every row, because nothing read an ISRC at all.
    It is now the row whose location names no audio file, and the answer is still
    an honest unmatched row with no call made to the provider.
    """
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1, 2)
    )
    client = use_client(
        monkeypatch,
        FakeClient(isrcs={isrc_for(str(row)): [str(500 + row)] for row in (1, 2)},
                   tracks={"1", "2"}),
    )
    record_session()
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert client.user.favorites.added == []
    assert client.isrc_asked == [] and client.track_asked == []
    reports = artifacts.committed(installed, job_id)
    assert [report["unmatched"] for report in reports] == [["1"], ["2"]]


def _tagged_flac(installed, tmp_path, index: int, isrc: str) -> str:
    """A real FLAC under the library root carrying ``isrc``, as an export location."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    made = synth_container(tmp_path, ".flac")
    target = Path(installed.library.root) / "Music" / f"{index}.flac"
    made.replace(target)
    assert tags.write_tags(target, {"isrc": isrc}) is True
    return locations.location_url(target)


def test_a_sweep_matches_through_the_isrc_the_file_carries(
    installed, monkeypatch, tmp_path
):
    """R-355 closed, driven with no substitution: the ISRC comes off the file.

    Row 1's file carries a hyphenated ISRC and row 2's file carries none, so one
    drive shows the read, the fold, and the untagged row staying unmatched.
    """
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound",
        favorites=(1, 2),
        locations={
            1: _tagged_flac(installed, tmp_path / "one", 1, "aa-000-00-00001"),
            2: _tagged_flac(installed, tmp_path / "two", 2, ""),
        },
    )
    client = use_client(
        monkeypatch,
        FakeClient(isrcs={isrc_for("1"): ["501"], isrc_for("2"): ["502"]}),
    )
    record_session()
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert client.isrc_asked == [isrc_for("1")]
    assert client.user.favorites.added == ["501"]
    reports = artifacts.committed(installed, job_id)
    assert [report["unmatched"] for report in reports] == [[], ["2"]]


# ═══════════════════════════════════════════════════════════════════════════
# 6. Structural guards over the adapter's own source
# ═══════════════════════════════════════════════════════════════════════════


def _tree() -> ast.Module:
    return ast.parse(ADAPTER_SOURCE.read_text(encoding="utf-8"))


def test_the_adapter_imports_nothing_vendored():
    imported: list[str] = []
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert imported, "the scan read no imports at all"
    assert not [name for name in imported if "_vendor" in name], imported


def test_the_adapter_pages_nothing_by_hand():
    calls = [
        (node.lineno, node.func.attr)
        for node in ast.walk(_tree())
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in listing.GUARDED_METHODS
    ]
    assert calls == [], f"the adapter calls a paging method directly: {calls}"


def test_the_adapter_names_no_remove_on_the_client():
    """Add only is the protocol's rule; a remove named here would be a new write."""
    shapes = ("remove", "delete", "unheart", "unlike", "clear")
    named = sorted(
        {
            node.attr
            for node in ast.walk(_tree())
            if isinstance(node, ast.Attribute)
            and any(shape in node.attr.lower() for shape in shapes)
        }
    )
    assert named == [], named


def test_the_adapter_satisfies_the_protocol_it_is_handed_out_as():
    declared = {
        name for name in vars(RemoteAccount) if not name.startswith("_")
    }
    assert declared == outbound_fakes.PROTOCOL_METHODS
    for name in declared:
        assert callable(getattr(tidal_account.TidalAccount, name, None)), name
