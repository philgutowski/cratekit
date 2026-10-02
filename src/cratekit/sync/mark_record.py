"""What ``sync mark`` renamed, by pass, so ``sync unmark`` can put it back (R-838).

The swept prefix is a retitle on somebody else's server, and the title alone
cannot say who put it there: the source system writes the same prefix, and a
person can type it. So a mark this product made is recorded as it lands, keyed
by the pass that made it and the playlist's identifier, with the name before
the mark and the name the mark wrote. ``sync unmark`` reads this and nothing
else to decide what a pass marked, which is how a playlist carrying the prefix
that no pass of this product wrote is refused rather than renamed.

AN ENTRY IS NEVER DELETED. An unmark stamps it, so a second unmark finds the
playlist already put back and plans nothing, and a later mark by the same pass
clears the stamp again.

NEVER RESTORED, declared on the state entry. The renames it records do not roll
back with a database restore, so a record rolled back with it would forget a
mark that is still on the account, and the one verb that can take it off would
then refuse it.
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

RECORD_VERSION = 1

_ORIGIN = ("sync.mark_record",)


@dataclass(frozen=True, slots=True)
class Marked:
    """One playlist one pass renamed, and whether it has been put back."""

    pass_name: str
    playlist_id: str
    #: The title before the mark, which is what an unmark renames back to.
    name: str
    #: The title the mark wrote, which is what an unmark expects to find.
    to: str
    marked: str
    #: When an unmark put the title back, or ``""`` while the mark stands.
    unmarked: str = ""

    def to_json(self) -> dict[str, str]:
        return {
            "pass": self.pass_name,
            "playlist_id": self.playlist_id,
            "name": self.name,
            "to": self.to,
            "marked": self.marked,
            "unmarked": self.unmarked,
        }


class MarkRecord:
    """The locked document of every mark ``sync mark`` made on one library."""

    def __init__(self, cfg: config.Config) -> None:
        self.cfg = cfg
        self.path: Path = config.state_path("sync_mark_record", cfg)
        self.lock_path: Path = config.state_path("sync_mark_record_lock", cfg)

    def _unusable(self, what: str) -> CratekitError:
        return refuse(
            "sync-mark-record-unusable",
            f"the record of what sync mark renamed, {self.path.name}, could not be "
            f"read ({what}), so which playlists a pass marked is unknown; reading it "
            f"as empty would refuse every mark it holds",
            steps=("repair or restore the mark record before marking or unmarking",),
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

    def _load(self) -> list[Marked]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise self._unusable("it could not be opened") from exc
        except ValueError as exc:
            raise self._unusable("it is not JSON") from exc
        return self._recognize(raw)

    def _recognize(self, raw: Any) -> list[Marked]:
        if not isinstance(raw, Mapping):
            raise self._unusable(f"the document is a {type(raw).__name__}, not a record")
        version = raw.get("version")
        if version != RECORD_VERSION:
            raise self._unusable(
                f"it says version {version!r} and this build writes {RECORD_VERSION}"
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
        return found

    def _write(self, entries: Sequence[Marked]) -> None:
        payload = {
            "version": RECORD_VERSION,
            "library_id": self.cfg.library.volume_id,
            "marks": [entry.to_json() for entry in entries],
        }
        config.atomic_write_bytes(
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            self.path,
        )

    def of_pass(self, pass_name: str) -> tuple[Marked, ...]:
        """Every playlist ``pass_name`` marked, in the order the marks landed."""
        return tuple(entry for entry in self._load() if entry.pass_name == pass_name)

    def passes(self) -> tuple[str, ...]:
        """Every pass the record holds a mark for, each once, oldest first."""
        return tuple(dict.fromkeys(entry.pass_name for entry in self._load()))

    def record_marked(
        self, pass_name: str, renamed: Mapping[str, tuple[str, str]], *, now: str | None = None
    ) -> None:
        """Record each ``playlist_id: (name, to)`` the pass just renamed.

        NOTHING TO RECORD WRITES NOTHING. A playlist this pass marked before and
        an unmark put back is the same entry marked again, its stamp cleared.
        """
        if not renamed:
            return
        when = now or timestamp()
        with self._locked():
            entries = self._load()
            for playlist_id, (name, to) in renamed.items():
                fresh = Marked(pass_name, playlist_id, name=name, to=to, marked=when)
                for index, entry in enumerate(entries):
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
                else:
                    entries.append(fresh)
            self._write(entries)

    def record_unmarked(self, pass_name: str, playlist_id: str, *, now: str | None = None) -> None:
        """Stamp the pass's mark on ``playlist_id`` as put back."""
        when = now or timestamp()
        with self._locked():
            entries = self._load()
            for index, entry in enumerate(entries):
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
                    self._write(entries)
                    return
        raise self._unusable(
            f"it holds no mark by {pass_name} on {playlist_id}, which was just put back"
        )


__all__ = ["RECORD_VERSION", "MarkRecord", "Marked"]
