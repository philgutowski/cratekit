"""The harness is itself verified: the timing shape, the calibration, both volumes.

The timing runner is driven by a scripted clock. The volume tests mount real
disk images, since a filesystem double proves nothing, and fail rather than
skip without hdiutil, as a skipped hardware proof reads as a pass.
"""

from __future__ import annotations

import errno
import json
from pathlib import Path

import pytest

from tests._hardware import (
    CALIBRATION_SCHEMA,
    FAT32_MIN_MB,
    TimingTable,
    _content_manifest,
    _detach,
    _run,
    calibrate,
    fat_volume,
    filesystem_kind,
    hdiutil_available,
    load_calibration,
    mount_flags,
    read_only_volume,
    threshold_seconds,
    time_repeated,
    write_calibration,
)


def _require_hdiutil() -> None:
    if not hdiutil_available():
        pytest.fail(
            "hdiutil is required to prove the volume fixtures against real mounts, and it is "
            "missing here. These fixtures target macOS, where hdiutil ships with the system. "
            "This fails rather than skips, since a skipped hardware proof reads as a pass."
        )


class ScriptedClock:
    """A perf_counter double replaying declared durations, two reads per run."""

    def __init__(self, durations: list[float]) -> None:
        readings: list[float] = []
        now = 0.0
        for duration in durations:
            readings.append(now)
            now += duration
            readings.append(now)
        self._readings = iter(readings)

    def __call__(self) -> float:
        return next(self._readings)

    def assert_exhausted(self) -> None:
        """Fail if the runner read fewer instants than the script provided."""
        leftover = list(self._readings)
        assert not leftover, f"{len(leftover)} scripted clock readings were never consumed"


# Timing arithmetic, no hardware and no sleeping.


def test_pass_rate_counts_only_runs_under_threshold() -> None:
    # Binary exact fractions, so the running sum picks up no float error.
    clock = ScriptedClock([0.25, 0.5, 0.75, 1.0, 1.25])
    table = time_repeated(lambda: None, repeats=5, threshold_seconds=0.75, clock=clock)
    assert table.repeats == 5
    assert table.passes == 3
    assert table.pass_rate == pytest.approx(0.6)
    assert table.median_seconds == pytest.approx(0.75)
    assert table.worst_seconds == pytest.approx(1.25)
    clock.assert_exhausted()


def test_row_reports_count_rate_median_and_worst_together() -> None:
    clock = ScriptedClock([0.25, 1.0])
    table = time_repeated(lambda: None, repeats=2, threshold_seconds=0.5, clock=clock)
    row = table.row()
    assert "1/2" in row
    assert "pass rate 0.50" in row
    assert "median" in row and "worst" in row


@pytest.mark.parametrize(
    ("repeats", "threshold", "said"),
    [(1, 1.0, "repeat count"), (2, 0.0, "positive")],
    ids=["single-run", "nonpositive-threshold"],
)
def test_a_timing_of_the_wrong_shape_is_refused(repeats, threshold, said) -> None:
    with pytest.raises(ValueError, match=said):
        time_repeated(lambda: None, repeats=repeats, threshold_seconds=threshold)


def test_a_measurement_is_a_record_not_a_workspace() -> None:
    clock = ScriptedClock([0.1, 0.2])
    table = time_repeated(lambda: None, repeats=2, threshold_seconds=1.0, clock=clock)
    with pytest.raises(AttributeError):
        table.passes = 99  # type: ignore[misc]


def test_timing_table_keeps_every_duration() -> None:
    clock = ScriptedClock([0.1, 0.2, 0.3])
    table = time_repeated(lambda: None, repeats=3, threshold_seconds=1.0, clock=clock)
    assert table.durations == pytest.approx((0.1, 0.2, 0.3))
    assert isinstance(table, TimingTable)
    clock.assert_exhausted()


def test_a_record_whose_count_disagrees_with_its_evidence_is_refused() -> None:
    with pytest.raises(ValueError, match="exactly the runs it measured"):
        TimingTable(repeats=2, threshold_seconds=1.0, durations=(0.1, 0.2, 0.3))
    with pytest.raises(ValueError, match="exactly the runs it measured"):
        TimingTable(repeats=0, threshold_seconds=1.0, durations=())


# Calibration: stored whole, loaded guarded, thresholds are multiples.


def test_calibration_round_trips_and_threshold_is_a_multiple(tmp_path: Path) -> None:
    payload = calibrate(repeats=2)
    # The spread is pinned, not measured: a live spread crosses the quiet machine
    # refusal under load, which test_an_unquiet_calibration_refuses_to_write covers.
    payload["relative_spread"] = 0.01
    stored = tmp_path / "cal.json"
    write_calibration(payload, stored)
    cal = load_calibration(stored)
    assert cal.median_seconds > 0
    assert cal.repeats == 2
    assert cal.relative_spread == pytest.approx(0.01)
    assert threshold_seconds(3.0, cal) == pytest.approx(3.0 * cal.median_seconds)


def test_unknown_calibration_schema_is_refused(tmp_path: Path) -> None:
    stored = tmp_path / "cal.json"
    stored.write_text(json.dumps({"schema": CALIBRATION_SCHEMA + 1}))
    with pytest.raises(ValueError, match="calibrate_timing"):
        load_calibration(stored)


def test_nonpositive_multiplier_is_refused() -> None:
    with pytest.raises(ValueError, match="positive"):
        threshold_seconds(0.0)


def test_a_calibration_from_another_machine_is_refused(tmp_path: Path) -> None:
    payload = calibrate(repeats=2)
    payload["cpu_count"] = int(payload["cpu_count"]) + 1
    # Pinned for the reason the round trip test above gives.
    payload["relative_spread"] = 0.01
    stored = tmp_path / "cal.json"
    write_calibration(payload, stored)
    with pytest.raises(ValueError, match="different machine"):
        load_calibration(stored)


def test_an_unquiet_calibration_refuses_to_write(tmp_path: Path) -> None:
    payload = calibrate(repeats=2)
    payload["relative_spread"] = 0.5
    stored = tmp_path / "cal.json"
    with pytest.raises(ValueError, match="not quiet"):
        write_calibration(payload, stored)
    assert not stored.exists()
    write_calibration(payload, stored, force=True)
    assert stored.exists()


def test_committed_calibration_loads() -> None:
    """The committed calibration's shape, never its magnitude, which is the machine's."""
    cal = load_calibration()
    assert cal.median_seconds > 0
    assert cal.repeats >= 2
    assert cal.captured


# Volumes: real images, real mounts, real teardown.


@pytest.mark.parametrize(
    ("asked", "said"),
    [({"size_mb": FAT32_MIN_MB - 1}, "newfs_msdos"), ({"label": "lowercase"}, "11 uppercase")],
    ids=["a-size-fat32-cannot-hold", "a-label-off-the-rules"],
)
def test_fat_volume_refuses_what_fat32_cannot_take(asked, said) -> None:
    with pytest.raises(ValueError, match=said):
        with fat_volume(**asked):
            raise AssertionError("the fixture must refuse before it yields")


def test_fat_volume_is_really_fat_and_is_torn_down() -> None:
    _require_hdiutil()
    with fat_volume() as mount:
        assert filesystem_kind(mount) == "msdos"
        (mount / "seed.txt").write_text("x")
        assert (mount / "SEED.TXT").read_text() == "x"
        kept = mount
    assert not kept.exists()


def test_read_only_volume_serves_content_and_refuses_writes() -> None:
    _require_hdiutil()

    def populate(root: Path) -> None:
        (root / "seed.txt").write_text("populated")

    with read_only_volume(populate) as mount:
        assert (mount / "seed.txt").read_text() == "populated"
        assert "read-only" in mount_flags(mount)
        with pytest.raises(OSError) as caught:
            (mount / "blocked.txt").write_text("x")
        assert caught.value.errno == errno.EROFS
        kept = mount
    assert not kept.exists()


def test_teardown_runs_when_the_body_raises() -> None:
    _require_hdiutil()

    class Boom(Exception):
        pass

    seen: list[Path] = []
    with pytest.raises(Boom):
        with fat_volume() as mount:
            seen.append(mount)
            raise Boom()
    assert seen and not seen[0].exists()


def test_content_manifest_pins_content_and_ignores_platform_noise(tmp_path: Path) -> None:
    root = tmp_path / "vol"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").write_text("one")
    (root / "sub" / "b.txt").write_text("two")
    (root / ".fseventsd").mkdir()
    (root / ".fseventsd" / "log").write_text("indexer droppings")
    before = _content_manifest(root)
    assert set(before) == {"a.txt", "sub/b.txt"}
    (root / "a.txt").write_text("changed")
    after = _content_manifest(root)
    assert before["sub/b.txt"] == after["sub/b.txt"]
    assert before["a.txt"] != after["a.txt"]


def test_mount_lookup_is_exact_never_a_prefix(tmp_path: Path) -> None:
    """The mount table answer for NAME must not come from a sibling ``NAME (1)``,
    as macOS mounts a second PIONEER stick."""
    _require_hdiutil()
    image = tmp_path / "probe.dmg"
    mountpoint = tmp_path / "PROBE (1)"
    mountpoint.mkdir()
    _run([
        "hdiutil", "create", "-size", "64m", "-fs", "MS-DOS FAT32", "-volname", "CKPROBE", "-quiet",
        str(image),
    ])
    _run(["hdiutil", "attach", str(image), "-mountpoint", str(mountpoint), "-nobrowse", "-quiet"])
    try:
        assert filesystem_kind(mountpoint) == "msdos"
        with pytest.raises(LookupError):
            filesystem_kind(tmp_path / "PROBE")
    finally:
        _detach(mountpoint)
