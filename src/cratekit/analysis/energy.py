"""Energy: a calibrated index over interpretable signals, mapped to a level.

THE METHOD, stated here because U58 was asked to state it. A track becomes one
fixed vector of acoustic measurements that drive perceived energy: loudness
and dynamics, spectral brightness, onset and percussive density, spectral
balance, and tempo. Each measurement is z-scored against the LIBRARY'S OWN
mean and standard deviation, the z-scores are combined by signed weights into
one index, and the index is mapped to a level from 1 to 10 by counting how
many of nine cut points it clears. The cut points are the deciles of the
library's own index distribution, so the levels spread evenly across this
library rather than piling into the middle the way the source system's
inherited values did. A beatless guard caps a track whose onset density sits
below the calibrated floor at the top of the low band, because a sustained
tone is not high energy however loud it is.

The calibration is therefore a property of one library, which is why
``core.config`` declares ``energy_calibration`` library scoped and never
restored: losing it changes where an unchanged track routes.

WITHOUT A CALIBRATION THERE IS NO LEVEL, AND THE ABSENCE SAYS SO. A level is
"where this track sits among its own library", and with no library
distribution to sit in the honest answer is none. ``STATUS_UNCALIBRATED`` is
that answer; the worker writes no tag for it, and the routing pass reads the
missing tag as the taxonomy's no-energy sink. The first version of
``detect.analyse_file`` returned ``"energy": None`` as a literal for every
track with no status beside it, which looked like this absence and was
actually "never computed".

THE STATE FILES ARE WRITTEN ATOMICALLY AND THE UNDO LOG UNDER A LOCK. The
undo log is declared by ``core.config`` as the only surviving copy of each
file's pre-restamp value, so a truncating write interrupted by a kill would
destroy every entry at once, and two restamp jobs driven concurrently over
overlapping folders would each discard the other's entries in a read, modify,
write race. ``config.atomic_write_bytes`` closes the first and the sibling
lock closes the second, the way the label watermark does.

librosa and numpy are imported inside the functions that need them, so a slim
install can import this module and read a calibration file.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from cratekit.core import config
from cratekit.core.cause import refuse

#: Fixed column order, so a feature vector is deterministic across runs. Every
#: column is measured and only the weighted ones score; the unweighted ones cost
#: little once the spectrum exists, and they are what a later re-weighting
#: would need. Nothing persists the vector yet, so re-weighting today still
#: means re-measuring, which is recorded as a residual rather than promised.
FEATURE_ORDER: tuple[str, ...] = (
    "rms_mean", "rms_std", "rms_dr", "rms_crest", "loudness_db",
    "centroid_mean", "centroid_std", "rolloff_mean", "rolloff_std",
    "bandwidth_mean", "bandwidth_std", "flatness_mean", "flatness_std",
    "flux_mean", "flux_std", "zcr_mean", "zcr_std",
    "onset_density", "onset_std", "beat_concentration", "percussive_fraction",
    "low_band_ratio", "mid_band_ratio", "high_band_ratio", "high_low_tilt", "tempo",
)

#: Signed weights on z-scored features. Positive reads as more energy.
DEFAULT_WEIGHTS: Mapping[str, float] = {
    "rms_mean": 1.5,
    "loudness_db": 1.0,
    "rms_dr": -0.5,
    "rms_crest": -0.5,
    "centroid_mean": 1.0,
    "rolloff_mean": 0.5,
    "flatness_mean": 0.5,
    "flux_mean": 0.75,
    "onset_density": 1.5,
    "beat_concentration": 0.5,
    "percussive_fraction": 1.0,
    "high_band_ratio": 0.75,
    "low_band_ratio": 0.5,
    "tempo": 0.5,
}

#: The central slice, in seconds, a track's features are measured over. A steady
#: middle is representative of whole-track feel and is a fraction of the cost.
SEGMENT_SECONDS = 120.0
#: The rate the restamp and calibrate paths decode at, the head's rate.
MEASURE_RATE = 22050

LEVEL_MIN = 1
LEVEL_MAX = 10
CUT_COUNT = LEVEL_MAX - LEVEL_MIN
#: The cap the beatless guard applies: the top of the low band.
BEATLESS_CAP = 3
#: The percentile of onset density below which a track is treated as beatless.
ONSET_FLOOR_PERCENTILE = 2.0

STATUS_CALIBRATED = "calibrated"
STATUS_UNCALIBRATED = "uncalibrated"
STATUS_FEATURES_UNAVAILABLE = "features-unavailable"

STATE_KEY_CALIBRATION = "energy_calibration"
STATE_KEY_UNDO_LOG = "energy_undo_log"
FORMAT = "decile"

_EPS = 1e-9
_NAN = float("nan")


@dataclass(frozen=True)
class Calibration:
    """One library's energy reference: what the index is measured against."""

    mean: Mapping[str, float]
    std: Mapping[str, float]
    weights: Mapping[str, float]
    #: Nine cut points on the index, ascending, so a level is one plus the
    #: number of them the index clears.
    thresholds: tuple[float, ...]
    onset_floor: float | None
    n_tracks: int
    note: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "format": FORMAT,
            "mean": dict(self.mean),
            "std": dict(self.std),
            "weights": dict(self.weights),
            "thresholds": list(self.thresholds),
            "onset_floor": self.onset_floor,
            "n_tracks": self.n_tracks,
            "note": self.note,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Calibration:
        thresholds = tuple(float(t) for t in data["thresholds"])
        if len(thresholds) != CUT_COUNT:
            raise ValueError(
                f"an energy calibration carries {CUT_COUNT} cut points, this one "
                f"carries {len(thresholds)}"
            )
        floor = data.get("onset_floor")
        return cls(
            mean={str(k): float(v) for k, v in data["mean"].items()},
            std={str(k): float(v) for k, v in data["std"].items()},
            weights={str(k): float(v) for k, v in data["weights"].items()},
            thresholds=thresholds,
            onset_floor=None if floor is None else float(floor),
            n_tracks=int(data["n_tracks"]),
            note=str(data.get("note", "")),
        )


# ---------------------------------------------------------------------------
# Measuring
# ---------------------------------------------------------------------------


def _central(samples: Any, rate: int) -> Any:
    width = int(SEGMENT_SECONDS * rate)
    if samples.shape[-1] <= width:
        return samples
    start = (samples.shape[-1] - width) // 2
    return samples[start : start + width]


def features_from_samples(samples: Any, rate: int) -> dict[str, float] | None:
    """The ordered feature vector for decoded mono samples, or None.

    Takes samples rather than a path so the head pass, which has already
    decoded the track for key and tempo, does not decode it a second time.
    Measured over the central :data:`SEGMENT_SECONDS`.

    THE TEMPO FEATURE IS MEASURED HERE, FROM THE SLICE, ON EVERY PATH. The
    first version took the head's whole track integer tempo when it had one
    and measured its own only on the restamp path, so the same file scored
    through ``analyze run`` and through ``analyze restamp`` carried two tempo
    readings against one calibration, and a level could move on a restamp
    with nothing changed. One method, so the two paths agree by construction.
    """
    try:
        import librosa
        import numpy as np

        from cratekit.analysis import separation
    except ImportError:
        return None
    try:
        y = _central(np.asarray(samples, dtype=np.float32), rate)
        if y.size == 0:
            return None
        hop = 512
        f: dict[str, float] = {}

        rms = librosa.feature.rms(y=y, hop_length=hop)[0]
        f["rms_mean"] = float(np.mean(rms))
        f["rms_std"] = float(np.std(rms))
        p5, p95 = np.percentile(rms, [5, 95])
        f["rms_dr"] = float(p95 - p5)
        f["rms_crest"] = float(np.max(rms) / (np.mean(rms) + _EPS))
        f["loudness_db"] = float(np.mean(librosa.amplitude_to_db(rms + _EPS)))

        spectrum = np.abs(librosa.stft(y, hop_length=hop))
        cent = librosa.feature.spectral_centroid(S=spectrum, sr=rate)[0]
        f["centroid_mean"], f["centroid_std"] = float(np.mean(cent)), float(np.std(cent))
        roll = librosa.feature.spectral_rolloff(S=spectrum, sr=rate)[0]
        f["rolloff_mean"], f["rolloff_std"] = float(np.mean(roll)), float(np.std(roll))
        width = librosa.feature.spectral_bandwidth(S=spectrum, sr=rate)[0]
        f["bandwidth_mean"], f["bandwidth_std"] = float(np.mean(width)), float(np.std(width))
        flat = librosa.feature.spectral_flatness(S=spectrum)[0]
        f["flatness_mean"], f["flatness_std"] = float(np.mean(flat)), float(np.std(flat))
        if spectrum.shape[1] > 1:
            flux = np.sqrt(np.sum(np.diff(spectrum, axis=1) ** 2, axis=0))
        else:
            flux = np.zeros(1)
        f["flux_mean"], f["flux_std"] = float(np.mean(flux)), float(np.std(flux))
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop)[0]
        f["zcr_mean"], f["zcr_std"] = float(np.mean(zcr)), float(np.std(zcr))

        onset_env = librosa.onset.onset_strength(y=y, sr=rate, hop_length=hop)
        f["onset_density"] = float(np.mean(onset_env))
        f["onset_std"] = float(np.std(onset_env))
        auto = librosa.autocorrelate(onset_env)
        auto = auto[1:] if auto.size > 1 else auto
        f["beat_concentration"] = (
            float(np.max(auto) / (np.mean(auto) + _EPS)) if auto.size else 0.0
        )

        try:
            harmonic, percussive = separation.harmonic_percussive(y)
            rp = float(np.sqrt(np.mean(percussive ** 2)))
            rh = float(np.sqrt(np.mean(harmonic ** 2)))
            f["percussive_fraction"] = rp / (rp + rh + _EPS)
        except Exception:
            f["percussive_fraction"] = _NAN

        freqs = librosa.fft_frequencies(sr=rate, n_fft=(spectrum.shape[0] - 1) * 2)
        power = (spectrum ** 2).sum(axis=1)
        total = float(power.sum()) + _EPS
        low = float(power[freqs < 200].sum())
        mid = float(power[(freqs >= 200) & (freqs < 4000)].sum())
        high = float(power[freqs >= 4000].sum())
        f["low_band_ratio"] = low / total
        f["mid_band_ratio"] = mid / total
        f["high_band_ratio"] = high / total
        f["high_low_tilt"] = high / (low + _EPS)

        try:
            measured = librosa.feature.tempo(
                onset_envelope=onset_env, sr=rate, hop_length=hop, aggregate=np.mean
            )
            tempo = float(np.atleast_1d(measured)[0])
        except Exception:
            tempo = _NAN
        f["tempo"] = float(tempo)
    except Exception:
        return None
    return {name: f.get(name, _NAN) for name in FEATURE_ORDER}


def features_from_path(path: Path) -> dict[str, float] | None:
    """Decode the central slice of ``path`` and measure it.

    The restamp and calibrate path, which has no head pass to share samples
    with. ONLY THE SLICE IS DECODED: the duration is read off the header and
    the decode is asked for the central :data:`SEGMENT_SECONDS`, so a ten
    minute file costs a fifth of itself rather than all of it and then a cut.
    """
    try:
        import librosa
    except ImportError:
        return None
    try:
        offset = 0.0
        try:
            duration = float(librosa.get_duration(path=str(path)))
        except Exception:
            duration = 0.0
        if duration > SEGMENT_SECONDS:
            offset = (duration - SEGMENT_SECONDS) / 2.0
        samples, decoded_rate = librosa.load(
            str(path), sr=MEASURE_RATE, mono=True, offset=offset, duration=SEGMENT_SECONDS
        )
    except Exception:
        return None
    return features_from_samples(samples, int(decoded_rate))


_EXTRACTOR: Any = None


def bind_extractor(extractor: Any) -> None:
    """Bind what measures a path for the restamp and calibrate verbs.

    None restores the shipped extractor. A test binds a function returning a
    feature vector so the whole seam runs without the extra installed.
    """
    global _EXTRACTOR
    _EXTRACTOR = extractor


def extractor_bound() -> bool:
    return _EXTRACTOR is not None


def measure(path: Path) -> dict[str, float] | None:
    """The bound extractor, or the shipped one, applied to one path."""
    extractor = _EXTRACTOR
    if extractor is None:
        extractor = features_from_path
    return extractor(path)


# ---------------------------------------------------------------------------
# Scoring, pure
# ---------------------------------------------------------------------------


def _weighted_index(
    features: Mapping[str, float],
    mean: Mapping[str, float],
    std: Mapping[str, float],
    weights: Mapping[str, float],
) -> float:
    total = 0.0
    for name, weight in weights.items():
        if weight == 0:
            continue
        value = float(features.get(name, _NAN))
        deviation = std.get(name, 1.0) or 1.0
        z = 0.0 if math.isnan(value) else (value - mean.get(name, 0.0)) / deviation
        total += weight * z
    return float(total)


def index(features: Mapping[str, float], calibration: Calibration) -> float:
    """The weighted sum of z-scored features. A missing feature imputes to z=0."""
    return _weighted_index(features, calibration.mean, calibration.std, calibration.weights)


def level_for(features: Mapping[str, float], calibration: Calibration) -> int:
    """The level 1 to 10 for one track, with the beatless cap applied."""
    score = index(features, calibration)
    level = LEVEL_MIN + sum(1 for cut in calibration.thresholds if score >= cut)
    level = max(LEVEL_MIN, min(LEVEL_MAX, level))
    if calibration.onset_floor is not None:
        density = float(features.get("onset_density", math.inf))
        if not math.isnan(density) and density < calibration.onset_floor:
            level = min(level, BEATLESS_CAP)
    return level


def calibrate(
    feature_dicts: Sequence[Mapping[str, float]],
    *,
    weights: Mapping[str, float] | None = None,
    note: str = "",
) -> Calibration:
    """Fit one library's reference from its tracks' feature vectors.

    Per feature mean and standard deviation ignoring NaN, then the nine decile
    cut points of the resulting index, so the levels spread evenly across the
    tracks that were measured. A standard deviation of zero becomes one, so a
    feature every track shares contributes nothing rather than infinity.
    """
    import numpy as np

    if not feature_dicts:
        raise ValueError("no feature vectors to calibrate from")
    chosen = dict(weights or DEFAULT_WEIGHTS)
    mean: dict[str, float] = {}
    std: dict[str, float] = {}
    for name in FEATURE_ORDER:
        values = np.array([float(fd.get(name, _NAN)) for fd in feature_dicts], dtype=float)
        if np.all(np.isnan(values)):
            mean[name], std[name] = 0.0, 1.0
            continue
        mean[name] = float(np.nanmean(values))
        deviation = float(np.nanstd(values))
        std[name] = deviation if deviation > _EPS else 1.0
    scores = np.array(
        [_weighted_index(fd, mean, std, chosen) for fd in feature_dicts], dtype=float
    )
    thresholds = tuple(
        float(t) for t in np.percentile(scores, [10, 20, 30, 40, 50, 60, 70, 80, 90])
    )
    densities = np.array(
        [float(fd.get("onset_density", _NAN)) for fd in feature_dicts], dtype=float
    )
    floor = (
        float(np.nanpercentile(densities, ONSET_FLOOR_PERCENTILE))
        if not np.all(np.isnan(densities))
        else None
    )
    return Calibration(
        mean=mean, std=std, weights=chosen, thresholds=thresholds,
        onset_floor=floor, n_tracks=len(feature_dicts), note=note,
    )


def distribution(levels: Sequence[int]) -> dict[str, int]:
    """How many tracks landed on each level, every level named even at zero."""
    counts = {str(level): 0 for level in range(LEVEL_MIN, LEVEL_MAX + 1)}
    for level in levels:
        counts[str(level)] = counts.get(str(level), 0) + 1
    return counts


# ---------------------------------------------------------------------------
# The library's state files
# ---------------------------------------------------------------------------


def write_json(path: Path, payload: Any) -> Path:
    """One state file, written whole or not at all, owner only."""
    config.atomic_write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), path
    )
    return path


def calibration_path(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY_CALIBRATION, cfg)


def undo_log_path(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY_UNDO_LOG, cfg)


def load_calibration(cfg: config.Config) -> Calibration | None:
    """The active calibration, or None when this library has none yet.

    An unreadable file REFUSES rather than reading as none, because a corrupt
    calibration and an absent one are different states, and folding the first
    into the second would restamp a whole library as though it had never been
    calibrated. The refusal names the remedy, which is to calibrate again, so
    a caller that let it through does not turn it into a defect report.
    """
    path = calibration_path(cfg)
    if not path.is_file():
        return None
    # AttributeError is in the tuple because ``from_json`` asks ``.items()`` of
    # three entries, and a file carrying a list where a mapping belongs raised
    # through the promise this docstring makes.
    try:
        return Calibration.from_json(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        raise refuse(
            "energy-calibration-unreadable",
            f"this library's energy calibration at {path} could not be read "
            f"({type(exc).__name__}: {exc}), so no level can be scored against it",
            steps=(
                "run `crate analyze calibrate LIBRARY_ROOT --recursive` again to "
                "rewrite it",
            ),
            origin=("analysis", "energy"),
            detail={"calibration": str(path), "kind": type(exc).__name__},
        ) from exc


def save_calibration(cfg: config.Config, calibration: Calibration) -> Path:
    return write_json(calibration_path(cfg), calibration.to_json())


def read_undo_log(cfg: config.Config) -> dict[str, str | None]:
    """Every file's pre-restamp tag TEXT, keyed by absolute path.

    Text rather than an integer, because the value being protected is whatever
    the file carried, and a tag another tool wrote as ``7/10`` would be
    recorded as null by an integer read and then be unrecoverable.
    """
    path = undo_log_path(cfg)
    if not path.is_file():
        return {}
    # AN UNREADABLE LOG REFUSES BY NAME. It is the only copy of every value a
    # restamp overwrote, so a truncated one must reach the person as a file to
    # repair, not as a defect report on every item of the next restamp, and a
    # record appended to a log that could not be read back would discard
    # whatever the unreadable text still held.
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError(f"expected a JSON object, found {type(loaded).__name__}")
        return {str(k): (None if v is None else str(v)) for k, v in loaded.items()}
    except (OSError, ValueError) as exc:
        raise refuse(
            "analysis-write-failed",
            f"the energy undo log at {path} could not be read ({type(exc).__name__}: "
            f"{exc}), and it is the only record of every value a restamp replaced, "
            f"so no restamp is recorded against it until it is repaired",
            steps=(
                "repair or move the undo log aside; it is a JSON object of file path "
                "to the energylevel text the file carried before its first restamp",
            ),
            origin=("analysis", "energy"),
            detail={"undo_log": str(path), "kind": type(exc).__name__},
        ) from exc


def record_previous(cfg: config.Config, path: Path, previous: str | None) -> bool:
    """Record a file's pre-restamp tag text, ONCE. Returns True when recorded.

    Never overwrites: the log holds the value the file carried before the FIRST
    restamp touched it, which is the only copy of that value anywhere, and a
    second restamp recording the first restamp's output would erase it.

    UNDER THE SIBLING LOCK. The driver lock is per job, so two restamp jobs
    over overlapping folders may run at once, and an unlocked read, modify,
    write would let each discard the other's entries.
    """
    target = undo_log_path(cfg)
    lock = config._exclusive_lock(target.with_name(target.name + ".lock"))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise refuse(
            "analysis-write-failed",
            f"the energy undo log could not be locked ({exc}), and recording a "
            f"previous value unlocked can discard another restamp's record",
            steps=("make the library state directory writable by this account",),
            origin=("analysis", "energy"),
            detail={"undo_log": str(target)},
        ) from exc
    try:
        log = read_undo_log(cfg)
        key = str(path)
        if key in log:
            return False
        log[key] = previous
        write_json(target, log)
        return True
    finally:
        lock.__exit__(None, None, None)


__all__ = [
    "BEATLESS_CAP",
    "Calibration",
    "DEFAULT_WEIGHTS",
    "FEATURE_ORDER",
    "SEGMENT_SECONDS",
    "STATUS_CALIBRATED",
    "STATUS_FEATURES_UNAVAILABLE",
    "STATUS_UNCALIBRATED",
    "bind_extractor",
    "calibrate",
    "calibration_path",
    "distribution",
    "extractor_bound",
    "features_from_path",
    "features_from_samples",
    "index",
    "level_for",
    "load_calibration",
    "measure",
    "read_undo_log",
    "record_previous",
    "save_calibration",
    "undo_log_path",
    "write_json",
]
