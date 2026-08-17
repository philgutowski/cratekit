"""Pass B: vocal score and finalize. Capped pool, model loaded once per worker.

The source system's kill was nine copies of a 300 megabyte model. The
ceiling here is 2, and the worker cost is one gibibyte, so plan_pool
can only go lower. A hand-built PoolPlan of nine would pass every
arithmetic test in U12 and still reproduce the kill.
"""

from __future__ import annotations

from typing import Any, Callable

from cratekit.core import pool

VOCAL_WORKER_BYTES = 1024 ** 3
VOCAL_CEILING = 2

_VOCAL_LOADER: Callable[[], Any] | None = None
_VOCAL_MODEL: Any = None
_VOCAL_FAILED = False


def bind_loader(loader: Callable[[], Any] | None) -> None:
    global _VOCAL_LOADER, _VOCAL_MODEL, _VOCAL_FAILED
    _VOCAL_LOADER = loader
    _VOCAL_MODEL = None
    _VOCAL_FAILED = False


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


def analyse(partial: dict[str, Any]) -> dict[str, Any]:
    """Attach a vocal score when the model loaded, otherwise leave it inactive."""
    result = dict(partial)
    if result.get("terminal") is not None:
        result["vocal_active"] = False
        result["voxlevel"] = None
        result["voxgender"] = None
        return result
    model = _load()
    if model is None:
        result["vocal_active"] = False
        result["voxlevel"] = None
        result["voxgender"] = None
        return result
    from cratekit.analysis.vocal import infer_frames, reduce_frames

    wav = result.get("wav")
    if wav is None:
        result["vocal_active"] = True
        result["voxlevel"] = 0
        result["voxgender"] = "U"
        return result
    score = reduce_frames(*infer_frames(model, wav))
    result["vocal_active"] = True
    result["voxlevel"] = int(round(score.presence))
    result["voxgender"] = score.gender
    return result


def run(
    partials: list[dict[str, Any]], cost: int = VOCAL_WORKER_BYTES
) -> list[dict[str, Any]]:
    plan = pool.plan_pool(
        worker_bytes=cost, items=len(partials), ceiling=VOCAL_CEILING
    )
    return pool.map_workers(plan, analyse, partials)
