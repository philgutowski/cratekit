"""U154: ``crate intake shelve`` files an imported batch into the processed tree.

Every test here lands real files through the native landing first, so the rows
the shelve moves are rows the product made, then drives the shelve through the
real dispatcher against the same disposable database. The guard is pinned on
its own, from the pure whitelist, before any drive.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, shelve, shelve_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import BATCH, _query, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

GATE = shelve_cli.SHELVE_GATE
#: What ``BATCH``, ``2026-09-29_favourites``, files as.
FILED = "09_29_26 favourites"
FILES = ("One.flac", "Three.flac", "Two.flac")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir


def _processed(cfg: config.Config) -> Path:
    # Spelled here and not through the engine, so the expectation is not the
    # code under test agreeing with itself.
    return _music(cfg) / "Processed_Tracks"


def _rows(cfg: config.Config) -> list[tuple]:
    """(ID, FolderPath, FileNameL, rb_file_id, AnalysisDataPath) of every row the landing made."""
    return _query(
        cfg,
        f"SELECT ID, FolderPath, FileNameL, {rb_writer.FILE_ID_COLUMN}, AnalysisDataPath "
        f"FROM djmdContent WHERE Title LIKE '01A - 124 - %' ORDER BY FileNameL",
    )


def _land_three(cfg: config.Config, silence: Path, *, name: str = BATCH) -> list[tuple]:
    for file in FILES:
        _stage(cfg, silence, file)
    verb = ["intake", "land", "--name", name]
    code, acted, _refused = (
        _two_acts(verb) if name == BATCH else _two_acts_of(verb, "intake.land.native")
    )
    assert code == int(ExitCode.OK), acted
    rows = _rows(cfg)
    assert len(rows) >= 3
    return rows


def _two_acts_of(verb: list[str], gate: str) -> tuple[int, dict, dict]:
    """R34's two acts against ``gate``, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == gate and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _shelve(*args: str) -> list[str]:
    return ["intake", "shelve", *args]


def _records(cfg: config.Config, workflow: str) -> list[session.SessionRecord]:
    return [record for record in session.records(cfg) if record.workflow == workflow]


# ---------------------------------------------------------------------------
# The guard, before any drive
# ---------------------------------------------------------------------------


def test_a_path_write_is_refused_by_the_whitelist_unless_the_shelve_policy_is_registered():
    dirty = [(rb_writer.CONTENT_TABLE, [rb_writer.FOLDER_PATH_COLUMN])]
    refused = rb_writer.guard_violations([], dirty, [])
    assert refused and rb_writer.FOLDER_PATH_COLUMN in refused[0], refused
    with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
        assert rb_writer.guard_violations([], dirty, []) == []
    assert rb_writer.guard_violations([], dirty, []), "the policy outlived its commit"


def test_the_shelve_policy_owns_the_path_column_and_nothing_else():
    assert dict(rb_writer.SHELVE_POLICY.fields) == {
        rb_writer.FOLDER_PATH_COLUMN: rb_writer.Ownership.OWNED
    }


# ---------------------------------------------------------------------------
# Names, pure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("batch", "expected"),
    [
        (
            "2026-10-08 Tidal playlists and Favorites",
            (date(2026, 10, 8), "Tidal playlists and Favorites"),
        ),
        (
            "2026-10-09 Tidal playlists and Favorites 2",
            (date(2026, 10, 9), "Tidal playlists and Favorites 2"),
        ),
        ("2026-10-01-labels-1pct", (date(2026, 10, 1), "labels-1pct")),
        ("2026-09-29_favourites", (date(2026, 9, 29), "favourites")),
        ("2026-09-29", (date(2026, 9, 29), "")),
        ("2026-09-23T222241Z-4773", (date(2026, 9, 23), "")),
        ("rekordbox_djoid", None),
        ("Processed_Tracks", None),
        ("2026-13-01 Nope", None),
        ("2026-09-23T222241Z-xyzw", None),
    ],
)
def test_parse_name_reads_the_two_shapes_and_refuses_the_rest(batch, expected):
    assert shelve.parse_name(batch) == expected


def test_filed_name_is_the_hand_convention_zero_padded():
    assert shelve.filed_name(date(2026, 9, 3), "Favorites") == "09_03_26 Favorites"
    assert shelve.filed_name(date(2025, 12, 19), "labels") == "12_19_25 labels"


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def test_the_report_names_the_target_every_row_and_a_digest_and_moves_nothing(
    native_library, silence
):
    cfg, _root = native_library
    before = _land_three(cfg, silence)

    code, envelope = drive(_shelve("--report", BATCH))

    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["action"] == shelve_cli.SHELVE
    assert item["to"] == str(_processed(cfg) / "2026" / FILED)
    assert item["filed_on"] == "2026-09-29" and item["subject"] == "favourites"
    assert [row["file"] for row in item["rows"]] == list(FILES)
    for row in item["rows"]:
        assert row["from"] == str(_music(cfg) / BATCH / row["file"])
        assert row["to"] == str(_processed(cfg) / "2026" / FILED / row["file"])
    assert envelope["data"]["totals"] == {"count": 1, "batches": 1, "rows": 3, "skipped": 0}
    assert len(envelope["data"]["digest"]) == 16
    # Nothing moved, nothing written.
    assert sorted(p.name for p in (_music(cfg) / BATCH).iterdir()) == list(FILES)
    assert not _processed(cfg).exists()
    assert _rows(cfg) == before
    assert _records(cfg, shelve.WORKFLOW) == []


def test_a_batch_whose_file_has_no_row_is_refused_whole_and_nothing_moves(native_library, silence):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    shutil.copyfile(silence, _music(cfg) / BATCH / "Unimported.flac")

    code, envelope = drive(_shelve(BATCH))

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "Unimported.flac" in envelope["cause"]["message"]
    assert "not been imported" in envelope["cause"]["message"]
    assert (_music(cfg) / BATCH / "Unimported.flac").exists()
    assert _rows(cfg) == before
    assert not _processed(cfg).exists()


def test_a_folder_with_a_subfolder_and_a_name_of_neither_shape_are_skipped_under_all(
    native_library, silence
):
    cfg, _root = native_library
    _land_three(cfg, silence)
    (_music(cfg) / "rekordbox_djoid").mkdir()
    (_music(cfg) / "rekordbox_djoid" / "export.xml").write_text("<x/>")
    (_music(cfg) / "2026-09-28 Nested").mkdir()
    (_music(cfg) / "2026-09-28 Nested" / "inner").mkdir()

    code, envelope = drive(_shelve("--report", "--all"))

    assert code == int(ExitCode.OK), envelope
    by_batch = {item["batch"]: item for item in envelope["data"]["items"]}
    assert by_batch[BATCH]["action"] == shelve_cli.SHELVE
    assert by_batch["rekordbox_djoid"]["action"] == shelve_cli.SKIPPED
    assert "no date" in by_batch["rekordbox_djoid"]["why"]
    assert by_batch["2026-09-28 Nested"]["action"] == shelve_cli.SKIPPED
    assert "subfolder" in by_batch["2026-09-28 Nested"]["why"]
    assert envelope["data"]["totals"]["skipped"] == 2
    assert {w["code"] for w in envelope["warnings"]} == {shelve_cli.BATCH_SKIPPED}


def test_a_plan_of_nothing_refuses_before_a_gate_is_asked(native_library):
    cfg, _root = native_library
    (_music(cfg) / "rekordbox_djoid").mkdir()

    code, envelope = drive(_shelve("--all"))

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "rekordbox_djoid" in envelope["cause"]["message"]
    assert _records(cfg, shelve.WORKFLOW) == []


def test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over(
    native_library, silence
):
    cfg, _root = native_library
    _land_three(cfg, silence)
    second = "2026-09-29 favourites"
    for file in FILES:
        _stage(cfg, silence, file)
    code, acted, _ = _two_acts_of(["intake", "land", "--name", second], "intake.land.native")
    assert code == int(ExitCode.OK), acted
    (_processed(cfg) / "2026" / FILED).mkdir(parents=True)

    code, envelope = drive(_shelve("--report", "--all"))

    assert code == int(ExitCode.OK), envelope
    targets = {item["batch"]: item["to"] for item in envelope["data"]["items"]}
    # In listing order: a space sorts before an underscore, so the second
    # landing is planned first and takes the first free suffix.
    assert targets == {
        second: str(_processed(cfg) / "2026" / f"{FILED} 2"),
        BATCH: str(_processed(cfg) / "2026" / f"{FILED} 3"),
    }


def test_the_command_line_refusals_name_the_flag(native_library):
    for args in (
        [],
        ["--all", BATCH],
        ["--as", "X", "--all"],
        ["--as", "X", "a", "b"],
        ["--as", " ", "a"],
    ):
        code, envelope = drive(_shelve(*args))
        assert code == int(ExitCode.PRECONDITION), (args, envelope)
        assert envelope["cause"]["remediation"]["remedy"] == "fix-command-line", (args, envelope)


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def test_apply_moves_the_folder_rewrites_the_paths_and_keeps_every_other_column(
    native_library, silence
):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    assert all(Path(row[1]).parent == _music(cfg) / BATCH for row in before)

    code, acted, refused = _two_acts_of(_shelve(BATCH), GATE)

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["digest"] == acted["data"]["digest"]
    target = _processed(cfg) / "2026" / FILED
    assert sorted(p.name for p in target.iterdir()) == list(FILES)
    assert not (_music(cfg) / BATCH).exists()

    after = _rows(cfg)
    assert [row[0] for row in after] == [row[0] for row in before]
    for was, now in zip(before, after):
        assert now[1] == str(target / was[2]), "the path did not follow the folder"
        assert now[2:] == was[2:], "a column the shelve does not own changed"
        assert (target / now[2]).exists()

    (item,) = acted["data"]["items"]
    assert item["action"] == shelve_cli.SHELVED
    assert [row["to"] for row in item["rows"]] == [str(target / f) for f in FILES]
    assert acted["data"]["totals"]["shelved"] == 1 and acted["data"]["totals"]["rows"] == 3

    (record,) = _records(cfg, shelve.WORKFLOW)
    assert record.state is session.SessionState.CLOSED
    assert record.detail[shelve.SHELVED_KEY] == [{"batch": BATCH, "to": str(target), "rows": 3}]
    assert {change.tree: change.updated for change in record.change.trees} == {
        rb_writer.CONTENT_TABLE: 3
    }
    assert record.snapshot_path, "the capture the commit happened behind is not attached"


def test_a_shelved_batch_name_stays_taken_so_a_landing_that_day_takes_the_next(
    native_library, silence
):
    cfg, _root = native_library
    _land_three(cfg, silence)
    assert batch_name.taken(cfg, BATCH)
    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    assert not (_music(cfg) / BATCH).exists()

    assert batch_name.taken(cfg, BATCH), "the folder is gone and the name reads free"
    assert batch_name.free(cfg, BATCH) == f"{BATCH} 2"
    assert not batch_name.taken(cfg, "2026-09-30 Favorites")


def test_an_abort_moves_nothing_and_writes_nothing(native_library, silence):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    code, refused = drive(_shelve(BATCH))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    code, envelope = drive(["--run", run_id, *_shelve(BATCH)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert (_music(cfg) / BATCH).is_dir() and _rows(cfg) == before
    assert _records(cfg, shelve.WORKFLOW) == []


def test_the_gate_takes_no_inline_answer(native_library, silence):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    code, envelope = drive(["-d", f"{GATE}=apply", *_shelve(BATCH)])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert (_music(cfg) / BATCH).is_dir() and _rows(cfg) == before


def test_a_target_made_after_the_plan_is_stale_and_the_folder_stays(native_library, silence):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    code, refused = drive(_shelve(BATCH))
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    (_processed(cfg) / "2026" / FILED).mkdir(parents=True)

    code, envelope = drive(["--run", run_id, *_shelve(BATCH)])

    assert code == int(ExitCode.DECISION_STALE), envelope
    assert (_music(cfg) / BATCH).is_dir()
    assert sorted(p.name for p in (_music(cfg) / BATCH).iterdir()) == list(FILES)
    assert _rows(cfg) == before
    assert _records(cfg, shelve.WORKFLOW) == []


def test_a_commit_that_fails_after_the_rename_puts_the_folder_back(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    before = _land_three(cfg, silence)

    def refuse_commit(db, **kwargs):
        raise RuntimeError("the disk went away")

    monkeypatch.setattr(rb_writer, "commit_guarded", refuse_commit)

    code, acted, _refused = _two_acts_of(_shelve(BATCH), GATE)

    assert code == int(ExitCode.INTERNAL), acted
    cause = acted["cause"]
    assert "renamed back" in cause["message"]
    assert cause["detail"]["renamed_back"] == [str(_music(cfg) / BATCH)]
    assert cause["detail"]["not_renamed_back"] == []
    assert (_music(cfg) / BATCH).is_dir()
    assert sorted(p.name for p in (_music(cfg) / BATCH).iterdir()) == list(FILES)
    assert not (_processed(cfg) / "2026" / FILED).exists()
    assert _rows(cfg) == before


def test_a_running_rekordbox_refuses_before_the_plan_is_shown(native_library, silence, monkeypatch):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    code, envelope = drive(_shelve(BATCH))

    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED), envelope
    assert (_music(cfg) / BATCH).is_dir() and _rows(cfg) == before


def test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given(
    native_library, silence
):
    cfg, _root = native_library
    run_named = "2026-09-23T222241Z-4773"
    _land_three(cfg, silence, name=run_named)

    code, envelope = drive(_shelve("--report", run_named))
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / "09_23_26 Downloads")

    code, envelope = drive(_shelve("--report", "--as", "Bandcamp", run_named))
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / "09_23_26 Bandcamp")


def test_nothing_under_the_processed_tree_is_touched_by_a_shelve(native_library, silence):
    cfg, _root = native_library
    _land_three(cfg, silence)
    kept = _processed(cfg) / "2025" / "10_10_25"
    kept.mkdir(parents=True)
    (kept / "old.flac").write_bytes(b"")
    stamp = os.stat(kept).st_mtime_ns

    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)

    assert code == int(ExitCode.OK), acted
    assert (kept / "old.flac").exists() and os.stat(kept).st_mtime_ns == stamp
    assert sorted(p.name for p in _processed(cfg).iterdir()) == ["2025", "2026"]


def test_the_grid_suites_still_see_no_tempo_on_the_moved_rows(native_library, silence):
    cfg, _root = native_library
    _land_three(cfg, silence)
    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        rows = conn.execute(
            "SELECT BPM FROM djmdContent WHERE Title LIKE '01A - 124 - %'"
        ).fetchall()
    finally:
        conn.close()
    assert rows and all(bpm in (None, 0) for (bpm,) in rows)


def test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive(
    native_library, silence, monkeypatch
):
    """The defect the hunt found: rows are stored under ``djmdProperty``'s base
    drive when the volume was renamed, and a confinement check that reads under
    the mounted path finds none of its own rows and refuses a correct commit."""
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    base, current = str(Path(cfg.library.root).parent / "elsewhere"), str(cfg.library.root)
    monkeypatch.setattr(rb_writer, "recorded_db_drives", lambda db: (base, current))

    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)

    assert code == int(ExitCode.OK), acted
    target = _processed(cfg) / "2026" / FILED
    assert sorted(p.name for p in target.iterdir()) == list(FILES)
    stored_target = base + str(target)[len(current) :]
    for was, now in zip(before, _rows(cfg)):
        assert now[1] == f"{stored_target}/{was[2]}", "the row is not stored under the base drive"
        assert now[2:] == was[2:]


# ---------------------------------------------------------------------------
# Review round one
# ---------------------------------------------------------------------------


def test_a_target_free_on_disk_but_holding_rows_in_the_collection_is_passed_over(
    native_library, silence
):
    """A folder filed by hand and moved since leaves rows stored under its name
    with nothing on disk; a target chosen by disk alone would put this batch's
    rows beside them and the confinement check would refuse its own commit."""
    cfg, _root = native_library
    _land_three(cfg, silence)
    ghost = _processed(cfg) / "2026" / FILED
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute(
            "UPDATE djmdContent SET FolderPath = ? WHERE ID = (SELECT MIN(ID) FROM djmdContent "
            "WHERE Title NOT LIKE '01A - 124 - %')",
            (str(ghost / "ghost.flac"),),
        )
        conn.commit()
    finally:
        conn.close()
    assert not ghost.exists()

    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)

    assert code == int(ExitCode.OK), acted
    (item,) = acted["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / f"{FILED} 2")
    assert (_processed(cfg) / "2026" / f"{FILED} 2").is_dir()


def test_a_subject_with_a_path_part_is_refused(native_library, silence):
    cfg, _root = native_library
    before = _land_three(cfg, silence)
    code, envelope = drive(_shelve("--as", "Tidal/Favorites", BATCH))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["remediation"]["remedy"] == "fix-command-line"
    assert (_music(cfg) / BATCH).is_dir() and _rows(cfg) == before


def test_a_batch_named_twice_is_planned_once(native_library, silence):
    cfg, _root = native_library
    _land_three(cfg, silence)
    code, acted, _ = _two_acts_of(_shelve(BATCH, BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["batches"] == 1
    assert (_processed(cfg) / "2026" / FILED).is_dir()
    assert not (_processed(cfg) / "2026" / f"{FILED} 2").exists()


def test_a_processed_tree_on_another_device_refuses_before_any_plan(
    native_library, silence, monkeypatch
):
    from cratekit.intake import landing

    cfg, _root = native_library
    before = _land_three(cfg, silence)
    music = _music(cfg)
    monkeypatch.setattr(landing, "_device_of", lambda path: 1 if Path(path) == music else 2)
    code, envelope = drive(_shelve("--report", BATCH))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "different device" in envelope["cause"]["message"]
    assert envelope["cause"]["remediation"]["remedy"] == "fix-config-values"
    assert _rows(cfg) == before


def test_an_unreadable_session_record_makes_the_name_rule_refuse_rather_than_read_a_name_free(
    native_library, silence
):
    cfg, _root = native_library
    _land_three(cfg, silence)
    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    assert batch_name.taken(cfg, BATCH)
    (session.log_dir(cfg) / "2026-10-26T00-00-00Z-dead.json").write_text("{not json")

    with pytest.raises(Exception) as caught:
        batch_name.free(cfg, BATCH)
    assert "cannot read" in str(caught.value)
