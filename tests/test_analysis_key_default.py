"""U276: an analysis run reads the key without the harmonic separation.

A121 (sitting 94) read U241's three key methods against rekordbox's own keys
on 300 library files: the whole track 159 equal, the windows 157, the plain
chroma 161, the plain chroma in about half the whole track's time. So
``plain`` is the default wherever a caller names no method, and ``whole`` and
``windows`` stay selectable. What a fixture can honestly hold is held here:
which method each caller gets, that the default never separates, that naming
``whole`` is the old arithmetic bit for bit, that nothing but the key can move
between the two, and that on the generated audio the two name the same key.
Whether ``plain`` agrees with rekordbox on a library is the attended
sitting's, with ``scripts/head_agreement.py --analyse 300 --step 4``.

The audio tests skip where the analysis extra is absent, because the chroma is
librosa's; the defaults and the bindings are held without it.
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import warnings
from pathlib import Path

import pytest

from cratekit.analysis import detect

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _script(name: str):
    spec = importlib.util.spec_from_file_location(f"u276_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Which method a caller gets when it names none
# ---------------------------------------------------------------------------


def test_the_default_key_method_is_the_plain_chroma():
    assert detect.KEY_DEFAULT == detect.KEY_PLAIN == "plain"
    assert detect.KEY_DEFAULT in detect.KEY_METHODS


@pytest.mark.parametrize("function", ["key_profile", "analyse_file"])
def test_a_detector_function_called_without_a_method_takes_the_default(function):
    parameters = inspect.signature(getattr(detect, function)).parameters
    name = "method" if function == "key_profile" else "key"
    assert parameters[name].default == detect.KEY_DEFAULT


def test_the_whole_and_windowed_methods_stay_selectable():
    assert detect.KEY_METHODS == ("whole", "windows", "plain")


def _keywords_of_partials(path: Path, callee: str) -> list[set[str]]:
    """The keyword names of every ``functools.partial(detect.<callee>, ...)`` in a module."""
    found: list[set[str]] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func, first = node.func, node.args[0]
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "partial"
            and isinstance(first, ast.Attribute)
            and first.attr == callee
        ):
            found.append({keyword.arg for keyword in node.keywords if keyword.arg})
    return found


@pytest.mark.parametrize("module", ["cli.py", "ahead.py"])
def test_the_runs_shipped_bindings_name_no_method_so_they_take_the_default(module):
    """``analyze run`` binds the detector in the driver and in each stream worker.

    Neither names a key method, so both read the key the way the default says,
    and a head measured ahead is the head the driver would have measured.
    """
    bound = _keywords_of_partials(REPO_ROOT / "src" / "cratekit" / "analysis" / module, "analyse_file")
    assert bound, f"no detector binding found in analysis/{module}"
    for keywords in bound:
        assert "key" not in keywords, keywords


def test_the_agreement_script_reads_the_default_method_when_none_is_named():
    script = _script("head_agreement")
    assert script.build_parser().parse_args([]).key == detect.KEY_DEFAULT
    for method in detect.KEY_METHODS:
        assert script.build_parser().parse_args(["--key", method]).key == method


def test_the_stage_script_times_the_default_method_when_none_is_named(tmp_path):
    script = _script("analyze_stages")
    assert script.build_parser().parse_args(["stages", str(tmp_path)]).key == detect.KEY_DEFAULT
    for method in detect.KEY_METHODS:
        parsed = script.build_parser().parse_args(["stages", str(tmp_path), "--key", method])
        assert parsed.key == method


# ---------------------------------------------------------------------------
# The stage report
# ---------------------------------------------------------------------------


def _result(method: str, totals: dict[str, float]) -> dict:
    return {
        "tracks": 1,
        "audio_seconds": 60.0,
        "wall_seconds": sum(totals.values()),
        "key": method,
        "energy_against": "a stand in",
        "vocals": "left out",
        "totals": totals,
    }


def test_the_stage_report_under_plain_counts_no_separation():
    script = _script("analyze_stages")
    totals = {"decode": 1.0, "tempo_drift": 1.0, "chroma_key": 1.0, "energy": 1.0}
    table = script.stage_table(_result(detect.KEY_PLAIN, totals))
    assert "harmonic separation" not in table, table
    assert "| chroma and key |" in table


@pytest.mark.parametrize("method", ["whole", "windows"])
def test_the_stage_report_under_a_separating_method_keeps_the_separation(method):
    script = _script("analyze_stages")
    totals = {"decode": 1.0, "tempo_drift": 1.0, "harmonic": 2.0, "chroma_key": 1.0, "energy": 1.0}
    table = script.stage_table(_result(method, totals))
    assert "| harmonic separation | 2.0 |" in table, table


def test_the_stages_a_run_times_are_the_methods_own():
    assert "harmonic" not in detect.stages_of(detect.KEY_PLAIN)
    for method in (detect.KEY_WHOLE, detect.KEY_WINDOWS):
        assert detect.stages_of(method) == detect.STAGES
    assert detect.stages_of(detect.KEY_PLAIN) == tuple(
        stage for stage in detect.STAGES if stage != "harmonic"
    )


def test_a_stage_set_for_a_method_nobody_built_is_refused():
    with pytest.raises(ValueError):
        detect.stages_of("halves")


# ---------------------------------------------------------------------------
# The audio: what each method computes
# ---------------------------------------------------------------------------


def _extra():
    np = pytest.importorskip("numpy")
    pytest.importorskip("librosa")
    soundfile = pytest.importorskip("soundfile")
    return np, soundfile


RATE = detect.MEASURE_RATE


def _in_key(np, tonic: int, seconds: float, *, minor: bool = False):
    """A key's I, IV, V, I in sustained triads with a bass, two seconds a chord.

    The fixture of ``tests/test_analysis_key_methods.py``, with its minor scale
    beside the major one so every one of the twenty four keys is written.
    """
    scale = [0, 2, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9, 11]
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


def _track(np, soundfile, folder: Path, seconds: float = 40.0) -> Path:
    """Clicks at 120 beats a minute over a C major pad, as a file the run reads."""
    path = folder / "track.flac"
    click = np.zeros(int(seconds * RATE), dtype=np.float32)
    for beat in range(int(seconds * 2)):
        at = int(beat * 0.5 * RATE)
        click[at : at + 200] += np.hanning(200).astype(np.float32)
    soundfile.write(str(path), 0.5 * click + _in_key(np, 0, seconds), RATE)
    return path


def _never(*args, **kwargs):
    raise AssertionError("the harmonic separation ran under the default key method")


def test_an_analysis_with_no_method_named_never_separates(tmp_path, monkeypatch):
    np, soundfile = _extra()
    from cratekit.analysis import separation

    path = _track(np, soundfile, tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from cratekit.analysis import warm

        warm.kernels()
        monkeypatch.setattr(separation, "harmonic", _never)
        timings: dict[str, float] = {}
        found = detect.analyse_file(path, timings=timings)
    assert found is not None and found.get("terminal") is None, found
    assert found["camelot"] == "8B"
    assert "harmonic" not in timings
    assert set(timings) == set(detect.stages_of(detect.KEY_DEFAULT))


def test_naming_whole_is_the_old_arithmetic_bit_for_bit(monkeypatch):
    """The harmonic part at margin four, then the mean chroma: what shipped before U276."""
    np, _soundfile = _extra()
    import librosa

    from cratekit.analysis import separation

    samples = _in_key(np, 7, 20.0)
    asked: list[object] = []
    real = separation.harmonic

    def recording(piece, **kwargs):
        asked.append(kwargs.get("margin"))
        return real(piece, **kwargs)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        expected = librosa.feature.chroma_cqt(
            y=real(samples, margin=4), sr=RATE
        ).mean(axis=1)
        monkeypatch.setattr(separation, "harmonic", recording)
        found = detect.key_profile(samples, RATE, method=detect.KEY_WHOLE)
    assert asked == [4]
    assert np.array_equal(found, expected)


def test_the_default_profile_is_the_plain_chroma_bit_for_bit():
    np, _soundfile = _extra()
    import librosa

    samples = _in_key(np, 7, 20.0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        expected = librosa.feature.chroma_cqt(y=samples, sr=RATE).mean(axis=1)
        found = detect.key_profile(samples, RATE)
    assert np.array_equal(found, expected)


def test_only_the_key_can_move_between_the_whole_and_the_default_method(tmp_path):
    """Tempo, drift, its verdict, energy and its status are read the same way under both."""
    np, soundfile = _extra()
    from cratekit.analysis import energy

    path = _track(np, soundfile, tmp_path)
    calibration = energy.calibrate(
        [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        whole = detect.analyse_file(path, calibration=calibration, key=detect.KEY_WHOLE)
        default = detect.analyse_file(path, calibration=calibration)
    assert whole is not None and default is not None
    assert whole.get("terminal") is None and default.get("terminal") is None
    assert whole["energy"] is not None, "the calibration did not score the fixture"
    assert {k: v for k, v in whole.items() if k != "camelot"} == {
        k: v for k, v in default.items() if k != "camelot"
    }


@pytest.mark.parametrize("minor", [False, True], ids=["major", "minor"])
def test_on_the_generated_audio_the_default_names_the_whole_tracks_key_in_every_key(minor):
    """The suite's own measurement of the change: the same key, all twelve tonics."""
    np, _soundfile = _extra()
    differs = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for tonic in range(12):
            samples = _in_key(np, tonic, 20.0, minor=minor)
            whole = detect.camelot_of(detect.key_profile(samples, RATE, method=detect.KEY_WHOLE))
            plain = detect.camelot_of(detect.key_profile(samples, RATE))
            if whole != plain or whole is None:
                differs.append((tonic, whole, plain))
    assert differs == []
