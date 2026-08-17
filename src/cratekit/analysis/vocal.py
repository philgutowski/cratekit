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
from dataclasses import dataclass
from typing import Any

import numpy as np

DEFAULT_FRAME_FLOOR = 0.05
DEFAULT_GENDER_MARGIN = 0.20
_EPS = 1e-9
DEFAULT_CHUNK_SAMPLES = 32000 * 8


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


def infer_frames(
    model: Any,
    wav: Any,
    *,
    chunk_samples: int | None = DEFAULT_CHUNK_SAMPLES,
    class_idx: tuple[int, int, int] = (0, 1, 2),
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
