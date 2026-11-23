"""Each synced playlist ``crate sync removed`` read whole, held for the pass (R-1716).

"Still on another synced playlist" is a claim about every one, so a run that
finds a removal reads each, two calls or more a playlist, past one command's
ceiling and the hour's read line on an account with hundreds of them. A run
stopped there read everything again on the next, so the step could never
finish within an hour. This store holds each playlist read whole, so the next
run reads only what is left.

A HELD READ IS USED ONLY WHILE THE ACCOUNT SAYS IT STANDS: the account's
listing, which every run reads first, shows the playlist now with the track
count and the last updated stamp it showed just before the read, and the read
is under :data:`HELD_FOR`. A playlist written since, by a person or by
Cratekit, moves its stamp and is read again; one the listing omits, or lists
with no count or no stamp that reads as an instant, is never taken from the
store.

AND ONLY A READ THE LISTING AGREES WITH IS HELD (round one's finding 2). The
provider serves a playlist's old rows for minutes after a write (sitting 86
measured 13 for a move), while its listing may already show the new stamp, so
a read is held only when it holds as many tracks as the listing counts and the
stamp is at least :data:`SETTLED` older than the read. A playlist written
lately is read on every run until it settles.

ONLY A READ WHOLE IS HELD. Gone, unreadable, short and empty playlists, a
retired one and the hearts are asked on every run, so the not found record
(U320) and every fail closed rule of :mod:`cratekit.sync.removed` stand as
they were: a playlist not read whole on this run still offers nothing.

Written as it goes, every :data:`FLUSH_EVERY` changes and on the way out, the
call ceiling's park and the hour's included, so a stopped run keeps what it
read; each write merges what another run wrote meanwhile, the later read of a
playlist winning. A refused write is said, never raised, and costs only calls.
A document that cannot be read, or is of another version, reads as nothing
held and is said, since nothing held only means every playlist is read again.
One library scoped document, ``sync_removed_reads.json``, never restored,
since a database restore does not undo what the account listed.

Layer: modules.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.core import config
from cratekit.sync import removed, unavailable

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: The declared state entry the document lives at.
STATE_KEY = "sync_removed_reads"

#: How long a read stays usable, counted from when it was made: three hours of
#: reading at the hour's line on the measured account (717 playlists, about
#: 2,300 calls), then time to rehearse and answer the gate.
HELD_FOR = timedelta(hours=6)

#: How much older than the read the listing's stamp must be for the read to
#: be held: twice the 13 minutes sitting 86 measured a paged read lagging.
SETTLED = timedelta(minutes=30)

#: Changes between two writes of the document, what a kill loses at most.
FLUSH_EVERY = 50

#: The document's version. Any other reads as nothing held.
VERSION = 1

#: Raised whenever what a read holds, or how it is folded, changes, so a read
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

    def settled(self, moment: datetime) -> bool:
        """Whether the stamp is :data:`SETTLED` older than ``moment``, so a read now is current."""
        stamped = _instant(self.updated)
        return stamped is not None and moment - stamped >= SETTLED


def mark_of(shown: catalogue.AccountPlaylist | None) -> Mark | None:
    """The listing's mark for a playlist, or ``None`` when it says too little to trust a held read.

    UNLISTED, UNCOUNTED OR UNSTAMPED IS NO MARK, so such a playlist is read
    every run, as it was before this store.
    """
    if shown is None:
        return None
    tracks, updated = shown.tracks, shown.updated
    if not isinstance(tracks, int) or isinstance(tracks, bool) or tracks < 0:
        return None
    if _instant(updated) is None:
        return None
    return Mark(tracks=tracks, updated=str(updated))


def _instant(held: Any) -> datetime | None:
    """``held`` as an instant with a zone, or ``None`` when it is not one."""
    try:
        moment = datetime.fromisoformat(held) if isinstance(held, str) else None
    except ValueError:
        moment = None
    return None if moment is None or moment.tzinfo is None else moment


def _strings(raw: Any) -> frozenset[str] | None:
    if not isinstance(raw, list) or not all(isinstance(one, str) for one in raw):
        return None
    return frozenset(raw)


def _document(path: Path) -> tuple[dict[str, dict[str, Any]], str]:
    """The document's entries by account id, and why it could not be used, ``""`` when it could.

    AN ENTRY THAT DOES NOT HOLD TOGETHER IS DROPPED, never trusted, and costs
    its playlist one read.
    """
    try:
        raw = json.loads(path.read_text())
    except FileNotFoundError:
        return {}, ""
    except (OSError, ValueError) as exc:
        return {}, f"it could not be read ({type(exc).__name__}: {exc})"
    if not isinstance(raw, Mapping):
        return {}, f"it is a {type(raw).__name__}, not a map"
    if raw.get("version") != VERSION:
        return {}, f"it says version {raw.get('version')!r} and this build reads {VERSION}"
    reads = raw.get("reads")
    if not isinstance(reads, Mapping):
        return {}, "it holds no map of reads"
    return {
        str(account): dict(entry) for account, entry in reads.items() if isinstance(entry, Mapping)
    }, ""


class SyncedReads:
    """The store, read once when a run starts and written as it reads.

    ``moment`` is the run's own clock, :func:`unavailable.now` read once, so
    the not found record and this store age by one instant; each read is
    stamped with :func:`unavailable.now` when it is made.
    """

    def __init__(self, cfg: config.Config, moment: datetime | None = None) -> None:
        self.path = config.state_path(STATE_KEY, cfg)
        self.moment = moment or unavailable.now()
        #: Every entry read or made, by account id, as the document stores it.
        self.entries, self.unread = _document(self.path)
        #: Why the last write failed, ``""`` while nothing is owed.
        self.unkept = ""
        #: The playlists this run took from the store, and read and held.
        self.used: dict[str, None] = {}
        self.kept: dict[str, None] = {}
        #: The playlists this run dropped, each with when it read it not whole.
        self.dropped: dict[str, datetime] = {}
        self._unwritten = 0

    def _fresh(self, read_at: datetime | None) -> bool:
        if read_at is None:
            return False
        age = self.moment - read_at
        return timedelta(0) <= age < HELD_FOR

    def get(
        self, account: str, shown: catalogue.AccountPlaylist | None
    ) -> removed.Listing | None:
        """The held read of ``account`` when the listing says it stands, else ``None``."""
        mark = mark_of(shown)
        entry = self.entries.get(account)
        if mark is None or shown is None or entry is None:
            return None
        if (
            not self._fresh(_instant(entry.get("read_at")))
            or entry.get("reader") != READER
            or entry.get("mark") != mark.stored()
        ):
            return None
        refs, isrcs, recordings = (
            _strings(entry.get(key)) for key in ("refs", "isrcs", "recordings")
        )
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
        """Hold a read made now, read whole and agreeing with a settled mark; else drop an older one."""
        mark = mark_of(shown)
        moment = unavailable.now()
        if (
            listing.state != removed.READ
            or mark is None
            or len(listing.refs) != mark.tracks
            or not mark.settled(moment)
        ):
            # A READ NOT WHOLE, UNMARKED, OR NOT YET AGREEING WITH THE LISTING
            # LEAVES NOTHING TO REUSE.
            if self.entries.pop(account, None) is not None:
                self.dropped[account] = moment
                self._counted()
            return
        self.entries[account] = {
            "read_at": moment.isoformat(),
            "reader": READER,
            "mark": mark.stored(),
            "refs": sorted(listing.refs),
            "isrcs": sorted(listing.isrcs),
            "recordings": sorted(listing.recordings),
        }
        self.dropped.pop(account, None)
        self.kept[account] = None
        self._counted()

    def _counted(self) -> None:
        self._unwritten += 1
        if self._unwritten >= FLUSH_EVERY:
            self.flush()

    def standing(self) -> int:
        """How many held reads a run starting now could use, whatever run made them.

        MEASURED AT NOW, not at this run's start, so the reads this run made
        count (round two's finding 1).
        """
        now = unavailable.now()
        return sum(
            1
            for entry in self.entries.values()
            if (read_at := _instant(entry.get("read_at"))) is not None
            and timedelta(0) <= now - read_at < HELD_FOR
        )

    def flush(self) -> None:
        """Write every entry still under :data:`HELD_FOR`, merged with what another run wrote.

        THE LATER READ OF A PLAYLIST WINS, and one this run dropped stays
        dropped unless another run read it after the drop. A REFUSED WRITE IS SAID,
        never raised: it costs the next run calls, and nothing it would have
        answered.
        """
        if not self._unwritten:
            return
        theirs, _why = _document(self.path)
        merged: dict[str, dict[str, Any]] = {}
        for account in sorted({*theirs, *self.entries}):
            other = theirs.get(account)
            dropped_at = self.dropped.get(account)
            if dropped_at is not None and other is not None:
                # DROPPED BY THIS RUN: another run's read stands only if made after the drop.
                other_at = _instant(other.get("read_at"))
                other = other if other_at is not None and other_at > dropped_at else None
            held = [
                (read_at, entry)
                for entry in (self.entries.get(account), other)
                if entry is not None
                and (read_at := _instant(entry.get("read_at"))) is not None
                and self.moment - read_at < HELD_FOR
            ]
            if held:
                merged[account] = max(held, key=lambda one: one[0])[1]
        document = {"version": VERSION, "reads": merged}
        try:
            payload = json.dumps(document, sort_keys=True, allow_nan=False).encode() + b"\n"
            config.atomic_write_bytes(payload, self.path)
        except (OSError, ValueError, TypeError) as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
        self.entries = merged
        self.unkept = ""
        self._unwritten = 0

    def warnings(self, synced: Iterable[str] = ()) -> list[dict[str, str]]:
        """What the envelope says of the store: reads taken from it, and a read or write refused."""
        found: list[dict[str, str]] = []
        if self.used:
            found.append({"code": FROM_KEPT, "message": self.from_held(synced)})
        if self.unread:
            found.append(
                {
                    "code": UNREAD,
                    "message": (
                        f"the reads held at {self.path.name} could not be used ({self.unread}), "
                        f"so every synced playlist was read again; deleting it is safe"
                    ),
                }
            )
        if self.unkept:
            found.append(
                {
                    "code": UNKEPT,
                    "message": (
                        f"the reads this run made could not be held at {self.path.name} "
                        f"({self.unkept}), so the next run reads them again"
                    ),
                }
            )
        return found

    def from_held(self, synced: Iterable[str] = ()) -> str:
        """The sentence that says how many synced playlists were taken from held reads."""
        asked = len(dict.fromkeys(synced)) or len(self.used)
        return (
            f"{len(self.used)} of the {asked} synced playlist(s) were taken from a read "
            f"made whole by a run in the last {hours(HELD_FOR)}, since the account lists "
            f"each with the count and the last updated stamp it listed then; a playlist "
            f"written since is read again"
        )


def hours(span: timedelta) -> str:
    return f"{int(span.total_seconds() // 3600)} hours"


__all__ = [
    "FLUSH_EVERY", "FROM_KEPT", "HELD_FOR", "Mark", "READER", "SETTLED", "STATE_KEY",
    "SyncedReads", "UNKEPT", "UNREAD", "VERSION", "hours", "mark_of",
]
