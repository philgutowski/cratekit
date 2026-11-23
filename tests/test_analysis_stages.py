"""U343: ``analyze run`` measures no key. What its detector times and answers.

The stage set and its timer with no audio; on generated audio, a whole file
measured with no chroma and no harmonic separation reached, its answer with
no key, and a tempo that moves late still read as variable. The audio tests
skip where the analysis extra is absent. Agreement with rekordbox is an
attended sitting's.
"""

from __future__ import annotations

import ast
import importlib.util
import warnings
from pathlib import Path

import pytest

from cratekit.analysis import detect
from cratekit.core import config, drift

REPO_ROOT = Path(__file__).resolve().parent.parent
RATE = detect.MEASURE_RATE
CUT = config.DEFAULT_DRIFT_CUT

#: Every name the key stage was made of before U343. None may come back.
KEY_SYMBOLS = (
    "KEY_DEFAULT",
    "KEY_METHODS",
    "KEY_PLAIN",
    "KEY_WHOLE",
    "KEY_WINDOWS",
    "camelot_of",
    "key_profile",
    "key_windows",
    "stages_of",
)


def _extra():
    np = pytest.importorskip("numpy")
    pytest.importorskip("librosa")
    soundfile = pytest.importorskip("soundfile")
    return np, soundfile


def _in_key(np, tonic: int, seconds: float):
    """A major key's I, IV, V, I in sustained triads with a bass, two seconds a chord."""
    scale = [0, 2, 4, 5, 7, 9, 11]
    out = np.zeros(int(seconds * RATE), dtype=np.float32)
    chord = int(2.0 * RATE)
    t = np.arange(chord) / RATE
    fade = np.minimum(1.0, np.minimum(t, t[::-1]) / 0.05).astype(np.float32)
    for index, start in enumerate(range(0, out.size, chord)):
        degree = (0, 3, 4, 0)[index % 4]
        notes = [
            tonic + scale[(degree + step) % 7] + (12 if degree + step >= 7 else 0)
            for step in (0, 2, 4)
        ]
        tone = sum(
            np.sin(2 * np.pi * 261.63 * 2 ** (note / 12.0) * t)
            + 0.4 * np.sin(2 * np.pi * 2 * 261.63 * 2 ** (note / 12.0) * t)
            for note in notes
        )
        tone = tone + 1.5 * np.sin(2 * np.pi * 65.41 * 2 ** (notes[0] / 12.0) * t)
        piece = (0.08 * tone * fade).astype(np.float32)
        stop = min(out.size, start + chord)
        out[start:stop] += piece[: stop - start]
    return out


def _tonal_track(np, soundfile, tmp_path: Path, seconds: float = 40.0) -> Path:
    """Clicks at 120 over a C major progression: a pulse and a key a detector could hear."""
    path = tmp_path / "tonal.flac"
    click = np.zeros(int(seconds * RATE), dtype=np.float32)
    for beat in range(int(seconds * 2)):
        at = int(beat * 0.5 * RATE)
        click[at : at + 200] += np.hanning(200).astype(np.float32)
    soundfile.write(str(path), 0.5 * click + _in_key(np, 0, seconds), RATE)
    return path


def test_the_stages_are_decode_tempo_and_drift_and_energy():
    assert detect.STAGES == ("decode", "tempo_drift", "energy")


@pytest.mark.parametrize("name", KEY_SYMBOLS)
def test_the_key_stage_is_gone_from_the_detector(name):
    assert not hasattr(detect, name), f"detect.{name} came back"


def test_the_detector_takes_no_key_method(tmp_path):
    with pytest.raises(TypeError):
        detect.analyse_file(tmp_path / "never read.flac", key="plain")


def test_the_recorded_agreement_carries_the_tempo_and_no_key():
    recorded = detect.head_agreement()
    assert "tempo" in recorded and "within_one" in recorded
    assert not {"key", "key_read_with", "key_by_method", "key_method"} & set(recorded)


def test_the_timer_adds_to_a_mapping_and_costs_a_caller_without_one_nothing():
    timings: dict[str, float] = {"decode": 1.0}
    with detect.timed(timings, "decode"):
        pass
    with detect.timed(timings, "energy"):
        pass
    assert timings["decode"] >= 1.0 and timings["energy"] >= 0.0
    with detect.timed(None, "decode"):
        pass
    assert set(timings) == {"decode", "energy"}


def test_the_timer_keeps_its_time_when_the_stage_raises():
    timings: dict[str, float] = {}
    with pytest.raises(RuntimeError):
        with detect.timed(timings, "tempo_drift"):
            raise RuntimeError("the tempogram raised")
    assert "tempo_drift" in timings


def _stage_script():
    path = REPO_ROOT / "scripts" / "analyze_stages.py"
    spec = importlib.util.spec_from_file_location("analyze_stages_for_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_scripts_stage_names_are_the_detectors_and_the_vocal_passs():
    """The instrument prints what the shipped functions time, under the same names."""
    module = _stage_script()
    assert tuple(key for key, _words in module.STAGE_WORDS) == (
        *detect.STAGES,
        "vocal_decode",
        "vocal_model",
    )
    assert len(module.SYNTHETIC_SET) >= 20, "the card asks for a set of at least twenty"
    lengths = [row[0] for row in module.SYNTHETIC_SET]
    assert min(lengths) < 30 and max(lengths) > 600, "the set is not of mixed length"
    assert module.stride(list(range(10)), 4) == [0, 3, 6, 9]
    assert module.stride(list(range(3)), 20) == [0, 1, 2]
    assert module.stride(list(range(9)), 1) == [0]


def test_the_stage_script_takes_no_key_method(tmp_path):
    module = _stage_script()
    with pytest.raises(SystemExit):
        module.build_parser().parse_args(["stages", str(tmp_path), "--key", "plain"])
    args = module.build_parser().parse_args(["stages", str(tmp_path)])
    assert not hasattr(args, "key")


def test_the_stage_table_has_a_row_per_stage_and_none_for_a_key():
    module = _stage_script()
    rows = [{"stages": {"decode": 1.0, "tempo_drift": 2.0, "energy": 3.0}}]
    totals = module.stage_totals(rows)
    assert totals["tempo_drift"] == 2.0 and "chroma_key" not in totals
    table = module.stage_table(
        {"tracks": 1, "audio_seconds": 60.0, "wall_seconds": 6.0, "energy_against": "x",
         "vocals": "left out", "totals": totals}
    )
    assert "| tempo and drift | 2.0 | 33% |" in table
    assert "key" not in table


def test_the_agreement_script_takes_no_key_method():
    path = REPO_ROOT / "scripts" / "head_agreement.py"
    spec = importlib.util.spec_from_file_location("head_agreement_for_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(SystemExit):
        module.build_parser().parse_args(["--analyse", "3", "--key", "plain"])


def _calls_in(path: Path) -> set[str]:
    """Every attribute or name called in ``path``'s source."""
    called: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call):
            target = node.func
            if isinstance(target, ast.Attribute):
                called.add(target.attr)
            elif isinstance(target, ast.Name):
                called.add(target.id)
    return called


def test_no_shipped_module_reads_a_chroma_or_names_the_key_stage():
    """Read from source: the key stage cannot return under another caller."""
    package = REPO_ROOT / "src" / "cratekit"
    found: list[str] = []
    for path in sorted(package.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        called = _calls_in(path)
        for name in ("chroma_cqt", "chroma_stft", "chroma_cens", *KEY_SYMBOLS):
            if name in called:
                found.append(f"{path.relative_to(package)}: {name}")
    assert found == []


def _never(*args, **kwargs):
    raise AssertionError("the run reached the key stage it no longer has")


def test_a_whole_file_is_measured_with_no_chroma_no_separation_and_no_key(tmp_path, monkeypatch):
    np, soundfile = _extra()
    import librosa

    from cratekit.analysis import separation, warm

    path = _tonal_track(np, soundfile, tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warm.kernels()
        monkeypatch.setattr(separation, "harmonic", _never)
        monkeypatch.setattr(librosa.feature, "chroma_cqt", _never)
        timings: dict[str, float] = {}
        found = detect.analyse_file(path, timings=timings)
        again = detect.analyse_file(path)
    assert found is not None and found.get("terminal") is None, found
    assert set(found) == {
        "path", "rate", "drift", "drift_verdict", "energy", "energy_status"
    }, found
    assert 118 <= found["rate"] <= 122, found
    assert set(timings) == set(detect.STAGES)
    assert all(seconds >= 0.0 for seconds in timings.values())
    assert found == again, "timing a run changed what it measured"


def test_a_tempo_that_moves_only_in_its_last_third_is_still_variable(tmp_path):
    """The drift is read over the whole track, so a late move is found (U241 keeps it so)."""
    np, soundfile = _extra()
    seconds = 180.0

    def tempo_at(at: float) -> float:
        late = max(0.0, at - 2.0 * seconds / 3.0) / (seconds / 3.0)
        return 124.0 * (1.0 + 0.10 * late)

    samples = np.zeros(int(RATE * seconds), dtype=np.float32)
    burst = np.hanning(200).astype(np.float32)
    rng = np.random.default_rng(0)
    for every, level in ((1.0, 1.0), (0.5, 0.3)):
        at = 0.0
        while True:
            start = int(round(at * RATE))
            if start + burst.size > samples.size:
                break
            samples[start : start + burst.size] += level * burst
            at += every * 60.0 / tempo_at(at)
    samples += 0.02 * rng.standard_normal(samples.size).astype(np.float32)

    first_two_thirds = samples[: int(RATE * 2.0 * seconds / 3.0)]
    _tempo, steady = detect.measure_tempo_and_drift(first_two_thirds, RATE, floor=80, ceiling=160)
    assert drift.verdict(steady, CUT) == drift.STEADY, "the fixture moves before its last third"

    _tempo, moved = detect.measure_tempo_and_drift(samples, RATE, floor=80, ceiling=160)
    assert moved is not None and drift.verdict(moved, CUT) == drift.VARIABLE, moved

    path = tmp_path / "late mover.flac"
    soundfile.write(str(path), samples + _in_key(np, 0, seconds), RATE)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        found = detect.analyse_file(path)
    assert found["drift_verdict"] == drift.VARIABLE, found
