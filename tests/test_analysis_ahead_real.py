"""U241: the shipped detector, on real audio, through the real verb, serial against pooled.

``tests/test_analysis_ahead.py`` proves the run ahead with a detector that
reads a file's name, because that suite runs without the analysis extra. This
file is the same claim with nothing faked on the measuring side: three
synthesized tracks, decoded and measured by ``detect.analyse_file`` under a
calibration, once in the driver and once in spawned workers that bind the
shipped detector from the settings the driver sends them. The two folders are
held to the same bytes.

It is also the only test in which a worker rebuilds the calibration and binds
the real detector for itself, which is the path every real run takes.

Skipped where the analysis extra is absent.
"""

from __future__ import annotations

import hashlib
import multiprocessing
import shutil
from pathlib import Path

import pytest

from cratekit.analysis import ahead, artifacts, energy, light, vocals
from cratekit.core import config, cores, jobs, pool, tags
from cratekit.core.exit_codes import ExitCode
from tests.cli_drive import drive
from tests.test_config import valid_data

np = pytest.importorskip("numpy")
pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")

GIB = 1024**3
RATE = 44100


def _track(seconds: float, tempo: float, tonic: int, seed: int):
    """A kick on the beat, a hat between, and a triad over a bass, in stereo."""
    rng = np.random.default_rng(seed)
    count = int(seconds * RATE)
    mix = np.zeros(count, dtype=np.float32)
    span = np.arange(int(0.2 * RATE)) / RATE
    kick = (np.sin(2 * np.pi * (50 + 100 * np.exp(-span * 40)) * span) * np.exp(-span * 14)).astype(
        np.float32
    )
    beat = 60.0 / tempo
    at = 0.0
    while at < seconds:
        start = int(at * RATE)
        stop = min(count, start + kick.size)
        mix[start:stop] += 0.8 * kick[: stop - start]
        off = int((at + beat / 2) * RATE)
        if off + 400 < count:
            mix[off : off + 400] += 0.2 * rng.standard_normal(400).astype(np.float32)
        at += beat
    t = np.arange(count) / RATE
    for step in (0, 4, 7):
        mix += (0.08 * np.sin(2 * np.pi * 261.63 * 2 ** ((tonic + step) / 12.0) * t)).astype(
            np.float32
        )
    mix += (0.15 * np.sin(2 * np.pi * 65.41 * 2 ** (tonic / 12.0) * t)).astype(np.float32)
    mix = 0.8 * mix / float(np.max(np.abs(mix)))
    return np.stack([mix, 0.97 * np.roll(mix, 11)], axis=1)


TRACKS = (("a", 14.0, 124.0, 0), ("b", 22.0, 128.0, 7), ("c", 18.0, 110.0, 4))


@pytest.fixture(scope="module")
def audio(tmp_path_factory) -> Path:
    folder = tmp_path_factory.mktemp("audio")
    for seed, (name, seconds, tempo, tonic) in enumerate(TRACKS):
        soundfile.write(
            str(folder / f"{name}.flac"), _track(seconds, tempo, tonic, seed), RATE, subtype="PCM_16"
        )
    return folder


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(autouse=True)
def shipped_seams(monkeypatch):
    """Nothing bound: the verb binds the shipped detector, here and in its workers."""
    monkeypatch.setattr(light, "_DETECT", None)
    monkeypatch.setattr(ahead, "_WORKER_BINDING", None)
    monkeypatch.setattr(ahead, "_SESSIONS", {})
    # No vocal model on the measuring side of this test: the loader is one that
    # answers "no model here", so both runs finalize alike with no vox tags.
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _no_model)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    yield
    for job_id in list(ahead._SESSIONS):
        ahead.close_session(job_id)


def _no_model():
    raise FileNotFoundError("no vocal model in this test")


def machine(monkeypatch, *, swap: int = 0) -> None:
    monkeypatch.setattr(cores, "usable_cores", lambda: 4)
    monkeypatch.setattr(pool, "available_bytes", lambda: 64 * GIB)
    monkeypatch.setattr(
        pool, "memory_pressure", lambda: pool.Pressure(swap_used_bytes=swap, used_percent=10.0)
    )


def what_is_on_disk(folder: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(folder.iterdir())
    }


def reports(cfg, envelope: dict) -> list[dict]:
    cleaned = []
    for report in artifacts.committed(cfg, envelope["data"]["job_id"]):
        report = dict(report)
        report["path"] = Path(report["path"]).name
        cleaned.append(report)
    return cleaned


def test_the_shipped_detector_in_workers_leaves_what_it_leaves_in_the_driver(
    cfg, audio, tmp_path, monkeypatch
):
    energy.save_calibration(
        cfg,
        energy.calibrate(
            [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
        ),
    )
    serial_folder = tmp_path / "serial"
    pooled_folder = tmp_path / "pooled"
    shutil.copytree(audio, serial_folder)
    shutil.copytree(audio, pooled_folder)

    machine(monkeypatch, swap=12 * GIB)
    code, serial = drive(["analyze", "run", str(serial_folder)])
    assert code == int(ExitCode.OK), serial
    assert serial["data"]["progress"]["analysis"]["checks"][0]["detail"].startswith(
        "one worker, this process: 12.0 GB of swap is in use"
    )

    machine(monkeypatch)
    code, pooled = drive(["analyze", "run", str(pooled_folder)])
    assert code == int(ExitCode.OK), pooled
    check = pooled["data"]["progress"]["analysis"]["checks"][0]
    assert check["detail"].startswith("2 workers measured key, tempo and energy ahead"), check
    assert check["detail"].endswith("3 of 3 waiting file(s) were read from them"), check
    assert multiprocessing.active_children() == []

    assert pooled["data"]["progress"]["analysis"]["by_status"] == {"analyzed": 3}
    assert reports(cfg, pooled) == reports(cfg, serial)
    assert what_is_on_disk(pooled_folder) == what_is_on_disk(serial_folder)
    # The heads are real ones: each carries a key, a level from the calibration
    # and a drift verdict, and no file was given a tempo tag by either run.
    for path in pooled_folder.iterdir():
        assert tags.read_tag(path, "initialkey")
        assert tags.read_energy_from_file(path) is not None
        assert tags.read_tag(path, "drift") in ("steady", "variable", "unknown")
    with jobs.open_store() as store:
        states = {
            str(item.state) for item in jobs.items(store, pooled["data"]["job_id"])
        }
    assert states == {"done"}
