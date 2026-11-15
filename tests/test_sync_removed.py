"""U287: ``crate sync removed`` reads each downloaded playlist again and answers every removed track.

Driven against the disposable database the native landing suite builds. A
pass is swept and landed as U128 lands one, then the account is a fake
catalogue listing each playlist as it stands after Phillip took tracks off it,
and ``crate sync removed`` is driven over both. Nothing is written by the verb,
so no gate is answered anywhere in this file.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import hashlib
import shutil
import socket
import sqlite3
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, rb_writer, session, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import native, set_playlist
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import playlists, removed, removed_cli, twins
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
from tests.test_intake_land_account_playlists_native import (
    RUN,
    _landed,
    _owned,
    _stage,
)
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

VERB = ["sync", "removed"]
SUNSET = "Sunset Warmup"
DEEP = "Deep Cuts"
#: A second run, so a pass of it is a pass no landing names.
OTHER_RUN = "2026-10-04T101500Z-ef56"


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    match.reset_cache()
    yield
    intake_cli.reset_cache()
    match.reset_cache()


@pytest.fixture
def offline(monkeypatch):
    """No provider can be reached: any socket the verb opens fails the test."""

    def refused(*_args, **_kwargs):
        raise AssertionError("sync removed opened a network connection")

    monkeypatch.setattr(socket.socket, "connect", refused)
    monkeypatch.setattr(socket, "create_connection", refused)


# ---------------------------------------------------------------------------
# The pass and the account
# ---------------------------------------------------------------------------


def isrc_of(title: str) -> str:
    return f"USPRB26{sum(map(ord, title)):05d}"


def swept(
    cfg: config.Config,
    listed: dict[str, tuple[str, tuple[str, ...]]],
    *,
    run_id: str = RUN,
    codes: bool = False,
) -> None:
    """One job per playlist, ``id -> (account name, titles)``, queued as a sweep does and run.

    ``tests/test_intake_land_account_playlists_native.py``'s helper, with an
    ISRC on each track when ``codes`` asks, so the identity rule's second test
    is reachable from a recorded pass.
    """
    queued = []
    with jobs.open_store() as store:
        for playlist_id, (name, titles) in listed.items():
            queued.append(
                intake_cli.queue_playlist(
                    store,
                    cfg,
                    handler_key="intake.playlist",
                    reference=playlist_id,
                    tracks={
                        f"tid-{title}": {
                            "artist": "Probe",
                            "title": title,
                            "origin": match.TIDAL,
                            "ref": f"tid-{title}",
                            **({"isrc": isrc_of(title)} if codes else {}),
                        }
                        for title in titles
                    },
                    run_id=run_id,
                    source_id=playlists.SOURCE_ID,
                    name=name,
                )
            )
    for job in queued:
        code, resumed = drive(cli_jobs.argv_for(job))
        assert code == int(ExitCode.OK), resumed
        assert resumed["data"]["state"] == str(jobs.JobState.SUCCEEDED), resumed


class Listed:
    """A provider track in the shape the playlist reader reads."""

    def __init__(self, track_id: str, name: str, *, artist: str = "Probe", code: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = code


def track(title: str, *, track_id: str | None = None, code: str = "") -> Listed:
    return Listed(track_id or f"tid-{title}", title, code=code)


class Account:
    """The account as the fake catalogue lists it now: each playlist and its tracks."""

    def __init__(self, monkeypatch) -> None:
        self.fake = FakeCatalogue()
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.fake))

    def lists(
        self,
        playlist_id: str,
        name: str,
        tracks: list[Listed],
        *,
        declared: int | None = -1,
        counted: int | None = -1,
    ) -> None:
        """The playlist listed with ``tracks``; ``declared`` and ``counted`` default to their length."""
        whole = len(tracks)
        self.fake.playlists[playlist_id] = FakePagedPlaylist(
            tracks, declared=whole if declared == -1 else declared
        )
        self.fake.account.append(
            AccountPlaylist(
                playlist_id=playlist_id, name=name, tracks=whole if counted == -1 else counted
            )
        )

    def names_only(self, playlist_id: str, name: str) -> None:
        """Listed by the account, and the playlist itself cannot be resolved."""
        self.fake.account.append(AccountPlaylist(playlist_id=playlist_id, name=name, tracks=3))


def _run() -> dict:
    code, out = drive(VERB)
    assert code == int(ExitCode.OK), out
    return out


def _by_title(out: dict) -> dict[str, dict]:
    return {
        item["title"]: item
        for item in out["data"]["items"]
        if item["action"] in (removed.OFFERED, removed.KEPT, removed.LEFT)
    }


def _sql(cfg: config.Config, statement: str, *params) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(statement, params)
    conn.close()


def _row(cfg: config.Config, title: str) -> str:
    (row,) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE Title LIKE ? AND rb_local_deleted = 0", f"%{title}"
    )
    return str(row[0])


def _hand_made(cfg: config.Config, name: str, *titles: str) -> str:
    """A playlist a person made at the playlist root, holding ``titles``' rows."""
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        made = handle.create_playlist(name)
        for title in titles:
            handle.add_to_playlist(made, _row(cfg, title))
        handle.session.commit()
        return str(made.ID)
    finally:
        rb_writer.close_db(handle)


def _five(cfg: config.Config, silence: Path, *, also: dict | None = None, codes: bool = False) -> None:
    """Three owned and two new on Sunset Warmup, swept and landed; ``also`` adds playlists."""
    _owned(cfg, silence, ("Held1", "Held2", "Held3"))
    swept(
        cfg,
        {"pl-a": (SUNSET, ("Held1", "New1", "Held2", "New2", "Held3")), **(also or {})},
        codes=codes,
    )
    titles = {"New1", "New2"} | {
        title for _name, listed in (also or {}).values() for title in listed if title.startswith("New")
    }
    for title in sorted(titles):
        _stage(cfg, silence, title)
    _landed(cfg)


# ---------------------------------------------------------------------------
# The scenarios the brief names
# ---------------------------------------------------------------------------


def test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("New2"), track("Held2"), track("Held3")])

    out = _run()

    answers = _by_title(out)
    assert set(answers) == {"New1", "Held1"}
    assert answers["New1"]["action"] == removed.OFFERED
    assert answers["New1"]["removed_from"] == [SUNSET]
    assert answers["New1"]["content_id"] == _row(cfg, "New1")
    assert answers["New1"]["file"].endswith("New1.flac")
    assert answers["Held1"]["action"] == removed.KEPT
    assert answers["Held1"]["why"] == removed.HELD_BEFORE
    assert out["data"]["totals"][removed.OFFERED] == 1
    assert out["data"]["totals"]["partial"] is False
    assert not out["warnings"]


def test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(
        cfg,
        silence,
        also={"pl-b": (DEEP, ("New3", "New4", "New5"))},
        codes=True,
    )
    account = Account(monkeypatch)
    # Both new tracks are off Sunset Warmup, which now lists New5 under another
    # id. Deep Cuts holds New1 by its id, New2 by its ISRC under another id and
    # title, and New3 under another id with the same artist and title, which is
    # a relinked track still on its playlist rather than a removal.
    account.lists(
        "pl-a",
        SUNSET,
        [track("Held1"), track("Held2"), track("Held3"), track("New5", track_id="tid-moved")],
    )
    account.lists(
        "pl-b",
        DEEP,
        [
            track("New1"),
            track("Renamed", track_id="tid-relinked", code=isrc_of("New2")),
            track("New3", track_id="tid-another-id"),
        ],
    )

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]
    assert answers["New2"]["why"] == removed.ON_ANOTHER
    assert answers["New2"]["kept_by"] == [DEEP]
    assert "New3" not in answers
    assert answers["New5"]["why"] == removed.ON_ANOTHER
    assert answers["New5"]["kept_by"] == [SUNSET]
    assert answers["New4"]["action"] == removed.OFFERED
    assert answers["New4"]["removed_from"] == [DEEP]


def test_a_track_in_a_playlist_of_yours_is_kept_and_its_own_filing_keeps_nothing(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    _hand_made(cfg, "Warmup Picks", "New1")
    _hand_made(cfg, "All Favorites", "New2")
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.IN_YOURS
    assert answers["New1"]["kept_by"] == ["Warmup Picks"]
    assert answers["New2"]["why"] == removed.IN_YOURS
    assert answers["New2"]["kept_by"] == ["All Favorites"]


def test_the_landings_own_playlists_keep_nothing(native_library, silence, monkeypatch, offline):
    cfg, root_id = native_library
    _five(cfg, silence)
    held = {
        str(name)
        for (name,) in _query(
            cfg,
            "SELECT p.Name FROM djmdSongPlaylist sp JOIN djmdPlaylist p ON p.ID = sp.PlaylistID "
            "WHERE sp.ContentID = ? AND sp.rb_local_deleted = 0",
            _row(cfg, "New1"),
        )
    }
    # The INBOX playlist, INBOX / Analyze and the custom playlist twin (U149).
    assert held == {"Sunset Warmup 2026-10-03", native.ANALYZE, SUNSET}, held
    ((folder,),) = _query(
        cfg,
        "SELECT f.Name FROM djmdPlaylist p JOIN djmdPlaylist f ON f.ID = p.ParentID "
        "WHERE p.Name = ? AND p.rb_local_deleted = 0",
        SUNSET,
    )
    assert str(folder).startswith(twins.FOLDER_PREFIX)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.OFFERED, answers["New1"]


@pytest.mark.parametrize("shape", ["unreadable", "short", "empty"])
def test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist(
    native_library, silence, monkeypatch, offline, shape
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New3",))})
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    if shape == "unreadable":
        account.names_only("pl-b", DEEP)
    elif shape == "short":
        account.lists("pl-b", DEEP, [track("New3")], declared=4)
    else:
        account.lists("pl-b", DEEP, [], declared=None, counted=None)

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["action"] == removed.KEPT
    assert answers["New1"]["why"] == removed.PARTIAL_READ
    assert out["data"]["totals"][removed.OFFERED] == 0
    assert out["data"]["totals"]["partial"] is True
    (warned,) = [one for one in out["warnings"] if one["code"] == removed_cli.PARTIAL]
    assert DEEP in warned["message"]
    (stopped,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert stopped["state"] == shape


def test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [], declared=0, counted=0)

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.OFFERED
    assert answers["New2"]["action"] == removed.OFFERED
    assert {answers[name]["why"] for name in ("Held1", "Held2", "Held3")} == {removed.HELD_BEFORE}


def test_a_downloaded_playlist_gone_from_the_account_is_named_and_offers_nothing(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    Account(monkeypatch)

    out = _run()

    assert _by_title(out) == {}
    (gone,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert gone["state"] == removed.GONE and gone["account"] == "pl-a"
    assert [one["code"] for one in out["warnings"]] == [removed_cli.GONE]
    assert out["data"]["totals"]["playlists gone"] == 1


def test_a_removed_track_whose_row_is_gone_or_claimed_twice_is_left(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    gone = _row(cfg, "New1")
    _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", gone)
    twice = _row(cfg, "New2")
    ((folder,),) = _query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", twice)
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('90002', 'New2 twin', ?, 0, '2026-10-09', '2026-10-09')",
        folder,
    )
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("Held2"), track("Held3")])

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.LEFT
    assert answers["New2"]["action"] == removed.LEFT
    assert answers["New2"]["why"] == set_playlist.AMBIGUOUS_ROWS


def test_a_match_on_a_file_the_pass_did_not_file_is_kept(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    landed = _row(cfg, "New1")
    ((folder,),) = _query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", landed)
    # The landed row and file are gone, and a copy of the same track brought in
    # by hand sits elsewhere in the library under a row of its own.
    elsewhere = Path(cfg.library.root) / cfg.library.music_dir / "By Hand" / "New1.flac"
    elsewhere.parent.mkdir(parents=True)
    shutil.move(str(folder), elsewhere)
    _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", landed)
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES ('90001', 'New1', ?, 0, '2026-10-09', '2026-10-09')",
        str(elsewhere),
    )
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.KEPT, answers["New1"]
    assert answers["New1"]["why"] == removed.NOT_THIS_PASS
    assert answers["New1"]["content_id"] == "90001"


def test_a_job_no_landing_names_is_not_read_as_downloaded(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    # A later pass swept Deep Cuts and never landed.
    swept(cfg, {"pl-c": (DEEP, ("New1",))}, run_id=OTHER_RUN)
    account = Account(monkeypatch)
    account.lists(
        "pl-a", SUNSET, [track(one) for one in ("Held1", "New1", "Held2", "New2", "Held3")]
    )
    account.lists("pl-c", DEEP, [])

    out = _run()

    assert _by_title(out) == {}
    assert "pl-c" not in account.fake.playlists_asked_for


def test_one_row_taken_off_two_downloaded_playlists_is_one_offer_naming_both(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New2", "New3"))})
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New1")])
    account.lists("pl-b", DEEP, [track("New3")])

    out = _run()

    (offer,) = [item for item in out["data"]["items"] if item["title"] == "New2"]
    assert offer["action"] == removed.OFFERED
    assert offer["removed_from"] == [SUNSET, DEEP]


def test_nothing_is_written_and_the_digest_holds_until_an_answer_moves(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    database = Path(cfg.library.db_path)
    before = hashlib.sha256(database.read_bytes()).hexdigest()
    records = len(session.records(cfg))
    with jobs.open_store() as store:
        queued = len(jobs.list_jobs(store))

    first = _run()
    second = _run()

    assert hashlib.sha256(database.read_bytes()).hexdigest() == before
    assert len(session.records(cfg)) == records
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == queued
    assert first["data"]["digest"] == second["data"]["digest"]
    # Held2 taken off as well moves one answer, and the digest with it.
    account.fake.playlists["pl-a"] = FakePagedPlaylist([track("Held1")], declared=1)
    assert _run()["data"]["digest"] != first["data"]["digest"]


def test_nothing_downloaded_asks_the_account_nothing(native_library, monkeypatch, offline):
    account = Account(monkeypatch)

    code, out = drive(VERB)

    assert code == int(ExitCode.OK), out
    assert out["outcome"] == "no_op", out
    assert out["data"]["items"] == []
    assert account.fake.account_listings == 0


def test_the_verb_declares_no_write_surface_and_no_gate():
    entry = registry.entry("sync.removed")
    assert entry.writes == frozenset()
    assert entry.gates == ()
    assert not entry.destructive


# ---------------------------------------------------------------------------
# The rules, held one at a time
# ---------------------------------------------------------------------------


def _listing(**kwargs) -> removed.Listing:
    return removed.Listing(account="pl", name="P", state=removed.READ, **kwargs)


def test_a_listing_holds_a_track_by_any_of_three_tests_and_nothing_unread_holds_anything():
    wanted = match.Wanted(artist="Probe", title="Song", isrc="usprb2600001", ref="tid-1")
    assert _listing(refs=frozenset({"tid-1"})).holds(wanted)
    assert _listing(isrcs=frozenset({"USPRB2600001"})).holds(wanted)
    assert _listing(recordings=frozenset({removed.recording(wanted)})).holds(wanted)
    assert not _listing(refs=frozenset({"tid-2"})).holds(wanted)
    for state in (removed.GONE, removed.UNREADABLE, removed.SHORT, removed.EMPTY):
        unread = removed.Listing(
            account="pl", name="P", state=state, refs=frozenset({"tid-1"})
        )
        assert not unread.holds(wanted)


def test_a_path_is_under_a_folder_only_past_a_separator_and_in_one_unicode_form():
    assert removed._under("/music/2026/Batch/a.flac", ["/music/2026/Batch"])
    assert removed._under("/music/2026/Batch/a.flac", ["/music/2026/Batch/"])
    assert not removed._under("/music/2026/Batch 2/a.flac", ["/music/2026/Batch"])
    assert not removed._under("/music/2026/Batch/a.flac", [""])
    assert removed._under("/music/Café/a.flac", ["/music/Café"])


def test_a_routing_tree_on_the_bridge_names_no_playlist_of_the_pass(native_library):
    cfg, _root = native_library
    from cratekit.core import active_taxonomy

    declared = active_taxonomy.load(cfg)
    registry_now = tree_registry.read(cfg)
    assert not registry_now.is_database_native(declared.tree.id)
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        assert removed._routing_nodes(handle, declared, registry_now) == frozenset()
    finally:
        rb_writer.close_db(handle)
