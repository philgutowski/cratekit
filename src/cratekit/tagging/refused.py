"""When each record shop began refusing this client, kept from run to run (U284).

A sweep's run count forgets its refusals when the run ends (U281), and a block
of minutes and a block of days ask different things of a person, so the date
a refusal began is kept here, for the sweep's report and a pass's refusal.

A refusal the catalogue was SENT sets ``since`` once and moves ``last``; a
match or a miss clears it. An outage, a parse break or a refusal answered from
the run's own count says nothing, so moves nothing. Only a sweep's run count,
:func:`cratekit.tagging.searchers.for_run`, writes it; Discogs keeps its own
memory and is not recorded.

The read, merge and replace is held under a sibling lock, so two sweeps never
lose each other's dates, and a lock not had in time skips the write. It never
raises: the cost of a record unread or unwritten is the word "since" in a
sentence, never a sweep that fails.
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable, Iterable, Mapping
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
    except (ValueError, RecursionError):
        # A RECORD NESTED past the parser's depth reads as none.
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
    """Every catalogue the record says is refusing this client, or none; a
    missing, unreadable or unparsed file is none."""
    try:
        text = (path or _path()).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return {}
    return _parse(text)


def since(sources: Iterable[str]) -> dict[str, str]:
    """The date each of ``sources`` began refusing, empty where none is recorded."""
    held = read()
    return {source: held[source].since if source in held else "" for source in sources}


def _locked(lock: Path, sleep: Callable[[float], None]):
    """Hold the sibling lock and yield True, or yield False when it was not had in time."""
    return config.lock_within(lock, wait_s=LOCK_WAIT_S, poll_s=LOCK_POLL_S, sleep=sleep)


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
            # Nothing to clear: no lock is taken and nothing is written.
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
    except (OSError, ValueError, RecursionError) as exc:
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
