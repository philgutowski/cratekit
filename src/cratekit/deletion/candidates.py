"""The proof that a file is unreferenced, and the answers a candidate can get.

**THE 144 FILE LOSS IS WHY.** A ported orphan sweep compared walked disk paths
against decoded rekordbox locations with ``==``; two composition forms of one
accented name are different strings, and 144 referenced files were deleted.

R37: **the filesystem decides.** A candidate is deletable only when its device
and inode match no active row's resolved file and its size matches the size the
removed row recorded. That covers case only and composition form differences, hard
and symbolic links, and a path later reclaimed by a different track, without
knowing about any of them.

**THE REFERENCE SET MUST BE COMPLETE FIRST.** An active row that resolves nowhere,
or cannot be inspected, contributes no inode, so the proof would pass on absence
of evidence. :func:`assert_complete` refuses the whole run instead. An active row
whose path simply does not exist is an ANSWER (it references no existing file)
and does not refuse; a rekordbox streaming row (U243) names no file either, see
:func:`_streaming`.

**THE ANCHOR.** ``FileNotFoundError`` under a directory that is not there is the
MAPPING failing, not an answer about the row. So the directory a path hangs off,
the library root or the rule's target, is checked once per anchor, and a row
under a missing one is ``unanchored`` and refuses naming it. The same split runs
in :func:`categorize`, where ``GONE`` is finished business.

**WHAT IT DOES NOT CATCH.** An anchor that exists but is the WRONG directory.
``run._assert_library_is_still`` refuses one on another disk by volume identity;
one on the right disk gets through, recorded in the residual "Five findings the
U24 review accepted, and the reason each stands", because every rule that
catches it needs a threshold that also refuses ordinary libraries.
``suspect_anchors`` is the signal without a threshold, per anchor. ``missing`` is
never silent: counted, reported and logged.

Layer note: MODULES. Pure apart from one injected ``stat``.
"""

from __future__ import annotations

import functools
import os
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from cratekit.core import locations
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.deletion.library import RemovedRow
from cratekit.write import trees

#: The stat this module uses. ``os.stat`` FOLLOWS symbolic links, so a row
#: recorded against a link names the inode the link points at.
Stat = Callable[[str], os.stat_result]


@dataclass(frozen=True, slots=True)
class FileIdentity:
    """What the filesystem calls one file: the pair, since inodes repeat across devices."""

    device: int
    inode: int

    @classmethod
    def of(cls, stats: os.stat_result) -> FileIdentity:
        return cls(device=stats.st_dev, inode=stats.st_ino)


class Category(StrEnum):
    """What this run decided about one removed row. Explicit, and closed.

    Every category but ``DELETABLE`` means no file moves; they stay apart because
    the act that clears each differs.
    """

    #: Proved unreferenced and proved to be the file the row described.
    DELETABLE = "deletable"
    #: The recorded path maps nowhere, is not a path, or could not be inspected.
    #: AE16: no file moves and the watermark does not treat it as handled.
    UNRESOLVED = "unresolved"
    #: The file is also the file an ACTIVE row points at, by inode.
    COLLIDES_WITH_ACTIVE_ROW = "collides-with-active-row"
    #: The file is not the size the row recorded, or the row recorded none.
    SIZE_MISMATCH = "size-mismatch"
    #: A playlist on this volume still points at it.
    STILL_REFERENCED = "still-referenced"
    #: The file is already gone. Finished business (in :data:`HANDLED`), which
    #: makes an interrupted run resume rather than re-offer.
    #:
    #: Only because the move and the tombstone are one act:
    #: ``run._record_or_put_it_back`` puts the file back on every failure the
    #: process can observe, and a confirmed GONE row with no tombstone is
    #: settled by ``run._settle_a_confirmed_absence``. A SIGKILL or power loss
    #: between rename and record still loses the tombstone, never the music;
    #: the residual "A SIGKILL between the move and the tombstone still loses
    #: the record, and no handler can catch it" holds the repair.
    GONE = "gone"
    #: A person said to keep it (R35); suspended until revoked, so not handled.
    DECLINED = "declined"
    #: Neither artist nor title, so R36's tombstone could name nothing. Checked
    #: before anything resolves, not between the move and the record.
    UNIDENTIFIABLE = "unidentifiable"
    #: Another removed row produces the same identity with a different ISRC: two
    #: recordings, so a tombstone for either suppresses the other. A convergence
    #: (one recording, one code) is required and stays deletable; see the
    #: residual "The Subtitle vocabulary's false negatives collide, and the ISRC
    #: tells a collision from a convergence".
    AMBIGUOUS_VERSION = "ambiguous-version"


#: The categories the watermark may pass over: those that can never change back.
#: Derived in one place so an unclassified new category joins neither side by
#: accident. ``DECLINED`` is not here: passing a declined row's sequence would
#: put it beyond the reach of its revocation (R35), and the cost of holding it is
#: one lookup per run, since a declined row short circuits :func:`categorize`.
HANDLED: frozenset[Category] = frozenset({Category.GONE})


@dataclass(frozen=True, slots=True)
class ReferenceSet:
    """Every active row's file, by filesystem identity, and what is missing from it.

    ``unmapped`` (no rule), ``uninspectable`` (will not stat) and ``unanchored``
    (a rule pointing at nothing) are the ways it is short, counted apart because
    each sends a person somewhere different.
    """

    by_identity: Mapping[FileIdentity, tuple[str, ...]]
    unmapped: tuple[str, ...] = ()
    uninspectable: tuple[str, ...] = ()
    #: Rows resolved to no file under an anchor that IS there. Evidence, not a
    #: refusal; never silent.
    missing: tuple[str, ...] = ()
    #: Rows anchored in a directory that does not exist. Refuses.
    unanchored: tuple[str, ...] = ()
    #: The missing anchors, first seen order, so a refusal names directories.
    dead_anchors: tuple[str, ...] = ()
    #: Rows whose recorded value is not an absolute path (a streaming pseudo
    #: location). Excused, and counted so the excusal has a visible size.
    not_a_path: tuple[str, ...] = ()
    #: Anchors that exist, indexed nothing, and had a row go missing. A signal,
    #: not a refusal: a wrong directory and one moved file look the same here.
    suspect_anchors: tuple[str, ...] = ()
    #: Anchors whose existence changed during the walk. Refuses.
    unstable_anchors: tuple[str, ...] = ()
    #: Rows in ``not_a_path`` that ARE paths spelled unnameably (:func:`_unnameable`).
    #: Refuses.
    unnameable: tuple[str, ...] = ()
    #: Rows recorded as a rekordbox streaming location (U243), ``/v4/catalog/tracks/<id>/``
    #: with nothing there. Excused as ``not_a_path`` is; see :func:`_streaming`.
    streaming: tuple[str, ...] = ()
    #: Each ``unmapped`` row's leading prefix and its count, most first, so the
    #: refusal names the rule to write.
    unmapped_prefixes: tuple[tuple[str, int], ...] = ()

    @property
    def ignored(self) -> int:
        """How many active rows the proof excused as referencing no local file."""
        return len(self.not_a_path) + len(self.streaming)

    @property
    def complete(self) -> bool:
        return not (
            self.unmapped
            or self.uninspectable
            or self.unanchored
            or self.unstable_anchors
            or self.unnameable
        )

    @property
    def counts(self) -> Mapping[str, int]:
        """Every ROW tally, for a log line and a refusal detail; anchors travel apart."""
        tallied = (
            "unmapped",
            "uninspectable",
            "unanchored",
            "missing",
            "not_a_path",
            "unnameable",
            "streaming",
        )
        return {
            "indexed": len(self.by_identity),
            **{name: len(getattr(self, name)) for name in tallied},
        }


#: A recorded value opening with a drive letter: absolutely a path, and one
#: ``resolve_recorded_path`` cannot name.
_DRIVE_LETTER = re.compile(r"^[A-Za-z]:[\\/]")

#: The ONE scheme that names a file. Not ``locations.looks_like_location``, which
#: is true of every streaming pseudo location. Case insensitive, anchored.
_FILE_LOCATION = re.compile(r"^file://", re.IGNORECASE)

#: The location rekordbox records for a track it streams from a store (U243):
#: letters and digits only, so never a file name with an extension, matched
#: whole with ``\Z`` (``$`` would accept a trailing newline).
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")


def _streaming(recorded: str, stat: Stat) -> bool:
    """Whether an unmapped row is a rekordbox streaming row, which names no file.

    TWO FACTS, EITHER ALONE NOT ENOUGH: the exact spelling, and
    ``FileNotFoundError`` at it. Anything else keeps the row unmapped. A renamed
    volume mounts under a volume directory, never at ``/v4``. Asked only of a row
    no rule placed; a rule mapping ``/v4`` wins.
    """
    text = str(recorded)
    if not _STREAMING_LOCATION.match(text):
        return False
    try:
        stat(text)
    except FileNotFoundError:
        return True
    except (OSError, ValueError):
        return False
    return False


def _unnameable(recorded: str) -> bool:
    """Whether a row excused as "not a path" is in fact a path, unnameably spelled.

    The excusal is sound only for rows that reference NO file. A drive letter
    or a ``file://`` location names a real file this build cannot decode, so
    excusing it empties the proof. Any other scheme names a service and stays
    excused. One ``^`` in each pattern, applied with ``search``.
    """
    text = str(recorded).strip()
    return bool(_DRIVE_LETTER.search(text)) or bool(_FILE_LOCATION.search(text))


def _anchor_text(value: str) -> str:
    """ONE spelling for an anchor, whichever side of the map it came from.

    ``PrefixRule`` NFC folds its target and the root arrives raw; on ext4 or
    exFAT two spellings of one directory would differ. A rule onto ``/`` stores
    the empty string, which is the root, not nowhere.
    """
    return locations.norm_for_compare(value).rstrip("/") or "/"


def _anchor_of(
    resolved: locations.ResolvedPath,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule],
) -> str | None:
    """The directory CONFIGURATION named for a resolved path: the root, or the rule's target."""
    if resolved.resolution is locations.Resolution.UNDER_ROOT:
        return _anchor_text(str(root))
    if resolved.resolution is locations.Resolution.REMAPPED and resolved.rule_index is not None:
        return _anchor_text(prefix_map[resolved.rule_index].target)
    return None  # pragma: no cover - the resolver produces a path no other way


class _Anchors:
    """Whether each anchor is there, asked ONCE per anchor, consistently within a run.

    The unsafe cached answer is "present": a volume ejected after its first row
    leaves later rows reading missing. So :meth:`changed` re-asks at the end and
    the caller refuses on any anchor whose answer moved.
    """

    def __init__(self, stat: Stat) -> None:
        self._stat = stat
        self._known: dict[str, bool] = {}

    def _ask(self, anchor: str) -> bool:
        try:
            self._stat(anchor)
        except (OSError, ValueError):
            return False
        return True

    def present(self, anchor: str | None) -> bool:
        if anchor is None:
            return True
        held = self._known.get(anchor)
        if held is None:
            held = self._ask(anchor)
            self._known[anchor] = held
        return held

    def changed(self) -> tuple[str, ...]:
        """Anchors whose answer, in either direction, is not the one the run was built on."""
        return tuple(anchor for anchor, held in self._known.items() if self._ask(anchor) != held)


def reference_set(
    active: Iterable[trees.ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
    stat: Stat = os.stat,
) -> ReferenceSet:
    """Index every active row by the file it actually points at.

    Through the shared resolver and the prefix map: a naive resolver resolved 0
    of 9,919 rows and would declare every file unreferenced. A row that is not a
    path is excused and counted in ``not_a_path``, unless :func:`_unnameable`
    says it is a real path; a streaming row is excused by :func:`_streaming`.
    Every other unmapped row refuses.
    """
    found: dict[FileIdentity, list[str]] = {}
    unmapped, uninspectable, missing, unanchored = [], [], [], []
    not_a_path, unnameable, streaming = [], [], []
    unmapped_under: dict[str, int] = {}
    dead: dict[str, None] = {}
    indexed_under: dict[str, int] = {}
    missing_under: dict[str, int] = {}
    rules = list(prefix_map)
    anchors = _Anchors(stat)
    for row in active:
        if row.deleted:
            # A caller defect, skipped so a removed row never claims a location.
            continue
        resolved = locations.resolve_recorded_path(row.recorded, root=root, prefix_map=rules)
        if resolved.resolution is locations.Resolution.NOT_A_PATH:
            (unnameable if _unnameable(row.recorded) else not_a_path).append(row.content_id)
            continue
        if resolved.path is None:
            if _streaming(row.recorded, stat):
                streaming.append(row.content_id)
                continue
            unmapped.append(row.content_id)
            prefix = resolved.prefix or "an unreadable prefix"
            unmapped_under[prefix] = unmapped_under.get(prefix, 0) + 1
            continue
        anchor = _anchor_of(resolved, root=root, prefix_map=rules)
        try:
            stats = stat(resolved.path)
        except FileNotFoundError:
            if anchors.present(anchor):
                missing.append(row.content_id)
                if anchor is not None:
                    missing_under[anchor] = missing_under.get(anchor, 0) + 1
            else:
                unanchored.append(row.content_id)
                dead[str(anchor)] = None
            continue
        except (OSError, ValueError):
            # ValueError is a NUL byte in the path, uninspectable as a permission
            # failure is, rather than an internal defect (S4).
            uninspectable.append(row.content_id)
            continue
        found.setdefault(FileIdentity.of(stats), []).append(row.content_id)
        if anchor is not None:
            indexed_under[anchor] = indexed_under.get(anchor, 0) + 1
    return ReferenceSet(
        by_identity={identity: tuple(ids) for identity, ids in found.items()},
        unmapped=tuple(unmapped),
        uninspectable=tuple(uninspectable),
        missing=tuple(missing),
        unanchored=tuple(unanchored),
        dead_anchors=tuple(dead),
        not_a_path=tuple(not_a_path),
        unnameable=tuple(unnameable),
        streaming=tuple(streaming),
        # Most rows first, then by prefix, so the order is the same every run.
        unmapped_prefixes=tuple(
            sorted(unmapped_under.items(), key=lambda pair: (-pair[1], pair[0]))
        ),
        suspect_anchors=tuple(anchor for anchor in missing_under if not indexed_under.get(anchor)),
        unstable_anchors=anchors.changed(),
    )


#: How many unmapped prefixes a refusal names before it counts the rest.
_NAMED_PREFIXES = 5

#: The step both refusals of a volume that moved mid walk give.
_REMOUNT_AND_RETRY = "leave the library volume and every mapped volume mounted, then run this again"


def assert_complete(references: ReferenceSet) -> None:
    """Refuse the run unless every active row contributed an answer.

    OFFERS NOTHING RATHER THAN LESS: every candidate would carry a proof with a
    hole the size of the dropped rows. The shapes a person can act on are named
    first: unnameable rows, an unstable anchor, then dead anchors and unmapped
    prefixes with the rule that would resolve them (U243).
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
    if references.unnameable:
        # Nothing the user can mount or remap answers this one.
        raise refuse(
            "deletion-reference-set-incomplete",
            f"{len(references.unnameable)} active rows record a location that is a path this build "
            "cannot name, a drive letter or a file:// location rather than an absolute path; "
            "those rows were excused from the proof as though they referenced no file at all, so "
            "a removed file would be shown unreferenced against a reference set they are missing "
            "from; nothing is offered this run",
            steps=(
                "run this on the machine and platform the library was recorded "
                "on, or report this with the recorded locations below, because "
                "no volume prefix rule can spell a path this build cannot read",
            ),
            scope=Scope.RUN,
            origin=("deletion.candidates",),
            detail={**references.counts, "unnameable_rows": list(references.unnameable[:20])},
        )
    if references.unstable_anchors:
        # Nothing is misconfigured: a volume came or went mid walk; run it again.
        raise refuse(
            "deletion-reference-set-incomplete",
            f"the directory at {', '.join(references.unstable_anchors)} was there for part of this "
            "run and not for the rest, so the reference set was assembled against two different "
            "filesystems and proves nothing about either; nothing is offered this run",
            steps=(_REMOUNT_AND_RETRY,),
            scope=Scope.RUN,
            origin=("deletion.candidates",),
            detail={**references.counts, "unstable_anchors": list(references.unstable_anchors)},
        )
    named = references.unmapped_prefixes[:_NAMED_PREFIXES]
    under = ", ".join(f"{count} under {prefix}" for prefix, count in named)
    more = len(references.unmapped_prefixes) - len(named)
    if more > 0:
        under += f", and {more} other prefix{'es' if more > 1 else ''}"
    raise refuse(
        "deletion-reference-set-incomplete",
        f"{len(references.unmapped)} active rows record a location this machine "
        f"cannot resolve{f' ({under})' if under else ''}, "
        f"{len(references.uninspectable)} resolve to files "
        f"that could not be inspected, and {anchored}so the proof that a removed "
        f"file is unreferenced would be a proof about the rows that happened to "
        f"answer; nothing is offered this run",
        # The commonest case is a two drive library with one unplugged, one act
        # from a run that works, so the act is spelled out.
        steps=(
            *(
                (
                    f"mount the volume holding {', '.join(references.dead_anchors)}, or correct "
                    "the volume prefix rule that points at it, then run this again",
                )
                if references.dead_anchors
                else ()
            ),
            # ONE ENTRY TO ADD, never an assignment of the list, which a
            # configuration already holding a rule would refuse.
            *(
                f'add {{ from = "{prefix}", to = "<where those files are now>" }} '
                f"to the library.location_prefix_map list in the configuration "
                f"for the {count} row(s) under {prefix}, with from equal to to "
                f"when the files are exactly where the rows say, then run this "
                f"again"
                for prefix, count in named
            ),
        ),
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.RUN,
        origin=("deletion.candidates",),
        detail={
            **references.counts,
            "unmapped_prefixes": dict(references.unmapped_prefixes),
            "dead_anchors": list(references.dead_anchors),
            "unmapped_rows": list(references.unmapped[:20]),
            "uninspectable_rows": list(references.uninspectable[:20]),
            "unanchored_rows": list(references.unanchored[:20]),
        },
    )


@dataclass(frozen=True, slots=True)
class Candidate:
    """One removed row, the answer this run reached, and the evidence for it.

    ``problem`` is a sentence and is never branched on; ``category`` is.
    """

    row: RemovedRow
    category: Category
    resolved: str | None = None
    identity: FileIdentity | None = None
    observed_size: int | None = None
    collides_with: tuple[str, ...] = ()
    problem: str = ""
    #: The directory configuration named, carried only when the file was not
    #: there, so ``run._the_anchor_proved_nothing`` can tell a deletion from an
    #: unmounted drive.
    anchor: str | None = None

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
    ambiguous: Callable[[RemovedRow], bool] = lambda _row: False,
    stat: Stat = os.stat,
) -> tuple[Candidate, ...]:
    """Answer every removed row, in the order R37 states its assertions.

    The order only decides which category a row failing several is reported
    under. A dead prefix rule would make every row through it look ``GONE``,
    which is finished business, so a missing anchor answers ``UNRESOLVED``; and
    the anchor cache is re-asked at the end and a moved answer refuses, since a
    drive dropping mid walk would otherwise retire rows off a stale "present".
    An existing but EMPTY mount point passes the anchor test, so the anchor is
    carried out on a ``GONE`` answer for the caller, which holds the
    counter evidence.
    """
    rules = list(prefix_map)
    anchors = _Anchors(stat)

    def answer(row: RemovedRow) -> Candidate:
        # Identifiability BEFORE the decline, whose predicate derives an
        # identifier from the row.
        if not identifiable(row):
            return Candidate(
                row=row,
                category=Category.UNIDENTIFIABLE,
                problem=(
                    "the row cannot be identified: R36's tombstone needs an artist or a title to "
                    "name the version this deletion suppresses, and the review item needs the "
                    "row's own identifier to be answerable"
                ),
            )
        if declined(row):
            return Candidate(row=row, category=Category.DECLINED)
        if ambiguous(row):
            return Candidate(
                row=row,
                category=Category.AMBIGUOUS_VERSION,
                problem=(
                    "another removed row produces the same version identity as this one and "
                    "carries a different ISRC, so the two are two recordings rather than one "
                    "filed twice; a tombstone for either would suppress the other"
                ),
            )
        resolved = locations.resolve_recorded_path(row.recorded, root=root, prefix_map=rules)
        if resolved.path is None:
            return Candidate(
                row=row,
                category=Category.UNRESOLVED,
                problem=(
                    "the recorded location is not a path this machine can name"
                    if resolved.resolution is locations.Resolution.NOT_A_PATH
                    else f"no volume prefix rule maps {resolved.prefix!r}"
                ),
            )
        try:
            stats = stat(resolved.path)
        except FileNotFoundError:
            anchor = _anchor_of(resolved, root=root, prefix_map=rules)
            if anchors.present(anchor):
                return Candidate(
                    row=row, category=Category.GONE, resolved=resolved.path, anchor=anchor
                )
            return Candidate(
                row=row,
                category=Category.UNRESOLVED,
                resolved=resolved.path,
                anchor=anchor,
                problem=(
                    f"{anchor} does not exist, so this path establishes "
                    f"nothing about the row: what is proved absent is the "
                    f"directory the volume prefix map named, not the file"
                ),
            )
        except OSError as exc:
            return Candidate(
                row=row,
                category=Category.UNRESOLVED,
                resolved=resolved.path,
                problem=f"the file could not be inspected: {exc}",
            )
        except ValueError as exc:
            # A NUL byte, see ``reference_set``.
            return Candidate(
                row=row,
                category=Category.UNRESOLVED,
                problem=f"the recorded location cannot be used as a path: {exc}",
            )
        identity = FileIdentity.of(stats)
        found = functools.partial(
            Candidate,
            row=row,
            resolved=resolved.path,
            identity=identity,
            observed_size=stats.st_size,
        )
        claimed = references.by_identity.get(identity, ())
        if claimed:
            return found(
                category=Category.COLLIDES_WITH_ACTIVE_ROW,
                collides_with=claimed,
                problem=(f"the same file is the file active row(s) {', '.join(claimed)} point at"),
            )
        if row.size is None or int(stats.st_size) != int(row.size):
            return found(
                category=Category.SIZE_MISMATCH,
                problem=(
                    "the removed row recorded no size, so nothing proves this is the file it named"
                    if row.size is None
                    else f"the row recorded {row.size} bytes and the file holds {stats.st_size}"
                ),
            )
        if row.content_id in referenced:
            return found(
                category=Category.STILL_REFERENCED,
                problem="a playlist on this volume still points at this track",
            )
        return found(category=Category.DELETABLE)

    out = [answer(row) for row in removed]
    moved = anchors.changed()
    if moved:
        raise refuse(
            "deletion-evidence-incomplete",
            f"the directory at {', '.join(moved)} was there for part of this walk and not for the "
            "rest, so the removals answered before it moved and the ones answered after describe "
            "two different filesystems; a row answered off the stale half reads as already "
            "deleted, which is finished business, and the watermark would retire it without "
            "anybody being asked",
            steps=(_REMOUNT_AND_RETRY,),
            scope=Scope.RUN,
            origin=("deletion.candidates",),
            detail={"unstable_anchors": list(moved)},
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
    stat: Stat = os.stat,
) -> Candidate:
    """Re-run every assertion THAT CAN CHANGE for ONE candidate, before its move (R37).

    THE SAME CODE PATH: :func:`categorize` over one row, so the preview and the
    write cannot disagree. ``identifiable`` and ``ambiguous`` are not accepted:
    both are functions of the plan the caller just rebuilt, which called this
    row deletable, so neither could alter an answer. ``declined`` is a fresh
    store read and can.
    """
    answered = categorize(
        [candidate.row],
        references,
        root=root,
        prefix_map=prefix_map,
        referenced=referenced,
        declined=declined,
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
