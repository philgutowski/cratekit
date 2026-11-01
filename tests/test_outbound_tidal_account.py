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
from cratekit.export import cli as export_cli
from cratekit.modules.outbound import account, artifacts, ledger, service, source, tidal_account
from cratekit.modules.outbound.service import RemoteAccount
from tests import outbound_fakes
from tests._containers import synth_container
from tests.cli_drive import approve_and_queue, drive, drive_human
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


class Artist:
    def __init__(self, name: str) -> None:
        self.name = name


class Track:
    """A provider track in the client's own shape: a name, a version field of its
    own, a first artist and the list of every artist billed."""

    def __init__(
        self,
        track_id: str,
        name: str = "",
        version: str | None = None,
        artists: tuple[str, ...] = (),
    ) -> None:
        self.id = int(track_id)
        self.name = name
        self.version = version
        self.artists = [Artist(one) for one in artists]
        self.artist = self.artists[0] if self.artists else None
        #: The client's own name for "the provider will play this".
        self.available = True


def withdrawn(track: Track) -> Track:
    """The track as the client hands out one the provider will not play.

    The client reads ``version`` only inside ``if self.available``, so a
    withdrawn extended mix arrives with no version and reads as the plain record.
    """
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
        # ``None`` until the client is asked, so a test can tell a playlist
        # made private from one whose visibility nobody touched.
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
    """A playlist the session does not own, which the client hands out unedited.

    The client returns a read only object for somebody else's playlist and an
    editable one for the account's own, so the absence of ``edit`` is the shape
    a rename meets rather than a raise.
    """

    def __init__(self, playlist_id: str, name: str = "") -> None:
        self.id = playlist_id
        self.name = name
        self.members: list[str] = []

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
        # The queued refusals belong to this playlist alone, so a test that
        # creates two cannot have the first one's leftovers reach the second.
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
        """``isrcs`` maps a code to identifiers, or to whole tracks when a test
        needs the provider's own spelling of each release."""
        self.isrc_asked.append(isrc)
        if isrc not in self.isrcs:
            raise ObjectNotFound(isrc)
        return [
            one if isinstance(one, Track) else Track(one) for one in self.isrcs[isrc]
        ]

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


# ── R-356: several releases under one ISRC ─────────────────────────────────

CODE = "AA0000000001"


def releases(*tracks: Track) -> FakeClient:
    return FakeClient(isrcs={CODE: list(tracks)})


def match_row(found: tidal_account.TidalAccount, title: str, artist: str = "Nova Reef"):
    return found.match_track(identity="7", isrc=CODE, title=title, artist=artist)


def test_the_measured_cost_three_releases_of_one_isrc_resolve_to_the_rows_version():
    """The fourth sitting's shape: a single, an EP cut and a compilation track.

    Before R-356 every one of these rows came back unmatched, which was two of
    four export rows and most of fifty favourites on a real library.
    """
    client = releases(
        Track("101", "Sun Path", "Radio Edit", ("Nova Reef",)),
        Track("202", "Sun Path", "Extended Mix", ("Nova Reef",)),
        Track("303", "Sun Path", "Ten Year Remaster", ("Nova Reef",)),
    )
    found = adapter(client)
    assert match_row(found, "Sun Path (Extended Mix)") == "202"
    assert found.unmatched_reason("7") == ""
    assert client.user.favorites.pages == [], "one agreeing track asks the hearts nothing"


def test_a_code_asked_to_agree_lists_its_one_track_only_when_it_is_the_row():
    """R-879: a code read off a library file's tag, which may be another
    recording's, names its one provider track only when that track agrees."""
    client = releases(Track("101", "Sun Path", None, ("Nova Reef",)))
    found = adapter(client)
    assert found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", agree=True
    ) == "101"
    assert found.match_track(
        identity="8", isrc=CODE, title="Moon Path", artist="Nova Reef", agree=True
    ) is None
    assert "none of them agrees" in found.unmatched_reason("8")
    # Without it, one track is the match as it always was.
    assert found.match_track(identity="9", isrc=CODE, title="Moon Path", artist="Nova Reef") == "101"


def test_a_row_with_no_version_agrees_with_an_original_mix_and_not_with_an_edit():
    client = releases(
        Track("101", "Sun Path", "Original Mix", ("Nova Reef",)),
        Track("202", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    assert match_row(adapter(client), "Sun Path") == "101"


def test_a_version_the_provider_spells_inside_the_title_is_read_the_same_way():
    client = releases(
        Track("101", "Sun Path - Radio Edit", None, ("Nova Reef",)),
        Track("202", "Sun Path (Extended Mix)", None, ("Nova Reef",)),
    )
    assert match_row(adapter(client), "Sun Path (Radio Edit)") == "101"


def test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
        Track("303", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert f"the ISRC {CODE} names 3 provider tracks" in reason
    assert "2 of them agree" in reason
    assert "hearts 0 of those" in reason


def test_among_releases_spelled_alike_the_one_already_hearted_is_the_match():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
    client.user.favorites.hearts = ["202"]
    found = adapter(client)
    assert match_row(found, "Sun Path") == "202"
    assert found.unmatched_reason("7") == ""


def test_two_hearted_releases_spelled_alike_are_still_no_match():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
    client.user.favorites.hearts = ["101", "202"]
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert "hearts 2 of those" in found.unmatched_reason("7")


def test_a_heart_on_a_release_the_row_does_not_name_decides_nothing():
    """The hearted one is the radio edit, and the row is the plain record."""
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
        Track("303", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    client.user.favorites.hearts = ["303"]
    assert match_row(adapter(client), "Sun Path") is None


def test_no_release_agreeing_is_no_match_and_the_hearts_are_not_read():
    """An ISRC the provider filed on another record chooses nothing, hearted or not."""
    client = releases(
        Track("101", "Moon Road", None, ("Nova Reef",)),
        Track("202", "Moon Road", "Dub", ("Nova Reef",)),
    )
    client.user.favorites.hearts = ["101"]
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert "none of them agrees" in found.unmatched_reason("7")
    assert client.user.favorites.pages == []


def test_another_artist_under_the_same_title_does_not_agree():
    client = releases(
        Track("101", "Sun Path", None, ("Aurora Bloom",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
    assert match_row(adapter(client), "Sun Path") == "202"


def test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef", "Mira Vale")),
        Track("202", "Sun Path", "Radio Edit", ("Nova Reef", "Mira Vale")),
    )
    found = adapter(client)
    assert match_row(found, "Sun Path", artist="Nova Reef, Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef & Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef") == "101"
    assert match_row(found, "Sun Path", artist="Mira Vale") is None, "the guest alone"
    assert match_row(found, "Sun Path", artist="Mira Vale, Nova Reef") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef feat. Mira Vale") == "101"
    assert match_row(found, "Sun Path", artist="Nova Reef, Mira Vale, Kai Tern") is None
    assert match_row(found, "Sun Path", artist="Nova") is None, "half a name"


def test_a_remixer_the_provider_bills_and_the_row_does_not_is_still_agreement():
    client = releases(
        Track("101", "Sun Path", "Kai Tern Remix", ("Nova Reef", "Kai Tern")),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
    assert match_row(adapter(client), "Sun Path (Kai Tern Remix)") == "101"


def test_a_track_the_provider_will_not_play_is_never_the_choice():
    """Its version was never read, so a withdrawn extended mix looks like the plain record."""
    client = releases(
        Track("101", "Sun Path", "Radio Edit", ("Nova Reef",)),
        withdrawn(Track("202", "Sun Path", "Extended Mix", ("Nova Reef",))),
    )
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert "1 cannot be streamed" in reason and "none of the rest agrees" in reason
    client.user.favorites.hearts = ["202"]
    assert match_row(adapter(client), "Sun Path") is None, "a heart does not revive it"


def test_a_withdrawn_release_does_not_stop_the_one_that_plays_from_being_chosen():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        withdrawn(Track("202", "Sun Path", None, ("Nova Reef",))),
    )
    assert match_row(adapter(client), "Sun Path") == "101"


def test_a_provider_title_that_reads_two_ways_agrees_under_either_too():
    """The same recording must resolve whichever side spelled the version with a dash."""
    client = releases(
        Track("101", "Sun Path - Live", None, ("Nova Reef",)),
        Track("202", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    assert match_row(adapter(client), "Sun Path (Live)") == "101"


def test_a_row_carrying_no_names_chooses_nothing_and_asks_the_hearts_nothing():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    client.user.favorites.hearts = ["101"]
    found = adapter(client)
    assert found.match_track(identity="7", isrc=CODE) is None
    assert found.match_track(identity="7", isrc=CODE, title="Sun Path") is None
    assert found.match_track(identity="7", isrc=CODE, artist="Nova Reef") is None
    assert "no artist and title" in found.unmatched_reason("7")
    assert client.user.favorites.pages == []


def test_a_release_that_cannot_be_read_stops_a_lone_agreeing_one_from_being_chosen():
    """One agreeing track beside one nobody could read is not known to be the only one."""
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "", None, ()),
    )
    found = adapter(client)
    assert match_row(found, "Sun Path") is None
    assert "1 could not be read" in found.unmatched_reason("7")
    client.user.favorites.hearts = ["101"]
    assert match_row(adapter(client), "Sun Path") == "101"


def test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one():
    one = releases(
        Track("101", "Sun Path", "Live", ("Nova Reef",)),
        Track("202", "Sun Path", "Radio Edit", ("Nova Reef",)),
    )
    assert match_row(adapter(one), "Sun Path - Live") == "101"
    both = releases(
        Track("101", "Sun Path", "Live", ("Nova Reef",)),
        Track("202", "Sun Path - Live", None, ("Nova Reef",)),
    )
    assert match_row(adapter(both), "Sun Path - Live") is None


def test_a_reason_does_not_outlive_the_match_it_was_about():
    client = releases(
        Track("101", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
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
    client = releases(Track("101", "Sun Path", None, ("Nova Reef",)))
    client.search = lambda *args, **kwargs: pytest.fail("the adapter searched")
    assert match_row(adapter(client), "Sun Path") == "101"
    assert client.isrc_asked == [CODE] and client.track_asked == []


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


# ── visibility, R-834 ───────────────────────────────────────────────────────


def test_a_created_playlist_is_made_private_once():
    client = FakeClient()

    created = adapter(client).create_playlist("Crate")

    playlist = client.playlists[created]
    assert playlist.public is False
    assert playlist.privates == 1


def test_a_private_step_refused_once_is_retried_once_and_lands():
    client = FakeClient()
    client.user.private_fail.append(TimeoutError("timed out"))

    created = adapter(client).create_playlist("Crate")

    playlist = client.playlists[created]
    assert playlist.privates == 2
    assert playlist.public is False
    assert client.user.created == ["Crate"]


def test_a_private_step_refused_twice_still_hands_back_the_one_playlist():
    """Raising here would leave the playlist unrecorded and the next item would
    create another; the refusal costs the visibility instead (R-849)."""
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

    class Bare:
        id = "00000000-0000-4000-8000-0000000000aa"

    client.user.create_playlist = lambda title, description: Bare()

    assert adapter(client).create_playlist("Crate") == Bare.id


# ── the retitle, R-358 ──────────────────────────────────────────────────────


def test_a_rename_retitles_the_playlist_and_leaves_its_membership_alone():
    playlist = Playlist("pl-1", ["101", "102"], name="Warmup")
    client = FakeClient(playlists={"pl-1": playlist})
    remote = adapter(client)

    remote.rename_playlist("pl-1", "DOWNLOADED Warmup")

    assert playlist.name == "DOWNLOADED Warmup"
    assert playlist.edits == [("DOWNLOADED Warmup", None)]
    assert playlist.members == ["101", "102"]
    assert playlist.adds == []


def test_a_rename_the_client_answers_false_is_the_items_cause_not_a_quiet_return():
    """A mark reported as applied over a title that never changed is the whole defect."""
    playlist = Playlist("pl-1", name="Warmup")
    playlist.edit_answer = False
    client = FakeClient(playlists={"pl-1": playlist})

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup")

    assert playlist.name == "Warmup"
    assert excinfo.value.cause.scope is Scope.ITEM
    assert excinfo.value.cause.reason == "unavailable-transient"


def test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename():
    """THE MESSAGE IS THE ASSERTION, because without the guard this still raises.

    A missing editor called anyway is a ``TypeError`` inside ``_call``, which
    ``provider_failure`` translates into the same slug at the same scope with the
    same doing string. Only the sentence naming the editor separates a refusal
    that diagnosed the playlist from one that tripped over it and was retried.
    """
    foreign = ForeignPlaylist("pl-1", name="Somebody Else")
    client = FakeClient(playlists={"pl-1": foreign})

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).rename_playlist("pl-1", "DOWNLOADED Somebody Else")

    assert excinfo.value.cause.scope is Scope.ITEM
    assert "cannot be retitled by this account" in excinfo.value.cause.message
    assert foreign.name == "Somebody Else"


def test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause():
    """The client answers an explicit not found rather than raising through, and
    a rename that returned here would be a mark nothing carries."""

    class Vanishing(Playlist):
        def edit(self, title=None, description=None):
            raise ObjectNotFound(self.id)

    playlist = Vanishing("pl-1", name="Warmup")
    client = FakeClient(playlists={"pl-1": playlist})

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup")

    assert excinfo.value.cause.scope is Scope.ITEM
    assert playlist.name == "Warmup"


@pytest.mark.parametrize("blank", ["", "   ", "\n"])
def test_a_rename_with_no_title_is_refused_before_the_client_sees_it(blank):
    """The client reads a falsy title as keep the current one and answers True,
    so an empty title would be a write that changed nothing, reported as a
    rename that succeeded."""
    playlist = Playlist("pl-1", name="Warmup")
    client = FakeClient(playlists={"pl-1": playlist})

    with pytest.raises(CratekitError) as excinfo:
        adapter(client).rename_playlist("pl-1", blank)

    assert playlist.edits == [], "the empty title reached the client"
    assert playlist.name == "Warmup"
    assert excinfo.value.cause.reason == "internal-error"
    assert excinfo.value.cause.scope is Scope.SOURCE
    # The MESSAGE, not only the slug. A refusal that says the right thing about
    # the wrong mechanism is the shape this file's other tests already watch for.
    assert "reads a falsy title as keep the current one" in excinfo.value.cause.message


def test_a_title_the_caller_padded_is_written_as_the_caller_asked():
    """The emptiness test strips. The write does not."""
    playlist = Playlist("pl-1", name="Warmup")
    client = FakeClient(playlists={"pl-1": playlist})

    adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup ")

    assert playlist.name == "DOWNLOADED Warmup "


def test_a_rename_of_a_playlist_the_provider_lacks_is_the_items_cause():
    with pytest.raises(CratekitError) as excinfo:
        adapter(FakeClient()).rename_playlist("pl-9", "DOWNLOADED Gone")

    assert excinfo.value.cause.scope is Scope.ITEM


def test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title():
    """Unlike a create, a retry asks for the state the first attempt asked for."""
    playlist = Playlist("pl-1", name="Warmup")
    playlist.edit_fail = [HTTPFailure(429)]
    client = FakeClient(playlists={"pl-1": playlist})

    adapter(client).rename_playlist("pl-1", "DOWNLOADED Warmup")

    assert playlist.edits == [("DOWNLOADED Warmup", None), ("DOWNLOADED Warmup", None)]
    assert playlist.name == "DOWNLOADED Warmup"


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


def _resume_human(job_id: str) -> tuple[int, str]:
    """The same resume as :func:`_resume`, answered in the default output mode."""
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    return drive_human(cli_jobs.argv_for(job))


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
    # Items two and three find the first item's record, so neither creates and
    # neither touches the visibility the first one set (R-834).
    assert playlist.privates == 1 and playlist.public is False
    assert playlist.members == ["701", "702", "703"]
    assert playlist.adds == [["701"], ["702"], ["703"]]
    assert ledger.playlist_remote_id(installed, outbound_fakes.CRATE) == playlist.id
    assert ledger.playlist_added(installed, outbound_fakes.CRATE) == frozenset(
        {"701", "702", "703"}
    )
    reports = artifacts.committed(installed, job_id)
    assert [report["remote_id"] for report in reports] == [playlist.id] * 3


def test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility(
    installed, monkeypatch
):
    """The check before write is the ledger's, and the private step is part of
    the create behind it, so a run that finds the playlist recorded never asks."""
    exported = outbound_fakes.write_export(installed.library.root / "outbound")
    client = use_client(
        monkeypatch,
        FakeClient(isrcs={isrc_for(str(row)): [str(700 + row)] for row in (1, 2, 3)}),
    )
    record_session()
    give_rows_an_isrc(monkeypatch)
    _run, first = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    assert _resume(first)[0] == int(ExitCode.OK)
    (playlist,) = client.playlists.values()
    # Somebody made it public at the provider since; that is theirs to keep.
    playlist.public = True
    account.forget()

    _run, second = approve_and_queue(export_verb(exported), "export.playlist.confirm")
    code, resumed = _resume(second)

    assert code == int(ExitCode.OK), resumed
    assert client.user.created == [outbound_fakes.CRATE]
    assert list(client.playlists) == [playlist.id]
    assert playlist.privates == 1 and playlist.public is True


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


# ── R-356, driven with no substitution: the names come off the export ─────


def _alike(first: str, second: str, title: str, artist: str) -> list[Track]:
    """Two releases of one recording spelled alike, a single and its album cut."""
    return [Track(first, title, None, (artist,)), Track(second, title, None, (artist,))]


def _three_tagged(installed, tmp_path) -> dict[int, str]:
    return {
        row: _tagged_flac(installed, tmp_path / str(row), row, isrc_for(str(row)))
        for row in (1, 2, 3)
    }


def _releases_for_three_rows() -> dict[str, list]:
    """Row 1 has an edit beside the plain record, row 2 has two spelled alike,
    and row 3 has one release. The export spells each row ``08A - 124 - Track N``."""
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
    bare = replace(installed, naming=replace(installed.naming, lossy_marker=""))
    from cratekit.modules.reports.export import CollectionEntry

    row = CollectionEntry(track_id="1", name="08A - 124 - Sun Path", artist="a", location="")
    assert source.release_title(row, template=source._template(bare)) == "Sun Path"


def test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not(
    installed, monkeypatch, tmp_path
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound",
        favorites=(1, 2, 3),
        locations=_three_tagged(installed, tmp_path),
    )
    client = use_client(monkeypatch, FakeClient(isrcs=_releases_for_three_rows()))
    record_session()
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert client.user.favorites.added == ["511", "503"]
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["unmatched"] == ["2"]
    (reason,) = outbound["reasons"]
    assert reason.startswith("Artist 2 - Track 2 (row 2): "), reason
    assert "names 2 provider tracks" in reason and "2 of them agree" in reason
    reports = artifacts.committed(installed, job_id)
    assert [[one["row"] for one in report["reasons"]] for report in reports] == [
        [],
        ["2"],
        [],
    ]


def test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not(
    installed, monkeypatch, tmp_path
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound",
        locations=_three_tagged(installed, tmp_path),
    )
    client = use_client(monkeypatch, FakeClient(isrcs=_releases_for_three_rows()))
    record_session()
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
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
    code, said = _resume_human(job_id)
    assert code == int(ExitCode.OK), said
    assert f"    unmatched: Artist 2 - 08A - 124 - Track 2: {row['reason']}" in said, said


def test_a_release_the_account_already_hearts_is_the_one_an_export_adds(
    installed, monkeypatch, tmp_path
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound",
        crate=(2,),
        locations=_three_tagged(installed, tmp_path),
    )
    client = use_client(
        monkeypatch, FakeClient(isrcs=_releases_for_three_rows(), hearts=["512"])
    )
    record_session()
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    (playlist,) = client.playlists.values()
    assert playlist.members == ["512"]
    assert resumed["data"]["progress"]["outbound"]["reasons"] == []


def test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope(
    installed, monkeypatch, tmp_path
):
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound",
        crate=(1, 3),
        locations=_three_tagged(installed, tmp_path),
    )
    use_client(monkeypatch, FakeClient(isrcs={isrc_for("3"): ["503"]}))
    record_session()
    _run, job_id = approve_and_queue(export_verb(exported), "export.playlist.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    outbound = resumed["data"]["progress"]["outbound"]
    assert outbound["unmatched"] == ["1"] and outbound["reasons"] == []
    # R-850: ``reasons`` omits it, and the answer's list still names it.
    (listed,) = outbound["unmatched_tracks"]
    assert listed["identity"] == "1" and listed["reason"] == export_cli.NO_MATCH


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


#: The removals the adapter may name on the client, each in the one member it
#: may name it in: R-836's by position, U123's playlist delete, and U143's root
#: playlist delete and legacy folder removal. Anything else with a removal
#: shape is a new write.
ADMITTED_REMOVALS = {
    "remove_tracks": "remove_by_indices",
    "remove_playlist": "delete",
    "remove_root_playlist": "delete",
    "remove_legacy_folder": "remove_folders_playlists",
}


def test_the_adapter_names_each_remove_on_the_client_inside_its_one_member():
    """The protocol declares two removals; a third named here would be a new write.

    Narrowed on R-836 from "no removal at all" to exactly one client call,
    ``remove_by_indices``, named only inside ``remove_tracks``, and on U123 to
    that and ``delete``, named only inside ``remove_playlist``. A removal shape
    anywhere else in the file, or a different one in either member, fails here.
    """
    shapes = ("remove", "delete", "unheart", "unlike", "clear")
    named: set[tuple[str, str]] = set()
    defined: list[str] = []
    for function in ast.walk(_tree()):
        if not isinstance(function, ast.FunctionDef):
            continue
        if any(shape in function.name.lower() for shape in shapes):
            defined.append(function.name)
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Attribute) and any(s in node.attr.lower() for s in shapes):
            named.add((_enclosing(node), node.attr))
    assert sorted(defined) == sorted(ADMITTED_REMOVALS), defined
    assert named == set(ADMITTED_REMOVALS.items()), sorted(named)


def _enclosing(target: ast.AST) -> str:
    """The name of the innermost function that holds ``target``, or ``""``."""
    found = ""
    for function in ast.walk(_tree()):
        if isinstance(function, ast.FunctionDef):
            for node in ast.walk(function):
                if node is target or (
                    isinstance(node, ast.Attribute)
                    and isinstance(target, ast.Attribute)
                    and (node.lineno, node.col_offset, node.attr)
                    == (target.lineno, target.col_offset, target.attr)
                ):
                    found = function.name
    return found


def test_the_client_library_still_offers_the_private_call_a_create_relies_on():
    """``_make_private`` passes over a client with no such call rather than
    orphan the playlist, so a rename upstream would turn R-834 off with a green
    suite. This is the guard that turns it red instead."""
    import tidalapi.playlist

    assert callable(getattr(tidalapi.playlist.UserPlaylist, "set_playlist_private", None))
    assert "set_playlist_private" in ADAPTER_SOURCE.read_text(encoding="utf-8")


def test_the_adapter_satisfies_the_protocol_it_is_handed_out_as():
    declared = {
        name for name in vars(RemoteAccount) if not name.startswith("_")
    }
    assert declared == outbound_fakes.PROTOCOL_METHODS
    for name in declared:
        assert callable(getattr(tidal_account.TidalAccount, name, None)), name


# ── R-572: the file's album tag tells releases spelled alike apart ─────────


class Album:
    def __init__(self, name: str) -> None:
        self.name = name


def on_album(track: Track, name: str) -> Track:
    """The track as the client hands it out, sitting on the release ``name``."""
    track.album = Album(name)
    return track


def single_and_album_cut() -> FakeClient:
    return releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
        on_album(Track("202", "Sun Path", None, ("Nova Reef",)), "Tidal Lines"),
    )


def test_releases_spelled_alike_resolve_to_the_one_the_files_album_names():
    found = adapter(single_and_album_cut())
    chosen = found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album=" tidal LINES "
    )
    assert chosen == "202"
    assert found.unmatched_reason("7") == ""


def test_a_file_album_naming_neither_release_stays_unmatched_and_says_so():
    found = adapter(single_and_album_cut())
    chosen = found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Night Drives"
    )
    assert chosen is None
    reason = found.unmatched_reason("7")
    assert "hearts 0 of those" in reason
    assert "the file's album 'Night Drives' names 0 of them" in reason


def test_a_file_album_matching_both_releases_stays_unmatched():
    client = releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
        on_album(Track("202", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
    )
    found = adapter(client)
    chosen = found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Sun Path"
    )
    assert chosen is None
    assert "the file's album 'Sun Path' names 2 of them" in found.unmatched_reason("7")


def test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing():
    found = adapter(single_and_album_cut())
    assert match_row(found, "Sun Path") is None
    reason = found.unmatched_reason("7")
    assert "2 of them agree" in reason and "hearts 0 of those" in reason
    assert "the file carries no album tag" in reason


def test_an_unreadable_track_stops_the_album_from_choosing_the_lone_agreeing_one():
    """Rule 1 already refuses this shape; the album must not choose the same lone track."""
    client = releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Tidal Lines"),
        on_album(Track("202", "", None, ()), "Tidal Lines"),
    )
    found = adapter(client)
    chosen = found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Tidal Lines"
    )
    assert chosen is None
    reason = found.unmatched_reason("7")
    assert "1 could not be read" in reason
    assert "so none was chosen" in reason
    client.user.favorites.hearts = ["101"]
    found = adapter(client)
    assert (
        found.match_track(
            identity="7",
            isrc=CODE,
            title="Sun Path",
            artist="Nova Reef",
            album="Tidal Lines",
        )
        == "101"
    ), "the heart rule still chooses among agreeing tracks"


def test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two():
    """Out of scope by the brief: how a hearted release breaks a tie is unchanged."""
    client = single_and_album_cut()
    client.user.favorites.hearts = ["101"]
    found = adapter(client)
    assert found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Tidal Lines"
    ) == "101"
    client = single_and_album_cut()
    client.user.favorites.hearts = ["101", "202"]
    found = adapter(client)
    assert found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Tidal Lines"
    ) is None
    assert "hearts 2 of those, so none was chosen" in found.unmatched_reason("7")


def test_the_album_chooses_only_among_releases_that_agree_with_the_row():
    """The radio edit sits on the album the file names, and the row is the plain record."""
    client = releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
        on_album(Track("202", "Sun Path", None, ("Nova Reef",)), "Night Drives"),
        on_album(Track("303", "Sun Path", "Radio Edit", ("Nova Reef",)), "Tidal Lines"),
    )
    found = adapter(client)
    assert found.match_track(
        identity="7", isrc=CODE, title="Sun Path", artist="Nova Reef", album="Tidal Lines"
    ) is None


def test_a_sweep_hearts_the_release_the_files_album_tag_names(
    installed, monkeypatch, tmp_path
):
    """Driven end to end: the album comes off the file in the same read as the ISRC."""
    placed = _three_tagged(installed, tmp_path)
    two = Path(installed.library.root) / "Music" / "2.flac"
    assert tags.write_tags(two, {"album": "Track 2 (Deluxe)"}) is True
    exported = outbound_fakes.write_export(
        installed.library.root / "outbound", favorites=(1, 2, 3), locations=placed
    )
    shapes = _releases_for_three_rows()
    single, cut = shapes[isrc_for("2")]
    on_album(single, "Track 2")
    on_album(cut, "Track 2 (Deluxe)")
    client = use_client(monkeypatch, FakeClient(isrcs=shapes))
    record_session()
    _run, job_id = approve_and_queue(favorites_verb(exported), "sync.favorites.confirm")

    code, resumed = _resume(job_id)

    assert code == int(ExitCode.OK), resumed
    assert client.user.favorites.added == ["511", "512", "503"]
    assert resumed["data"]["progress"]["outbound"]["unmatched"] == []


# ── R-1032: a listening copy takes one of several agreeing releases ────────


def any_release(found: tidal_account.TidalAccount, album: str = "", title: str = "Sun Path"):
    return found.match_track(
        identity="7",
        isrc=CODE,
        title=title,
        artist="Nova Reef",
        album=album,
        any_agreeing=True,
    )


def test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order():
    for listed in (("202", "101"), ("101", "202")):
        found = adapter(releases(*_alike(*listed, "Sun Path", "Nova Reef")))
        assert any_release(found) == "101", listed
        assert found.unmatched_reason("7") == ""
    found = adapter(releases(*_alike("100", "99", "Sun Path", "Nova Reef")))
    assert any_release(found) == "99", "numeric order, not the order of the characters"


def test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads():
    found = adapter(releases(*_alike("202", "101", "Sun Path", "Nova Reef")))
    assert match_row(found, "Sun Path") is None
    assert service.AGREEING_RELEASES in found.unmatched_reason("7")


def test_a_file_album_naming_none_of_the_tied_releases_still_takes_one():
    found = adapter(single_and_album_cut())
    assert any_release(found, album="Night Drives") == "101"


def test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two():
    client = releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
        on_album(Track("303", "Sun Path", None, ("Nova Reef",)), "Tidal Lines"),
        on_album(Track("202", "Sun Path", None, ("Nova Reef",)), "Tidal Lines"),
    )
    assert any_release(adapter(client), album="Tidal Lines") == "202"


def test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one():
    client = releases(*_alike("101", "202", "Sun Path", "Nova Reef"), *_alike("303", "404", "Sun Path", "Nova Reef"))
    client.user.favorites.hearts = ["404", "202"]
    assert any_release(adapter(client)) == "202"


def test_a_lone_heart_and_a_lone_album_choose_as_they_always_did():
    client = single_and_album_cut()
    client.user.favorites.hearts = ["202"]
    assert any_release(adapter(client)) == "202"
    assert any_release(adapter(single_and_album_cut()), album="Tidal Lines") == "202"


def test_a_release_that_does_not_agree_is_never_taken():
    client = releases(
        Track("101", "Sun Path", "Radio Edit", ("Nova Reef",)),
        Track("303", "Sun Path", None, ("Nova Reef",)),
        Track("202", "Sun Path", None, ("Nova Reef",)),
    )
    assert any_release(adapter(client)) == "202"
    client = releases(
        Track("101", "Sun Path", "Radio Edit", ("Nova Reef",)),
        Track("202", "Sun Path", "Extended Mix", ("Nova Reef",)),
    )
    found = adapter(client)
    assert any_release(found) is None
    assert "none of them agrees" in found.unmatched_reason("7")


def test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing():
    client = releases(
        *_alike("101", "202", "Sun Path", "Nova Reef"), Track("303", "", None, ())
    )
    found = adapter(client)
    assert any_release(found) is None
    reason = found.unmatched_reason("7")
    assert "1 could not be read" in reason and service.AGREEING_RELEASES in reason


def test_a_row_with_no_title_to_judge_agreement_by_still_refuses_with_any_agreeing():
    found = adapter(releases(*_alike("101", "202", "Sun Path", "Nova Reef")))
    assert any_release(found, title="") is None
    assert "no artist and title" in found.unmatched_reason("7")


def test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name():
    """An empty tag is not a name: it must not pick out the release the provider left unnamed."""
    client = releases(
        on_album(Track("101", "Sun Path", None, ("Nova Reef",)), "Sun Path"),
        on_album(Track("202", "Sun Path", None, ("Nova Reef",)), ""),
    )
    assert any_release(adapter(client)) == "101"


def test_the_files_album_narrows_a_tie_under_the_products_own_fold():
    """Case and spacing on the tag do not stop it naming the album cut over the lower single."""
    assert any_release(adapter(single_and_album_cut()), album=" tidal LINES ") == "202"
