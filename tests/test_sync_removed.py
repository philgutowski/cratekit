"""U287: ``crate sync removed`` reads each downloaded playlist again and answers every removed track.

A pass is swept and landed on the native landing suite's disposable database,
a fake catalogue lists each playlist after tracks were taken off, and the verb
is driven over both. D1 applies.
"""

from __future__ import annotations

import dataclasses
import functools
import hashlib
import re
import shutil
import socket
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import config, jobs, rb_writer, session, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import missing_cli, native, set_playlist
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import playlists, removed, removed_cli, twins
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
from tests.test_intake_land_account_playlists_native import (
    RUN,
    _land,
    _landed,
    _owned,
    _stage,
)
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query, _two_acts
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

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


# The pass and the account


def isrc_of(title: str) -> str:
    return f"USPRB26{sum(map(ord, title)):05d}"


def swept(
    cfg: config.Config,
    listed: dict[str, tuple[str, tuple[str, ...]]],
    *,
    run_id: str = RUN,
    codes: bool = False,
) -> None:
    """One job per playlist, ``id -> (name, titles)``, queued and run; ``codes`` adds ISRCs."""
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
        # ONE HEART THE PASS NEVER ASKED FOR, so the hearts read whole and keep
        # nothing unless a test hearts its own track.
        self.fake = FakeCatalogue(hearts=[track("Elsewhere", track_id="tid-heart")])
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
    """The plan as the verb shows it, a gate answered abort, which writes nothing (U288)."""
    code, out = drive(VERB)
    if code == int(ExitCode.DECISION_REQUIRED):
        detail = out["cause"]["detail"]
        assert detail["gate"] == removed_cli.CONFIRM_GATE and detail["explicit"] is True
        decided, envelope = drive(
            ["run", "decide", out["run_id"], removed_cli.CONFIRM_GATE, "abort", "--actor", "a-person"]
        )
        assert decided == int(ExitCode.OK), envelope
        code, out = drive(["--run", out["run_id"], *VERB])
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


# The scenarios the brief names


def test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before(
    five_landed, monkeypatch
):
    cfg = five_landed
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
    # Both new tracks are off Sunset Warmup, which lists New5 under another id.
    # Deep Cuts holds New1 by id, New2 by ISRC under another id and title, and
    # New3 under another id with the same artist and title, a relinked track
    # rather than a removal.
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
    five_landed, monkeypatch
):
    cfg = five_landed
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
    # A playlist not read whole says nothing about its tracks, so none of
    # Deep Cuts' is a removal.
    assert "New3" not in answers
    assert out["data"]["totals"][removed.OFFERED] == 0
    assert out["data"]["totals"]["partial"] is True
    (warned,) = [one for one in out["warnings"] if one["code"] == removed_cli.PARTIAL]
    assert DEEP in warned["message"]
    (stopped,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert stopped["state"] == shape


def test_a_track_hearted_on_the_account_is_kept_by_the_hearts(five_landed, monkeypatch):
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])
    account.fake.hearts.append(track("New1"))

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [removed.HEARTS_NAME]
    assert answers["New2"]["action"] == removed.OFFERED


@pytest.mark.parametrize("shape", ["unreadable", "short", "empty"])
def test_hearts_not_read_whole_offer_nothing(
    native_library, silence, monkeypatch, offline, shape
):
    cfg, _root = native_library
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])
    if shape == "unreadable":

        def refused():
            raise RuntimeError("the provider is down")

        account.fake.favourite_tracks = refused
    elif shape == "short":

        def short():
            # THE REAL CATALOGUE'S SHAPE: it raises the shortfall with the rows
            # served when the account declares more (R-504). No heart served
            # stays partial; served hearts and a count above them read whole
            # (U320, tests/test_sync_removed_gone.py).
            raise catalogue.HeartsShortfall((), 5)

        account.fake.favourite_tracks = short
    else:
        account.fake.hearts = []

    out = _run()

    assert out["data"]["totals"][removed.OFFERED] == 0
    assert out["data"]["totals"]["partial"] is True
    (stopped,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert stopped["account"] == removed.HEARTS and stopped["state"] == shape


def test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered(
    five_landed, monkeypatch
):
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [], declared=0, counted=0)

    answers = _by_title(_run())

    assert answers["New1"]["action"] == removed.OFFERED
    assert answers["New2"]["action"] == removed.OFFERED
    assert {answers[name]["why"] for name in ("Held1", "Held2", "Held3")} == {removed.HELD_BEFORE}


def test_a_downloaded_playlist_gone_from_the_account_is_named_and_offers_nothing(
    five_landed, monkeypatch
):
    Account(monkeypatch)

    out = _run()

    assert _by_title(out) == {}
    (gone,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert gone["state"] == removed.GONE and gone["account"] == "pl-a"
    assert [one["code"] for one in out["warnings"]] == [removed_cli.GONE]
    assert out["data"]["totals"]["playlists gone"] == 1


def test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New3",))})
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])
    # Deep Cuts still opens by id and holds New1, though the account's list
    # of playlists stopped before it.
    account.fake.playlists["pl-b"] = FakePagedPlaylist([track("New3"), track("New1")], declared=2)

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New2"]["action"] == removed.OFFERED
    assert out["data"]["totals"]["playlists gone"] == 0


def test_a_removed_track_whose_row_is_gone_or_claimed_twice_is_left(five_landed, monkeypatch):
    cfg = five_landed
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


def test_a_match_on_a_file_the_pass_did_not_file_is_kept(five_landed, monkeypatch):
    cfg = five_landed
    landed = _row(cfg, "New1")
    ((folder,),) = _query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", landed)
    # The landed row and file are gone, and a hand copy of the track sits
    # elsewhere under its own row.
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


def test_a_job_no_landing_names_is_not_read_as_downloaded(five_landed, monkeypatch):
    cfg = five_landed
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


def test_a_playlist_a_later_pass_swept_and_never_landed_still_keeps_its_tracks(
    five_landed, monkeypatch
):
    """The cursor's file holds a finished job only after the next sweep."""
    cfg = five_landed
    swept(cfg, {"pl-c": (DEEP, ("New1",))}, run_id=OTHER_RUN)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    account.lists("pl-c", DEEP, [track("New1")])

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]
    assert "pl-c" in account.fake.playlists_asked_for


def test_a_gone_downloaded_playlist_holds_what_its_pass_recorded(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New1", "New3"))})
    account = Account(monkeypatch)
    # Deep Cuts is neither listed nor openable, so gone, still holding the
    # New1 and New3 its pass recorded.
    account.lists("pl-a", SUNSET, [track("Held1")])

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]
    assert answers["New2"]["action"] == removed.OFFERED
    assert "New3" not in answers
    assert out["data"]["totals"]["partial"] is False


def test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    from cratekit.modules.outbound import pairs

    _five(cfg, silence)
    pairs.PairStore(config.load()).mark("acc-paired", "901", name="A Pair")
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])

    out = _run()

    assert out["data"]["totals"][removed.OFFERED] == 0
    assert out["data"]["totals"]["partial"] is True
    (stopped,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
    assert stopped["account"] == "acc-paired" and stopped["state"] == removed.UNREADABLE


def test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    _five(cfg, silence, also={"pl-b": (DEEP, ("New3",))}, codes=True)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    # A row with no title is set aside by the reader (U213), and its ISRC is New1's.
    account.lists(
        "pl-b", DEEP, [track("New3"), Listed("tid-relinked", "", code=isrc_of("New1"))]
    )

    out = _run()

    answers = _by_title(out)
    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [DEEP]


def test_a_file_another_pass_filed_is_not_this_pass_s_file(
    native_library, silence, monkeypatch, offline
):
    """Each report's pass is asked of its own landing's folder, never of any pass's."""
    cfg, _root = native_library
    other = missing_cli.synced_name(OTHER_RUN)
    swept(cfg, {"pl-a": (SUNSET, ("New1", "New2"))})
    swept(cfg, {"pl-b": (DEEP, ("New1", "New6"))}, run_id=OTHER_RUN)
    for title in ("New1", "New2"):
        _stage(cfg, silence, title)
    _landed(cfg)
    _stage(cfg, silence, "New6")
    code, acted, _ = _two_acts(_land(other))
    assert code == int(ExitCode.OK), acted
    account = Account(monkeypatch)
    # New1 is off Deep Cuts, whose pass found its file in the first pass's folder.
    account.lists("pl-a", SUNSET, [track("New1"), track("New2")])
    account.lists("pl-b", DEEP, [track("New6")])

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.NOT_THIS_PASS


def test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing(
    native_library, silence, monkeypatch, offline
):
    cfg, _root = native_library
    from datetime import date

    from cratekit.core import active_taxonomy

    _five(cfg, silence)
    declared = active_taxonomy.load(cfg)
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        folder = handle.create_playlist_folder("Genres")
        genre = handle.create_playlist("Deep House", parent=folder)
        handle.add_to_playlist(genre, _row(cfg, "New1"))
        handle.session.commit()
        root_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    native = tree_registry.read(cfg).with_record(
        tree_registry.TreeRecord(
            tree_id=declared.tree.id,
            mode=tree_registry.Mode.DATABASE,
            cutover_on=date(2026, 10, 1),
            root_id=root_id,
            source=next(iter(tree_registry.DerivationSource)),
        )
    )
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])

    bridged = _by_title(_run())
    monkeypatch.setattr(tree_registry, "read", lambda _cfg: native)
    filed = _by_title(_run())

    # On the bridge the genre playlist cannot be told from a person's: kept.
    assert bridged["New1"]["why"] == removed.IN_YOURS
    assert bridged["New1"]["kept_by"] == ["Deep House"]
    assert filed["New1"]["action"] == removed.OFFERED


def _damage_reports(job_id: str) -> None:
    """Take one committed report of the job off disk, as a pre U57 store lacks one."""
    import os

    for base in {os.environ.get(key) for key in ("XDG_STATE_HOME", "XDG_DATA_HOME", "HOME")}:
        if not base:
            continue
        for path in Path(base).rglob("*"):
            if path.is_file() and job_id in str(path) and "intake-artifacts" in str(path):
                path.unlink()
                return
    raise AssertionError(f"no report file of job {job_id} was found")


def _job_of(account: str) -> str:
    with jobs.open_store() as store:
        (job,) = [one for one in jobs.list_jobs(store) if playlists.playlist_of(one) == account]
    return job.job_id


@pytest.mark.parametrize("listed", [True, False])
def test_a_damaged_job_of_another_playlist_never_refuses_the_verb(
    native_library, silence, monkeypatch, offline, listed
):
    """The recorded contents are read only of a playlist that reads gone."""
    cfg, _root = native_library
    _five(cfg, silence)
    swept(cfg, {"pl-z": ("Other", ("Zed1", "Zed2"))}, run_id=OTHER_RUN)
    _damage_reports(_job_of("pl-z"))
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    if listed:
        account.lists("pl-z", "Other", [track("Zed1"), track("Zed2")])

    out = _run()

    answers = _by_title(out)
    if listed:
        assert answers["New1"]["action"] == removed.OFFERED
    else:
        # Gone, and its record cannot be read: not read whole, so nothing offered.
        assert answers["New1"]["why"] == removed.PARTIAL_READ
        (stopped,) = [item for item in out["data"]["items"] if item["action"] == "playlist"]
        assert stopped["account"] == "pl-z" and stopped["state"] == removed.UNREADABLE


def test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded(
    five_landed, monkeypatch
):
    cfg = five_landed
    swept(cfg, {"pl-c": (DEEP, ("New1",))}, run_id=OTHER_RUN)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1")])

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New2"]["action"] == removed.OFFERED


def test_a_playlist_still_titled_with_the_old_prefix_is_synced(five_landed, monkeypatch):
    """The prefix holds a playlist as taken until the strip records it (U242)."""
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("New2")])
    account.lists("pl-old", playlists.SWEPT_PREFIX + "Old Mix", [track("New1")])

    answers = _by_title(_run())

    assert answers["New1"]["why"] == removed.ON_ANOTHER
    assert answers["New1"]["kept_by"] == [playlists.SWEPT_PREFIX + "Old Mix"]


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


def test_nothing_is_written_and_the_digest_holds_until_an_answer_moves(five_landed, monkeypatch):
    cfg = five_landed
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


def test_the_verb_declares_the_collection_its_explicit_gate_and_the_cloud_decision():
    """U288: the write surface is destructive and R34's confirm gate explicit."""
    entry = registry.entry("sync.removed")
    assert entry.writes == frozenset({"db_tree", "db_metadata"})
    assert entry.destructive
    (confirm,) = [spec for spec in entry.gates if spec.name == removed_cli.CONFIRM_GATE]
    assert confirm.options == ("apply", "abort")
    assert confirm.explicit and confirm.digest_source == "plan"
    assert {"rekordbox.closed", "library.mounted"} <= set(entry.doctor_checks)


# The rules, held one at a time


def _listing(**kwargs) -> removed.Listing:
    return removed.Listing(account="pl", name="P", state=removed.READ, **kwargs)


def test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds():
    wanted = match.Wanted(artist="Probe", title="Song", isrc="usprb2600001", ref="tid-1")
    assert _listing(refs=frozenset({"tid-1"})).holds(wanted)
    assert _listing(isrcs=frozenset({"USPRB2600001"})).holds(wanted)
    assert _listing(recordings=frozenset({removed.recording(wanted)})).holds(wanted)
    assert not _listing(refs=frozenset({"tid-2"})).holds(wanted)
    gone = removed.Listing(account="pl", name="P", state=removed.GONE, refs=frozenset({"tid-1"}))
    assert gone.holds(wanted)
    for state in (removed.UNREADABLE, removed.SHORT, removed.EMPTY):
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


# U288: the gate, and the offered rows taken out of the collection

#: The tables a track's rows sit in beside the content row, one each here so
#: the apply has every kind A185 measured to delete.
_BESIDE = ("djmdCue", "contentCue", "contentFile", "djmdSongHistory", "djmdMixerParam")


def _every_table(cfg: config.Config) -> dict[str, list[tuple]]:
    """Every table of the disposable database, every row, sorted: the bytes a removal may move."""
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        names = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            )
        ]
        return {
            name: sorted((tuple(row) for row in conn.execute(f'SELECT * FROM "{name}"')), key=repr)
            for name in names
        }
    finally:
        conn.close()


def _columns_of(cfg: config.Config, table: str) -> list[str]:
    return [row[1] for row in _query(cfg, f'PRAGMA table_info("{table}")')]


def _give_state(cfg: config.Config, content_id: str, tag: str) -> None:
    """One row naming ``content_id`` in each table beside the content row, and a history list."""
    for table in _BESIDE:
        _sql(cfg, f'INSERT INTO "{table}" (ID, ContentID) VALUES (?, ?)', f"{tag}-{table}", content_id)


def _without(tables: dict[str, list[tuple]], cfg: config.Config, gone: set[str]) -> dict:
    """``tables`` with every row naming one of ``gone`` taken out, as rekordbox takes it out."""
    kept: dict[str, list[tuple]] = {}
    for name, rows in tables.items():
        columns = _columns_of(cfg, name)
        if name == "djmdContent":
            at = columns.index("ID")
        elif name in rb_writer.DELETABLE_TABLES:
            at = columns.index("ContentID")
        else:
            kept[name] = rows
            continue
        kept[name] = [row for row in rows if str(row[at]) not in gone]
    return kept


def _closed_up(
    tables: dict[str, list[tuple]],
    cfg: config.Config,
    before: dict[str, list[tuple]],
    gone: set[str],
    stamp: tuple[int, str],
) -> dict:
    """``tables`` with each removed membership's playlist renumbered 1 to N (R-1830, A197).

    Each row that moves is stamped with ``stamp``, the update count and the time,
    as rekordbox stamps it (U955, A202); a row that keeps its place is untouched.
    """
    columns = _columns_of(cfg, "djmdSongPlaylist")
    pid, cid, number = (columns.index(name) for name in ("PlaylistID", "ContentID", "TrackNo"))
    usn, at = columns.index("rb_local_usn"), columns.index("updated_at")
    by_playlist: dict[str, list[tuple]] = {}
    for row in before["djmdSongPlaylist"]:
        by_playlist.setdefault(str(row[pid]), []).append(row)
    for rows in by_playlist.values():
        assert sorted(int(row[number]) for row in rows) == list(range(1, len(rows) + 1)), rows
    touched = {key for key, rows in by_playlist.items() if any(str(row[cid]) in gone for row in rows)}
    kept = []
    for key, rows in by_playlist.items():
        survivors = sorted((row for row in rows if str(row[cid]) not in gone), key=lambda row: int(row[number]))
        for place, row in enumerate(survivors, start=1):
            if key in touched and int(row[number]) != place:
                moved = list(row)
                moved[number], moved[usn], moved[at] = place, stamp[0], stamp[1]
                row = tuple(moved)
            kept.append(row)
    return {**tables, "djmdSongPlaylist": sorted(kept, key=repr)}


def _counter(cfg: config.Config) -> int:
    ((value,),) = _query(cfg, "SELECT int_1 FROM agentRegistry WHERE registry_id = 'localUpdateCount'")
    return int(value)


#: rekordbox's own text form of a time, which a renumbered row's ``updated_at`` takes (U955).
_STAMP_FORM = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \+00:00")


def _stamp_read(cfg: config.Config, before: dict[str, list[tuple]]) -> tuple[int, str]:
    """The stamp a removal put on the rows it renumbered, read from SQL: one count, one time."""
    columns = _columns_of(cfg, "djmdSongPlaylist")
    key, number = columns.index("ID"), columns.index("TrackNo")
    was = {row[key]: row[number] for row in before["djmdSongPlaylist"]}
    stamps = {
        (row[columns.index("rb_local_usn")], row[columns.index("updated_at")])
        for row in _every_table(cfg)["djmdSongPlaylist"]
        if row[key] in was and row[number] != was[row[key]]
    }
    assert len(stamps) == 1, stamps
    ((counter, at),) = stamps
    assert counter == _counter(cfg), (counter, _counter(cfg))
    assert _STAMP_FORM.fullmatch(at), at
    return int(counter), str(at)


def _not_before(at: str, moment: datetime) -> bool:
    """Whether the stamp ``at`` is no earlier than ``moment`` cut to rekordbox's milliseconds."""
    stamped = rb_writer.stamp_moment(at)
    assert stamped is not None, at
    return stamped >= moment.replace(microsecond=moment.microsecond // 1000 * 1000)


def _apply() -> tuple[int, dict, dict]:
    """R34's two acts against the confirm gate, answered apply, then the acting drive."""
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == removed_cli.CONFIRM_GATE and detail["explicit"] is True
    decided, envelope = drive(
        ["run", "decide", refused["run_id"], removed_cli.CONFIRM_GATE, "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", refused["run_id"], *VERB])
    return code, acted, refused


def _one_offered(cfg: config.Config, silence: Path, monkeypatch) -> Account:
    """New1 offered, Held1 kept as held before the pass, on Sunset Warmup."""
    _five(cfg, silence)
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("New2"), track("Held2"), track("Held3")])
    return account


@pytest.fixture
def one_offered(native_library, silence, monkeypatch, offline) -> config.Config:
    """The configuration once :func:`_one_offered` ran, with no network."""
    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)
    return cfg


@pytest.fixture
def five_landed(native_library, silence, offline) -> config.Config:
    """The configuration once :func:`_five` ran, with no network."""
    cfg, _root = native_library
    _five(cfg, silence)
    return cfg


def test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them(one_offered):
    cfg = one_offered
    offered, held = _row(cfg, "New1"), _row(cfg, "Held1")
    _give_state(cfg, offered, "gone")
    _give_state(cfg, held, "kept")
    playlists = _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")
    before = _every_table(cfg)
    counted = _counter(cfg)
    planned = datetime.now(timezone.utc)
    music = Path(_query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", offered)[0][0])
    size = music.stat().st_size

    code, acted, refused = _apply()
    finished = datetime.now(timezone.utc)

    assert code == int(ExitCode.OK), acted
    # The screen the person approved names the offered row and its file.
    shown = refused["cause"]["detail"]["shown"]
    assert any("New1" in line and str(music) in line for line in shown["offered"]), shown
    assert acted["data"]["totals"]["removed"] == 1
    # New1 sat second of five on two pass playlists and fourth of five on
    # INBOX / Analyze, so three, three and one members are renumbered.
    assert shown["memberships renumbered"] == 7, shown
    assert acted["data"]["totals"]["memberships renumbered"] == 7
    (applied,) = [one for one in acted["warnings"] if one["code"] == removed_cli.APPLIED]
    assert "7 playlist membership(s) after them renumbered" in applied["message"], applied
    after = _every_table(cfg)
    # One count and one time on every renumbered row: the count the commit
    # left, and the removal's time in rekordbox's form (U955).
    stamp = _stamp_read(cfg, before)
    assert _not_before(stamp[1], planned), stamp
    assert rb_writer.stamp_moment(stamp[1]) <= finished, stamp
    expected = _closed_up(_without(before, cfg, {offered}), cfg, before, {offered}, stamp)
    # Read from SQL: the offered row and every row naming it are gone, later
    # members are numbered down and stamped with no other column moved
    # (R-1830, U955), and only the update count moved besides.
    registry_at = _columns_of(cfg, "agentRegistry").index("registry_id")
    for name in sorted(set(expected) | set(after)):
        if name == "agentRegistry":
            moved = [row for row in after[name] if row[registry_at] == "localUpdateCount"]
            assert [row for row in after[name] if row not in expected[name]] == moved, name
            continue
        assert after[name] == expected[name], name
    assert _counter(cfg) > counted
    for table in _BESIDE:
        assert _query(cfg, f'SELECT COUNT(*) FROM "{table}" WHERE ContentID = ?', offered) == [(0,)]
        assert _query(cfg, f'SELECT COUNT(*) FROM "{table}" WHERE ContentID = ?', held) == [(1,)]
    assert _query(cfg, "SELECT COUNT(*) FROM djmdSongPlaylist WHERE ContentID = ?", offered) == [(0,)]
    # The playlist rows stay as rekordbox leaves them, and the file is
    # untouched, the Trash being delete review's.
    assert _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID") == playlists
    assert music.exists() and music.stat().st_size == size


def test_the_session_record_names_every_row_removed_and_restore_list_reads_it(one_offered):
    cfg = one_offered
    offered = _row(cfg, "New1")

    code, acted, _ = _apply()

    assert code == int(ExitCode.OK), acted
    (record,) = [one for one in session.records(cfg) if one.workflow == removed.WORKFLOW]
    recorded = record.detail[rb_writer.RECORDED_REMOVALS_KEY]
    assert [row["content_id"] for row in recorded["rows"]] == [offered]
    assert recorded["rows"][0]["columns"]["ID"] == offered
    assert recorded["rows"][0]["removed_from"] == [SUNSET]
    assert recorded["sequence"] == _counter(cfg)
    assert recorded["database_identity"]
    assert record.snapshot_path
    code, listed = drive(["restore", "list"])
    assert code == int(ExitCode.OK), listed
    (item,) = [one for one in listed["data"]["items"] if one["session_id"] == record.session_id]
    assert item["change"] == [
        {"tree": removed.COLLECTION, "created": 0, "updated": 0, "removed": 1}
    ]
    assert [one["content_id"] for one in item["removed"]] == [offered]
    assert item["removed"][0]["title"].endswith("New1")


def test_abort_writes_nothing(one_offered):
    cfg = one_offered
    database = Path(cfg.library.db_path)
    before = hashlib.sha256(database.read_bytes()).hexdigest()

    out = _run()

    assert out["outcome"] == "no_op"
    assert out["data"]["totals"][removed.OFFERED] == 1
    assert hashlib.sha256(database.read_bytes()).hexdigest() == before
    assert not [one for one in session.records(cfg) if one.workflow == removed.WORKFLOW]


def test_a_plan_that_moved_before_the_write_refuses_with_nothing_written(one_offered, monkeypatch):
    """The engine takes the plan again on the write handle, and a moved digest refuses."""
    cfg = one_offered
    real = removed_cli.written
    seen: dict = {}

    def moved_first(cfg_, plan, **kwargs):
        # A person puts the offered track in their own playlist between the
        # gate and the write, so it is kept and the plan moved.
        _hand_made(cfg_, "Mine", "New1")
        seen["tables"] = _every_table(cfg_)
        return real(cfg_, plan, **kwargs)

    monkeypatch.setattr(removed_cli, "written", moved_first)

    code, acted, _ = _apply()

    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _every_table(cfg) == seen["tables"]


def test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed(
    five_landed, monkeypatch
):
    """The landing's own vox My Tag would make the removal refuse, so the track keeps."""
    cfg = five_landed
    account = Account(monkeypatch)
    account.lists("pl-a", SUNSET, [track("Held1"), track("Held2"), track("Held3")])
    tagged, clean = _row(cfg, "New1"), _row(cfg, "New2")
    _sql(cfg, 'INSERT INTO "djmdSongMyTag" (ID, ContentID) VALUES (?, ?)', "mt-1", tagged)

    code, acted, refused = _apply()

    assert code == int(ExitCode.OK), acted
    answers = _by_title(acted)
    assert answers["New1"]["action"] == removed.KEPT
    assert answers["New1"]["why"] == removed.UNMEASURED
    assert answers["New1"]["kept_by"] == ["djmdSongMyTag"]
    assert answers["New2"]["action"] == removed.OFFERED
    assert acted["data"]["totals"]["removed"] == 1
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent WHERE ID = ?", tagged) == [(1,)]
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent WHERE ID = ?", clean) == [(0,)]
    assert not any("New1" in line for line in refused["cause"]["detail"]["shown"]["offered"])


@pytest.mark.parametrize(
    "made, inserted",
    [
        # A table the binding maps and neither sitting measured.
        (None, 'INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES (\'x-1\', ?)'),
        # A table the binding does not even map, asked by its column alone.
        (
            'CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)',
            'INSERT INTO "someFutureTable" (ID, ContentID) VALUES (\'x-1\', ?)',
        ),
        # A row naming it by TargetID, as an image row does.
        (None, 'INSERT INTO "imageFile" (ID, TargetID) VALUES (\'x-1\', ?)'),
    ],
)
def test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written(
    native_library, silence, monkeypatch, offline, made, inserted
):
    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)
    offered = _row(cfg, "New1")
    if made:
        _sql(cfg, made)
    _sql(cfg, inserted, offered)
    before = _every_table(cfg)
    handle = _handle(cfg)
    try:
        assert rb_writer.CollectionRemoval.held(handle, [offered])[offered]
        with pytest.raises(rb_writer.RekordboxUnavailable, match="never measured"):
            rb_writer.CollectionRemoval.prepare(handle, [offered])
        with pytest.raises(rb_writer.RekordboxUnavailable, match="never measured"):
            rb_writer.remove_from_collection(handle, offered)
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_a_uuid_map_row_is_left_as_rekordbox_leaves_it(one_offered):
    cfg = one_offered
    offered = _row(cfg, "New1")
    _sql(cfg, 'INSERT INTO "uuidIDMap" (ID, TableName, TargetUUID, CurrentID) VALUES (?, ?, ?, ?)', "u-1", "djmdContent", "uu", offered)
    handle = _handle(cfg)
    try:
        assert rb_writer.CollectionRemoval.held(handle, [offered]) == {}
    finally:
        rb_writer.close_db(handle)


def test_delete_review_after_the_apply_offers_the_removed_file_and_none_other(
    native_library, silence, monkeypatch, offline, tmp_path
):
    """The removed row is gone outright, and delete review still offers its file (R-1037)."""
    from cratekit.deletion import watermark

    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)
    offered = _row(cfg, "New1")
    music = Path(_query(cfg, "SELECT FolderPath FROM djmdContent WHERE ID = ?", offered)[0][0])
    # NO DELETE REVIEW HAS EVER RUN ON THIS LIBRARY: the removal gives the pass
    # its first position, below its own commit.
    assert watermark.WatermarkStore(cfg).read() is None
    code, acted, _ = _apply()
    mark = watermark.WatermarkStore(cfg).read()
    assert mark is not None and mark.sequence < _counter(cfg)
    assert code == int(ExitCode.OK), acted
    # Deletion is a feature module and the slim profile hides it.
    config.save(dataclasses.replace(cfg, profile=config.ProfileConfig(name="full")))
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True)
    monkeypatch.setattr("cratekit.deletion.trash.Path.home", lambda: home)
    monkeypatch.setenv("XDG_DATA_HOME", str(home / "share"))

    code, refused = drive(["delete", "review"])

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["baselined"] is False, shown
    assert shown["offered"] == 1, shown
    decided, envelope = drive(
        ["run", "decide", refused["run_id"], "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, out = drive(["--run", refused["run_id"], "delete", "review"])
    assert code == int(ExitCode.OK), out
    assert not music.exists()
    trashed = [one for one in tmp_path.rglob(music.name) if one != music]
    assert len(trashed) == 1 and "Trash" in str(trashed[0]), trashed
    # Every other landed file is where it was.
    for title in ("New2", "Held1", "Held2", "Held3"):
        (path,) = _query(
            cfg, "SELECT FolderPath FROM djmdContent WHERE Title LIKE ?", f"%{title}"
        )[0]
        assert Path(path).exists(), title


@functools.cache
def _package_calls() -> tuple[tuple[str, str, tuple[str | None, ...]], ...]:
    """Each call in the package but ``_vendor``, as (module, callee, keywords), once per worker."""
    import ast

    root = Path(rb_writer.__file__).resolve().parents[1]
    found = []
    for path in sorted(root.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call):
                name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(
                    node.func, "id", ""
                )
                module = path.relative_to(root).as_posix()
                found.append((module, name, tuple(keyword.arg for keyword in node.keywords)))
    return tuple(found)


def test_only_the_collection_removal_asks_a_commit_to_admit_a_delete():
    """A source guard, read as syntax: who may pass ``deletions``, or a ``**`` mapping to a judge."""
    import re

    judges = {"commit_guarded", "assert_session_whitelisted", "guard_violations"}
    root = Path(rb_writer.__file__).resolve().parents[1]
    askers = [
        f"{module}::{name}"
        for module, name, keywords in _package_calls()
        for arg in keywords
        if arg == "deletions" or (arg is None and name in judges)
    ]
    assert sorted(set(askers)) == [
        "core/rb_writer.py::assert_session_whitelisted",
        "core/rb_writer.py::commit_guarded",
        "core/rb_writer.py::guard_violations",
    ], askers
    callers = sorted(
        str(path.relative_to(root))
        for path in root.rglob("*.py")
        if re.search(r"\bCollectionRemoval\.prepare\(", path.read_text(encoding="utf-8"))
        and path.name != "rb_writer.py"
    )
    assert callers == ["sync/removed.py"], callers


def test_the_record_key_and_its_columns_are_spelled_the_same_everywhere_they_are_read():
    from cratekit.deletion import library as deletion_library
    from cratekit.session import restore_cli

    assert deletion_library.RECORDED_REMOVALS_KEY == rb_writer.RECORDED_REMOVALS_KEY
    assert restore_cli.RECORDED_REMOVALS_KEY == rb_writer.RECORDED_REMOVALS_KEY
    assert deletion_library.RECORDED_COLUMNS == rb_writer.RECORDED_COLUMNS


def _handle(cfg: config.Config):
    return rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)


def test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit(
    one_offered
):
    """Every commit but the removal's refuses a binding delete; a raw session delete is a residual."""
    cfg = one_offered
    offered = _row(cfg, "New1")
    before = _every_table(cfg)
    handle = _handle(cfg)
    try:
        handle.delete(handle.get_content(ID=offered))
        with pytest.raises(rb_writer.RekordboxUnavailable, match="additive-only"):
            rb_writer.commit_guarded(handle)
        # Naming the membership table alone does not admit the content row.
        handle.delete(handle.get_content(ID=offered))
        with pytest.raises(rb_writer.RekordboxUnavailable, match="additive-only"):
            rb_writer.commit_guarded(handle, deletions=(rb_writer.MEMBERSHIP_TABLE,))
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit(one_offered):
    cfg = one_offered
    offered, held = _row(cfg, "New1"), _row(cfg, "Held1")
    _give_state(cfg, offered, "gone")
    before = _every_table(cfg)
    handle = _handle(cfg)
    try:
        reading = rb_writer.database_reading(handle)
        rb_writer.remove_from_collection(handle, offered)
        handle.get_content(ID=held).Title = "Moved"
        with pytest.raises(rb_writer.RekordboxUnavailable, match="did not plan"):
            rb_writer.assert_collection_removal_confined(handle, reading, removed=[offered])
        # A removal of a row nobody deleted is refused as a planned write never made.
        reading = rb_writer.database_reading(handle)
        with pytest.raises(rb_writer.RekordboxUnavailable, match="did not plan"):
            rb_writer.assert_collection_removal_confined(handle, reading, removed=[offered])
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_the_removal_refuses_a_row_that_is_not_live(one_offered):
    cfg = one_offered
    offered = _row(cfg, "New1")
    _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", offered)
    handle = _handle(cfg)
    try:
        for content_id in (offered, "no-such-row"):
            with pytest.raises(rb_writer.RekordboxUnavailable, match="no live row"):
                rb_writer.remove_from_collection(handle, content_id)
        assert not handle.session.deleted
    finally:
        rb_writer.close_db(handle)


def test_the_removal_writes_no_beat_grid_and_no_tempo(one_offered):
    """No tempo, BPM or grid column of any surviving row moves; the removal only deletes."""
    cfg = one_offered
    columns = ("ID", "BPM", "KeyID", "AnalysisDataPath", "FileSize")
    before = _query(cfg, f"SELECT {', '.join(columns)} FROM djmdContent ORDER BY ID")
    offered = _row(cfg, "New1")

    code, acted, _ = _apply()

    assert code == int(ExitCode.OK), acted
    after = _query(cfg, f"SELECT {', '.join(columns)} FROM djmdContent ORDER BY ID")
    assert after == [row for row in before if str(row[0]) != offered]


def test_a_recorded_removal_is_read_only_for_its_own_database_and_a_row_still_absent():
    from cratekit.deletion import library as deletion_library

    def detail(identity, sequence, *ids):
        return {
            rb_writer.RECORDED_REMOVALS_KEY: {
                "database_identity": identity,
                "sequence": sequence,
                "rows": [
                    {"columns": {"ID": one, "FolderPath": f"/m/{one}.flac", "FileSize": 9, "Title": one}}
                    for one in ids
                ],
            }
        }

    rows = deletion_library.recorded_removals(
        [
            detail("db-1", 40, "a", "b"),
            detail("db-2", 41, "c"),
            detail("db-1", True, "d"),
            detail("db-1", None, "e"),
            detail("db-1", 45, "a"),
            {"other": {}},
        ],
        database_identity="db-1",
        present=["b"],
    )
    assert [(row.content_id, row.sequence, row.recorded, row.size) for row in rows] == [
        ("a", 45, "/m/a.flac", 9)
    ]


# U288: the write's guards, a restored row and the deletion pass's position


def test_the_acknowledgment_is_read_before_the_gate_is_asked(one_offered, monkeypatch):
    def missing(_cfg, **_kwargs):
        raise session.refuse(
            "backup-acknowledgment-missing",
            "no acknowledgment, as a test says",
            origin=("tests",),
        )

    monkeypatch.setattr(removed_cli.session, "assert_backup_acknowledged", missing)

    code, out = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), out
    assert out["cause"]["reason"] == "backup-acknowledgment-missing", out


def test_rekordbox_running_at_the_write_refuses_before_any_session_opens(one_offered, monkeypatch):
    cfg = one_offered
    before = _every_table(cfg)
    real = removed_cli.written

    def running(cfg_, plan, **kwargs):
        monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
        return real(cfg_, plan, **kwargs)

    monkeypatch.setattr(removed_cli, "written", running)

    code, acted, _ = _apply()

    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] == "rekordbox-running", acted
    assert _every_table(cfg) == before
    # Refused at the open, before the gates: no session was begun for it.
    assert not [one for one in session.records(cfg) if one.workflow == removed.WORKFLOW]


def test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity(one_offered):
    cfg = one_offered
    offered, held = _row(cfg, "New1"), _row(cfg, "Held1")
    _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", held)
    handle = _handle(cfg)
    try:
        for content_id in (held, "no-such-row"):
            with pytest.raises(rb_writer.RekordboxUnavailable, match="no live row"):
                rb_writer.CollectionRemoval.prepare(handle, [offered, content_id])
    finally:
        rb_writer.close_db(handle)
    _sql(cfg, "UPDATE djmdProperty SET DBID = ''")
    handle = _handle(cfg)
    try:
        with pytest.raises(rb_writer.RekordboxUnavailable, match="no identity"):
            rb_writer.CollectionRemoval.prepare(handle, [offered])
    finally:
        rb_writer.close_db(handle)


def test_commit_proves_the_removal_confined_before_it_commits(one_offered):
    cfg = one_offered
    offered, held = _row(cfg, "New1"), _row(cfg, "Held1")
    before = _every_table(cfg)
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [offered])
        handle.get_content(ID=held).Title = "Moved"
        with pytest.raises(rb_writer.RekordboxUnavailable, match="did not plan"):
            removal.commit()
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_a_read_back_that_disagrees_refuses_as_unverified(one_offered, monkeypatch):
    monkeypatch.setattr(rb_writer.CollectionRemoval, "read_back", lambda self: ["a row moved"])

    code, acted, _ = _apply()

    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] == "session-committed-unverified", acted
    assert "a row moved" in acted["cause"]["message"]


def test_a_commit_that_lands_and_then_raises_still_records_every_row(one_offered, monkeypatch):
    cfg = one_offered
    offered = _row(cfg, "New1")
    real = rb_writer.commit_guarded

    def landed_then_raised(db, **kwargs):
        real(db, **kwargs)
        raise RuntimeError("the binding's legacy playlist file could not be saved")

    monkeypatch.setattr(rb_writer, "commit_guarded", landed_then_raised)

    code, acted, _ = _apply()

    assert code != int(ExitCode.OK)
    (record,) = [one for one in session.records(cfg) if one.workflow == removed.WORKFLOW]
    rows = record.detail[rb_writer.RECORDED_REMOVALS_KEY]["rows"]
    assert [row["content_id"] for row in rows] == [offered]
    assert record.detail[rb_writer.RECORDED_REMOVALS_KEY]["sequence"] == _counter(cfg)


def test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review(
    native_library, silence, monkeypatch, offline, tmp_path
):
    """A restore puts the row back live, and the live row answers for its file."""
    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)
    offered = _row(cfg, "New1")
    (content,) = [row for row in _every_table(cfg)["djmdContent"] if str(row[_columns_of(cfg, "djmdContent").index("ID")]) == offered]
    code, acted, _ = _apply()
    assert code == int(ExitCode.OK), acted
    columns = _columns_of(cfg, "djmdContent")
    _sql(
        cfg,
        f'INSERT INTO djmdContent ({", ".join(columns)}) VALUES ({", ".join("?" for _ in columns)})',
        *content,
    )
    config.save(dataclasses.replace(cfg, profile=config.ProfileConfig(name="full")))
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)

    code, refused = drive(["delete", "review"])

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["shown"]["offered"] == 0, refused
    # The live row means the recorded removal is none, so the pass never
    # judges it, not merely refused by the reference proof.
    from cratekit.deletion import run as deletion_run

    handle = _handle(cfg)
    try:
        found = deletion_run.plan(cfg, handle, actor="cli")
    finally:
        rb_writer.close_db(handle)
    assert offered not in {one.row.content_id for one in found.candidates}


def test_a_track_added_after_a_removal_goes_past_the_highest_position(one_offered):
    """The binding's count plus one would land on a live row's position."""
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    _sql(cfg, "DELETE FROM djmdSongPlaylist WHERE PlaylistID = ? AND ContentID = ?", mine, _row(cfg, "New1"))
    handle = _handle(cfg)
    try:
        playlist = handle.get_playlist(ID=mine)
        assert rb_writer.add_memberships(handle, playlist, [_row(cfg, "Held3")])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    numbers = sorted(row[0] for row in _query(cfg, "SELECT TrackNo FROM djmdSongPlaylist WHERE PlaylistID = ?", mine))
    assert numbers == [1, 3, 4], numbers


def test_two_appends_after_a_removal_each_take_the_next_position(one_offered):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    _sql(cfg, "DELETE FROM djmdSongPlaylist WHERE PlaylistID = ? AND ContentID = ?", mine, _row(cfg, "New1"))
    handle = _handle(cfg)
    try:
        playlist = handle.get_playlist(ID=mine)
        assert rb_writer.add_memberships(handle, playlist, [_row(cfg, "Held3"), _row(cfg, "New2")])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    numbers = sorted(row[0] for row in _query(cfg, "SELECT TrackNo FROM djmdSongPlaylist WHERE PlaylistID = ?", mine))
    assert numbers == [1, 3, 4, 5], numbers


def test_a_refused_removal_gives_the_deletion_pass_no_position(
    native_library, silence, monkeypatch, offline
):
    """The first position is written only once the removal's commit lands."""
    from cratekit.deletion import watermark

    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)

    def refused(self, **_kwargs):
        raise rb_writer.RekordboxUnavailable(
            rb_writer.refuse("whitelist-violation", "refused, as a test says", origin=("tests",)).cause
        )

    monkeypatch.setattr(rb_writer.CollectionRemoval, "commit", refused)

    code, acted, _ = _apply()

    assert code != int(ExitCode.OK)
    assert watermark.WatermarkStore(cfg).read() is None


def test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked(
    native_library, silence, monkeypatch, offline
):
    """With a position held, a marked row the pass could not read stops nothing."""
    from cratekit.deletion import library as deletion_library
    from cratekit.deletion import watermark

    cfg, _root = native_library
    _one_offered(cfg, silence, monkeypatch)
    handle = _handle(cfg)
    try:
        identity = deletion_library.database_identity(handle)
    finally:
        rb_writer.close_db(handle)
    watermark.WatermarkStore(cfg).baseline(database_identity=identity, sequence=3, actor="cli")
    walked: list = []
    real = deletion_library.read_collection
    monkeypatch.setattr(deletion_library, "read_collection", lambda rows: walked.append(1) or real(rows))

    code, acted, _ = _apply()

    assert code == int(ExitCode.OK), acted
    assert watermark.WatermarkStore(cfg).read().sequence == 3
    assert not walked


# The renumbering behind a removal (R-1830)


def _numbers(cfg: config.Config, playlist: str) -> list[tuple[str, int]]:
    """A playlist's members as (title, TrackNo), in TrackNo order."""
    return [
        (str(title), int(number))
        for title, number in _query(
            cfg,
            "SELECT c.Title, sp.TrackNo FROM djmdSongPlaylist sp JOIN djmdContent c ON c.ID = sp.ContentID "
            "WHERE sp.PlaylistID = ? ORDER BY sp.TrackNo",
            playlist,
        )
    ]


def _titles(pairs: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """``pairs`` with each title cut to its last word, the name the fixture gave it."""
    return [(title.split()[-1].split("-")[-1], number) for title, number in pairs]


def _remove(cfg: config.Config, *titles: str) -> rb_writer.CollectionRemoval:
    """The writer's own removal of ``titles``' rows, prepared, committed and read back clean."""
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, title) for title in titles])
        removal.commit()
        assert removal.read_back() == []
        return removal
    finally:
        rb_writer.close_db(handle)


def test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved(
    one_offered
):
    """A197's shape on a disposable library, compared byte for byte table by table."""
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    offered = _row(cfg, "New1")
    before = _every_table(cfg)
    first, third = (
        _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? AND TrackNo = ?", mine, place)[0]
        for place in (1, 3)
    )
    planned = datetime.now(timezone.utc)

    removal = _remove(cfg, "New1")
    finished = datetime.now(timezone.utc)

    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2)]
    # The renumbered row moves three columns, as rekordbox moved them (A202):
    # TrackNo, rb_local_usn to the count the commit left, and updated_at to the
    # removal's time. Every other column stays, and the row before it moves
    # in none.
    columns = _columns_of(cfg, "djmdSongPlaylist")
    (now,) = _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE ID = ?", third[0])
    moving = {columns.index(name) for name in ("TrackNo", "rb_local_usn", "updated_at")}
    assert now[columns.index("TrackNo")] == 2
    assert now[columns.index("rb_local_usn")] == _counter(cfg) == removal.stamp.counter
    assert now[columns.index("rb_local_usn")] != third[columns.index("rb_local_usn")]
    assert now[columns.index("updated_at")] == removal.stamp.at
    assert _STAMP_FORM.fullmatch(removal.stamp.at) and _not_before(removal.stamp.at, planned)
    assert rb_writer.stamp_moment(removal.stamp.at) <= finished
    assert [v for i, v in enumerate(now) if i not in moving] == [v for i, v in enumerate(third) if i not in moving]
    assert _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE ID = ?", first[0]) == [first]
    after = _every_table(cfg)
    stamp = (removal.stamp.counter, removal.stamp.at)
    assert _stamp_read(cfg, before) == stamp
    expected = _closed_up(_without(before, cfg, {offered}), cfg, before, {offered}, stamp)
    registry_at = _columns_of(cfg, "agentRegistry").index("registry_id")
    for name in sorted(set(expected) | set(after)):
        if name == "agentRegistry":
            moved = [row for row in after[name] if row[registry_at] == "localUpdateCount"]
            assert [row for row in after[name] if row not in expected[name]] == moved, name
            continue
        assert after[name] == expected[name], name
    assert removal.renumbered[str(third[0])] == (mine, 3, 2)
    detail: dict = {}
    removal.write_into(detail, sequence=1, about={})
    renumbered = detail[rb_writer.RECORDED_REMOVALS_KEY]["renumbered"]
    assert {"membership_id": str(third[0]), "playlist_id": mine, "from": 3, "to": 2} in renumbered
    assert len(renumbered) == len(removal.renumbered) == 8


def test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists(one_offered):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2", "New2", "Held3")
    other = _hand_made(cfg, "Other", "New1", "Held3", "Held1")
    untouched = _hand_made(cfg, "Untouched", "Held2", "Held3")
    kept = _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY ID", untouched)

    _remove(cfg, "New1", "New2")

    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2), ("Held3", 3)]
    assert _titles(_numbers(cfg, other)) == [("Held3", 1), ("Held1", 2)]
    assert _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY ID", untouched) == kept


def test_the_last_member_removed_renumbers_nothing_in_its_playlist(one_offered):
    cfg = one_offered
    last = _hand_made(cfg, "Last", "Held1", "Held2", "New1")
    kept = _query(
        cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? AND TrackNo < 3 ORDER BY ID", last
    )

    removal = _remove(cfg, "New1")

    assert _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY ID", last) == kept
    assert all(playlist != last for playlist, _was, _now in removal.renumbered.values())


def test_an_append_after_a_renumbering_takes_the_next_position(one_offered):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    _remove(cfg, "New1")
    handle = _handle(cfg)
    try:
        playlist = handle.get_playlist(ID=mine)
        assert rb_writer.add_memberships(handle, playlist, [_row(cfg, "Held3"), _row(cfg, "New2")])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2), ("Held3", 3), ("New2", 4)]


def test_a_history_list_holding_others_keeps_its_numbers(one_offered):
    """Unmeasured, so left as it is: only the removed track's own history row goes."""
    cfg = one_offered
    offered, held = _row(cfg, "New1"), _row(cfg, "Held1")
    for key, content_id, number in (("h-1", held, 1), ("h-2", offered, 2), ("h-3", held, 3)):
        _sql(
            cfg,
            "INSERT INTO djmdSongHistory (ID, HistoryID, ContentID, TrackNo) VALUES (?, 'h', ?, ?)",
            key,
            content_id,
            number,
        )

    _remove(cfg, "New1")

    assert _query(cfg, "SELECT ID, TrackNo FROM djmdSongHistory WHERE HistoryID = 'h' ORDER BY ID") == [
        ("h-1", 1),
        ("h-3", 3),
    ]


def test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written(
    one_offered, monkeypatch
):
    cfg = one_offered
    _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    untouched = _hand_made(cfg, "Untouched", "Held2", "Held3")
    before = _every_table(cfg)
    real = rb_writer.renumber_memberships

    def and_another(db, moved, **kwargs):
        real(db, moved, **kwargs)
        from sqlalchemy import text

        db.session.execute(
            text("UPDATE djmdSongPlaylist SET TrackNo = 7 WHERE PlaylistID = :p AND TrackNo = 2"),
            {"p": untouched},
        )

    monkeypatch.setattr(rb_writer, "renumber_memberships", and_another)
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, "New1")])
        with pytest.raises(rb_writer.RekordboxUnavailable, match="did not plan"):
            removal.commit()
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written(
    one_offered
):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, "New1")])
        from sqlalchemy import text

        handle.session.execute(
            text("UPDATE djmdSongPlaylist SET TrackNo = 9 WHERE PlaylistID = :p AND TrackNo = 3"),
            {"p": mine},
        )
        handle.session.commit()
        before = _every_table(cfg)
        with pytest.raises(rb_writer.RekordboxUnavailable, match="no longer holds the place 3"):
            removal.commit()
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


def test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale(
    one_offered, monkeypatch
):
    """The count is in the digest: one more member after the offered row moves the plan."""
    cfg = one_offered
    real = removed_cli.written
    seen: dict = {}

    def one_more_after(cfg_, plan, **kwargs):
        seen["approved"] = plan.renumbered
        (analyze,) = _query(cfg_, "SELECT ID FROM djmdPlaylist WHERE Name = 'Analyze'")
        _sql(
            cfg_,
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, rb_local_deleted) "
            "VALUES ('late-1', ?, ?, 6, 0)",
            analyze[0],
            _row(cfg_, "Held1"),
        )
        seen["tables"] = _every_table(cfg_)
        return real(cfg_, plan, **kwargs)

    monkeypatch.setattr(removed_cli, "written", one_more_after)

    code, acted, refused = _apply()

    assert seen["approved"] == 7
    assert refused["cause"]["detail"]["shown"]["memberships renumbered"] == 7
    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _every_table(cfg) == seen["tables"]


def test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members(one_offered):
    """Marked New1 and live Held2 share 2, so counting the marked row doubles a number."""
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2", "Held3")
    _sql(
        cfg,
        "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ? AND ContentID = ?",
        mine,
        _row(cfg, "New1"),
    )
    for title, number in (("Held2", 2), ("Held3", 3)):
        _sql(
            cfg,
            "UPDATE djmdSongPlaylist SET TrackNo = ? WHERE PlaylistID = ? AND ContentID = ?",
            number,
            mine,
            _row(cfg, title),
        )
    kept = _query(
        cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0 ORDER BY ID", mine
    )

    code, acted, refused = _apply()

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["memberships renumbered"] == 7
    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2), ("Held3", 3)]
    assert _query(cfg, "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY ID", mine) == kept


def test_renumbering_writes_the_three_columns_and_a_held_row_reads_them(one_offered):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "Held2")
    handle = _handle(cfg)
    try:
        held = [song for song in handle.get_playlist_songs(PlaylistID=mine) if int(song.TrackNo) == 2]
        (song,) = held
        stamp = rb_writer.RenumberingStamp(4242, "2031-01-02 03:04:05.006 +00:00")
        rb_writer.renumber_memberships(handle, {str(song.ID): (mine, 2, 1)}, stamp=stamp)
        # The mapped object the session held reads what SQL now holds.
        assert int(song.TrackNo) == 1
        assert int(song.rb_local_usn) == 4242
        from sqlalchemy import text

        assert handle.session.execute(
            text("SELECT updated_at FROM djmdSongPlaylist WHERE ID = :key"), {"key": str(song.ID)}
        ).scalar() == stamp.at
        handle.rollback()
    finally:
        rb_writer.close_db(handle)
    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2)]


def test_only_the_collection_removal_renumbers_memberships():
    """The one TrackNo write the whitelist does not see has one caller."""
    callers = [module for module, name, _keywords in _package_calls() if name == "renumber_memberships"]
    assert callers == ["core/rb_writer.py"], callers


def test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written(one_offered):
    """Other readers take a NULL marker as live, so the renumbering refuses it."""
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2", "Held3")
    _sql(
        cfg,
        "UPDATE djmdSongPlaylist SET rb_local_deleted = NULL WHERE PlaylistID = ? AND ContentID = ?",
        mine,
        _row(cfg, "Held2"),
    )
    before = _every_table(cfg)
    handle = _handle(cfg)
    try:
        with pytest.raises(CratekitError) as refused:
            rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, "New1")])
        assert refused.value.cause.reason == "soft-delete-marker-unreadable"
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


# The stamp on each renumbered row, as rekordbox's own removal writes it (U955, A202)


def _left_unstamped(cfg: config.Config, monkeypatch, statement: str, *params) -> dict:
    """The renumbering made, then ``statement`` run on the same handle; returns the tables before."""
    real = rb_writer.renumber_memberships

    def and_then(db, moved, **kwargs):
        real(db, moved, **kwargs)
        from sqlalchemy import text

        db.session.execute(text(statement), _named(params))

    monkeypatch.setattr(rb_writer, "renumber_memberships", and_then)
    return _every_table(cfg)


def _named(params: tuple) -> dict:
    return {f"p{at}": value for at, value in enumerate(params)}


def _refused_with_nothing_written(cfg: config.Config, before: dict, title: str, match: str) -> None:
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, title)])
        with pytest.raises(rb_writer.RekordboxUnavailable, match=match):
            removal.commit()
    finally:
        rb_writer.close_db(handle)
    assert _every_table(cfg) == before


@pytest.mark.parametrize(
    ("statement", "match"),
    [
        # rb_local_usn put back as it was: unmoved, refused.
        (
            "UPDATE djmdSongPlaylist SET rb_local_usn = :p1 WHERE ID = :p0",
            "was to be stamped rb_local_usn",
        ),
        # updated_at put back as it was: unmoved, refused.
        (
            "UPDATE djmdSongPlaylist SET updated_at = :p2 WHERE ID = :p0",
            "was to be stamped updated_at",
        ),
        # A fourth column moving on the renumbered row, refused.
        (
            "UPDATE djmdSongPlaylist SET UUID = 'moved-' || UUID WHERE ID = :p0",
            "other than TrackNo, rb_local_usn and updated_at",
        ),
    ],
    ids=["usn-unmoved", "time-unmoved", "uuid-moved"],
)
def test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back(
    one_offered, monkeypatch, statement, match
):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    (third,) = _query(
        cfg, "SELECT ID, rb_local_usn, updated_at FROM djmdSongPlaylist WHERE PlaylistID = ? AND TrackNo = 3", mine
    )
    before = _left_unstamped(cfg, monkeypatch, statement, *third)
    _refused_with_nothing_written(cfg, before, "New1", match)


def test_an_unplanned_membership_whose_count_moves_is_refused(one_offered, monkeypatch):
    """The members before a removed one, and every other playlist, move in no column."""
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    (first,) = _query(cfg, "SELECT ID FROM djmdSongPlaylist WHERE PlaylistID = ? AND TrackNo = 1", mine)
    before = _left_unstamped(
        cfg, monkeypatch, "UPDATE djmdSongPlaylist SET rb_local_usn = 1 + coalesce(rb_local_usn, 0) WHERE ID = :p0", first[0]
    )
    _refused_with_nothing_written(cfg, before, "New1", f"{first[0]}' changed")


def test_two_removed_before_a_survivor_move_it_two_places_stamped_once(one_offered):
    cfg = one_offered
    mine = _hand_made(cfg, "Mine", "Held1", "New1", "New2", "Held2")
    (last,) = _query(cfg, "SELECT ID FROM djmdSongPlaylist WHERE PlaylistID = ? AND TrackNo = 4", mine)

    removal = _remove(cfg, "New1", "New2")

    assert _titles(_numbers(cfg, mine)) == [("Held1", 1), ("Held2", 2)]
    assert removal.renumbered[str(last[0])] == (mine, 4, 2)
    # One UPDATE, one stamp: the count the whole removal's commit left.
    assert _query(cfg, "SELECT rb_local_usn, updated_at FROM djmdSongPlaylist WHERE ID = ?", last[0]) == [
        (_counter(cfg), removal.stamp.at)
    ]


def test_the_stamp_is_the_count_the_binding_s_commit_leaves(one_offered):
    """Read off the binding's buffer before the commit, and equal to the count after it."""
    cfg = one_offered
    _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    counted = _counter(cfg)
    removal = _remove(cfg, "New1")
    assert removal.stamp.counter == _counter(cfg) > counted
    # One step per row the binding deleted, and none for the renumbering's SQL.
    assert removal.stamp.counter - counted == sum(removal.deleted.values())


def test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit(one_offered, monkeypatch):
    """The confinement reads the count the commit would leave again, and refuses a different one."""
    cfg = one_offered
    _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    real = rb_writer.renumber_memberships

    def and_one_more(db, moved, **kwargs):
        real(db, moved, **kwargs)
        db.registry.on_move([])

    monkeypatch.setattr(rb_writer, "renumber_memberships", and_one_more)
    before = _every_table(cfg)
    _refused_with_nothing_written(cfg, before, "New1", "the commit would leave localUpdateCount")


def test_a_read_back_refuses_a_count_the_stamp_does_not_name(one_offered, monkeypatch):
    cfg = one_offered
    _hand_made(cfg, "Mine", "Held1", "New1", "Held2")
    handle = _handle(cfg)
    try:
        removal = rb_writer.CollectionRemoval.prepare(handle, [_row(cfg, "New1")])
        removal.commit()
        assert removal.read_back() == []
        removal.stamp = dataclasses.replace(removal.stamp, counter=removal.stamp.counter - 1)
        assert any("after the commit" in line for line in removal.read_back())
    finally:
        rb_writer.close_db(handle)
