"""The collection reader, against a real database and against no database at all.

``collection_rows`` is pure over mapped rows, so every branch of the derivation
runs with no database. ``read_collection`` opens a handle, and what is under test
there is that the open is a READ and the file is unchanged afterwards.

The database is a disposable one built from the binding's schema in a temporary
directory, or a supplied ``CRATEKIT_TEST_DB`` snapshot copied first. Never
anybody's library.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.adopt.scan import CollectionRow
from cratekit.core import config, locations, rb_writer
from cratekit.core.cause import CratekitError
from tests import adopt_fixtures
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row

#: An accented name in both composition forms; the reader returns each as recorded.
NFC_NAME = "Café"
NFD_NAME = "Café"


def _url(name: str) -> str:
    return locations.location_url(Path("/Music") / f"{name}.flac")


# ── Fixtures ──


@pytest.fixture(autouse=True)
def _clear_reader_cache():
    """No test may inherit another test's library."""
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    """Configuration with the application pin recorded, since an unset one refuses."""
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    return resolved


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What this machine cannot speak for on behalf of a temporary library; that
    the guards refuse a running application is proved in ``tests/test_rb_writer_db.py``."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


def seed(db_path: Path) -> None:
    """Three content rows, a genre, and a dangling genre reference, written through
    the binding's own mapper so the schema is the one the reader meets."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        session.add(_row(tables.DjmdGenre, ID="7", Name="Techno"))
        # Row 12 names a genre row that does not exist, as after a genre is deleted.
        for content_id, title, genre_id, deleted, location in (
            ("10", NFC_NAME, "7", 0, _url(NFC_NAME)),
            ("11", NFD_NAME, None, 0, _url(NFD_NAME)),
            ("12", "gone", "999", 1, locations.location_url(Path("/Music/gone.flac"))),
        ):
            session.add(
                _row(
                    tables.DjmdContent,
                    ID=content_id,
                    Title=title,
                    GenreID=genre_id,
                    rb_local_deleted=deleted,
                    FolderPath=location,
                )
            )
        session.commit()
    engine.dispose()


@pytest.fixture
def synthetic(cfg):
    """A disposable database carrying exactly the rows :func:`seed` writes.

    Never a supplied snapshot: these tests assert rows by identifier.
    """
    path = Path(cfg.library.db_path)
    _build_disposable_database(path, with_tag_category=False)
    seed(path)
    return path


@pytest.fixture
def seeded(cfg, synthetic):
    """The same database, with a supplied ``CRATEKIT_TEST_DB`` snapshot preferred
    and copied first (seam decisions Part 4). Its tests assert properties of the
    READ, which both files answer."""
    return adopt_fixtures.copy_supplied(cfg) or synthetic


class _Row:
    """One mapped row, as much of it as the reader asks about."""

    def __init__(self, identifier, path=None, genre=None, deleted=0) -> None:
        self.ID = identifier
        self.FolderPath = path
        self.GenreName = genre
        self.rb_local_deleted = deleted


# ── The derivation, with no database at all ──


def test_every_field_comes_off_the_row_it_belongs_to():
    rows = list(collection.collection_rows([_Row("1", "file://localhost/a.flac", "Techno")]))
    assert rows == [
        CollectionRow(
            content_id="1",
            recorded="file://localhost/a.flac",
            genre="Techno",
            deleted=False,
        )
    ]
    # The identifier is stringified, because the column need not be text.
    (row,) = collection.collection_rows([_Row(1234, "file://localhost/a.flac", "Techno")])
    assert row.content_id == "1234"


def test_a_null_location_and_a_null_genre_are_empty_strings_not_none():
    """``scan_rows`` asks string questions of both, so neither may arrive as None."""
    (row,) = collection.collection_rows([_Row("1")])
    assert row.recorded == ""
    assert row.genre == ""


def test_a_tombstone_is_carried_rather_than_dropped():
    """``scan_rows`` already skips a deleted row; skipping here too would leave no
    caller able to tell an empty library from a library of tombstones."""
    (row,) = collection.collection_rows([_Row("1", deleted=1)])
    assert row.deleted is True


def test_a_row_that_cannot_report_the_marker_refuses_rather_than_defaulting():
    """R-186's defect, refused rather than reproduced: a permissive default for a
    row it could not ask hands every tombstone to the census as live."""

    class _Mute:
        ID = "1"
        FolderPath = "file://localhost/a.flac"
        GenreName = "Techno"

    with pytest.raises(CratekitError) as excinfo:
        list(collection.collection_rows([_Mute()]))
    assert excinfo.value.cause.reason == "soft-delete-marker-unreadable"


# ── Against a real database ──


def test_the_reader_yields_the_rows_the_database_holds(cfg, synthetic):
    """The recorded value is the percent-encoded URL rekordbox writes, passed through.

    Both composition forms come back as recorded and distinct, a dangling genre
    reads as no genre, and a row whose file is absent is still a row.
    """
    rows = {row.content_id: row for row in collection.read_collection(cfg)}
    assert set(rows) == {"1", "2", "10", "11", "12"}
    assert rows["10"].genre == "Techno"
    assert rows["10"].recorded == _url(NFC_NAME)
    assert rows["11"].genre == ""
    assert rows["11"].recorded == _url(NFD_NAME)
    assert rows["12"].deleted is True
    assert rows["12"].genre == ""
    assert NFC_NAME != NFD_NAME
    for row in rows.values():
        if row.recorded:
            assert not Path(locations.location_to_path(row.recorded)).exists()


def test_the_reader_never_opens_the_database_for_writing(cfg, seeded, monkeypatch):
    """Asserted against the recorded call: ``require_closed`` is ``open_db``'s
    write-intent flag, and a reader asking for it would make a write's open."""
    calls: list[dict] = []
    real = rb_writer.open_db

    def recording(path=None, **kwargs):
        calls.append({"path": path, **kwargs})
        return real(path, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", recording)
    collection.read_collection(cfg)

    assert len(calls) == 1
    assert calls[0]["require_closed"] is False
    # The key question is left to the opener, which asks the file (R-239).
    assert "unlock" not in calls[0]


def test_the_database_file_is_byte_identical_after_a_full_read(cfg, seeded):
    """Bytes and modification time, sidecars included, since a checkpoint changes both."""
    suffixes = rb_writer.db_sidecar_suffixes()
    watched = [seeded, *(seeded.with_name(seeded.name + suffix) for suffix in suffixes)]

    def state():
        return {
            path: (path.read_bytes(), path.stat().st_mtime_ns) for path in watched if path.exists()
        }

    before = state()
    collection.read_collection(cfg)
    assert state() == before


def test_two_reads_in_one_process_open_the_database_once(cfg, seeded, monkeypatch):
    """KTD14. ``run_job`` drives every item in one process and each item reads."""
    opens: list[str] = []
    real = rb_writer.open_db

    def counting(path=None, **kwargs):
        opens.append(str(path))
        return real(path, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", counting)
    first = collection.read_collection(cfg)
    second = collection.read_collection(cfg)
    assert len(opens) == 1
    assert first == second

    collection.reset_cache()
    collection.read_collection(cfg)
    assert len(opens) == 2


def test_a_configured_library_with_no_database_is_a_named_refusal(cfg):
    """Named rather than a traceback, on two verbs' new refusal surface."""
    with pytest.raises(CratekitError) as excinfo:
        collection.read_collection(cfg)
    assert excinfo.value.cause.reason == "library-database-missing"


# ── The property that is not a behaviour ──


def test_this_module_holds_no_write_path_at_all():
    """An AST walk: no open with write intent, no session and no commit."""
    tree = ast.parse(Path(collection.__file__).read_text(encoding="utf-8"))
    nodes = list(ast.walk(tree))

    imported = {
        alias.name for node in nodes if isinstance(node, ast.Import) for alias in node.names
    }
    imported |= {
        f"{node.module}.{alias.name}"
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.module
        for alias in node.names
    }
    assert not any("session" in name for name in imported), imported

    attributes = {node.attr for node in nodes if isinstance(node, ast.Attribute)}
    assert "commit" not in attributes
    assert "session" not in attributes

    for node in nodes:
        if not isinstance(node, ast.Call):
            continue
        target = node.func
        if isinstance(target, ast.Attribute) and target.attr == "open_db":
            written = {
                keyword.arg: keyword.value for keyword in node.keywords if keyword.arg is not None
            }
            intent = written.get("require_closed")
            assert isinstance(intent, ast.Constant) and intent.value is False
