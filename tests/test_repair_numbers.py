"""U958: ``crate repair numbers`` numbers the product's playlists 1 to N again.

rekordbox's Remove from Playlist takes out the row numbered as the selected
row's shown position (sitting 107, A218), so a playlist whose live rows are not
1 to N loses the wrong track to a removal by hand. The engine on a disposable
library, then the verb through the command line for its gate and refusals.
"""

from __future__ import annotations

import pytest

from cratekit.core import active_taxonomy, analysis_store, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import numbers, numbers_cli
from tests.cli_drive import drive
from tests.test_favorites_backfill import _db, _sql
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414

VERB = ["repair", "numbers"]
GATE = numbers_cli.CONFIRM_GATE


@pytest.fixture
def cfg(acknowledged):
    """The acknowledged machine, its library holding eight live tracks."""
    _sql(
        acknowledged,
        "INSERT OR IGNORE INTO djmdContent (ID, Title, rb_local_deleted) VALUES (?, ?, 0)",
        *[(str(n), f"track {n}") for n in range(1, 9)],
    )
    return acknowledged


def _tracks(cfg, count: int) -> list[str]:
    rows = [str(row) for (row,) in _query(cfg, "SELECT ID FROM djmdContent ORDER BY ID")]
    assert len(rows) >= count, rows
    return rows[:count]


def _tree(cfg, *path: str, tracks: int = 4) -> str:
    """A playlist at ``path`` from the top, made folder by folder, holding ``tracks`` rows."""
    with _db(cfg) as handle:
        parent = None
        for name in path[:-1]:
            parent = rb_writer.ensure_folder(handle, name, parent)
        playlist = handle.create_playlist(path[-1], parent=parent)
        for row in _tracks(cfg, tracks):
            handle.add_to_playlist(playlist, row)
        return str(playlist.ID)


def _gap(cfg, playlist_id: str, *numbers_now: int, marked: int | None = None) -> None:
    """The playlist's rows given these numbers in row order, and one marked at ``marked``."""
    keys = [
        str(key)
        for (key,) in _query(
            cfg, "SELECT ID FROM djmdSongPlaylist WHERE PlaylistID = ? ORDER BY TrackNo, ID", playlist_id
        )
    ]
    _sql(cfg, "UPDATE djmdSongPlaylist SET TrackNo = ? WHERE ID = ?", *zip(numbers_now, keys))
    if marked is not None:
        _sql(
            cfg,
            "UPDATE djmdSongPlaylist SET rb_local_deleted = 1, TrackNo = ? WHERE ID = ?",
            (marked, keys[len(numbers_now)]),
        )


def _live(cfg, playlist_id: str) -> list[tuple[str, int]]:
    return [
        (str(content), int(number))
        for content, number in _query(
            cfg,
            "SELECT ContentID, TrackNo FROM djmdSongPlaylist WHERE PlaylistID = ? "
            "AND rb_local_deleted = 0 ORDER BY TrackNo, ID",
            playlist_id,
        )
    ]


def _memberships(cfg) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdSongPlaylist ORDER BY ID")


def _plan(cfg, named=()):
    with _db(cfg) as handle:
        return numbers.plan(handle, active_taxonomy.load(cfg), named=named)


def _apply(cfg, approved):
    with _db(cfg) as handle:
        return numbers.apply(
            cfg, handle, approved, declared=active_taxonomy.load(cfg),
            analysis_roots=analysis_store.watch_roots(cfg),
        )


def _tree_name(cfg) -> str:
    return active_taxonomy.load(cfg).tree.display


# ── the plan ──────────────────────────────────────────────────────────────────


def test_the_plan_lists_exactly_the_gapped_playlists_under_the_product_s_nodes(cfg):
    top = _tree_name(cfg)
    gapped = _tree(cfg, top, "Tech House", "High")
    whole = _tree(cfg, top, "Tech House", "Low")
    mine = _tree(cfg, "My Own", "Warmup")
    foreign = _tree(cfg, "DEADCA7", "Pushed")
    _gap(cfg, gapped, 1, 2, 4, marked=3)
    for other in (mine, foreign):
        _gap(cfg, other, 2, 5, 6)
    planned = _plan(cfg)
    assert [one.playlist_id for one in planned.items] == [gapped]
    (item,) = planned.items
    assert item.path == f"{top} / Tech House / High"
    assert (item.rows, item.lowest, item.highest, item.marked) == (3, 1, 4, 1)
    assert planned.scanned == 2 and whole not in {one.playlist_id for one in planned.items}


def test_a_playlist_named_joins_the_plan_and_an_unknown_name_refuses(cfg):
    mine = _tree(cfg, "My Own", "Warmup")
    _gap(cfg, mine, 2, 5, 6, 9)
    assert _plan(cfg).items == ()
    assert [one.playlist_id for one in _plan(cfg, named=["Warmup"]).items] == [mine]
    with pytest.raises(CratekitError, match="no live playlist"):
        _plan(cfg, named=["No Such Playlist"])
    foreign = _tree(cfg, "DEADCA7", "Pushed")
    _gap(cfg, foreign, 2, 5, 6, 9)
    with pytest.raises(CratekitError, match="'Pushed'"):
        _plan(cfg, named=["Pushed"])


def test_the_favourites_folder_and_a_twin_folder_are_in_scope(cfg):
    source = active_taxonomy.load(cfg).sub_class("favorites").signal_playlist
    month = _tree(cfg, "Favorites", "2026-10")
    _tree(cfg, "Favorites", source, tracks=1)
    twin = _tree(cfg, "Custom Playlists 2026", "Saturday")
    for one in (month, twin):
        _gap(cfg, one, 3, 4, 5, 6)
    assert {one.playlist_id for one in _plan(cfg).items} == {month, twin}


def test_the_digest_moves_when_a_planned_playlist_changes_and_not_otherwise(cfg):
    gapped = _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    _gap(cfg, gapped, 1, 3, 5, 7)
    first = _plan(cfg)
    assert _plan(cfg).digest == first.digest
    _gap(cfg, gapped, 1, 3, 5, 8)
    assert _plan(cfg).digest != first.digest


def test_a_playlist_whose_marker_cannot_be_read_is_held_and_never_written(cfg):
    held = _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    _gap(cfg, held, 1, 3, 5, 7)
    _sql(cfg, "UPDATE djmdSongPlaylist SET rb_local_deleted = NULL WHERE PlaylistID = ? AND TrackNo = 3", (held,))
    planned = _plan(cfg)
    assert planned.items == () and [one.playlist_id for one in planned.held] == [held]


# ── the write ─────────────────────────────────────────────────────────────────


def test_an_approved_plan_numbers_each_playlist_one_to_n_in_its_order_and_reads_it_back(cfg):
    top = _tree_name(cfg)
    gapped = _tree(cfg, top, "Tech House", "High")
    whole = _tree(cfg, top, "Tech House", "Low")
    _gap(cfg, gapped, 2, 5, 9, marked=5)
    before_order = [content for content, _n in _live(cfg, gapped)]
    untouched = [row for row in _memberships(cfg) if str(row[2]) == whole]
    written = _apply(cfg, _plan(cfg))
    assert written.disagreements == () and written.playlists == 1
    assert _live(cfg, gapped) == [(content, n) for n, content in enumerate(before_order, start=1)]
    assert _query(
        cfg, "SELECT TrackNo FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 1", gapped
    ) == [(0,)]
    assert [row for row in _memberships(cfg) if str(row[2]) == whole] == untouched
    (count,) = _query(cfg, "SELECT int_1 FROM agentRegistry WHERE registry_id = 'localUpdateCount'")[0]
    stamped = _query(
        cfg, "SELECT rb_local_usn FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0", gapped
    )
    assert {row[0] for row in stamped} == {count}
    assert written.moved == 4


def test_a_plan_that_moved_after_approval_refuses_and_writes_nothing(cfg):
    gapped = _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    _gap(cfg, gapped, 1, 3, 5, 7)
    approved = _plan(cfg)
    _gap(cfg, gapped, 1, 3, 5, 8)
    before = _memberships(cfg)
    with pytest.raises(CratekitError) as caught:
        _apply(cfg, approved)
    assert caught.value.cause.reason == "decision-stale"
    assert _memberships(cfg) == before


# ── the verb ──────────────────────────────────────────────────────────────────


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(cfg):
    gapped = _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    _gap(cfg, gapped, 1, 3, 5, 7)
    session.ack_path(cfg).unlink()
    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_the_verb_asks_then_writes_on_approval(cfg):
    gapped = _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    _gap(cfg, gapped, 1, 3, 5, 7)
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    (item,) = detail["shown"]["items"]
    assert (item["rows"], item["from"], item["to"]) == (4, 1, 7)
    assert _live(cfg, gapped)[-1][1] == 7
    decided, envelope = drive(["run", "decide", refused["run_id"], GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", refused["run_id"], *VERB])
    assert code == int(ExitCode.OK), acted
    assert [n for _c, n in _live(cfg, gapped)] == [1, 2, 3, 4]
    assert any(w["code"] == numbers_cli.NUMBERS_WRITTEN for w in acted["warnings"])


def test_nothing_gapped_asks_and_writes_nothing(cfg):
    _tree(cfg, _tree_name(cfg), "Deep House", "Mid")
    before = _memberships(cfg)
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    decided, _ = drive(["run", "decide", refused["run_id"], GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    code, acted = drive(["--run", refused["run_id"], *VERB])
    assert code == int(ExitCode.OK), acted
    assert any(w["code"] == numbers_cli.NOTHING_TO_WRITE for w in acted["warnings"])
    assert _memberships(cfg) == before


# ── the doctor row ────────────────────────────────────────────────────────────


def _doctor_row(cfg):
    from cratekit.cli import doctor, doctor_model
    from tests import doctor_machines

    probes = doctor_machines.green(numbers_survey=doctor_model._survey_numbers)
    return next(f for f in doctor.run(cfg, probes=probes).findings if f.key == "library.playlist_numbers")


def test_the_doctor_row_counts_a_fixture_s_gapped_playlists_off_a_copy(cfg):
    top = _tree_name(cfg)
    gapped = _tree(cfg, top, "Tech House", "High")
    _tree(cfg, top, "Tech House", "Low")
    clean = _doctor_row(cfg)
    assert clean.status.value == "ok" and "all 2 playlists" in clean.detail
    _gap(cfg, gapped, 1, 2, 4, marked=3)
    before = _memberships(cfg)
    found = _doctor_row(cfg)
    assert found.status.value == "info"
    assert found.detail.startswith("1 of 2 playlists under this product's nodes hold live rows not numbered 1 to N")
    assert f"'{top} / Tech House / High'" in found.detail and "crate repair numbers" in found.detail
    assert _memberships(cfg) == before


def test_the_doctor_s_two_machines_answer_the_row_opposite_ways(cfg):
    from cratekit.cli import doctor
    from tests import doctor_machines

    def row(probes):
        return next(f for f in doctor.run(cfg, probes=probes).findings if f.key == "library.playlist_numbers")

    assert row(doctor_machines.green()).status.value == "ok"
    hostile = row(doctor_machines.hostile())
    assert hostile.status.value != "ok" and "numbered 1 to N" in hostile.detail
    # The hostile machine's survey alone, rekordbox closed: sitting 107's playlist.
    gapped = row(doctor_machines.green(numbers_survey=doctor_machines.hostile().numbers_survey))
    assert gapped.status.value == "info" and gapped.detail.startswith("1 of 12 playlists")
