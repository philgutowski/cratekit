"""The guarded writer against a REAL database, a real object-mapper session, and a real commit.

The pure suite proves the decisions, this proves the ADAPTER, on a disposable database built
from the binding's schema and never a live library. ``CRATEKIT_TEST_DB`` points the same
battery at a snapshot copy, copied again first, which also exercises the key path.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core import rb_writer as W
from cratekit.core.exit_codes import Remedy
from tests.test_config import valid_data

#: The pin the tests record and satisfy, a shape rather than an installed version.
RECORDED_APP_VERSION = "9.9.9.0001"


# Building a disposable database


def _relaxed_schema():
    """A copy of the binding's schema with non-key columns nullable, as rekordbox's own is looser.

    Copied because the binding's metadata is shared process wide."""
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
    """One mapped row with every timestamp filled, since the binding's date type raises on null."""
    from pyrekordbox.db6 import tables

    now = datetime.now(timezone.utc)
    obj = model(**values)
    for key, column in model.__mapper__.columns.items():
        if isinstance(column.type, tables.DateTime) and getattr(obj, key, None) is None:
            setattr(obj, key, now)
    return obj


#: Each worker's built databases as bytes, keyed by tag category and schema pin, so every
#: call writes a private copy and no test can touch the template (U256).
_TEMPLATES: dict[tuple[bool, str], bytes] = {}

#: The files SQLite keeps for a database, a path holding any is built from nothing (U256).
_DATABASE_FILES = ("", "-wal", "-shm", "-journal")

#: SQLite's default database file mode, ``SQLITE_DEFAULT_FILE_PERMISSIONS``.
_SQLITE_FILE_MODE = 0o644


def _build_disposable_database(db_path: Path, *, with_tag_category: bool = True) -> None:
    """A database carrying the minimum the safety chain reads, copied from a template (U256)."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_version = W.pinned_db_version()
    if any(os.path.lexists(f"{db_path}{suffix}") for suffix in _DATABASE_FILES):
        _build_from_nothing(db_path, with_tag_category=with_tag_category, db_version=db_version)
        return
    key = (with_tag_category, db_version)
    template = _TEMPLATES.get(key)
    if template is None:
        template = _template(with_tag_category=with_tag_category, db_version=db_version)
        _TEMPLATES[key] = template
    # Created exclusively with SQLite's own mode, so a copy matches a build under any umask.
    descriptor = os.open(db_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _SQLITE_FILE_MODE)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(template)


def _template(*, with_tag_category: bool, db_version: str) -> bytes:
    """One database built from nothing and read as bytes, refusing if any sidecar is left."""
    with tempfile.TemporaryDirectory(prefix="cratekit-fixture-db-") as folder:
        path = Path(folder) / "master.db"
        _build_from_nothing(path, with_tag_category=with_tag_category, db_version=db_version)
        left = sorted(os.listdir(folder))
        if left != ["master.db"]:
            raise AssertionError(f"the fixture database build left {left}, not one file")
        with open(path, "rb") as handle:
            return handle.read()


def _build_from_nothing(db_path: Path, *, with_tag_category: bool, db_version: str) -> None:
    """Create the schema and insert the rows, from nothing, at ``db_path``."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    _relaxed_schema().create_all(engine)
    with Session(engine) as session:
        # The local update counter: what the canary's first read resolves.
        session.add(_row(tables.AgentRegistry, registry_id="localUpdateCount", int_1=100))
        # The schema version the pin compares against.
        session.add(_row(tables.DjmdProperty, DBID="1", DBVersion=db_version))
        session.add(_row(tables.DjmdContent, ID="1", Title="a track", rb_local_deleted=0))
        session.add(_row(tables.DjmdContent, ID="2", Title="another track", rb_local_deleted=0))
        if with_tag_category:
            session.add(
                _row(
                    tables.DjmdMyTag,
                    ID="10",
                    Name="a category",
                    Attribute=0,
                    ParentID="0",
                    Seq=0,
                    UUID="category-uuid",
                )
            )
        session.commit()
    engine.dispose()

    # WAL mode, the mode the real database runs in.
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.commit()
    conn.close()


def _encrypt_in_place(db_path: Path) -> None:
    """Encrypt a disposable database with the binding's own key, as a real library is (R-239).

    Folded out of WAL first so no plaintext sidecar is left, then put back into WAL."""
    from pyrekordbox.db6.database import BLOB
    from pyrekordbox.utils import deobfuscate
    from sqlcipher3 import dbapi2

    plain = sqlite3.connect(db_path)
    plain.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    plain.execute("PRAGMA journal_mode=DELETE")
    plain.close()

    key = deobfuscate(BLOB)
    encrypted = db_path.with_name(db_path.name + ".encrypting")
    conn = dbapi2.connect(str(db_path))
    try:
        conn.execute(f"ATTACH DATABASE '{encrypted}' AS encrypted KEY '{key}'")
        conn.execute("SELECT sqlcipher_export('encrypted')")
        conn.execute("DETACH DATABASE encrypted")
    finally:
        conn.close()
    os.replace(encrypted, db_path)

    conn = dbapi2.connect(str(db_path))
    try:
        conn.execute(f"PRAGMA key = '{key}'")
        conn.execute("PRAGMA journal_mode=WAL")
    finally:
        conn.close()
    assert W.unlock_needed(db_path), "the encrypted copy still carries a plain header"


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A temporary library root, with configuration pointing at it."""
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def pinned(library, monkeypatch):
    """Configuration with the application pin RECORDED, since an unset pin refuses writes (S2)."""
    cfg = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: cfg)
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    return cfg


@pytest.fixture(autouse=True)
def _rekordbox_closed(monkeypatch):
    """Every rekordbox probe patched where it is resolved, the binding's own included."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)


@pytest.fixture
def cloud_sync_off(monkeypatch):
    """Drive the canary's OFF branch through the settings reader's seam, not a settings file."""
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: {W.LIBRARY_SYNC_SETTING: 0}
    )


@pytest.fixture
def database(library, tmp_path):
    """The database under test, a supplied snapshot COPIED first since writing to it is not ours."""
    supplied = W.integration_db_path()
    if supplied is not None:
        target = tmp_path / "supplied" / supplied.name
        target.parent.mkdir(parents=True)
        shutil.copy2(supplied, target)
        for suffix in W.db_sidecar_suffixes():
            sidecar = supplied.with_name(supplied.name + suffix)
            if sidecar.exists():
                shutil.copy2(sidecar, target.with_name(target.name + suffix))
        return target, True

    path = library / "db" / "master.db"
    _build_disposable_database(path)
    return path, False


@pytest.fixture
def opened(database, cloud_sync_off):
    """A read-only open through the full gate, closed afterwards whatever happens."""
    path, unlock = database
    db = W.open_db(path, unlock=unlock)
    try:
        yield db
    finally:
        W.close_db(db)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# The open-side gate


def test_a_real_database_opens_through_the_whole_chain(opened):
    """Binding pin, open, canary reads, schema pin. All of it, against a real file."""
    assert opened.get_local_usn() is not None
    assert opened.get_content().first() is not None


def test_a_write_intent_open_passes_the_process_refusal_and_the_recorded_pin(
    database, pinned, cloud_sync_off
):
    """The path a writer actually takes: both processes clear, pin matched, cloud off."""
    path, unlock = database
    db = W.open_db(path, require_closed=True, unlock=unlock, cfg=pinned)
    try:
        assert db.get_local_usn() is not None
    finally:
        W.close_db(db)


def test_a_missing_database_directory_names_the_unmounted_volume(tmp_path):
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.open_db(tmp_path / "gone" / "master.db")
    assert excinfo.value.cause.reason == "library-directory-missing"


def test_a_missing_database_file_is_its_own_refusal(tmp_path):
    """A missing file is its own refusal, distinct from an unmounted volume."""
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.open_db(tmp_path / "master.db")
    assert excinfo.value.cause.reason == "library-database-missing"


def test_a_file_that_is_not_a_database_refuses_rather_than_returning_a_handle(tmp_path):
    """Existence is not readability, which is why the canary exists at all."""
    impostor = tmp_path / "master.db"
    impostor.write_bytes(b"this is not a database")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.open_db(impostor, unlock=False)
    assert excinfo.value.cause.reason in {"database-open-failed", "canary-read-failed"}


def test_the_binding_pin_refuses_before_anything_is_opened(database, monkeypatch):
    """Pin 1 has no escape and fires on a read too, since a mis-mapped read feeds the write."""
    path, unlock = database
    cfg = config.from_dict(
        valid_data(path.parent.parent, rekordbox={"pinned_pyrekordbox": "0.0.0"})
    )
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.open_db(path, unlock=unlock, cfg=cfg)
    assert excinfo.value.cause.reason == "pyrekordbox-pin-drift"


def test_the_schema_pin_refuses_on_a_drifted_database(database, cloud_sync_off):
    """Pin 2, folded into the open chain so no caller can omit it."""
    path, unlock = database
    cfg = config.from_dict(
        valid_data(path.parent.parent, rekordbox={"pinned_db_version": "5999"})
    )
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.open_db(path, unlock=unlock, cfg=cfg)
    assert excinfo.value.cause.reason == "db-schema-pin-drift"


def test_the_schema_pin_can_be_forced_for_a_deliberate_revalidation(database, cloud_sync_off):
    """The escape stays deliberate and loud, and it stays off by default."""
    path, unlock = database
    cfg = config.from_dict(
        valid_data(path.parent.parent, rekordbox={"pinned_db_version": "5999"})
    )
    W.close_db(W.open_db(path, unlock=unlock, cfg=cfg, force_schema=True))


# R-239: the key is asked of the file, by the opener, for every caller


@pytest.mark.parametrize("encrypted", [True, False], ids=["encrypted", "plain"])
def test_an_open_that_names_no_key_opens_either_kind_of_database(
    library, cloud_sync_off, encrypted
):
    """The opener answers the key question itself, so no caller can answer it wrong."""
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    if encrypted:
        _encrypt_in_place(path)
    db = W.open_db(path)
    try:
        assert {row.ID for row in db.get_content()} == {"1", "2"}
    finally:
        W.close_db(db)


def test_an_encrypted_database_does_not_open_with_the_key_withheld(library, cloud_sync_off):
    """The fixture is really encrypted: the binding cannot read it without the key."""
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    _encrypt_in_place(path)
    with pytest.raises(W.RekordboxUnavailable):
        W.close_db(W.open_db(path, unlock=False))


@pytest.mark.parametrize("encrypted", [True, False], ids=["encrypted", "plain"])
def test_a_snapshot_check_that_names_no_key_verifies_either_kind(
    library, tmp_path, cloud_sync_off, encrypted
):
    """The snapshot check, which once assumed the key, verifies either kind with no argument."""
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    if encrypted:
        _encrypt_in_place(path)
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    assert W.integrity_ok(snapshot) is True


def _unlock_arguments(tree) -> list[tuple[int, str]]:
    """Every call in ``tree`` to an opener that passes ``unlock=``, ``**kwargs`` included."""
    import ast

    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if name not in {"open_db", "integrity_ok"}:
            continue
        if any(kw.arg == "unlock" or kw.arg is None for kw in node.keywords):
            found.append((node.lineno, name))
    return found


def _forwarded_lines(tree) -> set[int]:
    """Where ``integrity_ok`` forwards its bare ``unlock`` to ``open_db``, and no other."""
    import ast

    lines: set[int] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == "integrity_ok"):
            continue
        for call in ast.walk(node):
            if not isinstance(call, ast.Call):
                continue
            if any(
                kw.arg == "unlock" and isinstance(kw.value, ast.Name) and kw.value.id == "unlock"
                for kw in call.keywords
            ):
                lines.add(call.lineno)
    return lines


def test_no_caller_in_src_answers_the_key_question_for_itself():
    """R-239: one function answers the key question, and only ``integrity_ok`` forwards it."""
    import ast

    root = Path(W.__file__).resolve().parents[1]
    problems = []
    scanned = 0
    forwards = 0
    for source in sorted(root.rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        scanned += 1
        forwarded = _forwarded_lines(tree) if source.name == "rb_copies.py" else set()
        for line, name in _unlock_arguments(tree):
            if line in forwarded:
                forwards += 1
                continue
            problems.append(f"{source.relative_to(root)}:{line}: {name}(unlock=...)")
    assert scanned > 100, f"scanned {scanned} files; the walk is not reaching src"
    assert forwards == 1, f"expected integrity_ok's one forward, found {forwards}"
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize(
    "source",
    [
        "def integrity_ok(snapshot, *, unlock=None):\n    open_db(snapshot, unlock=False)\n",
        "def other(path, *, unlock=None):\n    open_db(path, unlock=unlock)\n",
    ],
    ids=["literal-inside-integrity-ok", "forward-outside-integrity-ok"],
)
def test_the_forward_exemption_admits_only_integrity_ok_passing_its_own_argument(source):
    import ast

    tree = ast.parse(source)
    assert _unlock_arguments(tree)
    assert _forwarded_lines(tree) == set()


@pytest.mark.parametrize(
    "source",
    [
        "rb_writer.open_db(cfg=cfg, unlock=False)",
        "open_db(path, unlock=True)",
        "W.integrity_ok(snapshot, unlock=False)",
        "rb_writer.open_db(path, **options)",
    ],
)
def test_the_key_guard_sees_each_spelling_of_an_answered_question(source):
    """The key guard's refusals, on literal sources, so the scan cannot pass by seeing nothing."""
    import ast

    assert _unlock_arguments(ast.parse(source))


def test_the_key_guard_accepts_an_open_that_asks():
    import ast

    assert _unlock_arguments(ast.parse("rb_writer.open_db(cfg=cfg)")) == []


# The commit-side gate, against a real session


def test_a_registered_column_write_commits_and_persists(opened, cloud_sync_off):
    """The one operation that exists at this unit's time, end to end."""
    row = opened.get_content().first()
    assert W.write_metadata_field(row, "track-color", "ColorID", "4") is W.Decision.WRITE
    W.commit_guarded(opened)

    opened.session.expire_all()
    assert str(opened.get_content().first().ColorID) == "4"


def test_an_analysis_column_write_is_refused_and_rolled_back(opened, cloud_sync_off):
    """R17 on a REAL session, rolled back so a refused write never lands under a later commit."""
    row = opened.get_content().first()
    row.BPM = 12800

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(opened)
    assert excinfo.value.cause.reason == "whitelist-violation"
    assert "BPM" in str(excinfo.value)

    assert not opened.session.dirty, "the refused session was left pending"
    opened.session.expire_all()
    assert opened.get_content().first().BPM in (None, 0)


def test_an_unregistered_column_is_refused_even_though_it_is_ordinary_metadata(
    opened, cloud_sync_off
):
    """R14: nothing is writable until an operation registers it."""
    assert "Rating" not in W.content_writable_columns()
    row = opened.get_content().first()
    row.Rating = 5
    with pytest.raises(W.RekordboxUnavailable):
        W.commit_guarded(opened)


def test_a_registration_widens_the_gate_by_exactly_its_own_fields(opened, cloud_sync_off):
    """And by nothing else. The seam has to be usable or a later unit routes around it."""
    W.register_field_policy(
        W.FieldPolicy(owner="rating-backfill", fields={"Rating": W.Ownership.FILL_IF_EMPTY})
    )
    try:
        row = opened.get_content().first()
        assert W.write_metadata_field(row, "rating-backfill", "Rating", 4) is W.Decision.WRITE
        W.commit_guarded(opened)
        assert "Rating" in W.content_writable_columns()
        assert "GenreID" not in W.content_writable_columns()
    finally:
        W.reset_field_policies()


def test_a_real_delete_is_refused_and_rolled_back(opened, cloud_sync_off):
    """Every delete is refused and rolled back, since a deletion's damage is invisible."""
    row = opened.get_content().first()
    opened.session.delete(row)

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(opened)
    assert "additive-only" in str(excinfo.value)

    opened.session.expire_all()
    assert opened.get_content().first() is not None


def test_a_playlist_creation_commits_because_the_table_is_whitelisted(opened, cloud_sync_off):
    """The other side of the whitelist: the permitted tables really are permitted."""
    folder = W.ensure_folder(opened, "a folder")
    W.commit_guarded(opened)
    assert int(folder.Attribute) == 1

    playlist = W.ensure_playlist(opened, "a playlist", folder)
    W.commit_guarded(opened)
    assert str(playlist.ParentID) == str(folder.ID)


def test_the_tree_primitives_are_idempotent(opened, cloud_sync_off):
    """A re-run is a no-op, which is what makes a resumed run safe to repeat."""
    folder = W.ensure_folder(opened, "a folder")
    W.commit_guarded(opened)
    assert W.ensure_folder(opened, "a folder").ID == folder.ID

    playlist = W.ensure_playlist(opened, "a playlist", folder)
    W.commit_guarded(opened)
    assert W.ensure_playlist(opened, "a playlist", folder).ID == playlist.ID

    assert W.add_membership(opened, playlist, "1") is True
    W.commit_guarded(opened)
    assert W.add_membership(opened, playlist, "1") is False


def test_the_batch_membership_primitive_reads_presence_once_and_inserts_what_is_absent(
    opened, cloud_sync_off, monkeypatch
):
    """R-10: one presence read per call, counted at the binding, whatever the number of tracks."""
    folder = W.ensure_folder(opened, "a folder")
    playlist = W.ensure_playlist(opened, "a playlist", folder)
    W.commit_guarded(opened)
    assert W.add_membership(opened, playlist, "1") is True
    W.commit_guarded(opened)

    real_read = opened.get_playlist_songs
    reads = {"n": 0}

    def counting_read(**kwargs):
        reads["n"] += 1
        return real_read(**kwargs)

    monkeypatch.setattr(opened, "get_playlist_songs", counting_read)

    assert W.add_memberships(opened, playlist, ["1", "2", "2"]) == ["2"]
    assert reads["n"] == 1
    W.commit_guarded(opened)
    assert W.add_memberships(opened, playlist, ["2", "1"]) == []

    held = sorted(str(song.ContentID) for song in real_read(PlaylistID=str(playlist.ID)))
    assert held == ["1", "2"]


def test_the_tag_primitives_mirror_an_existing_category(opened, cloud_sync_off):
    value = W.ensure_my_tag_value(opened, "a category", "a value")
    W.commit_guarded(opened)
    assert str(value.ParentID) == "10", "the value was not filed under the existing category"

    assert W.add_my_tag(opened, value, "1") is True
    W.commit_guarded(opened)
    assert W.add_my_tag(opened, value, "1") is False


def test_a_library_with_no_tag_category_refuses_rather_than_inventing_one(
    library, cloud_sync_off
):
    """No tag category refuses, since a fabricated one corrupts while looking like success."""
    path = library / "db" / "master.db"
    _build_disposable_database(path, with_tag_category=False)
    db = W.open_db(path, unlock=False)
    try:
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            W.ensure_my_tag_value(db, "a category", "a value")
        assert excinfo.value.cause.reason == "mytag-category-template-missing"
    finally:
        W.close_db(db)


def test_the_commit_refuses_while_the_agent_is_running(opened, cloud_sync_off, monkeypatch):
    """Re-checked at commit, since rekordbox can be launched during a run."""
    row = opened.get_content().first()
    row.ColorID = "4"
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    with pytest.raises(W.RekordboxRunning) as excinfo:
        W.commit_guarded(opened)
    assert excinfo.value.cause.reason == "rekordbox-running"


def test_an_unreadable_cloud_state_refuses_a_commit(opened, monkeypatch):
    """An unreadable cloud state is a writer we cannot rule out, so a commit refuses."""

    def unreadable(*args, **kwargs):
        raise OSError("no rekordbox settings on this machine")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(opened)
    # Its own slug since the split, so the two cases do not share opposite remedies.
    assert excinfo.value.cause.reason == "cloud-sync-unreadable"
    assert "could not be read" in str(excinfo.value)


def test_an_unreadable_cloud_state_does_not_refuse_a_READ(database, monkeypatch):
    """A read must still work without rekordbox settings, or a user could not fix their setup."""

    def unreadable(*args, **kwargs):
        raise OSError("no rekordbox settings on this machine")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    path, unlock = database
    W.close_db(W.open_db(path, unlock=unlock))


# Snapshot, integrity, and the rehearsed restore


def test_a_good_snapshot_passes_its_integrity_check(database, tmp_path, cloud_sync_off):
    path, unlock = database
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    assert W.integrity_ok(snapshot, unlock=unlock) is True


def test_a_damaged_snapshot_fails_its_integrity_check(database, tmp_path, cloud_sync_off):
    """No session commits behind a snapshot that has not verified (U8)."""
    path, unlock = database
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    snapshot.write_bytes(b"truncated beyond recognition")
    assert W.integrity_ok(snapshot, unlock=unlock) is False


def test_a_rehearsed_restore_returns_a_modified_database_to_its_pre_session_state(
    database, tmp_path, cloud_sync_off
):
    """The rehearsal, run: both the bytes and the row must be back, since either alone can lie."""
    path, unlock = database
    db = W.open_db(path, unlock=unlock)
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps", db=db)
    before = _digest(snapshot)

    row = db.get_content().first()
    identifier = row.ID
    row.ColorID = "4"
    W.commit_guarded(db)
    # The FULL release, since a pooled connection holding the log makes the restore fail.
    W.close_db(db)

    W.restore_from_snapshot(snapshot, db_path=path)

    assert _digest(path) == before
    restored = W.open_db(path, unlock=unlock)
    try:
        recovered = restored.get_content(ID=identifier)
        assert recovered.ColorID in (None, "", 0, "0")
    finally:
        W.close_db(restored)


def test_the_binding_close_alone_does_not_release_the_database(database, tmp_path):
    """The binding's close leaves a pooled connection, which ``close_db`` exists to release."""
    path, unlock = database
    db = W.open_db(path, unlock=unlock)
    W.close_db(db)

    # The handle is gone: its sidecars are cleaned up and a fresh reader opens cleanly.
    assert not path.with_name(path.name + "-shm").exists()
    reopened = W.open_db(path, unlock=unlock)
    W.close_db(reopened)


# The lock, held across a real write


def test_the_write_lock_is_held_across_a_real_commit(opened, library, cloud_sync_off):
    """The lock and the write together, since the read then insert is race free only under it."""
    lock = library / "write.lock"
    with W.write_session_lock(lock):
        row = opened.get_content().first()
        row.ColorID = "4"
        W.commit_guarded(opened)
    assert lock.exists(), "the lock file is never unlinked; another holder locks its inode"


def test_the_lock_lands_beside_the_library_not_beside_the_installation(pinned):
    """KTD17 and R31: two installations contend on ONE lock file, beside the library."""
    assert W.write_lock_path(pinned).is_relative_to(pinned.library.root)


# The integration seam itself


def test_the_integration_path_reads_the_environment_and_never_the_live_library(
    monkeypatch, tmp_path
):
    """The seam returns None when unset, never falling back to the live library."""
    monkeypatch.delenv(W.TEST_DB_ENV, raising=False)
    assert W.integration_db_path() is None

    monkeypatch.setenv(W.TEST_DB_ENV, str(tmp_path / "snapshot" / "master.db"))
    assert W.integration_db_path() == tmp_path / "snapshot" / "master.db"


def test_the_battery_reports_which_database_it_ran_against(database):
    """Records whether the strongest half ran, since the synthetic database is not encrypted."""
    path, unlock = database
    supplied = os.environ.get(W.TEST_DB_ENV)
    assert unlock is bool(supplied), (
        "a supplied snapshot is opened with the key; the synthetic database is not"
    )
    assert path.exists()


# Round eight: a permission may never reach "restore from a snapshot"


def test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it(
    database, cloud_sync_off
):
    """THE ADVICE WAS DESTRUCTIVE: a sealed database is a grant, never a restore from snapshot.

    The path is recorded two links down, on the error carrying ``sqlite_errorname``."""
    path, unlock = database
    before = path.stat().st_mode
    path.chmod(0o000)
    try:
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            W.open_db(path, check_app_version=False, unlock=unlock)
        # READ WHILE THE FILE IS STILL SEALED, as the dispatcher reads it, since the
        # classification measures the path.
        error = excinfo.value
        cause = error.cause
    finally:
        path.chmod(before & 0o777)

    assert cause.remediation.remedy is not Remedy.RESTORE_FROM_SNAPSHOT, (
        "a chmod told the user to overwrite the library with an older copy"
    )
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.reason == "path-permission-denied"
    assert cause.detail["path"] == str(path)
    assert cause.detail["access"] == "permission"
    assert str(path) in cause.message

    # The site's own reading is kept, so this test kills the recording alone.
    assert error.declared_cause.reason == "canary-read-failed"

    # The classifiable error is two links down the DECLARED chain.
    chain = []
    current: BaseException | None = error
    while current is not None:
        chain.append(current)
        current = current.__cause__
    assert any(getattr(link, "sqlite_errorname", "") == "SQLITE_CANTOPEN" for link in chain), (
        f"the driver level error left the chain: {[type(link).__name__ for link in chain]}"
    )


def test_a_sealed_sidecar_beside_the_database_is_the_same_answer(database, cloud_sync_off):
    """A sealed playlist sidecar likewise never reaches an instruction to overwrite the library."""
    path, unlock = database
    sidecar = path.parent / W.MASTER_PLAYLIST_XML
    sidecar.write_text("<DJPLAYLISTS/>", encoding="utf-8")
    sidecar.chmod(0o000)
    try:
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            W.open_db(path, check_app_version=False, unlock=unlock)
        cause = excinfo.value.cause
    finally:
        sidecar.chmod(0o600)

    assert excinfo.value.declared_cause.reason == "database-open-failed"
    assert excinfo.value.declared_cause.remediation.remedy is Remedy.RESTORE_FROM_SNAPSHOT
    assert cause.remediation.remedy is Remedy.GRANT_PATH_ACCESS
    assert cause.reason == "path-permission-denied"
    assert cause.detail["path"] == str(sidecar)
