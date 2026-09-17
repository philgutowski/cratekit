"""Vocal frame inference and the reduction to a presence score.

Chunked inference under a no-gradient context is the memory lever the
source system named and did not land. A whole-track forward pass holds
activations for the entire file. Chunks bound that tensor. torch.no_grad
drops the autograd graph that the source pass never needed.

This module is pure on the reduction side: numpy arrays in, a score out.
The model object is injected so a test can prove chunked and unchunked
paths agree without loading PANNs.
"""

from __future__ import annotations

import contextlib
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

DEFAULT_FRAME_FLOOR = 0.05
DEFAULT_GENDER_MARGIN = 0.20
_EPS = 1e-9

#: The rate the model was trained at. The light pass decodes at 22050 for key
#: and tempo, and a signal at that rate fed to this model is a signal the model
#: hears at two thirds speed, so the vocal pass decodes for itself at its own
#: rate rather than borrowing the head's samples (U58).
MODEL_SAMPLE_RATE = 32000
DEFAULT_CHUNK_SAMPLES = MODEL_SAMPLE_RATE * 8

#: The shortest piece the network will take. Its time axis is pooled by two
#: five times, so a piece under about a third of a second pools to nothing
#: and the forward pass raises. A tail shorter than this is folded into the
#: piece before it, and a whole signal shorter than this is padded, because
#: the alternative was one track in thirty six failing on the length of its
#: last quarter second (R-371).
MIN_CHUNK_SAMPLES = MODEL_SAMPLE_RATE

#: The AudioSet leaf classes the scorer reads, resolved to columns BY NAME from
#: the model's own label table. Columns 0, 1 and 2 of that table are Speech,
#: Male speech and Female speech, which is what the first version read on a
#: real model, so a sung lead scored as an instrumental (R-370).
TARGET_LABELS = ("Singing", "Male singing", "Female singing")

#: What a model with no label table is read as: the first three columns. That
#: is the fixture path, and every fake in the suite fills those columns.
FIXTURE_CLASS_IDX = (0, 1, 2)

#: The frame level checkpoint the source system scored the library with. It is
#: named here, rather than left to the library's default, because the library
#: shells out to wget for a checkpoint it cannot find and this machine has no
#: wget. The loader refuses before that shell out can happen.
CHECKPOINT = Path.home() / "panns_data" / "Cnn14_DecisionLevelMax.pth"

#: The AudioSet label table the library reads AT IMPORT, and fetches the same
#: way when it is absent. Checked before the import for the same reason.
LABELS = Path.home() / "panns_data" / "class_labels_indices.csv"

#: The library's own floor: a file smaller than this is treated as a broken
#: download and fetched again, which is the shell out above.
CHECKPOINT_MIN_BYTES = 300_000_000


def decode(path: Any) -> np.ndarray | None:
    """The samples the model scores, decoded at the model's own rate.

    None when the extra is absent or the file cannot be decoded, and the CALLER
    decides what None means. ``vocals.analyse`` reports it as vocal inactive
    with the reason, never as a score of zero: a zero is a track the model
    heard and found instrumental, and a track the model never heard is not
    that (U58, the wav defect).

    librosa is imported inside the function so a slim install can still import
    the package.
    """
    try:
        import librosa
    except ImportError:
        return None
    try:
        wav, _rate = librosa.load(str(path), sr=MODEL_SAMPLE_RATE, mono=True)
    except Exception:
        return None
    if wav is None or wav.size == 0:
        return None
    return np.asarray(wav, dtype=np.float32)


def checkpoint_ready(path: Path | None = None) -> bool:
    """Whether the frame level checkpoint is on disk and not a truncated fetch.

    The path is read at call time, not bound as a default, so a test can point
    the module at a scratch file.
    """
    target = CHECKPOINT if path is None else path
    try:
        return target.is_file() and target.stat().st_size >= CHECKPOINT_MIN_BYTES
    except OSError:
        return False


def labels_ready(path: Path | None = None) -> bool:
    """Whether the label table the library reads at import is on disk."""
    target = LABELS if path is None else path
    try:
        return target.is_file() and target.stat().st_size > 0
    except OSError:
        return False


def default_loader() -> Any:
    """Load the pretrained FRAME level model, behind the extra.

    ``SoundEventDetection`` is the wrapper whose ``inference`` returns one row
    per frame, which is what ``infer_frames`` reduces. ``AudioTagging``, the
    wrapper the first version built, returns a clip level pair, has no frame
    output, and defaults to a different checkpoint (R-370).

    Raises when the extra is absent or the checkpoint is not on disk, which
    ``vocals._load`` records as a failed load and reports as vocal inactive.
    It does not return None, because a loader that returns None on a missing
    extra and a loader that returns None because the checkpoint is corrupt
    are the same None to the caller. The checkpoint is checked HERE, before
    the library is asked for it, because the library's answer to a missing
    checkpoint is a shell out to wget.
    """
    if not labels_ready():
        raise FileNotFoundError(
            f"the vocal model's label table is not at {LABELS}; place "
            f"class_labels_indices.csv there before scoring"
        )
    if not checkpoint_ready():
        raise FileNotFoundError(
            f"the vocal model checkpoint is not at {CHECKPOINT}, or is smaller "
            f"than {CHECKPOINT_MIN_BYTES} bytes; place Cnn14_DecisionLevelMax.pth "
            f"there before scoring"
        )
    from panns_inference import SoundEventDetection

    # The wrapper prints its checkpoint path and device to stdout on
    # construction, and stdout is where the JSON envelope goes.
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(CHECKPOINT), device="cpu")


def class_indices(model: Any) -> tuple[int, int, int]:
    """The columns of ``TARGET_LABELS`` in the model's frame output.

    Resolved by name from the label table the wrapper carries, so the columns
    follow the model rather than a number typed here. A model with no table is
    a fixture and is read at ``FIXTURE_CLASS_IDX``. A table that does not name
    a target raises, and ``vocals.analyse`` reports that as inference failed
    rather than scoring the wrong column.
    """
    labels = getattr(model, "labels", None)
    if labels is None:
        return FIXTURE_CLASS_IDX
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

    A lone piece shorter than the floor is padded with silence to the floor
    instead, so a very short clip still reaches the network as something it
    can pool.
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
    class_idx: tuple[int, int, int] = FIXTURE_CLASS_IDX,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (vocals, male, female) frame arrays for wav.

    chunk_samples None is the unchunked path, kept so a fixture can prove
    the chunked path agrees with it. A positive chunk size walks the
    signal and concatenates frames. Both paths run under no_grad.
    """
    batch = _as_batch(wav)
    width = int(batch.shape[-1])
    if chunk_samples is None or width <= chunk_samples:
        slices = [batch]
    else:
        slices = [
            batch[:, start : start + chunk_samples]
            for start in range(0, width, chunk_samples)
        ]
    slices = _without_a_short_tail(slices, floor=min(MIN_CHUNK_SAMPLES, chunk_samples or width))
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
    return vocals, male, female


def presence_score(vocals: np.ndarray, *, frame_floor: float = DEFAULT_FRAME_FLOOR) -> float:
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
