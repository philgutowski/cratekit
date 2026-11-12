"""The guarded writer against a REAL database, a real object-mapper session, and
a real commit.

WHY THIS EXISTS ALONGSIDE THE PURE GUARD SUITE. The pure suite proves the
decisions. It cannot prove the ADAPTER: that the session introspection actually
reports the table a real mapped object belongs to, that a real pending delete is
visible before the commit rather than after it, or that a rolled-back session
really leaves nothing behind. Those are the joints where a ported guard can be
perfectly correct and still guard nothing, and the source system's equivalents
were never covered at all outside a manual run against the author's own library.

WHICH DATABASE IT RUNS AGAINST. A disposable one, built here from the binding's
own schema, in a temporary directory. It is never a copy of anybody's library:
the live database is off limits, and a test that can reach it is a test that
eventually does.

Setting ``CRATEKIT_TEST_DB`` to a snapshot copy points the SAME battery at a
real database instead. The copy is copied again before anything runs, so even a
supplied file is never written to. That is the fixture-presence gate the
verification contract asks for, expressed as a substitution rather than as a
skip: the assertions run either way, and supplying a real snapshot strengthens
them rather than switching them on.

Two things the synthetic database cannot prove, stated plainly rather than left
for a reader to discover: it is not encrypted, so the key path is exercised only
when a real snapshot is supplied, and its column constraints come from the
binding's declaration rather than from what rekordbox actually created.
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

#: The pin the tests record and then satisfy. A shape, not anybody's installed
#: version: what is under test is that an exact comparison is made at all.
RECORDED_APP_VERSION = "9.9.9.0001"


# ---------------------------------------------------------------------------
# Building a disposable database
# ---------------------------------------------------------------------------


def _relaxed_schema():
    """The binding's schema with non-key columns made nullable.

    Copied into a fresh container rather than mutated in place, because the
    binding's own metadata is shared process-wide and relaxing it there would
    quietly change what every other test is running against.

    Relaxed because the declared schema is STRICTER than the database rekordbox
    actually creates: the binding's own playlist-folder helper writes a row that
    its own declaration rejects. A fixture that is stricter than production fails
    on the fixture rather than on the code.
    """
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
    """One mapped row with every timestamp column filled.

    Not a general default-filler. Only the timestamps are supplied, because the
    binding's date type raises on a missing value rather than storing null, which
    makes those columns mandatory in practice whatever the schema says.
    """
    from pyrekordbox.db6 import tables

    now = datetime.now(timezone.utc)
    obj = model(**values)
    for key, column in model.__mapper__.columns.items():
        if isinstance(column.type, tables.DateTime) and getattr(obj, key, None) is None:
            setattr(obj, key, now)
    return obj


#: Each worker's built databases, as bytes, keyed by what a build reads: whether
#: it carries the tag category, and the schema version the pin compares against.
#: The version is read at every call, as a build always read it, so a test that
#: configures another pin before it builds still finds that pin in its file.
#: Bytes rather than a file, so no test can open, write, encrypt or delete the
#: template: every call writes a private copy of its own (U256).
_TEMPLATES: dict[tuple[bool, str], bytes] = {}

#: The files SQLite keeps for a database. A path where any of them is already
#: present is built from nothing, as every path was before U256, rather than
#: having a copy written over it or beside it.
_DATABASE_FILES = ("", "-wal", "-shm", "-journal")


def _build_disposable_database(db_path: Path, *, with_tag_category: bool = True) -> None:
    """Create a database carrying the minimum the safety chain reads.

    Built from nothing once per process for each variant and schema pin, then
    copied, because building it took about 120 ms and was asked for 2,694 times
    in one run of the suite, where a copy takes a fraction of a millisecond
    (U256). Every call gets a file of its own. The one thing a copy carries that
    a fresh build would not is the time its rows were stamped: the first build
    of the variant in this process, not this call. No test reads those stamps
    as fresh; U256's record says how that was driven.
    """
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
    with open(db_path, "xb") as handle:
        handle.write(template)


def _template(*, with_tag_category: bool, db_version: str) -> bytes:
    """One database built from nothing in a directory of its own, read as bytes.

    The directory is removed before this returns, so the template exists only
    in memory. Closing the build's last connection folds the WAL into the main
    file; anything left beside it would be a part of the database a copy of the
    one file lost, so that refuses rather than copying half a database.
    """
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

    # WAL mode, because that is the mode the real database runs in and it is the
    # mode the snapshot pair is built for.
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.commit()
    conn.close()


def _encrypt_in_place(db_path: Path) -> None:
    """Encrypt a disposable database with the key the binding itself supplies.

    THE SHAPE A REAL LIBRARY HAS, built without touching one. Every other
    database in this suite is plain, so an open that never asks for the key
    passes against all of them and fails against every real machine, which is
    R-239. The key is the binding's own default rather than anything read from
    an installation, so the file opens exactly when the binding is asked to
    unlock it.

    The plain file is folded out of WAL first so no sidecar of the plaintext is
    left beside the encrypted copy, then the copy is put back into WAL, the mode
    the real database runs in.
    """
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
    """Configuration with the application pin RECORDED, and an install that matches.

    Recorded rather than defaulted: an unset pin refuses every write (S2), so a
    test of the write path has to record one first, which is the same thing the
    setup wizard makes a user do.
    """
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
    """Whether rekordbox is open on this machine is irrelevant to a temporary database.

    Three probes, patched in three places, and the third one is not optional. The
    two in ``rb_writer`` are patched where the guards RESOLVE them; patching a
    module that merely re-exports the names rebinds nothing a guard reads. The
    third belongs to the binding, whose own commit refuses while rekordbox runs
    and which bound the probe into its module at import.

    Neutralising them here does not weaken the guard under test. That the guard
    refuses a running application is proved directly, twice, by driving the same
    probes the other way.
    """
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)


@pytest.fixture
def cloud_sync_off(monkeypatch):
    """Drive the canary's OFF branch through the real settings reader's seam.

    Patched here rather than by writing a settings file, so the test states the
    marker it depends on instead of encoding a file format rekordbox owns.
    """
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: {W.LIBRARY_SYNC_SETTING: 0}
    )


@pytest.fixture
def database(library, tmp_path):
    """The database under test, and whether it needs the key to open.

    A supplied snapshot wins over the synthetic build, and is COPIED first: the
    battery writes, and writing to a file somebody handed us is not ours to do.
    """
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


# ---------------------------------------------------------------------------
# The open-side gate
# ---------------------------------------------------------------------------


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
    """Distinct from the directory case: an unmounted volume and a deleted file
    have nothing in common except that neither can be opened."""
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
    """Pin 1 has no escape, and it fires on a read as well as on a write.

    A mismatched binding maps table shapes this build was never validated
    against, and a read that mis-maps a column feeds the write that follows it.
    """
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


# ---------------------------------------------------------------------------
# R-239: the key is asked of the file, by the opener, for every caller
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("encrypted", [True, False], ids=["encrypted", "plain"])
def test_an_open_that_names_no_key_opens_either_kind_of_database(
    library, cloud_sync_off, encrypted
):
    """The opener answers the question itself, so no caller can answer it wrong.

    A real library is encrypted and every disposable database is plain. Both
    constant answers fail one of the two, which is how five verb sites came to
    pass ``unlock=False`` and fail at the open on every real machine.
    """
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
    """The fixture is what it claims to be: the binding cannot read it without the key.

    Without this, the test above could pass against a file that was never
    encrypted, and would then say nothing about a real library.
    """
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    _encrypt_in_place(path)
    with pytest.raises(W.RekordboxUnavailable):
        W.close_db(W.open_db(path, unlock=False))


@pytest.mark.parametrize("encrypted", [True, False], ids=["encrypted", "plain"])
def test_a_snapshot_check_that_names_no_key_verifies_either_kind(
    library, tmp_path, cloud_sync_off, encrypted
):
    """The same question one call over, where the constant was ``True``.

    ``snapshot`` calls ``integrity_ok`` with no argument, so a plain database
    failed its capture check and an encrypted one passed; the suite patched the
    check to ``unlock=False`` in every file that wrote.
    """
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    if encrypted:
        _encrypt_in_place(path)
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    assert W.integrity_ok(snapshot) is True


def _unlock_arguments(tree) -> list[tuple[int, str]]:
    """Every call in ``tree`` to an opener that passes ``unlock=`` itself.

    Matched on the called name's last attribute, so ``rb_writer.open_db``,
    ``W.open_db`` and a bare ``open_db`` are all seen. A ``**kwargs`` call counts,
    because it can carry the argument unseen.
    """
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
    """The lines where ``integrity_ok`` passes its own ``unlock`` to ``open_db``.

    Exactly that shape and nowhere else: a call inside the ``integrity_ok``
    definition whose ``unlock`` keyword is the bare name ``unlock``. A literal
    answer typed anywhere in ``rb_writer``, including inside ``integrity_ok``,
    is not a forward and is refused like any other.
    """
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
    """R-239's closing condition as a guard: one function answers, every open asks.

    The single exemption is ``integrity_ok`` forwarding its own argument to
    ``open_db`` inside ``rb_writer``, which is the question passed through rather
    than answered, and it is matched by shape rather than by file.
    """
    import ast

    root = Path(W.__file__).resolve().parents[1]
    problems = []
    scanned = 0
    forwards = 0
    for source in sorted(root.rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        scanned += 1
        forwarded = _forwarded_lines(tree) if source.name == "rb_writer.py" else set()
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
    """The guard's own refusals, driven with literal sources, so the scan above
    cannot be green because the walk stopped recognising a call."""
    import ast

    assert _unlock_arguments(ast.parse(source))


def test_the_key_guard_accepts_an_open_that_asks():
    import ast

    assert _unlock_arguments(ast.parse("rb_writer.open_db(cfg=cfg)")) == []


# ---------------------------------------------------------------------------
# The commit-side gate, against a real session
# ---------------------------------------------------------------------------


def test_a_registered_column_write_commits_and_persists(opened, cloud_sync_off):
    """The one operation that exists at this unit's time, end to end."""
    row = opened.get_content().first()
    assert W.write_metadata_field(row, "track-color", "ColorID", "4") is W.Decision.WRITE
    W.commit_guarded(opened)

    opened.session.expire_all()
    assert str(opened.get_content().first().ColorID) == "4"


def test_an_analysis_column_write_is_refused_and_rolled_back(opened, cloud_sync_off):
    """R17 as a property of a REAL session, not of a hand-built change set.

    The rollback is half the assertion. Leaving the rejected object pending would
    carry it into whatever commits next, so a refused write would land later
    under a different operation's name.
    """
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
    """R14 implemented rather than described.

    The source shipped a maximal union of every column any operation might ever
    want, so on a slim install with no metadata operations enabled four columns
    were still writable for no reason. Here nothing is writable until an
    operation registers it.
    """
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
    """Every delete, from every table, unconditionally, against a real session.

    Additive-only is what makes the snapshot a real safety net: extra rows are
    visible and removable, and a deletion is the one operation whose damage is
    invisible until somebody looks for a track that is gone.
    """
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
    """R-10. One presence read per call, whatever the number of tracks.

    The read is counted at the binding, because the cost R-10 recorded was round
    trips and a correct return value cannot see how many were made. The rows are
    asserted from the database afterwards, so a primitive that read less by
    deciding wrongly fails here too.
    """
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
    """One of the reserved refusals, and why it refuses rather than defaulting.

    The binding defines no constants for a tag row's shape, so the alternative to
    mirroring an existing one is fabricating an attribute value. A fabricated one
    produces rows rekordbox reads as a different kind of object, which is a
    corruption that looks exactly like a successful write.
    """
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
    """Re-checked at commit against a real open session, not only at open.

    A run takes minutes and the user can launch rekordbox during it, so the
    open-time check is a formality without this one.
    """
    row = opened.get_content().first()
    row.ColorID = "4"
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    with pytest.raises(W.RekordboxRunning) as excinfo:
        W.commit_guarded(opened)
    assert excinfo.value.cause.reason == "rekordbox-running"


def test_an_unreadable_cloud_state_refuses_a_commit(opened, monkeypatch):
    """The uncertain case, decided: a state we cannot read is a writer we cannot rule out.

    Deliberately NOT driven through ``cloud_sync_active``, which answers False on
    an unreadable state so that the falsified row-count predicate can never come
    back through it. The refusal lives in its own check with its own message.
    """

    def unreadable(*args, **kwargs):
        raise OSError("no rekordbox settings on this machine")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(opened)
    # Its own reason since the slug split. What this test pins is that an
    # unreadable state refuses a COMMIT against a real session; which slug it
    # refuses under was incidental to that, and sharing one with the
    # genuinely-active case gave two opposite remedies one exit code.
    assert excinfo.value.cause.reason == "cloud-sync-unreadable"
    assert "could not be read" in str(excinfo.value)


def test_an_unreadable_cloud_state_does_not_refuse_a_READ(database, monkeypatch):
    """Because refusing there would break the machine trying to verify a snapshot.

    A read-only open has to keep working with no rekordbox settings at all, or a
    user could not reach the step that fixes their own setup.
    """

    def unreadable(*args, **kwargs):
        raise OSError("no rekordbox settings on this machine")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    path, unlock = database
    W.close_db(W.open_db(path, unlock=unlock))


# ---------------------------------------------------------------------------
# Snapshot, integrity, and the rehearsed restore
# ---------------------------------------------------------------------------


def test_a_good_snapshot_passes_its_integrity_check(database, tmp_path, cloud_sync_off):
    path, unlock = database
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    assert W.integrity_ok(snapshot, unlock=unlock) is True


def test_a_damaged_snapshot_fails_its_integrity_check(database, tmp_path, cloud_sync_off):
    """The gate U8 puts in front of every commit: no session commits behind a
    snapshot that has not verified."""
    path, unlock = database
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps")
    snapshot.write_bytes(b"truncated beyond recognition")
    assert W.integrity_ok(snapshot, unlock=unlock) is False


def test_a_rehearsed_restore_returns_a_modified_database_to_its_pre_session_state(
    database, tmp_path, cloud_sync_off
):
    """The rehearsal, run rather than asserted.

    Snapshot through the open handle so the checkpoint folds the log into the
    file, write and commit a real change, restore, and require both the bytes and
    the row to be back. Comparing only the row would pass against a restore that
    left a stale log beside the file; comparing only the bytes would pass against
    a restore that never opened.
    """
    path, unlock = database
    db = W.open_db(path, unlock=unlock)
    snapshot = W.snapshot_db(path, stamp="s", root=tmp_path / "snaps", db=db)
    before = _digest(snapshot)

    row = db.get_content().first()
    identifier = row.ID
    row.ColorID = "4"
    W.commit_guarded(db)
    # The FULL release, not the binding's session close, which leaves a pooled
    # connection holding the log and the shared-memory index. Restoring under one
    # produces an input-output error against a database that is actually intact.
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
    """The gap ``close_db`` exists to cover, asserted so it cannot silently return.

    The binding's close ends the session and leaves the engine's pooled
    connection open, so the process still holds the log and the shared-memory
    index. A restore then replaces those files underneath a live connection and
    the next reader gets an input-output error against a database that is
    perfectly intact, which reads as a corrupted recovery and is not one.
    """
    path, unlock = database
    db = W.open_db(path, unlock=unlock)
    W.close_db(db)

    # The proof that the handle really is gone: the sidecars a live connection
    # keeps open have been cleaned up, and a fresh reader opens cleanly.
    assert not path.with_name(path.name + "-shm").exists()
    reopened = W.open_db(path, unlock=unlock)
    W.close_db(reopened)


# ---------------------------------------------------------------------------
# The lock, held across a real write
# ---------------------------------------------------------------------------


def test_the_write_lock_is_held_across_a_real_commit(opened, library, cloud_sync_off):
    """The lock and the write together, since the lock exists for this exact shape.

    The membership helper's read-then-insert and the update counter's
    autoincrement are race-free only under it, so a commit outside it is unsafe
    for two reasons rather than one.
    """
    lock = library / "write.lock"
    with W.write_session_lock(lock):
        row = opened.get_content().first()
        row.ColorID = "4"
        W.commit_guarded(opened)
    assert lock.exists(), "the lock file is never unlinked; another holder locks its inode"


def test_the_lock_lands_beside_the_library_not_beside_the_installation(pinned):
    """KTD17 and R31. Two installations must contend on ONE file.

    In the source system this lock sat under the installation root while the
    database it protects travelled with the library, so a second install held a
    lock the first could not see and both opened one database at once.
    """
    assert W.write_lock_path(pinned).is_relative_to(pinned.library.root)


# ---------------------------------------------------------------------------
# The integration seam itself
# ---------------------------------------------------------------------------


def test_the_integration_path_reads_the_environment_and_never_the_live_library(
    monkeypatch, tmp_path
):
    """The seam that lets this battery point at a real snapshot, asserted directly.

    It returns None when unset rather than falling back to the configured
    library, which is the whole safety property: a test that can silently reach
    the live database is a test that eventually does.
    """
    monkeypatch.delenv(W.TEST_DB_ENV, raising=False)
    assert W.integration_db_path() is None

    monkeypatch.setenv(W.TEST_DB_ENV, str(tmp_path / "snapshot" / "master.db"))
    assert W.integration_db_path() == tmp_path / "snapshot" / "master.db"


def test_the_battery_reports_which_database_it_ran_against(database):
    """A one-line record of whether the strongest half of this gate actually ran.

    The synthetic database proves the adapter and the decisions. It does not
    prove the key path, because it is not encrypted. Saying so in an assertion
    rather than in a comment means the claim cannot quietly become false.
    """
    path, unlock = database
    supplied = os.environ.get(W.TEST_DB_ENV)
    assert unlock is bool(supplied), (
        "a supplied snapshot is opened with the key; the synthetic database is not"
    )
    assert path.exists()


# ---------------------------------------------------------------------------
# Round eight: a permission may never reach "restore from a snapshot"
# ---------------------------------------------------------------------------


def test_a_sealed_database_is_a_grant_rather_than_an_order_to_overwrite_it(
    database, cloud_sync_off
):
    """THE ADVICE WAS DESTRUCTIVE, NOT MERELY WRONG.

    ``canary-read-failed`` sits on the library-unreadable band, whose declared
    remedy is ``restore-from-snapshot``, and over a ``chmod 000`` that sends the
    user to overwrite library state they still have. Every earlier finding in this
    unit was a wrong message; this one destroys data if followed.

    WHY IT WAS UNCLASSIFIED. The binding opens lazily, so a sealed file passes the
    open and fails at the canary's two reads, and what comes back is an object
    mapper error wrapping a ``sqlite3.OperationalError``: no errno, no filename,
    no path anywhere. ``queue.db`` and ``review.db`` are answered correctly
    because their connection sites record the path; this one did not, so the one
    thing the classification measures was absent and the destructive default
    stood.

    The chain is asserted rather than assumed, because the path has to be recorded
    on the exception two links down that actually carries ``sqlite_errorname``,
    not on the wrapper a handler can see.
    """
    path, unlock = database
    before = path.stat().st_mode
    path.chmod(0o000)
    try:
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            W.open_db(path, check_app_version=False, unlock=unlock)
        # READ WHILE THE FILE IS STILL SEALED, which is when the dispatcher reads
        # it. The classification MEASURES the path rather than trusting the
        # driver's sentence, so a condition that has already cleared correctly
        # claims nothing, and restoring the mode first would test the clearing.
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

    # The site's own reading is kept and is exactly what it was, so the row this
    # test kills is the recording rather than anything downstream of it.
    assert error.declared_cause.reason == "canary-read-failed"

    # The shape the recording had to cross: the classifiable error is two links
    # down the DECLARED chain, under a wrapper that carries none of its fields.
    chain = []
    current: BaseException | None = error
    while current is not None:
        chain.append(current)
        current = current.__cause__
    assert any(getattr(link, "sqlite_errorname", "") == "SQLITE_CANTOPEN" for link in chain), (
        f"the driver level error left the chain: {[type(link).__name__ for link in chain]}"
    )


def test_a_sealed_sidecar_beside_the_database_is_the_same_answer(database, cloud_sync_off):
    """THE OTHER HALF OF THE SAME CONNECTION, and the same destructive default.

    ``database-open-failed`` shares the canary's band and therefore shares
    ``restore-from-snapshot``. The binding reads rekordbox's own legacy playlist
    file while it constructs, and that file travels with the database through
    every snapshot and restore, so a mode on it is a state a real library reaches.

    A sealed sidecar is refused as a ``PermissionError``, which carries its own
    filename, so this leg needs no hand-off to be classifiable. It is driven
    anyway because the property being asserted is not "the hand-off works", it is
    that NO permission reaches an instruction to overwrite the library.
    """
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
