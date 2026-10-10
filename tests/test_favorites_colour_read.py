"""The favourites colour read against a real open, and a library that is not there.

The suite's autouse stub replaces ``read_pink_track_ids`` everywhere else, so
every test here is marked ``real_pink_read`` and reaches ``rb_writer``. A
missing database must stop both verbs with the open's own cause, never an
internal error, and under ``crate sync all`` it is the favourites source's
refusal while the rest of the pass still runs.
"""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import cli as favorites_cli
from tests.cli_drive import drive
from tests.test_outbound_workers import favorites_verb
from tests.test_rb_writer_db import _build_disposable_database, _row
from tests.test_sync_all import _confirmed, exported, installed  # noqa: F401

pytestmark = pytest.mark.real_pink_read


@pytest.fixture
def closed(monkeypatch):
    """Rekordbox and its agent read as closed, which a temporary library cannot say."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)


@pytest.mark.parametrize("gone", ["file", "directory"])
def test_a_missing_database_is_the_opens_own_cause_under_sync_favorites(
    installed, exported, closed, monkeypatch, gone  # noqa: F811
):
    target = installed.library.root / "absent" / "master.db"
    if gone == "file":
        target.parent.mkdir(parents=True)
    monkeypatch.setattr(rb_writer, "live_db_path", lambda cfg=None: target)

    code, refused = drive(favorites_verb(exported))

    assert code != int(ExitCode.OK), refused
    expected = "library-database-missing" if gone == "file" else "library-directory-missing"
    assert refused["cause"]["reason"] == expected, refused


def test_a_missing_database_is_the_favourites_refusal_under_sync_all(
    installed, exported, closed, monkeypatch  # noqa: F811
):
    target = installed.library.root / "absent" / "master.db"
    target.parent.mkdir(parents=True)
    monkeypatch.setattr(rb_writer, "live_db_path", lambda cfg=None: target)

    code, envelope = drive(["sync", "all", "--export", str(exported)])

    # EVERY SOURCE REFUSES ON ITS OWN HERE, no provider session being stored, so
    # the pass ends refused and names each source's reason. The favourites
    # source's is the open's own cause, and the hearts listing was still asked.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] != "internal-error", envelope
    sources = envelope["cause"]["detail"]["sources"]
    assert sources["summary"]["not_queued"]["favorites"] == "library-database-missing"
    checks = {check["key"]: check for check in sources["checks"]}
    assert checks["sync.favorites"]["remedy"] == "mount-library-volume"
    assert "sync.favorites.inbound" in checks


def test_the_real_read_finds_the_pink_row_in_a_disposable_library(installed, closed, monkeypatch):  # noqa: F811
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    target = installed.library.root / "disposable" / "master.db"
    _build_disposable_database(target)
    engine = create_engine(f"sqlite:///{target}")
    with Session(engine) as session:
        session.add(_row(tables.DjmdColor, ID="1", ColorCode=1, SortKey=1, Commnt="Pink"))
        session.add(_row(tables.DjmdColor, ID="2", ColorCode=2, SortKey=2, Commnt="Red"))
        session.query(tables.DjmdContent).filter_by(ID="1").update({"ColorID": "1"})
        session.query(tables.DjmdContent).filter_by(ID="2").update({"ColorID": "2"})
        session.commit()
    engine.dispose()
    monkeypatch.setattr(rb_writer, "live_db_path", lambda cfg=None: target)

    assert favorites_cli.read_pink_track_ids(installed) == ("1",)
