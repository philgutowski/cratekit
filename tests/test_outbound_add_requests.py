"""U255. Adding a track to an account playlist costs one write and one read.

THE COST WAS FOUR REQUESTS A TRACK, MEASURED AT THE ADAPTER (the speed survey
of 2026-11-12): the client's ``Session.playlist`` fetches an owned playlist
twice (a ``Playlist``, then the ``UserPlaylist`` its factory builds),
``TidalAccount.add_to_playlist`` opened the playlist afresh for every track,
and the client's own ``add`` reads it a third time after its POST. Every
provider request waits at the gate and counts against the command's ceiling,
so the two wasted requests were two seconds a track and half the ceiling.

The adapter now holds the object its membership read opened, per playlist,
and adds through it. These tests drive the REAL client over a transport that
keeps the account's playlists, moves each one's version tag on every write,
answers a write carrying a tag that is not the current one with 412, as the
provider answers a move (Sitting 62; one live add was answered 412 too, the
U147 mirror build, and whether every add on a stale tag is refused is owed to
an attended sitting), and counts every request by method and path. The request count is the assertion, never a wall clock.

Round one's review drove three things the first transport could not serve,
and the transport serves them now: a write by another writer between the
open and the tracks read, a playlist read or a tracks read served one write
behind, and a tracks read that fails after the open.
"""

from __future__ import annotations

import json
from collections import Counter
from urllib.parse import urlsplit

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError, refuse
from cratekit.modules.outbound import account, export, ledger
from cratekit.modules.outbound.tidal_account import TidalAccount
from tests.test_adapter_listing import OWNER, _logged_in_over, _owned_playlist

requests = pytest.importorskip("requests")


class _Data(dict):
    """A track as the provider serves it: any field the parser asks for and
    the test did not name reads as absent, as ``tests/test_isrc_cache.py`` builds one."""

    def __missing__(self, key):
        return None


def _track(identifier: str) -> _Data:
    return _Data(
        {
            "id": int(identifier),
            "title": f"Track {identifier}",
            "duration": 300,
            "allowStreaming": True,
            "streamReady": True,
            "trackNumber": 1,
            "volumeNumber": 1,
            "artist": {"id": 1, "name": "Aurora Bloom", "type": "MAIN"},
            "artists": [{"id": 1, "name": "Aurora Bloom", "type": "MAIN"}],
            "album": {"id": 77, "title": "Sun Path EP", "cover": None, "videoCover": None},
        }
    )


class _Answer:
    """What ``requests`` hands the client back, as far as the client reads it."""

    def __init__(self, url: str, body: dict, *, status: int = 200, tag: int = 1) -> None:
        self.request = type("Sent", (), {"url": url})()
        self.url = url
        self.status_code = status
        self.ok = status < 400
        self.reason = "Precondition Failed" if status == 412 else "Error"
        self.headers = {"etag": f'"{tag}"'}
        self.text = ""
        self.content = b""
        self._body = body

    def json(self) -> dict:
        return self._body

    def raise_for_status(self) -> None:
        if not self.ok:
            raise requests.HTTPError(f"{self.status_code} {self.reason}", response=self)


class Account:
    """The provider's side of the account's playlists, served to a real client.

    Each playlist holds its track identifiers in order and a version that every
    write moves on. A write whose ``If-None-Match`` is not the current tag is
    answered 412 and changes nothing. An add skips a track the playlist already
    holds and one in ``missing`` (the provider cannot find it), and answers with
    the identifiers it added, as the client asks it to.
    """

    def __init__(self, *uuids: str) -> None:
        self.items: dict[str, list[str]] = {uuid: [] for uuid in uuids}
        self.titles: dict[str, str] = {uuid: f"List {uuid}" for uuid in uuids}
        self.version: dict[str, int] = {uuid: 1 for uuid in uuids}
        self.requests: Counter[tuple[str, str]] = Counter()
        #: Every add as sent: the playlist, the form, and the tag it carried.
        self.adds: list[tuple[str, dict, str | None]] = []
        #: Track identifiers the provider cannot find, which an add skips.
        self.missing: set[str] = set()
        #: Statuses the next adds are answered with, in order, changing nothing.
        self.refusals: list[int] = []
        #: Answer every add 412, as a tag that never comes fresh.
        self.always_stale = False
        #: Every state each playlist has had, oldest first, for a lagging read.
        self.history: dict[str, list[tuple[int, list[str]]]] = {
            uuid: [(1, [])] for uuid in uuids
        }
        #: Serve the playlist read, or the tracks read, one write behind.
        self.lag_open = False
        self.lag_window = False
        #: Run once just before the next tracks read is served.
        self.before_tracks: list = []
        #: Refusals the next tracks reads raise, in order.
        self.tracks_fail: list[Exception] = []
        #: Statuses the next playlist reads are answered with, in order.
        self.open_fail: list[int] = []
        #: Statuses armed on ``open_fail`` when an add is refused 412.
        self.open_fail_after_refusal: list[int] = []

    def tag(self, uuid: str) -> str:
        return f'"{self.version[uuid]}"'

    def _moved(self, uuid: str) -> None:
        self.version[uuid] += 1
        self.history[uuid].append((self.version[uuid], list(self.items[uuid])))

    def outside_add(self, uuid: str, identifier: str) -> None:
        """A write made by something other than this adapter, which moves the tag."""
        self.items[uuid].append(identifier)
        self._moved(uuid)

    def _served(self, uuid: str, lagging: bool) -> tuple[int, list[str]]:
        """The playlist's state as a read serves it: now, or one write behind."""
        states = self.history[uuid]
        return states[-2] if lagging and len(states) > 1 else states[-1]

    def gets(self, uuid: str) -> int:
        """GETs of the playlist itself, the request the card counts."""
        return self.requests[("GET", f"/v1/playlists/{uuid}")]

    def posts(self, uuid: str) -> int:
        return self.requests[("POST", f"/v1/playlists/{uuid}/items")]

    def track_reads(self, uuid: str) -> int:
        return self.requests[("GET", f"/v1/playlists/{uuid}/tracks")]

    def _data(self, uuid: str, items: list[str]) -> dict:
        data = _owned_playlist(0)
        data.update(uuid=uuid, title=self.titles[uuid], numberOfTracks=len(items))
        return data

    def request(self, method, url, params=None, data=None, headers=None, **_):
        path = urlsplit(url).path
        self.requests[(method, path)] += 1
        parts = path.split("/")
        if len(parts) < 4 or parts[2] != "playlists" or parts[3] not in self.items:
            raise AssertionError(f"the account serves no {method} {path}")
        uuid = parts[3]
        rest = parts[4:]
        version = self.version[uuid]
        if method == "GET" and not rest:
            if self.open_fail:
                return _Answer(url, {}, status=self.open_fail.pop(0), tag=version)
            tag, items = self._served(uuid, self.lag_open)
            return _Answer(url, self._data(uuid, items), tag=tag)
        if method == "GET" and rest == ["tracks"]:
            while self.before_tracks:
                self.before_tracks.pop(0)()
            if self.tracks_fail:
                raise self.tracks_fail.pop(0)
            tag, items = self._served(uuid, self.lag_window)
            params = params or {}
            start = int(params.get("offset") or 0)
            window = items[start : start + int(params.get("limit") or 100)]
            body = {
                "items": [_track(one) for one in window],
                "totalNumberOfItems": len(items),
            }
            return _Answer(url, body, tag=tag)
        sent = (headers or {}).get("If-None-Match")
        if method == "POST" and rest == ["items"]:
            self.adds.append((uuid, dict(data or {}), sent))
            if self.refusals:
                return _Answer(url, {}, status=self.refusals.pop(0), tag=version)
            if self.always_stale or sent != self.tag(uuid):
                self.open_fail.extend(self.open_fail_after_refusal)
                self.open_fail_after_refusal = []
                return _Answer(url, {}, status=412, tag=version)
            added = []
            at = int(data["toIndex"])
            for one in str(data["trackIds"]).split(","):
                if one in self.missing:
                    continue
                if data["onDupes"] == "SKIP" and one in self.items[uuid]:
                    continue
                self.items[uuid].insert(at, one)
                at += 1
                added.append(one)
            self._moved(uuid)
            return _Answer(url, {"addedItemIds": added}, tag=self.version[uuid])
        if method == "POST" and not rest:
            # The client's ``edit``: a retitle, which moves the tag too.
            self.titles[uuid] = str(data["title"])
            self._moved(uuid)
            return _Answer(url, {}, tag=self.version[uuid])
        raise AssertionError(f"the account serves no {method} {path}")


def _adapter(provider: Account) -> TidalAccount:
    return TidalAccount(_logged_in_over(provider), sleep=lambda _: None)


def _ids(count: int, start: int = 100) -> list[str]:
    return [str(start + n) for n in range(count)]


# ═══════════════════════════════════════════════════════════════════════════
# The request count
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("count", [1, 10, 100])
def test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts(count):
    """The brief's first scenario, on the real client: today 3K + 2 GETs."""
    provider = Account("pl0")
    remote = _adapter(provider)
    wanted = _ids(count)

    for one in wanted:
        remote.add_to_playlist("pl0", one)

    # The one open is two GETs (the client's ``Playlist``, then the
    # ``UserPlaylist`` its factory builds), and the client reads the playlist
    # once after each POST for its next tag. Nothing else.
    assert provider.gets("pl0") == count + 2
    assert provider.posts("pl0") == count
    assert provider.track_reads("pl0") == 1
    assert set(provider.requests) == {
        ("GET", "/v1/playlists/pl0"),
        ("GET", "/v1/playlists/pl0/tracks"),
        ("POST", "/v1/playlists/pl0/items"),
    }
    assert provider.items["pl0"] == wanted
    assert remote.playlist_tracks("pl0") == tuple(wanted)


def test_each_add_writes_what_it_wrote_before_one_track_at_the_end_on_the_current_tag():
    """What is written is unchanged: one track a request, at the playlist's
    length, duplicates and missing tracks skipped, carrying the current tag."""
    provider = Account("pl0")
    provider.outside_add("pl0", "7")
    remote = _adapter(provider)
    wanted = _ids(5)

    for one in wanted:
        remote.add_to_playlist("pl0", one)

    assert [form for _, form, _ in provider.adds] == [
        {
            "onArtifactNotFound": "SKIP",
            "trackIds": one,
            "toIndex": position,
            "onDupes": "SKIP",
        }
        for position, one in enumerate(wanted, start=1)
    ]
    # Each add carried the tag the playlist held when it was sent, so none was
    # refused: the client's read after each POST is what the next one sends.
    assert [tag for _, _, tag in provider.adds] == [f'"{n}"' for n in range(2, 7)]
    assert provider.items["pl0"] == ["7", *wanted]


def test_a_track_already_on_the_playlist_makes_no_request_at_all():
    provider = Account("pl0")
    provider.outside_add("pl0", "100")
    remote = _adapter(provider)

    remote.add_to_playlist("pl0", "100")
    before = Counter(provider.requests)
    remote.add_to_playlist("pl0", "100")

    assert provider.posts("pl0") == 0
    assert provider.requests == before


def test_two_playlists_added_to_in_turn_each_keep_their_own_held_object():
    """The brief's fourth scenario: the hold is per identifier."""
    provider = Account("pl0", "pl1")
    remote = _adapter(provider)
    first, second = _ids(6), _ids(6, start=200)

    for one, other in zip(first, second, strict=True):
        remote.add_to_playlist("pl0", one)
        remote.add_to_playlist("pl1", other)

    for uuid, wanted in (("pl0", first), ("pl1", second)):
        assert provider.gets(uuid) == len(wanted) + 2
        assert provider.posts(uuid) == len(wanted)
        assert provider.items[uuid] == wanted
    # Every add carried its own playlist's tag, so neither was refused.
    assert all(tag == f'"{n}"' for n, (_, _, tag) in enumerate(provider.adds[::2], start=1))
    assert len(provider.adds) == 12


# ═══════════════════════════════════════════════════════════════════════════
# A held object the provider has moved on from
# ═══════════════════════════════════════════════════════════════════════════


def test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands():
    """The brief's second scenario: a write outside the adapter moved the tag."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    provider.outside_add("pl0", "7")
    gets_before = provider.gets("pl0")

    remote.add_to_playlist("pl0", "101")

    # The refused add, then one open (two GETs) and the add again, which the
    # client reads after: three GETs and two POSTs for this track.
    assert provider.gets("pl0") - gets_before == 3
    assert [tag for _, _, tag in provider.adds[1:]] == ['"2"', '"3"']
    assert provider.items["pl0"] == ["100", "7", "101"]
    # The fresh object is held: the next add makes no further open.
    remote.add_to_playlist("pl0", "102")
    assert provider.gets("pl0") - gets_before == 4
    assert provider.items["pl0"] == ["100", "7", "101", "102"]


@pytest.mark.parametrize("status", [412, 503])
def test_an_add_refused_twice_fails_the_item_with_nothing_more_sent(status):
    """The retry the policy allows is one, and the hold never adds a second."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    if status == 412:
        provider.always_stale = True
    else:
        provider.refusals = [status, status]

    with pytest.raises(CratekitError) as excinfo:
        remote.add_to_playlist("pl0", "101")

    assert excinfo.value.cause.scope.name == "ITEM"
    assert provider.posts("pl0") == 3
    assert provider.items["pl0"] == ["100"]
    assert "101" not in remote.playlist_tracks("pl0")


def test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh():
    """An add the provider refused leaves no object behind it to be reused."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    provider.always_stale = True
    with pytest.raises(CratekitError):
        remote.add_to_playlist("pl0", "101")
    provider.always_stale = False
    gets_before, current = provider.gets("pl0"), provider.tag("pl0")

    remote.add_to_playlist("pl0", "102")

    # One open, two GETs, then the add and the client's read after it.
    assert provider.gets("pl0") - gets_before == 3
    assert provider.adds[-1][2] == current
    assert provider.items["pl0"] == ["100", "102"]


def test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back():
    """A stale held object never lets a duplicate through: the same track put
    on by another writer is refused 412, sent again on a fresh open, skipped
    by the provider as a duplicate, and read back as held."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    provider.outside_add("pl0", "101")

    remote.add_to_playlist("pl0", "101")

    assert provider.items["pl0"] == ["100", "101"]
    assert remote.playlist_tracks("pl0") == ("100", "101")


# ═══════════════════════════════════════════════════════════════════════════
# The read back, and what drops the hold
# ═══════════════════════════════════════════════════════════════════════════


def test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses():
    """The brief's third scenario: unchanged, and read on a fresh open."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    provider.missing.add("101")
    gets_before, reads_before = provider.gets("pl0"), provider.track_reads("pl0")

    with pytest.raises(CratekitError) as excinfo:
        remote.add_to_playlist("pl0", "101")

    assert "added nothing" in excinfo.value.cause.message
    # The client's read after the POST, then the read back's own open (two
    # GETs) and its read of the tracks, as before this unit.
    assert provider.gets("pl0") - gets_before == 3
    assert provider.track_reads("pl0") - reads_before == 1
    assert remote.playlist_tracks("pl0") == ("100",)


def test_another_write_through_the_adapter_drops_the_hold():
    """A rename opens its own object and moves the tag; the next add opens
    afresh rather than sending the tag the rename made stale."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")

    remote.rename_playlist("pl0", "Renamed")
    gets_before = provider.gets("pl0")
    remote.add_to_playlist("pl0", "101")

    assert provider.titles["pl0"] == "Renamed"
    assert provider.gets("pl0") - gets_before == 3
    # No add was refused: the one after the rename carried the rename's tag.
    assert provider.posts("pl0") == 2
    assert provider.items["pl0"] == ["100", "101"]


def test_a_held_playlist_never_outlives_its_adapter(monkeypatch):
    """The brief's last scenario: ``forget`` drops the adapter, and with it the
    hold, so the next adapter opens the playlist again."""
    provider = Account("pl0")
    session = _logged_in_over(provider)
    first = TidalAccount(session, sleep=lambda _: None)
    first.add_to_playlist("pl0", "100")
    monkeypatch.setattr(account, "_OPENED", first)

    account.forget()
    assert account._OPENED is None
    gets_before = provider.gets("pl0")
    TidalAccount(session, sleep=lambda _: None).add_to_playlist("pl0", "101")

    # The next adapter's own open (two GETs), its read of the tracks, the add
    # and the client's read after it.
    assert provider.gets("pl0") - gets_before == 3
    assert provider.items["pl0"] == ["100", "101"]


# ═══════════════════════════════════════════════════════════════════════════
# The export, end to end at the adapter
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "install"))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.mark.parametrize("count", [1, 12, 100])
def test_an_export_of_up_to_a_hundred_tracks_to_a_recorded_playlist_makes_seven_requests(
    cfg, count
):
    """``export.apply``, the caller the card measured, over the real client:
    every track recorded, every track added once, in order. U270 sends the
    tracks the playlist lacks in one ``add_tracks``, so the count no longer
    grows with the tracks: one open and one tracks read for the membership,
    then one open, one POST and the client's read after it. U255 left this at
    K + 2 GETs and K POSTs, 203 requests for 100 tracks.
    """
    provider = Account("pl0")
    remote = _adapter(provider)
    ledger.reserve_playlist(cfg, "crate-one", lambda: "pl0")
    wanted = _ids(count)
    planned = export.ExportPlan(
        playlist_key="crate-one",
        name="Crate One",
        matched=tuple((f"row-{one}", one) for one in wanted),
        unmatched=(),
    )

    report = export.apply(cfg, remote, planned)

    assert report.created is False
    assert report.added == tuple(wanted)
    assert provider.items["pl0"] == wanted
    assert provider.gets("pl0") == 5
    assert provider.track_reads("pl0") == 1
    assert provider.posts("pl0") == 1
    assert sum(provider.requests.values()) == 7
    recorded = json.loads(config.state_path("outbound_writes", cfg).read_text())
    assert recorded["playlists"]["crate-one"]["remote_id"] == "pl0"
    record = recorded["playlists"]["crate-one"]
    assert record["added"] == wanted
    assert record["rows"] == {f"row-{one}": one for one in wanted}
    assert "sending" not in record


def test_the_owner_the_transport_serves_is_the_session_user():
    """The held object is the client's ``UserPlaylist``, the one with ``add``,
    because the transport serves the playlist as the logged in user's own."""
    provider = Account("pl0")
    session = _logged_in_over(provider)
    assert session.playlist("pl0").creator.id == OWNER
    assert callable(getattr(session.playlist("pl0"), "add", None))


# ═══════════════════════════════════════════════════════════════════════════
# Round one's review: the tag and the position come from one answer
# ═══════════════════════════════════════════════════════════════════════════


def _three(provider: Account) -> None:
    for one in ("1", "2", "3"):
        provider.outside_add("pl0", one)


def test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it():
    """Drive A: another writer adds between the open and the tracks read. The
    add is refused on the open's tag, sent again on a fresh open, and lands at
    the end, as main lands it; it is never accepted at the open's length."""
    provider = Account("pl0")
    _three(provider)
    provider.before_tracks.append(lambda: provider.outside_add("pl0", "7"))
    remote = _adapter(provider)

    remote.add_to_playlist("pl0", "100")

    assert provider.items["pl0"] == ["1", "2", "3", "7", "100"]
    assert [form["toIndex"] for _, form, _ in provider.adds] == [3, 4]
    assert remote.playlist_tracks("pl0") == ("1", "2", "3", "7", "100")


def test_a_playlist_read_one_write_behind_writes_nothing():
    """Drive B: every playlist read lags one write while the tracks read is
    current. The add carries the lagging read's tag with its length, so it is
    refused and refused again, and nothing is written, as on main."""
    provider = Account("pl0")
    _three(provider)
    provider.lag_open = True
    remote = _adapter(provider)

    with pytest.raises(CratekitError):
        remote.add_to_playlist("pl0", "100")

    assert provider.items["pl0"] == ["1", "2", "3"]
    assert [(form["toIndex"], tag) for _, form, tag in provider.adds] == [(2, '"3"')] * 2


def test_a_tracks_read_one_write_behind_never_reaches_the_add():
    """Finding two: the tag the add sends is the open's, not a lagging tracks
    read's, so one POST lands at the end and nothing is refused."""
    provider = Account("pl0")
    _three(provider)
    provider.lag_window = True
    remote = _adapter(provider)

    remote.add_to_playlist("pl0", "100")

    assert [(form["toIndex"], tag) for _, form, tag in provider.adds] == [(3, '"4"')]
    assert provider.items["pl0"] == ["1", "2", "3", "100"]


def test_a_tracks_read_that_fails_after_the_open_holds_nothing():
    """Drive H: the open succeeded and the read it was made for did not, so no
    object is held, and the next add after two more writes opens afresh and
    lands at the end rather than at the old length."""
    provider = Account("pl0")
    provider.outside_add("pl0", "7")
    provider.tracks_fail.append(
        refuse("credential-missing", "the session was refused mid read", retryable=False)
    )
    remote = _adapter(provider)
    with pytest.raises(CratekitError):
        remote.add_to_playlist("pl0", "100")
    provider.outside_add("pl0", "8")
    provider.outside_add("pl0", "9")

    remote.add_to_playlist("pl0", "100")

    assert provider.items["pl0"] == ["7", "8", "9", "100"]
    assert [form["toIndex"] for _, form, _ in provider.adds] == [3]


def test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent():
    """The first open, nothing held, is made before the add's attempts, as it
    always was: two tries of the open, then the open's own refusal, no POST."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    remote.rename_playlist("pl0", "Renamed")
    provider.open_fail = [503, 503]
    gets_before = provider.gets("pl0")

    with pytest.raises(CratekitError) as excinfo:
        remote.add_to_playlist("pl0", "101")

    assert "open the playlist pl0" in excinfo.value.cause.message
    assert provider.gets("pl0") - gets_before == 2
    assert provider.posts("pl0") == 1
    assert provider.items["pl0"] == ["100"]


def test_the_retrys_open_has_a_retry_of_its_own():
    """Finding three: an add refused 412 whose fresh open meets one transient
    failure still opens on the open's own retry and lands, as main's open did."""
    provider = Account("pl0")
    remote = _adapter(provider)
    remote.add_to_playlist("pl0", "100")
    provider.outside_add("pl0", "7")
    provider.open_fail_after_refusal = [503]

    remote.add_to_playlist("pl0", "101")

    assert provider.items["pl0"] == ["100", "7", "101"]
    assert provider.posts("pl0") == 3
