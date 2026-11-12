"""``crate organize --report`` opens the library once (U267).

Every step that reads the database used to open its own handle, so a report
paid the whole open path five to seven times: the key derivation, the
binding's configuration read, the process walk, the canary, the schema pin
and the foreign tree read. The report now opens one read handle at its first
read, hands it to every reader and closes it on every way out. The run that
answers a gate is not changed: its plans read and its writes open as before.

Every count here was measured on the base before the change: the ``world``
report made seven opens and its applying run, both gates answered, 26,
two of them the snapshot's integrity check on its copy.

The database is always the suite's disposable fixture.
"""

from __future__ import annotations

import re
import sqlite3
import sys
from typing import Any

import pytest
from sqlalchemy import text

from cratekit.core import rb_writer
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import rotate
from cratekit.organize import account as account_area
from cratekit.organize import own
from tests.cli_drive import drive
from tests.test_organize import (
    SET_NAME,
    VERB,
    _answered,
    _inspiration,
    _no_intake_file,
    _report,
    _steps,
)
from tests.test_organize import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_organize import machine as machine  # noqa: PLC0414
from tests.test_organize import seams as seams  # noqa: PLC0414
from tests.test_organize import world as world  # noqa: PLC0414

# ---------------------------------------------------------------------------
# What every open and every close was, counted at the binding's seam
# ---------------------------------------------------------------------------


class Opens:
    """Every ``open_db`` and ``close_db``, with the reader that called it."""

    def __init__(self, monkeypatch) -> None:
        self.opened: list[tuple[str, bool, Any]] = []
        self.closed: list[Any] = []
        real_open, real_close = rb_writer.open_db, rb_writer.close_db

        def opening(*args, **kwargs):
            caller = sys._getframe(1).f_code.co_name
            db = real_open(*args, **kwargs)
            self.opened.append((caller, bool(kwargs.get("require_closed", False)), db))
            return db

        def closing(db):
            self.closed.append(db)
            return real_close(db)

        monkeypatch.setattr(rb_writer, "open_db", opening)
        monkeypatch.setattr(rb_writer, "close_db", closing)

    @property
    def handles(self) -> list[Any]:
        return [db for _caller, _write, db in self.opened]

    def each_closed_once(self) -> bool:
        return all(sum(1 for one in self.closed if one is db) == 1 for db in self.handles)


def _without_sharing(monkeypatch) -> None:
    """The report as it was before U267: no shared read, so every reader opens its own."""
    monkeypatch.setattr(rb_writer, "SharedRead", lambda _cfg=None: None)


_SECONDS = re.compile(r"in [0-9.]+ s\b")


def _said(envelope: dict) -> tuple[dict, list]:
    """What a report says, its timing aside, which no two runs share."""
    data = _SECONDS.sub("in N s", repr(envelope["data"]))
    warnings = _SECONDS.sub("in N s", repr(envelope.get("warnings")))
    return data, warnings


# ---------------------------------------------------------------------------
# One open, one close
# ---------------------------------------------------------------------------


def test_the_report_opens_the_database_once_and_closes_it_once(world, monkeypatch):
    opens = Opens(monkeypatch)

    _report()

    assert len(opens.opened) == 1, [caller for caller, _w, _db in opens.opened]
    ((caller, write, db),) = opens.opened
    assert caller == "handle" and write is False
    assert opens.closed == [db]


def test_the_report_says_exactly_what_it_said_with_an_open_per_step(world, monkeypatch):
    shared = _report()
    with monkeypatch.context() as patched:
        opens = Opens(patched)
        _without_sharing(patched)
        separate = _report()
        # THE COMPARISON IS AGAINST THE OLD SHAPE, measured: seven opens.
        assert len(opens.opened) == 7 and opens.each_closed_once()

    assert _said(shared) == _said(separate)
    for area in ("rekordbox", "account"):
        assert _steps(shared, area) == _steps(separate, area)


def test_an_open_that_refuses_refuses_each_step_as_its_own_open_did(world, monkeypatch):
    """A failed open is not kept: the next reader asks again, as its own open did."""
    attempts: list[int] = []

    def refusing(*_args, **kwargs):
        attempts.append(1)
        assert kwargs.get("require_closed", False) is False
        raise rb_writer._unavailable("library-database-missing", "there is no database here")

    monkeypatch.setattr(rb_writer, "open_db", refusing)
    shared = _report()
    asked = len(attempts)
    attempts.clear()
    _without_sharing(monkeypatch)
    separate = _report()

    # AS MANY ATTEMPTS AS READERS THAT REACHED THEIR OPEN, five, measured on
    # the base; a refusal kept and handed on would make it one.
    assert asked == len(attempts) == 5
    assert _said(shared) == _said(separate)
    refused = [
        step["step"]
        for step in shared["data"]["summary"]["areas"]["rekordbox"]["steps"]
        if step.get("reason") == "library-database-missing"
    ]
    assert len(refused) >= 4, refused


# ---------------------------------------------------------------------------
# Every way out closes it
# ---------------------------------------------------------------------------


def test_a_step_that_refuses_after_the_open_leaves_no_handle_open(world, monkeypatch):
    opens = Opens(monkeypatch)

    def refusing(*_args, **_kwargs):
        raise rb_writer._unavailable("canary-read-failed", "the rotation refused on purpose")

    monkeypatch.setattr(rotate, "plan_rotation", refusing)
    envelope = _report()

    assert _steps(envelope, "rekordbox")["rotate"]["state"] == "refused"
    assert len(opens.opened) == 1 and opens.each_closed_once()


def test_a_failure_nobody_expected_still_closes_the_handle(world, monkeypatch):
    opens = Opens(monkeypatch)

    def failing(*_args, **_kwargs):
        raise RuntimeError("a defect in the middle of the report")

    # AFTER THE READ OF THE AUTHOR'S OWN LISTING, so the handle is open when
    # the report fails.
    monkeypatch.setattr(own, "rekordbox_home", failing)
    code, envelope = drive([*VERB, "--report"])

    assert code != int(ExitCode.OK), envelope
    assert len(opens.opened) == 1 and opens.each_closed_once()


# ---------------------------------------------------------------------------
# The run that answers a gate is not changed
# ---------------------------------------------------------------------------

#: The applying run's opens on the base, both gates answered by their two
#: acts and the run that writes, in order: who opened, and whether to write.
APPLYING = (
    *(
        ("read_collection", False),
        ("_read_tree", False),
        ("planned", False),
        ("reading", False),
        ("read_library", False),
        ("add_step", False),
        ("_yours", False),
    )
    * 2,
    ("read_collection", False),
    ("_read_tree", False),
    ("planned", False),
    ("reading", False),
    ("add_step", False),
    ("_yours", False),
    ("_read_tree", False),
    ("_write_memberships", True),
    ("integrity_ok", False),
    ("refresh_additive", True),
    ("written", True),
    ("integrity_ok", False),
)


def test_the_applying_run_opens_exactly_as_it_did(world, monkeypatch):
    def never(*_args, **_kwargs):
        raise AssertionError("a run that answers a gate made a shared read")

    opens = Opens(monkeypatch)
    monkeypatch.setattr(rb_writer, "SharedRead", never)

    code, done, _first = _answered()

    assert code == int(ExitCode.OK), done
    assert tuple((caller, write) for caller, write, _db in opens.opened) == APPLYING
    assert opens.each_closed_once()


# ---------------------------------------------------------------------------
# The readers a set or a selection reaches
# ---------------------------------------------------------------------------


def test_the_sets_step_reads_inspiration_through_the_one_handle(world, monkeypatch):
    cfg = world[0]
    _no_intake_file(cfg)
    _inspiration(cfg, SET_NAME)
    shared = _report()
    with monkeypatch.context() as patched:
        _without_sharing(patched)
        separate = _report()
    opens = Opens(monkeypatch)

    again = _report()

    step = _steps(again, account_area.AREA)[f"archive:{SET_NAME}"]
    assert step["state"] == "planned", step
    # EIGHT READERS, one open: the brief's seven and the INSPIRATION listing.
    assert len(opens.opened) == 1 and opens.each_closed_once()
    assert _said(shared) == _said(separate) == _said(again)


def test_a_selection_that_reads_no_database_opens_none(world, monkeypatch):
    opens = Opens(monkeypatch)

    code, envelope = drive([*VERB, "--report", "--only", account_area.FILE])

    assert code == int(ExitCode.OK), envelope
    assert opens.opened == []


# ---------------------------------------------------------------------------
# The shared read alone
# ---------------------------------------------------------------------------


def _first_playlist(db) -> Any:
    return sorted(db.get_playlist(), key=lambda row: str(row.ID))[0]


def _probe(cfg) -> bool:
    """Whether another connection could take the whole database for writing right now."""
    conn = sqlite3.connect(cfg.library.db_path, timeout=0)
    try:
        conn.execute("BEGIN EXCLUSIVE")
        conn.rollback()
        return True
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()


def test_a_shared_read_opens_at_its_first_read_and_once(world, monkeypatch):
    cfg = world[0]
    opens = Opens(monkeypatch)
    shared = rb_writer.SharedRead(cfg)

    assert opens.opened == []
    first = shared.handle()
    rb_writer.done_reading(first, shared)
    second = shared.handle()

    assert first is second and len(opens.opened) == 1
    assert opens.opened[0][1] is False, "opened with read intent"
    assert opens.closed == []
    shared.close()
    shared.close()
    assert opens.closed == [first]


def test_a_shared_read_asks_again_after_an_open_that_refused(world, monkeypatch):
    cfg = world[0]
    real = rb_writer.open_db
    attempts: list[int] = []

    def once_refusing(*args, **kwargs):
        attempts.append(1)
        if len(attempts) == 1:
            raise rb_writer._unavailable("database-open-failed", "not this time")
        return real(*args, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", once_refusing)
    shared = rb_writer.SharedRead(cfg)

    with pytest.raises(CratekitError) as refused:
        shared.handle()
    assert refused.value.cause.reason == "database-open-failed"
    db = shared.handle()
    shared.close()

    assert len(attempts) == 2 and db is not None


def test_a_release_forgets_every_row_so_the_next_reader_reads_afresh(world):
    cfg = world[0]
    shared = rb_writer.SharedRead(cfg)
    try:
        db = shared.handle()
        row = _first_playlist(db)
        playlist_id, was = str(row.ID), str(row.Name)
        conn = sqlite3.connect(cfg.library.db_path)
        conn.execute("UPDATE djmdPlaylist SET Name = ? WHERE ID = ?", ("Renamed elsewhere", playlist_id))
        conn.commit()
        conn.close()
        # THE CONTROL: unreleased, the session answers the row it loaded.
        assert str(db.get_playlist(ID=playlist_id).Name) == was
        rb_writer.done_reading(db, shared)

        again = shared.handle().get_playlist(ID=playlist_id)

        assert str(again.Name) == "Renamed elsewhere"
    finally:
        shared.close()


def test_a_released_handle_holds_no_lock_while_the_report_waits(world):
    """The report holds its handle across provider calls, so it must hold no lock there.

    IN THE ROLLBACK JOURNAL, the stricter mode, where a reader's lock keeps
    every writer out; in WAL a reader blocks no writer at all. The fixture is
    disposable, so its mode is switched for the probe.
    """
    cfg = world[0]
    conn = sqlite3.connect(cfg.library.db_path)
    ((mode,),) = conn.execute("PRAGMA journal_mode=DELETE").fetchall()
    conn.close()
    assert str(mode).lower() == "delete"
    shared = rb_writer.SharedRead(cfg)
    try:
        db = shared.handle()
        # THE CONTROL: a statement still open holds the database.
        open_statement = db.session.execute(text("SELECT ID FROM djmdContent"))
        open_statement.fetchone()
        assert _probe(cfg) is False
        open_statement.close()
        _first_playlist(db)
        rb_writer.done_reading(db, shared)

        assert _probe(cfg) is True
    finally:
        shared.close()


def test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close(world):
    cfg = world[0]
    shared = rb_writer.SharedRead(cfg)
    other = rb_writer.open_db(cfg.library.db_path, cfg=cfg)
    try:
        shared.handle()
        with pytest.raises(CratekitError) as foreign:
            rb_writer.done_reading(other, shared)
        assert foreign.value.cause.reason == "internal-error"
    finally:
        rb_writer.close_db(other)
        shared.close()

    with pytest.raises(CratekitError) as after:
        shared.handle()
    assert after.value.cause.reason == "internal-error"


def test_a_reader_with_no_shared_read_closes_its_own_handle(world, monkeypatch):
    cfg = world[0]
    opens = Opens(monkeypatch)
    db = rb_writer.open_db(cfg.library.db_path, cfg=cfg)

    rb_writer.done_reading(db, None)

    assert opens.closed == [db]


def test_the_inspiration_opener_refuses_to_write_through_a_shared_read(world):
    from cratekit.export import set_cli

    cfg = world[0]
    shared = rb_writer.SharedRead(cfg)
    try:
        with pytest.raises(CratekitError) as refused:
            with set_cli._inspiration_folder(cfg, read_only=False, one_read=shared):
                pass
        assert refused.value.cause.reason == "internal-error"
    finally:
        shared.close()
