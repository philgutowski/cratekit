"""U120: ``crate favorites backfill`` places the hearts that landed before the landing did.

Driven through the real dispatcher on the native landing suite's library: a
hearts job queued by hand and run, its files staged and landed with no pass,
which is how the September hearts landed, so nothing placed them. Then the
verb: the plan lists exactly those, the account supplies the dates the job
never froze, the approval places them, and a second run has nothing to do.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from cratekit.core import rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import backfill, backfill_cli, placement
from cratekit.intake import cli as intake_cli
from tests.cli_drive import drive
from tests.intake.test_workers import Track, bind_hearts
from tests.test_intake_land_hearts_native import SOURCE, _favorites, _home, hearts_swept
from tests.test_intake_land_hearts_native import pinned_day as pinned_day  # noqa: PLC0414
from tests.test_intake_land_native import _members, _query, _two_acts
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import _stage as _stage_native
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

VERB = ["favorites", "backfill"]
GATE = backfill_cli.APPROVE_GATE
BATCH = "2026-09-29-favorites"
UTC = timezone.utc
Q3 = datetime(2026, 9, 29, 22, 0, tzinfo=UTC)
Q4 = datetime(2026, 11, 3, 12, 0, tzinfo=UTC)


def _stage(cfg, silence: Path, title: str) -> Path:
    """A file tagged the way the hearts job's rows read, so the match rule ties them."""
    path = Path(cfg.paths.download_staging) / f"{title}.flac"
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    return path


def _land(batch: str = BATCH) -> None:
    code, acted, _refused = _two_acts(["intake", "land", "--name", batch])
    assert code == int(ExitCode.OK), acted


def _landed_hearts(cfg, silence, titles: dict[str, str | None], *, batch: str = BATCH):
    """A hearts job run by hand, its files staged and landed with no pass."""
    job = hearts_swept(cfg, titles, run_id="")
    for title in titles:
        _stage(cfg, silence, title)
    _land(batch)
    return job


def _account(monkeypatch, dates: dict[str, datetime | None]):
    """The account's hearts, each dated or not, under the identifiers the jobs froze."""
    rows = []
    for title, when in dates.items():
        row = Track(f"tid-{title}", "Probe", title)
        if when is not None:
            row.user_date_added = when
        rows.append(row)
    return bind_hearts(monkeypatch, rows)


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


def _rows(cfg) -> dict[str, str]:
    return {str(title): str(row) for row, title in _query(cfg, "SELECT ID, Title FROM djmdContent")}


# ---------------------------------------------------------------------------
# The brief's scenario: the three September hearts, listed exactly, placed
# ---------------------------------------------------------------------------


def test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None, "Fractals": None, "Find My Way": None})
    fake = _account(monkeypatch, {"Same Girl": Q3, "Fractals": Q3, "Find My Way": Q3, "Elsewhere": Q4})
    assert _favorites(cfg, folder_id) == {SOURCE: []}, "nothing placed them as they landed"

    code, acted, refused = _acts()

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert sorted(item["title"] for item in shown["items"]) == [
        "Probe - Find My Way",
        "Probe - Fractals",
        "Probe - Same Girl",
    ]
    assert {item["quarter"] for item in shown["items"]} == {"2026-Q3"}
    assert {item["dated_by"] for item in shown["items"]} == {"account"}
    assert shown["landed hearts"] == 3 and shown["memberships to add"] == 6
    assert shown["quarter playlists to create"] == ["2026-Q3"]
    assert shown["dates asked of the account"] == 3 and shown["undated"] == 0
    assert shown["into"].startswith(f"{SOURCE!r} (row {source_id}) under 'Favorites'")
    # Once per plan, and the two acts are two plans: the gate's refusal and
    # the run that carries the answer each plan the library afresh.
    assert fake.heart_listings == 2
    assert _favorites(cfg, folder_id) == {
        SOURCE: ["Find My Way", "Fractals", "Same Girl"],
        "2026-Q3": ["Find My Way", "Fractals", "Same Girl"],
    } or sorted(_favorites(cfg, folder_id)[SOURCE]) == ["Find My Way", "Fractals", "Same Girl"]
    totals = acted["data"]["totals"]
    assert (totals["count"], totals["added"], totals["created"]) == (3, 6, 1)
    (note,) = [w for w in acted["warnings"] if w["code"] == backfill_cli.PLACED]
    assert "6 membership(s) added for 3 landed heart(s)" in note["message"]
    assert "2026-Q3 (made)" in note["message"]
    # Every item of the plan names the file by its path under the library.
    assert all(item["path"].startswith(f"Music/{BATCH}/") for item in shown["items"])


def test_a_second_run_finds_the_same_hearts_and_writes_nothing(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": Q3})
    code, _acted, _refused = _acts()
    assert code == int(ExitCode.OK)

    code, acted, refused = _acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    (note,) = [w for w in acted["warnings"] if w["code"] == backfill_cli.NOTHING_TO_PLACE]
    assert "1 landed heart(s) found and every one is already" in note["message"]
    shown = refused["cause"]["detail"]["shown"]
    assert shown["memberships to add"] == 0 and shown["quarter playlists to create"] == []
    assert _favorites(cfg, folder_id) == {SOURCE: ["Same Girl"], "2026-Q3": ["Same Girl"]}
    assert len(_members(cfg, _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-Q3'")[0][0])) == 1


def test_an_owned_heart_the_source_system_filed_is_left_alone(native_library, silence, monkeypatch):
    """The open question's conservative default: a heart the library owned, or
    one filed deeper than a batch folder, is not a heart this product landed."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    # One heart owned when the job ran, under the source system's deep folder.
    deep = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025" / "Owned.flac"
    deep.parent.mkdir(parents=True)
    shutil.copyfile(silence, deep)
    assert tags.write_tags(deep, {"title": "Owned", "artist": "Probe"})
    # One heart missing when the job ran and later put under a deep folder by hand.
    job = hearts_swept(cfg, {"Owned": None, "Hand Filed": None, "Landed": None}, run_id="")
    hand = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "Hand Filed.flac"
    shutil.copyfile(silence, hand)
    assert tags.write_tags(hand, {"title": "Hand Filed", "artist": "Probe"})
    _stage(cfg, silence, "Landed")
    _land()
    _account(monkeypatch, {"Owned": Q3, "Hand Filed": Q3, "Landed": Q4})
    del job

    code, acted, refused = _acts()

    assert code == int(ExitCode.OK), acted
    assert [item["title"] for item in refused["cause"]["detail"]["shown"]["items"]] == ["Probe - Landed"]
    assert _favorites(cfg, folder_id) == {SOURCE: ["Landed"], "2026-Q4": ["Landed"]}


def test_a_date_the_job_froze_wins_and_the_account_is_not_asked(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _landed_hearts(cfg, silence, {"Dated": "2026-11-03T12:00:00+00:00"})
    fake = _account(monkeypatch, {"Dated": Q3})

    code, _acted, refused = _acts()

    assert code == int(ExitCode.OK)
    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["quarter"], item["dated_by"]) == ("2026-Q4", "job")
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id) == {SOURCE: ["Dated"], "2026-Q4": ["Dated"]}


def test_a_heart_the_account_dates_nowhere_goes_to_undated_and_is_said(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _landed_hearts(cfg, silence, {"Gone": None, "Kept": None})
    # The account no longer carries the first and dates the second nowhere.
    _account(monkeypatch, {"Kept": None})

    code, acted, refused = _acts()

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["undated"] == 2 and shown["dates asked of the account"] == 0
    assert {item["quarter"] for item in shown["items"]} == {"Undated"}
    assert {item["dated_by"] for item in shown["items"]} == {"none"}
    (note,) = [w for w in acted["warnings"] if w["code"] == backfill_cli.UNDATED]
    assert "2 heart(s) carry no date" in note["message"] and "nothing moves a heart" in note["message"]
    found = _favorites(cfg, folder_id)
    assert sorted(found[SOURCE]) == ["Gone", "Kept"] and sorted(found["Undated"]) == ["Gone", "Kept"]


def test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    hearts_swept(cfg, {"Twice": None}, run_id="")
    _landed_hearts(cfg, silence, {"Twice": "2026-09-29T22:00:00+00:00"}, batch="2026-09-30-favorites")
    fake = _account(monkeypatch, {"Twice": Q4})

    code, _acted, refused = _acts()

    assert code == int(ExitCode.OK)
    (item,) = refused["cause"]["detail"]["shown"]["items"]
    assert (item["quarter"], item["dated_by"]) == ("2026-Q3", "job")
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id) == {SOURCE: ["Twice"], "2026-Q3": ["Twice"]}


# ---------------------------------------------------------------------------
# The record, the refusals, the order
# ---------------------------------------------------------------------------


def test_the_record_carries_the_placement_under_the_favourites_key(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": Q3})

    code, acted, _refused = _acts()

    assert code == int(ExitCode.OK), acted
    (record,) = [r for r in session.records(cfg) if r.workflow == backfill.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert record.detail[placement.PLACED_KEY]["added_source"] == 1
    assert [(c.tree, c.created) for c in record.change.trees] == [(placement.RECORD_KEY, 2)]
    (note,) = [w for w in acted["warnings"] if w["code"] == backfill_cli.PLACED]
    assert record.session_id in note["message"]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": Q3})
    session.ack_path(cfg).unlink()

    code, refused = drive(VERB)

    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_with_no_source_playlist_the_verb_refuses_by_name_before_the_gate(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    _landed_hearts(cfg, silence, {"Same Girl": None})
    fake = _account(monkeypatch, {"Same Girl": Q3})

    code, refused = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == placement.SOURCE_MISSING
    assert fake.heart_listings == 0, "the home is resolved before the library is walked"


def test_an_unreadable_account_refuses_only_when_a_heart_needs_a_date(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    _home(cfg)
    _landed_hearts(cfg, silence, {"Dated": "2026-11-03T12:00:00+00:00"})

    class Unreadable:
        def favourite_tracks(self):
            raise RuntimeError("the favourites listing failed")

    from cratekit.label import catalogue

    monkeypatch.setattr(catalogue, "resolve", lambda _cfg: Unreadable())
    code, acted, _refused = _acts()
    assert code == int(ExitCode.OK), acted

    hearts_swept(cfg, {"Undated Too": None}, run_id="")
    _stage(cfg, silence, "Undated Too")
    _land("2026-09-30-favorites")
    code, refused = drive(VERB)

    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "label-playlist-unreadable"


def test_a_home_that_moved_between_the_two_acts_is_refused_by_the_write(
    native_library, silence, monkeypatch
):
    cfg, _root_id = native_library
    _folder_id, source_id = _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": Q3})
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, GATE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    # Somebody drags the heart into All Favorites by hand before the write.
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), _rows(cfg)["Same Girl"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, acted = drive(["--run", run_id, *VERB])

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-Q3'") == []


def test_with_nothing_landed_the_gate_is_still_asked_and_nothing_is_written(
    native_library, monkeypatch
):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    fake = _account(monkeypatch, {})

    code, acted, refused = _acts()

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert refused["cause"]["detail"]["shown"]["landed hearts"] == 0
    assert fake.heart_listings == 0
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_no_content_row_tempo_or_rating_is_written(native_library, silence, monkeypatch):
    cfg, _root_id = native_library
    _home(cfg)
    _landed_hearts(cfg, silence, {"Same Girl": None})
    _account(monkeypatch, {"Same Girl": Q3})
    before = _query(cfg, "SELECT COUNT(*) FROM djmdContent")

    code, _acted, _refused = _acts()

    assert code == int(ExitCode.OK)
    assert _query(cfg, "SELECT COUNT(*) FROM djmdContent") == before
    ((bpm, rating, analysis),) = _query(
        cfg, "SELECT BPM, Rating, AnalysisDataPath FROM djmdContent WHERE Title = 'Same Girl'"
    )
    assert bpm in (None, 0) and rating in (None, 0) and not analysis


def test_the_landed_path_rule_is_the_landings_own(native_library, silence):
    """A file the native landing just put down reads as landed, by the rule the backfill uses."""
    from cratekit.intake import landing

    cfg, _root_id = native_library
    _stage_native(cfg, silence, "One.flac")
    _land()
    landed = Path(cfg.library.root) / cfg.library.music_dir / BATCH / "One.flac"
    assert landed.is_file() and landing.is_landed_path(cfg, landed)
    assert intake_cli.FAVORITES_SOURCE_ID == "favorites"
