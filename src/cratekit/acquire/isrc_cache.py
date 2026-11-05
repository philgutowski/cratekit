"""What the streaming provider answered for an ISRC, kept so it is not asked again (U206).

WHAT WENT WRONG. The attended sitting that ran ``crate sync pair`` live for the
first time rehearsed it on a disposable library copy with library state
redirected, which is the rule ``docs/solutions`` gives for a copy run. Every
ISRC the rehearsal matched was thrown away with the copy's state, and the live
run asked the provider every one of them again, so the first sync paid for its
lookups twice. A mirror after a pair, or an intake after a sync, paid a third
time for the same answers.

ONE FILE OF THE INSTALLATION, NEVER OF THE LIBRARY. What the provider files
under an ISRC is a fact about its catalogue, not about any library, so the
file sits beside ``provider_gate.json`` under the installation's state
directory. A copy run that redirects ``library.state_dirname`` therefore
shares it with the live run, which is the whole saving.

AND A COPY RUN THAT REDIRECTS THE INSTALLATION STATE TOO KEEPS IT. Every copy
run since sitting 39 also copies the installation state and redirects
``CRATEKIT_STATE_DIR``, and so does ``core.rehearsal``, which would put this
file in the scratch area and throw its answers away with it. So
``CRATEKIT_ISRC_CACHE_DIR``, when set, names the directory the file and its
lock live in: ``core.rehearsal.redirected`` sets it to the live one for the
body it redirects, and a copy run by hand sets it the same way.

READ AND WRITTEN AT TWO SEAMS AND NOWHERE ELSE: the outbound account's
``match_track`` and the catalogue's ``tracks_for_isrc``. No caller above them
learns the cache exists, and ``sync pair``'s links and remembered misses on
the pairs document sit above it, unchanged.

ONLY AN ANSWER IS KEPT. A list of tracks is an answer, and so is a not found
the client said in so many words (its ``ObjectNotFound``, or a 404). An
outage, a rejected session, a rate limit and an ``InvalidISRC`` are never
kept: at the client version this product pins, ``InvalidISRC`` is what every
HTTP error but 404 and 429 arrives as, so it may hide any of the others
(``docs/solutions``, the InvalidISRC entry). Each seam decides what was an
answer, because each reads its client's failures its own way, and hands this
module only the answers.

AND ONLY AN ANSWER EVERY TRACK OF WHICH CAN BE READ. A track with no
identifier, or naming no artist or no title as the matcher reads it, is
something the provider may still fill in, and the callers already refuse to
choose beside one (``tidal_account._among``, ``intake.missing_cli``) and
``sync pair`` and the mirror never remember such an answer (R-988, U198). So
the answer is asked again next time rather than kept with the gap in it.

KEYED BY THE FOLDED ISRC AND THE COUNTRY THE CATALOGUE WAS ASKED IN, since one
recording can be filed differently in two countries. A spelling that is not
already its own fold is asked and never kept: the provider may answer a lower
case spelling differently from the folded one, and keeping that answer under
the folded key would answer the folded spelling with it.

HOW LONG. A found answer is reused for ``[provider] isrc_cache_days`` days,
thirty unless set. A not found for :data:`NOT_FOUND_DAYS`, or for the setting
when that is shorter, since a person who shortened the one wants the other no
staler. Zero turns the cache off: nothing is read and nothing is written. An
expired entry, or one stamped later than now, is asked again and replaced.

A SAVING, NEVER A GATE. Every write takes the sibling lock, reads the file
again, merges its one entry and replaces the file atomically, so two
processes never lose each other's answers or leave half a file. A lock not had
within :data:`LOCK_WAIT_S` skips the write. A file that does not parse is set
aside beside itself, named by ``crate doctor``, and rebuilt; a file that
cannot be read at all is left where it is and every lookup asks the provider.
No verb is refused over this file.

WHAT IT KEEPS OF A TRACK is what the callers read: the identifier, the title,
the version, the lead artist and every billed artist by name, the album's
name, whether the provider will play it, and its ISRC. A remembered track is a
:class:`Remembered`, which answers those attributes as the client's own track
does; a caller that starts reading another field off an ISRC answer adds it
here, or it reads ``None`` off every remembered one. The suite builds a real
client track offline and checks the two read alike.

Layer: acquire.
"""

from __future__ import annotations

import json
import math
import os
import time
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.core import config

#: The two declared state entries, installation scoped for the reason above.
STATE_KEY = "isrc_cache"
LOCK_KEY = "isrc_cache_lock"

#: The file's own shape version. A file of another version is set aside like
#: one that does not parse, since reading it as this one is a guess.
SCHEMA = 1

#: How many days an answer that the provider has no track under is kept,
#: unless ``isrc_cache_days`` is shorter.
NOT_FOUND_DAYS = 7

#: Seconds in a day, the unit the setting is written in.
DAY_S = 86_400

#: How long a write waits for the lock before it gives up and writes nothing.
#: A holder holds it for one read, one merge and one replace, so a wait this
#: long means the holder is not making progress, and the cache is not worth
#: holding a lookup up for.
LOCK_WAIT_S = 5.0

#: How often a waiting write asks for the lock again.
LOCK_POLL_S = 0.05

#: What a file that could not be parsed is renamed to, before a stamp.
SET_ASIDE = ".unreadable-"

#: This process's own counts, across every cache it built: lookups a
#: remembered answer settled, and lookups that went to the provider. The
#: dispatcher reads the difference over one verb and reports it, as it does
#: the provider spend.
_PROCESS_HITS = 0
_PROCESS_ASKED = 0


@dataclass(frozen=True, slots=True)
class Lookups:
    """ISRC lookups a remembered answer settled, and lookups the provider was asked."""

    remembered: int = 0
    asked: int = 0

    def since(self, earlier: Lookups) -> Lookups:
        """What happened between ``earlier`` and this snapshot."""
        return Lookups(
            remembered=max(0, self.remembered - earlier.remembered),
            asked=max(0, self.asked - earlier.asked),
        )


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

    ``available`` keeps ``None`` for a track that never said, which
    ``tidal_account._streamable`` reads as playable, exactly as it reads the
    client's object with the attribute missing.
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


def country_of(session: Any) -> str:
    """The country a client asks the catalogue in, ``""`` when it does not say."""
    country = getattr(session, "country_code", None)
    return country.strip().upper() if isinstance(country, str) else ""


def _resolved(key: str) -> Path:
    """Where one of the two entries lives: under ``CRATEKIT_ISRC_CACHE_DIR`` when
    it is set, else where the state inventory puts it.

    The override keeps the entry's own file name, so the two never disagree
    about what the file is called, and only its directory moves.
    """
    override = os.environ.get(config.ENV_ISRC_CACHE_DIR)
    if override:
        return Path(override) / config.state_file(key).relative
    return config.state_path(key)


def _stamp(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class Cache:
    """The ISRC answers file, its lock, and how long an answer is good for.

    ``clock`` is injectable so a suite ages an entry without waiting a week.
    """

    days: int = field(default_factory=lambda: int(config.DEFAULT_PROVIDER_ISRC_CACHE_DAYS))
    path: Path | None = None
    lock_path: Path | None = None
    clock: Callable[[], float] = time.time
    sleep: Callable[[float], None] = time.sleep
    #: The parsed file and the stat it was read at, so a run of a thousand
    #: lookups parses the file once rather than once per lookup.
    _held: tuple[tuple[int, int, int], dict[str, Any]] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.path is None:
            self.path = _resolved(STATE_KEY)
        if self.lock_path is None:
            self.lock_path = _resolved(LOCK_KEY)

    @classmethod
    def from_config(cls, cfg: Any) -> Cache:
        """The cache the ``[provider]`` section sets, off a loaded configuration.

        Read with a fallback rather than required, because a job queued before
        this setting existed carries a frozen configuration that never had it.
        """
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

        A file that reads and does not parse is set aside and read as empty. A
        file that cannot be read is left alone and answers nothing, since a
        rename over a file nobody could read is a guess about what is in it.
        ``locked`` says the caller holds the lock already, so the set aside
        does not ask for it a second time: a second ``flock`` from this same
        process on a fresh descriptor waits on the first.
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
        """The remembered answer for one ISRC in one country, or ``None`` to ask.

        An empty tuple is a remembered not found. Counted as a lookup the
        cache settled; a ``None`` is counted by the seam when it asks.
        """
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

    # ── writing ────────────────────────────────────────────────────────────

    @contextmanager
    def _locked(self) -> Iterator[bool]:
        """Hold the sibling lock and yield True, or yield False when it was not had in time.

        THE LOCK FILE IS NEVER UNLINKED, for the reason the provider gate's is
        not: one holder unlinking the name while another creates a fresh file
        at it is how two processes each hold "the" lock.
        """
        try:
            config._mkdir_private(self.lock_path.parent)
            fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        except OSError:
            yield False
            return
        try:
            try:
                import fcntl  # noqa: PLC0415 - POSIX only, see the except
            except ImportError:  # pragma: no cover - no advisory locks here
                fcntl = None
            had = True
            if fcntl is not None:
                had = False
                polls = 0
                while polls * LOCK_POLL_S < LOCK_WAIT_S:
                    try:
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        had = True
                        break
                    except BlockingIOError:
                        polls += 1
                        self.sleep(LOCK_POLL_S)
            yield had
        finally:
            os.close(fd)  # closing the descriptor releases the lock; the file stays

    def _set_aside(self) -> Path | None:
        """Rename a file that does not parse out of the way, taking the lock first."""
        with self._locked() as had:
            return self._set_aside_held() if had else None

    def _set_aside_held(self) -> Path | None:
        """Rename a file that does not parse out of the way; the caller holds the lock.

        Read again under the lock, so a file another process already replaced
        with a good one is never set aside on an old reading of it.
        """
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
        """Keep one answer, ``()`` for a not found. True when it was written.

        An answer holding a track that cannot be read is not kept, see the
        module's docstring.

        Under the lock the file is read again and only this entry changes, so
        another process's answers written since this one read survive. Entries
        past their time are dropped in the same write, so the file holds what
        can still answer and nothing else.
        """
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
                config._mkdir_private(self.path.parent)
                config.atomic_write_bytes(payload.encode("utf-8"), self.path)
                written = self._signature()
            except OSError:
                self._held = None
                return False
            # Held as written, so the next lookup in this run reads it without
            # parsing it again; another process's write changes the signature.
            self._held = (written, merged) if written is not None else None
            return True

    # ── what doctor reads ──────────────────────────────────────────────────

    def set_aside(self) -> tuple[Path, ...]:
        """Every file this cache set aside, oldest first."""
        try:
            return tuple(sorted(self.path.parent.glob(f"{self.path.name}{SET_ASIDE}*")))
        except OSError:
            return ()

    def count(self) -> int | None:
        """How many entries can still answer, or ``None`` when the file cannot be read."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return 0
        except (OSError, UnicodeDecodeError):
            return None
        entries = self._parse(text)
        if entries is None:
            return None
        now = self.clock()
        return sum(1 for entry in entries.values() if self._fresh(entry, now) is not None)


__all__ = [
    "DAY_S",
    "LOCK_KEY",
    "NOT_FOUND_DAYS",
    "SCHEMA",
    "SET_ASIDE",
    "STATE_KEY",
    "Cache",
    "Lookups",
    "Named",
    "Remembered",
    "asked",
    "country_of",
    "process_lookups",
]
