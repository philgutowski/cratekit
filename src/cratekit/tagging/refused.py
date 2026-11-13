"""When each record shop began refusing this client, kept from run to run (U284).

WHY IT IS KEPT. A sweep counts a catalogue's refusals in a row for its own run
and forgets them when the run ends (U281), so nothing could say how long a
catalogue had refused. Sitting 94's sync pass stopped at its tag step over a
Beatport that had refused every lookup since sitting 93, three days earlier,
and the refusal said nothing of it. A block of minutes and a block of days ask
different things of a person, so the date a refusal began is kept here, read
by the sweep's report and by the refusal a pass stops on.

WHAT MOVES IT. A refusal the catalogue was SENT and answered, a 403, a spent
rate limit or a challenge page, sets ``since`` once and moves ``last``. A match
or a miss means the catalogue answered this client, and clears it. An outage or
a parse break says nothing about whether it would refuse, and a refusal the run
answered from its own count (U281's ``not asked``) was never sent, so neither
moves it.

WHO WRITES IT. The ``tag folder`` worker's run count, :func:`cratekit.tagging.
searchers.for_run`, and nothing else: a searcher a test or a library caller
builds with no run count keeps no record, so nothing but a sweep touches this
file. Discogs is not under the run count (U244 keeps its own memory) and is not
recorded here.

THE READ, MERGE AND REPLACE IS HELD UNDER A SIBLING LOCK, the ISRC cache's
pattern: two sweeps in two processes never lose each other's dates, and a lock
not had in time skips the write rather than waiting on a holder that is not
moving.

IT NEVER RAISES. A record that cannot be read reads as none, and one that
cannot be written is left as it was: the cost is the words "since" in a
sentence, never a file left untagged or a sweep that fails.
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from cratekit.core import config

LOG = logging.getLogger(__name__)

#: The two state entries, declared in :data:`cratekit.core.config.STATE_FILES`.
KEY = "catalogue_refusals"
LOCK_KEY = "catalogue_refusals_lock"

#: How long a write waits for the lock before it is skipped, and how often it looks.
LOCK_WAIT_S = 2.0
LOCK_POLL_S = 0.05

#: The record's shape, written into the file so a later build can tell its own.
VERSION = 1


@dataclass(frozen=True, slots=True)
class Standing:
    """One catalogue refusing this client: since when, the latest refusal, how many."""

    since: str
    last: str
    count: int


def _now() -> datetime:
    """The clock, a module attribute so a test can fix it."""
    return datetime.now(timezone.utc)


def stamp(when: datetime) -> str:
    """A moment as the record writes it, UTC to the second."""
    return when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _path() -> Path:
    return config.state_path(KEY)


def _lock_path() -> Path:
    return config.state_path(LOCK_KEY)


def _parse(text: str) -> dict[str, Standing]:
    """The standings a file's text holds, skipping any entry this build cannot read."""
    try:
        document = json.loads(text)
    except ValueError:
        return {}
    held = document.get("catalogues") if isinstance(document, dict) else None
    if not isinstance(held, dict):
        return {}
    read: dict[str, Standing] = {}
    for source, entry in held.items():
        if not isinstance(entry, dict):
            continue
        since, last, count = entry.get("since"), entry.get("last"), entry.get("count")
        if isinstance(since, str) and since and isinstance(last, str) and isinstance(count, int):
            read[str(source)] = Standing(since=since, last=last, count=count)
    return read


def read(path: Path | None = None) -> dict[str, Standing]:
    """Every catalogue the record says is refusing this client, or none.

    Never raises: a missing file, one that cannot be read and one that does
    not parse all read as no catalogue refusing.
    """
    try:
        text = (path or _path()).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return {}
    return _parse(text)


def since(sources: Iterable[str]) -> dict[str, str]:
    """The date each of ``sources`` began refusing, empty where none is recorded."""
    held = read()
    return {source: held[source].since if source in held else "" for source in sources}


@contextmanager
def _locked(lock: Path, sleep: Callable[[float], None]) -> Iterator[bool]:
    """Hold the sibling lock and yield True, or yield False when it was not had in time.

    THE LOCK FILE IS NEVER UNLINKED, for the ISRC cache's reason: one holder
    unlinking the name while another creates a fresh file at it is how two
    processes each hold "the" lock.
    """
    try:
        config._mkdir_private(lock.parent)
        fd = os.open(lock, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
    except OSError:
        yield False
        return
    try:
        try:
            import fcntl  # noqa: PLC0415 - POSIX only, see the except
        except ImportError:  # pragma: no cover - no advisory locks here
            fcntl = None
        had = fcntl is None
        polls = 0
        while not had and polls * LOCK_POLL_S < LOCK_WAIT_S:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
            except BlockingIOError:
                polls += 1
                sleep(LOCK_POLL_S)
        yield had
    finally:
        os.close(fd)  # closing the descriptor releases the lock; the file stays


def _write(path: Path, held: Mapping[str, Standing]) -> None:
    document = {
        "version": VERSION,
        "catalogues": {
            source: {"since": entry.since, "last": entry.last, "count": entry.count}
            for source, entry in sorted(held.items())
        },
    }
    config.atomic_write_bytes(
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"), path
    )


def _change(
    source: str,
    refused: bool,
    *,
    path: Path | None,
    lock: Path | None,
    sleep: Callable[[float], None],
) -> None:
    """Record ``source`` refusing (``refused``) or answering, under the lock; never raise."""
    at = path or _path()
    try:
        if not refused and source not in read(at):
            # NOTHING TO CLEAR, which is every answer of a catalogue that is
            # not refusing: no lock is taken and nothing is written.
            return
        with _locked(lock or _lock_path(), sleep) as had:
            if not had:
                LOG.info("the catalogue refusal record was not written: its lock was held")
                return
            held = read(at)
            if refused:
                now = stamp(_now())
                before = held.get(source)
                held[source] = Standing(
                    since=before.since if before is not None else now,
                    last=now,
                    count=(before.count if before is not None else 0) + 1,
                )
            elif held.pop(source, None) is None:
                return
            _write(at, held)
    except (OSError, ValueError) as exc:
        LOG.info("the catalogue refusal record was not written: %s", exc)


def refused(
    source: str,
    *,
    path: Path | None = None,
    lock: Path | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """``source`` refused a lookup it was sent: keep when it began, move its latest."""
    _change(source, True, path=path, lock=lock, sleep=sleep)


def answered(
    source: str,
    *,
    path: Path | None = None,
    lock: Path | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """``source`` answered this client, a match or a miss: it is refusing no longer."""
    _change(source, False, path=path, lock=lock, sleep=sleep)


__all__ = [
    "KEY",
    "LOCK_KEY",
    "LOCK_POLL_S",
    "LOCK_WAIT_S",
    "VERSION",
    "Standing",
    "answered",
    "read",
    "refused",
    "since",
    "stamp",
]
