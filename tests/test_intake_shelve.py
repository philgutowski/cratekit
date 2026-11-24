"""U154: ``crate intake shelve`` files an imported batch into the processed tree.

The rows shelved are ones the native landing made. D1 applies."""

from __future__ import annotations

import contextlib
import os
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, shelve, shelve_cli
from tests.cli_drive import drive
from tests.test_inbox_rotate import _two_acts as _gated
from tests.test_intake_land_hearts_native import cfg as cfg  # noqa: PLC0414 - the fixture
from tests.test_intake_land_native import BATCH, _answered, _execute, _query, _stage, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

GATE = shelve_cli.SHELVE_GATE
#: What ``BATCH``, ``2026-09-29_favourites``, files as.
FILED = "09_29_26 favourites"
FILES = ("One.flac", "Three.flac", "Two.flac")


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir


def _processed(cfg: config.Config) -> Path:
    # Spelled here, not through the engine, so the expectation is not the code agreeing with itself.
    return _music(cfg) / "Processed_Tracks"


def _rows(cfg: config.Config) -> list[tuple]:
    """(ID, FolderPath, FileNameL, rb_file_id, AnalysisDataPath) of every row the landing made."""
    return _query(cfg, f"SELECT ID, FolderPath, FileNameL, {rb_writer.FILE_ID_COLUMN}, "
                  "AnalysisDataPath FROM djmdContent WHERE Title LIKE '01A - 124 - %' "
                  "ORDER BY FileNameL")


def _land_three(cfg: config.Config, silence: Path, *, name: str = BATCH) -> list[tuple]:
    for file in FILES:
        _stage(cfg, silence, file)
    verb = ["intake", "land", "--name", name]
    acts = _two_acts(verb) if name == BATCH else _two_acts_of(verb, "intake.land.native")
    assert acts[0] == int(ExitCode.OK), acts[1]
    _as_landed_before_u164(cfg, name)
    rows = _rows(cfg)
    assert len(rows) >= 3
    return rows


def _as_landed_before_u164(cfg: config.Config, batch: str) -> None:
    """Put a batch where a landing put one before U164, ``Music/<batch>``, rows and all."""
    from cratekit.intake import batch_name as names
    when, said = shelve.filed_parts(batch, on=names.today())
    filed = shelve.processed_root(cfg) / f"{when.year}" / shelve.filed_name(when, said)
    os.rename(filed, _music(cfg) / batch)
    for emptied in (filed.parent, filed.parent.parent):
        if not any(emptied.iterdir()):
            emptied.rmdir()
    suffix = f"/{cfg.library.processed_dir}/{when.year}/{shelve.filed_name(when, said)}/"
    sql = "UPDATE djmdContent SET FolderPath = replace(FolderPath, ?, ?) WHERE FolderPath LIKE ?"
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(sql, (suffix, f"/{batch}/", f"%{suffix}%"))


def _two_acts_of(verb: list[str], gate: str) -> tuple[int, dict, dict]:
    return _gated(verb, gate=gate, answer="apply")


def _shelve(*args: str) -> list[str]:
    return ["intake", "shelve", *args]


def _records(cfg: config.Config, workflow: str) -> list[session.SessionRecord]:
    return [record for record in session.records(cfg) if record.workflow == workflow]


def _plant_ghost_row(cfg: config.Config, path: Path) -> None:
    """Point one row rekordbox made at ``path``, a folder nothing on disk holds."""
    _execute(cfg, "UPDATE djmdContent SET FolderPath = ? WHERE ID = (SELECT MIN(ID) FROM "
             "djmdContent WHERE Title NOT LIKE '01A - 124 - %')", str(path))


@contextmanager
def _open(cfg: config.Config):
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        yield db
    finally:
        rb_writer.close_db(db)


def test_a_path_write_is_refused_unless_the_shelve_policy_owning_only_it_is_registered():
    dirty = [(rb_writer.CONTENT_TABLE, [rb_writer.FOLDER_PATH_COLUMN])]
    refused = rb_writer.guard_violations([], dirty, [])
    assert refused and rb_writer.FOLDER_PATH_COLUMN in refused[0], refused
    with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
        assert rb_writer.guard_violations([], dirty, []) == []
    assert rb_writer.guard_violations([], dirty, []), "the policy outlived its commit"
    owned = {rb_writer.FOLDER_PATH_COLUMN: rb_writer.Ownership.OWNED}
    assert dict(rb_writer.SHELVE_POLICY.fields) == owned
    # The filed name is the hand convention, zero padded.
    assert shelve.filed_name(date(2026, 9, 3), "Favorites") == "09_03_26 Favorites"
    assert shelve.filed_name(date(2025, 12, 19), "labels") == "12_19_25 labels"


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
        # U235: a run's tail is four hex before it and sixteen since; a width between is neither.
        ("2026-11-07T164826Z-ce458ab7cceccb0b", (date(2026, 11, 7), "")),
        ("2026-11-07T164826Z-ce458ab7", None),
        ("rekordbox_djoid", None),
        ("Processed_Tracks", None),
        ("2026-13-01 Nope", None),
        ("2026-09-23T222241Z-xyzw", None),
    ],
)
def test_parse_name_reads_the_two_shapes_and_refuses_the_rest(batch, expected):
    assert shelve.parse_name(batch) == expected


def test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were(
        cfg, silence, monkeypatch):
    from cratekit.core import analysis_store
    from cratekit.core.cause import CratekitError
    from cratekit.intake import landing
    before = _land_three(cfg, silence)

    def untouched() -> None:
        assert sorted(p.name for p in (_music(cfg) / BATCH).iterdir()) == list(FILES)
        assert _rows(cfg) == before
    # THE REPORT names the target, every row and a digest, and moves nothing.
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
    untouched()
    assert not _processed(cfg).exists()
    assert _records(cfg, shelve.WORKFLOW) == []
    # UNDER --all, A FOLDER WITH A SUBFOLDER AND A NAME OF NEITHER SHAPE ARE SKIPPED.
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
    untouched()
    # THE GATE TAKES NO INLINE ANSWER.
    code, envelope = drive(["-d", f"{GATE}=apply", *_shelve(BATCH)])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    untouched()
    # AN ABORT moves nothing and writes nothing.
    code, envelope, _ = _gated(_shelve(BATCH), gate=GATE, answer="abort")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    untouched()
    assert _records(cfg, shelve.WORKFLOW) == []
    # A SUBJECT WITH A PATH PART is refused.
    code, envelope = drive(_shelve("--as", "Tidal/Favorites", BATCH))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["remediation"]["remedy"] == "fix-command-line"
    untouched()
    # A RUNNING REKORDBOX refuses before the plan is shown.
    running = rb_writer.rekordbox_running
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    code, envelope = drive(_shelve(BATCH))
    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED), envelope
    untouched()
    monkeypatch.setattr(rb_writer, "rekordbox_running", running)
    # A PROCESSED TREE ON ANOTHER DEVICE refuses before any plan.
    device_of, music = landing._device_of, _music(cfg)
    monkeypatch.setattr(landing, "_device_of", lambda path: 1 if Path(path) == music else 2)
    code, envelope = drive(_shelve("--report", BATCH))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "different device" in envelope["cause"]["message"]
    assert envelope["cause"]["remediation"]["remedy"] == "fix-config-values"
    assert _rows(cfg) == before
    monkeypatch.setattr(landing, "_device_of", device_of)
    # A FILE WITH NO ROW refuses the batch whole.
    unimported = _music(cfg) / BATCH / "Unimported.flac"
    shutil.copyfile(silence, unimported)
    code, envelope = drive(_shelve(BATCH))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "Unimported.flac" in envelope["cause"]["message"]
    assert "not been imported" in envelope["cause"]["message"]
    assert unimported.exists() and _rows(cfg) == before
    assert not _processed(cfg).exists()
    unimported.unlink()
    # A TARGET MADE AFTER THE APPROVAL is stale through the verb.
    run_id = _answered(_shelve(BATCH), GATE)[1]
    target = _processed(cfg) / "2026" / FILED
    target.mkdir(parents=True)
    code, envelope = drive(["--run", run_id, *_shelve(BATCH)])
    assert code == int(ExitCode.DECISION_STALE), envelope
    untouched()
    assert _records(cfg, shelve.WORKFLOW) == []
    target.rmdir()
    # And THE ENGINE refuses one made between its plan and its apply, in its own words.
    with _open(cfg) as db:
        planned = shelve.plan(cfg, db, [BATCH])
        target.mkdir()
        with pytest.raises(CratekitError) as caught:
            shelve.apply(cfg, db, planned, analysis_roots=analysis_store.watch_roots(cfg))
    assert caught.value.cause.reason == "decision-stale"
    assert "could not be written" not in caught.value.cause.message
    assert "exists now" in caught.value.cause.message
    untouched()
    target.rmdir()
    # A COMMIT THAT FAILS AFTER THE RENAME puts the folder back.
    def refuse_commit(db, **kwargs):
        raise RuntimeError("the disk went away")
    monkeypatch.setattr(rb_writer, "commit_guarded", refuse_commit)
    code, acted, _refused = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.INTERNAL), acted
    cause = acted["cause"]
    assert "renamed back" in cause["message"]
    assert cause["detail"]["renamed_back"] == [str(_music(cfg) / BATCH)]
    assert cause["detail"]["not_renamed_back"] == []
    untouched()
    assert not target.exists()


def test_a_plan_of_nothing_and_every_command_line_refusal_refuse_before_a_gate(cfg):
    (_music(cfg) / "rekordbox_djoid").mkdir()
    code, envelope = drive(_shelve("--all"))
    assert code == int(ExitCode.PRECONDITION), envelope
    assert "rekordbox_djoid" in envelope["cause"]["message"]
    assert _records(cfg, shelve.WORKFLOW) == []
    # THE COMMAND LINE REFUSALS name the flag.
    for args in ([], ["--all", BATCH], ["--as", "X", "--all"], ["--as", "X", "a", "b"], ["--as", " ", "a"]):
        code, envelope = drive(_shelve(*args))
        assert code == int(ExitCode.PRECONDITION), (args, envelope)
        assert envelope["cause"]["remediation"]["remedy"] == "fix-command-line", (args, envelope)


def test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over(cfg, silence):
    _land_three(cfg, silence)
    second = "2026-09-29 favourites"
    for file in FILES:
        _stage(cfg, silence, file)
    code, acted, _ = _two_acts_of(["intake", "land", "--name", second], "intake.land.native")
    assert code == int(ExitCode.OK), acted
    _as_landed_before_u164(cfg, second)
    (_processed(cfg) / "2026" / FILED).mkdir(parents=True)
    code, envelope = drive(_shelve("--report", "--all"))
    assert code == int(ExitCode.OK), envelope
    targets = {item["batch"]: item["to"] for item in envelope["data"]["items"]}
    # A space sorts before an underscore, so the second landing takes the first free suffix.
    assert targets == {
        second: str(_processed(cfg) / "2026" / f"{FILED} 2"),
        BATCH: str(_processed(cfg) / "2026" / f"{FILED} 3"),
    }


def test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken(
        cfg, silence):
    before = _land_three(cfg, silence)
    assert all(Path(row[1]).parent == _music(cfg) / BATCH for row in before)
    assert batch_name.taken(cfg, BATCH)
    # NOTHING UNDER THE PROCESSED TREE IS TOUCHED, nor a row under a folder differing in case.
    kept = _processed(cfg) / "2025" / "10_10_25"
    kept.mkdir(parents=True)
    (kept / "old.flac").write_bytes(b"")
    stamp = os.stat(kept).st_mtime_ns
    _plant_ghost_row(cfg, _processed(cfg) / "2026" / FILED.upper() / "ghost.flac")
    # A BATCH NAMED TWICE is planned once.
    code, acted, refused = _two_acts_of(_shelve(BATCH, BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    assert acted["data"]["totals"]["batches"] == 1
    assert not (_processed(cfg) / "2026" / f"{FILED} 2").exists()
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
    assert item["to"] == str(target)
    assert [row["to"] for row in item["rows"]] == [str(target / f) for f in FILES]
    assert acted["data"]["totals"]["shelved"] == 1 and acted["data"]["totals"]["rows"] == 3
    (record,) = _records(cfg, shelve.WORKFLOW)
    assert record.state is session.SessionState.CLOSED
    assert record.detail[shelve.SHELVED_KEY] == [{"batch": BATCH, "to": str(target), "rows": 3}]
    assert {change.tree: change.updated for change in record.change.trees} == {
        rb_writer.CONTENT_TABLE: 3
    }
    assert record.snapshot_path, "the capture the commit happened behind is not attached"
    assert (kept / "old.flac").exists() and os.stat(kept).st_mtime_ns == stamp
    assert sorted(p.name for p in _processed(cfg).iterdir()) == ["2025", "2026"]
    # THE GRID SUITES STILL SEE NO TEMPO on the moved rows.
    rows = _query(cfg, "SELECT BPM FROM djmdContent WHERE Title LIKE '01A - 124 - %'")
    assert rows and all(bpm in (None, 0) for (bpm,) in rows)
    # A SHELVED BATCH NAME STAYS TAKEN, so a landing that day takes the next.
    assert batch_name.taken(cfg, BATCH), "the folder is gone and the name reads free"
    assert batch_name.free(cfg, BATCH) == f"{BATCH} 2"
    assert not batch_name.taken(cfg, "2026-09-30 Favorites")
    # AN UNREADABLE SESSION RECORD makes the name rule refuse rather than read a name free.
    (session.log_dir(cfg) / "2026-10-26T00-00-00Z-dead.json").write_text("{not json")
    with pytest.raises(Exception) as caught:
        batch_name.free(cfg, BATCH)
    assert "cannot read" in str(caught.value)


@pytest.mark.parametrize(
    "run_named",
    [
        pytest.param("2026-09-23T222241Z-4773", id="four-hex-before-u235"),
        pytest.param("2026-09-23T222241Z-ce458ab7cceccb0b", id="sixteen-hex-since-u235"),
    ])
def test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given(
        cfg, silence, run_named):
    """A batch named for a run, as ``default_name`` spells one, at either width."""
    _land_three(cfg, silence, name=run_named)
    code, envelope = drive(_shelve("--report", run_named))
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / "09_23_26 Downloads")
    code, envelope = drive(_shelve("--report", "--as", "Bandcamp", run_named))
    assert code == int(ExitCode.OK), envelope
    (item,) = envelope["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / "09_23_26 Bandcamp")


def test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive(
        cfg, silence, monkeypatch):
    """Rows stored under a renamed volume's base drive are still the commit's own."""
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


def test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over(
        cfg, silence, monkeypatch):
    """A folder moved since leaves rows with nothing on disk, which no plan may choose."""
    before = _land_three(cfg, silence)
    ghost = _processed(cfg) / "2026" / FILED
    _plant_ghost_row(cfg, ghost / "ghost.flac")
    assert not ghost.exists()
    real = shelve._free_target
    def unguarded(root, name, planned, *, stored_dirs, spell):
        return real(root, name, planned, stored_dirs=frozenset(), spell=spell)
    monkeypatch.setattr(shelve, "_free_target", unguarded)
    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.REFUSED_BY_POLICY), acted
    assert "did not plan" in acted["cause"]["message"]
    assert acted["cause"]["detail"]["renamed_back"] == [str(_music(cfg) / BATCH)]
    assert (_music(cfg) / BATCH).is_dir() and _rows(cfg) == before
    assert not ghost.exists()
    monkeypatch.setattr(shelve, "_free_target", real)
    code, acted, _ = _two_acts_of(_shelve(BATCH), GATE)
    assert code == int(ExitCode.OK), acted
    (item,) = acted["data"]["items"]
    assert item["to"] == str(_processed(cfg) / "2026" / f"{FILED} 2")
    assert (_processed(cfg) / "2026" / f"{FILED} 2").is_dir()


@pytest.mark.parametrize(
    ("alter", "said"),
    [
        (lambda path, kept: (path + "x", kept), "not the planned"),
        (lambda path, kept: (path, ("other", *kept[1:])), "changed a column"),
    ], ids=["path", "kept-column"])
def test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column(
        cfg, silence, monkeypatch, alter, said):
    from cratekit.core import analysis_store
    from cratekit.core.cause import CratekitError
    _land_three(cfg, silence)
    real = shelve._select_rows
    calls: list[int] = []

    def tampered(db, content_ids):
        rows = real(db, content_ids)
        calls.append(1)
        if len(calls) < 2:
            return rows
        first = next(iter(rows))
        path, kept = rows[first]
        return {**rows, first: alter(path, kept)}
    monkeypatch.setattr(shelve, "_select_rows", tampered)
    with _open(cfg) as db, pytest.raises(CratekitError) as caught:
        planned = shelve.plan(cfg, db, [BATCH])
        shelve.apply(cfg, db, planned, analysis_roots=analysis_store.watch_roots(cfg))
    assert caught.value.cause.reason == "internal-error"
    assert said in caught.value.cause.message
