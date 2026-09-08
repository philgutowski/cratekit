"""Pass B: vocal score and finalize. Capped pool, model loaded once per worker.

The source system's kill was nine copies of a 300 megabyte model. The
ceiling here is 2, and the worker cost is one gibibyte, so plan_pool
can only go lower. A hand-built PoolPlan of nine would pass every
arithmetic test in U12 and still reproduce the kill.

THE PASS DECODES FOR ITSELF, FROM THE PATH THE LIGHT PASS SUPPLIES (U58). The
first version of this module read a ``wav`` key off the partial, and nothing
in the package ever set one, so every track with a loaded model scored
``voxlevel=0, voxgender="U"``: the fallback for "no samples" was shaped
exactly like "the model listened and heard nothing". Two fixes were honest.
The light pass could have carried its decoded samples across, and it does
not, for two reasons that both stand on their own. The head decodes at 22050
for key and tempo, and the model was trained at 32000, so the head's samples
fed to the model are a track heard at two thirds speed. And a partial that
carried samples would hold every track's audio in the parent at once, across
the pool boundary, which is the memory shape the package exists to avoid. So
this side moved: the partial carries a path, and the decoder here reads it at
the model's rate through a seam a test can bind a fake to.

A DECODE THAT FAILS IS REPORTED, NOT SCORED. ``vocal_active`` is False and
``vocal_reason`` says why, so the report and the tag write both see an
absence rather than a zero.
"""

from __future__ import annotations

from typing import Any, Callable

from cratekit.core import pool

VOCAL_WORKER_BYTES = 1024 ** 3
VOCAL_CEILING = 2

#: Why a track came back vocal inactive, so an absence is never silent.
REASON_MODEL_UNAVAILABLE = "vocal-model-unavailable"
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
REASON_HEAD_TERMINAL = "vocal-head-terminal"

_VOCAL_LOADER: Callable[[], Any] | None = None
_VOCAL_MODEL: Any = None
_VOCAL_FAILED = False
_DECODER: Callable[[Any], Any] | None = None


def bind_loader(loader: Callable[[], Any] | None) -> None:
    global _VOCAL_LOADER, _VOCAL_MODEL, _VOCAL_FAILED
    _VOCAL_LOADER = loader
    _VOCAL_MODEL = None
    _VOCAL_FAILED = False


def loader_bound() -> bool:
    """Whether a model loader is bound in this process, without naming which."""
    return _VOCAL_LOADER is not None


def bind_decoder(decoder: Callable[[Any], Any] | None) -> None:
    """Bind what turns a path into samples. None restores the shipped decoder."""
    global _DECODER
    _DECODER = decoder


def _load() -> Any:
    global _VOCAL_MODEL, _VOCAL_FAILED
    if _VOCAL_FAILED:
        return None
    if _VOCAL_MODEL is not None:
        return _VOCAL_MODEL
    loader = _VOCAL_LOADER
    if loader is None:
        return None
    try:
        _VOCAL_MODEL = loader()
    except Exception:
        _VOCAL_FAILED = True
        _VOCAL_MODEL = None
    return _VOCAL_MODEL


def _decode(path: Any) -> Any:
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)


def _inactive(result: dict[str, Any], reason: str) -> dict[str, Any]:
    result["vocal_active"] = False
    result["vocal_reason"] = reason
    result["voxlevel"] = None
    result["voxgender"] = None
    result["voxgenderconf"] = None
    return result


def analyse(partial: dict[str, Any]) -> dict[str, Any]:
    """Attach a vocal score when the model loaded and the track decoded.

    The samples come from ``partial["path"]`` through the bound decoder. THE
    PARTIAL IS NEVER ASKED FOR SAMPLES: ``tests/test_analysis.py`` pins that
    this function scores a partial carrying nothing but a path, and that no
    line here reads a ``wav`` key, because that key is the one the first
    version waited on for ever.
    """
    result = dict(partial)
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    samples = _decode(result.get("path"))
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
    from cratekit.analysis.vocal import infer_frames, reduce_frames

    score = reduce_frames(*infer_frames(model, samples))
    result["vocal_active"] = True
    result["vocal_reason"] = None
    result["voxlevel"] = int(round(score.presence))
    result["voxgender"] = score.gender
    result["voxgenderconf"] = int(round(100 * score.gender_conf))
    return result


def run(
    partials: list[dict[str, Any]], cost: int = VOCAL_WORKER_BYTES
) -> list[dict[str, Any]]:
    plan = pool.plan_pool(
        worker_bytes=cost, items=len(partials), ceiling=VOCAL_CEILING
    )
    return pool.map_workers(plan, analyse, partials)
