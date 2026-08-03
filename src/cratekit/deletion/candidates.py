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

**AND THERE IS ONE PLACE THAT READING DOES NOT REACH, WHICH IS THE ANCHOR.**
``FileNotFoundError`` carries two facts and only one of them is an answer about
the row. "This row's file is gone" is an answer. "Every row that went through
prefix rule 2 points into a directory that is not there" is the MAPPING failing,
which is the same fault class as a prefix nothing maps, and that one already
refuses. Fused, the two produce a perverse property: OMITTING a prefix rule
refuses loudly, while adding a WRONG one proceeds silently. One character wrong
in a configured target, a mapped volume nobody plugged in, and a drive somebody
renamed all land there, and all three end the same way, with every active row
counted as a missing file, an EMPTY reference set, ``complete`` true, and every
removed row proved unreferenced against nothing at all.

So the DIRECTORY a resolved path is anchored in is checked, once per anchor: the
library root for a row under it, and the rule's target for a row a rule remapped.
A row whose anchor is not there is ``unanchored`` rather than ``missing``, and
``unanchored`` refuses and names the anchor. The check is per ANCHOR rather than
per parent directory deliberately: a user who deletes one album folder in the
Finder has a real library with a real hole in it and must still be served, while
a rule whose target does not exist can say nothing about any row that went
through it. The same split runs over the removed rows in :func:`categorize`,
where fusing them is worse still, since ``GONE`` is finished business and the
watermark passes over it.

**AND ``missing`` IS NEVER SILENT, even where it correctly does not refuse.** It
is counted, it rides on the reference set, it is reported in the refusal detail,
and the pass logs it, because "these active rows point at files that are not
there" is worth knowing on the run where it is still a handful.

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
    #: again until the decline is revoked, which means it is suspended rather
    #: than finished, which is why it is not in ``HANDLED``.
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
#:
#: EXACTLY ONE MEMBER, and the test for membership is "can this answer ever
#: change back". ``GONE`` cannot: the file is not there, and no act of the user's
#: brings it back into this row's business. Every other category can, including
#: ``DECLINED``, and that is why ``DECLINED`` is not here.
#:
#: **IT WAS HERE, AND IT BUILT THE ONE WAY DOOR ``stores`` ARGUES AGAINST.** The
#: watermark advances over everything handled and :meth:`WatermarkStore.advance`
#: never moves backward, so a declined row's sequence was passed the moment the
#: decline was recorded, and the next plan filtered it out by sequence before any
#: predicate saw it. Revoking the decline then changed a store nothing read
#: again: R35 says a declined file is never offered again UNTIL THE DECLINE IS
#: REVOKED, and the revocation could not reach the file. The decision stores were
#: chosen over a private ledger precisely so that "there would be no way back"
#: could not happen, and this frozenset had built the same door out of the
#: watermark instead.
#:
#: THE PRICE IS PAID KNOWINGLY. A declined row now holds the watermark at its own
#: sequence for as long as the decline stands, so later runs re-walk the removals
#: above it. That is the same monotonic cost every other non-handled category
#: already carries, and it is bounded cheaply: a declined row short-circuits at
#: the top of :func:`categorize`, before any path is resolved and before any file
#: is touched. Revocability is worth one dictionary lookup per run.
HANDLED: frozenset[Category] = frozenset({Category.GONE})


@dataclass(frozen=True, slots=True)
class ReferenceSet:
    """Every active row's file, by filesystem identity, and what is missing from it.

    ``unmapped``, ``uninspectable`` and ``unanchored`` are the three ways the set
    can be short, and they are counted separately because they send a person to
    three different places: a prefix nothing maps is a rule that is not there, a
    file that will not stat is permissions or a filesystem that is not answering,
    and an anchor that is not there is a rule that IS there and points at nothing.
    The third one is the one that looks like an answer and is not, so it is the
    one that had to stop being folded into ``missing``.
    """

    by_identity: Mapping[FileIdentity, tuple[str, ...]]
    unmapped: tuple[str, ...] = ()
    uninspectable: tuple[str, ...] = ()
    #: Active rows that resolved to a path with no file at it, UNDER an anchor
    #: that is there. Reported rather than blocking: see the module docstring for
    #: why this is evidence rather than the absence of it. Never silent.
    missing: tuple[str, ...] = ()
    #: Active rows whose resolved path is anchored in a directory that does not
    #: exist. The mapping failed, so the row answered nothing, and the run
    #: refuses exactly as it does for a prefix nothing maps.
    unanchored: tuple[str, ...] = ()
    #: The anchors that were not there, deduplicated in first-seen order, so a
    #: refusal can name the two directories rather than the 9,919 rows.
    dead_anchors: tuple[str, ...] = ()
    #: Active rows whose recorded value is not an absolute path at all: a
    #: streaming pseudo-location, or a location spelled in some form this
    #: machine cannot name. Counted rather than dropped without trace, because
    #: "none of these could be a row that references a file" is a claim, and a
    #: claim nobody can see the size of is a claim nobody can check.
    not_a_path: tuple[str, ...] = ()

    @property
    def complete(self) -> bool:
        return not self.unmapped and not self.uninspectable and not self.unanchored

    @property
    def counts(self) -> Mapping[str, int]:
        """Every tally in one mapping, for a log line and for a refusal detail.

        DERIVED here rather than assembled at each reader, because the whole
        defect this field set exists to close was a count that nothing read.
        """
        return {
            "indexed": len(self.by_identity),
            "unmapped": len(self.unmapped),
            "uninspectable": len(self.uninspectable),
            "unanchored": len(self.unanchored),
            "missing": len(self.missing),
            "not_a_path": len(self.not_a_path),
        }


def _anchor_of(
    resolved: locations.ResolvedPath,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
) -> str | None:
    """The directory a resolved path hangs off, or None when nothing named one.

    Two answers only, because the resolver produces a path in exactly two ways.
    A row under the library root is anchored on the root, and a row a rule
    remapped is anchored on that rule's target. Nothing guesses at a parent: the
    anchor is the thing CONFIGURATION named, so an anchor that is not there is a
    statement about the configuration and not about any row that went through it.
    """
    if resolved.resolution is locations.Resolution.UNDER_ROOT:
        return str(root)
    if resolved.resolution is locations.Resolution.REMAPPED and resolved.rule_index is not None:
        return prefix_map[resolved.rule_index].target
    return None  # pragma: no cover - the resolver produces a path no other way


class _Anchors:
    """Whether each anchor is there, asked ONCE per anchor rather than per row.

    A library resolves through a handful of anchors and holds thousands of rows,
    so the naive shape is one extra system call per row for an answer that cannot
    differ between them. Caching also makes the answer CONSISTENT within a run: a
    volume that unmounts halfway through must not make the first half of the
    reference set mean something different from the second half.
    """

    def __init__(self, stat: Stat) -> None:
        self._stat = stat
        self._known: dict[str, bool] = {}

    def present(self, anchor: str | None) -> bool:
        if anchor is None:
            return True
        held = self._known.get(anchor)
        if held is None:
            try:
                self._stat(anchor)
            except (OSError, ValueError):
                held = False
            else:
                held = True
            self._known[anchor] = held
        return held


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
    streamed anything. It IS counted, in ``not_a_path``, because a set of rows
    excused from the proof is worth being able to see the size of.
    """
    found: dict[FileIdentity, list[str]] = {}
    unmapped: list[str] = []
    uninspectable: list[str] = []
    missing: list[str] = []
    unanchored: list[str] = []
    not_a_path: list[str] = []
    dead: dict[str, None] = {}
    rules = list(prefix_map)
    anchors = _Anchors(stat)
    for row in active:
        if row.deleted:
            # The caller partitions before this, so a tombstone arriving here is a
            # caller defect rather than a case. Skipping it keeps the active-row
            # rule true whichever way it arrived: a removed row may never claim a
            # location, which is what makes a tombstone beside a live row read
            # cleanly rather than as a collision.
            continue
        resolved = locations.resolve_recorded_path(row.recorded, root=root, prefix_map=rules)
        if resolved.resolution is locations.Resolution.NOT_A_PATH:
            not_a_path.append(row.content_id)
            continue
        if resolved.path is None:
            unmapped.append(row.content_id)
            continue
        try:
            stats = stat(resolved.path)
        except FileNotFoundError:
            anchor = _anchor_of(resolved, root=root, prefix_map=rules)
            if anchors.present(anchor):
                missing.append(row.content_id)
            else:
                unanchored.append(row.content_id)
                dead[str(anchor)] = None
            continue
        except OSError:
            uninspectable.append(row.content_id)
            continue
        except ValueError:
            # A recorded path holding a NUL byte. ``os.stat`` raises ValueError
            # for that rather than OSError, so an except clause naming only the
            # filesystem's errors lets it out of the module as an internal defect
            # and the remedy it should have carried is discarded at the process
            # boundary (S4). It is uninspectable for the same reason a
            # permission failure is: the row answered nothing.
            uninspectable.append(row.content_id)
            continue
        found.setdefault(FileIdentity.of(stats), []).append(row.content_id)
    return ReferenceSet(
        by_identity={identity: tuple(ids) for identity, ids in found.items()},
        unmapped=tuple(unmapped),
        uninspectable=tuple(uninspectable),
        missing=tuple(missing),
        unanchored=tuple(unanchored),
        dead_anchors=tuple(dead),
        not_a_path=tuple(not_a_path),
    )


def assert_complete(references: ReferenceSet) -> None:
    """Refuse the run unless every active row contributed an answer.

    OFFERS NOTHING RATHER THAN OFFERING LESS. A run that dropped the unresolvable
    rows and carried on would still present candidates, and every one of those
    candidates would carry a proof with a hole in it exactly the size of the rows
    that were dropped. The user cannot see the hole, and the thing on the other
    side of it is their music.

    THE DEAD ANCHORS ARE NAMED FIRST in the sentence when there are any, because
    that is the shape a person can act on: "this directory is not there" is one
    correction, and "8,554 rows could not be proved" is a search.
    """
    if references.complete:
        return
    anchored = (
        f"{len(references.unanchored)} resolve under a directory that does not "
        f"exist ({', '.join(references.dead_anchors)}), which is the volume "
        f"prefix map failing rather than an answer about any of those rows, "
        if references.unanchored
        else ""
    )
    raise refuse(
        "deletion-reference-set-incomplete",
        f"{len(references.unmapped)} active rows record a location this machine "
        f"cannot resolve, {len(references.uninspectable)} resolve to files "
        f"that could not be inspected, and {anchored}so the proof that a removed "
        f"file is unreferenced would be a proof about the rows that happened to "
        f"answer; nothing is offered this run",
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.RUN,
        origin=("deletion.candidates",),
        detail={
            **references.counts,
            "dead_anchors": list(references.dead_anchors),
            "unmapped_rows": list(references.unmapped[:20]),
            "uninspectable_rows": list(references.uninspectable[:20]),
            "unanchored_rows": list(references.unanchored[:20]),
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

    THE ANCHOR SPLIT MATTERS MORE HERE THAN IN THE REFERENCE SET. A removed row
    whose file is not there is ``GONE``, which is finished business, so the
    watermark passes over it and it is never presented again. A dead prefix rule
    makes EVERY removed row that goes through it look gone, so one wrong
    character would quietly mark a library's whole removal history as dealt with,
    and fixing the rule afterwards would not bring any of it back.
    """
    out: list[Candidate] = []
    rules = list(prefix_map)
    anchors = _Anchors(stat)
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
        resolved = locations.resolve_recorded_path(row.recorded, root=root, prefix_map=rules)
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
            anchor = _anchor_of(resolved, root=root, prefix_map=rules)
            if anchors.present(anchor):
                out.append(Candidate(row=row, category=Category.GONE, resolved=resolved.path))
            else:
                out.append(
                    Candidate(
                        row=row,
                        category=Category.UNRESOLVED,
                        resolved=resolved.path,
                        problem=(
                            f"{anchor} does not exist, so this path establishes "
                            f"nothing about the row: what is proved absent is the "
                            f"directory the volume prefix map named, not the file"
                        ),
                    )
                )
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
        except ValueError as exc:
            # See ``reference_set``: a NUL byte in a recorded path is a ValueError
            # out of ``os.stat`` and would otherwise pass both handlers above and
            # reach the command line as an internal defect rather than a refusal.
            out.append(
                Candidate(
                    row=row,
                    category=Category.UNRESOLVED,
                    problem=f"the recorded location cannot be used as a path: {exc}",
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
