"""Rewrite the genres an older mapping wrote from the general catalogue's words (R-799).

WHY THIS EXISTS. The tagger writes a genre once, fill if empty, so a word
filed by a mapping that has since changed stays on the file. The general
catalogue's Pop was written as the dance bucket's name and its Alternative as
a bucket's bare name, by aliases written for the record shops. The taxonomy
now gives that catalogue a table of its own, and the files tagged before it
did are the ones this module finds and plans the rewrite of.

THE SELECTION IS WHAT THE TAG JOBS RECORDED, AND NOT THE GENRE ON THE FILE. A
file carrying the dance bucket's name got it from a record shop or from the
general catalogue, and only the first is right. The file cannot say which. The
tagging job's item record can: it names the path, the genre written, the
source that supplied it and that source's word. So every committed record is
read, and a record whose source is the general catalogue names a file to look
at.

ONLY A FILE UNDER THIS LIBRARY'S ROOT IS OPENED. The queue the records sit in
is the installation's, so it holds records of folders tagged before they were
landed and of any other library this machine has tagged. Those files are
resolved by another taxonomy or are gone, and are counted apart and never
read. A FILE IS FOLLOWED ONLY WHERE IT WAS TAGGED: one tagged in a staging
folder and landed since is not found, because nothing in its record says
where it went.

THE WORD IS RESOLVED AGAIN, ALONE, through :func:`cratekit.tagging.published.choose`,
which is what the tagger asks. The record carries the one word the tagger
picked from the album's list and not the list.

A FILE IS REWRITTEN ONLY WHEN IT STILL CARRIES WHAT A RECORD SAYS WAS WRITTEN.
Anything else on it was put there since, by a person or by another verb, and
is not this module's to replace. The same holds when two records explain the
file's genre with different words or different sources: the records carry no
time, so which of them wrote it is not known, and the file is listed and left.

A REWRITE IS RECORDED AS A TAGGING RECORD OF ITS OWN, committed beside the
others once the file reads back. Without it this module's own write would
look like a hand edit to the next run, and a word the taxonomy gives a new
genre a second time could never be corrected a second time.

A REWRITE RETIRES THE RECORD IT REPLACED. The records carry no time, so each
rewrite's record carries a GENERATION, one past the record that explained the
file, and only the highest generation of the source's records on a file is
still in force. Without that, a genre a person put back by hand after a
rewrite matched the retired record and was planned for rewrite on every run,
which is the undo this verb's own message describes being undone.

ONE FILE IS ONE GROUP, WHATEVER ITS RECORDS CALL IT. A folder tagged twice
under two spellings of its path, or two cases on a volume that folds case,
records one file under two strings. Grouped by the string, a record shop's
record of the same genre was never seen beside the general catalogue's, and
one file was planned twice.

EVERY PATH LANDS IN ONE OUTCOME, counted zero filled. A plan that names only
what it writes makes "nothing else was found" and "nothing else was looked at"
the same output. A file that is gone or cannot be read is counted under its
own name and never as agreeing.

NOTHING HERE OPENS A DATABASE. The row's genre follows by the row verb.

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

#: The name a plan digests under.
WORKFLOW = "tag-remap"

#: The source whose words are resolved again: the general catalogue, by the
#: name a tagging record gives it.
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
    AGREE,
    WRITE,
    CHANGED_SINCE,
    WORD_DECLINED,
    AMBIGUOUS_RECORD,
    FILE_MISSING,
    FILE_UNREADABLE,
    OUTSIDE_LIBRARY,
)

#: The outcomes of a file that was read, does not carry what the taxonomy now
#: gives its word, and is left alone. Each is listed in the plan as an item.
LEFT: tuple[str, ...] = (CHANGED_SINCE, WORD_DECLINED, AMBIGUOUS_RECORD)

#: The outcomes of a file under the library whose genre was never learned.
#: Each is listed too.
UNREAD: tuple[str, ...] = (FILE_MISSING, FILE_UNREADABLE)

#: What an item that is not written says it does.
LEAVE = "leave"

#: The name the rewrites of one plan are recorded under, before its digest.
RECORD_PREFIX = "remap-"

#: How several genre values on one file are shown as one string.
_JOINED = " | "


@dataclass(frozen=True, slots=True)
class Recorded:
    """One tagging record of a genre written onto a file.

    ``generation`` is zero for a tagging job's record and, for a rewrite's
    record, one past the record that explained the file when it was rewritten.
    """

    job_id: str
    path: str
    written: str
    source: str
    word: str
    generation: int = 0


@dataclass(frozen=True, slots=True)
class Item:
    """One file under the library that does not agree, or could not be read.

    ``word`` is the general catalogue's word a record carries for the file and
    ``recorded`` the genre that record says was written. ``current`` is what
    the file carries now, empty when it is blank or was not read. ``wanted`` is
    the genre the taxonomy gives the word now, empty when it gives none.
    ``action`` is :data:`WRITE` or :data:`LEAVE`, and ``reason`` is the outcome
    a left file was counted under, empty on a write.
    """

    path: str
    word: str
    recorded: str
    current: str
    wanted: str
    action: str
    reason: str = ""
    #: The generation of the record that explains the file, which the record
    #: of a rewrite goes one past. Bookkeeping, and not shown or digested.
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

    ``declared`` says whether the taxonomy has a table for the source at all.
    ``records_unread`` counts committed records that could not be parsed, each
    a file this plan might have needed to look at and did not.
    """

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
        """The fingerprint an approval is bound to.

        OVER THE ITEMS, THE COUNTS AND WHAT COULD NOT BE READ. The path is in
        it: this plan is about files where they are, and a decision about one
        folder's files is not a decision about another's.
        """
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
    """What an apply did. The four tuples are paths, and empty on a clean run.

    ``written`` counts the files whose write the tag writer said it made, and
    ``read_back`` those of them that read back as the genre wanted. ``moved``
    is a file that no longer carried what the plan read when the write reached
    it, and was not written. ``failed`` is a file the tag writer could not
    write, which is untouched. ``wrong`` is a file that was written and does
    not read back as wanted. ``unrecorded`` is a file that was rewritten and
    read back and whose record could not be committed. ``rewritten`` is every
    item that read back, which is what an undo needs when the run refuses.
    """

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


# ---------------------------------------------------------------------------
# The records
# ---------------------------------------------------------------------------


def recorded(reports: Iterable[tuple[str, Mapping[str, Any]]]) -> tuple[Recorded, ...]:
    """The records that say a genre was written, by any source.

    EVERY SOURCE IS KEPT, not only the general catalogue's. A record shop's
    record of the same genre on the same path is what makes a file's genre
    ambiguous, and a reader that dropped it would plan the rewrite of a genre
    a record shop supplied.

    A record with no path or no genre written says nothing was written, which
    is what the coarse genre correction's records look like too, so both are
    passed over by shape. This module's own records carry both and are read
    like any tagging record, which is the point of them.
    """
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


def _file_genres(path: Path) -> tuple[str, ...] | None:
    """Every genre value the file holds, or None when it could not be read.

    ONE OPEN, through the exact reader that keeps a failed read apart from an
    absent field. A file nobody could read must not be taken for a blank one,
    and a file holding a second genre does not carry only what a tagging job
    wrote, whatever its first value is.
    """
    try:
        values = tags.read_tag_values_checked(path, "genre") or ()
    except (tags.TagReadFailed, OSError):
        return None
    return tuple(word for word in (value.strip() for value in values) if word)


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
    """Whether a resolved path is under the library's resolved root.

    BY NAME, AND THEN BY THE DIRECTORY ITSELF. A volume that folds case names
    one directory two ways, and resolving a path does not fold it, so a folder
    typed in another case than the configured root reads as outside it while
    being the same directory. So a path that is not under the root by name is
    asked whether any directory above it IS the root. A directory that is not
    there is not the root.
    """
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
    """What makes two recorded paths one file: the file itself, where it exists.

    The device and the inode, so two spellings and two cases of one file are
    one group. A file that is gone has only its resolved name to go by.
    """
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)


def _settle(
    path: str, records: Sequence[Recorded], declared: taxonomy.Taxonomy
) -> tuple[str, Item | None]:
    """One file's outcome, and its item unless it agrees.

    ``records`` is every record of a genre written onto this file, and at
    least one of them is the source's. THEY CARRY NO TIME. What stands in for
    one is the generation a rewrite's record carries: only the source's
    records of the highest generation are still in force, and every lower one
    was replaced by a rewrite. When several are in force, the one a left item
    shows is whichever sorts last, which is display and no more.
    """
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
    if not target.is_file():
        return left(FILE_MISSING)
    values = _file_genres(target)
    if values is None:
        return left(FILE_UNREADABLE)
    current = _JOINED.join(values)

    # WHICH RECORDS EXPLAIN WHAT THE FILE CARRIES. One value, and a record that
    # wrote exactly it.
    explaining = [record for record in in_force if values == (record.written,)]
    if not explaining:
        # No record in force says this was written. It agrees when it is
        # already what one of the source's words is given now, which is a file
        # a person corrected, and is otherwise somebody's own value, a genre a
        # person put back after a rewrite among them.
        if any(current and current == _wanted(declared, record.word) for record in mine):
            return AGREE, None
        return left(CHANGED_SINCE, current=current, wanted=_wanted(declared, shown.word))
    if len({(record.source, record.word) for record in explaining}) > 1:
        return left(AMBIGUOUS_RECORD, current=current)
    wrote = explaining[0]
    if wrote.source != SOURCE:
        # A record shop wrote what the file carries, on a path the general
        # catalogue once wrote too. The shops' words resolve as they always
        # did, so there is nothing to correct.
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
    """Plan the rewrite over every tagging record this installation committed.

    Paths in sorted order, so two plans over one unchanged queue and one
    unchanged set of files digest equal.
    """
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
    # ONE GROUP PER FILE. Under the library a group is keyed by the file
    # itself, and named by the first of its resolved spellings in sorted
    # order. Outside it nothing is opened, so a group is its resolved name.
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
            # COUNTED AND NEVER OPENED. Not this library's file, or not where
            # it was when it was tagged, and this library's taxonomy is not
            # the one to resolve its word by.
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


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def _record(cfg: config.Config, name: str, ordinal: int, item: Item) -> bool:
    """Commit the tagging record of one rewrite. False when it could not be.

    Through the engine's own commit, staged and then renamed into place, so a
    run killed part way never leaves half a record for every later plan to
    count as unread.
    """
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
    """Write each planned genre onto its file, read it back and record it.

    EACH FILE IS READ AGAIN BEFORE IT IS WRITTEN. The plan was approved over
    what the files carried when it was made, and a file that carries something
    else by now is left and named rather than written over.

    THE WRITER'S OWN ANSWER IS KEPT. A file it says it could not write is
    untouched and is named as that, apart from one it wrote that does not read
    back, so a person is not sent looking for damage on a file nothing changed.

    THE RECORD FOLLOWS THE READ BACK, per file. Committed first, a write that
    then failed would leave a record of a genre the file never carried.
    Committed last of all, a run that died half way would leave every file it
    had rewritten looking like a hand edit to the next run.

    Nothing here raises for one file, so one that cannot be written does not
    stop the rest, and the caller refuses over what is named.
    """
    written = read_back = 0
    wrong: list[str] = []
    moved: list[str] = []
    failed: list[str] = []
    unrecorded: list[str] = []
    rewritten: list[Item] = []
    # ONCE. The digest serializes every item, and the records of one plan sit
    # under one name.
    name = f"{RECORD_PREFIX}{remap_plan.digest}"
    for ordinal, item in enumerate(remap_plan.writes):
        target = Path(item.path)
        if _file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
        if not tags.write_genre(target, item.wanted):
            failed.append(item.path)
            continue
        written += 1
        if _file_genres(target) != (item.wanted,):
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
    "AGREE",
    "AMBIGUOUS_RECORD",
    "CHANGED_SINCE",
    "FILE_MISSING",
    "FILE_UNREADABLE",
    "LEAVE",
    "LEFT",
    "OUTCOMES",
    "OUTSIDE_LIBRARY",
    "RECORD_PREFIX",
    "SOURCE",
    "UNREAD",
    "WORD_DECLINED",
    "WORKFLOW",
    "WRITE",
    "Item",
    "Recorded",
    "RemapPlan",
    "Written",
    "apply",
    "plan",
    "plan_records",
    "recorded",
]
