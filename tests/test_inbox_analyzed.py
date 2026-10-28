"""U166: every native landing fills INBOX / Analyze, and ``crate inbox analyzed`` empties it.

Driven against the disposable database the native landing suite builds. Files
are landed through the real dispatcher, rekordbox's analysis is simulated by
setting the two columns it writes, ``Analysed`` and ``AnalysisDataPath``, from
SQL, and the clear is driven over the result.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import sync_land
from cratekit.core import config, rb_writer, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import analyzed, analyzed_cli, land_cli, native, rotate
from tests.cli_drive import drive
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query, _stage
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import _two_acts as _land_acts
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
GATE = analyzed_cli.APPROVE_GATE
VERB = ["inbox", "analyzed"]

#: What rekordbox writes on a row it analysed, the shape and not a real path.
ANALYSIS_PATH = "/PIONEER/USBANLZ/a1b/0000-1111/ANLZ0000.DAT"


def _land(cfg: config.Config, silence: Path, batch: str, names: tuple[str, ...]) -> dict:
    for name in names:
        _stage(cfg, silence, f"{name}.flac")
    code, acted, _refused = _land_acts(["intake", "land", "--name", batch])
    assert code == int(ExitCode.OK), acted
    return acted


def _analyze_nodes(cfg: config.Config, root_id: str) -> list[tuple]:
    """(ID, Attribute, rb_local_deleted) of every node named Analyze under the root."""
    return _query(
        cfg,
        "SELECT ID, Attribute, rb_local_deleted FROM djmdPlaylist WHERE Name = ? AND ParentID = ?",
        native.ANALYZE,
        root_id,
    )


def _analyze_id(cfg: config.Config, root_id: str) -> str:
    (node,) = _analyze_nodes(cfg, root_id)
    assert int(node[1] or 0) == 0 and int(node[2] or 0) == 0, node
    return str(node[0])


def _titles(cfg: config.Config, playlist_id: str) -> list[str]:
    """The title stem of every live member, in track order."""
    rows = _query(
        cfg,
        "SELECT c.Title FROM djmdSongPlaylist s JOIN djmdContent c ON c.ID = s.ContentID "
        "WHERE s.PlaylistID = ? AND s.rb_local_deleted = 0 ORDER BY s.TrackNo",
        playlist_id,
    )
    return [str(row[0]).rsplit(" - ", 1)[-1] for row in rows]


def _content_id(cfg: config.Config, stem: str) -> str:
    ((content_id,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE Title LIKE ? AND rb_local_deleted = 0", f"% - {stem}"
    )
    return str(content_id)


def _analysed(cfg: config.Config, *stems: str, path: str | None = ANALYSIS_PATH) -> None:
    """Simulate rekordbox's analysis of each row: the two columns it writes."""
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        for stem in stems:
            conn.execute(
                "UPDATE djmdContent SET Analysed = 105, AnalysisDataPath = ? WHERE ID = ?",
                (path, _content_id(cfg, stem)),
            )
    conn.close()


def _clear_acts() -> tuple[int, dict, dict]:
    """R34's two acts against the clear's explicit gate, then the acting drive."""
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *VERB])
    return code, acted, refused


def _screen(refused: dict) -> dict:
    """The facts the landing's gate screen shows."""
    return refused["cause"]["detail"]["shown"]


FIVE = ("Alpha", "Bravo", "Charlie", "Delta", "Echo")
TWO = ("Foxtrot", "Golf")


# ---------------------------------------------------------------------------
# The landing fills one playlist
# ---------------------------------------------------------------------------


def test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root(
    native_library, silence
):
    cfg, root_id = native_library
    acted = _land(cfg, silence, "2026-10-28_five", FIVE)

    assert _titles(cfg, _analyze_id(cfg, root_id)) == list(FIVE)
    # THE WARNING NAMES THE ONE PLAYLIST, and no batch playlist.
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.AWAITING_ANALYSIS]
    assert f"{DECLARED.intake.display} / {native.ANALYZE}" in warning["message"]
    assert "2026-10-28_five" not in warning["message"]
    # The memberships are the intake tree's, counted on the record.
    (record,) = session.records(cfg)
    counted = {change.tree: change.created for change in record.change.trees}
    assert counted[DECLARED.intake.id] == 10


def test_a_second_landing_adds_its_own_beside_them_and_the_playlist_is_never_made_twice(
    native_library, silence
):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_five", FIVE)
    first = _analyze_id(cfg, root_id)
    for name in TWO:
        _stage(cfg, silence, f"{name}.flac")
    code, acted, refused = _land_acts(["intake", "land", "--name", "2026-10-28_two"])

    assert code == int(ExitCode.OK), acted
    assert _analyze_id(cfg, root_id) == first
    assert _titles(cfg, first) == [*FIVE, *TWO]
    # The second gate screen said the playlist was found, not made.
    assert _screen(refused)["analyze"].endswith(f"found (row {first})")


def test_the_gate_screen_names_analyze_and_whether_it_is_found_or_made(native_library, silence):
    cfg, root_id = native_library
    _stage(cfg, silence, "Alpha.flac")
    code, refused = drive(["intake", "land", "--name", "2026-10-28_one"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _screen(refused)["analyze"] == (
        f"{DECLARED.intake.display} / {native.ANALYZE}, every added row, made"
    )
    assert _analyze_nodes(cfg, root_id) == []


def test_a_row_the_collection_already_held_is_not_added_to_analyze(native_library, silence):
    """Only a row the landing created awaits analysis; a held row is rekordbox's already."""
    cfg, root_id = native_library
    _stage(cfg, silence, "Alpha.flac")
    _stage(cfg, silence, "Bravo.flac")
    held = str(Path(cfg.library.root) / cfg.library.music_dir / "2026-10-28_held" / "Bravo.flac")
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
            "updated_at) VALUES ('held-2', 'held', ?, 0, '2026-01-01', '2026-01-01')",
            (held,),
        )
    conn.close()

    code, acted, _refused = _land_acts(["intake", "land", "--name", "2026-10-28_held"])

    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["already present"] == 1
    assert _titles(cfg, _analyze_id(cfg, root_id)) == ["Alpha"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.AWAITING_ANALYSIS]
    assert warning["message"].startswith("1 row(s)")


def test_a_removed_or_smart_node_named_analyze_is_never_written_into(native_library, silence):
    cfg, root_id = native_library
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
            "created_at, updated_at) VALUES ('p-gone', 1, ?, 0, ?, 1, '2026-10-01', "
            "'2026-10-01')",
            (native.ANALYZE, root_id),
        )
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
            "created_at, updated_at) VALUES ('p-smart', 2, ?, 4, ?, 0, '2026-10-01', "
            "'2026-10-01')",
            (native.ANALYZE, root_id),
        )
    conn.close()
    _land(cfg, silence, "2026-10-28_five", FIVE)

    live = [node for node in _analyze_nodes(cfg, root_id) if node[0] not in ("p-gone", "p-smart")]
    assert len(live) == 1
    assert _titles(cfg, str(live[0][0])) == list(FIVE)
    assert _titles(cfg, "p-gone") == [] and _titles(cfg, "p-smart") == []


def test_the_rotation_leaves_analyze_alone(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_five", FIVE)
    analyze_id = _analyze_id(cfg, root_id)
    handle = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        plan = rotate.plan_rotation(
            cfg,
            handle,
            declared=DECLARED,
            registry=tree_registry.read(cfg),
            today=date(2027, 10, 28),
        )
    finally:
        rb_writer.close_db(handle)
    touched = {one.playlist_id for one in (*plan.moves, *plan.removals, *plan.kept)}
    assert analyze_id not in touched
    assert touched, "the batch a year old was not planned, so the probe proves nothing"


# ---------------------------------------------------------------------------
# The clear
# ---------------------------------------------------------------------------


def test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track(
    native_library, silence
):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_five", FIVE)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, "Alpha", "Charlie", "Echo")
    before = _query(cfg, "SELECT ID FROM djmdContent WHERE rb_local_deleted = 0 ORDER BY ID")
    batch = _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-10-28_five'")[0][0]

    code, acted, refused = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["digest"] == acted["data"]["digest"]
    assert _titles(cfg, analyze_id) == ["Bravo", "Delta"]
    assert acted["data"]["totals"]["clear"] == 3
    assert acted["data"]["totals"]["wait"] == 2
    assert acted["data"]["totals"]["removed"] == 3
    # NO TRACK LEFT THE COLLECTION, and the batch playlist still holds all five.
    after = _query(cfg, "SELECT ID FROM djmdContent WHERE rb_local_deleted = 0 ORDER BY ID")
    assert after == before
    assert _titles(cfg, str(batch)) == list(FIVE)
    # The removal is a soft delete: the rows stay, marked.
    marked = _query(
        cfg,
        "SELECT COUNT(*) FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 1",
        analyze_id,
    )
    assert marked == [(3,)]
    record = [r for r in session.records(cfg) if r.workflow == analyzed.WORKFLOW]
    assert len(record) == 1 and record[0].state is session.SessionState.CLOSED
    assert record[0].detail[analyzed.RECORD_KEY]["playlist"]["id"] == analyze_id
    assert sorted(record[0].detail[analyzed.RECORD_KEY]["removed"]) == sorted(
        _content_id(cfg, stem) for stem in ("Alpha", "Charlie", "Echo")
    )
    codes = [w["code"] for w in acted["warnings"]]
    assert analyzed_cli.WAITING in codes and analyzed_cli.CLEARED in codes


def test_a_row_marked_analysed_with_no_analysis_path_stays(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_five", FIVE)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, "Alpha", "Bravo")
    _analysed(cfg, "Charlie", path=None)
    _analysed(cfg, "Delta", path="  ")

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, analyze_id) == ["Charlie", "Delta", "Echo"]
    why = {item["title"].rsplit(" - ", 1)[-1]: item["why"] for item in acted["data"]["items"]}
    assert why["Charlie"] == analyzed.NO_ANALYSIS_PATH
    assert why["Delta"] == analyzed.NO_ANALYSIS_PATH
    assert why["Echo"] == analyzed.NOT_ANALYSED


def test_a_row_with_an_analysis_path_and_analysed_unset_stays(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_one", ("Alpha",))
    analyze_id = _analyze_id(cfg, root_id)
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "UPDATE djmdContent SET Analysed = 0, AnalysisDataPath = ? WHERE ID = ?",
            (ANALYSIS_PATH, _content_id(cfg, "Alpha")),
        )
    conn.close()

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _titles(cfg, analyze_id) == ["Alpha"]


def test_a_row_removed_from_the_collection_stays_and_is_named(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, *TWO)
    gone = _content_id(cfg, "Golf")
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        # rekordbox's own removal moves the library's update counter with it,
        # which the convergence check holds a removed row to.
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", (gone,))
        conn.execute(
            "UPDATE AgentRegistry SET int_1 = int_1 + 1 WHERE registry_id = 'localUpdateCount'"
        )
    conn.close()

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, analyze_id) == ["Golf"]
    (item,) = [one for one in acted["data"]["items"] if one["content_id"] == gone]
    assert item["action"] == analyzed.WAIT and item["why"] == analyzed.ROW_REMOVED


def test_nothing_analysed_still_asks_and_ends_no_op(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert analyzed_cli.NOTHING in [w["code"] for w in acted["warnings"]]
    assert _titles(cfg, analyze_id) == list(TWO)


def test_no_analyze_playlist_still_asks_creates_nothing_and_ends_no_op(native_library):
    cfg, root_id = native_library

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _analyze_nodes(cfg, root_id) == []


def test_a_second_clear_plans_nothing(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    _analysed(cfg, *TWO)
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK) and acted["data"]["totals"]["removed"] == 2

    code, again, _ = _clear_acts()

    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["data"]["totals"]["count"] == 0


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    code, refused = drive(VERB)

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing", refused


def test_an_intake_tree_on_the_bridge_is_refused_naming_the_cutover(acknowledged):
    code, refused = drive(VERB)

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "tree-unconverged", refused
    assert "tree cutover" in str(refused["cause"])


def test_an_analysis_finished_after_the_approval_is_refused_by_the_engine(
    native_library, silence
):
    """The engine's own stale check, with no gate in front (the gated verb solution)."""
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, "Foxtrot")
    plan = analyzed_cli.planned(cfg, DECLARED)
    assert plan.clears() == (_content_id(cfg, "Foxtrot"),)
    _analysed(cfg, "Golf")

    with pytest.raises(Exception) as caught:
        analyzed_cli.written(cfg, DECLARED, plan)

    assert getattr(caught.value, "cause", None) is not None
    assert caught.value.cause.reason == "decision-stale"
    assert _titles(cfg, analyze_id) == list(TWO)


def test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept():
    member = analyzed.Member
    plan = analyzed.AnalyzedPlan(
        tree_id="intake",
        root_id="r",
        root_name="INBOX",
        playlist_id="p",
        members=(
            member(content_id="1", title="a", action=analyzed.CLEAR),
            member(content_id="2", title="b", action=analyzed.WAIT, why=analyzed.NOT_ANALYSED),
        ),
    )
    analyzed.assert_read_back(
        plan, analyzed.Cleared(session_id="s", playlist_id="p", removed=("1",), read_back=("2",))
    )
    for read in ((), ("1", "2")):
        with pytest.raises(Exception) as caught:
            analyzed.assert_read_back(
                plan,
                analyzed.Cleared(session_id="s", playlist_id="p", removed=("1",), read_back=read),
            )
        assert caught.value.cause.reason == "session-committed-unverified"


def test_the_digest_names_every_row_and_its_answer():
    member = analyzed.Member
    base = analyzed.AnalyzedPlan(
        tree_id="intake",
        root_id="r",
        root_name="INBOX",
        playlist_id="p",
        members=(member(content_id="1", title="a", action=analyzed.CLEAR),),
    )
    waiting = analyzed.AnalyzedPlan(
        tree_id="intake",
        root_id="r",
        root_name="INBOX",
        playlist_id="p",
        members=(member(content_id="1", title="a", action=analyzed.WAIT, why="x"),),
    )
    assert analyzed.identity(base) != analyzed.identity(waiting)


# ---------------------------------------------------------------------------
# The name is reserved, and the guards the first review found unpinned
# ---------------------------------------------------------------------------


def test_the_playlist_is_inbox_slash_analyze_as_the_brief_names_it():
    """A literal, so a rename of the constant is a failure and not X equals X."""
    assert native.ANALYZE == "Analyze"
    assert sync_land.ANALYZE_PLAYLIST == f"{DECLARED.intake.display} / {native.ANALYZE}"
    assert sync_land.ANALYZE_PLAYLIST == "INBOX / Analyze"


def test_a_batch_named_analyze_is_refused_before_the_gate_and_nothing_moves(
    native_library, silence
):
    cfg, root_id = native_library
    _stage(cfg, silence, "Alpha.flac")

    code, refused = drive(["intake", "land", "--name", native.ANALYZE])

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "intake-list-unusable", refused
    assert "no batch may take it" in refused["cause"]["message"]
    assert _analyze_nodes(cfg, root_id) == []
    assert sorted(p.name for p in (Path(cfg.paths.download_staging)).glob("*.flac")) == [
        "Alpha.flac"
    ]


def test_an_account_playlist_named_analyze_lands_as_analyze_two():
    from cratekit.intake import batch_name

    assert batch_name.ANALYZE == native.ANALYZE
    assert batch_name.inbox_names(["Analyze", "Sunset"], (), batch="2026-10-28 x") == (
        "Analyze 2",
        "Sunset",
    )
    assert batch_name.inbox_names(["Analyze"], ("Analyze 2",), batch="b") == ("Analyze 3",)


def test_an_analyze_playlist_outside_the_root_is_never_written_into(native_library, silence):
    cfg, root_id = native_library
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
            "created_at, updated_at) VALUES ('p-elsewhere', 1, ?, 0, 'root', 0, '2026-10-01', "
            "'2026-10-01')",
            (native.ANALYZE,),
        )
    conn.close()

    _land(cfg, silence, "2026-10-28_two", TWO)

    assert _titles(cfg, "p-elsewhere") == []
    assert _titles(cfg, _analyze_id(cfg, root_id)) == list(TWO)


def test_analyze_removed_after_the_approval_is_refused_and_nothing_lands(
    native_library, silence
):
    """The digest names the playlist the plan found, so its removal is another plan."""
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_one", ("Alpha",))
    analyze_id = _analyze_id(cfg, root_id)
    _stage(cfg, silence, "Bravo.flac")
    verb = ["intake", "land", "--name", "2026-10-28_two"]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, land_cli.NATIVE_GATE, "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (analyze_id,))
        conn.execute(
            "UPDATE AgentRegistry SET int_1 = int_1 + 1 WHERE registry_id = 'localUpdateCount'"
        )
    conn.close()

    code, acted = drive(["--run", run_id, *verb])

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] in ("decision-stale", "decision-digest-mismatch"), acted
    live = [node for node in _analyze_nodes(cfg, root_id) if not int(node[2] or 0)]
    assert live == []


def test_a_track_held_twice_is_one_row_cleared_and_counted_once(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)
    foxtrot = _content_id(cfg, "Foxtrot")
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        # A second membership of the same track, the way the binding adds one.
        handle.add_to_playlist(handle.get_playlist(ID=analyze_id), foxtrot)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    _analysed(cfg, *TWO)

    code, acted, _ = _clear_acts()

    assert code == int(ExitCode.OK), acted
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["clear"], totals["removed"]) == (2, 2, 2)
    assert _titles(cfg, analyze_id) == []
    (record,) = [r for r in session.records(cfg) if r.workflow == analyzed.WORKFLOW]
    assert {c.tree: c.updated for c in record.change.trees} == {DECLARED.intake.id: 2}
