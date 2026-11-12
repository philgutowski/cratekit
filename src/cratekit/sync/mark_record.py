"""Which account playlists Cratekit holds as taken, and what any pass retitled (R-838, U242).

TWO LISTS IN ONE LOCKED DOCUMENT, ``sync_marks.json``.

THE TAKEN LEDGER (U242). The ``DOWNLOADED `` prefix is retired, decided by
Phillip on 2026-11-11: a playlist Cratekit has finished with, or found
already finished, is recorded here by its identifier, and no verb writes the
prefix on the account again. One entry per playlist: the title it had when it
was taken, less any prefix, who took it (a pass, ``label mark``, ``export
archive``, or the migration), how, and when, and a released stamp once ``sync
unmark`` lets it go. :func:`cratekit.sync.playlists.is_taken` is the one
question every reader asks of it, and it still answers yes for a legacy
prefixed title until ``crate sync strip`` takes the prefix off, so no state
exists in which a playlist taken today reads as new.

THE MARKS. What ``sync mark`` retitled with the prefix before U242, by pass,
and what ``crate sync strip`` retitled to take it off, under its own pass
name. Each with the title before and the title written, so ``sync unmark``
puts a title back by the one rule it always had: only while the account still
carries the title the record says was written. The title alone cannot say who
wrote a prefix, since the source system wrote the same one and a person can
type it.

AN ENTRY IS NEVER DELETED. An unmark that puts a title back stamps its mark;
a release stamps the taken entry it lets go, and the pass's legacy mark with
it when one stands, since that mark is then undone with no title to put back.
A second run finds them done and plans nothing.

VERSION 1 READS AS A RECORD WITH NOTHING TAKEN, so a record written before
U242 is never refused for its age; the first write rewrites it as version 2.

NEVER RESTORED, declared on the state entry. A rename it records does not roll
back with a database restore, and a playlist taken stays taken, so a record
rolled back with the database would offer a finished playlist as new.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse

RECORD_VERSION = 2

#: The retired prefix, spelled as ``sync.playlists`` spells it. Repeated here
#: rather than imported, since ``sync.playlists`` reads this record.
SWEPT_PREFIX = "DOWNLOADED "

#: Every version this build reads. Version 1 is the record before U242,
#: marks and no taken list.
READS = frozenset({1, RECORD_VERSION})

_ORIGIN = ("sync.mark_record",)

#: How a playlist came to be taken (U242).
#: A sync pass finished it, by ``sync mark`` or ``organize --only marks``, or
#: a mark of the prefix this record held from before U242. Its stamp is when.
BY_PASS = "pass"
#: ``label mark`` took a landed batch's year playlist.
BY_LABEL = "label"
#: ``export archive``, or a set landing's archive, filed a downloaded set.
BY_SET = "set"
#: The migration found the legacy prefix on it, with no mark saying when, so
#: its stamp is when it was found and says nothing of when it was downloaded.
FOUND_PREFIXED = "found-prefixed"
HOW = frozenset({BY_PASS, BY_LABEL, BY_SET, FOUND_PREFIXED})

#: Who the migration records a found prefix as taken by.
MIGRATION = "migration"


@dataclass(frozen=True, slots=True)
class Marked:
    """One playlist one pass retitled, and whether it has been put back."""

    pass_name: str
    playlist_id: str
    #: The title before the mark, which is what an unmark renames back to.
    name: str
    #: The title the mark wrote, which is what an unmark expects to find.
    to: str
    marked: str
    #: When an unmark put the title back, or let the playlist go with no title
    #: of the mark's left to put back (U242), or ``""`` while the mark stands.
    unmarked: str = ""

    @property
    def of_the_prefix(self) -> bool:
        """Whether this mark wrote the retired prefix, and is not one ``sync strip`` wrote.

        THE MARKS LIST HOLDS TWO KINDS SINCE U242 (round one of its review): a
        prefix a pass wrote before it, and a title the strip wrote taking a
        prefix off, recorded so ``sync unmark`` can put it back. Only the first
        says a pass finished the playlist, so every reader asking that asks
        this.
        """
        return self.to.startswith(SWEPT_PREFIX)

    def to_json(self) -> dict[str, str]:
        return {
            "pass": self.pass_name,
            "playlist_id": self.playlist_id,
            "name": self.name,
            "to": self.to,
            "marked": self.marked,
            "unmarked": self.unmarked,
        }


@dataclass(frozen=True, slots=True)
class Taken:
    """One account playlist Cratekit holds as taken (U242)."""

    playlist_id: str
    #: Its title when it was taken, less any legacy prefix.
    name: str
    #: The pass that took it, or the verb, or :data:`MIGRATION`.
    by: str
    #: One of :data:`HOW`.
    how: str
    at: str
    #: When ``sync unmark`` let it go, or ``""`` while it is held.
    released: str = ""

    @property
    def held(self) -> bool:
        return not self.released

    @property
    def dated(self) -> bool:
        """Whether its stamp is when a pass finished it, which filing reads a year from."""
        return self.how == BY_PASS

    def to_json(self) -> dict[str, str]:
        return {
            "playlist_id": self.playlist_id,
            "name": self.name,
            "by": self.by,
            "how": self.how,
            "at": self.at,
            "released": self.released,
        }


class MarkRecord:
    """The locked document of what Cratekit took and retitled on one library."""

    def __init__(self, cfg: config.Config) -> None:
        self.cfg = cfg
        self.path: Path = config.state_path("sync_mark_record", cfg)
        self.lock_path: Path = config.state_path("sync_mark_record_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-mark-record-unusable",
            f"the record of what Cratekit took and renamed, {self.path.name}, could not "
            f"be read ({what}), so which playlists are taken is unknown; reading it as "
            f"empty would offer every one of them as new",
            steps=("repair or restore the mark record before syncing, marking or unmarking",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"problem": what, "path": str(self.path)},
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        lock = config._exclusive_lock(self.lock_path)
        try:
            lock.__enter__()
        except config.ConfigLockUnavailable as exc:
            raise refuse(
                "sync-mark-record-unusable",
                f"the mark record could not be locked ({exc}), and writing it "
                f"unlocked discards whatever a second mark is recording at the same time",
                steps=("make the library's state directory writable by this account",),
                scope=Scope.RUN,
                origin=_ORIGIN,
                detail={"lock": str(self.lock_path)},
            ) from exc
        try:
            yield
        finally:
            lock.__exit__(None, None, None)

    def _read(self) -> tuple[list[Marked], list[Taken]]:
        if not self.path.exists():
            return [], []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _load(self) -> list[Marked]:
        return self._read()[0]

    def _recognize(self, raw: Any) -> tuple[list[Marked], list[Taken]]:
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a record")
        version = raw.get("version")
        if isinstance(version, bool) or not isinstance(version, int) or version not in READS:
            raise self._unusable(
                f"it says version {version!r} and this build reads "
                f"{', '.join(str(one) for one in sorted(READS))}"
            )
        library_id = raw.get("library_id")
        if library_id != self.cfg.library.volume_id:
            raise self._unusable(
                f"it was written for library {library_id!r} and this library is "
                f"{self.cfg.library.volume_id}"
            )
        entries = raw.get("marks")
        if not isinstance(entries, list):
            raise self._unusable("it has no list of marks")
        found: list[Marked] = []
        for number, entry in enumerate(entries, start=1):
            if not isinstance(entry, Mapping):
                raise self._unusable(f"mark {number} is not an object")
            fields = {
                key: entry.get(key)
                for key in ("pass", "playlist_id", "name", "to", "marked", "unmarked")
            }
            if not all(isinstance(value, str) for value in fields.values()):
                raise self._unusable(f"mark {number} has a field that is not text")
            if not all(fields[key] for key in ("pass", "playlist_id", "name", "to")):
                raise self._unusable(f"mark {number} names no pass, playlist or title")
            found.append(
                Marked(
                    pass_name=fields["pass"],
                    playlist_id=fields["playlist_id"],
                    name=fields["name"],
                    to=fields["to"],
                    marked=fields["marked"],
                    unmarked=fields["unmarked"],
                )
            )
        return found, self._recognize_taken(raw, version)

    def _recognize_taken(self, raw: Mapping[str, Any], version: Any) -> list[Taken]:
        if version == 1:
            # BEFORE U242 NOTHING WAS TAKEN HERE. A version 1 record that
            # somehow carries the key is still read as it was written.
            return []
        entries = raw.get("taken")
        if not isinstance(entries, list):
            raise self._unusable("it has no list of taken playlists")
        found: list[Taken] = []
        seen: set[str] = set()
        for number, entry in enumerate(entries, start=1):
            if not isinstance(entry, Mapping):
                raise self._unusable(f"taken entry {number} is not an object")
            fields = {
                key: entry.get(key)
                for key in ("playlist_id", "name", "by", "how", "at", "released")
            }
            if not all(isinstance(value, str) for value in fields.values()):
                raise self._unusable(f"taken entry {number} has a field that is not text")
            if not all(fields[key] for key in ("playlist_id", "by", "how", "at")):
                raise self._unusable(f"taken entry {number} names no playlist, taker or time")
            if fields["how"] not in HOW:
                raise self._unusable(
                    f"taken entry {number} was taken {fields['how']!r}, which this build "
                    f"does not know"
                )
            if fields["playlist_id"] in seen:
                raise self._unusable(
                    f"taken entry {number} names {fields['playlist_id']} a second time"
                )
            seen.add(fields["playlist_id"])
            found.append(Taken(**fields))
        return found

    def _write(self, marks: Sequence[Marked], taken: Sequence[Taken]) -> None:
        payload = {
            "version": RECORD_VERSION,
            "library_id": self.cfg.library.volume_id,
            "marks": [entry.to_json() for entry in marks],
            "taken": [entry.to_json() for entry in taken],
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            self.path,
        )

    def ready(self) -> tuple[Marked, ...]:
        """Every mark, read UNDER THE LOCK, or the refusal a write would raise.

        Asked before a gate that leads to a write, so a record that cannot be
        read or locked refuses while nothing has changed yet, rather than
        after a write it then cannot record.
        """
        with self._locked():
            return tuple(self._load())

    def all(self) -> tuple[Marked, ...]:
        return tuple(self._load())

    def of_pass(self, pass_name: str) -> tuple[Marked, ...]:
        """Every playlist ``pass_name`` retitled, in the order the marks landed."""
        return tuple(entry for entry in self._load() if entry.pass_name == pass_name)

    def record_marked(
        self, pass_name: str, renamed: Mapping[str, tuple[str, str]], *, now: str | None = None
    ) -> None:
        """Record each ``playlist_id: (name, to)`` the pass just retitled.

        NOTHING TO RECORD WRITES NOTHING. A playlist this pass marked before and
        an unmark put back is the same entry marked again, its stamp cleared.
        """
        if not renamed:
            return
        when = now or timestamp()
        with self._locked():
            entries, taken = self._read()
            for playlist_id, (name, to) in renamed.items():
                fresh = Marked(pass_name, playlist_id, name=name, to=to, marked=when)
                for index, entry in enumerate(entries):
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
                else:
                    entries.append(fresh)
            self._write(entries, taken)

    def record_unmarked(self, pass_name: str, playlist_id: str, *, now: str | None = None) -> None:
        """Stamp the pass's mark on ``playlist_id`` as put back."""
        when = now or timestamp()
        with self._locked():
            entries, taken = self._read()
            for index, entry in enumerate(entries):
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
                    self._write(entries, taken)
                    return
        raise self._unusable(
            f"it holds no mark by {pass_name} on {playlist_id}, which was just put back"
        )

    # ── the taken ledger (U242) ────────────────────────────────────────────

    def taken(self) -> dict[str, Taken]:
        """Every taken entry, held or released, by playlist identifier."""
        return {entry.playlist_id: entry for entry in self._read()[1]}

    def taken_ids(self) -> frozenset[str]:
        """Every playlist identifier held as taken now."""
        return frozenset(entry.playlist_id for entry in self._read()[1] if entry.held)

    def take(self, entries: Sequence[Taken]) -> tuple[str, ...]:
        """Hold each entry's playlist as taken. Returns the identifiers newly held.

        IDEMPOTENT. A playlist already held keeps the entry that holds it, so
        the first taker, and its stamp, stand, and a second migration records
        nothing. A released one is taken afresh by the new entry. NOTHING NEW
        WRITES NOTHING.
        """
        if not entries:
            return ()
        with self._locked():
            marks, taken = self._read()
            index = {entry.playlist_id: number for number, entry in enumerate(taken)}
            fresh: list[str] = []
            for entry in entries:
                if entry.how not in HOW or not entry.playlist_id or not entry.by:
                    raise ValueError(f"not a taken entry this record can hold: {entry!r}")
                at = index.get(entry.playlist_id)
                if at is None:
                    index[entry.playlist_id] = len(taken)
                    taken.append(replace(entry, released=""))
                elif not taken[at].held:
                    taken[at] = replace(entry, released="")
                else:
                    continue
                fresh.append(entry.playlist_id)
            if fresh:
                self._write(marks, taken)
            return tuple(fresh)

    def release(self, by: str, playlist_id: str, *, now: str | None = None) -> None:
        """Stamp ``by``'s hold on ``playlist_id`` as let go, or refuse."""
        when = now or timestamp()
        with self._locked():
            marks, taken = self._read()
            for number, entry in enumerate(taken):
                if entry.playlist_id == playlist_id and entry.by == by and entry.held:
                    taken[number] = replace(entry, released=when)
                    self._write(marks, taken)
                    return
        raise self._unusable(
            f"it holds no taken entry by {by} on {playlist_id}, which was just let go"
        )


__all__ = [
    "BY_LABEL",
    "BY_PASS",
    "BY_SET",
    "FOUND_PREFIXED",
    "HOW",
    "MIGRATION",
    "READS",
    "RECORD_VERSION",
    "SWEPT_PREFIX",
    "MarkRecord",
    "Marked",
    "Taken",
    "standing_prefix_marks",
]


def standing_prefix_marks(marks: Sequence[Marked]) -> tuple[Marked, ...]:
    """Every prefix mark no unmark put back, the strip's own records left out."""
    return tuple(entry for entry in marks if not entry.unmarked and entry.of_the_prefix)
