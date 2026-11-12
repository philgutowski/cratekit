"""A full label build's release reads, kept across runs (R-1091).

``crate label playlists LABEL`` without ``--releases`` reads every confirmed
release's tracks, two provider calls a release, and a label the size of
Defected is about 24,700 calls, nearly seven hours at the default pace. Held
only in memory, a breaker trip part way dropped every read and the next run
started from the first release, and the run that carries out an approved plan
read the whole catalogue a second time. This store keeps each read per label,
so a large label builds over several runs instead of starting over each time.

A READ IS KEPT FOR :data:`KEPT_FOR` AND NO LONGER. A release whose tracks the
provider changed after it was read is planned from the old rows until its read
is that old, then it is read again. The screen says how many reads were reused
and how old the oldest is, so the person approving a plan knows it was not all
read that day. Seven days is the recommendation put to Phillip on the
decisions page on 2026-11-01, and the one number to change if he picks another.

WHAT IS KEPT is what the plan reads off a release and nothing else: each
track's identifier, whether the provider will play it, and its artist and
title, and the year the provider dates the release by. The artist and title
are what a removed track is recognised by (U243), so a read kept before they
were kept is read again rather than judged without them. A release the provider no longer has is the
provider answering, and is kept as gone. A read that failed is not an answer
and is never kept.

WRITTEN AS IT GOES. :meth:`KeptReads.flush` writes the document whole and
atomically, and the reader calls it every :data:`FLUSH_EVERY` new reads and on
the way out, a breaker park included, so a stopped build loses at most the
reads since its last flush and only when the process itself is killed. A write
the filesystem refuses is recorded on the store as ``unkept`` and said on the
screen and in the run's warnings, never raised in place of the plan.

A STORE THAT CANNOT BE READ REFUSES, ``label-playlists-reads-unusable``, on
the rule every state document here keeps. Read as empty it would cost nothing
but calls, and that is still a clean read reported over a file the tool could
not read; the person repairs or deletes it, and deleting it is safe.

WHERE IT LIVES. Under the installation state entry ``label_crawl_cache``, one
document per label beside the verifier's own cache, since the entry already
declares what a catalogue lookup returned: replayable, library agnostic, and
never restored. A read of the provider is the same answer whichever library
asked for it.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.label import tombstoned

#: How long a kept read stays true before a build reads the release again.
KEPT_FOR = timedelta(days=7)

#: New reads between two writes of the document. Fifty releases is about a
#: hundred seconds of calls at the default pace, so a kill loses that at most,
#: and a label of twelve thousand releases is written some two hundred and
#: fifty times rather than twelve thousand.
FLUSH_EVERY = 50

#: The document's version. Any other refuses rather than being read.
VERSION = 1

#: The file inside the label's own directory of the crawl cache.
FILE_NAME = "reads.json"

UNUSABLE = "label-playlists-reads-unusable"

_ORIGIN = ("label.playlists",)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


#: The clock the store reads. A module attribute so a suite can age a read
#: without writing a document by hand.
clock: Callable[[], datetime] = _utcnow


def path_for(label_id: str) -> Path:
    return config.state_path("label_crawl_cache") / label_id / FILE_NAME


@dataclass(frozen=True, slots=True)
class KeptTrack:
    """One track as a kept read carries it: what the plan reads off a row."""

    id: str
    available: bool
    #: The track's words as :func:`cratekit.label.tombstoned.track_artist` and
    #: ``track_title`` read them off the provider row, ``None`` in a read kept
    #: before they were kept (U243). Named ``artist`` and ``title`` so the same
    #: readers read them back off this value.
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
        ):
            raise _unusable(path, f"a track of the read of {release_id!r} is malformed")
        words = {key: track.get(key) for key in ("artist", "title")}
        if any(value is not None and not isinstance(value, str) for value in words.values()):
            raise _unusable(path, f"a track of the read of {release_id!r} is malformed")
        kept.append(
            KeptTrack(
                id=track["id"],
                available=track["available"],
                artist=words["artist"],
                title=words["title"],
            )
        )
    return Kept(read_at=read_at, gone=False, tracks=tuple(kept), year=year)


def _row(track: Any) -> dict[str, Any]:
    return {
        "id": str(getattr(track, "id", "") or ""),
        # THE PLAN'S OWN TEST, ``available is not False``, so a row that says
        # nothing about playing reads as playable here exactly as it does live.
        "available": getattr(track, "available", True) is not False,
        "artist": tombstoned.track_artist(track),
        "title": tombstoned.track_title(track),
    }


def _stored(kept: Kept) -> dict[str, Any]:
    if kept.gone:
        return {"read_at": kept.read_at.isoformat(), "gone": True}
    return {
        "read_at": kept.read_at.isoformat(),
        "year": kept.year,
        "tracks": [
            {"id": one.id, "available": one.available, "artist": one.artist, "title": one.title}
            for one in kept.tracks
        ],
    }


class KeptReads:
    """One label's kept release reads, and what this run made of them.

    :meth:`fresh` answers a release from the store when its read is younger
    than :data:`KEPT_FOR`, and counts the reuse. :meth:`keep` and
    :meth:`keep_gone` hold a read this run made and write the document every
    :data:`FLUSH_EVERY` of them. ``reused`` and ``oldest`` are what the screen
    shows.
    """

    def __init__(self, label_id: str, held: Mapping[str, Kept], *, path: Path) -> None:
        self.label_id = label_id
        self.path = path
        self._held: dict[str, Kept] = dict(held)
        self._unwritten = 0
        #: New reads since the last attempt to write, which paces the retries.
        self._since = 0
        self.reused = 0
        self.read_now = 0
        #: When the oldest read this run reused was made, ``None`` before any.
        self.oldest: datetime | None = None
        #: Why the last write of the document failed, ``""`` while the reads
        #: held are written or none needs writing.
        self.unkept = ""

    @classmethod
    def load(cls, label_id: str) -> KeptReads:
        """The label's kept reads, an empty store when none was written, or the refusal."""
        path = path_for(label_id)
        if not path.exists():
            return cls(label_id, {}, path=path)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise _unusable(path, "it could not be opened") from exc
        except ValueError as exc:
            raise _unusable(path, "it is not JSON") from exc
        if not isinstance(raw, Mapping):
            raise _unusable(path, f"the document is a {type(raw).__name__}, not a map")
        version = raw.get("version")
        if version != VERSION:
            raise _unusable(
                path, f"it says version {version!r} and this build writes {VERSION}"
            )
        if raw.get("label_id") != label_id:
            raise _unusable(
                path, f"it names the label {raw.get('label_id')!r}, not {label_id!r}"
            )
        reads = raw.get("reads")
        if not isinstance(reads, Mapping):
            raise _unusable(path, "its reads are not a map")
        return cls(
            label_id,
            {str(key): _entry(path, str(key), value) for key, value in reads.items()},
            path=path,
        )

    def _is_fresh(self, kept: Kept) -> bool:
        # A READ FROM THE FUTURE IS NOT FRESH. A clock set back would otherwise
        # keep it for as long as the clock is wrong.
        age = clock() - kept.read_at
        # A READ WITHOUT THE TRACKS' WORDS IS NOT FRESH EITHER (U243): a
        # removed track is recognised by them, and judged without them it
        # would be added back to its year.
        return timedelta(0) <= age < KEPT_FOR and kept.named

    def kept(self, release_ids: Iterable[str]) -> tuple[int, str]:
        """How many of ``release_ids`` the store keeps fresh, and how old the oldest is.

        Counts no reuse: the estimate asks this before any release is read.
        """
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
        if self.oldest is None or held.read_at < self.oldest:
            self.oldest = held.read_at
        return held

    def _hold(self, release_id: str, kept: Kept) -> None:
        self._held[release_id] = kept
        self.read_now += 1
        self._unwritten += 1
        self._since += 1
        if self._since >= FLUSH_EVERY:
            self.flush()

    def keep(self, release_id: str, rows: Iterable[Any], year: int | None) -> None:
        """Hold one read this run made, the tracks and the year the provider stated."""
        stated = year if isinstance(year, int) and not isinstance(year, bool) else None
        self._hold(
            release_id,
            Kept(
                read_at=clock(),
                gone=False,
                tracks=tuple(KeptTrack(**_row(row)) for row in rows),
                year=stated,
            ),
        )

    def keep_gone(self, release_id: str) -> None:
        """Hold the provider's answer that the release is gone."""
        self._hold(release_id, Kept(read_at=clock(), gone=True))

    def flush(self) -> None:
        """Write every read held, whole and atomically, if any is unwritten.

        A WRITE THE FILESYSTEM REFUSES IS SAID, NEVER RAISED. The store saves
        provider calls and holds nothing else, so a full disk, a read only
        volume or a file where the label's directory belongs costs the next run
        its reads and must not cost this run its plan: ``unkept`` says why, the
        screen and the run's warnings say so, and the next flush tries again
        and clears it once the whole document is written.
        """
        self._since = 0
        if not self._unwritten:
            return
        document = {
            "version": VERSION,
            "label_id": self.label_id,
            "reads": {key: _stored(value) for key, value in sorted(self._held.items())},
        }
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

    def age_said(self) -> str:
        """How old the oldest reused read is, as a person reads it."""
        if self.oldest is None:
            return ""
        return age_text(clock() - self.oldest)


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
