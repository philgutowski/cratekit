"""The proof that a file is unreferenced, and the six answers a candidate can get.

**THE 144-FILE LOSS IS WHY THIS MODULE IS SHAPED THE WAY IT IS.** An ad-hoc
orphan sweep in the system being ported compared walked disk paths against
decoded rekordbox locations with ``==``. macOS hands filenames back in whichever
composition form they were created in, rekordbox exports them composed, and the
two spellings of one accented name are different strings. The sweep concluded
that 144 still-referenced files had nothing pointing at them and deleted every
one. Every single file lost was non-ASCII.

``core.locations`` fixes the string comparison, and R37 goes further and says a
string comparison is not what may authorise a deletion at all. **The filesystem
decides.** A candidate is deletable only when its device and inode match no
active row's resolved file, and when its size matches the size the removed row
recorded. Those two assertions cover, without knowing anything about any of them:

* a case-only difference, on a case-insensitive volume, because both spellings
  open the same inode;
* a composition-form difference, on a normalization-insensitive volume, for the
  same reason;
* a hard link, because two names for one inode are one inode;
* a symbolic link, because the stat follows it;
* a path later reclaimed by a DIFFERENT track through name truncation, because
  the file sitting there now is a different file and its size says so.

**THE REFERENCE SET MUST BE COMPLETE BEFORE ANY OF THAT MEANS ANYTHING.** "No
active row's inode matches" is a claim about every active row. An active row that
resolves nowhere, or that resolves and cannot be inspected, contributes no inode,
so the proof passes on ABSENCE OF EVIDENCE and the file it protected is trashed.
:func:`assert_complete` refuses the whole run in that case rather than offering a
smaller set, and it reports the count, because a partial answer to this question
is not a smaller answer, it is a wrong one.

**ONE DELIBERATE READING, RECORDED BECAUSE IT LOOKS LIKE A GAP.** An active row
whose resolved path simply does not exist is NOT treated as incomplete evidence.
It is the opposite: the filesystem answered, and the answer was that this row
references no existing file, so it cannot be the row that references a file that
does exist. Counting it as incomplete would refuse the whole feature for any
library holding a single row whose file the user moved by hand, which is every
real library. A row that exists and cannot be STAT'd is the incomplete case, and
so is one whose recorded prefix nothing maps, and both refuse.

Layer note: MODULES. Pure apart from one injected ``stat``, so every branch is
reachable without a filesystem shaped for it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from cratekit.core import locations
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.deletion.library import RemovedRow
from cratekit.write import trees

#: The stat this module uses. ``os.stat`` FOLLOWS symbolic links, deliberately: a
#: row recorded against a link into the library names the same inode as the file
#: the link points at, and a proof that used ``lstat`` would see two inodes and
#: report the file unreferenced.
Stat = Callable[[str], os.stat_result]


@dataclass(frozen=True, slots=True)
class FileIdentity:
    """What the filesystem calls one file, as opposed to what a string calls it.

    The pair is the identity, not either half: inode numbers are unique per
    filesystem and are reused freely across them, so a bare inode comparison
    across two mounted volumes reports collisions that are not collisions.
    """

    device: int
    inode: int

    @classmethod
    def of(cls, stats: os.stat_result) -> FileIdentity:
        return cls(device=stats.st_dev, inode=stats.st_ino)


class Category(StrEnum):
    """What this run decided about one removed row. Explicit, and closed.

    Every category except ``DELETABLE`` means "no file moves", and they are kept
    apart rather than collapsed into one because the ACT that clears each of them
    is different: fix the volume prefix map, look at which row is the mistake,
    work out why the file changed size, take the track out of the playlist, or
    nothing at all.
    """

    #: Proved unreferenced and proved to be the file the row described.
    DELETABLE = "deletable"
    #: The recorded path maps nowhere this machine can name, or names something
    #: that is not a path, or resolved and could not be inspected. AE16: no file
    #: moves and the watermark does not treat it as handled.
    UNRESOLVED = "unresolved"
    #: The file is also the file an ACTIVE row points at. Same path, a case-only
    #: difference, a composition-form difference, or a link: the inode says so.
    COLLIDES_WITH_ACTIVE_ROW = "collides-with-active-row"
    #: The file is not the size the removed row recorded, or the row recorded no
    #: size at all, so it cannot be proved to be the file that was removed.
    SIZE_MISMATCH = "size-mismatch"
    #: A playlist on this volume still points at it.
    STILL_REFERENCED = "still-referenced"
    #: The file is already gone. Somebody deleted it by hand, or a previous run
    #: of this pass trashed it and was interrupted before it advanced the
    #: watermark. Finished business either way, which is what makes a run that
    #: crashed mid-trash resume rather than re-offer.
    GONE = "gone"
    #: A person was shown this file and said to keep it (R35). Never offered
    #: again until the decline is revoked.
    DECLINED = "declined"
    #: The row records neither an artist nor a title, so R36's tombstone would
    #: have nothing to identify the version by. Its own category rather than one
    #: of the ones above, and it is checked BEFORE anything is resolved, because
    #: the alternative is discovering it in the one window where failing has
    #: already destroyed something: between the move to the Trash and the record
    #: of what was moved.
    UNIDENTIFIABLE = "unidentifiable"


#: The categories that are finished business, so the watermark may pass over
#: them. DERIVED into one place rather than tested inline at each caller, because
#: a category added later that nobody classified would silently join whichever
#: side the last ``if`` happened to leave it on.
HANDLED: frozenset[Category] = frozenset({Category.GONE, Category.DECLINED})


@dataclass(frozen=True, slots=True)
class ReferenceSet:
    """Every active row's file, by filesystem identity, and what is missing from it.

    ``unmapped`` and ``uninspectable`` are the two ways the set can be short, and
    they are counted separately because they send a person to different places: a
    prefix nothing maps is configuration, and a file that will not stat is
    permissions or a filesystem that is not answering.
    """

    by_identity: Mapping[FileIdentity, tuple[str, ...]]
    unmapped: tuple[str, ...] = ()
    uninspectable: tuple[str, ...] = ()
    #: Active rows that resolved to a path with no file at it. Reported rather
    #: than blocking: see the module docstring for why this is evidence rather
    #: than the absence of it.
    missing: tuple[str, ...] = ()

    @property
    def complete(self) -> bool:
        return not self.unmapped and not self.uninspectable


def reference_set(
    active: Iterable[trees.ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
    stat: Stat = os.stat,
) -> ReferenceSet:
    """Index every active row by the file it actually points at.

    Every recorded path goes through the same resolver the rest of the system
    uses, with the configured volume prefix map applied. Skipping that is not a
    smaller version of this function: measured against the library this was
    designed for, a naive resolver resolves zero of 9,919 active rows, so it
    would produce an empty reference set and declare every file in the library
    unreferenced.

    A row whose recorded location is not a path at all is neither indexed nor
    counted against completeness. A streamed track has a pseudo-location rather
    than a file, so it cannot be the row that references a file, and counting it
    as missing evidence would refuse the whole run for a library that has ever
    streamed anything.
    """
    found: dict[FileIdentity, list[str]] = {}
    unmapped: list[str] = []
    uninspectable: list[str] = []
    missing: list[str] = []
    for row in active:
        if row.deleted:
            # The caller partitions before this, so a tombstone arriving here is a
            # caller defect rather than a case. Skipping it keeps the active-row
            # rule true whichever way it arrived: a removed row may never claim a
            # location, which is what makes a tombstone beside a live row read
            # cleanly rather than as a collision.
            continue
        resolved = locations.resolve_recorded_path(
            row.recorded, root=root, prefix_map=prefix_map
        )
        if resolved.resolution is locations.Resolution.NOT_A_PATH:
            continue
        if resolved.path is None:
            unmapped.append(row.content_id)
            continue
        try:
            stats = stat(resolved.path)
        except FileNotFoundError:
            missing.append(row.content_id)
            continue
        except OSError:
            uninspectable.append(row.content_id)
            continue
        found.setdefault(FileIdentity.of(stats), []).append(row.content_id)
    return ReferenceSet(
        by_identity={identity: tuple(ids) for identity, ids in found.items()},
        unmapped=tuple(unmapped),
        uninspectable=tuple(uninspectable),
        missing=tuple(missing),
    )


def assert_complete(references: ReferenceSet) -> None:
    """Refuse the run unless every active row contributed an answer.

    OFFERS NOTHING RATHER THAN OFFERING LESS. A run that dropped the unresolvable
    rows and carried on would still present candidates, and every one of those
    candidates would carry a proof with a hole in it exactly the size of the rows
    that were dropped. The user cannot see the hole, and the thing on the other
    side of it is their music.
    """
    if references.complete:
        return
    raise refuse(
        "deletion-reference-set-incomplete",
        f"{len(references.unmapped)} active rows record a location this machine "
        f"cannot resolve and {len(references.uninspectable)} resolve to files "
        f"that could not be inspected, so the proof that a removed file is "
        f"unreferenced would be a proof about the rows that happened to answer; "
        f"nothing is offered this run",
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.RUN,
        origin=("deletion.candidates",),
        detail={
            "unmapped": len(references.unmapped),
            "uninspectable": len(references.uninspectable),
            "unmapped_rows": list(references.unmapped[:20]),
            "uninspectable_rows": list(references.uninspectable[:20]),
        },
    )


@dataclass(frozen=True, slots=True)
class Candidate:
    """One removed row, the answer this run reached, and the evidence for it.

    ``problem`` is a sentence and is never branched on. Anything a caller has to
    act on is the ``category``, which is the same rule the structured cause type
    applies to its own detail: a consumer reading prose for control flow has
    re-invented the untyped failure the type replaced.
    """

    row: RemovedRow
    category: Category
    resolved: str | None = None
    identity: FileIdentity | None = None
    observed_size: int | None = None
    collides_with: tuple[str, ...] = ()
    problem: str = ""

    @property
    def deletable(self) -> bool:
        return self.category is Category.DELETABLE

    @property
    def handled(self) -> bool:
        """Whether the watermark may pass over this row as finished business."""
        return self.category in HANDLED


def categorize(
    removed: Iterable[RemovedRow],
    references: ReferenceSet,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
    referenced: frozenset[str] = frozenset(),
    declined: Callable[[RemovedRow], bool] = lambda _row: False,
    identifiable: Callable[[RemovedRow], bool] = lambda _row: True,
    stat: Stat = os.stat,
) -> tuple[Candidate, ...]:
    """Answer every removed row, in the order R37 states its assertions.

    The order is the order of the sentence: identity, then size, then the
    playlist, then resolution. It decides only which category a row that fails
    several assertions is REPORTED under, since every one of them means the same
    thing about the file, which is that it stays where it is.

    ``declined`` is a predicate rather than a set, so the decision store answers
    it directly and nothing here has to know how a decline is addressed.
    """
    out: list[Candidate] = []
    for row in removed:
        if declined(row):
            out.append(Candidate(row=row, category=Category.DECLINED))
            continue
        if not identifiable(row):
            out.append(
                Candidate(
                    row=row,
                    category=Category.UNIDENTIFIABLE,
                    problem=(
                        "the row records neither an artist nor a title, so the "
                        "tombstone R36 requires could not identify the version "
                        "this deletion suppresses"
                    ),
                )
            )
            continue
        resolved = locations.resolve_recorded_path(
            row.recorded, root=root, prefix_map=prefix_map
        )
        if resolved.path is None:
            out.append(
                Candidate(
                    row=row,
                    category=Category.UNRESOLVED,
                    problem=(
                        "the recorded location is not a path this machine can name"
                        if resolved.resolution is locations.Resolution.NOT_A_PATH
                        else f"no volume prefix rule maps {resolved.prefix!r}"
                    ),
                )
            )
            continue
        try:
            stats = stat(resolved.path)
        except FileNotFoundError:
            out.append(Candidate(row=row, category=Category.GONE, resolved=resolved.path))
            continue
        except OSError as exc:
            out.append(
                Candidate(
                    row=row,
                    category=Category.UNRESOLVED,
                    resolved=resolved.path,
                    problem=f"the file could not be inspected: {exc}",
                )
            )
            continue
        identity = FileIdentity.of(stats)
        claimed = references.by_identity.get(identity, ())
        if claimed:
            out.append(
                Candidate(
                    row=row,
                    category=Category.COLLIDES_WITH_ACTIVE_ROW,
                    resolved=resolved.path,
                    identity=identity,
                    observed_size=stats.st_size,
                    collides_with=claimed,
                    problem=(
                        f"the same file is the file active row(s) "
                        f"{', '.join(claimed)} point at"
                    ),
                )
            )
            continue
        if row.size is None or int(stats.st_size) != int(row.size):
            out.append(
                Candidate(
                    row=row,
                    category=Category.SIZE_MISMATCH,
                    resolved=resolved.path,
                    identity=identity,
                    observed_size=stats.st_size,
                    problem=(
                        "the removed row recorded no size, so nothing proves this "
                        "is the file it named"
                        if row.size is None
                        else f"the row recorded {row.size} bytes and the file holds "
                        f"{stats.st_size}"
                    ),
                )
            )
            continue
        if row.content_id in referenced:
            out.append(
                Candidate(
                    row=row,
                    category=Category.STILL_REFERENCED,
                    resolved=resolved.path,
                    identity=identity,
                    observed_size=stats.st_size,
                    problem="a playlist on this volume still points at this track",
                )
            )
            continue
        out.append(
            Candidate(
                row=row,
                category=Category.DELETABLE,
                resolved=resolved.path,
                identity=identity,
                observed_size=stats.st_size,
            )
        )
    return tuple(out)


def recheck(
    candidate: Candidate,
    references: ReferenceSet,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
    referenced: frozenset[str] = frozenset(),
    declined: Callable[[RemovedRow], bool] = lambda _row: False,
    identifiable: Callable[[RemovedRow], bool] = lambda _row: True,
    stat: Stat = os.stat,
) -> Candidate:
    """Re-run every assertion for ONE candidate, immediately before its move.

    R37's last sentence, and it is not a formality. A review item is durable: a
    person may confirm one days after it was raised, from another process, and in
    between they may have re-imported the track, restored a backup over it, or
    added it to a playlist. The categories this run reached at review time are a
    photograph, and the move has to be made against the library as it is at the
    instant of the move.

    IT IS THE SAME CODE PATH, not a second smaller version of it. A re-check
    written as its own set of ``if`` statements would be a second opinion, and the
    two would eventually differ about what a collision is. This calls
    :func:`categorize` over one row, so the preview and the write are the same
    function by construction.
    """
    answered = categorize(
        [candidate.row],
        references,
        root=root,
        prefix_map=prefix_map,
        referenced=referenced,
        declined=declined,
        identifiable=identifiable,
        stat=stat,
    )
    return answered[0]


__all__ = [
    "HANDLED",
    "Candidate",
    "Category",
    "FileIdentity",
    "ReferenceSet",
    "Stat",
    "assert_complete",
    "categorize",
    "recheck",
    "reference_set",
]
