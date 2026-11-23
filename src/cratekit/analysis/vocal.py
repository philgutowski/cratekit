"""Vocal frame inference and the reduction to a presence score.

Chunks bound the activations a whole track forward pass would hold, and
torch.no_grad drops the autograd graph. The reduction is pure, arrays in and a
score out, and the model is injected so a test can prove chunked and unchunked
paths agree without loading PANNs.
"""

from __future__ import annotations

import contextlib
import io
from dataclasses import dataclass
from typing import Any

import numpy as np

DEFAULT_FRAME_FLOOR = 0.05
DEFAULT_GENDER_MARGIN = 0.20
_EPS = 1e-9

#: The rate the model was trained at, so the vocal pass decodes for itself
#: rather than borrowing the head's samples at another rate (U58).
MODEL_SAMPLE_RATE = 32000
DEFAULT_CHUNK_SAMPLES = MODEL_SAMPLE_RATE * 8

#: The shortest piece the network takes before its pooling raises. A shorter
#: tail is folded into the piece before it, and a shorter signal padded (R-371).
MIN_CHUNK_SAMPLES = MODEL_SAMPLE_RATE

#: The AudioSet classes the scorer reads, resolved to columns BY NAME from the
#: model's label table, with no numeric fallback (R-370).
TARGET_LABELS = ("Singing", "Male singing", "Female singing")


def decode(path: Any) -> np.ndarray | None:
    """The samples the model scores, decoded at the model's own rate.

    None when the extra is absent or the file cannot be decoded, which the
    caller reports as vocal inactive, never a zero (U58). Raises
    :class:`cratekit.analysis.decode.DecoderMissing` for a file only ffmpeg
    could decode on a machine without it (U263).
    """
    try:
        import librosa  # noqa: F401 - asked for so its absence is the extra's absence
    except ImportError:
        return None
    from cratekit.analysis import decode as decoder

    try:
        wav, _rate = decoder.load(path, MODEL_SAMPLE_RATE)
    except decoder.DecoderMissing:
        raise
    except Exception:
        return None
    if wav is None or wav.size == 0:
        return None
    return np.asarray(wav, dtype=np.float32)


def default_loader() -> Any:
    """Load the pretrained FRAME level model, behind the extra.

    ``SoundEventDetection`` returns one row per frame, what ``infer_frames``
    reduces (R-370). Raises, never None, when anything is missing, which
    ``vocals._load`` records; checked HERE because the library's answer to a
    missing checkpoint is a shell out to wget.
    """
    from cratekit.analysis import vocals as scoring

    missing = scoring.missing_requirement()
    if missing is not None:
        raise FileNotFoundError(missing)
    from panns_inference import SoundEventDetection

    # The wrapper prints its checkpoint path and device to stdout on
    # construction, and stdout is where the JSON envelope goes.
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")


def class_indices(model: Any) -> tuple[int, int, int]:
    """The columns of ``TARGET_LABELS`` in the model's frame output.

    Resolved by name from the wrapper's label table; a model with no table or
    a table missing a target raises rather than scoring the wrong column.
    """
    labels = getattr(model, "labels", None)
    if labels is None:
        raise ValueError(
            "the vocal model carries no label table, so its columns cannot be "
            "resolved by name and it will not be scored by number"
        )
    names = [str(name) for name in labels]
    try:
        first, second, third = (names.index(target) for target in TARGET_LABELS)
    except ValueError as exc:
        raise ValueError(
            f"the vocal model's label table does not name all of {TARGET_LABELS}"
        ) from exc
    return (first, second, third)


@dataclass(frozen=True)
class VocalScore:
    presence: float
    gender: str
    gender_conf: float
    coverage: float


def _no_grad():
    try:
        import torch

        return torch.no_grad()
    except ImportError:
        return contextlib.nullcontext()


def _as_batch(wav: Any) -> np.ndarray:
    batch = np.asarray(wav, dtype=np.float32)
    if batch.ndim == 1:
        batch = batch[None, :]
    return batch


def _without_a_short_tail(slices: list[np.ndarray], *, floor: int) -> list[np.ndarray]:
    """Fold a last piece shorter than ``floor`` into the one before it.

    A lone piece shorter than the floor is padded with silence to it instead.
    """
    if not slices or floor <= 0:
        return slices
    last = slices[-1]
    if int(last.shape[-1]) >= floor:
        return slices
    if len(slices) == 1:
        pad = floor - int(last.shape[-1])
        return [np.concatenate([last, np.zeros((last.shape[0], pad), last.dtype)], axis=-1)]
    merged = np.concatenate([slices[-2], last], axis=-1)
    return [*slices[:-2], merged]


def infer_frames(
    model: Any,
    wav: Any,
    *,
    chunk_samples: int | None = DEFAULT_CHUNK_SAMPLES,
    class_idx: tuple[int, int, int] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (vocals, male, female) frame arrays for wav.

    chunk_samples None is the unchunked path, kept so a fixture can prove the
    chunked one agrees. Both run under no_grad with the same floor, and frames
    the padding added are trimmed off again. ``class_idx`` None resolves the
    columns from the label table (R-370).
    """
    if class_idx is None:
        class_idx = class_indices(model)
    batch = _as_batch(wav)
    width = int(batch.shape[-1])
    if chunk_samples is None or width <= chunk_samples:
        slices = [batch]
    else:
        slices = [
            batch[:, start : start + chunk_samples]
            for start in range(0, width, chunk_samples)
        ]
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)
    slices = _without_a_short_tail(slices, floor=floor)
    padded = sum(int(piece.shape[-1]) for piece in slices)
    parts: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
    with _no_grad():
        for piece in slices:
            framewise = np.asarray(model.inference(piece))
            if framewise.ndim == 3:
                framewise = framewise[0]
            parts.append(
                (
                    framewise[:, class_idx[0]],
                    framewise[:, class_idx[1]],
                    framewise[:, class_idx[2]],
                )
            )
    vocals = np.concatenate([p[0] for p in parts], axis=0)
    male = np.concatenate([p[1] for p in parts], axis=0)
    female = np.concatenate([p[2] for p in parts], axis=0)
    if padded > width and vocals.size:
        keep = max(1, int(round(vocals.size * width / padded)))
        vocals, male, female = vocals[:keep], male[:keep], female[:keep]
    return vocals, male, female


def presence_score(vocals: np.ndarray, *, frame_floor: float = DEFAULT_FRAME_FLOOR) -> float:
    """The percentage of frames whose Singing score reaches ``frame_floor``.

    Coverage, not loudness. On a dense electronic mix the Singing score often
    never reaches the floor, a 0 the model meant (U171,
    ``tests/test_vocal_zeros.py``).
    """
    series = np.asarray(vocals, dtype=float)
    if series.size == 0:
        return 0.0
    return 100.0 * float((series >= frame_floor).mean())


def gender_call(
    vocals: np.ndarray,
    male: np.ndarray,
    female: np.ndarray,
    *,
    frame_floor: float = DEFAULT_FRAME_FLOOR,
    margin: float = DEFAULT_GENDER_MARGIN,
) -> tuple[str, float]:
    singing = np.asarray(vocals, dtype=float)
    men = np.asarray(male, dtype=float)
    women = np.asarray(female, dtype=float)
    if singing.size == 0:
        return ("U", 0.0)
    active = singing >= frame_floor
    if not active.any():
        return ("U", 0.0)
    male_mean = float(men[active].mean())
    female_mean = float(women[active].mean())
    total = male_mean + female_mean
    if total <= _EPS:
        return ("U", 0.0)
    dominance = abs(male_mean - female_mean) / total
    if dominance < margin:
        return ("U", dominance)
    return ("M" if male_mean > female_mean else "F", dominance)


def reduce_frames(
    vocals: np.ndarray,
    male: np.ndarray,
    female: np.ndarray,
    *,
    frame_floor: float = DEFAULT_FRAME_FLOOR,
    margin: float = DEFAULT_GENDER_MARGIN,
) -> VocalScore:
    singing = np.asarray(vocals, dtype=float)
    coverage = float((singing >= frame_floor).mean()) if singing.size else 0.0
    presence = presence_score(singing, frame_floor=frame_floor)
    gender, conf = gender_call(
        singing, male, female, frame_floor=frame_floor, margin=margin
    )
    return VocalScore(
        presence=presence, gender=gender, gender_conf=conf, coverage=coverage
    )
