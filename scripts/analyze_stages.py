#!/usr/bin/env python3
"""Measure where an ``analyze run`` spends its time, and what the pool buys (U241).

Reads audio and writes NOTHING onto it: no tag, no rename, no report, no job.
The one thing it can write is the synthetic set, into an empty folder you name.

    .venv/bin/python scripts/analyze_stages.py synthesize /path/to/empty/folder
    .venv/bin/python scripts/analyze_stages.py stages /path/to/folder --limit 20
    .venv/bin/python scripts/analyze_stages.py memory /path/to/folder --limit 5
    .venv/bin/python scripts/analyze_stages.py batch /path/to/folder --limit 20

``stages`` times each stage of the shipped functions in place, one process,
one track after another: decode, tempo and drift, harmonic separation, chroma
and key, energy, vocal decode, vocal model. ``memory`` measures the peak
memory of one light worker per track, each in a fresh process, which is the
number ``cratekit.analysis.light`` declares to the pool. ``batch`` runs the
measuring an ``analyze run`` does, once with one worker and once with the pool
this machine affords, compares the two sets of results, and prints the pool's
check line.

The folder is read one level deep, the sorted audio files, the walk ``analyze
run`` itself takes. ``--limit N`` takes N of them at an even stride so short
and long tracks are both in. Energy is scored against the configured library's
calibration when there is one, and against a flat stand-in otherwise, so the
energy stage is timed either way. The vocal stages run when the vocal model can
load here; ``--untrained-model`` times the shipped architecture with untrained
weights where the checkpoint is absent, which costs the same and scores
nothing meaningful, and ``--no-vocals`` leaves the pass out.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

#: The stages in the order a track meets them, and the words each is printed under.
STAGE_WORDS: tuple[tuple[str, str], ...] = (
    ("decode", "decode"),
    ("tempo_drift", "tempo and drift"),
    ("harmonic", "harmonic separation"),
    ("chroma_key", "chroma and key"),
    ("energy", "energy"),
    ("vocal_decode", "vocal decode"),
    ("vocal_model", "vocal model"),
)

#: The fixed synthetic set: seconds, tempo, tonic as semitones above C, minor,
#: and a shape. Mixed lengths from a stinger to eleven minutes, most of them
#: the seven to ten minute tracks the card was filed over. ``latekey`` changes
#: key in its last quarter, ``ramp`` and ``lastthird`` move their tempo, and
#: ``beatless`` has no drums. Fixed here so two machines measure one set.
SYNTHETIC_SET: tuple[tuple[int, float, int, bool, str], ...] = (
    (2, 124.0, 0, True, "steady"),
    (45, 122.0, 9, True, "steady"),
    (95, 128.0, 4, False, "steady"),
    (150, 126.0, 7, True, "steady"),
    (185, 120.0, 2, True, "steady"),
    (210, 100.0, 5, False, "steady"),
    (240, 132.0, 11, True, "steady"),
    (265, 124.5, 0, False, "latekey"),
    (290, 127.0, 3, True, "steady"),
    (320, 123.0, 8, True, "ramp"),
    (345, 125.0, 10, False, "steady"),
    (370, 121.3, 1, True, "steady"),
    (395, 129.0, 6, True, "lastthird"),
    (420, 126.0, 9, True, "steady"),
    (445, 124.0, 4, True, "beatless"),
    (470, 122.0, 7, False, "steady"),
    (500, 128.0, 2, True, "steady"),
    (530, 125.5, 5, True, "steady"),
    (560, 127.0, 0, True, "steady"),
    (590, 123.0, 3, False, "lastthird"),
    (600, 126.0, 8, True, "steady"),
    (615, 130.0, 10, True, "steady"),
    (660, 124.0, 1, True, "steady"),
)
SYNTHETIC_RATE = 44100


def synthetic_name(index: int) -> str:
    seconds, _tempo, _tonic, _minor, shape = SYNTHETIC_SET[index]
    return f"set{index:02d}-{seconds:03d}s-{shape}.flac"


# ---------------------------------------------------------------------------
# The synthetic set
# ---------------------------------------------------------------------------


def _beat_times(seconds: float, tempo: float, shape: str) -> list[float]:
    times: list[float] = []
    now = 0.0
    while now < seconds:
        times.append(now)
        position = now / seconds
        rate = tempo
        if shape == "ramp":
            rate = tempo * (1.0 + 0.08 * position)
        elif shape == "lastthird" and position > 2.0 / 3.0:
            rate = tempo * (1.0 + 0.10 * (position - 2.0 / 3.0) * 3.0)
        now += 60.0 / rate
    return times


def synthesize_track(index: int) -> Any:
    """One track of the set as stereo samples: drums, a bass and a triad pad in its key."""
    import numpy as np

    seconds, tempo, tonic, minor, shape = SYNTHETIC_SET[index]
    rate = SYNTHETIC_RATE
    rng = np.random.default_rng(1000 + index)
    count = int(seconds * rate)
    mix = np.zeros(count, dtype=np.float32)

    span = np.arange(int(0.22 * rate)) / rate
    sweep = 45.0 + 110.0 * np.exp(-span * 38.0)
    kick = (np.sin(2 * np.pi * np.cumsum(sweep) / rate) * np.exp(-span * 14.0)).astype(np.float32)
    hiss = np.diff(rng.standard_normal(int(0.05 * rate)).astype(np.float32), prepend=0.0)
    hat = hiss * np.exp(-np.arange(hiss.size) / rate * 90.0).astype(np.float32) * 0.5

    if shape != "beatless":
        for when in _beat_times(seconds, tempo, shape):
            position = when / seconds
            start = int(when * rate)
            if not 0.45 < position < 0.55 and position > 0.04:
                stop = min(count, start + kick.size)
                mix[start:stop] += 0.9 * kick[: stop - start]
            off = int((when + 0.5 * 60.0 / tempo) * rate)
            if off < count and position > 0.08:
                stop = min(count, off + hat.size)
                mix[off:stop] += hat[: stop - off]

    def tone(frequency: float, length: int, partials: tuple[float, ...]) -> Any:
        at = np.arange(length) / rate
        out = np.zeros(length, dtype=np.float32)
        for number, level in enumerate(partials, start=1):
            out += (level * np.sin(2 * np.pi * frequency * number * at)).astype(np.float32)
        return out

    scale = [0, 2, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9, 11]
    progression = [0, 5, 3, 4] if minor else [0, 3, 4, 0]
    bar = 4 * 60.0 / tempo
    bars = int(np.ceil(seconds / bar))
    for number in range(bars):
        start = int(number * bar * rate)
        stop = min(count, int((number + 1) * bar * rate))
        if stop <= start:
            break
        key = tonic
        if shape == "latekey" and number / max(1, bars) > 0.72:
            key = (tonic + 6) % 12
        degree = progression[number % len(progression)]
        root = key + scale[degree % 7]
        third = key + scale[(degree + 2) % 7] + (12 if degree + 2 >= 7 else 0)
        fifth = key + scale[(degree + 4) % 7] + (12 if degree + 4 >= 7 else 0)
        length = stop - start
        edge = 0.02 * rate
        envelope = np.minimum(1.0, np.arange(length) / edge)
        envelope = (envelope * np.minimum(1.0, (length - np.arange(length)) / edge)).astype(
            np.float32
        )
        pad = sum(
            tone(261.63 * 2 ** (step / 12.0), length, (1.0, 0.5, 0.25, 0.12))
            for step in (root, third, fifth)
        )
        bass = tone(65.41 * 2 ** (root / 12.0), length, (1.0, 0.3))
        level = 0.22 if shape == "beatless" else 0.10
        mix[start:stop] += envelope * (level * pad + 0.25 * bass)

    mix += 0.003 * rng.standard_normal(count).astype(np.float32)
    mix = 0.89 * mix / (float(np.max(np.abs(mix))) or 1.0)
    return np.stack([mix, np.roll(mix, 17) * 0.97], axis=1)


def synthesize(folder: Path) -> int:
    """Write the set into ``folder``, which must hold no audio of anyone's."""
    import soundfile

    folder.mkdir(parents=True, exist_ok=True)
    expected = {synthetic_name(index) for index in range(len(SYNTHETIC_SET))}
    strangers = sorted(entry.name for entry in folder.iterdir() if entry.name not in expected)
    if strangers:
        print(
            f"{folder} already holds other files ({strangers[0]} and "
            f"{len(strangers) - 1} more), and the set is only written into a folder "
            f"of its own"
        )
        return 2
    for index in range(len(SYNTHETIC_SET)):
        target = folder / synthetic_name(index)
        if target.exists():
            continue
        soundfile.write(str(target), synthesize_track(index), SYNTHETIC_RATE, subtype="PCM_16")
        print(target.name, flush=True)
    return 0


# ---------------------------------------------------------------------------
# What is measured, and under what
# ---------------------------------------------------------------------------


def chosen(folder: Path, limit: int | None) -> list[Path]:
    """The folder's audio, sorted, ``limit`` of it at an even stride."""
    from cratekit.core import discovery

    paths = [folder / name for name in discovery.scan_audio(folder).items]
    if limit is None or limit >= len(paths):
        return paths
    return stride(paths, limit)


def stride(items: list[Any], count: int) -> list[Any]:
    """``count`` of ``items`` spread evenly from the first to the last."""
    if count <= 0:
        return []
    if count >= len(items):
        return list(items)
    if count == 1:
        return [items[0]]
    step = (len(items) - 1) / (count - 1)
    return [items[round(index * step)] for index in range(count)]


def stand_in_calibration() -> Any:
    """A calibration that scores every track, so the energy stage runs and is timed.

    Not anybody's library: a flat reference with unit spread, used only where
    the configured library has no calibration to read.
    """
    from cratekit.analysis import energy

    rows = [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
    return energy.calibrate(rows)


def calibration_for_measuring() -> tuple[Any, str]:
    from cratekit.analysis import energy
    from cratekit.core import config
    from cratekit.core.cause import CratekitError

    try:
        cfg = config.load()
        found = energy.load_calibration(cfg)
    except (config.ConfigError, CratekitError, OSError):
        found = None
    if found is not None:
        return found, "the configured library's calibration"
    return stand_in_calibration(), "a stand-in calibration, since the library has none to read"


def untrained_model() -> Any:
    """The shipped architecture with untrained weights: the same arithmetic, so the same cost.

    For timing the vocal model where its checkpoint is absent. What it scores
    means nothing, and nothing here writes a score anywhere.
    """
    from cratekit.analysis import vocals

    if not vocals.labels_ready():
        raise SystemExit(
            f"--untrained-model still needs the label table at {vocals.LABELS}, because "
            f"the library reads it when it is imported"
        )
    import torch
    from panns_inference import SoundEventDetection, labels
    from panns_inference.models import Cnn14_DecisionLevelMax

    wrapper = SoundEventDetection.__new__(SoundEventDetection)
    wrapper.device = "cpu"
    wrapper.labels = labels
    wrapper.classes_num = len(labels)
    torch.manual_seed(0)
    wrapper.model = Cnn14_DecisionLevelMax(
        sample_rate=32000,
        window_size=1024,
        hop_size=320,
        mel_bins=64,
        fmin=50,
        fmax=14000,
        classes_num=wrapper.classes_num,
    )
    wrapper.model.eval()
    return wrapper


def bind_vocals(args: argparse.Namespace) -> str:
    """Bind the vocal loader this run measures with, and say which it was."""
    from cratekit.analysis import vocal, vocals

    if args.no_vocals:
        vocals.bind_loader(None)
        return "left out"
    if args.untrained_model:
        vocals.bind_loader(untrained_model)
        return "the shipped architecture with untrained weights, timing only"
    missing = vocals.missing_requirement()
    if missing is not None:
        vocals.bind_loader(None)
        return f"left out, since the model cannot load here ({missing})"
    vocals.bind_loader(vocal.default_loader)
    return "the shipped model"


def peak_megabytes() -> float:
    """This process's peak resident memory. Kilobytes on Linux, bytes on darwin."""
    import resource

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak / (1024 * 1024) if sys.platform == "darwin" else peak / 1024


# ---------------------------------------------------------------------------
# stages
# ---------------------------------------------------------------------------


def stages(args: argparse.Namespace) -> int:
    from cratekit.analysis import detect, light, vocals

    paths = chosen(args.folder, args.limit)
    calibration, calibration_words = calibration_for_measuring()
    vocal_words = bind_vocals(args)
    rows: list[dict[str, Any]] = []
    for path in paths:
        timings: dict[str, float] = {}
        started = time.perf_counter()
        found = detect.analyse_file(path, calibration=calibration, key=args.key, timings=timings)
        if found is not None and found.get("terminal") is None and not args.no_vocals:
            vocals.analyse({"path": str(path), "terminal": None}, timings=timings)
        rows.append(
            {
                "name": path.name,
                "seconds": light.seconds_of(path),
                "wall": time.perf_counter() - started,
                "stages": timings,
                "status": "analyzed"
                if found is not None and found.get("terminal") is None
                else (found or {}).get("terminal", "skipped-no-key"),
            }
        )
        if not args.json:
            print(f"  {path.name}: {rows[-1]['wall']:.1f} s", file=sys.stderr, flush=True)
    totals = {key: sum(row["stages"].get(key, 0.0) for row in rows) for key, _ in STAGE_WORDS}
    result = {
        "tracks": len(rows),
        "audio_seconds": sum(row["seconds"] for row in rows),
        "wall_seconds": sum(row["wall"] for row in rows),
        "key": args.key,
        "energy_against": calibration_words,
        "vocals": vocal_words,
        "totals": totals,
        "rows": rows,
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(stage_table(result))
    return 0


def stage_table(result: dict[str, Any]) -> str:
    """The stage totals as a table a record can hold, seconds and share of the run."""
    wall = result["wall_seconds"] or 1.0
    lines = [
        f"{result['tracks']} tracks, {result['audio_seconds'] / 60:.0f} minutes of audio, "
        f"key method {result['key']}",
        f"energy scored against {result['energy_against']}; vocals: {result['vocals']}",
        "",
        "| stage | seconds | share |",
        "|---|---|---|",
    ]
    for key, words in STAGE_WORDS:
        seconds = result["totals"].get(key, 0.0)
        lines.append(f"| {words} | {seconds:.1f} | {100 * seconds / wall:.0f}% |")
    lines.append(f"| the whole run | {result['wall_seconds']:.1f} | |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# memory
# ---------------------------------------------------------------------------

def one_head(args: argparse.Namespace) -> int:
    """Measure one file's head in THIS process and print the process's peak memory.

    What ``memory`` runs once per track, each in a process of its own, so the
    peak it prints is one track's and nothing before it.
    """
    from cratekit.analysis import detect

    detect.analyse_file(args.path, calibration=stand_in_calibration())
    print(peak_megabytes())
    return 0


def memory(args: argparse.Namespace) -> int:
    from cratekit.analysis import light

    rows = []
    for path in chosen(args.folder, args.limit):
        done = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "one-head", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if done.returncode != 0:
            print(f"{path.name}: could not be measured ({done.stderr.strip()[-200:]})")
            continue
        seconds = light.seconds_of(path)
        rows.append(
            {
                "name": path.name,
                "seconds": seconds,
                "peak_megabytes": float(done.stdout.strip().splitlines()[-1]),
                "declared_megabytes": light.worker_bytes(seconds) / (1024 * 1024),
            }
        )
    if args.json:
        print(json.dumps({"rows": rows}, indent=2))
        return 0
    print("| track | length | measured peak | declared to the pool |")
    print("|---|---|---|---|")
    for row in rows:
        print(
            f"| {row['name']} | {row['seconds']:.0f} s | {row['peak_megabytes']:.0f} MB "
            f"| {row['declared_megabytes']:.0f} MB |"
        )
    over = [row["name"] for row in rows if row["peak_megabytes"] > row["declared_megabytes"]]
    if over:
        print(f"\nMEASURED OVER DECLARED on {len(over)} track(s): {', '.join(over)}")
    return 0


# ---------------------------------------------------------------------------
# batch
# ---------------------------------------------------------------------------


def _measure_all(job: str, paths: list[str], settings: Any, no_vocals: bool) -> list[dict]:
    from cratekit.analysis import ahead, vocals

    found = []
    for path in paths:
        head = ahead.head(job, path, settings)
        found.append(head if no_vocals or head.get("terminal") is not None else vocals.analyse(head))
    return found


def batch(args: argparse.Namespace) -> int:
    from cratekit.analysis import ahead, detect, light, vocals
    from cratekit.core import config, pool

    paths = [str(path) for path in chosen(args.folder, args.limit)]
    calibration, calibration_words = calibration_for_measuring()
    vocal_words = bind_vocals(args)
    try:
        analysis = config.load().analysis
        window, cut = (analysis.tempo_floor, analysis.tempo_ceiling), analysis.drift_cut
    except (config.ConfigError, OSError):
        window = (config.DEFAULT_TEMPO_FLOOR, config.DEFAULT_TEMPO_CEILING)
        cut = config.DEFAULT_DRIFT_CUT
    settings = ahead.Settings(
        calibration=calibration.to_json(), tempo_window=window, drift_cut=float(cut)
    )
    ahead.bind_shipped(settings.calibration, settings.tempo_window, settings.drift_cut)

    started = time.perf_counter()
    serial = _measure_all("no-session", paths, settings, args.no_vocals)
    serial_seconds = time.perf_counter() - started

    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES
    if vocals.loader_bound():
        reserve += vocals.VOCAL_WORKER_BYTES
    session = ahead.open_session(
        "measured", paths, settings, reserve_bytes=reserve, reserved_cores=args.reserved_cores
    )
    started = time.perf_counter()
    try:
        pooled = _measure_all("measured", paths, settings, args.no_vocals)
    finally:
        ahead.close_session("measured")
    pooled_seconds = time.perf_counter() - started
    record = ahead.report(session)

    result = {
        "tracks": len(paths),
        "audio_seconds": sum(light.seconds_of(path) for path in paths),
        "energy_against": calibration_words,
        "vocals": vocal_words,
        "one_worker_seconds": serial_seconds,
        "pool_seconds": pooled_seconds,
        "workers": record["workers"],
        "pool": record["detail"],
        "results_equal": serial == pooled,
        "differing": [
            Path(path).name for path, one, other in zip(paths, serial, pooled) if one != other
        ],
        "heavy_available": detect.heavy_available(),
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"{result['tracks']} tracks, {result['audio_seconds'] / 60:.0f} minutes of audio; "
            f"vocals: {vocal_words}"
        )
        print(f"one worker: {serial_seconds:.1f} s, {serial_seconds / max(1, len(paths)):.1f} s a track")
        print(
            f"the pool:   {pooled_seconds:.1f} s, {pooled_seconds / max(1, len(paths)):.1f} s a "
            f"track, {serial_seconds / pooled_seconds:.2f} times faster"
        )
        print(f"analyze.pool: {record['detail']}")
        print(f"results equal: {result['results_equal']}")
        for name in result["differing"]:
            print(f"  DIFFERS: {name}")
    return 0 if result["results_equal"] else 1


# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)

    made = commands.add_parser("synthesize", help="write the fixed synthetic set into a folder")
    made.add_argument("folder", type=Path)
    made.set_defaults(run=lambda args: synthesize(args.folder))

    def measuring(name: str, words: str, run: Any) -> argparse.ArgumentParser:
        added = commands.add_parser(name, help=words)
        added.add_argument("folder", type=Path)
        added.add_argument("--limit", type=int, default=None, metavar="N")
        added.add_argument("--json", action="store_true")
        added.set_defaults(run=run)
        return added

    def with_vocals(added: argparse.ArgumentParser) -> None:
        chosen_model = added.add_mutually_exclusive_group()
        chosen_model.add_argument("--no-vocals", action="store_true")
        chosen_model.add_argument("--untrained-model", action="store_true")

    alone = commands.add_parser("one-head", help="one file's head and this process's peak memory")
    alone.add_argument("path", type=Path)
    alone.set_defaults(run=one_head)

    from cratekit.analysis import detect

    timed = measuring("stages", "wall time of each stage, one process", stages)
    timed.add_argument("--key", default=detect.KEY_WHOLE, choices=detect.KEY_METHODS)
    with_vocals(timed)
    measuring("memory", "peak memory of one light worker per track", memory)
    pooled = measuring("batch", "one worker against the pool this machine affords", batch)
    pooled.add_argument(
        "--reserved-cores",
        type=int,
        default=2,
        metavar="N",
        help="cores kept back from the light pool (the shipped figure is 2)",
    )
    with_vocals(pooled)

    args = parser.parse_args(argv)
    if args.command in ("stages", "memory", "batch") and not args.folder.is_dir():
        parser.error(f"{args.folder} is not a folder")
    if getattr(args, "limit", None) is not None and args.limit < 1:
        parser.error("--limit must be one or more")
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    return int(args.run(args))


if __name__ == "__main__":
    sys.exit(main())
