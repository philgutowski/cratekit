"""U166: every native landing fills INBOX / Analyze, and ``crate inbox analyzed`` empties it.

Files are landed through the real dispatcher on the native landing suite's
database, rekordbox's analysis is simulated by setting ``Analysed`` and
``AnalysisDataPath`` from SQL, and the clear is driven over the result. D1 applies.
"""

from __future__ import annotations

import contextlib
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import sync_land
from cratekit.core import config, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import analyzed, analyzed_cli, land_cli, native, rotate
from tests.cli_drive import drive
from tests.test_inbox_refill import offline as offline  # noqa: PLC0414
from tests.test_inbox_rotate import _handle
from tests.test_inbox_rotate import _two_acts as _gated
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _advance_usn, _music, _query, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
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
    sql = "UPDATE djmdContent SET Analysed = 105, AnalysisDataPath = ? WHERE ID = ?"
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        for stem in stems:
            conn.execute(sql, (path, _content_id(cfg, stem)))


def _clear_acts() -> tuple[int, dict, dict]:
    return _gated(VERB, gate=GATE, answer="apply")


def _screen(refused: dict) -> dict:
    """The facts the landing's gate screen shows."""
    return refused["cause"]["detail"]["shown"]


FIVE = ("Alpha", "Bravo", "Charlie", "Delta", "Echo")
TWO = ("Foxtrot", "Golf")


def test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it(
    native_library, silence
):
    cfg, root_id = native_library
    # THE GATE SCREEN NAMES ANALYZE, and says it is made, before anything is written.
    for name in FIVE:
        _stage(cfg, silence, f"{name}.flac")
    verb = ["intake", "land", "--name", "2026-10-28_five"]
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _screen(refused)["analyze"] == (
        f"{DECLARED.intake.display} / {native.ANALYZE}, every added row, made"
    )
    assert _analyze_nodes(cfg, root_id) == []
    code, acted, _refused = _land_acts(verb)
    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, _analyze_id(cfg, root_id)) == list(FIVE)
    # THE WARNING NAMES THE ONE PLAYLIST, and no batch playlist.
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.AWAITING_ANALYSIS]
    assert f"{DECLARED.intake.display} / {native.ANALYZE}" in warning["message"]
    assert "2026-10-28_five" not in warning["message"]
    # The memberships are the intake tree's, counted on the record.
    (record,) = session.records(cfg)
    counted = {change.tree: change.created for change in record.change.trees}
    assert counted[DECLARED.intake.id] == 10

    # A SECOND LANDING ADDS ITS OWN BESIDE THEM, and the playlist is never made twice.
    first = _analyze_id(cfg, root_id)
    for name in TWO:
        _stage(cfg, silence, f"{name}.flac")
    code, acted, refused = _land_acts(["intake", "land", "--name", "2026-10-28_two"])
    assert code == int(ExitCode.OK), acted
    assert _analyze_id(cfg, root_id) == first
    assert _titles(cfg, first) == [*FIVE, *TWO]
    assert _screen(refused)["analyze"].endswith(f"found (row {first})")

    # THE ROTATION LEAVES ANALYZE ALONE, a year on, while it plans the batches.
    with _handle(cfg) as handle:
        plan = rotate.plan_rotation(
            cfg, handle, declared=DECLARED, registry=tree_registry.read(cfg), today=date(2027, 10, 28)
        )
    touched = {one.playlist_id for one in (*plan.moves, *plan.removals, *plan.kept)}
    assert first not in touched
    assert touched, "the batch a year old was not planned, so the probe proves nothing"


def test_a_row_the_collection_already_held_is_not_added_to_analyze(native_library, silence):
    """Only a row the landing created awaits analysis; a held row is rekordbox's already."""
    cfg, root_id = native_library
    # Landed into again by its own name (U164), so the batch goes back to its
    # filed folder, where the collection holds a row for one of the files.
    verb = ["intake", "land", "--name", "2026-10-28_held"]
    _stage(cfg, silence, "Zero.flac")
    code, first, _refused = _land_acts(verb)
    assert code == int(ExitCode.OK), first
    _stage(cfg, silence, "Alpha.flac")
    _stage(cfg, silence, "Bravo.flac")
    held = str(_music(cfg, "2026-10-28_held") / "Bravo.flac")
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
            "updated_at) VALUES ('held-2', 'held', ?, 0, '2026-01-01', '2026-01-01')",
            (held,),
        )
        _advance_usn(conn)
    conn.close()
    code, acted, _refused = _land_acts(verb)
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["already present"] == 1
    assert _titles(cfg, _analyze_id(cfg, root_id)) == ["Zero", "Alpha"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == land_cli.AWAITING_ANALYSIS]
    assert warning["message"].startswith("1 row(s)")


def test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into(native_library, silence):
    cfg, root_id = native_library
    insert = (
        "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
        "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, '2026-10-01', '2026-10-01')"
    )
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(insert, ("p-gone", 1, native.ANALYZE, 0, root_id, 1))
        conn.execute(insert, ("p-smart", 2, native.ANALYZE, 4, root_id, 0))
        conn.execute(insert, ("p-elsewhere", 1, native.ANALYZE, 0, "root", 0))
    _land(cfg, silence, "2026-10-28_five", FIVE)
    live = [node for node in _analyze_nodes(cfg, root_id) if node[0] not in ("p-gone", "p-smart")]
    assert len(live) == 1
    assert _titles(cfg, str(live[0][0])) == list(FIVE)
    assert _titles(cfg, "p-gone") == [] and _titles(cfg, "p-smart") == []
    assert _titles(cfg, "p-elsewhere") == []


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


def test_a_row_with_no_analysis_path_or_analysed_unset_stays(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_five", FIVE)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, "Alpha", "Bravo")
    _analysed(cfg, "Charlie", path=None)
    _analysed(cfg, "Delta", path="  ")
    # An analysis path with ``Analysed`` unset is not analysed either.
    sql = "UPDATE djmdContent SET Analysed = 0, AnalysisDataPath = ? WHERE ID = ?"
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(sql, (ANALYSIS_PATH, _content_id(cfg, "Echo")))
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, analyze_id) == ["Charlie", "Delta", "Echo"]
    why = {item["title"].rsplit(" - ", 1)[-1]: item["why"] for item in acted["data"]["items"]}
    assert why["Charlie"] == analyzed.NO_ANALYSIS_PATH
    assert why["Delta"] == analyzed.NO_ANALYSIS_PATH
    assert why["Echo"] == analyzed.NOT_ANALYSED


def test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named(
    native_library, silence
):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)
    _analysed(cfg, *TWO)
    gone = _content_id(cfg, "Golf")
    # rekordbox's own changes move the library's update counter with them,
    # which the convergence check holds them to.
    bump = "UPDATE AgentRegistry SET int_1 = int_1 + 1 WHERE registry_id = 'localUpdateCount'"
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", (gone,))
        conn.execute(bump)
        # A membership nothing in the collection answers: never cleared on a guess.
        conn.execute(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, rb_local_deleted, "
            "created_at, updated_at) VALUES ('sp-ghost', ?, 'ghost', 9, 0, '2026-10-28', "
            "'2026-10-28')",
            (analyze_id,),
        )
        conn.execute(bump)
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, analyze_id) == ["Golf"]
    (item,) = [one for one in acted["data"]["items"] if one["content_id"] == gone]
    assert item["action"] == analyzed.WAIT and item["why"] == analyzed.ROW_REMOVED
    (ghost,) = [item for item in acted["data"]["items"] if item["content_id"] == "ghost"]
    assert ghost["action"] == analyzed.WAIT and ghost["why"] == analyzed.NO_ROW
    assert _query(
        cfg, "SELECT rb_local_deleted FROM djmdSongPlaylist WHERE ID = 'sp-ghost'"
    ) == [(0,)]
    assert acted["data"]["totals"]["removed"] == 1


def test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing(
    native_library, silence
):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    analyze_id = _analyze_id(cfg, root_id)

    # NOTHING ANALYSED STILL ASKS and ends no_op.
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert analyzed_cli.NOTHING in [w["code"] for w in acted["warnings"]]
    assert _titles(cfg, analyze_id) == list(TWO)

    # AN ANALYSIS FINISHED AFTER THE APPROVAL is refused by the engine's own
    # stale check, with no gate in front.
    _analysed(cfg, "Foxtrot")
    plan = analyzed_cli.planned(cfg, DECLARED)
    assert plan.clears() == (_content_id(cfg, "Foxtrot"),)
    _analysed(cfg, "Golf")
    with pytest.raises(Exception) as caught:
        analyzed_cli.written(cfg, DECLARED, plan)
    assert getattr(caught.value, "cause", None) is not None
    assert caught.value.cause.reason == "decision-stale"
    assert _titles(cfg, analyze_id) == list(TWO)

    # A TRACK HELD TWICE is one row cleared and counted once.
    with _handle(cfg) as handle:
        # A second membership of the same track, the way the binding adds one.
        handle.add_to_playlist(handle.get_playlist(ID=analyze_id), _content_id(cfg, "Foxtrot"))
        handle.session.commit()
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK), acted
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["clear"], totals["removed"]) == (2, 2, 2)
    assert _titles(cfg, analyze_id) == []
    (record,) = [r for r in session.records(cfg) if r.workflow == analyzed.WORKFLOW]
    assert {c.tree: c.updated for c in record.change.trees} == {DECLARED.intake.id: 2}

    # A SECOND CLEAR PLANS NOTHING.
    code, again, _ = _clear_acts()
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert again["data"]["totals"]["count"] == 0


def test_no_analyze_playlist_still_asks_and_a_batch_named_analyze_is_refused(native_library, silence):
    cfg, root_id = native_library
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _analyze_nodes(cfg, root_id) == []

    # A BATCH NAMED ANALYZE is refused before the gate and nothing moves.
    _stage(cfg, silence, "Alpha.flac")
    code, refused = drive(["intake", "land", "--name", native.ANALYZE])
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "intake-list-unusable", refused
    assert "no batch may take it" in refused["cause"]["message"]
    assert _analyze_nodes(cfg, root_id) == []
    staged = Path(cfg.paths.download_staging).glob("*.flac")
    assert sorted(p.name for p in staged) == ["Alpha.flac"]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    code, refused = drive(VERB)
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing", refused


def test_an_intake_tree_on_the_bridge_is_refused_naming_the_cutover(acknowledged):
    code, refused = drive(VERB)
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "tree-unconverged", refused
    assert "tree cutover" in str(refused["cause"])


def _clear_plan(*members: analyzed.Member) -> analyzed.AnalyzedPlan:
    return analyzed.AnalyzedPlan("intake", "r", "INBOX", "p", members)


def test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept():
    plan = _clear_plan(
        analyzed.Member("1", "a", analyzed.CLEAR),
        analyzed.Member("2", "b", analyzed.WAIT, why=analyzed.NOT_ANALYSED),
    )
    analyzed.assert_read_back(plan, analyzed.Cleared("s", "p", ("1",), ("2",)))
    for read in ((), ("1", "2")):
        with pytest.raises(Exception) as caught:
            analyzed.assert_read_back(plan, analyzed.Cleared("s", "p", ("1",), read))
        assert caught.value.cause.reason == "session-committed-unverified"


def test_the_digest_names_every_row_and_its_answer():
    base = _clear_plan(analyzed.Member("1", "a", analyzed.CLEAR))
    waiting = _clear_plan(analyzed.Member("1", "a", analyzed.WAIT, why="x"))
    assert analyzed.identity(base) != analyzed.identity(waiting)


def test_the_playlist_is_inbox_slash_analyze_as_the_brief_names_it():
    """A literal, so a rename of the constant is a failure and not X equals X."""
    assert native.ANALYZE == "Analyze"
    assert sync_land.ANALYZE_PLAYLIST == f"{DECLARED.intake.display} / {native.ANALYZE}"
    assert sync_land.ANALYZE_PLAYLIST == "INBOX / Analyze"


def test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze():
    """U175: the date at the end of every account playlist's name keeps it off ``Analyze``."""
    from cratekit.intake import batch_name
    assert batch_name.ANALYZE == native.ANALYZE
    named = batch_name.inbox_names(["Analyze", "Sunset"], ("Analyze",), batch="2026-10-28 x")
    assert named == ("Analyze 2026-10-03", "Sunset 2026-10-03")
    assert batch_name.ANALYZE not in named
    assert batch_name.inbox_names(["Analyze"], ("Analyze 2026-10-03",), batch="b") == (
        "Analyze 2026-10-03 2",
    )


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


def test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name(
    native_library, silence, offline
):
    """The second review's drive: an account playlist named Analyze, every track owned."""
    from tests.test_inbox_refill import _two_acts as _refill_acts
    from tests.test_intake_land_account_playlists_native import PASS, _owned, swept
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1", "Held2"))
    analyze_id = _analyze_id(cfg, root_id)
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "UPDATE djmdContent SET Analysed = 105, AnalysisDataPath = ? WHERE Title LIKE 'Held%'",
            (ANALYSIS_PATH,),
        )
    conn.close()
    code, acted, _ = _clear_acts()
    assert code == int(ExitCode.OK) and acted["data"]["totals"]["removed"] == 2, acted
    swept(cfg, {"pl-a": (native.ANALYZE, ("Held1", "Held2"))})
    drive(["intake", "land", "--pass", PASS])
    code, refused = drive(["inbox", "refill", "--pass", PASS])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    items = refused["cause"]["detail"]["shown"]["items"]
    assert [item["action"] for item in items] == ["unfound"], items
    code, acted, _ = _refill_acts(["inbox", "refill", "--pass", PASS])
    assert code == int(ExitCode.OK), acted
    assert _titles(cfg, analyze_id) == []


def test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says():
    """A landing named Analyze before the name was reserved left a record naming it."""
    from types import SimpleNamespace
    row = SimpleNamespace(ID="q", Name=native.ANALYZE, Attribute=0, rb_local_deleted=0)
    # A handle holding no membership, since a left playlist is counted (U214).
    empty = SimpleNamespace(get_playlist_songs=lambda **_where: [])
    found = rotate._classify(
        None,
        empty,
        row,
        place="INBOX",
        found=rotate.Landings(by_id={"q": date(2025, 1, 1)}, by_name={}, unreadable=0),
        today=date(2026, 10, 28),
    )
    assert isinstance(found, rotate.Left) and found.kind == "analyze", found


def test_a_removal_that_did_not_take_is_refused_after_the_commit(
    native_library, silence, monkeypatch
):
    """The first mutation table's zero: the verb holds its answer to the read back."""
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-28_two", TWO)
    _analysed(cfg, *TWO)
    # A writer that answers the ids and marks nothing, so the commit holds no change.
    monkeypatch.setattr(
        analyzed.rb_writer, "remove_memberships", lambda db, playlist, ids: list(ids)
    )
    code, acted, _ = _clear_acts()
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "session-committed-unverified", acted
    assert _titles(cfg, _analyze_id(cfg, root_id)) == list(TWO)
