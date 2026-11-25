"""U162: ``crate intake land --rehearse`` plans and applies the landing on its own scratch area.

A rehearsal leaves staging, the music folder and the live database as they were, digests as
the live plan, keeps every area apart and names the area it leaves when it fails. D1 applies."""

from __future__ import annotations

import errno
import hashlib
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, land_cli, landing, native, rehearsal
from tests import test_intake_land_native as land
from tests.cli_drive import drive
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414


def _bytes(folder: Path) -> dict[str, str]:
    """Every file in ``folder`` by name, its content hashed, and its time."""
    files = [path for path in sorted(folder.iterdir()) if path.is_file()]
    return {p.name: f"{hashlib.sha256(p.read_bytes()).hexdigest()} {p.stat().st_mtime_ns}"
            for p in files}


def _database(cfg: config.Config) -> str:
    return hashlib.sha256(Path(cfg.library.db_path).read_bytes()).hexdigest()


def _areas(cfg: config.Config) -> list[Path]:
    """Every rehearsal area left on either half."""
    found = []
    for root in (rehearsal.volume_root(cfg), rehearsal.local_root()):
        if root.is_dir():
            found.extend(path for path in root.iterdir() if path.is_dir())
    return found


def _rehearse() -> tuple[int, dict]:
    return drive(land._land("--rehearse"))


@pytest.fixture
def cfg(native_library, silence) -> config.Config:
    """The native library's configuration, with one file staged."""
    cfg, _root = native_library
    land._stage(cfg, silence, "One.flac")
    return cfg


# Nothing live moves, and the digest is the live plan's
def _rehearse_two_untouched(cfg: config.Config, silence: Path, name: str) -> dict:
    """Stage two files and rehearse them: applied on the copy, nothing live moved."""
    land._stage(cfg, silence, "One.flac")
    land._stage(cfg, silence, "Two.flac")
    staged = _bytes(land._staging(cfg))
    database = _database(cfg)
    code, rehearsed = drive(["intake", "land", "--name", name, "--rehearse"])
    assert code == int(ExitCode.OK), rehearsed
    assert _bytes(land._staging(cfg)) == staged
    assert not land._music(cfg, name).exists(), "the rehearsal made the live batch folder"
    assert _database(cfg) == database
    assert land._landed_rows(cfg) == []
    facts = rehearsed["data"]["totals"]["rehearsal"]
    assert facts["landed"] == 2 and facts["added"] == 2 and facts["refused"] == 0
    assert facts["area removed"] is True
    assert _areas(cfg) == [], "a rehearsal that ended left its area"
    _assert_live_equal(rehearsed, ["intake", "land", "--name", name])
    return rehearsed


def _assert_live_equal(rehearsed: dict, verb: list[str]) -> None:
    shown = land._shown(verb)
    assert shown["digest"] == rehearsed["data"]["digest"]
    assert rehearsed["run_id"] in shown["rehearsal"]
    assert "equal to this plan's" in shown["rehearsal"], shown["rehearsal"]
    assert "differs from the rehearsal" not in shown


def test_a_rehearsal_leaves_staging_music_and_database_as_they_were(cfg, silence):
    rehearsed = _rehearse_two_untouched(cfg, silence, land.BATCH)
    # The landing was applied, on the copy, and read back there.
    facts = rehearsed["data"]["totals"]["rehearsal"]
    assert facts["active rows after"] == facts["active rows before"] + 2
    assert facts["landed rows gridless"] is True and facts["integrity"] == "ok"
    # The plan shown is the live plan: the live staging folder and music folder.
    items = rehearsed["data"]["items"]
    assert sorted(Path(item["from"]).name for item in items) == ["One.flac", "Two.flac"]
    assert {str(Path(item["from"]).parent) for item in items} == {str(land._staging(cfg))}
    assert {str(Path(item["to"]).parent) for item in items} == {str(land._music(cfg))}


def test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines(cfg, silence):
    """A live plan shows no rehearsal line but its own batch's, never another batch's."""
    shown = land._shown(land._land())
    assert "rehearsal" not in shown and "differs from the rehearsal" not in shown
    code, rehearsed = drive(["intake", "land", "--name", "another batch", "--rehearse"])
    assert code == int(ExitCode.OK), rehearsed
    assert "rehearsal" not in land._shown(land._land())
    code, rehearsed = _rehearse()
    assert code == int(ExitCode.OK), rehearsed
    land._stage(cfg, silence, "Two.flac")
    shown = land._shown(land._land())
    assert shown["digest"] != rehearsed["data"]["digest"]
    assert rehearsed["run_id"] in shown["rehearsal"]
    assert f"differs from this plan's {shown['digest']}" in shown["rehearsal"]
    lines = shown["differs from the rehearsal"]
    assert any(line.startswith("+ ") and "Two.flac" in line for line in lines), lines
    assert not any("Two.flac" in line for line in lines if line.startswith("- ")), lines


# Refusals
def test_empty_staging_rehearses_nothing_and_rekordbox_refuses(
        native_library, silence, monkeypatch):
    cfg, _root = native_library
    code, envelope = _rehearse()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _areas(cfg) == []
    land._stage(cfg, silence, "One.flac")
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "rekordbox-running"
    assert _areas(cfg) == []
    assert land._staged_names(cfg) == ["One.flac"]


def test_a_rehearsal_on_the_bridge_is_refused(acknowledged, silence):
    cfg = acknowledged
    land._stage(cfg, silence, "One.flac")
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "intake-list-unusable"
    assert "--rehearse" in refused["cause"]["message"]
    assert _areas(cfg) == []


def test_a_scratch_plan_not_the_live_plan_applies_nothing(cfg, monkeypatch):
    """The area's plan, mapped back, must read as the live plan, or it refuses."""
    monkeypatch.setattr(rehearsal, "mapped", lambda value, _pairs: value)
    code, refused = _rehearse()
    assert refused["cause"]["reason"] == "decision-stale", refused
    assert "nothing was applied" in refused["cause"]["message"]
    differs = refused["cause"]["detail"]["differs"]
    # The area's lines are marked - and the live plan's +, as the gate screen marks them (U188).
    assert any(line.startswith("- ") and "rehearsals" in line for line in differs)
    assert not any(line.startswith("+ ") and "rehearsals" in line for line in differs)
    (volume, local) = refused["cause"]["detail"]["rehearsal_area"]
    # Kept and named, and nothing was landed even on the copy's staging clones.
    assert sorted(p.name for p in (Path(volume) / "staging").iterdir()) == ["One.flac"]
    assert Path(local).is_dir()
    assert land._staged_names(cfg) == ["One.flac"]


# Areas are per run, and a failed one is kept and named
def test_two_areas_are_apart_and_copy_library_state_only(native_library):
    """Land reads the newest rehearsal of its own folder and batch."""
    cfg, _root = native_library
    config.state_path("snapshots", cfg).joinpath("big").mkdir(parents=True)
    config.state_path("session_log", cfg).mkdir(parents=True, exist_ok=True)
    config.state_path("write_lock", cfg).parent.mkdir(parents=True, exist_ok=True)
    config.state_path("write_lock", cfg).write_text("")
    first = rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-aaaa")
    second = rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-bbbb")
    try:
        assert first.volume != second.volume and first.local != second.local
        assert first.database != second.database
        assert ":" not in first.volume.name, "a colon is refused on an exFAT volume"
        with pytest.raises(CratekitError) as caught:
            rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-aaaa")
        assert caught.value.cause.reason == "output-exists"
        # The origin a refusal carries kept its name when the module moved to intake (U331).
        assert tuple(caught.value.cause.origin) == ("core", "rehearsal")
        assert Path(config.library_state_dir(first.cfg)).is_relative_to(first.volume)
        for key in ("tree_registry", "backup_ack"):
            assert config.state_path(key, first.cfg).is_file(), key
        for key in ("snapshots", "session_log", "write_lock"):
            assert not config.state_path(key, first.cfg).exists(), key
        assert rb_writer.live_db_path(first.cfg) == first.database
        assert first.database.is_relative_to(first.volume)
        assert Path(first.cfg.library.root, first.cfg.library.music_dir).is_relative_to(
            first.volume)
    finally:
        rehearsal.remove(first)
        rehearsal.remove(second)
    key = {"folder": "/f", "batch": "b"}
    rehearsal.record("r1", verb=land_cli.REHEARSAL_VERB, key=key, digest="d1", plan=[], facts={})
    rehearsal.record("r2", verb="other verb", key=key, digest="d2", plan=[], facts={})
    found = rehearsal.latest(verb=land_cli.REHEARSAL_VERB, key=key)
    assert found is not None and found["run_id"] == "r1"
    assert (
        rehearsal.latest(verb=land_cli.REHEARSAL_VERB, key={"folder": "/f", "batch": "c"}) is None
    )


def test_a_rehearsal_leaves_another_runs_area_alone(cfg):
    other = rehearsal.open_area(
        cfg, "2026-10-31T01:00:00Z-other", files=[land._staging(cfg) / "One.flac"])
    held = _bytes(other.volume / "db")
    try:
        code, rehearsed = _rehearse()
        assert code == int(ExitCode.OK), rehearsed
        assert other.volume.is_dir() and other.local.is_dir()
        assert _bytes(other.volume / "db") == held
        assert sorted(p.name for p in other.staging.iterdir()) == ["One.flac"]
    finally:
        rehearsal.remove(other)


@pytest.mark.parametrize(
    ("failure", "reason"),
    [
        (RuntimeError("the power went"), "internal-error"),
        (KeyboardInterrupt(), "cancelled"),
        (None, "backup-acknowledgment"),
    ])
def test_a_failed_rehearsal_keeps_its_area_and_names_it(cfg, monkeypatch, failure, reason):
    """Failure is internal, interrupt a cancel, a refusal its own reason, each naming the area."""
    database = _database(cfg)

    def interrupted(*_args, **_kwargs):
        raise failure
    if failure is None:
        config.state_path("backup_ack", cfg).unlink()
    else:
        monkeypatch.setattr(native, "apply_rows", interrupted)
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"].startswith(reason), refused
    assert failure is not None or "rehearsal area is kept at" in refused["cause"]["message"]
    area = refused["cause"]["detail"]["rehearsal_area"]
    assert len(area) == 2 and all(Path(path).is_dir() for path in area)
    for path in area:
        assert path in refused["cause"]["message"]
    # The live library is as it was: the move happened at the area.
    assert land._staged_names(cfg) == ["One.flac"]
    assert not land._music(cfg).exists()
    assert _database(cfg) == database
    assert (Path(area[0]) / "staging").is_dir()


# The helper's own guards
def test_the_witness_refuses_a_live_change(cfg, tmp_path):
    staged = land._staging(cfg) / "One.flac"
    before = rehearsal.witness(cfg, (land._staging(cfg), land._music(cfg)))
    rehearsal.assert_untouched(before)
    staged.rename(staged.with_name("Moved.flac"))
    with pytest.raises(CratekitError) as caught:
        rehearsal.assert_untouched(before)
    assert str(land._staging(cfg)) in caught.value.cause.message
    before = rehearsal.witness(cfg, ())
    with Path(cfg.library.db_path).open("ab") as handle:
        handle.write(b"\0")
    with pytest.raises(CratekitError) as caught:
        rehearsal.assert_untouched(before, kept=(tmp_path,))
    assert caught.value.cause.reason == "internal-error"
    assert str(tmp_path) in caught.value.cause.message


def test_a_clone_is_never_a_hard_link_and_the_plan_lines_name_every_leaf(tmp_path):
    """The differing lines name both sides."""
    assert rehearsal.differing(["a = 1", "b = 2"], ["a = 1", "b = 3"]) == ["- b = 2", "+ b = 3"]
    assert rehearsal.differing(["a = 1"], ["a = 1"]) == []
    assert rehearsal.lines({"b": [1, {"c": "x"}], "a": True}) == [
        "a = true", "b[0] = 1", 'b[1].c = "x"'
    ]
    source = tmp_path / "one.flac"
    source.write_bytes(b"audio")
    copy = tmp_path / "area" / "one.flac"
    rehearsal.clone(source, copy)
    assert copy.read_bytes() == b"audio"
    assert copy.stat().st_ino != source.stat().st_ino
    assert copy.stat().st_mtime_ns == source.stat().st_mtime_ns
    copy.write_bytes(b"changed")
    assert source.read_bytes() == b"audio"


# The review's round one
def test_a_name_the_live_folder_holds_is_refused_at_the_area(native_library, silence):
    """The area holds the live folder's names, so it refuses what the live landing will."""
    cfg, _root = native_library
    # A batch landed again by name goes back to its filed folder (U164), so a name in it is held.
    land._land_first(cfg, silence)
    (land._music(cfg) / "One.flac").write_bytes(b"left by an earlier landing")
    land._stage(cfg, silence, "One.flac")
    land._stage(cfg, silence, "Two.flac")
    code, rehearsed = _rehearse()
    assert code == int(ExitCode.OK), rehearsed
    facts = rehearsed["data"]["totals"]["rehearsal"]
    assert facts["landed"] == 1 and facts["refused"] == 1 and facts["added"] == 1
    assert (land._music(cfg) / "One.flac").read_bytes() == b"left by an earlier landing"
    assert sorted(p.name for p in land._music(cfg).iterdir()) == ["One.flac", "Zero.flac"]
    assert land._staged_names(cfg) == ["One.flac", "Two.flac"]


def _stray_into(monkeypatch, folder: Path) -> None:
    """The engine's apply, run for real, then a file written into ``folder``."""
    real = landing.apply_native

    def straying(*args, **kwargs):
        landed = real(*args, **kwargs)
        (folder / "Stray.flac").write_bytes(b"x")
        return landed
    monkeypatch.setattr(landing, "apply_native", straying)


def test_a_rehearsal_that_touched_the_live_library_is_refused(cfg, monkeypatch):
    _stray_into(monkeypatch, land._staging(cfg))
    code, refused = _rehearse()
    assert refused["cause"]["reason"] == "internal-error", refused
    assert "rehearsal changed" in refused["cause"]["message"]
    assert str(land._staging(cfg)) in refused["cause"]["message"]
    assert all(Path(path).is_dir() for path in refused["cause"]["detail"]["kept"])


def test_a_rehearsal_that_touched_another_year_s_batch_is_refused(cfg, silence, monkeypatch):
    """A batch landed into again goes back to its recorded folder (U164), watched too."""
    monkeypatch.setattr(batch_name, "today", lambda: date(2025, 12, 31))
    verb = ["intake", "land", "--name", "Friday warmup"]
    code, first, _refused = land._two_acts(verb)
    assert code == int(ExitCode.OK), first
    filed = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025"
    filed = filed / "12_31_25 Friday warmup"
    assert (filed / "One.flac").is_file()
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 27))
    land._stage(cfg, silence, "Two.flac")
    _stray_into(monkeypatch, filed)
    code, refused = drive([*verb, "--rehearse"])
    assert refused["cause"]["reason"] == "internal-error", refused
    assert str(filed) in refused["cause"]["message"]


@pytest.mark.parametrize(
    ("check", "said"),
    [
        ("assert_rows_gridless", "a landed row carries an analysis value"),
        ("assert_rows_identified", "a landed row has no file id"),
    ])
def test_a_landed_row_the_read_back_refuses_is_refused(cfg, monkeypatch, check, said):
    """A row with a grid or with no file id, never reported gridless."""
    calls: list[object] = []

    def refusing(landed):
        calls.append(landed)
        raise land_cli.refuse("internal-error", said)
    monkeypatch.setattr(native, check, refusing)
    code, refused = _rehearse()
    assert calls, "the rehearsal never read its landed rows back"
    assert refused["cause"]["reason"] == "internal-error", refused
    assert said in refused["cause"]["message"]
    assert "gridless" not in str(refused.get("data"))


# A library whose rekordbox base drive is not its mount (U188)
def _renamed_drive(cfg: config.Config, tmp_path: Path, base: str | None = None) -> str:
    """Record the database as made on a drive no longer mounted; answers the base drive."""
    base = base or str(tmp_path.parent / "old-drive")
    land._execute(cfg, "UPDATE djmdProperty SET BaseDBDrive = ?, CurrentDBDrive = ?",
             base + "/", str(tmp_path) + "/")
    return base


def test_a_base_drive_not_the_mount_rehearses_equal(cfg, silence, tmp_path):
    """FolderPaths differ only by the area's prefix, and the accented name is escaped in JSON."""
    base = _renamed_drive(cfg, tmp_path)
    name = "2026-09-29_café"
    rehearsed = _rehearse_two_untouched(cfg, silence, name)
    # The plan shown is the live one, its rows stored under the base drive.
    stored = sorted(item["row"]["FolderPath"] for item in rehearsed["data"]["items"])
    assert stored == [str(native.stored_folder_path(
        land._music(cfg, name) / one, base_drive=base, current_drive=str(tmp_path)
    )) for one in ("One.flac", "Two.flac")]
    assert all(path.startswith(base + "/library/") for path in stored), stored


def test_on_a_renamed_drive_a_differing_name_still_refuses(cfg, tmp_path, monkeypatch):
    """The stored pair maps the prefix alone, so a difference past it is refused."""
    base = _renamed_drive(cfg, tmp_path)
    real = rehearsal.mapped

    def planted(value, pairs):
        back = real(value, pairs)
        if isinstance(back, dict) and "plan" in back:
            # The area's plan, mapped back, with one row's file name changed.
            columns = back["plan"]["rows"][0]["columns"]
            columns["FolderPath"] = columns["FolderPath"].replace("One.flac", "Uno.flac")
        return back
    monkeypatch.setattr(rehearsal, "mapped", planted)
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    cause = refused["cause"]
    assert cause["reason"] == "decision-stale", refused
    differs = cause["detail"]["differs"]
    assert any(
        line.startswith("- ") and "FolderPath" in line and "Uno.flac" in line for line in differs)
    assert any(
        line.startswith("+ ") and "FolderPath" in line and "One.flac" in line for line in differs)
    assert len(differs) == 2, differs
    # The message names the field and both spellings it compared under.
    message = cause["message"]
    assert "in rows.columns.FolderPath, so nothing was applied there" in message, message
    area_folder = cause["detail"]["mapped"]
    assert any(
        scratch.startswith(base + "/") and live.startswith(base + "/")
        for scratch, live in area_folder)
    for scratch, live in area_folder:
        assert scratch in message and live in message
    (volume, local) = cause["detail"]["rehearsal_area"]
    assert Path(volume).is_dir() and Path(local).is_dir()
    assert land._staged_names(cfg) == ["One.flac"]
    assert land._landed_rows(cfg) == []


def test_on_a_drive_recorded_as_its_mount_it_is_as_it_was(cfg, tmp_path):
    """A base drive that is the mount stores the mounted spelling, so the pair adds nothing."""
    _renamed_drive(cfg, tmp_path, base=str(tmp_path))
    code, rehearsed = _rehearse()
    assert code == int(ExitCode.OK), rehearsed
    (item,) = rehearsed["data"]["items"]
    assert item["row"]["FolderPath"] == str(land._music(cfg) / "One.flac")
    _assert_live_equal(rehearsed, land._land())


def test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once():
    """A longer pair is never half mapped by a shorter one, and an empty one is ignored."""
    short = ("/drive/area", "/drive/live")
    long = ("/old/drive/area", "/old/stored")
    value = {"a": "/old/drive/area/Music/a.flac", "b": ["/drive/area/Music/b.flac"]}
    for pairs in ((short, long), (long, short)):
        assert rehearsal.mapped(value, pairs + (("", "/nowhere"),)) == {
            "a": "/old/stored/Music/a.flac", "b": ["/drive/live/Music/b.flac"]
        }
    assert land_cli._fields_of([
        '- plan.rows[0].columns.FolderPath = "/a"', '+ plan.rows[1].columns.FolderPath = "/b"',
        "- plan.vox.rows[0][1] = 2", '+ gate.target = "/c"',
    ]) == ["rows.columns.FolderPath", "vox.rows", "target"]


# The rehearsal's check of its scratch database with no room for its copy (R-1677)
def _is_the_area_database(target) -> bool:
    """The rehearsal's scratch database, rather than its capture's copy of it."""
    path = Path(target)
    return path.parent.name == "db" and "rehearsals" in path.parts


def _area_check_answers(monkeypatch, *, error: OSError | None) -> list[dict]:
    """The real check everywhere, but the area's own copy failing with ``error``."""
    real = rb_writer.integrity_ok
    asked: list[dict] = []

    def checking(target, **kwargs):
        if _is_the_area_database(target):
            asked.append(kwargs)
            if error is not None and kwargs.get("raise_copy_failure"):
                raise rb_writer.IntegrityCheckCopyFailed(Path(target), error, Path("/scratch"))
            if error is not None:
                return False
        return real(target, unlock=False)
    monkeypatch.setattr(rb_writer, "integrity_ok", checking)
    return asked


@pytest.mark.parametrize("failing", ["no room", "the check", "its copy otherwise"])
def test_a_failed_integrity_check_is_refused_naming_the_area(cfg, monkeypatch, failing):
    """A copy that found no room is refused under the room slug; any other failure as failed."""
    asked = []
    if failing == "the check":
        monkeypatch.setattr(rb_writer, "integrity_ok", lambda *_args, **_kwargs: False)
    else:
        code = errno.ENOSPC if failing == "no room" else errno.EACCES
        asked = _area_check_answers(monkeypatch, error=OSError(code, "refused"))
    code, refused = _rehearse()
    assert "rehearsal area is kept at" in refused["cause"]["message"]
    if failing == "no room":
        assert asked == [{"raise_copy_failure": True}]
        assert refused["cause"]["reason"] == "snapshot-check-temp-full", refused
        assert "/scratch" in refused["cause"]["message"]
    else:
        assert refused["cause"]["reason"] == "snapshot-integrity-failed", refused


def test_no_room_for_the_check_refuses_before_its_copy(cfg, monkeypatch):
    """Measured before the check's copy, as the capture's is: no copy is attempted."""
    asked = _area_check_answers(monkeypatch, error=None)
    captured: list[object] = []
    real_measure, real_free = snapshot.assert_room_for_check, snapshot._free_bytes

    def the_captures_measure(database, **kwargs):
        # The capture measures the same database for its own check, naming its store.
        done = real_measure(database, **kwargs)
        if _is_the_area_database(database):
            captured.append(kwargs.get("store"))
        return done

    def no_room_once_captured(root):
        # What is measured after the capture's own check is the landing's, which
        # names no store and reads the measure through ``core.session`` (U331):
        # the measure itself is left real, and only the room it finds is gone.
        return 0 if captured else real_free(root)
    monkeypatch.setattr(snapshot, "assert_room_for_check", the_captures_measure)
    monkeypatch.setattr(snapshot, "_free_bytes", no_room_once_captured)
    assert session.assert_room_for_check is real_measure
    code, refused = _rehearse()
    assert refused["cause"]["reason"] == "snapshot-check-temp-full", refused
    assert "0 bytes free" in refused["cause"]["message"]
    assert refused["cause"]["detail"]["shares_volume_with"] is None, "the capture's check refused"
    assert asked == [], "the area's check copied after the measure refused"
    assert len(captured) == 1 and captured[0] is not None, captured


def test_a_stale_refusal_on_a_drive_that_never_moved_names_each_pair_once(cfg, monkeypatch):
    """R-2071. The stored pair repeats the folder pair here, and is dropped, not shown twice."""
    monkeypatch.setattr(rehearsal, "mapped", lambda value, _pairs: value)
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    cause = refused["cause"]
    assert cause["reason"] == "decision-stale", refused
    pairs = [tuple(pair) for pair in cause["detail"]["mapped"]]
    assert len(pairs) == 2, pairs
    assert len(set(pairs)) == len(pairs), pairs
    for scratch, live in pairs:
        assert cause["message"].count(f"{scratch} to {live}") == 1, cause["message"]


def test_a_rehearsal_refuses_an_analysis_value_its_rows_carry_after_the_commit(cfg, monkeypatch):
    """The area's rows are read again after its commit, as the live landing's are (R-2075).

    The key is planted on the area's own handle after the guarded commit, so
    only the read back after the commit can refuse it, in its own wording.
    """
    land.taint_after_the_guarded_commit(monkeypatch)
    code, rehearsed = _rehearse()
    assert code != int(ExitCode.OK), rehearsed
    land.assert_refused_after_the_commit(rehearsed)
