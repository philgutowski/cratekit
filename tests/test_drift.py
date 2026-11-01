"""U157: the drift verdict, its cut, and the two file tags the analysis writes.

Everything here runs without the analysis extra: the verdict words and the
comparison in ``core.drift``, the cut in configuration, the finalize writing
the two tags from whatever the detector answered, and the no grid rule over
the new fields. The measurement itself, which needs librosa, is
``tests/test_analysis_drift.py``.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import math
import shutil
from pathlib import Path

import pytest

from cratekit.analysis import artifacts, light, vocals
from cratekit.analysis import cli as analysis_cli
from cratekit.core import config, drift, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_analysis import _FakeModel
from tests.test_analysis_workers import analysis_job, resume_argv, voiced
from tests.test_analysis_workers import cfg as cfg  # noqa: PLC0414
from tests.test_analysis_workers import folder as folder  # noqa: PLC0414
from tests.test_analysis_workers import unbound as unbound  # noqa: PLC0414
from tests.test_config import valid_data
from tests.test_no_beatgrid_ever import FORBIDDEN_TAG_KEYS

# ---------------------------------------------------------------------------
# The verdict against the cut
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("measured", "expected"),
    [
        (4.4, drift.VARIABLE),
        (1.5, drift.VARIABLE),
        (1.49, drift.STEADY),
        (0.0, drift.STEADY),
        (None, drift.UNKNOWN),
        (math.nan, drift.UNKNOWN),
    ],
    ids=["moving", "at-the-cut", "just-below", "still", "unmeasured", "nan"],
)
def test_a_drift_at_or_above_the_cut_is_variable_and_no_measurement_is_unknown(
    measured, expected
):
    assert drift.verdict(measured, 1.5) == expected


@pytest.mark.parametrize(
    ("score", "verdict", "expected"),
    [
        ("4.4", drift.VARIABLE, (4.4, drift.VARIABLE)),
        ("4.4", drift.STEADY, (4.4, drift.VARIABLE)),
        ("0.3", drift.VARIABLE, (0.3, drift.STEADY)),
        (None, drift.UNKNOWN, (None, drift.UNKNOWN)),
        (None, " unknown ", (None, drift.UNKNOWN)),
        (None, None, (None, drift.UNSCORED)),
        (None, drift.VARIABLE, (None, drift.UNSCORED)),
        ("lots", drift.VARIABLE, (None, drift.UNSCORED)),
        ("-1.0", drift.VARIABLE, (None, drift.UNSCORED)),
        ("inf", drift.VARIABLE, (None, drift.UNSCORED)),
    ],
    ids=[
        "score-over-cut",
        "score-wins-over-a-stale-verdict",
        "score-under-cut",
        "unknown",
        "unknown-padded",
        "nothing",
        "verdict-without-score",
        "not-a-number",
        "negative",
        "infinite",
    ],
)
def test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown(
    score, verdict, expected
):
    assert drift.reading(score, verdict, 1.5) == expected


def test_a_drift_is_spelled_to_one_decimal_and_read_back_as_written():
    assert drift.shown(4.3667) == "4.4"
    assert drift.shown(0.0) == "0.0"
    assert drift.parse(drift.shown(12.25)) == 12.2


def test_the_verdict_words_are_the_three_the_tag_carries():
    assert drift.VERDICTS == ("steady", "variable", "unknown")
    assert drift.UNSCORED not in drift.VERDICTS, "unscored is a landing's word, never a tag's"


def test_the_normal_settings_are_the_visit_standard_the_sync_stop_prints():
    from cratekit.cli import tail

    assert drift.NORMAL_SETTINGS in tail.REKORDBOX_STEPS[0]
    assert drift.DYNAMIC_SETTINGS in tail.REKORDBOX_STEPS[0]
    assert "Analysis Mode Dynamic" in drift.DYNAMIC_SETTINGS


# ---------------------------------------------------------------------------
# The cut is configuration
# ---------------------------------------------------------------------------


def test_the_cut_defaults_to_the_shipped_value():
    assert config.DEFAULT_DRIFT_CUT == 1.5
    assert config.AnalysisConfig().drift_cut == config.DEFAULT_DRIFT_CUT


@pytest.mark.parametrize(
    "value", [0, 0.0, -1.0, True, "high", math.nan, math.inf, 100.5], ids=repr
)
def test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load(tmp_path, value):
    data = valid_data(tmp_path / "library", analysis={"drift_cut": value})
    problems = config.validate(data)
    assert any("analysis.drift_cut must be a percent" in one for one in problems), problems


def test_a_whole_number_cut_loads_and_reaches_the_detector_binding(tmp_path, monkeypatch):
    from cratekit.analysis import energy

    data = valid_data(tmp_path / "library", analysis={"drift_cut": 3})
    assert config.validate(data) == []
    loaded = config.from_dict(data)
    assert loaded.analysis.drift_cut == 3.0 and isinstance(loaded.analysis.drift_cut, float)
    monkeypatch.setattr(energy, "load_calibration", lambda cfg_: None)
    monkeypatch.setattr(analysis_cli, "_fake_detect_bound", lambda: False)
    monkeypatch.setattr(light, "_DETECT", None)
    analysis_cli._bind_defaults(loaded)
    assert light._DETECT.keywords["drift_cut"] == 3.0


# ---------------------------------------------------------------------------
# The finalize writes what the detector answered, and only that
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


def _detector(**drift_fields):
    def detect_(path: Path):
        return {
            "path": path,
            "camelot": "8A",
            "rate": 124,
            "energy": 6,
            "energy_status": "calibrated",
            **drift_fields,
        }

    return detect_


def _analysed(folder: Path, silence: Path, monkeypatch, detect_) -> tuple[Path, dict]:
    shutil.copy2(silence, folder / "a.flac")
    monkeypatch.setattr(light, "_DETECT", detect_)
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", voiced())
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    (report,) = artifacts.committed(config.load(), job.job_id)
    return folder / "08A - 124 - a.flac", report


def test_a_measured_drift_is_written_as_its_level_and_verdict(cfg, folder, silence, monkeypatch):
    done, report = _analysed(
        folder, silence, monkeypatch, _detector(drift=4.3667, drift_verdict=drift.VARIABLE)
    )
    assert tags.read_tags(done, ("driftlevel", "drift")) == {
        "driftlevel": "4.4",
        "drift": drift.VARIABLE,
    }
    assert (report["drift"], report["drift_verdict"]) == (4.3667, drift.VARIABLE)


def test_a_track_too_thin_to_judge_carries_unknown_and_no_level(cfg, folder, silence, monkeypatch):
    done, report = _analysed(
        folder, silence, monkeypatch, _detector(drift=None, drift_verdict=drift.UNKNOWN)
    )
    assert tags.read_tags(done, ("driftlevel", "drift")) == {
        "driftlevel": None,
        "drift": drift.UNKNOWN,
    }
    assert report["drift_verdict"] == drift.UNKNOWN


def test_a_detector_that_measures_no_drift_writes_neither_tag(cfg, folder, silence, monkeypatch):
    """The batch fakes and any detector older than U157: no level and no
    verdict, which a landing reads as unscored rather than as steady."""
    done, report = _analysed(folder, silence, monkeypatch, _detector())
    assert tags.read_tags(done, ("driftlevel", "drift")) == {"driftlevel": None, "drift": None}
    assert report["drift"] is None and report["drift_verdict"] is None


# ---------------------------------------------------------------------------
# Neither field is a tempo (R17)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("field", ["driftlevel", "drift"])
def test_the_drift_fields_carry_no_tempo_key_in_any_container(field):
    spec = tags.FIELDS[field]
    keys = {spec.vorbis, spec.id3, spec.mp4, spec.id3.removeprefix("TXXX:")}
    keys |= {spec.mp4.rsplit(":", 1)[-1]}
    assert not keys & FORBIDDEN_TAG_KEYS, keys
    assert not any("bpm" in key.lower() or "tempo" in key.lower() for key in keys), keys


@pytest.mark.parametrize("suffix", [".flac", ".mp3", ".m4a", ".aiff"])
def test_a_file_carrying_a_drift_carries_no_tempo_frame(tmp_path, suffix):
    """Read raw, below the tag table, so a writer that slipped a tempo frame
    in beside the drift would show here whatever the table says."""
    import mutagen

    path = synth_container(tmp_path, suffix)
    assert tags.write_tags(path, {"driftlevel": "4.4", "drift": drift.VARIABLE})
    raw = mutagen.File(str(path))
    held = {str(key) for key in (raw.tags.keys() if raw.tags is not None else ())}
    assert held, "the fixture wrote nothing"
    lowered = {key.lower() for key in held}
    assert not any(
        forbidden.lower() in key for forbidden in FORBIDDEN_TAG_KEYS for key in lowered
    ), held
