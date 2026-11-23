"""Analysis's check scenarios: `crate analyze check` reading rekordbox's result (U306).

On a disposable rekordbox database built from the binding's own schema, with
the intake tree cut over to an INBOX folder holding the Analyze playlist,
rows are left as rekordbox leaves them before and after a visit by setting
the columns it writes. The check waits on a pending action while rows are
not analysed, and names a row gone from the collection; it is suspect when
an analysed row's analysis file is missing or its stored path climbs out of
the share; it falls to every row not analysed when the intake tree is not
cut over; it ends with nothing checked when no row is in scope; and it
refuses a pass and a session no landing recorded, and a running rekordbox.

No scenario here writes an analysis file: a row analysed right carries a
beat grid in one, and nothing in this product writes a grid, so the verdict
that every row is done is the one path left to the suite. Self contained, so
the suites it stands beside can be trimmed without moving it.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.core import config, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from tests.test_config import valid_data

OK = int(ExitCode.OK)
PENDING = int(ExitCode.PENDING_HUMAN)
SUSPECT = int(ExitCode.LIBRARY_PREREQUISITE)
VERB = ("analyze", "check")
RECORDED_APP_VERSION = "9.9.9.0001"
DECLARED = taxonomy.default_taxonomy()
ROOT_ID = "p-inbox"
ANALYZE_ID = "p-analyze"


@dataclass(frozen=True)
class Row:
    """One collection row: whether rekordbox analysed it, where it says the file is."""

    content_id: str
    title: str
    analysed: int = 0
    stored: str = ""
    key: str | None = None
    deleted: bool = False
    in_analyze: bool = True


def _relaxed_schema():
    """The binding's schema copied with every non key column nullable, as rekordbox's is."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import MetaData

    schema = MetaData()
    for table in tables.Base.metadata.tables.values():
        table.to_metadata(schema)
    for table in schema.tables.values():
        for column in table.columns:
            if not column.primary_key:
                column.nullable = True
    return schema


def _row(model, **values):
    """One mapped row with every timestamp column filled, at the pinned instant."""
    from pyrekordbox.db6 import tables

    now = datetime.now(timezone.utc)
    made = model(**values)
    for key, column in model.__mapper__.columns.items():
        if isinstance(column.type, tables.DateTime) and getattr(made, key, None) is None:
            setattr(made, key, now)
    return made


def build(cfg: config.Config, *rows: Row, inbox: bool = True) -> None:
    """A disposable database holding ``rows``, and the INBOX folder with its Analyze playlist."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    db_path = Path(cfg.library.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    _relaxed_schema().create_all(engine)
    keys = sorted({row.key for row in rows if row.key})
    with Session(engine) as db_session:
        db_session.add(_row(tables.AgentRegistry, registry_id="localUpdateCount", int_1=100))
        db_session.add(_row(tables.DjmdProperty, DBID="1", DBVersion=rb_writer.pinned_db_version()))
        for index, scale in enumerate(keys):
            db_session.add(_row(tables.DjmdKey, ID=f"k-{scale}", ScaleName=scale, Seq=index + 1))
        if inbox:
            db_session.add(
                _row(
                    tables.DjmdPlaylist,
                    ID=ROOT_ID,
                    Name=DECLARED.intake.display,
                    Attribute=1,
                    ParentID="root",
                    Seq=1,
                    rb_local_deleted=0,
                )
            )
            db_session.add(
                _row(
                    tables.DjmdPlaylist,
                    ID=ANALYZE_ID,
                    Name="Analyze",
                    Attribute=0,
                    ParentID=ROOT_ID,
                    Seq=1,
                    rb_local_deleted=0,
                )
            )
        for number, row in enumerate(rows, start=1):
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=row.content_id,
                    Title=row.title,
                    Analysed=row.analysed,
                    AnalysisDataPath=row.stored or None,
                    KeyID=f"k-{row.key}" if row.key else None,
                    rb_local_deleted=1 if row.deleted else 0,
                )
            )
            if inbox and row.in_analyze:
                db_session.add(
                    _row(
                        tables.DjmdSongPlaylist,
                        ID=f"sp-{row.content_id}",
                        PlaylistID=ANALYZE_ID,
                        ContentID=row.content_id,
                        TrackNo=number,
                        rb_local_deleted=0,
                    )
                )
        db_session.commit()
    engine.dispose()
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.commit()
    connection.close()
    collection.reset_cache()


def cut_over(cfg: config.Config) -> None:
    """Record the intake tree native, anchored to the INBOX folder the database holds."""
    tree_registry.write(
        cfg,
        tree_registry.Registry().with_record(
            tree_registry.TreeRecord(
                tree_id=DECLARED.intake.id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 9, 29),
                root_id=ROOT_ID,
                source=tree_registry.DerivationSource.TAXONOMY,
            )
        ),
    )


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _reader_cache():
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the landing suite patches it."""
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


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A set up machine with the rekordbox pin recorded."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(
        valid_data(
            root,
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


FIVE = ("Alpha", "Bravo", "Charlie", "Delta", "Echo")


def stored(content_id: str) -> str:
    return f"/PIONEER/USBANLZ/c0f/{content_id}/ANLZ0000.DAT"


def test_waiting_on_the_visit(stage, machine):
    cut_over(machine)
    build(
        machine,
        Row("10", "01A - Alpha"),
        Row("11", "01A - Bravo"),
        Row("12", "01A - Charlie", deleted=True),
        Row("13", "Delta", analysed=105),
    )
    waiting = stage.crate(*VERB)
    assert waiting.code == PENDING, waiting.stderr
    assert stage.json(*VERB).code == PENDING


def test_suspect_analysis(stage, machine):
    cut_over(machine)
    build(
        machine,
        *(Row(str(10 + n), name, analysed=105, stored=stored(str(10 + n)), key="1A")
          for n, name in enumerate(FIVE[:3])),
        Row("13", "Delta", analysed=105, stored="/PIONEER/../../escape/ANLZ0000.DAT", key="1A"),
        Row("14", "Echo"),
    )
    suspect = stage.json(*VERB)
    assert suspect.code == SUSPECT, suspect.stdout
    assert stage.crate(*VERB).code == SUSPECT


def test_every_row_not_analysed_when_the_tree_is_not_cut_over(stage, machine):
    build(machine, *(Row(str(10 + n), name) for n, name in enumerate(FIVE)), inbox=False)
    fallen = stage.json(*VERB)
    assert fallen.code == PENDING, fallen.stdout


def test_nothing_in_scope_and_the_refusals(stage, machine, monkeypatch):
    cut_over(machine)
    build(machine, Row("10", "Alpha", analysed=105, stored=stored("10"), in_analyze=False))
    nothing = stage.crate(*VERB)
    assert nothing.code == OK, nothing.stderr
    assert stage.json(*VERB, "--pass", "no-such-pass").code != OK
    assert stage.crate(*VERB, "--session", "no-such-session").code != OK
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    assert stage.json(*VERB).code == int(ExitCode.REKORDBOX_OPEN)
