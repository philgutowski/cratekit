"""Pass A: key, tempo, energy. Wide pool, no vocal model.

Every worker here is librosa-scale, tens of megabytes. The count comes
from plan_pool. A ProcessPoolExecutor of our own would be a second
answer to R23.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from cratekit.core import pool

LIGHT_WORKER_BYTES = 64 * 1024 * 1024

_DETECT: Callable[[Path], dict[str, Any] | None] | None = None


def bind_detect(detect: Callable[[Path], dict[str, Any] | None] | None) -> None:
    global _DETECT
    _DETECT = detect


def bound() -> bool:
    """Whether a detector is bound in this process, without naming which."""
    return _DETECT is not None


def init_pass(detect_name: str | None = None) -> None:
    """Spawn initializer. Children re-import this module and start unbound.

    Tests bind before map_workers. The in-process plan (one worker) keeps
    the bound callable. A spawned child would need an importable detector;
    the default detect.analyse_file is that function.
    """
    if detect_name == "default" or _DETECT is None:
        from cratekit.analysis.detect import analyse_file

        bind_detect(analyse_file)


def analyse(path: str) -> dict[str, Any]:
    """One file's cheap head. Importable, so spawn can find it by name."""
    target = Path(path)
    detector = _DETECT
    if detector is None:
        from cratekit.analysis.detect import analyse_file

        detector = analyse_file
    found = detector(target)
    if found is None:
        return {"path": path, "terminal": "skipped-no-key"}
    payload = {"path": path, "terminal": None}
    payload.update(found)
    payload["path"] = path
    return payload


def run(paths: list[str], cost: int = LIGHT_WORKER_BYTES) -> list[dict[str, Any]]:
    plan = pool.plan_pool(worker_bytes=cost, items=len(paths))
    return pool.map_workers(plan, analyse, paths)
