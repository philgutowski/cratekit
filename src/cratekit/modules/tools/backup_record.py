"""U317: the record of what the last completed backup left, and the walk read against it.

A full backup lists the remote and compares every file on both sides, which on
the author's library is most of the 85 to 135 minutes a run takes, almost none
of it sending. This module is what lets a run that changed little skip that
listing: Cratekit keeps its own record of what the last completed mirror left,
walks the library (seconds, stat only) and compares the walk with the record.
An empty difference is a SKIP, a small one is a QUICK run that sends only it,
and anything this module cannot vouch for is a FULL run, which is the backup as
it always was.

THE RECORD DESCRIBES THE REMOTE, so it is held to three rules, each a merge
blocker of the card that built it.

* **It is written only after a mirror completed**, by ``run_backup``, and it is
  removed before the first transfer it describes. A run that fails or is killed
  part way therefore leaves no record, and the next run is full. A record that
  survived a failed run could be compared with a tree a person then put back,
  and would answer "nothing changed" over a remote the failed run half rewrote.
* **An entry is trusted only when the walk before the transfer and the walk
  after it agree.** A file that changed, appeared or vanished while rclone ran
  may or may not be on the remote in the version the record would claim, so it
  is kept as a DOUBT entry that matches no file, and the next run sends it
  again with the times ignored, or archives it.
* **A file whose time cannot be trusted carries a content hash.** A write that
  lands inside the file system's time granularity of an earlier one leaves the
  size and the time where they were (two seconds on exFAT), so a file modified
  within :data:`RACY_SECONDS` of the walk is hashed, and the next run hashes it
  again rather than trusting its time. git calls this the racily clean entry.

ANYTHING THE WALK CANNOT READ IS NOT ABSENCE. A directory that cannot be listed
would read as every file under it removed, and a quick run would archive them
all off the remote. So an unreadable directory, a name rclone's list cannot
carry, or an exclude this module cannot translate refuses the walk with
:class:`WalkRefused`, and the run is full, where rclone itself meets the
directory and refuses to delete over an input error.

THE DATABASE IS NOT MIRRORED BUT SNAPSHOTTED, so it gets a FINGERPRINT rather
than a record: the content hash of the database set, with the settings folders
and an outside analysis share by size and time. A database equal to the last
completed snapshot's needs no new snapshot. The fingerprint reads the live
database, so :func:`database_fingerprint` is called only after the plan has
confirmed both rekordbox processes gone, which is the one read CLAUDE.md's
backup rule allows.

Both records are INSTALLATION state, never library state. The library's own
state folder is inside the mirrored tree, so a record kept there would change
the tree every time it was written and no run could ever skip.
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

#: The inventory keys of the two records. Named once, so the writer, the reader
#: and the invalidation cannot disagree about which file is meant.
MANIFEST_KEY = "backup_manifest"
FINGERPRINT_KEY = "backup_database_fingerprint"
#: R-1761. How many files the last completed mirror walked, the third record.
CENSUS_KEY = "backup_census"

#: Bumped whenever the shape of either record changes. A record of any other
#: version is not read and the run is full, which costs one slow run and never
#: a wrong skip.
SCHEMA_VERSION = 1

#: How close to the walk a file's modification time may sit before the time
#: alone is not trusted and the content is hashed. exFAT keeps two seconds and
#: HFS+ one; the rest is margin for a clock that is not the volume's own.
RACY_SECONDS = 10

#: The most paths a quick run sends or archives. Past this a quick run's one
#: lookup per path costs more than the full run's one listing of the remote, so
#: the run is full. A choice of speed and never of safety: both kinds send
#: every change.
QUICK_LIMIT = 10_000

#: R-1761. A library root holding fewer than one file in this many of the
#: files the last completed backup walked is not proven to be the library: a
#: mount point a stray file landed in, where ``rclone sync`` would empty the
#: mirror to match. A person who removed that much is asked for
#: ``--library-emptied``, and the archive would have kept what went either way.
LIBRARY_FLOOR = 10

#: Characters a pattern may carry that :func:`_pattern` does not translate. A
#: pattern holding one is refused rather than guessed at, because an exclude
#: read differently here and in rclone is a file the walk counts and the mirror
#: never sends, or the reverse.
_UNTRANSLATED = frozenset("[]{}\\")


class WalkRefused(Exception):
    """The walk met something it cannot vouch for, so the run must be full."""


@dataclass(frozen=True, slots=True)
class Entry:
    """One file as the record holds it: size, time in nanoseconds, and a hash
    only where the time cannot be trusted."""

    size: int
    mtime_ns: int
    sha256: str | None = None

    def agrees(self, other: Entry) -> bool:
        """The same file to both readings, hashes compared where both hold one."""
        if self.size != other.size or self.mtime_ns != other.mtime_ns:
            return False
        if self.sha256 is not None and other.sha256 is not None:
            return self.sha256 == other.sha256
        return self.sha256 is None and other.sha256 is None


#: The entry a path gets when the record cannot say what the remote holds for
#: it. No file has a negative size, so it agrees with nothing, and the next run
#: sends the file if it is there and archives it if it is not.
DOUBT = Entry(size=-1, mtime_ns=-1)


@dataclass(frozen=True, slots=True)
class Walk:
    """One reading of the library: every file the mirror would carry."""

    entries: Mapping[str, Entry]
    #: Files modified at or after this instant were hashed.
    racy_after_ns: int
    seconds: float
    #: The device the library root was on throughout the walk. A quick run's
    #: archive is held to it, so a volume unmounted after the plan is not read
    #: as every file on it removed.
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
    #: A token this record was kept under, which the files fact published with
    #: it carries too. The mirror has other writers, a second installation or a
    #: build before U317 on the same state, and each publishes a files fact
    #: without this token, so a record whose token the library's fact no longer
    #: carries is not trusted.
    token: str = ""


@dataclass(frozen=True, slots=True)
class Difference:
    """What changed between the record and a walk, by path, in sorted order.

    ``rewritten`` is a file whose size and time held and whose content hash
    moved. It is apart from ``changed`` because rclone, which compares size and
    time, sends it only when told to ignore the times.

    ``self_written`` names the changed paths that are the backup's own record
    of its ages, which every run rewrites after its transfer. They are carried
    in the lists above and left out of :attr:`anything`.
    """

    added: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()
    rewritten: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    self_written: frozenset[str] = field(default_factory=frozenset)
    #: Present paths the record held as a DOUBT. They are sent with the times
    #: ignored, because what made them a doubt may be a rewrite that kept its
    #: size and time, which a comparison of size and time would never send.
    doubted: tuple[str, ...] = ()

    @property
    def paths(self) -> tuple[str, ...]:
        return (*self.added, *self.changed, *self.doubted, *self.rewritten, *self.removed)

    @property
    def anything(self) -> bool:
        """True when something other than the backup's own record changed."""
        return any(path not in self.self_written for path in self.paths)

    def counts(self) -> dict[str, int]:
        """How many paths changed by kind, the backup's own record left out.

        Left out because a person who added one file is told one was added; the
        fact file the last run rewrote still travels with them, and rclone's
        own count of what it sent includes it.
        """

        def counted(paths: tuple[str, ...]) -> int:
            return sum(1 for path in paths if path not in self.self_written)

        return {
            "added": counted(self.added),
            "changed": counted(self.changed) + counted(self.doubted),
            "rewritten": counted(self.rewritten),
            "removed": counted(self.removed),
        }


# ---------------------------------------------------------------------------
# Excludes, read the way rclone reads them
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Excludes:
    files: tuple[re.Pattern[str], ...]
    directories: tuple[re.Pattern[str], ...]

    def file(self, rel: str) -> bool:
        return any(p.search(rel) for p in self.files)

    def directory(self, rel: str) -> bool:
        return any(p.search(rel) for p in self.directories)


def _glob(text: str) -> str:
    """One rclone glob as a regular expression body.

    ``**`` matches across separators, ``*`` and ``?`` within one path segment,
    and every other character is itself. rclone's classes, alternations and
    escapes are refused by the caller before this is reached.
    """
    out: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("**", index):
            out.append(".*")
            index += 2
        elif text[index] == "*":
            out.append("[^/]*")
            index += 1
        elif text[index] == "?":
            out.append("[^/]")
            index += 1
        else:
            out.append(re.escape(text[index]))
            index += 1
    return "".join(out)


def _pattern(pattern: str) -> tuple[re.Pattern[str], re.Pattern[str] | None]:
    """A file matcher and, for ``dir/**``, a directory matcher, for one exclude.

    rclone anchors a pattern that starts with a slash at the root and matches
    any other against the END of the path, at a segment boundary. A pattern
    ending ``/**`` also excludes the directory itself, so rclone never descends
    into it; the walk prunes it the same way, which is what keeps a folder only
    the system can read, ``.Spotlight-V100`` on a Mac volume, from refusing
    every quick run.
    """
    if any(char in _UNTRANSLATED for char in pattern):
        raise WalkRefused(
            f"the exclude {pattern!r} uses a pattern this walk does not read the "
            f"way rclone does"
        )
    anchored = pattern.startswith("/")
    body = pattern[1:] if anchored else pattern
    head = "^" if anchored else "(?:^|/)"
    files = re.compile(head + _glob(body) + "$")
    directories = None
    if body.endswith("/**"):
        directories = re.compile(head + _glob(body[: -len("/**")]) + "$")
    return files, directories


def _excludes(patterns: Sequence[str]) -> _Excludes:
    files: list[re.Pattern[str]] = []
    directories: list[re.Pattern[str]] = []
    for pattern in patterns:
        matcher, directory = _pattern(pattern)
        files.append(matcher)
        if directory is not None:
            directories.append(directory)
    return _Excludes(files=tuple(files), directories=tuple(directories))


# ---------------------------------------------------------------------------
# The walk
# ---------------------------------------------------------------------------


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


def walk(
    root: Path,
    excludes: Sequence[str],
    *,
    hash_paths: Iterable[str] = (),
    racy_after_ns: int | None = None,
    clock_ns=time.time_ns,
) -> Walk:
    """Every regular file under ``root`` the mirror would carry, by relative path.

    The rules are rclone's own for the local side of a sync, so the walk and
    the mirror describe one tree: the excludes as :func:`_pattern` reads them,
    symbolic links skipped (rclone skips one without ``--links``), and anything
    that is not a regular file or a directory ignored.

    ``hash_paths`` are hashed whatever their time, because the record hashed
    them; every file modified at or after ``racy_after_ns`` is hashed because
    its time cannot yet be trusted. The default is :data:`RACY_SECONDS` before
    the walk began, and a caller walking twice passes the first walk's value so
    the two readings hash the same files.

    A FILE THAT VANISHED BETWEEN BEING LISTED AND BEING READ IS ABSENT, which is
    true of a file. A DIRECTORY that did refuses the walk, as does anything
    else that cannot be read, and a root that changed volume while it was read.
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
            # NOT ABSENCE. A folder listed a moment ago and gone now is a folder
            # renamed under the walk or a volume unmounted under it, and read as
            # absence its files would be archived off the mirror. The full run
            # this refusal makes meets the same state through rclone, which
            # refuses to delete over a directory that is gone; an empty
            # directory left where the volume was is the residual the full
            # sync carries from before U317.
            raise WalkRefused(
                f"{directory} was listed and then was not there, so the walk did "
                f"not see the whole library"
            ) from None
        except OSError as exc:
            raise WalkRefused(f"{directory} could not be listed: {exc}") from exc
        for item in listing:
            rel = f"{prefix}{item.name}"
            try:
                if item.is_symlink():
                    continue
                if item.is_dir(follow_symlinks=False):
                    if not matcher.directory(rel):
                        pending.append((Path(item.path), rel + "/"))
                    continue
                status = item.stat(follow_symlinks=False)
            except FileNotFoundError:
                continue
            except OSError as exc:
                raise WalkRefused(f"{item.path} could not be read: {exc}") from exc
            if not stat.S_ISREG(status.st_mode) or matcher.file(rel):
                continue
            _carriable(rel)
            digest = None
            if rel in must_hash or status.st_mtime_ns >= racy_after_ns:
                try:
                    digest = _hash(Path(item.path))
                except FileNotFoundError:
                    continue
                except OSError as exc:
                    raise WalkRefused(f"{item.path} could not be read: {exc}") from exc
            entries[rel] = Entry(size=status.st_size, mtime_ns=status.st_mtime_ns, sha256=digest)
    if _device(root) != root_dev:
        raise WalkRefused(f"the library root {root} changed volume while it was walked")
    return Walk(
        entries=entries,
        racy_after_ns=racy_after_ns,
        seconds=time.monotonic() - started,
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
    """Why a quick run must not archive ``paths`` now, or an empty string.

    Asked just before the archive runs, because the plan's walk can be minutes
    old by then: the root must still be the volume the walk read, and every
    path the walk found removed must still be absent. A path that came back is
    not to be archived off the mirror, and a root on another volume, or gone,
    is a library nobody walked.
    """
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
        added=tuple(sorted(added)),
        changed=tuple(sorted(changed)),
        rewritten=tuple(sorted(rewritten)),
        removed=tuple(sorted(removed)),
        self_written=frozenset(self_written),
        doubted=tuple(sorted(doubted)),
    )


def settled(before: Walk, after: Walk) -> dict[str, Entry]:
    """The entries a completed transfer leaves trusted, and DOUBT for the rest.

    A path both walks agree on is what the remote holds. A path that changed,
    or that only the walk before the transfer saw, may be on the remote in
    either version or in none, so it is a doubt. A path only the walk after it
    saw is left out, so the next run reads it as added.
    """
    out: dict[str, Entry] = {}
    for rel, was in before.entries.items():
        now = after.entries.get(rel)
        out[rel] = was if now is not None and was.agrees(now) else DOUBT
    return out


# ---------------------------------------------------------------------------
# The two records
# ---------------------------------------------------------------------------


def manifest_path() -> Path:
    return config.state_path(MANIFEST_KEY)


def fingerprint_path() -> Path:
    return config.state_path(FINGERPRINT_KEY)


def invalidate(path: Path) -> None:
    """Remove one record before the transfer it describes. Raises on failure.

    A record that could not be removed would survive a run that then failed,
    which is the one state this module exists to keep out of reach, so the
    caller does not transfer over an ``OSError`` from here.
    """
    path.unlink(missing_ok=True)


def read_manifest() -> tuple[Manifest | None, str]:
    """The record, or None and why there is none to trust.

    Every failure is a reason, never an exception: whatever is wrong with the
    record, the answer is the same full run, and the reason is what the report
    says about why it was full.
    """
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
                size=int(row[0]),
                mtime_ns=int(row[1]),
                sha256=None if row[2] is None else str(row[2]),
            )
            for rel, row in data["entries"].items()
        }
        manifest = Manifest(
            library_root=str(data["library_root"]),
            volume_id=None if data["volume_id"] is None else str(data["volume_id"]),
            dest=str(data["dest"]),
            archive_root=str(data["archive_root"]),
            excludes=tuple(str(p) for p in data["excludes"]),
            written_at=str(data["written_at"]),
            entries=entries,
            token=str(data["token"]),
        )
    except (
        OSError, EOFError, ValueError, KeyError, TypeError, IndexError,
        AttributeError, zlib.error,
    ) as exc:
        # Every way a damaged file fails to parse, the compressed stream's own
        # error included: whatever is wrong, the answer is a full run.
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
    cfg: config.Config,
    excludes: Sequence[str],
    entries: Mapping[str, Entry],
    *,
    at: datetime,
    token: str,
) -> Path:
    payload = {
        "token": token,
        "schema_version": SCHEMA_VERSION,
        "library_root": str(cfg.library.root),
        "volume_id": cfg.library.volume_id,
        "dest": str(cfg.backup.dest),
        "archive_root": str(cfg.backup.archive_root),
        "excludes": list(excludes),
        "written_at": at.isoformat(),
        "entries": {
            rel: [entry.size, entry.mtime_ns, entry.sha256]
            for rel, entry in sorted(entries.items())
        },
    }
    path = manifest_path()
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    config.atomic_write_bytes(gzip.compress(raw, mtime=0), path)
    return path


def database_fingerprint(
    files: Sequence[Path], folders: Sequence[Path]
) -> str | None:
    """One digest of the database set's content and the folders that travel with it.

    ``files`` are hashed whole, each named, and an absent one is recorded as
    absent, since a sidecar that came or went is a different database.
    ``folders`` are read by size and time, through the same walk the mirror
    uses with no excludes. None when anything could not be read, which the
    caller takes as changed.
    """
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
        "db_dest_root": str(cfg.backup.db_dest_root),
        "identity": marker,
    }


def write_fingerprint(key: Mapping[str, object], fingerprint: str, *, at: datetime) -> Path:
    payload = {
        "schema_version": SCHEMA_VERSION,
        **key,
        "fingerprint": fingerprint,
        "written_at": at.isoformat(),
    }
    path = fingerprint_path()
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def first_uncomposed(paths: Iterable[str]) -> str | None:
    """The first path not in composed Unicode form (NFC), or None.

    A full sync matches names across a remote that composes them, because rclone
    normalises names when it compares two listings. A quick run lists nothing
    and looks each name up as written, so a decomposed name, which a Mac volume
    can hold, could miss the file on such a remote: a removal archived nothing
    and a change uploaded beside the old copy. Such a path makes the run full.
    """
    for path in paths:
        if not unicodedata.is_normalized("NFC", path):
            return path
    return None


def paths_from(feed: str | None) -> tuple[str, ...]:
    """The paths a list from :func:`paths_list` carries, split where rclone splits.

    On the line feed alone: ``str.splitlines`` also splits on separators a file
    name may hold, which rclone reads as part of the name.
    """
    if not feed:
        return ()
    return tuple(feed.split("\n")[:-1])


def paths_list(paths: Iterable[str]) -> str:
    """A list rclone reads from standard input with ``--files-from-raw -``."""
    return "".join(f"{path}\n" for path in paths)


# ---------------------------------------------------------------------------
# The census: what proves the root is the library (R-1761)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Census:
    """How many files outside the library's own state folder the last completed
    files portion walked, for this library root and mirror.

    ``files`` is None where a backup was kept and its count cannot be read: a
    damaged census, or a run whose walk refused and whose probe found files.
    A count nobody can read still says a backup happened here.
    """

    files: int | None


def census_path() -> Path:
    return config.state_path(CENSUS_KEY)


def held(rel: str, state_dirname: str) -> bool:
    """Whether a walked path is the library's own, rather than its state folder."""
    return not (rel == state_dirname or rel.startswith(f"{state_dirname}/"))


def count_held(entries: Iterable[str], state_dirname: str) -> int:
    """How many walked paths lie outside the library's own state folder."""
    return sum(1 for rel in entries if held(rel, state_dirname))


def probe(root: Path, excludes: Sequence[str], state_dirname: str) -> tuple[bool, bool]:
    """Whether the root holds any file the mirror carries, and any outside the
    state folder, stopping at the first of the second kind.

    THE STAND IN FOR A WALK THAT REFUSED, and the check just before the mirror.
    Best effort by design and failing closed: a folder it cannot list is passed
    over, so what it cannot read is never counted as a file, and a root it can
    read nothing of reads as empty and is refused. An exclude the walk cannot
    translate is left out rather than refusing, since the probe stands in for
    a walk that may have refused for that very reason; what it then counts is
    the database set a configuration with such a name keeps under the root.
    """
    matcher = _excludes([p for p in excludes if not any(c in _UNTRANSLATED for c in p)])
    anything = False
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
                if item.is_symlink():
                    continue
                if item.is_dir(follow_symlinks=False):
                    if not matcher.directory(rel):
                        pending.append((Path(item.path), rel + "/"))
                    continue
                regular = item.is_file(follow_symlinks=False)
            except OSError:
                continue
            if not regular or matcher.file(rel):
                continue
            anything = True
            if held(rel, state_dirname):
                return True, True
    return anything, False


def root_still_holds(
    root: Path,
    root_dev: int,
    excludes: Sequence[str],
    state_dirname: str,
    *,
    files: bool,
) -> str:
    """Why the full mirror must not run now, or an empty string (R-1761).

    Asked just before ``rclone sync``, because the plan's walk can be minutes
    old: the root must still be the volume the plan read, and, where the plan
    found the library's files, must still hold one. A volume lost in between
    leaves a folder that ``rclone sync`` would empty the mirror to match.
    """
    try:
        if os.stat(root).st_dev != root_dev:
            return f"the library root {root} is on another volume than the one the plan read"
    except OSError as exc:
        return f"the library root {root} could not be read before the mirror: {exc}"
    if files and not probe(root, excludes, state_dirname)[1]:
        return (
            f"the library root {root} held the library's files when the backup "
            f"was planned and holds none now"
        )
    return ""


def read_census(cfg: config.Config) -> Census | None:
    """The census kept for this root and mirror, or None when there is none.

    FAILING CLOSED: a census that is there and cannot be read is a backup that
    happened, with its count unknown, never no census. One kept for another
    root or mirror says nothing about this one.
    """
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


def write_census(cfg: config.Config, files: int | None, *, at: datetime) -> Path:
    """Keep the census a completed files portion leaves. NEVER removed before a
    transfer, unlike the record, so a failed run still leaves it saying what
    the library held."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        "library_root": str(cfg.library.root),
        "dest": str(cfg.backup.dest),
        "files": files,
        "written_at": at.isoformat(),
    }
    path = census_path()
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


__all__ = [
    "CENSUS_KEY",
    "DOUBT",
    "LIBRARY_FLOOR",
    "FINGERPRINT_KEY",
    "MANIFEST_KEY",
    "QUICK_LIMIT",
    "RACY_SECONDS",
    "SCHEMA_VERSION",
    "Census",
    "Difference",
    "Entry",
    "Manifest",
    "Walk",
    "WalkRefused",
    "census_path",
    "count_held",
    "database_fingerprint",
    "difference",
    "fingerprint_key",
    "fingerprint_path",
    "first_uncomposed",
    "held",
    "invalidate",
    "manifest_mismatch",
    "manifest_path",
    "new_token",
    "paths_from",
    "paths_list",
    "probe",
    "read_census",
    "read_fingerprint",
    "read_manifest",
    "root_still_holds",
    "settled",
    "still_removed",
    "walk",
    "write_census",
    "write_fingerprint",
    "write_manifest",
]
