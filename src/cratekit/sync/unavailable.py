"""Which synced playlists the account answered not found for, and which are retired (U320).

``crate sync removed`` asks every synced playlist whether it still holds a
track taken off another, and a playlist it cannot read whole stops every
offer (R37). A playlist deleted on the account is never read whole again, so
before U320 one deleted playlist stopped every offer for good (R-1714). This
record is how such a playlist stops stopping them, without ever reading a
playlist that is only unreadable as gone.

A SIGHTING is one run in which the playlist was absent from the account's own
list AND its id answered the provider's not found, a 404 or the client's not
found class read along the failure's chain (:func:`answered_unavailable`).
Both, because the list alone stops on an empty page and publishes no total
(R-385), and because a failed open is otherwise any provider failure (R-1713):
an outage, a refused session or a rate limit records nothing, so a playlist
that is only unreadable is never retired.

A PLAYLIST IS RETIRED when a sighting comes at least a day after the first of
its run of sightings, or when a person retires it behind the explicit gate
``sync.removed.retire`` after a sighting this run. A retired playlist holds
nothing and stops nothing. ANY OTHER ANSWER ENDS THE RUN OF SIGHTINGS: a
playlist the account lists again, or whose id opens again, is dropped from the
record, its retirement with it, and is read as any other. A failure that is
not a not found leaves the entry as it stands.

ONE LOCKED DOCUMENT, ``sync_unavailable.json``, library scoped and never
restored, declared on its state entry. It records what the account answered,
which a database restore does not undo. It writes nothing on the account and
nothing in the database. An entry is a playlist, its last known name, the
first and the latest sighting, and when and by whom it was retired.

AN UNREAD RECORD REFUSES, never reading as empty, since empty would read a
retired playlist as unretired, which only keeps rows, and would also forget a
first sighting, which only delays a retirement: both safe, but a record that
cannot be read cannot be written either, and a run would then report a
retirement it never kept.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, answered_not_found, failure_links, refuse

RECORD_VERSION = 1

_ORIGIN = ("sync.unavailable",)

#: How long after its first sighting a not found retires a playlist.
APART = timedelta(hours=24)

#: The provider client's own not found class, ``tidalapi.exceptions.ObjectNotFound``,
#: by its exact name, so this module imports no client.
CLIENT_NOT_FOUND = "ObjectNotFound"

#: Who retired a playlist: a second sighting a day after the first, or a person at the gate.
BY_SIGHTINGS = "sightings"
BY_PERSON = "person"
BY = frozenset({BY_SIGHTINGS, BY_PERSON})


def now() -> datetime:
    """The moment a sighting is stamped with. A function so a suite can pin it."""
    return datetime.now(timezone.utc)


def stamp(moment: datetime) -> str:
    """An ISO 8601 instant in UTC, the one spelling the record holds."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat()


def day(text: str) -> str:
    """The date of a recorded instant, as a person reads it."""
    return text[:10]


def answered_unavailable(exc: BaseException) -> bool:
    """Whether the provider answered not found for this failure, and nothing else did.

    BY CLASS NAME ON THE DECLARED CHAIN, OR BY THE NEAREST STATUS, NEVER BY
    THE TEXT, the rule ``label.tidal_catalogue._gone`` keeps for a release:
    the message carries the playlist's id, and an id can hold the digits 404.
    The NEAREST link that says anything decides, walked as
    ``core.cause.nearest_status`` walks (R-1313): a link carrying a status
    answers by it, so a server error met while handling a not found is the
    server error, and a link of the client's not found class answers yes, read
    only off links the failure declares as its causes, since a not found met
    while handling something else is not this answer. THE CLIENT'S CLASS BY
    ITS EXACT NAME, never a name that merely holds "not found" (round one):
    Python's own ``FileNotFoundError`` is raised by the provider gate's lock
    before any request is sent, and read as the provider's answer it recorded
    a sighting of a playlist nobody asked about.
    """
    for link, declared in failure_links(exc):
        if getattr(getattr(link, "response", None), "status_code", None) is not None:
            return answered_not_found(link)
        if declared and type(link).__name__ == CLIENT_NOT_FOUND:
            return True
    return False


@dataclass(frozen=True, slots=True)
class Sighting:
    """One synced playlist the account answered not found for, and whether it is retired."""

    playlist_id: str
    name: str
    #: The first sighting of the current run of them, an ISO 8601 instant.
    first: str
    #: The latest sighting, an ISO 8601 instant, not moved once retired.
    last: str
    #: When it was retired, or ``""`` while it is not.
    retired: str = ""
    #: Who retired it, one of :data:`BY`, or ``""`` while it is not.
    by: str = ""

    @property
    def is_retired(self) -> bool:
        return bool(self.retired)

    def seen(self) -> str:
        """The dates it was seen unavailable, as a person reads them."""
        first, last = day(self.first), day(self.last)
        return first if first == last else f"{first} and {last}"

    def to_json(self) -> dict[str, str]:
        return {
            "playlist_id": self.playlist_id,
            "name": self.name,
            "first": self.first,
            "last": self.last,
            "retired": self.retired,
            "by": self.by,
        }


def sighted(prior: Sighting | None, playlist_id: str, name: str, moment: datetime) -> Sighting:
    """The entry after one more not found at ``moment``. Pure.

    The first sighting starts a run; one at least :data:`APART` after the
    first retires it, stamped by the sightings. A retired entry is kept as it
    stands, so the dates a person was shown when it retired do not move.
    """
    when = stamp(moment)
    if prior is None:
        return Sighting(playlist_id=playlist_id, name=name, first=when, last=when)
    if prior.is_retired:
        return prior
    latest = max(datetime.fromisoformat(prior.last), datetime.fromisoformat(when))
    held = replace(prior, name=name or prior.name, last=stamp(latest))
    if latest - datetime.fromisoformat(held.first) >= APART:
        return replace(held, retired=held.last, by=BY_SIGHTINGS)
    return held


def retired_by_person(prior: Sighting, moment: datetime) -> Sighting:
    """The entry a person retired at the gate. Pure."""
    if prior.is_retired:
        return prior
    return replace(prior, retired=stamp(moment), by=BY_PERSON)


class UnavailableRecord:
    """The locked document of the synced playlists the account answered not found for."""

    def __init__(self, cfg: config.Config) -> None:
        self.cfg = cfg
        self.path: Path = config.state_path("sync_unavailable_record", cfg)
        self.lock_path: Path = config.state_path("sync_unavailable_record_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-unavailable-record-unusable",
            f"the record of the synced playlists the account no longer has, "
            f"{self.path.name}, could not be read ({what}), so which of them are "
            f"retired is unknown",
            steps=("repair or restore the record before running sync removed",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"problem": what, "path": str(self.path)},
        )

    def read(self) -> dict[str, Sighting]:
        """Every entry by playlist id, or the refusal; an absent record holds none."""
        try:
            raw = json.loads(self.path.read_bytes())
        except FileNotFoundError:
            return {}
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            # Not UTF-8 is a ``ValueError`` too, and as unreadable.
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> dict[str, Sighting]:
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a record")
        version = raw.get("version")
        if isinstance(version, bool) or version != RECORD_VERSION:
            raise self._unusable(
                f"it says version {version!r} and this build reads {RECORD_VERSION}"
            )
        if raw.get("library_id") != self.cfg.library.volume_id:
            raise self._unusable(
                f"it was written for library {raw.get('library_id')!r} and this library "
                f"is {self.cfg.library.volume_id}"
            )
        entries = raw.get("playlists")
        if not isinstance(entries, list):
            raise self._unusable("it has no list of playlists")
        found: dict[str, Sighting] = {}
        keys = ("playlist_id", "name", "first", "last", "retired", "by")
        for number, entry in enumerate(entries, start=1):
            if not isinstance(entry, Mapping):
                raise self._unusable(f"entry {number} is not an object")
            fields = {key: entry.get(key) for key in keys}
            if not all(isinstance(value, str) for value in fields.values()):
                raise self._unusable(f"entry {number} has a field that is not text")
            if not all(fields[key] for key in ("playlist_id", "first", "last")):
                raise self._unusable(f"entry {number} names no playlist or sighting")
            try:
                for key in ("first", "last", *(("retired",) if fields["retired"] else ())):
                    if datetime.fromisoformat(fields[key]).tzinfo is None:
                        raise ValueError(key)
            except ValueError as exc:
                raise self._unusable(f"entry {number} has a time that is not an instant") from exc
            if bool(fields["retired"]) != bool(fields["by"]) or (
                fields["by"] and fields["by"] not in BY
            ):
                raise self._unusable(f"entry {number} is retired by {fields['by']!r}")
            if fields["playlist_id"] in found:
                raise self._unusable(f"entry {number} names {fields['playlist_id']} a second time")
            found[fields["playlist_id"]] = Sighting(**fields)
        return found

    def update(self, changes: Mapping[str, Sighting | None]) -> dict[str, Sighting]:
        """Apply ``changes`` under the lock, ``None`` dropping an entry; writes only on a change."""
        try:
            with config.exclusive_lock(self.lock_path):
                return self._apply(changes)
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "sync-unavailable-record-unusable",
                f"the record of the synced playlists the account no longer has could "
                f"not be locked ({exc}), and writing it unlocked discards what a "
                f"second run records at the same time",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=_ORIGIN,
                detail={"lock": str(self.lock_path)},
            ) from exc

    def _apply(self, changes: Mapping[str, Sighting | None]) -> dict[str, Sighting]:
        entries = self.read()
        after = {key: value for key, value in entries.items() if key not in changes}
        after.update({key: value for key, value in changes.items() if value is not None})
        if after != entries:
            document = {
                "version": RECORD_VERSION,
                "library_id": self.cfg.library.volume_id,
                "playlists": [after[key].to_json() for key in sorted(after)],
            }
            text = json.dumps(document, indent=2, sort_keys=True) + "\n"
            config.atomic_write_bytes(text.encode("utf-8"), self.path)
        return after


__all__ = [
    "APART",
    "CLIENT_NOT_FOUND",
    "BY",
    "BY_PERSON",
    "BY_SIGHTINGS",
    "RECORD_VERSION",
    "Sighting",
    "UnavailableRecord",
    "answered_unavailable",
    "day",
    "now",
    "retired_by_person",
    "sighted",
    "stamp",
]
