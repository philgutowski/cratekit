"""U8: the destructive-session boundary, its lock, and its acknowledgment.

The plan's test scenarios for this unit, one test per scenario, plus the two
standing debts it is on the hook to close.

* AE5. A session with no recorded acknowledgment parks blocked and names the fix.
* AE19. A second process refuses while the library lock is held, and names the
  holder.
* AE20. Every affirmative flag and configuration key together still leaves the
  acknowledgment required (R34).
* A non-interactive, agent-shaped invocation cannot mint an acknowledgment.
* A multi-source run refused at source two leaves source one committed and names
  both states; a resume skips source one (R29).
* A commit whose read-back disagrees ends ``committed-unverified``, advances
  nothing, and refuses the next write session (AE13).
* A capture that fails its integrity check blocks the commit behind it.
* A run holding an un-imported XML output reports that state and refuses to write
  a database surface for a row that does not exist.
* A nested session acquisition in one process is refused as a programming error
  rather than reported as a foreign lock holder.

Plus:

* R-8. The backup restore passes the same gates, because KTD24 binds them to
  destruction and a restore destroys while writing no database row.
* The runtime half of R17's fifth surface: a real analysis file is moved while a
  session is open and the session refuses.

Everything is hermetic. The volume identity, the terminal probe, the process
liveness answer and the database handle are all injected, so no test depends on
what is mounted, what is running, or whether anybody is sitting at a terminal.
"""

from __future__ import annotations

import inspect
import json
import os
import re
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import config, preflight, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup
from tests._pending import requires
from tests.test_config import valid_data

UTC = timezone.utc

#: The identity the fixture library records. Read from the config rather than
#: restated, wherever it is used.
_ELSEWHERE = "0000-0000-not-this-disk"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(
        valid_data(
            library,
            backup={
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        )
    )
    config.state_path("rekordbox_db", resolved).write_bytes(b"a database")
    return resolved


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


def matching_identity(cfg):
    """An identity provider that agrees with what the library recorded."""
    return lambda _path: cfg.library.volume_id


def foreign_identity(_path):
    return _ELSEWHERE


def open_gates(cfg, **overrides):
    """The real gates with only the platform seams injected.

    Everything that would otherwise depend on this machine is supplied: the
    volume identity, and nothing else. The refusals themselves are real.
    """
    arguments = {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}
    arguments.update(overrides)
    return arguments


@pytest.fixture
def volume_matches(cfg, monkeypatch):
    """Make the platform's own identity probe agree with what the library recorded.

    Patched at the PRECONDITION seam rather than passed into the gate, so the
    tests below drive the gates with no seam injected at all, which is exactly
    how a caller that supplies nothing reaches them. Without this the volume
    refusal fires first and the result depends on which disk the temporary
    directory happens to be on.
    """
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    return cfg


def acknowledge(cfg, **kwargs):
    """Mint an acknowledgment with the terminal check answered yes."""
    return session.record_acknowledgment(cfg, terminal=lambda: True, **kwargs)


def state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root."""
    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        base = Path(root)
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                path = Path(current) / name
                try:
                    stat_result = path.stat()
                except OSError:  # pragma: no cover - vanished mid-walk
                    continue
                found[str(path)] = (stat_result.st_size, stat_result.st_mtime_ns)
    return found


# ═══════════════════════════════════════════════════════════════════════════
# The three gates: three codes, and nothing written on any refused path
# ═══════════════════════════════════════════════════════════════════════════


def test_the_three_refusals_carry_three_distinct_codes_and_write_nothing(cfg):
    """AE5 and AE19 together, asserted against the filesystem rather than assumed.

    "Zero writes" is the assertion people skip because it looks obvious. It is
    not: a gate that took the lock before checking the acknowledgment would leave
    a file behind on a refused path, and every other assertion here would still
    pass.
    """
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())

    def refuse_with(**arguments):
        before = state_fingerprint(*roots)
        with pytest.raises(CratekitError) as excinfo:
            with session.assert_gates(cfg, workflow="a-destructive-workflow", **arguments):
                raise AssertionError("the gates admitted a session they should have refused")
        assert state_fingerprint(*roots) == before, "a refused session left a trace"
        return excinfo.value.cause

    wrong_volume = refuse_with(
        identity_provider=foreign_identity, mount_enumerator=lambda: ()
    )
    assert wrong_volume.code is ExitCode.LIBRARY_UNAVAILABLE
    assert wrong_volume.reason == "library-volume-mismatch"

    no_acknowledgment = refuse_with(**open_gates(cfg))
    assert no_acknowledgment.code is ExitCode.ACK_REQUIRED
    assert no_acknowledgment.reason == "backup-acknowledgment-missing"

    acknowledge(cfg)
    contender = open(session.lock_path(cfg), "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        busy = refuse_with(**open_gates(cfg))
    finally:
        contender.close()
    assert busy.code is ExitCode.LIBRARY_BUSY
    assert busy.reason == "session-lock-held"

    assert len({wrong_volume.code, no_acknowledgment.code, busy.code}) == 3


def test_the_gates_admit_a_session_once_all_three_pass(cfg):
    acknowledge(cfg)
    with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)) as held:
        assert held.lock == session.lock_path(cfg)
        assert held.acknowledgment.actor
        assert held.volume.ok


def test_the_volume_is_judged_before_any_library_path_is_resolved(cfg):
    """The order is the property, not a preference.

    With the wrong disk mounted, the acknowledgment file and the lock both sit on
    a volume that is not this library. Reading either one first would answer a
    question about somebody else's disk, and "no acknowledgment recorded" is a
    perfectly convincing answer to get from the wrong library.
    """
    acknowledge(cfg)
    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(
            cfg,
            workflow="a-destructive-workflow",
            identity_provider=foreign_identity,
            mount_enumerator=lambda: (),
        ):
            pass
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE
    assert not session.lock_path(cfg).exists(), "the lock was created before the volume check"


@pytest.mark.parametrize("state", sorted(preflight.MountState, key=str))
def test_every_mount_verdict_has_a_declared_refusal_slug(state):
    """P3. A verdict added with no entry must fail here rather than fall through.

    A new mount state falling through to a default is how a refusal ends up
    wearing an unrelated code, which is the collapse the cause registry exists to
    prevent.
    """
    from cratekit.core.cause import REASONS

    if state is preflight.MountState.OK:
        assert state not in session._MOUNT_REASONS
        return
    slug = session._MOUNT_REASONS[state]
    assert REASONS[slug] is ExitCode.LIBRARY_UNAVAILABLE


# ═══════════════════════════════════════════════════════════════════════════
# The lock
# ═══════════════════════════════════════════════════════════════════════════


def test_a_second_process_refuses_and_names_the_holder(cfg):
    """AE19. Naming the holder is the difference between waiting and guessing."""
    with session.session_lock(cfg):
        recorded = session.read_lock_holder(session.lock_path(cfg))
        assert recorded is not None
        assert recorded.pid == os.getpid()
        assert recorded.host and recorded.boot and recorded.started

        # A separate handle on the same file is what a second process looks like
        # to the kernel, so the in-process composition check must not see it.
        session._HELD.discard(str(session.lock_path(cfg).absolute()))
        with pytest.raises(CratekitError) as excinfo:
            with session.session_lock(cfg):
                pass
    cause = excinfo.value.cause
    assert cause.code is ExitCode.LIBRARY_BUSY
    assert str(os.getpid()) in cause.message


def test_a_nested_session_is_a_programming_error_not_a_foreign_holder(cfg):
    """The distinction matters because the two remedies are opposite.

    A foreign holder is waited for. A session nested inside another in ONE
    process can never resolve: the caller would be told to wait for itself,
    forever, and the report would name the run that is stuck as the thing
    blocking it.
    """
    with session.session_lock(cfg):
        with pytest.raises(session.SessionComposition) as excinfo:
            with session.session_lock(cfg):
                pass
    cause = excinfo.value.cause
    assert cause.code is ExitCode.INTERNAL
    assert cause.reason != "session-lock-held"
    assert "nest" in cause.message


def test_the_lock_file_is_never_unlinked_and_is_private_under_any_umask(cfg):
    """Unlinking a lock file is how two processes both come to believe they hold it.

    The first holds a lock on the inode and unlinks the NAME; the second creates
    a fresh file at that name and locks that instead, with nothing raised.
    """
    previous = os.umask(0)
    try:
        with session.session_lock(cfg) as held:
            assert held.exists()
            assert stat.S_IMODE(held.stat().st_mode) == config.PRIVATE_FILE_MODE
            assert (
                stat.S_IMODE(held.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
            )
        assert held.exists(), "the lock file was unlinked on release"
    finally:
        os.umask(previous)


def test_releasing_the_lock_clears_the_holder_so_the_next_run_is_not_told_to_wait(cfg):
    with session.session_lock(cfg):
        assert session.read_lock_holder(session.lock_path(cfg)) is not None
    assert session.read_lock_holder(session.lock_path(cfg)) is None


def test_releasing_a_dead_holders_lock_is_an_explicit_verb(cfg):
    """Never automatic. Clearing another run's claim mid-write is the failure."""
    lock = session.lock_path(cfg)
    lock.parent.mkdir(parents=True, exist_ok=True)
    dead = session.Holder(
        host=session.current_holder().host,
        boot=session.current_holder().boot,
        pid=os.getpid(),
        started="0.000",  # this process did not start at the epoch
    )
    lock.write_text(json.dumps({"holder": dead.to_json()}))

    assert session.holder_alive(dead) is False
    cleared = session.release_stale_lock(cfg)
    assert cleared == dead
    assert session.read_lock_holder(lock) is None


def test_releasing_a_live_holders_lock_refuses(cfg):
    with session.session_lock(cfg):
        with pytest.raises(CratekitError) as excinfo:
            session.release_stale_lock(cfg)
    assert excinfo.value.cause.code is ExitCode.LIBRARY_BUSY


def test_a_holder_on_another_machine_or_another_boot_is_assumed_alive(cfg):
    """Fails towards alive on every question this process cannot answer.

    Guessing "dead" would let one machine clear another machine's claim on the
    library, and the operation the lock protects is the one that removes files.
    """
    here = session.current_holder()
    other_host = session.Holder(
        host="another-machine", boot=here.boot, pid=here.pid, started=here.started
    )
    other_boot = session.Holder(
        host=here.host, boot="0", pid=here.pid, started=here.started
    )
    assert session.holder_alive(other_host) is True
    assert session.holder_alive(other_boot) is True


def test_the_holder_carries_all_four_identifying_fields(cfg):
    """A bare process identifier is meaningless across machines and is reused."""
    holder = session.current_holder()
    assert {"host", "boot", "pid", "started"} == set(holder.to_json())
    assert session.Holder.from_json(holder.to_json()) == holder


# ═══════════════════════════════════════════════════════════════════════════
# The acknowledgment (KTD18, R34)
# ═══════════════════════════════════════════════════════════════════════════


def test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment(cfg):
    """The gate protecting the operation that removes files is not self-servable."""
    with pytest.raises(CratekitError) as excinfo:
        session.record_acknowledgment(cfg, terminal=lambda: False)
    cause = excinfo.value.cause
    assert cause.code is ExitCode.ACK_REQUIRED
    assert cause.reason == "backup-acknowledgment-no-terminal"
    assert session.read_acknowledgment(cfg) is None


def test_the_terminal_check_is_a_terminal_check_and_not_a_standard_input_read():
    """R33 still holds. A terminal check does not consume a byte from anywhere.

    Derived from the source rather than asserted about behaviour, because the
    property is the ABSENCE of a read and absence is only visible structurally.
    """
    import ast

    source = Path(session.__file__).read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            raise AssertionError("the session module names standard input")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"input", "raw_input"}


def test_the_recorded_actor_is_derived_from_the_invocation_and_never_supplied():
    """R34's sharpest clause, asserted by INTROSPECTION rather than by reading.

    If a caller could name the actor, an agent driving the command line would
    mint the gate and sign somebody else's name to it. So the assertion is that
    no parameter could carry one, which stays true when the function is edited.
    """
    parameters = inspect.signature(session.record_acknowledgment).parameters
    assert not [name for name in parameters if "actor" in name.lower()]
    assert not [name for name in parameters if "user" in name.lower()]


def test_the_acknowledgment_records_the_backup_age_that_was_shown(cfg):
    """KTD18. An acknowledgment with no age is a click, not a decision.

    The portions are DERIVED from the backup fact vocabulary, so a portion added
    later cannot be silently absent from what a person was shown.
    """
    from cratekit.core import backup_facts

    now = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=now - timedelta(days=2),
        destination="remote:mirror",
    )
    recorded = acknowledge(cfg, now=now)

    shown = {entry.portion: entry for entry in recorded.shown}
    assert set(shown) == {str(portion) for portion in backup_facts.Portion}
    assert shown[str(backup_facts.Portion.FILES)].age_seconds == timedelta(days=2).total_seconds()
    assert shown[str(backup_facts.Portion.DATABASE)].state == str(
        backup_facts.AgeState.NEVER_RECORDED
    )


def test_an_expired_acknowledgment_refuses_exactly_as_an_absent_one_does(cfg):
    now = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    acknowledge(cfg, now=now, validity=timedelta(hours=1))

    session.assert_backup_acknowledged(cfg, now=now + timedelta(minutes=30))
    with pytest.raises(CratekitError) as excinfo:
        session.assert_backup_acknowledged(cfg, now=now + timedelta(hours=2))
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
    assert excinfo.value.cause.detail["expired"] is True


def test_the_acknowledgment_file_is_private_under_any_umask(cfg):
    previous = os.umask(0)
    try:
        acknowledge(cfg)
    finally:
        os.umask(previous)
    mode = stat.S_IMODE(session.ack_path(cfg).stat().st_mode)
    assert mode == config.PRIVATE_FILE_MODE


def test_no_blanket_affirmative_satisfies_the_acknowledgment(cfg):
    """AE20 and R34. Three affirmative surfaces exist, and all three are closed.

    R34 names a flag, a configuration key, and an environment variable, so each
    one is checked in the shape it would actually take, and each check is derived
    rather than restated.

    1. A FLAG would be a boolean parameter on the gate or on the consult. The set
       is read from the signatures, so a parameter added later is covered.
    2. A CONFIGURATION KEY would be a module toggle, which is the only boolean
       surface the configuration schema has. Every declared module is switched
       on, iterating the profile module registry rather than naming any of them.
    3. An ENVIRONMENT VARIABLE cannot satisfy something the code never reads, so
       the whole acknowledgment path is scanned for an environment read. That is
       structural on purpose: a behavioural test would have to guess the variable
       name, and the one that mattered would be the name nobody guessed.
    """
    from cratekit.core import profiles

    for function in (session.assert_gates, session.assert_backup_acknowledged):
        booleans = [
            name
            for name, parameter in inspect.signature(function).parameters.items()
            if isinstance(parameter.default, bool)
        ]
        assert not booleans, f"{function.__name__} takes {booleans}, which is a blanket flag"

    toggles = {module: True for module in profiles.MODULES}
    assert toggles, "no module toggle was found, so the walk is broken"
    object.__setattr__(cfg.modules, "explicit", toggles)

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
            pass
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED

    reads_environment = [
        function.__name__
        for function in (
            session.assert_gates,
            session.assert_backup_acknowledged,
            session.read_acknowledgment,
            session.ack_path,
        )
        if "environ" in inspect.getsource(function) or "getenv" in inspect.getsource(function)
    ]
    assert not reads_environment, (
        f"{reads_environment} read the environment on the acknowledgment path, so a "
        f"variable could answer the one gate a person has to answer"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The session log
# ═══════════════════════════════════════════════════════════════════════════


def test_the_log_records_everything_a_restore_has_to_judge(cfg):
    """Identifier, workflow, timestamp, capture path, change summary, state, actor."""
    acknowledged = acknowledge(cfg)
    record = session.open_session(
        cfg,
        workflow="a-destructive-workflow",
        actor=acknowledged.actor,
        acknowledged_at=acknowledged.recorded_at.isoformat(),
    )
    session.attach_capture(record, "/captures/one/master.db", cfg)
    record.change = session.ChangeSummary(
        (
            session.TreeChange(tree="tree-one", created=3, updated=1),
            session.TreeChange(tree="tree-two", created=0, updated=7),
        )
    )
    session.close_session(record, cfg)

    written = json.loads(session.log_path(record.session_id, cfg).read_text())
    assert written["session_id"] == record.session_id
    assert written["workflow"] == "a-destructive-workflow"
    assert written["started"]
    assert written[session.SNAPSHOT_KEY] == "/captures/one/master.db"
    assert written[session.STATE_KEY] == str(session.SessionState.CLOSED)
    assert written["actor"] == acknowledged.actor

    trees = {entry["tree"]: entry for entry in written["change"]["trees"]}
    assert trees["tree-one"]["created"] == 3
    assert trees["tree-two"]["updated"] == 7
    assert written["change"]["created"] == 3 and written["change"]["updated"] == 8


def test_a_session_record_is_private_under_any_umask(cfg):
    previous = os.umask(0)
    try:
        record = session.open_session(cfg, workflow="a-destructive-workflow")
    finally:
        os.umask(previous)
    path = session.log_path(record.session_id, cfg)
    assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE
    assert stat.S_IMODE(path.parent.stat().st_mode) == config.PRIVATE_DIR_MODE


def test_a_session_record_round_trips(cfg):
    record = session.open_session(cfg, workflow="a-destructive-workflow", sources=("one",))
    record.change = session.ChangeSummary((session.TreeChange("tree-one", created=2),))
    session.write_record(record, cfg)
    reread = session.read_record(record.session_id, cfg)
    assert reread.to_json() == record.to_json()


def test_closing_into_a_non_terminal_state_refuses(cfg):
    """A terminal state RELEASES the capture, so closing into a live one lies."""
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    with pytest.raises(CratekitError):
        session.close_session(record, cfg, state=session.SessionState.AWAITING_IMPORT)


def test_an_unreadable_record_does_not_stop_the_log_being_read(cfg):
    good = session.open_session(cfg, workflow="a-destructive-workflow")
    (session.log_dir(cfg) / "damaged.json").write_text("{not json")
    assert [r.session_id for r in session.records(cfg)] == [good.session_id]


# ═══════════════════════════════════════════════════════════════════════════
# One source per run (R29)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_refusal_at_source_two_leaves_source_one_committed_and_names_both(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two", "three")
    )

    def run_one(source):
        if source == "two":
            raise refuse("refused-by-policy", "source two is not acceptable")
        return session.ChangeSummary((session.TreeChange(tree=f"tree-{source}", created=1),))

    with pytest.raises(CratekitError) as excinfo:
        session.commit_sources(record, ("one", "two", "three"), run_one, cfg=cfg)

    cause = excinfo.value.cause
    assert cause.detail["committed"] == ["one"]
    assert cause.detail["refused_source"] == "two"
    assert set(cause.detail["remaining"]) == {"two", "three"}
    assert cause.inner is not None and cause.inner.reason == "refused-by-policy"

    # And the same facts are on disk, not only in the exception.
    persisted = session.read_record(record.session_id, cfg)
    assert persisted.sources["one"] == str(session.SourceState.COMMITTED)
    assert persisted.sources["two"] == str(session.SourceState.REFUSED)
    assert persisted.change.trees[0].tree == "tree-one"


def test_a_resume_skips_a_committed_source_and_finishes_the_rest(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two")
    )
    attempted: list[str] = []

    def run_one(source):
        attempted.append(source)
        if source == "two" and len(attempted) == 2:
            raise refuse("refused-by-policy", "not this time")
        return session.ChangeSummary((session.TreeChange(tree=f"tree-{source}", created=1),))

    with pytest.raises(CratekitError):
        session.commit_sources(record, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two"]

    resumed = session.read_record(record.session_id, cfg)
    session.commit_sources(resumed, ("one", "two"), run_one, cfg=cfg)
    assert attempted == ["one", "two", "two"], "a committed source was run again"
    assert resumed.committed_sources() == ("one", "two")
    assert {entry.tree for entry in resumed.change.trees} == {"tree-one", "tree-two"}


# ═══════════════════════════════════════════════════════════════════════════
# The capture gate, and the post-commit read-back (AE13)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_capture_that_failed_its_check_blocks_the_commit_behind_it(cfg):
    record = snapshot.capture(cfg, verifier=lambda _path: False)
    with pytest.raises(CratekitError) as excinfo:
        snapshot.assert_verified(record)
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_read_back_that_disagrees_ends_committed_unverified_and_advances_nothing(cfg):
    record = session.open_session(
        cfg, workflow="a-destructive-workflow", sources=("one", "two")
    )
    session.attach_capture(record, "/captures/one/master.db", cfg)
    record.sources["one"] = str(session.SourceState.COMMITTED)
    record.change = session.ChangeSummary((session.TreeChange("tree-one", created=4),))
    session.write_record(record, cfg)

    closed: list[object] = []

    class Handle:
        pass

    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(
            record,
            cfg,
            expect=lambda _db: False,
            reopen=Handle,
        )
    cause = excinfo.value.cause
    assert cause.code is ExitCode.LIBRARY_UNREADABLE
    assert cause.reason == "session-committed-unverified"
    assert cause.detail["snapshot_path"] == "/captures/one/master.db"
    assert cause.detail["change"]["trees"][0]["tree"] == "tree-one"

    persisted = session.read_record(record.session_id, cfg)
    assert persisted.state is session.SessionState.COMMITTED_UNVERIFIED
    assert persisted.sources["two"] == str(session.SourceState.PENDING), (
        "a source was marked done behind a read-back that disagreed"
    )
    assert closed == []


def test_the_read_back_releases_the_database_completely(cfg):
    """Closing a database does not release it: the pooled connection stays open.

    A restore over a file this process still holds produces an input-output error
    against a database that is perfectly intact, which reads as a corrupt restore
    at the worst possible moment. The full release is asserted rather than
    assumed, because the binding's own close looks like it is enough.
    """
    disposed: list[str] = []

    class Engine:
        def dispose(self):
            disposed.append("engine")

    class Handle:
        session = object()
        engine = Engine()

        def close(self):
            disposed.append("session")

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    assert session.verify_commit(record, cfg, expect=lambda _db: True, reopen=Handle) is True
    assert disposed == ["session", "engine"]


def test_a_disagreement_reports_a_live_rekordbox_separately(cfg, monkeypatch):
    """Two facts with two fixes, carried as a chain rather than collapsed into one."""
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    with pytest.raises(CratekitError) as excinfo:
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    cause = excinfo.value.cause
    assert cause.reason == "session-committed-unverified"
    assert cause.inner is not None
    assert cause.inner.reason == "rekordbox-running"
    assert cause.inner.code is ExitCode.REKORDBOX_OPEN


def test_an_unresolved_session_refuses_every_further_write(cfg):
    """Post-commit rollback does not exist, so the next write waits for a person."""
    acknowledge(cfg)
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    with pytest.raises(CratekitError):
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="a-destructive-workflow", **open_gates(cfg)):
            pass
    assert excinfo.value.cause.reason == "session-committed-unverified"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_an_unresolved_session_keeps_its_capture_out_of_the_pruner(cfg):
    """The state is deliberately non-terminal, and this is what that buys."""
    capture_path = cfg.library.root / "captures" / "one" / "master.db"
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, capture_path, cfg)
    with pytest.raises(CratekitError):
        session.verify_commit(record, cfg, expect=lambda _db: False, reopen=object)

    assert rb_writer.default_protected_snapshot_paths(cfg) == {capture_path.resolve()}


# ═══════════════════════════════════════════════════════════════════════════
# The un-imported XML output as a first-class state
# ═══════════════════════════════════════════════════════════════════════════


def test_a_run_holding_an_unimported_output_refuses_a_database_surface(cfg):
    """XML surfaces are strictly upstream of database surfaces within a run.

    The XML is what creates the row. A database surface written before the import
    addresses a row the database does not contain, so the refusal is not caution,
    it is the invariant.
    """
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.assert_database_surface_allowed(record)  # nothing pending, nothing refused

    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "Music" / "out.xml",
        summary="import the generated collection",
        verify_verb="run.show",
        blocks=("route.inbox",),
        steps=("import the file in rekordbox",),
    )
    session.mark_awaiting_import(record, pending, cfg)

    with pytest.raises(CratekitError) as excinfo:
        session.assert_database_surface_allowed(record)
    cause = excinfo.value.cause
    assert cause.code is ExitCode.PENDING_HUMAN
    assert cause.reason == "awaiting-import"
    assert cause.detail["verify_verb"] == "run.show"

    persisted = session.read_record(record.session_id, cfg)
    assert persisted.state is session.SessionState.AWAITING_IMPORT
    assert persisted.pending is not None
    assert persisted.pending.blocks == ("route.inbox",)


def test_the_pending_action_is_the_one_the_command_line_layer_already_enforces(cfg):
    """Connected to the existing mechanism rather than a parallel one.

    The command-line layer's own check refuses any verb named in ``blocks`` while
    the action is outstanding. Feeding the session's action straight into it is
    what makes the state load-bearing instead of advisory.
    """
    from cratekit.cli import gates, registry

    record = session.open_session(cfg, workflow="a-destructive-workflow")
    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "Music" / "out.xml",
        summary="import the generated collection",
        verify_verb="run.show",
        blocks=("route.inbox",),
    )
    assert pending.kind == "rekordbox_import"

    entry = next(e for e in registry.entries() if e.name == "run.show")
    run = gates.new_run(entry)
    run.pending = pending
    assert gates.blocked_by(run, "route.inbox") is not None
    assert gates.blocked_by(run, "profile.show") is None


# ═══════════════════════════════════════════════════════════════════════════
# The runtime half of R17's fifth surface
# ═══════════════════════════════════════════════════════════════════════════


def _analysis_tree(root: Path) -> list[Path]:
    directory = root / "PIONEER" / "USBANLZ" / "one"
    directory.mkdir(parents=True)
    written = []
    for name in ("ANLZ0000.DAT", "ANLZ0000.EXT", "ANLZ0000.2EX", "ANLZ0000.3EX"):
        path = directory / name
        path.write_bytes(b"analysis")
        written.append(path)
    return written


def test_a_moved_analysis_file_refuses_the_session(cfg, tmp_path):
    """A REAL moved file, not an assertion that a function exists.

    This is the half the source scan cannot do. It forbids every symbol that
    serialises one of these files, and reading them stays legal by decision, so a
    grid rewritten through a handle the binding already returned names none of
    the forbidden symbols and is invisible to it.
    """
    written = _analysis_tree(tmp_path / "library")
    victim = written[1]

    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            victim.write_bytes(b"a rewritten grid")
            stat_result = victim.stat()
            os.utime(victim, ns=(stat_result.st_atime_ns, stat_result.st_mtime_ns + 10**9))

    cause = excinfo.value.cause
    assert cause.reason == "anlz-modified"
    assert cause.code is ExitCode.REFUSED_BY_POLICY
    assert any(str(victim) in line for line in cause.detail["changed"])


def test_a_removed_analysis_file_refuses_too(cfg, tmp_path):
    """A destroyed grid is not a smaller problem than a rewritten one."""
    written = _analysis_tree(tmp_path / "library")
    with pytest.raises(CratekitError) as excinfo:
        with session.analysis_files_unmoved([tmp_path / "library"]):
            written[0].unlink()
    assert "was removed" in excinfo.value.cause.detail["changed"][0]


def test_a_session_that_touches_nothing_passes(cfg, tmp_path):
    """P7. A guard that fires on correct code is one people route around."""
    _analysis_tree(tmp_path / "library")
    with session.analysis_files_unmoved([tmp_path / "library"]) as watched:
        assert len(watched) == 4
    # And reading them is still perfectly legal.
    with session.analysis_files_unmoved([tmp_path / "library"]):
        for path in session.analysis_files_under([tmp_path / "library"]):
            path.read_bytes()


def test_the_gates_can_arm_the_analysis_watch_for_the_body_of_a_session(cfg, tmp_path):
    """Composed at the one place every destructive session passes through.

    The roots are supplied by the caller rather than defaulted to the library
    root, because the alternative is walking a whole music volume on every
    session to watch files nothing intends to open. The default of watching
    nothing is closed by the countdown below.
    """
    written = _analysis_tree(tmp_path / "library")
    acknowledge(cfg)
    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(
            cfg,
            workflow="a-destructive-workflow",
            analysis_roots=[tmp_path / "library"],
            **open_gates(cfg),
        ):
            written[2].write_bytes(b"a rewritten grid, mid session")
            moved = written[2].stat()
            os.utime(written[2], ns=(moved.st_atime_ns, moved.st_mtime_ns + 10**9))
    assert excinfo.value.cause.reason == "anlz-modified"


@requires("cratekit.write.trees")
def test_the_tree_writers_reach_for_the_session_spine(cfg):
    """P5. The countdown that closes this unit's own softening path.

    Three obligations, all on the unit that lands the tree writers, and none of
    them enforceable from here today because the module does not exist:

    * pass the three gates rather than re-deriving any of them;
    * commit behind a capture that VERIFIED, which is what makes the undo real;
    * name the analysis roots it could touch, so the watch that is the runtime
      half of R17's fifth surface actually watches something.

    The third is the one that matters most, because the default is to watch
    nothing and a default that silently does nothing is exactly the shape a
    docstring assertion fails to prevent.
    """
    import importlib

    trees = importlib.import_module("cratekit.write.trees")
    source = Path(trees.__file__).read_text()
    for obligation in ("assert_gates", "analysis_roots", "assert_verified"):
        assert obligation in source, (
            f"the tree writers do not reach for {obligation!r}, so the "
            f"destructive-session spine is optional for the unit that needs it most"
        )


def test_the_watched_set_is_never_narrower_than_the_binding_recognises():
    """P4. The claim is about a real API, so it is checked against that API.

    The alternatives are pulled out of the binding's own compiled pattern rather
    than retyped, so a binding that learns a fourth name fails here instead of
    quietly leaving one file unwatched.
    """
    from pyrekordbox.anlz import RE_ANLZ

    alternatives = re.search(r"\(([^)]*)\)", RE_ANLZ.pattern).group(1).split("|")
    assert alternatives, "the binding's pattern has no alternation, so the walk is broken"
    for suffix in alternatives:
        assert session.is_analysis_file(f"ANLZ0000.{suffix}"), suffix


def test_the_watched_set_covers_every_file_surface_five_declares():
    """And WIDER than the binding, deliberately.

    The binding recognises three names. R17's fifth surface declares four, and
    the fourth is a real grid-bearing file, so recognising only what the binding
    recognises would leave one unwatched. The four are read from that surface's
    own declaration rather than retyped here.
    """
    import tests.test_no_beatgrid_ever as surface_five

    declared = set(re.findall(r"``\.([0-9A-Z]{3})``", surface_five.__doc__))
    assert len(declared) == 4, f"surface five declares {sorted(declared)}"
    for suffix in declared:
        assert session.is_analysis_file(f"ANLZ0001.{suffix}"), suffix
    assert not session.is_analysis_file("ANLZ0001.TXT")
    assert not session.is_analysis_file("something.DAT")


# ═══════════════════════════════════════════════════════════════════════════
# R-8: the backup restore passes the same gates
# ═══════════════════════════════════════════════════════════════════════════


def test_the_backup_restore_passes_the_destructive_session_gates(volume_matches, cfg, tmp_path):
    """KTD24. A restore destroys a library and writes no database row.

    A rule that bound the gates to database WRITES would leave the single most
    destructive operation in the product outside the safety spine entirely.
    """
    target = tmp_path / "scratch"
    target.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        backup.plan_restore(
            cfg,
            target=target,
            confirmed=True,
            snapshot="2026-08-01T000000Z",
            runner=lambda command: backup.CommandResult(returncode=0),
            process_lister=lambda: (),
        )
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


def test_the_restores_own_refusals_survive_the_gates_being_added(cfg, tmp_path):
    """Added to, never replaced. An unconfirmed restore is still refused by name."""
    acknowledge(cfg)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg,
            target=tmp_path,
            confirmed=False,
            runner=lambda command: backup.CommandResult(returncode=0),
            process_lister=lambda: (),
            gates=lambda: session.assert_gates(
                cfg, workflow=backup.RESTORE_WORKFLOW, **open_gates(cfg)
            ),
        )
    assert excinfo.value.refusal is backup.Refusal.RESTORE_NOT_CONFIRMED


def test_a_rehearsed_restore_is_not_exempt_from_the_gates(volume_matches, cfg, tmp_path):
    """The decision, asserted. See ``run_restore`` for the three reasons.

    The lock is the one that matters: a rehearsal running while another
    destructive session writes describes a library that is changing underneath
    it, so its preview is a report about a world that no longer exists.
    """
    database_target = backup.database_target_for(cfg, tmp_path / "scratch")
    plan = backup.RestorePlan(
        target=tmp_path / "scratch",
        database_target=database_target,
        snapshot="2026-08-01T000000Z",
        clears=(),
        commands=(backup.Command(label=backup.RESTORE_DATABASE, argv=("rclone", "copy")),),
    )
    with pytest.raises(CratekitError) as excinfo:
        backup.run_restore(
            plan, cfg, runner=lambda command: backup.CommandResult(returncode=0), dry_run=True
        )
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


def test_the_destructive_half_of_a_restore_has_no_ungated_call_shape():
    """``cfg`` is required, so there is no way to reach it with nothing to gate on.

    An optional configuration would be a softening path: a caller that omitted it
    would get an ungated restore and no error, which is the shape P5 exists to
    close in the same commit that creates it.
    """
    parameters = inspect.signature(backup.run_restore).parameters
    assert parameters["cfg"].default is inspect.Parameter.empty
    assert parameters["cfg"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
