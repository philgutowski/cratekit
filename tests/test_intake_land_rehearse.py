"""U162: ``crate intake land --rehearse`` plans and applies the landing on its own scratch area.

The session's rule approves a database write gate only when a rehearsal
matches. These tests drive the real dispatcher over real FLAC containers
against the disposable database ``tests/test_intake_land_native.py`` builds,
and pin what the brief asks: a rehearsal leaves the staging folder, the music
folder and the live database byte for byte as they were, digests as the live
plan, refuses under a running rekordbox, keeps every area apart, and names the
area it leaves when it fails. The live landing's gate then names the
rehearsal and says whether its plan equals it.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, rehearsal
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli, landing, native
from tests.cli_drive import drive
from tests.test_intake_land_native import (
    _land,
    _land_first,
    _landed_rows,
    _music,
    _stage,
    _staged_names,
    _staging,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414


def _bytes(folder: Path) -> dict[str, str]:
    """Every file in ``folder`` by name, its content hashed, and its time."""
    return {
        path.name: f"{hashlib.sha256(path.read_bytes()).hexdigest()} {path.stat().st_mtime_ns}"
        for path in sorted(folder.iterdir())
        if path.is_file()
    }


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
    return drive(_land("--rehearse"))


# ---------------------------------------------------------------------------
# Nothing live moves, and the digest is the live plan's
# ---------------------------------------------------------------------------


def test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    staged = _bytes(_staging(cfg))
    database = _database(cfg)

    code, rehearsed = _rehearse()

    assert code == int(ExitCode.OK), rehearsed
    assert _bytes(_staging(cfg)) == staged
    assert not _music(cfg).exists(), "the rehearsal made the live batch folder"
    assert _database(cfg) == database
    assert _landed_rows(cfg) == []
    # The landing was applied, on the copy, and read back there.
    facts = rehearsed["data"]["totals"]["rehearsal"]
    assert facts["landed"] == 2 and facts["added"] == 2 and facts["refused"] == 0
    assert facts["active rows after"] == facts["active rows before"] + 2
    assert facts["landed rows gridless"] is True and facts["integrity"] == "ok"
    assert facts["area removed"] is True
    assert _areas(cfg) == [], "a rehearsal that ended left its area"
    # The plan shown is the live plan: the live staging folder and music folder.
    items = rehearsed["data"]["items"]
    assert sorted(Path(item["from"]).name for item in items) == ["One.flac", "Two.flac"]
    assert {str(Path(item["from"]).parent) for item in items} == {str(_staging(cfg))}
    assert {str(Path(item["to"]).parent) for item in items} == {str(_music(cfg))}


def test_the_rehearsal_digest_equals_the_live_plans_and_the_live_gate_says_so(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")
    code, rehearsed = _rehearse()
    assert code == int(ExitCode.OK), rehearsed

    code, live = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), live
    shown = live["cause"]["detail"]["shown"]
    assert shown["digest"] == rehearsed["data"]["digest"]
    assert rehearsed["run_id"] in shown["rehearsal"]
    assert "equal to this plan's" in shown["rehearsal"]
    assert "differs from the rehearsal" not in shown


def test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, rehearsed = _rehearse()
    assert code == int(ExitCode.OK), rehearsed
    _stage(cfg, silence, "Two.flac")

    code, live = drive(_land())

    assert code == int(ExitCode.DECISION_REQUIRED), live
    shown = live["cause"]["detail"]["shown"]
    assert shown["digest"] != rehearsed["data"]["digest"]
    assert rehearsed["run_id"] in shown["rehearsal"]
    assert f"differs from this plan's {shown['digest']}" in shown["rehearsal"]
    lines = shown["differs from the rehearsal"]
    assert any(line.startswith("+ ") and "Two.flac" in line for line in lines), lines
    assert not any("Two.flac" in line for line in lines if line.startswith("- ")), lines


def test_a_live_plan_with_no_rehearsal_shows_no_rehearsal_line(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, live = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), live
    shown = live["cause"]["detail"]["shown"]
    assert "rehearsal" not in shown and "differs from the rehearsal" not in shown


def test_a_rehearsal_of_another_batch_is_not_the_one_compared(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, rehearsed = drive(["intake", "land", "--name", "another batch", "--rehearse"])
    assert code == int(ExitCode.OK), rehearsed
    code, live = drive(_land())
    assert "rehearsal" not in live["cause"]["detail"]["shown"]


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------


def test_a_rehearsal_with_rekordbox_running_refuses_and_copies_nothing(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)

    code, refused = _rehearse()

    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "rekordbox-running"
    assert _areas(cfg) == []
    assert _staged_names(cfg) == ["One.flac"]


def test_a_rehearsal_on_the_bridge_is_refused(acknowledged, silence):
    cfg = acknowledged
    _stage(cfg, silence, "One.flac")
    code, refused = _rehearse()
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "intake-list-unusable"
    assert "--rehearse" in refused["cause"]["message"]
    assert _areas(cfg) == []


def test_an_empty_staging_folder_rehearses_nothing(native_library):
    cfg, _root = native_library
    code, envelope = _rehearse()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert _areas(cfg) == []


def test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing(
    native_library, silence, monkeypatch
):
    """The area's plan, mapped back, must read as the live plan. Mapping nothing
    back leaves every scratch path in it, so the rehearsal refuses before the
    apply and names the lines."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    monkeypatch.setattr(rehearsal, "mapped", lambda value, _pairs: list(value))

    code, refused = _rehearse()

    assert refused["cause"]["reason"] == "decision-stale", refused
    assert "nothing was applied" in refused["cause"]["message"]
    differs = refused["cause"]["detail"]["differs"]
    assert any(line.startswith("+ ") and "rehearsals" in line for line in differs)
    (volume, local) = refused["cause"]["detail"]["rehearsal_area"]
    # Kept and named, and nothing was landed even on the copy's staging clones.
    assert sorted(p.name for p in (Path(volume) / "staging").iterdir()) == ["One.flac"]
    assert Path(local).is_dir()
    assert _staged_names(cfg) == ["One.flac"]


# ---------------------------------------------------------------------------
# Areas are per run, and a failed one is kept and named
# ---------------------------------------------------------------------------


def test_two_rehearsals_use_two_areas_and_one_area_is_never_shared(native_library):
    cfg, _root = native_library
    first = rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-aaaa")
    second = rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-bbbb")
    try:
        assert first.volume != second.volume and first.local != second.local
        assert first.database != second.database
        assert ":" not in first.volume.name, "a colon is refused on an exFAT volume"
        with pytest.raises(CratekitError) as caught:
            rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-aaaa")
        assert caught.value.cause.reason == "output-exists"
    finally:
        rehearsal.remove(first)
        rehearsal.remove(second)


def test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    other = rehearsal.open_area(
        cfg, "2026-10-31T01:00:00Z-other", files=[_staging(cfg) / "One.flac"]
    )
    held = _bytes(other.volume / "db")
    try:
        code, rehearsed = _rehearse()
        assert code == int(ExitCode.OK), rehearsed
        assert other.volume.is_dir() and other.local.is_dir()
        assert _bytes(other.volume / "db") == held
        assert sorted(p.name for p in other.staging.iterdir()) == ["One.flac"]
    finally:
        rehearsal.remove(other)


def test_an_interrupted_rehearsal_keeps_its_area_and_names_it(native_library, silence, monkeypatch):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    database = _database(cfg)

    def interrupted(*_args, **_kwargs):
        raise RuntimeError("the power went")

    monkeypatch.setattr(native, "apply_rows", interrupted)

    code, refused = _rehearse()

    assert code != int(ExitCode.OK), refused
    area = refused["cause"]["detail"]["rehearsal_area"]
    assert len(area) == 2 and all(Path(path).is_dir() for path in area)
    for path in area:
        assert path in refused["cause"]["message"]
    # The live library is as it was: the move happened at the area.
    assert _staged_names(cfg) == ["One.flac"]
    assert not _music(cfg).exists()
    assert _database(cfg) == database
    assert (Path(area[0]) / "staging").is_dir()


def test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    config.state_path("backup_ack", cfg).unlink()

    code, refused = _rehearse()

    assert refused["cause"]["reason"].startswith("backup-acknowledgment"), refused
    assert "rehearsal area is kept at" in refused["cause"]["message"]
    assert all(Path(path).is_dir() for path in refused["cause"]["detail"]["rehearsal_area"])


# ---------------------------------------------------------------------------
# The helper's own guards
# ---------------------------------------------------------------------------


def test_the_witness_refuses_a_live_database_that_changed(native_library, tmp_path):
    cfg, _root = native_library
    before = rehearsal.witness(cfg, ())
    with Path(cfg.library.db_path).open("ab") as handle:
        handle.write(b"\0")
    with pytest.raises(CratekitError) as caught:
        rehearsal.assert_untouched(before, kept=(tmp_path,))
    assert caught.value.cause.reason == "internal-error"
    assert str(tmp_path) in caught.value.cause.message


def test_the_witness_refuses_a_live_folder_that_changed(native_library, silence):
    cfg, _root = native_library
    staged = _stage(cfg, silence, "One.flac")
    before = rehearsal.witness(cfg, (_staging(cfg), _music(cfg)))
    rehearsal.assert_untouched(before)
    staged.rename(staged.with_name("Moved.flac"))
    with pytest.raises(CratekitError) as caught:
        rehearsal.assert_untouched(before)
    assert str(_staging(cfg)) in caught.value.cause.message


def test_the_area_copies_library_state_but_no_lock_snapshot_or_session(native_library):
    cfg, _root = native_library
    config.state_path("snapshots", cfg).joinpath("big").mkdir(parents=True)
    config.state_path("session_log", cfg).mkdir(parents=True, exist_ok=True)
    config.state_path("write_lock", cfg).parent.mkdir(parents=True, exist_ok=True)
    config.state_path("write_lock", cfg).write_text("")
    area = rehearsal.open_area(cfg, "2026-10-31T01:00:00Z-state")
    try:
        assert Path(config.library_state_dir(area.cfg)).is_relative_to(area.volume)
        for key in ("tree_registry", "backup_ack"):
            assert config.state_path(key, area.cfg).is_file(), key
        for key in ("snapshots", "session_log", "write_lock"):
            assert not config.state_path(key, area.cfg).exists(), key
        assert rb_writer.live_db_path(area.cfg) == area.database
        assert area.database.is_relative_to(area.volume)
        assert Path(area.cfg.library.root, area.cfg.library.music_dir).is_relative_to(area.volume)
    finally:
        rehearsal.remove(area)


def test_a_clone_is_never_a_hard_link(tmp_path):
    source = tmp_path / "one.flac"
    source.write_bytes(b"audio")
    copy = tmp_path / "area" / "one.flac"
    rehearsal.clone(source, copy)
    assert copy.read_bytes() == b"audio"
    assert copy.stat().st_ino != source.stat().st_ino
    assert copy.stat().st_mtime_ns == source.stat().st_mtime_ns
    copy.write_bytes(b"changed")
    assert source.read_bytes() == b"audio"


def test_the_differing_lines_name_both_sides():
    assert rehearsal.differing(["a = 1", "b = 2"], ["a = 1", "b = 3"]) == ["- b = 2", "+ b = 3"]
    assert rehearsal.differing(["a = 1"], ["a = 1"]) == []


def test_the_plan_lines_name_every_leaf():
    assert rehearsal.lines({"b": [1, {"c": "x"}], "a": True}) == [
        "a = true",
        "b[0] = 1",
        'b[1].c = "x"',
    ]


def test_land_cli_reads_the_newest_rehearsal_of_its_folder_and_batch(native_library):
    cfg, _root = native_library
    key = {"folder": "/f", "batch": "b"}
    rehearsal.record("r1", verb=land_cli.REHEARSAL_VERB, key=key, digest="d1", plan=[], facts={})
    rehearsal.record("r2", verb="other verb", key=key, digest="d2", plan=[], facts={})
    found = rehearsal.latest(verb=land_cli.REHEARSAL_VERB, key=key)
    assert found is not None and found["run_id"] == "r1"
    assert (
        rehearsal.latest(verb=land_cli.REHEARSAL_VERB, key={"folder": "/f", "batch": "c"}) is None
    )


# ---------------------------------------------------------------------------
# The review's round one
# ---------------------------------------------------------------------------


def test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live(
    native_library, silence
):
    """Occupancy is asked at the move, not in the plan, so the area holds the
    live folder's names too and the rehearsal refuses the file the live landing
    will refuse, rather than reporting it landed."""
    cfg, _root = native_library
    # A batch landed into again by its own name goes back to its filed folder
    # (U164), so an earlier landing makes it, and a name in it is then held.
    _land_first(cfg, silence)
    (_music(cfg) / "One.flac").write_bytes(b"left by an earlier landing")
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")

    code, rehearsed = _rehearse()

    assert code == int(ExitCode.OK), rehearsed
    facts = rehearsed["data"]["totals"]["rehearsal"]
    assert facts["landed"] == 1 and facts["refused"] == 1 and facts["added"] == 1
    assert (_music(cfg) / "One.flac").read_bytes() == b"left by an earlier landing"
    assert sorted(p.name for p in _music(cfg).iterdir()) == ["One.flac", "Zero.flac"]
    assert _staged_names(cfg) == ["One.flac", "Two.flac"]


def test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    real = landing.apply_native

    def straying(*args, **kwargs):
        landed = real(*args, **kwargs)
        (_staging(cfg) / "Stray.flac").write_bytes(b"x")
        return landed

    monkeypatch.setattr(landing, "apply_native", straying)

    code, refused = _rehearse()

    assert refused["cause"]["reason"] == "internal-error", refused
    assert "rehearsal changed" in refused["cause"]["message"]
    assert str(_staging(cfg)) in refused["cause"]["message"]
    assert all(Path(path).is_dir() for path in refused["cause"]["detail"]["kept"])


def test_a_copy_that_fails_its_integrity_check_is_refused_naming_the_area(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    monkeypatch.setattr(rb_writer, "integrity_ok", lambda *_args, **_kwargs: False)

    code, refused = _rehearse()

    assert refused["cause"]["reason"] == "snapshot-integrity-failed", refused
    assert "rehearsal area is kept at" in refused["cause"]["message"]


def test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    calls: list[object] = []

    def refusing(landed):
        calls.append(landed)
        raise land_cli.refuse("internal-error", "a landed row carries an analysis value")

    monkeypatch.setattr(native, "assert_rows_gridless", refusing)

    code, refused = _rehearse()

    assert calls, "the rehearsal never read its landed rows back"
    assert refused["cause"]["reason"] == "internal-error", refused
    assert "analysis value" in refused["cause"]["message"]
    assert "gridless" not in str(refused.get("data"))


def test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    def unidentified(_landed):
        raise land_cli.refuse("internal-error", "a landed row has no file id")

    monkeypatch.setattr(native, "assert_rows_identified", unidentified)

    code, refused = _rehearse()

    assert refused["cause"]["reason"] == "internal-error", refused
    assert "no file id" in refused["cause"]["message"]


def test_an_interrupted_rehearsal_is_a_cancel_that_names_its_area(
    native_library, silence, monkeypatch
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    def interrupted(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(native, "apply_rows", interrupted)

    code, refused = _rehearse()

    assert refused["cause"]["reason"] == "cancelled", refused
    area = refused["cause"]["detail"]["rehearsal_area"]
    assert all(Path(path).is_dir() and path in refused["cause"]["message"] for path in area)
    assert _staged_names(cfg) == ["One.flac"]
