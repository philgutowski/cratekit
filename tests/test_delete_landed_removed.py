"""R-1037: a landed row rekordbox's Remove from Collection deleted outright is offered.

rekordbox 7.2.19 deletes a removed track's rows outright (A178, A185), so no soft delete
marker says the row went. A native landing names every row it made on its session
record, and the pass reads a landed row neither live nor marked, numbered by the update
count at the first run that sees it absent; the rest is the pass's own. These land real
files on a disposable library, remove rows as rekordbox does, and drive ``crate delete
review`` through the dispatcher (D1).
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


def _land(cfg: config.Config, silence: Path, *titles: str, name: str = "landed batch") -> None:
    for title in titles:
        _stage(cfg, silence, f"{title}.flac")
    code, acted, _ = _two_acts(["intake", "land", "--name", name])
    assert code == int(ExitCode.OK), acted


def _row(cfg: config.Config, title: str) -> tuple[str, Path]:
    ((content_id, folder),) = _query(
        cfg, "SELECT ID, FolderPath FROM djmdContent WHERE Title LIKE ? AND rb_local_deleted = 0",
        f"% - {title}")
    return str(content_id), Path(folder)


def _sql(cfg: config.Config, *statements: tuple[str, tuple]) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        for statement, params in statements:
            conn.execute(statement, params)
    conn.close()


#: The row holding the database's update count, which rekordbox moves on every change.
COUNT = "registry_id = 'localUpdateCount'"


def _counter(cfg: config.Config) -> int:
    ((value,),) = _query(cfg, f"SELECT int_1 FROM agentRegistry WHERE {COUNT}")
    return int(value)


def _moved_on(by: int) -> tuple[str, tuple]:
    """The statement that moves the update count on by ``by``."""
    return (f"UPDATE agentRegistry SET int_1 = int_1 + ? WHERE {COUNT}", (by,))


def _count_at(cfg: config.Config, value: int) -> None:
    _sql(cfg, (f"UPDATE agentRegistry SET int_1 = ? WHERE {COUNT}", (value,)))


def _remove_outright(cfg: config.Config, content_id: str) -> None:
    """rekordbox's Remove from Collection: the row and its memberships, gone, the count past them."""
    _sql(
        cfg, ("DELETE FROM djmdSongPlaylist WHERE ContentID = ?", (content_id,)),
        ("DELETE FROM djmdContent WHERE ID = ?", (content_id,)), _moved_on(12))


def _mark_removed(cfg: config.Config, content_id: str) -> None:
    """The soft delete an earlier rekordbox wrote, the row kept with its marker set."""
    marked = (
        "UPDATE djmdContent SET rb_local_deleted = 1, rb_local_usn = "
        f"(SELECT int_1 FROM agentRegistry WHERE {COUNT}) WHERE ID = ?"
    )
    _sql(cfg, _moved_on(1), (marked, (content_id,)))


def _deletion_on(cfg: config.Config, monkeypatch) -> Path:
    """The full profile, rekordbox closed, a Trash beside the library's own. Returns the home."""
    config.save(dataclasses.replace(cfg, profile=config.ProfileConfig(name="full")))
    config.reset_cache()
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    home = Path(cfg.library.root).parent / "home"
    (home / ".Trash").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("cratekit.deletion.trash.Path.home", lambda: home)
    monkeypatch.setenv("XDG_DATA_HOME", str(home / "share"))
    return home


def _review() -> tuple[int, dict]:
    return drive(["delete", "review"])


def _gated() -> dict:
    """A review driven to the gate it always reaches; the refusal."""
    code, refused = _review()
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused


def _shown(refused: dict) -> dict:
    return refused["cause"]["detail"]["shown"]


def _trash(refused: dict) -> dict:
    decided, envelope = drive(
        ["run", "decide", refused["run_id"], GATE, "trash", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, out = drive(["--run", refused["run_id"], "delete", "review"])
    assert code == int(ExitCode.OK), out
    return out


def _baseline(cfg: config.Config) -> None:
    """The pass's first position, taken before anything was removed (R35)."""
    refused = _gated()
    assert _shown(refused)["baselined"] is True, _shown(refused)
    assert watermark.WatermarkStore(cfg).read() is not None


def _ready(native_library, silence, monkeypatch, *titles, name="landed batch"):
    """Land ``titles``, switch deletion on and take the pass's first position."""
    cfg, _root = native_library
    _land(cfg, silence, *titles, name=name)
    _deletion_on(cfg, monkeypatch)
    _baseline(cfg)
    return cfg


@pytest.fixture
def ready(native_library, silence, monkeypatch):
    """``_ready`` over this test's own library, given the titles and the batch's name."""

    def land(*titles, name="landed batch"):
        return _ready(native_library, silence, monkeypatch, *titles, name=name)
    return land


def _offered() -> int:
    """How many files a review offers, read off the gate it always reaches."""
    return int(_shown(_gated())["offered"])


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


def _edit_record(cfg: config.Config, session_id: str, change) -> None:
    """Rewrite one session record's ``detail`` through ``change``, as a hand edit would."""
    path = _record_path(cfg, session_id)
    raw = json.loads(path.read_text())
    change(raw["detail"])
    path.write_text(json.dumps(raw))


def _landing_record(cfg: config.Config, content_id: str) -> session.SessionRecord:
    """The one landing record naming ``content_id``, chosen by the row, never by list order."""
    (landing,) = [
        one
        for one in session.records(cfg)
        if content_id
        in {row["content_id"] for row in one.detail.get(native.LANDED_ROWS_KEY, {}).get("rows", ())}
    ]
    return landing


# ═══ The landing names what it made ════════════════════════════════════════


def test_the_landing_record_names_every_row_it_made_as_the_database_holds_it(
    native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    landed = _landing_record(cfg, _row(cfg, "One")[0]).detail[native.LANDED_ROWS_KEY]
    ((dbid,),) = _query(cfg, "SELECT DBID FROM djmdProperty")
    assert landed["database_identity"] == str(dbid)
    assert landed["sequence"] == _counter(cfg)
    held = {
        str(values[0]): dict(zip(("ID", "FolderPath", "FileSize", "Title"), values))
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
    # The one playlist it made, the batch, by id, which a removal leaves.
    (batch,) = landed["playlists"]
    assert _query(cfg, "SELECT Name FROM djmdPlaylist WHERE ID = ?", batch) == [("landed batch",)]


def test_the_key_and_its_columns_are_spelled_the_same_where_they_are_read():
    assert deletion_library.LANDED_ROWS_KEY == native.LANDED_ROWS_KEY
    assert deletion_library.RECORDED_COLUMNS == native.LANDED_COLUMNS == rb_writer.RECORDED_COLUMNS


# ═══ A landed row removed outright is offered once, and trashed ════════════


def test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once(ready, tmp_path):
    cfg = ready("One", "Two")
    gone, music = _row(cfg, "One")
    _kept, other = _row(cfg, "Two")
    before = music.read_bytes()
    _remove_outright(cfg, gone)
    refused = _gated()
    assert _shown(refused)["offered"] == 1, _shown(refused)
    out = _trash(refused)
    assert not music.exists()
    (trashed,) = [one for one in tmp_path.rglob(music.name) if one != music]
    assert "Trash" in str(trashed) and trashed.read_bytes() == before
    assert other.exists()
    # The tombstone carries the landing's artist and title, for label matching (U243).
    (stone,) = stores.list_tombstones(cfg)
    assert stone.payload["artist"] == "Probe", stone.payload
    assert stone.payload["title"].endswith(" - One"), stone.payload
    identity = tombstone.version_identity(artist="Probe", title=stone.payload["title"])
    assert stone.identity == identity, stone.identity
    assert out["outcome"] == "ok"
    # ONCE: the next run offers nothing, the row still absent.
    assert _offered() == 0
    assert gone not in _candidates(cfg)


def test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden(ready):
    cfg = ready("One")
    gone, _music = _row(cfg, "One")
    _remove_outright(cfg, gone)
    first = _plan(cfg)
    sighted = watermark.WatermarkStore(cfg).read().absent[gone]
    # Another change to the library between two reviews moves the count on.
    _sql(cfg, _moved_on(5))
    second = _plan(cfg)
    assert [one.row.sequence for one in first.candidates] == [sighted]
    assert [one.row.sequence for one in second.candidates] == [sighted]
    assert sighted > first.watermark.sequence
    assert [str(one.category) for one in second.candidates] == ["deletable"]


def test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired(ready):
    cfg = ready("One", "Two")
    one, one_file = _row(cfg, "One")
    _remove_outright(cfg, one)
    refused = _gated()
    assert _shown(refused)["offered"] == 1
    _trash(refused)
    # The watermark passed the trashed row, so only the second removal is offered.
    two, two_file = _row(cfg, "Two")
    _remove_outright(cfg, two)
    assert _shown(_gated())["offered"] == 1
    assert {item.row.content_id for item in _plan(cfg).deletable} == {two}
    assert two_file.exists() and not one_file.exists()


def test_a_landed_file_a_new_row_now_references_is_never_offered(ready):
    """Sitting 102 put Anabaz back by import: its old row is absent, its file a new row's."""
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    again = {**_columns(cfg, gone), "ID": str(int(gone) + 1), "UUID": "re-imported"}
    _remove_outright(cfg, gone)
    # A re-import: a new row of another id naming the same file.
    _insert(cfg, again)
    assert _offered() == 0
    categories = _candidates(cfg)
    assert categories[gone] != "deletable", categories
    assert music.exists()


def test_a_landing_of_another_database_offers_nothing(ready):
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    _edit_landing(cfg, gone, lambda landed: landed.update(database_identity="another-library"))
    _remove_outright(cfg, gone)
    assert gone not in _candidates(cfg)
    assert music.exists()


def test_an_unreadable_landing_record_offers_nothing_and_says_so(ready, caplog):
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    _record_path(cfg, _landing_record(cfg, gone).session_id).write_text("{ not json")
    _remove_outright(cfg, gone)
    with caplog.at_level(logging.WARNING, logger="cratekit.deletion.run"):
        assert gone not in _candidates(cfg)
    assert any("could not be read" in one.getMessage() for one in caplog.records), caplog.text
    assert music.exists()


def test_rows_no_record_names_removed_outright_offer_nothing(native_library, silence, monkeypatch):
    """A landing from before this card names no row, and neither does a hand import."""
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    for landing in session.records(cfg):
        _edit_record(cfg, landing.session_id, lambda raw: raw.pop(native.LANDED_ROWS_KEY, None))
    _deletion_on(cfg, monkeypatch)
    _baseline(cfg)
    for title in ("One", "Two"):
        _remove_outright(cfg, _row(cfg, title)[0])
    assert _offered() == 0
    assert _plan(cfg).candidates == ()


def test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal(
    native_library, silence, monkeypatch):
    """R35: a library's first review baselines, the outright removals before it included."""
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two", "Three")
    _deletion_on(cfg, monkeypatch)
    old_one, _ = _row(cfg, "One")
    old_two, _ = _row(cfg, "Two")
    _remove_outright(cfg, old_one)
    _remove_outright(cfg, old_two)
    refused = _gated()
    assert _shown(refused)["baselined"] is True
    assert _shown(refused)["accepted_as_history"] == 2, _shown(refused)
    found = _plan(cfg)
    assert found.candidates == (), found.candidates
    later, _ = _row(cfg, "Three")
    _remove_outright(cfg, later)
    assert set(_candidates(cfg)) == {later}


def test_a_landing_a_restore_rolled_back_offers_nothing(ready, silence):
    """The rows are absent and nobody removed them: the database is from before the landing."""
    cfg = ready("Zero")
    shutil_copy = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="rolled back batch")
    one, music = _row(cfg, "One")
    # The database put back before the second landing; its session record kept.
    Path(cfg.library.db_path).write_bytes(shutil_copy)
    assert one not in _candidates(cfg)
    assert music.exists()


def test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered(ready, silence):
    """Round two's B1: a hand restore writes no record, and a landing that made no
    playlist cannot be told from its rollback, so nothing is offered.
    """
    cfg = ready("Zero", name="same batch")
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="same batch")
    one, music = _row(cfg, "One")
    landed = _landing_record(cfg, one).detail[native.LANDED_ROWS_KEY]
    assert landed["playlists"] == [], landed
    Path(cfg.library.db_path).write_bytes(before)
    _count_at(cfg, landed["sequence"] + 40)
    assert _offered() == 0
    assert one not in _candidates(cfg)
    assert music.exists() and stores.list_tombstones(cfg) == ()


def test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept(ready, silence):
    """The price of that rule, said: a real removal of such a landing's track is not offered."""
    cfg = ready("Zero", name="same batch")
    _land(cfg, silence, "One", name="same batch")
    one, music = _row(cfg, "One")
    _remove_outright(cfg, one)
    assert one not in _candidates(cfg)
    assert music.exists()


# ═══ One row, one candidate ════════════════════════════════════════════════


def test_a_landed_row_marked_soft_deleted_is_one_candidate(ready):
    cfg = ready("One")
    gone, _music = _row(cfg, "One")
    _mark_removed(cfg, gone)
    found = _plan(cfg)
    assert [one.row.content_id for one in found.candidates] == [gone]
    assert gone not in watermark.WatermarkStore(cfg).read().absent


def test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number(ready):
    cfg = ready("One")
    gone, _music = _row(cfg, "One")
    landing = _landing_record(cfg, gone)
    (named,) = [
        one for one in landing.detail[native.LANDED_ROWS_KEY]["rows"] if one["content_id"] == gone
    ]
    _remove_outright(cfg, gone)
    recorded_at = _counter(cfg)
    # The record ``sync removed`` writes for the same row (U288).
    removals = {
        "database_identity": landing.detail[native.LANDED_ROWS_KEY]["database_identity"],
        "sequence": recorded_at,
        "rows": [{"content_id": gone, "columns": named["columns"]}],
    }
    key = deletion_library.RECORDED_REMOVALS_KEY
    _edit_record(cfg, landing.session_id, lambda detail: detail.update({key: removals}))
    found = _plan(cfg)
    assert [(one.row.content_id, one.row.sequence) for one in found.candidates] == [
        (gone, recorded_at)
    ]


def test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered(ready):
    cfg = ready("One")
    gone, _music = _row(cfg, "One")
    held = _columns(cfg, gone)
    _remove_outright(cfg, gone)
    first = _plan(cfg)
    assert [one.row.content_id for one in first.candidates] == [gone]
    # A restore puts it back live: forgotten.
    _insert(cfg, held)
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
    old = {"version": 1, "database_identity": "db", "sequence": 7, "recorded": "", "actor": ""}
    store.path.write_text(json.dumps(old))
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
    native_library):
    cfg, _root = native_library
    store = watermark.WatermarkStore(cfg)
    store.baseline(database_identity="db", sequence=5, actor="a-person")
    store.sight(database_identity="db", absent=("1",), present=(), counter=8)
    assert store.read().absent == {"1": 8}
    assert store.advance(database_identity="db", sequence=8, actor="a-person").absent == {"1": 8}
    # Numbered once: a later sighting at a later count keeps the first number.
    store.sight(database_identity="db", absent=("1", "2"), present=(), counter=9)
    assert store.read().absent == {"1": 8, "2": 9}
    # Seen live again: forgotten.
    store.sight(database_identity="db", absent=(), present=("1",), counter=10)
    assert store.read().absent == {"2": 9}
    # Another database: the sightings went with the old position.
    mark, baselined = store.baseline(database_identity="other", sequence=1, actor="a-person")
    assert baselined and mark.absent == {}


# ═══ What the merge bar names: still in the collection, referenced, a copy ══


def _columns(cfg: config.Config, content_id: str) -> dict:
    """``content_id``'s collection row, column by column."""
    names = [row[1] for row in _query(cfg, "PRAGMA table_info(djmdContent)")]
    (values,) = _query(cfg, "SELECT * FROM djmdContent WHERE ID = ?", content_id)
    return dict(zip(names, values))


def _insert(cfg: config.Config, row: dict) -> None:
    """A collection row written as ``row`` spells it."""
    marks = ", ".join("?" for _ in row)
    _sql(cfg, (f"INSERT INTO djmdContent ({', '.join(row)}) VALUES ({marks})", tuple(row.values())))


def _insert_like(cfg: config.Config, content_id: str, **changed) -> None:
    """A new collection row copied from ``content_id``'s, with ``changed`` columns."""
    _insert(cfg, {**_columns(cfg, content_id), **changed})


def test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned(ready):
    """One removal re-imported, one left in a playlist, one copy a live row names, one free."""
    cfg = ready("One", "Two", "Three", "Four")
    files = {title: _row(cfg, title) for title in ("One", "Two", "Three", "Four")}
    # One: re-imported, a new row of another id naming the same file.
    one, _ = files["One"]
    _insert_like(cfg, one, ID=str(int(one) + 7), UUID="re-imported-one")
    _remove_outright(cfg, one)
    # Two: its row deleted and a membership left naming it.
    two, _ = files["Two"]
    _sql(cfg, ("DELETE FROM djmdContent WHERE ID = ?", (two,)), _moved_on(3))
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
    refused = _gated()
    assert categories == {
        one: "collides-with-active-row", two: "still-referenced",
        three: "collides-with-active-row", four: "deletable",
    }, categories
    assert _shown(refused)["offered"] == 1
    _trash(refused)
    assert not four_file.exists()
    for title, held in kept.items():
        assert files[title][1].read_bytes() == held, title
    (stone,) = stores.list_tombstones(cfg)
    assert stone.payload["title"].endswith(" - Four"), stone.payload


def test_a_rolled_back_landing_is_kept_by_its_playlist_whatever_the_count(ready, silence):
    """The playlist guard alone: the count is already past the landing at the first sighting."""
    cfg = ready("Zero")
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", name="rolled back batch")
    one, music = _row(cfg, "One")
    landed_at = _landing_record(cfg, one).detail[native.LANDED_ROWS_KEY]["sequence"]
    Path(cfg.library.db_path).write_bytes(before)
    _count_at(cfg, landed_at + 500)
    assert one not in _candidates(cfg)
    assert one not in watermark.WatermarkStore(cfg).read().absent
    assert music.exists()


# ═══ A restore takes a landing's rows away, leaving a record (round one's B1)


def _restore(session_id: str) -> None:
    """``crate restore run`` of one session's capture, both acts."""
    code, refused = drive(["restore", "run", session_id])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, "restore.run.confirm", "restore", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, envelope = drive(["--run", run_id, "restore", "run", session_id])
    assert code == int(ExitCode.OK), envelope


def test_a_restored_landing_into_a_playlist_already_there_is_never_offered(ready, silence):
    """Round one's B1: the playlist was there, so the landing names none and offers nothing."""
    cfg = ready("Zero", name="same batch")
    _land(cfg, silence, "One", name="same batch")
    one, music = _row(cfg, "One")
    landing = _landing_record(cfg, one)
    landed = landing.detail[native.LANDED_ROWS_KEY]
    before = music.read_bytes()
    _restore(landing.session_id)
    assert not _query(cfg, "SELECT ID FROM djmdContent WHERE ID = ?", one)
    # It made no playlist, and later work moves the count past the landing.
    assert landed["playlists"] == []
    _land(cfg, silence, "Two", "Three", name="next batch")
    assert _counter(cfg) > landed["sequence"]
    assert _offered() == 0
    assert one not in _candidates(cfg)
    assert music.read_bytes() == before
    assert stores.list_tombstones(cfg) == ()


def test_a_landing_after_a_restore_is_still_offered_when_removed(ready, silence):
    """A landing after a restore makes its own playlist, and its removal is offered."""
    cfg = ready("Zero", name="same batch")
    _land(cfg, silence, "One", name="same batch")
    _restore(_landing_record(cfg, _row(cfg, "One")[0]).session_id)
    _land(cfg, silence, "Two", name="next batch")
    two, _music = _row(cfg, "Two")
    _remove_outright(cfg, two)
    assert _candidates(cfg) == {two: "deletable"}


def test_one_row_two_landings_name_keeps_the_later_landings_count():
    columns = {"ID": "7", "FolderPath": "/x/a.flac", "FileSize": 1, "ArtistName": "A", "Title": "T"}

    def landed(sequence: int) -> dict:
        return {
            native.LANDED_ROWS_KEY: {
                "database_identity": "db",
                "sequence": sequence,
                "playlists": ["p"],
                "rows": [{"content_id": "7", "columns": columns}],
            }
        }
    for order in ((landed(5), landed(9)), (landed(9), landed(5))):
        found = deletion_library.landed_absences(
            order, database_identity="db", present=(), uuids={}, playlist_held=lambda _one: True)
        assert {key: one.landed for key, one in found.absent.items()} == {"7": 9}


def _edit_landing(cfg: config.Config, content_id: str, change) -> None:
    landing = _landing_record(cfg, content_id)
    _edit_record(cfg, landing.session_id, lambda detail: change(detail[native.LANDED_ROWS_KEY]))


def _without_uuids(landed: dict) -> None:
    """A record as written before rows named their UUID."""
    for entry in landed["rows"]:
        entry.pop(native.LANDED_UUID_KEY)


@pytest.mark.parametrize("sequence", [None, "12", True])
def test_a_landing_record_with_no_update_count_offers_nothing(sequence, ready):
    """Row M2: a record that cannot say what its commit left is not guessed at."""
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    _edit_landing(cfg, gone, lambda landed: landed.update(sequence=sequence))
    _remove_outright(cfg, gone)
    assert gone not in _candidates(cfg)
    assert music.exists()


def test_a_landing_one_of_whose_playlists_is_gone_offers_nothing(ready):
    """Row M5: every playlist the landing made must remain, not any one of them."""
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    _edit_landing(cfg, gone, lambda landed: landed["playlists"].append("999999999"))
    _remove_outright(cfg, gone)
    assert gone not in _candidates(cfg)
    assert music.exists()


# ═══ A playlist deleted by hand is no rollback (R-1844, #926) ═══════════════


def _delete_playlist_outright(cfg: config.Config, playlist_id: str) -> None:
    """rekordbox's sidebar delete (A200): the playlist row and its members, gone, no marker."""
    _sql(
        cfg, ("DELETE FROM djmdSongPlaylist WHERE PlaylistID = ?", (playlist_id,)),
        ("DELETE FROM djmdPlaylist WHERE ID = ?", (playlist_id,)), _moved_on(3))


def test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once(ready):
    """The defect: the playlist gone outright read as a rollback, so the removal was never offered."""
    cfg = ready("One", "Two")
    gone, music = _row(cfg, "One")
    _kept, other = _row(cfg, "Two")
    (batch,) = _landing_record(cfg, gone).detail[native.LANDED_ROWS_KEY]["playlists"]
    _delete_playlist_outright(cfg, batch)
    _remove_outright(cfg, gone)
    refused = _gated()
    assert _shown(refused)["offered"] == 1, _shown(refused)
    assert "landings read as rolled back" not in _shown(refused)
    _trash(refused)
    assert not music.exists() and other.exists()
    assert _offered() == 0


def _batch(cfg: config.Config, content_id: str) -> str:
    (batch,) = _landing_record(cfg, content_id).detail[native.LANDED_ROWS_KEY]["playlists"]
    return batch


def _rolled_back() -> int:
    return int(_shown(_gated()).get("landings read as rolled back", 0))


def test_the_landing_record_names_each_row_by_the_uuid_the_database_holds(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "One", "Two")
    landed = _landing_record(cfg, _row(cfg, "One")[0]).detail[native.LANDED_ROWS_KEY]
    held = {str(key): uuid for key, uuid in _query(cfg, "SELECT ID, UUID FROM djmdContent")}
    for entry in landed["rows"]:
        uuid = entry[native.LANDED_UUID_KEY]
        assert uuid and uuid == held[entry["content_id"]], entry
    assert native.LANDED_UUID_KEY == deletion_library.LANDED_UUID_KEY


def test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it(ready, silence):
    """Every row and every playlist of the landing gone, the count past it: a rollback."""
    cfg = ready("Zero")
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", "Two", name="rolled back batch")
    one, music = _row(cfg, "One")
    two, other = _row(cfg, "Two")
    landed_at = _landing_record(cfg, one).detail[native.LANDED_ROWS_KEY]["sequence"]
    Path(cfg.library.db_path).write_bytes(before)
    _count_at(cfg, landed_at + 50)
    refused = _gated()
    assert _shown(refused)["offered"] == 0, _shown(refused)
    assert _shown(refused)["landings read as rolled back"] == 1, _shown(refused)
    assert not ({one, two} & set(_candidates(cfg)))
    assert music.exists() and other.exists()
    assert stores.list_tombstones(cfg) == ()


def test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing(ready):
    """A later import can draw a rolled back row's random id; only the id and UUID together prove it."""
    cfg = ready("One", "Two")
    gone, music = _row(cfg, "One")
    two, _other = _row(cfg, "Two")
    _sql(cfg, ("UPDATE djmdContent SET UUID = ? WHERE ID = ?", ("another-row", two)))
    _delete_playlist_outright(cfg, _batch(cfg, gone))
    _remove_outright(cfg, gone)
    assert gone not in _candidates(cfg)
    assert _rolled_back() == 1
    assert music.exists()


def test_a_landed_row_marked_soft_deleted_still_proves_its_landing(ready):
    """Held means live or marked: a marked row of the landing is still the landing's own row."""
    cfg = ready("One", "Two")
    gone, _music = _row(cfg, "One")
    marked, _other = _row(cfg, "Two")
    _delete_playlist_outright(cfg, _batch(cfg, gone))
    _mark_removed(cfg, marked)
    _remove_outright(cfg, gone)
    # The marked row is its own candidate; the removal beside it rides its proof.
    found = _candidates(cfg)
    assert found[gone] == "deletable" and marked in found, found


def test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row(ready):
    """As before this card: a marked playlist is held, so the lone landed row's removal is offered."""
    cfg = ready("One")
    gone, _music = _row(cfg, "One")
    _sql(cfg, ("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (_batch(cfg, gone),)))
    _remove_outright(cfg, gone)
    assert _candidates(cfg) == {gone: "deletable"}
    assert _rolled_back() == 0


def test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted(ready):
    """The price, said: nothing left tells this from a rollback, so the files stay and the screen counts it."""
    cfg = ready("One", "Two")
    one, music = _row(cfg, "One")
    two, other = _row(cfg, "Two")
    _delete_playlist_outright(cfg, _batch(cfg, one))
    _remove_outright(cfg, one)
    _remove_outright(cfg, two)
    assert not ({one, two} & set(_candidates(cfg)))
    assert _rolled_back() == 1
    assert music.exists() and other.exists()


def test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone(ready):
    """A record R-1037 wrote names no UUID: its playlist gone, it offers nothing, counted."""
    cfg = ready("One", "Two")
    gone, music = _row(cfg, "One")
    batch = _batch(cfg, gone)
    _edit_landing(cfg, gone, _without_uuids)
    _delete_playlist_outright(cfg, batch)
    _remove_outright(cfg, gone)
    assert gone not in _candidates(cfg)
    assert _rolled_back() == 1
    assert music.exists()


def test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains(
    ready, silence):
    """R-1843's case with a second row: the row left under its UUID proves the landing."""
    cfg = ready("Zero", name="same batch")
    _land(cfg, silence, "One", "Two", name="same batch")
    one, _music = _row(cfg, "One")
    assert _landing_record(cfg, one).detail[native.LANDED_ROWS_KEY]["playlists"] == []
    _remove_outright(cfg, one)
    assert _candidates(cfg) == {one: "deletable"}


def test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted():
    columns = {"ID": "7", "FolderPath": "/x/a.flac", "FileSize": 1, "ArtistName": "A", "Title": "T"}

    def landed(*rows: tuple[str, str], playlists=()) -> dict:
        return {
            native.LANDED_ROWS_KEY: {
                "database_identity": "db",
                "sequence": 5,
                "playlists": list(playlists),
                "rows": [
                    {"content_id": key, "columns": {**columns, "ID": key}, "uuid": uuid}
                    for key, uuid in rows
                ],
            }
        }
    found = deletion_library.landed_absences(
        [
            landed(("1", "u1")),  # every row held: no question to ask
            landed(("2", "u2"), ("3", "u3")),  # 3 held under its UUID: stands
            landed(("4", "u4"), ("5", "u5")),  # 5 held under another UUID: rolled back
            landed(("6", "u6"), playlists=["gone"]),  # its playlist gone: rolled back
            landed(("8", "u8"), playlists=["here"]),  # its playlist held: stands
            landed(("9", ""), ("10", "")),  # 10 held with no UUID either: rolled back
            landed(("11", "")),  # no proof, but every row held: nothing to list
        ],
        database_identity="db",
        present={"1", "3", "5", "10", "11"},
        uuids={"1": "u1", "3": "u3", "5": "another", "10": "", "11": ""},
        playlist_held=lambda one: one == "here")
    assert sorted(found.absent) == ["2", "8"]
    assert found.rolled_back == (frozenset({"4"}), frozenset({"6"}), frozenset({"9"}))
    assert found.unasked(()) == 3
    # A landing whose every absent row an earlier run numbered was asked about.
    assert found.unasked({"4", "9"}) == 1


def test_read_collection_keeps_each_rows_uuid_read_only():
    class Row:
        def __init__(self, content_id, uuid, deleted=0):
            self.ID, self.UUID, self.rb_local_deleted = content_id, uuid, deleted
            self.FolderPath, self.rb_local_usn, self.FileSize = f"/x/{content_id}.flac", 1, 1
            self.ArtistName = self.Title = "A"
    read = deletion_library.read_collection([Row("1", "u1"), Row("2", "u2", 1), Row("3", None)])
    assert dict(read.uuids) == {"1": "u1", "2": "u2", "3": ""}
    with pytest.raises(TypeError):
        read.uuids["4"] = "u4"  # type: ignore[index]


def test_a_handled_landing_whose_playlist_went_later_is_not_counted(ready):
    """Its one removal was offered and trashed; deleting its playlist afterwards asks nothing new."""
    cfg = ready("One")
    gone, music = _row(cfg, "One")
    batch = _batch(cfg, gone)
    _remove_outright(cfg, gone)
    refused = _gated()
    assert _shown(refused)["offered"] == 1, _shown(refused)
    _trash(refused)
    assert not music.exists()
    _delete_playlist_outright(cfg, batch)
    assert _rolled_back() == 0


def test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted(ready):
    """The first removal is offered on its siblings' proof; once they go, the landing is counted."""
    cfg = ready("One", "Two", "Three")
    one, music = _row(cfg, "One")
    two, _ = _row(cfg, "Two")
    three, _ = _row(cfg, "Three")
    _delete_playlist_outright(cfg, _batch(cfg, one))
    _remove_outright(cfg, one)
    assert _offered() == 1
    _remove_outright(cfg, two)
    _remove_outright(cfg, three)
    assert not ({one, two, three} & set(_candidates(cfg)))
    assert _rolled_back() == 1
    assert music.exists()


def test_a_landing_whose_rows_are_all_held_is_not_counted_whatever_its_playlist(ready):
    """No row absent, no question: an older record with its playlist gone is not a rollback to count."""
    cfg = ready("One")
    held, _music = _row(cfg, "One")
    _edit_landing(cfg, held, _without_uuids)
    _delete_playlist_outright(cfg, _batch(cfg, held))
    assert _rolled_back() == 0


def test_the_first_review_counts_a_landing_already_rolled_back(
    native_library, silence, monkeypatch):
    """The run that baselines says it too: a landing rolled back before any review is counted."""
    cfg, _root = native_library
    before = Path(cfg.library.db_path).read_bytes()
    _land(cfg, silence, "One", "Two")
    Path(cfg.library.db_path).write_bytes(before)
    _deletion_on(cfg, monkeypatch)
    refused = _gated()
    assert _shown(refused)["baselined"] is True, _shown(refused)
    assert _shown(refused)["landings read as rolled back"] == 1, _shown(refused)
