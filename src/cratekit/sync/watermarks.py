"""Per-source audit records. They advance only on clean completion.

The document is library-scoped and coupled (R25, R30, KTD21). A cursor is a
record of how far a source got, not a floor the next increment filters by.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.sync import sources

WATERMARK_VERSION = 1


@dataclass(frozen=True, slots=True)
class SourceWatermark:
    """One source's last clean completion, bound to the library it describes."""

    source_id: str
    cursor: str
    items: int
    recorded: str
    library_id: str

    def to_json(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "cursor": self.cursor,
            "items": self.items,
            "recorded": self.recorded,
            "library_id": self.library_id,
        }


class WatermarkStore:
    """The locked document of every source cursor for one library."""

    def __init__(self, cfg: config.Config) -> None:
        self.cfg = cfg
        self.path: Path = config.state_path("source_watermarks", cfg)
        self.lock_path: Path = config.state_path("source_watermarks_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-watermark-unusable",
            f"the source watermark at {self.path.name} could not be read "
            f"({what}), so how far each increment has got is unknown; treating "
            f"it as unset would make the next run look like a first run",
            steps=("repair or restore the source watermark before running sync",),
            scope=Scope.RUN,
            origin=("sync.watermarks",),
            detail={"problem": what, "path": str(self.path)},
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        lock = config._exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "sync-watermark-unusable",
                f"the source watermark could not be locked ({exc}), and "
                f"advancing it unlocked discards whatever a second increment is "
                f"recording at the same time",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=("sync.watermarks",),
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            lock.__exit__(None, None, None)

    def _load(self) -> dict[str, SourceWatermark]:
        if not self.path.exists():
            return {}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> dict[str, SourceWatermark]:
        if not isinstance(raw, Mapping):
            raise self._unusable(
                f"the document is a {type(raw).__name__}, not a watermark map"
            )
        version = raw.get("version")
        if version != WATERMARK_VERSION:
            raise self._unusable(
                f"it says version {version!r} and this build writes {WATERMARK_VERSION}"
            )
        records = raw.get("sources")
        if not isinstance(records, Mapping):
            raise self._unusable("it has no sources map")
        found: dict[str, SourceWatermark] = {}
        for key, value in records.items():
            if not isinstance(value, Mapping):
                raise self._unusable(f"source {key!r} is not an object")
            source_id = str(value.get("source_id") or key)
            cursor = value.get("cursor")
            items = value.get("items")
            library_id = value.get("library_id")
            if not isinstance(cursor, str) or not cursor:
                raise self._unusable(f"source {source_id!r} names no cursor")
            if isinstance(items, bool) or not isinstance(items, int):
                raise self._unusable(f"source {source_id!r} has a non-integer items count")
            if not isinstance(library_id, str) or not library_id:
                raise self._unusable(f"source {source_id!r} names no library")
            if library_id != self.cfg.library.volume_id:
                raise self._unusable(
                    f"source {source_id!r} was recorded against library "
                    f"{library_id} and this library is {self.cfg.library.volume_id}"
                )
            found[source_id] = SourceWatermark(
                source_id=source_id,
                cursor=cursor,
                items=items,
                recorded=str(value.get("recorded") or ""),
                library_id=library_id,
            )
        return found

    def _write(self, records: Mapping[str, SourceWatermark]) -> None:
        payload = {
            "version": WATERMARK_VERSION,
            "sources": {key: mark.to_json() for key, mark in sorted(records.items())},
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            self.path,
        )

    def read(self, source_id: str) -> SourceWatermark | None:
        """The last clean completion for ``source_id``, or None if never completed."""
        return self._load().get(source_id)

    def all(self) -> dict[str, SourceWatermark]:
        return self._load()

    def advance(
        self,
        source_id: str,
        *,
        cursor: str,
        items: int,
        library_id: str,
        now: str | None = None,
    ) -> SourceWatermark:
        """Record a clean completion. Callers must not call this on a shortfall."""
        mark = SourceWatermark(
            source_id=source_id,
            cursor=cursor,
            items=items,
            recorded=now or timestamp(),
            library_id=library_id,
        )
        with self._locked():
            records = self._load()
            records[source_id] = mark
            self._write(records)
        return mark


def status_rows(cfg: config.Config) -> tuple[dict[str, str], ...]:
    """One row per declared source, plus any extra cursor the document holds.

    Derived from ``sources.DECLARED`` union the document, so a later source
    added in one place cannot go unreported (P3).
    """
    store = WatermarkStore(cfg)
    records = store.all()
    ids = list(sources.DECLARED)
    for extra in records:
        if extra not in ids:
            ids.append(extra)
    rows: list[dict[str, str]] = []
    for source_id in ids:
        mark = records.get(source_id)
        if mark is None:
            rows.append(
                {
                    "source_id": source_id,
                    "state": "never",
                    "detail": "no clean increment has completed",
                }
            )
        else:
            rows.append(
                {
                    "source_id": source_id,
                    "state": "completed",
                    "detail": (
                        f"cursor {mark.cursor}, {mark.items} items, "
                        f"recorded {mark.recorded}"
                    ),
                }
            )
    return tuple(rows)
