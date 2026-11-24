"""U134: an INBOX account playlist is refilled from its recorded pass.

A pass is landed, its INBOX playlist emptied as sitting 34 emptied four, and
``crate inbox refill`` driven over it. D1 applies.
"""

from __future__ import annotations

import contextlib
import socket
import sqlite3
from pathlib import Path

import pytest

from cratekit.cli.output import digest_of
from cratekit.core import active_taxonomy, config, jobs, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import missing_cli, native, refill, refill_cli, set_playlist
from cratekit.sync import twins
from tests import cutover_fixtures
from tests.cli_drive import drive
from tests.test_inbox_rotate import _handle
from tests.test_inbox_rotate import _two_acts as _gated
from tests.test_intake_land_account_playlists_native import (
    PASS,
    _landed,
    _owned,
    _stage,
    swept,
)
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_native import _members, _query
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_session_log_unlisted import _refuse_listing

GATE = refill_cli.APPROVE_GATE
ACCOUNT = "Sunset Warmup"
#: The INBOX playlist a landing on the pinned day makes for it, dated since U175.
INBOX_NAME = "Sunset Warmup 2026-10-03"
LIVE_TITLED = "FROM djmdContent WHERE Title = ? AND rb_local_deleted = 0"


def _refill(pass_name: str = PASS) -> list[str]:
    return ["inbox", "refill", "--pass", pass_name]


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    return _gated(verb, gate=GATE, answer="apply")


def _acted() -> tuple[dict, dict]:
    """The refill's two acts and the acting drive, which must succeed."""
    code, acted, refused = _two_acts(_refill())
    assert code == int(ExitCode.OK), acted
    return acted, refused


def _playlist_id(cfg: config.Config, name: str) -> str:
    """The landing's INBOX playlist of this name, never its custom playlist twin (U149)."""
    sql = (
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND rb_local_deleted = 0 "
        "AND ParentID NOT IN (SELECT ID FROM djmdPlaylist WHERE Name LIKE ? AND Attribute = 1)"
    )
    ((playlist_id,),) = _query(cfg, sql, name, f"{twins.FOLDER_PREFIX} %")
    return str(playlist_id)


def _sql(cfg: config.Config, statement: str, *params) -> None:
    with contextlib.closing(sqlite3.connect(cfg.library.db_path)) as conn, conn:
        conn.execute(statement, params)


def _emptied(cfg: config.Config, name: str = INBOX_NAME) -> str:
    """Sitting 34: every row of the playlist removed and dropped back in under a new id."""
    playlist_id = _playlist_id(cfg, name)
    held = _members(cfg, playlist_id)
    insert = (
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, ?, 0, '2026-10-09', '2026-10-09')"
    )
    for number, cid in enumerate(held, start=1):
        ((title, folder),) = _query(cfg, "SELECT Title, FolderPath FROM djmdContent WHERE ID = ?", cid)
        _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", cid)
        _sql(cfg, "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ContentID = ?", cid)
        _sql(cfg, insert, f"9{number:04d}{cid}", title, folder)
    assert _live_members(cfg, playlist_id) == []
    return playlist_id


def _named_before_u175(cfg: config.Config, playlist_id: str) -> None:
    """The landed playlist renamed as a landing before U175 named it, the account's name alone."""
    _sql(cfg, "UPDATE djmdPlaylist SET Name = ? WHERE ID = ?", ACCOUNT, playlist_id)


def _rewrite_entries(cfg: config.Config, rewrite) -> None:
    """Every landing record's account playlist entries, rewritten and written back."""
    for record in session.records(cfg):
        if native.INBOX_PLAYLISTS_KEY in record.detail:
            entries = record.detail[native.INBOX_PLAYLISTS_KEY]
            record.detail[native.INBOX_PLAYLISTS_KEY] = rewrite(entries)
            session.write_record(record, cfg)


def _new_playlist(cfg: config.Config, name: str, parent_id: str) -> str:
    with _handle(cfg) as handle:
        row = handle.create_playlist(name, parent=handle.get_playlist(ID=parent_id))
        handle.session.commit()
        return str(row.ID)


def _refills(cfg: config.Config) -> list[session.SessionRecord]:
    return [r for r in session.records(cfg) if r.workflow == refill.WORKFLOW]


def _live_members(cfg: config.Config, playlist_id: str) -> list[str]:
    titles = dict(_query(cfg, "SELECT ID, Title FROM djmdContent"))
    sql = "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0"
    return [str(titles[str(row[0])]) for row in _query(cfg, sql + " ORDER BY TrackNo", playlist_id)]


def _five_landed_and_emptied(cfg: config.Config, silence: Path) -> str:
    _owned(cfg, silence, ("Held1", "Held2", "Held3"))
    swept(cfg, {"pl-a": (ACCOUNT, ("Held1", "New1", "Held2", "New2", "Held3"))})
    for title in ("New1", "New2"):
        _stage(cfg, silence, title)
    _landed(cfg)
    return _emptied(cfg)


@pytest.fixture
def offline(monkeypatch):
    """No provider can be reached: any socket the verb opens fails the test."""

    def refused(*_args, **_kwargs):
        raise AssertionError("the refill opened a network connection")
    monkeypatch.setattr(socket.socket, "connect", refused)
    monkeypatch.setattr(socket, "create_connection", refused)


def test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once(
        native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    rows_before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")
    acted, refused = _acted()
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    # The rows are the library's new ones, and no content row was made.
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == rows_before
    assert acted["data"]["totals"]["added"] == 5
    assert acted["data"]["totals"]["read back"] == 5
    added = [item for item in refused["cause"]["detail"]["shown"]["items"] if item["action"] == "add"]
    assert [item["title"] for item in added] == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert not [w for w in acted["warnings"] if w["code"] == refill_cli.LEFT_OUT]
    # Recorded under the intake tree, with the playlist named.
    (record,) = _refills(cfg)
    playlists = [{"id": playlist_id, "name": INBOX_NAME, "added": 5}]
    assert record.detail[refill.RECORD_KEY] == {"pass": PASS, "playlists": playlists}
    # A SECOND RUN PLANS NOTHING and ends no_op, writing no second record.
    again, _ = _acted()
    assert again["outcome"] == "no_op", again
    assert again["data"]["totals"]["add"] == 0
    assert [w for w in again["warnings"] if w["code"] == refill_cli.NOTHING]
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert len(_refills(cfg)) == 1


def test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left(
        native_library, silence, offline, monkeypatch):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    elsewhere = cutover_fixtures.add_folder(cfg, "Kept By Hand")
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", elsewhere, playlist_id)

    def unread(*_args, **_kwargs):
        raise AssertionError("a report of the pass was read before the refusal")
    reports = missing_cli.job_reports
    monkeypatch.setattr(missing_cli, "job_reports", unread)
    code, refused = drive(_refill())
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == refill.OUTSIDE_INBOX, refused
    assert f"{INBOX_NAME!r} (row {playlist_id})" in refused["cause"]["message"]
    assert _live_members(cfg, playlist_id) == []
    assert not _refills(cfg)
    # Moved back, with New2's file gone from disk: its row stays, as rekordbox
    # keeps a missing file's row, and the track is named and left.
    monkeypatch.setattr(missing_cli, "job_reports", reports)
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", root_id, playlist_id)
    ((folder,),) = _query(cfg, f"SELECT FolderPath {LIVE_TITLED}", "New2")
    Path(folder).unlink()
    acted, _ = _acted()
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "Held3"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.LEFT_OUT]
    assert f"{INBOX_NAME} 4. Probe - New2" in warning["message"]
    assert set_playlist.NOT_RESOLVED in warning["message"]


def test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it(
        native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    _named_before_u175(cfg, playlist_id)
    _rewrite_entries(cfg, lambda entries: [])
    second_id = _new_playlist(cfg, ACCOUNT, root_id)
    acted, refused = _acted()
    assert acted["outcome"] == "no_op", acted
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.UNFOUND]
    assert refill.TWO_FOUND in warning["message"]
    assert _live_members(cfg, playlist_id) == []
    # The second one gone and the first moved into a folder under INBOX, as the
    # rotation moves a batch: the one left is found by the account's name.
    _sql(cfg, "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", second_id)
    old = cutover_fixtures.add_folder(cfg, "Old")
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", root_id, old)
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", old, playlist_id)
    acted, refused = _acted()
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    shown = refused["cause"]["detail"]["shown"]["playlists"]
    assert shown == [f"{ACCOUNT} (row {playlist_id}, {refill.BY_NAME}): 5 track(s) "
                     f"the library owns, 5 to add, 0 left out"]


def test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks(
        native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    with jobs.open_store() as store:
        before = [(job.job_id, job.state) for job in jobs.list_jobs(store)]
    code, refused = drive(_refill())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    # THE JOB STORE IS READ, NOT WRITTEN, by a plan.
    with jobs.open_store() as store:
        assert [(job.job_id, job.state) for job in jobs.list_jobs(store)] == before
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    # A track added in rekordbox between the approval and the apply.
    ((held3,),) = _query(cfg, f"SELECT ID {LIVE_TITLED}", "Held3")
    with _handle(cfg) as handle:
        rb_writer.add_memberships(handle, handle.get_playlist(ID=playlist_id), [str(held3)])
        handle.session.commit()
    code, acted = drive(["--run", run_id, *_refill()])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] in ("decision-stale", "decision-digest-mismatch"), acted
    assert _live_members(cfg, playlist_id) == ["Held3"]
    # THE PLAYLIST NOW HOLDS SOME, and a fresh run plans only what it lacks.
    acted, refused = _acted()
    actions = [(item["title"], item["action"]) for item in refused["cause"]["detail"]["shown"]["items"]]
    assert actions == [
        ("Held1", refill.ADD), ("New1", refill.ADD), ("Held2", refill.ADD), ("New2", refill.ADD),
        ("Held3", refill.HELD),
    ]
    assert _live_members(cfg, playlist_id) == ["Held3", "Held1", "New1", "Held2", "New2"]
    assert acted["data"]["totals"]["added"] == 4


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    code, refused = drive(_refill())
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing", refused


def test_the_digest_names_every_row_so_another_row_is_another_plan():
    from dataclasses import replace

    def one(content_id: str) -> refill.RefillPlan:
        member = set_playlist.Member(1, "Probe", "One", set_playlist.OWNED, content_id=content_id)
        target = refill.Target("pl-a", ACCOUNT, "j-1", "7", ACCOUNT, refill.BY_RECORD)
        target = replace(target, members=(member,), adds=(content_id,))
        return refill.RefillPlan(PASS, "intake", "3", "INBOX", (target,))
    assert digest_of(refill.identity(one("11"))) != digest_of(refill.identity(one("12")))


def test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror(
        native_library, silence, offline):
    """A later landing of the same pass makes ``Name 2`` with the same account and pass keys."""
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": (ACCOUNT, ("Held1", "New1", "Late"))})
    _stage(cfg, silence, "New1")
    _landed(cfg)
    _stage(cfg, silence, "Late")
    _landed(cfg)
    twin_id = _playlist_id(cfg, f"{INBOX_NAME} 2")
    assert _live_members(cfg, twin_id) == ["Late"]
    playlist_id = _emptied(cfg)
    acted, refused = _acted()
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Late"]
    assert _live_members(cfg, twin_id) == ["Late"]
    assert refused["cause"]["detail"]["shown"]["playlists"] == [
        f"{INBOX_NAME} (row {playlist_id}, {refill.BY_RECORD}): 3 track(s) the library owns, "
        f"3 to add, 0 left out"
    ]


def test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed(
        native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    _sql(cfg, "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", playlist_id)
    # A live playlist of the account's name, which the record does not name.
    other_id = _new_playlist(cfg, ACCOUNT, root_id)
    acted, _ = _acted()
    assert acted["outcome"] == "no_op", acted
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.UNFOUND]
    assert refill.GONE in warning["message"]
    assert _live_members(cfg, other_id) == []


def test_a_track_the_account_lists_twice_is_one_membership_and_counted_once(
        native_library, silence, offline, monkeypatch):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": (ACCOUNT, ("Held1", "New1"))})
    _stage(cfg, silence, "New1")
    _landed(cfg)
    playlist_id = _emptied(cfg)
    # The account lists Held1 a second time, after New1.
    real = set_playlist.reports_of
    twice = lambda store, job: (*real(store, job), real(store, job)[0])
    monkeypatch.setattr(set_playlist, "reports_of", twice)
    acted, refused = _acted()
    actions = [(i["title"], i["action"]) for i in refused["cause"]["detail"]["shown"]["items"]]
    assert actions == [("Held1", refill.ADD), ("New1", refill.ADD), ("Held1", refill.AGAIN)]
    totals = acted["data"]["totals"]
    assert (totals["add"], totals["held"], totals["again"]) == (2, 0, 1)
    assert _live_members(cfg, playlist_id) == ["Held1", "New1"]


def test_the_name_is_asked_only_of_a_playlist_no_record_gives_another_pass_and_only_if_read():
    from types import SimpleNamespace

    def row(row_id: str) -> SimpleNamespace:
        return SimpleNamespace(ID=row_id, Name=ACCOUNT, ParentID="root", Attribute=0, rb_local_deleted=0)
    under = {"1": row("1"), "2": row("2")}
    db = SimpleNamespace(get_playlist=lambda ID=None: under.get(ID))  # noqa: N803
    found = refill.locate(db, under, (), others=frozenset({"2"}), account="pl-a", name=ACCOUNT, job_id="j")
    assert isinstance(found, refill.Target)
    assert (found.playlist_id, found.found_by) == ("1", refill.BY_NAME)
    # Not trusted while a session record cannot be read.
    mine = {"1": under["1"]}
    found = refill.locate(db, mine, (), unreadable=1, account="pl-a", name=ACCOUNT, job_id="j")
    assert isinstance(found, refill.Unfound) and found.why == refill.UNREADABLE
    # One playlist two jobs answer to is neither job's.
    first = refill.Target("pl-a", ACCOUNT, "j1", "7", ACCOUNT, refill.BY_NAME)
    second = refill.Target("pl-b", ACCOUNT, "j2", "7", ACCOUNT, refill.BY_NAME)
    third = refill.Target("pl-c", "Deep Cuts", "j3", "8", "Deep Cuts", refill.BY_RECORD)
    shared = refill._shared([(None, first), (None, second), (None, third)])
    assert [type(one).__name__ for _job, one in shared] == ["Unfound", "Unfound", "Target"]
    assert {one.why for _job, one in shared[:2]} == {refill.SHARED}


def test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id():
    """An intake file's recorded name is asked only for its own account and pass (U175)."""
    closed, workflow = session.SessionState.CLOSED, native.WORKFLOW

    def record(tag, state, entries, *, ident="", workflow=workflow) -> session.SessionRecord:
        ident = ident or f"20261003T1200{tag}-landing"
        started = f"2026-10-03T12:00:{tag}+00:00"
        detail = {native.INBOX_PLAYLISTS_KEY: entries}
        return session.SessionRecord(ident, workflow, started, state, detail=detail)

    def entry(name: str, account: str, pass_name: str = PASS, **more) -> dict:
        return {"name": name, "batch": "b", "account": account, "pass": pass_name, **more}
    records = [
        # Started later, though its identifier sorts first: the order is by start.
        record("02", closed, [entry(f"{INBOX_NAME} 2", "pl-a")], ident="20261003T000000-a-landing"),
        # A record that no longer stands, and one of another workflow, name nothing.
        record("03", session.SessionState.ABANDONED, [entry("Abandoned 2026-10-03", "pl-a")]),
        record("04", closed, [entry("Elsewhere 2026-10-03", "pl-a")], workflow=refill.WORKFLOW),
        record("01", session.SessionState.AWAITING_IMPORT, [
            entry(INBOX_NAME, "pl-a"), entry("Deep Cuts 2026-10-03", "pl-b"),
            entry("Other pass 2026-10-03", "pl-a", "another_synced"),
            entry("Native 2026-10-03", "pl-a", id="77"),
        ]),
    ]
    found = refill.bridge_names(records, pass_name=PASS, account="pl-a")
    assert found == (INBOX_NAME, f"{INBOX_NAME} 2")
    assert refill.bridge_names(records, pass_name=PASS, account="pl-c") == ()


def test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one(
        native_library, silence, offline, monkeypatch):
    """R-1255: the plan carries the listing to its warning, never a count of one record."""
    cfg, root_id = native_library
    # A PASS WITH NO ACCOUNT PLAYLIST JOB is refused naming the pass.
    code, refused = drive(_refill("2026-01-01T000000Z-0000_synced"))
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "job-unknown", refused
    assert "2026-01-01T000000Z-0000_synced" in refused["cause"]["message"]
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # A PRE U128 RECORD IS MATCHED BY THE ACCOUNT'S EXACT NAME, so the
    # twin a second landing of the pass made (U113's ``Name 2``) is left.
    twin_id = _new_playlist(cfg, f"{ACCOUNT} 2", root_id)
    # The landing record rewritten as a landing before U128 wrote it, and a
    # second record of the same pass naming the twin.
    (landing,) = [r for r in session.records(cfg) if native.INBOX_PLAYLISTS_KEY in r.detail]
    _named_before_u175(cfg, playlist_id)
    stripped = [{"id": one["id"], "name": ACCOUNT} for one in landing.detail[native.INBOX_PLAYLISTS_KEY]]
    stripped.append({"id": twin_id, "name": f"{ACCOUNT} 2"})
    detail = {**landing.detail, native.INBOX_PLAYLISTS_KEY: stripped}
    records = [session.SessionRecord.from_json({**landing.to_json(), "detail": detail})]
    entries = refill.recorded_entries(records)
    found = refill.recorded_ids(entries, pass_name=PASS, account="pl-a", name=ACCOUNT)
    assert found == (playlist_id,)
    assert refill.recorded_ids(entries, pass_name="another_synced", account="pl-a", name=ACCOUNT) == ()
    # Then the log cannot be listed.
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))
    plan = refill_cli.planned(cfg, active_taxonomy.load(cfg), PASS)
    assert (plan.unreadable, plan.log_unlisted) == (1, True)
    warned = refill_cli.warnings_of(plan)
    (warning,) = [one for one in warned if one["code"] == refill_cli.RECORDS_UNREADABLE]
    assert warning["message"] == (
        "the session log could not be listed, so no account playlist without a readable "
        "landing record was found by its name"
    )


def test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name(
        native_library, silence, offline):
    """U175: an intake file names its playlist dated and records no id, so its name is asked."""
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # The record rewritten to the shape an intake file's landing writes: the
    # dated name, the batch folder, the account and the pass, and no id.
    batch = "2026-10-03 Tidal playlists"
    _rewrite_entries(cfg, lambda entries: [
        {**{k: v for k, v in one.items() if k != "id"}, "batch": batch} for one in entries
    ])
    acted, refused = _acted()
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    shown = refused["cause"]["detail"]["shown"]["playlists"]
    assert shown == [
        f"{INBOX_NAME} (row {playlist_id}, {refill.BY_NAME}): 5 track(s) "
        f"the library owns, 5 to add, 0 left out"
    ]
