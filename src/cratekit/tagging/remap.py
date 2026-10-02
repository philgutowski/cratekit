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

THE WORD IS RESOLVED AGAIN, ALONE, through :func:`cratekit.tagging.published.choose`,
which is what the tagger asks. The record carries the one word the tagger
picked from the album's list and not the list.

A FILE IS REWRITTEN ONLY WHEN IT STILL CARRIES WHAT THE JOB WROTE. Anything
else on it was put there since, by a person or by another verb, and is not
this module's to replace. The same holds when two records explain the file's
genre with different words or different sources: which of them wrote it last
is not recorded, so the file is listed and left.

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

OUTCOMES: tuple[str, ...] = (
    AGREE,
    WRITE,
    CHANGED_SINCE,
    WORD_DECLINED,
    AMBIGUOUS_RECORD,
    FILE_MISSING,
    FILE_UNREADABLE,
)

#: The outcomes of a file that was read, does not carry what the taxonomy now
#: gives its word, and is left alone.
LEFT: tuple[str, ...] = (CHANGED_SINCE, WORD_DECLINED, AMBIGUOUS_RECORD)

#: The outcomes in which the file's genre was never learned.
UNREAD: tuple[str, ...] = (FILE_MISSING, FILE_UNREADABLE)

#: What an item that is not written says it does.
LEAVE = "leave"

#: How several genre values on one file are shown as one string.
_JOINED = " | "


@dataclass(frozen=True, slots=True)
class Recorded:
    """One tagging record of a genre written onto a file."""

    job_id: str
    path: str
    written: str
    source: str
    word: str


@dataclass(frozen=True, slots=True)
class Item:
    """One file that does not agree, or could not be read.

    ``word`` is the general catalogue's word a record carries for the file and
    ``recorded`` the genre that record's job wrote. ``current`` is what the
    file carries now, empty when it is blank or was not read. ``wanted`` is
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
        """Every file a record of the source names."""
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
    """What an apply did. ``wrong`` and ``moved`` are paths, and empty when clean.

    ``moved`` is a file that no longer carried what the plan read when the
    write reached it, and was not written. ``wrong`` is a file that was
    written and does not read back as the genre wanted.
    """

    written: int
    read_back: int
    wrong: tuple[str, ...] = ()
    moved: tuple[str, ...] = ()


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
    is what the correction verb's own records look like too, so both are
    passed over by shape.
    """
    found: list[Recorded] = []
    for job_id, report in reports:
        path, written = report.get("path"), report.get("genre_written")
        if not isinstance(path, str) or not path:
            continue
        if not isinstance(written, str) or not written.strip():
            continue
        found.append(
            Recorded(
                job_id=job_id,
                path=path,
                written=written.strip(),
                source=str(report.get("source") or ""),
                word=str(report.get("source_genre") or "").strip(),
            )
        )
    return tuple(found)


def _file_genres(path: Path) -> tuple[str, ...] | None:
    """Every genre value the file holds, or None when it could not be read.

    THE CHECKED READER FIRST, because the exact reader folds a failed read
    into an absent field and a file nobody could read must not be taken for a
    blank one. Then every value, since a file holding a second genre does not
    carry only what a tagging job wrote, whatever its first value is.
    """
    try:
        tags.read_tags_checked(path, ("genre",))
    except (tags.TagReadFailed, OSError):
        return None
    values = tags.read_tag_values(path, "genre") or ()
    return tuple(
        word
        for value in values
        for word in (part.strip() for part in value.split("\x00"))
        if word
    )


def _wanted(declared: taxonomy.Taxonomy, word: str) -> str:
    """The genre the taxonomy gives one of the source's words now, or empty."""
    chosen = published.choose(declared, [word]) if word else None
    return chosen[1] if chosen else ""


def _settle(
    path: str, records: Sequence[Recorded], declared: taxonomy.Taxonomy
) -> tuple[str, Item | None]:
    """One file's outcome, and its item unless it agrees.

    ``records`` is every record of a genre written onto this path, and at
    least one of them is the source's.
    """
    mine = [record for record in records if record.source == SOURCE]
    last = mine[-1]

    def left(reason: str, *, current: str = "", wanted: str = "", of: Recorded = last):
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
    explaining = [record for record in records if values == (record.written,)]
    if not explaining:
        # Nobody recorded writing this. It agrees when it is already what one
        # of the source's words is given now, which is a file this verb or a
        # person corrected, and is otherwise somebody's own value.
        if any(current and current == _wanted(declared, record.word) for record in mine):
            return AGREE, None
        return left(CHANGED_SINCE, current=current, wanted=_wanted(declared, last.word))
    if len({(record.source, record.word) for record in explaining}) > 1:
        return left(AMBIGUOUS_RECORD, current=current)
    wrote = explaining[-1]
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
    return WRITE, Item(path, wrote.word, wrote.written, current, wanted, WRITE)


def plan(cfg: config.Config, declared: taxonomy.Taxonomy) -> RemapPlan:
    """Plan the rewrite over every tagging record this installation committed.

    Paths in sorted order, so two plans over one unchanged queue and one
    unchanged set of files digest equal.
    """
    reports, unread = artifacts.every_committed(cfg)
    return plan_records(recorded(reports), declared, records_unread=unread)


def plan_records(
    records: Sequence[Recorded], declared: taxonomy.Taxonomy, *, records_unread: int = 0
) -> RemapPlan:
    """The plan over records already read. Split out so it is driven with no queue."""
    by_path: dict[str, list[Recorded]] = {}
    for record in records:
        by_path.setdefault(record.path, []).append(record)
    counts = dict.fromkeys(OUTCOMES, 0)
    items: list[Item] = []
    for path in sorted(by_path):
        group = by_path[path]
        if not any(record.source == SOURCE for record in group):
            continue
        outcome, item = _settle(path, group, declared)
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


def apply(remap_plan: RemapPlan) -> Written:
    """Write each planned genre onto its file and read it back.

    EACH FILE IS READ AGAIN BEFORE IT IS WRITTEN. The plan was approved over
    what the files carried when it was made, and a file that carries something
    else by now is left and named rather than written over. A file whose write
    failed, or that does not read back as wanted, is named too. Nothing here
    raises for one file, so one that cannot be written does not stop the rest,
    and the caller refuses over what is named.
    """
    written = read_back = 0
    wrong: list[str] = []
    moved: list[str] = []
    for item in remap_plan.writes:
        target = Path(item.path)
        if _file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
        written += 1
        tags.write_genre(target, item.wanted)
        if _file_genres(target) == (item.wanted,):
            read_back += 1
        else:
            wrong.append(item.path)
    return Written(written=written, read_back=read_back, wrong=tuple(wrong), moved=tuple(moved))


__all__ = [
    "AGREE",
    "AMBIGUOUS_RECORD",
    "CHANGED_SINCE",
    "FILE_MISSING",
    "FILE_UNREADABLE",
    "LEAVE",
    "LEFT",
    "OUTCOMES",
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
