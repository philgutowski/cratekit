"""U63: the provider account adapter behind the outbound seam, driven against fakes.

The client is a fake injected at ``provider_session.CLIENT_FACTORY``, so nothing
here reaches the provider. ONE SUBSTITUTION BEYOND IT: some end to end drives give
the rows an ISRC through ``source.local_tracks`` and ``source.heart_candidates``,
since a collection export carries none. D1 applies: no real volume, person or track.
"""

from __future__ import annotations

import ast
import functools
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.acquire import isrc_cache, listing, provider_session
from cratekit.core import jobs, locations, secrets, tags
from cratekit.core.cause import CratekitError, Scope
from cratekit.core.exit_codes import ExitCode
from cratekit.export import cli as export_cli
from cratekit.modules.outbound import account, artifacts, ledger, service, source, tidal_account
from cratekit.modules.outbound.service import RemoteAccount
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

#: Every module the adapter is made of: the structural guards read them all.
ADAPTER_SOURCES = sorted(Path(tidal_account.__file__).parent.glob("tidal_*.py"))

STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 946684800.0,
}


# ── fakes: a provider client that answers from memory and counts what it is asked ──


class ObjectNotFound(Exception):
    """Named as the client names its not found, which is how the adapter reads it."""


class HTTPFailure(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"HTTP {status_code}")
        self.response = SimpleNamespace(status_code=status_code)


class Track:
    """A provider track in the client's shape: name, version, first artist, every artist billed."""

    def __init__(
        self, track_id: str, name: str = "", version: str | None = None, artists: tuple = ()
    ) -> None:
        self.id = int(track_id)
        self.name = name
        self.version = version
        self.artists = [SimpleNamespace(name=one) for one in artists]
        self.artist = self.artists[0] if self.artists else None
        #: The client's own name for "the provider will play this".
        self.available = True


def withdrawn(track: Track) -> Track:
    """The track as the client hands out one the provider will not play: no version read."""
    track.available = False
    track.version = None
    return track


class Playlist:
    """An owned playlist that pages its tracks and records every add and retitle."""

    def __init__(self, playlist_id: str, members: list[str] = (), name: str = "") -> None:
        self.id = playlist_id
        self.members = list(members)
        self.name = name
        self.adds: list[list[str]] = []
        self.pages: list[tuple[int, int]] = []
        self.edits: list[tuple[str | None, str | None]] = []
        self.edit_fail: list[Exception] = []
        self.edit_answer = True
        #: ``None`` until the client is asked: made private, or never touched.
        self.public: bool | None = None
        self.privates = 0
        self.private_fail: list[Exception] = []

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Track]:
        size = 100 if limit is None else limit
        self.pages.append((size, offset))
        return [Track(member) for member in self.members[offset : offset + size]]

    def add(self, media_ids: list[str], allow_duplicates: bool = False) -> list[str]:
        del allow_duplicates
        self.adds.append(list(media_ids))
        self.members.extend(media_ids)
        return list(media_ids)

    def edit(self, title: str | None = None, description: str | None = None) -> bool:
        """The client's own shape: a bool answer, and a falsy title keeps the old one."""
        self.edits.append((title, description))
        if self.edit_fail:
            raise self.edit_fail.pop(0)
        if not self.edit_answer:
            return False
        if title:
            self.name = title
        return True

    def set_playlist_private(self) -> bool:
        """The client's own shape: a raise on refusal, else the response's ``ok``."""
        self.privates += 1
        if self.private_fail:
            raise self.private_fail.pop(0)
        self.public = False
        return True


class ForeignPlaylist:
    """A playlist the session does not own: the client hands it out with no ``edit``."""

    def __init__(self, playlist_id: str, members: list[str] = (), name: str = "") -> None:
        self.id = playlist_id
        self.name = name
        self.members: list[str] = list(members)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Track]:
        del limit, offset
        return []


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
        #: Refusals the next created playlist's private step raises, in order.
        self.private_fail: list[Exception] = []

    def create_playlist(self, title: str, description: str) -> Playlist:
        del description
        self.created.append(title)
        if self.create_fail is not None:
            raise self.create_fail
        playlist = Playlist(f"00000000-0000-4000-8000-{len(self.created):012d}")
        # The queued refusals belong to this playlist alone.
        playlist.private_fail = self.private_fail[:]
        self.private_fail.clear()
        self._client.playlists[playlist.id] = playlist
        return playlist


class FakeClient:
    def __init__(
        self,
        *,
        isrcs: dict[str, list] | None = None,
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
        """``isrcs`` maps a code to identifiers, or to whole tracks for the provider's spelling."""
        self.isrc_asked.append(isrc)
        if isrc not in self.isrcs:
            raise ObjectNotFound(isrc)
        return [one if isinstance(one, Track) else Track(one) for one in self.isrcs[isrc]]

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


def another_catalogue(client: FakeClient) -> tidal_account.TidalAccount:
    """An adapter sharing no remembered ISRC answer (U206), for a catalogue filed differently."""
    return tidal_account.TidalAccount(client, sleep=no_sleep, cache=isrc_cache.Cache(days=0))


def refused(call):
    """The cause ``call`` raises."""
    with pytest.raises(CratekitError) as excinfo:
        call()
    return excinfo.value.cause


# ── 1. the seam ─────────────────────────────────────────────────────────────


def test_a_recorded_session_resolves_the_adapter_and_the_build_is_bound(installed, monkeypatch):
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
    assert refused(lambda: account.resolve(installed)).reason == "credential-missing"
    assert client.logins == 0


def test_a_session_removed_after_an_open_is_refused_rather_than_reused(installed, monkeypatch):
    use_client(monkeypatch, FakeClient())
    record_session()
    account.resolve(installed)
    monkeypatch.setattr(secrets, "exists", lambda name: False)
    assert refused(lambda: account.resolve(installed)).reason == "credential-missing"


@pytest.mark.parametrize(
    ("failure", "reason"),
    [(HTTPFailure(401), "credential-missing"), (ConnectionError("refused"), "unavailable-transient")],
    ids=["rejected", "unreachable"],
)
def test_a_login_that_fails_names_whether_to_log_in_again_or_wait(
    installed, monkeypatch, failure, reason
):
    use_client(monkeypatch, FakeClient(login_raises=failure))
    record_session()
    assert refused(lambda: account.resolve(installed)).reason == reason
    with pytest.raises(CratekitError):
        account.resolve(installed)


# ── 2. matching is exact or it is None ──────────────────────────────────────


def test_an_isrc_naming_one_track_is_the_match():
    client = FakeClient(isrcs={"AA0000000001": ["101", "101"]})
    assert adapter(client).match_track(identity="7", isrc="AA0000000001") == "101"
    assert client.track_asked == []


def test_an_isrc_naming_two_tracks_is_no_match_rather_than_the_first():
    client = FakeClient(isrcs={"AA0000000001": ["101", "202"]}, tracks={"101"})
    url = "https://tidal.com/browse/track/101"
    assert adapter(client).match_track(identity=url, isrc="AA0000000001") is None


# ── R-356: several releases under one ISRC ──

CODE = "AA0000000001"


def releases(*tracks: Track, hearts: list[str] = ()) -> FakeClient:
    """A client whose ISRC ``CODE`` names ``tracks``, the account hearting ``hearts``."""
    return FakeClient(isrcs={CODE: list(tracks)}, hearts=hearts)


def sun(track_id: str, version: str | None = None, *artists: str, name: str = "Sun Path") -> Track:
    """A release named ``name``, billed to Nova Reef unless ``artists`` says otherwise."""
    return Track(track_id, name, version, artists or ("Nova Reef",))


def unreadable(track_id: str) -> Track:
    return Track(track_id, "", None, ())


def match_row(
    found: tidal_account.TidalAccount, title: str, artist: str = "Nova Reef", identity="7", **more
):
    return found.match_track(identity=identity, isrc=CODE, title=title, artist=artist, **more)


def test_the_measured_cost_three_releases_of_one_isrc_resolve_to_the_rows_version():
    """The fourth sitting's shape: a single, an EP cut and a compilation track (R-356)."""
    client = releases(
        sun("101", "Radio Edit"), sun("202", "Extended Mix"), sun("303", "Ten Year Remaster")
    )
    found = adapter(client)
    assert match_row(found, "Sun Path (Extended Mix)") == "202"
    assert found.unmatched_reason("7") == ""
    assert client.user.favorites.pages == [], "one agreeing track asks the hearts nothing"


def test_a_code_asked_to_agree_lists_its_one_track_only_when_it_is_the_row():
    """R-879: a code read off a file's tag names its one track only when that track agrees."""
    found = adapter(releases(sun("101")))
    assert match_row(found, "Sun Path", agree=True) == "101"
    assert match_row(found, "Moon Path", identity="8", agree=True) is None
    assert "none of them agrees" in found.unmatched_reason("8")
    # Without it, one track is the match as it always was.
    assert match_row(found, "Moon Path", identity="9") == "101"


def test_a_row_with_no_version_agrees_with_an_original_mix_and_not_with_an_edit():
    client = releases(sun("101", "Original Mix"), sun("202", "Radio Edit"))
    assert match_row(adapter(client), "Sun Path") == "101"


def test_a_version_the_provider_spells_inside_the_title_is_read_the_same_way():
    client = releases(
        sun("101", name="Sun Path - Radio Edit"), sun("202", name="Sun Path (Extended Mix)")
    )
    assert match_row(adapter(client), "Sun Path (Radio Edit)") == "101"


def test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them():
    found = adapter(releases(sun("101"), sun("202"), sun("303", "Radio Edit")))
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert f"the ISRC {CODE} names 3 provider tracks" in reason
    assert "2 of them agree" in reason
    assert "hearts 0 of those" in reason


def test_among_releases_spelled_alike_the_one_already_hearted_is_the_match():
    found = adapter(releases(sun("101"), sun("202"), hearts=["202"]))
    assert match_row(found, "Sun Path") == "202"
    assert found.unmatched_reason("7") == ""


def test_two_hearted_releases_spelled_alike_are_still_no_match():
    found = adapter(releases(sun("101"), sun("202"), hearts=["101", "202"]))
    assert match_row(found, "Sun Path") is None
    assert "hearts 2 of those" in found.unmatched_reason("7")


def test_a_heart_on_a_release_the_row_does_not_name_decides_nothing():
    """The hearted one is the radio edit, and the row is the plain record."""
    client = releases(sun("101"), sun("202"), sun("303", "Radio Edit"), hearts=["303"])
    assert match_row(adapter(client), "Sun Path") is None


def test_no_release_agreeing_is_no_match_and_the_hearts_are_not_read():
    """An ISRC the provider filed on another record chooses nothing, hearted or not."""
    client = releases(sun("101", name="Moon Road"), sun("202", "Dub", name="Moon Road"))
    client.user.favorites.hearts = ["101"]
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert "none of them agrees" in found.unmatched_reason("7")
    assert client.user.favorites.pages == []


def test_another_artist_under_the_same_title_does_not_agree():
    client = releases(sun("101", None, "Aurora Bloom"), sun("202"))
    assert match_row(adapter(client), "Sun Path") == "202"


def test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two():
    pair = ("Nova Reef", "Mira Vale")
    found = adapter(releases(sun("101", None, *pair), sun("202", "Radio Edit", *pair)))
    assert match_row(found, "Sun Path", artist="Nova Reef, Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef & Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef") == "101"
    assert match_row(found, "Sun Path", artist="Mira Vale") is None, "the guest alone"
    assert match_row(found, "Sun Path", artist="Mira Vale, Nova Reef") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef feat. Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef, Mira Vale, Kai Tern") is None
    assert match_row(found, "Sun Path", artist="Nova") is None, "half a name"


def test_a_remixer_the_provider_bills_and_the_row_does_not_is_still_agreement():
    client = releases(sun("101", "Kai Tern Remix", "Nova Reef", "Kai Tern"), sun("202"))
    assert match_row(adapter(client), "Sun Path (Kai Tern Remix)") == "101"


def test_a_track_the_provider_will_not_play_is_never_the_choice():
    """Its version was never read, so a withdrawn extended mix looks like the plain record."""
    client = releases(sun("101", "Radio Edit"), withdrawn(sun("202", "Extended Mix")))
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert "1 cannot be streamed" in reason and "none of the rest agrees" in reason
    client.user.favorites.hearts = ["202"]
    assert match_row(adapter(client), "Sun Path") is None, "a heart does not revive it"


def test_a_withdrawn_release_does_not_stop_the_one_that_plays_from_being_chosen():
    assert match_row(adapter(releases(sun("101"), withdrawn(sun("202")))), "Sun Path") == "101"


def test_a_provider_title_that_reads_two_ways_agrees_under_either_too():
    """The same recording must resolve whichever side spelled the version with a dash."""
    client = releases(sun("101", name="Sun Path - Live"), sun("202", "Radio Edit"))
    assert match_row(adapter(client), "Sun Path (Live)") == "101"


def test_a_row_carrying_no_names_chooses_nothing_and_asks_the_hearts_nothing():
    client = releases(sun("101"), sun("202", "Radio Edit"), hearts=["101"])
    found = adapter(client)
    assert found.match_track(identity="7", isrc=CODE) is None
    assert found.match_track(identity="7", isrc=CODE, title="Sun Path") is None
    assert found.match_track(identity="7", isrc=CODE, artist="Nova Reef") is None
    assert "no artist and title" in found.unmatched_reason("7")
    assert client.user.favorites.pages == []


def test_a_release_that_cannot_be_read_stops_a_lone_agreeing_one_from_being_chosen():
    """One agreeing track beside one nobody could read is not known to be the only one."""
    client = releases(sun("101"), unreadable("202"))
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert "1 could not be read" in found.unmatched_reason("7")
    client.user.favorites.hearts = ["101"]
    assert match_row(adapter(client), "Sun Path") == "101"


def test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one():
    one = releases(sun("101", "Live"), sun("202", "Radio Edit"))
    assert match_row(adapter(one), "Sun Path - Live") == "101"
    both = releases(sun("101", "Live"), sun("202", name="Sun Path - Live"))
    assert match_row(another_catalogue(both), "Sun Path - Live") is None


def test_a_reason_does_not_outlive_the_match_it_was_about():
    client = releases(sun("101"), sun("202"))
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert found.unmatched_reason("7")
    assert found.unmatched_reason("8") == "", "a reason belongs to one row"
    client.user.favorites.hearts.append("101")
    found._hearts = None
    assert match_row(found, "Sun Path") == "101"
    assert found.unmatched_reason("7") == ""


def test_a_row_the_provider_has_never_heard_of_carries_no_reason():
    found = adapter(FakeClient())
    assert found.match_track(identity="7", isrc=CODE, title="Sun Path", artist="x") is None
    assert found.unmatched_reason("7") == ""


def test_the_names_are_never_sent_to_the_provider():
    """They choose among what the ISRC named. A search on them would heart a cover."""
    client = releases(sun("101"))
    client.search = lambda *args, **kwargs: pytest.fail("the adapter searched")
    assert match_row(adapter(client), "Sun Path") == "101"
    assert client.isrc_asked == [CODE] and client.track_asked == []


def test_an_isrc_the_provider_lacks_falls_back_to_an_exact_track_reference():
    client = FakeClient(tracks={"303"})
    url = "https://listen.tidal.com/track/303"
    assert adapter(client).match_track(identity=url, isrc="ZZ0000000009") == "303"
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


def test_a_reference_the_provider_lacks_or_redirects_is_no_match():
    """A lookup that lands on a different identifier is a redirect, not the track."""
    client = FakeClient()
    assert adapter(client).match_track(identity="https://tidal.com/track/9") is None
    assert client.track_asked == ["9"]
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


# ── 3. one paged read answers every heart question ──────────────────────────
# Under U65 a complete walk ends on the empty page after the last, so a corpus
# this small is two requests; a cache miss would show a second (100, 0).


def test_has_heart_answers_a_whole_sweep_from_one_paged_read():
    client = FakeClient(hearts=[str(1000 + index) for index in range(250)])
    remote = adapter(client)
    answers = [remote.has_heart(str(1000 + index)) for index in range(400)]
    assert answers == [index < 250 for index in range(400)]
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
    assert client.user.favorites.pages == [(100, 0), (100, 100)]


def test_a_member_already_on_the_playlist_makes_no_write():
    playlist = Playlist("00000000-0000-4000-8000-00000000000a", ["11", "12"])
    remote = adapter(FakeClient(playlists={playlist.id: playlist}))
    remote.add_to_playlist(playlist.id, "12")
    assert playlist.adds == []
    remote.add_to_playlist(playlist.id, "13")
    remote.add_to_playlist(playlist.id, "13")
    assert playlist.adds == [["13"]]
    assert remote.playlist_tracks(playlist.id) == ("11", "12", "13")
    assert playlist.pages == [(100, 0), (100, 100)]


def test_a_created_playlist_returns_the_identifier_the_provider_assigned():
    client = FakeClient()
    remote = adapter(client)
    created = remote.create_playlist("Crate")
    assert created == "00000000-0000-4000-8000-000000000001"
    assert client.user.created == ["Crate"]
    assert remote.playlist_tracks(created) == ()


# ── visibility, R-834 ──


def test_a_created_playlist_is_made_private_once():
    client = FakeClient()
    playlist = client.playlists[adapter(client).create_playlist("Crate")]
    assert playlist.public is False
    assert playlist.privates == 1


def test_a_private_step_refused_once_is_retried_once_and_lands():
    client = FakeClient()
    client.user.private_fail.append(TimeoutError("timed out"))
    playlist = client.playlists[adapter(client).create_playlist("Crate")]
    assert playlist.privates == 2
    assert playlist.public is False
    assert client.user.created == ["Crate"]


def test_a_private_step_refused_twice_still_hands_back_the_one_playlist():
    """Raising would leave it unrecorded and the next item would create another (R-849)."""
    client = FakeClient()
    client.user.private_fail.extend([TimeoutError("one"), TimeoutError("two")])
    remote = adapter(client)
    created = remote.create_playlist("Crate")
    assert created == "00000000-0000-4000-8000-000000000001"
    assert client.user.created == ["Crate"]
    assert client.playlists[created].privates == 2
    assert client.playlists[created].public is None
    assert remote.playlist_tracks(created) == ()


def test_a_created_playlist_the_client_offers_no_private_call_for_is_still_returned():
    client = FakeClient()
    bare = SimpleNamespace(id="00000000-0000-4000-8000-0000000000aa")
    client.user.create_playlist = lambda title, description: bare
    assert adapter(client).create_playlist("Crate") == bare.id


# ── the retitle, R-358 ──


def warmup(kind: type = Playlist, members: list[str] = (), name: str = "Warmup"):
    """A playlist ``pl-1`` named ``name``, and a client serving it."""
    playlist = kind("pl-1", members, name=name)
    return playlist, FakeClient(playlists={"pl-1": playlist})


def test_a_rename_retitles_the_playlist_and_leaves_its_membership_alone():
    playlist, client = warmup(members=["101", "102"])
    adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup")
    assert playlist.name == "DOWNLOADED Warmup"
    assert playlist.edits == [("DOWNLOADED Warmup", None)]
    assert playlist.members == ["101", "102"]
    assert playlist.adds == []


def test_a_rename_the_client_answers_false_is_the_items_cause_not_a_quiet_return():
    """A mark reported as applied over a title that never changed is the whole defect."""
    playlist, client = warmup()
    playlist.edit_answer = False
    cause = refused(lambda: adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup"))
    assert playlist.name == "Warmup"
    assert cause.scope is Scope.ITEM
    assert cause.reason == "unavailable-transient"


def test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename():
    """THE MESSAGE IS THE ASSERTION: a missing editor called anyway fails inside ``_call``
    with the same slug, scope and doing string; only the sentence tells them apart."""
    foreign, client = warmup(ForeignPlaylist, name="Somebody Else")
    cause = refused(lambda: adapter(client).rename_playlist("pl-1", "DOWNLOADED Somebody Else"))
    assert cause.scope is Scope.ITEM
    assert "cannot be retitled by this account" in cause.message
    assert foreign.name == "Somebody Else"


def test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause():
    """The client answers an explicit not found; returning would be a mark nothing carries."""

    class Vanishing(Playlist):
        def edit(self, title=None, description=None):
            raise ObjectNotFound(self.id)

    playlist, client = warmup(Vanishing)
    cause = refused(lambda: adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup"))
    assert cause.scope is Scope.ITEM
    assert playlist.name == "Warmup"


@pytest.mark.parametrize("blank", ["", "   ", "\n"])
def test_a_rename_with_no_title_is_refused_before_the_client_sees_it(blank):
    """The client reads a falsy title as keep the current one and answers True."""
    playlist, client = warmup()
    cause = refused(lambda: adapter(client).rename_playlist("pl-1", blank))
    assert playlist.edits == [], "the empty title reached the client"
    assert playlist.name == "Warmup"
    assert cause.reason == "internal-error"
    assert cause.scope is Scope.SOURCE
    # The MESSAGE, not only the slug.
    assert "reads a falsy title as keep the current one" in cause.message


def test_a_title_the_caller_padded_is_written_as_the_caller_asked():
    """The emptiness test strips. The write does not."""
    playlist, client = warmup()
    adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup ")
    assert playlist.name == "DOWNLOADED Warmup "


def test_a_rename_of_a_playlist_the_provider_lacks_is_the_items_cause():
    cause = refused(lambda: adapter(FakeClient()).rename_playlist("pl-9", "DOWNLOADED Gone"))
    assert cause.scope is Scope.ITEM


def test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title():
    """Unlike a create, a retry asks for the state the first attempt asked for."""
    playlist, client = warmup()
    playlist.edit_fail = [HTTPFailure(429)]
    adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup")
    assert playlist.edits == [("DOWNLOADED Warmup", None), ("DOWNLOADED Warmup", None)]
    assert playlist.name == "DOWNLOADED Warmup"


# ── 4. a provider failure is the item's cause, with one retry on a write ────


def hearting(*failures: Exception) -> FakeClient:
    """A client whose next hearts fail with ``failures``, in order."""
    client = FakeClient()
    client.user.favorites.fail = list(failures)
    return client


def test_a_write_the_provider_refuses_once_is_retried_once_and_lands():
    client = hearting(HTTPFailure(429))
    adapter(client).add_heart("8")
    assert client.user.favorites.added == ["8", "8"]


def test_a_write_refused_twice_is_the_items_cause_and_is_not_tried_a_third_time():
    client = hearting(HTTPFailure(429), HTTPFailure(429), HTTPFailure(429))
    cause = refused(lambda: adapter(client).add_heart("8"))
    assert client.user.favorites.added == ["8", "8"]
    assert cause.reason == "unavailable-transient"
    assert cause.scope is Scope.ITEM


def test_a_rejected_session_mid_sweep_asks_for_a_login_at_item_scope():
    cause = refused(lambda: adapter(hearting(HTTPFailure(401), HTTPFailure(401))).add_heart("8"))
    assert cause.reason == "credential-missing"
    assert cause.scope is Scope.ITEM


def test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session():
    try:
        raise HTTPFailure(401)
    except HTTPFailure as inner:
        wrapped = RuntimeError("the client's own error")
        wrapped.__cause__ = inner
    assert refused(lambda: adapter(hearting(wrapped, wrapped)).add_heart("8")).reason == (
        "credential-missing"
    )


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
    cause = refused(lambda: adapter(client).create_playlist("Crate"))
    assert client.user.created == ["Crate"]
    assert cause.reason == "unavailable-transient"


@pytest.mark.parametrize("make", ["create_playlist", "create_folder"])
def test_a_playlist_or_folder_created_with_no_identifier_is_not_taken_as_created(make):
    """What the provider created must carry an identifier, or the create is a failure."""
    client = FakeClient()
    setattr(client.user, make, lambda *names: SimpleNamespace(id=""))
    assert refused(lambda: getattr(adapter(client), make)("Crate")).reason == "unavailable-transient"


def vouched(cfg, *members: str) -> tuple[Playlist, FakeClient, tidal_account.TidalAccount]:
    """A playlist the ledger records as made here, and an adapter over a client serving it."""
    playlist = Playlist("pl-made", list(members))
    ledger.reserve_set_playlist(cfg, "Set", "2026", lambda: playlist.id)
    client = FakeClient(playlists={playlist.id: playlist})
    return playlist, client, tidal_account.TidalAccount(client, sleep=no_sleep, cfg=cfg)


def test_a_playlist_found_gone_forgets_the_membership_it_was_remembered_with(installed):
    """Once the provider no longer serves a playlist, its old membership is never answered."""
    playlist, client, remote = vouched(installed, "11")
    assert remote.playlist_tracks(playlist.id) == ("11",)
    del client.playlists[playlist.id]
    remote.remove_playlist(playlist.id)
    refused(lambda: remote.playlist_tracks(playlist.id))


def test_a_delete_meeting_a_transient_failure_is_sent_once(installed):
    """A retried delete could remove twice, so a timed out delete is never sent again."""
    playlist, _client, remote = vouched(installed)
    sent: list[str] = []

    def delete() -> bool:
        sent.append(playlist.id)
        raise TimeoutError("timed out")

    playlist.delete = delete
    refused(lambda: remote.remove_playlist(playlist.id))
    assert sent == [playlist.id]


def adding(suffix: str, add) -> tuple[Playlist, tidal_account.TidalAccount]:
    """A playlist holding ``11`` whose client answers an add with ``add``."""
    playlist = Playlist(f"00000000-0000-4000-8000-00000000000{suffix}", ["11"])
    playlist.add = add
    return playlist, adapter(FakeClient(playlists={playlist.id: playlist}))


def test_an_add_the_client_answers_with_nothing_is_not_recorded_as_a_member():
    """The client skips a track it cannot find and raises nothing."""
    playlist, remote = adding("b", lambda media_ids, allow_duplicates=False: [])
    assert refused(lambda: remote.add_to_playlist(playlist.id, "14")).scope is Scope.ITEM
    assert remote.playlist_tracks(playlist.id) == ("11",)


def test_an_empty_answer_for_a_track_the_playlist_now_holds_is_not_a_failure():
    def add_elsewhere(media_ids, allow_duplicates=False):
        playlist.members.extend(media_ids)
        return []

    playlist, remote = adding("c", add_elsewhere)
    remote.add_to_playlist(playlist.id, "15")
    assert remote.playlist_tracks(playlist.id) == ("11", "15")


def test_an_add_to_a_playlist_deleted_mid_run_is_the_items_cause():
    def gone(media_ids, allow_duplicates=False):
        raise ObjectNotFound(playlist.id)

    playlist, remote = adding("d", gone)
    cause = refused(lambda: remote.add_to_playlist(playlist.id, "16"))
    assert cause.reason == "unavailable-transient"
    assert "16" not in remote.playlist_tracks(playlist.id)


def test_a_bad_request_on_a_write_is_not_read_as_a_rejected_session():
    cause = refused(lambda: adapter(hearting(HTTPFailure(400), HTTPFailure(400))).add_heart("8"))
    assert cause.reason == "unavailable-transient"


def test_a_session_rejected_mid_run_drops_the_held_account(installed, monkeypatch):
    use_client(monkeypatch, FakeClient())
    record_session()
    held = account.resolve(installed)
    account.provider_failure(HTTPFailure(401), "heart a track")
    assert account.resolve(installed) is not held


def test_a_build_whose_client_library_does_not_import_is_not_bound(monkeypatch):
    monkeypatch.setitem(sys.modules, "tidalapi", None)
    monkeypatch.delitem(sys.modules, account.ADAPTER_MODULE, raising=False)
    assert account.bound() is False


# ── 5. the real workers, end to end, against the fake client ────────────────


def isrc_for(row: str) -> str:
    return f"AA00000000{int(row):02d}"


def give_rows_an_isrc(monkeypatch) -> None:
    """The one substitution beyond the client. See the module docstring."""
    for name, key in (("local_tracks", "identity"), ("heart_candidates", "row_id")):

        def given(library, track_ids, *, cfg, real=getattr(source, name), key=key):
            rows = real(library, track_ids, cfg=cfg)
            return tuple(replace(row, isrc=isrc_for(getattr(row, key))) for row in rows)

        monkeypatch.setattr(source, name, given)


def _argv(job_id: str) -> list[str]:
    """The command line that resumes ``job_id``."""
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def queue(exported: Path, *, sweep: bool) -> str:
    """The sweep or the export over ``exported``, approved and queued: its job."""
    if sweep:
        verb, gate = ["sync", "favorites"], "sync.favorites.confirm"
    else:
        verb, gate = ["export", "playlist", outbound_fakes.CRATE], "export.playlist.confirm"
    return approve_and_queue([*verb, "--export", str(exported)], gate)[1]


def run_job(monkeypatch, client: FakeClient, exported: Path, *, sweep: bool, ok: bool = True):
    """``client`` in, a session recorded, the job queued and resumed, its exit OK exactly
    when ``ok``: the answer and the job."""
    use_client(monkeypatch, client)
    record_session()
    job_id = queue(exported, sweep=sweep)
    code, resumed = drive(_argv(job_id))
    assert (code == int(ExitCode.OK)) is ok, resumed
    return resumed, job_id


def write_export(installed, **rows) -> Path:
    return outbound_fakes.write_export(installed.library.root / "outbound", **rows)


def numbered(base: int, rows=(1, 2, 3)) -> dict[str, list[str]]:
    """Each row's ISRC naming the one provider track ``base`` plus the row."""
    return {isrc_for(str(row)): [str(base + row)] for row in rows}


def test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart(installed, monkeypatch):
    exported = write_export(installed, favorites=(1, 2, 3))
    client = FakeClient(isrcs=numbered(500), hearts=["502"])
    give_rows_an_isrc(monkeypatch)
    resumed, _job = run_job(monkeypatch, client, exported, sweep=True)
    assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED)
    assert client.user.favorites.added == ["501", "503"]
    assert ledger.recorded_hearts(installed) == frozenset({"501", "503"})
    assert client.logins == 1
    assert client.user.favorites.pages == [(100, 0), (100, 100)]


def test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add(installed, monkeypatch):
    """And a second export finds the playlist recorded, so it neither creates nor sets the
    visibility: the private step is part of the create behind the ledger's check."""
    exported = write_export(installed)
    client = FakeClient(isrcs=numbered(700))
    give_rows_an_isrc(monkeypatch)
    resumed, job_id = run_job(monkeypatch, client, exported, sweep=False)
    assert client.user.created == [outbound_fakes.CRATE]
    (playlist,) = client.playlists.values()
    # Items two and three find the first item's record, so neither creates nor
    # touches the visibility the first one set (R-834).
    assert playlist.privates == 1 and playlist.public is False
    assert playlist.members == ["701", "702", "703"]
    # ONE ADD FOR THE JOB'S THREE TRACKS (U270): the batch goes in one request.
    assert playlist.adds == [["701", "702", "703"]]
    assert ledger.playlist_remote_id(installed, outbound_fakes.CRATE) == playlist.id
    assert ledger.playlist_added(installed, outbound_fakes.CRATE) == {"701", "702", "703"}
    reports = artifacts.committed(installed, job_id)
    assert [report["remote_id"] for report in reports] == [playlist.id] * 3
    # Somebody made it public at the provider since; that is theirs to keep.
    playlist.public = True
    account.forget()
    code, resumed = drive(_argv(queue(exported, sweep=False)))
    assert code == int(ExitCode.OK), resumed
    assert client.user.created == [outbound_fakes.CRATE]
    assert list(client.playlists) == [playlist.id]
    assert playlist.privates == 1 and playlist.public is True


def test_a_provider_failure_on_one_heart_fails_that_item_and_no_other(installed, monkeypatch):
    exported = write_export(installed, favorites=(1, 2, 3))
    client = FakeClient(isrcs=numbered(500))
    monkeypatch.setattr(tidal_account.time, "sleep", no_sleep)
    real_add = client.user.favorites.add_track

    def add_track(track_id: str) -> bool:
        if track_id == "502":
            raise HTTPFailure(503)
        return real_add(track_id)

    client.user.favorites.add_track = add_track
    give_rows_an_isrc(monkeypatch)
    _resumed, job_id = run_job(monkeypatch, client, exported, sweep=True, ok=False)
    with jobs.open_store() as store:
        causes = {
            item.item_id: (item.cause.reason if item.cause else None)
            for item in jobs.items(store, job_id)
        }
    assert causes == {"1": None, "2": "unavailable-transient", "3": None}
    assert ledger.recorded_hearts(installed) == frozenset({"501", "503"})


def test_a_row_whose_file_carries_no_isrc_matches_nothing(installed, monkeypatch):
    """No substitution and no file behind the rows: honest unmatched rows, no call (R-355)."""
    exported = write_export(installed, favorites=(1, 2))
    client = FakeClient(isrcs=numbered(500, (1, 2)), tracks={"1", "2"})
    resumed, job_id = run_job(monkeypatch, client, exported, sweep=True)
    assert client.user.favorites.added == []
    assert client.isrc_asked == [] and client.track_asked == []
    reports = artifacts.committed(installed, job_id)
    assert [report["unmatched"] for report in reports] == [["1"], ["2"]]


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> bytes:
    """One FLAC of silence, synthesized once for every drive that tags a file."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac").read_bytes()


def _tagged_flac(installed, silence: bytes, index: int, isrc: str) -> str:
    """A real FLAC under the library root carrying ``isrc``, as an export location."""
    target = Path(installed.library.root) / "Music" / f"{index}.flac"
    target.write_bytes(silence)
    assert tags.write_tags(target, {"isrc": isrc}) is True
    return locations.location_url(target)


def test_a_sweep_matches_through_the_isrc_the_file_carries(installed, monkeypatch, silence):
    """R-355 closed, no substitution: row 1's file carries a hyphenated ISRC, row 2's none."""
    exported = write_export(
        installed,
        favorites=(1, 2),
        locations={
            1: _tagged_flac(installed, silence, 1, "aa-000-00-00001"),
            2: _tagged_flac(installed, silence, 2, ""),
        },
    )
    client = FakeClient(isrcs={isrc_for("1"): ["501"], isrc_for("2"): ["502"]})
    resumed, job_id = run_job(monkeypatch, client, exported, sweep=True)
    assert client.isrc_asked == [isrc_for("1")]
    assert client.user.favorites.added == ["501"]
    reports = artifacts.committed(installed, job_id)
    assert [report["unmatched"] for report in reports] == [[], ["2"]]


# ── R-356, driven with no substitution: the names come off the export ──


def _alike(first: str, second: str, title: str, artist: str) -> list[Track]:
    """Two releases of one recording spelled alike, a single and its album cut."""
    return [Track(first, title, None, (artist,)), Track(second, title, None, (artist,))]


def _three_tagged(installed, silence: bytes) -> dict[int, str]:
    return {row: _tagged_flac(installed, silence, row, isrc_for(str(row))) for row in (1, 2, 3)}


def _releases_for_three_rows() -> dict[str, list]:
    """Row 1 has an edit beside the plain record, row 2 two spelled alike, row 3 one
    release. The export spells each row ``08A - 124 - Track N``."""
    return {
        isrc_for("1"): [
            Track("501", "Track 1", "Radio Edit", ("Artist 1",)),
            Track("511", "Track 1", None, ("Artist 1",)),
        ],
        isrc_for("2"): _alike("502", "512", "Track 2", "Artist 2"),
        isrc_for("3"): ["503"],
    }


def test_the_release_title_is_the_display_title_with_the_naming_head_off(installed):
    from cratekit.modules.reports.export import CollectionEntry

    template = source._template(installed)
    marker = installed.naming.lossy_marker
    assert marker, "the fixture configuration declares a lossy marker"

    def entry(name: str) -> CollectionEntry:
        return CollectionEntry(track_id="1", name=name, artist="a", location="")

    assert source.release_title(entry("08A - 124 - Sun Path"), template=template) == "Sun Path"
    assert (
        source.release_title(entry(f"08A - 124 - {marker} Sun Path (Dub)"), template=template)
        == "Sun Path (Dub)"
    )
    assert source.release_title(entry("Sun Path"), template=template) == "Sun Path"


def test_a_configuration_with_no_marker_text_still_strips_the_head(installed):
    from cratekit.modules.reports.export import CollectionEntry

    bare = replace(installed, naming=replace(installed.naming, lossy_marker=""))
    row = CollectionEntry(track_id="1", name="08A - 124 - Sun Path", artist="a", location="")
    assert source.release_title(row, template=source._template(bare)) == "Sun Path"


def test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not(
    installed, monkeypatch, silence
):
    placed = _three_tagged(installed, silence)
    exported = write_export(installed, favorites=(1, 2, 3), locations=placed)
    client = FakeClient(isrcs=_releases_for_three_rows())
    resumed, job_id = run_job(monkeypatch, client, exported, sweep=True)
    assert client.user.favorites.added == ["511", "503"]
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["unmatched"] == ["2"]
    (reason,) = outbound["reasons"]
    assert reason.startswith("Artist 2 - Track 2 (row 2): "), reason
    assert "names 2 provider tracks" in reason and "2 of them agree" in reason
    reports = artifacts.committed(installed, job_id)
    assert [[one["row"] for one in report["reasons"]] for report in reports] == [[], ["2"], []]


def test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not(
    installed, monkeypatch, silence
):
    exported = write_export(installed, locations=_three_tagged(installed, silence))
    client = FakeClient(isrcs=_releases_for_three_rows())
    resumed, job_id = run_job(monkeypatch, client, exported, sweep=False)
    (playlist,) = client.playlists.values()
    assert playlist.members == ["511", "503"]
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["unmatched"] == ["2"]
    (reason,) = outbound["reasons"]
    assert reason.startswith("Artist 2 - 08A - 124 - Track 2 (row 2): "), reason
    assert "names 2 provider tracks" in reason
    (row,) = [
        row for report in artifacts.committed(installed, job_id) for row in report["unmatched"]
    ]
    assert row["title"] == "08A - 124 - Track 2", "reported as the library shows it"
    assert "names 2 provider tracks" in row["reason"]
    # R-850: the answer lists the row with that same reason, and counts it.
    assert outbound["counts"] == {"written": 2, "already": 0, "unmatched": 1}
    (listed,) = outbound["unmatched_tracks"]
    assert (listed["artist"], listed["title"]) == ("Artist 2", "08A - 124 - Track 2")
    assert listed["reason"] == row["reason"]
    code, said = drive_human(_argv(job_id))
    assert code == int(ExitCode.OK), said
    assert f"    unmatched: Artist 2 - 08A - 124 - Track 2: {row['reason']}" in said, said


def test_a_release_the_account_already_hearts_is_the_one_an_export_adds(
    installed, monkeypatch, silence
):
    exported = write_export(installed, crate=(2,), locations=_three_tagged(installed, silence))
    client = FakeClient(isrcs=_releases_for_three_rows(), hearts=["512"])
    resumed, _job = run_job(monkeypatch, client, exported, sweep=False)
    (playlist,) = client.playlists.values()
    assert playlist.members == ["512"]
    assert resumed["data"]["progress"]["outbound"]["reasons"] == []


def test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope(
    installed, monkeypatch, silence
):
    exported = write_export(installed, crate=(1, 3), locations=_three_tagged(installed, silence))
    client = FakeClient(isrcs={isrc_for("3"): ["503"]})
    resumed, _job = run_job(monkeypatch, client, exported, sweep=False)
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["unmatched"] == ["1"] and outbound["reasons"] == []
    # R-850: ``reasons`` omits it, and the answer's list still names it.
    (listed,) = outbound["unmatched_tracks"]
    assert listed["identity"] == "1" and listed["reason"] == export_cli.NO_MATCH


# ── 6. structural guards over the adapter's own source ──────────────────────


@functools.cache
def _trees() -> tuple[ast.Module, ...]:
    """Each adapter module parsed once for every guard."""
    return tuple(ast.parse(path.read_text(encoding="utf-8")) for path in ADAPTER_SOURCES)


def test_the_adapter_imports_nothing_vendored():
    imported: list[str] = []
    for node in (node for tree in _trees() for node in ast.walk(tree)):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert imported, "the scan read no imports at all"
    assert not [name for name in imported if "_vendor" in name], imported


def test_the_adapter_pages_nothing_by_hand():
    calls = [
        (node.lineno, node.func.attr)
        for tree in _trees()
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in listing.GUARDED_METHODS
    ]
    assert calls == [], f"the adapter calls a paging method directly: {calls}"


#: The removals the adapter may name on the client, each in the one member it
#: may name it in: R-836's by position, U123's playlist delete, and U143's root
#: playlist delete and legacy folder removal. Anything else is a new write.
ADMITTED_REMOVALS = {
    "remove_tracks": "remove_by_indices",
    "remove_playlist": "delete",
    "remove_root_playlist": "delete",
    "remove_legacy_folder": "remove_folders_playlists",
}


def test_the_adapter_names_each_remove_on_the_client_inside_its_one_member():
    """A removal shape anywhere else in the adapter's modules, or another in a member, fails."""
    shapes = ("remove", "delete", "unheart", "unlike", "clear")
    defined = [
        node.name
        for tree in _trees()
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and any(s in node.name.lower() for s in shapes)
    ]
    named = {
        (inside, attr)
        for tree in _trees()
        for inside, attr in _attributes(tree)
        if any(s in attr.lower() for s in shapes)
    }
    assert sorted(defined) == sorted(ADMITTED_REMOVALS), defined
    assert named == set(ADMITTED_REMOVALS.items()), sorted(named)


def _attributes(node: ast.AST, inside: str = ""):
    """Each attribute named under ``node``, with the innermost function holding it, or ``""``."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Attribute):
            yield inside, child.attr
        yield from _attributes(child, child.name if isinstance(child, ast.FunctionDef) else inside)


def test_the_client_library_still_offers_the_private_call_a_create_relies_on():
    """``_make_private`` passes over a client with no such call rather than orphan the
    playlist, so a rename upstream would turn R-834 off with a green suite."""
    import tidalapi.playlist

    assert callable(getattr(tidalapi.playlist.UserPlaylist, "set_playlist_private", None))
    assert any("set_playlist_private" in path.read_text("utf-8") for path in ADAPTER_SOURCES)


def test_the_adapter_satisfies_the_protocol_it_is_handed_out_as():
    declared = {name for name in vars(RemoteAccount) if not name.startswith("_")}
    assert declared == outbound_fakes.PROTOCOL_METHODS
    for name in declared:
        assert callable(getattr(tidal_account.TidalAccount, name, None)), name


# ── R-572: the file's album tag tells releases spelled alike apart ──


def on_album(track: Track, name: str) -> Track:
    """The track as the client hands it out, sitting on the release ``name``."""
    track.album = SimpleNamespace(name=name)
    return track


def single_and_album_cut(hearts: list[str] = ()) -> FakeClient:
    """A single and its album cut, spelled alike, the account hearting ``hearts``."""
    single, cut = on_album(sun("101"), "Sun Path"), on_album(sun("202"), "Tidal Lines")
    return releases(single, cut, hearts=hearts)


def by_album(found: tidal_account.TidalAccount, album: str) -> str | None:
    return match_row(found, "Sun Path", album=album)


def test_releases_spelled_alike_resolve_to_the_one_the_files_album_names():
    found = adapter(single_and_album_cut())
    assert by_album(found, " tidal LINES ") == "202"
    assert found.unmatched_reason("7") == ""


def test_a_file_album_naming_neither_release_stays_unmatched_and_says_so():
    found = adapter(single_and_album_cut())
    assert by_album(found, "Night Drives") is None
    reason = found.unmatched_reason("7")
    assert "hearts 0 of those" in reason
    assert "the file's album 'Night Drives' names 0 of them" in reason


def test_a_file_album_matching_both_releases_stays_unmatched():
    found = adapter(releases(on_album(sun("101"), "Sun Path"), on_album(sun("202"), "Sun Path")))
    assert by_album(found, "Sun Path") is None
    assert "the file's album 'Sun Path' names 2 of them" in found.unmatched_reason("7")


def test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing():
    found = adapter(single_and_album_cut())
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert "2 of them agree" in reason and "hearts 0 of those" in reason
    assert "the file carries no album tag" in reason


def test_an_unreadable_track_stops_the_album_from_choosing_the_lone_agreeing_one():
    """Rule 1 already refuses this shape; the album must not choose the same lone track."""
    client = releases(*(on_album(one, "Tidal Lines") for one in (sun("101"), unreadable("202"))))
    found = adapter(client)
    assert by_album(found, "Tidal Lines") is None
    reason = found.unmatched_reason("7")
    assert "1 could not be read" in reason
    assert "so none was chosen" in reason
    client.user.favorites.hearts = ["101"]
    assert by_album(adapter(client), "Tidal Lines") == "101", (
        "the heart rule still chooses among agreeing tracks"
    )


def test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two():
    """Out of scope by the brief: how a hearted release breaks a tie is unchanged."""
    assert by_album(adapter(single_and_album_cut(["101"])), "Tidal Lines") == "101"
    found = adapter(single_and_album_cut(["101", "202"]))
    assert by_album(found, "Tidal Lines") is None
    assert "hearts 2 of those, so none was chosen" in found.unmatched_reason("7")


def test_the_album_chooses_only_among_releases_that_agree_with_the_row():
    """The radio edit sits on the album the file names, and the row is the plain record."""
    client = releases(
        on_album(sun("101"), "Sun Path"),
        on_album(sun("202"), "Night Drives"),
        on_album(sun("303", "Radio Edit"), "Tidal Lines"),
    )
    assert by_album(adapter(client), "Tidal Lines") is None


def test_a_sweep_hearts_the_release_the_files_album_tag_names(installed, monkeypatch, silence):
    """Driven end to end: the album comes off the file in the same read as the ISRC."""
    placed = _three_tagged(installed, silence)
    two = Path(installed.library.root) / "Music" / "2.flac"
    assert tags.write_tags(two, {"album": "Track 2 (Deluxe)"}) is True
    exported = write_export(installed, favorites=(1, 2, 3), locations=placed)
    shapes = _releases_for_three_rows()
    single, cut = shapes[isrc_for("2")]
    on_album(single, "Track 2")
    on_album(cut, "Track 2 (Deluxe)")
    client = FakeClient(isrcs=shapes)
    resumed, _job = run_job(monkeypatch, client, exported, sweep=True)
    assert client.user.favorites.added == ["511", "512", "503"]
    assert resumed["data"]["progress"]["outbound"]["unmatched"] == []


# ── R-1032: a listening copy takes one of several agreeing releases ──


def any_release(found: tidal_account.TidalAccount, album: str = "", title: str = "Sun Path"):
    return match_row(found, title, album=album, any_agreeing=True)


def three_on_albums() -> FakeClient:
    return releases(
        on_album(sun("101"), "Sun Path"),
        on_album(sun("303"), "Tidal Lines"),
        on_album(sun("202"), "Tidal Lines"),
    )


def tie(*ids: str) -> list[Track]:
    return [sun(one) for one in ids]


def test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order():
    for listed in (("202", "101"), ("101", "202")):
        found = another_catalogue(releases(*tie(*listed)))
        assert any_release(found) == "101", listed
        assert found.unmatched_reason("7") == ""
    found = another_catalogue(releases(*tie("100", "99")))
    assert any_release(found) == "99", "numeric order, not the order of the characters"


def test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads():
    found = adapter(releases(*tie("202", "101")))
    assert match_row(found, "Sun Path") is None
    assert service.AGREEING_RELEASES in found.unmatched_reason("7")


def test_a_file_album_naming_none_of_the_tied_releases_still_takes_one():
    assert any_release(adapter(single_and_album_cut()), album="Night Drives") == "101"


def test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two():
    assert any_release(adapter(three_on_albums()), album="Tidal Lines") == "202"


def test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one():
    client = releases(*tie("101", "202", "303", "404"), hearts=["404", "202"])
    assert any_release(adapter(client)) == "202"


def test_a_lone_heart_and_a_lone_album_choose_as_they_always_did():
    assert any_release(adapter(single_and_album_cut(["202"]))) == "202"
    assert any_release(adapter(single_and_album_cut()), album="Tidal Lines") == "202"


def test_a_release_that_does_not_agree_is_never_taken():
    assert any_release(adapter(releases(sun("101", "Radio Edit"), *tie("303", "202")))) == "202"
    found = another_catalogue(releases(sun("101", "Radio Edit"), sun("202", "Extended Mix")))
    assert any_release(found) is None
    assert "none of them agrees" in found.unmatched_reason("7")


def test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing():
    found = adapter(releases(*tie("101", "202"), unreadable("303")))
    assert any_release(found) is None
    reason = found.unmatched_reason("7")
    assert "1 could not be read" in reason and service.AGREEING_RELEASES in reason


def test_a_row_with_no_title_to_judge_agreement_by_still_refuses_with_any_agreeing():
    found = adapter(releases(*tie("101", "202")))
    assert any_release(found, title="") is None
    assert "no artist and title" in found.unmatched_reason("7")


def test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name():
    """An empty tag is not a name: it must not pick out the release the provider left unnamed."""
    client = releases(on_album(sun("101"), "Sun Path"), on_album(sun("202"), ""))
    assert any_release(adapter(client)) == "101"


def test_the_files_album_narrows_a_tie_under_the_products_own_fold():
    """Case and spacing on the tag do not stop it naming the album cut over the lower single."""
    assert any_release(adapter(single_and_album_cut()), album=" tidal LINES ") == "202"


# ── U208: the adapter says when ``any_agreeing`` broke a tie ──


def test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is():
    found = adapter(releases(*tie("202", "101")))
    assert any_release(found) == "101"
    assert found.tie_broken("7") is True
    assert match_row(found, "Sun Path") is None, "without any_agreeing the tie refuses"
    assert found.tie_broken("7") is False, "a miss clears what the last match said"


def test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie():
    found = adapter(releases(sun("101")))
    assert any_release(found) == "101" and found.tie_broken("7") is False
    found = another_catalogue(single_and_album_cut(["202"]))
    assert any_release(found) == "202" and found.tie_broken("7") is False
    found = another_catalogue(single_and_album_cut())
    assert any_release(found, album="Tidal Lines") == "202"
    assert found.tie_broken("7") is False, "the album rule chose, as it does without the flag"


def test_two_hearts_or_an_album_naming_two_is_a_broken_tie():
    found = adapter(releases(*tie("101", "202"), hearts=["202", "101"]))
    assert any_release(found) == "101" and found.tie_broken("7") is True
    found = another_catalogue(three_on_albums())
    assert any_release(found, album="Tidal Lines") == "202" and found.tie_broken("7") is True


def test_a_refused_tie_is_never_said_to_be_broken():
    found = adapter(releases(*tie("101", "202"), unreadable("303")))
    assert any_release(found) is None and found.tie_broken("7") is False


def test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie():
    """Without ``any_agreeing`` two hearts refuse whatever the album says, so this broke one."""
    client = releases(
        on_album(sun("101"), "Sun Path"),
        on_album(sun("202"), "Tidal Lines"),
        on_album(sun("303"), "Night Drives"),
        hearts=["303", "202"],
    )
    found = adapter(client)
    assert any_release(found, album="Tidal Lines") == "202"
    assert found.tie_broken("7") is True
    assert match_row(found, "Sun Path") is None
