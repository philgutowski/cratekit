"""The guarded writer's refusals: whitelist, two-process refuse, pin, canary, lock.

Every assertion here is ported unchanged in substance from the source system's
guard suite. It is pure and seamed: no live database, no real library, no
rekordbox. That is not a limitation, it is the design. A guard that can only be
tested against a real database is a guard that gets tested rarely, and rarely is
how the source system nearly lost a library.

What the layer this file guards actually promises, and why each promise is
load-bearing rather than decorative:

* **An additive whitelist.** A write session may CREATE rows only in named
  playlist and tag tables, may MODIFY only a named column subset of the content
  table, and may DELETE nothing at all, ever. The commit is rolled back
  otherwise. This is what makes grid and analysis data structurally unwritable
  rather than merely untested, which is R17 stated as a database property.
* **A two-process refusal.** Both the application and its background agent are
  checked, at open and again at commit. The agent is the one that gets missed:
  it mutates the database through cloud sync with the application closed, so
  checking only the application leaves the exact window a long write runs in.
* **A version pin.** The library binding, the schema version, and the installed
  application version. Drift refuses rather than guessing.
* **A cloud canary.** Wired to refuse, deliberately never claiming a positive on
  a signal known to be false. See the parametrized test below, which encodes a
  three-day outage.
* **A cross-process write-session lock**, held from snapshot through smoke test.

WHY THIS FILE IS SKIPPED TODAY. U6 ports the guards before the engine on
purpose, so a violation cannot be introduced silently between now and U7. The
module these assertions run against lands in U7. The bodies are complete and
unweakened, the production module is NOT stubbed to make them green, and
tests/test_pending_units.py fails the build the moment U7 lands unless the skip
is removed. A stub would turn a real guard into a test of the stub.
"""

from __future__ import annotations

import multiprocessing as mp

import pytest

from tests._pending import requires

# Gate the whole module. The import below is deliberately tolerant rather than a
# hard import, because a module-level ImportError happens at COLLECTION time,
# before any skip mark is consulted, and would take the whole suite down.
pytestmark = requires("cratekit.core.rb_writer")

try:  # pragma: no cover - the success branch arrives with U7
    from cratekit.core import rb_writer as W
except ImportError:  # pragma: no cover - the state until U7 lands
    W = None


# ── the pure whitelist judge ─────────────────────────────────────────────────


def test_permitted_playlist_and_mytag_writes_pass():
    new = [
        ("djmdPlaylist", set()),
        ("djmdSongPlaylist", set()),
        ("djmdMyTag", set()),
        ("djmdSongMyTag", set()),
    ]
    dirty = [("djmdContent", {"ColorID"})]  # the favourites colour write
    assert W.guard_violations(new, dirty, []) == []


def test_creating_a_track_row_is_forbidden():
    """New content rows mean new-track intake, and intake stays in XML.

    The reason is R15's safety chain: an XML import is something the user
    performs, reviews, and can undo from rekordbox. A row conjured into the
    database directly is none of those things.
    """
    violations = W.guard_violations([("djmdContent", set())], [], [])
    assert len(violations) == 1
    assert "djmdContent" in violations[0] and "intake" in violations[0]


@pytest.mark.parametrize(
    "column", ["BPM", "Analysed", "AnalysisDataPath", "CueUpdated", "AnalysisUpdated"]
)
def test_writing_a_grid_or_analysis_column_is_forbidden(column):
    """R17 as a structural property of the database, not a code review note."""
    violations = W.guard_violations([], [("djmdContent", {column})], [])
    assert len(violations) == 1 and column in violations[0]


def test_new_row_in_unlisted_table_is_forbidden():
    """The whitelist is a whitelist. An unnamed table is refused, not inspected."""
    violations = W.guard_violations([("djmdBeatGrid", set())], [], [])
    assert len(violations) == 1 and "djmdBeatGrid" in violations[0]


def test_deletes_are_forbidden_additive_only():
    """Every delete, from every table, unconditionally.

    Additive-only is what makes the snapshot a real safety net: if nothing is
    ever removed, the worst outcome of a bad run is extra rows, which a person
    can see and remove. Deletion is the one operation whose damage is invisible.
    """
    violations = W.guard_violations([], [], ["djmdSongPlaylist"])
    assert len(violations) == 1 and "additive-only" in violations[0]


def test_bookkeeping_columns_are_ignored_on_dirty_content():
    """The binding bumps sync counters and timestamps on commit by itself.

    Those must not trip the guard, or every legitimate write fails and the guard
    gets disabled, which is the failure mode that actually loses data.
    """
    assert (
        W.guard_violations([], [("djmdContent", {"usn", "rb_local_usn", "updated_at"})], [])
        == []
    )


def test_mixed_session_reports_every_violation():
    """All of them, not the first. A guard that stops at the first finding turns
    one review into several."""
    violations = W.guard_violations(
        [("djmdContent", set()), ("djmdPlaylist", set())],  # one forbidden, one fine
        [("djmdContent", {"BPM", "ColorID"})],  # BPM forbidden, ColorID fine
        ["djmdMyTag"],  # every delete forbidden
    )
    assert len(violations) == 3


# ── the whitelist over a session object ──────────────────────────────────────


class _FakeAttr:
    def __init__(self, key, changed):
        self.key = key
        self._changed = changed

    @property
    def history(self):
        outer = self

        class _History:
            def has_changes(self_inner):
                return outer._changed

        return _History()


class _FakeObj:
    def __init__(self, table, changed_cols):
        class _Table:
            name = table

        self.__table__ = _Table()
        self._attrs = [_FakeAttr(col, True) for col in changed_cols]


class _FakeSession:
    def __init__(self, new=(), dirty=(), deleted=()):
        self.new = list(new)
        self.dirty = list(dirty)
        self.deleted = list(deleted)


@pytest.fixture
def patch_inspect(monkeypatch):
    """Make the ORM's introspection return our fake attribute set.

    Seaming here rather than building real ORM objects keeps the test about the
    guard's decision, which is the part that must never regress, instead of about
    the ORM's object lifecycle, which is not ours.
    """
    import sqlalchemy

    def fake_inspect(obj):
        class _State:
            attrs = obj._attrs

        return _State()

    monkeypatch.setattr(sqlalchemy, "inspect", fake_inspect)


def test_assert_whitelisted_passes_pink_write(patch_inspect):
    session = _FakeSession(dirty=[_FakeObj("djmdContent", {"ColorID"})])
    W.assert_session_whitelisted(session)  # no raise


def test_assert_whitelisted_rejects_beatgrid_write(patch_inspect):
    session = _FakeSession(dirty=[_FakeObj("djmdContent", {"BPM"})])
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_session_whitelisted(session)
    assert "BPM" in str(excinfo.value)


# ── the two-process refusal ──────────────────────────────────────────────────


def test_processes_running_reports_both_names(monkeypatch):
    monkeypatch.setattr(W, "rekordbox_running", lambda: True)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    assert W.rekordbox_processes_running() == "rekordbox, rekordboxAgent"


def test_agent_only_is_reported(monkeypatch):
    """The gap this check was added to close.

    The background agent mutates the database through cloud sync while the
    application is closed. Checking only the application declares the coast clear
    during exactly the window a long write runs in.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    assert W.rekordbox_processes_running() == "rekordboxAgent"


def test_commit_guarded_refuses_when_agent_running(monkeypatch):
    """Checked again at COMMIT, not only at open.

    A run can take minutes. The user can launch rekordbox during it. Re-checking
    at commit is what makes the open-time check more than a formality.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    with pytest.raises(W.RekordboxRunning) as excinfo:
        W.commit_guarded(object())
    assert "rekordboxAgent" in str(excinfo.value)


# ── the application version pin ──────────────────────────────────────────────


def test_app_version_pin_refuses_on_drift(monkeypatch):
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "7.3.0.0001")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    message = str(excinfo.value)
    assert "7.3.0.0001" in message and str(W.pinned_app_version()) in message


def test_app_version_pin_passes_on_match(monkeypatch):
    monkeypatch.setattr(W, "read_installed_app_version", lambda: W.pinned_app_version())
    W.assert_app_version()  # no raise


def test_app_version_pin_skips_when_app_not_found(monkeypatch):
    """A missing application warns and continues; the schema pin still guards.

    Refusing here would break every headless and CI run for no safety gain: if
    the application is not installed, it cannot be holding the database open.
    """
    monkeypatch.setattr(W, "read_installed_app_version", lambda: None)
    W.assert_app_version()  # no raise


# ── the cloud-sync canary ────────────────────────────────────────────────────


class _FakeDB:
    def __init__(self, cloud_rows):
        self._rows = cloud_rows

    class _Session:
        def __init__(self, rows):
            self._rows = rows

        def execute(self, *_args, **_kwargs):
            rows = self._rows

            class _Result:
                def scalar(self_inner):
                    return rows

            return _Result()

    @property
    def session(self):
        return _FakeDB._Session(self._rows)


@pytest.mark.parametrize("rows", [0, 1, 2])
def test_cloud_sync_reports_undetectable(rows):
    """No usable predicate exists, so the probe never claims a positive.

    A registry row USED to be read as "sync is active". A real library carried
    one for years with cloud sync switched off, so that predicate refused every
    open for three days. Refusing on a signal known to be false is the
    blocks-blindly failure this guard exists to avoid. The live protection is the
    agent process check, not this. Encoded as a test so nobody re-derives the
    plausible-looking predicate and repeats the outage.
    """
    assert W.cloud_sync_active(_FakeDB(cloud_rows=rows)) is False


def test_commit_guarded_refuses_on_active_cloud(monkeypatch):
    """The refusal path stays wired for the day a real predicate lands.

    Driven at the seam rather than through the falsified registry count, so the
    wiring is proved without reinstating the false predicate.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(W, "cloud_sync_active", lambda _db: True)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(_FakeDB(cloud_rows=0))
    assert "Cloud Library Sync" in str(excinfo.value)


# ── the cross-process write-session lock ─────────────────────────────────────


def _hold_lock(path, ready, release):
    with W.write_session_lock(path):
        ready.set()
        release.wait(timeout=10)


def test_second_writer_refuses_while_lock_held(tmp_path):
    """A real second PROCESS, not a second call in this one.

    An in-process test would pass against a lock implemented with a module-level
    flag, which protects nothing: the case that matters is two runs started from
    two terminals against one library.
    """
    lock = tmp_path / "rb_writer.lock"
    ctx = mp.get_context("fork")
    ready, release = ctx.Event(), ctx.Event()
    holder = ctx.Process(target=_hold_lock, args=(lock, ready, release))
    holder.start()
    try:
        assert ready.wait(timeout=10), "holder never acquired the lock"
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            with W.write_session_lock(lock):
                pass
        assert "write-session lock" in str(excinfo.value)
    finally:
        release.set()
        holder.join(timeout=10)
    # Once released, the lock is acquirable again. Without this the test would
    # pass against a lock that never releases, which is its own outage.
    with W.write_session_lock(lock):
        pass
