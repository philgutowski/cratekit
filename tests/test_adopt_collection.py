"""The collection reader, against a real database and against no database at all.

TWO HALVES, DRIVEN SEPARATELY, because they answer different questions.
``collection_rows`` is pure over mapped rows, so every branch in the derivation
runs here with no database and no configuration. ``read_collection`` is the thin
half that opens a handle, and what is under test there is that the open is a READ
and that the file is unchanged afterwards.

WHICH DATABASE. A disposable one, built from the binding's own schema in a
temporary directory, or a supplied ``CRATEKIT_TEST_DB`` snapshot copied again
first. Never anybody's library: the live database is off limits, and a test that
can reach it is a test that eventually does.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.adopt.scan import CollectionRow
from cratekit.core import config, rb_writer
from cratekit.core.cause import CratekitError
from tests import adopt_fixtures
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row

#: A name carrying an accented character, spelled in both composition forms. The
#: reader must return each one exactly as recorded: normalizing here would put a
#: second opinion beside ``cratekit.core.locations``, which is the module that
#: owns composition form and is where the 144 missing files were paid for.
NFC_NAME = "Café"
NFD_NAME = "Café"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
    monkeypatch.setattr(
        rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION
    )
    return resolved


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What this machine cannot speak for on behalf of a temporary library.

    Neutralising the process probes here weakens nothing under test: that the
    guards refuse a running application is proved directly, twice, in
    ``tests/test_rb_writer_db.py``.
    """
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
    """Three content rows, a genre, and a dangling genre reference.

    Written through the binding's own mapper rather than raw SQL, so the schema
    the rows land in is the one the reader will meet.
    """
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        session.add(_row(tables.DjmdGenre, ID="7", Name="Techno"))
        session.add(
            _row(
                tables.DjmdContent,
                ID="10",
                Title=NFC_NAME,
                GenreID="7",
                rb_local_deleted=0,
                FolderPath=f"file://localhost/Music/{NFC_NAME}.flac",
            )
        )
        session.add(
            _row(
                tables.DjmdContent,
                ID="11",
                Title=NFD_NAME,
                GenreID=None,
                rb_local_deleted=0,
                FolderPath=f"file://localhost/Music/{NFD_NAME}.flac",
            )
        )
        session.add(
            _row(
                tables.DjmdContent,
                ID="12",
                Title="gone",
                # A genre row that does not exist. Reachable in a real library
                # after a genre is deleted while a track still points at it.
                GenreID="999",
                rb_local_deleted=1,
                FolderPath="file://localhost/Music/gone.flac",
            )
        )
        session.commit()
    engine.dispose()


@pytest.fixture
def synthetic(cfg):
    """A disposable database carrying exactly the rows :func:`seed` writes.

    NEVER SUBSTITUTED BY A SUPPLIED SNAPSHOT, and the split from :func:`seeded`
    below is deliberate rather than an oversight. The tests using this fixture
    assert against rows BY IDENTIFIER, and a real snapshot carries somebody else's
    rows, so a substitution here would make every one of those assertions false
    about the file it was handed. Making them conditional on the environment would
    be a skip wearing an ``if``, which this repository routes through
    ``tests/_pending.py`` or does not write at all.
    """
    path = Path(cfg.library.db_path)
    _build_disposable_database(path, with_tag_category=False)
    seed(path)
    return path


@pytest.fixture
def seeded(cfg, synthetic):
    """The same database, with a supplied ``CRATEKIT_TEST_DB`` snapshot preferred.

    A supplied snapshot SUBSTITUTES for the synthetic build rather than switching
    anything on, which is the convention seam decisions Part 4 sets: the battery
    runs either way and supplying a real database strengthens it. Every test using
    this fixture asserts a property of the READ rather than a fact about the rows,
    so both files answer it. The supplied file is copied first, because reading a
    file somebody handed us is fine and leaving our fingerprints on it is not.
    """
    return adopt_fixtures.copy_supplied(cfg) or synthetic


class _Row:
    """One mapped row, as much of it as the reader asks about."""

    def __init__(self, identifier, path=None, genre=None, deleted=0) -> None:
        self.ID = identifier
        self.FolderPath = path
        self.GenreName = genre
        self.rb_local_deleted = deleted


# ---------------------------------------------------------------------------
# The derivation, with no database at all
# ---------------------------------------------------------------------------


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


def test_a_null_location_and_a_null_genre_are_empty_strings_not_none():
    """``scan_rows`` asks string questions of both, so neither may arrive as None."""
    (row,) = collection.collection_rows([_Row("1")])
    assert row.recorded == ""
    assert row.genre == ""


def test_a_tombstone_is_carried_rather_than_dropped():
    """Dropping it here would put one decision in two places.

    ``scan_rows`` already skips a deleted row and says why. A reader that also
    skipped would leave no caller able to tell an empty library from a library
    whose rows are all tombstones, which is the difference the scan verb reports.
    """
    (row,) = collection.collection_rows([_Row("1", deleted=1)])
    assert row.deleted is True


def test_a_row_that_cannot_report_the_marker_refuses_rather_than_defaulting():
    """R-186's defect, refused rather than reproduced.

    ``getattr(row, "rb_local_deleted", False)`` answers the permissive default for
    a row it could not ask, which hands every tombstone to the census as live.
    """

    class _Mute:
        ID = "1"
        FolderPath = "file://localhost/a.flac"
        GenreName = "Techno"

    with pytest.raises(CratekitError) as excinfo:
        list(collection.collection_rows([_Mute()]))
    assert excinfo.value.cause.reason == "soft-delete-marker-unreadable"


def test_the_identifier_is_stringified_because_the_column_need_not_be_text():
    (row,) = collection.collection_rows([_Row(1234, "file://localhost/a.flac", "Techno")])
    assert row.content_id == "1234"


# ---------------------------------------------------------------------------
# Against a real database
# ---------------------------------------------------------------------------


def test_the_reader_yields_the_rows_the_database_holds(cfg, synthetic):
    rows = {row.content_id: row for row in collection.read_collection(cfg)}
    assert set(rows) == {"1", "2", "10", "11", "12"}
    assert rows["10"].genre == "Techno"
    assert rows["10"].recorded.endswith(f"{NFC_NAME}.flac")
    assert rows["11"].genre == ""
    assert rows["11"].recorded.endswith(f"{NFD_NAME}.flac")
    assert rows["12"].deleted is True


def test_both_composition_forms_come_back_exactly_as_recorded(cfg, synthetic):
    """The reader normalizes nothing, which is ``core.locations``' job one layer down.

    Two rows whose names differ only in composition form must stay distinct here.
    A reader that normalized would collapse them and the resolver below would then
    be comparing a value nothing in the library actually holds.
    """
    recorded = {row.recorded for row in collection.read_collection(cfg)}
    assert f"file://localhost/Music/{NFC_NAME}.flac" in recorded
    assert f"file://localhost/Music/{NFD_NAME}.flac" in recorded
    assert NFC_NAME != NFD_NAME


def test_a_dangling_genre_reference_reads_as_no_genre(cfg, synthetic):
    """Measured, not assumed. The proxy answers None rather than raising."""
    rows = {row.content_id: row for row in collection.read_collection(cfg)}
    assert rows["12"].genre == ""
    assert rows["11"].genre == ""


def test_a_row_whose_file_is_absent_is_still_a_row(cfg, synthetic):
    """The reader stats nothing. Deciding whether a file is there is ``scan_rows``."""
    for row in collection.read_collection(cfg):
        if row.recorded:
            assert not Path(row.recorded.replace("file://localhost", "")).exists()


def test_the_reader_never_opens_the_database_for_writing(cfg, seeded, monkeypatch):
    """Asserted mechanically against the recorded call, not by reading the source.

    ``require_closed`` is ``open_db``'s write-intent flag. A reader that asked for
    one would pass the two-process refusal and the application pin, which is the
    open a WRITE makes, and nothing else about this module would look different.
    """
    calls: list[dict] = []
    real = rb_writer.open_db

    def recording(path=None, **kwargs):
        calls.append({"path": path, **kwargs})
        return real(path, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", recording)
    collection.read_collection(cfg)

    assert len(calls) == 1
    assert calls[0]["require_closed"] is False
    assert calls[0]["unlock"] is rb_writer.unlock_needed(seeded)


def test_the_database_file_is_byte_identical_after_a_full_read(cfg, seeded):
    """The strongest statement available without watching the file descriptor.

    Bytes AND modification time, and the write ahead log sidecars too, because a
    read that checkpointed would leave the main file changed and the log empty
    while every row still came back correct.
    """
    watched = [seeded, *(
        seeded.with_name(seeded.name + suffix)
        for suffix in rb_writer.db_sidecar_suffixes()
    )]
    before = {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in watched
        if path.exists()
    }
    collection.read_collection(cfg)
    after = {
        path: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in watched
        if path.exists()
    }
    assert after == before


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
    """Named rather than a traceback. This is a new refusal surface on two verbs."""
    with pytest.raises(CratekitError) as excinfo:
        collection.read_collection(cfg)
    assert excinfo.value.cause.reason == "library-database-missing"


# ---------------------------------------------------------------------------
# The property that is not a behaviour
# ---------------------------------------------------------------------------


def test_this_module_holds_no_write_path_at_all():
    """An AST walk, not a grep and not a review.

    Three shapes would each turn this module into one that can write: an open
    asking for write intent, a session, or a commit. A grep for ``commit`` would
    also match the word in a docstring, and a review is what every defect in this
    repository has already survived.
    """
    source = Path(collection.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported |= {
        f"{node.module}.{alias.name}"
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
        for alias in node.names
    }
    assert not any("session" in name for name in imported), imported

    attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert "commit" not in attributes
    assert "session" not in attributes

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        target = node.func
        if isinstance(target, ast.Attribute) and target.attr == "open_db":
            written = {
                keyword.arg: keyword.value
                for keyword in node.keywords
                if keyword.arg is not None
            }
            intent = written.get("require_closed")
            assert isinstance(intent, ast.Constant) and intent.value is False
