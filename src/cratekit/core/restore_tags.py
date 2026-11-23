"""The files' half of a restore: the title tag and key tag a session kept (R-1924).

The analyze adopt verb writes each file's title tag and ``initialkey`` beside
the row's ``Title``, and keeps every old value in its session record before the
first file is written. A restore of that session replaces the database, which
puts the rows back; this part puts the files back from the same record, so the
two surfaces agree again.

**THE RECORD IS THE ONLY SOURCE.** Nothing here reads the database or plans
again: the values are the ones the adopt read off each file before it wrote,
and the record held them on disk before the first write. A record that holds
the key in a form this build cannot read refuses at the plan, before anything
is replaced, rather than restoring the rows and leaving the files unsaid.

**A BLANK VALUE IS PUT BACK ABSENT.** The adopt read an absent tag as blank, so
a blank before value is cleared, never written as an empty tag the file never
had (U23's rule for every revert).

**ONLY WHAT DIFFERS IS WRITTEN, AND EVERY FILE IS READ BACK.** A file already as
it was writes nothing and counts as put back. One file that cannot be written
never stops the rest: it is named, and the verb's answer is then not ``ok``.

The key is spelled here, not imported from ``cratekit.analysis``, which is a
toggle: a restore puts the files back whether or not the analysis module is on.
``tests/test_restore_tags.py`` pins the two spellings equal.

Layer: write, a part of ``core.restore``, which re-exports it (U300).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core import session, tags
from cratekit.core.cause import refuse

#: Where ``analyze adopt`` keeps each file's old title tag and key tag in its
#: session record; ``cratekit.analysis.head_adopt.RECORD_KEY`` is the same name.
RECORD_KEY = "head_adopt_before"

#: The two tags a restore puts back, as ``core.tags`` names them.
FIELDS: tuple[str, ...] = ("title", "initialkey")

#: Each recorded entry's key for a field, in :data:`FIELDS` order.
_RECORDED: Mapping[str, str] = {"title": "tag_title", "initialkey": "initialkey"}


@dataclass(frozen=True, slots=True)
class FileBefore:
    """One file's tags as they stood before the session that wrote them."""

    path: Path
    title: str
    initialkey: str
    session_id: str

    def value(self, name: str) -> str:
        return self.title if name == "title" else self.initialkey


@dataclass(frozen=True, slots=True)
class TagsPutBack:
    """What the restore did with each file: put back and read back, not
    written, or written and reading back otherwise. Paths as text."""

    planned: int = 0
    read_back: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    wrong: tuple[str, ...] = ()

    @property
    def unwritten(self) -> tuple[str, ...]:
        """Every file that does not carry its old tags, failed before wrong."""
        return self.failed + self.wrong

    def to_json(self) -> dict[str, Any]:
        """The put back as an answer's totals carry it."""
        return {
            "planned": self.planned,
            "read_back": len(self.read_back),
            "failed": list(self.failed),
            "wrong": list(self.wrong),
        }


def _unreadable(record: session.SessionRecord, why: str) -> Exception:
    return refuse(
        "restore-record-unusable",
        f"session {record.session_id} keeps its files' old title and key tag under "
        f"{RECORD_KEY!r} in a form this build cannot read ({why}), so a restore "
        f"would put the rows back and could not put the files back; nothing was "
        f"replaced",
        steps=(
            "the record was changed after the session wrote it, since no build "
            "writes another shape: put back the list the session wrote, from a "
            "copy of the state folder, and run the restore again",
        ),
        origin=("core.restore_tags",),
        detail={"session_id": record.session_id, "key": RECORD_KEY, "why": why},
    )


def kept_by(record: session.SessionRecord) -> tuple[FileBefore, ...]:
    """The before values one record keeps, in its order; none when it keeps none.

    Refuses a record that holds :data:`RECORD_KEY` in any other shape than a
    list of entries each naming a path and both tags as text.
    """
    if RECORD_KEY not in record.detail:
        return ()
    entries = record.detail[RECORD_KEY]
    if not isinstance(entries, list):
        raise _unreadable(record, f"a {type(entries).__name__}, not a list")
    kept: list[FileBefore] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise _unreadable(record, f"entry {index} is not a mapping")
        wanted = ("path", *_RECORDED.values())
        missing = [name for name in wanted if not isinstance(entry.get(name), str)]
        if missing:
            raise _unreadable(record, f"entry {index} has no text for {', '.join(missing)}")
        # A PATH THAT IS NOT ABSOLUTE would resolve against wherever the verb ran,
        # and a BLANK TITLE TAG would be cleared: the adopt writes neither, since it
        # adopts only a title tag with a head on a resolved file (review round one).
        if entry["path"].strip() != entry["path"] or not Path(entry["path"]).is_absolute():
            raise _unreadable(record, f"entry {index} names no absolute path")
        if not entry["tag_title"].strip():
            raise _unreadable(record, f"entry {index} keeps a blank title tag")
        kept.append(
            FileBefore(
                path=Path(entry["path"]),
                title=entry["tag_title"],
                initialkey=entry["initialkey"],
                session_id=record.session_id,
            )
        )
    return tuple(kept)


def befores(
    records: Iterable[session.SessionRecord],
    *,
    rebased: Callable[[Path], Path] = lambda path: path,
) -> tuple[FileBefore, ...]:
    """One before value per file over ``records``, oldest record first.

    THE FIRST RECORD TO NAME A FILE WINS: a restore goes back to before the
    earliest session it undoes, so a later session's before value, which is the
    earlier one's after, is never what a file is put back to. Each path is passed
    through ``rebased``, as every recorded path a restore spends is.
    """
    seen: dict[Path, FileBefore] = {}
    for record in records:
        for kept in kept_by(record):
            where = rebased(kept.path)
            if where not in seen:
                seen[where] = FileBefore(where, kept.title, kept.initialkey, kept.session_id)
    return tuple(seen.values())


def _read(path: Path) -> dict[str, str] | None:
    """The file's two tags, blank for absent, or None when they cannot be read."""
    try:
        read = tags.read_tags_checked(path, FIELDS)
    except (tags.TagReadFailed, ValueError, OSError):
        return None
    return {name: str(read[name] or "") for name in FIELDS}


def _write(path: Path, changes: Mapping[str, str]) -> bool:
    """Write the non-blank values and clear the blank ones; False on any failure."""
    written = {name: value for name, value in changes.items() if value}
    cleared = [name for name, value in changes.items() if not value]
    try:
        return bool(
            (not written or tags.write_tags(path, dict(written)))
            and (not cleared or tags.clear_tags(path, cleared))
        )
    except (ValueError, OSError):
        # An unknown container raises rather than answers; it is one file.
        return False


def put_back(planned: Sequence[FileBefore], *, dry_run: bool = False) -> TagsPutBack:
    """Put each file's title tag and key tag back where they differ, then read both back.

    Nothing raises for one file. A file that is gone, or that refuses the write,
    is ``failed``; one that reads back otherwise, or cannot be read back, ``wrong``.
    A DRY RUN WRITES NOTHING: a file gone or unreadable is ``failed``, as the run
    would find it, and no file counts as read back.
    """
    read_back: list[str] = []
    failed: list[str] = []
    wrong: list[str] = []
    for before in planned:
        shown = str(before.path)
        try:
            present = before.path.is_file()
        except (OSError, ValueError):
            present = False
        if not present:
            failed.append(shown)
            continue
        now = _read(before.path)
        if dry_run:
            if now is None:
                failed.append(shown)
            continue
        changes = {
            name: before.value(name)
            for name in FIELDS
            if now is None or now[name] != before.value(name)
        }
        if changes and not _write(before.path, changes):
            failed.append(shown)
            continue
        again = _read(before.path)
        if again is None or any(again[name] != before.value(name) for name in FIELDS):
            wrong.append(shown)
            continue
        read_back.append(shown)
    return TagsPutBack(len(planned), tuple(read_back), tuple(failed), tuple(wrong))


__all__: Sequence[str] = (
    "FIELDS", "RECORD_KEY", "FileBefore", "TagsPutBack", "befores", "kept_by", "put_back",
)
