"""What the streaming provider answered for an ISRC, kept so it is not asked again (U206).

The file belongs to the installation, since it holds facts about the catalogue, so
a copy run shares it; ``CRATEKIT_ISRC_CACHE_DIR`` names its directory when
installation state is redirected too. Only an answer is kept, a list of readable
tracks or a not found the client said in so many words, keyed by the folded ISRC and
the country. It is a saving, never a gate: writes merge under a lock, and no verb is
refused over the file. :class:`Remembered` keeps only the fields callers read.

Layer: acquire.
"""

from __future__ import annotations

import json
import math
import os
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.core import config
from cratekit.core.cause import answered_not_found

#: The two declared state entries, installation scoped for the reason above.
STATE_KEY = "isrc_cache"
LOCK_KEY = "isrc_cache_lock"

#: The file's own shape version; another version is set aside like a bad parse.
SCHEMA = 1

#: Days a not found is kept, unless ``isrc_cache_days`` is shorter.
NOT_FOUND_DAYS = 7

#: Seconds in a day, the unit the setting is written in.
DAY_S = 86_400

#: How long a write waits for the lock before it writes nothing.
LOCK_WAIT_S = 5.0

#: How often a waiting write asks for the lock again.
LOCK_POLL_S = 0.05

#: What a file that could not be parsed is renamed to, before a stamp.
SET_ASIDE = ".unreadable-"

#: What :meth:`Cache.count` answers for a file it cannot open, and one that does not parse.
UNREADABLE = "unreadable"
UNPARSED = "unparsed"

#: This process's lookups settled from the cache and asked of the provider.
_PROCESS_HITS = 0
_PROCESS_ASKED = 0


@dataclass(frozen=True, slots=True)
class Lookups:
    """ISRC lookups a remembered answer settled, and lookups the provider was asked."""

    remembered: int = 0
    asked: int = 0


def process_lookups() -> Lookups:
    """What THIS process has looked up so far, across every cache it built."""
    return Lookups(remembered=_PROCESS_HITS, asked=_PROCESS_ASKED)


def asked() -> None:
    """Count one ISRC lookup that goes to the provider, once however often it is retried."""
    global _PROCESS_ASKED
    _PROCESS_ASKED += 1


@dataclass(frozen=True, slots=True)
class Named:
    """An artist or an album as a remembered track carries it: by its name."""

    name: str


@dataclass(frozen=True, slots=True)
class Remembered:
    """One track out of a remembered answer, read the way the client's track is read.

    ``available`` keeps ``None`` for a track that never said, read as playable.
    """

    id: str
    title: str | None = None
    name: str | None = None
    version: str | None = None
    artist: Named | None = None
    artists: tuple[Named, ...] = ()
    album: Named | None = None
    available: bool | None = None
    isrc: str | None = None


def _name_of(value: Any) -> str | None:
    """The name an artist or album entry carries, a string or a mapping or an object."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    name = value.get("name") if isinstance(value, Mapping) else getattr(value, "name", None)
    return name if isinstance(name, str) else ""


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _kept(track: Any) -> dict[str, Any]:
    """One client track as the file keeps it."""
    lead = getattr(track, "artist", None)
    album = getattr(track, "album", None)
    available = getattr(track, "available", None)
    found_isrc = match.row_isrc(track)
    return {
        "id": str(getattr(track, "id", "") or ""),
        "title": _text(getattr(track, "title", None)),
        "name": _text(getattr(track, "name", None)),
        "version": _text(getattr(track, "version", None)),
        "artist": _name_of(lead),
        "artists": [_name_of(entry) or "" for entry in getattr(track, "artists", None) or ()],
        "album": _name_of(album),
        "available": available if isinstance(available, bool) else None,
        "isrc": str(found_isrc) if found_isrc else None,
    }


def _readable(track: Any) -> bool:
    """Whether a track carries an identifier and names an artist and a title."""
    if not str(getattr(track, "id", "") or "").strip():
        return False
    try:
        match.read_row(track, origin=match.TIDAL, position=1)
    except match.UnreadableList:
        return False
    return True


def _remembered(kept: Any) -> Remembered:
    """A kept track back as one a caller reads. Raises on a shape this module never writes."""
    if not isinstance(kept, Mapping):
        raise ValueError("a remembered track is not a mapping")
    identifier = kept["id"]
    if not isinstance(identifier, str):
        raise ValueError("a remembered track carries no identifier")
    artists = kept.get("artists") or []
    if not isinstance(artists, list) or not all(isinstance(one, str) for one in artists):
        raise ValueError("a remembered track's artists are not names")
    lead = kept.get("artist")
    album = kept.get("album")
    available = kept.get("available")
    for value in (kept.get("title"), kept.get("name"), kept.get("version"), lead, album, kept.get("isrc")):
        if value is not None and not isinstance(value, str):
            raise ValueError("a remembered track carries a field that is not text")
    if available is not None and not isinstance(available, bool):
        raise ValueError("a remembered track's availability is not a flag")
    return Remembered(
        id=identifier,
        title=kept.get("title"),
        name=kept.get("name"),
        version=kept.get("version"),
        artist=None if lead is None else Named(lead),
        artists=tuple(Named(one) for one in artists),
        album=None if album is None else Named(album),
        available=available,
        isrc=kept.get("isrc"),
    )


def _key(isrc: str, country: str) -> str | None:
    """The entry's key, or ``None`` for a spelling that is never kept."""
    folded = match.isrc_token(isrc)
    if not folded or folded != isrc:
        return None
    return f"{folded}|{country}"


def said_not_found(exc: BaseException) -> bool:
    """Whether a failure is the client's own ``ObjectNotFound`` or a 404 (R-1313)."""
    if type(exc).__name__ == "ObjectNotFound":
        return True
    return answered_not_found(exc)


def country_of(session: Any) -> str:
    """The country a client asks the catalogue in, ``""`` when it does not say."""
    country = getattr(session, "country_code", None)
    return country.strip().upper() if isinstance(country, str) else ""


def _resolved(key: str) -> Path:
    """Where one of the two entries lives, under ``CRATEKIT_ISRC_CACHE_DIR`` when set."""
    override = os.environ.get(config.ENV_ISRC_CACHE_DIR)
    if override:
        return Path(override) / config.state_file(key).relative
    return config.state_path(key)


def _stamp(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class Cache:
    """The ISRC answers file, its lock, and how long an answer is good for."""

    days: int = field(default_factory=lambda: int(config.DEFAULT_PROVIDER_ISRC_CACHE_DAYS))
    path: Path | None = None
    lock_path: Path | None = None
    clock: Callable[[], float] = time.time
    sleep: Callable[[float], None] = time.sleep
    #: The parsed file and the stat it was read at, so a run parses it once.
    _held: tuple[tuple[int, int, int], dict[str, Any]] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.path is None:
            self.path = _resolved(STATE_KEY)
        if self.lock_path is None:
            self.lock_path = _resolved(LOCK_KEY)

    @classmethod
    def from_config(cls, cfg: Any) -> Cache:
        """The cache the ``[provider]`` section sets, falling back for an older frozen config."""
        provider = getattr(cfg, "provider", None)
        days = getattr(provider, "isrc_cache_days", None)
        if not isinstance(days, int) or isinstance(days, bool) or days < 0:
            return cls()
        return cls(days=days)

    @property
    def enabled(self) -> bool:
        return self.days > 0

    # ── reading ────────────────────────────────────────────────────────────

    def _signature(self) -> tuple[int, int, int] | None:
        try:
            seen = os.stat(self.path)
        except FileNotFoundError:
            return None
        return (seen.st_ino, seen.st_size, seen.st_mtime_ns)

    def _parse(self, text: str) -> dict[str, Any] | None:
        """The entries a file holds, or ``None`` for a file this module did not write."""
        try:
            data = json.loads(text)
        except ValueError:
            return None
        if not isinstance(data, Mapping) or data.get("schema") != SCHEMA:
            return None
        entries = data.get("entries")
        if not isinstance(entries, Mapping):
            return None
        return dict(entries)

    def _entries(self, *, locked: bool = False) -> dict[str, Any] | None:
        """Every entry, or ``None`` when the file cannot be read at all.

        A file that does not parse is set aside and read as empty. ``locked`` says the
        caller holds the lock, since a second ``flock`` would wait on the first.
        """
        try:
            signature = self._signature()
        except OSError:
            return None
        if signature is None:
            self._held = None
            return {}
        if self._held is not None and self._held[0] == signature:
            return self._held[1]
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return {}
        except (OSError, UnicodeDecodeError):
            return None
        entries = self._parse(text)
        if entries is None:
            if locked:
                self._set_aside_held()
            else:
                self._set_aside()
            return {}
        self._held = (signature, entries)
        return entries

    def _fresh(self, entry: Any, now: float) -> tuple[Remembered, ...] | None:
        """An entry's tracks while it is good, else ``None``."""
        if not isinstance(entry, Mapping):
            return None
        stamped = entry.get("asked_at")
        tracks = entry.get("tracks")
        if (
            isinstance(stamped, bool)
            or not isinstance(stamped, (int, float))
            or not math.isfinite(stamped)
            or not isinstance(tracks, list)
        ):
            return None
        age = now - stamped
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
        if age < 0 or age >= days * DAY_S:
            return None
        try:
            return tuple(_remembered(one) for one in tracks)
        except (KeyError, TypeError, ValueError):
            return None

    def recall(self, isrc: str, country: str) -> tuple[Remembered, ...] | None:
        """The remembered answer, ``()`` for a not found, or ``None`` to ask."""
        global _PROCESS_HITS
        if not self.enabled:
            return None
        key = _key(isrc, country)
        if key is None:
            return None
        entries = self._entries()
        if not entries:
            return None
        held = self._fresh(entries.get(key), self.clock())
        if held is not None:
            _PROCESS_HITS += 1
        return held

    def holds(self, isrc: str, country: str) -> bool:
        """Whether :meth:`recall` would answer this code now, counting nothing."""
        if not self.enabled:
            return False
        key = _key(isrc, country)
        if key is None:
            return False
        entries = self._entries()
        if not entries:
            return False
        return self._fresh(entries.get(key), self.clock()) is not None

    # ── writing ────────────────────────────────────────────────────────────

    def _locked(self):
        """Hold the sibling lock and yield True, or yield False when it was not had in time."""
        return config.lock_within(
            self.lock_path, wait_s=LOCK_WAIT_S, poll_s=LOCK_POLL_S, sleep=self.sleep
        )

    def _set_aside(self) -> Path | None:
        """Rename a file that does not parse out of the way, taking the lock first."""
        with self._locked() as had:
            return self._set_aside_held() if had else None

    def _set_aside_held(self) -> Path | None:
        """Rename a file that still does not parse under the caller's lock out of the way."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except (OSError, UnicodeDecodeError):
            return None
        if self._parse(text) is not None:
            return None
        aside = self.path.with_name(
            f"{self.path.name}{SET_ASIDE}{_stamp(self.clock())}-{os.getpid()}"
        )
        try:
            os.replace(self.path, aside)
        except OSError:
            return None
        self._held = None
        return aside

    def remember(self, isrc: str, country: str, tracks: Iterable[Any]) -> bool:
        """Keep one answer, ``()`` for a not found, merged under the lock; True when written."""
        if not self.enabled:
            return False
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
        if not all(_readable(track) for track in tracks):
            return False
        kept = [_kept(track) for track in tracks]
        with self._locked() as had:
            if not had:
                return False
            entries = self._entries(locked=True)
            if entries is None:
                return False
            now = self.clock()
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
            merged[key] = {"asked_at": now, "tracks": kept}
            payload = json.dumps(
                {"schema": SCHEMA, "entries": merged}, indent=1, sort_keys=True
            ) + "\n"
            try:
                config.mkdir_private(self.path.parent)
                config.atomic_write_bytes(payload.encode("utf-8"), self.path)
                written = self._signature()
            except OSError:
                self._held = None
                return False
            # Held as written, so the next lookup reads it without parsing again.
            self._held = (written, merged) if written is not None else None
            return True

    # ── what doctor reads ──────────────────────────────────────────────────

    def set_aside(self) -> tuple[Path, ...]:
        """Every file this cache set aside, oldest first."""
        try:
            return tuple(sorted(self.path.parent.glob(f"{self.path.name}{SET_ASIDE}*")))
        except OSError:
            return ()

    def count(self) -> int | str:
        """How many entries can still answer, or :data:`UNREADABLE` or :data:`UNPARSED`."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return 0
        except (OSError, UnicodeDecodeError):
            return UNREADABLE
        entries = self._parse(text)
        if entries is None:
            return UNPARSED
        now = self.clock()
        return sum(1 for entry in entries.values() if self._fresh(entry, now) is not None)


__all__ = [
    "DAY_S", "LOCK_KEY", "NOT_FOUND_DAYS", "SCHEMA", "SET_ASIDE", "STATE_KEY", "UNPARSED",
    "UNREADABLE", "Cache", "Lookups", "Named", "Remembered", "asked", "country_of",
    "process_lookups", "said_not_found",
]
