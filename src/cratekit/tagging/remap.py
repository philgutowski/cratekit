"""Rewrite the genres an older mapping wrote from the general catalogue's words (R-799).

THE SELECTION IS WHAT THE TAG JOBS RECORDED, NOT THE GENRE ON THE FILE, which
cannot say who supplied it. Only a file under this library's root is opened,
followed only where it was tagged, and its word resolved again through
:func:`cratekit.tagging.published.choose`. A FILE IS REWRITTEN ONLY WHILE IT
CARRIES WHAT A RECORD SAYS WAS WRITTEN; two records explaining it differently
leave it as ambiguous. A rewrite is recorded one GENERATION past the record it
replaced and only the highest is in force, so a genre put back by hand is not
planned again. One file is one group however its path is spelled; every path
lands in one outcome. Nothing here opens a database.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config, tags, taxonomy
from cratekit.tagging import artifacts, published
from cratekit.tagging.tag import file_genres

#: The name a plan digests under.
WORKFLOW = "tag-remap"

#: The source whose words are resolved again, as a tagging record names it.
SOURCE = published.SOURCE

#: The outcomes, in the order a summary lists them.
AGREE = "agree"
WRITE = "write"
CHANGED_SINCE = "changed-since"
WORD_DECLINED = "word-declined"
AMBIGUOUS_RECORD = "ambiguous-record"
FILE_MISSING = "file-missing"
FILE_UNREADABLE = "file-unreadable"
OUTSIDE_LIBRARY = "outside-library"

OUTCOMES: tuple[str, ...] = (
    AGREE, WRITE, CHANGED_SINCE, WORD_DECLINED, AMBIGUOUS_RECORD, FILE_MISSING, FILE_UNREADABLE,
    OUTSIDE_LIBRARY,
)

#: The outcomes of a file read, not carrying its word's genre, and left; each an item.
LEFT: tuple[str, ...] = (CHANGED_SINCE, WORD_DECLINED, AMBIGUOUS_RECORD)

#: The outcomes of a file under the library whose genre was never learned, listed.
UNREAD: tuple[str, ...] = (FILE_MISSING, FILE_UNREADABLE)

#: What an item that is not written says it does.
LEAVE = "leave"

#: The name the rewrites of one plan are recorded under, before its digest.
RECORD_PREFIX = "remap-"

#: How several genre values on one file are shown as one string.
_JOINED = " | "


@dataclass(frozen=True, slots=True)
class Recorded:
    """One tagging record of a genre written onto a file. ``generation`` is zero
    for a tagging job's, and one past the record it replaced for a rewrite's."""

    job_id: str
    path: str
    written: str
    source: str
    word: str
    generation: int = 0


@dataclass(frozen=True, slots=True)
class Item:
    """One file under the library that does not agree, or could not be read."""

    path: str
    word: str
    recorded: str
    current: str
    wanted: str
    action: str
    reason: str = ""
    #: The explaining record's generation. Bookkeeping, not shown or digested.
    generation: int = 0

    def to_json(self) -> dict[str, str]:
        return {
            "path": self.path,
            "word": self.word,
            "recorded": self.recorded,
            "current": self.current,
            "wanted": self.wanted,
            "action": self.action,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class RemapPlan:
    """Every file that does not agree, and the count of every outcome.
    ``declared`` says the taxonomy has a table for the source; ``records_unread``
    counts committed records that could not be parsed."""

    items: tuple[Item, ...]
    counts: Mapping[str, int]
    declared: bool
    records_unread: int = 0

    @property
    def writes(self) -> tuple[Item, ...]:
        return tuple(item for item in self.items if item.action == WRITE)

    @property
    def files(self) -> int:
        """Every file a record of the source names, wherever it is."""
        return sum(self.counts.values())

    def pairs(self) -> list[dict[str, Any]]:
        """The rewrites as word pairs with their counts, largest first."""
        seen: dict[tuple[str, str], int] = {}
        for item in self.writes:
            key = (item.current, item.wanted)
            seen[key] = seen.get(key, 0) + 1
        return [
            {"from": current, "to": wanted, "files": count}
            for (current, wanted), count in sorted(
                seen.items(), key=lambda entry: (-entry[1], entry[0])
            )
        ]

    @property
    def digest(self) -> str:
        """The fingerprint an approval is bound to, paths included: a decision
        about one folder's files is not one about another's."""
        return digest_of(
            {
                "kind": WORKFLOW,
                "source": SOURCE,
                "items": [item.to_json() for item in self.items],
                "counts": dict(self.counts),
                "declared": self.declared,
                "records_unread": self.records_unread,
            }
        )


@dataclass(frozen=True, slots=True)
class Written:
    """What an apply did, the tuples paths and empty on a clean run;
    ``rewritten`` is every item that read back, the undo of a run that refuses."""

    written: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    unrecorded: tuple[str, ...] = ()
    rewritten: tuple[Item, ...] = ()

    @property
    def clean(self) -> bool:
        return not (self.wrong or self.moved or self.failed or self.unrecorded)


def recorded(reports: Iterable[tuple[str, Mapping[str, Any]]]) -> tuple[Recorded, ...]:
    """The records that say a genre was written, by ANY source, since a shop's
    record is what makes a file ambiguous; a record with no path or genre is not."""
    found: list[Recorded] = []
    for job_id, report in reports:
        path, written = report.get("path"), report.get("genre_written")
        if not isinstance(path, str) or not path:
            continue
        if not isinstance(written, str) or not written.strip():
            continue
        generation = report.get("generation")
        found.append(
            Recorded(
                job_id=job_id,
                path=path,
                written=written.strip(),
                source=str(report.get("source") or ""),
                word=str(report.get("source_genre") or "").strip(),
                generation=(
                    generation
                    if isinstance(generation, int)
                    and not isinstance(generation, bool)
                    and generation > 0
                    else 0
                ),
            )
        )
    return tuple(found)


def _wanted(declared: taxonomy.Taxonomy, word: str) -> str:
    """The genre the taxonomy gives one of the source's words now, or empty."""
    chosen = published.choose(declared, [word]) if word else None
    return chosen[1] if chosen else ""


def _resolved(path: str) -> Path | None:
    """A recorded path with its links and its dots resolved, or None."""
    try:
        return Path(path).resolve()
    except (OSError, ValueError, RuntimeError):
        return None


def _inside(resolved: Path, root: Path) -> bool:
    """Whether a resolved path is under the library's resolved root: by name,
    then by whether a directory above it IS the root, for a volume that folds case."""
    if resolved.is_relative_to(root):
        return True
    for parent in resolved.parents:
        try:
            if parent.samefile(root):
                return True
        except OSError:
            continue
    return False


def _identity(resolved: Path) -> tuple[str, int, int] | tuple[str, str]:
    """What makes two recorded paths one file: its device and inode, else its
    resolved name when it is gone."""
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)


def _settle(
    path: str, records: Sequence[Recorded], declared: taxonomy.Taxonomy
) -> tuple[str, Item | None]:
    """One file's outcome, and its item unless it agrees. Only the source's
    records of the highest generation are in force."""
    newest = max(record.generation for record in records if record.source == SOURCE)
    mine = [
        record
        for record in records
        if record.source == SOURCE and record.generation == newest
    ]
    in_force = [record for record in records if record.source != SOURCE or record in mine]
    shown = mine[-1]

    def left(reason: str, *, current: str = "", wanted: str = "", of: Recorded = shown):
        return reason, Item(path, of.word, of.written, current, wanted, LEAVE, reason)

    target = Path(path)
    try:
        present = target.is_file()
    except OSError:
        # A directory above it this account cannot enter: not gone, and not
        # a reason to end the plan.
        return left(FILE_UNREADABLE)
    if not present:
        return left(FILE_MISSING)
    values = file_genres(target)
    if values is None:
        return left(FILE_UNREADABLE)
    current = _JOINED.join(values)

    # THE RECORDS THAT WROTE EXACTLY THE ONE VALUE THE FILE CARRIES.
    explaining = [record for record in in_force if values == (record.written,)]
    if not explaining:
        # Not written by a record in force: agreeing when it is already what a
        # word is given now, otherwise somebody's own value.
        if any(current and current == _wanted(declared, record.word) for record in mine):
            return AGREE, None
        return left(CHANGED_SINCE, current=current, wanted=_wanted(declared, shown.word))
    if len({(record.source, record.word) for record in explaining}) > 1:
        return left(AMBIGUOUS_RECORD, current=current)
    wrote = explaining[0]
    if wrote.source != SOURCE:
        # A record shop's genre, whose words resolve as they always did.
        return AGREE, None
    wanted = _wanted(declared, wrote.word)
    if not wanted:
        return left(WORD_DECLINED, current=current, of=wrote)
    if wanted == current:
        return AGREE, None
    return WRITE, Item(
        path, wrote.word, wrote.written, current, wanted, WRITE, generation=wrote.generation
    )


def plan(cfg: config.Config, declared: taxonomy.Taxonomy) -> RemapPlan:
    """Plan the rewrite over every tagging record this installation committed,
    in sorted path order so an unchanged queue digests equal."""
    reports, unread = artifacts.every_committed(cfg)
    return plan_records(
        recorded(reports), declared, root=cfg.library.root, records_unread=unread
    )


def plan_records(
    records: Sequence[Recorded],
    declared: taxonomy.Taxonomy,
    *,
    root: Path,
    records_unread: int = 0,
) -> RemapPlan:
    """The plan over records already read. Split out so it is driven with no queue."""
    try:
        library = root.resolve()
    except (OSError, RuntimeError):
        library = root
    # ONE GROUP PER FILE, keyed by the file and named by its first resolved
    # spelling; outside the library nothing is opened, so by its name.
    groups: dict[object, list[Recorded]] = {}
    named: dict[object, str] = {}
    outside: set[object] = set()
    for record in sorted(records, key=lambda one: one.path):
        resolved = _resolved(record.path)
        if resolved is None or not _inside(resolved, library):
            key: object = ("outside", str(resolved) if resolved is not None else record.path)
            outside.add(key)
        else:
            key = _identity(resolved)
        groups.setdefault(key, []).append(record)
        named.setdefault(key, str(resolved) if resolved is not None else record.path)
    counts = dict.fromkeys(OUTCOMES, 0)
    items: list[Item] = []
    for key in sorted(groups, key=lambda one: named[one]):
        group = groups[key]
        if not any(record.source == SOURCE for record in group):
            continue
        if key in outside:
            # COUNTED AND NEVER OPENED: not this library's file, or moved.
            counts[OUTSIDE_LIBRARY] += 1
            continue
        outcome, item = _settle(named[key], group, declared)
        counts[outcome] += 1
        if item is not None:
            items.append(item)
    return RemapPlan(
        items=tuple(items),
        counts=counts,
        declared=declared.vocabulary(SOURCE) is not None,
        records_unread=records_unread,
    )


def _record(cfg: config.Config, name: str, ordinal: int, item: Item) -> bool:
    """Commit the tagging record of one rewrite, staged and renamed into place.
    False when it could not be."""
    try:
        artifacts.commit(
            cfg,
            name,
            ordinal,
            {
                "item": item.path,
                "path": item.path,
                "genre_written": item.wanted,
                "skipped": None,
                "source": SOURCE,
                "source_genre": item.word,
                "remapped_from": item.current,
                "generation": item.generation + 1,
            },
        )
    except OSError:
        return False
    return True


def apply(cfg: config.Config, remap_plan: RemapPlan) -> Written:
    """Write each planned genre onto its file, read it back and record it. Each
    file is read again first, and nothing raises for one file."""
    written = read_back = 0
    wrong: list[str] = []
    moved: list[str] = []
    failed: list[str] = []
    unrecorded: list[str] = []
    rewritten: list[Item] = []
    # ONCE: the records of one plan sit under one name.
    name = f"{RECORD_PREFIX}{remap_plan.digest}"
    for ordinal, item in enumerate(remap_plan.writes):
        target = Path(item.path)
        if file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
        if not tags.write_genre(target, item.wanted):
            failed.append(item.path)
            continue
        written += 1
        if file_genres(target) != (item.wanted,):
            wrong.append(item.path)
            continue
        read_back += 1
        rewritten.append(item)
        if not _record(cfg, name, ordinal, item):
            unrecorded.append(item.path)
    return Written(
        written=written,
        read_back=read_back,
        wrong=tuple(wrong),
        moved=tuple(moved),
        failed=tuple(failed),
        unrecorded=tuple(unrecorded),
        rewritten=tuple(rewritten),
    )


__all__ = [
    "AGREE", "AMBIGUOUS_RECORD", "CHANGED_SINCE", "FILE_MISSING", "FILE_UNREADABLE", "LEAVE",
    "LEFT", "OUTCOMES", "OUTSIDE_LIBRARY", "RECORD_PREFIX", "SOURCE", "UNREAD", "WORD_DECLINED",
    "WORKFLOW", "WRITE", "Item", "Recorded", "RemapPlan", "Written", "apply", "plan",
    "plan_records", "recorded",
]
