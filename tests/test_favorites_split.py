"""U145: ``crate favorites split`` turns the quarter playlists under Favorites into months.

Driven through the real dispatcher on the native landing suite's library: hearts
jobs run by hand, their tracks in the library with nothing placing them, and the
quarter playlists U120 left made by hand. The plan dates each member by its job,
else the account; the approval fills the months in one commit and retires the
quarters in a second.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest

from cratekit.core import analysis_store, jobs, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import placement, split, split_cli
from cratekit.intake import missing_cli
from tests.cli_drive import drive
from tests.test_favorites_backfill import (
    _account,
    _db,
    _landed_hearts,
    _live,
    _note,
    _put,
    _rows,
    _seed,
    _take_out,
)
from tests.test_favorites_backfill import home as home  # noqa: PLC0414
from tests.test_intake_land_hearts_native import SOURCE, UNKNOWN, _favorites, _home, hearts_swept
from tests.test_intake_land_hearts_native import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

VERB = ["favorites", "split"]
GATE = split_cli.APPROVE_GATE
UTC = timezone.utc
OCT = "2026-10-{day:02d}T12:00:00+00:00"
NOV = "2026-11-03T12:00:00+00:00"
AUG = datetime(2026, 8, 2, 9, 0, tzinfo=UTC)


def _quarter(cfg, folder_id: str, name: str, *titles: str) -> str:
    """A quarter playlist under the folder holding the rows of these titles, as U120 left one."""
    rows = _rows(cfg)
    with _db(cfg) as handle:
        parent = handle.get_playlist(ID=folder_id) if folder_id else None
        made = handle.create_playlist(name, parent=parent)
        for title in titles:
            handle.add_to_playlist(made, rows[title])
        made_id = str(made.ID)
    return made_id


def _acts(verb: list[str] = VERB) -> tuple[int, dict, dict]:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == GATE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


def _approved(verb: list[str] = VERB) -> tuple[dict, dict]:
    """The verb's two acts, approved, ending OK: the answer and what the gate showed."""
    code, acted, refused = _acts(verb)
    assert code == int(ExitCode.OK), acted
    return acted, refused["cause"]["detail"]["shown"]


def _removed(cfg, playlist_id: str) -> bool:
    ((marker,),) = _query(cfg, "SELECT rb_local_deleted FROM djmdPlaylist WHERE ID = ?", playlist_id)
    return bool(marker)


def _staged(native_library, silence, titles: dict[str, str | None], *quarters: tuple[str, ...]):
    """The home, the hearts and each quarter of ``(name, *titles)``: the cfg, folder and rows."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _landed_hearts(cfg, silence, titles)
    return cfg, folder_id, [_quarter(cfg, folder_id, *one) for one in quarters]


def _written_refused(cfg, approved) -> CratekitError:
    with pytest.raises(CratekitError) as caught:
        split_cli.written(cfg, approved, source=SOURCE)
    return caught.value


def test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired(
    native_library, silence, monkeypatch
):
    october = [f"Oct {n:02d}" for n in range(1, 16)]
    november = ["Nov A", "Nov B"]
    titles = {title: OCT.format(day=n) for n, title in enumerate(october, start=1)}
    titles.update({title: NOV for title in november})
    cfg, folder_id, (q4,) = _staged(
        native_library, silence, titles, ("2026-Q4", *october, *november)
    )
    fake = _account(monkeypatch, {})

    acted, shown = _approved()

    assert shown["quarters to retire"] == ["2026-Q4 (17)"]
    assert shown["month playlists"] == ["2026-10 (15), made", "2026-11 (2), made"]
    assert shown["memberships to add"] == 17
    assert "undated" not in shown
    assert fake.heart_listings == 0, "every member is dated by its job, so the account is never asked"
    found = _favorites(cfg, folder_id)
    assert sorted(found["2026-10"]) == sorted(october)
    assert sorted(found["2026-11"]) == sorted(november)
    assert "2026-Q4" not in found and _removed(cfg, q4)
    assert set(found) == {SOURCE, "2026-10", "2026-11"}
    totals = acted["data"]["totals"]
    assert (totals["added"], totals["created"], totals["retired"]) == (17, 2, 1)
    note = _note(acted, split_cli.SPLIT)
    assert "17 membership(s) added for 17 member(s) of 1 quarter playlist(s)" in note
    assert "2026-10 15 (made), 2026-11 2 (made)" in note
    assert "2026-Q4 retired" in note


def test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated(
    native_library, silence, monkeypatch
):
    # Two hearts whose job froze no date key, as every job before U120 did.
    cfg, folder_id, (q3,) = _staged(
        native_library, silence, {"Summer": None, "Nowhere": None}, ("2026-Q3", "Summer", "Nowhere")
    )
    fake = _account(monkeypatch, {"Summer": AUG, "Nowhere": None})

    acted, shown = _approved()

    assert shown["month playlists"] == ["2026-08 (1), made", "Undated (1), made"]
    # The row's artist is linked, so the screen names it (U163).
    assert shown["undated"] == [f"Probe - Nowhere (row {_rows(cfg)['Nowhere']}, from 2026-Q3)"]
    totals = acted["data"]["totals"]
    assert (totals["dates from the account"], totals["dates from jobs"], totals["undated"]) == (1, 0, 1)
    assert fake.heart_listings == 2, "listed once per plan, and the two acts are two plans"
    found = _favorites(cfg, folder_id)
    assert found["2026-08"] == ["Summer"] and found["Undated"] == ["Nowhere"]
    assert _removed(cfg, q3)
    assert "Nowhere (from 2026-Q3)" in _note(acted, split_cli.UNDATED)


def test_a_second_run_plans_nothing_and_opens_no_gate(native_library, silence, monkeypatch):
    cfg, folder_id, _quarters = _staged(
        native_library, silence, {"Once": OCT.format(day=20)}, ("2026-Q4", "Once")
    )
    _account(monkeypatch, {})
    _approved()
    before = _query(cfg, "SELECT ID, rb_local_deleted, updated_at FROM djmdSongPlaylist ORDER BY ID")

    code, acted = drive(VERB)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert "nothing to split" in _note(acted, split_cli.NOTHING_TO_SPLIT)
    assert acted["data"]["items"] == []
    assert _query(cfg, "SELECT ID, rb_local_deleted, updated_at FROM djmdSongPlaylist ORDER BY ID") == before
    assert _favorites(cfg, folder_id) == {SOURCE: [], "2026-10": ["Once"]}


def test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account(
    native_library, silence, monkeypatch
):
    _staged(native_library, silence, {"Kept": None})
    fake = _account(monkeypatch, {"Kept": AUG})

    def walked(*_args, **_kwargs):
        raise AssertionError("the library was walked with no quarter to split")

    monkeypatch.setattr(split.match_cli, "library_view", walked)

    code, acted = drive(VERB)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op" and fake.heart_listings == 0


def test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire(
    native_library, silence, monkeypatch
):
    cfg, folder_id, (q3, q4) = _staged(
        native_library,
        silence,
        {"Twice": NOV, "Once": OCT.format(day=2)},
        ("2026-Q3", "Twice"),
        ("2026-Q4", "Twice", "Once"),
    )
    _account(monkeypatch, {})

    acted, shown = _approved()

    assert shown["quarters to retire"] == ["2026-Q3 (1)", "2026-Q4 (2)"]
    found = _favorites(cfg, folder_id)
    assert found["2026-11"] == ["Twice"] and found["2026-10"] == ["Once"]
    assert _removed(cfg, q3) and _removed(cfg, q4)


def test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice(
    native_library, silence, monkeypatch
):
    cfg, _folder_id, (october, _q4) = _staged(
        native_library,
        silence,
        {"Held": OCT.format(day=5), "New": OCT.format(day=6)},
        ("2026-10", "Held"),
        ("2026-Q4", "Held", "New"),
    )
    _account(monkeypatch, {})

    acted, shown = _approved()

    assert shown["month playlists"] == ["2026-10 (2)"]
    assert shown["memberships to add"] == 1
    assert _live(cfg, october) == [_rows(cfg)["Held"], _rows(cfg)["New"]]


def test_the_record_carries_both_commits_under_the_favourites_key(native_library, silence, monkeypatch):
    cfg, _folder_id, _quarters = _staged(
        native_library, silence, {"One": OCT.format(day=1), "Two": NOV}, ("2026-Q4", "One", "Two")
    )
    _account(monkeypatch, {})

    acted, _shown = _approved()

    (record,) = [r for r in session.records(cfg) if r.workflow == split.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert [(c.tree, c.created, c.updated) for c in record.change.trees] == [
        (placement.RECORD_KEY, 2, 1)
    ]
    assert record.session_id in _note(acted, split_cli.SPLIT)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(native_library, silence, monkeypatch):
    cfg, _folder_id, _quarters = _staged(native_library, silence, {"One": NOV}, ("2026-Q4", "One"))
    fake = _account(monkeypatch, {})
    session.ack_path(cfg).unlink()

    code, refused = drive(VERB)

    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})
    assert fake.heart_listings == 0


def test_with_no_source_playlist_the_verb_refuses_by_name(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    _landed_hearts(cfg, silence, {"One": NOV})
    _account(monkeypatch, {})

    code, refused = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == placement.SOURCE_MISSING


def test_a_quarter_that_changed_after_the_approval_is_refused_and_nothing_is_written(
    native_library, silence, monkeypatch
):
    cfg, folder_id, (q4,) = _staged(
        native_library, silence, {"One": NOV, "Late": OCT.format(day=9)}, ("2026-Q4", "One")
    )
    _account(monkeypatch, {})
    approved = split_cli.planned(cfg, source=SOURCE)
    _put(cfg, q4, _rows(cfg)["Late"])

    assert _written_refused(cfg, approved).cause.reason == "decision-stale"
    assert not _removed(cfg, q4)
    assert set(_favorites(cfg, folder_id)) == {SOURCE, "2026-Q4"}


def test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes(
    native_library, silence, monkeypatch
):
    cfg, folder_id, (q4,) = _staged(
        native_library, silence, {"One": OCT.format(day=1), "Two": NOV}, ("2026-Q4", "One", "Two")
    )
    _account(monkeypatch, {})
    approved = split_cli.planned(cfg, source=SOURCE)

    def stopped(_db, _row):
        raise RuntimeError("the machine went to sleep")

    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_playlist_node", stopped)
        with pytest.raises(RuntimeError, match="went to sleep"):
            split_cli.written(cfg, approved, source=SOURCE)

    found = _favorites(cfg, folder_id)
    assert found["2026-10"] == ["One"] and found["2026-11"] == ["Two"]
    assert "2026-Q4" in found and not _removed(cfg, q4)
    again = split_cli.planned(cfg, source=SOURCE)
    assert again.digest == approved.digest
    assert again.adds == 0 and again.creates == ()

    done = split_cli.written(cfg, again, source=SOURCE)

    assert done.added == 0 and done.retired == ("2026-Q4",) and not done.disagreements
    assert _removed(cfg, q4)
    assert _favorites(cfg, folder_id) == {SOURCE: [], "2026-10": ["One"], "2026-11": ["Two"]}


def test_the_writer_refuses_a_membership_the_plan_did_not_name(native_library, silence, monkeypatch):
    cfg, folder_id, (q4,) = _staged(
        native_library, silence, {"One": NOV, "Stray": OCT.format(day=3)}, ("2026-Q4", "One")
    )
    _account(monkeypatch, {})
    approved = split_cli.planned(cfg, source=SOURCE)
    stray = _rows(cfg)["Stray"]
    real = rb_writer.add_memberships
    monkeypatch.setattr(
        rb_writer, "add_memberships", lambda db, playlist, ids: real(db, playlist, [*ids, stray])
    )

    refused = _written_refused(cfg, approved)

    assert refused.cause.reason == "whitelist-violation"
    assert f"puts row {stray!r}" in refused.cause.message
    assert set(_favorites(cfg, folder_id)) == {SOURCE, "2026-Q4"}
    assert not _removed(cfg, q4)


def test_a_quarter_whose_member_its_month_lacks_is_not_retired(native_library, silence, monkeypatch):
    cfg, _folder_id, (q4,) = _staged(
        native_library, silence, {"One": NOV, "Two": OCT.format(day=8)}, ("2026-Q4", "One", "Two")
    )
    _account(monkeypatch, {})
    approved = split_cli.planned(cfg, source=SOURCE)
    real = rb_writer.add_memberships
    two = _rows(cfg)["Two"]
    monkeypatch.setattr(
        rb_writer,
        "add_memberships",
        lambda db, playlist, ids: real(db, playlist, [one for one in ids if one != two]),
    )

    refused = _written_refused(cfg, approved)

    assert refused.cause.reason == "session-committed-unverified"
    assert "no quarter was retired" in refused.cause.message
    assert not _removed(cfg, q4)


def test_the_retirement_is_confined_to_the_quarters(home, silence, monkeypatch):
    cfg, folder_id, source_id = home
    _landed_hearts(cfg, silence, {"One": NOV})
    q4 = _quarter(cfg, folder_id, "2026-Q4", "One")
    _account(monkeypatch, {})
    approved = split_cli.planned(cfg, source=SOURCE)
    real = rb_writer.remove_playlist_node

    def reaches_further(db, row):
        marked = real(db, row)
        real(db, db.get_playlist(ID=source_id))
        return marked

    monkeypatch.setattr(rb_writer, "remove_playlist_node", reaches_further)

    assert _written_refused(cfg, approved).cause.reason == "whitelist-violation"
    assert not _removed(cfg, q4) and not _removed(cfg, source_id)


def test_no_content_row_tempo_or_grid_is_written(native_library, silence, monkeypatch):
    """The standing constraint, read from SQL across the whole split."""
    cfg, _folder_id, _quarters = _staged(
        native_library, silence, {"One": NOV, "Two": OCT.format(day=4)}, ("2026-Q4", "One", "Two")
    )
    _account(monkeypatch, {})
    before = _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")

    acted, _shown = _approved()

    assert _query(cfg, "SELECT * FROM djmdContent ORDER BY ID") == before
    assert analysis_store.watch_roots(cfg)


def _tables(playlists: dict, memberships: dict, content: dict | None = None) -> rb_writer.NodeTables:
    return rb_writer.NodeTables(
        content=content or {"1": "a", "2": "b"},
        playlists=playlists,
        memberships=memberships,
        playlist_columns=("ID", "Name", "ParentID", "Attribute", "Seq", "rb_local_deleted", "updated_at"),
        membership_columns=("ID", "PlaylistID", "ContentID", "TrackNo", "rb_local_deleted"),
    )


FOLDER = ("f", "Favorites", "root", 1, 1, 0, "t0")
QUARTER = ("q", "2026-Q4", "f", 0, 1, 0, "t0")
MONTH = ("m", "2026-10", "f", 0, 2, 0, "t1")
IN_QUARTER = ("s1", "q", "1", 1, 0)


def _before() -> rb_writer.NodeTables:
    return _tables({"f": FOLDER, "q": QUARTER}, {"s1": IN_QUARTER})


def test_a_planned_addition_into_a_made_month_is_confined():
    after = _tables({"f": FOLDER, "q": QUARTER, "m": MONTH}, {"s1": IN_QUARTER, "s2": ("s2", "m", "1", 1, 0)})
    assert split.addition_violations(
        _before(), after, planned={"m": ["1"]}, created={"m": ("2026-10", "f")}
    ) == []


@pytest.mark.parametrize(
    ("shape", "expected"),
    [
        ("unplanned row", "puts row '2'"),
        ("wrong playlist", "puts row '1' in playlist 'q'"),
        ("removed addition", "puts row '1'"),
        ("changed membership", "row 's1' changed"),
        ("gone membership", "row 's1' disappeared"),
        ("unplanned playlist", "unplanned djmdPlaylist row 'x'"),
        ("wrong name", "not a live plain playlist named '2026-10'"),
        ("wrong parent", "not a live plain playlist named '2026-10' under 'f'"),
        ("not made", "was not made"),
        ("quarter renamed", "row 'q' changed ['Name']"),
        ("content", "djmdContent row changed"),
    ],
)
def test_an_addition_the_plan_did_not_name_is_a_violation(shape, expected):
    playlists = {"f": FOLDER, "q": QUARTER, "m": MONTH}
    memberships = {"s1": IN_QUARTER, "s2": ("s2", "m", "1", 1, 0)}
    content = None
    created = {"m": ("2026-10", "f")}
    if shape == "unplanned row":
        memberships["s3"] = ("s3", "m", "2", 2, 0)
    elif shape == "wrong playlist":
        memberships["s3"] = ("s3", "q", "1", 2, 0)
    elif shape == "removed addition":
        memberships["s2"] = ("s2", "m", "1", 1, 1)
    elif shape == "changed membership":
        memberships["s1"] = ("s1", "q", "1", 1, 1)
    elif shape == "gone membership":
        del memberships["s1"]
    elif shape == "unplanned playlist":
        playlists["x"] = ("x", "2026-11", "f", 0, 3, 0, "t1")
    elif shape == "wrong name":
        playlists["m"] = ("m", "2026-1", "f", 0, 2, 0, "t1")
    elif shape == "wrong parent":
        playlists["m"] = ("m", "2026-10", "root", 0, 2, 0, "t1")
    elif shape == "not made":
        created = {"m": ("2026-10", "f"), "n": ("2026-11", "f")}
    elif shape == "quarter renamed":
        playlists["q"] = ("q", "2026-Q3", "f", 0, 1, 0, "t0")
    elif shape == "content":
        content = {"1": "a", "2": "changed"}
    after = _tables(playlists, memberships, content)

    violations = split.addition_violations(_before(), after, planned={"m": ["1"]}, created=created)

    assert any(expected in one for one in violations), violations


def test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires(
    home, silence, monkeypatch
):
    """The backfill's rule: a heart the author took back is never put back."""
    cfg, folder_id, source_id = home
    _landed_hearts(cfg, silence, {"Kept": NOV, "Dropped": NOV})
    rows = _rows(cfg)
    _put(cfg, source_id, rows["Kept"])
    _put(cfg, source_id, rows["Dropped"])
    _take_out(cfg, source_id, rows["Dropped"])
    q4 = _quarter(cfg, folder_id, "2026-Q4", "Kept", "Dropped")
    _account(monkeypatch, {})

    acted, shown = _approved()

    assert shown["month playlists"] == ["2026-11 (1), made"]
    assert shown["taken back"] == [
        f"Probe - Dropped (row {rows['Dropped']}, from 2026-Q4), removed from {SOURCE!r} in rekordbox"
    ]
    assert _favorites(cfg, folder_id)["2026-11"] == ["Kept"]
    assert _removed(cfg, q4)
    assert "Dropped (from 2026-Q4)" in _note(acted, split_cli.TAKEN_BACK)


def test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention(
    home, silence, monkeypatch
):
    cfg, folder_id, _source_id = home
    # The oldest job froze no date, the next dated it in October, the last in November.
    hearts_swept(cfg, {"Often": UNKNOWN}, run_id="")
    hearts_swept(cfg, {"Often": OCT.format(day=7)}, run_id="")
    _landed_hearts(cfg, silence, {"Often": NOV}, batch="2026-11-04-favorites")
    _quarter(cfg, folder_id, "2026-Q4", "Often")
    _account(monkeypatch, {})
    asked: list[str] = []
    real = split.match.resolve_one

    def counted(track, *args, **kwargs):
        asked.append(track.ref)
        return real(track, *args, **kwargs)

    monkeypatch.setattr(split.match, "resolve_one", counted)

    acted, _shown = _approved()

    assert _favorites(cfg, folder_id)["2026-10"] == ["Often"]
    assert asked == ["tid-Often", "tid-Often"], "once per plan, and the two acts are two plans"


def test_the_one_removal_the_favourites_package_makes_is_the_splits_quarter_retirement():
    """Nothing under favorites/ takes a membership out of a playlist that lives on."""
    calls: list[tuple[str, str]] = []
    for path in sorted(Path(split.__file__).resolve().parent.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"remove_memberships", "remove_playlist_node", "remove_from_playlist"}:
                    calls.append((path.name, node.func.attr))
    assert calls == [("split.py", "remove_playlist_node")]


def test_a_job_row_owned_when_its_job_ran_still_dates_the_member(home, silence, monkeypatch):
    """The quarters hold owned hearts above all, so every match state is read."""
    cfg, folder_id, _source_id = home
    _seed(cfg, silence, "Owned", batch="2026-09-01-favorites")
    job = hearts_swept(cfg, {"Owned": OCT.format(day=11)}, run_id="")
    _quarter(cfg, folder_id, "2026-Q4", "Owned")
    fake = _account(monkeypatch, {})

    acted, _shown = _approved()

    with jobs.open_store() as store:
        states = {report.get("state") for report in missing_cli.job_reports(store, job)}
    assert states == {"owned"}, "the heart was owned when its job ran"
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id)["2026-10"] == ["Owned"]


def test_a_heart_taken_back_and_hearted_again_is_not_taken_back(home, silence, monkeypatch):
    cfg, folder_id, source_id = home
    _landed_hearts(cfg, silence, {"Again": NOV})
    again = _rows(cfg)["Again"]
    _put(cfg, source_id, again)
    _take_out(cfg, source_id, again)
    _put(cfg, source_id, again)
    _quarter(cfg, folder_id, "2026-Q4", "Again")
    _account(monkeypatch, {})

    acted, shown = _approved()

    assert "taken back" not in shown
    assert _favorites(cfg, folder_id)["2026-11"] == ["Again"]


def test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month(native_library, silence, monkeypatch):
    """R-758: a membership rekordbox marked removed is not a member."""
    cfg, folder_id, (q4,) = _staged(
        native_library, silence, {"Stays": NOV, "Went": OCT.format(day=12)}, ("2026-Q4", "Stays", "Went")
    )
    _take_out(cfg, q4, _rows(cfg)["Went"])
    _account(monkeypatch, {})

    acted, shown = _approved()

    assert shown["quarters to retire"] == ["2026-Q4 (1)"]
    assert _favorites(cfg, folder_id) == {SOURCE: [], "2026-11": ["Stays"]}
