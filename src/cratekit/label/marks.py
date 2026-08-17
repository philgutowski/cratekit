"""Per-label last-pulled years. Audit records. They are not a date floor.

KTD11: scope comes from newest-N plus owned-dedup. A year written here is
what a status view reports, and nothing in the sweep reads it to filter.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Mapping

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

MARKS_VERSION = 1


def _unusable(path, what: str) -> CratekitError:
    return refuse(
        "label-watermark-unusable",
        f"the per-label watermark at {path.name} could not be read ({what}), "
        f"so treating it as unset would hide that a sweep already completed",
        steps=("repair or restore the per-label watermark before running a sweep",),
        scope=Scope.RUN,
        origin=("label.marks",),
        detail={"problem": what, "path": str(path)},
    )


def _load(cfg: config.Config) -> dict[str, str]:
    path = config.state_path("label_watermarks", cfg)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _unusable(path, "it could not be opened") from exc
    except ValueError as exc:
        raise _unusable(path, "it is not JSON") from exc
    if not isinstance(raw, Mapping):
        raise _unusable(path, f"the document is a {type(raw).__name__}, not a map")
    version = raw.get("version")
    if version not in (None, MARKS_VERSION):
        raise _unusable(
            path, f"it says version {version!r} and this build writes {MARKS_VERSION}"
        )
    records = raw.get("labels", raw)
    if not isinstance(records, Mapping):
        raise _unusable(path, "it has no labels map")
    found: dict[str, str] = {}
    for key, value in records.items():
        if isinstance(value, Mapping):
            year = value.get("last_pulled")
        else:
            year = value
        if year:
            found[str(key)] = str(year)
    return found


def _write(cfg: config.Config, records: Mapping[str, str]) -> None:
    path = config.state_path("label_watermarks", cfg)
    payload: dict[str, Any] = {
        "version": MARKS_VERSION,
        "labels": {key: {"last_pulled": year} for key, year in sorted(records.items())},
    }
    config.atomic_write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        path,
    )


def read(cfg: config.Config, label_id: str) -> str | None:
    """The last-pulled year for ``label_id``, or None if never recorded."""
    return _load(cfg).get(label_id)


def advance(cfg: config.Config, label_id: str, *, year: str | None = None) -> str:
    """Record that this label was swept. Does not change the next scope."""
    recorded = year or str(datetime.now().year)
    lock = config._exclusive_lock(config.state_path("label_watermarks_lock", cfg))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise refuse(
            "label-watermark-unusable",
            f"the per-label watermark could not be locked ({exc}), and "
            f"advancing it unlocked discards a neighbour sweep's year",
            steps=("make the library state directory writable by this account",),
            scope=Scope.RUN,
            origin=("label.marks",),
        ) from exc
    try:
        records = _load(cfg)
        records[label_id] = recorded
        _write(cfg, records)
        return recorded
    finally:
        lock.__exit__(None, None, None)
