"""R-744: a head is a measurement with a known error, and the error is measured.

Three things are pinned here. The bucketing, which is the vocabulary the
record and the verb's answer use. The key notation mapping, because rekordbox
stores whichever notation its display was set to and a comparison that knows
one spelling matches one library. And the measurement over a fixture copy,
driven through the script, so the four buckets a session reads off the live
library are the four buckets this suite has seen printed.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit.analysis import agreement, detect
from cratekit.core import config, preflight, rb_writer
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "head_agreement.py"


# ---------------------------------------------------------------------------
# The buckets
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("head", "reference", "bucket"),
    [
        (127, 127.00, agreement.EQUAL),
        (127, 126.50, agreement.EQUAL),
        (127, 127.49, agreement.EQUAL),
        (129, 127.00, agreement.OFF_ONE_TO_THREE),
        (112, 110.11, agreement.OFF_ONE_TO_THREE),
        (120, 123.00, agreement.OFF_ONE_TO_THREE),
        (124, 120.00, agreement.OTHER_LEVEL),
        (83, 166.00, agreement.HALF_OR_DOUBLE),
        (166, 83.13, agreement.HALF_OR_DOUBLE),
        (83, 126.00, agreement.OTHER_LEVEL),
        (123, 90.96, agreement.OTHER_LEVEL),
        (120, 0.0, agreement.OTHER_LEVEL),
    ],
)
def test_the_four_tempo_buckets(head, reference, bucket):
    assert agreement.tempo_bucket(head, reference) == bucket


def test_a_head_rounds_half_up_the_way_the_source_system_did():
    assert agreement.round_half_up(126.5) == 127
    assert agreement.round_half_up(126.49) == 126


@pytest.mark.parametrize(
    ("name", "camelot"),
    [
        ("8A", "08A"),
        ("08A", "08A"),
        ("12B", "12B"),
        ("Am", "08A"),
        ("F#m", "11A"),
        ("Gbm", "11A"),
        ("Dbm", "12A"),
        ("C#m", "12A"),
        ("Db", "03B"),
        ("C#", "03B"),
        ("Gb", "02B"),
        ("F#", "02B"),
        ("C", "08B"),
        ("Abm", "01A"),
        ("G#m", "01A"),
        ("Bb", "06B"),
        ("A#", "06B"),
        ("  8a ", "08A"),
        ("", None),
        (None, None),
        ("13A", None),
        ("0A", None),
        ("H", None),
        ("Amaj", None),
    ],
)
def test_either_key_notation_maps_to_one_padded_camelot(name, camelot):
    assert agreement.camelot_from_scale_name(name) == camelot


def test_every_classic_name_reaches_a_code_the_detector_can_emit():
    emitted = {agreement.pad_camelot(code) for code in detect._KEY_TO_CAMELOT.values()}
    for name in agreement._CLASSIC_TO_CAMELOT:
        assert agreement.camelot_from_scale_name(name) in emitted


# ---------------------------------------------------------------------------
# The comparison over rows
# ---------------------------------------------------------------------------


def _row_of(identifier, filename, hundredths, scale_name):
    return agreement.HeadRow(
        identifier=identifier,
        filename=filename,
        stored_hundredths=hundredths,
        scale_name=scale_name,
        folder_path=None,
    )


ROWS = [
    _row_of("1", "08A - 127 - equal.flac", 12700, "8A"),
    _row_of("2", "8A - 127 - equal by rounding.flac", 12650, "08A"),
    _row_of("3", "03B - 144 - off by four.flac", 14000, "2B"),
    _row_of("4", "04B - 117 - off by three.flac", 12000, "Db"),
    _row_of("5", "12A - 83 - other level.flac", 12600, "Dbm"),
    _row_of("6", "9A - 83 - half.flac", 16600, "Em"),
    _row_of("7", "no head at all.flac", 12000, "8A"),
    _row_of("8", "07A - 120 - never analysed.flac", 0, "7A"),
    _row_of("9", "07A - 120 - never analysed either.flac", None, None),
    _row_of("10", "10A - 128 - keyed by nobody.flac", 12800, None),
]


def test_the_comparison_buckets_every_row_and_counts_what_it_could_not_compare():
    found = agreement.compare(ROWS)
    assert found.files == 10
    assert found.no_head == 1
    assert found.unanalysed == 2
    assert dict(found.tempo) == {
        agreement.EQUAL: 3,
        agreement.OFF_ONE_TO_THREE: 1,
        agreement.HALF_OR_DOUBLE: 1,
        agreement.OTHER_LEVEL: 2,
    }
    assert found.within_one == 3
    assert dict(found.key) == {agreement.KEY_EQUAL: 4, agreement.KEY_DIFFERS: 2}
    assert found.unkeyed == 1
    assert [example[1:] for example in found.examples] == [(144, 140.0), (83, 126.0)]


def test_a_head_off_by_four_is_not_off_by_one_to_three():
    """Sitting 19's case, 144 against 140.00, is in the other bucket, not the
    near miss one: the near miss bucket is the estimator's bin width and four
    is outside it."""
    assert agreement.tempo_bucket(144, 140.0) == agreement.OTHER_LEVEL


def test_the_dictionary_form_names_every_bucket_even_when_empty():
    found = agreement.compare([])
    assert found.as_dict()["tempo"] == {bucket: 0 for bucket in agreement.TEMPO_BUCKETS}
    assert found.as_dict()["key"] == {agreement.KEY_EQUAL: 0, agreement.KEY_DIFFERS: 0}


def test_a_fractional_stored_tempo_is_rekordbox_own_analysis_and_a_whole_one_is_not():
    assert _row_of("a", "x", 12650, None).analysed_by_rekordbox
    assert not _row_of("b", "x", 12700, None).analysed_by_rekordbox
    assert not _row_of("c", "x", 0, None).analysed_by_rekordbox
    assert not _row_of("d", "x", None, None).analysed_by_rekordbox


def test_the_detector_head_is_the_stamped_head_and_a_terminal_is_none():
    assert agreement.head_from_detection({"camelot": "8A", "rate": 127}) == ("08A", 127)
    assert agreement.head_from_detection({"camelot": None, "rate": 127}) == (None, 127)
    assert agreement.head_from_detection({"terminal": "skipped-undecodable"}) is None
    assert agreement.head_from_detection(None) is None


def test_reanalysis_samples_rekordbox_own_rows_with_a_file_and_buckets_the_detector(
    tmp_path, monkeypatch
):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    # The suite's conftest points the library root elsewhere through the
    # environment, and the environment wins over the mapping.
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(valid_data(root))
    on_disk = root / "Music" / "own.flac"
    on_disk.write_bytes(b"")
    rows = [
        agreement.HeadRow("1", "01A - 100 - own.flac", 12650, "8A", str(on_disk)),
        agreement.HeadRow("2", "01A - 100 - imported.flac", 12700, "8A", str(on_disk)),
        agreement.HeadRow("3", "01A - 100 - gone.flac", 12650, "8A", str(root / "Music" / "gone.flac")),
        agreement.HeadRow("4", "01A - 100 - streamed.flac", 12650, "8A", "soundcloud:tracks:1"),
    ]
    seen = []

    def detector(path):
        seen.append(path)
        return {"camelot": "8A", "rate": 127}

    found = agreement.reanalyse(rows, cfg, detector=detector, limit=10)
    assert seen == [on_disk]
    assert found.files == 1
    assert dict(found.tempo) == {agreement.EQUAL: 1}
    assert dict(found.key) == {agreement.KEY_EQUAL: 1}


def test_the_sample_stops_resolving_rows_once_it_is_full(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    cfg = config.from_dict(valid_data(root))
    on_disk = root / "Music" / "own.flac"
    on_disk.write_bytes(b"")
    rows = [
        agreement.HeadRow(str(n), "01A - 100 - own.flac", 12650, "8A", str(on_disk))
        for n in range(1, 41)
    ]
    resolved = []
    real = agreement.local_path

    def counted(row, **kwargs):
        resolved.append(row.identifier)
        return real(row, **kwargs)

    monkeypatch.setattr(agreement, "local_path", counted)
    chosen = agreement.sample_for_reanalysis(rows, cfg, limit=3, step=1)
    assert [row.identifier for row, _path in chosen] == ["1", "2", "3"]
    assert resolved == ["1", "2", "3"]
    resolved.clear()
    chosen = agreement.sample_for_reanalysis(rows, cfg, limit=3, step=4)
    assert [row.identifier for row, _path in chosen] == ["1", "5", "9"]
    assert len(resolved) == 9
    with pytest.raises(ValueError):
        agreement.sample_for_reanalysis(rows, cfg, limit=3, step=0)


def test_the_script_refuses_a_step_below_one_before_it_reads_anything():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--analyse", "3", "--step", "0"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "--step must be one or more" in completed.stderr


# ---------------------------------------------------------------------------
# The measurement over a fixture copy, through the script
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What a temporary library cannot speak for, as the cutover suite patches it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


FIXTURE_ROWS = (
    # identifier, filename, stored hundredths, key name
    ("11", "08A - 127 - equal.flac", 12700, "8A"),
    ("12", "8A - 127 - rounds.flac", 12651, "Am"),
    ("13", "03B - 144 - four off.flac", 14000, "02B"),
    ("14", "04B - 117 - three off.flac", 12000, "Db"),
    ("15", "12A - 83 - level.flac", 12600, "12A"),
    ("16", "09A - 83 - half.flac", 16600, "9A"),
    ("17", "no head.flac", 12000, "8A"),
    ("18", "07A - 120 - unanalysed.flac", 0, "7A"),
)


def _fixture_library(tmp_path, monkeypatch) -> config.Config:
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = valid_data(
        root,
        profile={"name": "full"},
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    cfg = config.from_dict(data)
    config.save(cfg)
    config.reset_cache()
    _build_disposable_database(Path(cfg.library.db_path), with_tag_category=False)
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        names = sorted({name for *_rest, name in FIXTURE_ROWS})
        key_ids = {}
        for index, name in enumerate(names, start=1):
            key_ids[name] = str(500 + index)
            db_session.add(_row(tables.DjmdKey, ID=key_ids[name], ScaleName=name, Seq=index))
        for identifier, filename, hundredths, name in FIXTURE_ROWS:
            db_session.add(
                _row(
                    tables.DjmdContent,
                    ID=identifier,
                    Title=filename,
                    FileNameL=filename,
                    FolderPath=str(root / "Music" / filename),
                    BPM=hundredths,
                    KeyID=key_ids[name],
                    Length=300,
                    FileType=5,
                    rb_local_deleted=0,
                )
            )
        # A deleted row is not a row.
        db_session.add(
            _row(
                tables.DjmdContent,
                ID="19",
                Title="gone",
                FileNameL="01A - 100 - gone.flac",
                BPM=10000,
                KeyID=key_ids["8A"],
                rb_local_deleted=1,
            )
        )
        db_session.commit()
    engine.dispose()
    return cfg


def test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture(tmp_path, monkeypatch):
    cfg = _fixture_library(tmp_path, monkeypatch)
    opened = []
    real = rb_writer.read_only_copy

    def watched(source, **kwargs):
        opened.append(Path(source))
        return real(source, **kwargs)

    monkeypatch.setattr(rb_writer, "read_only_copy", watched)
    found = agreement.measure(cfg)
    assert opened == [Path(cfg.library.db_path)]
    # The two rows the fixture builder seeds carry no filename and count as headless.
    assert found.files == 10
    assert found.no_head == 3
    assert found.unanalysed == 1
    assert dict(found.tempo) == {
        agreement.EQUAL: 2,
        agreement.OFF_ONE_TO_THREE: 1,
        agreement.HALF_OR_DOUBLE: 1,
        agreement.OTHER_LEVEL: 2,
    }
    assert dict(found.key) == {agreement.KEY_EQUAL: 4, agreement.KEY_DIFFERS: 2}


def test_the_live_path_is_never_handed_to_the_binding(tmp_path, monkeypatch):
    cfg = _fixture_library(tmp_path, monkeypatch)
    handed = []
    real = rb_writer.open_db

    def watched(target, *args, **kwargs):
        handed.append(Path(target))
        return real(target, *args, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", watched)
    agreement.measure(cfg)
    assert handed and all(path != Path(cfg.library.db_path) for path in handed)


def test_the_measurement_refuses_while_rekordbox_is_running(tmp_path, monkeypatch):
    cfg = _fixture_library(tmp_path, monkeypatch)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    with pytest.raises(Exception) as caught:
        agreement.measure(cfg)
    assert "rekordbox" in str(caught.value).lower()


def test_the_script_prints_the_four_buckets_over_a_fixture_copy(tmp_path, monkeypatch):
    cfg = _fixture_library(tmp_path, monkeypatch)
    # Copy the fixture so the script reads a database that is not the configured
    # one, which is the shape a session uses on a copy of the live library.
    copy = tmp_path / "copy.db"
    copy.write_bytes(Path(cfg.library.db_path).read_bytes())
    env = {
        **os.environ,
        config.ENV_LIBRARY_ROOT: str(cfg.library.root),
        config.ENV_CONFIG_DIR: str(config.config_dir()),
        config.ENV_STATE_DIR: str(config.installation_state_dir()),
    }
    sitecustomize = tmp_path / "site"
    sitecustomize.mkdir()
    (sitecustomize / "sitecustomize.py").write_text(
        "from cratekit.core import rb_writer, preflight\n"
        "from pyrekordbox.db6 import database as binding\n"
        "rb_writer.rekordbox_running = lambda: False\n"
        "rb_writer.rekordbox_agent_running = lambda: False\n"
        "binding.get_rekordbox_pid = lambda *a, **k: 0\n"
        "rb_writer.read_rekordbox_settings = lambda *a, **k: {rb_writer.LIBRARY_SYNC_SETTING: 0}\n"
        f"rb_writer.read_installed_app_version = lambda **_: {RECORDED_APP_VERSION!r}\n"
        "_real = rb_writer.integrity_ok\n"
        "rb_writer.integrity_ok = lambda target, **k: _real(target, unlock=False)\n"
        "preflight.local_mount_points = lambda: ()\n",
        encoding="utf-8",
    )
    env["PYTHONPATH"] = str(sitecustomize)
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--database", str(copy)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    out = completed.stdout
    for line in (
        "tempo equal: 2",
        "tempo off one to three: 1",
        "tempo half or double: 1",
        "tempo other level: 2",
        "key equal: 4",
        "key differs: 2",
    ):
        assert line in out, out
    assert "heads on disk against rekordbox own analysis" in out


# ---------------------------------------------------------------------------
# The recorded rate the verb answers with
# ---------------------------------------------------------------------------


def test_the_recorded_agreement_is_a_fresh_copy_with_every_bucket_named():
    first = detect.head_agreement()
    second = detect.head_agreement()
    assert first == second and first is not second
    first["tempo"]["equal"] = 0
    assert detect.head_agreement()["tempo"]["equal"] != 0
    assert first["window"] == {
        "floor": config.DEFAULT_TEMPO_FLOOR,
        "ceiling": config.DEFAULT_TEMPO_CEILING,
    }


def test_the_recorded_shape_is_the_shape_the_measurement_prints():
    """Re-recording is a copy: every key the measurement's dictionary form
    carries is in the record at the same level, so a session pasting the
    script's JSON cannot drop within_one or nest it."""
    printed = agreement.compare(ROWS).as_dict()
    recorded = detect.head_agreement()
    for name in ("files", "tempo", "within_one", "key"):
        assert name in recorded, name
    assert set(recorded["tempo"]) == set(printed["tempo"]) == set(agreement.TEMPO_BUCKETS)
    assert set(recorded["key"]) == set(printed["key"])
    assert isinstance(recorded["within_one"], int)


def test_the_recorded_buckets_sum_to_the_files_measured():
    recorded = detect.head_agreement()
    tempo = recorded["tempo"]
    assert sum(tempo[bucket] for bucket in agreement.TEMPO_BUCKETS) == recorded["files"]
    assert recorded["within_one"] >= tempo["equal"]
    assert sum(recorded["key"].values()) == recorded["files"]


def test_the_record_says_whether_it_applies_to_the_bound_window():
    measured = (config.DEFAULT_TEMPO_FLOOR, config.DEFAULT_TEMPO_CEILING)
    assert detect.head_agreement()["applies_to_window"] is True
    assert detect.head_agreement(window=measured)["applies_to_window"] is True
    raised = detect.head_agreement(window=(140, 280))
    assert raised["applies_to_window"] is False
    # The numbers stay, so the reader sees what was measured, not an absence.
    assert raised["tempo"] == detect.head_agreement()["tempo"]


def test_the_run_answer_carries_the_bound_window_to_the_record():
    source = (REPO_ROOT / "src" / "cratekit" / "analysis" / "cli.py").read_text(encoding="utf-8")
    assert "window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling)" in source


def test_the_run_answer_carries_the_recorded_agreement():
    source = (REPO_ROOT / "src" / "cratekit" / "analysis" / "cli.py").read_text(encoding="utf-8")
    assert 'summary["head_agreement"] = detect.head_agreement(' in source


# ---------------------------------------------------------------------------
# The window is a named setting, refused when empty
# ---------------------------------------------------------------------------


def test_the_window_defaults_are_the_source_system_window():
    assert (config.DEFAULT_TEMPO_FLOOR, config.DEFAULT_TEMPO_CEILING) == (80, 160)
    cfg = config.AnalysisConfig()
    assert (cfg.tempo_floor, cfg.tempo_ceiling) == (80, 160)


@pytest.mark.parametrize(
    ("analysis", "fragment"),
    [
        ({"tempo_floor": 160, "tempo_ceiling": 160}, "must be below"),
        ({"tempo_floor": 170}, "must be below"),
        ({"tempo_ceiling": 70}, "must be below"),
        ({"tempo_floor": 0}, "tempo_floor must be a whole number"),
        ({"tempo_ceiling": "fast"}, "tempo_ceiling must be a whole number"),
        ({"tempo_floor": True}, "tempo_floor must be a whole number"),
        ({"tempo_floor": 80.5}, "tempo_floor must be a whole number"),
    ],
)
def test_an_empty_or_ill_typed_window_is_refused_at_load(tmp_path, analysis, fragment):
    data = valid_data(tmp_path / "library", analysis=analysis)
    problems = config.validate(data)
    assert any(fragment in problem for problem in problems), problems


def test_a_raised_window_loads_and_reaches_the_detector_binding(tmp_path, monkeypatch):
    from cratekit.analysis import cli as analysis_cli
    from cratekit.analysis import energy, light

    data = valid_data(tmp_path / "library", analysis={"tempo_floor": 100, "tempo_ceiling": 200})
    assert config.validate(data) == []
    cfg = config.from_dict(data)
    assert (cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling) == (100, 200)
    monkeypatch.setattr(energy, "load_calibration", lambda cfg_: None)
    monkeypatch.setattr(analysis_cli, "_fake_detect_bound", lambda: False)
    analysis_cli._bind_defaults(cfg)
    assert light._DETECT.keywords["tempo_window"] == (100, 200)
