"""U167: ``crate analyze check`` reads rekordbox's result for the landed rows.

Two halves. The engine's pure parts (the grid read from an analysis file's
bytes, the key on the Camelot wheel, the verdict over rows) are driven on
values built here. The verb is driven through the real dispatcher against the
disposable database the native landing suite builds: files are landed, and
rekordbox's analysis is simulated by setting the columns it writes, writing an
analysis file with a beat grid tag where the row says it is, and giving the
row a key.

The analysis files are built byte by byte from the published layout, and one
test parses them with pyrekordbox's own file reader as well, so the fixture is
known to be a file the binding reads and not only one this module reads.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import builtins
import io
import os
import sqlite3
import struct
from pathlib import Path

import pytest

from cratekit.analysis import check_cli
from cratekit.analysis import rekordbox_check as rc
from cratekit.core import analysis_store, config, rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import native
from tests.cli_drive import drive
from tests.test_inbox_analyzed import _content_id, _land
from tests.test_inbox_refill import offline as offline  # noqa: PLC0414
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
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

VERB = ["analyze", "check"]
FIVE = ("Alpha", "Bravo", "Charlie", "Delta", "Echo")

# ---------------------------------------------------------------------------
# Analysis files, byte by byte
# ---------------------------------------------------------------------------


def _tag(kind: bytes, header: bytes, body: bytes = b"") -> bytes:
    """One ANLZ tag: its kind, its header length, its whole length, then the rest."""
    return struct.pack(">4sII", kind, 12 + len(header), 12 + len(header) + len(body)) + header + body


def anlz(tempos: list[int] | None, *, before: bytes = b"") -> bytes:
    """An analysis file holding a beat grid with one tick per tempo, in hundredths.

    ``None`` writes a file with no grid tag at all. ``before`` is a tag placed
    ahead of the grid, so the walk has to step over one to find it.
    """
    tags = before
    if tempos is not None:
        ticks = b"".join(
            struct.pack(">HHI", index % 4 + 1, tempo, 500 * index)
            for index, tempo in enumerate(tempos)
        )
        tags += _tag(b"PQTZ", struct.pack(">III", 0, 0x80000, len(tempos)), ticks)
    header_length = 28
    return struct.pack(">4sII", b"PMAI", header_length, header_length + len(tags)) + bytes(16) + tags


#: A tag the walk must step over: a path tag carrying a short UTF-16 path.
PATH_TAG = _tag(b"PPTH", struct.pack(">I", 8), "/a.mp3".encode("utf-16-be")[:8])

CONSTANT_GRID = [12400] * 64
VARIABLE_GRID = [12400] * 30 + [12650] * 4 + [11980] * 30


def test_the_fixture_is_a_file_pyrekordbox_itself_reads():
    """The bytes built here parse with the binding's own reader, grid and all."""
    from pyrekordbox.anlz import AnlzFile

    parsed = AnlzFile.parse(anlz(VARIABLE_GRID, before=PATH_TAG))
    assert list(parsed.get_tag("PQTZ").get_bpms()) == [t / 100 for t in VARIABLE_GRID]


def test_a_constant_grid_reads_constant(tmp_path):
    path = tmp_path / "ANLZ0000.DAT"
    path.write_bytes(anlz(CONSTANT_GRID, before=PATH_TAG))

    grid = rc.read_grid(path)

    assert grid.state == rc.CONSTANT
    assert (grid.beats, grid.low, grid.high, grid.span) == (64, 12400, 12400, 0.0)


def test_a_variable_grid_reads_variable_with_its_span(tmp_path):
    path = tmp_path / "ANLZ0000.DAT"
    path.write_bytes(anlz(VARIABLE_GRID))

    grid = rc.read_grid(path)

    assert grid.state == rc.VARIABLE
    assert (grid.low, grid.high) == (11980, 12650)
    assert grid.span == pytest.approx(6.7)
    shown = grid.as_dict()
    assert (shown["tempo_low"], shown["tempo_high"]) == (119.8, 126.5)


def test_a_file_with_no_grid_tag_reads_absent_never_constant(tmp_path):
    path = tmp_path / "ANLZ0000.DAT"
    path.write_bytes(anlz(None, before=PATH_TAG))
    assert rc.read_grid(path).state == rc.ABSENT
    path.write_bytes(anlz([]))
    assert rc.read_grid(path).state == rc.ABSENT


def test_a_missing_file_reads_missing(tmp_path):
    grid = rc.read_grid(tmp_path / "ANLZ0000.DAT")
    assert grid.state == rc.MISSING and "no analysis file" in grid.why
    assert rc.read_grid(None).state == rc.MISSING


@pytest.mark.parametrize(
    "damage",
    [
        pytest.param(lambda data: data[:-3], id="cut-off-mid-write"),
        pytest.param(lambda data: b"PMAX" + data[4:], id="not-an-analysis-file"),
        pytest.param(lambda data: data[:10], id="shorter-than-a-header"),
        pytest.param(
            lambda data: data[:28] + struct.pack(">4sII", b"PQTZ", 24, 4000) + data[40:],
            id="a-tag-that-overruns",
        ),
        pytest.param(
            lambda data: data[:28] + struct.pack(">4sII", b"PQTZ", 24, 4) + data[40:],
            id="a-tag-shorter-than-its-header",
        ),
        pytest.param(
            lambda data: data[:44] + struct.pack(">I", 0x70000) + data[48:],
            id="a-grid-tag-that-will-not-parse",
        ),
    ],
)
def test_a_damaged_file_reads_unreadable_never_absent(tmp_path, damage):
    path = tmp_path / "ANLZ0000.DAT"
    path.write_bytes(damage(anlz(CONSTANT_GRID)))

    grid = rc.read_grid(path)

    assert grid.state == rc.UNREADABLE, grid
    assert str(path) in grid.why


# ---------------------------------------------------------------------------
# The key, on the Camelot wheel
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("head", "reference", "relation"),
    [
        ("8A", "08A", rc.KEY_EQUAL),
        ("08A", "9A", rc.KEY_ONE_STEP),
        ("8A", "7A", rc.KEY_ONE_STEP),
        ("12B", "1B", rc.KEY_ONE_STEP),
        ("1A", "12A", rc.KEY_ONE_STEP),
        ("8A", "8B", rc.KEY_ONE_STEP),
        ("8A", "9B", rc.KEY_FAR),
        ("8A", "10A", rc.KEY_FAR),
        ("8A", "2A", rc.KEY_FAR),
        (None, "8A", rc.KEY_UNKEYED),
        ("8A", None, rc.KEY_UNKEYED),
        ("8A", "Am", rc.KEY_UNKEYED),
    ],
)
def test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s(head, reference, relation):
    assert rc.key_relation(head, reference) == relation


def test_the_key_floor_is_the_recorded_rate_less_three_standard_errors():
    recorded = 158 / 299
    assert rc.key_floor(0) is None
    assert rc.key_floor(100) == pytest.approx(recorded - 3 * (recorded * (1 - recorded) / 100) ** 0.5)
    # A handful of rows can never read as suspect: the floor is below zero.
    assert rc.key_floor(5) < 0


# ---------------------------------------------------------------------------
# The verdict over rows
# ---------------------------------------------------------------------------


def _row(
    state: str = rc.ANALYSED,
    grid: str = rc.CONSTANT,
    *,
    relation: str = rc.KEY_EQUAL,
    dyn: bool = False,
    key: str | None = "08A",
) -> rc.Row:
    return rc.Row(
        content_id="c",
        title="t",
        state=state,
        grid=rc.Grid(state=grid if state == rc.ANALYSED else rc.NOT_READ),
        key=key,
        relation=relation,
        dyn=dyn,
    )


def _verdict(*rows: rc.Row) -> str:
    return rc.Check(scope=rc.Scope(kind=rc.SCOPE_ANALYZE, name="s", content_ids=()), rows=rows).verdict


def test_every_row_analysed_on_a_constant_grid_is_done():
    assert _verdict(_row(), _row(), _row(key=None, relation=rc.KEY_UNKEYED)) == rc.DONE


def test_a_row_not_analysed_is_waiting():
    assert _verdict(_row(), _row(state=rc.NOT_ANALYSED)) == rc.WAITING


@pytest.mark.parametrize("grid", [rc.VARIABLE, rc.ABSENT, rc.MISSING, rc.UNREADABLE])
def test_a_variable_or_unread_grid_is_suspect(grid):
    assert _verdict(_row(), _row(grid=grid)) == rc.SUSPECT


def test_a_variable_grid_on_a_row_marked_dyn_is_done():
    assert _verdict(_row(), _row(grid=rc.VARIABLE, dyn=True)) == rc.DONE


def test_an_unread_grid_on_a_row_marked_dyn_is_still_suspect():
    assert _verdict(_row(grid=rc.MISSING, dyn=True)) == rc.SUSPECT


def test_suspect_outranks_waiting():
    assert _verdict(_row(state=rc.NOT_ANALYSED), _row(grid=rc.VARIABLE)) == rc.SUSPECT


def test_keys_far_below_the_recorded_agreement_are_suspect_and_near_it_are_not():
    far = [_row(relation=rc.KEY_FAR) for _ in range(60)]
    # 20 equal in 80 is 25 percent, far below the floor for 80 (about 36).
    assert _verdict(*far, *[_row() for _ in range(20)]) == rc.SUSPECT
    # 40 equal in 80 is 50 percent, inside the floor.
    assert _verdict(*far[:40], *[_row() for _ in range(40)]) == rc.DONE
    # One step and unkeyed rows count as compared and as not compared.
    steps = [_row(relation=rc.KEY_ONE_STEP) for _ in range(40)]
    unkeyed = [_row(relation=rc.KEY_UNKEYED, key=None) for _ in range(500)]
    assert _verdict(*steps, *[_row() for _ in range(40)], *unkeyed) == rc.DONE


def test_no_row_or_only_gone_rows_is_nothing():
    assert _verdict() == rc.NOTHING
    assert _verdict(_row(state=rc.GONE)) == rc.NOTHING


# ---------------------------------------------------------------------------
# The verb, through the dispatcher
# ---------------------------------------------------------------------------


def _key_id(cfg: config.Config, scale: str) -> str:
    """The djmdKey row naming ``scale``, made when absent, as rekordbox keeps them."""
    found = _query(cfg, "SELECT ID FROM djmdKey WHERE ScaleName = ?", scale)
    if found:
        return str(found[0][0])
    key_id = f"k-{scale}"
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdKey (ID, ScaleName, Seq, rb_local_deleted, created_at, updated_at) "
            "VALUES (?, ?, 1, 0, '2026-10-31', '2026-10-31')",
            (key_id, scale),
        )
    conn.close()
    return key_id


def _visit(
    cfg: config.Config,
    stem: str,
    *,
    tempos: list[int] | None = CONSTANT_GRID,
    scale: str | None = "1A",
    write_file: bool = True,
) -> Path:
    """Simulate rekordbox analysing one row: its columns, its analysis file, its key."""
    content_id = _content_id(cfg, stem)
    stored = f"/PIONEER/USBANLZ/c0f/{content_id}/ANLZ0000.DAT"
    path = analysis_store.analysis_file(cfg, stored)
    assert path is not None
    if write_file:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(anlz(tempos, before=PATH_TAG))
    key_id = _key_id(cfg, scale) if scale else None
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "UPDATE djmdContent SET Analysed = 105, AnalysisDataPath = ?, KeyID = ? WHERE ID = ?",
            (stored, key_id, content_id),
        )
    conn.close()
    return path


def _mark_dyn(cfg: config.Config, *stems: str) -> None:
    """Give each row the dyn My Tag value U157 will write."""
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(
            "INSERT INTO djmdMyTag (ID, Seq, Name, Attribute, ParentID, rb_local_deleted, "
            "created_at, updated_at) VALUES ('t-dyn', 1, ?, 0, 't-root', 0, '2026-10-31', "
            "'2026-10-31')",
            (rc.DYN_VALUE,),
        )
        for index, stem in enumerate(stems):
            conn.execute(
                "INSERT INTO djmdSongMyTag (ID, MyTagID, ContentID, TrackNo, rb_local_deleted, "
                "created_at, updated_at) VALUES (?, 't-dyn', ?, 0, 0, '2026-10-31', "
                "'2026-10-31')",
                (f"sm-{index}", _content_id(cfg, stem)),
            )
    conn.close()


def _items(envelope: dict) -> dict[str, dict]:
    """Every row the check read, by its title's stem."""
    return {
        item["title"].rsplit(" - ", 1)[-1]: item for item in envelope["data"]["summary"]["items"]
    }


def test_rows_landed_and_not_yet_analysed_are_waiting_on_a_pending_action(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    _visit(cfg, "Alpha")

    code, envelope = drive(VERB)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["outcome"] == "pending"
    assert envelope["pending_human_action"]["verify_verb"] == "analyze.check"
    summary = envelope["data"]["summary"]
    assert summary["verdict"] == rc.WAITING
    assert (summary["scope"], summary["rows"]) == (rc.SCOPE_ANALYZE, 5)
    assert (summary["analysed"], summary["not_analysed"]) == (1, 4)
    items = _items(envelope)
    assert items["Alpha"]["grid"] == rc.CONSTANT
    assert items["Bravo"]["state"] == rc.NOT_ANALYSED and items["Bravo"]["grid"] == rc.NOT_READ


def test_every_row_analysed_right_is_done_and_exits_zero(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    for stem in FIVE:
        _visit(cfg, stem)

    code, envelope = drive(VERB)

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["verdict"] == rc.DONE
    assert summary["grids"][rc.CONSTANT] == 5
    # The staged head is 01A and rekordbox said 1A: equal, every one.
    assert summary["key_agreement"][rc.KEY_EQUAL] == 5
    assert summary["key_filled"] == 5
    statuses = {check["key"]: check["status"] for check in envelope["data"]["checks"]}
    assert statuses == {
        "check.scope": "info",
        "check.analysed": "ok",
        "check.grids": "ok",
        "check.key_column": "ok",
        "check.key_agreement": "ok",
    }


def test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    for stem in FIVE:
        _visit(cfg, stem, tempos=VARIABLE_GRID if stem == "Charlie" else CONSTANT_GRID)

    code, envelope = drive(VERB)

    assert code == int(ExitCode.LIBRARY_PREREQUISITE), envelope
    assert envelope["cause"]["reason"] == "analysis-suspect"
    assert "1 row(s) have variable grids" in envelope["cause"]["message"]
    assert envelope["data"]["summary"]["verdict"] == rc.SUSPECT
    charlie = _items(envelope)["Charlie"]
    assert (charlie["grid"], charlie["tempo_span"], charlie["suspect"]) == (rc.VARIABLE, 6.7, True)
    grids = [c for c in envelope["data"]["checks"] if c["key"] == "check.grids"]
    assert grids[0]["status"] == "fail" and "Charlie" in grids[0]["detail"]


def test_the_same_variable_grid_on_a_row_marked_dyn_is_done(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    for stem in FIVE:
        _visit(cfg, stem, tempos=VARIABLE_GRID if stem == "Charlie" else CONSTANT_GRID)
    _mark_dyn(cfg, "Charlie")

    code, envelope = drive(VERB)

    assert code == int(ExitCode.OK), envelope
    assert _items(envelope)["Charlie"]["dyn"] is True


def test_an_analysed_row_whose_file_is_missing_is_suspect(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    for stem in FIVE:
        _visit(cfg, stem, write_file=stem != "Delta")

    code, envelope = drive(VERB)

    assert code == int(ExitCode.LIBRARY_PREREQUISITE), envelope
    assert _items(envelope)["Delta"]["grid"] == rc.MISSING
    assert "could not read" in envelope["cause"]["message"]


def test_suspect_outranks_waiting_through_the_verb(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    _visit(cfg, "Alpha", tempos=VARIABLE_GRID)

    code, envelope = drive(VERB)

    assert code == int(ExitCode.LIBRARY_PREREQUISITE), envelope
    assert envelope["data"]["summary"]["not_analysed"] == 4


def test_title_keys_are_classified_equal_one_step_and_far(native_library, silence):
    cfg, _root = native_library
    for name, head in (("Alpha", "01A - 124"), ("Bravo", "02A - 124"), ("Charlie", "07B - 124")):
        _stage(cfg, silence, f"{name}.flac", head=head)
    code, acted, _refused = _land_acts(["intake", "land", "--name", "2026-10-31_keys"])
    assert code == int(ExitCode.OK), acted
    for stem in ("Alpha", "Bravo", "Charlie"):
        _visit(cfg, stem, scale="1A")

    code, envelope = drive(VERB)

    assert code == int(ExitCode.OK), envelope
    items = _items(envelope)
    assert {stem: items[stem]["key_agreement"] for stem in items} == {
        "Alpha": rc.KEY_EQUAL,
        "Bravo": rc.KEY_ONE_STEP,
        "Charlie": rc.KEY_FAR,
    }
    assert items["Charlie"]["head_key"] == "07B" and items["Charlie"]["key"] == "01A"


def test_a_pass_names_its_landing_s_rows_over_the_playlist(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    for name in ("Foxtrot", "Golf"):
        _stage(cfg, silence, f"{name}.flac")
    code, acted, _refused = _land_acts(
        ["intake", "land", "--name", "2026-10-31_two", "--pass", "pass-two"]
    )
    assert code == int(ExitCode.OK), acted
    for stem in ("Foxtrot", "Golf"):
        _visit(cfg, stem)

    code, envelope = drive([*VERB, "--pass", "pass-two"])

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["scope"], summary["scope_name"]) == (rc.SCOPE_PASS, "pass-two")
    assert sorted(_items(envelope)) == ["Foxtrot", "Golf"]


def test_a_landing_s_session_names_its_rows(native_library, silence):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    (landing,) = [r.session_id for r in native_records(cfg)]
    _visit(cfg, "Alpha")

    code, envelope = drive([*VERB, "--session", landing])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert envelope["data"]["summary"]["scope"] == rc.SCOPE_SESSION
    assert sorted(_items(envelope)) == sorted(FIVE)


def native_records(cfg: config.Config):
    from cratekit.core import session

    return [r for r in session.records(cfg) if r.workflow == native.WORKFLOW]


@pytest.mark.parametrize("flag", ["--pass", "--session"])
def test_a_landing_nothing_recorded_refuses_rather_than_reading_empty(native_library, silence, flag):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)

    code, envelope = drive([*VERB, flag, "no-such-landing"])

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "analysis-check-landing-unknown"


def test_an_empty_analyze_playlist_falls_to_every_row_not_analysed(native_library, silence):
    cfg, root_id = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    analyze = _query(
        cfg, "SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ?", native.ANALYZE, root_id
    )[0][0]
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute("UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ?", (analyze,))
    conn.close()
    for stem in FIVE[:3]:
        _visit(cfg, stem)

    code, envelope = drive(VERB)

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = envelope["data"]["summary"]
    assert summary["scope"] == rc.SCOPE_UNANALYSED
    assert {"Delta", "Echo"} <= set(_items(envelope))
    assert not {"Alpha", "Bravo", "Charlie"} & set(_items(envelope))
    scope = [c for c in envelope["data"]["checks"] if c["key"] == "check.scope"][0]
    assert "holds no row" in scope["detail"]


def test_nothing_in_scope_ends_no_op_and_says_nothing_was_checked(native_library, silence, monkeypatch):
    cfg, _root = native_library
    monkeypatch.setattr(rc, "_unanalysed", lambda db: ())

    code, envelope = drive(VERB)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["verdict"] == rc.NOTHING
    assert [w["code"] for w in envelope["warnings"]] == [check_cli.NOTHING_CHECKED]


def test_with_rekordbox_running_the_check_refuses_as_every_reader_does(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    code, envelope = drive(VERB)

    assert code == int(ExitCode.REKORDBOX_OPEN), envelope


def test_no_file_under_the_library_is_opened_for_writing(native_library, silence, monkeypatch):
    """Every open the check makes is watched: none writes, and no byte under the library moves."""
    cfg, _root = native_library
    _land(cfg, silence, "2026-10-31_five", FIVE)
    files = [_visit(cfg, stem) for stem in FIVE[:4]]
    _visit(cfg, "Echo", tempos=VARIABLE_GRID)
    library_root = Path(cfg.library.root)
    watched = [Path(cfg.library.db_path), *files, *analysis_store.watch_roots(cfg)]
    before = {
        path: path.read_bytes() for root in watched for path in ([root] if root.is_file() else root.rglob("*")) if path.is_file()
    }

    writes: list[tuple[str, str]] = []
    reads: list[str] = []
    real_open = io.open
    real_os_open = os.open

    def watching_open(file, mode="r", *args, **kwargs):
        if isinstance(file, (str, os.PathLike)):
            (writes if any(flag in mode for flag in "wax+") else reads).append(
                (str(file), mode) if any(flag in mode for flag in "wax+") else str(file)
            )
        return real_open(file, mode, *args, **kwargs)

    def watching_os_open(path, flags, *args, **kwargs):
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            writes.append((str(path), f"flags {flags:#o}"))
        return real_os_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", watching_open)
    monkeypatch.setattr(io, "open", watching_open)
    monkeypatch.setattr(os, "open", watching_os_open)
    try:
        code, envelope = drive(VERB)
    finally:
        monkeypatch.undo()

    assert code == int(ExitCode.LIBRARY_PREREQUISITE), envelope
    # The analysis files were opened, so the watch saw the reads it guards.
    assert {str(path) for path in files} <= set(reads)
    under_library = [
        (path, mode) for path, mode in writes if Path(path).resolve().is_relative_to(library_root.resolve())
    ]
    assert under_library == []
    after = {path: path.read_bytes() for path in before}
    assert after == before
