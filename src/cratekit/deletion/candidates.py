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
refuses loudly, while adding a WRONG one proceeds silently. A target with one
character wrong in it and a mapped volume nobody plugged in both land there, and
both end the same way, with every active row counted as a missing file, an EMPTY
reference set, ``complete`` true, and every removed row proved unreferenced
against nothing at all.

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

**WHAT THE ANCHOR CHECK DOES NOT CATCH, STATED BECAUSE THE FIRST VERSION OF THIS
PARAGRAPH CLAIMED MORE THAN THE CODE DELIVERS.** The check asks whether the
anchor IS THERE. It cannot ask whether the anchor is RIGHT. A rule whose target
exists and is the wrong directory produces the original defect in full: every row
through it is missing, nothing is indexed under it, ``complete`` is true, and a
candidate that would have collided with an active row is judged deletable and
trashed. A drive somebody renamed only reaches the refusing branch while nothing
else is mounted at the old name; mount anything there and it does not. This is
recorded rather than fixed, and the residual finding
"Five findings the U24 review accepted, and the reason each stands"
in ``docs/residual-findings.md`` carries the
reproduction and the reasoning, which is short: every rule that catches it needs
a threshold, and every threshold that catches the dangerous case also refuses the
ordinary one, which is a rule matching a handful of rows whose files the user
moved by hand.

What IS delivered against it is a signal with no threshold in it.
``suspect_anchors`` names every anchor that exists, contributed no filesystem
identity at all, and had at least one row go missing under it. That is per
ANCHOR rather than per run, which is what the previous all-or-nothing version got
wrong: one unrelated active row resolving anywhere in the library silenced it
entirely.

**AND ``missing`` IS NEVER SILENT, even where it correctly does not refuse.** It
is counted, it rides on the reference set, it is reported in the refusal detail,
and the pass logs it, because "these active rows point at files that are not
there" is worth knowing on the run where it is still a handful.

Layer note: MODULES. Pure apart from one injected ``stat``, so every branch is
reachable without a filesystem shaped for it.
"""

from __future__ import annotations

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
    #: watermark. Finished business, which is what makes a run that crashed
    #: mid-trash resume rather than re-offer.
    #:
    #: **IT IS ONLY FINISHED BUSINESS BECAUSE THE MOVE AND THE TOMBSTONE ARE ONE
    #: ACT, AND THIS SENTENCE USED TO SAY "either way" AS IF THEY WERE NOT.**
    #: This category is in :data:`HANDLED`, so the watermark passes over the row
    #: and it is never offered again. That is correct for a file whose deletion
    #: was RECORDED and wrong for one whose deletion was not: a run that trashed
    #: a file and then failed to write its tombstone would leave the file in the
    #: Trash, the version un-suppressed, and this category quietly retiring the
    #: only row that could ever have said so.
    #:
    #: **WHAT ACTUALLY PROTECTS THE INVARIANT, STATED AS THE PARTIAL GUARANTEE IT
    #: IS.** ``run._record_or_put_it_back`` puts the file back whenever the
    #: tombstone cannot be written, and it catches ``BaseException``, so it covers
    #: every failure THIS PROCESS CAN OBSERVE: a store refusal, a full disk, a
    #: lock it cannot take, a Ctrl-C, and the ``SystemExit`` a SIGTERM handler
    #: raises. It cannot cover what the process never observes. A SIGKILL or a
    #: power loss in the window between the rename and the record leaves the file
    #: in the Trash with no tombstone. NO HANDLER CLOSES THAT WINDOW, and
    #: claiming the state is unreachable would be claiming something no
    #: in-process code can deliver.
    #:
    #: **WHAT THE NEXT RUN DOES ABOUT IT HAS CHANGED, AND IT IS THE HALF THAT WAS
    #: ACTUALLY REACHABLE.** This category used to retire the row silently, so
    #: the suppression was lost with nothing recording it. A move only ever
    #: happens after a person confirms, and a verdict is durable, so the next run
    #: finds a CONFIRMED row whose file is absent with no tombstone and settles it
    #: through ``run._settle_a_confirmed_absence``, which writes the record the
    #: deletion owes. The interrupted deletion therefore completes rather than
    #: disappearing, for as long as the confirmation is still in the queue.
    #:
    #: Three things bound the cost rather than remove it. The window is one
    #: rename plus one store write per candidate, so it is small and it is not a
    #: long-running operation. The file is in the TRASH rather than unlinked, so
    #: it is still the user's file and recoverable by hand. And the tombstone is
    #: the thing lost, not the music: the version becomes re-acquirable, which is
    #: the under-suppression direction this package calls the milder one. The
    #: durable repair is a write-ahead intent, the record written as pending
    #: BEFORE the rename and settled after, which is a change to the store
    #: contract rather than to this category. It is recorded as the residual
    #: finding "A SIGKILL between the move and the tombstone still loses the record, and no handler can catch it".
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
    #: The tombstone this deletion would write is addressed by an identity a
    #: SECOND removed row also produces, and the two rows carry two different
    #: ISRCs, so they are two recordings rather than one recording filed twice.
    #: Deleting either would suppress the other, which is over-suppression: the
    #: user silently stops being able to acquire a version they never deleted.
    #:
    #: **IT IS NOT THE SAME AS A CONVERGENCE, WHICH IS REQUIRED.** ``Strobe``
    #: with a remixer column against ``Strobe (Michael Woods Remix)`` with none
    #: is one version filed under two conventions, and composition exists to give
    #: those two rows ONE identity. Both shapes are two rows on one identity and
    #: nothing about the identity separates them, which is what the residual
    #: finding "The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence"
    #: recorded as unresolvable. The ISRC separates them, and the rows already
    #: carry it.
    AMBIGUOUS_VERSION = "ambiguous-version"


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
    #: Anchors that ARE there and contributed no filesystem identity at all while
    #: at least one row through them was missing. Does not refuse, and the reason
    #: it does not is written out in the module docstring: the same shape is a
    #: prefix rule pointing at the wrong existing directory, which is dangerous,
    #: and a rule that legitimately matches one row whose file the user moved by
    #: hand, which is ordinary. Nothing here can tell those apart, so this is the
    #: loudest honest signal rather than a refusal with a threshold in it.
    suspect_anchors: tuple[str, ...] = ()
    #: Anchors whose existence answer was different at the end of the walk from
    #: the one the walk was built on: a volume ejected or mounted underneath a
    #: run in progress. Refuses, because half this set describes one filesystem
    #: and half describes another.
    unstable_anchors: tuple[str, ...] = ()
    #: The rows inside ``not_a_path`` that ARE a path, spelled in a form this
    #: build cannot name. Refuses. See :func:`_unnameable`: the excusal that
    #: ``not_a_path`` performs is only sound for a row that references no file at
    #: all, and reading a real path as one of those is how the proof comes back
    #: empty and every candidate passes it.
    unnameable: tuple[str, ...] = ()

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
        """Every ROW tally in one mapping, for a log line and for a refusal detail.

        DERIVED here rather than assembled at each reader, because the whole
        defect this field set exists to close was a count that nothing read.

        Rows only. The three anchor tuples are named directories rather than
        tallies and travel beside this under their own keys, so nothing has to
        guess whether ``dead_anchors`` in a detail mapping is a number or a list.
        """
        return {
            "indexed": len(self.by_identity),
            "unmapped": len(self.unmapped),
            "uninspectable": len(self.uninspectable),
            "unanchored": len(self.unanchored),
            "missing": len(self.missing),
            "not_a_path": len(self.not_a_path),
            "unnameable": len(self.unnameable),
        }


#: A recorded value opening with a drive letter, the one path shape that is
#: absolutely a path and that ``resolve_recorded_path`` cannot name. It tests for
#: a leading ``/`` and returns NOT_A_PATH for everything else, which is right on
#: macOS, where the rows that fail it are streaming pseudo-locations referencing
#: no file. On Windows every ``C:\`` row fails it too.
_DRIVE_LETTER = re.compile(r"^[A-Za-z]:[\\/]")

#: The ONE scheme that names a file, and therefore the only scheme whose rows are
#: paths rather than rows referencing no file. Tested as its own pattern rather
#: than through ``locations.looks_like_location``, which is ``"://" in value`` and
#: is true of every streaming pseudo-location there is. Case-insensitive because a
#: URL scheme is case-insensitive and an upper-case spelling names a file just as
#: surely; anchored, because a title containing the text ``file://`` is not a
#: location.
_FILE_LOCATION = re.compile(r"^file://", re.IGNORECASE)


def _unnameable(recorded: str) -> bool:
    """Whether a row excused as "not a path" is in fact a path, unnameably spelled.

    **THE EXCUSAL IS SOUND FOR ONE REASON AND ONE ONLY**, which the reference
    set's docstring states: a streamed track has a pseudo-location rather than a
    file, so it cannot be the row that references a file, and counting it against
    completeness would refuse the whole run for any library that has ever
    streamed anything. That argument is about rows THAT REFERENCE NO FILE. It
    does not extend one inch to a row that references a file perfectly well and
    is written in a form this build does not decode, and the difference is not
    cosmetic: such a row contributes no filesystem identity, so a candidate that
    would have collided with it is proved unreferenced against nothing.

    Two shapes reach that state today and both are recognised here rather than in
    ``core.locations``, which belongs to another unit and is not rewritten from
    inside this one:

    * a DRIVE LETTER. ``resolve_recorded_path`` requires a leading ``/``, so on
      Windows every row in the collection is excused, the reference set comes
      back empty, ``complete`` is true, and every removed row passes a proof
      about nothing. ``core.locations`` already ships a Windows separator seam,
      so the platform is anticipated elsewhere in the same module.
    * a ``file://`` LOCATION. ``core.locations.location_to_path`` is the decoder
      built for exactly the two spellings rekordbox has used, and neither this
      module nor ``library.read_collection`` routes a recorded value through it,
      so a percent-encoded location is excused the same way.

    REFUSING IS THE NARROW ANSWER RATHER THAN THE BROAD ONE, AND IT USED TO BE
    THE BROAD ONE. The second test asked ``locations.looks_like_location``, which
    is ``"://" in value`` and therefore true of ``tidal://track/123``,
    ``spotify://track/abc`` and ``https://api.tidal.com/v1/tracks/123`` as
    readily as of ``file://``. Every one of those is a row that references NO
    file, which is the exact case the excusal exists for, so the whole
    destructive verb refused for any library holding one streamed row spelled as
    a URL, with a remedy, "run this on the machine the library was recorded on",
    that a streamed row can never satisfy and no configuration can clear.

    The scheme is what carries the meaning: ``file`` names a file and every other
    scheme names a service. So the test is the ``file`` scheme by name, and a
    pseudo-location under any other scheme stays excused exactly as it was. A
    destructive verb proving a file unreferenced against an empty reference set
    is the worst shape this unit has, and this is the half of it U24 can close
    from inside its own package, without taking the feature away from anybody who
    has ever streamed anything.

    THE ANCHOR IS EXPRESSED ONCE, IN THE PATTERN, and it used to be expressed
    twice. Both patterns carry a leading ``^`` and both were applied with
    ``re.match``, which anchors at the start on its own, so the ``^`` was
    unkillable: delete it and nothing anywhere behaves differently, which is a
    guard that reads as load-bearing and is not. ``re.search`` under a pattern
    that says ``^`` is the same operation with the rule stated in one place, and
    a value that merely MENTIONS ``file://`` or a drive letter now costs a test
    rather than nothing.
    """
    text = str(recorded).strip()
    return bool(_DRIVE_LETTER.search(text)) or bool(_FILE_LOCATION.search(text))


def _anchor_text(value: str) -> str:
    """ONE spelling for an anchor, whichever side of the map it arrived from.

    THE SEAM THE 144-FILE INCIDENT IS ABOUT, in the one place this module builds
    a path string from two sources. ``PrefixRule`` NFC folds and right-strips its
    target in ``__post_init__``; the library root arrives raw from configuration.
    Without this, one library root spelled in NFD and one rule target spelled in
    NFC are two cache keys and two stats for one directory, and worse, two
    directories that ARE one compare as different. macOS hides it, because APFS
    and HFS+ normalize on lookup and both spellings open the same inode. An ext4
    or exFAT root does not, and exFAT is what an external music drive is usually
    formatted as, which is exactly the disk a prefix rule exists to reach.

    An anchor that strips to nothing is the filesystem root. ``PrefixRule`` right
    strips its target, so a rule mapping onto ``/`` stores the empty string, and
    a resolved path under it is genuinely anchored at ``/`` rather than nowhere.
    Returning the empty string would stat ``""``, fail, and refuse the run naming
    an anchor the user cannot read.
    """
    return locations.norm_for_compare(value).rstrip("/") or "/"


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
        return _anchor_text(str(root))
    if resolved.resolution is locations.Resolution.REMAPPED and resolved.rule_index is not None:
        return _anchor_text(prefix_map[resolved.rule_index].target)
    return None  # pragma: no cover - the resolver produces a path no other way


class _Anchors:
    """Whether each anchor is there, asked ONCE per anchor rather than per row.

    A library resolves through a handful of anchors and holds thousands of rows,
    so the naive shape is one extra system call per row for an answer that cannot
    differ between them. Caching also makes the answer CONSISTENT within a run: a
    volume that unmounts halfway through must not make the first half of the
    reference set mean something different from the second half.

    **THE CACHE HAS A DIRECTION AND THE UNSAFE ONE IS "PRESENT".** Eject a volume
    BEFORE its first row and every row through it is unanchored and the run
    refuses, which is right. Eject it AFTER and the cached "present" stands, so
    the remaining rows through it answer ``FileNotFoundError``, land in
    ``missing``, and quietly shrink the very set the proof is made of. Saying
    which half wins is not enough, because the half that wins is the wrong one.
    So :meth:`changed` re-asks at the end and the caller refuses on any anchor
    whose answer moved. One extra stat per ANCHOR, not per row, buys the property
    that the reference set describes one filesystem rather than two.
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
        """Anchors whose answer is no longer the answer this run was built on.

        Asked once, at the end, over the anchors that were actually consulted. It
        catches the mount that went away mid-pass in the direction that matters
        and the one that arrived in the direction that does not, and it reports
        both, because either one means the set was assembled against a filesystem
        that no longer exists and neither is a state to guess about.
        """
        return tuple(
            anchor for anchor, held in self._known.items() if self._ask(anchor) != held
        )


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

    THAT EXCUSAL IS SPLIT IN TWO, and :func:`_unnameable` is the half that
    refuses. The argument above holds for a row referencing no file and for
    nothing else, and the resolver answers ``NOT_A_PATH`` for a drive-letter path
    and a ``file://`` location as readily as for a streaming pseudo-location. A
    row of the second kind names a real file, so excusing it removes real
    evidence from the proof rather than declining to add irrelevant evidence.
    """
    found: dict[FileIdentity, list[str]] = {}
    unmapped: list[str] = []
    uninspectable: list[str] = []
    missing: list[str] = []
    unanchored: list[str] = []
    not_a_path: list[str] = []
    unnameable: list[str] = []
    dead: dict[str, None] = {}
    # Per anchor rather than per run, because the global tally is exactly what
    # the all-or-nothing warning got wrong: one unrelated active row that
    # resolves anywhere in the library made the whole set look productive while
    # every row through one rule answered nothing.
    indexed_under: dict[str, int] = {}
    missing_under: dict[str, int] = {}
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
            if _unnameable(row.recorded):
                unnameable.append(row.content_id)
            else:
                not_a_path.append(row.content_id)
            continue
        if resolved.path is None:
            unmapped.append(row.content_id)
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
        suspect_anchors=tuple(
            anchor for anchor in missing_under if not indexed_under.get(anchor)
        ),
        unstable_anchors=anchors.changed(),
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
    if references.unnameable:
        # ITS OWN SENTENCE AND ITS OWN STEPS, because nothing the user can mount
        # or remap answers it. The rows are readable, they name real files, and
        # this build cannot turn the spelling into a path, so the honest report
        # is that the proof would be built out of nothing rather than out of
        # less. Named before the generic sentence below for the same reason the
        # dead anchors are: it is the shape a person can act on.
        raise refuse(
            "deletion-reference-set-incomplete",
            f"{len(references.unnameable)} active rows record a location that is "
            f"a path this build cannot name, a drive letter or a file:// "
            f"location rather than an absolute path; those rows were excused "
            f"from the proof as though they referenced no file at all, so a "
            f"removed file would be shown unreferenced against a reference set "
            f"they are missing from; nothing is offered this run",
            steps=(
                "run this on the machine and platform the library was recorded "
                "on, or report this with the recorded locations below, because "
                "no volume prefix rule can spell a path this build cannot read",
            ),
            scope=Scope.RUN,
            origin=("deletion.candidates",),
            detail={
                **references.counts,
                "unnameable_rows": list(references.unnameable[:20]),
            },
        )
    if references.unstable_anchors:
        # ITS OWN SENTENCE, because the act is different from every other way
        # this set comes up short. Nothing is misconfigured and no row is at
        # fault: a volume appeared or went away while the walk was running, so
        # half of the set describes one filesystem and half describes another,
        # and the answer is to run it again rather than to repair anything.
        raise refuse(
            "deletion-reference-set-incomplete",
            f"the directory at {', '.join(references.unstable_anchors)} was "
            f"there for part of this run and not for the rest, so the reference "
            f"set was assembled against two different filesystems and proves "
            f"nothing about either; nothing is offered this run",
            steps=(
                "leave the library volume and every mapped volume mounted, then "
                "run this again",
            ),
            scope=Scope.RUN,
            origin=("deletion.candidates",),
            detail={**references.counts, "unstable_anchors": list(references.unstable_anchors)},
        )
    raise refuse(
        "deletion-reference-set-incomplete",
        f"{len(references.unmapped)} active rows record a location this machine "
        f"cannot resolve, {len(references.uninspectable)} resolve to files "
        f"that could not be inspected, and {anchored}so the proof that a removed "
        f"file is unreferenced would be a proof about the rows that happened to "
        f"answer; nothing is offered this run",
        # THE STEPS ARE SPELLED OUT FOR THE ANCHOR CASE because "run doctor" on
        # its own is not service here. The commonest way to meet this refusal is
        # a two drive library with the second drive unplugged, and that person is
        # one act away from a run that works. Saying which act is the difference
        # between a refusal and a wall.
        steps=(
            (
                f"mount the volume holding {', '.join(references.dead_anchors)}, "
                f"or correct the volume prefix rule that points at it, then run "
                f"this again"
            ),
        )
        if references.dead_anchors
        else (),
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
    #: The directory CONFIGURATION named for this row, carried out only when the
    #: file was not there, because that is the only answer whose meaning depends
    #: on it. A caller holding a ``GONE`` row cannot otherwise ask whether the
    #: absence was a statement about the file or about the directory it hangs
    #: off, and the two are the difference between a deletion and an unmounted
    #: drive: see ``ReferenceSet.suspect_anchors``, which is the answer, and
    #: ``run._the_anchor_proved_nothing``, which is the caller that needs it.
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

    **AND THE CACHE IS RE-ASKED AT THE END, FOR THE SAME REASON AND WITH MORE AT
    STAKE.** :class:`_Anchors` says which way its cache is unsafe: eject a volume
    BEFORE its first row and every row through it refuses, which is right, but
    eject it AFTER and the cached "present" stands. ``reference_set`` re-asks and
    refuses on any anchor whose answer moved, because "the half that wins is the
    wrong one". This walk had the identical cache and never asked, so ejecting a
    volume partway through it left every remaining row through that anchor
    reading ``GONE`` off a stale ``present``. ``GONE`` is the single member of
    :data:`HANDLED`, so those rows are RETIRED: the watermark passes over them,
    nobody is ever asked, and remounting the volume brings none of them back.
    That is the paragraph above happening to a correct configuration, and an
    external drive dropping mid-walk is an ordinary afternoon rather than a
    curiosity.

    **AN ANCHOR THAT IS THERE IS NOT PROOF, AND THIS FUNCTION DOES NOT PRETEND
    OTHERWISE ANY MORE.** The test above is existence, so an EMPTY directory
    standing where a volume mounts passes it, and macOS leaves exactly that
    behind after an unclean eject, as does anything at all that writes to the
    path while the drive is detached. Every removed row through it then reads
    ``GONE`` off a directory holding nothing. What this function does about that
    is CARRY THE ANCHOR OUT on the answer, because the caller is the only place
    the counter-evidence exists: ``reference_set`` has already walked the ACTIVE
    rows through the same anchor and knows whether any of them found a file
    there. A row is answered here and the answer is qualified there, rather than
    this walk taking a second opinion on a question the reference set has
    already settled.
    """
    out: list[Candidate] = []
    rules = list(prefix_map)
    anchors = _Anchors(stat)
    for row in removed:
        # IDENTIFIABILITY IS ASKED FIRST, BEFORE THE DECLINE. It used to be
        # asked second, and the decline predicate derives a suppression
        # identifier from the row, so a row that cannot be addressed at all
        # raised inside the question about whether somebody had already answered
        # for it. Neither question touches a file, so the order costs nothing and
        # the only thing it changes is which category an unaddressable row that
        # somebody once declined is reported under, where UNIDENTIFIABLE is the
        # more useful answer anyway.
        if not identifiable(row):
            out.append(
                Candidate(
                    row=row,
                    category=Category.UNIDENTIFIABLE,
                    problem=(
                        "the row cannot be identified: R36's tombstone needs an "
                        "artist or a title to name the version this deletion "
                        "suppresses, and the review item needs the row's own "
                        "identifier to be answerable"
                    ),
                )
            )
            continue
        if declined(row):
            out.append(Candidate(row=row, category=Category.DECLINED))
            continue
        if ambiguous(row):
            out.append(
                Candidate(
                    row=row,
                    category=Category.AMBIGUOUS_VERSION,
                    problem=(
                        "another removed row produces the same version identity "
                        "as this one and carries a different ISRC, so the two are "
                        "two recordings rather than one filed twice; a tombstone "
                        "for either would suppress the other"
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
                out.append(
                    Candidate(
                        row=row,
                        category=Category.GONE,
                        resolved=resolved.path,
                        anchor=anchor,
                    )
                )
            else:
                out.append(
                    Candidate(
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
    moved = anchors.changed()
    if moved:
        raise refuse(
            "deletion-evidence-incomplete",
            f"the directory at {', '.join(moved)} was there for part of this walk "
            f"and not for the rest, so the removals answered before it moved and "
            f"the ones answered after describe two different filesystems; a row "
            f"answered off the stale half reads as already deleted, which is "
            f"finished business, and the watermark would retire it without "
            f"anybody being asked",
            steps=(
                "leave the library volume and every mapped volume mounted, then "
                "run this again",
            ),
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
    """Re-run every assertion THAT CAN CHANGE for ONE candidate, before its move.

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

    **TWO OF THE CATEGORISER'S PREDICATES ARE NOT ACCEPTED HERE, AND THE ABSENCE
    IS A DECISION RATHER THAN A GAP.** ``identifiable`` and ``ambiguous`` were
    both accepted and both forwarded, and deleting either one at the only call
    site killed ZERO tests, measured. Neither could measure otherwise. Both
    answers are functions of a row and of the whole collection walk the caller
    has just redone, so neither changes between the plan and the move the way a
    file's size or a decline does; and the caller only ever re-checks a candidate
    the rebuilt plan called DELETABLE, which a row failing either predicate never
    is. A parameter that cannot alter an answer is a guard that reads as
    load-bearing and is not.

    ``declined`` IS accepted, because a decline is a store read and the caller
    takes a fresh one after the plan, so it is the one predicate here that can
    genuinely have changed.
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
