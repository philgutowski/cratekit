"""U144: every downloaded set on the account gets its INSPIRATION playlist, by matching.

Driven through the real dispatcher against the disposable database the native
landing suite builds, with the account and the catalogue faked the way the
organize suite fakes them: a strict account holding a ``Downloaded Sets
<year>`` folder of ``DOWNLOADED`` set playlists, and a catalogue that lists
each set's tracks from memory. A library track is a tagged file under the
music folder with the collection row rekordbox gave it, so the match engine
and the collection both answer from what is on disk and in SQL.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.cli import registry
from cratekit.core import active_taxonomy, config, preflight, rb_writer, session, tags
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import set_playlist
from cratekit.label import catalogue
from cratekit.modules.outbound import folders, sets
from cratekit.organize import cli as organize_cli
from cratekit.organize import inspiration, rekordbox
from cratekit.sync import playlists as sync_playlists
from tests import adopt_fixtures, cutover_fixtures, outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, catalogue_factory
from tests.test_config import valid_data
from tests.test_intake_land_native import DECLARED, _cut_over_intake, _seed_binding_rows
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_intake_missing import Track
from tests.test_outbound_workers import bind as bind_account
from tests.test_rb_writer_db import RECORDED_APP_VERSION

GATE = organize_cli.REKORDBOX_GATE
VERB = ["organize", "--only", rekordbox.INSPIRATION]
FOLDER = DECLARED.inspiration.display
SETS_FOLDER = "Downloaded Sets 2026"
#: The brief's set, whose INSPIRATION name is its account name without the prefix.
FEMME = "5_28_26 Probe DJ Femme House Mix 10-18"
GOATS = "6_16_26 Other DJ Radio Mix 4-26"


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    collection.reset_cache()
    yield
    intake_cli.reset_cache()


@pytest.fixture
def machine(library, monkeypatch):
    """The native landing suite's machine on the full profile, acknowledged and cut over."""
    resolved = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, ())
    _seed_binding_rows(resolved)
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    _cut_over_intake(resolved)
    return resolved


class Account:
    """The faked account and catalogue, and a set folder to put sets in."""

    def __init__(self, monkeypatch) -> None:
        self.held = outbound_fakes.StrictAccount()
        self.found = FakeCatalogue()
        bind_account(monkeypatch, self.held)
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.found))
        self.folder = self.add_folder(SETS_FOLDER)

    def add_folder(self, name: str) -> str:
        folder_id = f"folder-{len(self.held.folder_names) + 1}"
        self.held.folder_names[folder_id] = name
        return folder_id

    def add_set(self, name: str, titles, *, folder: str | None = None, declared=None) -> str:
        playlist_id = f"acc-{len(self.held.titles) + 1}"
        self.held.titles[playlist_id] = name
        self.held.placed[playlist_id] = folder or self.folder
        tracks = [
            Track(f"{playlist_id}-{position}", "Probe", title)
            for position, title in enumerate(titles, start=1)
        ]
        self.found.playlists[playlist_id] = FakePagedPlaylist(tracks, declared=declared)
        return playlist_id


@pytest.fixture
def account(machine, monkeypatch):
    return Account(monkeypatch)


def _owned(cfg: config.Config, silence: Path, title: str) -> str:
    """A library file tagged ``Probe - title`` and its collection row; answers the row."""
    path = Path(cfg.library.root) / cfg.library.music_dir / "Owned" / f"{title}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    content_id = f"row-{title.replace(' ', '-').lower()}"
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute(
        "INSERT INTO djmdContent (ID, Title, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, ?, 0, '2026-01-01', '2026-01-01')",
        (content_id, title, str(path)),
    )
    conn.commit()
    conn.close()
    return content_id


def _query(cfg: config.Config, sql: str, *params) -> list[tuple]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _inspiration_id(cfg: config.Config) -> str:
    ((folder_id,),) = _query(
        cfg,
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
        "AND COALESCE(rb_local_deleted, 0) = 0",
        FOLDER,
    )
    return str(folder_id)


def _playlists_under(cfg: config.Config, folder_id: str) -> dict[str, str]:
    return {
        str(name): str(playlist_id)
        for playlist_id, name in _query(
            cfg,
            "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND Attribute = 0 "
            "AND COALESCE(rb_local_deleted, 0) = 0",
            folder_id,
        )
    }


def _members(cfg: config.Config, playlist_id: str) -> list[str]:
    return [
        str(row[0])
        for row in _query(
            cfg,
            "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
            "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY TrackNo",
            playlist_id,
        )
    ]


def _report() -> dict:
    collection.reset_cache()
    code, envelope = drive([*VERB, "--report"])
    assert code == int(ExitCode.OK), envelope
    return envelope


def _step(envelope: dict) -> dict:
    (step,) = [
        one
        for one in envelope["data"]["summary"]["areas"][rekordbox.AREA]["steps"]
        if one["step"] == rekordbox.INSPIRATION
    ]
    return step


def _by_set(step: dict) -> dict[str, dict]:
    return {item["set"]: item for item in step["plan"]}


def _approved(option: str = "approve") -> tuple[int, dict, dict]:
    """The rekordbox area's gate answered by its two acts, then the run that writes."""
    collection.reset_cache()
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == GATE
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, GATE, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    collection.reset_cache()
    code, done = drive(["--run", run_id, *VERB])
    return code, done, refused


#: Fifteen the library holds, and three it does not whose titles share no word
#: with any held, so the engine answers missing rather than asking a question.
TITLES = (
    *(f"Cut {number:02d}" for number in range(1, 16)),
    "Absent Harbor",
    "Absent Lantern",
    "Absent Meadow",
)


# ---------------------------------------------------------------------------
# The declaration
# ---------------------------------------------------------------------------


def test_the_step_is_a_kind_of_the_rekordbox_area_that_only_may_name():
    assert rekordbox.INSPIRATION in rekordbox.STEPS
    assert rekordbox.INSPIRATION in organize_cli.KINDS
    entry = registry.entry("organize")
    assert "inspiration" in entry.taxonomy_terms and "db_tree" in entry.writes


def test_the_prefix_is_the_one_the_mark_and_the_sweep_spell():
    assert inspiration.PREFIX == folders.MARK_PREFIX == sync_playlists.SWEPT_PREFIX


@pytest.mark.parametrize(
    ("name", "is_sets"),
    [
        ("Downloaded Sets 2026", True),
        ("Downloaded Sets 2025", True),
        ("Downloaded Sets", False),
        ("Downloaded Sets 26", False),
        ("downloaded sets 2026", False),
        ("Downloaded Sets 2026 old", False),
        ("2026", False),
    ],
)
def test_only_a_year_of_downloaded_sets_is_a_sets_folder(name, is_sets):
    assert inspiration.sets_folder(name) is is_sets
    assert inspiration.sets_folder(sets.folder_name("2026"))


# ---------------------------------------------------------------------------
# The brief's scenarios
# ---------------------------------------------------------------------------


def test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three(
    machine, account, silence
):
    rows = {title: _owned(machine, silence, title) for title in TITLES[:15]}
    account.add_set(f"DOWNLOADED {FEMME}", TITLES[3:] + TITLES[:3])

    step = _step(_report())

    assert step["state"] == "planned"
    planned = _by_set(step)[FEMME]
    assert planned["action"] == inspiration.CREATE and planned["tracks"] == 15
    assert planned["misses"] == [
        f"{position}. Probe - {title}: {set_playlist.NOT_HELD}"
        for position, title in zip((13, 14, 15), TITLES[15:], strict=True)
    ]
    assert step["counts"]["tracks matched"] == 15 and step["counts"]["tracks missed"] == 3

    code, done, refused = _approved()

    assert code == int(ExitCode.OK), done
    assert refused["cause"]["detail"]["shown"]["deletes"].startswith("nothing")
    under = _playlists_under(machine, _inspiration_id(machine))
    assert set(under) == {FEMME}
    # IN THE SET'S ORDER, as the account plays it, and only the matched rows.
    assert _members(machine, under[FEMME]) == [rows[title] for title in TITLES[3:15] + TITLES[:3]]
    applied = _step(done)["applied"]
    assert applied["playlists created"] == 1 and applied["memberships added"] == 15
    assert applied["read back"] == {FEMME: 15}
    # The account is read and never written.
    assert account.held.created == [] and account.held.moves == []
    assert account.held.renamed == [] and account.held.added == []
    (record,) = [r for r in session.records(machine) if r.workflow == inspiration.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert {c.tree: c.created for c in record.change.trees} == {DECLARED.inspiration.id: 15}
    assert record.detail[inspiration.RECORD_KEY] == [
        {"id": under[FEMME], "name": FEMME, "added": 15}
    ]


def test_a_near_match_is_a_question_named_as_a_miss_and_never_written(
    machine, account, silence
):
    _owned(machine, silence, "Cut 15")
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 16"))

    planned = _by_set(_step(_report()))[FEMME]

    assert planned["tracks"] == 1
    assert planned["misses"] == [f"2. Probe - Cut 16: {set_playlist.UNANSWERED}"]


def test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    folder_id = cutover_fixtures.add_folder(machine, FOLDER)
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), cfg=machine)
    try:
        handle.create_playlist(GOATS, parent=handle.get_playlist(ID=folder_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    done_id = account.add_set(f"DOWNLOADED {GOATS}", ("Cut 01",))

    step = _step(_report())

    assert step["state"] == "nothing"
    assert _by_set(step)[GOATS]["action"] == inspiration.SKIP
    assert done_id not in account.found.playlists_asked_for


def test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    account.add_set(f"DOWNLOADED {GOATS}", ("Cut 07", "Cut 08"))

    step = _step(_report())
    empty = _by_set(step)[GOATS]
    assert empty["action"] == inspiration.EMPTY and empty["tracks"] == 0
    assert len(empty["misses"]) == 2 and "nothing is written" in empty["reason"]

    code, done, _refused = _approved()

    assert code == int(ExitCode.OK), done
    assert set(_playlists_under(machine, _inspiration_id(machine))) == {FEMME}


def test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing(
    machine, account
):
    account.add_set(f"DOWNLOADED {GOATS}", ("Cut 07",))

    step = _step(_report())

    assert step["state"] == "nothing" and step["counts"]["no match"] == 1
    assert _query(machine, "SELECT ID FROM djmdPlaylist WHERE Name = ?", GOATS) == []


def test_the_name_written_is_the_account_name_without_its_prefix(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))

    code, done, _refused = _approved()

    assert code == int(ExitCode.OK), done
    assert set(_playlists_under(machine, _inspiration_id(machine))) == {FEMME}
    assert _query(machine, "SELECT ID FROM djmdPlaylist WHERE Name = ?", f"DOWNLOADED {FEMME}") == []


def test_a_second_run_plans_nothing(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 02"))
    code, done, _refused = _approved()
    assert code == int(ExitCode.OK), done
    read = list(account.found.playlists_asked_for)

    step = _step(_report())

    assert step["state"] == "nothing"
    assert {item["action"] for item in step["plan"]} == {inspiration.SKIP}
    assert "digest" in step and step["counts"]["to create"] == 0
    # The set is not read again: a skipped set's tracks are never listed.
    assert account.found.playlists_asked_for == read


def test_the_writer_refuses_a_membership_the_plan_did_not_name(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 02"))
    declared = active_taxonomy.load(machine)
    approved = _plan(machine, declared, account)
    assert [len(row.members) for row in approved.creates] == [1]
    # A track the plan named as a miss now matches a row nobody was shown.
    unshown = _owned(machine, silence, "Cut 02")

    with pytest.raises(CratekitError) as refused:
        inspiration.apply(machine, declared, approved)

    assert refused.value.cause.reason == "decision-stale"
    assert refused.value.cause.detail["unnamed"] == [unshown]
    assert _query(machine, "SELECT ID FROM djmdPlaylist WHERE Name = ?", FEMME) == []
    assert not [r for r in session.records(machine) if r.workflow == inspiration.WORKFLOW]


def test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    # THE FOLDER IS THERE AT THE PLAN, so its id is not what moves: only the
    # playlist made since, which the write must skip rather than add to.
    folder_id = cutover_fixtures.add_folder(machine, FOLDER)
    declared = active_taxonomy.load(machine)
    approved = _plan(machine, declared, account)
    assert approved.folder_id == folder_id and len(approved.creates) == 1
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), cfg=machine)
    try:
        handle.create_playlist(FEMME, parent=handle.get_playlist(ID=folder_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    with pytest.raises(CratekitError) as refused:
        inspiration.apply(machine, declared, approved)

    assert refused.value.cause.reason == "decision-stale"
    assert _members(machine, _playlists_under(machine, folder_id)[FEMME]) == []


def test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused():
    made = inspiration.Wrote("A set", "p1", True, ("r1", "r2"), 2, read_back=("r1", "r2", "r9"))
    with pytest.raises(CratekitError) as refused:
        inspiration.assert_read_back([made])
    assert refused.value.cause.reason == "session-committed-unverified"
    assert refused.value.cause.detail["unnamed"] == ["r9"]
    found = inspiration.Wrote("A set", "p1", False, ("r1",), 0, read_back=("r0", "r1"))
    inspiration.assert_read_back([found])
    short = inspiration.Wrote("A set", "p1", False, ("r1", "r2"), 1, read_back=("r1",))
    with pytest.raises(CratekitError):
        inspiration.assert_read_back([short])


def _plan(cfg: config.Config, declared, account: Account) -> inspiration.ParityPlan:
    @contextmanager
    def reading():
        handle = rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
        try:
            yield handle
        finally:
            rb_writer.close_db(handle)

    return inspiration.plan(
        cfg, declared, remote=account.held, found=account.found, reading=reading
    )


def test_a_convergence_latch_refuses_the_write_before_anything_is_written(
    machine, account, silence, monkeypatch
):
    from cratekit.core import convergence

    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    declared = active_taxonomy.load(machine)
    approved = _plan(machine, declared, account)
    asked: list[str] = []

    def latched(_cfg, _db, tree_id, _registry, **_kwargs):
        from cratekit.core.cause import refuse

        asked.append(tree_id)
        raise refuse("tree-unconverged", "the tree is marked unconverged")

    monkeypatch.setattr(convergence, "assert_tree_writable", latched)

    with pytest.raises(CratekitError) as refused:
        inspiration.apply(machine, declared, approved)

    assert refused.value.cause.reason == "tree-unconverged"
    assert asked == [DECLARED.inspiration.id]
    assert _query(machine, "SELECT ID FROM djmdPlaylist WHERE Name = ?", FEMME) == []
    assert not [r for r in session.records(machine) if r.workflow == inspiration.WORKFLOW]


def test_a_slash_in_the_account_name_is_written_as_a_dash(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set("DOWNLOADED 5_28_26 A b2b B / Night 10-18", ("Cut 01",))

    code, done, _refused = _approved()

    assert code == int(ExitCode.OK), done
    assert set(_playlists_under(machine, _inspiration_id(machine))) == {
        "5_28_26 A b2b B - Night 10-18"
    }


# ---------------------------------------------------------------------------
# What is not a set, and what cannot be read
# ---------------------------------------------------------------------------


def test_only_prefixed_playlists_in_a_downloaded_sets_folder_are_sets(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    other = account.add_folder("2026")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",), folder=other)
    retitled = account.add_set(GOATS, ("Cut 01",))
    later = account.add_folder("Downloaded Sets 2025")
    account.add_set("DOWNLOADED 1_02_25 Old DJ Old Mix 12-24", ("Cut 01",), folder=later)

    step = _step(_report())

    shown = _by_set(step)
    assert set(shown) == {"1_02_25 Old DJ Old Mix 12-24", GOATS}
    assert shown["1_02_25 Old DJ Old Mix 12-24"]["account folder"] == "Downloaded Sets 2025"
    # AN UNPREFIXED PLAYLIST IN A SETS FOLDER IS NAMED, never silently passed over.
    assert shown[GOATS]["action"] == inspiration.UNPREFIXED
    assert "prefix" in shown[GOATS]["reason"]
    assert retitled not in account.found.playlists_asked_for
    assert step["counts"]["not taken"] == 1


def test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now(
    machine, account, silence
):
    from cratekit.modules.outbound import ledger

    _owned(machine, silence, "Cut 01")
    renamed = account.add_folder("Sets of 2024")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",), folder=renamed)
    unrecorded = account.add_folder("Other sets")
    account.add_set(f"DOWNLOADED {GOATS}", ("Cut 01",), folder=unrecorded)
    ledger.reserve_set_folder(machine, "Downloaded Sets 2024", lambda: renamed)

    step = _step(_report())

    assert set(_by_set(step)) == {FEMME}
    assert _by_set(step)[FEMME]["account folder"] == "Sets of 2024"


def test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan(
    machine, account, silence, monkeypatch
):
    from cratekit.core.cause import refuse

    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    broken = account.add_folder("Downloaded Sets 2025")
    real = account.held.folder_playlists

    def listing(folder_id):
        if folder_id == broken:
            raise refuse("credential-missing", "the folder could not be listed")
        return real(folder_id)

    monkeypatch.setattr(account.held, "folder_playlists", listing)

    envelope = _report()
    step = _step(envelope)

    assert step["state"] == "planned" and step["counts"]["folders unread"] == 1
    (unread,) = [item for item in step["plan"] if item["action"] == inspiration.FOLDER_UNREAD]
    assert unread["account folder"] == "Downloaded Sets 2025"
    assert any("Downloaded Sets 2025" in w["message"] for w in envelope["warnings"])


def test_two_account_sets_of_one_name_are_both_left(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    later = account.add_folder("Downloaded Sets 2025")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",), folder=later)

    step = _step(_report())

    assert step["state"] == "nothing"
    assert [item["action"] for item in step["plan"]] == [inspiration.TWICE] * 2
    assert account.found.playlists_asked_for == []


def test_a_set_the_provider_cannot_list_is_shown_unread_and_the_rest_still_plan(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",))
    unlisted = account.add_set(f"DOWNLOADED {GOATS}", ("Cut 01",))
    del account.found.playlists[unlisted]

    envelope = _report()
    step = _step(envelope)

    assert step["state"] == "planned"
    assert _by_set(step)[GOATS]["action"] == inspiration.UNREAD
    assert _by_set(step)[GOATS]["reason"]
    assert any(
        w["code"] == "organize-inspiration-unread" and GOATS in w["message"]
        for w in envelope["warnings"]
    )


def test_a_short_listing_counts_what_the_provider_withheld(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01",), declared=3)

    step = _step(_report())

    assert "2 track(s)" in _by_set(step)[FEMME]["withheld"]
    assert step["counts"]["tracks missed"] == 2


def test_an_account_that_cannot_be_reached_refuses_the_step_alone(machine, monkeypatch):
    from cratekit.modules.outbound import account as account_module

    def refused(_cfg):
        from cratekit.core.cause import refuse

        raise refuse("credential-missing", "no provider session is stored")

    monkeypatch.setattr(account_module, "resolve", refused)
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(FakeCatalogue()))

    step = _step(_report())

    assert step["state"] == "refused" and step["reason"] == "credential-missing"


def test_an_intake_tree_on_the_bridge_refuses_the_step(library, monkeypatch):
    resolved = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, ())
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    Account(monkeypatch)

    step = _step(_report())

    assert step["state"] == "refused" and step["reason"] == "tree-unconverged"


def test_a_profile_without_the_export_module_lists_the_step(machine, account, monkeypatch):
    import dataclasses

    from cratekit.core import profiles

    real = profiles.resolve

    def without_export(*args, **kwargs):
        resolved = real(*args, **kwargs)
        return dataclasses.replace(
            resolved, modules=resolved.modules - {rekordbox.EXPORT_MODULE}
        )

    monkeypatch.setattr(profiles, "resolve", without_export)

    step = _step(_report())

    assert step["state"] == "listed" and "export module is off" in step["detail"]
    assert account.found.playlists_asked_for == []


# ---------------------------------------------------------------------------
# R-1295: a set is read row by row, so one track the account lists with no
# title or no artist is named and the set's other tracks still reach
# INSPIRATION
# ---------------------------------------------------------------------------


def _unread_line(position: int, artist: str, title: str, half: str, track: str) -> str:
    return (
        f"{position}. {artist} - {title}: the account lists it with no {half} "
        f"(track {track}), so it was not asked of the library"
    )


def test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written(
    machine, account, silence
):
    rows = {title: _owned(machine, silence, title) for title in ("Cut 01", "Cut 02")}
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 02", ""))

    envelope = _report()
    step = _step(envelope)

    assert step["state"] == "planned"
    planned = _by_set(step)[FEMME]
    assert planned["action"] == inspiration.CREATE and planned["tracks"] == 2
    assert planned["misses"] == [
        _unread_line(3, "Probe", "no title", "title", f"{playlist_id}-3")
    ]
    assert step["counts"]["tracks matched"] == 2 and step["counts"]["tracks missed"] == 1
    assert not [w for w in envelope["warnings"] if w["code"] == "organize-inspiration-unread"]

    code, done, _refused = _approved()

    assert code == int(ExitCode.OK), done
    under = _playlists_under(machine, _inspiration_id(machine))
    assert _members(machine, under[FEMME]) == [rows["Cut 01"], rows["Cut 02"]]
    assert _step(done)["applied"]["read back"] == {FEMME: 2}


def test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written(
    machine, account, silence
):
    rows = {title: _owned(machine, silence, title) for title in ("Cut 01", "Cut 02")}
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 03", "Cut 02"))
    account.found.playlists[playlist_id]._tracks[1].artist = {"name": ""}

    step = _step(_report())

    planned = _by_set(step)[FEMME]
    assert planned["action"] == inspiration.CREATE and planned["tracks"] == 2
    assert planned["misses"] == [
        _unread_line(2, "no artist", "Cut 03", "artist", f"{playlist_id}-2")
    ]

    code, done, _refused = _approved()

    assert code == int(ExitCode.OK), done
    under = _playlists_under(machine, _inspiration_id(machine))
    assert _members(machine, under[FEMME]) == [rows["Cut 01"], rows["Cut 02"]]


def test_an_unread_track_keeps_the_sets_positions_for_every_other_miss(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("", "Cut 01", "Absent Harbor"))

    planned = _by_set(_step(_report()))[FEMME]

    # IN THE SET'S ORDER, each at the place the account lists it.
    assert planned["misses"] == [
        _unread_line(1, "Probe", "no title", "title", f"{playlist_id}-1"),
        f"3. Probe - Absent Harbor: {set_playlist.NOT_HELD}",
    ]


def test_a_set_whose_unread_track_carries_no_provider_id_is_still_filed_unread(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", ""))
    account.found.playlists[playlist_id]._tracks[1].id = ""

    envelope = _report()
    step = _step(envelope)

    unread = _by_set(step)[FEMME]
    assert unread["action"] == inspiration.UNREAD
    assert unread["reason"].startswith("track 2 names no title")
    assert "it carries no provider id either" in unread["reason"]
    assert step["state"] == "nothing"
    assert any(
        w["code"] == "organize-inspiration-unread" and FEMME in w["message"]
        for w in envelope["warnings"]
    )


def test_a_readable_track_with_no_provider_id_is_matched_as_before(
    machine, account, silence
):
    rows = {title: _owned(machine, silence, title) for title in ("Cut 01", "Cut 02")}
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("Cut 01", "Cut 02"))
    account.found.playlists[playlist_id]._tracks[1].id = ""

    planned = _by_set(_step(_report()))[FEMME]

    assert planned["action"] == inspiration.CREATE and planned["tracks"] == 2
    assert planned["misses"] == []
    code, done, _refused = _approved()
    assert code == int(ExitCode.OK), done
    under = _playlists_under(machine, _inspiration_id(machine))
    assert _members(machine, under[FEMME]) == [rows["Cut 01"], rows["Cut 02"]]


def test_a_set_no_track_of_which_reads_is_filed_unread_naming_each(machine, account, silence):
    _owned(machine, silence, "Cut 01")
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("", ""))

    envelope = _report()
    step = _step(envelope)

    unread = _by_set(step)[FEMME]
    assert unread["action"] == inspiration.UNREAD
    assert unread["reason"] == (
        f"no track of the set could be read: {playlist_id}-1 (the account lists it "
        f"with no title), {playlist_id}-2 (the account lists it with no title)"
    )
    assert step["state"] == "nothing" and step["counts"]["unread"] == 1
    assert step["counts"]["no match"] == 0
    assert any(
        w["code"] == "organize-inspiration-unread" and FEMME in w["message"]
        for w in envelope["warnings"]
    )


def test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order(
    machine, account, silence
):
    _owned(machine, silence, "Cut 01")
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("Absent Harbor", "", "Cut 01"))

    planned = _by_set(_step(_report()))[FEMME]

    assert planned["tracks"] == 1
    assert planned["misses"] == [
        f"1. Probe - Absent Harbor: {set_playlist.NOT_HELD}",
        _unread_line(2, "Probe", "no title", "title", f"{playlist_id}-2"),
    ]


def test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld(
    machine, account, silence
):
    playlist_id = account.add_set(f"DOWNLOADED {FEMME}", ("",) * 7, declared=10)

    unread = _by_set(_step(_report()))[FEMME]

    assert inspiration.NAMED_UNREAD == 5
    assert unread["action"] == inspiration.UNREAD
    assert unread["reason"] == (
        "no track of the set could be read: "
        + ", ".join(
            f"{playlist_id}-{place} (the account lists it with no title)" for place in range(1, 6)
        )
        + ", and 2 more the same way; the provider also counts 3 track(s) on the "
        "playlist it would not list"
    )
