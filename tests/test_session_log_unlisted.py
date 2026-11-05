"""R-1255: a session log that is there and cannot be listed is unread, never empty.

``session.scan_log`` used to glob the log, and a glob over a directory the
account cannot list yields nothing rather than raising, so the scan answered
no record and no unreadable one. Every gate that reads the log through the
scan then admitted the write the log may refuse, and every report was clean
over a log nobody read. U214 asked the listing itself in the rotation's
classifier only; this file holds the scan and each consumer to it.

THE CONTAINER RUNS AS ROOT, which no file mode bars, so each test refuses the
two OS calls that list a directory (``os.listdir``, and ``os.scandir`` that a
glob uses) for the one path, as an account the log is closed to is refused.
Each case keeps its readable twin beside it, so the plain answer is pinned too.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from cratekit.analysis import rekordbox_check as rc
from cratekit.core import session, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, native, refill, refill_cli, rotate, rotate_cli
from tests.cli_drive import drive
from tests.test_restore import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_restore import acknowledge, completed_session, gate_seams
from tests.test_restore import cfg as cfg  # noqa: PLC0414 - fixture

BATCH = "2026-10-20 Tidal playlists"


def _refuse_listing(monkeypatch, directory: Path) -> None:
    """List ``directory`` as an account it is closed to: both listing calls are refused."""
    for call in ("listdir", "scandir"):
        real = getattr(os, call)

        def refused(path=".", *args, _real=real, **kwargs):
            if Path(os.fsdecode(path)) == directory:
                raise PermissionError(13, "Permission denied", str(path))
            return _real(path, *args, **kwargs)

        monkeypatch.setattr(os, call, refused)


def _record(cfg, state: session.SessionState, *, detail=None, session_id="s-1") -> None:
    session.write_record(
        session.SessionRecord(
            session_id=session_id,
            workflow=native.WORKFLOW,
            started="2026-10-20T12:00:00+00:00",
            state=state,
            sources={"intake": str(session.SourceState.COMMITTED)},
            ended="2026-10-20T12:05:00+00:00",
            detail=detail or {},
        ),
        cfg,
    )


def _unverified(cfg) -> Path:
    """A log holding one session that committed behind a read-back that disagreed."""
    _record(cfg, session.SessionState.COMMITTED_UNVERIFIED)
    return Path(session.log_dir(cfg))


# ═══════════════════════════════════════════════════════════════════════════
# 1. The scan
# ═══════════════════════════════════════════════════════════════════════════


def test_a_log_that_cannot_be_listed_is_returned_as_the_one_unread_entry(cfg, monkeypatch):
    log = _unverified(cfg)
    assert [record.session_id for record in session.scan_log(cfg)[0]] == ["s-1"]
    _refuse_listing(monkeypatch, log)

    parsed, unreadable = session.scan_log(cfg)

    assert parsed == ()
    assert unreadable == (log,)
    assert session.log_unlisted(unreadable, cfg) is True


def test_the_reporting_reader_refuses_a_log_it_cannot_list(cfg, monkeypatch):
    """Review round one: restore list, restore run and session release read this.

    Skipping a damaged record leaves the others reported; a log nobody could
    list leaves none, and an empty answer told a person their session was never
    recorded. One damaged record is still skipped, which the twin pins.
    """
    log = _unverified(cfg)
    (log / "2026-10-21-dead.json").write_text("{not json")
    assert [record.session_id for record in session.records(cfg)] == ["s-1"]
    _refuse_listing(monkeypatch, log)

    with pytest.raises(CratekitError) as refused:
        session.records(cfg)

    assert str(refused.value.cause.message).startswith(
        "the session log exists and cannot be listed by this account, so no session "
        "recorded in it can be read"
    )
    assert refused.value.cause.detail == {"log": str(log), "unlisted": True}


def test_a_listed_log_is_read_and_names_nothing_unlisted(cfg):
    log = _unverified(cfg)
    (log / "2026-10-21-dead.json").write_text("{not json")
    (log / "notes.txt").write_text("not a record")

    parsed, unreadable = session.scan_log(cfg)

    assert [record.session_id for record in parsed] == ["s-1"]
    assert unreadable == (log / "2026-10-21-dead.json",)
    assert session.log_unlisted(unreadable, cfg) is False
    assert session.unread_clause(unreadable, cfg) == (
        "the session log holds 1 entry this build cannot read"
    )


def test_a_log_that_is_not_there_is_no_record_at_all(cfg):
    log = Path(session.log_dir(cfg))
    assert not log.exists()

    assert session.scan_log(cfg) == ((), ())


def test_a_log_path_that_is_a_file_is_there_and_unread(cfg, monkeypatch, tmp_path):
    held = tmp_path / "log-is-a-file"
    held.write_text("not a directory")
    monkeypatch.setattr(session, "log_dir", lambda _cfg: held)

    assert session.scan_log(cfg) == ((), (held,))


def test_a_log_under_a_file_is_not_there(cfg, monkeypatch, tmp_path):
    parent = tmp_path / "state-is-a-file"
    parent.write_text("not a directory")
    monkeypatch.setattr(session, "log_dir", lambda _cfg: parent / "session_log")

    assert session.scan_log(cfg) == ((), ())


def test_the_clause_names_the_listing_and_not_an_entry(cfg, monkeypatch):
    log = _unverified(cfg)
    _refuse_listing(monkeypatch, log)

    _parsed, unreadable = session.scan_log(cfg)

    assert session.unread_clause(unreadable, cfg) == (
        "the session log exists and cannot be listed by this account"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. Every gate refuses, rather than admitting the write the log may refuse
# ═══════════════════════════════════════════════════════════════════════════


def test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list(cfg, monkeypatch):
    log = _unverified(cfg)
    with pytest.raises(CratekitError) as readable:
        session.assert_no_unresolved_session(cfg)
    assert readable.value.cause.reason == "session-committed-unverified"
    _refuse_listing(monkeypatch, log)

    with pytest.raises(CratekitError) as caught:
        session.assert_no_unresolved_session(cfg)

    assert caught.value.cause.reason == "internal-error"
    message = caught.value.cause.message
    assert "the session log exists and cannot be listed by this account" in message
    assert "cannot vouch that no session ended unresolved" in message
    assert "holds 1 entry" not in message
    assert caught.value.cause.detail["unreadable"] == [str(log)]
    assert caught.value.cause.detail["unlisted"] is True


def test_every_destructive_session_is_refused_at_its_gate(cfg, monkeypatch):
    """The latch is enforced at the one gate every destructive session passes."""
    log = _unverified(cfg)
    acknowledge(cfg)
    _refuse_listing(monkeypatch, log)

    with pytest.raises(CratekitError) as caught:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            pytest.fail("the gate admitted a write over a log it could not list")

    assert "cannot be listed by this account" in caught.value.cause.message


def test_the_batch_name_rule_refuses_rather_than_call_a_name_free(cfg, monkeypatch):
    """A record keeping the name is unseen, so the name would read free and merge two batches."""
    _record(
        cfg,
        session.SessionState.CLOSED,
        detail={native.BATCH_PLAYLIST_KEY: {"id": "p-1", "name": BATCH}},
    )
    assert batch_name.free(cfg, BATCH) == f"{BATCH} 2"
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    with pytest.raises(CratekitError) as caught:
        batch_name.free(cfg, BATCH)

    message = caught.value.cause.message
    assert "the session log exists and cannot be listed by this account" in message
    assert "so no batch name can be called free" in message
    assert caught.value.cause.detail["unlisted"] is True


def test_the_tree_registry_refuses_rather_than_read_no_open_run(cfg, monkeypatch):
    _record(cfg, session.SessionState.OPEN)
    assert [one.session_id for one in tree_registry._whole_log(cfg, so="x")] == ["s-1"]
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    with pytest.raises(CratekitError) as caught:
        tree_registry._whole_log(cfg, so="whether a run is still open was not established")

    message = caught.value.cause.message
    assert "the session log exists and cannot be listed by this account" in message
    assert "so whether a run is still open was not established" in message
    assert caught.value.cause.detail["unlisted"] is True


def test_an_unreadable_record_keeps_its_own_refusal(cfg):
    """The record case reads as it did: the count, and no claim about the listing."""
    _record(cfg, session.SessionState.CLOSED)
    log = Path(session.log_dir(cfg))
    (log / "2026-10-21-dead.json").write_text("{not json")

    for asked in (
        lambda: session.assert_no_unresolved_session(cfg),
        lambda: batch_name.free(cfg, BATCH),
        lambda: tree_registry._whole_log(cfg, so="x"),
    ):
        with pytest.raises(CratekitError) as caught:
            asked()
        assert "the session log holds 1 entry this build cannot read" in (
            caught.value.cause.message
        )
        assert caught.value.cause.detail["unlisted"] is False


# ═══════════════════════════════════════════════════════════════════════════
# 3. The reports say so, rather than reading clean
# ═══════════════════════════════════════════════════════════════════════════


def test_the_rotation_reads_the_listing_from_the_scan(cfg, monkeypatch):
    _record(cfg, session.SessionState.CLOSED)
    assert rotate.landings(cfg).unread() == ""
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    found = rotate.landings(cfg)

    assert found.unlisted is True
    assert found.unreadable == 1
    assert found.unread() == "the session log could not be listed, and a record in it may"


def _rotation_plan(**overrides) -> rotate.RotationPlan:
    fields = {
        "tree_id": "t",
        "root_id": "1",
        "root_name": "INBOX",
        "old_place": "old",
        "old_display": "Old",
        "old_id": None,
        "as_of": date(2026, 11, 5),
        "stale_days": 14,
        "expired_days": 60,
        "moves": (),
        "removals": (),
        "kept": (),
        "left": (),
        "unreadable_records": 0,
        "digest": "",
    }
    fields.update(overrides)
    return rotate.RotationPlan(**fields)


def test_the_rotation_warns_on_a_log_it_could_not_list():
    (warning,) = rotate_cli.records_warnings(
        _rotation_plan(unreadable_records=1, log_unlisted=True)
    )

    assert warning["code"] == rotate_cli.RECORDS_UNREADABLE
    assert warning["message"] == (
        "the session log could not be listed, so a batch a record in it names was "
        "aged from its playlist's creation date"
    )


def test_the_rotation_warns_on_records_it_could_not_read_as_it_did():
    (warning,) = rotate_cli.records_warnings(_rotation_plan(unreadable_records=2))

    assert warning["message"] == (
        "2 session record(s) could not be read, so a batch one of them names was "
        "aged from its playlist's creation date"
    )
    assert rotate_cli.records_warnings(_rotation_plan()) == []


def _refill_plan(**overrides) -> refill.RefillPlan:
    fields = {"pass_name": "p", "tree_id": "t", "root_id": "1", "root_name": "INBOX", "targets": ()}
    fields.update(overrides)
    return refill.RefillPlan(**fields)


def test_the_refill_warns_on_a_log_it_could_not_list():
    (warning,) = [
        one
        for one in refill_cli.warnings_of(_refill_plan(unreadable=1, log_unlisted=True))
        if one["code"] == refill_cli.RECORDS_UNREADABLE
    ]

    assert warning["message"] == (
        "the session log could not be listed, so no account playlist without a "
        "readable landing record was found by its name"
    )


def test_the_refill_warns_on_records_it_could_not_read_as_it_did():
    (warning,) = [
        one
        for one in refill_cli.warnings_of(_refill_plan(unreadable=3))
        if one["code"] == refill_cli.RECORDS_UNREADABLE
    ]

    assert warning["message"].startswith("3 session record(s) could not be read, so no ")


def test_the_check_refuses_an_unknown_landing_naming_the_listing(cfg, monkeypatch):
    _record(cfg, session.SessionState.CLOSED)
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    with pytest.raises(CratekitError) as caught:
        rc.resolve_scope(cfg, None, declared=None, registry=None, pass_name="2026-10-20 sync")

    assert caught.value.cause.reason == "analysis-check-landing-unknown"
    assert caught.value.cause.message.endswith(
        "; the session log could not be listed and it may be in it"
    )
    assert caught.value.cause.detail["log_unlisted"] is True



# ═══════════════════════════════════════════════════════════════════════════
# 5. The verbs that read the log to report it refuse rather than answer none
# ═══════════════════════════════════════════════════════════════════════════


def test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing(cfg, monkeypatch):
    """Review round one: exit 0 with no item and no warning, over a recorded session."""
    record, _captured = completed_session(cfg)
    code, listing = drive(["restore", "list"])
    assert code == int(ExitCode.OK), listing
    assert [row["session_id"] for row in listing["data"]["items"]] == [record.session_id]
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    code, refused = drive(["restore", "list"])

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["message"].startswith(
        "the session log exists and cannot be listed by this account, so no session "
        "recorded in it can be read"
    )


def test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session(cfg, monkeypatch):
    """Review round one: it said no session was recorded under an id that was."""
    record, _captured = completed_session(cfg)
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    code, refused = drive(["restore", "run", record.session_id])

    assert code != int(ExitCode.OK), refused
    assert "cannot be listed by this account" in refused["cause"]["message"]
    assert "is recorded under" not in refused["cause"]["message"]


def test_the_native_landing_lookups_refuse_a_log_they_cannot_list(cfg, monkeypatch):
    """Review round two: both answered no landing, and sync mark sent a person to land again."""
    _record(cfg, session.SessionState.CLOSED, detail={native.PASS_KEY: "2026-10-20 sync"})
    assert native.landed_passes(cfg) == ("2026-10-20 sync",)
    assert native.landings_of_pass(cfg, "2026-10-20 sync") == ("s-1",)
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    for lookup in (
        lambda: native.landed_passes(cfg),
        lambda: native.landings_of_pass(cfg, "2026-10-20 sync"),
    ):
        with pytest.raises(CratekitError) as refused:
            lookup()
        assert "cannot be listed by this account" in refused.value.cause.message

