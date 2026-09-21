"""Per-source audit records. They advance only on clean completion.

The document is library-scoped and coupled (R25, R30, KTD21). A cursor is a
record of how far a source got, not a floor the next increment filters by.

**THE PLAYLISTS CURSOR IS A SET, NOT A POSITION (U64).** A labels increment has
a newest item and a cursor naming it. A playlists sweep does not: each account
playlist is swept once, in no order, and what the next pass needs is WHICH
playlists completed. ``swept`` holds those provider identifiers, and it is the
one record a later pass does filter by: ``sync.playlists`` excludes those ids.
It is an exclusion by identity, never a date floor. It is optional
on every record, so a document written before it existed still reads, and it is
written only when it has something in it. It never holds a title (D5).
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

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
    #: The identifiers a set shaped source has completed. Empty for every other.
    swept: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "source_id": self.source_id,
            "cursor": self.cursor,
            "items": self.items,
            "recorded": self.recorded,
            "library_id": self.library_id,
        }
        if self.swept:
            record["swept"] = list(self.swept)
        return record


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
            swept = value.get("swept", [])
            if not isinstance(swept, list) or not all(
                isinstance(identity, str) and identity for identity in swept
            ):
                raise self._unusable(
                    f"source {source_id!r} has a swept list that is not identifiers"
                )
            found[source_id] = SourceWatermark(
                source_id=source_id,
                cursor=cursor,
                items=items,
                recorded=str(value.get("recorded") or ""),
                library_id=library_id,
                swept=tuple(swept),
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

    def record_swept(
        self,
        source_id: str,
        identities: Sequence[str],
        *,
        library_id: str,
        now: str | None = None,
    ) -> SourceWatermark | None:
        """Add completed identifiers to a set shaped source's cursor.

        NOTHING TO RECORD RECORDS NOTHING, and returns the record as it stands.
        A pass that swept nothing is not a clean completion of anything, and
        rewriting the record would move its timestamp as if it were (R-135).

        The union keeps first seen order and is taken UNDER THE LOCK, so two
        passes recording at once both land. ``cursor`` names the last identifier
        this call added and ``items`` counts the whole set.
        """
        wanted = [str(identity) for identity in identities if str(identity)]
        with self._locked():
            records = self._load()
            existing = records.get(source_id)
            if not wanted:
                return existing
            merged = list(existing.swept) if existing is not None else []
            known = set(merged)
            for identity in wanted:
                if identity not in known:
                    known.add(identity)
                    merged.append(identity)
            mark = SourceWatermark(
                source_id=source_id,
                cursor=wanted[-1],
                items=len(merged),
                recorded=now or timestamp(),
                library_id=library_id,
                swept=tuple(merged),
            )
            records[source_id] = mark
            self._write(records)
        return mark


def status_rows(cfg: config.Config) -> tuple[dict[str, str], ...]:
    """One row per declared source, plus any extra cursor the document holds.

    Derived from ``sources.DECLARED`` union the document, so a later source
    added in one place cannot go unreported (P3).

    A declared source whose spec carries ``no_cursor`` is ``unrecorded``, never
    ``never`` (R-263): nothing writes its record, so the absence says nothing
    about whether it ran. A record an earlier build left for it is reported as
    stale rather than as its last completion, since that record no longer moves.
    """
    store = WatermarkStore(cfg)
    records = store.all()
    no_cursor = {spec.source_id: spec.no_cursor for spec in sources.SPECS if spec.no_cursor}
    ids = list(sources.DECLARED)
    for extra in records:
        if extra not in ids:
            ids.append(extra)
    rows: list[dict[str, str]] = []
    for source_id in ids:
        mark = records.get(source_id)
        reason = no_cursor.get(source_id)
        if reason is not None:
            detail = reason
            if mark is not None:
                detail += (
                    f"; a cursor an earlier build recorded {mark.recorded} "
                    f"no longer moves"
                )
            rows.append({"source_id": source_id, "state": "unrecorded", "detail": detail})
        elif mark is None:
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
