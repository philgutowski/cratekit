"""Each synced playlist ``crate sync removed`` read whole, kept for the pass (R-1716).

"Still on another synced playlist" is a claim about every one, so a run that
finds a removal reads each, about two calls a playlist, past one command's
ceiling and the hour's read line on an account with hundreds of them. A run
stopped there read everything again on the next, so the step could never
finish within an hour. This store keeps each playlist read whole, so the next
run reads only what is left.

A KEPT READ IS USED ONLY WHILE THE ACCOUNT SAYS IT STANDS: the account's
listing, which every run reads first, shows the playlist now with the track
count and the last updated stamp it showed just before the read, the stamp
reported, and the read is under :data:`KEPT_FOR`. A playlist written since, by
a person or by Cratekit, moves its stamp and is read again; one the listing
omits, or lists with no stamp or no count, is never taken from the store.

ONLY A READ WHOLE IS KEPT. Gone, unreadable, short and empty playlists, a
retired one and the hearts are asked on every run, so the not found record
(U320) and every fail closed rule of :mod:`cratekit.sync.removed` stand as
they were: a playlist not read whole on this run still offers nothing.

Written as it goes, every :data:`FLUSH_EVERY` new reads and on the way out,
the call ceiling's park and the hour's included, so a stopped run keeps what
it read. A refused write is said, never raised, and costs only calls. A
document that cannot be read, or is of another version, reads as nothing
kept and is said, since nothing kept only means every playlist is read
again. One library scoped document, ``sync_removed_reads.json``, never
restored, since a database restore does not undo what the account listed.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from cratekit.core import config
from cratekit.sync import removed, unavailable

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: The declared state entry the document lives at.
STATE_KEY = "sync_removed_reads"

#: How long a read stays usable: the hour a stopped run's calls hold the hour's
#: line, the next hour to finish, and an hour to answer the gate.
KEPT_FOR = timedelta(hours=3)

#: New reads between two writes of the document, what a kill loses at most.
FLUSH_EVERY = 50

#: The document's version. Any other reads as nothing kept.
VERSION = 1

#: Raised whenever what a read keeps, or how it is folded, changes, so a read
#: made by an older build is read again rather than trusted.
READER = 1

#: The warnings the verb carries: what was taken from the store, and why the
#: store could not be read or written.
FROM_KEPT = "sync-removed-reads-kept"
UNREAD = "sync-removed-reads-unread"
UNKEPT = "sync-removed-reads-unkept"


@dataclass(frozen=True, slots=True)
class Mark:
    """What the account's listing said of one playlist: its count and its last updated stamp."""

    tracks: int
    updated: str

    def stored(self) -> dict[str, Any]:
        return {"tracks": self.tracks, "updated": self.updated}


def mark_of(shown: catalogue.AccountPlaylist | None) -> Mark | None:
    """The listing's mark for a playlist, or ``None`` when it says too little to trust a kept read.

    UNLISTED, UNCOUNTED OR UNSTAMPED IS NO MARK, so such a playlist is read
    every run, as it was before this store.
    """
    if shown is None:
        return None
    tracks, updated = shown.tracks, shown.updated
    if not isinstance(tracks, int) or isinstance(tracks, bool) or tracks < 0:
        return None
    if not isinstance(updated, str) or not updated.strip():
        return None
    return Mark(tracks=tracks, updated=updated)


def _instant(raw: Any) -> datetime | None:
    if not isinstance(raw, str):
        return None
    try:
        moment = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


def _strings(raw: Any) -> frozenset[str] | None:
    if not isinstance(raw, list) or not all(isinstance(one, str) for one in raw):
        return None
    return frozenset(raw)


class KeptReads:
    """The store, read once when a run starts and written as it reads.

    ``moment`` is the run's own clock, :func:`unavailable.now` read once, so
    the not found record and this store age by one instant.
    """

    def __init__(self, cfg: config.Config, moment: datetime | None = None) -> None:
        self.path = config.state_path(STATE_KEY, cfg)
        self.moment = moment or unavailable.now()
        #: Every entry read or made, by account id, as the document stores it.
        self.entries: dict[str, dict[str, Any]] = {}
        #: Why the document could not be read, ``""`` when it could.
        self.unread = ""
        #: Why the last write failed, ``""`` while nothing is owed.
        self.unkept = ""
        #: The playlists this run took from the store, and those it read and kept.
        self.used: dict[str, None] = {}
        self.kept: dict[str, None] = {}
        self._unwritten = 0
        self._load()

    def _load(self) -> None:
        try:
            raw = json.loads(self.path.read_text())
        except FileNotFoundError:
            return
        except (OSError, ValueError) as exc:
            self.unread = f"it could not be read ({type(exc).__name__}: {exc})"
            return
        if not isinstance(raw, Mapping):
            self.unread = f"it is a {type(raw).__name__}, not a map"
            return
        if raw.get("version") != VERSION:
            self.unread = f"it says version {raw.get('version')!r} and this build reads {VERSION}"
            return
        reads = raw.get("reads")
        if not isinstance(reads, Mapping):
            self.unread = "it holds no map of reads"
            return
        # AN ENTRY THAT DOES NOT HOLD TOGETHER IS DROPPED, never trusted, and
        # costs its playlist one read.
        self.entries = {
            str(account): dict(entry)
            for account, entry in reads.items()
            if isinstance(entry, Mapping)
        }

    def _fresh(self, read_at: datetime) -> bool:
        age = self.moment - read_at
        return timedelta(0) <= age < KEPT_FOR

    def get(
        self, account: str, shown: catalogue.AccountPlaylist | None
    ) -> removed.Listing | None:
        """The kept read of ``account`` when the listing says it stands, else ``None``."""
        mark = mark_of(shown)
        entry = self.entries.get(account)
        if mark is None or shown is None or entry is None:
            return None
        read_at = _instant(entry.get("read_at"))
        if (
            read_at is None
            or not self._fresh(read_at)
            or entry.get("reader") != READER
            or entry.get("mark") != mark.stored()
        ):
            return None
        held = [_strings(entry.get(key)) for key in ("refs", "isrcs", "recordings")]
        refs, isrcs, recordings = held
        if refs is None or isrcs is None or recordings is None:
            return None
        self.used[account] = None
        return removed.Listing(
            account=account,
            name=shown.name,
            state=removed.READ,
            refs=refs,
            isrcs=isrcs,
            recordings=recordings,
        )

    def keep(
        self, account: str, shown: catalogue.AccountPlaylist | None, listing: removed.Listing
    ) -> None:
        """Keep a read made now, when it was read whole and the listing marked it; drop any older one."""
        mark = mark_of(shown)
        if listing.state != removed.READ or mark is None:
            # A READ NOT WHOLE NOW, OR UNMARKED, LEAVES NOTHING TO REUSE.
            if self.entries.pop(account, None) is not None:
                self._counted()
            return
        self.entries[account] = {
            "read_at": self.moment.isoformat(),
            "reader": READER,
            "mark": mark.stored(),
            "refs": sorted(listing.refs),
            "isrcs": sorted(listing.isrcs),
            "recordings": sorted(listing.recordings),
        }
        self.kept[account] = None
        self._counted()

    def _counted(self) -> None:
        self._unwritten += 1
        if self._unwritten >= FLUSH_EVERY:
            self.flush()

    def flush(self) -> None:
        """Write every entry still under :data:`KEPT_FOR`, if any change is unwritten.

        A REFUSED WRITE IS SAID, never raised: it costs the next run calls, and
        nothing it would have answered.
        """
        if not self._unwritten:
            return
        reads = {
            account: entry
            for account, entry in sorted(self.entries.items())
            if (read_at := _instant(entry.get("read_at"))) is not None and self._fresh(read_at)
        }
        document = {"version": VERSION, "reads": reads}
        try:
            payload = json.dumps(document, sort_keys=True, allow_nan=False).encode() + b"\n"
            config.atomic_write_bytes(payload, self.path)
        except (OSError, ValueError, TypeError) as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
        self.unkept = ""
        self._unwritten = 0

    def until(self) -> str:
        """When the reads this run made stop being used, in the not found record's spelling."""
        return unavailable.stamp(self.moment + KEPT_FOR)

    def warnings(self, synced: Iterable[str] = ()) -> list[dict[str, str]]:
        """What the envelope says of the store: reads taken from it, and a read or write refused."""
        found: list[dict[str, str]] = []
        asked = list(dict.fromkeys(synced))
        if self.used:
            found.append(
                {
                    "code": FROM_KEPT,
                    "message": (
                        f"{len(self.used)} of the {len(asked) or len(self.used)} synced "
                        f"playlist(s) were taken from a read whole by a run in the last "
                        f"{_hours(KEPT_FOR)}, since the account lists each with the count "
                        f"and the last updated stamp it listed then; a playlist written "
                        f"since is read again"
                    ),
                }
            )
        if self.unread:
            found.append(
                {
                    "code": UNREAD,
                    "message": (
                        f"the reads kept at {self.path.name} could not be used ({self.unread}), "
                        f"so every synced playlist was read again; deleting it is safe"
                    ),
                }
            )
        if self.unkept:
            found.append(
                {
                    "code": UNKEPT,
                    "message": (
                        f"the reads this run made could not be kept at {self.path.name} "
                        f"({self.unkept}), so the next run reads them again"
                    ),
                }
            )
        return found


def _hours(span: timedelta) -> str:
    hours = int(span.total_seconds() // 3600)
    return f"{hours} hour(s)"


__all__ = [
    "FLUSH_EVERY", "FROM_KEPT", "KEPT_FOR", "KeptReads", "Mark", "READER", "STATE_KEY", "UNKEPT",
    "UNREAD", "VERSION", "mark_of",
]
