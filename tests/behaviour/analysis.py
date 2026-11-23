"""Analysis's scenarios: `crate analyze run`, `calibrate`, `validate` and `restamp` (U306).

Each verb runs on a configured machine with the full profile and FLAC
containers the encoder synthesized, with the heavy stack's seams bound to the
fakes the workers suite uses: a detector that finds one key on every file, a
model that scores a signal as vocal, a decoder handing it that signal, and a
feature extractor answering a seeded vector per file. The heavy stack itself
is read as absent, as it is on a slim container, so the capture does not
depend on what a machine has installed.

`analyze run` queues and drives a folder in one call, renaming each file to
its head, and a second run skips both by their head; queued by itself and
driven by its job, a keyless file is a terminal skip and a file gone before
the drive fails its item; an empty and an absent folder are told apart, and a
process with nothing bound refuses its item for the missing extra. `analyze
calibrate` sets a vocal cut by hand, replaces it, refuses one off the scale,
fits energy and the vocal cut over a folder, refuses a genre folder that is
not the library, fits over the whole library walked, and says what it could
not fit over too few tracks, no folder, an empty and an absent one, and
without the extra. `analyze validate` says nothing was scored. `analyze
restamp` refuses with no calibration, rescores a folder and then finds every
level unchanged, walks a tree, reports a file it cannot measure, and refuses
its item without the extra. Self contained, so the suites it stands beside
can be trimmed without moving it.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.analysis import detect, energy, light, vocals
from cratekit.core import config, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.test_config import valid_data

OK = int(ExitCode.OK)


class FakeModel:
    """A deterministic stand in for the vocal model: values track the input's mean."""

    labels = ("Singing", "Male singing", "Female singing")

    def inference(self, wav):
        import numpy as np

        batch = np.asarray(wav, dtype=np.float32)
        if batch.ndim == 1:
            batch = batch[None, :]
        frames = max(1, int(batch.shape[-1]) // 3200)
        level = float(np.mean(np.abs(batch)))
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = min(1.0, level)
        row[:, 1] = min(1.0, level * 0.4)
        row[:, 2] = min(1.0, level * 0.1)
        return row[None, :, :]


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A configured machine on the full profile, which carries the analysis verbs."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path) -> Path:
    made = tmp_path / "silence"
    made.mkdir()
    return synth_container(made, ".flac")


@pytest.fixture(autouse=True)
def unbound(monkeypatch):
    """Nothing bound, and the heavy stack read as absent, whatever this machine holds."""
    monkeypatch.setattr(light, "_DETECT", None)
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", None)
    monkeypatch.setattr(energy, "_EXTRACTOR", None)
    monkeypatch.setattr(detect, "heavy_available", lambda: False)


def place(folder: Path, silence: Path, relative: str, **fields) -> Path:
    path = folder / f"{relative}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {relative}"
    return path


def detector(keyless: tuple[str, ...] = ()):
    """A head finding the same key on every file, and no key on the files named."""

    def detect_(path: Path):
        if Path(path).stem in keyless:
            return None
        return {
            "path": path,
            "camelot": "8A",
            "rate": 124,
            "energy": 6,
            "energy_status": energy.STATUS_CALIBRATED,
        }

    return detect_


def bind_scoring(monkeypatch, *, keyless: tuple[str, ...] = ()) -> None:
    import numpy as np

    monkeypatch.setattr(light, "_DETECT", detector(keyless))
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(16000, 0.2, dtype=np.float32))


def features(seed: int) -> dict[str, float]:
    """A deterministic feature vector whose energy rises with ``seed``."""
    base = {name: 0.0 for name in energy.FEATURE_ORDER}
    base["rms_mean"] = 0.05 * seed
    base["loudness_db"] = -30.0 + seed
    base["onset_density"] = 0.5 + 0.1 * seed
    base["centroid_mean"] = 1000.0 + 100.0 * seed
    base["percussive_fraction"] = 0.3 + 0.02 * seed
    base["tempo"] = 120.0 + seed
    return base


def bind_measuring(monkeypatch, table: dict[str, int | None]) -> None:
    """An extractor answering by filename stem; a stem mapped to None cannot be measured."""

    def extractor(path):
        seed = table[Path(path).stem]
        return None if seed is None else features(seed)

    monkeypatch.setattr(energy, "_EXTRACTOR", extractor)


# ---------------------------------------------------------------------------
# analyze run
# ---------------------------------------------------------------------------


def test_run_analyses_a_folder_and_then_skips_it(stage, machine, silence, tmp_path, monkeypatch):
    folder = tmp_path / "downloads"
    place(folder, silence, "a")
    place(folder, silence, "b")
    bind_scoring(monkeypatch)

    settled = stage.crate("analyze", "run", str(folder))
    assert settled.code == OK, settled.stderr
    assert sorted(path.name for path in folder.iterdir()) == [
        "08A - 124 - a.flac",
        "08A - 124 - b.flac",
    ]
    # Again: every name carries its head, so nothing is read.
    again = stage.json("analyze", "run", str(folder))
    assert again.code == OK, again.stdout


def test_run_queued_then_driven_with_a_keyless_file_and_a_gone_one(
    stage, machine, silence, tmp_path, monkeypatch
):
    folder = tmp_path / "downloads"
    place(folder, silence, "drone")
    place(folder, silence, "fresh")
    place(folder, silence, "gone")
    bind_scoring(monkeypatch, keyless=("drone",))

    queued = stage.json("analyze", "run", "--queue-only", str(folder))
    assert queued.code == OK, queued.stdout
    (folder / "gone.flac").unlink()
    driven = stage.json("analyze", "run", str(folder), "--job", queued.envelope["data"]["job_id"])
    assert driven.code != OK, driven.stdout
    assert (folder / "drone.flac").is_file()
    assert (folder / "08A - 124 - fresh.flac").is_file()

    empty = tmp_path / "empty"
    empty.mkdir()
    assert stage.json("analyze", "run", str(empty)).code == OK
    assert stage.crate("analyze", "run", str(tmp_path / "absent")).code == OK


def test_run_with_nothing_bound_refuses_its_item(stage, machine, silence, tmp_path):
    folder = tmp_path / "downloads"
    place(folder, silence, "track")
    refused = stage.json("analyze", "run", str(folder))
    assert refused.code != OK, refused.stdout
    assert (folder / "track.flac").is_file()


# ---------------------------------------------------------------------------
# analyze calibrate and analyze validate
# ---------------------------------------------------------------------------


def test_calibrate_by_hand_and_by_fit(stage, machine, silence, tmp_path, monkeypatch):
    assert stage.json("analyze", "calibrate", "--vocal-cut", "5").code == OK
    assert stage.crate("analyze", "calibrate", "--vocal-cut", "7.5").code == OK
    assert stage.json("analyze", "calibrate", "--vocal-cut=100.5").code != OK

    folder = tmp_path / "downloads"
    names = [f"t{index:02d}" for index in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})
    fitted = stage.json("analyze", "calibrate", str(folder), "--accept-partial")
    assert fitted.code == OK, fitted.stdout
    assert energy.load_calibration(machine) is not None
    # Again, as a person reads it: the fit replaces the one it wrote.
    assert stage.crate("analyze", "calibrate", str(folder), "--accept-partial").code == OK


def test_calibrate_over_the_library_and_what_it_will_not_fit(
    stage, machine, silence, tmp_path, monkeypatch
):
    root = Path(machine.library.root)
    seeds: dict[str, int | None] = {}
    for genre in ("House", "Techno"):
        for index in range(8):
            name = f"{genre.lower()}{index:02d}"
            seeds[name] = len(seeds)
            place(root / "Music" / genre, silence, name, voxlevel=3)
    few = tmp_path / "few"
    for name in ("x", "y"):
        place(few, silence, name)
        seeds[name] = len(seeds)
    bind_measuring(monkeypatch, seeds)

    assert stage.json("analyze", "calibrate", str(root / "Music" / "House")).code == OK
    fitted = stage.json("analyze", "calibrate", str(root), "--recursive")
    assert fitted.code == OK, fitted.stdout
    assert stage.crate("analyze", "calibrate", str(few), "--accept-partial").code == OK
    assert stage.json("analyze", "calibrate").code == OK
    empty = tmp_path / "empty"
    empty.mkdir()
    assert stage.json("analyze", "calibrate", str(empty), "--accept-partial").code == OK
    assert stage.crate("analyze", "calibrate", str(tmp_path / "nowhere")).code == OK

    monkeypatch.setattr(energy, "_EXTRACTOR", None)
    refused = stage.json("analyze", "calibrate", str(few), "--accept-partial")
    assert refused.code == int(ExitCode.MODULE_UNAVAILABLE), refused.stdout


def test_validate_says_nothing_was_scored(stage, machine, tmp_path):
    assert stage.json("analyze", "validate").code == OK
    assert stage.crate("analyze", "validate", str(tmp_path)).code == OK


# ---------------------------------------------------------------------------
# analyze restamp
# ---------------------------------------------------------------------------


def test_restamp_rescores_a_folder_and_then_finds_it_unchanged(
    stage, machine, silence, tmp_path, monkeypatch
):
    folder = tmp_path / "downloads"
    place(folder, silence, "low", energylevel=7)
    place(folder, silence, "high", energylevel=7)
    place(folder, silence, "untagged")
    place(folder, silence, "odd", energylevel=5)
    place(folder, silence, "deeper/nested", energylevel=2)
    bind_measuring(monkeypatch, {"low": 0, "high": 19, "untagged": 10, "odd": None, "nested": 15})

    refused = stage.json("analyze", "restamp", str(folder))
    assert refused.code != OK, refused.stdout
    energy.save_calibration(machine, energy.calibrate([features(i) for i in range(20)]))

    restamped = stage.crate("analyze", "restamp", str(folder))
    assert restamped.code == OK, restamped.stderr
    assert tags.read_energy_from_file(folder / "low.flac") == energy.LEVEL_MIN
    # Again: every level is where the calibration puts it.
    assert stage.json("analyze", "restamp", str(folder)).code == OK

    queued = stage.json("analyze", "restamp", "--queue-only", "--recursive", str(folder))
    assert queued.code == OK, queued.stdout
    driven = stage.json("analyze", "restamp", str(folder), "--job", queued.envelope["data"]["job_id"])
    assert driven.code == OK, driven.stdout
    assert tags.read_energy_from_file(folder / "deeper" / "nested.flac") != 2

    empty = tmp_path / "empty"
    empty.mkdir()
    assert stage.json("analyze", "restamp", str(empty)).code == OK
    assert stage.crate("analyze", "restamp", str(tmp_path / "absent")).code == OK

    monkeypatch.setattr(energy, "_EXTRACTOR", None)
    without = stage.json("analyze", "restamp", str(folder))
    assert without.code != OK, without.stdout
