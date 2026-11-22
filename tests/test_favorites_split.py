"""U145: ``crate favorites split`` turns the quarter playlists under Favorites into months."""

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
from tests.test_favorites_backfill import _approved as _backfill_approved
from tests.test_favorites_backfill import _silent as _silent  # noqa: PLC0414
from tests.test_favorites_backfill import given as given  # noqa: PLC0414
from tests.test_favorites_backfill import home as home  # noqa: PLC0414
from tests.test_favorites_backfill import silence as silence  # noqa: PLC0414
from tests.test_intake_land_hearts_native import SOURCE, UNKNOWN, _favorites, hearts_swept
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
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture

VERB = ["favorites", "split"]
GATE = split_cli.APPROVE_GATE
UTC = timezone.utc
OCT = "2026-10-{day:02d}T12:00:00+00:00"
NOV = "2026-11-03T12:00:00+00:00"
AUG = datetime(2026, 8, 2, 9, 0, tzinfo=UTC)
MEMBERSHIPS = "SELECT ID, rb_local_deleted, updated_at FROM djmdSongPlaylist ORDER BY ID"


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


def _approved(verb: list[str] = VERB) -> tuple[dict, dict]:
    """The verb's two acts, approved, ending OK: the answer and what the gate showed."""
    return _backfill_approved(verb, GATE)


def _removed(cfg, playlist_id: str) -> bool:
    ((marker,),) = _query(cfg, "SELECT rb_local_deleted FROM djmdPlaylist WHERE ID = ?", playlist_id)
    return bool(marker)


@pytest.fixture
def staged(given):
    """Hearts in ``home``, the account bound (empty by default) and each ``(name, *titles)``."""
    def made(titles: dict, *quarters: tuple[str, ...], dates: dict | None = None):
        cfg, folder_id, _source_id, fake = given(titles, dates or {})
        return cfg, folder_id, [_quarter(cfg, folder_id, *one) for one in quarters], fake
    return made


def _written_refused(cfg, approved) -> CratekitError:
    with pytest.raises(CratekitError) as caught:
        split_cli.written(cfg, approved, source=SOURCE)
    return caught.value


def _rewritten(monkeypatch, cfg, change) -> CratekitError:
    """The planned split written with ``rb_writer.add_memberships`` handed ``change(ids)``."""
    approved = split_cli.planned(cfg, source=SOURCE)
    real = rb_writer.add_memberships
    monkeypatch.setattr(
        rb_writer, "add_memberships", lambda db, playlist, ids: real(db, playlist, change(ids))
    )
    return _written_refused(cfg, approved)


def test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired(staged):
    october = [f"Oct {n:02d}" for n in range(1, 16)]
    november = ["Nov A", "Nov B"]
    titles = {title: OCT.format(day=n) for n, title in enumerate(october, start=1)}
    titles.update({title: NOV for title in november})
    cfg, folder_id, (q4,), fake = staged(titles, ("2026-Q4", *october, *november))
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
    staged,
):
    # Two hearts whose job froze no date key, as every job before U120 did.
    cfg, folder_id, (q3,), fake = staged(
        {"Summer": None, "Nowhere": None}, ("2026-Q3", "Summer", "Nowhere"),
        dates={"Summer": AUG, "Nowhere": None},
    )
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


def test_a_second_run_plans_nothing_and_opens_no_gate(staged):
    cfg, folder_id, _quarters, _fake = staged({"Once": OCT.format(day=20)}, ("2026-Q4", "Once"))
    _approved()
    before = _query(cfg, MEMBERSHIPS)
    code, acted = drive(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert "nothing to split" in _note(acted, split_cli.NOTHING_TO_SPLIT)
    assert acted["data"]["items"] == []
    assert _query(cfg, MEMBERSHIPS) == before
    assert _favorites(cfg, folder_id) == {SOURCE: [], "2026-10": ["Once"]}


def test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account(staged, monkeypatch):
    _cfg, _folder_id, _quarters, fake = staged({"Kept": None}, dates={"Kept": AUG})
    def walked(*_args, **_kwargs):
        raise AssertionError("the library was walked with no quarter to split")
    monkeypatch.setattr(split.match_cli, "library_view", walked)
    code, acted = drive(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op" and fake.heart_listings == 0


def test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire(staged):
    cfg, folder_id, (q3, q4), _fake = staged(
        {"Twice": NOV, "Once": OCT.format(day=2)}, ("2026-Q3", "Twice"), ("2026-Q4", "Twice", "Once")
    )
    acted, shown = _approved()
    assert shown["quarters to retire"] == ["2026-Q3 (1)", "2026-Q4 (2)"]
    found = _favorites(cfg, folder_id)
    assert found["2026-11"] == ["Twice"] and found["2026-10"] == ["Once"]
    assert _removed(cfg, q3) and _removed(cfg, q4)


def test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice(staged):
    cfg, _folder_id, (october, _q4), _fake = staged(
        {"Held": OCT.format(day=5), "New": OCT.format(day=6)},
        ("2026-10", "Held"), ("2026-Q4", "Held", "New"),
    )
    acted, shown = _approved()
    assert shown["month playlists"] == ["2026-10 (2)"]
    assert shown["memberships to add"] == 1
    assert _live(cfg, october) == [_rows(cfg)["Held"], _rows(cfg)["New"]]


def test_the_record_carries_both_commits_under_the_favourites_key(staged):
    cfg, _folder_id, _quarters, _fake = staged(
        {"One": OCT.format(day=1), "Two": NOV}, ("2026-Q4", "One", "Two")
    )
    acted, _shown = _approved()
    (record,) = [r for r in session.records(cfg) if r.workflow == split.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert [(c.tree, c.created, c.updated) for c in record.change.trees] == [
        (placement.RECORD_KEY, 2, 1)
    ]
    assert record.session_id in _note(acted, split_cli.SPLIT)


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(staged):
    cfg, _folder_id, _quarters, fake = staged({"One": NOV}, ("2026-Q4", "One"))
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


def test_a_quarter_that_changed_after_the_approval_is_refused_and_nothing_is_written(staged):
    cfg, folder_id, (q4,), _fake = staged({"One": NOV, "Late": OCT.format(day=9)}, ("2026-Q4", "One"))
    approved = split_cli.planned(cfg, source=SOURCE)
    _put(cfg, q4, _rows(cfg)["Late"])
    assert _written_refused(cfg, approved).cause.reason == "decision-stale"
    assert not _removed(cfg, q4)
    assert set(_favorites(cfg, folder_id)) == {SOURCE, "2026-Q4"}


def test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes(
    staged, monkeypatch
):
    cfg, folder_id, (q4,), _fake = staged(
        {"One": OCT.format(day=1), "Two": NOV}, ("2026-Q4", "One", "Two")
    )
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


def test_the_writer_refuses_a_membership_the_plan_did_not_name(staged, monkeypatch):
    cfg, folder_id, (q4,), _fake = staged({"One": NOV, "Stray": OCT.format(day=3)}, ("2026-Q4", "One"))
    stray = _rows(cfg)["Stray"]
    refused = _rewritten(monkeypatch, cfg, lambda ids: [*ids, stray])
    assert refused.cause.reason == "whitelist-violation"
    assert f"puts row {stray!r}" in refused.cause.message
    assert set(_favorites(cfg, folder_id)) == {SOURCE, "2026-Q4"}
    assert not _removed(cfg, q4)


def test_a_quarter_whose_member_its_month_lacks_is_not_retired(staged, monkeypatch):
    cfg, _folder_id, (q4,), _fake = staged(
        {"One": NOV, "Two": OCT.format(day=8)}, ("2026-Q4", "One", "Two")
    )
    two = _rows(cfg)["Two"]
    refused = _rewritten(monkeypatch, cfg, lambda ids: [one for one in ids if one != two])
    assert refused.cause.reason == "session-committed-unverified"
    assert "no quarter was retired" in refused.cause.message
    assert not _removed(cfg, q4)


def test_the_retirement_is_confined_to_the_quarters(given, monkeypatch):
    cfg, folder_id, source_id, _fake = given({"One": NOV}, {})
    q4 = _quarter(cfg, folder_id, "2026-Q4", "One")
    approved = split_cli.planned(cfg, source=SOURCE)
    real = rb_writer.remove_playlist_node
    def reaches_further(db, row):
        marked = real(db, row)
        real(db, db.get_playlist(ID=source_id))
        return marked
    monkeypatch.setattr(rb_writer, "remove_playlist_node", reaches_further)
    assert _written_refused(cfg, approved).cause.reason == "whitelist-violation"
    assert not _removed(cfg, q4) and not _removed(cfg, source_id)


def test_no_content_row_tempo_or_grid_is_written(staged):
    """The standing constraint, read from SQL across the whole split."""
    cfg, _folder_id, _quarters, _fake = staged(
        {"One": NOV, "Two": OCT.format(day=4)}, ("2026-Q4", "One", "Two")
    )
    before = _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")
    acted, _shown = _approved()
    assert _query(cfg, "SELECT * FROM djmdContent ORDER BY ID") == before
    assert analysis_store.watch_roots(cfg)


def _tables(playlists: dict, memberships: dict, content: dict | None = None) -> rb_writer.NodeTables:
    return rb_writer.NodeTables(
        content=content or {"1": "a", "2": "b"}, playlists=playlists, memberships=memberships,
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


_SHAPES = {
    "unplanned row": lambda w: w["memberships"].update(s3=("s3", "m", "2", 2, 0)),
    "wrong playlist": lambda w: w["memberships"].update(s3=("s3", "q", "1", 2, 0)),
    "removed addition": lambda w: w["memberships"].update(s2=("s2", "m", "1", 1, 1)),
    "changed membership": lambda w: w["memberships"].update(s1=("s1", "q", "1", 1, 1)),
    "gone membership": lambda w: w["memberships"].pop("s1"),
    "unplanned playlist": lambda w: w["playlists"].update(x=("x", "2026-11", "f", 0, 3, 0, "t1")),
    "wrong name": lambda w: w["playlists"].update(m=("m", "2026-1", "f", 0, 2, 0, "t1")),
    "wrong parent": lambda w: w["playlists"].update(m=("m", "2026-10", "root", 0, 2, 0, "t1")),
    "not made": lambda w: w["created"].update(n=("2026-11", "f")),
    "quarter renamed": lambda w: w["playlists"].update(q=("q", "2026-Q3", "f", 0, 1, 0, "t0")),
    "content": lambda w: w.update(content={"1": "a", "2": "changed"}),
}


@pytest.mark.parametrize(
    ("shape", "expected"),
    [
        ("unplanned row", "puts row '2'"), ("wrong playlist", "puts row '1' in playlist 'q'"),
        ("removed addition", "puts row '1'"), ("changed membership", "row 's1' changed"),
        ("gone membership", "row 's1' disappeared"),
        ("unplanned playlist", "unplanned djmdPlaylist row 'x'"),
        ("wrong name", "not a live plain playlist named '2026-10'"),
        ("wrong parent", "not a live plain playlist named '2026-10' under 'f'"),
        ("not made", "was not made"), ("quarter renamed", "row 'q' changed ['Name']"),
        ("content", "djmdContent row changed"),
    ],
)
def test_an_addition_the_plan_did_not_name_is_a_violation(shape, expected):
    world = {
        "playlists": {"f": FOLDER, "q": QUARTER, "m": MONTH},
        "memberships": {"s1": IN_QUARTER, "s2": ("s2", "m", "1", 1, 0)},
        "content": None, "created": {"m": ("2026-10", "f")},
    }
    _SHAPES[shape](world)
    after = _tables(world["playlists"], world["memberships"], world["content"])
    violations = split.addition_violations(
        _before(), after, planned={"m": ["1"]}, created=world["created"]
    )
    assert any(expected in one for one in violations), violations


def test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires(
    given,
):
    """The backfill's rule: a heart the author took back is never put back."""
    cfg, folder_id, source_id, _fake = given({"Kept": NOV, "Dropped": NOV}, {})
    rows = _rows(cfg)
    _put(cfg, source_id, rows["Kept"])
    _put(cfg, source_id, rows["Dropped"])
    _take_out(cfg, source_id, rows["Dropped"])
    q4 = _quarter(cfg, folder_id, "2026-Q4", "Kept", "Dropped")
    acted, shown = _approved()
    assert shown["month playlists"] == ["2026-11 (1), made"]
    assert shown["taken back"] == [
        f"Probe - Dropped (row {rows['Dropped']}, from 2026-Q4), removed from {SOURCE!r} in rekordbox"
    ]
    assert _favorites(cfg, folder_id)["2026-11"] == ["Kept"]
    assert _removed(cfg, q4)
    assert "Dropped (from 2026-Q4)" in _note(acted, split_cli.TAKEN_BACK)


def test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention(
    given, monkeypatch
):
    # The oldest job froze no date, the next dated it in October, the last in November.
    hearts_swept(given.cfg, {"Often": UNKNOWN}, run_id="")
    hearts_swept(given.cfg, {"Often": OCT.format(day=7)}, run_id="")
    cfg, folder_id, _source_id, _fake = given(
        {"Often": NOV}, {}, hearted={"batch": "2026-11-04-favorites"}
    )
    _quarter(cfg, folder_id, "2026-Q4", "Often")
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


def test_a_job_row_owned_when_its_job_ran_still_dates_the_member(given):
    """The quarters hold owned hearts above all, so every match state is read."""
    cfg, folder_id, _source_id = given.home
    _seed(cfg, given.silence, "Owned", batch="2026-09-01-favorites")
    job = hearts_swept(cfg, {"Owned": OCT.format(day=11)}, run_id="")
    _quarter(cfg, folder_id, "2026-Q4", "Owned")
    fake = given.account({})
    acted, _shown = _approved()
    with jobs.open_store() as store:
        states = {report.get("state") for report in missing_cli.job_reports(store, job)}
    assert states == {"owned"}, "the heart was owned when its job ran"
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id)["2026-10"] == ["Owned"]


def test_a_heart_taken_back_and_hearted_again_is_not_taken_back(given):
    cfg, folder_id, source_id, _fake = given({"Again": NOV}, {})
    again = _rows(cfg)["Again"]
    _put(cfg, source_id, again)
    _take_out(cfg, source_id, again)
    _put(cfg, source_id, again)
    _quarter(cfg, folder_id, "2026-Q4", "Again")
    acted, shown = _approved()
    assert "taken back" not in shown
    assert _favorites(cfg, folder_id)["2026-11"] == ["Again"]


def test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month(staged):
    """R-758: a membership rekordbox marked removed is not a member."""
    cfg, folder_id, (q4,), _fake = staged(
        {"Stays": NOV, "Went": OCT.format(day=12)}, ("2026-Q4", "Stays", "Went")
    )
    _take_out(cfg, q4, _rows(cfg)["Went"])
    acted, shown = _approved()
    assert shown["quarters to retire"] == ["2026-Q4 (1)"]
    assert _favorites(cfg, folder_id) == {SOURCE: [], "2026-11": ["Stays"]}
