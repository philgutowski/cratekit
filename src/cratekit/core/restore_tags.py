"""The files' half of a restore: the tags a session kept (R-1924, U339).

The analyze adopt verb writes each file's title tag and ``initialkey`` beside
the row's ``Title``, and ``tag set`` each file's genre beside the row's
``GenreID``; each keeps every old value in its session record before the first
file is written, under its own key. A restore of that session replaces the
database, which puts the rows back; this part puts the files back from the same
record, so the two surfaces agree again. A file is put back only in the tags its
record kept.

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
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.core import session, tags
from cratekit.core.cause import refuse

#: Where ``analyze adopt`` keeps each file's old title tag and key tag in its
#: session record; ``cratekit.analysis.head_adopt.RECORD_KEY`` is the same name.
RECORD_KEY = "head_adopt_before"

#: Where ``tag set`` keeps each file's old genre (U339);
#: ``cratekit.tagging.genre_set.RECORD_KEY`` is the same name.
GENRE_RECORD_KEY = "genre_set_before"

#: Every tag a restore puts back, as ``core.tags`` names them.
FIELDS: tuple[str, ...] = ("title", "initialkey", "genre")

#: Each record key, the tags its entries keep, and each tag's entry key. THE
#: TITLE TAG MAY NOT BE KEPT BLANK, since the adopt only adopts a title tag with
#: a head; a blank genre is put back absent.
_KEPT: Mapping[str, Mapping[str, str]] = {
    RECORD_KEY: {"title": "tag_title", "initialkey": "initialkey"},
    GENRE_RECORD_KEY: {"genre": "genre"},
}

#: The tags whose kept value may not be blank.
_NEVER_BLANK = frozenset({"title"})


@dataclass(frozen=True, slots=True)
class FileBefore:
    """One file's tags as they stood before the session that wrote them. A tag
    no record kept for the file is None and is not touched."""

    path: Path
    title: str | None
    initialkey: str | None
    session_id: str
    genre: str | None = None

    def value(self, name: str) -> str | None:
        return getattr(self, name)

    @property
    def kept(self) -> tuple[str, ...]:
        """The tags some record kept for this file, in :data:`FIELDS` order."""
        return tuple(name for name in FIELDS if self.value(name) is not None)


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


def _unreadable(record: session.SessionRecord, why: str, key: str = RECORD_KEY) -> Exception:
    return refuse(
        "restore-record-unusable",
        f"session {record.session_id} keeps its files' old tags under "
        f"{key!r} in a form this build cannot read ({why}), so a restore "
        f"would put the rows back and could not put the files back; nothing was "
        f"replaced",
        steps=(
            "the record was changed after the session wrote it, since no build "
            "writes another shape: put back the list the session wrote, from a "
            "copy of the state folder, and run the restore again",
        ),
        origin=("core.restore_tags",),
        detail={"session_id": record.session_id, "key": key, "why": why},
    )


def kept_by(record: session.SessionRecord) -> tuple[FileBefore, ...]:
    """The before values one record keeps, in its order; none when it keeps none.

    Under every record key it holds, one entry per file and key. Refuses a
    record that holds a key in any other shape than a list of entries each
    naming an absolute, unpadded path and each tag as text, a title tag not blank.
    """
    kept: list[FileBefore] = []
    for key, names in _KEPT.items():
        if key not in record.detail:
            continue
        entries = record.detail[key]
        if not isinstance(entries, list):
            raise _unreadable(record, f"a {type(entries).__name__}, not a list", key)
        for index, entry in enumerate(entries):
            kept.append(_entry(record, key, names, index, entry))
    return tuple(kept)


def _entry(
    record: session.SessionRecord, key: str, names: Mapping[str, str], index: int, entry: Any
) -> FileBefore:
    if not isinstance(entry, dict):
        raise _unreadable(record, f"entry {index} is not a mapping", key)
    wanted = ("path", *names.values())
    missing = [name for name in wanted if not isinstance(entry.get(name), str)]
    if missing:
        raise _unreadable(record, f"entry {index} has no text for {', '.join(missing)}", key)
    # A PATH THAT IS NOT ABSOLUTE would resolve against wherever the verb ran,
    # and a BLANK TITLE TAG would be cleared: the adopt writes neither, since it
    # adopts only a title tag with a head on a resolved file (review round one).
    if entry["path"].strip() != entry["path"] or not Path(entry["path"]).is_absolute():
        raise _unreadable(record, f"entry {index} names no absolute path", key)
    values = {tag: entry[recorded] for tag, recorded in names.items()}
    for tag in _NEVER_BLANK & set(values):
        if not values[tag].strip():
            raise _unreadable(record, f"entry {index} keeps a blank title tag", key)
    return FileBefore(
        path=Path(entry["path"]),
        title=values.get("title"),
        initialkey=values.get("initialkey"),
        genre=values.get("genre"),
        session_id=record.session_id,
    )


def befores(
    records: Iterable[session.SessionRecord],
    *,
    rebased: Callable[[Path], Path] = lambda path: path,
) -> tuple[FileBefore, ...]:
    """One before value per file over ``records``, oldest record first.

    THE FIRST RECORD TO NAME A FILE'S TAG WINS, tag by tag: a restore goes back
    to before the earliest session it undoes, so a later session's before value,
    which is the earlier one's after, is never what a file is put back to, and a
    tag only a later session kept is put back to that session's before. Each
    path is passed through ``rebased``, as every recorded path a restore spends is.
    """
    seen: dict[Path, FileBefore] = {}
    for record in records:
        for kept in kept_by(record):
            where = rebased(kept.path)
            held = seen.get(where)
            if held is None:
                seen[where] = replace(kept, path=where)
                continue
            fill = {
                name: kept.value(name)
                for name in FIELDS
                if held.value(name) is None and kept.value(name) is not None
            }
            if fill:
                seen[where] = replace(held, **fill)
    return tuple(seen.values())


def _read(path: Path, names: Sequence[str]) -> dict[str, str] | None:
    """The file's named tags, blank for absent, or None when they cannot be read."""
    try:
        read = tags.read_tags_checked(path, tuple(names))
    except (tags.TagReadFailed, ValueError, OSError):
        return None
    return {name: str(read[name] or "") for name in names}


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
    """Put each file's kept tags back where they differ, then read them back.

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
        names = before.kept
        now = _read(before.path, names)
        if dry_run:
            if now is None:
                failed.append(shown)
            continue
        changes = {
            name: str(before.value(name))
            for name in names
            if now is None or now[name] != before.value(name)
        }
        if changes and not _write(before.path, changes):
            failed.append(shown)
            continue
        again = _read(before.path, names)
        if again is None or any(again[name] != before.value(name) for name in names):
            wrong.append(shown)
            continue
        read_back.append(shown)
    return TagsPutBack(len(planned), tuple(read_back), tuple(failed), tuple(wrong))


__all__: Sequence[str] = (
    "FIELDS", "GENRE_RECORD_KEY", "RECORD_KEY", "FileBefore", "TagsPutBack", "befores", "kept_by", "put_back",
)
