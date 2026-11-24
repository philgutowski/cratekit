"""R-1255: a session log that is there and cannot be listed is unread, never empty.

A glob over an unlistable directory yields nothing, so every gate admitted a
write the log may refuse. The container runs as root, so each test refuses the
two OS calls that list the one path; each case keeps a readable twin. D1 applies.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import session, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.intake import batch_name, native, refill, refill_cli, rotate, rotate_cli
from cratekit.intake import rekordbox_check as rc
from tests._sync_builders import exited, failed
from tests.cli_drive import drive
from tests.test_restore import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_restore import acknowledge, completed_session, gate_seams
from tests.test_restore import cfg as cfg  # noqa: PLC0414 - fixture

BATCH = "2026-10-20 Tidal playlists"
UNLISTED = "the session log exists and cannot be listed by this account"
NONE_READ = f"{UNLISTED}, so no session recorded in it can be read"
ONE_UNREAD = "the session log holds 1 entry this build cannot read"


def _refuse_listing(monkeypatch, directory: Path) -> None:
    """List ``directory`` as an account it is closed to: both listing calls are refused."""
    for call in ("listdir", "scandir"):
        real = getattr(os, call)

        def refused(path=".", *args, _real=real, **kwargs):
            if Path(os.fsdecode(path)) == directory:
                raise PermissionError(13, "Permission denied", str(path))
            return _real(path, *args, **kwargs)

        monkeypatch.setattr(os, call, refused)


def _record(cfg, state: session.SessionState, *, detail=None, session_id="s-1") -> Path:
    """Write one record and answer the log it is in."""
    record = session.SessionRecord(
        session_id=session_id, workflow=native.WORKFLOW, started="2026-10-20T12:00:00+00:00",
        state=state, sources={"intake": str(session.SourceState.COMMITTED)},
        ended="2026-10-20T12:05:00+00:00", detail=detail or {},
    )
    session.write_record(record, cfg)
    return Path(session.log_dir(cfg))


def _unverified(cfg) -> Path:
    """A log holding one session that committed behind a read-back that disagreed."""
    return _record(cfg, session.SessionState.COMMITTED_UNVERIFIED)


# 1. The scan


def test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so(
    cfg, monkeypatch
):
    """The clause names the listing and not an entry."""
    log = _unverified(cfg)
    assert [record.session_id for record in session.scan_log(cfg)[0]] == ["s-1"]
    _refuse_listing(monkeypatch, log)
    parsed, unreadable = session.scan_log(cfg)
    assert parsed == ()
    assert unreadable == (log,)
    assert session.log_unlisted(unreadable, cfg) is True
    assert session.unread_clause(unreadable, cfg) == UNLISTED


def test_the_reporting_reader_refuses_a_log_it_cannot_list(cfg, monkeypatch):
    """Restore and session release read this: a damaged record is skipped, the unlisted log not."""
    log = _unverified(cfg)
    (log / "2026-10-21-dead.json").write_text("{not json")
    assert [record.session_id for record in session.records(cfg)] == ["s-1"]
    _refuse_listing(monkeypatch, log)
    with pytest.raises(CratekitError) as refused:
        session.records(cfg)
    assert str(refused.value.cause.message).startswith(NONE_READ)
    assert refused.value.cause.detail == {"log": str(log), "unlisted": True}


def test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread(
    cfg, monkeypatch, tmp_path
):
    assert not Path(session.log_dir(cfg)).exists()
    assert session.scan_log(cfg) == ((), ())
    log = _unverified(cfg)
    (log / "2026-10-21-dead.json").write_text("{not json")
    (log / "notes.txt").write_text("not a record")
    parsed, unreadable = session.scan_log(cfg)
    assert [record.session_id for record in parsed] == ["s-1"]
    assert unreadable == (log / "2026-10-21-dead.json",)
    assert session.log_unlisted(unreadable, cfg) is False
    assert session.unread_clause(unreadable, cfg) == ONE_UNREAD
    held = tmp_path / "log-is-a-file"
    held.write_text("not a directory")
    monkeypatch.setattr(session, "log_dir", lambda _cfg: held)
    assert session.scan_log(cfg) == ((), (held,))
    # A log under a file is not there.
    monkeypatch.setattr(session, "log_dir", lambda _cfg: held / "session_log")
    assert session.scan_log(cfg) == ((), ())


# 2. Every gate refuses, rather than admitting the write the log may refuse


@pytest.mark.parametrize(
    ("state", "detail", "ask", "readable", "said"),
    [
        (
            session.SessionState.COMMITTED_UNVERIFIED,
            None,
            lambda cfg: session.assert_no_unresolved_session(cfg),
            "session-committed-unverified",
            "cannot vouch that no session ended unresolved",
        ),
        (
            # A record keeping the name is unseen, so the name would read free.
            session.SessionState.CLOSED,
            {native.BATCH_PLAYLIST_KEY: {"id": "p-1", "name": BATCH}},
            lambda cfg: batch_name.free(cfg, BATCH),
            f"{BATCH} 2",
            "so no batch name can be called free",
        ),
        (
            session.SessionState.OPEN,
            None,
            lambda cfg: [
                one.session_id
                for one in tree_registry._whole_log(
                    cfg, so="whether a run is still open was not established"
                )
            ],
            ["s-1"],
            "so whether a run is still open was not established",
        ),
    ],
)
def test_every_gate_refuses_a_log_it_cannot_list(
    cfg, monkeypatch, state, detail, ask, readable, said
):
    log = _record(cfg, state, detail=detail)
    try:
        assert ask(cfg) == readable
    except CratekitError as exc:
        assert exc.cause.reason == readable
    _refuse_listing(monkeypatch, log)
    with pytest.raises(CratekitError) as caught:
        ask(cfg)
    message = caught.value.cause.message
    assert UNLISTED in message
    assert said in message
    assert caught.value.cause.detail["unlisted"] is True
    if state is session.SessionState.COMMITTED_UNVERIFIED:
        assert caught.value.cause.reason == "internal-error"
        assert "holds 1 entry" not in message
        assert caught.value.cause.detail["unreadable"] == [str(log)]


def test_every_destructive_session_is_refused_at_its_gate(cfg, monkeypatch):
    """The latch is enforced at the one gate every destructive session passes."""
    log = _unverified(cfg)
    acknowledge(cfg)
    _refuse_listing(monkeypatch, log)
    with pytest.raises(CratekitError) as caught:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            pytest.fail("the gate admitted a write over a log it could not list")
    assert "cannot be listed by this account" in caught.value.cause.message


def test_an_unreadable_record_keeps_its_own_refusal(cfg):
    """The record case reads as it did: the count, and no claim about the listing."""
    log = _record(cfg, session.SessionState.CLOSED)
    (log / "2026-10-21-dead.json").write_text("{not json")
    for asked in (
        lambda: session.assert_no_unresolved_session(cfg),
        lambda: batch_name.free(cfg, BATCH),
        lambda: tree_registry._whole_log(cfg, so="x"),
    ):
        with pytest.raises(CratekitError) as caught:
            asked()
        assert ONE_UNREAD in caught.value.cause.message
        assert caught.value.cause.detail["unlisted"] is False


# 3. The reports say so, rather than reading clean


def test_the_rotation_reads_the_listing_from_the_scan(cfg, monkeypatch):
    log = _record(cfg, session.SessionState.CLOSED)
    assert rotate.landings(cfg).unread() == ""
    _refuse_listing(monkeypatch, log)
    found = rotate.landings(cfg)
    assert found.unlisted is True
    assert found.unreadable == 1
    assert found.unread() == "the session log could not be listed, and a record in it may"


def _rotation_plan(**overrides) -> rotate.RotationPlan:
    fields = {
        "tree_id": "t", "root_id": "1", "root_name": "INBOX", "old_place": "old",
        "old_display": "Old", "old_id": None, "as_of": date(2026, 11, 5), "stale_days": 14,
        "expired_days": 60, "moves": (), "removals": (), "kept": (), "left": (),
        "unreadable_records": 0, "digest": "",
    }  # fmt: skip
    fields.update(overrides)
    return rotate.RotationPlan(**fields)


@pytest.mark.parametrize(
    ("given", "said"),
    [
        ({"unreadable_records": 1, "log_unlisted": True}, "the session log could not be listed"),
        ({"unreadable_records": 2}, "2 session record(s) could not be read"),
    ],
)
def test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read(given, said):
    (warning,) = rotate_cli.records_warnings(_rotation_plan(**given))
    assert warning["code"] == rotate_cli.RECORDS_UNREADABLE
    names = "a record in it names" if "log_unlisted" in given else "one of them names"
    aged = f"{said}, so a batch {names} was aged from its playlist's creation date"
    assert warning["message"] == aged
    assert rotate_cli.records_warnings(_rotation_plan()) == []


def _refill_warning(**given) -> str:
    plan = refill.RefillPlan(
        pass_name="p", tree_id="t", root_id="1", root_name="INBOX", targets=(), **given
    )
    warned = refill_cli.warnings_of(plan)
    (warning,) = [one for one in warned if one["code"] == refill_cli.RECORDS_UNREADABLE]
    return warning["message"]


def test_the_refill_warns_on_a_log_it_could_not_list_or_records_it_could_not_read():
    assert _refill_warning(unreadable=1, log_unlisted=True) == (
        "the session log could not be listed, so no account playlist without a "
        "readable landing record was found by its name"
    )
    assert _refill_warning(unreadable=3).startswith("3 session record(s) could not be read, so no ")


def test_the_check_refuses_an_unknown_landing_naming_the_listing(cfg, monkeypatch):
    _refuse_listing(monkeypatch, _record(cfg, session.SessionState.CLOSED))
    with pytest.raises(CratekitError) as caught:
        rc.resolve_scope(cfg, None, declared=None, registry=None, pass_name="2026-10-20 sync")
    assert caught.value.cause.reason == "analysis-check-landing-unknown"
    said = "; the session log could not be listed and it may be in it"
    assert caught.value.cause.message.endswith(said)
    assert caught.value.cause.detail["log_unlisted"] is True


# 4. The verbs that read the log to report it refuse rather than answer none


def test_restore_list_and_run_refuse_a_log_they_cannot_list(cfg, monkeypatch):
    """List answered nothing over a recorded session, and run said no session had its id."""
    record, _captured = completed_session(cfg)
    listing = exited(drive(["restore", "list"]))
    assert [row["session_id"] for row in listing["data"]["items"]] == [record.session_id]
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))
    refused = failed(drive(["restore", "list"]))
    assert refused["cause"]["message"].startswith(NONE_READ)
    refused = failed(drive(["restore", "run", record.session_id]))
    assert "cannot be listed by this account" in refused["cause"]["message"]
    assert "is recorded under" not in refused["cause"]["message"]


def test_the_native_landing_lookups_refuse_a_log_they_cannot_list(cfg, monkeypatch):
    """Both answered no landing, and sync mark sent a person to land again."""
    sync = "2026-10-20 sync"
    log = _record(cfg, session.SessionState.CLOSED, detail={native.PASS_KEY: sync})
    assert native.landed_passes(cfg) == ("2026-10-20 sync",)
    assert native.landings_of_pass(cfg, "2026-10-20 sync") == ("s-1",)
    _refuse_listing(monkeypatch, log)
    for lookup in (lambda: native.landed_passes(cfg), lambda: native.landings_of_pass(cfg, sync)):
        with pytest.raises(CratekitError) as refused:
            lookup()
        assert "cannot be listed by this account" in refused.value.cause.message
