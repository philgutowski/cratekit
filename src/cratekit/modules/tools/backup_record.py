"""The record of what the last completed backup left, and the walk read against it.

The walk (stat only) is compared with the record of what the last completed
mirror left: no difference is a SKIP, a small one a QUICK run, anything not
vouched for a FULL run. The record is written only after a mirror completed and
removed before the first transfer it describes; an entry the walks before and
after a transfer disagree on is a DOUBT; a file modified within
:data:`RACY_SECONDS` of the walk is hashed. What the walk cannot read refuses
it (:class:`WalkRefused`), never reads as absence. The database gets a
FINGERPRINT instead, read only with rekordbox confirmed gone. Every record is
installation state, since one inside the mirrored tree would change it.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import stat
import time
import unicodedata
import uuid
import zlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from cratekit.core import config

#: The inventory keys of the three records.
MANIFEST_KEY = "backup_manifest"
FINGERPRINT_KEY = "backup_database_fingerprint"
CENSUS_KEY = "backup_census"
#: A record of any other version is not read and the run is full.
SCHEMA_VERSION = 1
#: How near the walk a modification time may sit before the content is hashed
#: (exFAT keeps two seconds, HFS+ one, the rest is clock margin).
RACY_SECONDS = 10
#: Past this many paths one lookup each costs more than listing the remote.
QUICK_LIMIT = 10_000
#: A root holding under one file in this many of what the last completed backup
#: walked is not proven to be the library.
LIBRARY_FLOOR = 10
#: Pattern characters :func:`_pattern` refuses rather than translates, since an
#: exclude read differently here and in rclone miscounts what the mirror sends.
_UNTRANSLATED = frozenset("[]{}\\")


class WalkRefused(Exception):
    """The walk met something it cannot vouch for, so the run must be full."""


@dataclass(frozen=True, slots=True)
class Entry:
    """One file: size, time in nanoseconds, and a hash where time is not trusted."""

    size: int
    mtime_ns: int
    sha256: str | None = None

    def agrees(self, other: Entry) -> bool:
        """The same file to both readings: size, time, and a hash held by both or neither."""
        return (self.size, self.mtime_ns, self.sha256) == (other.size, other.mtime_ns, other.sha256)


#: The entry for a path whose remote copy is unknown. No file has a negative
#: size, so it agrees with nothing: the next run sends or archives the path.
DOUBT = Entry(size=-1, mtime_ns=-1)


@dataclass(frozen=True, slots=True)
class Walk:
    """One reading of the library: every file the mirror would carry."""

    entries: Mapping[str, Entry]
    #: Files modified at or after this instant were hashed.
    racy_after_ns: int
    seconds: float
    #: The device the root was on throughout the walk, which a quick run's
    #: archive is held to.
    root_dev: int = -1


@dataclass(frozen=True, slots=True)
class Manifest:
    """The record of what the last completed mirror left on the remote."""

    library_root: str
    volume_id: str | None
    dest: str
    archive_root: str
    excludes: tuple[str, ...]
    written_at: str
    entries: Mapping[str, Entry]
    #: The token the files fact published with this record carries too; the
    #: record is trusted only while the library's fact still carries it, since
    #: other writers of the mirror publish a fact without it.
    token: str = ""


@dataclass(frozen=True, slots=True)
class Difference:
    """What changed between the record and a walk, by path, in sorted order.

    ``rewritten`` kept size and time and moved its hash, so rclone sends it only
    with times ignored. ``self_written`` is the backup's own fact file, rewritten
    after every run: listed, and left out of :attr:`anything`.
    """

    added: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()
    rewritten: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    self_written: frozenset[str] = field(default_factory=frozenset)
    #: Present paths the record held as a DOUBT, sent with the times ignored.
    doubted: tuple[str, ...] = ()

    @property
    def paths(self) -> tuple[str, ...]:
        return (*self.added, *self.changed, *self.doubted, *self.rewritten, *self.removed)

    @property
    def anything(self) -> bool:
        """True when something other than the backup's own record changed."""
        return any(path not in self.self_written for path in self.paths)

    def counts(self) -> dict[str, int]:
        """How many paths changed by kind, the backup's own record left out."""

        def counted(paths: tuple[str, ...]) -> int:
            return sum(1 for path in paths if path not in self.self_written)

        return {
            "added": counted(self.added), "changed": counted(self.changed) + counted(self.doubted),
            "rewritten": counted(self.rewritten), "removed": counted(self.removed),
        }


@dataclass(frozen=True, slots=True)
class _Excludes:
    files: tuple[re.Pattern[str], ...]
    directories: tuple[re.Pattern[str], ...]

    def file(self, rel: str) -> bool:
        return any(p.search(rel) for p in self.files)

    def directory(self, rel: str) -> bool:
        return any(p.search(rel) for p in self.directories)


_GLOB = {"**": ".*", "*": "[^/]*", "?": "[^/]"}


def _glob(text: str) -> str:
    """One rclone glob as a regex body: ``**`` crosses separators, ``*`` and
    ``?`` stay within a segment, anything else is literal."""
    return "".join(_GLOB.get(t) or re.escape(t) for t in re.findall(r"\*\*|.", text, re.S))


def _pattern(pattern: str) -> tuple[re.Pattern[str], re.Pattern[str] | None]:
    """A file matcher and, for ``dir/**``, a directory matcher, for one exclude:
    anchored at the root by a leading slash, else matched at the path's end."""
    if any(char in _UNTRANSLATED for char in pattern):
        raise WalkRefused(
            f"the exclude {pattern!r} uses a pattern this walk does not read the way rclone does"
        )
    anchored = pattern.startswith("/")
    body = pattern[1:] if anchored else pattern
    head = "^" if anchored else "(?:^|/)"
    files = re.compile(head + _glob(body) + "$")
    if not body.endswith("/**"):
        return files, None
    return files, re.compile(head + _glob(body[: -len("/**")]) + "$")


def _excludes(patterns: Sequence[str]) -> _Excludes:
    pairs = [_pattern(pattern) for pattern in patterns]
    return _Excludes(
        files=tuple(f for f, _ in pairs), directories=tuple(d for _, d in pairs if d is not None)
    )


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _carriable(rel: str) -> None:
    """Refuse a name rclone's list of paths cannot carry, one path per line."""
    if "\n" in rel or "\r" in rel:
        raise WalkRefused(f"a file name holds a line break, which a list of paths cannot carry: {rel!r}")
    try:
        rel.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise WalkRefused(f"a file name is not valid UTF-8: {rel!r}") from exc


def _passed_or_queued(
    item: os.DirEntry, rel: str, matcher: _Excludes, pending: list[tuple[Path, str]]
) -> bool:
    """Whether the walk is done with one entry: a symbolic link passed over, as
    rclone does without ``--links``, or a folder queued unless excluded. Raises
    what reading the entry raises."""
    if item.is_symlink():
        return True
    if item.is_dir(follow_symlinks=False):
        if not matcher.directory(rel):
            pending.append((Path(item.path), rel + "/"))
        return True
    return False


def walk(
    root: Path, excludes: Sequence[str], *, hash_paths: Iterable[str] = (),
    racy_after_ns: int | None = None, clock_ns=time.time_ns,
) -> Walk:
    """Every regular file under ``root`` the mirror would carry, by rclone's rules.

    ``hash_paths``, and files modified from ``racy_after_ns`` on, are hashed. A
    vanished file is absent; a vanished directory, anything unreadable or a
    root that changed volume refuses the walk.
    """
    started = time.monotonic()
    if racy_after_ns is None:
        racy_after_ns = clock_ns() - RACY_SECONDS * 1_000_000_000
    root_dev = _device(root)
    matcher = _excludes(excludes)
    must_hash = frozenset(hash_paths)
    entries: dict[str, Entry] = {}
    pending: list[tuple[Path, str]] = [(root, "")]
    while pending:
        directory, prefix = pending.pop()
        try:
            listing = list(os.scandir(directory))
        except FileNotFoundError:
            # NOT ABSENCE. A folder gone since it was listed is a rename or an
            # unmount under the walk, and read as absence its files would be
            # archived off the mirror.
            raise WalkRefused(
                f"{directory} was listed and then was not there, so the walk did "
                f"not see the whole library"
            ) from None
        except OSError as exc:
            raise WalkRefused(f"{directory} could not be listed: {exc}") from exc
        for item in listing:
            rel = f"{prefix}{item.name}"
            try:
                if _passed_or_queued(item, rel, matcher, pending):
                    continue
                status = item.stat(follow_symlinks=False)
                if not stat.S_ISREG(status.st_mode) or matcher.file(rel):
                    continue
                _carriable(rel)
                digest = None
                if rel in must_hash or status.st_mtime_ns >= racy_after_ns:
                    digest = _hash(Path(item.path))
            except FileNotFoundError:
                continue
            except OSError as exc:
                raise WalkRefused(f"{item.path} could not be read: {exc}") from exc
            entries[rel] = Entry(size=status.st_size, mtime_ns=status.st_mtime_ns, sha256=digest)
    if _device(root) != root_dev:
        raise WalkRefused(f"the library root {root} changed volume while it was walked")
    return Walk(
        entries=entries, racy_after_ns=racy_after_ns, seconds=time.monotonic() - started,
        root_dev=root_dev,
    )


def _device(root: Path) -> int:
    try:
        return os.stat(root).st_dev
    except FileNotFoundError:
        raise WalkRefused(f"the library root {root} is not there") from None
    except OSError as exc:
        raise WalkRefused(f"the library root {root} could not be read: {exc}") from exc


def still_removed(root: Path, root_dev: int, paths: Sequence[str]) -> str:
    """Why a quick run must not archive ``paths`` now, or an empty string: the
    root must still be the walked volume and every path still absent."""
    try:
        if os.stat(root).st_dev != root_dev:
            return f"the library root {root} is on another volume than the one walked"
    except OSError as exc:
        return f"the library root {root} could not be read before the archive: {exc}"
    for rel in paths:
        try:
            os.lstat(root / rel)
        except FileNotFoundError:
            continue
        except OSError as exc:
            return f"{rel} could not be read before the archive: {exc}"
        return f"{rel} was found removed by the walk and is there again"
    return ""


def difference(
    recorded: Mapping[str, Entry], walked: Mapping[str, Entry], *, self_written: Iterable[str] = ()
) -> Difference:
    """What a walk differs from the record by, each list sorted."""
    added: list[str] = []
    changed: list[str] = []
    rewritten: list[str] = []
    doubted: list[str] = []
    for rel, now in walked.items():
        was = recorded.get(rel)
        if was is None:
            added.append(rel)
        elif was == DOUBT:
            doubted.append(rel)
        elif was.size != now.size or was.mtime_ns != now.mtime_ns:
            changed.append(rel)
        elif was.sha256 is not None and was.sha256 != now.sha256:
            rewritten.append(rel)
    removed = [rel for rel in recorded if rel not in walked]
    return Difference(
        added=tuple(sorted(added)), changed=tuple(sorted(changed)),
        rewritten=tuple(sorted(rewritten)), removed=tuple(sorted(removed)),
        self_written=frozenset(self_written), doubted=tuple(sorted(doubted)),
    )


def settled(before: Walk, after: Walk) -> dict[str, Entry]:
    """The entries both walks agree on, DOUBT for the rest of the first walk's;
    a path only the second saw is left out, so the next run reads it as added."""
    out: dict[str, Entry] = {}
    for rel, was in before.entries.items():
        now = after.entries.get(rel)
        out[rel] = was if now is not None and was.agrees(now) else DOUBT
    return out


def manifest_path() -> Path:
    return config.state_path(MANIFEST_KEY)


def fingerprint_path() -> Path:
    return config.state_path(FINGERPRINT_KEY)


def invalidate(path: Path) -> None:
    """Remove one record before the transfer it describes. Raises on failure,
    and the caller does not transfer over that."""
    path.unlink(missing_ok=True)


def read_manifest() -> tuple[Manifest | None, str]:
    """The record, or None and why there is none to trust. Every failure is a
    reason, never an exception: the answer is the same full run."""
    path = manifest_path()
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return None, "no record of the last completed backup is kept here"
    except OSError as exc:
        return None, f"the record of the last backup could not be read: {exc}"
    try:
        data = json.loads(gzip.decompress(raw).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("not an object")
        if data.get("schema_version") != SCHEMA_VERSION:
            return None, (
                f"the record of the last backup is at schema version "
                f"{data.get('schema_version')!r} and this build reads {SCHEMA_VERSION}"
            )
        entries = {
            str(rel): Entry(
                size=int(row[0]), mtime_ns=int(row[1]),
                sha256=None if row[2] is None else str(row[2]),
            )
            for rel, row in data["entries"].items()
        }
        manifest = Manifest(
            library_root=str(data["library_root"]),
            volume_id=None if data["volume_id"] is None else str(data["volume_id"]),
            dest=str(data["dest"]), archive_root=str(data["archive_root"]),
            excludes=tuple(str(p) for p in data["excludes"]),
            written_at=str(data["written_at"]), entries=entries, token=str(data["token"]),
        )
    except (OSError, EOFError, ValueError, KeyError, TypeError, IndexError, AttributeError,
            zlib.error) as exc:
        return None, f"the record of the last backup is damaged: {exc}"
    return manifest, ""


def manifest_mismatch(manifest: Manifest, cfg: config.Config, excludes: Sequence[str]) -> str:
    """Why a record cannot describe this backup, or an empty string when it can."""
    checks = (
        ("library root", manifest.library_root, str(cfg.library.root)),
        ("volume identity", manifest.volume_id, cfg.library.volume_id),
        ("mirror", manifest.dest, str(cfg.backup.dest)),
        ("archive root", manifest.archive_root, str(cfg.backup.archive_root)),
        ("exclude set", list(manifest.excludes), list(excludes)),
    )
    for name, held, now in checks:
        if held != now:
            return f"the record of the last backup was kept for another {name}"
    return ""


def new_token() -> str:
    return uuid.uuid4().hex


def write_manifest(
    cfg: config.Config, excludes: Sequence[str], entries: Mapping[str, Entry], *,
    at: datetime, token: str,
) -> Path:
    payload = {
        "token": token, "schema_version": SCHEMA_VERSION,
        "library_root": str(cfg.library.root), "volume_id": cfg.library.volume_id,
        "dest": str(cfg.backup.dest), "archive_root": str(cfg.backup.archive_root),
        "excludes": list(excludes), "written_at": at.isoformat(),
        "entries": {
            rel: [entry.size, entry.mtime_ns, entry.sha256]
            for rel, entry in sorted(entries.items())
        },
    }
    path = manifest_path()
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    config.atomic_write_bytes(gzip.compress(raw, mtime=0), path)
    return path


def database_fingerprint(files: Sequence[Path], folders: Sequence[Path]) -> str | None:
    """One digest of ``files`` hashed whole (absent recorded as such) and
    ``folders`` by size and time, or None when anything could not be read."""
    digest = hashlib.sha256()
    try:
        for path in files:
            digest.update(f"file {path}\n".encode())
            try:
                digest.update(_hash(path).encode())
            except FileNotFoundError:
                digest.update(b"absent")
            digest.update(b"\n")
        for folder in folders:
            digest.update(f"folder {folder}\n".encode())
            found = walk(folder, (), racy_after_ns=1 << 62)
            for rel, entry in sorted(found.entries.items()):
                digest.update(f"{rel}\t{entry.size}\t{entry.mtime_ns}\n".encode())
    except (OSError, WalkRefused):
        return None
    return digest.hexdigest()


def read_fingerprint() -> dict | None:
    """The last completed snapshot's fingerprint record, or None for any doubt."""
    try:
        data = json.loads(fingerprint_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        return None
    return data


def fingerprint_key(cfg: config.Config, marker: str | None) -> dict[str, object]:
    """What a fingerprint must have been taken for to be compared with this one."""
    return {
        "database": str(config.state_path("rekordbox_db", cfg)),
        "db_dest_root": str(cfg.backup.db_dest_root), "identity": marker,
    }


def write_fingerprint(key: Mapping[str, object], fingerprint: str, *, at: datetime) -> Path:
    payload = {
        "schema_version": SCHEMA_VERSION, **key, "fingerprint": fingerprint,
        "written_at": at.isoformat(),
    }
    path = fingerprint_path()
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def first_uncomposed(paths: Iterable[str]) -> str | None:
    """The first path not in NFC, which a quick run's lookup could miss on a
    remote that composes names, or None."""
    return next((path for path in paths if not unicodedata.is_normalized("NFC", path)), None)


def paths_from(feed: str | None) -> tuple[str, ...]:
    """The paths a :func:`paths_list` list carries, split on the line feed alone,
    as rclone splits (``str.splitlines`` splits on more)."""
    return tuple(feed.split("\n")[:-1]) if feed else ()


def paths_list(paths: Iterable[str]) -> str:
    """A list rclone reads from standard input with ``--files-from-raw -``."""
    return "".join(f"{path}\n" for path in paths)


@dataclass(frozen=True, slots=True)
class Census:
    """How many files outside the state folder the last completed files portion
    walked, for this root and mirror; None where a census is there and cannot be
    read, which still says a backup happened."""

    files: int | None


def census_path() -> Path:
    return config.state_path(CENSUS_KEY)


def held(rel: str, state_dirname: str) -> bool:
    """Whether a walked path is the library's own, rather than its state folder."""
    return not (rel == state_dirname or rel.startswith(f"{state_dirname}/"))


def count_held(entries: Iterable[str], state_dirname: str) -> int:
    """How many walked paths lie outside the library's own state folder."""
    return sum(1 for rel in entries if held(rel, state_dirname))


def probe(
    root: Path, excludes: Sequence[str], state_dirname: str, *, first: bool = False
) -> tuple[bool, int]:
    """Whether the root holds any file the mirror carries, and how many lie
    outside the state folder (with ``first``, stopping at one). Stands in for a
    walk that refused, so it never refuses: an unlistable folder counts nothing
    and an untranslatable exclude is left out.
    """
    matcher = _excludes([p for p in excludes if not any(c in _UNTRANSLATED for c in p)])
    anything = False
    found = 0
    pending: list[tuple[Path, str]] = [(root, "")]
    while pending:
        directory, prefix = pending.pop()
        try:
            listing = list(os.scandir(directory))
        except OSError:
            continue
        for item in listing:
            rel = f"{prefix}{item.name}"
            try:
                if _passed_or_queued(item, rel, matcher, pending):
                    continue
                regular = item.is_file(follow_symlinks=False)
            except OSError:
                continue
            if not regular or matcher.file(rel):
                continue
            anything = True
            if held(rel, state_dirname):
                found += 1
                if first:
                    return True, found
    return anything, found


def root_still_holds(
    root: Path, root_dev: int, excludes: Sequence[str], state_dirname: str, *, files: bool
) -> str:
    """Why the full mirror must not run now, or an empty string: the root must
    still be the planned volume and, where it held the library's files, hold one."""
    try:
        if os.stat(root).st_dev != root_dev:
            return f"the library root {root} is on another volume than the one the plan read"
    except OSError as exc:
        return f"the library root {root} could not be read before the mirror: {exc}"
    if files and not probe(root, excludes, state_dirname, first=True)[1]:
        return (
            f"the library root {root} held the library's files when the backup "
            f"was planned and holds none now"
        )
    return ""


def read_census(cfg: config.Config) -> Census | None:
    """The census kept for this root and mirror, or None when there is none.
    One that is there and unreadable is a backup with its count unknown."""
    try:
        raw = census_path().read_bytes()
    except FileNotFoundError:
        return None
    except OSError:
        return Census(files=None)
    try:
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("not this schema")
        if data["library_root"] != str(cfg.library.root) or data["dest"] != str(cfg.backup.dest):
            return None
        files = data["files"]
        if files is not None and (not isinstance(files, int) or isinstance(files, bool) or files < 0):
            raise ValueError("not a count")
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        return Census(files=None)
    return Census(files=files)


def write_census(cfg: config.Config, files: int, *, at: datetime) -> Path:
    """Keep the census a completed files portion leaves. Never removed before a
    transfer, so a failed run still leaves it saying what the library held."""
    payload = {
        "schema_version": SCHEMA_VERSION, "library_root": str(cfg.library.root),
        "dest": str(cfg.backup.dest), "files": files, "written_at": at.isoformat(),
    }
    path = census_path()
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


__all__ = [
    "CENSUS_KEY", "DOUBT", "LIBRARY_FLOOR", "FINGERPRINT_KEY", "MANIFEST_KEY", "QUICK_LIMIT",
    "RACY_SECONDS", "SCHEMA_VERSION", "Census", "Difference", "Entry", "Manifest", "Walk",
    "WalkRefused", "census_path", "count_held", "database_fingerprint", "difference",
    "fingerprint_key", "fingerprint_path", "first_uncomposed", "held", "invalidate",
    "manifest_mismatch", "manifest_path", "new_token", "paths_from", "paths_list", "probe",
    "read_census", "read_fingerprint", "read_manifest", "root_still_holds", "settled",
    "still_removed", "walk", "write_census", "write_fingerprint", "write_manifest",
]
