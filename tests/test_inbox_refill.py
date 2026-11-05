"""U134: an INBOX account playlist is refilled from its recorded pass.

Driven against the disposable database the native landing suite builds. A
pass is swept and landed as U128 lands one, the INBOX playlist is emptied the
way sitting 34 emptied four of them, every native row removed and the files
dropped back in under new rows, and ``crate inbox refill --pass`` is driven
over it.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

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


def _refill(pass_name: str = PASS) -> list[str]:
    return ["inbox", "refill", "--pass", pass_name]


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    """R34's two acts against the refill's explicit gate, then the acting drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _playlist_id(cfg: config.Config, name: str) -> str:
    """The landing's INBOX playlist of this name, never its custom playlist twin (U149).

    Since U149 the landing also writes a twin of the same name into ``Custom
    Playlists <year>``, so the name alone names two live playlists; the one this
    suite refills is the one outside that folder.
    """
    (row,) = _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND rb_local_deleted = 0 "
        "AND ParentID NOT IN (SELECT ID FROM djmdPlaylist WHERE Name LIKE ? AND Attribute = 1)",
        name,
        f"{twins.FOLDER_PREFIX} %",
    )
    return str(row[0])


def _sql(cfg: config.Config, statement: str, *params) -> None:
    conn = sqlite3.connect(cfg.library.db_path)
    with conn:
        conn.execute(statement, params)
    conn.close()


def _emptied(cfg: config.Config, name: str = INBOX_NAME) -> str:
    """Sitting 34: every row of the playlist removed and dropped back in under a new id.

    Each member's content row is marked removed with its memberships, and a new
    live row is made for the same file, the way rekordbox makes one for a file
    dropped from Finder. The playlist is left live and empty.
    """
    playlist_id = _playlist_id(cfg, name)
    held = _members(cfg, playlist_id)
    for number, content_id in enumerate(held, start=1):
        ((title, folder),) = _query(
            cfg, "SELECT Title, FolderPath FROM djmdContent WHERE ID = ?", content_id
        )
        _sql(cfg, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", content_id)
        _sql(cfg, "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ContentID = ?", content_id)
        _sql(
            cfg,
            "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
            "updated_at) VALUES (?, ?, ?, 0, '2026-10-09', '2026-10-09')",
            f"9{number:04d}{content_id}",
            title,
            folder,
        )
    assert _live_members(cfg, playlist_id) == []
    return playlist_id


def _named_before_u175(cfg: config.Config, playlist_id: str) -> None:
    """The landed playlist renamed as a landing before U175 named it, the account's name alone.

    A record that names no account playlist, or names one by its name with no
    account and no pass, is a landing from before U128, and every such landing
    named its INBOX playlist undated; the refill's fallback by the account's
    exact name is for those. An intake file's landing since U175 records its
    dated name with the account and the pass, and is asked by that name.
    """
    _sql(cfg, "UPDATE djmdPlaylist SET Name = ? WHERE ID = ?", ACCOUNT, playlist_id)


def _live_members(cfg: config.Config, playlist_id: str) -> list[str]:
    titles = dict(_query(cfg, "SELECT ID, Title FROM djmdContent"))
    return [
        str(titles[str(row[0])])
        for row in _query(
            cfg,
            "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
            "AND rb_local_deleted = 0 ORDER BY TrackNo",
            playlist_id,
        )
    ]


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


# ---------------------------------------------------------------------------
# The scenarios the brief names
# ---------------------------------------------------------------------------


def test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order(
    native_library, silence, offline
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    rows_before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    # The rows are the library's new ones, and no content row was made.
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == rows_before
    assert acted["data"]["totals"]["added"] == 5
    assert acted["data"]["totals"]["read back"] == 5
    added = [item for item in refused["cause"]["detail"]["shown"]["items"] if item["action"] == "add"]
    assert [item["title"] for item in added] == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert not [w for w in acted["warnings"] if w["code"] == refill_cli.LEFT_OUT]
    # Recorded under the intake tree, with the playlist named.
    (record,) = [r for r in session.records(cfg) if r.workflow == refill.WORKFLOW]
    assert record.detail[refill.RECORD_KEY] == {
        "pass": PASS,
        "playlists": [{"id": playlist_id, "name": INBOX_NAME, "added": 5}],
    }


def test_a_track_the_library_lost_is_named_and_left(native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # New2's file is gone from disk. Its row stays, as rekordbox keeps a
    # missing file's row, and the row count stays where the fingerprint saw it.
    ((folder,),) = _query(
        cfg,
        "SELECT FolderPath FROM djmdContent WHERE Title = 'New2' AND rb_local_deleted = 0",
    )
    Path(folder).unlink()

    code, acted, _ = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "Held3"]
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.LEFT_OUT]
    assert f"{INBOX_NAME} 4. Probe - New2" in warning["message"]
    assert set_playlist.NOT_RESOLVED in warning["message"]


def test_a_second_run_plans_nothing_and_ends_no_op(native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    code, first, _ = _two_acts(_refill())
    assert code == int(ExitCode.OK), first

    code, again, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op", again
    assert again["data"]["totals"]["add"] == 0
    assert [w for w in again["warnings"] if w["code"] == refill_cli.NOTHING]
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    assert len([r for r in session.records(cfg) if r.workflow == refill.WORKFLOW]) == 1


def test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read(
    native_library, silence, monkeypatch
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    elsewhere = cutover_fixtures.add_folder(cfg, "Kept By Hand")
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", elsewhere, playlist_id)

    def unread(*_args, **_kwargs):
        raise AssertionError("a report of the pass was read before the refusal")

    monkeypatch.setattr(missing_cli, "job_reports", unread)
    code, refused = drive(_refill())

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == refill.OUTSIDE_INBOX, refused
    assert f"{INBOX_NAME!r} (row {playlist_id})" in refused["cause"]["message"]
    assert _live_members(cfg, playlist_id) == []
    assert not [r for r in session.records(cfg) if r.workflow == refill.WORKFLOW]


# ---------------------------------------------------------------------------
# How the playlist is found
# ---------------------------------------------------------------------------


def test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left(
    native_library, silence, offline
):
    """The live records of sitting 38 carry no account and no pass on their entries."""
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # A twin a second landing of the same pass made, named the way U113 named it.
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        twin = handle.create_playlist(f"{ACCOUNT} 2", parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        twin_id = str(twin.ID)
    finally:
        rb_writer.close_db(handle)
    # The landing record rewritten as a landing before U128 wrote it, and a
    # second record of the same pass naming the twin.
    (landing,) = [r for r in session.records(cfg) if native.INBOX_PLAYLISTS_KEY in r.detail]
    _named_before_u175(cfg, playlist_id)
    stripped = [{"id": one["id"], "name": ACCOUNT} for one in landing.detail[native.INBOX_PLAYLISTS_KEY]]
    stripped.append({"id": twin_id, "name": f"{ACCOUNT} 2"})
    records = [
        session.SessionRecord.from_json(
            {**landing.to_json(), "detail": {**landing.detail, native.INBOX_PLAYLISTS_KEY: stripped}}
        )
    ]

    entries = refill.recorded_entries(records)
    found = refill.recorded_ids(entries, pass_name=PASS, account="pl-a", name=ACCOUNT)

    assert found == (playlist_id,)
    assert refill.recorded_ids(entries, pass_name="another_synced", account="pl-a", name=ACCOUNT) == ()


def test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox(
    native_library, silence, offline
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # The playlist moved into a folder under INBOX, as the rotation moves a batch.
    old = cutover_fixtures.add_folder(cfg, "Old")
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", root_id, old)
    _sql(cfg, "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", old, playlist_id)
    # And no record names it: the record's account playlists are cleared, and
    # the playlist carries the undated name every such landing gave it.
    _named_before_u175(cfg, playlist_id)
    for record in session.records(cfg):
        if native.INBOX_PLAYLISTS_KEY in record.detail:
            record.detail[native.INBOX_PLAYLISTS_KEY] = []
            session.write_record(record, cfg)

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    shown = refused["cause"]["detail"]["shown"]["playlists"]
    assert shown == [f"{ACCOUNT} (row {playlist_id}, {refill.BY_NAME}): 5 track(s) "
                     f"the library owns, 5 to add, 0 left out"]


def test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name(
    native_library, silence, offline
):
    """U175: an intake file names its playlist dated and records no id, so its name is asked."""
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    # The record rewritten to the shape an intake file's landing writes: the
    # dated name, the batch folder, the account and the pass, and no id.
    for record in session.records(cfg):
        if native.INBOX_PLAYLISTS_KEY in record.detail:
            record.detail[native.INBOX_PLAYLISTS_KEY] = [
                {**{k: v for k, v in one.items() if k != "id"}, "batch": "2026-10-03 Tidal playlists"}
                for one in record.detail[native.INBOX_PLAYLISTS_KEY]
            ]
            session.write_record(record, cfg)

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Held2", "New2", "Held3"]
    shown = refused["cause"]["detail"]["shown"]["playlists"]
    assert shown == [
        f"{INBOX_NAME} (row {playlist_id}, {refill.BY_NAME}): 5 track(s) "
        f"the library owns, 5 to add, 0 left out"
    ]


def test_two_playlists_of_the_accounts_name_under_inbox_are_neither_filled(
    native_library, silence, offline
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    _named_before_u175(cfg, playlist_id)
    for record in session.records(cfg):
        if native.INBOX_PLAYLISTS_KEY in record.detail:
            record.detail[native.INBOX_PLAYLISTS_KEY] = []
            session.write_record(record, cfg)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist(ACCOUNT, parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op", acted
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.UNFOUND]
    assert refill.TWO_FOUND in warning["message"]
    assert _live_members(cfg, playlist_id) == []


def test_a_pass_with_no_account_playlist_job_is_refused_naming_the_pass(native_library):
    code, refused = drive(_refill("2026-01-01T000000Z-0000_synced"))

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "job-unknown", refused
    assert "2026-01-01T000000Z-0000_synced" in refused["cause"]["message"]


# ---------------------------------------------------------------------------
# What the write holds to
# ---------------------------------------------------------------------------


def test_a_playlist_that_holds_some_gets_only_what_it_lacks(native_library, silence, offline):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    ((held2,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE Title = 'Held2' AND rb_local_deleted = 0"
    )
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        rb_writer.add_memberships(handle, handle.get_playlist(ID=playlist_id), [str(held2)])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    actions = [
        (item["title"], item["action"])
        for item in refused["cause"]["detail"]["shown"]["items"]
    ]
    assert actions == [
        ("Held1", refill.ADD),
        ("New1", refill.ADD),
        ("Held2", refill.HELD),
        ("New2", refill.ADD),
        ("Held3", refill.ADD),
    ]
    assert _live_members(cfg, playlist_id) == ["Held2", "Held1", "New1", "New2", "Held3"]
    assert acted["data"]["totals"]["added"] == 4


def test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written(
    native_library, silence, offline
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    code, refused = drive(_refill())
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "apply", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    # A track added in rekordbox between the approval and the apply.
    ((held3,),) = _query(
        cfg, "SELECT ID FROM djmdContent WHERE Title = 'Held3' AND rb_local_deleted = 0"
    )
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        rb_writer.add_memberships(handle, handle.get_playlist(ID=playlist_id), [str(held3)])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, acted = drive(["--run", run_id, *_refill()])

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] in ("decision-stale", "decision-digest-mismatch"), acted
    assert _live_members(cfg, playlist_id) == ["Held3"]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(machine):
    code, refused = drive(_refill())

    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert refused["cause"]["reason"] == "backup-acknowledgment-missing", refused


def test_the_digest_names_every_row_so_another_row_is_another_plan():
    member = set_playlist.Member(1, "Probe", "One", set_playlist.OWNED, content_id="11")
    target = refill.Target(
        account="pl-a",
        account_name=ACCOUNT,
        job_id="j-1",
        playlist_id="7",
        name=ACCOUNT,
        found_by=refill.BY_RECORD,
        members=(member,),
        adds=("11",),
    )
    plan = refill.RefillPlan(
        pass_name=PASS, tree_id="intake", root_id="3", root_name="INBOX", targets=(target,)
    )
    other = refill.RefillPlan(
        pass_name=PASS,
        tree_id="intake",
        root_id="3",
        root_name="INBOX",
        targets=(
            refill.Target(
                **{
                    **{name: getattr(target, name) for name in refill.Target.__slots__},
                    "members": (
                        set_playlist.Member(1, "Probe", "One", set_playlist.OWNED, content_id="12"),
                    ),
                    "adds": ("12",),
                }
            ),
        ),
    )
    assert digest_of(refill.identity(plan)) != digest_of(refill.identity(other))


def test_the_job_store_is_read_not_written_by_a_plan(native_library, silence, offline):
    cfg, root_id = native_library
    _five_landed_and_emptied(cfg, silence)
    with jobs.open_store() as store:
        before = [(job.job_id, job.state) for job in jobs.list_jobs(store)]

    code, refused = drive(_refill())

    assert code == int(ExitCode.DECISION_REQUIRED), refused
    with jobs.open_store() as store:
        assert [(job.job_id, job.state) for job in jobs.list_jobs(store)] == before


# ---------------------------------------------------------------------------
# The review's findings, driven
# ---------------------------------------------------------------------------


def test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror(
    native_library, silence, offline
):
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

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert _live_members(cfg, playlist_id) == ["Held1", "New1", "Late"]
    assert _live_members(cfg, twin_id) == ["Late"]
    assert refused["cause"]["detail"]["shown"]["playlists"] == [
        f"{INBOX_NAME} (row {playlist_id}, {refill.BY_RECORD}): 3 track(s) the library owns, "
        f"3 to add, 0 left out"
    ]


def test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed(
    native_library, silence, offline
):
    cfg, root_id = native_library
    playlist_id = _five_landed_and_emptied(cfg, silence)
    _sql(cfg, "UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", playlist_id)
    # A live playlist of the account's name, which the record does not name.
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        other = handle.create_playlist(ACCOUNT, parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        other_id = str(other.ID)
    finally:
        rb_writer.close_db(handle)

    code, acted, _ = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op", acted
    (warning,) = [w for w in acted["warnings"] if w["code"] == refill_cli.UNFOUND]
    assert refill.GONE in warning["message"]
    assert _live_members(cfg, other_id) == []


def test_a_track_the_account_lists_twice_is_one_membership_and_counted_once(
    native_library, silence, offline, monkeypatch
):
    cfg, root_id = native_library
    _owned(cfg, silence, ("Held1",))
    swept(cfg, {"pl-a": (ACCOUNT, ("Held1", "New1"))})
    _stage(cfg, silence, "New1")
    _landed(cfg)
    playlist_id = _emptied(cfg)
    # The account lists Held1 a second time, after New1.
    real = set_playlist.reports_of
    monkeypatch.setattr(
        set_playlist, "reports_of", lambda store, job: (*real(store, job), real(store, job)[0])
    )

    code, acted, refused = _two_acts(_refill())

    assert code == int(ExitCode.OK), acted
    actions = [(i["title"], i["action"]) for i in refused["cause"]["detail"]["shown"]["items"]]
    assert actions == [("Held1", refill.ADD), ("New1", refill.ADD), ("Held1", refill.AGAIN)]
    totals = acted["data"]["totals"]
    assert (totals["add"], totals["held"], totals["again"]) == (2, 0, 1)
    assert _live_members(cfg, playlist_id) == ["Held1", "New1"]


class _Row:
    def __init__(self, row_id: str, name: str, *, parent: str = "root") -> None:
        self.ID = row_id
        self.Name = name
        self.ParentID = parent
        self.Attribute = 0
        self.rb_local_deleted = 0


class _Db:
    def __init__(self, *rows: _Row) -> None:
        self._rows = {row.ID: row for row in rows}

    def get_playlist(self, ID=None):  # noqa: N803 - the binding's spelling
        return self._rows.get(ID)


def test_the_name_is_not_asked_of_a_playlist_a_record_gives_another_pass():
    mine, theirs = _Row("1", ACCOUNT), _Row("2", ACCOUNT)
    under = {"1": mine, "2": theirs}

    found = refill.locate(
        _Db(mine, theirs), under, (), others=frozenset({"2"}), account="pl-a", name=ACCOUNT, job_id="j"
    )

    assert isinstance(found, refill.Target)
    assert (found.playlist_id, found.found_by) == ("1", refill.BY_NAME)


def test_the_name_is_not_trusted_while_a_session_record_cannot_be_read():
    mine = _Row("1", ACCOUNT)

    found = refill.locate(
        _Db(mine), {"1": mine}, (), unreadable=1, account="pl-a", name=ACCOUNT, job_id="j"
    )

    assert isinstance(found, refill.Unfound) and found.why == refill.UNREADABLE


def test_one_playlist_two_jobs_answer_to_is_neither_jobs():
    first = refill.Target("pl-a", ACCOUNT, "j1", "7", ACCOUNT, refill.BY_NAME)
    second = refill.Target("pl-b", ACCOUNT, "j2", "7", ACCOUNT, refill.BY_NAME)
    third = refill.Target("pl-c", "Deep Cuts", "j3", "8", "Deep Cuts", refill.BY_RECORD)

    shared = refill._shared([(None, first), (None, second), (None, third)])

    assert [type(one).__name__ for _job, one in shared] == ["Unfound", "Unfound", "Target"]
    assert {one.why for _job, one in shared[:2]} == {refill.SHARED}


def test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id():
    """An intake file's recorded name is asked only for its own account and pass (U175)."""

    def record(
        tag: str,
        state: session.SessionState,
        entries: list[dict],
        *,
        ident: str = "",
        workflow: str = native.WORKFLOW,
    ) -> session.SessionRecord:
        return session.SessionRecord(
            session_id=ident or f"20261003T1200{tag}-landing",
            workflow=workflow,
            started=f"2026-10-03T12:00:{tag}+00:00",
            state=state,
            detail={native.INBOX_PLAYLISTS_KEY: entries},
        )

    def entry(name: str, account: str, pass_name: str = PASS, **more) -> dict:
        return {"name": name, "batch": "b", "account": account, "pass": pass_name, **more}

    records = [
        # Started later, though its identifier sorts first: the order is by start.
        record(
            "02",
            session.SessionState.CLOSED,
            [entry(f"{INBOX_NAME} 2", "pl-a")],
            ident="20261003T000000-a-landing",
        ),
        # A record that no longer stands, and one of another workflow, name nothing.
        record("03", session.SessionState.ABANDONED, [entry("Abandoned 2026-10-03", "pl-a")]),
        record(
            "04",
            session.SessionState.CLOSED,
            [entry("Elsewhere 2026-10-03", "pl-a")],
            workflow=refill.WORKFLOW,
        ),
        record(
            "01",
            session.SessionState.AWAITING_IMPORT,
            [
                entry(INBOX_NAME, "pl-a"),
                entry("Deep Cuts 2026-10-03", "pl-b"),
                entry("Other pass 2026-10-03", "pl-a", "another_synced"),
                entry("Native 2026-10-03", "pl-a", id="77"),
            ],
        ),
    ]

    assert refill.bridge_names(records, pass_name=PASS, account="pl-a") == (
        INBOX_NAME,
        f"{INBOX_NAME} 2",
    )
    assert refill.bridge_names(records, pass_name=PASS, account="pl-c") == ()


def test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan(
    native_library, silence, offline, monkeypatch
):
    """R-1255: the plan carries the listing to its warning, never a count of one record."""
    cfg, _root = native_library
    _five_landed_and_emptied(cfg, silence)
    _refuse_listing(monkeypatch, Path(session.log_dir(cfg)))

    plan = refill_cli.planned(cfg, active_taxonomy.load(cfg), PASS)

    assert (plan.unreadable, plan.log_unlisted) == (1, True)
    (warning,) = [
        one for one in refill_cli.warnings_of(plan) if one["code"] == refill_cli.RECORDS_UNREADABLE
    ]
    assert warning["message"] == (
        "the session log could not be listed, so no account playlist without a readable "
        "landing record was found by its name"
    )
