"""R-1037: a landed row rekordbox's Remove from Collection deleted outright is offered.

rekordbox 7.2.19 deletes a removed track's rows outright (A178, A185), so the
soft delete marker the deletion pass partitions on never says the row went,
and before this card the pass offered only the marked rows and the rows ``crate
sync removed`` recorded (U288). A native landing now names every row it made
on its session record, and the pass reads a landed row of this database that
is neither live nor marked as a removal, numbered by the update count at the
first run that sees it absent. Everything after that is the pass's own: the
watermark, the reference set, the inode and size proof, the gate, the Trash
and the tombstone.

These land real files through the native landing on a disposable library,
take rows out the way rekordbox does (the row and every membership naming it,
deleted outright, the update count advanced), and drive ``crate delete
review`` through the dispatcher. D1 applies: nothing here names a real
volume, a real person or a real track.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import sqlite3
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, session, tombstone
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import library as deletion_library
from cratekit.deletion import run as deletion_run
from cratekit.deletion import stores, watermark
from cratekit.intake import native
from tests.cli_drive import drive
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query, _stage, _two_acts
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

GATE = "delete.review.confirm"


# ---------------------------------------------------------------------------
# The library, landed, and a removal as rekordbox makes one
# ---------------------------------------------------------------------------


def _land(cfg: config.Config, silence: Path, *titles: str, name: str = "landed batch") -> None:
    for title in titles:
        _stage(cfg, silence, f"{title}.flac")
    code, acted, _ = _two_acts(["intake", "land", "--name", name])
    assert code == int(ExitCode.OK), acted


def _row(cfg: config.Config, title: str) -> tuple[str, Path]:
    ((content_id, folder),) = _query(
        cfg,
        "SELECT ID, FolderPath FROM djmdContent WHERE Title LIKE ? AND rb_local_deleted = 0",
        f"% - {title}",
    )
    return str(content_id), Path(folder)


def _sql(cfg: config.Config, *statements: tuple[str, tuple]) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        for statement, params in statements:
            conn.execute(statement, params)
    conn.close()


def _counter(cfg: config.Config) -> int:
    ((value,),) = _query(
        cfg, "SELECT int_1 FROM agentRegistry WHERE registry_id = 'localUpdateCount'"
    )
    return int(value)


def _remove_outright(cfg: config.Config, content_id: str) -> None:
    """rekordbox's Remove from Collection: the row and its memberships, gone, the count past them."""
    _sql(
        cfg,
        ("DELETE FROM djmdSongPlaylist WHERE ContentID = ?", (content_id,)),
        ("DELETE FROM djmdContent WHERE ID = ?", (content_id,)),
        (
            "UPDATE agentRegistry SET int_1 = int_1 + 12 WHERE registry_id = 'localUpdateCount'",
            (),
        ),
    )


def _mark_removed(cfg: config.Config, content_id: str) -> None:
    """The soft delete an earlier rekordbox wrote, the row kept with its marker set."""
    _sql(
        cfg,
        (
            "UPDATE agentRegistry SET int_1 = int_1 + 1 WHERE registry_id = 'localUpdateCount'",
            (),
        ),
        (
            "UPDATE djmdContent SET rb_local_deleted = 1, rb_local_usn = "
            "(SELECT int_1 FROM agentRegistry WHERE registry_id = 'localUpdateCount') "
            "WHERE ID = ?",
            (content_id,),
        ),
    )


def _deletion_on(cfg: config.Config, monkeypatch, tmp_path: Path) -> Path:
    """The full profile, rekordbox closed, a Trash of the test's own. Returns the home."""
    config.save(dataclasses.replace(cfg, profile=config.ProfileConfig(name="full")))
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    home = tmp_path / "home"
    (home / ".Trash").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("cratekit.deletion.trash.Path.home", lambda: home)
    monkeypatch.setenv("XDG_DATA_HOME", str(home / "share"))
    return home


def _review() -> tuple[int, dict]:
    return drive(["delete", "review"])


def _shown(refused: dict) -> dict:
    return refused["cause"]["detail"]["shown"]


def _trash(refused: dict) -> dict:
    decided, envelope = drive(
        ["run", "decide", refused["run_id"], GATE, "trash", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, out = drive(["--run", refused["run_id"], "delete", "review"])
    assert code == int(ExitCode.OK), out
    return out


def _baseline(cfg: config.Config) -> None:
    """The pass's first position, taken before anything was removed (R35)."""
    code, refused = _review()
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _shown(refused)["baselined"] is True, _shown(refused)
    assert watermark.WatermarkStore(cfg).read() is not None


def _offered() -> int:
    """How many files a review offers, read off the gate it always reaches."""
    code, refused = _review()
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return int(_shown(refused)["offered"])


def _plan(cfg: config.Config) -> deletion_run.Plan:
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        return deletion_run.plan(cfg, handle, actor="cli")
    finally:
        rb_writer.close_db(handle)


def _candidates(cfg: config.Config) -> dict[str, str]:
    return {one.row.content_id: str(one.category) for one in _plan(cfg).candidates}


def _record_path(cfg: config.Config, session_id: str) -> Path:
    return session.log_path(session_id, cfg)


def _landing_record(cfg: config.Config) -> session.SessionRecord:
    landings = [
        one for one in session.records(cfg) if native.LANDED_ROWS_KEY in one.detail
    ]
    assert landings, "no landing record names a landed row"
    return landings[-1]


# ---------------------------------------------------------------------------
# The landing names what it made
# ---------------------------------------------------------------------------


def test_the_landing_record_names_every_row_it_made_as_the_database_holds_it(
    native_library, silence
):
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")

    landed = _landing_record(cfg).detail[native.LANDED_ROWS_KEY]

    ((dbid,),) = _query(cfg, "SELECT DBID FROM djmdProperty")
    assert landed["database_identity"] == str(dbid)
    assert landed["sequence"] == _counter(cfg)
    held = {
        str(values[0]): {"ID": values[0], "FolderPath": values[1], "FileSize": values[2], "Title": values[3]}
        for values in _query(cfg, "SELECT ID, FolderPath, FileSize, Title FROM djmdContent")
    }
    named = {one["content_id"]: one["columns"] for one in landed["rows"]}
    # Exactly the two rows this landing made, and none the library held before.
    assert sorted(named) == sorted(_row(cfg, title)[0] for title in ("One", "Two"))
    for content_id, recorded in named.items():
        row = held[content_id]
        assert recorded["ID"] == str(row["ID"])
        assert recorded["FolderPath"] == row["FolderPath"]
        assert recorded["FileSize"] == row["FileSize"] == Path(row["FolderPath"]).stat().st_size
        assert recorded["Title"] == row["Title"]
        assert recorded["ArtistName"] == "Probe"
    # The playlists it made, by id, which a removal in rekordbox leaves.
    assert landed["playlists"], landed
    for playlist_id in landed["playlists"]:
        assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE ID = ?", playlist_id)


def test_the_key_and_its_columns_are_spelled_the_same_where_they_are_read():
    assert deletion_library.LANDED_ROWS_KEY == native.LANDED_ROWS_KEY
    assert deletion_library.RECORDED_COLUMNS == native.LANDED_COLUMNS == rb_writer.RECORDED_COLUMNS


# ---------------------------------------------------------------------------
# A landed row removed outright is offered once, and trashed with its tombstone
# ---------------------------------------------------------------------------


def test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, music = _row(cfg, "One")
    _kept, other = _row(cfg, "Two")
    before = music.read_bytes()
    _remove_outright(cfg, gone)

    code, refused = _review()

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _shown(refused)["offered"] == 1, _shown(refused)
    out = _trash(refused)
    assert not music.exists()
    (trashed,) = [one for one in tmp_path.rglob(music.name) if one != music]
    assert "Trash" in str(trashed) and trashed.read_bytes() == before
    assert other.exists()
    # The tombstone carries the landing's artist and title, which is what
    # ``label prune`` and ``label playlists`` match a track against (U243).
    (stone,) = stores.list_tombstones(cfg)
    assert stone.payload["artist"] == "Probe", stone.payload
    assert stone.payload["title"].endswith(" - One"), stone.payload
    assert stone.identity == tombstone.version_identity(
        artist="Probe", title=stone.payload["title"]
    ), stone.identity
    assert out["outcome"] == "ok"
    # ONCE: the next run offers nothing, the row still absent.
    assert _offered() == 0
    assert gone not in _candidates(cfg)


def test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, _music = _row(cfg, "One")
    _remove_outright(cfg, gone)

    first = _plan(cfg)
    sighted = watermark.WatermarkStore(cfg).read().absent[gone]
    # Another change to the library between two reviews moves the count on.
    _sql(cfg, ("UPDATE agentRegistry SET int_1 = int_1 + 5 WHERE registry_id = 'localUpdateCount'", ()))
    second = _plan(cfg)

    assert [one.row.sequence for one in first.candidates] == [sighted]
    assert [one.row.sequence for one in second.candidates] == [sighted]
    assert sighted > first.watermark.sequence
    assert [str(one.category) for one in second.candidates] == ["deletable"]


def test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    one, one_file = _row(cfg, "One")
    _remove_outright(cfg, one)
    code, refused = _review()
    assert _shown(refused)["offered"] == 1
    _trash(refused)
    # The watermark passed the trashed row, so a second removal after it is
    # the only one offered.
    two, two_file = _row(cfg, "Two")
    _remove_outright(cfg, two)

    code, refused = _review()

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _shown(refused)["offered"] == 1
    assert {item.row.content_id for item in _plan(cfg).deletable} == {two}
    assert two_file.exists() and not one_file.exists()


# ---------------------------------------------------------------------------
# Never offered
# ---------------------------------------------------------------------------


def test_a_landed_file_a_new_row_now_references_is_never_offered(
    native_library, silence, monkeypatch, tmp_path
):
    """Sitting 102 put Anabaz back by import: its old row is absent, its file a new row's."""
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, music = _row(cfg, "One")
    (columns,) = [
        values
        for values in _query(cfg, "SELECT * FROM djmdContent WHERE ID = ?", gone)
    ]
    names = [row[1] for row in _query(cfg, "PRAGMA table_info(djmdContent)")]
    _remove_outright(cfg, gone)
    # A re-import: a new row of another id naming the same file.
    again = dict(zip(names, columns))
    again["ID"] = str(int(gone) + 1)
    again["UUID"] = "re-imported"
    _sql(
        cfg,
        (
            f"INSERT INTO djmdContent ({', '.join(names)}) VALUES ({', '.join('?' for _ in names)})",
            tuple(again[name] for name in names),
        ),
    )

    assert _offered() == 0
    categories = _candidates(cfg)
    assert categories[gone] != "deletable", categories
    assert music.exists()


def test_a_landing_of_another_database_offers_nothing(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, music = _row(cfg, "One")
    landing = _landing_record(cfg)
    path = _record_path(cfg, landing.session_id)
    raw = json.loads(path.read_text())
    raw["detail"][native.LANDED_ROWS_KEY]["database_identity"] = "another-library"
    path.write_text(json.dumps(raw))
    _remove_outright(cfg, gone)

    assert gone not in _candidates(cfg)
    assert music.exists()


def test_an_unreadable_landing_record_offers_nothing_and_says_so(
    native_library, silence, monkeypatch, tmp_path, caplog
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, music = _row(cfg, "One")
    _record_path(cfg, _landing_record(cfg).session_id).write_text("{ not json")
    _remove_outright(cfg, gone)

    with caplog.at_level(logging.WARNING, logger="cratekit.deletion.run"):
        assert gone not in _candidates(cfg)
    assert any("could not be read" in one.getMessage() for one in caplog.records), caplog.text
    assert music.exists()


def test_rows_no_record_names_removed_outright_offer_nothing(
    native_library, silence, monkeypatch, tmp_path
):
    """A landing from before this card names no row, and neither does a hand import."""
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    for landing in session.records(cfg):
        path = _record_path(cfg, landing.session_id)
        raw = json.loads(path.read_text())
        raw["detail"].pop(native.LANDED_ROWS_KEY, None)
        path.write_text(json.dumps(raw))
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    for title in ("One", "Two"):
        _remove_outright(cfg, _row(cfg, title)[0])

    assert _offered() == 0
    assert _plan(cfg).candidates == ()


def test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal(
    native_library, silence, monkeypatch, tmp_path
):
    """R35: a library's first review baselines, the outright removals before it included."""
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two", "Three")
    _deletion_on(cfg, monkeypatch, tmp_path)
    old_one, _ = _row(cfg, "One")
    old_two, _ = _row(cfg, "Two")
    _remove_outright(cfg, old_one)
    _remove_outright(cfg, old_two)

    code, refused = _review()

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _shown(refused)["baselined"] is True
    assert _shown(refused)["accepted_as_history"] == 2, _shown(refused)
    found = _plan(cfg)
    assert found.candidates == (), found.candidates
    later, _ = _row(cfg, "Three")
    _remove_outright(cfg, later)
    assert set(_candidates(cfg)) == {later}


def test_a_landing_a_restore_rolled_back_offers_nothing(
    native_library, silence, monkeypatch, tmp_path
):
    """The rows are absent and nobody removed them: the database is from before the landing."""
    cfg, _root = native_library
    _land(cfg, silence, "Zero")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    shutil_copy = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="rolled back batch")
    one, music = _row(cfg, "One")
    # The database put back as it was before the second landing, the session
    # record of that landing kept (the log survives a rollback by design).
    Path(cfg.library.db_path).write_bytes(shutil_copy)

    assert one not in _candidates(cfg)
    assert music.exists()


def test_a_rolled_back_landing_whose_playlist_was_kept_is_history_by_its_count(
    native_library, silence, monkeypatch, tmp_path
):
    """A landing into a batch playlist already there leaves no playlist to miss."""
    cfg, _root = native_library
    _land(cfg, silence, "Zero")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="rolled back batch")
    one, music = _row(cfg, "One")
    landing = _landing_record(cfg)
    path = _record_path(cfg, landing.session_id)
    raw = json.loads(path.read_text())
    raw["detail"][native.LANDED_ROWS_KEY]["playlists"] = []
    path.write_text(json.dumps(raw))
    Path(cfg.library.db_path).write_bytes(before)

    assert one not in {
        key for key, category in _candidates(cfg).items() if category == "deletable"
    }
    # And it stays history once the count passes the landing's.
    _sql(cfg, ("UPDATE agentRegistry SET int_1 = int_1 + 500 WHERE registry_id = 'localUpdateCount'", ()))
    assert one not in _candidates(cfg)
    assert music.exists()


# ---------------------------------------------------------------------------
# One row, one candidate
# ---------------------------------------------------------------------------


def test_a_landed_row_marked_soft_deleted_is_one_candidate(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, _music = _row(cfg, "One")
    _mark_removed(cfg, gone)

    found = _plan(cfg)

    assert [one.row.content_id for one in found.candidates] == [gone]
    assert gone not in watermark.WatermarkStore(cfg).read().absent


def test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, _music = _row(cfg, "One")
    landing = _landing_record(cfg)
    (named,) = [
        one for one in landing.detail[native.LANDED_ROWS_KEY]["rows"] if one["content_id"] == gone
    ]
    _remove_outright(cfg, gone)
    recorded_at = _counter(cfg)
    # The record ``sync removed`` writes for the same row (U288).
    path = _record_path(cfg, landing.session_id)
    raw = json.loads(path.read_text())
    raw["detail"][deletion_library.RECORDED_REMOVALS_KEY] = {
        "database_identity": landing.detail[native.LANDED_ROWS_KEY]["database_identity"],
        "sequence": recorded_at,
        "rows": [{"content_id": gone, "columns": named["columns"]}],
    }
    path.write_text(json.dumps(raw))

    found = _plan(cfg)

    assert [(one.row.content_id, one.row.sequence) for one in found.candidates] == [
        (gone, recorded_at)
    ]


def test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered(
    native_library, silence, monkeypatch, tmp_path
):
    cfg, _root = native_library
    _land(cfg, silence, "One")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    gone, _music = _row(cfg, "One")
    names = [row[1] for row in _query(cfg, "PRAGMA table_info(djmdContent)")]
    (values,) = _query(cfg, "SELECT * FROM djmdContent WHERE ID = ?", gone)
    _remove_outright(cfg, gone)
    first = _plan(cfg)
    assert [one.row.content_id for one in first.candidates] == [gone]
    # A restore puts it back live: forgotten.
    _sql(
        cfg,
        (
            f"INSERT INTO djmdContent ({', '.join(names)}) VALUES ({', '.join('?' for _ in names)})",
            tuple(values),
        ),
    )
    assert _plan(cfg).candidates == ()
    assert gone not in watermark.WatermarkStore(cfg).read().absent
    # Removed again, at a later count.
    _remove_outright(cfg, gone)
    (again,) = _plan(cfg).candidates
    assert again.row.content_id == gone
    assert again.row.sequence > first.candidates[0].row.sequence


def test_the_watermark_reads_version_one_as_no_sightings_and_refuses_a_bad_one(native_library):
    cfg, _root = native_library
    store = watermark.WatermarkStore(cfg)
    store.path.parent.mkdir(parents=True, exist_ok=True)
    store.path.write_text(
        json.dumps({"version": 1, "database_identity": "db", "sequence": 7, "recorded": "", "actor": ""})
    )
    assert store.read().absent == {}
    mark = store.advance(database_identity="db", sequence=9, actor="a-person")
    assert json.loads(store.path.read_text())["version"] == watermark.WATERMARK_VERSION == 2
    assert mark.sequence == 9 and mark.absent == {}
    for bad in ([], {"1": True}, {"1": "7"}, {"": 7}):
        raw = json.loads(store.path.read_text())
        raw["absent"] = bad
        store.path.write_text(json.dumps(raw))
        with pytest.raises(CratekitError) as caught:
            store.read()
        assert caught.value.cause.reason == "deletion-watermark-unusable", bad


def test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says(
    native_library,
):
    cfg, _root = native_library
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db", sequence=5, actor="a-person")
    store.sight(database_identity="db", absent={"1": 3}, present=(), counter=8)
    assert store.read().absent == {"1": 8}
    assert store.advance(database_identity="db", sequence=8, actor="a-person").absent == {"1": 8}
    # A count not past the landing's own commit: history, at the watermark.
    store.sight(database_identity="db", absent={"2": 9}, present=(), counter=9)
    assert store.read().absent == {"1": 8, "2": 8}
    # Seen live again: forgotten.
    store.sight(database_identity="db", absent={}, present=("1",), counter=10)
    assert store.read().absent == {"2": 8}
    # Another database: the sightings went with the old position.
    mark, baselined = store.baseline(database_identity="other", sequence=1, actor="a-person")
    assert baselined and mark.absent == {}


# ---------------------------------------------------------------------------
# What the merge bar names: still in the collection, still referenced, a copy
# ---------------------------------------------------------------------------


def _insert_like(cfg: config.Config, content_id: str, **changed) -> None:
    """A new collection row copied from ``content_id``'s, with ``changed`` columns."""
    names = [row[1] for row in _query(cfg, "PRAGMA table_info(djmdContent)")]
    (values,) = _query(cfg, "SELECT * FROM djmdContent WHERE ID = ?", content_id)
    row = {**dict(zip(names, values)), **changed}
    _sql(
        cfg,
        (
            f"INSERT INTO djmdContent ({', '.join(names)}) VALUES ({', '.join('?' for _ in names)})",
            tuple(row[name] for name in names),
        ),
    )


def test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned(
    native_library, silence, monkeypatch, tmp_path
):
    """One removal re-imported, one left in a playlist, one copy a live row names, one free."""
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two", "Three", "Four")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    files = {title: _row(cfg, title) for title in ("One", "Two", "Three", "Four")}
    # One: re-imported, a new row of another id naming the same file.
    one, _ = files["One"]
    _insert_like(cfg, one, ID=str(int(one) + 7), UUID="re-imported-one")
    _remove_outright(cfg, one)
    # Two: its row deleted and a membership left naming it.
    two, _ = files["Two"]
    _sql(
        cfg,
        ("DELETE FROM djmdContent WHERE ID = ?", (two,)),
        ("UPDATE agentRegistry SET int_1 = int_1 + 3 WHERE registry_id = 'localUpdateCount'", ()),
    )
    # Three: a hard link of its file, at another path, is a live row's file.
    three, three_file = files["Three"]
    copy = three_file.with_name("Three copy.flac")
    copy.hardlink_to(three_file)
    _insert_like(cfg, three, ID=str(int(three) + 7), UUID="copy-three", FolderPath=str(copy))
    _remove_outright(cfg, three)
    # Four: removed, and nothing names its file.
    four, four_file = files["Four"]
    _remove_outright(cfg, four)
    kept = {title: path.read_bytes() for title, (_id, path) in files.items() if title != "Four"}

    categories = _candidates(cfg)
    code, refused = _review()

    assert categories == {
        one: "collides-with-active-row",
        two: "still-referenced",
        three: "collides-with-active-row",
        four: "deletable",
    }, categories
    assert code == int(ExitCode.DECISION_REQUIRED) and _shown(refused)["offered"] == 1
    _trash(refused)
    assert not four_file.exists()
    for title, held in kept.items():
        assert files[title][1].read_bytes() == held, title
    (stone,) = stores.list_tombstones(cfg)
    assert stone.payload["title"].endswith(" - Four"), stone.payload


def test_a_rolled_back_landing_is_kept_by_its_playlist_whatever_the_count(
    native_library, silence, monkeypatch, tmp_path
):
    """The playlist guard alone: the count is already past the landing at the first sighting."""
    cfg, _root = native_library
    _land(cfg, silence, "Zero")
    _deletion_on(cfg, monkeypatch, tmp_path)
    _baseline(cfg)
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="rolled back batch")
    one, music = _row(cfg, "One")
    landed_at = _landing_record(cfg).detail[native.LANDED_ROWS_KEY]["sequence"]
    Path(cfg.library.db_path).write_bytes(before)
    _sql(
        cfg,
        (
            "UPDATE agentRegistry SET int_1 = ? WHERE registry_id = 'localUpdateCount'",
            (landed_at + 500,),
        ),
    )

    assert one not in _candidates(cfg)
    assert one not in watermark.WatermarkStore(cfg).read().absent
    assert music.exists()
