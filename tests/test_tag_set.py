"""U339: ``crate tag set GENRE`` gives the rows named a declared genre over the one they carry.

The plan on a disposable database and real containers, one row per outcome;
the apply with every column and every other tag compared across the write; the
lookup row minted on the linking commit; then the verb through the dispatcher,
the restore of its session, and the record ``adopt move`` reads. The library
is ``tests/test_tag_rows.py``'s. D1 applies.
"""

from __future__ import annotations

import ast
import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import genre_moves
from cratekit.core import active_taxonomy, rb_writer, restore_tags, session, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import genre_set as gs
from cratekit.tagging import genre_set_cli, rows
from cratekit.write import metadata
from tests.cli_drive import drive
from tests.test_rb_writer_db import _row
from tests.test_tag_rows import (
    ABSENT,
    DEEP,
    MELODIC,
    OLD,
    UNREADABLE,
    Track,
    _content,
    _file,
    _genre_ids,
    _genre_of,
    _query,
    build,
)
from tests.test_tag_rows import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_tag_rows import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_tag_rows import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_tag_rows import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_tag_rows import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_tag_rows import machine as machine  # noqa: PLC0414
from tests.test_tag_rows import silence as silence  # noqa: PLC0414

GATE = genre_set_cli.CONFIRM_GATE

#: A genre the shipped taxonomy declares and the library here has no lookup row for.
AFRO = "Afro House"

#: The playlist folder and playlist this file seeds, and its path.
FOLDER_ID, PICKS_ID = "700", "701"
PICKS = "INBOX / Picks"


def _verb(*argv: str) -> list[str]:
    return ["tag", "set", *argv]


def _plan(cfg, genre: str, ids, *, playlist: str = "", leave=()) -> gs.SetPlan:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return gs.plan_set(
            cfg,
            db,
            active_taxonomy.load(cfg),
            genre,
            gs.scoped(db, ids, playlist),
            playlist=playlist,
            leave=leave,
        )
    finally:
        rb_writer.close_db(db)


def _apply(cfg, genre: str, ids, **kwargs) -> tuple[gs.SetPlan, gs.Written]:
    plan = _plan(cfg, genre, ids, **kwargs)
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        written = gs.apply_set(
            cfg,
            db,
            plan,
            declared=active_taxonomy.load(cfg),
            analysis_roots=[Path(cfg.library.root) / "analysis"],
        )
    finally:
        rb_writer.close_db(db)
    return plan, written


def _two_acts(argv: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *argv])
    return code, acted, refused


def _genre_rows(cfg, name: str) -> list[tuple]:
    return _query(
        cfg, "SELECT ID, rb_local_deleted FROM djmdGenre WHERE Name = ? ORDER BY ID", name
    )


def _tags_of(cfg, content_id: str) -> dict[str, str | None]:
    path = _file(cfg, content_id)
    return {name: tags.read_tag(path, name) for name in ("genre", "title", "artist", "album")}


def _seed_picks(cfg, *content_ids: str, attribute: int = 0) -> None:
    """``INBOX / Picks``, holding ``content_ids`` in that order, one removed member too."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(_row(tables.DjmdPlaylist, ID=FOLDER_ID, Seq=1, Name="INBOX",
                            Attribute=1, ParentID="root", rb_local_deleted=0))
        db_session.add(_row(tables.DjmdPlaylist, ID=PICKS_ID, Seq=1, Name="Picks",
                            Attribute=attribute, ParentID=FOLDER_ID, rb_local_deleted=0))
        for number, content_id in enumerate(content_ids, start=1):
            db_session.add(_row(tables.DjmdSongPlaylist, ID=f"8{number:02d}",
                                PlaylistID=PICKS_ID, ContentID=content_id, TrackNo=number,
                                rb_local_deleted=0))
        db_session.add(_row(tables.DjmdSongPlaylist, ID="899", PlaylistID=PICKS_ID,
                            ContentID="99", TrackNo=99, rb_local_deleted=1))
        db_session.commit()
    engine.dispose()


def _tombstone(cfg, name: str, genre_id: str = "900") -> None:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        connection.execute(
            "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
            "VALUES (?, ?, 'u', 1, '2026-01-01', '2026-01-01')",
            (genre_id, name),
        )
        connection.commit()
    finally:
        connection.close()


# 1. The plan: one item per named row


def test_a_row_with_another_genre_is_planned_for_its_file_and_its_row(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    plan = _plan(machine, DEEP, ["10"])
    (item,) = plan.items
    assert (item.row, item.file, item.action, item.reason) == (MELODIC, MELODIC, gs.WRITE, "")
    assert item.file_writes and item.row_writes
    assert plan.genre_row == _genre_ids()[DEEP]


def test_only_the_surface_that_differs_is_planned(machine, silence):
    build(machine, silence, Track("10", DEEP, MELODIC), Track("11", MELODIC, DEEP))
    first, second = _plan(machine, DEEP, ["10", "11"]).items
    assert (first.file_writes, first.row_writes) == (True, False)
    assert (second.file_writes, second.row_writes) == (False, True)


def test_every_named_row_is_one_item_in_the_order_named_and_counted_once(machine, silence):
    build(
        machine, silence,
        Track("10", MELODIC, MELODIC),
        Track("11", DEEP, DEEP),
        Track("12", MELODIC, ABSENT),
        Track("13", MELODIC, UNREADABLE),
        Track("14", MELODIC, MELODIC, deleted=True),
        Track("15", "", ""),
    )
    plan = _plan(machine, DEEP, ["15", "14", "13", "12", "11", "10", "404", "10"])
    assert [(item.content_id, item.reason) for item in plan.items] == [
        ("15", ""), ("14", gs.ROW_GONE), ("13", rows.FILE_UNREADABLE),
        ("12", rows.FILE_MISSING), ("11", gs.ALREADY), ("10", ""), ("404", gs.ROW_GONE),
    ]
    assert dict(plan.counts) == {
        **dict.fromkeys(gs.OUTCOMES, 0),
        gs.WRITE: 2, gs.ROW_GONE: 2, rows.FILE_UNREADABLE: 1, rows.FILE_MISSING: 1,
        gs.ALREADY: 1,
    }
    assert sum(plan.counts.values()) == len(plan.items)


def test_a_file_holding_two_genres_is_left_and_both_are_shown(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    assert tags.write_tag_values(_file(machine, "10"), "genre", [MELODIC, OLD])
    (item,) = _plan(machine, DEEP, ["10"]).items
    assert item.reason == gs.FILE_MULTI_VALUED and item.file == f"{MELODIC}; {OLD}"


def test_a_row_held_out_is_listed_and_a_held_identifier_naming_none_is_carried(
    machine, silence
):
    build(machine, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    plan = _plan(machine, DEEP, ["10", "11"], leave=("11", "77"))
    assert [(item.content_id, item.reason) for item in plan.items] == [
        ("10", ""), ("11", gs.HELD_OUT)
    ]
    assert plan.leave_unmatched == ("77",)
    assert plan.digest != _plan(machine, DEEP, ["10", "11"], leave=("11",)).digest


def test_the_digest_names_no_path_and_moves_with_a_word(machine, silence, tmp_path):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    plan = _plan(machine, DEEP, ["10"])
    assert str(_file(machine, "10")) not in json.dumps([i.digested() for i in plan.items])
    assert tags.write_genre(_file(machine, "10"), OLD)
    assert _plan(machine, DEEP, ["10"]).digest != plan.digest


# 2. The scope


def test_a_playlist_names_its_live_rows_in_its_order(machine, silence):
    build(machine, silence, *(Track(cid, MELODIC, MELODIC) for cid in ("10", "11", "12")))
    _seed_picks(machine, "12", "10")
    plan = _plan(machine, DEEP, [], playlist=PICKS)
    assert [item.content_id for item in plan.items] == ["12", "10"]
    assert plan.playlist == PICKS
    # THE PLAYLIST IS DIGESTED, so the same rows named another way ask again.
    assert plan.digest != _plan(machine, DEEP, ["12", "10"]).digest


@pytest.mark.parametrize(
    ("path", "attribute", "said"),
    [
        pytest.param("INBOX / Nowhere", 0, "no playlist or folder is at", id="absent"),
        pytest.param("INBOX", 0, "is a folder", id="a-folder"),
        pytest.param(PICKS, 4, "is a smart playlist", id="smart"),
        pytest.param(" / Picks", 0, "is not a playlist path", id="blank-part"),
    ],
)
def test_a_playlist_path_naming_no_plain_playlist_refuses(machine, silence, path, attribute, said):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    _seed_picks(machine, "10", attribute=attribute)
    with pytest.raises(CratekitError) as refused:
        _plan(machine, DEEP, [], playlist=path)
    assert refused.value.cause.reason == "tag-set-scope-unknown"
    assert said in refused.value.cause.message


def test_two_nodes_of_one_name_refuse(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    _seed_picks(machine, "10")
    connection = sqlite3.connect(machine.library.db_path)
    connection.execute(
        "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
        "created_at, updated_at) VALUES ('702', 2, 'Picks', 0, ?, 0, '2026-01-01', '2026-01-01')",
        (FOLDER_ID,),
    )
    connection.commit()
    connection.close()
    with pytest.raises(CratekitError) as refused:
        _plan(machine, DEEP, [], playlist=PICKS)
    assert "2 nodes are at 'INBOX / Picks'" in refused.value.cause.message


def _seed_nodes(cfg, *nodes: tuple[str, str, int, str], members: tuple[str, ...] = ()) -> None:
    """Playlist nodes as (ID, name, attribute, parent ID), the last holding ``members``."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        for node_id, name, attribute, parent in nodes:
            db_session.add(_row(tables.DjmdPlaylist, ID=node_id, Seq=1, Name=name,
                                Attribute=attribute, ParentID=parent, rb_local_deleted=0))
        for number, content_id in enumerate(members, start=1):
            db_session.add(_row(tables.DjmdSongPlaylist, ID=f"{nodes[-1][0]}{number:02d}",
                                PlaylistID=nodes[-1][0], ContentID=content_id,
                                TrackNo=number, rb_local_deleted=0))
        db_session.commit()
    engine.dispose()


def test_a_playlist_under_a_folder_whose_name_holds_the_separator_is_found(machine, silence):
    """The genre folders adoption makes are often named with ' / ' (review round one)."""
    build(machine, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    _seed_nodes(
        machine,
        ("710", "BY GENRE + ENERGY", 1, "root"),
        ("711", "House", 1, "710"),
        ("712", "House / Funky House / Disco", 1, "710"),
        ("713", "High", 0, "712"),
        members=("11", "10"),
    )
    _seed_nodes(machine, ("720", "TEE EM DEE 1/7", 0, "root"), members=("10",))
    path = "BY GENRE + ENERGY / House / Funky House / Disco / High"
    assert [item.content_id for item in _plan(machine, DEEP, [], playlist=path).items] == [
        "11", "10"
    ]
    assert [i.content_id for i in _plan(machine, DEEP, [], playlist="TEE EM DEE 1/7").items] == [
        "10"
    ]
    with pytest.raises(CratekitError) as refused:
        _plan(machine, DEEP, [], playlist="BY GENRE + ENERGY / House / Funky House / Disco / Low")
    assert "'BY GENRE + ENERGY / House / Funky House / Disco' is found" in (
        refused.value.cause.message
    )


def test_a_genre_naming_the_folder_the_row_is_filed_in_leaves_none():
    declared = taxonomy.default_taxonomy()
    filed = _held_in("house_funky_disco")
    assert gs._leaves(declared, "Disco", "Funky House", "10", filed) == ""
    assert gs._leaves(declared, DEEP, "Funky House", "10", filed) == "house_funky_disco"
    assert gs._leaves(declared, DEEP, "", "10", filed) == ""


@pytest.mark.parametrize("path", ["INBOX / Picks /", "INBOX /  / Picks", "/ INBOX / Picks"])
def test_a_path_with_an_empty_name_is_not_a_playlist_path(machine, silence, path):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    _seed_picks(machine, "10")
    with pytest.raises(CratekitError) as refused:
        _plan(machine, DEEP, [], playlist=path)
    assert "is not a playlist path" in refused.value.cause.message


def test_the_rows_file_skips_blank_lines_comments_and_a_byte_order_mark(tmp_path):
    listed = tmp_path / "rows.txt"
    listed.write_text("\ufeff# the set\n10  # the first\n\n  11  \n#12\n", encoding="utf-8")
    args = SimpleNamespace(rows=["9"], rows_from=str(listed), playlist=None)
    assert genre_set_cli.named_rows(args) == (["9", "10", "11"], "")


def test_no_rows_named_and_an_unreadable_rows_file_refuse(tmp_path):
    for args in (
        SimpleNamespace(rows=[], rows_from=None, playlist=None),
        SimpleNamespace(rows=[], rows_from=str(tmp_path / "absent.txt"), playlist=None),
    ):
        with pytest.raises(CratekitError) as refused:
            genre_set_cli.named_rows(args)
        assert refused.value.cause.reason == "tag-set-scope-unknown"


# 3. The apply


def test_the_apply_writes_the_genre_on_file_and_row_and_nothing_else(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", OLD, ""), Track("12", OLD, OLD))
    assert tags.write_tags(_file(cfg, "10"), {"title": "a title", "artist": "an artist"})
    before, other = _content(cfg), _tags_of(cfg, "12")
    tagged = _tags_of(cfg, "10")

    _plan_, written = _apply(cfg, DEEP, ["10", "11"])

    assert (written.written, written.read_back, written.wrong, written.moved) == (2, 2, (), ())
    assert written.files.read_back == ("10", "11") and written.files.clean
    assert [_genre_of(cfg, cid) for cid in ("10", "11", "12")] == [DEEP, DEEP, OLD]
    assert _tags_of(cfg, "10") == {**tagged, "genre": DEEP}
    assert _tags_of(cfg, "11")["genre"] == DEEP and _tags_of(cfg, "12") == other
    after = _content(cfg)
    for content_id, row in before.items():
        changed = {
            column for column in row
            if after[content_id][column] != row[column]
            and column not in rb_writer.BOOKKEEPING_COLUMNS
        }
        assert changed == ({"GenreID"} if content_id in ("10", "11") else set())


def test_a_file_that_moved_since_the_plan_is_named_and_its_row_left(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    plan = _plan(cfg, DEEP, ["10", "11"])
    assert tags.write_genre(_file(cfg, "11"), OLD)
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        written = gs.apply_set(
            cfg, db, plan, declared=active_taxonomy.load(cfg),
            analysis_roots=[Path(cfg.library.root) / "analysis"],
        )
    finally:
        rb_writer.close_db(db)
    assert written.files.moved == ("11",) and written.written == 1
    assert _genre_of(cfg, "11") == MELODIC and _tags_of(cfg, "11")["genre"] == OLD


def test_the_session_record_keeps_each_written_files_old_genre(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", OLD, ""),
          Track("12", MELODIC, DEEP))
    _plan_, written = _apply(cfg, DEEP, ["10", "11", "12"])
    record = session.read_record(written.session_id, cfg)
    assert record.detail[restore_tags.GENRE_RECORD_KEY] == [
        {"content_id": "10", "path": str(_file(cfg, "10")), "genre": MELODIC},
        {"content_id": "11", "path": str(_file(cfg, "11")), "genre": ""},
    ]
    kept = restore_tags.kept_by(record)
    assert [(f.path.name, f.kept, f.genre) for f in kept] == [
        ("track-10.flac", ("genre",), MELODIC), ("track-11.flac", ("genre",), "")
    ]
    assert record.sources == {gs.CHANGE_KEY: "committed"}


def _held_in(*buckets: str) -> SimpleNamespace:
    """A tree as adoption reads it, holding every row in ``buckets``' high band."""
    return SimpleNamespace(read=True, holds=lambda bucket, _cid: ("high",) * (bucket in buckets))


def test_a_row_leaves_the_folder_its_old_genre_filed_it_in_only_where_the_tree_holds_it(
    machine, silence
):
    build(machine, silence, Track("10", MELODIC, MELODIC), Track("11", "", ""),
          Track("12", DEEP, MELODIC), Track("13", OLD, OLD))
    db = rb_writer.open_db(machine.library.db_path, unlock=False, cfg=machine)
    try:
        declared = active_taxonomy.load(machine)
        ids = ["10", "11", "12", "13"]
        filed = gs.plan_set(machine, db, declared, DEEP, ids, held=_held_in("melodic_house"))
        unread = gs.plan_set(machine, db, declared, DEEP, ids,
                             held=SimpleNamespace(read=False, holds=_held_in().holds))
        nowhere = gs.plan_set(machine, db, declared, DEEP, ids, held=_held_in())
    finally:
        rb_writer.close_db(db)
    # A blank row, a row already carrying the genre and a row the tree does not
    # hold in its old folder leave none; the leaving folder is digested.
    assert [item.leaves for item in filed.items] == ["melodic_house", "", "", ""]
    # A TREE THAT COULD NOT BE READ records the old folder, which the move asks
    # only where the tree it reads then holds the row (review round two).
    assert [item.leaves for item in unread.items] == ["melodic_house", "", "", ""]
    assert [item.leaves for item in nowhere.items] == ["", "", "", ""]
    assert filed.digest != nowhere.digest
    assert gs.moved_out_of(filed.items) == {
        "10": frozenset({"melodic_house"}), "11": frozenset(), "12": frozenset(),
        "13": frozenset(),
    }


def test_a_second_run_plans_nothing_and_writes_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    _apply(cfg, DEEP, ["10"])
    settled = _content(cfg)
    plan = _plan(cfg, DEEP, ["10"])
    assert plan.writes == () and [item.reason for item in plan.items] == [gs.ALREADY]
    assert _content(cfg) == settled


def test_the_policy_registered_is_the_retag_genres_and_no_creation_is_asked_for(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    asked: list = []
    real = rb_writer.commit_guarded

    def noting(db, **kwargs):
        asked.append(tuple(kwargs.get("creations", ())))
        return real(db, **kwargs)

    monkeypatch.setattr(rb_writer, "commit_guarded", noting)
    _apply(cfg, DEEP, ["10"])
    assert asked == [()]
    assert metadata.RETAG_GENRE in rb_writer.registered_field_policies()


# 4. The read back


def test_a_clean_read_back_raises_nothing_and_a_moved_column_refuses_first():
    clean = gs.Written(session_id="s", written=1, read_back=1)
    gs.assert_read_back(clean)
    with pytest.raises(CratekitError) as moved:
        gs.assert_read_back(gs.Written("s", 1, 0, wrong=("10: x",), moved=("10: Title",)))
    assert moved.value.cause.reason == "whitelist-violation"
    with pytest.raises(CratekitError) as wrong:
        gs.assert_read_back(gs.Written("s", 1, 0, wrong=("10: reads 'x'",)))
    assert wrong.value.cause.reason == "internal-error"
    assert "restore session s" in " ".join(wrong.value.cause.remediation.steps)


def test_the_judge_names_a_row_off_its_genre_and_one_with_another_column_moved():
    item = gs.Item("10", "/x", "t", MELODIC, MELODIC, gs.WRITE, row_writes=True)
    before = {"10": {"GenreID": "1", "Title": "a"}}
    after = {"10": {"GenreID": "2", "Title": "b"}}
    wrong, moved = gs.judge(DEEP, [item], before, after, {"2": OLD})
    assert wrong == ("10: reads 'Progressive / Melodic', not 'Deep House'",)
    assert moved == ("10: Title",)
    assert gs.judge(DEEP, [item], before, {}, {}) == (("10: the row could not be read",), ())


# 5. The verb


def test_an_undeclared_genre_refuses_before_the_acknowledgment_and_any_read(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    code, refused = drive(_verb("Zydeco", "--row", "10"))
    assert code != int(ExitCode.OK)
    assert refused["cause"]["reason"] == "review-selection-invalid"
    assert "'Zydeco'" in refused["cause"]["message"]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC))
    code, refused = drive(_verb(DEEP, "--row", "10"))
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing"
    assert _genre_of(machine, "10") == MELODIC


def test_planned_written_and_read_back_through_the_two_acts(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", DEEP, DEEP))
    _seed_picks(cfg, "11", "10")

    code, acted, refused = _two_acts(_verb(DEEP, "--playlist", PICKS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == acted["data"]["digest"]
    assert shown["genre_row"] == _genre_ids()[DEEP] and shown["playlist"] == PICKS
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["written"], totals["read_back"]) == (2, 1, 1)
    assert [_genre_of(cfg, cid) for cid in ("10", "11")] == [DEEP, DEEP]
    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes == [
        genre_set_cli.GENRE_WRITTEN, genre_set_cli.FILE_NEXT, genre_set_cli.ROWS_LEFT
    ]
    # NO TREE IS READ HERE, so the row's old folder is recorded for the move to
    # ask, and both steps are named.
    assert "run `crate adopt apply`" in acted["warnings"][1]["message"]
    assert "then `crate adopt move`, which takes the 1 row(s)" in acted["warnings"][1]["message"]
    assert "`with vox` or Favorites membership" in acted["warnings"][1]["message"]
    assert "(1 already-that-genre)" in acted["warnings"][2]["message"]


def test_a_plan_of_gone_rows_alone_names_no_missing_genre_row(acknowledged, silence):
    """The reason given is the true one (review round two)."""
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    code, acted, _refused = _two_acts(_verb(AFRO, "--row", "404"))
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op"
    said = [warning["message"] for warning in acted["warnings"]]
    assert "no genre row" not in said[0] and "0 of 1 named row(s)" in said[0]
    assert "(1 row-gone)" in said[1]
    assert _genre_rows(cfg, AFRO) == []
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == MELODIC


def test_the_gate_takes_no_inline_answer_and_a_declined_gate_writes_nothing(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    code, refused = drive(_verb(DEEP, "--row", "10"))
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *_verb(DEEP, "--row", "10")])
    assert acted["outcome"] == "no_op" and _genre_of(cfg, "10") == MELODIC
    assert _tags_of(cfg, "10")["genre"] == MELODIC


def test_a_file_changed_between_the_gate_and_the_apply_refuses_stale(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    argv = _verb(DEEP, "--row", "10")
    _code, refused = drive(argv)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert tags.write_genre(_file(cfg, "10"), OLD)

    code, acted = drive(["--run", run_id, *argv])

    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] in {"decision-stale", "decision-invalidated"}
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == OLD


def test_a_file_changed_after_the_gate_refuses_stale_on_the_write_handle(acknowledged, silence):
    """The stale check in the apply itself, past the gate layer's own (review round one)."""
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    args = SimpleNamespace(rows=["10"], rows_from=None, playlist=None, leave=[])
    declared = active_taxonomy.load(cfg)
    approved = genre_set_cli.read_plan(cfg, declared, DEEP, args)
    assert tags.write_genre(_file(cfg, "10"), OLD)
    with pytest.raises(CratekitError) as refused:
        genre_set_cli.apply_plan(cfg, approved, declared, args)
    assert refused.value.cause.reason == "decision-stale"
    assert refused.value.cause.detail["moved"] == ["10"]
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == OLD
    assert [r for r in session.records(cfg) if r.workflow == gs.WORKFLOW] == []


def test_a_file_gone_between_the_plan_and_the_apply_writes_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    plan = _plan(cfg, DEEP, ["10", "11"])
    _file(cfg, "11").unlink()
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        again = _plan(cfg, DEEP, ["10", "11"])
        with pytest.raises(CratekitError) as refused:
            gs.assert_plan_unchanged(plan, again)
    finally:
        rb_writer.close_db(db)
    assert refused.value.cause.reason == "decision-stale"
    assert refused.value.cause.detail["moved"] == ["11"]
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == MELODIC


def test_a_second_run_after_a_clean_one_asks_and_is_a_no_op(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    code, _acted, _refused = _two_acts(_verb(DEEP, "--row", "10"))
    assert code == int(ExitCode.OK)
    code, acted, refused = _two_acts(_verb(DEEP, "--row", "10"))
    assert acted["outcome"] == "no_op"
    assert acted["warnings"][0]["code"] == genre_set_cli.NOTHING_TO_WRITE
    assert refused["cause"]["detail"]["shown"]["items"][0]["reason"] == gs.ALREADY


def test_a_file_that_will_not_take_the_genre_refuses_after_the_rest_landed(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    real = tags.write_genre
    monkeypatch.setattr(
        tags, "write_genre", lambda path, genre: False if "11" in path.name else real(path, genre)
    )
    code, acted, _refused = _two_acts(_verb(DEEP, "--row", "10", "--row", "11"))
    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] == genre_set_cli.UNWRITTEN
    assert acted["data"]["totals"]["written"] == 1
    assert [_genre_of(cfg, cid) for cid in ("10", "11")] == [DEEP, MELODIC]


def test_the_restore_puts_the_files_and_rows_back(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", OLD, ""))
    code, acted, _refused = _two_acts(_verb(DEEP, "--row", "10", "--row", "11"))
    assert code == int(ExitCode.OK), acted
    (record,) = [one for one in session.records(cfg) if one.workflow == gs.WORKFLOW]

    restore_gate = "restore.run.confirm"
    verb = ["restore", "run", record.session_id]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, restore_gate, "restore", "--actor", "a-person"])
    code, restored = drive(["--run", run_id, *verb])

    assert code == int(ExitCode.OK), restored
    assert [_genre_of(cfg, cid) for cid in ("10", "11")] == [MELODIC, OLD]
    assert _tags_of(cfg, "10")["genre"] == MELODIC
    # A GENRE THE FILE NEVER HAD IS PUT BACK ABSENT.
    assert _tags_of(cfg, "11")["genre"] is None
    assert restored["data"]["totals"]["file_tags"]["read_back"] == 2
    assert dict(genre_moves.read(cfg)) == {}


# 6. What the verb is


def test_the_verb_declares_the_files_and_the_row_behind_an_explicit_gate():
    from cratekit.cli import registry

    entry = registry.entry("tag.set")
    assert entry.writes == frozenset({"files", "db_metadata"}) and entry.destructive
    (confirm,) = [gate for gate in entry.gates if gate.name == GATE]
    assert confirm.explicit and confirm.digest_source == "plan"


def test_the_record_key_is_the_one_the_restore_reads():
    assert gs.RECORD_KEY == restore_tags.GENRE_RECORD_KEY


def test_the_engine_writes_no_tag_but_the_genre():
    tree = ast.parse(Path(gs.__file__).read_text(encoding="utf-8"))
    writers = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "tags"
        and node.func.attr.startswith(("write", "clear"))
    }
    assert writers == {"write_genre"}


# 7. The genre row the library lacks, made on the commit that links it (R-1967)


def _active_genre_rows(cfg, name: str) -> list[str]:
    return [genre_id for genre_id, deleted in _genre_rows(cfg, name) if not deleted]


def _noting_commits(monkeypatch) -> list[tuple]:
    """Every ``creations`` the apply's commits ask for, in order."""
    asked: list[tuple] = []
    real = rb_writer.commit_guarded

    def noting(db, **kwargs):
        asked.append(tuple(kwargs.get("creations", ())))
        return real(db, **kwargs)

    monkeypatch.setattr(rb_writer, "commit_guarded", noting)
    return asked


def _query_write(cfg, sql: str) -> None:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        connection.execute(sql)
        connection.commit()
    finally:
        connection.close()


def _activate(cfg, name: str, genre_id: str = "901") -> None:
    """An active lookup row for ``name``, as rekordbox would make it."""
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        connection.execute(
            "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
            "VALUES (?, ?, 'v', 0, '2026-01-01', '2026-01-01')",
            (genre_id, name),
        )
        connection.commit()
    finally:
        connection.close()


def test_a_genre_with_no_lookup_row_is_planned_to_be_made_and_a_tombstone_is_not_its_row(
    machine, silence
):
    build(machine, silence, Track("10", MELODIC, MELODIC), Track("11", "", ""))
    _tombstone(machine, AFRO)
    plan = _plan(machine, AFRO, ["10", "11", "404"])
    assert plan.genre_row == "" and plan.mint and plan.shown_row == gs.MINT
    assert [(item.content_id, item.action, item.reason) for item in plan.items] == [
        ("10", gs.WRITE, ""), ("11", gs.WRITE, ""), ("404", gs.LEAVE, gs.ROW_GONE)
    ]
    assert genre_set_cli._payload(plan)["totals"]["genre_row"] == gs.MINT
    assert genre_set_cli._facts(plan)["genre_row"] == gs.MINT
    # THE ROW SHOWN IS DIGESTED: the same rows with the row made are another plan.
    _activate(machine, AFRO)
    found = _plan(machine, AFRO, ["10", "11", "404"])
    assert found.genre_row == "901" and not found.mint and found.digest != plan.digest


def test_nothing_is_to_be_made_when_no_row_is_to_link_it(machine, silence):
    build(machine, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    plan = _plan(machine, AFRO, ["10", "11", "404"], leave=("10", "11"))
    assert plan.writes == () and not plan.mint and plan.shown_row == gs.NO_ROW
    assert genre_set_cli._payload(plan)["totals"]["genre_row"] == gs.NO_ROW


def test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", OLD, ""),
          Track("12", "", OLD), Track("13", OLD, OLD))
    _tombstone(cfg, AFRO)
    before = _content(cfg)
    asked = _noting_commits(monkeypatch)

    _plan_, written = _apply(cfg, AFRO, ["10", "11", "12"])

    (made,) = _active_genre_rows(cfg, AFRO)
    assert made != "900" and written.minted == made
    assert _genre_rows(cfg, AFRO) == sorted([("900", 1), (made, 0)])
    assert asked == [(rb_writer.GENRE_TABLE,)]
    assert (written.written, written.read_back, written.wrong, written.moved) == (3, 3, (), ())
    assert [_genre_of(cfg, cid) for cid in ("10", "11", "12", "13")] == [AFRO, AFRO, AFRO, OLD]
    linked = _query(cfg, "SELECT ID, GenreID FROM djmdContent WHERE ID IN ('10','11','12')")
    assert {genre_id for _cid, genre_id in linked} == {made}
    # THE ROW IS MADE AS THE LANDING MAKES ONE: an unused id, the name, a UUID.
    ((name, uuid),) = _query(cfg, "SELECT Name, UUID FROM djmdGenre WHERE ID = ?", made)
    assert name == AFRO and len(uuid) == 36 and uuid != "u"
    after = _content(cfg)
    for content_id, row in before.items():
        changed = {
            column for column in row
            if after[content_id][column] != row[column]
            and column not in rb_writer.BOOKKEEPING_COLUMNS
        }
        assert changed == ({"GenreID"} if content_id in ("10", "11", "12") else set())
    # And a second run links the row it made and makes none.
    again = _plan(cfg, AFRO, ["10", "11", "12"])
    assert again.genre_row == made and not again.mint and again.writes == ()


def test_nothing_is_made_when_no_file_takes_the_genre(acknowledged, silence, monkeypatch):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", MELODIC, MELODIC))
    asked = _noting_commits(monkeypatch)
    monkeypatch.setattr(tags, "write_genre", lambda _path, _genre: False)

    plan, written = _apply(cfg, AFRO, ["10", "11"])

    assert plan.mint and written.minted == "" and written.written == 0
    assert written.files.failed == ("10", "11")
    assert _genre_rows(cfg, AFRO) == [] and asked == []
    assert [_genre_of(cfg, cid) for cid in ("10", "11")] == [MELODIC, MELODIC]


def test_nothing_is_made_for_a_file_alone(acknowledged, silence, monkeypatch):
    """A row linked to a tombstone of the name reads the genre already, so only
    its file is written, and no row is made for nothing to link."""
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    _tombstone(cfg, AFRO)
    _query_write(cfg, "UPDATE djmdContent SET GenreID = '900' WHERE ID = '10'")
    asked = _noting_commits(monkeypatch)

    plan, written = _apply(cfg, AFRO, ["10"])

    (item,) = plan.items
    assert item.file_writes and not item.row_writes and not plan.mint
    assert plan.shown_row == gs.NO_ROW
    assert written.files.read_back == ("10",) and written.minted == "" and asked == []
    assert _genre_rows(cfg, AFRO) == [("900", 1)]
    assert _tags_of(cfg, "10")["genre"] == AFRO


def test_a_row_made_by_another_hand_after_the_plan_refuses_before_any_file(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    plan = _plan(cfg, AFRO, ["10"])
    assert plan.mint
    _activate(cfg, AFRO)
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        with pytest.raises(CratekitError) as refused:
            gs.apply_set(
                cfg, db, plan, declared=active_taxonomy.load(cfg),
                analysis_roots=[Path(cfg.library.root) / "analysis"],
            )
    finally:
        rb_writer.close_db(db)
    assert refused.value.cause.reason == "decision-stale"
    assert "(901)" in refused.value.cause.message
    assert refused.value.cause.detail == {"genre": AFRO, "genre_row": "901"}
    assert [r for r in session.records(cfg) if r.workflow == gs.WORKFLOW] == []
    assert _active_genre_rows(cfg, AFRO) == ["901"]
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == MELODIC


def test_a_row_made_between_the_gate_and_the_apply_refuses_stale(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    argv = _verb(AFRO, "--row", "10")
    code, refused = drive(argv)
    assert refused["cause"]["detail"]["shown"]["genre_row"] == gs.MINT
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    _activate(cfg, AFRO)
    code, acted = drive(["--run", run_id, *argv])
    assert code != int(ExitCode.OK)
    assert acted["cause"]["reason"] in {"decision-stale", "decision-invalidated"}, acted
    assert _active_genre_rows(cfg, AFRO) == ["901"]
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == MELODIC


def test_a_row_made_after_the_gate_refuses_stale_on_the_write_handle(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    args = SimpleNamespace(rows=["10"], rows_from=None, playlist=None, leave=[])
    declared = active_taxonomy.load(cfg)
    approved = genre_set_cli.read_plan(cfg, declared, AFRO, args)
    _activate(cfg, AFRO)
    with pytest.raises(CratekitError) as refused:
        genre_set_cli.apply_plan(cfg, approved, declared, args)
    assert refused.value.cause.reason == "decision-stale"
    assert refused.value.cause.detail["moved"] == ["the lookup row for 'Afro House'"]
    assert "(0 named row(s) moved)" in refused.value.cause.message
    assert _active_genre_rows(cfg, AFRO) == ["901"]
    assert _genre_of(cfg, "10") == MELODIC and _tags_of(cfg, "10")["genre"] == MELODIC


def test_a_declined_gate_says_the_row_would_be_made_and_makes_none(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC))
    argv = _verb(AFRO, "--row", "10")
    _code, refused = drive(argv)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *argv])
    assert acted["outcome"] == "no_op"
    (first, *_rest) = acted["warnings"]
    assert first["code"] == genre_set_cli.GENRE_ROW_TO_MAKE
    assert "no genre row for 'Afro House', so the apply makes one" in first["message"]
    assert _genre_rows(cfg, AFRO) == [] and _genre_of(cfg, "10") == MELODIC


def test_the_restore_takes_the_made_row_back(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("10", MELODIC, MELODIC), Track("11", OLD, ""))
    code, acted, _refused = _two_acts(_verb(AFRO, "--row", "10", "--row", "11"))
    assert code == int(ExitCode.OK), acted
    (made,) = _active_genre_rows(cfg, AFRO)
    said = acted["warnings"][0]["message"]
    assert acted["warnings"][0]["code"] == genre_set_cli.GENRE_WRITTEN
    assert f"to the genre row {made} this run made for it" in said
    assert "takes the genre row away" in said
    assert genre_set_cli.GENRE_ROW_TO_MAKE not in [one["code"] for one in acted["warnings"]]
    (record,) = [one for one in session.records(cfg) if one.workflow == gs.WORKFLOW]

    restore_gate = "restore.run.confirm"
    verb = ["restore", "run", record.session_id]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, restore_gate, "restore", "--actor", "a-person"])
    code, restored = drive(["--run", run_id, *verb])

    assert code == int(ExitCode.OK), restored
    assert _genre_rows(cfg, AFRO) == []
    assert [_genre_of(cfg, cid) for cid in ("10", "11")] == [MELODIC, OLD]
    assert _tags_of(cfg, "10")["genre"] == MELODIC and _tags_of(cfg, "11")["genre"] is None
