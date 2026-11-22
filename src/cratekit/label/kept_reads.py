"""A full label build's release reads, kept across runs (R-1091).

A full build reads two provider calls a release, hours on a large label. This
store keeps each read per label for :data:`KEPT_FOR`, so a stopped build
resumes and the apply run reads nothing again. It keeps each track's
identifier, playability, artist and title (U243; a read without the words is
read again) and the release's year, or that it is gone; a failed read is never
kept. Written whole as it goes, a refused write is ``unkept`` and said, never
raised. One that cannot be read refuses, ``label-playlists-reads-unusable``;
deleting it is safe. One document per label under ``label_crawl_cache``.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import tombstoned

#: How long a kept read stays true before a build reads the release again.
KEPT_FOR = timedelta(days=7)

#: New reads between two writes of the document, what a kill loses at most.
FLUSH_EVERY = 50

#: The document's version. Any other refuses rather than being read.
VERSION = 1

#: The file inside the label's own directory of the crawl cache.
FILE_NAME = "reads.json"

UNUSABLE = "label-playlists-reads-unusable"

_ORIGIN = ("label.playlists",)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


#: The clock the store reads, a module attribute so a suite can age a read.
clock: Callable[[], datetime] = _utcnow


def path_for(label_id: str) -> Path:
    return config.state_path("label_crawl_cache") / label_id / FILE_NAME


@dataclass(frozen=True, slots=True)
class KeptTrack:
    """One track as a kept read carries it: what the plan reads off a row."""

    id: str
    available: bool
    #: The row's words as ``tombstoned`` reads them, ``None`` in an older read (U243).
    artist: str | None = None
    title: str | None = None


@dataclass(frozen=True, slots=True)
class Kept:
    """One release's kept read: its tracks and year, or that it is gone."""

    read_at: datetime
    gone: bool
    tracks: tuple[KeptTrack, ...] = ()
    year: int | None = None

    @property
    def named(self) -> bool:
        """Whether every kept track carries the words a removal is judged by."""
        return self.gone or all(
            one.artist is not None and one.title is not None for one in self.tracks
        )


def _unusable(path: Path, what: str) -> CratekitError:
    return refuse(
        UNUSABLE,
        f"the release reads kept for this label at {path.name} could not be read "
        f"({what}), so which releases were already read is unknown; nothing was "
        f"asked of the provider and nothing was written to the account",
        steps=(
            f"delete {path} to read the label's catalogue again from the start; "
            f"it holds provider answers only and nothing else is lost",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
        detail={"problem": what, "path": str(path)},
    )


def _instant(raw: Any) -> datetime | None:
    if not isinstance(raw, str):
        return None
    try:
        moment = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


def _entry(path: Path, release_id: str, raw: Any) -> Kept:
    """One entry of the document, or the refusal naming what is wrong with it."""
    if not isinstance(raw, Mapping):
        raise _unusable(path, f"the read of {release_id!r} is not a map")
    read_at = _instant(raw.get("read_at"))
    if read_at is None:
        raise _unusable(path, f"the read of {release_id!r} carries no instant")
    gone = raw.get("gone", False)
    if not isinstance(gone, bool):
        raise _unusable(path, f"the read of {release_id!r} says gone as {gone!r}")
    if gone:
        return Kept(read_at=read_at, gone=True)
    year = raw.get("year")
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
        raise _unusable(path, f"the read of {release_id!r} carries the year {year!r}")
    tracks = raw.get("tracks")
    if not isinstance(tracks, list):
        raise _unusable(path, f"the read of {release_id!r} carries no track list")
    kept: list[KeptTrack] = []
    for track in tracks:
        if (
            not isinstance(track, Mapping)
            or not isinstance(track.get("id"), str)
            or not isinstance(track.get("available"), bool)
            or not all(isinstance(track.get(key), (str, type(None))) for key in ("artist", "title"))
        ):
            raise _unusable(path, f"a track of the read of {release_id!r} is malformed")
        words = {key: track.get(key) for key in ("artist", "title")}
        kept.append(KeptTrack(id=track["id"], available=track["available"], **words))
    return Kept(read_at=read_at, gone=False, tracks=tuple(kept), year=year)


def _row(track: Any) -> dict[str, Any]:
    return {
        "id": str(getattr(track, "id", "") or ""),
        # THE PLAN'S OWN TEST, so a row silent on playing reads as playable.
        "available": getattr(track, "available", True) is not False,
        "artist": tombstoned.track_artist(track),
        "title": tombstoned.track_title(track),
    }


def _stored(kept: Kept) -> dict[str, Any]:
    if kept.gone:
        return {"read_at": kept.read_at.isoformat(), "gone": True}
    tracks = [asdict(one) for one in kept.tracks]
    return {"read_at": kept.read_at.isoformat(), "year": kept.year, "tracks": tracks}


class _Store:
    """What both kept stores share: their counters, the header checks and the write."""

    #: The store's document version, each store's own.
    version = VERSION

    def __init__(self, label_id: str, path: Path) -> None:
        self.label_id = label_id
        self.path = path
        self._unwritten = 0
        #: New answers since the last attempt to write, which paces the retries.
        self._since = 0
        #: When the oldest answer this run reused was given, ``None`` before any.
        self.oldest: datetime | None = None
        #: Why the last write failed, ``""`` while nothing is owed.
        self.unkept = ""

    def _counted(self) -> None:
        self._unwritten += 1
        self._since += 1

    def _reusing(self, read_at: datetime) -> None:
        self.oldest = read_at if self.oldest is None else min(self.oldest, read_at)

    @classmethod
    def _document(
        cls, path: Path, label_id: str, unusable: Callable[[Path, str], CratekitError]
    ) -> Mapping[str, Any] | None:
        """The store's document, ``None`` when none was written, or the refusal."""
        raw = config.read_json_map(path, lambda why: unusable(path, why))
        if raw is None:
            return None
        version = raw.get("version")
        if version != cls.version:
            raise unusable(path, f"it says version {version!r} and this build writes {cls.version}")
        if raw.get("label_id") != label_id:
            raise unusable(path, f"it names the label {raw.get('label_id')!r}, not {label_id!r}")
        return raw

    def flush(self) -> None:
        """Write every answer held, if any is unwritten, by :meth:`_write`'s rule."""
        self._since = 0
        if self._unwritten:
            self._write({"version": self.version, "label_id": self.label_id, **self._sections()})

    def _sections(self) -> dict[str, Any]:
        """The store's own sections of its document, beside the shared header."""
        raise NotImplementedError

    def _write(self, document: Mapping[str, Any]) -> None:
        """Write the document whole and atomically. A REFUSED WRITE IS SAID, NEVER
        RAISED, as ``unkept``: it costs the next run calls, never this run its plan."""
        try:
            config.atomic_write_bytes(
                (json.dumps(document, indent=1, sort_keys=True) + "\n").encode("utf-8"),
                self.path,
            )
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
        self._unwritten = 0
        self.unkept = ""


class KeptReads(_Store):
    """One label's kept release reads, and what this run made of them."""

    def __init__(self, label_id: str, held: Mapping[str, Kept], *, path: Path) -> None:
        super().__init__(label_id, path)
        self._held: dict[str, Kept] = dict(held)
        self.reused = 0
        self.read_now = 0

    @classmethod
    def load(cls, label_id: str) -> KeptReads:
        """The label's kept reads, an empty store when none was written, or the refusal."""
        path = path_for(label_id)
        raw = cls._document(path, label_id, _unusable)
        if raw is None:
            return cls(label_id, {}, path=path)
        reads = raw.get("reads")
        if not isinstance(reads, Mapping):
            raise _unusable(path, "its reads are not a map")
        held = {str(key): _entry(path, str(key), value) for key, value in reads.items()}
        return cls(label_id, held, path=path)

    def _is_fresh(self, kept: Kept) -> bool:
        # NOT FRESH FROM THE FUTURE, NOR WITHOUT THE TRACKS' WORDS (U243).
        age = clock() - kept.read_at
        return timedelta(0) <= age < KEPT_FOR and kept.named

    def kept(self, release_ids: Iterable[str]) -> tuple[int, str]:
        """How many of ``release_ids`` are kept fresh and the oldest's age, counting no reuse."""
        found = [
            held.read_at
            for one in dict.fromkeys(release_ids)
            if (held := self._held.get(one)) is not None and self._is_fresh(held)
        ]
        return len(found), age_text(clock() - min(found)) if found else ""

    def fresh(self, release_id: str) -> Kept | None:
        """The release's kept read when it is younger than the age, else ``None``."""
        held = self._held.get(release_id)
        if held is None or not self._is_fresh(held):
            return None
        self.reused += 1
        self._reusing(held.read_at)
        return held

    def _hold(self, release_id: str, kept: Kept) -> None:
        self._held[release_id] = kept
        self.read_now += 1
        self._counted()
        if self._since >= FLUSH_EVERY:
            self.flush()

    def keep(self, release_id: str, rows: Iterable[Any], year: int | None) -> None:
        """Hold one read this run made, the tracks and the year the provider stated."""
        stated = year if isinstance(year, int) and not isinstance(year, bool) else None
        tracks = tuple(KeptTrack(**_row(row)) for row in rows)
        self._hold(release_id, Kept(read_at=clock(), gone=False, tracks=tracks, year=stated))

    def keep_gone(self, release_id: str) -> None:
        """Hold the provider's answer that the release is gone."""
        self._hold(release_id, Kept(read_at=clock(), gone=True))

    def _sections(self) -> dict[str, Any]:
        return {"reads": {key: _stored(value) for key, value in sorted(self._held.items())}}

    def age_said(self) -> str:
        """How old the oldest reused read is, as a person reads it."""
        return "" if self.oldest is None else age_text(clock() - self.oldest)


def age_text(age: timedelta) -> str:
    minutes = max(0, int(age.total_seconds() // 60))
    if minutes < 60:
        return f"{minutes} minute(s)"
    hours = minutes // 60
    if hours < 48:
        return f"{hours} hour(s)"
    return f"{hours // 24} day(s)"


def kept_for_said() -> str:
    days = KEPT_FOR.days
    return f"{days} day(s)" if days else age_text(KEPT_FOR)


__all__ = [
    "FLUSH_EVERY",
    "KEPT_FOR",
    "UNUSABLE",
    "Kept",
    "KeptReads",
    "KeptTrack",
    "age_text",
    "kept_for_said",
    "path_for",
]
