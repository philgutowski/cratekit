"""R-816: ``crate tag rows`` writes a row's genre from its file, and nothing else.

Three layers, in the order they are trusted. The plan, against a disposable
database and real tagged containers, one row per outcome. The apply, with every
column of every row compared across the write. Then the verb through the real
dispatcher: the two acts R34 requires, the acknowledgment, the stale digest,
the second run, and the genre report the residual names as its symptom.

The too coarse word is taken from the shipped taxonomy. The other genre words
are spelled here, because what is under test is that the row comes to carry
whatever the file says, and the library's lookup rows are whatever this file
seeds.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
import hashlib
import os
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import collection
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import gates, registry
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    locations,
    preflight,
    rb_writer,
    session,
    tags,
    taxonomy,
)
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import retag, rows, rows_cli
from cratekit.write import metadata, metadata_cli
from tests._containers import synth_container
from tests.cli_drive import drive, drive_human
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row

DECLARED = taxonomy.default_taxonomy()
VERB = ["tag", "rows"]
GATE = rows_cli.CONFIRM_GATE

OLD = "Progressive / Melodic"
MELODIC = "Melodic House"
PROGRESSIVE = "Progressive House"
DEEP = "Deep House"
#: A word the shipped taxonomy calls too coarse to be a final genre.
COARSE = next(word for word in DECLARED.fallback.too_coarse_as_source if word)
#: A word the library has no lookup row for.
UNSEEN = "Zydeco"

#: The genre lookup rows every library here carries, by name.
LOOKUPS = (OLD, MELODIC, PROGRESSIVE, DEEP, COARSE)

#: The two rows ``_build_disposable_database`` seeds. They record no path.
BASELINE = 2

#: What a file can be besides a tagged container.
ABSENT = object()
UNREADABLE = object()


@dataclass(frozen=True)
class Track:
    """One row to seed and the file it names.

    ``file`` is the genre the file carries, an empty string for a readable
    file with no genre, :data:`ABSENT` for no file at all, or
    :data:`UNREADABLE` for bytes no tag library opens. ``recorded`` overrides
    the location the row records.
    """

    content_id: str
    row: str
    file: object
    deleted: bool = False
    recorded: str | None = None


def _genre_ids() -> dict[str, str]:
    return {name: str(ordinal) for ordinal, name in enumerate(LOOKUPS, start=100)}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _field_policies():
    """The policy registry is process wide and the apply registers into it."""
    rb_writer.reset_field_policies()
    yield
    rb_writer.reset_field_policies()


@pytest.fixture(autouse=True)
def _reader_cache():
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the metadata verb patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One synthesized container, copied per track. The encoder runs once."""
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set up machine with every module on and no acknowledgment yet."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(
        valid_data(
            root,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(cfg)
    config.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


@pytest.fixture
def acknowledged(machine) -> config.Config:
    session.record_acknowledgment(machine, terminal=lambda: True)
    return machine


def _music(cfg: config.Config) -> Path:
    return Path(cfg.library.root) / "Music"


def _file(cfg: config.Config, content_id: str) -> Path:
    return _music(cfg) / f"track-{content_id}.flac"


def _write_file(cfg: config.Config, silence: Path, track: Track) -> None:
    path = _file(cfg, track.content_id)
    if track.file is ABSENT:
        return
    if track.file is UNREADABLE:
        path.write_bytes(b"\x00" * 64)
        return
    shutil.copyfile(silence, path)
    if track.file:
        assert tags.write_tags(path, {"genre": str(track.file)})


def build(cfg: config.Config, silence: Path, *tracks: Track) -> Path:
    """A disposable database holding ``tracks``, each with the file it names."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    db_path = Path(cfg.library.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    _build_disposable_database(db_path, with_tag_category=False)
    ids = _genre_ids()
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as db_session:
        for name, genre_id in ids.items():
            db_session.add(_row(tables.DjmdGenre, ID=genre_id, Name=name))
        for track in tracks:
            _write_file(cfg, silence, track)
            recorded = track.recorded
            if recorded is None:
                recorded = locations.location_url(_file(cfg, track.content_id))
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=track.content_id,
                    Title=f"track {track.content_id}",
                    GenreID=ids.get(track.row),
                    BPM=12400,
                    Rating=3,
                    Commnt="a comment a person typed",
                    rb_local_deleted=1 if track.deleted else 0,
                    FolderPath=recorded,
                )
            )
        db_session.commit()
    engine.dispose()
    collection.reset_cache()
    return db_path


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()


def _genre_of(cfg: config.Config, content_id: str) -> str:
    """The word one row carries, read with plain SQL and no binding."""
    ((name,),) = _query(
        cfg,
        "SELECT g.Name FROM djmdContent c LEFT JOIN djmdGenre g ON g.ID = c.GenreID "
        "WHERE c.ID = ?",
        content_id,
    )
    return name or ""


def _content(cfg: config.Config) -> dict[str, dict]:
    """Every column of every content row, by identifier."""
    connection = sqlite3.connect(cfg.library.db_path)
    connection.row_factory = sqlite3.Row
    try:
        found = connection.execute("SELECT * FROM djmdContent").fetchall()
        return {str(row["ID"]): dict(row) for row in found}
    finally:
        connection.close()


def _files(cfg: config.Config) -> dict[str, str]:
    """Every file under the music folder, by its bytes."""
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(_music(cfg).iterdir())
        if path.is_file()
    }


def _planned(cfg: config.Config, leave: tuple[str, ...] = ()) -> rows.RowsPlan:
    db = rb_writer.open_db(cfg.library.db_path, unlock=False, cfg=cfg)
    try:
        return rows.plan_rows(cfg, db, active_taxonomy.load(cfg), leave=leave)
    finally:
        rb_writer.close_db(db)


def _counts(plan: rows.RowsPlan, **expected: int) -> None:
    """Every outcome's count, the unnamed ones held to zero."""
    wanted = dict.fromkeys(rows.OUTCOMES, 0)
    wanted.update({name.replace("_", "-"): count for name, count in expected.items()})
    assert dict(plan.counts) == wanted


def _two_acts(verb: list[str] = VERB) -> tuple[int, dict, dict]:
    """R34's two acts against the explicit gate, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


# ═══════════════════════════════════════════════════════════════════════════
# 1. The plan: one outcome per row
# ═══════════════════════════════════════════════════════════════════════════


def test_a_stale_row_is_planned_with_the_rows_word_and_the_files(machine, silence):
    build(machine, silence, Track("10", OLD, MELODIC))
    plan = _planned(machine)
    (item,) = plan.items
    assert (item.content_id, item.row, item.file, item.action) == ("10", OLD, MELODIC, rows.WRITE)
    assert item.genre_id == _genre_ids()[MELODIC] and item.reason == ""
    assert item.path == str(_file(machine, "10"))
    _counts(plan, write=1, no_path=BASELINE)


def test_a_blank_row_with_a_file_genre_is_planned(machine, silence):
    build(machine, silence, Track("10", "", MELODIC))
    (item,) = _planned(machine).items
    assert (item.row, item.file, item.action) == ("", MELODIC, rows.WRITE)


def test_a_row_with_a_genre_and_a_blank_file_is_left_alone_and_counted(machine, silence):
    build(machine, silence, Track("10", DEEP, ""))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, file_blank=1, no_path=BASELINE)


def test_a_row_and_file_that_agree_are_not_in_the_plan(machine, silence):
    build(machine, silence, Track("10", DEEP, DEEP))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, agree=1, no_path=BASELINE)


def test_a_too_coarse_file_does_not_replace_a_specific_row(machine, silence):
    build(machine, silence, Track("10", DEEP, COARSE))
    plan = _planned(machine)
    (item,) = plan.items
    assert (item.action, item.reason, item.genre_id) == (rows.LEAVE, rows.FILE_TOO_COARSE, "")
    assert (item.row, item.file) == (DEEP, COARSE)
    assert plan.writes == () and plan.changes.changes == ()
    _counts(plan, file_too_coarse=1, no_path=BASELINE)


def test_a_too_coarse_file_is_written_onto_a_blank_row(machine, silence):
    """The row loses nothing and now agrees with its file."""
    build(machine, silence, Track("10", "", COARSE))
    (item,) = _planned(machine).items
    assert (item.action, item.file) == (rows.WRITE, COARSE)


def test_a_file_word_with_no_lookup_row_is_left_alone_and_never_minted(machine, silence):
    build(machine, silence, Track("10", DEEP, UNSEEN))
    plan = _planned(machine)
    (item,) = plan.items
    assert (item.action, item.reason) == (rows.LEAVE, rows.GENRE_UNKNOWN)
    _counts(plan, genre_unknown=1, no_path=BASELINE)
    assert _query(machine, "SELECT COUNT(*) FROM djmdGenre WHERE Name = ?", UNSEEN) == [(0,)]


def test_a_file_that_is_gone_is_counted_missing(machine, silence):
    build(machine, silence, Track("10", DEEP, ABSENT))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, file_missing=1, no_path=BASELINE)


def test_a_file_no_tag_library_opens_is_unreadable_and_not_blank(machine, silence):
    build(machine, silence, Track("10", DEEP, UNREADABLE))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, file_unreadable=1, no_path=BASELINE)


def test_a_row_recorded_under_no_prefix_rule_is_counted_unmapped(machine, silence, tmp_path):
    elsewhere = tmp_path / "another-volume" / "Music" / "track.flac"
    build(machine, silence, Track("10", DEEP, ABSENT, recorded=str(elsewhere)))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, path_unmapped=1, no_path=BASELINE)


def test_a_row_naming_another_host_is_counted_as_having_no_path(machine, silence):
    build(machine, silence, Track("10", DEEP, ABSENT, recorded="file://elsewhere/Music/track.flac"))
    _counts(_planned(machine), no_path=1 + BASELINE)


def test_a_removed_row_is_neither_planned_nor_counted(machine, silence):
    build(machine, silence, Track("10", OLD, MELODIC, deleted=True))
    plan = _planned(machine)
    assert plan.items == ()
    _counts(plan, no_path=BASELINE)


def test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order(
    machine, silence
):
    build(
        machine,
        silence,
        Track("31", OLD, PROGRESSIVE),
        Track("30", OLD, MELODIC),
        Track("32", "", MELODIC),
        Track("33", DEEP, DEEP),
        Track("34", DEEP, COARSE),
        Track("35", DEEP, UNSEEN),
        Track("36", DEEP, ""),
        Track("37", DEEP, ABSENT),
        Track("38", DEEP, UNREADABLE),
        Track("39", OLD, MELODIC, deleted=True),
    )
    plan = _planned(machine)
    assert [item.content_id for item in plan.items] == ["30", "31", "32", "34", "35"]
    assert [item.content_id for item in plan.writes] == ["30", "31", "32"]
    _counts(
        plan,
        write=3,
        agree=1,
        file_too_coarse=1,
        genre_unknown=1,
        file_blank=1,
        file_missing=1,
        file_unreadable=1,
        no_path=BASELINE,
    )
    assert plan.rows == 9 + BASELINE
    assert plan.unread == 2 + BASELINE


def test_the_pairs_are_the_writes_counted_largest_first(machine, silence):
    build(
        machine,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", OLD, MELODIC),
        Track("32", OLD, PROGRESSIVE),
        Track("33", "", MELODIC),
        Track("34", DEEP, COARSE),
    )
    plan = _planned(machine)
    assert plan.pairs() == [
        {"row": OLD, "file": MELODIC, "rows": 2},
        {"row": "", "file": MELODIC, "rows": 1},
        {"row": OLD, "file": PROGRESSIVE, "rows": 1},
    ]
    assert plan.pairs(limit=1) == [{"row": OLD, "file": MELODIC, "rows": 2}]
    assert rows.NAMED_PAIRS == 5


# ── what the review found: the walk is total, and a row can be held ────────


def test_a_file_whose_bytes_are_not_here_is_counted_and_never_opened(
    machine, silence, monkeypatch
):
    """Opening an evicted file is a download. The probe answers without one."""
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", OLD, MELODIC))
    evicted = _file(machine, "31")
    real_probe = adopt_scan.probe_readability
    monkeypatch.setattr(
        adopt_scan,
        "probe_readability",
        lambda path: adopt_scan.Readability.ONLINE_ONLY if path == evicted else real_probe(path),
    )
    real_read = tags.read_tags_checked
    opened: list[Path] = []

    def reading(path, fields):
        opened.append(path)
        return real_read(path, fields)

    monkeypatch.setattr(tags, "read_tags_checked", reading)
    plan = _planned(machine)
    assert [item.content_id for item in plan.items] == ["30"]
    _counts(plan, write=1, file_online_only=1, no_path=BASELINE)
    assert opened == [_file(machine, "30")]
    assert plan.unread == 1 + BASELINE


def test_a_file_under_a_directory_this_account_cannot_enter_does_not_end_the_walk(
    machine, silence
):
    """``Path.is_file`` raises PermissionError there and took the whole plan."""
    locked = _music(machine) / "locked"
    locked.mkdir()
    shutil.copyfile(silence, locked / "track.flac")
    build(
        machine,
        silence,
        Track("30", OLD, ABSENT, recorded=locations.location_url(locked / "track.flac")),
        Track("31", OLD, MELODIC),
    )
    os.chmod(locked, 0)
    try:
        plan = _planned(machine)
    finally:
        os.chmod(locked, 0o700)
    assert [item.content_id for item in plan.items] == ["31"]
    _counts(plan, write=1, file_unreadable=1, no_path=BASELINE)


def test_an_answer_the_probe_gains_later_is_counted_unreadable(machine, silence, monkeypatch):
    build(machine, silence, Track("30", OLD, MELODIC))
    monkeypatch.setattr(adopt_scan, "probe_readability", lambda path: "something-new")
    _counts(_planned(machine), file_unreadable=1, no_path=BASELINE)


def test_a_file_holding_two_genres_is_left_alone_and_both_are_shown(machine, silence):
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", DEEP, MELODIC))
    assert tags.write_tag_values(_file(machine, "30"), "genre", [MELODIC, PROGRESSIVE])
    # The first value agreeing is agreement: nothing is written either way.
    assert tags.write_tag_values(_file(machine, "31"), "genre", [DEEP, MELODIC])
    plan = _planned(machine)
    (item,) = plan.items
    assert (item.content_id, item.action, item.reason) == ("30", rows.LEAVE, rows.FILE_MULTI_VALUED)
    assert item.file == f"{MELODIC}; {PROGRESSIVE}" and item.genre_id == ""
    assert plan.changes.changes == ()
    _counts(plan, file_multi_valued=1, agree=1, no_path=BASELINE)


def test_a_row_a_person_holds_out_is_listed_and_left(machine, silence):
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", DEEP, PROGRESSIVE))
    free = _planned(machine)
    assert [item.action for item in free.items] == [rows.WRITE, rows.WRITE]

    plan = _planned(machine, leave=("31",))
    assert [(item.content_id, item.action, item.reason) for item in plan.items] == [
        ("30", rows.WRITE, ""),
        ("31", rows.LEAVE, rows.HELD_OUT),
    ]
    assert [change.content_id for change in plan.changes.changes] == ["30"]
    assert plan.leave_unmatched == ()
    _counts(plan, write=1, held_out=1, no_path=BASELINE)
    assert plan.digest != free.digest


def test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested(
    machine, silence
):
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", DEEP, DEEP))
    free = _planned(machine)
    plan = _planned(machine, leave=("31", "999"))
    assert plan.leave_unmatched == ("31", "999")
    assert [item.digested() for item in plan.items] == [item.digested() for item in free.items]
    assert dict(plan.counts) == dict(free.counts)
    assert plan.digest != free.digest


def test_a_majority_under_no_prefix_rule_is_read_off_the_walk(machine, silence, tmp_path):
    away = tmp_path / "another-volume" / "Music"
    build(
        machine,
        silence,
        Track("30", OLD, MELODIC),
        *(Track(str(40 + n), OLD, ABSENT, recorded=str(away / f"{n}.flac")) for n in range(3)),
    )
    plan = _planned(machine)
    # Three of six: exactly half is not a majority.
    assert (plan.rows, plan.counts[rows.PATH_UNMAPPED]) == (6, 3)
    assert not plan.majority_unmapped
    assert sum(plan.unmapped_prefixes.values()) == 3


def test_each_distinct_file_word_is_resolved_once(machine, silence, monkeypatch):
    build(
        machine,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", OLD, MELODIC),
        Track("32", "", MELODIC),
        Track("33", OLD, PROGRESSIVE),
        Track("34", OLD, UNSEEN),
        Track("35", DEEP, UNSEEN),
    )
    real = metadata.resolve_genre_id
    asked: list[str] = []

    def counting(db, name):
        asked.append(name)
        return real(db, name)

    monkeypatch.setattr(metadata, "resolve_genre_id", counting)
    plan = _planned(machine)
    assert sorted(asked) == sorted([MELODIC, PROGRESSIVE, UNSEEN])
    _counts(plan, write=4, genre_unknown=2, no_path=BASELINE)
    assert plan.unknown_words() == [(UNSEEN, 2)]


# ── the digest ─────────────────────────────────────────────────────────────


def test_the_digest_is_the_same_for_the_same_library_on_another_copy(
    machine, silence, tmp_path
):
    """A rehearsal on a copy of the database digests equal to the live plan."""
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", DEEP, DEEP))
    live = _planned(machine)

    copy = tmp_path / "rehearsal" / "master.db"
    copy.parent.mkdir()
    shutil.copyfile(machine.library.db_path, copy)
    db = rb_writer.open_db(copy, unlock=False, cfg=machine)
    try:
        rehearsed = rows.plan_rows(machine, db, DECLARED)
    finally:
        rb_writer.close_db(db)
    assert rehearsed.digest == live.digest
    assert str(tmp_path) not in str([item.digested() for item in live.items])


def test_the_digest_moves_when_one_files_genre_moves(machine, silence):
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", OLD, MELODIC))
    before = _planned(machine).digest
    assert _planned(machine).digest == before
    assert tags.write_tags(_file(machine, "31"), {"genre": PROGRESSIVE})
    assert _planned(machine).digest != before


def test_the_digest_moves_when_only_a_count_moves(machine, silence):
    """A file that stops being readable changes no item and still moves it."""
    build(machine, silence, Track("30", OLD, MELODIC), Track("31", DEEP, DEEP))
    before = _planned(machine)
    _file(machine, "31").unlink()
    after = _planned(machine)
    assert [item.digested() for item in after.items] == [item.digested() for item in before.items]
    assert after.digest != before.digest


# ═══════════════════════════════════════════════════════════════════════════
# 2. The apply and the read back
# ═══════════════════════════════════════════════════════════════════════════


def _apply(cfg: config.Config) -> tuple[rows.RowsPlan, rows.Written]:
    db = rb_writer.open_db(cfg.library.db_path, require_closed=True, unlock=False, cfg=cfg)
    try:
        plan = rows.plan_rows(cfg, db, active_taxonomy.load(cfg))
        return plan, rows.apply_rows(
            cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def test_the_apply_writes_the_genre_and_no_other_column_of_any_row(acknowledged, silence):
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", "", PROGRESSIVE),
        Track("32", DEEP, DEEP),
        Track("33", DEEP, COARSE),
        Track("34", DEEP, ""),
    )
    before, files = _content(cfg), _files(cfg)

    plan, written = _apply(cfg)

    assert (written.written, written.read_back, written.wrong, written.moved) == (2, 2, (), ())
    rows.assert_read_back(written)
    assert [_genre_of(cfg, cid) for cid in ("30", "31", "32", "33", "34")] == [
        MELODIC, PROGRESSIVE, DEEP, DEEP, DEEP
    ]
    after = _content(cfg)
    assert set(after) == set(before)
    for content_id, row in after.items():
        changed = {
            column
            for column in row
            if row[column] != before[content_id][column]
            and column not in rb_writer.BOOKKEEPING_COLUMNS
        }
        assert changed == ({"GenreID"} if content_id in ("30", "31") else set()), content_id
    # NEVER A TEMPO: spelled out although the loop above already holds it.
    assert {row["BPM"] for row in after.values() if row["FolderPath"]} == {12400}
    # NOTHING IS WRITTEN TO ANY FILE.
    assert _files(cfg) == files
    # NO LOOKUP ROW WAS MADE.
    assert _query(cfg, "SELECT COUNT(*) FROM djmdGenre") == [(len(LOOKUPS),)]


def test_the_apply_is_a_recorded_session_a_restore_can_undo(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", OLD, PROGRESSIVE))
    _plan, written = _apply(cfg)
    (record,) = session.records(cfg)
    assert record.session_id == written.session_id
    assert record.state is session.SessionState.CLOSED
    assert record.sources == {rows.CHANGE_KEY: "committed"}
    assert [(change.tree, change.created, change.updated) for change in record.change.trees] == [
        (rows.CHANGE_KEY, 0, 2)
    ]


def test_a_second_apply_plans_nothing_and_writes_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    _apply(cfg)
    settled = _content(cfg)
    plan = _planned(cfg)
    assert plan.writes == () and plan.items == ()
    _counts(plan, agree=1, no_path=BASELINE)
    assert _content(cfg) == settled


def test_the_apply_refuses_with_no_acknowledgment_and_writes_nothing(machine, silence):
    build(machine, silence, Track("30", OLD, MELODIC))
    before = _content(machine)
    with pytest.raises(CratekitError) as refused:
        _apply(machine)
    assert refused.value.cause.reason == "backup-acknowledgment-missing"
    assert _content(machine) == before


def test_the_apply_refuses_a_watch_over_nothing(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    db = rb_writer.open_db(cfg.library.db_path, require_closed=True, unlock=False, cfg=cfg)
    try:
        plan = rows.plan_rows(cfg, db, DECLARED)
        with pytest.raises(ValueError, match="analysis_roots is empty"):
            rows.apply_rows(cfg, db, plan, analysis_roots=())
    finally:
        rb_writer.close_db(db)
    assert _genre_of(cfg, "30") == OLD


def test_a_commit_that_refuses_leaves_the_row_as_it_was_and_claims_no_commit(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))

    def refuse_commit(db, **kwargs):
        raise RuntimeError("the commit did not happen")

    monkeypatch.setattr(rb_writer, "commit_guarded", refuse_commit)
    with pytest.raises(RuntimeError, match="did not happen"):
        _apply(cfg)
    assert _genre_of(cfg, "30") == OLD
    (record,) = session.records(cfg)
    assert record.sources == {}


def test_an_unregistered_policy_would_write_nothing_and_the_apply_registers_it(
    acknowledged, silence
):
    """The first caller's own failure path: unregistered, every change is unowned."""
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    assert metadata.RETAG_GENRE not in rb_writer.registered_field_policies()
    _apply(cfg)
    assert metadata.RETAG_GENRE in rb_writer.registered_field_policies()
    assert _genre_of(cfg, "30") == MELODIC


def _plan_then(cfg: config.Config, sql: str, *params) -> rows.RowsPlan:
    """A plan, then one statement run against the database behind its back."""
    plan = _planned(cfg)
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        connection.execute(sql, params)
        connection.commit()
    finally:
        connection.close()
    return plan


def _apply_plan(cfg: config.Config, plan: rows.RowsPlan) -> rows.Written:
    db = rb_writer.open_db(cfg.library.db_path, require_closed=True, unlock=False, cfg=cfg)
    try:
        return rows.apply_rows(cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)


def test_a_row_whose_genre_moved_since_the_plan_refuses_and_nothing_is_written(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", OLD, MELODIC))
    plan = _plan_then(
        cfg, "UPDATE djmdContent SET GenreID = ? WHERE ID = '31'", _genre_ids()[DEEP]
    )
    with pytest.raises(CratekitError) as refused:
        _apply_plan(cfg, plan)
    cause = refused.value.cause
    assert cause.reason == "decision-stale" and "1 of 2" in cause.message
    assert cause.detail["moved"] == ["31: its genre changed since the plan"]
    assert [_genre_of(cfg, cid) for cid in ("30", "31")] == [OLD, DEEP]
    # Refused before the session is entered: no record and no capture.
    assert session.records(cfg) == ()


def test_a_row_removed_since_the_plan_refuses_and_nothing_is_written(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    plan = _plan_then(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '30'")
    with pytest.raises(CratekitError) as refused:
        _apply_plan(cfg, plan)
    assert refused.value.cause.reason == "decision-stale"
    assert refused.value.cause.detail["moved"] == ["30: no longer a live row"]
    assert _genre_of(cfg, "30") == OLD and session.records(cfg) == ()


@pytest.mark.parametrize("held", [None, "", 0, "0"])
def test_a_blank_row_is_as_planned_however_the_database_spells_blank(held):
    change = metadata.Change("30", metadata.RETAG_GENRE, "GenreID", None, "101")
    plan = rows.RowsPlan(
        items=(), counts={}, changes=metadata.Plan(metadata.RETAG_GENRE, (change,))
    )
    def mapped(genre_id, **marker):
        return {"30": SimpleNamespace(ID="30", GenreID=genre_id, **marker)}

    rows.assert_rows_as_planned(plan, mapped(held, rb_local_deleted=0))
    with pytest.raises(CratekitError):
        rows.assert_rows_as_planned(plan, mapped("100", rb_local_deleted=0))
    with pytest.raises(CratekitError):
        rows.assert_rows_as_planned(plan, {})
    # A row that cannot say whether it is a tombstone refuses in the reader's
    # own words and is never read as live.
    with pytest.raises(CratekitError) as unreadable:
        rows.assert_rows_as_planned(plan, mapped(held))
    assert unreadable.value.cause.reason == "soft-delete-marker-unreadable"


# ── the read back's judgement, with no database ────────────────────────────


def _item(content_id: str = "30") -> rows.Item:
    return rows.Item(content_id, "/music/a.flac", OLD, MELODIC, rows.WRITE, genre_id="101")


def _snapshot(**columns) -> dict[str, dict]:
    row = {"ID": "30", "GenreID": "100", "BPM": 12400, "Title": "a", "usn": 4, "updated_at": "t0"}
    return {"30": {**row, **columns}}


NAMES = {"100": OLD, "101": MELODIC}


def test_the_read_back_passes_a_row_whose_genre_and_bookkeeping_alone_moved():
    after = _snapshot(GenreID="101", usn=5, updated_at="t1")
    assert rows.judge([_item()], _snapshot(), after, NAMES) == ((), ())


def test_the_read_back_names_a_row_that_does_not_carry_its_files_word():
    wrong, moved = rows.judge([_item()], _snapshot(), _snapshot(), NAMES)
    assert moved == () and len(wrong) == 1
    assert "30" in wrong[0] and repr(OLD) in wrong[0] and repr(MELODIC) in wrong[0]


def test_the_read_back_names_a_row_whose_genre_points_at_no_lookup_row():
    (wrong,), _moved = rows.judge([_item()], _snapshot(), _snapshot(GenreID="999"), NAMES)
    assert "reads ''" in wrong


def test_the_read_back_names_every_other_column_that_moved():
    after = _snapshot(GenreID="101", BPM=12800, Title="b")
    wrong, moved = rows.judge([_item()], _snapshot(), after, NAMES)
    assert wrong == () and moved == ("30: BPM, Title",)


def test_the_read_back_names_a_row_it_cannot_find():
    (wrong,), moved = rows.judge([_item()], _snapshot(), {}, NAMES)
    assert "could not be read" in wrong and moved == ()
    (wrong,), _ = rows.judge([_item()], {}, _snapshot(GenreID="101"), NAMES)
    assert "could not be read" in wrong


def test_a_clean_read_back_raises_nothing():
    rows.assert_read_back(rows.Written(session_id="s", written=1, read_back=1))


def test_a_moved_column_refuses_as_the_guards_defect_and_names_the_undo():
    written = rows.Written("session-1", 1, 1, moved=("30: BPM",))
    with pytest.raises(CratekitError) as refused:
        rows.assert_read_back(written)
    cause = refused.value.cause
    assert cause.reason == "whitelist-violation" and "30: BPM" in cause.message
    assert "session-1" in " ".join(cause.remediation.steps)


def test_a_genre_that_reads_wrong_refuses_and_names_the_undo():
    written = rows.Written("session-1", 2, 1, wrong=("30: reads '' ...",))
    with pytest.raises(CratekitError) as refused:
        rows.assert_read_back(written)
    cause = refused.value.cause
    assert cause.reason == "internal-error" and "1 of 2" in cause.message
    assert "session-1" in " ".join(cause.remediation.steps)


# ═══════════════════════════════════════════════════════════════════════════
# 3. The verb, through the real dispatcher
# ═══════════════════════════════════════════════════════════════════════════


def test_planned_written_and_read_back_through_the_two_acts(acknowledged, silence):
    cfg = acknowledged
    build(
        cfg,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", OLD, MELODIC),
        Track("32", "", PROGRESSIVE),
        Track("33", DEEP, COARSE),
        Track("34", DEEP, DEEP),
    )
    files = _files(cfg)

    code, acted, refused = _two_acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "ok"
    # The plan the person approved is the plan that was applied.
    shown = refused["cause"]["detail"]["shown"]
    assert shown["digest"] == acted["data"]["digest"]
    assert shown["count"] == 4 and shown["items"] == acted["data"]["items"]
    assert shown["outcomes"]["write"] == 3 and shown["outcomes"]["file-too-coarse"] == 1
    assert shown["pairs"][0] == {"row": OLD, "file": MELODIC, "rows": 2}

    assert [(item["content_id"], item["action"]) for item in acted["data"]["items"]] == [
        ("30", rows.WRITE), ("31", rows.WRITE), ("32", rows.WRITE), ("33", rows.LEAVE)
    ]
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["written"], totals["read_back"]) == (4, 3, 3)
    assert totals["rows"] == 5 + BASELINE
    assert totals["outcomes"] == {
        **dict.fromkeys(rows.OUTCOMES, 0),
        "write": 3, "agree": 1, "file-too-coarse": 1, "no-path": BASELINE,
    }
    assert [_genre_of(cfg, cid) for cid in ("30", "31", "32", "33", "34")] == [
        MELODIC, MELODIC, PROGRESSIVE, DEEP, DEEP
    ]
    assert _files(cfg) == files

    codes = [warning["code"] for warning in acted["warnings"]]
    assert codes == [rows_cli.GENRES_WRITTEN, rows_cli.ROWS_LEFT, rows_cli.FILES_NOT_READ]
    assert "1 row(s) differ from their file and were left alone (1 file-too-coarse)" in (
        acted["warnings"][1]["message"]
    )
    summary = acted["warnings"][0]["message"]
    assert "3 row(s) now carry" in summary and "3 read back" in summary
    assert repr(OLD) in summary and repr(MELODIC) in summary and "a blank genre" in summary


def test_the_plan_refusal_writes_nothing_and_a_declined_gate_writes_nothing(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    before = _content(cfg)

    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _content(cfg) == before and session.records(cfg) == ()

    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "abort", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, declined = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), declined
    assert declined["outcome"] == "no_op" and declined["data"]["totals"]["written"] == 0
    assert _content(cfg) == before and session.records(cfg) == ()


def test_the_gate_takes_no_inline_answer(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    code, refused = drive(["-d", f"{GATE}=apply", *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert _genre_of(cfg, "30") == OLD


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine, silence):
    build(machine, silence, Track("30", OLD, MELODIC))
    code, envelope = drive(VERB)
    assert envelope["cause"]["reason"] == "backup-acknowledgment-missing", envelope
    assert code != int(ExitCode.OK)
    assert "gate" not in (envelope["cause"].get("detail") or {})
    assert not gates.run_path(envelope["run_id"]).exists()
    assert _genre_of(machine, "30") == OLD


def test_a_file_changed_between_plan_and_apply_refuses_the_apply(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", OLD, MELODIC))
    before = _content(cfg)

    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope

    assert tags.write_tags(_file(cfg, "31"), {"genre": PROGRESSIVE})

    code, stale = drive(["--run", run_id, *VERB])
    assert stale["cause"]["reason"] == "decision-stale", stale
    assert code != int(ExitCode.OK)
    assert _content(cfg) == before and session.records(cfg) == ()


def test_a_second_run_after_a_clean_one_asks_and_is_a_no_op(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", DEEP, COARSE))
    code, acted, _ = _two_acts()
    assert code == int(ExitCode.OK), acted
    settled = _content(cfg)

    code, again, shown = _two_acts()
    assert code == int(ExitCode.OK), again
    assert shown["cause"]["detail"]["shown"]["outcomes"]["write"] == 0
    assert again["outcome"] == "no_op"
    assert again["data"]["totals"]["outcomes"]["write"] == 0
    assert again["data"]["totals"]["outcomes"]["agree"] == 1
    assert again["data"]["totals"]["written"] == 0
    # The row left alone is still listed, and still left.
    assert [(item["content_id"], item["action"]) for item in again["data"]["items"]] == [
        ("31", rows.LEAVE)
    ]
    assert again["warnings"][0]["code"] == rows_cli.NOTHING_TO_WRITE
    assert _content(cfg) == settled
    assert len(session.records(cfg)) == 1


def test_an_empty_plan_still_asks_and_opens_nothing_to_write(acknowledged, silence, monkeypatch):
    """Every declared gate fires, and a plan that writes nothing never reaches
    the write handle: an opener asked for write intent fails this case."""
    cfg = acknowledged
    build(cfg, silence, Track("30", DEEP, DEEP))
    real_open = rb_writer.open_db

    def read_only(path, *args, require_closed=False, **kwargs):
        assert not require_closed, "an empty plan opened the database to write"
        return real_open(path, *args, require_closed=require_closed, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", read_only)
    code, acted, refused = _two_acts()
    assert refused["cause"]["detail"]["shown"]["count"] == 0
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op" and session.records(cfg) == ()


def test_the_plan_is_read_with_rekordbox_open_and_the_write_refuses(
    acknowledged, silence, monkeypatch
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)

    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope

    code, running = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK), running
    assert running["cause"]["reason"] == "rekordbox-running", running
    assert _genre_of(cfg, "30") == OLD and session.records(cfg) == ()


def test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail(
    acknowledged, silence, tmp_path
):
    cfg = acknowledged
    away = tmp_path / "another-volume" / "Music" / "track.flac"
    build(
        cfg,
        silence,
        Track("30", OLD, MELODIC),
        Track("31", OLD, ABSENT),
        Track("32", OLD, ABSENT, recorded=str(away)),
    )
    code, acted, _ = _two_acts()
    assert code == int(ExitCode.OK), acted
    outcomes = acted["data"]["totals"]["outcomes"]
    assert (outcomes["write"], outcomes["file-missing"], outcomes["path-unmapped"]) == (1, 1, 1)
    assert [_genre_of(cfg, cid) for cid in ("30", "31", "32")] == [MELODIC, OLD, OLD]
    (warning,) = [w for w in acted["warnings"] if w["code"] == rows_cli.FILES_NOT_READ]
    assert f"{2 + BASELINE} of {3 + BASELINE} row(s)" in warning["message"]
    assert "1 file-missing" in warning["message"] and "1 path-unmapped" in warning["message"]


def test_the_genre_report_stops_naming_the_old_word_after_the_run(acknowledged, silence):
    """The residual's own symptom: the report reads the row."""
    cfg = acknowledged
    build(cfg, silence, *(Track(str(30 + n), OLD, MELODIC) for n in range(3)))

    def words() -> set[str]:
        code, report = drive(["report", "genres"])
        assert code == int(ExitCode.OK), report
        return {
            source["genre"]
            for genre in report["data"]["summary"]["genres"]
            for source in genre["sources"]
        }

    assert OLD in words()
    code, acted, _ = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert OLD not in words()


def test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", DEEP, ""))
    code, screen = drive_human(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), screen
    assert "write: 1" in screen and "file-blank: 1" in screen
    assert f"row={OLD}" in screen and f"file={MELODIC}" in screen
    assert "takes no inline answer" in screen

    run_id = screen.rsplit("crate run decide ", 1)[1].split()[0]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, text = drive_human(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), text
    assert "1 row(s) now carry their file's genre" in text and "restore of session" in text
    assert _genre_of(cfg, "30") == MELODIC


def test_a_library_most_of_whose_rows_are_unmapped_refuses_before_the_gate(
    acknowledged, silence, tmp_path
):
    """R-372's shape: the plan is empty for a reason a prefix rule fixes."""
    cfg = acknowledged
    away = tmp_path / "another-volume" / "Music"
    build(
        cfg,
        silence,
        Track("30", OLD, MELODIC),
        *(Track(str(40 + n), OLD, ABSENT, recorded=str(away / f"{n}.flac")) for n in range(4)),
    )
    code, envelope = drive(VERB)
    cause = envelope["cause"]
    assert cause["reason"] == metadata_cli.PATHS_MAJORITY_UNRESOLVED, envelope
    assert code != int(ExitCode.OK) and code != int(ExitCode.DECISION_REQUIRED)
    assert "gate" not in cause["detail"]
    assert "4 of 7 active rows" in cause["message"]
    assert "no row's genre can be compared with its file" in cause["message"]
    assert "vocals" not in cause["message"]
    assert (cause["detail"]["active"], cause["detail"]["unmapped"]) == (7, 4)
    assert sum(cause["detail"]["prefixes"].values()) == 4
    assert _genre_of(cfg, "30") == OLD


def test_the_sibling_verbs_refusal_still_speaks_of_vocals(acknowledged):
    """The clause is a parameter now, and its default is the sentence it was."""
    totals = metadata_cli.ResolutionTotals(active=4, unresolved=3, unmapped=3, prefixes={"/x": 3})
    assert "nothing about its vocals can be reported or written until the rule exists" in (
        metadata_cli.majority_unmapped_cause(acknowledged, totals).message
    )


def test_a_held_row_survives_the_write_and_the_apply_must_name_it_again(
    acknowledged, silence
):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", DEEP, PROGRESSIVE))
    held = [*VERB, "--leave", "31"]

    code, refused = drive(held)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["outcomes"]["held-out"] == 1 and shown["outcomes"]["write"] == 1
    assert "leave_unmatched" not in shown
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope

    # WITHOUT THE FLAG THE PLAN IS ANOTHER PLAN, and the answer does not carry.
    code, stale = drive(["--run", run_id, *VERB])
    assert stale["cause"]["reason"] == "decision-stale", stale
    assert [_genre_of(cfg, cid) for cid in ("30", "31")] == [OLD, DEEP]

    code, acted = drive(["--run", run_id, *held])
    assert code == int(ExitCode.OK), acted
    assert [_genre_of(cfg, cid) for cid in ("30", "31")] == [MELODIC, DEEP]
    assert acted["data"]["totals"]["written"] == 1
    (left,) = [w for w in acted["warnings"] if w["code"] == rows_cli.ROWS_LEFT]
    assert "1 held-out" in left["message"]


def test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about(acknowledged, silence):
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC))
    verb = [*VERB, "--leave", "3O"]
    code, acted, refused = _two_acts(verb)
    assert refused["cause"]["detail"]["shown"]["leave_unmatched"] == ["3O"]
    assert code == int(ExitCode.OK), acted
    (warning,) = [w for w in acted["warnings"] if w["code"] == rows_cli.LEAVE_UNMATCHED]
    assert "3O" in warning["message"] and "a row this plan writes" in warning["message"]
    assert _genre_of(cfg, "30") == MELODIC


def test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote(
    acknowledged, silence
):
    """The retag verb sends a person here, so the row it leaves names what to do."""
    cfg = acknowledged
    build(cfg, silence, Track("30", OLD, MELODIC), Track("31", OLD, UNSEEN))
    code, acted, _ = _two_acts()
    assert code == int(ExitCode.OK), acted
    assert [_genre_of(cfg, cid) for cid in ("30", "31")] == [MELODIC, OLD]
    (left,) = [w for w in acted["warnings"] if w["code"] == rows_cli.ROWS_LEFT]
    assert f"no genre row for {UNSEEN!r} on 1" in left["message"]
    assert "give one track that genre in rekordbox" in left["message"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. What the registry and the source say
# ═══════════════════════════════════════════════════════════════════════════


def test_the_verb_declares_the_row_and_no_file():
    entry = registry.entry("tag.rows")
    assert entry.writes == frozenset({"db_metadata"})
    assert entry.destructive and not entry.long_running
    (confirm,) = [spec for spec in entry.gates if spec.name == GATE]
    assert confirm.explicit and confirm.digest_source == "plan"
    assert confirm.options == ("apply", "abort")
    assert registry.CLOUD_SYNC_UNREADABLE_GATE in entry.gates


def _called(module) -> set[str]:
    """Every attribute called on ``tags`` in a module, by an AST walk."""
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    return {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "tags"
    }


def test_the_engine_calls_the_tag_reader_and_no_tag_writer():
    """Nothing here writes a file from a row. Held on the syntax tree."""
    assert _called(rows) == {"read_tags_checked", "read_tag_values"}
    assert _called(rows_cli) == set()
    # AND BY WHAT THE WRITERS ARE, not only by what this module calls today:
    # nothing it reaches on the tag module writes, clears or embeds.
    assert all(name.startswith("read_") for name in _called(rows))


def test_the_apply_goes_through_the_policy_the_retag_module_registers():
    """One home for registering before applying, and this verb is its caller."""
    tree = ast.parse(Path(rows.__file__).read_text(encoding="utf-8"))
    dotted = {
        f"{node.func.value.id}.{node.func.attr}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
    }
    assert "retag.apply_library" in dotted
    assert "metadata.plan_genre_retag" in dotted
    assert retag.apply_library is not None
