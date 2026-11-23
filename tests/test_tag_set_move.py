"""U339: after ``tag set``, ``adopt move`` files the track under its new genre's folder.

A filed track's genre is moved, through the verb, to a genre another top level
folder files by; then ``adopt move`` takes it out of its old genre folder's
energy band and into the new folder's, the one move it makes across folders.
A track a person put in a second genre folder by hand is left there, and a
genre moved back asks nothing. The library is ``tests/test_adopt_move.py``'s.
D1 applies.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import collection, genre_moves
from cratekit.adopt import move as adopt_move
from cratekit.core import session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import genre_set_cli
from cratekit.write.routing_pass import destination
from tests.cli_drive import approve_and_queue, drive
from tests.test_adopt_move import DECLARED, HIGH, LOW, _live, _removed, seed_library
from tests.test_adopt_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_adopt_workers import _reader_cache as _reader_cache  # noqa: PLC0414
from tests.test_adopt_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_adopt_workers import _resume
from tests.test_adopt_workers import library as library  # noqa: PLC0414
from tests.test_adopt_workers import machine as machine  # noqa: PLC0414
from tests.test_adopt_workers import silence as silence  # noqa: PLC0414

#: The bucket the track is filed in, and the one its new genre names.
OLD_BUCKET, OLD_GENRE = "house_funky_disco", "Funky House"
NEW_BUCKET, NEW_GENRE = "deep_house", "Deep House"


def _place(bucket: str, band: str) -> tuple[str, str]:
    return destination(DECLARED, bucket, band)


@pytest.fixture
def filed(machine, silence):
    """``mover`` and ``stays`` in the old folder's high band, ``second`` in the new
    folder's low band and, put there by hand, in the old folder's high band too."""
    tracks = [
        ("mover", OLD_GENRE, "8"),
        ("stays", OLD_GENRE, "8"),
        ("second", NEW_GENRE, "2"),
    ]
    places = [
        (*_place(OLD_BUCKET, HIGH), "mover"),
        (*_place(OLD_BUCKET, HIGH), "stays"),
        (*_place(NEW_BUCKET, LOW), "second"),
        (*_place(OLD_BUCKET, HIGH), "second"),
    ]
    seed_library(machine, silence, tracks, places, on=date(2026, 10, 1))
    music = Path(machine.library.root) / "Music"
    for stray in ("one.flac", "two.flac"):
        (music / stray).unlink(missing_ok=True)
    for content_id, genre, _energy in tracks:
        assert tags.write_tags(music / f"{content_id}.flac", {"genre": genre})
    session.record_acknowledgment(machine, terminal=lambda: True)
    collection.reset_cache()
    return machine


def _held(cfg, content_id: str) -> set[tuple[str, str]]:
    collection.reset_cache()
    return set(_live(cfg).get(content_id, ()))


def _tag_set(*argv: str) -> dict:
    verb = ["tag", "set", NEW_GENRE, *argv]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    return acted


def _shown() -> dict:
    code, refused = drive(["adopt", "move"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused["cause"]["detail"]["shown"]


def _move() -> dict:
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    collection.reset_cache()
    return resumed


def test_the_moved_track_leaves_its_old_genre_folder_for_the_new_ones_band(filed):
    old, new = _place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)
    assert _held(filed, "mover") == {old}
    acted = _tag_set("--row", "mover")
    assert "crate adopt move" in acted["warnings"][-1]["message"]
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET})}

    shown = _shown()
    (move,) = shown["items"]
    assert (move["content_id"], move["bucket"], move["target_bucket"]) == (
        "mover", OLD_BUCKET, NEW_BUCKET
    )
    assert (move["target"], move["add"], move["remove"]) == (HIGH, HIGH, [HIGH])
    assert move["decided_by"] == adopt_move.DECIDED_BY_GENRE

    _move()

    assert _held(filed, "mover") == {new}
    assert old in set(_removed(filed).get("mover", ()))
    # THE ENTRY IS SPENT, and the others stay where they were.
    assert dict(genre_moves.read(filed)) == {}
    assert _held(filed, "stays") == {old}
    assert _held(filed, "second") == {old, _place(NEW_BUCKET, LOW)}


def test_rows_never_filed_are_filed_by_the_step_the_run_names(filed, silence):
    """A row with no genre given one, filed nowhere: the run names `adopt apply`
    first, and the two steps file every row (review round one)."""
    import shutil

    from tests.test_adopt_move import _sql

    music = Path(filed.library.root) / "Music"
    shutil.copyfile(music / "stays.flac", music / "fresh.flac")
    assert tags.clear_tags(music / "fresh.flac", ["genre"])
    _sql(
        filed,
        "INSERT INTO djmdContent (ID, FolderPath, Title, GenreID, rb_local_deleted, "
        "created_at, updated_at) SELECT 'fresh', REPLACE(FolderPath, 'stays', 'fresh'), "
        "'fresh', NULL, 0, created_at, updated_at FROM djmdContent WHERE ID = 'stays'",
    )
    collection.reset_cache()
    acted = _tag_set("--row", "fresh", "--row", "mover")
    said = acted["warnings"][1]["message"]
    assert "run `crate adopt apply`" in said and "then `crate adopt move`, which takes the 1" in said
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, applied = drive(_resume(job_id))
    assert code == int(ExitCode.OK), applied
    _move()
    assert _held(filed, "fresh") == {_place(NEW_BUCKET, HIGH)}
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {}


def test_a_genre_given_again_after_the_approval_refuses_the_move_stale(filed):
    """The folder a move files into is part of what was approved (review round one)."""
    from tests.test_adopt_move import _sql

    _sql(
        filed,
        "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
        "VALUES ('9990', 'Tech House', 'u', 0, '2026-10-01', '2026-10-01')",
    )
    _tag_set("--row", "mover")
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    verb = ["tag", "set", "Tech House", "--row", "mover"]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK) and acted["data"]["totals"]["written"] == 1, acted
    collection.reset_cache()

    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    inner = resumed["cause"]["inner"]
    assert inner["reason"] == "decision-stale"
    assert inner["detail"]["moved_under"] == {"mover": "its genre names another folder now"}
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH)}


def test_a_track_leaving_two_folders_in_one_job_spends_both(filed):
    """Two moves of one track in one job each spend their folder (review round two)."""
    from tests.test_adopt_move import _sql

    _sql(
        filed,
        "INSERT INTO djmdGenre (ID, Name, UUID, rb_local_deleted, created_at, updated_at) "
        "VALUES ('9990', 'Tech House', 'u', 0, '2026-10-01', '2026-10-01')",
    )
    _tag_set("--row", "mover")
    for _ in range(2):
        _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
        assert drive(_resume(job_id))[0] == int(ExitCode.OK)
        collection.reset_cache()
        if _ == 0:
            verb = ["tag", "set", "Tech House", "--row", "mover"]
            _code, refused = drive(verb)
            run_id = refused["run_id"]
            drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply",
                   "--actor", "a-person"])
            assert drive(["--run", run_id, *verb])[0] == int(ExitCode.OK)
            collection.reset_cache()
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET, NEW_BUCKET})}
    _move()
    assert _held(filed, "mover") == {_place("tech_house", HIGH)}
    assert dict(genre_moves.read(filed)) == {}


def test_a_hand_placed_second_folder_is_never_asked_without_a_genre_move(filed):
    assert _shown()["items"] == []
    assert _held(filed, "second") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, LOW)}


def test_a_move_already_half_made_by_adoption_only_removes(filed):
    _tag_set("--row", "mover")
    # ADOPTION FILES IT IN THE NEW FOLDER FIRST, and leaves the old one.
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, applied = drive(_resume(job_id))
    assert code == int(ExitCode.OK), applied
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)}
    (move,) = _shown()["items"]
    assert (move["add"], move["remove"]) == ("", [HIGH])
    _move()
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}


def test_a_genre_moved_back_asks_nothing_of_the_old_folder(filed):
    _tag_set("--row", "mover")
    verb = ["tag", "set", OLD_GENRE, "--row", "mover"]
    _code, refused = drive(verb)
    run_id = refused["run_id"]
    drive(["run", "decide", run_id, genre_set_cli.CONFIRM_GATE, "apply", "--actor", "a-person"])
    code, acted = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), acted
    collection.reset_cache()
    # THE OLD BUCKET IS THE ONE THE GENRE NAMES AGAIN, and the new one was never
    # filed, so the entry is spent and nothing waits on it.
    assert dict(genre_moves.read(filed)) == {}
    assert _shown()["items"] == []
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH)}


def _entry(bucket: str, genre: str) -> "adopt_move.PlanEntry":
    from cratekit.adopt.plan import PlanEntry
    from cratekit.adopt.scan import Disposition, Readability

    return PlanEntry(
        entry_id=f"e-{bucket}", content_id="mover", recorded="/m.flac",
        disposition=Disposition.ROUTE, category=Readability.READABLE, genre=genre,
        tree=DECLARED.tree.id, bucket=bucket, sub=HIGH, energy=8,
    )


def test_a_bucket_any_entry_of_the_track_claims_is_never_left():
    """Per content identifier, never per entry, so a second genre folder an
    entry of the same track files it in (U340) is kept."""
    moved = {"mover": frozenset({OLD_BUCKET})}
    alone = [_entry(NEW_BUCKET, NEW_GENRE)]
    assert adopt_move.still_moved(alone, DECLARED, moved) == moved
    both = [*alone, _entry(OLD_BUCKET, NEW_GENRE)]
    assert adopt_move.still_moved(both, DECLARED, moved) == {}
    named = [_entry(NEW_BUCKET, OLD_GENRE)]
    assert adopt_move.still_moved(named, DECLARED, moved) == {}


def test_a_move_stopped_before_its_removal_keeps_its_entry_and_a_resume_finishes(
    filed, monkeypatch
):
    """The entry is spent only once the track reads back moved (mutation table, M24)."""
    from cratekit.core import jobs, rb_writer
    from tests.test_adopt_move import _fails

    _tag_set("--row", "mover")
    _run_id, job_id = approve_and_queue(["adopt", "move"], "adopt.move.approve")
    with monkeypatch.context() as patched:
        patched.setattr(rb_writer, "remove_memberships", _fails)
        code, failed = drive(_resume(job_id))
    assert code != int(ExitCode.OK), failed
    assert _held(filed, "mover") == {_place(OLD_BUCKET, HIGH), _place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {"mover": frozenset({OLD_BUCKET})}

    with jobs.open_store() as store:
        jobs.retry(store, job_id)
    collection.reset_cache()
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    assert _held(filed, "mover") == {_place(NEW_BUCKET, HIGH)}
    assert dict(genre_moves.read(filed)) == {}
