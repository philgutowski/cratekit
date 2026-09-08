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

librosa and numpy are imported inside the functions that need them, so a slim
install can import this module and read a calibration file.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from cratekit.core import config

#: Fixed column order, so a feature vector is deterministic across runs.
FEATURE_ORDER: tuple[str, ...] = (
    "rms_mean", "rms_std", "rms_dr", "rms_crest", "loudness_db",
    "centroid_mean", "centroid_std", "rolloff_mean", "rolloff_std",
    "bandwidth_mean", "bandwidth_std", "flatness_mean", "flatness_std",
    "flux_mean", "flux_std", "zcr_mean", "zcr_std",
    "onset_density", "onset_std", "beat_concentration", "percussive_fraction",
    "low_band_ratio", "mid_band_ratio", "high_band_ratio", "high_low_tilt", "tempo",
)

#: Signed weights on z-scored features. Positive reads as more energy. A feature
#: absent here carries no weight and is still measured, so a later re-weighting
#: needs no re-analysis.
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

LEVEL_MIN = 1
LEVEL_MAX = 10
#: The cap the beatless guard applies: the top of the low band.
BEATLESS_CAP = 3
#: The percentile of onset density below which a track is treated as beatless.
ONSET_FLOOR_PERCENTILE = 2.0

STATUS_CALIBRATED = "calibrated"
STATUS_UNCALIBRATED = "uncalibrated"
STATUS_FEATURES_UNAVAILABLE = "features-unavailable"

STATE_KEY_CALIBRATION = "energy_calibration"
STATE_KEY_UNDO_LOG = "energy_undo_log"

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
    method: str = "decile"
    note: str = ""
    feature_order: tuple[str, ...] = field(default=FEATURE_ORDER)

    def to_json(self) -> dict[str, Any]:
        return {
            "feature_order": list(self.feature_order),
            "mean": dict(self.mean),
            "std": dict(self.std),
            "weights": dict(self.weights),
            "thresholds": list(self.thresholds),
            "onset_floor": self.onset_floor,
            "n_tracks": self.n_tracks,
            "method": self.method,
            "note": self.note,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Calibration:
        thresholds = tuple(float(t) for t in data["thresholds"])
        if len(thresholds) != LEVEL_MAX - LEVEL_MIN:
            raise ValueError(
                f"an energy calibration carries {LEVEL_MAX - LEVEL_MIN} cut points, "
                f"this one carries {len(thresholds)}"
            )
        floor = data.get("onset_floor")
        return cls(
            mean={str(k): float(v) for k, v in data["mean"].items()},
            std={str(k): float(v) for k, v in data["std"].items()},
            weights={str(k): float(v) for k, v in data["weights"].items()},
            thresholds=thresholds,
            onset_floor=None if floor is None else float(floor),
            n_tracks=int(data["n_tracks"]),
            method=str(data.get("method", "decile")),
            note=str(data.get("note", "")),
            feature_order=tuple(data.get("feature_order") or FEATURE_ORDER),
        )


# ---------------------------------------------------------------------------
# Measuring
# ---------------------------------------------------------------------------


def _central(samples: Any, rate: int, segment: float | None) -> Any:
    if segment is None:
        return samples
    width = int(segment * rate)
    if samples.shape[-1] <= width:
        return samples
    start = (samples.shape[-1] - width) // 2
    return samples[start : start + width]


def features_from_samples(
    samples: Any, rate: int, *, tempo: float | None = None, segment: float | None = SEGMENT_SECONDS
) -> dict[str, float] | None:
    """The ordered feature vector for decoded mono samples, or None.

    Takes samples rather than a path so the head pass, which has already
    decoded the track for key and tempo, does not decode it a second time.
    ``tempo`` is the head's own reading when it has one.
    """
    try:
        import librosa
        import numpy as np
    except ImportError:
        return None
    try:
        y = _central(np.asarray(samples, dtype=np.float32), rate, segment)
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
            harmonic, percussive = librosa.effects.hpss(y)
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

        if tempo is None:
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


def features_from_path(path: Path, *, rate: int = 22050, tempo: float | None = None) -> dict[str, float] | None:
    """Decode ``path`` and measure it. The restamp path, which has no head pass."""
    try:
        import librosa
    except ImportError:
        return None
    try:
        samples, decoded_rate = librosa.load(str(path), sr=rate, mono=True)
    except Exception:
        return None
    return features_from_samples(samples, int(decoded_rate), tempo=tempo)


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


def _is_nan(value: float) -> bool:
    return value != value


def index(features: Mapping[str, float], calibration: Calibration) -> float:
    """The weighted sum of z-scored features. A missing feature imputes to z=0."""
    total = 0.0
    for name, weight in calibration.weights.items():
        if weight == 0:
            continue
        value = float(features.get(name, _NAN))
        mean = calibration.mean.get(name, 0.0)
        deviation = calibration.std.get(name, 1.0) or 1.0
        z = 0.0 if _is_nan(value) else (value - mean) / deviation
        total += weight * z
    return float(total)


def level_for(features: Mapping[str, float], calibration: Calibration) -> int:
    """The level 1 to 10 for one track, with the beatless cap applied."""
    score = index(features, calibration)
    level = LEVEL_MIN + sum(1 for cut in calibration.thresholds if score >= cut)
    level = max(LEVEL_MIN, min(LEVEL_MAX, level))
    if calibration.onset_floor is not None:
        density = float(features.get("onset_density", math.inf))
        if not _is_nan(density) and density < calibration.onset_floor:
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
    reference = Calibration(
        mean=mean, std=std, weights=chosen, thresholds=(0.0,) * 9,
        onset_floor=None, n_tracks=len(feature_dicts),
    )
    scores = np.array([index(fd, reference) for fd in feature_dicts], dtype=float)
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


def calibration_path(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY_CALIBRATION, cfg)


def undo_log_path(cfg: config.Config) -> Path:
    return config.state_path(STATE_KEY_UNDO_LOG, cfg)


def load_calibration(cfg: config.Config) -> Calibration | None:
    """The active calibration, or None when this library has none yet.

    An unreadable file RAISES rather than reading as none, because a corrupt
    calibration and an absent one are different states with different
    remedies, and folding the first into the second would restamp a whole
    library as though it had never been calibrated.
    """
    path = calibration_path(cfg)
    if not path.is_file():
        return None
    return Calibration.from_json(json.loads(path.read_text(encoding="utf-8")))


def save_calibration(cfg: config.Config, calibration: Calibration) -> Path:
    path = calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text(
        json.dumps(calibration.to_json(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def read_undo_log(cfg: config.Config) -> dict[str, int | None]:
    path = undo_log_path(cfg)
    if not path.is_file():
        return {}
    loaded = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): (None if v is None else int(v)) for k, v in loaded.items()}


def record_previous(cfg: config.Config, path: Path, previous: int | None) -> bool:
    """Record a file's pre-restamp level, ONCE. Returns True when it was recorded.

    Never overwrites: the log holds the value the file carried before the FIRST
    restamp touched it, which is the only copy of that value anywhere, and a
    second restamp recording the first restamp's output would erase it.
    """
    log = read_undo_log(cfg)
    key = str(path)
    if key in log:
        return False
    log[key] = previous
    target = undo_log_path(cfg)
    config._mkdir_private(target.parent)
    target.write_text(json.dumps(log, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True


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
]
